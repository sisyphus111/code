# OJ 模式与 C++ 输入输出总结

这份材料解决“不同平台代码长什么样”和“题面输入怎么读”的问题。

## 平台模式对比

| 模式 | 代码形态 | 输入输出 | 常见平台 |
|---|---|---|---|
| LeetCode 函数模式 | 写 `class Solution` 里的函数 | 平台把参数传给函数，通常不写 `main` | LeetCode |
| ACM/ICPC 模式 | 写完整 `main` | 从 `stdin` 读，向 `stdout` 写 | ICPC、牛客、很多高校机试 |
| 洛谷/传统 OJ | 写完整 `main` | 通常标准输入输出，题目特殊要求时文件读写 | 洛谷、Codeforces 类 |
| OI 文件模式 | 写完整 `main` | `freopen("xxx.in","r",stdin)` 等 | 部分 OI/校内评测 |
| 交互题 | 写完整 `main` 或指定函数 | 输出后要 flush，按协议交互 | 少见，按题面来 |

夏令营代码机试最常见的是 ACM/传统 OJ：你自己读输入、输出答案。

## 通用 ACM 模板

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // solve here

    return 0;
}
```

注意：

- `ios::sync_with_stdio(false); cin.tie(nullptr);` 可以加速 C++ I/O。
- 加速后不要混用 `cin/cout` 和 `scanf/printf`。
- 高频输出用 `'\n'`，少用 `endl`。

## LeetCode 模式

LeetCode 通常给函数签名，你只写核心函数：

```cpp
class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        int best = nums[0], cur = 0;
        for (int x : nums) {
            cur = max(x, cur + x);
            best = max(best, cur);
        }
        return best;
    }
};
```

特点：

- 不写 `main`。
- 不自己读 `cin`，不自己打印答案。
- 参数、返回值由平台处理。
- 树、链表等结构通常已定义好。
- 调试可以临时 `cerr`，最终建议删掉。

把 LeetCode 题改成本地 ACM 模式时，需要自己写输入解析。例如数组题：

```cpp
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> nums(n);
    for (int& x : nums) cin >> x;

    Solution sol;
    cout << sol.maxSubArray(nums) << '\n';
}
```

## 洛谷/传统 OJ 模式

通常和 ACM 一样，从标准输入读：

```cpp
int n, m;
cin >> n >> m;
```

如果题面明确要求文件输入输出，再使用：

```cpp
freopen("problem.in", "r", stdin);
freopen("problem.out", "w", stdout);
```

建议：

- 没有明确要求文件读写时，不要主动加 `freopen`。
- 本地调试可用条件编译，提交时不影响标准输入输出。

```cpp
#ifdef LOCAL
freopen("in.txt", "r", stdin);
freopen("out.txt", "w", stdout);
#endif
```

## 单组输入

题面：

```text
n
a1 a2 ... an
```

代码：

```cpp
int n;
cin >> n;
vector<int> a(n);
for (int i = 0; i < n; ++i) cin >> a[i];
```

## 多组输入：第一行给 `T`

题面：

```text
T
case1
case2
...
```

代码：

```cpp
void solve() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int& x : a) cin >> x;
    // ...
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while (T--) solve();
    return 0;
}
```

注意：`solve()` 内不要遗留上一个 case 的全局状态。全局数组如果复用，要清空实际使用范围。

## 多组输入：读到 EOF

题面没有 `T`，而是多行直到文件结束：

```cpp
int a, b;
while (cin >> a >> b) {
    cout << a + b << '\n';
}
```

读取数组直到 EOF：

```cpp
vector<int> a;
int x;
while (cin >> x) a.push_back(x);
```

## 每行一个 case

适合：一行里数量不固定。

```cpp
string line;
while (getline(cin, line)) {
    if (line.empty()) continue;
    stringstream ss(line);
    vector<int> a;
    int x;
    while (ss >> x) a.push_back(x);
}
```

如果前面用过 `cin >> n`，再读整行：

```cpp
int n;
cin >> n;
cin.ignore(numeric_limits<streamsize>::max(), '\n');

