# 前缀和与差分

## 什么时候用

看到以下特征优先考虑前缀和/差分：
- **多次查询**区间和/区域和
- 子数组和问题：和为 k、最大子数组和
- 二维矩阵的子矩形和
- **多次区间修改 + 一次查询**：差分数组

核心思路：**用 O(1) 查询替代 O(n) 的累加**。

## 前缀和核心公式

### 一维前缀和

```cpp
// 构建
vector<long long> pre(n + 1, 0);
for (int i = 0; i < n; ++i) {
    pre[i + 1] = pre[i] + arr[i];
}

// 查询 [l, r] 的和
long long sum = pre[r + 1] - pre[l];
```

**为什么用 n+1**：避免 `l=0` 时特判，`pre[0] = 0` 表示空前缀。

### 二维前缀和

```cpp
// 构建
vector<vector<long long>> pre(n + 1, vector<long long>(m + 1, 0));
for (int i = 0; i < n; ++i) {
    for (int j = 0; j < m; ++j) {
        pre[i + 1][j + 1] = pre[i][j + 1] + pre[i + 1][j] 
                          - pre[i][j] + mat[i][j];
    }
}

// 查询矩形 (x1, y1) 到 (x2, y2) 的和
long long sum = pre[x2 + 1][y2 + 1] - pre[x1][y2 + 1] 
              - pre[x2 + 1][y1] + pre[x1][y1];
```

**记忆方法**：容斥原理，加右下，减左下和右上，加回左上。

## 差分数组

差分是前缀和的逆运算，用于**批量区间修改**。

```cpp
// 初始化
vector<long long> diff(n + 1, 0);

// 区间 [l, r] 加 v
diff[l] += v;
diff[r + 1] -= v;

// 还原数组
vector<long long> arr(n);
long long sum = 0;
for (int i = 0; i < n; ++i) {
    sum += diff[i];
    arr[i] = sum;
}
```

**适用场景**：多次区间修改，最后一次性查询。

## 例题演示

### 例题 1：区域和检索（不可变）

**题目**：LeetCode 303 - 给定数组，多次查询区间 [l, r] 的和。

```cpp
#include <bits/stdc++.h>
using namespace std;

class NumArray {
private:
    vector<long long> pre;
    
public:
    NumArray(vector<int>& nums) {
        int n = nums.size();
        pre.resize(n + 1, 0);
        for (int i = 0; i < n; ++i) {
            pre[i + 1] = pre[i] + nums[i];
        }
    }
    
    int sum_range(int left, int right) {
        return pre[right + 1] - pre[left];
    }
};

int main() {
    int n, q;
    cin >> n >> q;
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    
    NumArray arr(nums);
    
    while (q--) {
        int l, r;
        cin >> l >> r;
        cout << arr.sum_range(l, r) << "\n";
    }
    
    return 0;
}
```

**复杂度**：预处理 O(n)，每次查询 O(1)

---

### 例题 2：和为 K 的子数组

**题目**：LeetCode 560 - 给定数组和整数 k，找出和为 k 的连续子数组个数。

**思路**：前缀和 + 哈希表。如果 `pre[j] - pre[i] = k`，则 `pre[i] = pre[j] - k`。

```cpp
#include <bits/stdc++.h>
using namespace std;

int subarray_sum(vector<int>& nums, int k) {
    unordered_map<long long, int> mp;
    mp[0] = 1; // 空前缀
    
    long long pre = 0;
    int count = 0;
    
    for (int num : nums) {
        pre += num;
        
        // 找有多少个前缀和 = pre - k
        if (mp.count(pre - k)) {
            count += mp[pre - k];
        }
        
        mp[pre]++;
    }
    
    return count;
}

int main() {
    int n, k;
    cin >> n >> k;
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    
    cout << subarray_sum(nums, k) << "\n";
    
    return 0;
}
```

**复杂度**：时间 O(n)，空间 O(n)

---

### 例题 3：连续子数组的最大和（前缀和优化）

**题目**：LeetCode 53 - 找出数组中和最大的连续子数组。

**思路 1**：Kadane 算法（贪心）

