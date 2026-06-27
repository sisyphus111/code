# 并查集

## 什么时候用

看到以下特征优先考虑并查集：
- **动态连通性**：判断两个元素是否连通
- **集合合并**：合并两个集合
- **连通分量计数**：统计有多少个独立的连通区域
- **最小生成树**：Kruskal 算法
- **朋友圈、社交网络**：判断关系传递
- 题目中出现"连通"、"合并"、"分组"、"等价关系"等字眼

核心思路：**用树形结构表示集合，支持快速查找根节点和合并操作**。

## 核心模板

### 基础并查集

```cpp
class UnionFind {
private:
    vector<int> parent;
    vector<int> rank;  // 树的高度
    int count;  // 连通分量数量
    
public:
    UnionFind(int n) {
        parent.resize(n);
        rank.resize(n, 1);
        count = n;
        
        for (int i = 0; i < n; ++i) {
            parent[i] = i;
        }
    }
    
    // 查找根节点（带路径压缩）
    int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);  // 路径压缩
        }
        return parent[x];
    }
    
    // 合并两个集合
    bool unite(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);
        
        if (rootX == rootY) return false;
        
        // 按秩合并
        if (rank[rootX] < rank[rootY]) {
            parent[rootX] = rootY;
        } else if (rank[rootX] > rank[rootY]) {
            parent[rootY] = rootX;
        } else {
            parent[rootY] = rootX;
            rank[rootX]++;
        }
        
        count--;
        return true;
    }
    
    // 判断是否连通
    bool connected(int x, int y) {
        return find(x) == find(y);
    }
    
    // 获取连通分量数量
    int getCount() {
        return count;
    }
};
```

### 带权并查集

```cpp
class WeightedUnionFind {
private:
    vector<int> parent;
    vector<int> weight;  // 到父节点的权值
    
public:
    WeightedUnionFind(int n) {
        parent.resize(n);
        weight.resize(n, 0);
        
        for (int i = 0; i < n; ++i) {
            parent[i] = i;
        }
    }
    
    int find(int x) {
        if (parent[x] != x) {
            int root = find(parent[x]);
            weight[x] += weight[parent[x]];
            parent[x] = root;
        }
        return parent[x];
    }
    
    void unite(int x, int y, int w) {
        int rootX = find(x);
        int rootY = find(y);
        
        if (rootX != rootY) {
            parent[rootX] = rootY;
            weight[rootX] = weight[y] - weight[x] + w;
        }
    }
};
```

## 例题演示

### 例题 1：省份数量（朋友圈）

**题目**：给定 n×n 矩阵，`isConnected[i][j] = 1` 表示城市 i 和 j 直接相连，求省份数量（连通分量数量）。

**思路**：并查集，合并所有直接相连的城市，最后统计根节点数量。

```cpp
#include <bits/stdc++.h>
using namespace std;

class UnionFind {
private:
    vector<int> parent;
    int count;
    
public:
    UnionFind(int n) : count(n) {
        parent.resize(n);
        for (int i = 0; i < n; ++i) {
            parent[i] = i;
        }
    }
    
    int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }
    
    void unite(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);
        
        if (rootX != rootY) {
            parent[rootX] = rootY;
            count--;
        }
    }
    
    int getCount() {
        return count;
    }
};

int findCircleNum(vector<vector<int>>& isConnected) {
    int n = isConnected.size();
    UnionFind uf(n);
    
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (isConnected[i][j] == 1) {
                uf.unite(i, j);
            }
        }
    }
    
    return uf.getCount();
}

int main() {
    int n;
    cin >> n;
    
    vector<vector<int>> isConnected(n, vector<int>(n));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            cin >> isConnected[i][j];
        }
    }
    
    cout << findCircleNum(isConnected) << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(n^2 × α(n))`，α 是反阿克曼函数，几乎为常数

**易错点**：
- 矩阵是对称的，只需要遍历上三角
- 初始时有 n 个连通分量

---

### 例题 2：冗余连接（检测环）

