# C++ 算法模板库

可直接复制使用的算法模板集合，考前快速复习用。

## 基础主函数

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;

const int INF = 0x3f3f3f3f;
const ll LINF = 4e18;
const int MOD = 1e9 + 7;

void solve() {
    // 主逻辑
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    solve();
    return 0;
}
```

**多组测试**：
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

---

## 二分查找

### 查找第一个 >= x

```cpp
int lower_bound_manual(const vector<int>& a, int x) {
    int l = 0, r = a.size();
    while (l < r) {
        int m = l + (r - l) / 2;
        if (a[m] >= x) r = m;
        else l = m + 1;
    }
    return l;
}
```

### 二分答案 - 最小可行

```cpp
bool check(long long x) {
    return true; // 判断 x 是否可行
}

long long binary_min(long long l, long long r) {
    while (l < r) {
        long long m = l + (r - l) / 2;
        if (check(m)) r = m;
        else l = m + 1;
    }
    return l;
}
```

### 二分答案 - 最大可行

```cpp
long long binary_max(long long l, long long r) {
    while (l < r) {
        long long m = l + (r - l + 1) / 2;
        if (check(m)) l = m;
        else r = m - 1;
    }
    return l;
}
```

---

## 前缀和与差分

### 一维前缀和

```cpp
vector<ll> pre(n + 1, 0);
for (int i = 0; i < n; ++i) {
    pre[i + 1] = pre[i] + a[i];
}

// 查询 [l, r]
ll sum = pre[r + 1] - pre[l];
```

### 二维前缀和

```cpp
vector<vector<ll>> pre(n + 1, vector<ll>(m + 1, 0));
for (int i = 0; i < n; ++i) {
    for (int j = 0; j < m; ++j) {
        pre[i + 1][j + 1] = pre[i][j + 1] + pre[i + 1][j] 
                          - pre[i][j] + mat[i][j];
    }
}

// 查询 (x1,y1) 到 (x2,y2)
ll sum = pre[x2 + 1][y2 + 1] - pre[x1][y2 + 1] 
       - pre[x2 + 1][y1] + pre[x1][y1];
```

### 差分数组

```cpp
vector<ll> diff(n + 1, 0);

// 区间 [l, r] 加 v
diff[l] += v;
diff[r + 1] -= v;

// 还原
vector<ll> a(n);
ll sum = 0;
for (int i = 0; i < n; ++i) {
    sum += diff[i];
    a[i] = sum;
}
```

---

## 单调栈与单调队列

### 下一个更大元素

```cpp
vector<int> next_greater(n, -1);
stack<int> st;

for (int i = 0; i < n; ++i) {
    while (!st.empty() && a[st.top()] < a[i]) {
        next_greater[st.top()] = i;
        st.pop();
    }
    st.push(i);
}
```

### 滑动窗口最大值

```cpp
deque<int> dq;
vector<int> ans;

for (int i = 0; i < n; ++i) {
    while (!dq.empty() && dq.front() <= i - k) dq.pop_front();
    while (!dq.empty() && a[dq.back()] <= a[i]) dq.pop_back();
    dq.push_back(i);
    if (i >= k - 1) ans.push_back(a[dq.front()]);
}
```

---

## DFS 与 BFS

### DFS 网格

```cpp
int n, m;
vector<vector<int>> vis;
int dx[4] = {1, -1, 0, 0};
int dy[4] = {0, 0, 1, -1};

bool inside(int x, int y) {
    return x >= 0 && x < n && y >= 0 && y < m;
}

void dfs(int x, int y) {
    vis[x][y] = 1;
    for (int d = 0; d < 4; ++d) {
        int nx = x + dx[d], ny = y + dy[d];
        if (!inside(nx, ny) || vis[nx][ny]) continue;
        dfs(nx, ny);
    }
}
```

### BFS 网格最短路

```cpp
vector<vector<int>> dist(n, vector<int>(m, -1));
queue<pii> q;

dist[sx][sy] = 0;
q.push({sx, sy});

