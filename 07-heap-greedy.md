# 堆与贪心

## 什么时候用

看到以下特征优先考虑堆和贪心：
- **动态维护最值**：第 K 大/小元素、中位数
- **多路归并**：合并 K 个有序链表/数组
- **任务调度**：最少会议室、CPU 任务安排
- **哈夫曼编码**：合并代价最小
- **区间问题**：区间覆盖、区间调度
- 题目中出现"最多"、"最少"、"最优"等字眼，且局部最优能推出全局最优

核心思路：**贪心选择当前最优解，堆高效维护动态最值**。

## 核心模板

### 优先队列（大根堆）

```cpp
priority_queue<int> maxHeap;           // 大根堆
priority_queue<int, vector<int>, greater<int>> minHeap;  // 小根堆

maxHeap.push(x);
int top = maxHeap.top();
maxHeap.pop();
```

### 自定义比较

```cpp
struct Node {
    int val, idx;
    bool operator<(const Node& o) const {
        return val > o.val;  // 注意：小根堆要用 >
    }
};

priority_queue<Node> pq;
```

### 贪心区间调度模板

```cpp
// 按结束时间排序
sort(intervals.begin(), intervals.end(), [](auto& a, auto& b) {
    return a[1] < b[1];
});

int count = 0, end = INT_MIN;
for (auto& interval : intervals) {
    if (interval[0] >= end) {
        count++;
        end = interval[1];
    }
}
```

## 例题演示

### 例题 1：数据流中的第 K 大元素

**题目**：设计一个类，支持添加元素和查询当前第 K 大元素。

**思路**：维护大小为 K 的小根堆，堆顶就是第 K 大。

```cpp
#include <bits/stdc++.h>
using namespace std;

class KthLargest {
private:
    priority_queue<int, vector<int>, greater<int>> minHeap;
    int k;
    
public:
    KthLargest(int k, vector<int>& nums) : k(k) {
        for (int num : nums) {
            add(num);
        }
    }
    
    int add(int val) {
        minHeap.push(val);
        if (minHeap.size() > k) {
            minHeap.pop();
        }
        return minHeap.top();
    }
};

int main() {
    int k, n;
    cin >> k >> n;
    
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    
    KthLargest kthLargest(k, nums);
    
    int m;
    cin >> m;
    for (int i = 0; i < m; ++i) {
        int val;
        cin >> val;
        cout << kthLargest.add(val) << "\n";
    }
    
    return 0;
}
```

**复杂度**：每次 add 操作 `O(log k)`

**易错点**：
- 堆大小超过 K 时要弹出最小的
- 堆顶是第 K 大，不是最大

---

### 例题 2：合并 K 个有序链表

**题目**：给定 K 个有序链表，合并成一个有序链表。

**思路**：用小根堆维护 K 个链表的当前节点，每次取最小的。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x) : val(x), next(nullptr) {}
};

struct Compare {
    bool operator()(ListNode* a, ListNode* b) {
        return a->val > b->val;  // 小根堆
    }
};

ListNode* mergeKLists(vector<ListNode*>& lists) {
    priority_queue<ListNode*, vector<ListNode*>, Compare> pq;
    
    // 将每个链表的头节点加入堆
    for (ListNode* head : lists) {
        if (head) pq.push(head);
    }
    
    ListNode dummy(0);
    ListNode* tail = &dummy;
    
    while (!pq.empty()) {
        ListNode* node = pq.top();
        pq.pop();
        
        tail->next = node;
        tail = tail->next;
        
        if (node->next) {
            pq.push(node->next);
        }
    }
    
    return dummy.next;
}

