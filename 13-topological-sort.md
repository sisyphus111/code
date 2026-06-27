# 拓扑排序与 DAG

## 什么时候用

看到以下特征优先考虑拓扑排序：
- **有向无环图（DAG）**：依赖关系、先后顺序
- **任务调度**：某些任务必须在其他任务之前完成
- **课程安排**：先修课程关系
- **编译顺序**：模块依赖
- **事件顺序**：事件之间有先后约束
- 题目中出现"依赖"、"前置条件"、"顺序"、"先后"等字眼

核心思路：**不断选择入度为 0 的节点，去除后更新其他节点的入度**。

## 核心模板

### BFS 拓扑排序（Kahn 算法）

```cpp
vector<int> topologicalSort(int n, vector<vector<int>>& edges) {
    vector<vector<int>> graph(n);
    vector<int> inDegree(n, 0);
    
    // 建图并统计入度
    for (auto& edge : edges) {
        int u = edge[0], v = edge[1];
        graph[u].push_back(v);
        inDegree[v]++;
    }
    
    // 将入度为 0 的节点入队
    queue<int> q;
    for (int i = 0; i < n; ++i) {
        if (inDegree[i] == 0) {
            q.push(i);
        }
    }
    
    vector<int> result;
    
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        result.push_back(u);
        
        // 删除该节点，更新邻居的入度
        for (int v : graph[u]) {
            if (--inDegree[v] == 0) {
                q.push(v);
            }
        }
    }
    
    // 如果不能访问所有节点，说明有环
    return result.size() == n ? result : vector<int>();
}
```

### DFS 拓扑排序

```cpp
bool dfs(int u, vector<vector<int>>& graph, vector<int>& color, vector<int>& result) {
    color[u] = 1;  // 标记为访问中
    
    for (int v : graph[u]) {
        if (color[v] == 1) return false;  // 有环
        if (color[v] == 0 && !dfs(v, graph, color, result)) {
            return false;
        }
    }
    
    color[u] = 2;  // 标记为已完成
    result.push_back(u);
    return true;
}

vector<int> topologicalSort(int n, vector<vector<int>>& edges) {
    vector<vector<int>> graph(n);
    
    for (auto& edge : edges) {
        graph[edge[0]].push_back(edge[1]);
    }
    
    vector<int> color(n, 0);
    vector<int> result;
    
    for (int i = 0; i < n; ++i) {
        if (color[i] == 0) {
            if (!dfs(i, graph, color, result)) {
                return {};  // 有环
            }
        }
    }
    
    reverse(result.begin(), result.end());  // 逆序
    return result;
}
```

### DAG 上的最长路径

```cpp
int longestPath(int n, vector<vector<int>>& edges) {
    vector<vector<int>> graph(n);
    vector<int> inDegree(n, 0);
    
    for (auto& edge : edges) {
        graph[edge[0]].push_back(edge[1]);
        inDegree[edge[1]]++;
    }
    
    queue<int> q;
    vector<int> dist(n, 0);
    
    for (int i = 0; i < n; ++i) {
        if (inDegree[i] == 0) {
            q.push(i);
        }
    }
    
    int maxDist = 0;
    
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        
        maxDist = max(maxDist, dist[u]);
        
        for (int v : graph[u]) {
            dist[v] = max(dist[v], dist[u] + 1);
            
            if (--inDegree[v] == 0) {
                q.push(v);
            }
        }
    }
    
    return maxDist;
}
```

## 例题演示

### 例题 1：课程表

**题目**：n 门课程，给定先修关系，判断是否能完成所有课程（是否有环）。

**思路**：拓扑排序，如果能排序成功说明无环。

