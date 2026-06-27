# 图的遍历与连通性

## 什么时候用

看到以下特征优先考虑图的遍历：
- **连通性判断**：判断两点是否连通
- **路径存在性**：是否存在从 A 到 B 的路径
- **所有可达节点**：从某点出发能到达哪些节点
- **环检测**：有向图/无向图是否有环
- **二分图判定**：能否将节点分成两组，组内无边
- **强连通分量**：有向图中互相可达的节点集合
- 题目中出现"图"、"网络"、"依赖关系"等字眼

核心思路：**DFS 用于深度探索和路径问题，BFS 用于层次遍历和最短路径**。

## 核心模板

### DFS 遍历（邻接表）

```cpp
vector<vector<int>> graph;
vector<bool> visited;

void dfs(int u) {
    visited[u] = true;
    
    for (int v : graph[u]) {
        if (!visited[v]) {
            dfs(v);
        }
    }
}
```

### BFS 遍历

```cpp
void bfs(int start) {
    queue<int> q;
    vector<bool> visited(n, false);
    
    q.push(start);
    visited[start] = true;
    
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        
        for (int v : graph[u]) {
            if (!visited[v]) {
                visited[v] = true;
                q.push(v);
            }
        }
    }
}
```

### 无向图环检测（DFS）

```cpp
bool hasCycleDFS(int u, int parent) {
    visited[u] = true;
    
    for (int v : graph[u]) {
        if (!visited[v]) {
            if (hasCycleDFS(v, u)) return true;
        } else if (v != parent) {
            return true;  // 访问到非父节点的已访问节点，有环
        }
    }
    
    return false;
}
```

### 有向图环检测（拓扑排序）

```cpp
bool hasCycleTopo(int n, vector<vector<int>>& graph) {
    vector<int> inDegree(n, 0);
    
    for (int u = 0; u < n; ++u) {
        for (int v : graph[u]) {
            inDegree[v]++;
        }
    }
    
    queue<int> q;
    for (int i = 0; i < n; ++i) {
        if (inDegree[i] == 0) q.push(i);
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
    
    return count != n;  // 不能访问所有节点说明有环
}
```

### 二分图判定（染色法）

```cpp
bool isBipartite(vector<vector<int>>& graph) {
    int n = graph.size();
    vector<int> color(n, -1);
    
    for (int i = 0; i < n; ++i) {
        if (color[i] == -1) {
            queue<int> q;
            q.push(i);
            color[i] = 0;
            
            while (!q.empty()) {
                int u = q.front();
                q.pop();
                
                for (int v : graph[u]) {
                    if (color[v] == -1) {
                        color[v] = 1 - color[u];
                        q.push(v);
                    } else if (color[v] == color[u]) {
                        return false;
                    }
                }
            }
        }
    }
    
    return true;
}
```

## 例题演示

### 例题 1：所有可达节点

**题目**：给定有向图和起点，返回从起点可达的所有节点。

**思路**：DFS 或 BFS 遍历，记录访问过的节点。

```cpp
#include <bits/stdc++.h>
using namespace std;

void dfs(int u, vector<vector<int>>& graph, vector<bool>& visited) {
    visited[u] = true;
    
    for (int v : graph[u]) {
        if (!visited[v]) {
            dfs(v, graph, visited);
        }
    }
}

vector<int> reachableNodes(int n, vector<vector<int>>& edges, int start) {
    vector<vector<int>> graph(n);
    
    for (auto& edge : edges) {
        graph[edge[0]].push_back(edge[1]);
    }
    
    vector<bool> visited(n, false);
    dfs(start, graph, visited);
    
    vector<int> result;
    for (int i = 0; i < n; ++i) {
        if (visited[i]) {
            result.push_back(i);
        }
    }
    
    return result;
}

int main() {
    int n, m, start;
    cin >> n >> m >> start;
    
    vector<vector<int>> edges(m, vector<int>(2));
    for (int i = 0; i < m; ++i) {
        cin >> edges[i][0] >> edges[i][1];
    }
    
    vector<int> result = reachableNodes(n, edges, start);
    
    for (int i = 0; i < result.size(); ++i) {
        cout << result[i] << " \n"[i == result.size() - 1];
    }
    
    return 0;
}
```

**复杂度**：时间 `O(V + E)`，空间 `O(V)`