**题目**：给定无向图的边列表，找出最后一条导致成环的边。

**思路**：并查集，逐条加边，如果两个节点已经连通则该边会导致环。

```cpp
#include <bits/stdc++.h>
using namespace std;

class UnionFind {
private:
    vector<int> parent;
    
public:
    UnionFind(int n) {
        parent.resize(n + 1);
        for (int i = 0; i <= n; ++i) {
            parent[i] = i;
        }
    }
    
    int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }
    
    bool unite(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);
        
        if (rootX == rootY) return false;  // 已经连通，会成环
        
        parent[rootX] = rootY;
        return true;
    }
};

vector<int> findRedundantConnection(vector<vector<int>>& edges) {
    int n = edges.size();
    UnionFind uf(n);
    
    for (auto& edge : edges) {
        if (!uf.unite(edge[0], edge[1])) {
            return edge;
        }
    }
    
    return {};
}

int main() {
    int n;
    cin >> n;
    
    vector<vector<int>> edges(n, vector<int>(2));
    for (int i = 0; i < n; ++i) {
        cin >> edges[i][0] >> edges[i][1];
    }
    
    vector<int> result = findRedundantConnection(edges);
    cout << result[0] << " " << result[1] << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(n × α(n))`，空间 `O(n)`

**易错点**：
- 节点编号从 1 开始，数组要开 n+1
- 第一条导致环的边就是答案

---

### 例题 3：账户合并

**题目**：给定账户列表，每个账户有名字和若干邮箱，如果两个账户有相同邮箱则属于同一人，合并账户。

**思路**：并查集，将邮箱作为节点，相同账户的邮箱合并。

```cpp
#include <bits/stdc++.h>
using namespace std;

class UnionFind {
private:
    unordered_map<string, string> parent;
    
public:
    string find(string x) {
        if (!parent.count(x)) {
            parent[x] = x;
        }
        
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        
        return parent[x];
    }
    
    void unite(string x, string y) {
        string rootX = find(x);
        string rootY = find(y);
        
        if (rootX != rootY) {
            parent[rootX] = rootY;
        }
    }
};

vector<vector<string>> accountsMerge(vector<vector<string>>& accounts) {
    UnionFind uf;
    unordered_map<string, string> emailToName;
    
    // 建立并查集
    for (auto& account : accounts) {
        string name = account[0];
        string firstEmail = account[1];
        
        for (int i = 1; i < account.size(); ++i) {
            string email = account[i];
            emailToName[email] = name;
            uf.unite(firstEmail, email);
        }
    }
    
    // 合并结果
    unordered_map<string, set<string>> groups;
    for (auto& [email, name] : emailToName) {
        string root = uf.find(email);
        groups[root].insert(email);
    }
    
    // 构造答案
    vector<vector<string>> result;
    for (auto& [root, emails] : groups) {
        vector<string> account;
        account.push_back(emailToName[root]);
        for (auto& email : emails) {
            account.push_back(email);
        }
        result.push_back(account);
    }
    
    return result;
}

int main() {
    int n;
    cin >> n;
    cin.ignore();
    
    vector<vector<string>> accounts(n);
    for (int i = 0; i < n; ++i) {
        string line;
        getline(cin, line);
        stringstream ss(line);
        string item;
        
        while (ss >> item) {
            accounts[i].push_back(item);
        }
    }
    
    vector<vector<string>> result = accountsMerge(accounts);
    
    for (auto& account : result) {
        for (int i = 0; i < account.size(); ++i) {
            cout << account[i] << " \n"[i == account.size() - 1];
        }
    }
    
    return 0;
}
```

**复杂度**：时间 `O(n × k × α(n))`，n 是账户数，k 是平均邮箱数

**易错点**：
- 并查集的节点是邮箱（字符串），不是账户
- 同一账户的所有邮箱要合并到第一个邮箱
- 结果要按邮箱字典序排序（用 set）

---

### 例题 4：等式方程的可满足性

**题目**：给定形如 "a==b" 或 "a!=b" 的方程，判断是否矛盾。

