num, system = input().split()
num = int(num)
system = int(system)
new_num = []
while num >= system:
    new_num.append(num % system)
    num = num // system
new_num.append(num)
answ = new_num[::-1]
for i in range(len(answ)):
    print(answ[i], end='')
