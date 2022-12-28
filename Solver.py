import itertools
import random
import math
import numpy
import pygad
import sys as lim
import Models as model

def fetch():
    return sys, R

def Importance(x, p):
    sys.R = [R[p[i]] if i != x else 1 for i in range(0, sys.n + 1)]
    ret = sys.curModel()
    sys.R = [R[p[i]] if i != x else 0 for i in range(0, sys.n + 1)]
    ret -= sys.curModel()
    return ret

class LK:
    def LKA(self):
        n = sys.n
        s = set([i for i in range(1, n + 1)])
        p = [1 for i in range(0, n + 1)]  # which component for each position
        for i in range(n, 1, -1):
            mx = 0
            change = 0
            for x in s:
                I = Importance(x, p)
                if I >= mx:
                    mx = I
                    change = x
            s.remove(change)
            p[change] = i
        sys.R = [R[p[i]] for i in range(0, n + 1)]
        return sys.curModel(), p[:]
    def LKB(self):
        n = sys.n
        s = set([i for i in range(1, n + 1)])
        p = [n for i in range(0, n + 1)]
        for i in range(1, n):
            mn = 1
            change = 0
            for x in s:
                I = Importance(x, p)
                if I <= mn:
                    mn = I
                    change = x
            s.remove(change)
            p[change] = i
        sys.R = [R[p[i]] for i in range(0, n + 1)]
        return sys.curModel(), p[:]
    def LKC(self):
        n = sys.n
        s = set([i for i in range(1, n + 1)])
        p = [1 for i in range(0, n + 1)]
        for i in range(2, n + 1):
            mn = 1
            change = 0
            for x in s:
                I = Importance(x, p)
                if I <= mn:
                    mn = I
                    change = x
            s.remove(change)
            for x in s:
                p[x] = i
        sys.R = [R[p[i]] for i in range(0, n + 1)]
        return sys.curModel(), p[:]
    def LKD(self):
        n = sys.n
        s = set([i for i in range(1, n + 1)])
        p = [n for i in range(0, n + 1)]
        for i in range(n - 1, 0, -1):
            mx = 0
            change = 0
            for x in s:
                I = Importance(x, p)
                if I >= mx:
                    mx = I
                    change = x
            s.remove(change)
            for x in s:
                p[x] = i
        sys.R = [R[p[i]] for i in range(0, n + 1)]
        return sys.curModel(), p[:]

class SA:
    def metropolis(self, delta, Temp):
        return True if math.exp(-delta / Temp) >= random.random() else False
    def SA(self):
        n = sys.n
        p = [i for i in range(0, n + 1)]
        Temp = 100000000
        while Temp > 0.01:
            x = random.randint(1, n - 1)
            y = random.randint(x + 1, n)
            sys.R = [R[p[i]] for i in range(0, n + 1)]
            delta = sys.curModel()
            sys.R[x], sys.R[y] = sys.R[y], sys.R[x]
            delta -= sys.curModel()
            # delta = last - new
            if self.metropolis(delta, Temp):
                p[x], p[y] = p[y], p[x]
            Temp *= 0.99
        sys.R = [R[p[i]] for i in range(0, n + 1)]
        return sys.curModel(), p[:]

class BF:
    def bruteForce(self):
        n = sys.n
        ansMx, ansMn = 0, 1
        for p in list(itertools.permutations([i for i in range(1, n + 1)])):
            sys.R = [R[p[i]] if i > -1 else 0 for i in range(-1, n)]
            tmp = sys.curModel()
            if tmp >= ansMx:
                ansMx = tmp
            if tmp <= ansMn:
                ansMn = tmp
        return ansMx, ansMn
    def randomization(self):
        n = sys.n
        ansMx, ansMn = 0, 1
        for i in range(10000):
            p = random.sample(range(1, n + 1), n)
            sys.R = [R[p[i]] if i > -1 else 0 for i in range(-1, n)]
            tmp = sys.curModel()
            if tmp >= ansMx:
                ansMx = tmp
            if tmp <= ansMn:
                ansMn = tmp
        return ansMx, ansMn