**思路**：先处理 ==，用并查集合并，再检查 != 是否矛盾。

```cpp
#include <bits/stdc++.h>
using namespace std;

class UnionFind {
private:
    vector<int> parent;
    
public:
    UnionFind(int n) {
        parent.resize(n);
        for (int i = 0; i < n; ++i) {
            parent[i] = i;
        }
    }
    
    int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }
    
    void unite(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);
        
        if (rootX != rootY) {
            parent[rootX] = rootY;
        }
    }
    
    bool connected(int x, int y) {
        return find(x) == find(y);
    }
};

bool equationsPossible(vector<string>& equations) {
    UnionFind uf(26);
    
    // 先处理等式
    for (auto& eq : equations) {
        if (eq[1] == '=') {
            int x = eq[0] - 'a';
            int y = eq[3] - 'a';
            uf.unite(x, y);
        }
    }
    
    // 检查不等式是否矛盾
    for (auto& eq : equations) {
        if (eq[1] == '!') {
            int x = eq[0] - 'a';
            int y = eq[3] - 'a';
            
            if (uf.connected(x, y)) {
                return false;  // 矛盾
            }
        }
    }
    
    return true;
}

int main() {
    int n;
    cin >> n;
    
    vector<string> equations(n);
    for (int i = 0; i < n; ++i) {
        cin >> equations[i];
    }
    
    cout << (equationsPossible(equations) ? "YES" : "NO") << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(n × α(26))` ≈ `O(n)`，空间 `O(26)` = `O(1)`

**易错点**：
- 要先处理 ==，再检查 !=
- 字符映射到数字：`c - 'a'`

---

### 例题 5：最小生成树（Kruskal 算法）

**题目**：给定带权无向图，求最小生成树的权值和。

**思路**：边按权值排序，用并查集判断是否成环，贪心选边。

```cpp
#include <bits/stdc++.h>
using namespace std;

class UnionFind {
private:
    vector<int> parent;
    
public:
    UnionFind(int n) {
        parent.resize(n);
        for (int i = 0; i < n; ++i) {
            parent[i] = i;
        }
    }
    
    int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }
    
    bool unite(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);
        
        if (rootX == rootY) return false;
        
        parent[rootX] = rootY;
        return true;
    }
};

int kruskal(int n, vector<vector<int>>& edges) {
    // 按权值排序
    sort(edges.begin(), edges.end(), [](auto& a, auto& b) {
        return a[2] < b[2];
    });
    
    UnionFind uf(n);
    int totalWeight = 0;
    int edgeCount = 0;
    
    for (auto& edge : edges) {
        int u = edge[0], v = edge[1], w = edge[2];
        
        if (uf.unite(u, v)) {
            totalWeight += w;
            edgeCount++;
            
            if (edgeCount == n - 1) break;  // 生成树有 n-1 条边
        }
    }
    
    return edgeCount == n - 1 ? totalWeight : -1;  // -1 表示不连通
}

int main() {
    int n, m;
    cin >> n >> m;
    
    vector<vector<int>> edges(m, vector<int>(3));
    for (int i = 0; i < m; ++i) {
        cin >> edges[i][0] >> edges[i][1] >> edges[i][2];
    }
    
    cout << kruskal(n, edges) << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(m log m)`，空间 `O(n)`

**易错点**：
- 边要按权值排序
- 生成树有 n-1 条边，选够就可以停止
- 如果选不够 n-1 条边说明图不连通

---

### 例题 6：岛屿数量 II（动态加陆地）

**题目**：初始全是水，每次操作在某位置加一块陆地，返回每次操作后的岛屿数量。

**思路**：并查集，每次加陆地时检查四周，合并相邻陆地。