```cpp
#include <bits/stdc++.h>
using namespace std;

bool canFinish(int n, vector<vector<int>>& prerequisites) {
    vector<vector<int>> graph(n);
    vector<int> inDegree(n, 0);
    
    for (auto& pre : prerequisites) {
        int course = pre[0], prerequisite = pre[1];
        graph[prerequisite].push_back(course);
        inDegree[course]++;
    }
    
    queue<int> q;
    for (int i = 0; i < n; ++i) {
        if (inDegree[i] == 0) {
            q.push(i);
        }
    }
    
    int count = 0;
    
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        count++;
        
        for (int v : graph[u]) {
            if (--inDegree[v] == 0) {
                q.push(v);
            }
        }
    }
    
    return count == n;
}

int main() {
    int n, m;
    cin >> n >> m;
    
    vector<vector<int>> prerequisites(m, vector<int>(2));
    for (int i = 0; i < m; ++i) {
        cin >> prerequisites[i][0] >> prerequisites[i][1];
    }
    
    cout << (canFinish(n, prerequisites) ? "YES" : "NO") << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(V + E)`，空间 `O(V + E)`

**易错点**：
- 边的方向：prerequisite → course
- 如果 count != n 说明有环
- 也可以用 DFS 三色标记判断环

---

### 例题 2：课程表 II（输出拓扑序）

**题目**：返回一个合法的课程学习顺序，如果不存在返回空。

**思路**：拓扑排序，记录访问顺序。

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> findOrder(int n, vector<vector<int>>& prerequisites) {
    vector<vector<int>> graph(n);
    vector<int> inDegree(n, 0);
    
    for (auto& pre : prerequisites) {
        graph[pre[1]].push_back(pre[0]);
        inDegree[pre[0]]++;
    }
    
    queue<int> q;
    for (int i = 0; i < n; ++i) {
        if (inDegree[i] == 0) {
            q.push(i);
        }
    }
    
    vector<int> result;
    
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        result.push_back(u);
        
        for (int v : graph[u]) {
            if (--inDegree[v] == 0) {
                q.push(v);
            }
        }
    }
    
    return result.size() == n ? result : vector<int>();
}

int main() {
    int n, m;
    cin >> n >> m;
    
    vector<vector<int>> prerequisites(m, vector<int>(2));
    for (int i = 0; i < m; ++i) {
        cin >> prerequisites[i][0] >> prerequisites[i][1];
    }
    
    vector<int> order = findOrder(n, prerequisites);
    
    if (order.empty()) {
        cout << "Impossible\n";
    } else {
        for (int i = 0; i < order.size(); ++i) {
            cout << order[i] << " \n"[i == order.size() - 1];
        }
    }
    
    return 0;
}
```

**复杂度**：时间 `O(V + E)`，空间 `O(V + E)`

**易错点**：
- 拓扑序不唯一，任何合法序列都可以
- 结果长度不等于 n 说明有环

---

### 例题 3：外星文字典（推导字符顺序）

**题目**：给定按字典序排列的外星单词，推导字符的字典序。

**思路**：相邻单词比较，第一个不同字符决定顺序，建图后拓扑排序。

```cpp
#include <bits/stdc++.h>
using namespace std;

string alienOrder(vector<string>& words) {
    unordered_map<char, set<char>> graph;
    unordered_map<char, int> inDegree;
    
    // 初始化所有字符
    for (auto& word : words) {
        for (char c : word) {
            inDegree[c] = 0;
        }
    }
    
    // 建图
    for (int i = 0; i < words.size() - 1; ++i) {
        string w1 = words[i], w2 = words[i + 1];
        int len = min(w1.size(), w2.size());
        
        // 特判：w1 是 w2 的前缀但更长，非法
        if (w1.size() > w2.size() && w1.substr(0, len) == w2) {
            return "";
        }
        
        for (int j = 0; j < len; ++j) {
            if (w1[j] != w2[j]) {
                if (!graph[w1[j]].count(w2[j])) {
                    graph[w1[j]].insert(w2[j]);
                    inDegree[w2[j]]++;
                }
                break;
            }
        }
    }
    
    // 拓扑排序
    queue<char> q;
    for (auto& [c, deg] : inDegree) {
        if (deg == 0) {
            q.push(c);
        }
    }
    
    string result;
    
    while (!q.empty()) {
        char u = q.front();
        q.pop();
        result += u;
        
        for (char v : graph[u]) {
            if (--inDegree[v] == 0) {
                q.push(v);
            }
        }
    }
    
    return result.size() == inDegree.size() ? result : "";
}

