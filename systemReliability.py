import sympy
import time

class System:
    def __init__(self, n):
        self.R = [0]
        self.n = n
        for i in range(1, n + 1):
            s = "r(" + str(i) + ")"
            self.R.append(sympy.Symbol(s))
    def G(self, k):
        R = self.R
        n = self.n
        f = [0 for i in range(0, k + 1)]
        f[0] = 1
        for i in range(1, n + 1):
            f[k] = f[k] + f[k - 1] * R[i]
            for j in range(k - 1, 0, -1):
                f[j] = f[j] * (1 - R[i]) + f[j - 1] * R[i]
            f[0] = f[0] * (1 - R[i])
        ans = sympy.expand(f[k])
        return ans
    def F(self, k):
        n = self.n
        self.R = [1 - self.R[i] for i in range(0, n + 1)]
        ans = 1 - self.G(k)
        self.R = [1 - self.R[i] for i in range(0, n + 1)]
        return ans
    def LinConGBackpack(self, k):
        R = self.R
        n = self.n
        f = [0 for i in range(0, k + 1)]
        f[0] = 1
        for i in range(1, n + 1):
            f0 = (1 - f[k]) * (1 - R[i])
            f[k] = f[k] + f[k - 1] * R[i]
            for j in range(k - 1, 0, -1):
                f[j] = f[j - 1] * R[i]
            f[0] = f0
        ans = sympy.expand(f[k])
        return ans
    def LinConG(self, k):
        R = self.R
        n = self.n
        f = [0 for i in range(0, n + 1)]
        f[k] = 1
        for i in range(1, k + 1):
            f[k] = f[k] * R[i]
        mul = f[k]
        for i in range(k + 1, n + 1):
            f[i] = f[i - 1]
            mul = mul * R[i] / R[i - k]
            f[i] = f[i] + mul * (1 - R[i - k]) * (1 - f[i - k - 1])
        ans = sympy.expand(f[n])
        return ans
    def LinConF(self, k):
        n = self.n
        self.R = [1 - self.R[i] for i in range(0, n + 1)]
        ans = 1 - self.LinConG(k)
        self.R = [1 - self.R[i] for i in range(0, n + 1)]
        return ans
    def CycleG(self, k): # n >= 2
        R = self.R
        n = self.n
        ans = self.LinConG(k)
        mulF = 1
        for i in range(1, k):
            mulF = mulF * R[i]
            f = [0 for j in range(0, n + 1)]
            if i + k + 1 <= n:
                f[i + k + 1] = 1
                for j in range(i + 2, i + k + 2):
                    f[i + k + 1] = f[i + k + 1] * R[j]
                mul = f[i + k + 1]
                for j in range(i + k + 2, n + 1):
                    f[j] = f[j - 1]
                    mul = mul * R[j] / R[j - k]
                    f[j] = f[j] + mul * (1 - R[j - k]) * (1 - f[j - k - 1])
            mulB = 1
            for j in range(n, max(n - k + 1, i + 1), -1):
                mulB = mulB * R[j]
                if (n - j + 1) + i >= k:
                    if i + 1 == j - 1:
                        ans = ans + mulF * mulB * (1 - R[i + 1])
                    else:
                        ans = ans + mulF * mulB * (1 - R[i + 1]) * (1 - R[j - 1]) * (1 - f[j - 2])
        ans = sympy.expand(ans)
        return ans
    def CycleF(self, k):
        n = self.n
        self.R = [1 - self.R[i] for i in range(0, n + 1)]
        ans = 1 - self.CycleG(k)
        self.R = [1 - self.R[i] for i in range(0, n + 1)]
        return ans
    def CycleInEx(self, k):
        R = self.R
        n = self.n
        for i in range(1, n + 1):
            R.append(R[i])
        ans = 0
        for S in range(1, 2**n):
            vis = [0 for i in range(0, n + 1)]
            bcnt = 1
            tmp = 1
            for i in range(0, n):
                if (S >> i & 1) == 1:
                    for j in range(i + 1, i + k + 1):
                        id = (j - 1) % n + 1
                        if vis[id] == 0:
                            tmp = tmp * R[id]
                        vis[id] = 1
                    bcnt += 1
            ans = ans + (-1)**bcnt * tmp
        return ans

def main():
    n = 15
    m = 6
    S = System(n)
    start = time.perf_counter()
    print(S.CycleInEx(m))
    end = time.perf_counter()
    print("Time = ", end - start, "s")
    start = time.perf_counter()
    print(S.CycleG(m))
    end = time.perf_counter()
    print("Time = ", end - start, "s")
    # print(CycleG(n, m))
    #assert(LinConGBackpack(n, m).equals(LinConG(n, m)))
    # expr = ""
    # with open("./lincon3550g.m") as f:
    #    text = f.readlines()
    #    expr = text[3][14 : -2]
    # assert(sympy.sympify(str(LinConG(50, 35))) == sympy.sympify(expr))

if __name__ == "__main__":
    main()