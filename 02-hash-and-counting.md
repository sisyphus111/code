# 哈希表与计数

## 什么时候用

看到以下特征优先考虑哈希：
- 统计频次、出现次数
- 判断元素是否存在
- 去重
- 两数之和、多数之和
- 字符串/数组的分组、映射
- 编号映射：将字符串、坐标等映射到整数 ID

核心思路：**用 O(1) 的查找替代 O(n) 的遍历**。

## 容器选择

| 容器 | 复杂度 | 有序性 | 使用场景 |
|------|--------|--------|----------|
| `unordered_map` | 平均 O(1) | 无序 | 频次统计、快速查找 |
| `map` | O(log n) | 按 key 有序 | 需要有序遍历、找前驱后继 |
| `unordered_set` | 平均 O(1) | 无序 | 去重、判断存在 |
| `set` | O(log n) | 有序 | 有序去重、动态维护有序集合 |

## 核心模板

### 频次统计

```cpp
unordered_map<int, int> cnt;
for (int x : arr) {
    cnt[x]++;
}

// 找出现次数最多的元素
int max_cnt = 0, most_frequent = -1;
for (auto [val, freq] : cnt) {
    if (freq > max_cnt) {
        max_cnt = freq;
        most_frequent = val;
    }
}
```

### 判断存在（避免插入）

```cpp
unordered_map<int, int> mp;

// 错误：会插入默认值 0
if (mp[x] > 0) { ... }

// 正确：不插入
if (mp.count(x)) { ... }
if (mp.find(x) != mp.end()) { ... }
```

### 编号映射

```cpp
unordered_map<string, int> id;

int get_id(const string& s) {
    if (!id.count(s)) {
        id[s] = id.size();
    }
    return id[s];
}
```

## 例题演示

### 例题 1：两数之和

**题目**：LeetCode 1 - 给定数组和目标值，找出两个数的索引使得它们相加等于目标值。

**思路**：遍历数组，对于每个 `nums[i]`，查找 `target - nums[i]` 是否在哈希表中。

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> two_sum(vector<int>& nums, int target) {
    unordered_map<int, int> mp; // value -> index
    
    for (int i = 0; i < (int)nums.size(); ++i) {
        int complement = target - nums[i];
        if (mp.count(complement)) {
            return {mp[complement], i};
        }
        mp[nums[i]] = i;
    }
    
    return {};
}

int main() {
    int n, target;
    cin >> n >> target;
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    
    auto res = two_sum(nums, target);
    if (res.empty()) {
        cout << "No solution\n";
    } else {
        cout << res[0] << " " << res[1] << "\n";
    }
    
    return 0;
}
```

**复杂度**：时间 O(n)，空间 O(n)

**易错点**：
- 要返回索引而不是值
- 注意同一个元素不能使用两次

---

### 例题 2：字母异位词分组

**题目**：LeetCode 49 - 给定字符串数组，将字母异位词分组。

**思路**：字母异位词排序后相同，用排序后的字符串作为哈希表的 key。

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<vector<string>> group_anagrams(vector<string>& strs) {
    unordered_map<string, vector<string>> mp;
    
    for (const string& s : strs) {
        string key = s;
        sort(key.begin(), key.end());
        mp[key].push_back(s);
    }
    
    vector<vector<string>> result;
    for (auto& [key, group] : mp) {
        result.push_back(move(group));
    }
    
    return result;
}

int main() {
    int n;
    cin >> n;
    vector<string> strs(n);
    for (int i = 0; i < n; ++i) {
        cin >> strs[i];
    }
    
    auto groups = group_anagrams(strs);
    
    for (const auto& group : groups) {
        for (const auto& s : group) {
            cout << s << " ";
        }
        cout << "\n";
    }
    
    return 0;
}
```

**复杂度**：时间 O(n·k log k)，k 为字符串平均长度

**另一种 key 生成方式**（更快，O(n·k)）：

```cpp
string get_key(const string& s) {
    int cnt[26] = {0};
    for (char c : s) {
        cnt[c - 'a']++;
    }
    string key;
    for (int i = 0; i < 26; ++i) {
        if (cnt[i] > 0) {
            key += char('a' + i);
            key += to_string(cnt[i]);
        }
    }
    return key;
}
```

---

### 例题 3：最长连续序列

**题目**：LeetCode 128 - 给定无序数组，找出最长连续序列的长度。要求 O(n) 时间。

**思路**：用哈希集合存储所有数字，对于每个数字 x，如果 x-1 不存在（即 x 是序列起点），则向右扩展计数。

```cpp
#include <bits/stdc++.h>
using namespace std;

int longest_consecutive(vector<int>& nums) {
    unordered_set<int> st(nums.begin(), nums.end());
    
    int max_len = 0;
    for (int num : st) {
        // 只从序列起点开始计数
        if (!st.count(num - 1)) {
            int current = num;
            int len = 1;
            
            while (st.count(current + 1)) {
                current++;
                len++;
            }
            
            max_len = max(max_len, len);
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
    
    cout << longest_consecutive(nums) << "\n";
    
    return 0;
}
```

