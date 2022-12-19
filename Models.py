import time
import random

class System:
    # attribute variable = public
    def __init__(self, n, k, R):
        # instance variable = private
        self.R = R
        self.n = n
        self.k = k
    def G(self):
        R = self.R
        n = self.n
        k = self.k
        f = [0 for i in range(0, k + 1)]
        f[0] = 1
        for i in range(1, n + 1):
            f[k] = f[k] + f[k - 1] * R[i]
            for j in range(k - 1, 0, -1):
                f[j] = f[j] * (1 - R[i]) + f[j - 1] * R[i]
            f[0] = f[0] * (1 - R[i])
        return f[k]
    def F(self):
        n = self.n
        self.R = [1 - self.R[i] for i in range(0, n + 1)]
        ans = 1 - self.G()
        self.R = [1 - self.R[i] for i in range(0, n + 1)]
        return ans
    def LinConGBackpack(self):
        R = self.R
        n = self.n
        k = self.k
        f = [0 for i in range(0, k + 1)]
        f[0] = 1
        for i in range(1, n + 1):
            f0 = (1 - f[k]) * (1 - R[i])
            f[k] = f[k] + f[k - 1] * R[i]
            for j in range(k - 1, 0, -1):
                f[j] = f[j - 1] * R[i]
            f[0] = f0
        return f[k]
    def LinConG(self):
        R = self.R
        n = self.n
        k = self.k
        f = [0 for i in range(0, n + 1)]
        f[k] = 1
        for i in range(1, k + 1):
            f[k] = f[k] * R[i]
        mul = f[k]
        zero = 0
        for i in range(k + 1, n + 1):
            f[i] = f[i - 1]
            if R[i] == 0:
                zero += 1
            else:
                mul *= R[i]
            if R[i - k] == 0:
                zero -= 1
            else:
                mul /= R[i - k]
            f[i] = f[i] + (mul if zero == 0 else 0) * (1 - R[i - k]) * (1 - f[i - k - 1])
        return f[n]
    def LinConF(self):
        n = self.n
        self.R = [1 - self.R[i] for i in range(0, n + 1)]
        ans = 1 - self.LinConG()
        self.R = [1 - self.R[i] for i in range(0, n + 1)]
        return ans
    def CycleG(self): # n >= 2
        R = self.R
        n = self.n
        k = self.k
        ans = self.LinConG()
        mulF = 1
        for i in range(1, k):
            mulF = mulF * R[i]
            f = [0 for j in range(0, n + 1)]
            if i + k + 1 <= n:
                f[i + k + 1] = 1
                for j in range(i + 2, i + k + 2):
                    f[i + k + 1] = f[i + k + 1] * R[j]
                mul = f[i + k + 1]
                zero = 0
                for j in range(i + k + 2, n + 1):
                    f[j] = f[j - 1]
                    if R[j] == 0:
                        zero += 1
                    else:
                        mul *= R[j]
                    if R[j - k] == 0:
                        zero -= 1
                    else:
                        mul /= R[j - k]
                    f[j] = f[j] + (mul if zero == 0 else 0) * (1 - R[j - k]) * (1 - f[j - k - 1])
            mulB = 1
            for j in range(n, max(n - k + 1, i + 1), -1):
                mulB = mulB * R[j]
                if (n - j + 1) + i >= k:
                    if i + 1 == j - 1:
                        ans = ans + mulF * mulB * (1 - R[i + 1])
                    else:
                        ans = ans + mulF * mulB * (1 - R[i + 1]) * (1 - R[j - 1]) * (1 - f[j - 2])
        return ans
    def CycleF(self):
        n = self.n
        self.R = [1 - self.R[i] for i in range(0, n + 1)]
        ans = 1 - self.CycleG()
        self.R = [1 - self.R[i] for i in range(0, n + 1)]
        return ans
    def CycleInEx(self):
        R = self.R
        n = self.n
        k = self.k
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
    def curModel(self): # which model to use
        return self.LinConF()

def main():
    n = 15
    m = 6
    S = System(n, m, [0 for i in range(0, n + 1)])
    start = time.perf_counter()
    print(S.CycleInEx())
    end = time.perf_counter()
    print("Time = ", end - start, "s")
    start = time.perf_counter()
    print(S.CycleG())
    end = time.perf_counter()
    print("Time = ", end - start, "s")

if __name__ == "__main__":
    main()