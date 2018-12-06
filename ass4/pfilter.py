import socket, sys
import binascii
from base64 import b64encode, b64decode
import binascii
from struct import *

# Packet reading from https://www.binarytides.com/python-packet-sniffer-code-linux/


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

# Read in packet file
with open(packetFile, mode='rb') as f: 
    packet = f.read() # read as list of lines
f.close()

# PacketData
packetProtocol = ""
packetSourceIP = ""
packetSourcePort = ""
packetDestIP = ""
packetDestPort = ""

# Parse the packet and populate variables
ip_header = packet[0:20]

#now unpack them :)
iph = unpack('!BBHHHBBH4s4s' , ip_header)

version_ihl = iph[0]
version = version_ihl >> 4
ihl = version_ihl & 0xF

iph_length = ihl * 4

ttl = iph[5]
protocol = iph[6]
s_addr = socket.inet_ntoa(iph[8]);
d_addr = socket.inet_ntoa(iph[9]);

# print 'Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(d_addr)

#TCP protocol
if protocol == 6 :
    t = iph_length
    tcp_header = packet[t:t+20]

    #now unpack them :)
    tcph = unpack('!HHLLBBHHH' , tcp_header)
    
    source_port = tcph[0]
    dest_port = tcph[1]
    sequence = tcph[2]
    acknowledgement = tcph[3]
    doff_reserved = tcph[4]
    tcph_length = doff_reserved >> 4
    
    # print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length)
    
    h_size = iph_length + tcph_length * 4
    data_size = len(packet) - h_size
    
    packetProtocol = "tcp"
    packetSourceIP = str(s_addr)
    packetSourcePort = str(source_port)
    packetDestIP = str(d_addr)
    packetDestPort = str(dest_port)

#UDP packets
elif protocol == 17 :
    u = iph_length 
    udph_length = 8
    udp_header = packet[u:u+8]

    #now unpack them :)
    udph = unpack('!HHHH' , udp_header)
    
    source_port = udph[0]
    dest_port = udph[1]
    length = udph[2]
    checksum = udph[3]
    
    # print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Length : ' + str(length) + ' Checksum : ' + str(checksum)
    
    h_size = iph_length + udph_length
    data_size = len(packet) - h_size
    
    packetProtocol = "udp"
    packetSourceIP = str(s_addr)
    packetSourcePort = str(source_port)
    packetDestIP = str(d_addr)
    packetDestPort = str(dest_port)


# print("Protocol: " + packetProtocol)
# print("sourceIP: " + packetSourceIP)
# print("source Port: " + packetSourcePort)
# print("destIP: " + packetDestIP)
# print("destPort: " + packetDestPort + "\n\n")

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


    # print("Filter Type: " + filterType)
    # print("Protocol: " + protocol)
    # print("sourceIP: " + sourceIP)
    # print("source Port: " + sourcePort)
    # print("destIP: " + destIP)
    # print("destPort: " + destPort + "\n\n")

    # Check if the Protocol matches (ie tcp == tcp)
    if (protocol != packetProtocol):
        continue
    
    # check if srcip matches
    if (sourceIP != packetSourceIP):
        # check if last bit of IP is wild card
        # get last bit of IP
        lastBitRule = sourceIP.split(".")[3]
        LastBitPacket = packetSourceIP.split(".")[3]
        #print(lastBitRule, LastBitPacket)
        if not ("*" in lastBitRule and sourceIP.split(".")[0] == packetSourceIP.split(".")[0] and sourceIP.split(".")[1] == packetSourceIP.split(".")[1] and sourceIP.split(".")[2] == packetSourceIP.split(".")[2]):
            continue

    # check if srcPort matches 
    if (sourcePort != packetSourcePort):
        # check if port is wild card
        if  "*" not in sourcePort:
            continue

    # check if dstip matches 
    if (destIP != packetDestIP):
        # check if last bit of IP is wild card
        # get last bit of IP
        lastBitRule = destIP.split(".")[3]
        LastBitPacket = packetDestIP.split(".")[3]
        #print(lastBitRule, LastBitPacket)
        if not ("*" in lastBitRule and destIP.split(".")[0] == packetDestIP.split(".")[0] and destIP.split(".")[1] == packetDestIP.split(".")[1] and destIP.split(".")[2] == packetDestIP.split(".")[2]):
            continue

    # Check if dstport matches
    if (destPort != packetDestPort):
        # check if port is wild card
        if  "*" not in destPort:
            continue

    # Perfect match: Handle Allow or Deny
    print(filterType + "\n")
    exit(0)

# exit loop and no matching rule was found
print("unspecified\n")
exit(0)

# [allow|deny] [tcp|udp] srcip:srcport -> dstip:dstport

