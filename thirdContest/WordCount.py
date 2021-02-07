string = input()
l1 = list(string.split())
s = tuple(string.split())
l2 = []
for i in range(len(s)):
    l2.append(l1.count(s[i]))
print(int(max(l2)) / len(l1))
