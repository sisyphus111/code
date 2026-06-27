# BFS 与网格问题

## 什么时候用

看到以下特征优先考虑 BFS：
- **最短路径**：无权图、网格中的最短距离
- **层序遍历**：树的层序、分层处理
- **最少步数**：最少操作次数、最少转换次数
- **扩散问题**：腐烂的橘子、病毒传播
- **拓扑排序**：有向无环图的层次关系
- 题目中出现"最短"、"最少"、"最近"、"层"等字眼

核心思路：**逐层扩展，先访问到的就是最短路径**。

## 核心模板

### BFS 基本框架

```cpp
queue<Node> q;
set<Node> visited;

q.push(start);
visited.insert(start);

while (!q.empty()) {
    Node node = q.front();
    q.pop();
    
    if (node == target) return;
    
    for (Node next : node.neighbors()) {
        if (!visited.count(next)) {
            q.push(next);
            visited.insert(next);
        }
    }
}
```

### 网格 BFS 模板

```cpp
int dx[] = {0, 0, 1, -1};
int dy[] = {1, -1, 0, 0};

queue<pair<int,int>> q;
vector<vector<bool>> visited(m, vector<bool>(n, false));

q.push({startX, startY});
visited[startX][startY] = true;
int steps = 0;

while (!q.empty()) {
    int size = q.size();
    
    for (int i = 0; i < size; ++i) {
        auto [x, y] = q.front();
        q.pop();
        
        if (x == targetX && y == targetY) return steps;
        
        for (int d = 0; d < 4; ++d) {
            int nx = x + dx[d];
            int ny = y + dy[d];
            
            if (nx >= 0 && nx < m && ny >= 0 && ny < n && 
                !visited[nx][ny] && grid[nx][ny] != obstacle) {
                q.push({nx, ny});
                visited[nx][ny] = true;
            }
        }
    }
    
    steps++;
}

return -1;  // 无法到达
```

### 双向 BFS

```cpp
set<Node> q1 = {start}, q2 = {end};
set<Node> visited;
int steps = 0;

while (!q1.empty() && !q2.empty()) {
    // 优化：总是扩展较小的集合
    if (q1.size() > q2.size()) swap(q1, q2);
    
    set<Node> next;
    for (Node node : q1) {
        if (q2.count(node)) return steps;
        
        for (Node neighbor : node.neighbors()) {
            if (!visited.count(neighbor)) {
                next.insert(neighbor);
                visited.insert(neighbor);
            }
        }
    }
    
    q1 = next;
    steps++;
}

return -1;
```

## 例题演示

### 例题 1：二叉树的层序遍历

**题目**：给定二叉树，返回其层序遍历结果。

**思路**：BFS，用队列逐层处理。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

vector<vector<int>> levelOrder(TreeNode* root) {
    vector<vector<int>> result;
    if (!root) return result;
    
    queue<TreeNode*> q;
    q.push(root);
    
    while (!q.empty()) {
        int size = q.size();
        vector<int> level;
        
        for (int i = 0; i < size; ++i) {
            TreeNode* node = q.front();
            q.pop();
            
            level.push_back(node->val);
            
            if (node->left) q.push(node->left);
            if (node->right) q.push(node->right);
        }
        
        result.push_back(level);
    }
    
    return result;
}

int main() {
    // 简化输入：层序构建树
    // 输入格式：n 个节点值，-1 表示空节点
    int n;
    cin >> n;
    
    if (n == 0) return 0;
    
    vector<int> vals(n);
    for (int i = 0; i < n; ++i) {
        cin >> vals[i];
    }
    
    TreeNode* root = new TreeNode(vals[0]);
    queue<TreeNode*> q;
    q.push(root);
    
    int idx = 1;
    while (!q.empty() && idx < n) {
        TreeNode* node = q.front();
        q.pop();
        
        if (idx < n && vals[idx] != -1) {
            node->left = new TreeNode(vals[idx]);
            q.push(node->left);
        }
        idx++;
        
        if (idx < n && vals[idx] != -1) {
            node->right = new TreeNode(vals[idx]);
            q.push(node->right);
        }
        idx++;
    }
    
    vector<vector<int>> result = levelOrder(root);
    
    for (auto& level : result) {
        for (int i = 0; i < level.size(); ++i) {
            cout << level[i] << " \n"[i == level.size() - 1];
        }
    }
    
    return 0;
}
```

**复杂度**：时间 `O(n)`，空间 `O(n)`

**易错点**：
- 每层处理前要记录当前队列大小
- 空节点不入队

---

### 例题 2：网格中的最短路径

**题目**：给定二维网格，0 表示空地，1 表示障碍，求从左上角到右下角的最短路径长度。

**思路**：BFS，逐层扩展，第一次到达终点即为最短路径。

```cpp
#include <bits/stdc++.h>
using namespace std;

