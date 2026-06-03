# C++ STL 与常用数据结构速查

这份材料按“机试时应该怎么用”整理，默认使用 C++17。代码模板里会使用：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    return 0;
}
```

`bits/stdc++.h` 在多数 OJ 的 GCC/Clang 环境可用；如果目标平台明确不支持，就改成精确 include。

## 常用类型与别名

```cpp
using ll = long long;
using pii = pair<int, int>;
using pll = pair<long long, long long>;

const int INF = 0x3f3f3f3f;
const long long LINF = 4e18;
const int MOD = 1'000'000'007;
```

## `vector`

适合：动态数组、邻接表、二维矩阵、排序。

常用操作：

```cpp
vector<int> a;
a.push_back(3);
a.pop_back();
a.size();
a.empty();
a.clear();
a.resize(n);
a.assign(n, 0);
a.back();
a[i];
```

初始化：

```cpp
vector<int> a(n);
vector<int> b(n, -1);
vector<vector<int>> grid(n, vector<int>(m, 0));
```

遍历：

```cpp
for (int x : a) {}
for (int i = 0; i < (int)a.size(); ++i) {}
```

排序与去重：

```cpp
sort(a.begin(), a.end());
a.erase(unique(a.begin(), a.end()), a.end());
```

易错点：

- `a.size()` 是无符号类型，和 `int` 混用时建议强转。
- `erase` 中间元素是 `O(n)`。
- `resize(n)` 保留已有元素并补默认值；`assign(n, x)` 会重置全部元素。

## `string`

常用操作：

```cpp
string s;
cin >> s;             // 读到空白停止
getline(cin, s);      // 读整行
s.size();
s.empty();
s[i];
s.substr(pos, len);
s.find("abc");
s.push_back('x');
s.pop_back();
reverse(s.begin(), s.end());
```

字符处理：

```cpp
isdigit(c);
isalpha(c);
tolower(c);
toupper(c);
```

注意：这些函数参数最好转成 `unsigned char` 或保证字符非负，普通 ASCII 题通常没问题。

## `pair`、`tuple`、结构体

```cpp
pair<int, int> p = {1, 2};
cout << p.first << " " << p.second << "\n";
```

`pair` 默认按字典序比较：先比 `first`，再比 `second`。

结构体排序：

```cpp
struct Node {
    int score;
    string name;
};

sort(v.begin(), v.end(), [](const Node& a, const Node& b) {
    if (a.score != b.score) return a.score > b.score;
    return a.name < b.name;
});
```

## `deque`

适合：两端插入删除、单调队列。

```cpp
deque<int> q;
q.push_back(x);
q.push_front(x);
q.pop_back();
q.pop_front();
q.front();
q.back();
```

## `stack`

适合：括号、表达式、单调栈。

```cpp
stack<int> st;
st.push(x);
st.top();
st.pop();
st.empty();
st.size();
```

注意：`stack` 不能遍历。如果需要遍历，用 `vector` 模拟栈。

## `queue`

适合：BFS。

```cpp
queue<int> q;
q.push(x);
q.front();
q.pop();
q.empty();
```

BFS 常用写法：

```cpp
queue<int> q;
vector<int> dist(n, -1);
dist[s] = 0;
q.push(s);

