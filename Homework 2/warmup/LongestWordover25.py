from collections import Counter

f = open("ulysses.txt","r")


contents = f.read()
contents = contents.replace(' ','\n')

frequency = (Counter(contents.split()))
frequency = sorted(frequency.items(), key=lambda x: x[1], reverse=False)

longestWord = ""

for word in frequency:
    if (len(word[0]) > len(longestWord) and word[1] > 25):
        longestWord = word[0]
print "The longest word that occurs >25 times is: ", longestWord, "With a length of: ", len(longestWord)