int shortestPath(vector<vector<int>>& grid) {
    int m = grid.size(), n = grid[0].size();
    
    if (grid[0][0] == 1 || grid[m-1][n-1] == 1) return -1;
    
    int dx[] = {0, 0, 1, -1};
    int dy[] = {1, -1, 0, 0};
    
    queue<pair<int,int>> q;
    vector<vector<bool>> visited(m, vector<bool>(n, false));
    
    q.push({0, 0});
    visited[0][0] = true;
    int steps = 0;
    
    while (!q.empty()) {
        int size = q.size();
        
        for (int i = 0; i < size; ++i) {
            auto [x, y] = q.front();
            q.pop();
            
            if (x == m - 1 && y == n - 1) return steps;
            
            for (int d = 0; d < 4; ++d) {
                int nx = x + dx[d];
                int ny = y + dy[d];
                
                if (nx >= 0 && nx < m && ny >= 0 && ny < n && 
                    !visited[nx][ny] && grid[nx][ny] == 0) {
                    q.push({nx, ny});
                    visited[nx][ny] = true;
                }
            }
        }
        
        steps++;
    }
    
    return -1;
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
    
    cout << shortestPath(grid) << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(m × n)`，空间 `O(m × n)`

**易错点**：
- 起点和终点也要检查是否是障碍
- 步数是层数，不是节点数
- 入队时就标记 visited，而不是出队时

---

### 例题 3：腐烂的橘子

**题目**：网格中 0 表示空，1 表示新鲜橘子，2 表示腐烂橘子。每分钟腐烂橘子会使相邻橘子腐烂，求所有橘子腐烂的最少时间。

**思路**：多源 BFS，将所有腐烂橘子作为起点同时扩散。

```cpp
#include <bits/stdc++.h>
using namespace std;

int orangesRotting(vector<vector<int>>& grid) {
    int m = grid.size(), n = grid[0].size();
    int fresh = 0;
    queue<pair<int,int>> q;
    
    // 统计新鲜橘子数量，将腐烂橘子加入队列
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            if (grid[i][j] == 1) fresh++;
            else if (grid[i][j] == 2) q.push({i, j});
        }
    }
    
    if (fresh == 0) return 0;
    
    int dx[] = {0, 0, 1, -1};
    int dy[] = {1, -1, 0, 0};
    int minutes = 0;
    
    while (!q.empty()) {
        int size = q.size();
        bool rotted = false;
        
        for (int i = 0; i < size; ++i) {
            auto [x, y] = q.front();
            q.pop();
            
            for (int d = 0; d < 4; ++d) {
                int nx = x + dx[d];
                int ny = y + dy[d];
                
                if (nx >= 0 && nx < m && ny >= 0 && ny < n && 
                    grid[nx][ny] == 1) {
                    grid[nx][ny] = 2;
                    fresh--;
                    q.push({nx, ny});
                    rotted = true;
                }
            }
        }
        
        if (rotted) minutes++;
    }
    
    return fresh == 0 ? minutes : -1;
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
    
    cout << orangesRotting(grid) << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(m × n)`，空间 `O(m × n)`

**易错点**：
- 多源 BFS：所有起点同时入队
- 只有本轮有橘子腐烂才增加时间
- 最后要检查是否还有新鲜橘子

---

### 例题 4：单词接龙

**题目**：给定开始单词、结束单词和单词列表，每次只能改变一个字母，求最短转换序列长度。

**思路**：BFS，每个单词是节点，可以转换的单词是邻居。

```cpp
#include <bits/stdc++.h>
using namespace std;

int ladderLength(string beginWord, string endWord, vector<string>& wordList) {
    unordered_set<string> wordSet(wordList.begin(), wordList.end());
    
    if (!wordSet.count(endWord)) return 0;
    
    queue<string> q;
    q.push(beginWord);
    int steps = 1;
    
    while (!q.empty()) {
        int size = q.size();
        
        for (int i = 0; i < size; ++i) {
            string word = q.front();
            q.pop();
            
            if (word == endWord) return steps;
            
            // 尝试改变每个位置的字母
            for (int j = 0; j < word.size(); ++j) {
                char original = word[j];
                
                for (char c = 'a'; c <= 'z'; ++c) {
                    if (c == original) continue;
                    
                    word[j] = c;
                    
                    if (wordSet.count(word)) {
                        q.push(word);
                        wordSet.erase(word);  // 避免重复访问
                    }
                }
                
                word[j] = original;  // 恢复
            }
        }
        
        steps++;
    }
    
    return 0;
}

