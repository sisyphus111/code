# 高级数据结构

## 什么时候用

看到以下特征优先考虑高级数据结构：
- 区间查询 + 单点修改 → 树状数组
- 区间查询 + 区间修改 → 线段树
- 动态维护有序集合 → set/multiset
- 动态维护区间最值 → 线段树/ST 表
- 前缀和 + 单点修改 → 树状数组
- 逆序对、区间第 k 小 → 树状数组/线段树

核心思路：**用树形结构加速查询和修改操作**。

## 核心要点

1. **树状数组**：适合单点修改 + 区间查询，代码简单
2. **线段树**：适合区间修改 + 区间查询，功能强大
3. **时间复杂度**：修改和查询都是 `O(log n)`
4. **空间复杂度**：树状数组 `O(n)`，线段树 `O(4n)`
5. **下标从 1 开始**：树状数组习惯从 1 开始

## 例题演示

### 例题 1：树状数组 - 区间和查询

**题目**：给定数组，支持单点修改和区间和查询。

**思路**：树状数组维护前缀和，区间和 = `query(r) - query(l-1)`。

```cpp
#include <bits/stdc++.h>
using namespace std;

class BIT {
    vector<int> tree;
    int n;
    
    int lowbit(int x) {
        return x & -x;
    }
    
public:
    BIT(int size) : n(size), tree(size + 1, 0) {}
    
    // 单点修改：给位置 i 加上 delta
    void update(int i, int delta) {
        while (i <= n) {
            tree[i] += delta;
            i += lowbit(i);
        }
    }
    
    // 前缀和查询：[1, i]
    int query(int i) {
        int sum = 0;
        while (i > 0) {
            sum += tree[i];
            i -= lowbit(i);
        }
        return sum;
    }
    
    // 区间和查询：[l, r]
    int range_query(int l, int r) {
        return query(r) - query(l - 1);
    }
};

int main() {
    int n, q;
    cin >> n >> q;
    
    BIT bit(n);
    
    for (int i = 1; i <= n; ++i) {
        int x;
        cin >> x;
        bit.update(i, x);
    }
    
    while (q--) {
        int op;
        cin >> op;
        
        if (op == 1) {
            // 单点修改
            int i, delta;
            cin >> i >> delta;
            bit.update(i, delta);
        } else {
            // 区间查询
            int l, r;
            cin >> l >> r;
            cout << bit.range_query(l, r) << "\n";
        }
    }
    
    return 0;
}
```

**复杂度**：修改和查询都是 `O(log n)`

**易错点**：
- 下标从 1 开始
- `lowbit(x) = x & -x` 是关键
- 修改时向上更新，查询时向下累加

---

### 例题 2：树状数组 - 逆序对

**题目**：给定数组，求逆序对个数（i < j 且 a[i] > a[j]）。

**思路**：从左到右遍历，对于每个元素，查询比它大的元素个数。

```cpp
#include <bits/stdc++.h>
using namespace std;

class BIT {
    vector<int> tree;
    int n;
    
    int lowbit(int x) { return x & -x; }
    
public:
    BIT(int size) : n(size), tree(size + 1, 0) {}
    
    void update(int i, int delta) {
        while (i <= n) {
            tree[i] += delta;
            i += lowbit(i);
        }
    }
    
    int query(int i) {
        int sum = 0;
        while (i > 0) {
            sum += tree[i];
            i -= lowbit(i);
        }
        return sum;
    }
};

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    
    for (int i = 0; i < n; ++i) {
        cin >> a[i];
    }
    
    // 离散化
    vector<int> sorted_a = a;
    sort(sorted_a.begin(), sorted_a.end());
    sorted_a.erase(unique(sorted_a.begin(), sorted_a.end()), sorted_a.end());
    
    for (int& x : a) {
        x = lower_bound(sorted_a.begin(), sorted_a.end(), x) - sorted_a.begin() + 1;
    }
    
    BIT bit(sorted_a.size());
    long long inversions = 0;
    
    for (int i = 0; i < n; ++i) {
        // 查询比 a[i] 大的元素个数
        inversions += bit.query(sorted_a.size()) - bit.query(a[i]);
        bit.update(a[i], 1);
    }
    
    cout << inversions << "\n";
    return 0;
}
```