while (!q.empty()) {
    int u = q.front();
    q.pop();
    for (int v : g[u]) {
        if (dist[v] != -1) continue;
        dist[v] = dist[u] + 1;
        q.push(v);
    }
}
```

## `priority_queue`

默认大根堆：

```cpp
priority_queue<int> pq;
pq.push(x);
pq.top();
pq.pop();
```

小根堆：

```cpp
priority_queue<int, vector<int>, greater<int>> pq;
```

存 pair：

```cpp
priority_queue<pair<int, int>> pq; // 先按 first 大，再按 second 大
```

Dijkstra 小根堆：

```cpp
using P = pair<long long, int>; // dist, node
priority_queue<P, vector<P>, greater<P>> pq;
```

自定义比较：

```cpp
struct Cmp {
    bool operator()(const Node& a, const Node& b) const {
        return a.cost > b.cost; // cost 小的优先
    }
};
priority_queue<Node, vector<Node>, Cmp> pq;
```

注意：`priority_queue` 的比较器语义容易反，`return a.cost > b.cost` 表示小根堆。

## `set` / `multiset`

适合：有序去重、前驱后继、动态维护有序集合。

```cpp
set<int> s;
s.insert(x);
s.erase(x);
s.count(x);
s.find(x);
s.lower_bound(x); // 第一个 >= x
s.upper_bound(x); // 第一个 > x
```

`multiset` 允许重复。删除一个元素：

```cpp
auto it = ms.find(x);
if (it != ms.end()) ms.erase(it);
```

注意：`ms.erase(x)` 会删除所有等于 `x` 的元素。

## `map` / `unordered_map`

`map` 有序，`unordered_map` 平均更快但无序。

```cpp
map<string, int> mp;
mp["alice"]++;

if (mp.count("bob")) {}

auto it = mp.find("bob");
if (it != mp.end()) {}
```

遍历：

```cpp
for (auto [key, val] : mp) {
    cout << key << " " << val << "\n";
}
```

`unordered_map` 提速：

```cpp
unordered_map<int, int> mp;
mp.reserve(n * 2);
mp.max_load_factor(0.7);
```

注意：

- 只判断存在性时，不要写 `mp[x]`，会插入默认值。
- `unordered_map` 不能按 key 有序遍历。
- pair/vector 作为 key 时需要自定义 hash。

## `bitset`

适合：固定长度布尔集合、位运算优化。

```cpp
bitset<1000> b;
b.set(i);
b.reset(i);
b.flip(i);
b.test(i);
b.count();
```

## `algorithm` 常用函数

排序：

```cpp
sort(a.begin(), a.end());
sort(a.rbegin(), a.rend());
stable_sort(a.begin(), a.end(), cmp);
```

二分：

```cpp
auto it = lower_bound(a.begin(), a.end(), x);
int pos = it - a.begin();
```

最大最小：

```cpp
min(a, b);
max(a, b);
min_element(v.begin(), v.end());
max_element(v.begin(), v.end());
```

累加：

```cpp
long long sum = accumulate(v.begin(), v.end(), 0LL);
```

排列：

```cpp
sort(a.begin(), a.end());
do {
    // use a
} while (next_permutation(a.begin(), a.end()));
```

反转、填充：

```cpp
reverse(a.begin(), a.end());
fill(a.begin(), a.end(), 0);
```

## 数学函数

```cpp
gcd(a, b);      // <numeric>, C++17
lcm(a, b);      // <numeric>, C++17
abs(x);
sqrt(x);
pow(a, b);
```

快速幂取模：

```cpp
long long mod_pow(long long a, long long e, long long mod) {
    long long r = 1 % mod;
    while (e > 0) {
        if (e & 1) r = r * a % mod;
        a = a * a % mod;
        e >>= 1;
    }
    return r;
}
```

## 并查集

适合：连通性、合并集合、最小生成树 Kruskal。

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
};
```

## 树状数组 Fenwick

适合：单点加、前缀和、区间和。

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

    long long range_sum(int l, int r) {
        if (r < l) return 0;
        return sum_prefix(r) - (l == 0 ? 0 : sum_prefix(l - 1));
    }
};
```

## 线段树

适合：区间查询、单点修改。夏令营机试不一定常考，但会写基础版很有用。

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

## Trie

适合：前缀匹配、字典树、字符串集合。

```cpp
struct Trie {
    struct Node {
        int next[26];
        bool end = false;
        Node() {
            fill(next, next + 26, -1);
        }
    };

    vector<Node> tr{Node()};

