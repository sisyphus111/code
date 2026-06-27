# 二分查找与二分答案

## 什么时候用

看到以下特征优先考虑二分：
- **有序数组**查找元素
- "最小化最大值" 或 "最大化最小值"
- "能否在 x 时间内完成"
- 数据范围很大（≤10⁹）但答案范围可枚举
- 分配、切割、运输类问题

核心思路：**将 O(n) 的线性查找优化为 O(log n)**。

## 二分查找模板

### 查找第一个 ≥ x 的位置

```cpp
int lower_bound_manual(const vector<int>& arr, int x) {
    int l = 0, r = arr.size(); // 左闭右开 [l, r)
    while (l < r) {
        int mid = l + (r - l) / 2;
        if (arr[mid] >= x) {
            r = mid;
        } else {
            l = mid + 1;
        }
    }
    return l;
}
```

### 查找最后一个 ≤ x 的位置

```cpp
int upper_bound_manual(const vector<int>& arr, int x) {
    int l = 0, r = arr.size();
    while (l < r) {
        int mid = l + (r - l) / 2;
        if (arr[mid] <= x) {
            l = mid + 1;
        } else {
            r = mid;
        }
    }
    return l - 1;
}
```

### STL 二分

```cpp
// 第一个 >= x
auto it = lower_bound(arr.begin(), arr.end(), x);

// 第一个 > x
auto it = upper_bound(arr.begin(), arr.end(), x);

// 是否存在
bool exists = binary_search(arr.begin(), arr.end(), x);
```

## 二分答案模板

### 找最小可行值

```cpp
bool check(long long x) {
    // 判断 x 是否可行
    return true;
}

long long binary_answer_min(long long l, long long r) {
    while (l < r) {
        long long mid = l + (r - l) / 2;
        if (check(mid)) {
            r = mid; // 可行，尝试更小
        } else {
            l = mid + 1; // 不可行，必须更大
        }
    }
    return l;
}
```

### 找最大可行值

```cpp
long long binary_answer_max(long long l, long long r) {
    while (l < r) {
        long long mid = l + (r - l + 1) / 2; // 注意 +1
        if (check(mid)) {
            l = mid; // 可行，尝试更大
        } else {
            r = mid - 1; // 不可行，必须更小
        }
    }
    return l;
}
```

**关键差异**：求最大值时 `mid` 要加 1，否则 `l = r - 1` 时会死循环。

## 例题演示

### 例题 1：搜索插入位置

**题目**：LeetCode 35 - 有序数组中查找目标值，如果不存在则返回插入位置。

```cpp
#include <bits/stdc++.h>
using namespace std;

int search_insert(vector<int>& nums, int target) {
    int l = 0, r = nums.size();
    while (l < r) {
        int mid = l + (r - l) / 2;
        if (nums[mid] >= target) {
            r = mid;
        } else {
            l = mid + 1;
        }
    }
    return l;
}

int main() {
    int n, target;
    cin >> n >> target;
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    cout << search_insert(nums, target) << "\n";
    return 0;
}
```

**复杂度**：O(log n)

---

### 例题 2：在排序数组中查找元素的第一个和最后一个位置

**题目**：LeetCode 34 - 找出目标值的起始和结束位置。

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> search_range(vector<int>& nums, int target) {
    if (nums.empty()) return {-1, -1};
    
    // 找第一个 >= target
    int l = 0, r = nums.size();
    while (l < r) {
        int mid = l + (r - l) / 2;
        if (nums[mid] >= target) r = mid;
        else l = mid + 1;
    }
    
    int first = l;
    if (first >= (int)nums.size() || nums[first] != target) {
        return {-1, -1};
    }
    
    // 找最后一个 <= target
    l = 0; r = nums.size();
    while (l < r) {
        int mid = l + (r - l) / 2;
        if (nums[mid] <= target) l = mid + 1;
        else r = mid;
    }
    
    int last = l - 1;
    
    return {first, last};
}

