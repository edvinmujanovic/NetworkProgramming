def fibonacci(maxnum):
    a, b = 0, 1
    while a <= maxnum:
        yield a
        a, b = b, a + b
 

for i in fibonacci(1000000):
    print(i)
