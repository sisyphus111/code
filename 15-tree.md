# 树

## 什么时候用

看到以下特征优先考虑树算法：
- 题目明确提到"树"、"二叉树"、"父子节点"
- 层次结构、递归结构的数据
- 求路径、深度、祖先、子树
- 前序/中序/后序遍历
- 树的直径、重心、最近公共祖先

核心思路：**递归思维 + DFS/BFS 遍历 + 分治思想**。

## 核心要点

1. **树的定义**：n 个节点，n-1 条边，连通无环
2. **遍历方式**：前序、中序、后序、层序
3. **递归三要素**：终止条件、递归逻辑、返回值
4. **DFS vs BFS**：深度优先用递归/栈，广度优先用队列
5. **树形 DP**：从子树信息推导当前节点信息

## 树的表示

### 邻接表（常用）

```cpp
vector<vector<int>> tree(n + 1);
tree[u].push_back(v);
tree[v].push_back(u);
```

### 结构体（二叉树）

```cpp
struct TreeNode {
    int val;
    TreeNode *left, *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};
```

## 例题演示

### 例题 1：二叉树的前序/中序/后序遍历

**题目**：给定二叉树，输出前序、中序、后序遍历结果。

**思路**：
- 前序：根 → 左 → 右
- 中序：左 → 根 → 右
- 后序：左 → 右 → 根

```cpp
#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left, *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

// 前序遍历
void preorder(TreeNode* root, vector<int>& res) {
    if (!root) return;
    res.push_back(root->val);
    preorder(root->left, res);
    preorder(root->right, res);
}

// 中序遍历
void inorder(TreeNode* root, vector<int>& res) {
    if (!root) return;
    inorder(root->left, res);
    res.push_back(root->val);
    inorder(root->right, res);
}

// 后序遍历
void postorder(TreeNode* root, vector<int>& res) {
    if (!root) return;
    postorder(root->left, res);
    postorder(root->right, res);
    res.push_back(root->val);
}

// 迭代版本 - 前序遍历
vector<int> preorder_iterative(TreeNode* root) {
    vector<int> res;
    if (!root) return res;
    
    stack<TreeNode*> st;
    st.push(root);
    
    while (!st.empty()) {
        TreeNode* node = st.top();
        st.pop();
        res.push_back(node->val);
        
        // 先右后左，因为栈是后进先出
        if (node->right) st.push(node->right);
        if (node->left) st.push(node->left);
    }
    
    return res;
}

// 迭代版本 - 中序遍历
vector<int> inorder_iterative(TreeNode* root) {
    vector<int> res;
    stack<TreeNode*> st;
    TreeNode* cur = root;
    
    while (cur || !st.empty()) {
        while (cur) {
            st.push(cur);
            cur = cur->left;
        }
        cur = st.top();
        st.pop();
        res.push_back(cur->val);
        cur = cur->right;
    }
    
    return res;
}

int main() {
    // 构建示例树
    TreeNode* root = new TreeNode(1);
    root->left = new TreeNode(2);
    root->right = new TreeNode(3);
    root->left->left = new TreeNode(4);
    root->left->right = new TreeNode(5);
    
    vector<int> pre, in, post;
    preorder(root, pre);
    inorder(root, in);
    postorder(root, post);
    
    cout << "前序: ";
    for (int x : pre) cout << x << " ";
    cout << "\n";
    
    cout << "中序: ";
    for (int x : in) cout << x << " ";
    cout << "\n";
    
    cout << "后序: ";
    for (int x : post) cout << x << " ";
    cout << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(n)`，空间 `O(h)` - h 是树高

**易错点**：迭代中序遍历要注意先走到最左，再处理当前节点

---

### 例题 2：层序遍历（BFS）

**题目**：按层输出二叉树节点。

**思路**：用队列进行 BFS。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left, *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

vector<vector<int>> level_order(TreeNode* root) {
    vector<vector<int>> res;
    if (!root) return res;
    
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
        
        res.push_back(level);
    }
    
    return res;
}

