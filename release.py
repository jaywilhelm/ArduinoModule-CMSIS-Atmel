import tarfile
import os
import glob

VERSION = "1.0.0"
ROOT_PROJECT_DIRNAME = "CMSIS-Atmel"

fileNames = os.listdir(ROOT_PROJECT_DIRNAME)

fileList = glob.glob("*.tar.bz2")
print(fileList)
for efile in fileList:
    try:
        print("Removing file: " + efile)
        os.remove(efile)
    except:
        print("could not delete: " + efile)

print(fileNames)

tar = tarfile.open(ROOT_PROJECT_DIRNAME+VERSION+".tar.bz2", "w:bz2")
for name in fileNames:
    tar.add(ROOT_PROJECT_DIRNAME+"/" + name)
tar.close()


import hashlib
BLOCKSIZE = 65536
hasher = hashlib.sha256()
with open(ROOT_PROJECT_DIRNAME+VERSION+'.tar.bz2', 'rb') as afile:
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(BLOCKSIZE)
checksum = hasher.hexdigest()
print(checksum)

fileSize = os.path.getsize(ROOT_PROJECT_DIRNAME+VERSION+'.tar.bz2')
print(fileSize)


jtemp = open("jsontemplate.txt","r")
jtempstr = jtemp.read()
jtemp.close()
URL = "https://github.com/jaywilhelm/ArduinoModule-CMSIS-Atmel/releases/download/etag-v"+VERSION+"/"+ROOT_PROJECT_DIRNAME+VERSION+".tar.bz2"
FILENAME = ROOT_PROJECT_DIRNAME+VERSION+".tar.bz2"

jtempstr = jtempstr.replace("$URL$",URL)
jtempstr = jtempstr.replace("$FILENAME$",FILENAME)
jtempstr = jtempstr.replace("$VERSION$",checksum)
jtempstr = jtempstr.replace("$SHA$",checksum)
jtempstr = jtempstr.replace("$SIZE$",str(fileSize) )


print(jtempstr)


f= open("index.json","w+")
f.write(jtempstr)
f.close()