**易错点**：
- DFS 要先标记再递归，避免重复访问
- 有向图和无向图建图方式不同

---

### 例题 2：无向图中的环

**题目**：判断无向图是否有环。

**思路**：DFS，记录父节点，如果访问到非父节点的已访问节点则有环。

```cpp
#include <bits/stdc++.h>
using namespace std;

bool dfs(int u, int parent, vector<vector<int>>& graph, vector<bool>& visited) {
    visited[u] = true;
    
    for (int v : graph[u]) {
        if (!visited[v]) {
            if (dfs(v, u, graph, visited)) {
                return true;
            }
        } else if (v != parent) {
            return true;  // 访问到非父节点的已访问节点
        }
    }
    
    return false;
}

bool hasCycle(int n, vector<vector<int>>& edges) {
    vector<vector<int>> graph(n);
    
    for (auto& edge : edges) {
        graph[edge[0]].push_back(edge[1]);
        graph[edge[1]].push_back(edge[0]);
    }
    
    vector<bool> visited(n, false);
    
    for (int i = 0; i < n; ++i) {
        if (!visited[i]) {
            if (dfs(i, -1, graph, visited)) {
                return true;
            }
        }
    }
    
    return false;
}

int main() {
    int n, m;
    cin >> n >> m;
    
    vector<vector<int>> edges(m, vector<int>(2));
    for (int i = 0; i < m; ++i) {
        cin >> edges[i][0] >> edges[i][1];
    }
    
    cout << (hasCycle(n, edges) ? "YES" : "NO") << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(V + E)`，空间 `O(V)`

**易错点**：
- 无向图需要记录父节点，避免回到父节点被误判为环
- 图可能不连通，要遍历所有未访问的节点

---

### 例题 3：有向图中的环

**题目**：判断有向图是否有环。

**思路**：DFS + 三色标记（白色未访问，灰色访问中，黑色已完成）。

```cpp
#include <bits/stdc++.h>
using namespace std;

bool dfs(int u, vector<vector<int>>& graph, vector<int>& color) {
    color[u] = 1;  // 标记为访问中（灰色）
    
    for (int v : graph[u]) {
        if (color[v] == 1) {
            return true;  // 访问到灰色节点，有环
        }
        
        if (color[v] == 0 && dfs(v, graph, color)) {
            return true;
        }
    }
    
    color[u] = 2;  // 标记为已完成（黑色）
    return false;
}

bool hasCycle(int n, vector<vector<int>>& edges) {
    vector<vector<int>> graph(n);
    
    for (auto& edge : edges) {
        graph[edge[0]].push_back(edge[1]);
    }
    
    vector<int> color(n, 0);  // 0-白色, 1-灰色, 2-黑色
    
    for (int i = 0; i < n; ++i) {
        if (color[i] == 0) {
            if (dfs(i, graph, color)) {
                return true;
            }
        }
    }
    
    return false;
}

int main() {
    int n, m;
    cin >> n >> m;
    
    vector<vector<int>> edges(m, vector<int>(2));
    for (int i = 0; i < m; ++i) {
        cin >> edges[i][0] >> edges[i][1];
    }
    
    cout << (hasCycle(n, edges) ? "YES" : "NO") << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(V + E)`，空间 `O(V)`

**易错点**：
- 有向图环检测用三色标记，不能只用 visited
- 灰色节点表示在当前 DFS 路径上
- 访问到灰色节点说明有环

---

### 例题 4：二分图判定

**题目**：判断图是否是二分图（能否用两种颜色染色，相邻节点颜色不同）。

**思路**：BFS/DFS 染色，如果相邻节点颜色相同则不是二分图。

```cpp
#include <bits/stdc++.h>
using namespace std;

bool bfs(int start, vector<vector<int>>& graph, vector<int>& color) {
    queue<int> q;
    q.push(start);
    color[start] = 0;
    
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        
        for (int v : graph[u]) {
            if (color[v] == -1) {
                color[v] = 1 - color[u];
                q.push(v);
            } else if (color[v] == color[u]) {
                return false;
            }
        }
    }
    
    return true;
}

bool isBipartite(int n, vector<vector<int>>& edges) {
    vector<vector<int>> graph(n);
    
    for (auto& edge : edges) {
        graph[edge[0]].push_back(edge[1]);
        graph[edge[1]].push_back(edge[0]);
    }
    
    vector<int> color(n, -1);
    
    for (int i = 0; i < n; ++i) {
        if (color[i] == -1) {
            if (!bfs(i, graph, color)) {
                return false;
            }
        }
    }
    
    return true;
}

int main() {
    int n, m;
    cin >> n >> m;
    
    vector<vector<int>> edges(m, vector<int>(2));
    for (int i = 0; i < m; ++i) {
        cin >> edges[i][0] >> edges[i][1];
    }
    
    cout << (isBipartite(n, edges) ? "YES" : "NO") << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(V + E)`，空间 `O(V)`