int main() {
    int n;
    cin >> n;
    
    vector<string> words(n);
    for (int i = 0; i < n; ++i) {
        cin >> words[i];
    }
    
    string order = alienOrder(words);
    
    if (order.empty()) {
        cout << "Invalid\n";
    } else {
        cout << order << "\n";
    }
    
    return 0;
}
```

**复杂度**：时间 `O(C)` C 是所有单词的字符总数，空间 `O(1)` 最多 26 个字符

**易错点**：
- 只比较相邻单词的第一个不同字符
- 特判：前面单词是后面单词的前缀但更长，非法
- 用 set 避免重复边

---

### 例题 4：并行课程（最少学期数）

**题目**：给定课程依赖关系，每学期可以学多门课，求最少需要多少学期。

**思路**：拓扑排序 + 分层 BFS，层数就是学期数。

```cpp
#include <bits/stdc++.h>
using namespace std;

int minimumSemesters(int n, vector<vector<int>>& relations) {
    vector<vector<int>> graph(n + 1);
    vector<int> inDegree(n + 1, 0);
    
    for (auto& rel : relations) {
        graph[rel[0]].push_back(rel[1]);
        inDegree[rel[1]]++;
    }
    
    queue<int> q;
    for (int i = 1; i <= n; ++i) {
        if (inDegree[i] == 0) {
            q.push(i);
        }
    }
    
    int semesters = 0;
    int studied = 0;
    
    while (!q.empty()) {
        int size = q.size();
        semesters++;
        
        for (int i = 0; i < size; ++i) {
            int u = q.front();
            q.pop();
            studied++;
            
            for (int v : graph[u]) {
                if (--inDegree[v] == 0) {
                    q.push(v);
                }
            }
        }
    }
    
    return studied == n ? semesters : -1;
}

