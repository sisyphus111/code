# 最短路径：Dijkstra, Floyd 等

## 什么时候用

看到以下特征优先考虑最短路径算法：
- **单源最短路径**：从一个点到其他所有点的最短距离
- **全源最短路径**：任意两点之间的最短距离
- **带权图最短路径**：边有权值（距离、时间、代价）
- **网络延迟、最小成本**：实际应用问题
- 题目中出现"最短"、"最快"、"最小代价"、"最优路径"等字眼

核心思路：**贪心选择当前最近的未访问节点（Dijkstra），或动态规划枚举中间节点（Floyd）**。

## 核心模板

### Dijkstra（单源最短路径，非负权）

```cpp
vector<int> dijkstra(int n, vector<vector<pair<int,int>>>& graph, int start) {
    vector<int> dist(n, INT_MAX);
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;
    
    dist[start] = 0;
    pq.push({0, start});  // {距离, 节点}
    
    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        
        if (d > dist[u]) continue;  // 已经找到更短路径
        
        for (auto [v, w] : graph[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    
    return dist;
}
```

### Floyd-Warshall（全源最短路径）

```cpp
void floyd(vector<vector<int>>& dist, int n) {
    // dist[i][j] 初始化为边权，无边为 INF，自己到自己为 0
    
    for (int k = 0; k < n; ++k) {
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                if (dist[i][k] != INT_MAX && dist[k][j] != INT_MAX) {
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);
                }
            }
        }
    }
}
```

### Bellman-Ford（单源最短路径，可有负权）

```cpp
vector<int> bellmanFord(int n, vector<vector<int>>& edges, int start) {
    vector<int> dist(n, INT_MAX);
    dist[start] = 0;
    
    // 松弛 n-1 次
    for (int i = 0; i < n - 1; ++i) {
        for (auto& edge : edges) {
            int u = edge[0], v = edge[1], w = edge[2];
            if (dist[u] != INT_MAX && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
            }
        }
    }
    
    // 检测负环
    for (auto& edge : edges) {
        int u = edge[0], v = edge[1], w = edge[2];
        if (dist[u] != INT_MAX && dist[u] + w < dist[v]) {
            return {};  // 有负环
        }
    }
    
    return dist;
}
```

### SPFA（Bellman-Ford 优化）

```cpp
vector<int> spfa(int n, vector<vector<pair<int,int>>>& graph, int start) {
    vector<int> dist(n, INT_MAX);
    vector<bool> inQueue(n, false);
    queue<int> q;
    
    dist[start] = 0;
    q.push(start);
    inQueue[start] = true;
    
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        inQueue[u] = false;
        
        for (auto [v, w] : graph[u]) {
            if (dist[u] != INT_MAX && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                
                if (!inQueue[v]) {
                    q.push(v);
                    inQueue[v] = true;
                }
            }
        }
    }
    
    return dist;
}
```

## 例题演示

### 例题 1：网络延迟时间（Dijkstra）

**题目**：n 个节点的网络，给定边和传输时间，从节点 k 发信号，求所有节点收到信号的时间。

**思路**：单源最短路径，Dijkstra 算法。

```cpp
#include <bits/stdc++.h>
using namespace std;

int networkDelayTime(vector<vector<int>>& times, int n, int k) {
    vector<vector<pair<int,int>>> graph(n + 1);
    
    for (auto& time : times) {
        int u = time[0], v = time[1], w = time[2];
        graph[u].push_back({v, w});
    }
    
    vector<int> dist(n + 1, INT_MAX);
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;
    
    dist[k] = 0;
    pq.push({0, k});
    
    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        
        if (d > dist[u]) continue;
        
        for (auto [v, w] : graph[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    
    int maxDelay = 0;
    for (int i = 1; i <= n; ++i) {
        if (dist[i] == INT_MAX) return -1;
        maxDelay = max(maxDelay, dist[i]);
    }
    
    return maxDelay;
}

int main() {
    int n, m, k;
    cin >> n >> m >> k;
    
    vector<vector<int>> times(m, vector<int>(3));
    for (int i = 0; i < m; ++i) {
        cin >> times[i][0] >> times[i][1] >> times[i][2];
    }
    
    cout << networkDelayTime(times, n, k) << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O((V + E) log V)`，空间 `O(V + E)`

**易错点**：
- 优先队列存 {距离, 节点}，按距离排序
- 如果有节点不可达，返回 -1
- 答案是最大的距离，不是总和

---

### 例题 2：最便宜的航班（有限制的最短路径）

**题目**：n 个城市，给定航班和价格，从 src 到 dst 最多经过 k 站，求最低价格。

**思路**：BFS + 分层，或 Bellman-Ford 限制松弛次数。