**复杂度**：时间 `O(n log n)`，空间 `O(n)`

**易错点**：
- 需要离散化处理大范围数值
- 查询时用总数减去前缀和

---

### 例题 3：线段树 - 区间和查询与区间修改

**题目**：支持区间加一个数和区间和查询。

**思路**：线段树 + 懒标记（lazy tag）。

```cpp
#include <bits/stdc++.h>
using namespace std;

class SegmentTree {
    vector<long long> tree, lazy;
    int n;
    
    void push_down(int node, int start, int end) {
        if (lazy[node] == 0) return;
        
        int mid = (start + end) / 2;
        tree[node * 2] += lazy[node] * (mid - start + 1);
        tree[node * 2 + 1] += lazy[node] * (end - mid);
        
        lazy[node * 2] += lazy[node];
        lazy[node * 2 + 1] += lazy[node];
        
        lazy[node] = 0;
    }
    
    void build(vector<int>& arr, int node, int start, int end) {
        if (start == end) {
            tree[node] = arr[start];
            return;
        }
        
        int mid = (start + end) / 2;
        build(arr, node * 2, start, mid);
        build(arr, node * 2 + 1, mid + 1, end);
        tree[node] = tree[node * 2] + tree[node * 2 + 1];
    }
    
    void update_range(int node, int start, int end, int l, int r, int val) {
        if (l > end || r < start) return;
        
        if (l <= start && end <= r) {
            tree[node] += (long long)val * (end - start + 1);
            lazy[node] += val;
            return;
        }
        
        push_down(node, start, end);
        int mid = (start + end) / 2;
        update_range(node * 2, start, mid, l, r, val);
        update_range(node * 2 + 1, mid + 1, end, l, r, val);
        tree[node] = tree[node * 2] + tree[node * 2 + 1];
    }
    
    long long query_range(int node, int start, int end, int l, int r) {
        if (l > end || r < start) return 0;
        
        if (l <= start && end <= r) {
            return tree[node];
        }
        
        push_down(node, start, end);
        int mid = (start + end) / 2;
        return query_range(node * 2, start, mid, l, r) +
               query_range(node * 2 + 1, mid + 1, end, l, r);
    }
    
public:
    SegmentTree(vector<int>& arr) {
        n = arr.size();
        tree.resize(4 * n);
        lazy.resize(4 * n);
        build(arr, 1, 0, n - 1);
    }
    
    void update(int l, int r, int val) {
        update_range(1, 0, n - 1, l, r, val);
    }
    
    long long query(int l, int r) {
        return query_range(1, 0, n - 1, l, r);
    }
};

int main() {
    int n, q;
    cin >> n >> q;
    
    vector<int> arr(n);
    for (int i = 0; i < n; ++i) {
        cin >> arr[i];
    }
    
    SegmentTree seg(arr);
    
    while (q--) {
        int op;
        cin >> op;
        
        if (op == 1) {
            // 区间修改
            int l, r, val;
            cin >> l >> r >> val;
            seg.update(l, r, val);
        } else {
            // 区间查询
            int l, r;
            cin >> l >> r;
            cout << seg.query(l, r) << "\n";
        }
    }
    
    return 0;
}
```

**复杂度**：修改和查询都是 `O(log n)`

**易错点**：
- 懒标记要正确下传
- 区间长度计算：`end - start + 1`
- 树的大小是 `4n`

---

### 例题 4：线段树 - 区间最大值

**题目**：支持单点修改和区间最大值查询。

**思路**：线段树维护区间最大值。