```cpp
int max_subarray(vector<int>& nums) {
    int max_sum = INT_MIN, current_sum = 0;
    
    for (int num : nums) {
        current_sum = max(num, current_sum + num);
        max_sum = max(max_sum, current_sum);
    }
    
    return max_sum;
}
```

**思路 2**：前缀和 + 维护最小前缀

```cpp
int max_subarray(vector<int>& nums) {
    long long pre = 0, min_pre = 0, max_sum = LLONG_MIN;
    
    for (int num : nums) {
        pre += num;
        max_sum = max(max_sum, pre - min_pre);
        min_pre = min(min_pre, pre);
    }
    
    return max_sum;
}
```

**复杂度**：时间 O(n)，空间 O(1)

---

### 例题 4：二维区域和检索

**题目**：LeetCode 304 - 给定矩阵，多次查询子矩形和。

```cpp
#include <bits/stdc++.h>
using namespace std;

class NumMatrix {
private:
    vector<vector<long long>> pre;
    
public:
    NumMatrix(vector<vector<int>>& matrix) {
        if (matrix.empty()) return;
        int n = matrix.size(), m = matrix[0].size();
        pre.resize(n + 1, vector<long long>(m + 1, 0));
        
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < m; ++j) {
                pre[i + 1][j + 1] = pre[i][j + 1] + pre[i + 1][j]
                                  - pre[i][j] + matrix[i][j];
            }
        }
    }
    
    int sum_region(int x1, int y1, int x2, int y2) {
        return pre[x2 + 1][y2 + 1] - pre[x1][y2 + 1] 
             - pre[x2 + 1][y1] + pre[x1][y1];
    }
};

int main() {
    int n, m, q;
    cin >> n >> m >> q;
    vector<vector<int>> matrix(n, vector<int>(m));
    
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            cin >> matrix[i][j];
        }
    }
    
    NumMatrix mat(matrix);
    
    while (q--) {
        int x1, y1, x2, y2;
        cin >> x1 >> y1 >> x2 >> y2;
        cout << mat.sum_region(x1, y1, x2, y2) << "\n";
    }
    
    return 0;
}
```

**复杂度**：预处理 O(n·m)，每次查询 O(1)

---

### 例题 5：差分数组 - 区间加法

**题目**：LeetCode 370 - 给定长度 n 的全 0 数组，执行 m 次区间加操作，返回最终数组。

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> get_modified_array(int n, vector<vector<int>>& updates) {
    vector<long long> diff(n + 1, 0);
    
    // 批量修改
    for (const auto& update : updates) {
        int l = update[0], r = update[1], val = update[2];
        diff[l] += val;
        diff[r + 1] -= val;
    }
    
    // 还原数组
    vector<int> result(n);
    long long sum = 0;
    for (int i = 0; i < n; ++i) {
        sum += diff[i];
        result[i] = sum;
    }
    
    return result;
}

int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<int>> updates(m, vector<int>(3));
    
    for (int i = 0; i < m; ++i) {
        cin >> updates[i][0] >> updates[i][1] >> updates[i][2];
    }
    
    auto result = get_modified_array(n, updates);
    
    for (int i = 0; i < n; ++i) {
        cout << result[i] << " \n"[i == n - 1];
    }
    
    return 0;
}
```

**复杂度**：时间 O(n + m)，空间 O(n)

**不用差分**：直接修改需要 O(n·m)

---

### 例题 6：航班预订统计

**题目**：LeetCode 1109 - n 个航班，m 个预订记录 [first, last, seats]，统计每个航班的座位数。

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> corp_flight_bookings(vector<vector<int>>& bookings, int n) {
    vector<long long> diff(n + 2, 0); // 注意：航班编号 1-indexed
    
    for (const auto& b : bookings) {
        int first = b[0], last = b[1], seats = b[2];
        diff[first] += seats;
        diff[last + 1] -= seats;
    }
    
    vector<int> result(n);
    long long sum = 0;
    for (int i = 1; i <= n; ++i) {
        sum += diff[i];
        result[i - 1] = sum;
    }
    
    return result;
}

int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<int>> bookings(m, vector<int>(3));
    
    for (int i = 0; i < m; ++i) {
        cin >> bookings[i][0] >> bookings[i][1] >> bookings[i][2];
    }
    
    auto result = corp_flight_bookings(bookings, n);
    
    for (int i = 0; i < n; ++i) {
        cout << result[i] << " \n"[i == n - 1];
    }
    
    return 0;
}
```

