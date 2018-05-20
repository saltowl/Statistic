import matplotlib.pyplot as plt
import numpy as np
import math

countInterval = 12
t = 1.95

def PrintHistogram(x, y, step):
    plt.style.use("bmh")
    plt.bar(x, y, step - 0.05, align = 'edge', color = 'sandybrown', edgecolor = 'sienna')
    plt.xlabel("x")
    plt.ylabel("p / h")
    plt.title("Histogram")
    plt.show()


def PrintGraph(Fn, middleX, begin, end):
    if min(Fn) != 0.0:
        Fn.append(0.0)
    if max(Fn) != 1.0:
        Fn.append(1.0)

    buf = Fn[:]
    Fn.extend(buf)
    Fn.sort()

    
    buf.clear()
    buf = middleX[:]
    middleX.extend(buf)
    middleX.extend([begin, end])
    middleX.sort()

    plt.style.use("bmh")
    plt.xlim([begin, end])
    #plt.plot(middleX, Fn)
    #plt.show()
    n = min(len(Fn), len(middleX))
    i = 0
    while i < n:
        print("{0:5} {1:5}".format(Fn[i], middleX[i]))
        i += 1
    print(middleX)
    print(Fn)


def TableHeader():
    print("_________________________________________________________________________________________________")
    print("|\t\t|   Borders of  | Middle of | Count of numbers |\t     |         |         |")
    print("| № of interval |    interval   |  interval |    on interval   | Probability |  xᵢ*pᵢ  |  xᵢ²*pᵢ |")
    print("|_______________|_______________|___________|__________________|_____________|_________|_________|")


def Table(begin, data, end, step, minNum, maxNum):
    i = 0
    xi = begin
    x = []
    y = []
    Fn = []
    middleX = [minNum]
    expectedValue = 0
    dispersion = 0
    countLessThanMiddle = 0

    TableHeader()
    
    while i < countInterval:
        countNumOnInterval = 0
        countLessThanMiddle = 0

        for item in data:
            if (((item < xi + step) & (item > xi) & (xi != begin) & (xi != end)) 
                | ((xi == begin) & (item < xi + step)) 
                | ((xi == end) & (item > xi))):
                countNumOnInterval +=1
        
        middle = xi + step / 2
        middleX.append(middle)

        probability = countNumOnInterval / len(data)

        for item in data:
            if (item <= middle):
                countLessThanMiddle += 1
        
        Fn.append(countLessThanMiddle / len(data))

        expectedValue += probability * middle
        dispersion += probability * middle**2

        print('| {0:^13} | ({1:5};{2:5}) | {3:9} | {4:^16} | {5:^11} | {6:^7} | {7:^7} |'
              .format(i + 1, xi, xi + step, middle, countNumOnInterval, round(probability, 3), 
                      round (probability * middle, 3), round(probability * middle**2,3)))
        
        x.append(xi)
        y.append(probability / step)
        i += 1
        xi += step
    
    print("——————————————————————————————————————————————————————————————————————————————————————————————————")
    print("\nExpected value = {0:4}".format(round(expectedValue, 3)))
    dispersion -= expectedValue**2
    print("Dispersion = {0:4}".format(round(dispersion, 3)))
    beginConfidence = expectedValue - t * (dispersion / len(data))
    endConfidence = expectedValue + t * (dispersion / len(data))
    print("Confidence interval for mathematical expectation: [{0}, {1}], i.e {0} < {2} < {1}"
          .format(round(beginConfidence, 3), round(endConfidence, 3), round(expectedValue, 3)))

    countLessThanMiddle = 0
    for item in data:
       if (item < maxNum):
           countLessThanMiddle += 1
    print(countLessThanMiddle)
    Fn.append(countLessThanMiddle / len(data))

    middleX.append(maxNum)
    PrintHistogram(x, y, step)
    PrintGraph(Fn, middleX, begin, end)


def Main():
    input = open("data.txt")
    dataStrings = input.readlines()

    data = [float(item) for item in dataStrings]
    data.sort()

    #print(data)

    minNum = data[0]
    begin = math.floor(minNum)
    maxNum = data[len(data)-1]
    end = math.ceil(maxNum)

    step = round((maxNum - minNum) / countInterval, 1)

    Table(begin, data, end, step, minNum, maxNum)


Main()