int main() {
    TreeNode* root = new TreeNode(3);
    root->left = new TreeNode(9);
    root->right = new TreeNode(20);
    root->right->left = new TreeNode(15);
    root->right->right = new TreeNode(7);
    
    auto levels = level_order(root);
    
    for (const auto& level : levels) {
        for (int val : level) {
            cout << val << " ";
        }
        cout << "\n";
    }
    
    return 0;
}
```

**复杂度**：时间 `O(n)`，空间 `O(n)`

**易错点**：要先记录当前层的大小，再遍历

---

### 例题 3：二叉树的最大深度

**题目**：求二叉树的最大深度。

**思路**：递归，深度 = max(左子树深度, 右子树深度) + 1。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left, *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

int max_depth(TreeNode* root) {
    if (!root) return 0;
    return max(max_depth(root->left), max_depth(root->right)) + 1;
}

int main() {
    TreeNode* root = new TreeNode(3);
    root->left = new TreeNode(9);
    root->right = new TreeNode(20);
    root->right->left = new TreeNode(15);
    root->right->right = new TreeNode(7);
    
    cout << max_depth(root) << "\n";  // 输出 3
    return 0;
}
```

**复杂度**：时间 `O(n)`，空间 `O(h)`

---

### 例题 4：树的直径

**题目**：树的直径是任意两节点间最长路径的边数。

**思路**：对每个节点，直径可能经过它（左子树最大深度 + 右子树最大深度），递归更新答案。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left, *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
    int diameter = 0;
    
    int depth(TreeNode* root) {
        if (!root) return 0;
        
        int left = depth(root->left);
        int right = depth(root->right);
        
        // 更新直径：经过当前节点的最长路径
        diameter = max(diameter, left + right);
        
        // 返回当前节点的深度
        return max(left, right) + 1;
    }
    
public:
    int diameter_of_binary_tree(TreeNode* root) {
        depth(root);
        return diameter;
    }
};

int main() {
    TreeNode* root = new TreeNode(1);
    root->left = new TreeNode(2);
    root->right = new TreeNode(3);
    root->left->left = new TreeNode(4);
    root->left->right = new TreeNode(5);
    
    Solution sol;
    cout << sol.diameter_of_binary_tree(root) << "\n";  // 输出 3
    return 0;
}
```

**复杂度**：时间 `O(n)`，空间 `O(h)`

**易错点**：直径不一定经过根节点，需要全局变量记录

---

### 例题 5：最近公共祖先 LCA

**题目**：给定二叉树和两个节点 p、q，找它们的最近公共祖先。

**思路**：递归，如果当前节点是 p 或 q，返回当前节点；如果左右子树都找到，当前节点就是 LCA。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left, *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

TreeNode* lowest_common_ancestor(TreeNode* root, TreeNode* p, TreeNode* q) {
    if (!root || root == p || root == q) return root;
    
    TreeNode* left = lowest_common_ancestor(root->left, p, q);
    TreeNode* right = lowest_common_ancestor(root->right, p, q);
    
    if (left && right) return root;  // 两边都找到，当前节点是 LCA
    return left ? left : right;      // 只有一边找到，返回那一边
}

int main() {
    TreeNode* root = new TreeNode(3);
    root->left = new TreeNode(5);
    root->right = new TreeNode(1);
    root->left->left = new TreeNode(6);
    root->left->right = new TreeNode(2);
    
    TreeNode* lca = lowest_common_ancestor(root, root->left, root->left->right);
    cout << lca->val << "\n";  // 输出 5
    return 0;
}
```

**复杂度**：时间 `O(n)`，空间 `O(h)`

**易错点**：要理解递归的含义，left/right 非空表示在那个子树找到了目标

---

### 例题 6：路径总和

**题目**：判断是否存在根到叶路径，路径和等于目标值。

**思路**：递归，每次减去当前节点值，到叶子节点判断是否为 0。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left, *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

bool has_path_sum(TreeNode* root, int target_sum) {
    if (!root) return false;
    
    // 叶子节点
    if (!root->left && !root->right) {
        return root->val == target_sum;
    }
    
    // 递归左右子树
    int remain = target_sum - root->val;
    return has_path_sum(root->left, remain) || has_path_sum(root->right, remain);
}

