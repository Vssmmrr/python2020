import math

num = int(input())
simple_num = []
count = int(2)
while len(simple_num) < num:
    flag = True
    for i in range(2, int(math.sqrt(count)) + 1):
        if count % i == 0:
            flag = False
            break
    if flag:
        simple_num.append(count)
    count = count + 1
print(simple_num.pop())