```cpp
#include <bits/stdc++.h>
using namespace std;

class UnionFind {
private:
    vector<int> parent;
    int count;
    
public:
    UnionFind(int n) : count(0) {
        parent.resize(n, -1);  // -1 表示水
    }
    
    int find(int x) {
        if (parent[x] < 0) return -1;
        
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }
    
    void addLand(int x) {
        if (parent[x] >= 0) return;  // 已经是陆地
        
        parent[x] = x;
        count++;
    }
    
    void unite(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);
        
        if (rootX != -1 && rootY != -1 && rootX != rootY) {
            parent[rootX] = rootY;
            count--;
        }
    }
    
    int getCount() {
        return count;
    }
};

vector<int> numIslands2(int m, int n, vector<vector<int>>& positions) {
    UnionFind uf(m * n);
    vector<int> result;
    
    int dx[] = {0, 0, 1, -1};
    int dy[] = {1, -1, 0, 0};
    
    for (auto& pos : positions) {
        int x = pos[0], y = pos[1];
        int idx = x * n + y;
        
        uf.addLand(idx);
        
        // 检查四个方向
        for (int d = 0; d < 4; ++d) {
            int nx = x + dx[d];
            int ny = y + dy[d];
            
            if (nx >= 0 && nx < m && ny >= 0 && ny < n) {
                int nidx = nx * n + ny;
                uf.unite(idx, nidx);
            }
        }
        
        result.push_back(uf.getCount());
    }
    
    return result;
}

int main() {
    int m, n, k;
    cin >> m >> n >> k;
    
    vector<vector<int>> positions(k, vector<int>(2));
    for (int i = 0; i < k; ++i) {
        cin >> positions[i][0] >> positions[i][1];
    }
    
    vector<int> result = numIslands2(m, n, positions);
    
    for (int i = 0; i < result.size(); ++i) {
        cout << result[i] << " \n"[i == result.size() - 1];
    }
    
    return 0;
}
```

**复杂度**：时间 `O(k × α(mn))`，k 是操作数

**易错点**：
- 二维坐标转一维：`x * n + y`
- 用 -1 标记水，防止和陆地索引混淆
- 合并前要检查邻居是否是陆地

---

### 例题 7：除法求值（带权并查集）

**题目**：给定除法方程 `a / b = k`，和查询，求查询结果或返回 -1。

**思路**：带权并查集，权值表示到根节点的倍数关系。

```cpp
#include <bits/stdc++.h>
using namespace std;

class UnionFind {
private:
    unordered_map<string, string> parent;
    unordered_map<string, double> weight;  // 到父节点的权值
    
public:
    void addNode(string x) {
        if (!parent.count(x)) {
            parent[x] = x;
            weight[x] = 1.0;
        }
    }
    
    string find(string x) {
        if (parent[x] != x) {
            string root = find(parent[x]);
            weight[x] *= weight[parent[x]];
            parent[x] = root;
        }
        return parent[x];
    }
    
    void unite(string x, string y, double value) {
        addNode(x);
        addNode(y);
        
        string rootX = find(x);
        string rootY = find(y);
        
        if (rootX != rootY) {
            parent[rootX] = rootY;
            weight[rootX] = weight[y] * value / weight[x];
        }
    }
    
    double query(string x, string y) {
        if (!parent.count(x) || !parent.count(y)) return -1.0;
        
        string rootX = find(x);
        string rootY = find(y);
        
        if (rootX != rootY) return -1.0;
        
        return weight[x] / weight[y];
    }
};

vector<double> calcEquation(vector<vector<string>>& equations, 
                            vector<double>& values, 
                            vector<vector<string>>& queries) {
    UnionFind uf;
    
    for (int i = 0; i < equations.size(); ++i) {
        uf.unite(equations[i][0], equations[i][1], values[i]);
    }
    
    vector<double> result;
    for (auto& query : queries) {
        result.push_back(uf.query(query[0], query[1]));
    }
    
    return result;
}

int main() {
    int n, q;
    cin >> n >> q;
    
    vector<vector<string>> equations(n, vector<string>(2));
    vector<double> values(n);
    
    for (int i = 0; i < n; ++i) {
        cin >> equations[i][0] >> equations[i][1] >> values[i];
    }
    
    vector<vector<string>> queries(q, vector<string>(2));
    for (int i = 0; i < q; ++i) {
        cin >> queries[i][0] >> queries[i][1];
    }
    
    vector<double> result = calcEquation(equations, values, queries);
    
    for (double val : result) {
        cout << fixed << setprecision(5) << val << "\n";
    }
    
    return 0;
}
```

