n = int(input())

first = int(n / 100000)
second = int(n / 10000 - first * 10)
third = int(n / 1000 - first * 100 - second * 10)
sixth = n % 10
fifth = int((n % 100 - sixth) / 10)
fourth = int((n % 1000 - fifth * 10 - sixth) / 100)

if first + second + third == fourth + fifth + sixth:
    print(n)
else:
    i = n
    j = n
    while first + second + third != fourth + fifth + sixth:
        i += 1
        first = int(i / 100000)
        second = int(i / 10000 - first * 10)
        third = int(i / 1000 - first * 100 - second * 10)
        sixth = i % 10
        fifth = int((i % 100 - sixth) / 10)
        fourth = int((i % 1000 - fifth * 10 - sixth) / 100)
        if first + second + third == fourth + fifth + sixth:
            print(i)
            break
        else:
            j -= 1
            first = int(j / 100000)
            second = int(j / 10000 - first * 10)
            third = int(j / 1000 - first * 100 - second * 10)
            sixth = j % 10
            fifth = int((j % 100 - sixth) / 10)
            fourth = int((j % 1000 - fifth * 10 - sixth) / 100)
            if first + second + third == fourth + fifth + sixth:
                print(j)
                break
