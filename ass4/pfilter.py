import socket, sys
import binascii
from base64 import b64encode, b64decode
import binascii
from struct import *


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

#print (rules)

#2. Packet -- Packet to examine
# with open(packetFile, mode='rb') as f: 
#     packet = f.read() # read as list of lines
# f.close()

# struct.unpack("iiiii", packet[:20])
# struct.unpack("i" * ((len(packet) -24) // 4), packet[20:-4])
# struct.unpack("i", packet[-4:])

# with open(packetFile, "rb") as binaryfile :
#     packet = bytearray(binaryfile.read())


# bstr = packet.replace(' ', '')
# packet = '%0*X' % ((len(packet) + 3) // 4, int(packet, 2))


# binFile = open(packetFile,'rb')
# binaryData = binFile.read(8)
# packet=  binascii.hexlify(binaryData)

# 	ip_header = packet[0:20]
	
# 	#now unpack them :)
# 	iph = unpack('!BBHHHBBH4s4s' , ip_header)


# Read in packet file
with open(packetFile, mode='rb') as f: 
    packet = f.read() # read as list of lines
f.close()

ip_header = packet[0:20]
iph = unpack('!BBHHHBBH4s4s' , ip_header)

version_ihl = iph[0]
version = version_ihl >> 4
ihl = version_ihl & 0xF

iph_length = ihl * 4

ttl = iph[5]
protocol = iph[6]
s_addr = socket.inet_ntoa(iph[8]);
d_addr = socket.inet_ntoa(iph[9]);

print 'Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(d_addr)

tcp_header = packet[iph_length:iph_length+20]

#now unpack them :)
tcph = unpack('!HHLLBBHHH' , tcp_header)

source_port = tcph[0]
dest_port = tcph[1]
sequence = tcph[2]
acknowledgement = tcph[3]
doff_reserved = tcph[4]
tcph_length = doff_reserved >> 4

print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length)


exit()

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
