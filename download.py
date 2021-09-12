#coding=utf-8
import os
import sys
import base64
import requests

from os import path
from Crypto.Cipher import AES

from subprocess import Popen

key = b''
base64key = base64.b64encode(key)

def main():
    if len(sys.argv) != 3:
        return

    url = sys.argv[1]
    name = sys.argv[2]

    cacheDir = name + '_tmp'
    m3u8file = path.join(cacheDir, name + ".m3u8")

    saveName = name
    baseUrl = url[:url.rfind('/')+1]

    commandLine = 'cli \"%s\" --workDir %s --saveName %s --useKeyBase64 %s' % \
        (path.abspath(m3u8file), path.abspath(cacheDir), saveName, base64key)

    print("url:", url, "name:", name)

    r = requests.get(sys.argv[1])
    if r.status_code != 200:
        print("request return:", r.status_code)
        return

    encData = r.content

    cipher = AES.new(key, AES.MODE_ECB)
    decData = cipher.decrypt(encData)
    data = decData

    def m3u8_abspath(baseUrl, str):
        lines = str.splitlines()
        for i in range(len(lines)):
            if lines[i].find(b'#EXTINF:') != -1:
                lines[i+1] = bytes(baseUrl, encoding='utf-8') + lines[i+1]
        return b'\n'.join(lines)

    data = m3u8_abspath(baseUrl, data)

    if not os.path.exists(cacheDir):
        os.mkdir(cacheDir)

    with open(m3u8file, 'wb') as f:
        f.write(data)

    #print(commandLine)
    os.system(commandLine)
    

if __name__ == '__main__':
    main()
    print("done.")