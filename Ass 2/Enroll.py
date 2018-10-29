# Enroll Program
# Libraries used: 
# PyCryptodome for AES encryption
# argon2_cffi used for hasing in argon2 https://pypi.org/project/argon2_cffi/

import sys
from argon2 import PasswordHasher
import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import Padding
from base64 import b64encode, b64decode

#-- Global Vars --#
ph = PasswordHasher()
mode = AES.MODE_CBC
bs = AES.block_size
# The IV and Key would be shared ahead of time
key = "wOSAAiJgPNktvoZ7draMW1TZPYCip2IM".encode('utf-8') # Key randomly generated from https://randomkeygen.com/
iv = key[8:bs+8]

def saveEncryptedData(plaintext):
    body = Padding.pad(json.dumps(plaintext).encode('utf-8'), bs)
    cipher = AES.new(key, mode, iv)
    cipherText = b64encode(cipher.encrypt(body)).decode('utf-8')

    dataFile = open("encryptedData", "w")
    dataFile.write(cipherText)
    dataFile.close()

def getDatabaseInPlaintext():
    # Open and read encrypted data
    f = open("encryptedData","r")
    encyptedData = f.read()
    f.close()

    encyptedData = b64decode(encyptedData.encode('utf-8'))
    cipher = AES.new(key, mode, iv)
    plainText = Padding.unpad(cipher.decrypt(encyptedData), bs).decode('utf-8')
    return plainText

def filterWeakPasswords(password):
    # Read word file into list
    lines = [line.rstrip('\n') for line in open('words.txt')]

    # Check if password is just numbers
    if ("" == password.rstrip('0123456789')):
        print("Rejected\n")
        sys.exit(-1)

    for line in lines:
        # Check if password is in word list
        if (line.lower() == password.lower()):
            print("Rejected\n")
            sys.exit(-1)
        
        # Check if password with numbers at start striped is in word list
        if (line.lower() == password.lstrip('0123456789')):
            print("Rejected\n")
            sys.exit(-1)

        # Check if password with numbers at end striped is in word list
        if (line.lower() == password.rstrip('0123456789')):
            print("Rejected\n")
            sys.exit(-1)

def checkForExistingUser(userName):
    data = json.loads(getDatabaseInPlaintext())
    print (data)
    i = 0
    while (i < (len(data["database"]))):
        if (userName == data["database"][i]["username"]):
            print("Rejected\n")
            sys.exit(-1)

        i += 1
    # REMNANT REMOVAL - Delete the unencrypted data once we no longer need it
    del data 
    

def addUser(userName, password): 
    data = json.loads(getDatabaseInPlaintext())   
    passHash = ph.hash(password)
    data["database"].append({'username':userName, 'hash':passHash})
    saveEncryptedData(data)
    # REMNANT REMOVAL - Delete the unencrypted data once we no longer need it
    del data

# *** START *** #
 # Make sure that
if not (len(sys.argv) == 3):
    print("Rejected\n")
    sys.exit(-1)

userName = sys.argv[1]
password = sys.argv[2]

# Make sure that the password is strong
filterWeakPasswords(password)

# Make sure that Username isnt already in the file
checkForExistingUser(userName)

# !!!Note!!!, the library I am using implements salting of the hash by default
addUser(userName, password)

# User added to system
print ("Accepted\n")
sys.exit(0)

