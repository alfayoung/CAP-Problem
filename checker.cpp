#include <bits/stdc++.h>
using namespace std;
const int maxn = 1000005;
int n, m;
double f[maxn]; // probabilty not conducted
double p[maxn];
int deg[maxn];
int head[maxn], nxt[maxn], tail[maxn], ecnt;

void addedge(int u, int v) {
	nxt[++ecnt] = head[u];
	head[u] = ecnt;
	tail[ecnt] = v;
}

double solve() {
	for (int i = 1; i <= n; i++) f[i] = 1;
	queue<int> que;
	que.push(1);
	f[1] = 0; p[1] = 1;
	while (!que.empty()) {
		int u = que.front(); que.pop();
		for (int e = head[u]; e; e = nxt[e]) {
			int v = tail[e];
			f[v] = f[v] * (f[u] + (1 - f[u]) * (1 - p[u]));
			if (--deg[v] == 0) que.push(v);
		}
	}
	return 1 - f[n];
}

int main() {
	cin >> n >> m;
	for (int i = 2; i <= n - 1; i++) cin >> p[i];
	for (int i = 1; i <= m; i++) {
		int u, v; cin >> u >> v;
		addedge(u, v);
		deg[v]++;
	}
	cout << solve() << endl;
	return 0;
}
