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


def PrintData(data):
    x = 0
    print("\nInitial data\n")
    for i in range(5):
        for j in range(4):
            print("{:6} {:6} {:6} {:6} {:6} {:6} {:6} {:6} {:6} {:6} ".format(*data[x:x+10]))
            x += 10
        print()

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

    Table(begin, data, end, step, minNum, maxNum)


Main()