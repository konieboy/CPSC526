from collections import Counter
from itertools import cycle
import string
import re

def cleantext( longText ):
    longText = ''.join(ch for ch in longText if ch not in set(string.punctuation))
    longText = ''.join(longText.split())
    longText = longText.upper()
    return longText


# read huge text file to xor with encrypted text
f = open("PrideandPrejudice.txt","r", encoding='utf8')
longText = f.read()
longText = cleantext(longText)

f2 = open("transmission3","r", encoding='utf8')
trans3text = f2.read()

# Xor with Long text
decryptText =  ''.join(chr(ord(a) ^ ord(b)) for (a,b) in zip(longText, cycle(trans3text)))

#Find length of cypher + possible word
for i in range(1 , len(decryptText)):
    # find most common substring of length i
    counter = Counter(decryptText[j: j + i] for j in range(len(decryptText) - i))
    key, foundCount = counter.most_common(1)[0]
    #print (counter.most_common(1)[0])
    # ignore low Probability results
    if (foundCount <= 3): 
        break; 
    print ("Test length:", i, " \tTimes found:", foundCount, "\t\tKey:",  key)

# Key word is "swing"
ByteDataT3 = []
with open("transmission3", "rb") as b:
    byte = b.read(1)
    while byte:
        ByteDataT3+=byte
        byte = b.read(1)

unencryptedText = [ chr(ord(a) ^ b) for (a,b) in zip(cycle("swing"), ByteDataT3)]

print("\n#### Unencrypted Text ####\n\n", cleantext(unencryptedText))


