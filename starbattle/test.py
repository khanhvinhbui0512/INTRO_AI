import math

n = 2
check = False
while check == False:
    t = int(math.sqrt((n^2+n+5)*(n^3+n+5)))
    if(t*t == (n^2+n+5)*(n^3+n+5) and (n-1)%7 != 0):
         check = True
    else:
        n=n+1
        print(n)