```cpp
#include <bits/stdc++.h>
using namespace std;

class MaxSegmentTree {
    vector<int> tree;
    int n;
    
    void build(vector<int>& arr, int node, int start, int end) {
        if (start == end) {
            tree[node] = arr[start];
            return;
        }
        
        int mid = (start + end) / 2;
        build(arr, node * 2, start, mid);
        build(arr, node * 2 + 1, mid + 1, end);
        tree[node] = max(tree[node * 2], tree[node * 2 + 1]);
    }
    
    void update_point(int node, int start, int end, int idx, int val) {
        if (start == end) {
            tree[node] = val;
            return;
        }
        
        int mid = (start + end) / 2;
        if (idx <= mid) {
            update_point(node * 2, start, mid, idx, val);
        } else {
            update_point(node * 2 + 1, mid + 1, end, idx, val);
        }
        tree[node] = max(tree[node * 2], tree[node * 2 + 1]);
    }
    
    int query_range(int node, int start, int end, int l, int r) {
        if (l > end || r < start) return INT_MIN;
        
        if (l <= start && end <= r) {
            return tree[node];
        }
        
        int mid = (start + end) / 2;
        return max(query_range(node * 2, start, mid, l, r),
                   query_range(node * 2 + 1, mid + 1, end, l, r));
    }
    
public:
    MaxSegmentTree(vector<int>& arr) {
        n = arr.size();
        tree.resize(4 * n);
        build(arr, 1, 0, n - 1);
    }
    
    void update(int idx, int val) {
        update_point(1, 0, n - 1, idx, val);
    }
    
    int query(int l, int r) {
        return query_range(1, 0, n - 1, l, r);
    }
};

int main() {
    int n, q;
    cin >> n >> q;
    
    vector<int> arr(n);
    for (int i = 0; i < n; ++i) {
        cin >> arr[i];
    }
    
    MaxSegmentTree seg(arr);
    
    while (q--) {
        int op;
        cin >> op;
        
        if (op == 1) {
            int idx, val;
            cin >> idx >> val;
            seg.update(idx, val);
        } else {
            int l, r;
            cin >> l >> r;
            cout << seg.query(l, r) << "\n";
        }
    }
    
    return 0;
}
```

**复杂度**：修改和查询都是 `O(log n)`

---

### 例题 5：ST 表 - 静态区间最值查询

**题目**：数组不变，多次查询区间最大值。

**思路**：Sparse Table 预处理，`O(1)` 查询。

```cpp
#include <bits/stdc++.h>
using namespace std;

class SparseTable {
    vector<vector<int>> st;
    vector<int> lg;
    int n;
    
public:
    SparseTable(vector<int>& arr) {
        n = arr.size();
        int max_log = log2(n) + 1;
        st.assign(n, vector<int>(max_log));
        lg.resize(n + 1);
        
        // 预处理 log2
        lg[1] = 0;
        for (int i = 2; i <= n; ++i) {
            lg[i] = lg[i / 2] + 1;
        }
        
        // 初始化长度为 1 的区间
        for (int i = 0; i < n; ++i) {
            st[i][0] = arr[i];
        }
        
        // 动态规划
        for (int j = 1; (1 << j) <= n; ++j) {
            for (int i = 0; i + (1 << j) <= n; ++i) {
                st[i][j] = max(st[i][j - 1], st[i + (1 << (j - 1))][j - 1]);
            }
        }
    }
    
    int query(int l, int r) {
        int len = r - l + 1;
        int k = lg[len];
        return max(st[l][k], st[r - (1 << k) + 1][k]);
    }
};

int main() {
    int n, q;
    cin >> n >> q;
    
    vector<int> arr(n);
    for (int i = 0; i < n; ++i) {
        cin >> arr[i];
    }
    
    SparseTable st(arr);
    
    while (q--) {
        int l, r;
        cin >> l >> r;
        cout << st.query(l, r) << "\n";
    }
    
    return 0;
}
```

**复杂度**：预处理 `O(n log n)`，查询 `O(1)`

**易错点**：只适用于可重复贡献的问题（max、min、gcd），不适用于 sum

---

### 例题 6：单调栈 - 下一个更大元素

**题目**：对每个元素，找到右边第一个比它大的元素。

**思路**：维护单调递减栈。

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> next_greater_element(vector<int>& nums) {
    int n = nums.size();
    vector<int> res(n, -1);
    stack<int> st;  // 存储下标
    
    for (int i = 0; i < n; ++i) {
        while (!st.empty() && nums[st.top()] < nums[i]) {
            res[st.top()] = nums[i];
            st.pop();
        }
        st.push(i);
    }
    
    return res;
}

