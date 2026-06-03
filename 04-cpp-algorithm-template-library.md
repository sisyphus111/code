# C++ 算法模板库

这份模板库用于两件事：

- 平时训练时反复默写，直到不需要查资料。
- 考前复习时快速检查自己是否能完整写出来。

模板不是越多越好。你应该先掌握“必背模板”，再根据目标学校难度补充“进阶模板”。

## 基础主函数

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;

const int INF = 0x3f3f3f3f;
const ll LINF = 4e18;

void solve() {
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    solve();
    return 0;
}
```

多组：

```cpp
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while (T--) solve();
    return 0;
}
```

## 二分

找第一个 `>= x` 的位置：

```cpp
int lower_bound_manual(const vector<int>& a, int x) {
    int l = 0, r = a.size(); // [l, r)
    while (l < r) {
        int m = l + (r - l) / 2;
        if (a[m] >= x) r = m;
        else l = m + 1;
    }
    return l;
}
```

二分答案，找最小可行：

```cpp
bool check(long long x) {
    return true;
}

long long binary_answer_min(long long l, long long r) {
    while (l < r) {
        long long m = l + (r - l) / 2;
        if (check(m)) r = m;
        else l = m + 1;
    }
    return l;
}
```

二分答案，找最大可行：

```cpp
long long binary_answer_max(long long l, long long r) {
    while (l < r) {
        long long m = l + (r - l + 1) / 2;
        if (check(m)) l = m;
        else r = m - 1;
    }
    return l;
}
```

## 前缀和

一维：

```cpp
vector<long long> pre(n + 1, 0);
for (int i = 0; i < n; ++i) {
    pre[i + 1] = pre[i] + a[i];
}

auto range_sum = [&](int l, int r) {
    return pre[r + 1] - pre[l];
};
```

二维：

```cpp
vector<vector<long long>> pre(n + 1, vector<long long>(m + 1, 0));
for (int i = 0; i < n; ++i) {
    for (int j = 0; j < m; ++j) {
        pre[i + 1][j + 1] = pre[i][j + 1] + pre[i + 1][j] - pre[i][j] + a[i][j];
    }
}

auto sum_rect = [&](int x1, int y1, int x2, int y2) {
    return pre[x2 + 1][y2 + 1] - pre[x1][y2 + 1] - pre[x2 + 1][y1] + pre[x1][y1];
};
```

## 差分

```cpp
vector<long long> diff(n + 1, 0);

auto add_range = [&](int l, int r, long long v) {
    diff[l] += v;
    if (r + 1 < n) diff[r + 1] -= v;
};

vector<long long> a(n);
long long cur = 0;
for (int i = 0; i < n; ++i) {
    cur += diff[i];
    a[i] = cur;
}
```

## 滑动窗口

最长满足条件窗口：

```cpp
int ans = 0;
int l = 0;
for (int r = 0; r < n; ++r) {
    // add a[r]
    while (/* window invalid */) {
        // remove a[l]
        ++l;
    }
    ans = max(ans, r - l + 1);
}
```

最短满足条件窗口：

```cpp
int ans = INF;
int l = 0;
for (int r = 0; r < n; ++r) {
    // add a[r]
    while (/* window valid */) {
        ans = min(ans, r - l + 1);
        // remove a[l]
        ++l;
    }
}
```

## 单调栈

下一个更大元素：

```cpp
vector<int> next_greater(n, -1);
stack<int> st; // store indices

for (int i = 0; i < n; ++i) {
    while (!st.empty() && a[st.top()] < a[i]) {
        next_greater[st.top()] = i;
        st.pop();
    }
    st.push(i);
}
```

左侧第一个更小元素：

```cpp
vector<int> left_less(n, -1);
stack<int> st;

for (int i = 0; i < n; ++i) {
    while (!st.empty() && a[st.top()] >= a[i]) st.pop();
    if (!st.empty()) left_less[i] = st.top();
    st.push(i);
}
```

## 单调队列

滑动窗口最大值：

```cpp
deque<int> dq; // store indices
vector<int> ans;

for (int i = 0; i < n; ++i) {
    while (!dq.empty() && dq.front() <= i - k) dq.pop_front();
    while (!dq.empty() && a[dq.back()] <= a[i]) dq.pop_back();
    dq.push_back(i);
    if (i >= k - 1) ans.push_back(a[dq.front()]);
}
```

## DFS 网格

```cpp
int n, m;
vector<string> grid;
vector<vector<int>> vis;
int dx[4] = {1, -1, 0, 0};
int dy[4] = {0, 0, 1, -1};

bool inside(int x, int y) {
    return 0 <= x && x < n && 0 <= y && y < m;
}

