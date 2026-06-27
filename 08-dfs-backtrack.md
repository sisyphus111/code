# DFS 与回溯

## 什么时候用

看到以下特征优先考虑 DFS 与回溯：
- **排列组合**：全排列、子集、组合
- **路径搜索**：迷宫、岛屿数量、连通性
- **棋盘问题**：N 皇后、数独
- **字符串分割**：括号生成、IP 地址还原
- **决策树遍历**：选或不选、剪枝优化
- 题目要求"所有可能"、"所有方案"、"是否存在"

核心思路：**尝试所有可能的选择，不符合条件就回退，符合条件就继续深入**。

## 核心模板

### DFS 基本框架

```cpp
void dfs(当前状态, 路径, 结果集) {
    // 终止条件
    if (满足条件) {
        结果集.add(路径);
        return;
    }
    
    // 剪枝
    if (不可能有解) return;
    
    // 遍历所有选择
    for (选择 in 选择列表) {
        做选择;
        dfs(新状态, 路径, 结果集);
        撤销选择;  // 回溯
    }
}
```

### 回溯三要素

1. **路径**：已经做出的选择
2. **选择列表**：当前可以做的选择
3. **终止条件**：到达决策树底层

### 常见剪枝技巧

```cpp
// 1. 排序后去重
sort(nums.begin(), nums.end());
if (i > start && nums[i] == nums[i-1]) continue;

// 2. 可行性剪枝
if (当前和 > 目标) return;

// 3. 最优性剪枝
if (当前步数 >= 已知最优) return;
```

## 例题演示

### 例题 1：全排列

**题目**：给定不含重复数字的数组，返回所有可能的全排列。

**思路**：每次选择一个未使用的数字，递归处理剩余数字。

```cpp
#include <bits/stdc++.h>
using namespace std;

void backtrack(vector<int>& nums, vector<bool>& used, vector<int>& path, vector<vector<int>>& result) {
    if (path.size() == nums.size()) {
        result.push_back(path);
        return;
    }
    
    for (int i = 0; i < nums.size(); ++i) {
        if (used[i]) continue;
        
        path.push_back(nums[i]);
        used[i] = true;
        
        backtrack(nums, used, path, result);
        
        path.pop_back();
        used[i] = false;
    }
}

vector<vector<int>> permute(vector<int>& nums) {
    vector<vector<int>> result;
    vector<int> path;
    vector<bool> used(nums.size(), false);
    
    backtrack(nums, used, path, result);
    return result;
}

int main() {
    int n;
    cin >> n;
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    
    vector<vector<int>> result = permute(nums);
    
    for (auto& perm : result) {
        for (int i = 0; i < perm.size(); ++i) {
            cout << perm[i] << " \n"[i == perm.size() - 1];
        }
    }
    
    return 0;
}
```

**复杂度**：时间 `O(n × n!)`，空间 `O(n)`

**易错点**：
- 回溯时要撤销选择（pop_back 和恢复 used）
- used 数组标记已使用的元素

---

### 例题 2：子集

**题目**：给定不含重复元素的数组，返回所有可能的子集。

**思路**：每个元素有选或不选两种选择。

```cpp
#include <bits/stdc++.h>
using namespace std;

void backtrack(vector<int>& nums, int start, vector<int>& path, vector<vector<int>>& result) {
    result.push_back(path);
    
    for (int i = start; i < nums.size(); ++i) {
        path.push_back(nums[i]);
        backtrack(nums, i + 1, path, result);
        path.pop_back();
    }
}

vector<vector<int>> subsets(vector<int>& nums) {
    vector<vector<int>> result;
    vector<int> path;
    backtrack(nums, 0, path, result);
    return result;
}

int main() {
    int n;
    cin >> n;
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    
    vector<vector<int>> result = subsets(nums);
    
    for (auto& subset : result) {
        if (subset.empty()) {
            cout << "[]";
        } else {
            for (int i = 0; i < subset.size(); ++i) {
                cout << subset[i] << " \n"[i == subset.size() - 1];
            }
        }
    }
    
    return 0;
}
```

**复杂度**：时间 `O(n × 2^n)`，空间 `O(n)`

**易错点**：
- 每个节点都是一个解，不只是叶子节点
- start 参数避免重复选择

---

### 例题 3：组合总和（元素可重复使用）

**题目**：给定候选数组和目标数，找出所有和为目标数的组合，每个数字可以无限次使用。

**思路**：每次可以选择当前数字或跳过，选择后可以继续选择同一数字。

```cpp
#include <bits/stdc++.h>
using namespace std;

void backtrack(vector<int>& candidates, int target, int start, vector<int>& path, vector<vector<int>>& result) {
    if (target == 0) {
        result.push_back(path);
        return;
    }
    
    if (target < 0) return;
    
    for (int i = start; i < candidates.size(); ++i) {
        path.push_back(candidates[i]);
        // 可以重复使用，所以还是从 i 开始
        backtrack(candidates, target - candidates[i], i, path, result);
        path.pop_back();
    }
}

vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
    vector<vector<int>> result;
    vector<int> path;
    backtrack(candidates, target, 0, path, result);
    return result;
}

int main() {
    int n, target;
    cin >> n >> target;
    
    vector<int> candidates(n);
    for (int i = 0; i < n; ++i) {
        cin >> candidates[i];
    }
    
    vector<vector<int>> result = combinationSum(candidates, target);
    
    for (auto& combo : result) {
        for (int i = 0; i < combo.size(); ++i) {
            cout << combo[i] << " \n"[i == combo.size() - 1];
        }
    }
    
    return 0;
}
```

