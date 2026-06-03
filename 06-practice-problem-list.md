# 知识点配套题单

这份题单用于配合两个月学习路线。题目链接以公开题面为主，优先选择 LeetCode、洛谷、牛客中比较稳定、适合 C++ 机试训练的题。

使用建议：

- 每个专题先做“必做”，再按时间做“选做”。
- LeetCode 适合练题型和边界；洛谷/牛客适合练完整 `main`、输入输出和 OJ 模式。
- 同一道题如果看题解才做出来，隔 1-3 天重写一次。
- 不要被题量吓到；两个月完成 150-200 道，并且认真复盘，就已经很扎实。

表格中的 `Hot 100` 表示该题来自 LeetCode 官方 Top 100 Liked / 力扣热题 100。这里不单独列 Hot 100 文件，而是把它们穿插到对应知识点下，作为每个专题的高质量示例题。

## 平台入口

- LeetCode 题目页：`https://leetcode.com/problems/<slug>/`
- 洛谷题目页：`https://www.luogu.com.cn/problem/Pxxxx`
- 牛客题目页：`https://www.nowcoder.com/practice/<id>`

部分平台可能要求登录后才能提交或查看完整运行记录，但下面挑选的链接一般可以直接打开题面。若遇到需要登录的牛客页面，可以先跳过，用同知识点的 LeetCode/洛谷题替代。

## 第 1 周：C++ 基础、I/O、模拟、字符串、排序、哈希

### 基础输入输出与模拟