void dfs(int x, int y) {
    vis[x][y] = 1;
    for (int d = 0; d < 4; ++d) {
        int nx = x + dx[d], ny = y + dy[d];
        if (!inside(nx, ny)) continue;
        if (vis[nx][ny]) continue;
        if (grid[nx][ny] == '#') continue;
        dfs(nx, ny);
    }
}
```

## BFS 网格最短路

```cpp
vector<vector<int>> dist(n, vector<int>(m, -1));
queue<pair<int, int>> q;

dist[sx][sy] = 0;
q.push({sx, sy});

while (!q.empty()) {
    auto [x, y] = q.front();
    q.pop();
    for (int d = 0; d < 4; ++d) {
        int nx = x + dx[d], ny = y + dy[d];
        if (!inside(nx, ny)) continue;
        if (dist[nx][ny] != -1) continue;
        if (grid[nx][ny] == '#') continue;
        dist[nx][ny] = dist[x][y] + 1;
        q.push({nx, ny});
    }
}
```

## 回溯

组合：

```cpp
vector<int> path;
vector<vector<int>> ans;

void backtrack(int start, int n, int k) {
    if ((int)path.size() == k) {
        ans.push_back(path);
        return;
    }
    for (int i = start; i <= n; ++i) {
        if ((int)path.size() + (n - i + 1) < k) break;
        path.push_back(i);
        backtrack(i + 1, n, k);
        path.pop_back();
    }
}
```

排列：

```cpp
vector<int> nums, path, used;
vector<vector<int>> ans;

void permute() {
    if ((int)path.size() == (int)nums.size()) {
        ans.push_back(path);
        return;
    }
    for (int i = 0; i < (int)nums.size(); ++i) {
        if (used[i]) continue;
        used[i] = 1;
        path.push_back(nums[i]);
        permute();
        path.pop_back();
        used[i] = 0;
    }
}
```

## 并查集

```cpp
struct DSU {
    vector<int> p, sz;

    DSU(int n) : p(n), sz(n, 1) {
        iota(p.begin(), p.end(), 0);
    }

    int find(int x) {
        if (p[x] == x) return x;
        return p[x] = find(p[x]);
    }

    bool unite(int a, int b) {
        a = find(a);
        b = find(b);
        if (a == b) return false;
        if (sz[a] < sz[b]) swap(a, b);
        p[b] = a;
        sz[a] += sz[b];
        return true;
    }

    bool same(int a, int b) {
        return find(a) == find(b);
    }
};
```

## 拓扑排序

```cpp
vector<int> topo_sort(int n, vector<vector<int>>& g) {
    vector<int> indeg(n, 0);
    for (int u = 0; u < n; ++u) {
        for (int v : g[u]) ++indeg[v];
    }

    queue<int> q;
    for (int i = 0; i < n; ++i) {
        if (indeg[i] == 0) q.push(i);
    }

    vector<int> order;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        order.push_back(u);
        for (int v : g[u]) {
            if (--indeg[v] == 0) q.push(v);
        }
    }
    return order; // size < n means there is a cycle
}
```

## Dijkstra

```cpp
vector<long long> dijkstra(int n, int s, vector<vector<pair<int, int>>>& g) {
    vector<long long> dist(n, LINF);
    priority_queue<pair<long long, int>,
                   vector<pair<long long, int>>,
                   greater<pair<long long, int>>> pq;

    dist[s] = 0;
    pq.push({0, s});

    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d != dist[u]) continue;

        for (auto [v, w] : g[u]) {
            if (dist[v] > d + w) {
                dist[v] = d + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
```

## Floyd

适合 `n <= 400-500` 的任意两点最短路。

```cpp
vector<vector<long long>> dist(n, vector<long long>(n, LINF));
for (int i = 0; i < n; ++i) dist[i][i] = 0;

for (auto [u, v, w] : edges) {
    dist[u][v] = min(dist[u][v], (long long)w);
}

for (int k = 0; k < n; ++k) {
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (dist[i][k] == LINF || dist[k][j] == LINF) continue;
            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);
        }
    }
}
```

## Kruskal 最小生成树

```cpp
struct Edge {
    int u, v, w;
};

long long kruskal(int n, vector<Edge>& edges) {
    sort(edges.begin(), edges.end(), [](const Edge& a, const Edge& b) {
        return a.w < b.w;
    });

    DSU dsu(n);
    long long cost = 0;
    int cnt = 0;
    for (auto [u, v, w] : edges) {
        if (dsu.unite(u, v)) {
            cost += w;
            ++cnt;
        }
    }
    if (cnt != n - 1) return -1;
    return cost;
}
```

## 01 背包

```cpp
vector<long long> dp(W + 1, 0);

for (int i = 0; i < n; ++i) {
    for (int cap = W; cap >= weight[i]; --cap) {
        dp[cap] = max(dp[cap], dp[cap - weight[i]] + value[i]);
    }
}
```

## 完全背包

```cpp
vector<long long> dp(W + 1, 0);

