# 动态规划

## 什么时候用

看到以下特征优先考虑动态规划：
- 求最优解（最大值、最小值、最长、最短）
- 求方案数、可行性判断
- 问题可以分解为重叠子问题
- 当前状态只依赖之前的状态（最优子结构）
- 暴力递归会超时，但子问题会重复计算

核心思路：**定义状态 → 找转移方程 → 确定边界 → 确定计算顺序**。

## 核心要点

1. **状态定义**：`dp[i]` 或 `dp[i][j]` 代表什么含义
2. **转移方程**：当前状态如何从之前的状态得到
3. **初始状态**：边界条件是什么
4. **计算顺序**：从小到大还是从大到小
5. **优化空间**：能否滚动数组、能否降维

## DP 分类

### 1. 线性 DP
- 单序列：爬楼梯、打家劫舍
- 双序列：最长公共子序列、编辑距离

### 2. 背包问题
- 0/1 背包：每个物品选或不选
- 完全背包：每个物品可以选无限次
- 多重背包：每个物品有数量限制

### 3. 区间 DP
- 石子合并、括号匹配

### 4. 树形 DP
- 树的直径、树上背包

### 5. 状态压缩 DP
- 旅行商问题、集合覆盖

## 例题演示

### 例题 1：爬楼梯（基础线性 DP）

**题目**：爬 n 阶楼梯，每次可以爬 1 或 2 阶，有多少种方法？

**思路**：`dp[i]` 表示爬到第 i 阶的方法数，可以从第 i-1 阶爬 1 步，或从第 i-2 阶爬 2 步。

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    
    if (n <= 2) {
        cout << n << "\n";
        return 0;
    }
    
    vector<long long> dp(n + 1);
    dp[1] = 1;
    dp[2] = 2;
    
    for (int i = 3; i <= n; ++i) {
        dp[i] = dp[i - 1] + dp[i - 2];
    }
    
    cout << dp[n] << "\n";
    return 0;
}
```

**空间优化**：只需要记录前两个状态。

```cpp
long long climb_stairs(int n) {
    if (n <= 2) return n;
    
    long long prev2 = 1, prev1 = 2;
    for (int i = 3; i <= n; ++i) {
        long long cur = prev1 + prev2;
        prev2 = prev1;
        prev1 = cur;
    }
    return prev1;
}
```

**复杂度**：时间 `O(n)`，空间 `O(1)`

---

### 例题 2：打家劫舍（线性 DP - 状态依赖）

**题目**：一排房子，每个房子有金额，不能偷相邻的房子，求最大金额。

**思路**：`dp[i]` 表示前 i 个房子能偷的最大金额。
- 不偷第 i 个：`dp[i-1]`
- 偷第 i 个：`dp[i-2] + nums[i]`

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    
    if (n == 0) {
        cout << 0 << "\n";
        return 0;
    }
    if (n == 1) {
        cout << nums[0] << "\n";
        return 0;
    }
    
    vector<int> dp(n);
    dp[0] = nums[0];
    dp[1] = max(nums[0], nums[1]);
    
    for (int i = 2; i < n; ++i) {
        dp[i] = max(dp[i - 1], dp[i - 2] + nums[i]);
    }
    
    cout << dp[n - 1] << "\n";
    return 0;
}
```

**空间优化版本**：

```cpp
int rob(vector<int>& nums) {
    int n = nums.size();
    if (n == 0) return 0;
    if (n == 1) return nums[0];
    
    int prev2 = nums[0];
    int prev1 = max(nums[0], nums[1]);
    
    for (int i = 2; i < n; ++i) {
        int cur = max(prev1, prev2 + nums[i]);
        prev2 = prev1;
        prev1 = cur;
    }
    
    return prev1;
}
```

**复杂度**：时间 `O(n)`，空间 `O(1)`

**易错点**：初始状态 `dp[1] = max(nums[0], nums[1])`，不是 `nums[1]`

---

### 例题 3：最长上升子序列 LIS（经典序列 DP）

**题目**：给定数组，求最长严格上升子序列长度。

**思路 1：O(n²) DP**