int main() {
    string beginWord, endWord;
    int n;
    cin >> beginWord >> endWord >> n;
    
    vector<string> wordList(n);
    for (int i = 0; i < n; ++i) {
        cin >> wordList[i];
    }
    
    cout << ladderLength(beginWord, endWord, wordList) << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(n × L^2)`，n 是单词数，L 是单词长度

**易错点**：
- 从 wordSet 中删除已访问单词，避免重复
- 修改单词后要恢复原字符
- 步数从 1 开始（包含起点）

---

### 例题 5：01 矩阵（到最近 0 的距离）

**题目**：给定只包含 0 和 1 的矩阵，求每个位置到最近 0 的距离。

**思路**：多源 BFS，将所有 0 作为起点同时扩散。

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<vector<int>> updateMatrix(vector<vector<int>>& mat) {
    int m = mat.size(), n = mat[0].size();
    vector<vector<int>> dist(m, vector<int>(n, -1));
    queue<pair<int,int>> q;
    
    // 将所有 0 加入队列
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            if (mat[i][j] == 0) {
                q.push({i, j});
                dist[i][j] = 0;
            }
        }
    }
    
    int dx[] = {0, 0, 1, -1};
    int dy[] = {1, -1, 0, 0};
    
    while (!q.empty()) {
        auto [x, y] = q.front();
        q.pop();
        
        for (int d = 0; d < 4; ++d) {
            int nx = x + dx[d];
            int ny = y + dy[d];
            
            if (nx >= 0 && nx < m && ny >= 0 && ny < n && dist[nx][ny] == -1) {
                dist[nx][ny] = dist[x][y] + 1;
                q.push({nx, ny});
            }
        }
    }
    
    return dist;
}

int main() {
    int m, n;
    cin >> m >> n;
    
    vector<vector<int>> mat(m, vector<int>(n));
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            cin >> mat[i][j];
        }
    }
    
    vector<vector<int>> result = updateMatrix(mat);
    
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            cout << result[i][j] << " \n"[j == n - 1];
        }
    }
    
    return 0;
}
```

**复杂度**：时间 `O(m × n)`，空间 `O(m × n)`

**易错点**：
- 多源 BFS：所有 0 同时作为起点
- 距离数组用 -1 表示未访问
- 不需要单独的 visited 数组

---

### 例题 6：打开转盘锁

**题目**：4 位数字转盘，初始 "0000"，每次可以转动一位（向上或向下），给定死亡数字列表，求到达目标的最少步数。

**思路**：BFS，每个状态最多有 8 个邻居（4 位 × 2 方向）。

```cpp
#include <bits/stdc++.h>
using namespace std;

int openLock(vector<string>& deadends, string target) {
    unordered_set<string> dead(deadends.begin(), deadends.end());
    
    if (dead.count("0000")) return -1;
    if (target == "0000") return 0;
    
    queue<string> q;
    unordered_set<string> visited;
    
    q.push("0000");
    visited.insert("0000");
    int steps = 0;
    
    while (!q.empty()) {
        int size = q.size();
        
        for (int i = 0; i < size; ++i) {
            string curr = q.front();
            q.pop();
            
            if (curr == target) return steps;
            
            // 尝试转动每一位
            for (int j = 0; j < 4; ++j) {
                // 向上转
                string next = curr;
                next[j] = (next[j] - '0' + 1) % 10 + '0';
                if (!dead.count(next) && !visited.count(next)) {
                    q.push(next);
                    visited.insert(next);
                }
                
                // 向下转
                next = curr;
                next[j] = (next[j] - '0' + 9) % 10 + '0';
                if (!dead.count(next) && !visited.count(next)) {
                    q.push(next);
                    visited.insert(next);
                }
            }
        }
        
        steps++;
    }
    
    return -1;
}

int main() {
    string target;
    int n;
    cin >> target >> n;
    
    vector<string> deadends(n);
    for (int i = 0; i < n; ++i) {
        cin >> deadends[i];
    }
    
    cout << openLock(deadends, target) << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(10^4)`，最多 10000 个状态

**易错点**：
- 向下转：`(x + 9) % 10` 而不是 `(x - 1) % 10`（负数取模问题）
- 起点可能就是死亡数字
- visited 和 dead 都要检查

---

### 例题 7：完全平方数（最少数量）

**题目**：给定正整数 n，求最少需要多少个完全平方数相加等于 n。

**思路**：BFS，每次减去一个完全平方数，求到达 0 的最短路径。

```cpp
#include <bits/stdc++.h>
using namespace std;

int numSquares(int n) {
    if (n == 0) return 0;
    
    queue<int> q;
    vector<bool> visited(n + 1, false);
    
    q.push(n);
    visited[n] = true;
    int steps = 0;
    
    while (!q.empty()) {
        int size = q.size();
        steps++;
        
        for (int i = 0; i < size; ++i) {
            int curr = q.front();
            q.pop();
            
            // 尝试减去每个完全平方数
            for (int j = 1; j * j <= curr; ++j) {
                int next = curr - j * j;
                
                if (next == 0) return steps;
                
                if (!visited[next]) {
                    q.push(next);
                    visited[next] = true;
                }
            }
        }
    }
    
    return -1;
}

int main() {
    int n;
    cin >> n;
    cout << numSquares(n) << "\n";
    return 0;
}
```

**复杂度**：时间 `O(n × √n)`，空间 `O(n)`

**易错点**：
- 从 n 出发，目标是 0
- 步数在每层开始时增加
- 减到 0 时立即返回

---

### 例题 8：被围绕的区域

**题目**：给定二维矩阵，X 和 O 组成，将被 X 围绕的 O 变为 X（边界上的 O 及其连通的 O 不算被围绕）。

**思路**：从边界的 O 开始 BFS/DFS，标记所有连通的 O，其余 O 全部变为 X。

```cpp
#include <bits/stdc++.h>
using namespace std;

void solve(vector<vector<char>>& board) {
    if (board.empty()) return;
    
    int m = board.size(), n = board[0].size();
    queue<pair<int,int>> q;
    
    // 将边界的 O 加入队列
    for (int i = 0; i < m; ++i) {
        if (board[i][0] == 'O') {
            q.push({i, 0});
            board[i][0] = '#';  // 临时标记
        }
        if (board[i][n-1] == 'O') {
            q.push({i, n-1});
            board[i][n-1] = '#';
        }
    }
    
    for (int j = 0; j < n; ++j) {
        if (board[0][j] == 'O') {
            q.push({0, j});
            board[0][j] = '#';
        }
        if (board[m-1][j] == 'O') {
            q.push({m-1, j});
            board[m-1][j] = '#';
        }
    }
    
    // BFS 标记所有与边界连通的 O
    int dx[] = {0, 0, 1, -1};
    int dy[] = {1, -1, 0, 0};
    
    while (!q.empty()) {
        auto [x, y] = q.front();
        q.pop();
        
        for (int d = 0; d < 4; ++d) {
            int nx = x + dx[d];
            int ny = y + dy[d];
            
            if (nx >= 0 && nx < m && ny >= 0 && ny < n && board[nx][ny] == 'O') {
                board[nx][ny] = '#';
                q.push({nx, ny});
            }
        }
    }
    
    // 将 O 变为 X，# 恢复为 O
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            if (board[i][j] == 'O') board[i][j] = 'X';
            else if (board[i][j] == '#') board[i][j] = 'O';
        }
    }
}

int main() {
    int m, n;
    cin >> m >> n;
    
    vector<vector<char>> board(m, vector<char>(n));
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            cin >> board[i][j];
        }
    }
    
    solve(board);
    
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            cout << board[i][j] << " \n"[j == n - 1];
        }
    }
    
    return 0;
}
```

**复杂度**：时间 `O(m × n)`，空间 `O(m × n)`

**易错点**：
- 从边界出发，而不是从内部出发
- 要用临时标记避免混淆
- 边界 O 的四条边都要检查

---

## 常见陷阱

1. **步数计数**：
   - 在每层开始或结束时增加步数
   - 区分"包含起点"还是"不包含起点"

2. **visited 标记时机**：
   - 入队时标记，而不是出队时（避免重复入队）

3. **多源 BFS**：
   - 所有起点同时入队
   - 第一次到达的就是最短距离

4. **网格越界**：
   - 四个边界条件都要检查
   - 使用方向数组简化代码

5. **状态去重**：
   - 用 set 或 visited 数组
   - 或者原地修改（如果允许）

## 适用场景总结

| 问题类型 | 关键技巧 | 时间复杂度 |
|---------|---------|-----------|
| 层序遍历 | 记录每层大小 | O(n) |
| 最短路径（无权图） | 第一次到达即最短 | O(V + E) |
| 网格最短路径 | 四方向扩展 | O(m × n) |
| 多源扩散 | 所有起点同时入队 | O(m × n) |
| 单词转换 | 每个字符尝试 26 个字母 | O(n × L^2) |
| 状态转换 | 每个状态尝试所有操作 | 看状态空间 |
| 边界连通性 | 从边界开始 BFS/DFS | O(m × n) |

**核心技巧**：
- BFS 保证第一次到达就是最短路径（无权图）
- 队列 + visited 避免重复访问
- 多源 BFS：多个起点同时扩展
- 层次遍历：记录每层大小，逐层处理
- 双向 BFS：从两端同时搜索，相遇时结束（优化大状态空间）
