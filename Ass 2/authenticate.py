# authenticate
import sys
from argon2 import PasswordHasher
import json

ph = PasswordHasher()

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