**易错点**：
- 图可能不连通，要遍历所有未染色的节点
- 用 -1 表示未染色，0 和 1 表示两种颜色
- 有奇数环的图一定不是二分图

---

### 例题 5：克隆图

**题目**：深拷贝无向连通图。

**思路**：DFS/BFS 遍历，用哈希表存储原节点到新节点的映射。

```cpp
#include <bits/stdc++.h>
using namespace std;

class Node {
public:
    int val;
    vector<Node*> neighbors;
    
    Node() : val(0) {}
    Node(int _val) : val(_val) {}
    Node(int _val, vector<Node*> _neighbors) : val(_val), neighbors(_neighbors) {}
};

Node* cloneGraph(Node* node) {
    if (!node) return nullptr;
    
    unordered_map<Node*, Node*> visited;
    
    function<Node*(Node*)> dfs = [&](Node* u) -> Node* {
        if (visited.count(u)) {
            return visited[u];
        }
        
        Node* clone = new Node(u->val);
        visited[u] = clone;
        
        for (Node* neighbor : u->neighbors) {
            clone->neighbors.push_back(dfs(neighbor));
        }
        
        return clone;
    };
    
    return dfs(node);
}

int main() {
    // 简化输入：邻接表格式
    int n;
    cin >> n;
    
    if (n == 0) {
        cout << "null\n";
        return 0;
    }
    
    vector<Node*> nodes(n + 1);
    for (int i = 1; i <= n; ++i) {
        nodes[i] = new Node(i);
    }
    
    for (int i = 1; i <= n; ++i) {
        int k;
        cin >> k;
        for (int j = 0; j < k; ++j) {
            int neighbor;
            cin >> neighbor;
            nodes[i]->neighbors.push_back(nodes[neighbor]);
        }
    }
    
    Node* cloned = cloneGraph(nodes[1]);
    
    cout << "Cloned graph with root value: " << cloned->val << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(V + E)`，空间 `O(V)`

**易错点**：
- 要先创建新节点再递归，避免无限递归
- 用哈希表记录原节点和新节点的对应关系
- 如果已经克隆过，直接返回对应的新节点

---

### 例题 6：课程表（有向图环检测）

**题目**：n 门课程，给定先修关系，判断是否能完成所有课程。

**思路**：建立有向图，判断是否有环。

```cpp
#include <bits/stdc++.h>
using namespace std;

bool dfs(int u, vector<vector<int>>& graph, vector<int>& color) {
    color[u] = 1;
    
    for (int v : graph[u]) {
        if (color[v] == 1) return true;
        if (color[v] == 0 && dfs(v, graph, color)) return true;
    }
    
    color[u] = 2;
    return false;
}

bool canFinish(int n, vector<vector<int>>& prerequisites) {
    vector<vector<int>> graph(n);
    
    for (auto& pre : prerequisites) {
        graph[pre[1]].push_back(pre[0]);  // pre[1] -> pre[0]
    }
    
    vector<int> color(n, 0);
    
    for (int i = 0; i < n; ++i) {
        if (color[i] == 0) {
            if (dfs(i, graph, color)) {
                return false;
            }
        }
    }
    
    return true;
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

**复杂度**：时间 `O(V + E)`，空间 `O(V)`

**易错点**：
- 建图时注意方向：pre[1] 是 pre[0] 的前置
- 有环则不能完成所有课程

---

### 例题 7：连通分量计数

**题目**：计算无向图中连通分量的数量。

**思路**：DFS/BFS，每次从未访问节点开始遍历，计数加一。

```cpp
#include <bits/stdc++.h>
using namespace std;

void dfs(int u, vector<vector<int>>& graph, vector<bool>& visited) {
    visited[u] = true;
    
    for (int v : graph[u]) {
        if (!visited[v]) {
            dfs(v, graph, visited);
        }
    }
}

