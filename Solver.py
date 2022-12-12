import itertools
import random
import math
import Models as model
import matplotlib.pyplot as plt

def Importance(x, p, sys, R):
    sys.R = [R[p[i]] if i != x else 1 for i in range(0, sys.n + 1)]
    ret = sys.LinConG()
    sys.R = [R[p[i]] if i != x else 0 for i in range(0, sys.n + 1)]
    ret -= sys.LinConG()
    return ret

def LKA(sys, R):
    n = sys.n
    s = set([i for i in range(1, n + 1)])
    p = [1 for i in range(0, n + 1)] # which component for each position
    s.remove(1)
    for i in range(n, 1, -1):
        mx = 0
        change = 0
        for x in s:
            I = Importance(x, p, sys, R)
            if I > mx:
                mx = I
                change = x
        p[change] = i
        s.remove(change)
    print("============LK=============")
    sys.R = [R[p[i]] for i in range(0, n + 1)]
    print(sys.LinConG())
    print(p[1:])

def metropolis(delta, Temp):
    return math.exp(-delta / Temp) >= random.random()

def SA(sys, R):
    n = sys.n
    p = [i for i in range(0, n + 1)]
    Temp = 100000000
    while Temp > 0.01:
        x = random.randint(1, n - 1)
        y = random.randint(x + 1, n)
        sys.R = [R[p[i]] for i in range(0, n + 1)]
        delta = sys.LinConG()
        sys.R[x], sys.R[y] = sys.R[y], sys.R[x]
        delta -= sys.LinConG()
        # delta = last - new
        if metropolis(delta, Temp) == 1:
            p[x], p[y] = p[y], p[x]
        Temp *= 0.99
    print("===============SA============")
    sys.R = [R[p[i]] for i in range(0, n + 1)]
    print(sys.LinConG())
    print(p[1:])

def bruteForce(sys, R):
    n = sys.n
    perm = []
    ans = 0
    for p in list(itertools.permutations([i for i in range(1, n + 1)])):
        sys.R = [R[p[i]] if i > -1 else 0 for i in range(-1, n)]
        tmp = sys.LinConG()
        if tmp > ans:
            ans = tmp
            perm = list(p)
    print("============Brute Force===========")
    print(ans)
    print(perm)

def ZK(sys, R, ver):
    n = sys.n
    p = [i for i in range(0, n + 1)]
    update = True
    while update:
        update = False
        for k in range(1, n):
            idk = 0
            idk1 = 0
            if ver == "A":
                for i in range(1, n + 1):
                    if p[i] == k:
                        idk = i
                    elif p[i] == k + 1:
                        idk1 = i
            elif ver == "B":
                for i in range(1, n + 1):
                    if p[i] == k:
                        idk = i
                mn = 1
                for i in range(1, n + 1):
                    if R[p[i]] > R[p[idk]]:
                        I = Importance(i, p, sys, R)
                        if I <= mn:
                            mn = I
                            idk1 = i
            if Importance(idk, p, sys, R) > Importance(idk1, p, sys, R):
                sys.R = [R[p[i]] for i in range(0, n + 1)]
                delta = -sys.LinConG()
                sys.R[idk], sys.R[idk1] = sys.R[idk1], sys.R[idk]
                delta += sys.LinConG()
                if delta > 0:
                    p[idk], p[idk1] = p[idk1], p[idk]
                    update = True
    print("==============ZK Type" + ver + "=============")
    sys.R = [R[p[i]] for i in range(0, n + 1)]
    print(sys.LinConG())
    print(p[1:])

def main():
    n = 10
    k = 5
    R = [1 - random.random() * 0.2 for i in range(0, n)]
    R[1 :] = sorted(R)
    sys = model.System(n, k, R)
    LKA(sys, R)
    ZK(sys, R, "A")
    ZK(sys, R, "B")
    SA(sys, R)
    bruteForce(sys, R)

if __name__ == "__main__":
    main()