int main() {
    TreeNode* root = new TreeNode(5);
    root->left = new TreeNode(4);
    root->right = new TreeNode(8);
    root->left->left = new TreeNode(11);
    root->left->left->left = new TreeNode(7);
    root->left->left->right = new TreeNode(2);
    
    cout << (has_path_sum(root, 22) ? "YES" : "NO") << "\n";
    return 0;
}
```

**复杂度**：时间 `O(n)`，空间 `O(h)`

**易错点**：必须是根到叶路径，要判断 `!root->left && !root->right`

---

### 例题 7：树的重心

**题目**：找到一个节点，删除它后剩余连通块的最大节点数最小。

**思路**：DFS 计算每个节点的子树大小，删除节点 u 后，最大连通块是 max(子树大小, n - subtree[u])。

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 1e5 + 5;
vector<int> tree[MAXN];
int subtree[MAXN];
int n;
int center = -1;
int min_max_part = INT_MAX;

int dfs(int u, int parent) {
    subtree[u] = 1;
    int max_part = 0;
    
    for (int v : tree[u]) {
        if (v == parent) continue;
        
        int size = dfs(v, u);
        subtree[u] += size;
        max_part = max(max_part, size);
    }
    
    // 删除 u 后，上方的连通块大小
    max_part = max(max_part, n - subtree[u]);
    
    // 更新重心
    if (max_part < min_max_part) {
        min_max_part = max_part;
        center = u;
    }
    
    return subtree[u];
}

int main() {
    cin >> n;
    
    for (int i = 0; i < n - 1; ++i) {
        int u, v;
        cin >> u >> v;
        tree[u].push_back(v);
        tree[v].push_back(u);
    }
    
    dfs(1, -1);
    
    cout << "重心: " << center << "\n";
    cout << "最大连通块大小: " << min_max_part << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(n)`，空间 `O(n)`

**易错点**：删除节点后，上方的连通块大小是 `n - subtree[u]`

---

### 例题 8：从前序和中序构造二叉树

**题目**：给定前序和中序遍历，重建二叉树。

**思路**：前序第一个是根，在中序找到根的位置，左边是左子树，右边是右子树，递归构造。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left, *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
    unordered_map<int, int> inorder_map;
    
    TreeNode* build(vector<int>& preorder, int pre_left, int pre_right,
                    vector<int>& inorder, int in_left, int in_right) {
        if (pre_left > pre_right) return nullptr;
        
        int root_val = preorder[pre_left];
        TreeNode* root = new TreeNode(root_val);
        
        int in_root = inorder_map[root_val];
        int left_size = in_root - in_left;
        
        root->left = build(preorder, pre_left + 1, pre_left + left_size,
                          inorder, in_left, in_root - 1);
        root->right = build(preorder, pre_left + left_size + 1, pre_right,
                           inorder, in_root + 1, in_right);
        
        return root;
    }
    
public:
    TreeNode* build_tree(vector<int>& preorder, vector<int>& inorder) {
        for (int i = 0; i < inorder.size(); ++i) {
            inorder_map[inorder[i]] = i;
        }
        return build(preorder, 0, preorder.size() - 1,
                    inorder, 0, inorder.size() - 1);
    }
};

void print_inorder(TreeNode* root) {
    if (!root) return;
    print_inorder(root->left);
    cout << root->val << " ";
    print_inorder(root->right);
}

int main() {
    vector<int> preorder = {3, 9, 20, 15, 7};
    vector<int> inorder = {9, 3, 15, 20, 7};
    
    Solution sol;
    TreeNode* root = sol.build_tree(preorder, inorder);
    
    print_inorder(root);
    cout << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(n)`，空间 `O(n)`

**易错点**：用哈希表加速查找根在中序的位置，计算左子树大小

---

## 常见陷阱

1. **空节点处理**：递归前要判断 `if (!root) return ...`
2. **叶子节点判断**：`!root->left && !root->right`
3. **递归返回值**：明确每个递归函数返回什么
4. **全局变量**：树的直径、路径和等问题需要全局变量
5. **父节点传递**：无向树 DFS 要传递父节点避免回溯
6. **树的表示**：二叉树用指针，多叉树/图用邻接表
7. **层序遍历**：要先记录当前层大小 `size = q.size()`

## 树的遍历总结

| 遍历方式 | 访问顺序 | 应用场景 |
|---------|---------|---------|
| 前序 | 根 → 左 → 右 | 复制树、序列化 |
| 中序 | 左 → 根 → 右 | BST 得到有序序列 |
| 后序 | 左 → 右 → 根 | 删除树、计算子树信息 |
| 层序 | 逐层访问 | 最短路径、层次关系 |

## 递归模板

```cpp
void dfs(TreeNode* root) {
    // 终止条件
    if (!root) return;
    
    // 当前层逻辑
    process(root->val);
    
    // 递归子问题
    dfs(root->left);
    dfs(root->right);
    
    // 回溯（如果需要）
    // restore_state();
}
```

## 适用场景总结

- **遍历问题**：前序/中序/后序/层序遍历
- **路径问题**：路径和、直径、最长路径
- **子树问题**：子树大小、子树统计
- **祖先问题**：LCA、路径上的节点
- **构造问题**：从遍历序列重建树
- **树形 DP**：树上背包、树的染色
