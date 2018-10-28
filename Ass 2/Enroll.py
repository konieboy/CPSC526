# Enroll Program
import sys
from argon2 import PasswordHasher
import json
# make sure UserName isnt in the DB
# Make sure Password isnt in wrong format


ph = PasswordHasher()


# *** START *** #
if (len(sys.argv) < 3):
    print ("Rejected arg length")
    sys.exit(-1)

userName = sys.argv[1]
password = sys.argv[2]

# Read word file into list
lines = [line.rstrip('\n') for line in open('words.txt')]

# Check if password is just numbers
if ("" == password.rstrip('0123456789')):
    print ("Reject Numbers")

    sys.exit()

for line in lines:
    # Check if password is in word list
    if (line.lower() == password.lower()):
        print ("Reject In list")
        sys.exit(-1)
    
    # Check if password with numbers at start striped is in word list
    if (line.lower() == password.lstrip('0123456789')):
        print ("Reject Start Numbers")
        sys.exit(-1)

    # Check if password with numbers at end striped is in word list
    if (line.lower() == password.rstrip('0123456789')):
        print ("Reject end numbers")
        sys.exit(-1)

# Check if username is in file
with open('data.json', encoding='utf-8') as data_file:
    data = json.loads(data_file.read())
i = 0
while (i < (len(data["database"]))):

    #print (data["database"][i]["username"])
    if (userName == data["database"][i]["username"]):
        print ("Reject In Database")
        sys.exit(-1)

    i += 1


# Note, the library I am using implements hashing by default

# Everything is good! send
passHash = ph.hash(password)

data["database"].append({'username':userName, 'hash':passHash})

with open("data.json", "w") as write_file:
    json.dump(data, write_file)


# verify test
print (ph.verify(passHash, password))
sys.exit(0)



# Test ideas
# hash1 = ph.hash("s3kr3tp4ssw0rd")
# hash2 = ph.hash("s3kr3tp4ssw0rd")

# print (hash1 == hash2)