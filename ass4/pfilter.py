import sys
# https://www.binarytides.com/python-packet-sniffer-code-linux/
# *** START *** #
## Take in arguments ##
if not (len(sys.argv) == 3):
    print("Improper arguments\n")
    sys.exit(-1)

rulesFile = sys.argv[1]
packetFile = sys.argv[2]


#1. Rules File -- Rules to follow
with open(rulesFile) as f: 
    rules = f.readlines() # read as list of lines
f.close()

print (rules)

#2. Packet -- Packet to examine
with open(packetFile) as f: 
    packet = f.readlines() # read as list of lines
f.close()

print (packet)

## For each 

## Loop through each rule and match with packet ##
for rule in rules:
    # Spilt rule into sections
    splitRules = rule.split()

    filterType = "unspecified"
    if (splitRules[0] == "allow"):
        filterType = "allow"
    elif (splitRules[0] == "deny"):
        filterType = "deny"
    else:
        filterType = "unspecified"

    protocol = splitRules[1]

    destPort = splitRules[4].split(":")[1]
    destIP = splitRules[4].split(":")[0]
    sourcePort = splitRules[2].split(":")[1]
    sourceIP = splitRules[2].split(":")[0]

    print("Filter Type: " + filterType)
    print("Protocol: " + protocol)
    print("sourceIP: " + sourceIP)
    print("source Port: " + sourcePort)
    print("destIP: " + destIP)
    print("destPort: " + destPort + "\n\n")

    # Check if the Protocol matches

    # Check if dstport matches

    # check if srcport matches

    # check if srcip matches 

    # check if dstip matches 
    

    # !!! ONMatch: Handle Allow or Deny


# [allow|deny] [tcp|udp] srcip:srcport -> dstip:dstport

# 

# print
# print("allow\n")
# print("deny\n")
# print("unspecified\n")