```cpp
#include <bits/stdc++.h>
using namespace std;

int findCheapestPrice(int n, vector<vector<int>>& flights, int src, int dst, int k) {
    vector<int> dist(n, INT_MAX);
    dist[src] = 0;
    
    // 最多 k+1 次松弛（k 个中间站）
    for (int i = 0; i <= k; ++i) {
        vector<int> temp = dist;
        
        for (auto& flight : flights) {
            int u = flight[0], v = flight[1], w = flight[2];
            
            if (dist[u] != INT_MAX) {
                temp[v] = min(temp[v], dist[u] + w);
            }
        }
        
        dist = temp;
    }
    
    return dist[dst] == INT_MAX ? -1 : dist[dst];
}

int main() {
    int n, m, src, dst, k;
    cin >> n >> m >> src >> dst >> k;
    
    vector<vector<int>> flights(m, vector<int>(3));
    for (int i = 0; i < m; ++i) {
        cin >> flights[i][0] >> flights[i][1] >> flights[i][2];
    }
    
    cout << findCheapestPrice(n, flights, src, dst, k) << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(k × E)`，空间 `O(V)`

**易错点**：
- 每次松弛要用上一轮的结果，不能直接修改 dist
- k 个中间站意味着最多 k+1 次松弛
- Dijkstra 不适用，因为贪心会跳过一些绕路但更便宜的路径

---

### 例题 3：找到最小权值路径（Floyd）

**题目**：给定 n 个节点的带权有向图，求任意两点之间的最短距离。

**思路**：Floyd-Warshall 算法，O(n³) 求全源最短路径。

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<vector<int>> floydWarshall(int n, vector<vector<int>>& edges) {
    vector<vector<int>> dist(n, vector<int>(n, INT_MAX));
    
    // 初始化
    for (int i = 0; i < n; ++i) {
        dist[i][i] = 0;
    }
    
    for (auto& edge : edges) {
        int u = edge[0], v = edge[1], w = edge[2];
        dist[u][v] = w;
    }
    
    // Floyd
    for (int k = 0; k < n; ++k) {
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                if (dist[i][k] != INT_MAX && dist[k][j] != INT_MAX) {
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);
                }
            }
        }
    }
    
    return dist;
}

int main() {
    int n, m;
    cin >> n >> m;
    
    vector<vector<int>> edges(m, vector<int>(3));
    for (int i = 0; i < m; ++i) {
        cin >> edges[i][0] >> edges[i][1] >> edges[i][2];
    }
    
    vector<vector<int>> dist = floydWarshall(n, edges);
    
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (dist[i][j] == INT_MAX) {
                cout << "INF ";
            } else {
                cout << dist[i][j] << " ";
            }
        }
        cout << "\n";
    }
    
    return 0;
}
```

**复杂度**：时间 `O(n³)`，空间 `O(n²)`

**易错点**：
- k 必须在最外层循环
- 防止溢出：先判断 dist[i][k] 和 dist[k][j] 不是 INT_MAX
- 适合小规模图（n ≤ 500）

---

### 例题 4：路径最小代价（带权重）

**题目**：二维网格，每个格子有代价，从左上角到右下角的最小代价。

**思路**：Dijkstra 或 DP，这里用 Dijkstra。

```cpp
#include <bits/stdc++.h>
using namespace std;

int minPathCost(vector<vector<int>>& grid) {
    int m = grid.size(), n = grid[0].size();
    vector<vector<int>> dist(m, vector<int>(n, INT_MAX));
    priority_queue<tuple<int,int,int>, vector<tuple<int,int,int>>, greater<>> pq;
    
    dist[0][0] = grid[0][0];
    pq.push({grid[0][0], 0, 0});
    
    int dx[] = {0, 0, 1, -1};
    int dy[] = {1, -1, 0, 0};
    
    while (!pq.empty()) {
        auto [d, x, y] = pq.top();
        pq.pop();
        
        if (d > dist[x][y]) continue;
        
        if (x == m - 1 && y == n - 1) return d;
        
        for (int i = 0; i < 4; ++i) {
            int nx = x + dx[i];
            int ny = y + dy[i];
            
            if (nx >= 0 && nx < m && ny >= 0 && ny < n) {
                int newDist = dist[x][y] + grid[nx][ny];
                
                if (newDist < dist[nx][ny]) {
                    dist[nx][ny] = newDist;
                    pq.push({newDist, nx, ny});
                }
            }
        }
    }
    
    return dist[m-1][n-1];
}

