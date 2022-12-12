#include <bits/stdc++.h>
using namespace std;

mt19937_64 gen(chrono::steady_clock::now().time_since_epoch().count());

// assume 1 -> S   n -> T

int getRand(int l, int r) {
	return uniform_int_distribution<int>(l, r)(gen);
}

double getRandP(double l, double r) {
	return uniform_real_distribution<double>(l, r)(gen);
}

void construct(int n, int m) {
	srand(time(0));
	set<pair<int, int> > edges;
	
	// L + n - 2 <= m
	int L = getRand(1, min(n - 2, m - n + 2));

	set<int> leafs; leafs.insert(n - 1);
	while (leafs.size() < L) leafs.insert(getRand(2, n - 2));
	for (auto x : leafs) cerr << x << endl;
		
	set<int> used;
	for (int i = n - 1; i > 1; i--) {
		set<int>::iterator it1 = used.find(i - 1), it2 = leafs.find(i - 1);
		if (it1 == used.end() && it2 == leafs.end()) {
			edges.insert(make_pair(i - 1, i));
			used.insert(i - 1);
		} else {
			for (;;) {
				int fa = getRand(1, i - 1); it2 = leafs.find(fa);
				if (it2 != leafs.end()) continue;
				edges.insert(make_pair(fa, i));
				used.insert(fa);
				break;
			}
		}
	}
		
	for (int leaf : leafs) edges.insert(make_pair(leaf, getRand(leaf + 1, n)));
	
	while (edges.size() < m) {
		int x = getRand(1, n), y = getRand(1, n);
		if (x == y) continue;
		else if (x > y) swap(x, y);
		edges.insert(make_pair(x, y));
	}
	
	for (auto e : edges) cout << e.first << " " << e.second << endl;
}

int main() {
	construct(100, 233);
	return 0;
}