while (!q.empty()) {
    auto [x, y] = q.front();
    q.pop();
    
    for (int d = 0; d < 4; ++d) {
        int nx = x + dx[d], ny = y + dy[d];
        if (!inside(nx, ny) || dist[nx][ny] != -1) continue;
        dist[nx][ny] = dist[x][y] + 1;
        q.push({nx, ny});
    }
}
```

---

## 回溯

### 组合

```cpp
vector<int> path;
vector<vector<int>> ans;

void backtrack(int start, int n, int k) {
    if ((int)path.size() == k) {
        ans.push_back(path);
        return;
    }
    for (int i = start; i <= n; ++i) {
        path.push_back(i);
        backtrack(i + 1, n, k);
        path.pop_back();
    }
}
```

### 排列

```cpp
vector<int> path, used;
vector<vector<int>> ans;

void permute(vector<int>& nums) {
    if (path.size() == nums.size()) {
        ans.push_back(path);
        return;
    }
    for (int i = 0; i < (int)nums.size(); ++i) {
        if (used[i]) continue;
        used[i] = 1;
        path.push_back(nums[i]);
        permute(nums);
        path.pop_back();
        used[i] = 0;
    }
}
```

---

## 并查集

```cpp
struct DSU {
    vector<int> p, sz;
    
    DSU(int n) : p(n), sz(n, 1) {
        iota(p.begin(), p.end(), 0);
    }
    
    int find(int x) {
        return p[x] == x ? x : p[x] = find(p[x]);
    }
    
    bool unite(int a, int b) {
        a = find(a); b = find(b);
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

---

## 拓扑排序

```cpp
vector<int> topo_sort(int n, vector<vector<int>>& g) {
    vector<int> indeg(n, 0);
    for (int u = 0; u < n; ++u) {
        for (int v : g[u]) indeg[v]++;
    }
    
    queue<int> q;
    for (int i = 0; i < n; ++i) {
        if (indeg[i] == 0) q.push(i);
    }
    
    vector<int> order;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        order.push_back(u);
        for (int v : g[u]) {
            if (--indeg[v] == 0) q.push(v);
        }
    }
    
    return order; // size < n 说明有环
}
```

---

## Dijkstra 最短路

```cpp
vector<ll> dijkstra(int n, int s, vector<vector<pii>>& g) {
    vector<ll> dist(n, LINF);
    priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<>> pq;
    
    dist[s] = 0;
    pq.push({0, s});
    
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
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

---

## Floyd 全源最短路

```cpp
vector<vector<ll>> dist(n, vector<ll>(n, LINF));
for (int i = 0; i < n; ++i) dist[i][i] = 0;

// 添加边
for (auto [u, v, w] : edges) {
    dist[u][v] = min(dist[u][v], (ll)w);
}

for (int k = 0; k < n; ++k) {
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (dist[i][k] != LINF && dist[k][j] != LINF) {
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);
            }
        }
    }
}
```

---

## 动态规划

### 0/1 背包

```cpp
vector<ll> dp(W + 1, 0);

for (int i = 0; i < n; ++i) {
    for (int w = W; w >= weight[i]; --w) {
        dp[w] = max(dp[w], dp[w - weight[i]] + value[i]);
    }
}
```

### 完全背包

```cpp
vector<ll> dp(W + 1, 0);

for (int i = 0; i < n; ++i) {
    for (int w = weight[i]; w <= W; ++w) {
        dp[w] = max(dp[w], dp[w - weight[i]] + value[i]);
    }
}
```

### LIS (最长上升子序列)

```cpp
vector<int> tails;
for (int x : a) {
    auto it = lower_bound(tails.begin(), tails.end(), x);
    if (it == tails.end()) tails.push_back(x);
    else *it = x;
}
int lis_len = tails.size();
```

---

## 树状数组

```cpp
struct Fenwick {
    int n;
    vector<ll> bit;
    
    Fenwick(int n) : n(n), bit(n + 1, 0) {}
    
