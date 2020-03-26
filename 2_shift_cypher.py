def solve(text):
    alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    num = {}
    n = 0
    r = range(26)
    for each in alpha:
        num[each] = n
        n += 1
        result = ""
    num[" "] = " "
    for l in r:
        for each in text:
            if each != " ":
                n = num[each]
                result += alpha[(n + l) % 26]
            else:
                result += each
        result += "\n"
    print(result)

if __name__ == "__main__":
    text = input("enter:\n")
    solve(text)