**复杂度**：时间 `O(n^(target/min))`，最坏情况

**易错点**：
- 可以重复使用，递归时传 i 而不是 i+1
- 剪枝：target < 0 时提前返回

---

### 例题 4：N 皇后

**题目**：在 n×n 棋盘上放置 n 个皇后，使得它们不能互相攻击。

**思路**：逐行放置，检查列、对角线是否冲突。

```cpp
#include <bits/stdc++.h>
using namespace std;

bool isValid(vector<string>& board, int row, int col, int n) {
    // 检查列
    for (int i = 0; i < row; ++i) {
        if (board[i][col] == 'Q') return false;
    }
    
    // 检查左上对角线
    for (int i = row - 1, j = col - 1; i >= 0 && j >= 0; --i, --j) {
        if (board[i][j] == 'Q') return false;
    }
    
    // 检查右上对角线
    for (int i = row - 1, j = col + 1; i >= 0 && j < n; --i, ++j) {
        if (board[i][j] == 'Q') return false;
    }
    
    return true;
}

void backtrack(int row, int n, vector<string>& board, vector<vector<string>>& result) {
    if (row == n) {
        result.push_back(board);
        return;
    }
    
    for (int col = 0; col < n; ++col) {
        if (!isValid(board, row, col, n)) continue;
        
        board[row][col] = 'Q';
        backtrack(row + 1, n, board, result);
        board[row][col] = '.';
    }
}

vector<vector<string>> solveNQueens(int n) {
    vector<vector<string>> result;
    vector<string> board(n, string(n, '.'));
    backtrack(0, n, board, result);
    return result;
}

int main() {
    int n;
    cin >> n;
    
    vector<vector<string>> result = solveNQueens(n);
    
    cout << result.size() << "\n";
    for (auto& solution : result) {
        for (auto& row : solution) {
            cout << row << "\n";
        }
        cout << "\n";
    }
    
    return 0;
}
```

**复杂度**：时间 `O(n!)`，空间 `O(n^2)`

**易错点**：
- 只需要检查上方、左上、右上，因为是逐行放置
- 对角线检查：左上 (i-1, j-1)，右上 (i-1, j+1)

---

### 例题 5：岛屿数量

**题目**：给定二维网格，1 表示陆地，0 表示水，计算岛屿数量（连通的陆地）。

**思路**：DFS 遍历每个未访问的陆地，标记连通区域。

```cpp
#include <bits/stdc++.h>
using namespace std;

void dfs(vector<vector<char>>& grid, int i, int j) {
    int m = grid.size(), n = grid[0].size();
    
    if (i < 0 || i >= m || j < 0 || j >= n || grid[i][j] != '1') {
        return;
    }
    
    grid[i][j] = '0';  // 标记为已访问
    
    dfs(grid, i + 1, j);
    dfs(grid, i - 1, j);
    dfs(grid, i, j + 1);
    dfs(grid, i, j - 1);
}

int numIslands(vector<vector<char>>& grid) {
    if (grid.empty()) return 0;
    
    int count = 0;
    int m = grid.size(), n = grid[0].size();
    
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            if (grid[i][j] == '1') {
                count++;
                dfs(grid, i, j);
            }
        }
    }
    
    return count;
}

int main() {
    int m, n;
    cin >> m >> n;
    
    vector<vector<char>> grid(m, vector<char>(n));
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            cin >> grid[i][j];
        }
    }
    
    cout << numIslands(grid) << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(m × n)`，空间 `O(m × n)` 递归栈

**易错点**：
- 访问过的陆地要标记，避免重复访问
- 边界检查要在递归函数开头

---

### 例题 6：括号生成

**题目**：生成 n 对有效括号的所有组合。

**思路**：回溯，左括号数不超过 n，右括号数不超过左括号数。

```cpp
#include <bits/stdc++.h>
using namespace std;

void backtrack(int left, int right, int n, string& path, vector<string>& result) {
    if (path.size() == 2 * n) {
        result.push_back(path);
        return;
    }
    
    // 可以添加左括号
    if (left < n) {
        path.push_back('(');
        backtrack(left + 1, right, n, path, result);
        path.pop_back();
    }
    
    // 可以添加右括号
    if (right < left) {
        path.push_back(')');
        backtrack(left, right + 1, n, path, result);
        path.pop_back();
    }
}

vector<string> generateParenthesis(int n) {
    vector<string> result;
    string path;
    backtrack(0, 0, n, path, result);
    return result;
}

int main() {
    int n;
    cin >> n;
    
    vector<string> result = generateParenthesis(n);
    
    for (auto& s : result) {
        cout << s << "\n";
    }
    
    return 0;
}
```