`dp[i]` 表示以 `nums[i]` 结尾的最长上升子序列长度。

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    
    vector<int> dp(n, 1);
    int ans = 1;
    
    for (int i = 1; i < n; ++i) {
        for (int j = 0; j < i; ++j) {
            if (nums[j] < nums[i]) {
                dp[i] = max(dp[i], dp[j] + 1);
            }
        }
        ans = max(ans, dp[i]);
    }
    
    cout << ans << "\n";
    return 0;
}
```

**思路 2：O(n log n) 贪心 + 二分**

维护一个数组 `tails`，`tails[i]` 表示长度为 `i+1` 的上升子序列的最小末尾元素。

```cpp
#include <bits/stdc++.h>
using namespace std;

int length_of_LIS(vector<int>& nums) {
    vector<int> tails;
    
    for (int num : nums) {
        auto it = lower_bound(tails.begin(), tails.end(), num);
        if (it == tails.end()) {
            tails.push_back(num);
        } else {
            *it = num;
        }
    }
    
    return tails.size();
}

int main() {
    int n;
    cin >> n;
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    
    cout << length_of_LIS(nums) << "\n";
    return 0;
}
```

**复杂度**：
- DP 方法：时间 `O(n²)`，空间 `O(n)`
- 贪心方法：时间 `O(n log n)`，空间 `O(n)`

**易错点**：
- `lower_bound` 找第一个 `>=` 的位置（严格上升）
- 如果是非严格上升，用 `upper_bound`

---

### 例题 4：最长公共子序列 LCS（双序列 DP）

**题目**：给定两个字符串，求最长公共子序列长度。

**思路**：`dp[i][j]` 表示 `s1[0..i-1]` 和 `s2[0..j-1]` 的 LCS 长度。

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    string s1, s2;
    cin >> s1 >> s2;
    
    int m = s1.size(), n = s2.size();
    vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
    
    for (int i = 1; i <= m; ++i) {
        for (int j = 1; j <= n; ++j) {
            if (s1[i - 1] == s2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }
    
    cout << dp[m][n] << "\n";
    return 0;
}
```

**空间优化**：只需要两行。

```cpp
int lcs(string s1, string s2) {
    int m = s1.size(), n = s2.size();
    vector<int> prev(n + 1, 0), cur(n + 1, 0);
    
    for (int i = 1; i <= m; ++i) {
        for (int j = 1; j <= n; ++j) {
            if (s1[i - 1] == s2[j - 1]) {
                cur[j] = prev[j - 1] + 1;
            } else {
                cur[j] = max(prev[j], cur[j - 1]);
            }
        }
        swap(prev, cur);
    }
    
    return prev[n];
}
```

**复杂度**：时间 `O(mn)`，空间 `O(n)`

---

### 例题 5：编辑距离（双序列 DP）

**题目**：将字符串 s1 转换为 s2，可以插入、删除、替换字符，求最少操作数。

**思路**：`dp[i][j]` 表示 `s1[0..i-1]` 转换为 `s2[0..j-1]` 的最少操作数。

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    string s1, s2;
    cin >> s1 >> s2;
    
    int m = s1.size(), n = s2.size();
    vector<vector<int>> dp(m + 1, vector<int>(n + 1));
    
    // 初始化：从空串转换
    for (int i = 0; i <= m; ++i) dp[i][0] = i;
    for (int j = 0; j <= n; ++j) dp[0][j] = j;
    
    for (int i = 1; i <= m; ++i) {
        for (int j = 1; j <= n; ++j) {
            if (s1[i - 1] == s2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = min({
                    dp[i - 1][j] + 1,      // 删除 s1[i-1]
                    dp[i][j - 1] + 1,      // 插入 s2[j-1]
                    dp[i - 1][j - 1] + 1   // 替换
                });
            }
        }
    }
    
    cout << dp[m][n] << "\n";
    return 0;
}
```

**复杂度**：时间 `O(mn)`，空间 `O(mn)`

**易错点**：初始状态要设置为从空串转换的代价

---

### 例题 6：0/1 背包（经典背包 DP）

**题目**：n 个物品，每个有重量 w[i] 和价值 v[i]，背包容量 W，求最大价值。

**思路**：`dp[i][j]` 表示前 i 个物品，容量 j 的最大价值。

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, W;
    cin >> n >> W;
    
    vector<int> w(n + 1), v(n + 1);
    for (int i = 1; i <= n; ++i) {
        cin >> w[i] >> v[i];
    }
    
    vector<vector<int>> dp(n + 1, vector<int>(W + 1, 0));
    
    for (int i = 1; i <= n; ++i) {
        for (int j = 0; j <= W; ++j) {
            // 不选第 i 个物品
            dp[i][j] = dp[i - 1][j];
            // 选第 i 个物品
            if (j >= w[i]) {
                dp[i][j] = max(dp[i][j], dp[i - 1][j - w[i]] + v[i]);
            }
        }
    }
    
    cout << dp[n][W] << "\n";
    return 0;
}
```