    void insert(const string& s) {
        int u = 0;
        for (char c : s) {
            int x = c - 'a';
            if (tr[u].next[x] == -1) {
                tr[u].next[x] = tr.size();
                tr.push_back(Node());
            }
            u = tr[u].next[x];
        }
        tr[u].end = true;
    }

    bool search(const string& s) {
        int u = 0;
        for (char c : s) {
            int x = c - 'a';
            if (tr[u].next[x] == -1) return false;
            u = tr[u].next[x];
        }
        return tr[u].end;
    }
};
```

## 图的常用建法

无权图：

```cpp
int n, m;
cin >> n >> m;
vector<vector<int>> g(n);
for (int i = 0; i < m; ++i) {
    int u, v;
    cin >> u >> v;
    --u; --v;
    g[u].push_back(v);
    g[v].push_back(u);
}
```

带权图：

```cpp
vector<vector<pair<int, int>>> g(n); // to, weight
g[u].push_back({v, w});
```

Dijkstra：

```cpp
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
```

## 网格模板

```cpp
int dx[4] = {1, -1, 0, 0};
int dy[4] = {0, 0, 1, -1};

auto inside = [&](int x, int y) {
    return 0 <= x && x < n && 0 <= y && y < m;
};
```

## 坐标离散化

适合：数值很大但不同值数量不多。

```cpp
vector<int> vals = a;
sort(vals.begin(), vals.end());
vals.erase(unique(vals.begin(), vals.end()), vals.end());

