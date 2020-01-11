# Technical Demonstration

### Video Demonstration:
- https://www.youtube.com/watch?v=q7n0kfBVM6U&feature=youtu.be

#### WARNING: THIS SOFTWARE IS MEANT FOR EDUCATIONAL AND DEMONSTRATION PURPOSES ONLY. ONLY RUN THIS SOFTWARE ON A VIRTUAL MACHINE THAT DOES NOT CONTAIN ANY SENSITIVE OR MEANINGFUL DATA. *USE AT YOUR OWN RISK.*

Start by cloning the repository:
```console
user@host:~$ git clone https://github.com/cdalseth/techdemo.git
```
For this demo to work, you need the *pycrypto, Tkinter* and *psutil* libraries installed. To install them, you can just run *GetLibs.sh*:
```console
user@host:~/techdemo$ sh GetLibs.sh
```
You can then run **GenR-ware.py** from inside *techdemo*:
```console
user@host:~/techdemo$ python GenR-ware.py
```
It will prompt you to enter a name of a fictional target the ransomware will be sent to (if you already have a target by that name, it will ask if you're sure you want to regenerate the keys).

There should now be a *Targets* directory in *techdemo*. If you change into that directory, a folder for your target has been created. All future targets will appear in this directory as well. Navigating into one of those directories will provide you with the RSA private key and RSA public key in .txt files. Going into the *RWPackage* folder will provide you with the ransomware and decryption programs named **R-ware.py** and **R-Decryption.py**, respectively. Before running these, I suggest populating the folders inside the home directory with some sub-directories and files so you can see what happens. 

__NOTE: If you have *techdemo* in your Home directory, it will not be an issue as long as you don't change the name of the folder. The ransomware will intentionally pass over it.__ 

You can now run the ransomware:
```console
user@host:~/techdemo/Targets/<-TARGET1->/RWPackage$ python R-ware.py
```
You'll be greeted with a ransom note that you cannot close and a browser window at Coinbase. When you try to close the window it will just open a new tab for Coinbase. All of your files in your Home directory and it's subdirectories have now been encrypted using AES encryption. You'll also see a folder on the desktop named *RANSOM_INFO* which contains your encrypted AES key and a copy of the ransom note. To decrypt all of your files you can either open a new bash window, or you can kill the ransomware process in the current window by using *CTRL+c* and moving the window. 

To decrypt everything, run:
```console
user@host:~/techdemo/Targets/<-TARGET1->/RWPackage$ python R-Decryption.py
```

And that's it! You should be back to normal.

#### WARNING: THIS SOFTWARE IS MEANT FOR EDUCATIONAL AND DEMONSTRATION PURPOSES ONLY. ONLY RUN THIS SOFTWARE ON A VIRTUAL MACHINE THAT DOES NOT CONTAIN ANY SENSITIVE OR MEANINGFUL DATA. *USE AT YOUR OWN RISK.*
