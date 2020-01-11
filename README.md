# Technical Demonstration

#### WARNING: THIS SOFTWARE IS MEANT FOR EDUCATIONAL AND DEMONSTRATION PURPOSES ONLY. ONLY RUN THIS SOFTWARE IN A VIRTUAL MACHINE THAT DOES NOT HAVE SENSITIVE OR MEANINGFUL DATA.

Start by cloning the repository:
```console
user@host:~$ git clone  
```
For this demo to work, you need the *urllib2, pycrypto, Tkinter* and *psutil* libraries. To install them, you can just run *GetLibs.sh*:
```console
user@host:~/techdemo$ sh GetLibs.sh
```
You can then run GenR-ware.py from inside *techdemo*:
```console
user@host:~/techdemo$ python GenR-ware.py
```
It will prompt you to enter a name of a (hypothetical) target the ransomware will be sent to (if you already have a target by that name, it will ask if you're sure you want to regenerate the keys).

There should now be a *Targets* directory in *techdemo*. If you change into that directory, a folder for your target has been created. All future targets will appear in this directory as well. Navigating into one of those directories will provide you with the RSA private key and RSA public key in .txt files. Going into the *RWPackage* folder will provide you with the ransomware and decryption programs named *R-ware.py* and *R-Decryption.py*, respectively. Before running these, I suggest populating the folders inside the home directory with some sub-directories and files so you can see what is happening
