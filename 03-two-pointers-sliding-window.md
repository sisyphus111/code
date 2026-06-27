# 双指针与滑动窗口

## 什么时候用

看到以下特征优先考虑双指针：
- **连续子数组/子串**问题
- **有序数组**的两数之和、三数之和
- 最长/最短满足某条件的区间
- 去重、原地修改数组
- 链表相关：快慢指针、相交、环检测

核心思路：**用 O(n) 或 O(n²) 替代 O(n²) 或 O(n³) 的暴力枚举**。

## 双指针分类

### 对撞指针

两个指针从两端向中间移动，常用于**有序数组**。

```cpp
int left = 0, right = n - 1;
while (left < right) {
    if (满足条件) {
        // 记录答案
        left++; // 或 right--
    } else if (需要增大) {
        left++;
    } else {
        right--;
    }
}
```

### 快慢指针

两个指针同向移动，速度不同，常用于**链表**和**原地修改**。

```cpp
int slow = 0;
for (int fast = 0; fast < n; ++fast) {
    if (满足保留条件) {
        arr[slow++] = arr[fast];
    }
}
// slow 是新数组长度
```

### 滑动窗口

两个指针维护一个动态区间，常用于**连续子数组/子串**。

```cpp
int left = 0;
for (int right = 0; right < n; ++right) {
    // 扩展右边界，加入 arr[right]
    window_add(arr[right]);
    
    // 收缩左边界直到满足条件
    while (窗口不满足条件) {
        window_remove(arr[left]);
        left++;
    }
    
    // 更新答案
    ans = max(ans, right - left + 1);
}
```

## 例题演示

### 例题 1：两数之和 II（有序数组）

**题目**：LeetCode 167 - 给定**有序数组**和目标值，找出两个数的索引使得它们相加等于目标值。

