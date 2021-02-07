first = input()
second = list(set(input().replace(' ', '')))
for i in range(len(second)):
    first = first.replace(second[i], '')
print(first)