**复杂度**：时间 `O(4^n / √n)` 卡特兰数，空间 `O(n)`

**易错点**：
- 左括号数量不能超过 n
- 右括号数量不能超过左括号数量
- 这是隐式的剪枝

---

### 例题 7：单词搜索

**题目**：给定二维字符网格和单词，判断单词是否存在于网格中（可以上下左右移动）。

**思路**：DFS + 回溯，尝试每个起点，标记访问过的位置。

```cpp
#include <bits/stdc++.h>
using namespace std;

bool dfs(vector<vector<char>>& board, string& word, int i, int j, int k) {
    if (k == word.size()) return true;
    
    int m = board.size(), n = board[0].size();
    
    if (i < 0 || i >= m || j < 0 || j >= n || board[i][j] != word[k]) {
        return false;
    }
    
    char temp = board[i][j];
    board[i][j] = '#';  // 标记为已访问
    
    bool found = dfs(board, word, i + 1, j, k + 1) ||
                 dfs(board, word, i - 1, j, k + 1) ||
                 dfs(board, word, i, j + 1, k + 1) ||
                 dfs(board, word, i, j - 1, k + 1);
    
    board[i][j] = temp;  // 回溯
    
    return found;
}

bool exist(vector<vector<char>>& board, string word) {
    int m = board.size(), n = board[0].size();
    
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            if (dfs(board, word, i, j, 0)) {
                return true;
            }
        }
    }
    
    return false;
}

int main() {
    int m, n;
    string word;
    cin >> m >> n >> word;
    
    vector<vector<char>> board(m, vector<char>(n));
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            cin >> board[i][j];
        }
    }
    
    cout << (exist(board, word) ? "YES" : "NO") << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(m × n × 4^L)`，L 是单词长度

**易错点**：
- 访问过的格子要临时标记，回溯时要恢复
- 四个方向可以用数组简化：`dx[] = {0,0,1,-1}, dy[] = {1,-1,0,0}`

---

### 例题 8：分割回文串

**题目**：给定字符串，将其分割成若干回文子串，返回所有可能的分割方案。

**思路**：回溯，尝试每个分割点，检查子串是否是回文。

```cpp
#include <bits/stdc++.h>
using namespace std;

bool isPalindrome(const string& s, int left, int right) {
    while (left < right) {
        if (s[left++] != s[right--]) return false;
    }
    return true;
}

void backtrack(string& s, int start, vector<string>& path, vector<vector<string>>& result) {
    if (start == s.size()) {
        result.push_back(path);
        return;
    }
    
    for (int end = start; end < s.size(); ++end) {
        if (isPalindrome(s, start, end)) {
            path.push_back(s.substr(start, end - start + 1));
            backtrack(s, end + 1, path, result);
            path.pop_back();
        }
    }
}

vector<vector<string>> partition(string s) {
    vector<vector<string>> result;
    vector<string> path;
    backtrack(s, 0, path, result);
    return result;
}

int main() {
    string s;
    cin >> s;
    
    vector<vector<string>> result = partition(s);
    
    for (auto& partition : result) {
        for (int i = 0; i < partition.size(); ++i) {
            cout << partition[i] << " \n"[i == partition.size() - 1];
        }
    }
    
    return 0;
}
```

**复杂度**：时间 `O(n × 2^n)`，空间 `O(n)`

**易错点**：
- 子串的长度是 end - start + 1
- 回文判断可以预处理用 DP 优化到 `O(n^2)` 预处理，`O(1)` 查询

---

## 常见陷阱

1. **忘记回溯**：做选择后要在递归返回时撤销选择
2. **重复解**：
   - 排序 + 跳过相同元素：`if (i > start && nums[i] == nums[i-1]) continue`
   - 使用 set 去重（效率较低）
3. **边界条件**：
   - 数组越界、负数索引
   - 空字符串、空数组
4. **visited 标记**：
   - 全排列：需要 visited 数组
   - 组合/子集：用 start 参数控制
   - 网格问题：原地标记或额外 visited 数组
5. **剪枝遗漏**：不剪枝可能超时

## 适用场景总结

| 问题类型 | 关键技巧 | 时间复杂度 |
|---------|---------|-----------|
| 全排列 | visited 数组 | O(n × n!) |
| 组合/子集 | start 参数 | O(n × 2^n) |
| 组合总和 | 可重复用传 i，不可重复传 i+1 | 指数级 |
| N 皇后 | 逐行放置 + 冲突检查 | O(n!) |
| 岛屿问题 | DFS 标记连通分量 | O(m × n) |
| 括号生成 | 左右括号计数剪枝 | O(4^n / √n) |
| 单词搜索 | 临时标记 + 回溯 | O(m × n × 4^L) |
| 分割问题 | 枚举分割点 | O(n × 2^n) |

**核心技巧**：
- 画决策树，明确选择和路径
- 先写终止条件，再写选择逻辑
- 做选择 → 递归 → 撤销选择（回溯三部曲）
- 剪枝是优化的关键，想清楚什么情况不可能有解