int main() {
    int n;
    cin >> n;
    vector<int> nums(n);
    
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    
    auto res = next_greater_element(nums);
    
    for (int x : res) {
        cout << x << " ";
    }
    cout << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(n)`，空间 `O(n)`

**易错点**：栈中存下标而非值，方便记录位置

---

### 例题 7：单调队列 - 滑动窗口最大值

**题目**：给定数组和窗口大小 k，求每个窗口的最大值。

**思路**：维护单调递减队列。

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> max_sliding_window(vector<int>& nums, int k) {
    vector<int> res;
    deque<int> dq;  // 存储下标
    
    for (int i = 0; i < nums.size(); ++i) {
        // 移除超出窗口的元素
        if (!dq.empty() && dq.front() < i - k + 1) {
            dq.pop_front();
        }
        
        // 移除所有比当前元素小的元素
        while (!dq.empty() && nums[dq.back()] < nums[i]) {
            dq.pop_back();
        }
        
        dq.push_back(i);
        
        // 窗口形成后开始记录结果
        if (i >= k - 1) {
            res.push_back(nums[dq.front()]);
        }
    }
    
    return res;
}

int main() {
    int n, k;
    cin >> n >> k;
    
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    
    auto res = max_sliding_window(nums, k);
    
    for (int x : res) {
        cout << x << " ";
    }
    cout << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(n)`，空间 `O(k)`

**易错点**：队头可能超出窗口，需要及时移除

---

### 例题 8：并查集 - 连通性判断

**题目**：给定 n 个节点，支持合并两个节点和查询是否连通。

**思路**：并查集 + 路径压缩 + 按秩合并。

```cpp
#include <bits/stdc++.h>
using namespace std;

class UnionFind {
    vector<int> parent, rank;
    
public:
    UnionFind(int n) {
        parent.resize(n);
        rank.resize(n, 1);
        for (int i = 0; i < n; ++i) {
            parent[i] = i;
        }
    }
    
    int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);  // 路径压缩
        }
        return parent[x];
    }
    
    bool unite(int x, int y) {
        int root_x = find(x);
        int root_y = find(y);
        
        if (root_x == root_y) return false;
        
        // 按秩合并
        if (rank[root_x] < rank[root_y]) {
            parent[root_x] = root_y;
        } else if (rank[root_x] > rank[root_y]) {
            parent[root_y] = root_x;
        } else {
            parent[root_y] = root_x;
            rank[root_x]++;
        }
        
        return true;
    }
    
    bool connected(int x, int y) {
        return find(x) == find(y);
    }
};

int main() {
    int n, q;
    cin >> n >> q;
    
    UnionFind uf(n);
    
    while (q--) {
        int op, x, y;
        cin >> op >> x >> y;
        
        if (op == 1) {
            uf.unite(x, y);
        } else {
            cout << (uf.connected(x, y) ? "YES" : "NO") << "\n";
        }
    }
    
    return 0;
}
```

**复杂度**：接近 `O(1)` 的均摊时间

**易错点**：`find` 中要进行路径压缩

---

## 常见陷阱

1. **树状数组下标**：习惯从 1 开始，注意转换
2. **线段树空间**：需要 `4n` 大小
3. **懒标记**：区间修改必须用懒标记，否则超时
4. **离散化**：值域过大时要先离散化
5. **单调栈/队列**：栈中存下标而非值
6. **并查集路径压缩**：`find` 中要压缩，不能只是返回
7. **区间边界**：注意是 `[l, r]` 还是 `[l, r)`

## 数据结构选择

| 需求 | 数据结构 | 时间复杂度 |
|------|---------|-----------|
| 单点修改 + 区间查询 | 树状数组 | `O(log n)` |
| 区间修改 + 区间查询 | 线段树 | `O(log n)` |
| 静态区间最值 | ST 表 | 预处理 `O(n log n)`，查询 `O(1)` |
| 滑动窗口最值 | 单调队列 | `O(n)` |
| 下一个更大/更小 | 单调栈 | `O(n)` |
| 动态连通性 | 并查集 | 接近 `O(1)` |

## 适用场景总结

- **树状数组**：前缀和、逆序对、区间统计
- **线段树**：区间最值、区间和、懒标记
- **ST 表**：静态 RMQ（区间最值查询）
- **单调栈**：下一个更大/更小元素
- **单调队列**：滑动窗口最值
- **并查集**：动态连通性、最小生成树
