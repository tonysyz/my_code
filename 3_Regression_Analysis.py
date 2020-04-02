import math

def ra():
    x = []
    y = []
    i = 0
    while True:
        i += 1
        nums = input("data%s(eg. 1.4 12)(enter 'stop' to finish):" % i)
        if nums != "stop":
            n1 = nums.split(' ')[0]
            n2 = nums.split(' ')[-1]
            x.append(n1)
            y.append(n2)
        else:
            break
    xn = 0.0
    for each in x:
        xn += float(each)
    xba = xn/len(x)
    yn = 0.0
    for each in y:
        yn += float(each)
    yba = yn/len(y)
    up = 0.0
    down = 0.0
    for each in range(len(x)):
        up += float(x[each]) * float(y[each])
        down += float(x[each])**2
    up -= len(x)*xba*yba
    down -= len(x)*(xba**2)
    bhat = up/down
    ahat = yba - bhat*xba
    print("xba = " + str(xba))
    print('yba = ' + str(yba))
    print("function: y=%sx+%s"%(bhat, ahat))
    rdown = 0.0
    rx = 0.0
    ry = 0.0
    for each in range(len(x)):
        rx += (float(x[each])-xba)**2
        ry += (float(y[each])-yba)**2
    rdown = math.sqrt(rx*ry)
    if rdown != 0:
        r = up/rdown
    else:
        r = "error!0!"
    print("r = "+str(r))
    Rup = 0.0
    Rdown = 0.0
    for each in range(len(x)):
        yhat = float(x[each])*bhat + ahat
        Rup += (float(y[each])-yhat)**2
        Rdown += (float(y[each])-yba)**2
    R2 = Rup/Rdown
    R2 = 1 - R2
    print("R^2 = "+str(R2))

if __name__ == "__main__":
    ra()