for (int& x : a) {
    x = lower_bound(vals.begin(), vals.end(), x) - vals.begin();
}
```

## 容器选择口诀

- 不确定用什么，先想 `vector`。
- 需要队首队尾操作，用 `deque`。
- 只要最大/最小，用 `priority_queue`。
- 要有序且查前驱后继，用 `set/map`。
- 只查存在或计数，用 `unordered_set/unordered_map`。
- 连通性动态合并，用并查集。
- 前缀和动态单点修改，用树状数组。
- 区间查询加修改，用线段树。

## 常见坑

- `endl` 会刷新缓冲，频繁输出时用 `'\n'`。
- `cin/cout` 加速后不要混用 `scanf/printf`。
- `vector<int> a[n]` 里的 `n` 非编译期常量时不标准，推荐 `vector<vector<int>> a(n)`。
- `memset(dist, 0x3f, sizeof dist)` 只适合普通数组；`vector` 用 `fill`。
- `priority_queue` 无法删除任意元素，常用“懒删除”。
- `set` 遍历时删除当前迭代器要先保存下一个。

## 两个月 STL 学习路线

STL 不应该只背 API，要在题里反复使用。建议分四层。

### 第 1 层：必须写顺

- `vector`
- `string`
- `pair`
- `sort`
- `map`
- `unordered_map`
- `set`
- `queue`
- `stack`

完成标准：

- 不查资料写出初始化、插入、删除、遍历。
- 能处理结构体排序。
- 能解释 `map` 和 `unordered_map` 的时间复杂度。

### 第 2 层：常见中等题工具

- `priority_queue`
- `deque`
- `multiset`
- `lower_bound`
- `upper_bound`
- `unique`
- `accumulate`
- `next_permutation`

完成标准：

- 能写小根堆。
- 能用 `deque` 写单调队列。
- 能用 `multiset` 处理重复元素删除一个的问题。

### 第 3 层：提高实现效率

- `array`
- `bitset`
- `tuple`
- `iota`
- `partial_sum`
- `nth_element`
- `min_element/max_element`

完成标准：

- 知道什么时候 `nth_element` 比完整排序更合适。
- 能用 `bitset` 做布尔集合和状态压缩辅助。

### 第 4 层：谨慎使用

- `list`
- `forward_list`
- `unordered_multimap`
- `unordered_multiset`
- C++20 ranges

这些不是不能用，而是机试常规题很少必须用。优先把前 3 层练熟。

## API 专项练习

### `vector` 练习

要求不用查资料写出：

- 输入 `n` 个数，排序，去重。
- 删除所有等于 `x` 的元素。
- 二维矩阵初始化为 `-1`。
- 把一个数组离散化。

参考片段：

```cpp
a.erase(remove(a.begin(), a.end(), x), a.end());
```

### `string` 练习

要求能处理：

- 读无空格字符串。
- 读整行。
- 按空格切词。
- 截取子串。
- 统计字符频率。
- 判断回文。

常用片段：

```cpp
stringstream ss(line);
string word;
while (ss >> word) {
    // use word
}
```

### `map/unordered_map` 练习

要求能写：

- 单词频率统计。
- 字符串到整数 id 映射。
- 两数之和。
- 按 key 有序输出统计结果。

常见选择：

```text
需要有序输出 -> map
只需要快速查找 -> unordered_map
key 是复杂结构 -> map 更省心，unordered_map 需要 hash
```

### `set/multiset` 练习

要求能写：

- 动态插入删除，并查询是否存在。
- 找第一个大于等于 `x` 的数。
- 维护窗口内最大/最小值。
- 删除一个重复元素。

片段：

```cpp
auto it = s.lower_bound(x);
if (it != s.end()) {
    // *it >= x
}
```

### `priority_queue` 练习

要求能写：

- 第 k 大。
- 合并多个有序序列。
- Dijkstra 小根堆。
- 自定义结构体比较。

小根堆记忆法：

```cpp
priority_queue<int, vector<int>, greater<int>> pq;
```

### `algorithm` 练习

要求能熟练使用：

```cpp
sort
stable_sort
lower_bound
upper_bound
reverse
unique
min_element
max_element
accumulate
next_permutation
nth_element
```

特别注意：`unique` 只把重复元素移动到末尾，不会真的改变容器大小，必须接 `erase`。

## 常用结构的选择练习

看到需求时，先选结构：

| 需求 | 优先结构 |
|---|---|
| 顺序存储、随机访问 | `vector` |
| 频繁头尾插入删除 | `deque` |
| LIFO | `stack` |
| FIFO | `queue` |
| 最大/最小优先 | `priority_queue` |
| 有序唯一集合 | `set` |
| 有序可重复集合 | `multiset` |
| key-value 且按 key 有序 | `map` |
| key-value 快速查找 | `unordered_map` |
| 固定长度布尔状态 | `bitset` |
| 连通集合合并 | 并查集 |
| 前缀和动态维护 | 树状数组 |
| 区间查询和修改 | 线段树 |

## STL 失误专项清单

每周检查一次自己是否还会犯这些错：

- `priority_queue` 默认是大根堆。
- `set.erase(value)` 删除所有等于该值的元素，`multiset` 删除一个要传迭代器。
- `unordered_map[key]` 会插入默认值。
- `lower_bound` 要求范围已经按相同规则有序。
- `sort` comparator 不能写 `<=`。
- `vector` 扩容会导致迭代器和引用失效。
- `getline` 前可能要清掉残留换行。
- `size_t` 和 `int` 混用可能导致倒序循环错误。

## 什么时候手写数据结构

优先使用 STL，除非：

- STL 不支持需要的操作，例如区间查询 + 修改。
- 需要并查集这种专门结构。
- 题目要求复杂度必须依赖自定义结构。
- 你需要维护更复杂的信息，例如线段树节点保存多个值。

常规夏令营机试中，手写优先级：

1. 并查集。
2. 树状数组。
3. 线段树基础版。
4. Trie。
5. 更复杂结构通常不必优先准备。

## 每周 STL 默写任务

第 1 周：

- `vector` 排序去重。
- `string` 整行读取和切词。
- 结构体排序。

第 2 周：

- `map/unordered_map` 计数。
- `set.lower_bound`。
- `lower_bound` 查数组边界。

第 3 周：

- 小根堆。
- 单调队列。
- `multiset` 删除单个元素。

第 4 周之后：

- 每周随机选 5 个 API，写一个 20 行以内的小程序验证。
