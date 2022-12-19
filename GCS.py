import queue
import math
import sympy

class Graph: # source : 0   terminal : n + 1
    def __init__(self, n):
        self.n = n
        self.son = [[] for i in range(0, n + 2)]
        self.deg = [0 for i in range(0, n + 2)]
        self.R = [sympy.Symbol("r(%d)" % i) for i in range(0, n + 1)]
    def addEdge(self, x, y):
        son, deg = self.son, self.deg
        if y not in son[x]:
            son[x].append(y)
            deg[y] += 1
    def solve(self):
        n, R, deg, son = self.n, self.R, self.deg, self.son
        f = [1 for i in range(0, n + 2)]
        que = queue.Queue()
        que.put(0)
        f[0] = 0
        while not que.empty():
            u = que.get()
            for v in son[u]:
                f[v] = f[v] * (f[u] + (1 - f[u]) * (1 - R[u]))
                deg[v] -= 1
                if deg[v] == 0:
                    que.put(v)
        expr = sympy.expand(1 - f[n + 1])
        terms = list(expr.args)
        ans = 0
        for term in terms:
            for i in range(0, n + 1):
                cnt = int(math.log2(term.subs([(R[i], 2)]) / term.subs([(R[i], 1)])))
                if cnt > 0:
                    term /= R[i]**(cnt - 1)
            ans += term / R[0]
        print(sympy.expand(ans))

def main():
    n = int(input("请输入点数"))
    m = int(input("请输入边数"))
    G = Graph(n)
    print("请依次输入所有边")
    for i in range(0, m):
        try:
            x, y = input().split(" ", 2)
            G.addEdge(int(x), int(y))
        except:
            raise IOError("输入的不是合法的边！")
    G.solve()

if __name__ == "__main__":
    main()