#!/usr/bin/env python

import random, os;

wordLen=12
wordCount=10000
sampleCount=100
OUTPUT="./inputSummary.txt"
countMax=500


letters=['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y']
#The extra 0 are intended, it is probably the easiest (but not very effective) way to make the array sparse
possibleCounts=range(countMax)+[0]*(countMax*4)

print "Output: ",
print os.path.abspath(OUTPUT)
with open(OUTPUT, 'w') as output:
    for i in xrange(wordCount-1):
        tmpLetters=[]
        for j in range(wordLen):
            tmpLetters.append(letters[random.randint(0,19)])
        tmpWord=''.join(tmpLetters)

        tmpCounts=[]
        for k in range(sampleCount):
            tmpCounts.append(str(possibleCounts[random.randint(0,len(possibleCounts)-1)]))
        output.write(tmpWord)
        output.write('\t')
        output.write('\t'.join(tmpCounts))
        output.write('\n')
            
    tmpLetters=[]
    for j in range(wordLen):
        tmpLetters.append(letters[random.randint(0,19)])
    tmpWord=''.join(tmpLetters)

    tmpCounts=[]
    for k in range(sampleCount):
        tmpCounts.append(str(possibleCounts[random.randint(0,len(possibleCounts)-1)]))
    output.write(tmpWord)
    output.write('\t')
    output.write('\t'.join(tmpCounts))

print "Done"