**思路**：对撞指针，如果和太小则左指针右移，太大则右指针左移。

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> two_sum(vector<int>& nums, int target) {
    int left = 0, right = nums.size() - 1;
    
    while (left < right) {
        int sum = nums[left] + nums[right];
        if (sum == target) {
            return {left + 1, right + 1}; // 1-indexed
        } else if (sum < target) {
            left++;
        } else {
            right--;
        }
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
    cout << res[0] << " " << res[1] << "\n";
    
    return 0;
}
```

**复杂度**：时间 O(n)，空间 O(1)

**关键点**：利用有序性，和太小/太大决定移动方向

---

### 例题 2：三数之和

**题目**：LeetCode 15 - 找出数组中所有和为 0 的不重复三元组。

**思路**：先排序，固定第一个数，对剩余部分用对撞指针找两数之和。

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<vector<int>> three_sum(vector<int>& nums) {
    vector<vector<int>> result;
    int n = nums.size();
    if (n < 3) return result;
    
    sort(nums.begin(), nums.end());
    
    for (int i = 0; i < n - 2; ++i) {
        // 跳过重复的第一个数
        if (i > 0 && nums[i] == nums[i - 1]) continue;
        
        // 剪枝：最小的三个数之和 > 0
        if (nums[i] + nums[i + 1] + nums[i + 2] > 0) break;
        
        // 剪枝：当前数 + 最大的两个数 < 0
        if (nums[i] + nums[n - 2] + nums[n - 1] < 0) continue;
        
        int target = -nums[i];
        int left = i + 1, right = n - 1;
        
        while (left < right) {
            int sum = nums[left] + nums[right];
            if (sum == target) {
                result.push_back({nums[i], nums[left], nums[right]});
                
                // 跳过重复
                while (left < right && nums[left] == nums[left + 1]) left++;
                while (left < right && nums[right] == nums[right - 1]) right--;
                
                left++;
                right--;
            } else if (sum < target) {
                left++;
            } else {
                right--;
            }
        }
    }
    
    return result;
}

int main() {
    int n;
    cin >> n;
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    
    auto result = three_sum(nums);
    
    cout << result.size() << "\n";
    for (const auto& triplet : result) {
        cout << triplet[0] << " " << triplet[1] << " " << triplet[2] << "\n";
    }
    
    return 0;
}
```

**复杂度**：时间 O(n²)，空间 O(1)（不计结果）

**易错点**：
- 去重要在正确位置：`i > 0` 而不是 `i > 1`
- 找到结果后两个指针都要移动

---

### 例题 3：盛水最多的容器

**题目**：LeetCode 11 - 给定数组表示高度，找两条线与 x 轴构成的容器能盛最多的水。

**思路**：对撞指针，每次移动较短的那一边（移动长的不可能更优）。

```cpp
#include <bits/stdc++.h>
using namespace std;

int max_area(vector<int>& height) {
    int left = 0, right = height.size() - 1;
    int max_water = 0;
    
    while (left < right) {
        int h = min(height[left], height[right]);
        int w = right - left;
        max_water = max(max_water, h * w);
        
        // 移动较短的一边
        if (height[left] < height[right]) {
            left++;
        } else {
            right--;
        }
    }
    
    return max_water;
}

int main() {
    int n;
    cin >> n;
    vector<int> height(n);
    for (int i = 0; i < n; ++i) {
        cin >> height[i];
    }
    
    cout << max_area(height) << "\n";
    
    return 0;
}
```

**复杂度**：时间 O(n)，空间 O(1)

**证明**：移动长边只会让宽度减小且高度不增，一定更差

---

### 例题 4：删除有序数组中的重复项

**题目**：LeetCode 26 - 原地删除有序数组中的重复项，返回新长度。

**思路**：快慢指针，`slow` 指向不重复部分的末尾。

```cpp
#include <bits/stdc++.h>
using namespace std;

int remove_duplicates(vector<int>& nums) {
    if (nums.empty()) return 0;
    
    int slow = 0;
    for (int fast = 1; fast < (int)nums.size(); ++fast) {
        if (nums[fast] != nums[slow]) {
            slow++;
            nums[slow] = nums[fast];
        }
    }
    
    return slow + 1;
}

int main() {
    int n;
    cin >> n;
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    
    int len = remove_duplicates(nums);
    
    cout << len << "\n";
    for (int i = 0; i < len; ++i) {
        cout << nums[i] << " \n"[i == len - 1];
    }
    
    return 0;
}
```

**复杂度**：时间 O(n)，空间 O(1)

---

### 例题 5：长度最小的子数组（滑动窗口）

**题目**：LeetCode 209 - 找出数组中和 ≥ target 的最短连续子数组。

**思路**：滑动窗口，右指针扩展累加和，当满足条件时收缩左指针。

```cpp
#include <bits/stdc++.h>
using namespace std;

int min_subarray_len(int target, vector<int>& nums) {
    int n = nums.size();
    int left = 0, sum = 0;
    int min_len = INT_MAX;
    
    for (int right = 0; right < n; ++right) {
        sum += nums[right];
        
        // 当满足条件时尽量收缩
        while (sum >= target) {
            min_len = min(min_len, right - left + 1);
            sum -= nums[left];
            left++;
        }
    }
    
    return min_len == INT_MAX ? 0 : min_len;
}

int main() {
    int n, target;
    cin >> n >> target;
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    
    cout << min_subarray_len(target, nums) << "\n";
    
    return 0;
}
```

**复杂度**：时间 O(n)，空间 O(1)

**关键点**：每个元素最多被访问两次（一次加入，一次移出）

---

### 例题 6：无重复字符的最长子串

**题目**：LeetCode 3 - 找出字符串中无重复字符的最长子串长度。

**思路**：滑动窗口 + 哈希表记录字符最后出现位置。

```cpp
#include <bits/stdc++.h>
using namespace std;

int length_of_longest_substring(string s) {
    unordered_map<char, int> last_pos; // 字符 -> 最后出现位置
    int max_len = 0;
    int left = 0;
    
    for (int right = 0; right < (int)s.size(); ++right) {
        char c = s[right];
        
        // 如果字符重复，更新左边界
        if (last_pos.count(c) && last_pos[c] >= left) {
            left = last_pos[c] + 1;
        }
        
        last_pos[c] = right;
        max_len = max(max_len, right - left + 1);
    }
    
    return max_len;
}

int main() {
    string s;
    cin >> s;
    cout << length_of_longest_substring(s) << "\n";
    return 0;
}
```

**复杂度**：时间 O(n)，空间 O(字符集大小)

**另一种写法**（用集合 + while 收缩）：

```cpp
int length_of_longest_substring(string s) {
    unordered_set<char> window;
    int max_len = 0;
    int left = 0;
    
    for (int right = 0; right < (int)s.size(); ++right) {
        while (window.count(s[right])) {
            window.erase(s[left]);
            left++;
        }
        window.insert(s[right]);
        max_len = max(max_len, right - left + 1);
    }
    
    return max_len;
}
```

---

### 例题 7：字符串的排列（滑动窗口 + 计数）

**题目**：LeetCode 567 - 判断 s2 是否包含 s1 的排列。

**思路**：固定长度的滑动窗口，维护字符频次。

```cpp
#include <bits/stdc++.h>
using namespace std;

bool check_inclusion(string s1, string s2) {
    if (s1.size() > s2.size()) return false;
    
    int cnt1[26] = {0}, cnt2[26] = {0};
    
    // 统计 s1 的字符频次
    for (char c : s1) {
        cnt1[c - 'a']++;
    }
    
    int k = s1.size();
    
    // 初始化窗口
    for (int i = 0; i < k; ++i) {
        cnt2[s2[i] - 'a']++;
    }
    
    if (memcmp(cnt1, cnt2, sizeof(cnt1)) == 0) return true;
    
    // 滑动窗口
    for (int i = k; i < (int)s2.size(); ++i) {
        cnt2[s2[i] - 'a']++;           // 加入右边
        cnt2[s2[i - k] - 'a']--;       // 移出左边
        
        if (memcmp(cnt1, cnt2, sizeof(cnt1)) == 0) return true;
    }
    
    return false;
}

int main() {
    string s1, s2;
    cin >> s1 >> s2;
    cout << (check_inclusion(s1, s2) ? "YES" : "NO") << "\n";
    return 0;
}
```

**复杂度**：时间 O(n)，空间 O(1)

**优化**：用一个变量记录匹配字符种类数，避免每次比较整个数组

---

### 例题 8：最小覆盖子串

**题目**：LeetCode 76 - 找出 s 中包含 t 所有字符的最小子串。

**思路**：滑动窗口 + 计数，维护窗口内字符频次。

```cpp
#include <bits/stdc++.h>
using namespace std;

string min_window(string s, string t) {
    if (s.empty() || t.empty()) return "";
    
    unordered_map<char, int> need, window;
    for (char c : t) need[c]++;
    
    int left = 0, right = 0;
    int valid = 0; // 已满足的字符种类数
    int start = 0, min_len = INT_MAX;
    
    while (right < (int)s.size()) {
        char c = s[right];
        right++;
        
        // 扩展窗口
        if (need.count(c)) {
            window[c]++;
            if (window[c] == need[c]) {
                valid++;
            }
        }
        
        // 收缩窗口
        while (valid == (int)need.size()) {
            // 更新答案
            if (right - left < min_len) {
                start = left;
                min_len = right - left;
            }
            
            char d = s[left];
            left++;
            
            if (need.count(d)) {
                if (window[d] == need[d]) {
                    valid--;
                }
                window[d]--;
            }
        }
    }
    
    return min_len == INT_MAX ? "" : s.substr(start, min_len);
}

int main() {
    string s, t;
    cin >> s >> t;
    cout << min_window(s, t) << "\n";
    return 0;
}
```

**复杂度**：时间 O(n + m)，空间 O(字符集大小)

**关键点**：用 `valid` 变量优化判断，避免每次遍历 need

---

## 滑动窗口模板

### 最长满足条件窗口

```cpp
int left = 0, ans = 0;
for (int right = 0; right < n; ++right) {
    // 加入 arr[right]
    window_add(arr[right]);
    
    // 收缩直到满足条件
    while (窗口不满足条件) {
        window_remove(arr[left]);
        left++;
    }
    
    ans = max(ans, right - left + 1);
}
```

### 最短满足条件窗口

```cpp
int left = 0, ans = INT_MAX;
for (int right = 0; right < n; ++right) {
    // 加入 arr[right]
    window_add(arr[right]);
    
    // 收缩直到不满足条件
    while (窗口满足条件) {
        ans = min(ans, right - left + 1);
        window_remove(arr[left]);
        left++;
    }
}
```

## 常见陷阱

1. **边界条件**：空数组、单元素、全部相同
2. **重复处理**：三数之和的去重逻辑要写对
3. **指针移动时机**：先更新答案还是先移动指针
4. **窗口状态维护**：加入/移出元素时要同步更新状态
5. **整数溢出**：对撞指针求和时注意溢出

## 适用场景总结

| 模式 | 适用场景 | 复杂度 |
|------|----------|--------|
| 对撞指针 | 有序数组、两数之和、三数之和、容器问题 | O(n) 或 O(n²) |
| 快慢指针 | 链表环检测、原地去重、数组分区 | O(n) |
| 滑动窗口 | 连续子数组/子串、最长/最短满足条件 | O(n) |