**复杂度**：时间 O(n + m)，空间 O(n)

---

### 例题 7：连续数组（01 个数相等）

**题目**：LeetCode 525 - 找出 01 数组中 0 和 1 数量相等的最长连续子数组。

**思路**：将 0 看作 -1，问题转化为"和为 0 的最长子数组"。用前缀和 + 哈希表记录每个前缀和第一次出现的位置。

```cpp
#include <bits/stdc++.h>
using namespace std;

int find_max_length(vector<int>& nums) {
    unordered_map<int, int> first_pos;
    first_pos[0] = -1; // 空前缀在位置 -1
    
    int pre = 0, max_len = 0;
    
    for (int i = 0; i < (int)nums.size(); ++i) {
        pre += (nums[i] == 1 ? 1 : -1);
        
        if (first_pos.count(pre)) {
            max_len = max(max_len, i - first_pos[pre]);
        } else {
            first_pos[pre] = i;
        }
    }
    
    return max_len;
}

int main() {
    int n;
    cin >> n;
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    
    cout << find_max_length(nums) << "\n";
    
    return 0;
}
```

**复杂度**：时间 O(n)，空间 O(n)

---

### 例题 8：可被 K 整除的子数组

**题目**：LeetCode 974 - 找出和可被 k 整除的连续子数组个数。

**思路**：前缀和取模。如果 `(pre[j] - pre[i]) % k == 0`，则 `pre[j] % k == pre[i] % k`。

```cpp
#include <bits/stdc++.h>
using namespace std;

int subarrays_div_by_k(vector<int>& nums, int k) {
    unordered_map<int, int> mod_count;
    mod_count[0] = 1; // 空前缀
    
    int pre = 0, count = 0;
    
    for (int num : nums) {
        pre += num;
        int mod = ((pre % k) + k) % k; // 处理负数
        
        count += mod_count[mod];
        mod_count[mod]++;
    }
    
    return count;
}

int main() {
    int n, k;
    cin >> n >> k;
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    
    cout << subarrays_div_by_k(nums, k) << "\n";
    
    return 0;
}
```

**复杂度**：时间 O(n)，空间 O(k)

**易错点**：C++ 负数取模是负数，需要 `((x % k) + k) % k` 转换为正数

---

## 前缀和变体

### 前缀积

```cpp
vector<long long> pre(n + 1, 1);
for (int i = 0; i < n; ++i) {
    pre[i + 1] = pre[i] * arr[i];
}
```

### 前缀异或

```cpp
vector<int> pre(n + 1, 0);
for (int i = 0; i < n; ++i) {
    pre[i + 1] = pre[i] ^ arr[i];
}

// 区间 [l, r] 的异或和
int xor_sum = pre[r + 1] ^ pre[l];
```

### 前缀最大值/最小值

```cpp
vector<int> pre_max(n);
pre_max[0] = arr[0];
for (int i = 1; i < n; ++i) {
    pre_max[i] = max(pre_max[i - 1], arr[i]);
}
```

## 常见陷阱

1. **溢出**：累加和用 `long long`
2. **下标混淆**：统一用 `pre[n+1]`，查询 `[l, r]` 用 `pre[r+1] - pre[l]`
3. **负数取模**：C++ 中 `-5 % 3 = -2`，需要 `((x % k) + k) % k`
4. **二维前缀和公式**：容斥原理，注意符号
5. **哈希表初始化**：`mp[0] = 1` 或 `mp[0] = -1`，根据题意决定

## 适用场景总结

| 技巧 | 适用场景 | 复杂度 |
|------|----------|--------|
| 一维前缀和 | 多次查询区间和 | 预处理 O(n)，查询 O(1) |
| 二维前缀和 | 多次查询子矩形和 | 预处理 O(n·m)，查询 O(1) |
| 差分数组 | 多次区间修改 + 一次查询 | O(n + m) |
| 前缀和 + 哈希 | 子数组和为 k、和可被 k 整除 | O(n) |
| 前缀和 + 最值 | 最大子数组和 | O(n) |
