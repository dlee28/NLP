import sys
import re
file = sys.argv[1]
import json

vaweightTrueOrFake = {}
vaweightPosOrNeg = {}
averageweightTrueOrFake = {}
averageweightPosOrNeg = {}
fTrueOrFake = {}
fPosOrNeg={}
c = 1
array = []
arrayb = []
arrayc = []

def deal(word):
    for x in range(3,len(word)):
        rule = re.compile(r'[^a-zA-z]')
        word[x] = rule.sub("",word[x])
        word[x] = word[x].lower()

def countnumfunc():
    countword = {}
    for x in range(3,len(word)):
        if word[x] in countword:
            countword[word[x]]+=1
        else:
            countword[word[x]]=1
    return countword


def vanilla(weight,aveweight,isTrue,b,B,c):
    total = 0
    for x in countword:
        if x in weight:
            total += weight[x]*countword[x]
            c = c + 1
    total += b
    mutitotal = isTrue*total
    if mutitotal <= 0:
        b += isTrue
        B += isTrue*c
        for x in countword:
            if x in weight:
                weight[x] =weight[x]+isTrue*countword[x]
                aveweight[x] = aveweight[x]+isTrue*countword[x]*c
            else:
                weight[x]=isTrue*countword[x]
                aveweight[x] = isTrue * countword[x] * c

    #print(b)
    return b,B,c


# with open("train-labeled.txt","r") as f:
with open(file, "r") as f:
    content = f.readlines()
    bvanillaTrueOrFake = 0
    bvanillaNegOrPos = 0
    BTrueOrFake = 0
    BNegOrPos = 0
    i = 0
    while i < 30:
        i += 1
        for x in content:
            x = x.strip()
            word = x.split(" ")
            array.append(word[0])
            deal(word)
            countword = countnumfunc()
            if word[1] == 'Fake':
                bvanillaTrueOrFake,BTrueOrFake,c = vanilla(vaweightTrueOrFake,averageweightTrueOrFake, -1, bvanillaTrueOrFake,BTrueOrFake,c)
            else:
                bvanillaTrueOrFake,BTrueOrFake,c = vanilla(vaweightTrueOrFake,averageweightTrueOrFake, 1, bvanillaTrueOrFake,BTrueOrFake,c)

            if word[2] == 'Neg':
                bvanillaNegOrPos,BNegOrPos,c = vanilla(vaweightPosOrNeg,averageweightPosOrNeg, -1, bvanillaNegOrPos,BNegOrPos,c)
            else:
                bvanillaNegOrPos,BNegOrPos,c = vanilla(vaweightPosOrNeg,averageweightPosOrNeg, 1, bvanillaNegOrPos,BNegOrPos,c)


    for key in vaweightTrueOrFake:
        fTrueOrFake[key] = vaweightTrueOrFake[key] - (1/float(c))*averageweightTrueOrFake[key]

    for key in vaweightPosOrNeg:
        fPosOrNeg[key] = vaweightPosOrNeg[key] - (1 / float(c)) * averageweightPosOrNeg[key]

    averBTrueOrFake = bvanillaTrueOrFake - (1/float(c))*BTrueOrFake
    averPosOrNeg = bvanillaNegOrPos - (1/float(c))*BNegOrPos

    arrayb.append(bvanillaTrueOrFake)
    print(bvanillaTrueOrFake)
    arrayb.append(bvanillaNegOrPos)
    print(bvanillaNegOrPos)
    arrayc.append(averBTrueOrFake)
    print(averBTrueOrFake)
    arrayc.append(averPosOrNeg)
    print(averPosOrNeg)




import json
listdic={}
listdic["arrayb"]=arrayb
listdic1={}
listdic1["arrayb"]=arrayc
jsObj1 = json.dumps(vaweightTrueOrFake)
jsObj2= json.dumps(vaweightPosOrNeg)
jsObj3 = json.dumps(listdic)
jsObj4= json.dumps(fTrueOrFake)
jsObj5= json.dumps(fPosOrNeg)
jsObj6 = json.dumps(listdic1)

fileObject = open("vanillamodel.txt","w")
fileObject.write(jsObj1)
fileObject.write('\n')
fileObject.write(jsObj2)
fileObject.write('\n')
fileObject.write(jsObj3)


fileObject = open("averagedmodel.txt","w")
fileObject.write(jsObj4)
fileObject.write('\n')
fileObject.write(jsObj5)
fileObject.write('\n')
fileObject.write(jsObj6)