for (int i = 0; i < n; ++i) {
    for (int cap = weight[i]; cap <= W; ++cap) {
        dp[cap] = max(dp[cap], dp[cap - weight[i]] + value[i]);
    }
}
```

## LIS

`O(n log n)` 求长度：

```cpp
vector<int> tails;
for (int x : a) {
    auto it = lower_bound(tails.begin(), tails.end(), x);
    if (it == tails.end()) tails.push_back(x);
    else *it = x;
}
int lis = tails.size();
```

严格上升用 `lower_bound`，非严格上升用 `upper_bound`。

## 树上 DFS

```cpp
vector<vector<int>> g;
vector<int> parent, depth, sub_size;

void dfs_tree(int u, int p) {
    parent[u] = p;
    sub_size[u] = 1;
    for (int v : g[u]) {
        if (v == p) continue;
        depth[v] = depth[u] + 1;
        dfs_tree(v, u);
        sub_size[u] += sub_size[v];
    }
}
```

## 树状数组

```cpp
struct Fenwick {
    int n;
    vector<long long> bit;

    Fenwick(int n) : n(n), bit(n + 1, 0) {}

    void add(int idx, long long val) {
        for (++idx; idx <= n; idx += idx & -idx) bit[idx] += val;
    }

    long long sum_prefix(int idx) {
        long long res = 0;
        for (++idx; idx > 0; idx -= idx & -idx) res += bit[idx];
        return res;
    }

    long long sum_range(int l, int r) {
        if (r < l) return 0;
        return sum_prefix(r) - (l == 0 ? 0 : sum_prefix(l - 1));
    }
};
```

## 线段树：区间和 + 单点改

```cpp
struct SegTree {
    int n;
    vector<long long> tr;

    SegTree(const vector<int>& a) {
        n = a.size();
        tr.assign(n * 4, 0);
        build(1, 0, n - 1, a);
    }

    void build(int o, int l, int r, const vector<int>& a) {
        if (l == r) {
            tr[o] = a[l];
            return;
        }
        int m = (l + r) / 2;
        build(o * 2, l, m, a);
        build(o * 2 + 1, m + 1, r, a);
        tr[o] = tr[o * 2] + tr[o * 2 + 1];
    }

    void update(int o, int l, int r, int idx, int val) {
        if (l == r) {
            tr[o] = val;
            return;
        }
        int m = (l + r) / 2;
        if (idx <= m) update(o * 2, l, m, idx, val);
        else update(o * 2 + 1, m + 1, r, idx, val);
        tr[o] = tr[o * 2] + tr[o * 2 + 1];
    }

    long long query(int o, int l, int r, int ql, int qr) {
        if (ql <= l && r <= qr) return tr[o];
        int m = (l + r) / 2;
        long long res = 0;
        if (ql <= m) res += query(o * 2, l, m, ql, qr);
        if (qr > m) res += query(o * 2 + 1, m + 1, r, ql, qr);
        return res;
    }
};
```

## 快速幂

```cpp
long long mod_pow(long long a, long long e, long long mod) {
    long long r = 1 % mod;
    a %= mod;
    while (e > 0) {
        if (e & 1) r = r * a % mod;
        a = a * a % mod;
        e >>= 1;
    }
    return r;
}
```

## 埃氏筛

```cpp
vector<int> primes;
vector<bool> is_prime(n + 1, true);
if (n >= 0) is_prime[0] = false;
if (n >= 1) is_prime[1] = false;

for (int i = 2; i <= n; ++i) {
    if (is_prime[i]) {
        primes.push_back(i);
        if ((long long)i * i <= n) {
            for (long long j = 1LL * i * i; j <= n; j += i) {
                is_prime[j] = false;
            }
        }
    }
}
```

## 子集枚举

枚举所有子集：

```cpp
for (int mask = 0; mask < (1 << n); ++mask) {
    for (int i = 0; i < n; ++i) {
        if (mask >> i & 1) {
            // choose i
        }
    }
}
```

枚举一个 mask 的所有非空子集：

```cpp
for (int sub = mask; sub; sub = (sub - 1) & mask) {
    // sub is a non-empty subset of mask
}
```

## 坐标离散化

```cpp
vector<int> vals = a;
sort(vals.begin(), vals.end());
vals.erase(unique(vals.begin(), vals.end()), vals.end());

for (int& x : a) {
    x = lower_bound(vals.begin(), vals.end(), x) - vals.begin();
}
```

## 模板默写计划

第一轮：看着材料抄一遍。  
第二轮：隔天不看材料写一遍。  
第三轮：用模板解决真实题。  
第四轮：限时 10 分钟内写出关键模板。

优先级：

1. 二分、前缀和、BFS、DFS、并查集。
2. Dijkstra、拓扑排序、背包、LIS。
3. 单调栈、单调队列、树状数组、线段树。
