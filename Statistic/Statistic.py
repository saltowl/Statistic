import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.stats import norm

countInterval = 12
t = 1.95

def PrintHistogram(x, y, step):
    plt.style.use("bmh")
    plt.bar(x, y, step, align = 'edge', color = 'sandybrown', edgecolor = 'sienna', linewidth = 1.5)
    plt.xlabel("x")
    plt.ylabel("p / h")
    plt.title("Histogram")

    s = 'S = p₄ = ' + str(round(y[3] * step, 3))
    plt.annotate(s, xy=(x[3] + (step / 2), y[3]), xytext=(x[0], y[4]),
            arrowprops={'facecolor': 'brown', 'shrink': 0.05})

    plt.show()


def PrintGraph(Fn, xGraph, begin, end):
    if min(Fn) != 0.0:
        Fn.extend([0.0] * 2)
    if max(Fn) != 1.0:
        Fn.extend([1.0] * 4)

    xGraph.extend([begin, end])

    Fn.sort()
    xGraph.sort()

    plt.style.use("bmh")
    plt.xlim([begin, end])
    plt.ylim([-0.05, 1.05])

    i = 0
    while i < len(Fn) - 2:
        plt.plot([xGraph[i], xGraph[i+1]], [Fn[i], Fn[i+1]], color = 'firebrick')
        plt.plot([xGraph[i]] * 2, [Fn[i], 0], color = 'tomato', linestyle = '--', linewidth = 1)
        plt.plot([begin, xGraph[i]], [Fn[i]] * 2, color = 'brown', linestyle = ':', linewidth = 1)
        i += 2

    plt.plot([xGraph[i], xGraph[i+1]], [Fn[i], Fn[i+1]], color = 'firebrick')
    plt.xlabel("X")
    plt.ylabel("F(X)")
    plt.title("Graph of the empirical distribution function")
    plt.show()


def TableHeader():
    print("\nTable 1")
    print("_________________________________________________________________________________________________")
    print("|\t\t|   Borders of  | Middle of | Count of numbers |\t     |         |         |")
    print("| № of interval |    interval   |  interval |    on interval   | Probability |  xᵢ*pᵢ  |  xᵢ²*pᵢ |")
    print("|_______________|_______________|___________|__________________|_____________|_________|_________|")

def TableHeaderNew():
    print("\nTable 2")
    print("_____________________________________________________")
    print("|   Borders of  |        |        |        |        |")
    print("|    interval   |   Zᵢ   |  F(Zᵢ) |   pᵢ   |   nᵢ   |")
    print("|_______________|________|________|________|________|")


def Table(begin, data, end, step, minNum, maxNum):
    i = 0
    xi = begin
    x = []
    y = []
    Fn = []
    xGraph = [xi]
    expectedValue = 0
    dispersion = 0
    yFn = 0

    TableHeader()
    
    while i < countInterval:
        countNumOnInterval = 0

        for item in data:
            if (((item < xi + step) & (item > xi) & (xi != begin) & (xi != end)) 
                | ((xi == begin) & (item < xi + step)) 
                | ((xi == end) & (item > xi))):
                countNumOnInterval +=1
        
        middle = xi + step / 2
        probability = countNumOnInterval / len(data)
        
        yFn += probability
        xGraph.extend([xi, xi + step])
        Fn.extend([yFn] * 2)

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

    PrintHistogram(x, y, step)
    xGraph.append(float(end))
    Fn.extend([1.0] * 2)
    PrintGraph(Fn, xGraph, begin - 1, end + 1)
    return (expectedValue, dispersion)


def PrintData(data):
    x = 0
    print("\nInitial data\n")

    for i in range(5):
        for j in range(4):
            print("{:6} {:6} {:6} {:6} {:6} {:6} {:6} {:6} {:6} {:6} ".format(*data[x:x+10]))
            x += 10
        print()

