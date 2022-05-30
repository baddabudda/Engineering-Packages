# lecture 28.03
def task1(initLine):
    print(initLine[1],initLine[0], sep='')

def task2(initLine):
    startIdx = 0
    endIdx = 0
    flag = 0
    for symbol in initLine:
        if (symbol == '\"' or symbol == '\'') and (flag == 0):
            startIdx = initLine.find(symbol)
            flag = 1
        elif (symbol == '\"' or symbol == '\'') and (flag == 1):
            endIdx = initLine.find(symbol, startIdx+1, len(initLine))

    print(initLine[(startIdx+1):(endIdx)])

def task3(initLine):
    print(int(initLine)*2)

def task4(initLine):
    startIdx = 0

    for symbol in initLine:
        if symbol == ' ':
            startIdx = initLine.find(symbol)

    print(initLine[startIdx+1:len(initLine)], initLine[0:startIdx])

def task5(initLine):
    endIdx = 0

    for symbol in initLine:
        if symbol == '@':
            endIdx = initLine.find(symbol)

    print(initLine[0:endIdx])

def task6(initLine):
    x = initLine.replace(' ', '')
    y = x.replace('-', '')
    z = y.replace('(', '')
    w = z.replace(')', '')

    print(w)

# def task7(initLine, reversedLine=None):
#     str reversedLine
#     for idx in range(len(initLine), 0):
#         reversedLine = reversedLine + initLine[idx]
#
#     print(reversedLine)

def filter(val):
    return val

with open('task2.txt') as file:
    lines = file.readlines()
    zooList = []

    for i in range(0, len(lines)):
        animInfo = lines[i].split()
        zooList.append(animInfo)

    # print(zooList)

    isMatch = False
    matchList = []

    for i in range(0, len(zooList)):
        for j in range(i, len(zooList)):
            if (zooList[j][1] == zooList[i][1]) and (zooList[j][2] != zooList[i][2]):
                matchList.append(zooList[i][1])

    if (len(matchList) == 0):
        print("No matches found")
    else:
        matchList.sort(reverse=False, key=filter)
        for i in range(0, len(matchList)):
            print(matchList[i])