**空间优化**：逆序遍历容量。

```cpp
int knapsack_01(int n, int W, vector<int>& w, vector<int>& v) {
    vector<int> dp(W + 1, 0);
    
    for (int i = 1; i <= n; ++i) {
        for (int j = W; j >= w[i]; --j) {
            dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
        }
    }
    
    return dp[W];
}
```

**复杂度**：时间 `O(nW)`，空间 `O(W)`

**易错点**：一维优化时必须逆序遍历，否则会重复选择同一物品

---

### 例题 7：完全背包

**题目**：n 个物品，每个可以选无限次，背包容量 W，求最大价值。

**思路**：与 0/1 背包类似，但容量正序遍历。

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, W;
    cin >> n >> W;
    
    vector<int> w(n + 1), v(n + 1);
    for (int i = 1; i <= n; ++i) {
        cin >> w[i] >> v[i];
    }
    
    vector<int> dp(W + 1, 0);
    
    for (int i = 1; i <= n; ++i) {
        for (int j = w[i]; j <= W; ++j) {
            dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
        }
    }
    
    cout << dp[W] << "\n";
    return 0;
}
```

**复杂度**：时间 `O(nW)`，空间 `O(W)`

**易错点**：完全背包正序遍历，0/1 背包逆序遍历

---

### 例题 8：零钱兑换（完全背包 - 求最少数量）

**题目**：给定面额数组 coins，凑成金额 amount，求最少硬币数。

**思路**：`dp[i]` 表示凑成金额 i 的最少硬币数。

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, amount;
    cin >> n >> amount;
    
    vector<int> coins(n);
    for (int i = 0; i < n; ++i) {
        cin >> coins[i];
    }
    
    vector<int> dp(amount + 1, INT_MAX);
    dp[0] = 0;
    
    for (int coin : coins) {
        for (int i = coin; i <= amount; ++i) {
            if (dp[i - coin] != INT_MAX) {
                dp[i] = min(dp[i], dp[i - coin] + 1);
            }
        }
    }
    
    cout << (dp[amount] == INT_MAX ? -1 : dp[amount]) << "\n";
    return 0;
}
```

**复杂度**：时间 `O(n × amount)`，空间 `O(amount)`

**易错点**：初始值设为 `INT_MAX`，更新时检查是否为 `INT_MAX`

---

### 例题 9：零钱兑换 II（完全背包 - 求方案数）

**题目**：给定面额数组 coins，凑成金额 amount，求方案数。

**思路**：`dp[i]` 表示凑成金额 i 的方案数。

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, amount;
    cin >> n >> amount;
    
    vector<int> coins(n);
    for (int i = 0; i < n; ++i) {
        cin >> coins[i];
    }
    
    vector<long long> dp(amount + 1, 0);
    dp[0] = 1;
    
    for (int coin : coins) {
        for (int i = coin; i <= amount; ++i) {
            dp[i] += dp[i - coin];
        }
    }
    
    cout << dp[amount] << "\n";
    return 0;
}
```

**复杂度**：时间 `O(n × amount)`，空间 `O(amount)`

**易错点**：枚举顺序影响结果，先枚举物品再枚举容量（组合），先枚举容量再枚举物品（排列）

---

### 例题 10：石子合并（区间 DP）

**题目**：n 堆石子排成一排，每次合并相邻两堆，代价是两堆石子数之和，求最小总代价。

**思路**：`dp[i][j]` 表示合并第 i 到 j 堆的最小代价。

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    
    vector<int> stones(n + 1);
    vector<int> sum(n + 1, 0);
    
    for (int i = 1; i <= n; ++i) {
        cin >> stones[i];
        sum[i] = sum[i - 1] + stones[i];
    }
    
    vector<vector<int>> dp(n + 1, vector<int>(n + 1, 0));
    
    // len 是合并的长度
    for (int len = 2; len <= n; ++len) {
        for (int i = 1; i + len - 1 <= n; ++i) {
            int j = i + len - 1;
            dp[i][j] = INT_MAX;
            
            for (int k = i; k < j; ++k) {
                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k + 1][j] + sum[j] - sum[i - 1]);
            }
        }
    }
    
    cout << dp[1][n] << "\n";
    return 0;
}
```