**复杂度**：时间 `O((n + q) × α(n))`

**易错点**：
- weight[x] 表示 x 到 parent[x] 的倍数，即 x / parent[x]
- 路径压缩时要累乘权值：`weight[x] *= weight[parent[x]]`
- 查询时：`x / y = weight[x] / weight[y]`（都是到同一根的倍数）

---

### 例题 8：情侣牵手（置换环）

**题目**：n 对情侣坐成一排，交换最少次数使得每对情侣相邻。

**思路**：并查集，将同一组的情侣合并，每个连通分量大小为 k 需要 k-1 次交换。

```cpp
#include <bits/stdc++.h>
using namespace std;

class UnionFind {
private:
    vector<int> parent;
    
public:
    UnionFind(int n) {
        parent.resize(n);
        for (int i = 0; i < n; ++i) {
            parent[i] = i;
        }
    }
    
    int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }
    
    bool unite(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);
        
        if (rootX == rootY) return false;
        
        parent[rootX] = rootY;
        return true;
    }
};

int minSwapsCouples(vector<int>& row) {
    int n = row.size() / 2;
    UnionFind uf(n);
    
    // 将坐在一起的情侣对（编号）合并
    for (int i = 0; i < row.size(); i += 2) {
        int couple1 = row[i] / 2;
        int couple2 = row[i + 1] / 2;
        uf.unite(couple1, couple2);
    }
    
    // 统计连通分量
    unordered_map<int, int> groups;
    for (int i = 0; i < n; ++i) {
        int root = uf.find(i);
        groups[root]++;
    }
    
    // 每个大小为 k 的连通分量需要 k-1 次交换
    int swaps = 0;
    for (auto& [root, size] : groups) {
        swaps += size - 1;
    }
    
    return swaps;
}

int main() {
    int n;
    cin >> n;
    
    vector<int> row(2 * n);
    for (int i = 0; i < 2 * n; ++i) {
        cin >> row[i];
    }
    
    cout << minSwapsCouples(row) << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(n × α(n))`，空间 `O(n)`

**易错点**：
- 情侣对编号：`person / 2`（0 和 1 是一对，2 和 3 是一对...）
- 每个连通分量大小为 k，需要 k-1 次交换
- 这是置换环问题的经典模型

---

## 常见陷阱

1. **路径压缩**：
   - 必须在 find 中实现：`parent[x] = find(parent[x])`
   - 否则复杂度退化到 O(n)

2. **按秩合并**：
   - 将深度小的树合并到深度大的树
   - 防止树退化成链

3. **初始化**：
   - parent[i] = i（每个节点是自己的根）
   - count = n（初始有 n 个连通分量）

4. **带权并查集**：
   - 路径压缩时要更新权值
   - 权值的含义要清晰（到父节点还是到根节点）

5. **字符串节点**：
   - 可以用 `unordered_map<string, string>` 作为 parent
   - 或者先映射到整数

## 适用场景总结

| 问题类型 | 关键操作 | 时间复杂度 |
|---------|---------|-----------|
| 连通性判断 | find | O(α(n)) |
| 集合合并 | unite | O(α(n)) |
| 连通分量计数 | getCount | O(1) |
| 检测环 | unite 返回 false | O(α(n)) |
| 最小生成树 | 排序 + unite | O(m log m) |
| 动态连通性 | 逐步 unite | O(k × α(n)) |
| 等价关系 | unite + connected | O(α(n)) |
| 带权关系 | 带权并查集 | O(α(n)) |

**核心技巧**：
- 路径压缩：`parent[x] = find(parent[x])`
- 按秩合并：将小树合并到大树
- 两个优化使得单次操作接近 O(1)
- 并查集只能合并，不能拆分
- 适合处理动态连通性和等价关系