class ZK:
    def ZKA(self, p = None):
        n = sys.n
        if p is None:
            p = [i for i in range(0, n + 1)]
        update = True
        while update:
            update = False
            for k in range(1, n):
                idk = 0
                idk1 = 0
                for i in range(1, n + 1):
                    if p[i] == k:
                        idk = i
                    elif p[i] == k + 1:
                        idk1 = i
                if Importance(idk, p) > Importance(idk1, p):
                    sys.R = [R[p[i]] for i in range(0, n + 1)]
                    delta = -sys.curModel()
                    sys.R[idk], sys.R[idk1] = sys.R[idk1], sys.R[idk]
                    delta += sys.curModel()
                    if delta > 0:
                        p[idk], p[idk1] = p[idk1], p[idk]
                        update = True
        sys.R = [R[p[i]] for i in range(0, n + 1)]
        return sys.curModel(), p[:]
    def ZKB(self, p = None):
        n = sys.n
        if p is None:
            p = [i for i in range(0, n + 1)]
        update = True
        while update:
            update = False
            for k in range(1, n):
                idk = 0
                idk1 = 0
                for i in range(1, n + 1):
                    if p[i] == k:
                        idk = i
                mn = 1
                for i in range(1, n + 1):
                    if R[p[i]] > R[p[idk]]:
                        I = Importance(i, p)
                        if I <= mn:
                            mn = I
                            idk1 = i
                if Importance(idk, p) > Importance(idk1, p):
                    sys.R = [R[p[i]] for i in range(0, n + 1)]
                    delta = -sys.curModel()
                    sys.R[idk], sys.R[idk1] = sys.R[idk1], sys.R[idk]
                    delta += sys.curModel()
                    if delta > 0:
                        p[idk], p[idk1] = p[idk1], p[idk]
                        update = True
        sys.R = [R[p[i]] for i in range(0, n + 1)]
        return sys.curModel(), p[:]
    def ZKC(self, p = None):
        n = sys.n
        if p is None:
            p = [i for i in range(0, n + 1)]
        update = True
        while update:
            update = False
            for k in range(n, 1, -1):
                idk = 0
                idk1 = 0
                for i in range(1, n + 1):
                    if p[i] == k:
                        idk = i
                    elif p[i] == k - 1:
                        idk1 = i
                if Importance(idk, p) < Importance(idk1, p):
                    sys.R = [R[p[i]] for i in range(0, n + 1)]
                    delta = -sys.curModel()
                    sys.R[idk], sys.R[idk1] = sys.R[idk1], sys.R[idk]
                    delta += sys.curModel()
                    if delta > 0:
                        p[idk], p[idk1] = p[idk1], p[idk]
                        update = True
        sys.R = [R[p[i]] for i in range(0, n + 1)]
        return sys.curModel(), p[:]
    def ZKD(self, p = None):
        n = sys.n
        if p is None:
            p = [i for i in range(0, n + 1)]
        update = True
        while update:
            update = False
            for k in range(n, 1, -1):
                idk = 0
                idk1 = 0
                for i in range(1, n + 1):
                    if p[i] == k:
                        idk = i
                mx = 0
                for i in range(1, n + 1):
                    if R[p[i]] < R[p[idk]]:
                        I = Importance(i, p)
                        if I >= mx:
                            mx = I
                            idk1 = i
                if Importance(idk, p) < Importance(idk1, p):
                    sys.R = [R[p[i]] for i in range(0, n + 1)]
                    delta = -sys.curModel()
                    sys.R[idk], sys.R[idk1] = sys.R[idk1], sys.R[idk]
                    delta += sys.curModel()
                    if delta > 0:
                        p[idk], p[idk1] = p[idk1], p[idk]
                        update = True
        sys.R = [R[p[i]] for i in range(0, n + 1)]
        return sys.curModel(), p[:]

class BIT:
    def BIT(self):
        a, pA = LK().LKA()
        b, pB = LK().LKB()
        lowComp = True
        for i in range(1, sys.n + 1):
            if R[i] > 0.2:
                lowComp = False
        if lowComp:
            b1, p1 = ZK().ZKB(pA[:])
            b2, p2 = ZK().ZKB(pB[:])
            return (b1, p1) if b1 > b2 else (b2, p2)
        else:
            d1, p1 = ZK().ZKD(pA[:])
            d2, p2 = ZK().ZKD(pB[:])
            return (d1, p1) if d1 > d2 else (d2, p2)

# Genetic Algorithm
def fitnessFunc(solution, solution_idx):
    sys, R = fetch()
    sys.R = [R[solution[i]] if i > -1 else 0 for i in range(-1, sys.n)]
    return sys.curModel()
def findFa(x, fa):
    stack = [x]
    flag = True
    while len(stack) > 0:
        top = stack[-1]
        if top == fa[top]:
            flag = False
        if flag:
            stack.append(fa[top])
        else:
            stack.pop()
            if len(stack) > 0:
                fa[stack[-1]] = fa[top]
    return fa[x]