**复杂度**：时间 O(n)，空间 O(n)

**关键点**：通过 `if (!st.count(num - 1))` 确保每个序列只被遍历一次

---

### 例题 4：和为 K 的子数组数量

**题目**：LeetCode 560 - 给定整数数组和整数 k，找出和为 k 的连续子数组个数。

**思路**：前缀和 + 哈希表。`presum[j] - presum[i] = k` 等价于 `presum[i] = presum[j] - k`。

```cpp
#include <bits/stdc++.h>
using namespace std;

int subarray_sum(vector<int>& nums, int k) {
    unordered_map<int, int> mp; // presum -> count
    mp[0] = 1; // 空前缀
    
    int presum = 0, count = 0;
    for (int num : nums) {
        presum += num;
        
        // 找有多少个 j 使得 presum[j] = presum - k
        if (mp.count(presum - k)) {
            count += mp[presum - k];
        }
        
        mp[presum]++;
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

**易错点**：初始化 `mp[0] = 1` 表示和本身等于 k 的情况

---

### 例题 5：四数相加 II

**题目**：LeetCode 454 - 给定四个数组，找出满足 A[i] + B[j] + C[k] + D[l] = 0 的元组数量。

**思路**：将问题拆成两半。用哈希表存储 A+B 的所有可能和，然后枚举 C+D 查找 -(C[k]+D[l]) 的出现次数。

```cpp
#include <bits/stdc++.h>
using namespace std;

int four_sum_count(vector<int>& A, vector<int>& B, 
                   vector<int>& C, vector<int>& D) {
    unordered_map<int, int> mp; // sum -> count
    
    // 统计 A[i] + B[j] 的所有可能
    for (int a : A) {
        for (int b : B) {
            mp[a + b]++;
        }
    }
    
    int count = 0;
    // 枚举 C[k] + D[l]，查找 -(c + d)
    for (int c : C) {
        for (int d : D) {
            int target = -(c + d);
            if (mp.count(target)) {
                count += mp[target];
            }
        }
    }
    
    return count;
}

int main() {
    int n;
    cin >> n;
    
    vector<int> A(n), B(n), C(n), D(n);
    for (int i = 0; i < n; ++i) cin >> A[i];
    for (int i = 0; i < n; ++i) cin >> B[i];
    for (int i = 0; i < n; ++i) cin >> C[i];
    for (int i = 0; i < n; ++i) cin >> D[i];
    
    cout << four_sum_count(A, B, C, D) << "\n";
    
    return 0;
}
```

**复杂度**：时间 O(n²)，空间 O(n²)

**关键思想**：四层循环 O(n⁴) → 分组哈希 O(n²)

---

### 例题 6：第一个只出现一次的字符

**题目**：找出字符串中第一个只出现一次的字符。

```cpp
#include <bits/stdc++.h>
using namespace std;

char first_unique_char(const string& s) {
    unordered_map<char, int> cnt;
    for (char c : s) {
        cnt[c]++;
    }
    
    for (char c : s) {
        if (cnt[c] == 1) {
            return c;
        }
    }
    
    return '\0'; // 没有
}

int main() {
    string s;
    cin >> s;
    
    char result = first_unique_char(s);
    if (result == '\0') {
        cout << "None\n";
    } else {
        cout << result << "\n";
    }
    
    return 0;
}
```

**复杂度**：时间 O(n)，空间 O(字符集大小)

---

## 常见陷阱

1. **`mp[key]` 会插入默认值**：判断存在性用 `count` 或 `find`
2. **哈希冲突**：竞赛中一般不会刻意卡哈希，但极端情况下 `unordered_map` 会退化到 O(n)
3. **自定义 key**：
   - `pair<int, int>` 在 C++11 后可直接作为 key
   - 自定义结构体需要定义 `hash` 和 `==`
4. **迭代器失效**：遍历过程中修改 map/set 可能导致迭代器失效
5. **数据范围**：如果 key 是整数且范围小（如 ≤10⁶），用数组更快

## 优化技巧

### 用数组替代哈希表

当 key 范围小且连续时：

```cpp
// 字符统计
int cnt[26] = {0};
for (char c : s) {
    cnt[c - 'a']++;
}

// 整数范围 [0, 1e6)
int cnt[1000005] = {0};
```

### 离线处理：坐标离散化

当坐标值域大但数量少时：

```cpp
vector<int> vals = coords; // 复制一份
sort(vals.begin(), vals.end());
vals.erase(unique(vals.begin(), vals.end()), vals.end());

// 映射到 [0, vals.size())
for (int& x : coords) {
    x = lower_bound(vals.begin(), vals.end(), x) - vals.begin();
}
```