int main() {
    int n, target;
    cin >> n >> target;
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    
    auto result = search_range(nums, target);
    cout << result[0] << " " << result[1] << "\n";
    
    return 0;
}
```

**复杂度**：O(log n)

---

### 例题 3：x 的平方根

**题目**：LeetCode 69 - 计算并返回 x 的平方根（取整）。

```cpp
#include <bits/stdc++.h>
using namespace std;

int my_sqrt(int x) {
    if (x == 0) return 0;
    
    long long l = 1, r = x;
    while (l < r) {
        long long mid = l + (r - l + 1) / 2;
        if (mid * mid <= x) {
            l = mid;
        } else {
            r = mid - 1;
        }
    }
    
    return l;
}

int main() {
    int x;
    cin >> x;
    cout << my_sqrt(x) << "\n";
    return 0;
}
```

**复杂度**：O(log n)

**易错点**：`mid * mid` 可能溢出，用 `long long`

---

### 例题 4：分割数组的最大值（二分答案）

**题目**：LeetCode 410 - 将数组分成 m 个非空连续子数组，使得这 m 个子数组各自和的最大值最小。

**思路**：二分答案。答案范围是 [max(nums), sum(nums)]。check(x) 判断能否在每段和 ≤ x 的条件下分成 ≤ m 段。

```cpp
#include <bits/stdc++.h>
using namespace std;

bool can_split(vector<int>& nums, int m, long long max_sum) {
    int segments = 1;
    long long current_sum = 0;
    
    for (int num : nums) {
        if (current_sum + num > max_sum) {
            segments++;
            current_sum = num;
            if (segments > m) return false;
        } else {
            current_sum += num;
        }
    }
    
    return true;
}

int split_array(vector<int>& nums, int m) {
    long long l = *max_element(nums.begin(), nums.end());
    long long r = accumulate(nums.begin(), nums.end(), 0LL);
    
    while (l < r) {
        long long mid = l + (r - l) / 2;
        if (can_split(nums, m, mid)) {
            r = mid;
        } else {
            l = mid + 1;
        }
    }
    
    return l;
}

int main() {
    int n, m;
    cin >> n >> m;
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    
    cout << split_array(nums, m) << "\n";
    
    return 0;
}
```

**复杂度**：O(n log S)，S 为数组和

---

### 例题 5：爱吃香蕉的珂珂

**题目**：LeetCode 875 - 有 n 堆香蕉，每堆 piles[i] 根。珂珂每小时吃 k 根（一堆吃完才吃下一堆），h 小时内吃完所有香蕉，求最小的 k。

**思路**：二分答案 k，范围 [1, max(piles)]。

```cpp
#include <bits/stdc++.h>
using namespace std;

bool can_finish(vector<int>& piles, int h, int k) {
    long long hours = 0;
    for (int pile : piles) {
        hours += (pile + k - 1) / k; // 向上取整
        if (hours > h) return false;
    }
    return true;
}

int min_eating_speed(vector<int>& piles, int h) {
    int l = 1, r = *max_element(piles.begin(), piles.end());
    
    while (l < r) {
        int mid = l + (r - l) / 2;
        if (can_finish(piles, h, mid)) {
            r = mid;
        } else {
            l = mid + 1;
        }
    }
    
    return l;
}

int main() {
    int n, h;
    cin >> n >> h;
    vector<int> piles(n);
    for (int i = 0; i < n; ++i) {
        cin >> piles[i];
    }
    
    cout << min_eating_speed(piles, h) << "\n";
    
    return 0;
}
```

**复杂度**：O(n log M)，M 为最大堆数

---

### 例题 6：在 D 天内送达包裹的能力

**题目**：LeetCode 1011 - 传送带上有包裹，第 i 个包裹重量 weights[i]。每天按顺序装载包裹，船的载重量至少为多少才能在 D 天内送达所有包裹？

```cpp
#include <bits/stdc++.h>
using namespace std;

bool can_ship(vector<int>& weights, int days, int capacity) {
    int used_days = 1, current_weight = 0;
    
    for (int w : weights) {
        if (current_weight + w > capacity) {
            used_days++;
            current_weight = w;
            if (used_days > days) return false;
        } else {
            current_weight += w;
        }
    }
    
    return true;
}

