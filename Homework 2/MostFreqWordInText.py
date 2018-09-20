from collections import Counter

f = open("ulysses.txt","r")


contents = f.read()
contents = contents.replace(' ','\n')

frequency = (Counter(contents.split()))
frequency = sorted(frequency.items(), key=lambda x: x[1], reverse=False)

print (frequency)

