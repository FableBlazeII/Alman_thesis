#!/usr/bin/env python

import random, os;

expressionsCount=50
minLen=2 #Set between 1 and 12
maxLen=12 #Set between 1 and 12

OUTPUT="./Testandmed/inputRegex.txt"


print "Output: ",
print os.path.abspath(OUTPUT)

#The extra dots are intended because the real regular expressions usually also contain more dots
regexLetters=['.']*50+['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y']

with open(OUTPUT, 'w') as output:
    for i in range(expressionsCount-1):
        expression=[]
        expressionLen=random.randint(minLen,maxLen)
        for j in range(expressionLen):
            expression.append(regexLetters[random.randint(0,len(regexLetters)-1)])

        #Make sure that at least one character in regex is not a dot (regex consisting onfly of dots is considered meaningless)
        expression[random.randint(0,expressionLen-1)]=regexLetters[random.randint(50,len(regexLetters)-1)]

        output.write(''.join(expression)+'\n')



    expression=[]
    expressionLen=random.randint(1,12)
    for j in range(expressionLen):
        expression.append(regexLetters[random.randint(0,len(regexLetters)-1)])

    #Make sure that at least one character in regex is not a dot (regex consisting onfly of dots is considered meaningless)
    expression[random.randint(0,expressionLen-1)]=regexLetters[random.randint(50,len(regexLetters)-1)]

    output.write(''.join(expression))

print "Done"