int countComponents(int n, vector<vector<int>>& edges) {
    vector<vector<int>> graph(n);
    
    for (auto& edge : edges) {
        graph[edge[0]].push_back(edge[1]);
        graph[edge[1]].push_back(edge[0]);
    }
    
    vector<bool> visited(n, false);
    int count = 0;
    
    for (int i = 0; i < n; ++i) {
        if (!visited[i]) {
            dfs(i, graph, visited);
            count++;
        }
    }
    
    return count;
}

int main() {
    int n, m;
    cin >> n >> m;
    
    vector<vector<int>> edges(m, vector<int>(2));
    for (int i = 0; i < m; ++i) {
        cin >> edges[i][0] >> edges[i][1];
    }
    
    cout << countComponents(n, edges) << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(V + E)`，空间 `O(V)`

**易错点**：
- 每次 DFS 从一个未访问节点开始，就是一个新的连通分量
- 也可以用并查集解决

---

### 例题 8：所有路径（有向无环图）

**题目**：给定有向无环图，找出从起点到终点的所有路径。

**思路**：DFS + 回溯，记录当前路径。

```cpp
#include <bits/stdc++.h>
using namespace std;

void dfs(int u, int target, vector<vector<int>>& graph, 
         vector<int>& path, vector<vector<int>>& result) {
    path.push_back(u);
    
    if (u == target) {
        result.push_back(path);
    } else {
        for (int v : graph[u]) {
            dfs(v, target, graph, path, result);
        }
    }
    
    path.pop_back();
}

vector<vector<int>> allPathsSourceTarget(vector<vector<int>>& graph) {
    vector<vector<int>> result;
    vector<int> path;
    
    dfs(0, graph.size() - 1, graph, path, result);
    
    return result;
}

int main() {
    int n;
    cin >> n;
    
    vector<vector<int>> graph(n);
    for (int i = 0; i < n; ++i) {
        int k;
        cin >> k;
        for (int j = 0; j < k; ++j) {
            int neighbor;
            cin >> neighbor;
            graph[i].push_back(neighbor);
        }
    }
    
    vector<vector<int>> result = allPathsSourceTarget(graph);
    
    for (auto& path : result) {
        for (int i = 0; i < path.size(); ++i) {
            cout << path[i] << " \n"[i == path.size() - 1];
        }
    }
    
    return 0;
}
```

**复杂度**：时间 `O(2^V × V)`，最坏情况指数级

**易错点**：
- DAG 不需要 visited，因为无环
- 要回溯（pop_back），保证路径正确
- 每个节点都可能被访问多次（在不同路径中）

---

## 常见陷阱

1. **图的表示**：
   - 邻接表：`vector<vector<int>>`，适合稀疏图
   - 邻接矩阵：`vector<vector<int>>`，适合密集图
   - 边列表：`vector<pair<int,int>>`，建图前需要转换

2. **有向图 vs 无向图**：
   - 无向图建图：两个方向都要加边
   - 有向图环检测：用三色标记
   - 无向图环检测：记录父节点

3. **连通性**：
   - 图可能不连通，要遍历所有未访问节点
   - 连通分量计数：每次 DFS 开始计数加一

4. **visited 时机**：
   - DFS：进入时标记
   - BFS：入队时标记
   - 回溯：需要撤销标记

5. **环检测**：
   - 有向图：三色标记（白灰黑）
   - 无向图：记录父节点
   - 也可以用拓扑排序判断有向图环

## 适用场景总结

| 问题类型 | 算法 | 时间复杂度 |
|---------|------|-----------|
| 连通性判断 | DFS/BFS | O(V + E) |
| 所有可达节点 | DFS/BFS | O(V + E) |
| 无向图环检测 | DFS + 父节点 | O(V + E) |
| 有向图环检测 | DFS + 三色 | O(V + E) |
| 二分图判定 | BFS/DFS 染色 | O(V + E) |
| 连通分量计数 | DFS/BFS/并查集 | O(V + E) |
| 克隆图 | DFS + 哈希表 | O(V + E) |
| 所有路径 | DFS + 回溯 | 指数级 |

**核心技巧**：
- DFS 适合路径问题、环检测、连通性
- BFS 适合层次遍历、最短路径
- 三色标记是有向图环检测的标准方法
- 染色法是二分图判定的标准方法
- 图可能不连通，要考虑多个起点
