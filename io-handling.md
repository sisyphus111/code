# 输入输出处理

## OJ 模式分类

### LeetCode 函数模式

**特点**：给定函数签名，直接写逻辑，不需要处理输入输出。

```cpp
class Solution {
public:
    int twoSum(vector<int>& nums, int target) {
        // 直接写逻辑
        return 0;
    }
};
```

---

### ACM/ICPC 模式

**特点**：需要自己处理输入输出，完整的 `main` 函数。

#### 单组输入

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; ++i) {
        cin >> a[i];
    }
    
    // 处理
    
    cout << result << "\n";
    
    return 0;
}
```

#### 多组输入（给定组数）

```cpp
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int T;
    cin >> T;
    while (T--) {
        int n;
        cin >> n;
        // 处理每组
    }
    
    return 0;
}
```

#### 多组输入（读到 EOF）

```cpp
int main() {
    int n;
    while (cin >> n) {
        // 处理
    }
    return 0;
}

// 或者
int main() {
    string line;
    while (getline(cin, line)) {
        // 处理
    }
    return 0;
}
```

---

## 常见输入格式

### 读取数组

```cpp
// 一行 n 个数
int n;
cin >> n;
vector<int> a(n);
for (int i = 0; i < n; ++i) {
    cin >> a[i];
}

// 不指定 n，读一行所有数
string line;
getline(cin, line);
stringstream ss(line);
vector<int> a;
int x;
while (ss >> x) {
    a.push_back(x);
}
```

---

### 读取矩阵

```cpp
int n, m;
cin >> n >> m;
vector<vector<int>> mat(n, vector<int>(m));

for (int i = 0; i < n; ++i) {
    for (int j = 0; j < m; ++j) {
        cin >> mat[i][j];
    }
}

// 字符矩阵
vector<string> grid(n);
for (int i = 0; i < n; ++i) {
    cin >> grid[i];
}
```

---

### 读取整行

```cpp
string line;
getline(cin, line);

// 按空白分割
stringstream ss(line);
string word;
while (ss >> word) {
    // 处理每个单词
}

// 按特定分隔符分割
stringstream ss(line);
string part;
while (getline(ss, part, ',')) {
    // 按逗号分割
}
```

---

### 混合输入（数字 + 整行）

**问题**：`cin >> x` 后用 `getline` 会读到残留换行符。

**解决**：
```cpp
int n;
cin >> n;
cin.ignore();  // 忽略换行符

string line;
getline(cin, line);
```

---

### 读到特定标记

```cpp
int n;
while (cin >> n && n != 0) {  // 读到 0 结束
    // 处理
}

string s;
while (cin >> s && s != "#") {  // 读到 # 结束
    // 处理
}
```

---

## 常见输出格式

### 基本输出

```cpp
cout << x << "\n";              // 输出 + 换行
cout << x << " " << y << "\n";  // 多个值

// 行末无空格
for (int i = 0; i < n; ++i) {
    cout << a[i];
    if (i < n - 1) cout << " ";
}
cout << "\n";

// 更简洁的写法
for (int i = 0; i < n; ++i) {
    cout << a[i] << " \n"[i == n - 1];
}
```

---

### 格式化输出

```cpp
#include <iomanip>

// 保留小数
cout << fixed << setprecision(2) << x << "\n";

// 宽度和填充
cout << setw(5) << setfill('0') << x << "\n";  // 00123

// 科学计数法
cout << scientific << x << "\n";
```

---

### 布尔值

```cpp
bool flag = true;

// 输出 1 或 0
cout << flag << "\n";

// 输出 true 或 false
cout << boolalpha << flag << "\n";

// 输出 YES 或 NO
cout << (flag ? "YES" : "NO") << "\n";
```

---

## 输入输出优化

### 关闭同步（C++ 常用）

```cpp
ios::sync_with_stdio(false);
cin.tie(nullptr);
```

**效果**：加速 `cin/cout`，但不能混用 `scanf/printf`。

---

### 使用 scanf/printf（C 风格）

```cpp
int n;
scanf("%d", &n);

double x;
scanf("%lf", &x);

long long ll;
scanf("%lld", &ll);

printf("%d\n", n);
printf("%.2lf\n", x);
printf("%lld\n", ll);
```

**优点**：比 `cin/cout` 快（不开优化时）  
**缺点**：容易写错格式串

---

### 读入整个文件

```cpp
string content((istreambuf_iterator<char>(cin)),
               istreambuf_iterator<char>());
```

---

## 特殊情况处理

### 空行处理

```cpp
string line;
while (getline(cin, line)) {
    if (line.empty()) {
        // 空行
        continue;
    }
    // 处理非空行
}
```

---

### 前导/后缀空格

```cpp
// 去掉前导空格
line.erase(line.begin(), find_if(line.begin(), line.end(), [](char c) {
    return !isspace(c);
}));

// 去掉后缀空格
line.erase(find_if(line.rbegin(), line.rend(), [](char c) {
    return !isspace(c);
}).base(), line.end());

// 使用 stringstream 自动忽略空格
stringstream ss(line);
string word;
while (ss >> word) { }  // 自动跳过前后空格
```

---

### 不定长数组

```cpp
// 方法 1：读一行再解析
string line;
getline(cin, line);
stringstream ss(line);
vector<int> a;
int x;
while (ss >> x) {
    a.push_back(x);
}

// 方法 2：读到换行符
vector<int> a;
int x;
while (cin >> x) {
    a.push_back(x);
    if (cin.peek() == '\n') break;
}
```

---

## 文件输入输出

### 从文件读取

```cpp
freopen("input.txt", "r", stdin);
freopen("output.txt", "w", stdout);

// 之后用 cin/cout 正常读写即可
int n;
cin >> n;
cout << n << "\n";
```

### 使用 fstream

```cpp
#include <fstream>

ifstream fin("input.txt");
ofstream fout("output.txt");

int n;
fin >> n;
fout << n << "\n";

fin.close();
fout.close();
```

---

## 调试输出

### 标准错误流

```cpp
cerr << "Debug: x = " << x << "\n";  // 不影响标准输出
```

### 条件编译

```cpp
#ifdef LOCAL
    freopen("input.txt", "r", stdin);
    #define debug(x) cerr << #x << " = " << x << "\n"
#else
    #define debug(x)
#endif

debug(n);  // 本地运行时输出，提交时自动忽略
```

---

## 常见陷阱

1. **混用 cin 和 getline**：`cin >> x` 后用 `getline` 要先 `cin.ignore()`
2. **行末空格**：题目要求行末无空格时注意处理
3. **多组数据不清空**：`vector`、`map`、全局数组要清空
4. **EOF 判断**：`while (cin >> n)` 自动处理 EOF
5. **精度问题**：浮点输出注意 `fixed` 和 `setprecision`
6. **换行符**：`\n` 比 `endl` 快（`endl` 会刷新缓冲区）

## 输入输出速度对比

| 方法 | 速度 | 使用场景 |
|------|------|----------|
| `scanf/printf` | 快 | 简单格式，需要速度 |
| `cin/cout` + 优化 | 中等 | C++ 风格，推荐 |
| `cin/cout` 不优化 | 慢 | 数据量小 |
| `getline` | 中等 | 需要读整行 |

## 推荐做法

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    // 使用 cin/cout 即可
    
    return 0;
}
```
