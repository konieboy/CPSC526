from collections import Counter
from itertools import cycle
import string
import re

# Read chapter 8
f = open("ulysses.txt","r", encoding='utf8')
contents = f.read()

#contents = contents.replace('\n',' ')
#"".join(contents.split())

# Read encrypted text as a byte array
ByteDataT1 = []
with open("transmission1", "rb") as b:
    byte = b.read(1)
    while byte:
        ByteDataT1+=byte
        byte = b.read(1)

#print(ByteDataT1)
# Xor the two files together - https://stackoverflow.com/questions/2612720/how-to-do-bitwise-exclusive-or-of-two-strings-in-python

key = [ chr(ord(a) ^ b) for (a,b) in zip(contents, ByteDataT1)]
print(key[:30])

# Key is snowboard!

# Read trans 2
ByteDataT2 = []
with open("transmission2", "rb") as b2:
    byte2 = b2.read(1)
    while byte2:
        ByteDataT2+=byte2
        byte2 = b2.read(1)

unencryptedText = [ chr(ord(a) ^ b) for (a,b) in zip(cycle("snowboard"), ByteDataT2)]
print(unencryptedText[:30])

# Text is from chapter 13!
