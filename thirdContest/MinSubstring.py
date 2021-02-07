string = input()
s = list(set(string))
s.sort()
for i in range(len(s)):
    max_len = 1
    while s[i] * (max_len + 1) in string:
        max_len += 1
    print(s[i], max_len)
