# Enroll Program
import sys
from argon2 import PasswordHasher
import json

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import Padding
from base64 import b64encode, b64decode

# Global Vars
ph = PasswordHasher()
mode = AES.MODE_CBC
bs = AES.block_size
key = "wOSAAiJgPNktvoZ7draMW1TZPYCip2IM".encode('utf-8')
iv = key[8:bs+8]

def saveEncryptedData(plaintext):
    body = Padding.pad(json.dumps(plaintext).encode('utf-8'), bs)
    cipher = AES.new(key, mode, iv)
    #key = b64encode(key).decode('utf-8')
    cipherText = b64encode(cipher.encrypt(body)).decode('utf-8')

    dataFile = open("encryptedData", "w")
    dataFile.write(cipherText)
    dataFile.close()

    # return cipherText

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
    # with open('data.json', encoding='utf-8') as data_file:
    #     data = json.loads(data_file.read())
    # data_file.close()
    data = json.loads(getDatabaseInPlaintext())
    print (data)
    i = 0
    while (i < (len(data["database"]))):
        #print (data["database"][i]["username"])
        if (userName == data["database"][i]["username"]):
            print("Rejected\n")
            sys.exit(-1)

        i += 1
    # REMNANT REMOVAL - Delete the unencrypted data one we no longer need it
    del data 
    

def addUser(userName, password): 
    # with open('data.json', encoding='utf-8') as data_file:
    #     data = json.loads(data_file.read())
    # data_file.close()
    data = json.loads(getDatabaseInPlaintext())   
    passHash = ph.hash(password)
    data["database"].append({'username':userName, 'hash':passHash})

    saveEncryptedData(data)
    # with open("data.json", "w") as write_file:
    #     json.dump(data, write_file)
    # write_file.close()    

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

# # with open("data.json", "w") as write_file:
# #     json.dump(data, write_file)

# # Key randomly generated from https://randomkeygen.com/

# key = "wOSAAiJgPNktvoZ7draMW1TZPYCip2IM".encode('utf-8')
# body = Padding.pad(json.dumps(data).encode('utf-8'), bs)
# iv = key[8:bs+8]

# cipher = AES.new(key, mode, iv)
# #key = b64encode(key).decode('utf-8')
# body = b64encode(cipher.encrypt(body)).decode('utf-8')
# #iv = b64encode(iv).decode('utf-8')

# # result = "%s.%s.%s" % (key, body, iv)
# # print(result)

# # with open("encryptedData.bin", "w") as write_file:
# #    write(body, write_file)
   
# dataFile = open("encryptedData.txt", "w")
# dataFile.write(body)
# dataFile.close()

# # decrypting
# # key, body, iv = result.split(".")
# f = open("encryptedData.txt","r")
# encyptedData = f.read()
# f.close()

    
# #print (encyptedData)
# #print (body)

# #key = b64decode(key.encode('utf-8'))
# encyptedData = b64decode(encyptedData.encode('utf-8'))
# #iv = b64decode(iv.encode('utf-8'))

# cipher = AES.new(key, mode, iv)

# plainText = Padding.unpad(cipher.decrypt(encyptedData), bs).decode('utf-8')

# print (plainText)