int ship_within_days(vector<int>& weights, int days) {
    int l = *max_element(weights.begin(), weights.end());
    int r = accumulate(weights.begin(), weights.end(), 0);
    
    while (l < r) {
        int mid = l + (r - l) / 2;
        if (can_ship(weights, days, mid)) {
            r = mid;
        } else {
            l = mid + 1;
        }
    }
    
    return l;
}

int main() {
    int n, days;
    cin >> n >> days;
    vector<int> weights(n);
    for (int i = 0; i < n; ++i) {
        cin >> weights[i];
    }
    
    cout << ship_within_days(weights, days) << "\n";
    
    return 0;
}
```

**复杂度**：O(n log S)

---

### 例题 7：寻找旋转排序数组中的最小值

**题目**：LeetCode 153 - 旋转后的有序数组，找最小值。

```cpp
#include <bits/stdc++.h>
using namespace std;

int find_min(vector<int>& nums) {
    int l = 0, r = nums.size() - 1;
    
    while (l < r) {
        int mid = l + (r - l) / 2;
        
        if (nums[mid] > nums[r]) {
            // 最小值在右半部分
            l = mid + 1;
        } else {
            // 最小值在左半部分（包括 mid）
            r = mid;
        }
    }
    
    return nums[l];
}

int main() {
    int n;
    cin >> n;
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    
    cout << find_min(nums) << "\n";
    
    return 0;
}
```

**复杂度**：O(log n)

---

### 例题 8：搜索旋转排序数组

**题目**：LeetCode 33 - 旋转后的有序数组中查找目标值。

```cpp
#include <bits/stdc++.h>
using namespace std;

int search(vector<int>& nums, int target) {
    int l = 0, r = nums.size() - 1;
    
    while (l <= r) {
        int mid = l + (r - l) / 2;
        
        if (nums[mid] == target) return mid;
        
        // 判断哪一半是有序的
        if (nums[l] <= nums[mid]) {
            // 左半有序
            if (nums[l] <= target && target < nums[mid]) {
                r = mid - 1;
            } else {
                l = mid + 1;
            }
        } else {
            // 右半有序
            if (nums[mid] < target && target <= nums[r]) {
                l = mid + 1;
            } else {
                r = mid - 1;
            }
        }
    }
    
    return -1;
}

int main() {
    int n, target;
    cin >> n >> target;
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    
    cout << search(nums, target) << "\n";
    
    return 0;
}
```

**复杂度**：O(log n)

---

## 浮点二分

用于求解方程、精度要求的问题。

```cpp
double binary_search_float(double l, double r, double eps = 1e-9) {
    for (int iter = 0; iter < 100; ++iter) { // 固定迭代次数更稳
        double mid = (l + r) / 2;
        if (check(mid)) {
            r = mid;
        } else {
            l = mid;
        }
    }
    return l;
}
```

## 常见陷阱

1. **整数溢出**：`(l + r) / 2` 可能溢出，用 `l + (r - l) / 2`
2. **死循环**：求最大值时忘记 `mid = l + (r - l + 1) / 2`
3. **边界混淆**：
   - `while (l < r)` 配 `[l, r)` 或 `[l, r]`
   - `while (l <= r)` 配 `[l, r]`
   - 统一使用一种模板
4. **check 函数单调性**：必须保证答案越大/越小，条件越容易/越难满足
5. **答案范围**：左边界要能通过 check，右边界要保证答案在内

## 二分答案适用场景

| 题型 | 特征 | 模板 |
|------|------|------|
| 最小化最大值 | 分配、切割、运输 | 求最小可行值 |
| 最大化最小值 | 间距、分组 | 求最大可行值 |
| 能否完成 | 时间限制、容量限制 | 判定性二分 |

## 识别二分答案的技巧

1. 题目出现"最小化最大"或"最大化最小"
2. 直接求答案很难，但判断某个值是否可行很容易
3. 答案具有单调性：如果 x 可行，那么 x+1 也可行（或相反）
4. 答案范围很大但可以枚举
