arr = input().split()
s = set()
max_c = 0
best_time = 0
min_c = len(arr) + 10
count = 0
for i in range(len(arr)):
    if arr[i] in s:
        count = count - 1
        s.remove(arr[i])
        if count == 0 and min_c == len(arr) + 10:
            min_c = i + 1
    else:
        count = count + 1
        s.add(arr[i])
        if count > max_c:
            max_c = count
            best_time = i + 1
if min_c == len(arr) + 10:
    min_c = 0
print(count == 0, min_c, best_time)
