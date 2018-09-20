from collections import Counter

f = open("ulysses.txt","r")


contents = f.read()
contents = contents.replace(' ','\n')

frequency = (Counter(contents.split()))
frequency = sorted(frequency.items(), key=lambda x: x[1], reverse=False)

longestWord = ""

for word in frequency:
    if (len(word[0]) > len(longestWord)):
        longestWord = word[0]
print "The longest word is: " , longestWord, "With a length of: ", len(longestWord)