def crossoverFunc(parents, offspring_size, ga_instance):
    # partial matched crossover
    offspring = []
    idx = 0
    while len(offspring) != offspring_size[0]:
        parent1 = parents[idx % parents.shape[0], :].copy()
        parent2 = parents[(idx + 1) % parents.shape[0], :].copy()
        sp1, sp2 = sorted(random.sample(range(offspring_size[1]), 2))
        fa = [i for i in range(offspring_size[1] + 1)]
        for i in range(sp1, sp2 + 1):
            fa[parent2[i]] = parent1[i]
        for i in range(offspring_size[1]):
            if sp1 <= i and i <= sp2:
                continue
            parent1[i] = findFa(parent1[i], fa)
        parent1[sp1 : sp2 + 1] = parent2[sp1 : sp2 + 1]
        assert(sorted(parent1) == [i for i in range(1, offspring_size[1] + 1)])
        offspring.append(parent1)
        idx += 1
    return numpy.array(offspring)
def onGeneration(instance):
    # print("Generation", instance.generations_completed)
    # print(instance.population)
    pop = instance.population
    solution, solution_fitness, i = instance.best_solution()
    p = [pop[i, j] if j > -1 else 0 for j in range(-1, pop.shape[1])]
    tmp, p = ZK().ZKD(p[:])
    pop[i, :] = numpy.array(p[1:])
def GA():
    sys, R = fetch()
    instance = pygad.GA(num_generations=100,
                        num_parents_mating=2,
                        sol_per_pop=10,
                        num_genes=sys.n,
                        init_range_low=1,
                        init_range_high=sys.n + 1,
                        parent_selection_type="rws",
                        crossover_type=crossoverFunc,
                        mutation_type="swap",
                        mutation_percent_genes=20,
                        keep_elitism=2, # save the best to the next gen
                        fitness_func=fitnessFunc,
                        gene_type=int,
                        allow_duplicate_genes=False,
                        on_generation=onGeneration,
                        on_start=onGeneration)
    instance.run()
    solution, solution_fitness, solution_idx = instance.best_solution()
    # print("Parameters of the best solution : {solution}".format(solution=solution))
    # print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
    # print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))
    return solution_fitness, solution

def main():
    n = 7
    k = 3
    testCases = 100
    avgLKA, avgLKB, avgLKC, avgLKD = 0, 0, 0, 0
    avgZKA, avgZKB, avgZKC, avgZKD = 0, 0, 0, 0
    avgBIT = 0
    avgSA = 0
    avgGA = 0

    for t in range(0, testCases):
        global sys, R # declare global variable
        R = [0.99 - random.random() * 0.19 for i in range(0, n)] # high
        # R = [0.01 + random.random() * 0.19 for i in range(0, n)] # low
        # R = [0.01 + random.random() * 0.98 for i in range(0, n)] # arbitrary

        R[1:] = sorted(R)
        sys = model.System(n, k, R)
        print("Running on %d/%d" % (t + 1, testCases))

        mx, mn = BF().bruteForce()

        a, p1 = LK().LKA()
        avgLKA += (a - mn) / (mx - mn)
        b, p2 = LK().LKB()
        avgLKB += (b - mn) / (mx - mn)
        c, p = LK().LKC()
        avgLKC += (c - mn) / (mx - mn)
        d, p = LK().LKD()
        avgLKD += (d - mn) / (mx - mn)

        a1, p = ZK().ZKA(p1[:])
        a2, p = ZK().ZKA(p2[:])
        avgZKA += (max(a1, a2) - mn) / (mx - mn)
        b1, p = ZK().ZKB(p1[:])
        b2, p = ZK().ZKB(p2[:])
        avgZKB += (max(b1, b2) - mn) / (mx - mn)
        c1, p = ZK().ZKC(p1[:])
        c2, p = ZK().ZKC(p2[:])
        avgZKC += (max(c1, c2) - mn) / (mx - mn)
        d1, p = ZK().ZKD(p1[:])
        d2, p = ZK().ZKD(p2[:])
        avgZKD += (max(d1, d2) - mn) / (mx - mn)

        b, p = BIT().BIT()
        avgBIT += (b - mn) / (mx - mn)

        a, p = SA().SA()
        avgSA += (a - mn) / (mx - mn)

        a, p = GA()
        avgGA += (a - mn) / (mx - mn)

    print("LK: ", avgLKA / testCases, avgLKB / testCases, avgLKC / testCases, avgLKD / testCases)
    print("ZK: ", avgZKA / testCases, avgZKB / testCases, avgZKC / testCases, avgZKD / testCases)
    print("BIT: ", avgBIT / testCases)
    print("SA: ", avgSA / testCases)
    print("GA: ", avgGA / testCases)

if __name__ == "__main__":
    main()