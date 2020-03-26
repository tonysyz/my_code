import random

#x 为生成随机斐波那契数列的次数
def random_fi(x):
    i1 = 1
    i2 = 1
    i3 = 0
    def fi(n, a, b):
        if n == 1:
            c = a + b
        if n == 2:
            c = a - b
        return c
    print(i1)
    print(i2)
    count = 0
    a = ""
    b = ""
    while count < x:
        count += 1
        n = random.randint(1, 2)
        i3 = fi(n, i1, i2)
        b += str(i3) + "\n"
        a += str(i3/i2) + "\n"
        n = random.randint(1, 2)
        i1 = fi(n, i2, i3)
        b += str(i1) + "\n"
        a += str(i1/i3) + "\n"
        n = random.randint(1, 2)
        i2 = fi(n, i1, i3)
        b += str(i2) + "\n"
        a += str(i2/i3) + "\n"
    return [a, b]
if __name__ == "__main__":
    x = input("please enter a number:")
    try:
        l = random_fi(int(x)/3)
        print(l[1])
        print(l[0])
    except ZeroDivisionError:
        print("cannot count the constant because zero appears, please try again!")