string line;
getline(cin, line);
```

## 读取字符串

无空格字符串：

```cpp
string s;
cin >> s;
```

整行字符串：

```cpp
string s;
getline(cin, s);
```

多个单词：

```cpp
string word;
while (cin >> word) {
    // word has no spaces
}
```

## 读取矩阵

数字矩阵：

```cpp
int n, m;
cin >> n >> m;
vector<vector<int>> a(n, vector<int>(m));
for (int i = 0; i < n; ++i) {
    for (int j = 0; j < m; ++j) {
        cin >> a[i][j];
    }
}
```

字符网格：

```cpp
int n, m;
cin >> n >> m;
vector<string> grid(n);
for (int i = 0; i < n; ++i) cin >> grid[i];
```

如果字符之间有空格：

```cpp
vector<vector<char>> grid(n, vector<char>(m));
for (int i = 0; i < n; ++i) {
    for (int j = 0; j < m; ++j) cin >> grid[i][j];
}
```

## 读取图

无权无向图，输入点编号从 1 开始：

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

有向图：

```cpp
g[u].push_back(v);
```

带权图：

```cpp
vector<vector<pair<int, int>>> g(n);
for (int i = 0; i < m; ++i) {
    int u, v, w;
    cin >> u >> v >> w;
    --u; --v;
    g[u].push_back({v, w});
}
```

## 读取树

树一般是 `n - 1` 条边：

```cpp
int n;
cin >> n;
vector<vector<int>> g(n);
for (int i = 0; i < n - 1; ++i) {
    int u, v;
    cin >> u >> v;
    --u; --v;
    g[u].push_back(v);
    g[v].push_back(u);
}
```

DFS 时传父节点：

```cpp
void dfs(int u, int parent) {
    for (int v : g[u]) {
        if (v == parent) continue;
        dfs(v, u);
    }
}
```

## 输出数组

空格分隔，末尾不多空格：

```cpp
for (int i = 0; i < n; ++i) {
    if (i) cout << ' ';
    cout << a[i];
}
cout << '\n';
```

也可以接受末尾空格的平台很多，但考场建议写规范。

## 输出浮点数

```cpp
cout << fixed << setprecision(6) << ans << '\n';
```

如果题面要求误差 `1e-6`，通常输出 8-10 位更稳：

```cpp
cout << fixed << setprecision(10) << ans << '\n';
```

## `Yes/No` 与大小写

严格按题面输出。常见有：

```cpp
cout << (ok ? "Yes" : "No") << '\n';
cout << (ok ? "YES" : "NO") << '\n';
```

## Case 编号输出

```cpp
int T;
cin >> T;
for (int tc = 1; tc <= T; ++tc) {
    // ...
    cout << "Case #" << tc << ": " << ans << '\n';
}
```

有些题是 `Case 1:`，不要凭习惯写错。

## 混合输入的常见坑

### `cin >>` 后接 `getline`

错误原因：`cin >>` 留下换行，`getline` 直接读到空行。

解决：

```cpp
cin.ignore(numeric_limits<streamsize>::max(), '\n');
getline(cin, line);
```

### 读取字符时读到换行

如果用 `cin >> c`，会自动跳过空白。  
如果用 `getchar()` 或 `cin.get(c)`，会读到换行，需要自己处理。

## 交互题 I/O

交互题很少出现在普通夏令营机试，但如果遇到：

```cpp
cout << "? " << x << endl; // endl 会 flush
cin >> reply;
```

或者：

```cpp
cout << "? " << x << '\n' << flush;
```

注意：

- 每次询问后必须刷新输出。
- 严格按题面协议，不要多输出调试信息。

## 本地调试模板

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

void solve() {
    // ...
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

#ifdef LOCAL
    freopen("in.txt", "r", stdin);
#endif

    solve();
    return 0;
}
```

多组版本：

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

读到 EOF 版本：

```cpp
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    while (solve_one_case()) {
        // solve_one_case returns false when input ends
    }
    return 0;
}
```

更常见写法：

```cpp
int n;
while (cin >> n) {
    vector<int> a(n);
    for (int& x : a) cin >> x;
    // ...
}
```

## 平台差异带来的策略

LeetCode：

- 重心是函数逻辑和边界。
- 不练标准输入输出会导致转到 ACM 模式时不适应。
- 树、链表题平台帮你建结构，本地机试通常不会这么友好。

洛谷/牛客/ACM：

- 重心是完整程序、输入输出、复杂度。
- 要能自己建图、建树、读矩阵。
- 样例只是基本检查，需要自己造反例。

OI 文件模式：

- 只有题面明确要求时用 `freopen`。
- 文件名必须完全一致。

## 考前 I/O 检查清单

- 题面有没有 `T`。
- 是读到 EOF 还是固定一组。
- 点编号是 0-based 还是 1-based。
- 字符串是否包含空格。
- 矩阵字符是否有空格分隔。
- 图是有向还是无向。
- 输出大小写、空格、换行、精度是否匹配题面。
- 是否把本地 `freopen` 或调试输出带进提交。

## 两个月 I/O 专项训练

很多同学算法会，但机试输在输入输出。建议前两周专门练，后面每周保持一次。

### 第 1 组：基础输入

练习目标：

- 单个整数。
- 一维数组。
- 二维矩阵。
- 字符网格。
- 字符串数组。

你应该能不查资料写出这些输入。

### 第 2 组：多组输入

练习目标：

- 第一行给 `T`。
- 没有 `T`，读到 EOF。
- 每行一个 case。
- 每组输入规模不同。

练习片段：

