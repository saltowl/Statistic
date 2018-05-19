import matplotlib.pyplot as plt
import numpy as np

countInterval = 12

input = open("data.txt")
dataStrings = input.readlines()

data = [float(item) for item in dataStrings]
data.sort()

#print(data)

minNum = data[0]
begin = round(minNum)
maxNum = data[len(data)-1]
end = round(maxNum)

step = round((maxNum - minNum) / countInterval, 1)

i = 0
xi = begin
x = []
y = []
print("_____________________________________________________________________________")
print("|\t\t|   Borders of  | Middle of | Count of numbers |\t     |")
print("| № of interval |    interval   |  interval |    on interval   | Probability |")
print("|_______________|_______________|___________|__________________|_____________|")
while i < countInterval:
    num = 0
    for item in data:
        if (item < xi + step) & (item > xi) & (xi != begin) & (xi != end):
            num +=1
        elif (xi == begin) & (item < xi + step):
            num +=1
        elif (xi == end) & (item > xi):
            num +=1
    middle = xi + step / 2
    probability = num / len(data)
    print('| {0:^13} | ({1:5};{2:5}) | {3:9} | {4:^16} | {5:^11} |'
          .format(i + 1, xi, xi + step, middle, num, round(probability, 3)))
    x.append(xi)
    y.append(probability / step)
    i += 1
    xi += step
print("—————————————————————————————————————————————————————————————————————————————")

plt.style.use("bmh")
plt.bar(x, y, step - 0.05, align = 'edge', color = 'sandybrown', edgecolor = 'sienna')
plt.xlabel("x")
plt.ylabel("p / h")
plt.title("Histogram")
plt.show()