必做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| 洛谷 | [P1001 A+B Problem](https://www.luogu.com.cn/problem/P1001) | 标准输入输出 |
| 洛谷 | [P5703 苹果采购](https://www.luogu.com.cn/problem/P5703) | 基础表达式 |
| 洛谷 | [P5704 字母转换](https://www.luogu.com.cn/problem/P5704) | 字符处理 |
| 洛谷 | [P5705 数字反转](https://www.luogu.com.cn/problem/P5705) | 字符串/数字 |
| 洛谷 | [P5710 数的性质](https://www.luogu.com.cn/problem/P5710) | 条件判断 |
| 牛客 | [HJ1 字符串最后一个单词的长度](https://www.nowcoder.com/practice/8c949ea5f36f422594b306a2300315da) | 字符串、整行输入 |
| 牛客 | [HJ2 计算某字符出现次数](https://www.nowcoder.com/practice/a35ce98431874e3a820dbe4b2d0508b1) | 字符统计 |
| 牛客 | [HJ3 明明的随机数](https://www.nowcoder.com/practice/3245215fffb84b7b81285493eae92ff0) | 排序去重 |
| 牛客 | [HJ5 进制转换](https://www.nowcoder.com/practice/8f3df50d2b9043208c5eed283d1d4da6) | 字符串解析、进制 |

选做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| 洛谷 | [P1421 小玉买文具](https://www.luogu.com.cn/problem/P1421) | 基础算术 |
| 洛谷 | [P1425 小鱼的游泳时间](https://www.luogu.com.cn/problem/P1425) | 时间计算 |
| 洛谷 | [P1046 陶陶摘苹果](https://www.luogu.com.cn/problem/P1046) | 数组遍历 |
| 洛谷 | [P1055 ISBN 号码](https://www.luogu.com.cn/problem/P1055) | 字符串模拟 |
| 洛谷 | [P1307 数字反转](https://www.luogu.com.cn/problem/P1307) | 数字处理 |
| 牛客 | [HJ8 合并表记录](https://www.nowcoder.com/practice/de044e89123f4a7482bd2b214a685201) | `map`、有序统计 |
| 牛客 | [HJ10 字符个数统计](https://www.nowcoder.com/practice/eb94f6a5b2ba49c6ac72d40b5ce95f50) | `set`、去重 |
| 牛客 | [HJ14 字符串排序](https://www.nowcoder.com/practice/5af18ba2eb45443aa91a11e848aa6723) | 排序、字符串 |

### LeetCode 基础题

必做：

| 题目 | 知识点 |
|---|---|
| [1. Two Sum](https://leetcode.com/problems/two-sum/) | 哈希；Hot 100 |
| [49. Group Anagrams](https://leetcode.com/problems/group-anagrams/) | 哈希、字符串分组；Hot 100 |
| [128. Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) | 哈希集合；Hot 100 |
| [217. Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) | 哈希/集合 |
| [242. Valid Anagram](https://leetcode.com/problems/valid-anagram/) | 字符频次 |
| [125. Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) | 双指针、字符处理 |
| [344. Reverse String](https://leetcode.com/problems/reverse-string/) | 双指针 |
| [58. Length of Last Word](https://leetcode.com/problems/length-of-last-word/) | 字符串扫描 |
| [14. Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/) | 字符串 |
| [387. First Unique Character in a String](https://leetcode.com/problems/first-unique-character-in-a-string/) | 频次统计 |

选做：

| 题目 | 知识点 |
|---|---|
| [66. Plus One](https://leetcode.com/problems/plus-one/) | 数组模拟 |
| [118. Pascal's Triangle](https://leetcode.com/problems/pascals-triangle/) | 二维数组；Hot 100 |
| [169. Majority Element](https://leetcode.com/problems/majority-element/) | 计数/投票；Hot 100 |
| [283. Move Zeroes](https://leetcode.com/problems/move-zeroes/) | 数组原地操作；Hot 100 |
| [48. Rotate Image](https://leetcode.com/problems/rotate-image/) | 矩阵原地旋转；Hot 100 |
| [54. Spiral Matrix](https://leetcode.com/problems/spiral-matrix/) | 矩阵模拟；Hot 100 |
| [73. Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/) | 矩阵标记；Hot 100 |
| [412. Fizz Buzz](https://leetcode.com/problems/fizz-buzz/) | 基础模拟 |

## 第 2 周：复杂度、前缀和、差分、双指针、二分

### 前缀和与差分

必做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [303. Range Sum Query - Immutable](https://leetcode.com/problems/range-sum-query-immutable/) | 一维前缀和 |
| LeetCode | [304. Range Sum Query 2D - Immutable](https://leetcode.com/problems/range-sum-query-2d-immutable/) | 二维前缀和 |
| LeetCode | [560. Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | 前缀和 + 哈希；Hot 100 |
| LeetCode | [724. Find Pivot Index](https://leetcode.com/problems/find-pivot-index/) | 前缀和思想 |
| 洛谷 | [P1115 最大子段和](https://www.luogu.com.cn/problem/P1115) | 前缀/线性扫描 |
| 洛谷 | [P2367 语文成绩](https://www.luogu.com.cn/problem/P2367) | 差分 |
| 洛谷 | [P3397 地毯](https://www.luogu.com.cn/problem/P3397) | 二维差分 |
| 洛谷 | [P2004 领地选择](https://www.luogu.com.cn/problem/P2004) | 二维前缀和 |

选做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [238. Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | 前后缀；Hot 100 |
| 洛谷 | [P1719 最大加权矩形](https://www.luogu.com.cn/problem/P1719) | 二维前缀和/最大子段 |

### 双指针与滑动窗口

必做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [3. Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | 滑动窗口；Hot 100 |
| LeetCode | [209. Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/) | 滑动窗口 |
| LeetCode | [11. Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | 对撞指针；Hot 100 |
| LeetCode | [167. Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | 有序双指针 |
| LeetCode | [977. Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/) | 对撞指针 |

选做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [15. 3Sum](https://leetcode.com/problems/3sum/) | 排序 + 双指针；Hot 100 |
| LeetCode | [438. Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/) | 滑动窗口 + 频次；Hot 100 |
| LeetCode | [76. Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | 滑动窗口 Hard；Hot 100 |
| LeetCode | [42. Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | 双指针/单调栈 Hard；Hot 100 |
| LeetCode | [18. 4Sum](https://leetcode.com/problems/4sum/) | 枚举 + 双指针 |

### 二分与二分答案

必做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [704. Binary Search](https://leetcode.com/problems/binary-search/) | 基础二分 |
| LeetCode | [35. Search Insert Position](https://leetcode.com/problems/search-insert-position/) | 下界；Hot 100 |
| LeetCode | [34. Find First and Last Position of Element](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) | 左右边界；Hot 100 |
| LeetCode | [33. Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | 旋转数组二分；Hot 100 |
| LeetCode | [74. Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/) | 矩阵二分；Hot 100 |
| LeetCode | [153. Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) | 旋转数组二分；Hot 100 |
| LeetCode | [69. Sqrt(x)](https://leetcode.com/problems/sqrtx/) | 答案二分 |
| LeetCode | [875. Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) | 二分答案 |
| 洛谷 | [P2249 查找](https://www.luogu.com.cn/problem/P2249) | 二分查找 |
| 洛谷 | [P1102 A-B 数对](https://www.luogu.com.cn/problem/P1102) | 排序 + 二分 |
| 洛谷 | [P1873 砍树](https://www.luogu.com.cn/problem/P1873) | 二分答案 |
| 洛谷 | [P2678 跳石头](https://www.luogu.com.cn/problem/P2678) | 二分答案 |

选做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [410. Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/) | 二分答案/DP 对照 |
| 洛谷 | [P1182 数列分段 Section II](https://www.luogu.com.cn/problem/P1182) | 二分答案 |

## 第 3 周：栈、队列、堆、单调结构、贪心

### 栈与表达式

必做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [20. Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | 栈；Hot 100 |
| LeetCode | [155. Min Stack](https://leetcode.com/problems/min-stack/) | 辅助栈；Hot 100 |
| LeetCode | [150. Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) | 栈、表达式 |
| LeetCode | [394. Decode String](https://leetcode.com/problems/decode-string/) | 栈、字符串解码；Hot 100 |
| 洛谷 | [P1739 表达式括号匹配](https://www.luogu.com.cn/problem/P1739) | 栈/计数 |
| 洛谷 | [P1449 后缀表达式](https://www.luogu.com.cn/problem/P1449) | 栈、后缀表达式 |
| 牛客 | [HJ50 四则运算](https://www.nowcoder.com/practice/9999764a61484d819056f807d2a91f1e) | 表达式解析 |

选做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [232. Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/) | 栈和队列互转 |
| LeetCode | [225. Implement Stack using Queues](https://leetcode.com/problems/implement-stack-using-queues/) | 队列模拟栈 |

### 单调栈、单调队列、堆

必做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [496. Next Greater Element I](https://leetcode.com/problems/next-greater-element-i/) | 单调栈 |
| LeetCode | [739. Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | 单调栈；Hot 100 |
| LeetCode | [84. Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) | 单调栈 Hard；Hot 100 |
| LeetCode | [239. Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) | 单调队列；Hot 100 |
| LeetCode | [215. Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | 堆/快速选择；Hot 100 |
| LeetCode | [347. Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | 哈希 + 堆；Hot 100 |
| 洛谷 | [P1886 滑动窗口](https://www.luogu.com.cn/problem/P1886) | 单调队列 |
| 洛谷 | [P1090 合并果子](https://www.luogu.com.cn/problem/P1090) | 小根堆、贪心 |

选做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [23. Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) | 堆、链表；Hot 100 |
| LeetCode | [295. Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) | 双堆 Hard；Hot 100 |

### 贪心

必做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [56. Merge Intervals](https://leetcode.com/problems/merge-intervals/) | 区间排序；Hot 100 |
| LeetCode | [435. Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) | 区间贪心 |
| LeetCode | [452. Minimum Number of Arrows to Burst Balloons](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/) | 区间贪心 |
| LeetCode | [55. Jump Game](https://leetcode.com/problems/jump-game/) | 贪心；Hot 100 |
| LeetCode | [45. Jump Game II](https://leetcode.com/problems/jump-game-ii/) | 贪心；Hot 100 |
| LeetCode | [763. Partition Labels](https://leetcode.com/problems/partition-labels/) | 贪心、区间划分；Hot 100 |
| 洛谷 | [P1803 凌乱的 yyy / 线段覆盖](https://www.luogu.com.cn/problem/P1803) | 区间贪心 |
| 洛谷 | [P2240 部分背包问题](https://www.luogu.com.cn/problem/P2240) | 贪心、排序 |

选做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [621. Task Scheduler](https://leetcode.com/problems/task-scheduler/) | 贪心/计数 |

## 第 4 周：DFS、BFS、回溯、并查集

### DFS/BFS 网格与状态搜索

必做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [200. Number of Islands](https://leetcode.com/problems/number-of-islands/) | DFS/BFS 连通块；Hot 100 |
| LeetCode | [695. Max Area of Island](https://leetcode.com/problems/max-area-of-island/) | DFS/BFS |
| LeetCode | [733. Flood Fill](https://leetcode.com/problems/flood-fill/) | DFS/BFS |
| LeetCode | [994. Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) | 多源 BFS；Hot 100 |
| LeetCode | [542. 01 Matrix](https://leetcode.com/problems/01-matrix/) | 多源 BFS |
| LeetCode | [1091. Shortest Path in Binary Matrix](https://leetcode.com/problems/shortest-path-in-binary-matrix/) | BFS 最短路 |
| 洛谷 | [P1605 迷宫](https://www.luogu.com.cn/problem/P1605) | DFS 搜索 |
| 洛谷 | [P1135 奇怪的电梯](https://www.luogu.com.cn/problem/P1135) | BFS |
| 洛谷 | [P1141 01 迷宫](https://www.luogu.com.cn/problem/P1141) | 连通块预处理 |
| 洛谷 | [P1162 填涂颜色](https://www.luogu.com.cn/problem/P1162) | DFS/BFS 填充 |
| 洛谷 | [P1451 求细胞数量](https://www.luogu.com.cn/problem/P1451) | 连通块 |

选做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [130. Surrounded Regions](https://leetcode.com/problems/surrounded-regions/) | 边界 BFS/DFS |
| LeetCode | [79. Word Search](https://leetcode.com/problems/word-search/) | 回溯、网格；Hot 100 |

### 回溯

必做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [46. Permutations](https://leetcode.com/problems/permutations/) | 全排列；Hot 100 |
| LeetCode | [78. Subsets](https://leetcode.com/problems/subsets/) | 子集；Hot 100 |
| LeetCode | [77. Combinations](https://leetcode.com/problems/combinations/) | 组合 |
| LeetCode | [39. Combination Sum](https://leetcode.com/problems/combination-sum/) | 回溯；Hot 100 |
| LeetCode | [17. Letter Combinations of a Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) | 回溯、字符串映射；Hot 100 |
| LeetCode | [22. Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) | 回溯、括号生成；Hot 100 |
| 洛谷 | [P1219 八皇后](https://www.luogu.com.cn/problem/P1219) | 回溯、剪枝 |

选做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [47. Permutations II](https://leetcode.com/problems/permutations-ii/) | 去重回溯 |
| LeetCode | [90. Subsets II](https://leetcode.com/problems/subsets-ii/) | 去重回溯 |
| LeetCode | [40. Combination Sum II](https://leetcode.com/problems/combination-sum-ii/) | 去重回溯 |
| LeetCode | [131. Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/) | 回溯 + 回文判断；Hot 100 |
| LeetCode | [51. N-Queens](https://leetcode.com/problems/n-queens/) | 回溯 Hard；Hot 100 |

### 并查集

必做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [547. Number of Provinces](https://leetcode.com/problems/number-of-provinces/) | 并查集/DFS |
| LeetCode | [684. Redundant Connection](https://leetcode.com/problems/redundant-connection/) | 并查集 |
| 洛谷 | [P1551 亲戚](https://www.luogu.com.cn/problem/P1551) | 并查集 |
| 洛谷 | [P3367 并查集](https://www.luogu.com.cn/problem/P3367) | 并查集模板 |

选做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [990. Satisfiability of Equality Equations](https://leetcode.com/problems/satisfiability-of-equality-equations/) | 并查集 |
| LeetCode | [721. Accounts Merge](https://leetcode.com/problems/accounts-merge/) | 并查集 + 哈希 |

## 第 5 周：图论基础

### 建图、遍历、拓扑排序

必做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [841. Keys and Rooms](https://leetcode.com/problems/keys-and-rooms/) | 图遍历 |
| LeetCode | [797. All Paths From Source to Target](https://leetcode.com/problems/all-paths-from-source-to-target/) | DAG DFS |
| LeetCode | [133. Clone Graph](https://leetcode.com/problems/clone-graph/) | 图遍历 + 哈希 |
| LeetCode | [207. Course Schedule](https://leetcode.com/problems/course-schedule/) | 拓扑排序/环检测；Hot 100 |
| LeetCode | [210. Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) | 拓扑排序 |
| 洛谷 | [P3916 图的遍历](https://www.luogu.com.cn/problem/P3916) | 图遍历 |
| 洛谷 | [P5318 查找文献](https://www.luogu.com.cn/problem/P5318) | DFS/BFS 遍历顺序 |
| 洛谷 | [P1113 杂务](https://www.luogu.com.cn/problem/P1113) | 拓扑排序/DP |
| 洛谷 | [P1807 最长路](https://www.luogu.com.cn/problem/P1807) | DAG 最长路 |

### 树与链表选练

这些题大多来自 Hot 100，适合补递归、指针、层序遍历和结构设计。研究生夏令营机试如果是传统 OJ，树和链表一般不会像 LeetCode 那样直接给 `TreeNode*` / `ListNode*`，所以建议作为第 5 周的选练，不要挤占图论和最短路时间。

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [94. Binary Tree Inorder Traversal](https://leetcode.com/problems/binary-tree-inorder-traversal/) | 二叉树遍历；Hot 100 |
| LeetCode | [98. Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) | BST、递归边界；Hot 100 |
| LeetCode | [101. Symmetric Tree](https://leetcode.com/problems/symmetric-tree/) | 二叉树递归；Hot 100 |
| LeetCode | [102. Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) | BFS 层序遍历；Hot 100 |
| LeetCode | [104. Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | 树高递归；Hot 100 |
| LeetCode | [105. Construct Binary Tree from Preorder and Inorder Traversal](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) | 建树、哈希定位；Hot 100 |
| LeetCode | [114. Flatten Binary Tree to Linked List](https://leetcode.com/problems/flatten-binary-tree-to-linked-list/) | 树结构改造；Hot 100 |
| LeetCode | [226. Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) | 递归/层序；Hot 100 |
| LeetCode | [230. Kth Smallest Element in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) | BST 中序；Hot 100 |
| LeetCode | [236. Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | LCA、递归返回值；Hot 100 |
| LeetCode | [437. Path Sum III](https://leetcode.com/problems/path-sum-iii/) | 树上前缀和；Hot 100 |
| LeetCode | [543. Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/) | 树形 DP 入门；Hot 100 |
| LeetCode | [21. Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | 链表合并；Hot 100 |
| LeetCode | [141. Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | 快慢指针；Hot 100 |
| LeetCode | [142. Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/) | 快慢指针进阶；Hot 100 |
| LeetCode | [160. Intersection of Two Linked Lists](https://leetcode.com/problems/intersection-of-two-linked-lists/) | 双指针；Hot 100 |
| LeetCode | [206. Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | 链表反转；Hot 100 |
| LeetCode | [234. Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list/) | 链表 + 快慢指针；Hot 100 |
| LeetCode | [146. LRU Cache](https://leetcode.com/problems/lru-cache/) | 哈希 + 双向链表；Hot 100 |

### 最短路与最小生成树

必做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [743. Network Delay Time](https://leetcode.com/problems/network-delay-time/) | Dijkstra |
| LeetCode | [1631. Path With Minimum Effort](https://leetcode.com/problems/path-with-minimum-effort/) | Dijkstra/二分 + BFS |
| LeetCode | [1584. Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points/) | 最小生成树 |
| 洛谷 | [P3371 单源最短路径（弱化版）](https://www.luogu.com.cn/problem/P3371) | Dijkstra/SPFA 对照 |
| 洛谷 | [P4779 单源最短路径（标准版）](https://www.luogu.com.cn/problem/P4779) | Dijkstra 模板 |
| 洛谷 | [P1346 电车](https://www.luogu.com.cn/problem/P1346) | 最短路 |
| 洛谷 | [P3366 最小生成树](https://www.luogu.com.cn/problem/P3366) | Kruskal/Prim |
| 洛谷 | [P1991 无线通讯网](https://www.luogu.com.cn/problem/P1991) | 最小生成树 |

选做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [787. Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/) | 限制步数最短路 |
| LeetCode | [1514. Path with Maximum Probability](https://leetcode.com/problems/path-with-maximum-probability/) | Dijkstra 变形 |
| LeetCode | [399. Evaluate Division](https://leetcode.com/problems/evaluate-division/) | 图建模 |

## 第 6 周：动态规划、数学、位运算

### 线性 DP、路径 DP、背包

必做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [70. Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) | 线性 DP；Hot 100 |
| LeetCode | [53. Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) | 最大子段和；Hot 100 |
| LeetCode | [198. House Robber](https://leetcode.com/problems/house-robber/) | 线性 DP；Hot 100 |
| LeetCode | [62. Unique Paths](https://leetcode.com/problems/unique-paths/) | 路径 DP；Hot 100 |
| LeetCode | [64. Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/) | 路径 DP；Hot 100 |
| LeetCode | [120. Triangle](https://leetcode.com/problems/triangle/) | 路径 DP |
| LeetCode | [416. Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) | 01 背包；Hot 100 |
| LeetCode | [322. Coin Change](https://leetcode.com/problems/coin-change/) | 完全背包/最短；Hot 100 |
| LeetCode | [518. Coin Change II](https://leetcode.com/problems/coin-change-ii/) | 完全背包/方案数 |
| 洛谷 | [P1216 数字三角形](https://www.luogu.com.cn/problem/P1216) | 路径 DP |
| 洛谷 | [P1048 采药](https://www.luogu.com.cn/problem/P1048) | 01 背包 |
| 洛谷 | [P1060 开心的金明](https://www.luogu.com.cn/problem/P1060) | 01 背包 |
| 洛谷 | [P1616 疯狂的采药](https://www.luogu.com.cn/problem/P1616) | 完全背包 |

选做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [213. House Robber II](https://leetcode.com/problems/house-robber-ii/) | 环形 DP |
| LeetCode | [63. Unique Paths II](https://leetcode.com/problems/unique-paths-ii/) | 障碍路径 DP |
| LeetCode | [279. Perfect Squares](https://leetcode.com/problems/perfect-squares/) | 完全背包/BFS；Hot 100 |
| LeetCode | [32. Longest Valid Parentheses](https://leetcode.com/problems/longest-valid-parentheses/) | DP/栈 Hard；Hot 100 |

### 序列 DP、区间 DP、字符串 DP

必做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [300. Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) | LIS；Hot 100 |
| LeetCode | [1143. Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) | LCS；Hot 100 |
| LeetCode | [72. Edit Distance](https://leetcode.com/problems/edit-distance/) | 字符串 DP；Hot 100 |
| LeetCode | [5. Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) | 区间/中心扩展；Hot 100 |
| LeetCode | [516. Longest Palindromic Subsequence](https://leetcode.com/problems/longest-palindromic-subsequence/) | 区间 DP |
| LeetCode | [139. Word Break](https://leetcode.com/problems/word-break/) | DP + 哈希；Hot 100 |
| 洛谷 | [P1020 导弹拦截](https://www.luogu.com.cn/problem/P1020) | LIS |
| 洛谷 | [P1439 最长公共子序列](https://www.luogu.com.cn/problem/P1439) | LCS/LIS 转化 |
| 洛谷 | [P1002 过河卒](https://www.luogu.com.cn/problem/P1002) | 路径 DP |
| 洛谷 | [P1880 石子合并](https://www.luogu.com.cn/problem/P1880) | 区间 DP |
| 洛谷 | [P1057 传球游戏](https://www.luogu.com.cn/problem/P1057) | DP |
| 洛谷 | [P1137 旅行计划](https://www.luogu.com.cn/problem/P1137) | DAG DP |

选做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [152. Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) | 状态 DP；Hot 100 |
| LeetCode | [121. Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | 前缀最小/DP；Hot 100 |
| LeetCode | [122. Best Time to Buy and Sell Stock II](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/) | 贪心/DP |

### 数学与位运算

必做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [50. Pow(x, n)](https://leetcode.com/problems/powx-n/) | 快速幂 |
| LeetCode | [204. Count Primes](https://leetcode.com/problems/count-primes/) | 筛法 |
| LeetCode | [231. Power of Two](https://leetcode.com/problems/power-of-two/) | 位运算 |
| LeetCode | [136. Single Number](https://leetcode.com/problems/single-number/) | 异或；Hot 100 |
| LeetCode | [191. Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/) | 位计数 |
| LeetCode | [338. Counting Bits](https://leetcode.com/problems/counting-bits/) | 位运算/DP |
| 洛谷 | [P1226 快速幂](https://www.luogu.com.cn/problem/P1226) | 快速幂模板 |
| 洛谷 | [P3383 线性筛素数](https://www.luogu.com.cn/problem/P3383) | 筛法 |
| 洛谷 | [P1029 最大公约数和最小公倍数问题](https://www.luogu.com.cn/problem/P1029) | gcd/lcm |
| 洛谷 | [P1143 进制转换](https://www.luogu.com.cn/problem/P1143) | 进制 |
| 牛客 | [HJ61 放苹果](https://www.nowcoder.com/practice/bfd8234bb5e84be0b493656e390bdebf) | 递归/DP |

选做：

| 平台 | 题目 | 知识点 |
|---|---|---|
| 洛谷 | [P1464 Function](https://www.luogu.com.cn/problem/P1464) | 记忆化搜索 |

## 第 7-8 周：混合训练与模拟题单

### 混合套 1：保分基础

| 平台 | 题目 | 知识点 |
|---|---|---|
| 牛客 | [HJ17 坐标移动](https://www.nowcoder.com/practice/119bcca3befb405fbe58abe9c532eb29) | 字符串模拟 |
| 牛客 | [HJ20 密码验证合格程序](https://www.nowcoder.com/practice/184edec193864f0985ad2684fbc86841) | 字符串、规则判断 |
| 牛客 | [HJ26 字符串排序](https://www.nowcoder.com/practice/5190a1db6f4f4ddb92fd9c365c944584) | 字符串、稳定排序 |
| 牛客 | [HJ27 查找兄弟单词](https://www.nowcoder.com/practice/03ba8aeeef73400ca7a37a5f3370fe68) | 排序、哈希 |

### 混合套 2：中等算法

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [560. Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | 前缀和 + 哈希；Hot 100 |
| LeetCode | [200. Number of Islands](https://leetcode.com/problems/number-of-islands/) | DFS/BFS；Hot 100 |
| LeetCode | [207. Course Schedule](https://leetcode.com/problems/course-schedule/) | 拓扑排序；Hot 100 |
| LeetCode | [322. Coin Change](https://leetcode.com/problems/coin-change/) | DP；Hot 100 |

### 混合套 3：洛谷完整程序

| 平台 | 题目 | 知识点 |
|---|---|---|
| 洛谷 | [P2249 查找](https://www.luogu.com.cn/problem/P2249) | 二分 |
| 洛谷 | [P1886 滑动窗口](https://www.luogu.com.cn/problem/P1886) | 单调队列 |
| 洛谷 | [P3367 并查集](https://www.luogu.com.cn/problem/P3367) | 并查集 |
| 洛谷 | [P3371 单源最短路径](https://www.luogu.com.cn/problem/P3371) | 最短路 |

### 混合套 4：DP 与图综合

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [300. Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) | LIS；Hot 100 |
| LeetCode | [416. Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) | 背包；Hot 100 |
| LeetCode | [743. Network Delay Time](https://leetcode.com/problems/network-delay-time/) | Dijkstra |
| 洛谷 | [P1113 杂务](https://www.luogu.com.cn/problem/P1113) | 拓扑 + DP |

### 混合套 5：Hot 100 综合选练

这一套放在第 7-8 周使用，不看标签限时做。它们都来自 Hot 100，但覆盖的是不同模式，适合检验你是否真的能识别题型。

| 平台 | 题目 | 知识点 |
|---|---|---|
| LeetCode | [31. Next Permutation](https://leetcode.com/problems/next-permutation/) | 数组模拟、字典序；Hot 100 |
| LeetCode | [41. First Missing Positive](https://leetcode.com/problems/first-missing-positive/) | 原地哈希 Hard；Hot 100 |
| LeetCode | [75. Sort Colors](https://leetcode.com/problems/sort-colors/) | 三指针、原地排序；Hot 100 |
| LeetCode | [189. Rotate Array](https://leetcode.com/problems/rotate-array/) | 数组旋转；Hot 100 |
| LeetCode | [240. Search a 2D Matrix II](https://leetcode.com/problems/search-a-2d-matrix-ii/) | 矩阵搜索；Hot 100 |
| LeetCode | [287. Find the Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number/) | 二分/快慢指针；Hot 100 |
| LeetCode | [4. Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/) | 二分 Hard；Hot 100 |
| LeetCode | [124. Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | 树形 DP Hard；Hot 100 |

## 按知识点快速查题

| 知识点 | 推荐题 |
|---|---|
| 排序去重 | 洛谷 P1102、牛客 HJ3、LeetCode 217 |
| 字符串解析 | 牛客 HJ1/HJ5/HJ17/HJ20、洛谷 P1055 |
| 前缀和 | LeetCode 303/304/560、洛谷 P2004/P1719 |
| 差分 | 洛谷 P2367/P3397 |
| 双指针 | LeetCode 3/11/15/167/209/977 |
| 二分答案 | LeetCode 875/410、洛谷 P1873/P2678/P1182 |
| 栈 | LeetCode 20/155/150、洛谷 P1449/P1739 |
| 单调结构 | LeetCode 739/84/239、洛谷 P1886 |
| 堆 | LeetCode 215/347/23、洛谷 P1090 |
| 贪心 | LeetCode 56/435/452/55/45、洛谷 P1803/P2240 |
| DFS/BFS | LeetCode 200/695/994/542/1091、洛谷 P1605/P1135/P1141 |
| 回溯 | LeetCode 46/47/77/78/90/39/40、洛谷 P1219 |
| 并查集 | LeetCode 547/684/990/721、洛谷 P1551/P3367 |
| 拓扑排序 | LeetCode 207/210、洛谷 P1113/P1807 |
| 最短路 | LeetCode 743/787/1514/1631、洛谷 P3371/P4779/P1346 |
| 最小生成树 | LeetCode 1584、洛谷 P3366/P1991 |
| 背包 DP | LeetCode 416/322/518、洛谷 P1048/P1060/P1616 |
| 序列 DP | LeetCode 300/1143/72、洛谷 P1020/P1439 |
| 区间 DP | LeetCode 516、洛谷 P1880 |
| 数学/位运算 | LeetCode 50/204/231/136/191/338、洛谷 P1226/P3383 |

## 如何把题单接入每日学习

每天选题建议：

```text
1 道入门题：练 API 或模板
1-2 道标准题：练典型题型
0-1 道变形题：练识别和迁移
```

每周模拟建议：

```text
第 1-2 周：牛客 HJ/洛谷入门 + LeetCode easy
第 3-4 周：LeetCode medium + 洛谷普及/提高-
第 5-6 周：图论/DP 专项套题
第 7-8 周：混合题，不看标签限时做
```

题单不是任务清单，而是训练素材库。真正的完成标准是：同类题能独立识别、独立实现、独立调试。