```cpp
int n;
while (cin >> n) {
    vector<int> a(n);
    for (int& x : a) cin >> x;
}
```

### 第 3 组：整行输入

练习目标：

- `getline` 读句子。
- `stringstream` 切词。
- 空行处理。
- `cin >>` 后接 `getline`。

必会片段：

```cpp
cin.ignore(numeric_limits<streamsize>::max(), '\n');
```

### 第 4 组：图和树输入

练习目标：

- 无向图。
- 有向图。
- 带权图。
- 树的 `n - 1` 条边。
- 1-based 转 0-based。

练习时每次建图前写注释：

```cpp
// directed or undirected?
// weighted or unweighted?
// 0-based or 1-based?
```

### 第 5 组：输出格式

练习目标：

- 数组空格分隔。
- Case 编号。
- 浮点精度。
- `Yes/No` 大小写。
- 多答案按行输出。

输出数组模板要默写：

```cpp
for (int i = 0; i < n; ++i) {
    if (i) cout << ' ';
    cout << a[i];
}
cout << '\n';
```

## 平台模式转换训练

### LeetCode 函数模式转 ACM 模式

LeetCode 给你：

```cpp
class Solution {
public:
    int longestConsecutive(vector<int>& nums) {
        // ...
    }
};
```

ACM 模式要补：

```cpp
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> nums(n);
    for (int& x : nums) cin >> x;

    Solution sol;
    cout << sol.longestConsecutive(nums) << '\n';
    return 0;
}
```

训练方法：

- 每周选 3 道 LeetCode 数组/字符串题，手动改成 ACM 输入输出版本。
- 对树和链表题暂时不用强行转换，除非目标机试明确会考。

### ACM 模式转函数模式

把核心逻辑封装成函数：

```cpp
long long solve_one(vector<int>& a) {
    return 0;
}
```

好处：

- 本地更容易写多组测试。
- 逻辑和 I/O 分离，减少调试噪声。

## 本地调试习惯

### 使用样例文件

```cpp
#ifdef LOCAL
freopen("in.txt", "r", stdin);
#endif
```

编译时加：

```bash
g++ -std=c++17 -O2 -DLOCAL main.cpp && ./a.out
```

提交前不要让 `LOCAL` 生效。

### 使用 `cerr`

调试输出用：

```cpp
cerr << "x=" << x << '\n';
```

`cerr` 通常不影响标准输出答案，但提交前仍建议删掉大量调试信息。

### 造样例

每题至少造：

- 最小规模。
- 最大边界附近。
- 全相同。
- 严格递增/递减。
- 无解。
- 多组输入。

## 常见输入格式与代码

### 输入第一行 `n m`，后面 `n` 行字符串

```cpp
int n, m;
cin >> n >> m;
vector<string> grid(n);
for (int i = 0; i < n; ++i) cin >> grid[i];
```

### 输入若干操作

```cpp
int q;
cin >> q;
while (q--) {
    string op;
    cin >> op;
    if (op == "add") {
        int x;
        cin >> x;
    } else if (op == "query") {
        int l, r;
        cin >> l >> r;
    }
}
```

### 输入一行未知数量整数

```cpp
string line;
getline(cin, line);
stringstream ss(line);
vector<int> a;
int x;
while (ss >> x) a.push_back(x);
```

如果前面已经用 `cin >>`，记得先 `ignore`。

### 输入逗号分隔

```cpp
string line;
getline(cin, line);
for (char& c : line) {
    if (c == ',') c = ' ';
}
stringstream ss(line);
vector<int> a;
int x;
while (ss >> x) a.push_back(x);
```

### 输入形如 `[1,2,3]`

这种更像 LeetCode raw input 或面试手写解析，传统 OJ 较少。可以这样处理：

```cpp
string s;
cin >> s;
for (char& c : s) {
    if (c == '[' || c == ']' || c == ',') c = ' ';
}
stringstream ss(s);
vector<int> a;
int x;
while (ss >> x) a.push_back(x);
```

## 文件输入输出的判断

只有题面明确写：

```text
输入文件：xxx.in
输出文件：xxx.out
```

才加：

```cpp
freopen("xxx.in", "r", stdin);
freopen("xxx.out", "w", stdout);
```

如果题面没有写，就坚持标准输入输出。

## 输出比较和 Special Judge

多数传统题是普通文本比较，通常会忽略行末空格和文末换行，但不要依赖这个宽容。  
浮点题、构造题、多解题可能使用 Special Judge，此时只要满足题面条件即可。

训练时仍按严格格式输出，这能减少不必要的 WA。

## I/O 周测

每周做一次 30 分钟小测：

1. 写一个多组输入模板。
2. 写一个读到 EOF 模板。
3. 写一个整行切词模板。
4. 写一个无向带权图输入。
5. 写一个数组输出无多余空格。

如果这些还要查资料，说明 I/O 还没稳定。
