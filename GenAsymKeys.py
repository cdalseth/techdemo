import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast
import os
from os.path import expanduser
import sys
import glob

#adapted from answers at
#https://stackoverflow.com/questions/30056762/rsa-encryption-and-decryption-in-python
#https://stackoverflow.com/questions/47522009/make-directory-in-python

class GenAsymKeys:
    def __init__(self, path, name):

        file_path = path

        #random_generator = Random.new().read
        key = RSA.generate(1024) #generate pub and priv key

        #checking to see if the path doesn't already exist. otherwise make it
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        else:
            valid = 0
            while valid == 0:
                answer = raw_input("\nThat person is already on the list, are you sure you want to create new keys? [y/n]: ")
                if answer == 'y' or answer == 'Y':
                    valid = 1
                elif answer == 'n' or answer == 'N':
                    sys.exit()
                else:
                    print("\nEnter either y or n")

        public_key = key.publickey()

        private_key_str = key.exportKey("PEM")
        public_key_str = key.publickey().exportKey("PEM")

        print("\n\n" + private_key_str)
        print("\n" + public_key_str)

        f = open (file_path + '/publicKey.txt', 'w')
        f.write(public_key_str) #write ciphertext to file
        f.close()

        f = open (file_path + '/privateKey.txt', 'w')
        f.write(private_key_str) #write ciphertext to file
        f.close()

        rw_path = file_path + '/RWPackage'

        print("\n\nKEYS SUCCESSFULLY GENERATED FOR " + name + "\n")
        print(rw_path + "\n")