int main() {
    int m, n;
    cin >> m >> n;
    
    vector<vector<int>> grid(m, vector<int>(n));
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            cin >> grid[i][j];
        }
    }
    
    cout << minPathCost(grid) << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(mn log(mn))`，空间 `O(mn)`

**易错点**：
- 起点的代价也要计算
- 可以用 DP 优化到 O(mn)，但 Dijkstra 更通用
- 优先队列存 {距离, x, y}

---

### 例题 5：概率最大的路径

**题目**：带概率的图，求从起点到终点成功概率最大的路径。

**思路**：Dijkstra 变形，最大化概率（乘法变加法用对数）。

```cpp
#include <bits/stdc++.h>
using namespace std;

double maxProbability(int n, vector<vector<int>>& edges, 
                      vector<double>& succProb, int start, int end) {
    vector<vector<pair<int,double>>> graph(n);
    
    for (int i = 0; i < edges.size(); ++i) {
        int u = edges[i][0], v = edges[i][1];
        double prob = succProb[i];
        graph[u].push_back({v, prob});
        graph[v].push_back({u, prob});
    }
    
    vector<double> maxProb(n, 0.0);
    priority_queue<pair<double,int>> pq;  // 大根堆
    
    maxProb[start] = 1.0;
    pq.push({1.0, start});
    
    while (!pq.empty()) {
        auto [prob, u] = pq.top();
        pq.pop();
        
        if (prob < maxProb[u]) continue;
        
        for (auto [v, edgeProb] : graph[u]) {
            double newProb = maxProb[u] * edgeProb;
            
            if (newProb > maxProb[v]) {
                maxProb[v] = newProb;
                pq.push({newProb, v});
            }
        }
    }
    
    return maxProb[end];
}

