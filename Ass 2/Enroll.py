# Enroll Program
import sys
# make sure UserName isnt in the DB
# Make sure that Password isnt in the DB
# Make sure Password isnt in wrong format



# *** START *** #
if (len(sys.argv) < 3):
    print ("Rejected")

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
        sys.exit()
    
    # Check if password with numbers at start striped is in word list
    if (line.lower() == password.lstrip('0123456789')):
        print ("Reject Start Numbers")
        sys.exit()

    # Check if password with numbers at end striped is in word list
    if (line.lower() == password.rstrip('0123456789')):
        print ("Reject end numbers")
        sys.exit()




