def pascal_triangle():
    array = [1]
    while True:
        for i in array:
            yield i
        array.append(0)
        new_array = [array[i - 1] + array[i] for i in range(0, len(array))]
        array = new_array