int main() {
    int n, m, start, end;
    cin >> n >> m >> start >> end;
    
    vector<vector<int>> edges(m, vector<int>(2));
    vector<double> succProb(m);
    
    for (int i = 0; i < m; ++i) {
        cin >> edges[i][0] >> edges[i][1] >> succProb[i];
    }
    
    cout << fixed << setprecision(5) << maxProbability(n, edges, succProb, start, end) << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O((V + E) log V)`，空间 `O(V + E)`

**易错点**：
- 概率是乘法，要用大根堆（求最大）
- 初始概率是 1.0，不是 0
- 也可以用对数转换成加法，用小根堆

---

### 例题 6：有负权边的最短路径（Bellman-Ford）

**题目**：带负权边的图，求单源最短路径，如果有负环返回 -1。

**思路**：Bellman-Ford 算法，可以检测负环。

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> bellmanFord(int n, vector<vector<int>>& edges, int start) {
    vector<int> dist(n, INT_MAX);
    dist[start] = 0;
    
    // 松弛 n-1 次
    for (int i = 0; i < n - 1; ++i) {
        bool updated = false;
        
        for (auto& edge : edges) {
            int u = edge[0], v = edge[1], w = edge[2];
            
            if (dist[u] != INT_MAX && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                updated = true;
            }
        }
        
        if (!updated) break;  // 提前终止
    }
    
    // 检测负环
    for (auto& edge : edges) {
        int u = edge[0], v = edge[1], w = edge[2];
        
        if (dist[u] != INT_MAX && dist[u] + w < dist[v]) {
            return {};  // 有负环
        }
    }
    
    return dist;
}

int main() {
    int n, m, start;
    cin >> n >> m >> start;
    
    vector<vector<int>> edges(m, vector<int>(3));
    for (int i = 0; i < m; ++i) {
        cin >> edges[i][0] >> edges[i][1] >> edges[i][2];
    }
    
    vector<int> dist = bellmanFord(n, edges, start);
    
    if (dist.empty()) {
        cout << "Negative cycle detected\n";
    } else {
        for (int i = 0; i < n; ++i) {
            if (dist[i] == INT_MAX) {
                cout << "INF ";
            } else {
                cout << dist[i] << " ";
            }
        }
        cout << "\n";
    }
    
    return 0;
}
```

**复杂度**：时间 `O(VE)`，空间 `O(V)`

**易错点**：
- 松弛 n-1 次（n 个节点最多 n-1 条边）
- 如果第 n 次还能松弛，说明有负环
- Dijkstra 不适用于负权图

---

### 例题 7：K 站中转内最便宜航班（SPFA）

**题目**：带限制次数的最短路径。

**思路**：SPFA（队列优化的 Bellman-Ford）。

```cpp
#include <bits/stdc++.h>
using namespace std;

int findCheapestPrice(int n, vector<vector<int>>& flights, int src, int dst, int k) {
    vector<vector<pair<int,int>>> graph(n);
    
    for (auto& flight : flights) {
        int u = flight[0], v = flight[1], w = flight[2];
        graph[u].push_back({v, w});
    }
    
    vector<int> dist(n, INT_MAX);
    queue<pair<int,int>> q;  // {节点, 步数}
    
    dist[src] = 0;
    q.push({src, 0});
    
    while (!q.empty()) {
        auto [u, steps] = q.front();
        q.pop();
        
        if (steps > k) continue;
        
        for (auto [v, w] : graph[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                q.push({v, steps + 1});
            }
        }
    }
    
    return dist[dst] == INT_MAX ? -1 : dist[dst];
}

int main() {
    int n, m, src, dst, k;
    cin >> n >> m >> src >> dst >> k;
    
    vector<vector<int>> flights(m, vector<int>(3));
    for (int i = 0; i < m; ++i) {
        cin >> flights[i][0] >> flights[i][1] >> flights[i][2];
    }
    
    cout << findCheapestPrice(n, flights, src, dst, k) << "\n";
    
    return 0;
}
```

**复杂度**：时间 平均 `O(kE)`，最坏 `O(VE)`

**易错点**：
- 队列存 {节点, 步数}，步数超过 k 就停止
- SPFA 可能被卡成 O(VE)，慎用

---

### 例题 8：二维网格中的最短路径（障碍物消除）

**题目**：网格中有障碍，可以消除 k 个障碍，求最短路径。

**思路**：BFS + 状态 {x, y, 剩余消除次数}。

```cpp
#include <bits/stdc++.h>
using namespace std;

int shortestPath(vector<vector<int>>& grid, int k) {
    int m = grid.size(), n = grid[0].size();
    
    if (k >= m + n - 3) return m + n - 2;  // 可以直走
    
    queue<tuple<int,int,int>> q;  // {x, y, 剩余消除次数}
    vector<vector<vector<bool>>> visited(m, vector<vector<bool>>(n, vector<bool>(k + 1, false)));
    
    q.push({0, 0, k});
    visited[0][0][k] = true;
    int steps = 0;
    
    int dx[] = {0, 0, 1, -1};
    int dy[] = {1, -1, 0, 0};
    
    while (!q.empty()) {
        int size = q.size();
        
        for (int i = 0; i < size; ++i) {
            auto [x, y, remain] = q.front();
            q.pop();
            
            if (x == m - 1 && y == n - 1) return steps;
            
            for (int d = 0; d < 4; ++d) {
                int nx = x + dx[d];
                int ny = y + dy[d];
                
                if (nx >= 0 && nx < m && ny >= 0 && ny < n) {
                    int newRemain = remain - grid[nx][ny];
                    
                    if (newRemain >= 0 && !visited[nx][ny][newRemain]) {
                        visited[nx][ny][newRemain] = true;
                        q.push({nx, ny, newRemain});
                    }
                }
            }
        }
        
        steps++;
    }
    
    return -1;
}

int main() {
    int m, n, k;
    cin >> m >> n >> k;
    
    vector<vector<int>> grid(m, vector<int>(n));
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            cin >> grid[i][j];
        }
    }
    
    cout << shortestPath(grid, k) << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(mnk)`，空间 `O(mnk)`

**易错点**：
- 状态是三维：{x, y, 剩余消除次数}
- visited 也是三维数组
- 如果 k 足够大可以直走，特判优化

---

## 常见陷阱

1. **算法选择**：
   - 非负权单源：Dijkstra
   - 有负权单源：Bellman-Ford / SPFA
   - 全源最短路：Floyd（小规模）或多次 Dijkstra
   - 无权图：BFS

2. **Dijkstra 易错**：
   - 不适用于负权边
   - 优先队列存 {距离, 节点}，按距离排序
   - 出队时检查是否已找到更短路径

3. **Floyd 易错**：
   - k 必须在最外层
   - 防止溢出：先判断不是 INT_MAX

4. **Bellman-Ford 易错**：
   - 松弛 n-1 次
   - 第 n 次还能松弛说明有负环
   - 每次松弛要遍历所有边

5. **INF 处理**：
   - 用 INT_MAX 表示不可达
   - 加法前要检查是否为 INT_MAX，防止溢出

## 适用场景总结

| 算法 | 适用场景 | 时间复杂度 | 能否处理负权 |
|------|---------|-----------|------------|
| Dijkstra | 非负权单源 | O((V+E) log V) | 否 |
| Bellman-Ford | 有负权单源 | O(VE) | 是 |
| SPFA | 一般情况单源 | 平均 O(kE) | 是 |
| Floyd-Warshall | 全源最短路 | O(V³) | 是 |
| BFS | 无权图 | O(V + E) | - |

**核心技巧**：
- Dijkstra：贪心 + 优先队列，适合非负权
- Floyd：DP，枚举中间节点，适合小规模全源
- Bellman-Ford：松弛所有边 n-1 次，可检测负环
- 状态扩展：网格问题可以用多维状态（位置 + 其他信息）
- 变形问题：最大概率、最小代价等都可以套用模板