**复杂度**：时间 `O(n³)`，空间 `O(n²)`

**易错点**：
- 区间 DP 要按区间长度递增枚举
- 合并代价是 `sum[j] - sum[i-1]`（前缀和）

---

### 例题 11：最大正方形（二维 DP）

**题目**：给定 0/1 矩阵，找到最大的全 1 正方形，返回面积。

**思路**：`dp[i][j]` 表示以 `(i, j)` 为右下角的最大正方形边长。

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int m, n;
    cin >> m >> n;
    
    vector<vector<int>> matrix(m, vector<int>(n));
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            cin >> matrix[i][j];
        }
    }
    
    vector<vector<int>> dp(m, vector<int>(n, 0));
    int max_side = 0;
    
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            if (matrix[i][j] == 1) {
                if (i == 0 || j == 0) {
                    dp[i][j] = 1;
                } else {
                    dp[i][j] = min({dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]}) + 1;
                }
                max_side = max(max_side, dp[i][j]);
            }
        }
    }
    
    cout << max_side * max_side << "\n";
    return 0;
}
```

**复杂度**：时间 `O(mn)`，空间 `O(mn)`

**易错点**：转移方程是三个方向的最小值加 1

---

### 例题 12：分割等和子集（0/1 背包变形）

**题目**：给定数组，判断能否分成两个子集，使得两个子集元素和相等。

**思路**：转化为背包问题，目标是凑成 `sum/2`。

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    
    vector<int> nums(n);
    int sum = 0;
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
        sum += nums[i];
    }
    
    if (sum % 2 != 0) {
        cout << "NO\n";
        return 0;
    }
    
    int target = sum / 2;
    vector<bool> dp(target + 1, false);
    dp[0] = true;
    
    for (int num : nums) {
        for (int j = target; j >= num; --j) {
            dp[j] = dp[j] || dp[j - num];
        }
    }
    
    cout << (dp[target] ? "YES" : "NO") << "\n";
    return 0;
}
```

**复杂度**：时间 `O(n × sum)`，空间 `O(sum)`

**易错点**：必须逆序遍历，避免重复使用元素

---

## 常见陷阱

1. **状态定义不清**：`dp[i]` 到底是以 i 结尾还是前 i 个？明确定义
2. **初始状态错误**：边界条件要仔细检查
3. **转移方程遗漏情况**：所有可能的转移都考虑到了吗？
4. **循环顺序错误**：
   - 0/1 背包：逆序
   - 完全背包：正序
   - 区间 DP：按长度递增
5. **空间优化后出错**：滚动数组要注意依赖关系
6. **整数溢出**：累加、乘法用 `long long`
7. **返回值错误**：注意是返回 `dp[n]` 还是 `max(dp)`

## DP 解题步骤

1. **确定状态**：变量是什么，维度是多少
2. **写出状态转移方程**：当前状态如何从之前状态得到
3. **确定初始状态**：边界条件
4. **确定遍历顺序**：从小到大还是从大到小
5. **返回结果**：最终答案在哪个状态

## 优化技巧

1. **滚动数组**：`dp[i]` 只依赖 `dp[i-1]`，用两个数组交替
2. **降维**：0/1 背包从二维降到一维
3. **剪枝**：提前结束不可能的状态
4. **记忆化搜索**：自顶向下的 DP，用递归 + 缓存

## 适用场景总结

- **线性 DP**：单序列或双序列最优化问题
- **背包 DP**：选择物品凑成目标的问题
- **区间 DP**：合并、分割区间的问题
- **树形 DP**：树上路径、子树统计的问题
- **状态压缩 DP**：集合选择、排列组合的问题
