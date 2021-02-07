n = int(input())
for i in range(1, n):
    if i % 15 == 0:
        print("Fizz Buzz", end=", ")
    elif i % 3 == 0:
        print ("Fizz", end=", ")
    elif i % 5 == 0:
        print("Buzz", end=", ")
    else:
        print(i, end=", ")
if n % 15 == 0:
    print("Fizz Buzz")
elif n % 3 == 0:
    print("Fizz")
elif n % 5 == 0:
    print("Buzz")
else:
    print(n)