int main() {
    int n, m;
    cin >> n >> m;
    
    vector<vector<int>> relations(m, vector<int>(2));
    for (int i = 0; i < m; ++i) {
        cin >> relations[i][0] >> relations[i][1];
    }
    
    cout << minimumSemesters(n, relations) << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(V + E)`，空间 `O(V + E)`

**易错点**：
- 每层是一个学期，要记录层数
- 如果 studied != n 说明有环

---

### 例题 5：序列重建（唯一拓扑序）

**题目**：给定原序列和若干子序列，判断子序列能否唯一重建原序列。

**思路**：拓扑排序，检查是否唯一（每次只有一个入度为 0 的节点）。

```cpp
#include <bits/stdc++.h>
using namespace std;

bool sequenceReconstruction(vector<int>& org, vector<vector<int>>& seqs) {
    int n = org.size();
    unordered_map<int, set<int>> graph;
    unordered_map<int, int> inDegree;
    
    // 初始化
    for (int i = 1; i <= n; ++i) {
        inDegree[i] = 0;
    }
    
    // 建图
    for (auto& seq : seqs) {
        for (int i = 0; i < seq.size(); ++i) {
            if (seq[i] < 1 || seq[i] > n) return false;
            
            if (i > 0) {
                if (!graph[seq[i-1]].count(seq[i])) {
                    graph[seq[i-1]].insert(seq[i]);
                    inDegree[seq[i]]++;
                }
            }
        }
    }
    
    // 拓扑排序
    queue<int> q;
    for (int i = 1; i <= n; ++i) {
        if (inDegree[i] == 0) {
            q.push(i);
        }
    }
    
    int idx = 0;
    
    while (!q.empty()) {
        if (q.size() > 1) return false;  // 不唯一
        
        int u = q.front();
        q.pop();
        
        if (idx >= n || org[idx] != u) return false;
        idx++;
        
        for (int v : graph[u]) {
            if (--inDegree[v] == 0) {
                q.push(v);
            }
        }
    }
    
    return idx == n;
}

int main() {
    int n, m;
    cin >> n >> m;
    
    vector<int> org(n);
    for (int i = 0; i < n; ++i) {
        cin >> org[i];
    }
    
    vector<vector<int>> seqs(m);
    for (int i = 0; i < m; ++i) {
        int k;
        cin >> k;
        seqs[i].resize(k);
        for (int j = 0; j < k; ++j) {
            cin >> seqs[i][j];
        }
    }
    
    cout << (sequenceReconstruction(org, seqs) ? "YES" : "NO") << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(V + E)`，空间 `O(V + E)`

**易错点**：
- 唯一性：每次队列只有一个元素
- 要验证拓扑序和原序列完全一致
- 数字范围要在 [1, n]

---

### 例题 6：DAG 上的最长路径

**题目**：有向无环图，求最长路径长度。

**思路**：拓扑排序 + DP，每个节点的最长路径是其前驱的最长路径 + 1。

```cpp
#include <bits/stdc++.h>
using namespace std;

int longestPath(int n, vector<vector<int>>& edges) {
    vector<vector<int>> graph(n);
    vector<int> inDegree(n, 0);
    
    for (auto& edge : edges) {
        graph[edge[0]].push_back(edge[1]);
        inDegree[edge[1]]++;
    }
    
    queue<int> q;
    vector<int> dist(n, 0);
    
    for (int i = 0; i < n; ++i) {
        if (inDegree[i] == 0) {
            q.push(i);
        }
    }
    
    int maxDist = 0;
    
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        
        maxDist = max(maxDist, dist[u]);
        
        for (int v : graph[u]) {
            dist[v] = max(dist[v], dist[u] + 1);
            
            if (--inDegree[v] == 0) {
                q.push(v);
            }
        }
    }
    
    return maxDist;
}

int main() {
    int n, m;
    cin >> n >> m;
    
    vector<vector<int>> edges(m, vector<int>(2));
    for (int i = 0; i < m; ++i) {
        cin >> edges[i][0] >> edges[i][1];
    }
    
    cout << longestPath(n, edges) << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(V + E)`，空间 `O(V)`

**易错点**：
- dist[v] 取所有前驱的最大值 + 1
- 最长路径不一定经过所有节点

---

### 例题 7：受限条件下的可达性

**题目**：给定有向图和一些限制边，问从起点到终点是否可达且满足限制。

**思路**：拓扑排序 + 可达性判断。

```cpp
#include <bits/stdc++.h>
using namespace std;

bool isReachable(int n, vector<vector<int>>& edges, 
                 vector<vector<int>>& restrictions, int src, int dst) {
    vector<vector<int>> graph(n);
    vector<int> inDegree(n, 0);
    set<pair<int,int>> restricted;
    
    for (auto& r : restrictions) {
        restricted.insert({r[0], r[1]});
    }
    
    for (auto& edge : edges) {
        int u = edge[0], v = edge[1];
        
        if (!restricted.count({u, v})) {
            graph[u].push_back(v);
            inDegree[v]++;
        }
    }
    
    queue<int> q;
    vector<bool> visited(n, false);
    
    for (int i = 0; i < n; ++i) {
        if (inDegree[i] == 0) {
            q.push(i);
        }
    }
    
    // 从 src 开始 BFS
    queue<int> bfsQ;
    bfsQ.push(src);
    visited[src] = true;
    
    while (!bfsQ.empty()) {
        int u = bfsQ.front();
        bfsQ.pop();
        
        if (u == dst) return true;
        
        for (int v : graph[u]) {
            if (!visited[v]) {
                visited[v] = true;
                bfsQ.push(v);
            }
        }
    }
    
    return false;
}

int main() {
    int n, m, r, src, dst;
    cin >> n >> m >> r >> src >> dst;
    
    vector<vector<int>> edges(m, vector<int>(2));
    for (int i = 0; i < m; ++i) {
        cin >> edges[i][0] >> edges[i][1];
    }
    
    vector<vector<int>> restrictions(r, vector<int>(2));
    for (int i = 0; i < r; ++i) {
        cin >> restrictions[i][0] >> restrictions[i][1];
    }
    
    cout << (isReachable(n, edges, restrictions, src, dst) ? "YES" : "NO") << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(V + E)`，空间 `O(V + E)`

**易错点**：
- 受限边要从图中删除
- 用 BFS 判断可达性

---

### 例题 8：找到所有的祖先节点

**题目**：给定 DAG，找到每个节点的所有祖先。

**思路**：拓扑排序 + 传递祖先集合。

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<vector<int>> getAncestors(int n, vector<vector<int>>& edges) {
    vector<vector<int>> graph(n);
    vector<int> inDegree(n, 0);
    
    for (auto& edge : edges) {
        graph[edge[0]].push_back(edge[1]);
        inDegree[edge[1]]++;
    }
    
    queue<int> q;
    vector<set<int>> ancestors(n);
    
    for (int i = 0; i < n; ++i) {
        if (inDegree[i] == 0) {
            q.push(i);
        }
    }
    
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        
        for (int v : graph[u]) {
            // v 的祖先包括 u 和 u 的所有祖先
            ancestors[v].insert(u);
            for (int ancestor : ancestors[u]) {
                ancestors[v].insert(ancestor);
            }
            
            if (--inDegree[v] == 0) {
                q.push(v);
            }
        }
    }
    
    vector<vector<int>> result(n);
    for (int i = 0; i < n; ++i) {
        result[i] = vector<int>(ancestors[i].begin(), ancestors[i].end());
    }
    
    return result;
}

int main() {
    int n, m;
    cin >> n >> m;
    
    vector<vector<int>> edges(m, vector<int>(2));
    for (int i = 0; i < m; ++i) {
        cin >> edges[i][0] >> edges[i][1];
    }
    
    vector<vector<int>> result = getAncestors(n, edges);
    
    for (int i = 0; i < n; ++i) {
        cout << i << ": ";
        for (int j = 0; j < result[i].size(); ++j) {
            cout << result[i][j] << " \n"[j == result[i].size() - 1];
        }
        if (result[i].empty()) cout << "\n";
    }
    
    return 0;
}
```

**复杂度**：时间 `O(V × (V + E))`，空间 `O(V^2)`

**易错点**：
- 要传递祖先集合，不只是直接父节点
- 用 set 自动去重和排序

---

## 常见陷阱

1. **环检测**：
   - 拓扑排序成功 ⇔ 无环
   - 如果访问节点数 < 总节点数，说明有环

2. **边的方向**：
   - 依赖关系：前置 → 后续
   - 入度：指向该节点的边数

3. **拓扑序不唯一**：
   - 多个入度为 0 的节点可以任意顺序
   - 唯一性判断：每次只有一个入度为 0 的节点

4. **BFS vs DFS**：
   - BFS（Kahn）：更直观，易于分层
   - DFS：代码更短，结果需要逆序

5. **初始化**：
   - 所有节点都要初始化入度
   - 孤立节点入度为 0

## 适用场景总结

| 问题类型 | 关键技巧 | 时间复杂度 |
|---------|---------|-----------|
| 环检测 | 拓扑排序成功 ⇔ 无环 | O(V + E) |
| 任务调度 | 拓扑序就是执行顺序 | O(V + E) |
| 最少批次 | 拓扑排序 + 分层 BFS | O(V + E) |
| 唯一性判断 | 每次队列只有一个元素 | O(V + E) |
| DAG 最长路径 | 拓扑排序 + DP | O(V + E) |
| 字典序推导 | 相邻比较 + 拓扑排序 | O(C) |
| 祖先传递 | 拓扑排序 + 集合合并 | O(V × (V+E)) |

**核心技巧**：
- 拓扑排序只适用于 DAG（有向无环图）
- BFS（Kahn）：从入度为 0 开始，逐步删除节点
- DFS：后序遍历逆序就是拓扑序
- 拓扑排序 + DP 可以求 DAG 上的路径问题
- 分层 BFS 可以求最少批次/最短时间
- 唯一拓扑序：每次只有一个选择