    void add(int idx, ll val) {
        for (++idx; idx <= n; idx += idx & -idx) 
            bit[idx] += val;
    }
    
    ll sum(int idx) {
        ll res = 0;
        for (++idx; idx > 0; idx -= idx & -idx) 
            res += bit[idx];
        return res;
    }
    
    ll range_sum(int l, int r) {
        return sum(r) - (l == 0 ? 0 : sum(l - 1));
    }
};
```

---

## 线段树

```cpp
struct SegTree {
    int n;
    vector<ll> tr;
    
    SegTree(const vector<int>& a) : n(a.size()), tr(n * 4, 0) {
        build(1, 0, n - 1, a);
    }
    
    void build(int o, int l, int r, const vector<int>& a) {
        if (l == r) { tr[o] = a[l]; return; }
        int m = (l + r) / 2;
        build(o * 2, l, m, a);
        build(o * 2 + 1, m + 1, r, a);
        tr[o] = tr[o * 2] + tr[o * 2 + 1];
    }
    
    void update(int o, int l, int r, int idx, int val) {
        if (l == r) { tr[o] = val; return; }
        int m = (l + r) / 2;
        if (idx <= m) update(o * 2, l, m, idx, val);
        else update(o * 2 + 1, m + 1, r, idx, val);
        tr[o] = tr[o * 2] + tr[o * 2 + 1];
    }
    
    ll query(int o, int l, int r, int ql, int qr) {
        if (ql <= l && r <= qr) return tr[o];
        int m = (l + r) / 2;
        ll res = 0;
        if (ql <= m) res += query(o * 2, l, m, ql, qr);
        if (qr > m) res += query(o * 2 + 1, m + 1, r, ql, qr);
        return res;
    }
};
```

---

## 数学

### GCD 和 LCM

```cpp
ll gcd(ll a, ll b) {
    return b == 0 ? a : gcd(b, a % b);
}

ll lcm(ll a, ll b) {
    return a / gcd(a, b) * b;
}
```

### 快速幂

```cpp
ll mod_pow(ll a, ll e, ll mod) {
    ll r = 1 % mod;
    a %= mod;
    while (e > 0) {
        if (e & 1) r = r * a % mod;
        a = a * a % mod;
        e >>= 1;
    }
    return r;
}
```

### 埃氏筛

```cpp
vector<int> primes;
vector<bool> is_prime(n + 1, true);
is_prime[0] = is_prime[1] = false;

for (int i = 2; i <= n; ++i) {
    if (is_prime[i]) {
        primes.push_back(i);
        if ((ll)i * i <= n) {
            for (ll j = 1LL * i * i; j <= n; j += i) {
                is_prime[j] = false;
            }
        }
    }
}
```

---

## 位运算

```cpp
// 基本操作
x & 1              // 判断奇偶
x & (x - 1)        // 清除最低位的 1
x & -x             // 保留最低位的 1
x | (1 << k)       // 第 k 位置 1
x & ~(1 << k)      // 第 k 位置 0
x ^ (1 << k)       // 第 k 位翻转
(x >> k) & 1       // 取第 k 位

// 统计 1 的个数
__builtin_popcount(x)      // int
__builtin_popcountll(x)    // long long

// 枚举子集
for (int s = mask; s; s = (s - 1) & mask) {
    // s 是 mask 的子集
}
```

---

## 常用技巧

### 坐标离散化

```cpp
vector<int> vals = coords;
sort(vals.begin(), vals.end());
vals.erase(unique(vals.begin(), vals.end()), vals.end());

for (int& x : coords) {
    x = lower_bound(vals.begin(), vals.end(), x) - vals.begin();
}
```

### 读到 EOF

```cpp
int n;
while (cin >> n) {
    // 处理
}

string line;
while (getline(cin, line)) {
    // 处理
}
```

### 输出格式

```cpp
// 行末无空格
for (int i = 0; i < n; ++i) {
    cout << a[i] << " \n"[i == n - 1];
}

// 固定精度
cout << fixed << setprecision(2) << x << "\n";
```