def PearsonDistribution(begin, data, end, step, expectedValue, dispersion):
    i = 0
    xi = begin
    newCount = 0
    probabilityGroup = 0
    nGroup = 0
    npiGroup = 0
    itemForRearsonGroup = 0
    nGroupList = []
    probabilityGroupList = []

    TableHeaderNew()
    
    while i < countInterval:
        countNumOnInterval = 0
        zi = 0
        F = 0
        probability = 0
        npi = 0
        itemForPearson = 0
        
        if i != countInterval - 1:
            zi = ((xi + step) - expectedValue) / math.sqrt(dispersion)
        else:
            zi = math.inf

        F = norm.cdf(zi)

        if i != 0:
            probability = F - buf
        else:
            probability = F

        for item in data:
            if (((item < xi + step) & (item > xi) & (xi != begin) & (xi != end)) 
                | ((xi == begin) & (item < xi + step)) 
                | ((xi == end) & (item > xi))):
                countNumOnInterval +=1
        
        if (countNumOnInterval >= 5):
            newCount += 1
            probabilityGroupList.append(probability)
            nGroupList.append(countNumOnInterval)
        else:
            probabilityGroup += probability
            nGroup += countNumOnInterval
            if nGroup >= 5:
                nGroupList.append(nGroup)
                probabilityGroupList.append(probabilityGroup)
                nGroup = 0
                probabilityGroup = 0
            elif i == countInterval - 1:
                nGroupList.append(nGroupList.pop() + nGroup)
                probabilityGroupList.append(probabilityGroupList.pop() + probabilityGroup)
        
        npi = probability * len(data)
        itemForPearson = countNumOnInterval**2 / npi

        if (i > 0 and i < countInterval - 1):
            print('| ({0:5};{1:5}) | {2:6} | {3:^6} | {4:^6} | {5:^6} |'
              .format(xi, xi + step, round(zi, 3), round(F, 3), round(probability, 3), countNumOnInterval))
        elif (i == 0):
            print('| (  -∞ ;{1:5}) | {2:6} | {3:^6} | {4:^6} | {5:^6} |'
              .format(xi, xi + step, round(zi, 3), round(F, 3), round(probability, 3), countNumOnInterval))
        elif (i == countInterval - 1):
            print('| ({0:5};  +∞ ) |   +∞   | {1:^6} | {2:^6} | {3:^6} |'
              .format(xi, round(F, 3), round(probability, 3), countNumOnInterval))
        
        i += 1
        xi += step
        buf = F

    print("————————————————————————————————————————————————————")
    PrintGroupTable(nGroupList, probabilityGroupList, newCount)
  

def PrintGroupTable(nGroupList, probabilityGroupList, newCount):
    print('\n\nResults of grouping in {0} intervals'.format(newCount))
    print('\nProbability:')
    print([ '%.2f' % elem for elem in probabilityGroupList ])

    print('\nCount of numbers on interval:')
    print(nGroupList)

    print('\nnᵢ²')
    i = 0
    while i <= newCount:
        nGroupList[i] = nGroupList[i]**2
        i += 1
    print(nGroupList)

    print('\nnpᵢ')
    i = 0
    while i <= newCount:
        probabilityGroupList[i] *= 200
        i += 1
    print([ '%.2f' % elem for elem in probabilityGroupList ])

    print('\nnᵢ²/npᵢ')
    i = 0
    sum = 0
    while i <= newCount:
        nGroupList[i] /= probabilityGroupList[i]
        sum += nGroupList[i]
        i += 1
    print([ '%.2f' % elem for elem in nGroupList ])

    print('\nSum (nᵢ²/npᵢ) = {0:5}'.format(round(sum, 3)))
    print('\nPearson test = {0:5}'.format(round(sum - 200, 3)))



def Main():
    input = open("data.txt")
    dataStrings = input.readlines()

    data = [float(item) for item in dataStrings]
    data.sort()

    PrintData(data)

    minNum = data[0]
    begin = math.floor(minNum)
    maxNum = data[len(data)-1]
    end = math.ceil(maxNum)

    step = round((maxNum - minNum) / countInterval, 1)

    (expectedValue, dispersion) = Table(begin, data, end, step, minNum, maxNum)
    PearsonDistribution(begin, data, end, step, expectedValue, dispersion)


Main()