int main() {
    int k;
    cin >> k;
    
    vector<ListNode*> lists(k);
    for (int i = 0; i < k; ++i) {
        int n;
        cin >> n;
        
        ListNode dummy(0);
        ListNode* tail = &dummy;
        
        for (int j = 0; j < n; ++j) {
            int val;
            cin >> val;
            tail->next = new ListNode(val);
            tail = tail->next;
        }
        
        lists[i] = dummy.next;
    }
    
    ListNode* result = mergeKLists(lists);
    
    while (result) {
        cout << result->val << " ";
        result = result->next;
    }
    cout << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(N log k)`，N 是总节点数，k 是链表数

**易错点**：
- 堆中存储指针，比较时用节点的值
- 取出节点后，如果有 next 要加入堆

---

### 例题 3：会议室 II（最少会议室数量）

**题目**：给定会议时间区间，求最少需要多少个会议室。

**思路**：按开始时间排序，用小根堆维护每个会议室的结束时间。

```cpp
#include <bits/stdc++.h>
using namespace std;

int minMeetingRooms(vector<vector<int>>& intervals) {
    if (intervals.empty()) return 0;
    
    // 按开始时间排序
    sort(intervals.begin(), intervals.end());
    
    // 小根堆，存储每个会议室的结束时间
    priority_queue<int, vector<int>, greater<int>> pq;
    
    for (auto& interval : intervals) {
        int start = interval[0], end = interval[1];
        
        // 如果最早结束的会议室已经结束，可以复用
        if (!pq.empty() && pq.top() <= start) {
            pq.pop();
        }
        
        pq.push(end);
    }
    
    return pq.size();
}

int main() {
    int n;
    cin >> n;
    
    vector<vector<int>> intervals(n, vector<int>(2));
    for (int i = 0; i < n; ++i) {
        cin >> intervals[i][0] >> intervals[i][1];
    }
    
    cout << minMeetingRooms(intervals) << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(n log n)`

**易错点**：
- 按开始时间排序，而不是结束时间
- 能复用会议室时要先 pop 再 push

---

### 例题 4：哈夫曼编码（最小合并代价）

**题目**：给定 n 个数，每次可以选两个数合并，代价是两数之和，求最小总代价。

**思路**：贪心，每次选最小的两个合并。

```cpp
#include <bits/stdc++.h>
using namespace std;

long long minCost(vector<int>& nums) {
    priority_queue<long long, vector<long long>, greater<long long>> pq;
    
    for (int num : nums) {
        pq.push(num);
    }
    
    long long totalCost = 0;
    
    while (pq.size() > 1) {
        long long first = pq.top(); pq.pop();
        long long second = pq.top(); pq.pop();
        
        long long cost = first + second;
        totalCost += cost;
        
        pq.push(cost);
    }
    
    return totalCost;
}

int main() {
    int n;
    cin >> n;
    
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    
    cout << minCost(nums) << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(n log n)`

**易错点**：
- 用 long long 防止溢出
- 合并后的结果要放回堆中

---

### 例题 5：无重叠区间（最多保留多少区间）

**题目**：给定区间集合，移除最少的区间使得剩余区间不重叠。

**思路**：按结束时间排序，贪心选择结束最早的。

```cpp
#include <bits/stdc++.h>
using namespace std;

int eraseOverlapIntervals(vector<vector<int>>& intervals) {
    if (intervals.empty()) return 0;
    
    // 按结束时间排序
    sort(intervals.begin(), intervals.end(), [](auto& a, auto& b) {
        return a[1] < b[1];
    });
    
    int count = 1;  // 至少保留第一个
    int end = intervals[0][1];
    
    for (int i = 1; i < intervals.size(); ++i) {
        if (intervals[i][0] >= end) {
            count++;
            end = intervals[i][1];
        }
    }
    
    return intervals.size() - count;
}

int main() {
    int n;
    cin >> n;
    
    vector<vector<int>> intervals(n, vector<int>(2));
    for (int i = 0; i < n; ++i) {
        cin >> intervals[i][0] >> intervals[i][1];
    }
    
    cout << eraseOverlapIntervals(intervals) << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(n log n)`

**易错点**：
- 必须按结束时间排序，不能按开始时间
- 判断不重叠：`start >= end`，注意等号

---

### 例题 6：跳跃游戏 II（最少跳跃次数）

**题目**：给定数组，每个位置的值表示最大跳跃距离，求到达最后位置的最少跳跃次数。

**思路**：贪心，每次在当前能到达的范围内选择能跳得最远的位置。

```cpp
#include <bits/stdc++.h>
using namespace std;

int jump(vector<int>& nums) {
    int n = nums.size();
    int jumps = 0;
    int currentEnd = 0;
    int farthest = 0;
    
    for (int i = 0; i < n - 1; ++i) {
        farthest = max(farthest, i + nums[i]);
        
        if (i == currentEnd) {
            jumps++;
            currentEnd = farthest;
            
            if (currentEnd >= n - 1) break;
        }
    }
    
    return jumps;
}

int main() {
    int n;
    cin >> n;
    
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    
    cout << jump(nums) << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(n)`

**易错点**：
- 循环到 n-1 而不是 n，因为已经在最后不需要跳
- 每次到达 currentEnd 才跳跃

---

### 例题 7：数据流的中位数

**题目**：设计数据结构，支持添加数字和查询当前中位数。

**思路**：用两个堆，大根堆存较小的一半，小根堆存较大的一半。

```cpp
#include <bits/stdc++.h>
using namespace std;

class MedianFinder {
private:
    priority_queue<int> maxHeap;  // 存较小的一半
    priority_queue<int, vector<int>, greater<int>> minHeap;  // 存较大的一半
    
public:
    void addNum(int num) {
        if (maxHeap.empty() || num <= maxHeap.top()) {
            maxHeap.push(num);
        } else {
            minHeap.push(num);
        }
        
        // 平衡两个堆的大小
        if (maxHeap.size() > minHeap.size() + 1) {
            minHeap.push(maxHeap.top());
            maxHeap.pop();
        } else if (minHeap.size() > maxHeap.size()) {
            maxHeap.push(minHeap.top());
            minHeap.pop();
        }
    }
    
    double findMedian() {
        if (maxHeap.size() == minHeap.size()) {
            return (maxHeap.top() + minHeap.top()) / 2.0;
        } else {
            return maxHeap.top();
        }
    }
};

int main() {
    MedianFinder mf;
    int n;
    cin >> n;
    
    for (int i = 0; i < n; ++i) {
        string op;
        cin >> op;
        
        if (op == "add") {
            int num;
            cin >> num;
            mf.addNum(num);
        } else {
            cout << fixed << setprecision(1) << mf.findMedian() << "\n";
        }
    }
    
    return 0;
}
```

**复杂度**：添加 `O(log n)`，查询 `O(1)`

**易错点**：
- 大根堆存较小的数，小根堆存较大的数
- 大根堆大小等于或比小根堆大 1
- 中位数：大小相等取平均，否则取大根堆堆顶

---

### 例题 8：任务调度器（CPU 冷却时间）

**题目**：给定任务数组和冷却时间 n，相同任务之间至少间隔 n，求最少时间。

**思路**：贪心，优先执行剩余次数最多的任务。

```cpp
#include <bits/stdc++.h>
using namespace std;

int leastInterval(vector<char>& tasks, int n) {
    unordered_map<char, int> count;
    for (char task : tasks) {
        count[task]++;
    }
    
    priority_queue<int> pq;
    for (auto& [task, cnt] : count) {
        pq.push(cnt);
    }
    
    int time = 0;
    
    while (!pq.empty()) {
        vector<int> temp;
        
        // 执行 n+1 个时间单位
        for (int i = 0; i <= n; ++i) {
            if (!pq.empty()) {
                int cnt = pq.top();
                pq.pop();
                
                if (cnt > 1) {
                    temp.push_back(cnt - 1);
                }
            }
            
            time++;
            
            // 如果所有任务都完成了，提前结束
            if (pq.empty() && temp.empty()) {
                break;
            }
        }
        
        for (int cnt : temp) {
            pq.push(cnt);
        }
    }
    
    return time;
}

int main() {
    int m, n;
    cin >> m >> n;
    
    vector<char> tasks(m);
    for (int i = 0; i < m; ++i) {
        cin >> tasks[i];
    }
    
    cout << leastInterval(tasks, n) << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(m)` 其中 m 是任务总数

**易错点**：
- 每轮执行 n+1 个任务（包括空闲）
- 执行后剩余次数 > 0 的任务要暂存，下轮放回堆
- 所有任务完成要提前退出

---

## 常见陷阱

1. **堆的比较方向**：
   - 大根堆：`priority_queue<int>`（默认）
   - 小根堆：`priority_queue<int, vector<int>, greater<int>>`
   - 自定义：小根堆用 `>`，大根堆用 `<`

2. **贪心正确性证明**：
   - 反证法：假设最优解不选贪心选择，推出矛盾
   - 交换论证：交换两个元素不会使解变差

3. **区间问题排序**：
   - 区间调度：按结束时间排序
   - 区间覆盖：按开始时间排序
   - 会议室：按开始时间排序

4. **溢出问题**：合并代价、路径和等问题用 `long long`

5. **堆为空判断**：访问 top() 前必须检查

## 适用场景总结

| 问题类型 | 数据结构 | 贪心策略 |
|---------|---------|---------|
| 第 K 大/小 | 堆（大小为 K） | 维护固定大小堆 |
| 多路归并 | 小根堆 | 每次取最小 |
| 会议室调度 | 小根堆 + 排序 | 按开始时间，维护结束时间 |
| 哈夫曼编码 | 小根堆 | 每次合并最小两个 |
| 区间调度 | 排序 | 按结束时间，贪心选择 |
| 区间覆盖 | 排序 | 按开始时间，贪心扩展 |
| 跳跃游戏 | 无 | 贪心选最远位置 |
| 中位数 | 两个堆 | 平衡左右两半 |

**核心技巧**：
- 堆维护动态最值，复杂度 `O(log n)`
- 贪心需要证明局部最优 → 全局最优
- 区间问题：排序 + 贪心是常见套路
- 两个堆可以维护对称的数据结构（如中位数）
