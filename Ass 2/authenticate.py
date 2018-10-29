# Authenticate Program
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

ph = PasswordHasher()

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


# *** START *** #
if not (len(sys.argv) == 3):
    print ("Rejected\n")
    sys.exit(-1)

userName = sys.argv[1]
password = sys.argv[2]

with open('data.json', encoding='utf-8') as data_file:
    data = json.loads(data_file.read())

usernameFound = False
i = 0
while (i < (len(data["database"]))):

    #print (data["database"][i]["username"])
    if (userName == data["database"][i]["username"]):
        print ("Found user in database")
        usernameFound = True
        break
    i += 1

if not (usernameFound):
    print ("No username In Database")
    sys.exit(-1)

# Check that hashed password works
hashedPass = data["database"][i]["hash"]
try:
  ph.verify(hashedPass, password)
except: 
    print("Access Denied\n")
    sys.exit(-1) 

if (ph.verify(hashedPass, password)):
    print("Access Granted\n")
    sys.exit(0)


