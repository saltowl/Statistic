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
    print('{0:5}  ({1:5};{2:5})  {3:5}  {4:5}  {5:6}'.format(i + 1, xi, xi + step, middle, num, round(probability, 3)))
    i += 1
    xi += step