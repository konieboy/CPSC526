from collections import Counter

f = open("ulysses.txt","r", encoding='utf8')


contents = f.read()
contents = contents.replace(' ','\n')



frequency = (Counter(contents.split()))
frequency = sorted(frequency.items(), key=lambda x: x[1], reverse=False)

print ("\n\nThe most frequent word that occurs is: -",frequency[-1][0],"- And it occurs -", frequency[-1][1], "- times in the text")


longestWord = ""

for word in frequency:
    if (len(word[0]) > len(longestWord) and word[1] > 25):
        longestWord = word[0]
print ("\n\nThe longest word that occurs >25 times is: ", longestWord, "With a length of: ", len(longestWord))

for word in frequency:
    if (len(word[0]) > len(longestWord)):
        longestWord = word[0]
print ("\n\nThe longest word that occurs is: ", longestWord, "With a length of: ", len(longestWord))

