# C++ 研究生夏令营机试两个月学习材料

这组材料面向“写代码的机试”，默认使用 C++17/20 风格训练，目标周期为 8 周。它不是考前速查，而是一套可以每天推进的学习包：先建立题型地图，再补 C++ STL 和常用数据结构，随后系统训练输入输出、模板、调试、限时模拟。

## 学习目标

两个月结束时，你应该做到：

- 看到题目能先判断题型：模拟、哈希、二分、前缀和、DFS/BFS、图论、DP、贪心、数学。
- 能根据数据范围估复杂度，主动排除会 TLE 的写法。
- C++ STL 能熟练使用，不在 `priority_queue`、`map`、`set`、`sort` comparator、`getline` 这些地方失误。
- 能手写基础模板：并查集、BFS/DFS、Dijkstra、拓扑排序、二分答案、前缀和、背包、LIS、树状数组。
- 能适应 LeetCode 函数模式、洛谷/牛客/ACM 标准输入输出模式、读到 EOF、多组输入、整行输入、文件重定向。
- 能做 2-3 小时限时模拟，并形成“先保分、再冲中等题、最后处理难题”的考场节奏。

## 文件顺序

0. [00-two-month-curriculum.md](00-two-month-curriculum.md)
   - 8 周学习路线、每周目标、每日安排、阶段验收。
1. [01-problem-types-and-points.md](01-problem-types-and-points.md)
   - 代码题类型、考点、复杂度判断、题型识别、学习深度。
2. [02-cpp-stl-and-data-structures.md](02-cpp-stl-and-data-structures.md)
   - C++ STL、算法库、字符串、常用手写数据结构、API 练习。
3. [03-oj-modes-and-io.md](03-oj-modes-and-io.md)
   - LeetCode、洛谷、ACM/ICPC、OI 文件读写等模式，以及输入输出专项训练。
4. [04-cpp-algorithm-template-library.md](04-cpp-algorithm-template-library.md)
   - 可背诵、可默写、可直接迁移的 C++ 模板库。
5. [05-practice-review-and-mock-exams.md](05-practice-review-and-mock-exams.md)
   - 刷题量安排、错题本、复盘方法、限时模拟方案、考场策略。
6. [06-practice-problem-list.md](06-practice-problem-list.md)
   - 按 8 周和知识点整理的 LeetCode、洛谷、牛客配套题单，Hot 100 题会穿插标注。

## 推荐使用方式

第 1 周先读 `00` 和 `03`，把环境、输入输出、基础 C++ 写顺。  
第 2-6 周按 `00` 的节奏学习 `01` 的题型，同时查 `02` 和默写 `04`。  
全程配合 `06` 选题练习；LeetCode Hot 100 会作为示例题穿插在对应知识点里。  
第 7-8 周主要使用 `05` 做限时模拟、错题重做和模板稳定性训练。

每天最小训练单元：

```text
20 分钟：读材料/复习模板
60-90 分钟：刷 2-4 道题
20 分钟：复盘错因，补错题本
10 分钟：默写一个小模板或 STL 用法
```

## 训练平台建议

- LeetCode：适合练题型识别、边界、函数式解法。
- 洛谷：适合练标准输入输出、完整程序、算法模板。
- 牛客/高校机试题：适合练夏令营/保研机试风格。
- Codeforces/AtCoder 入门和中等题：适合练限时和题意转化。

不用一开始追求难题。前 6 周的重点是把中等难度常见题稳定做出来；第 7-8 周再集中练整套。

## 官方参考

- C++ 容器与算法：cppreference Containers library、Algorithms library。
- LeetCode 帮助中心：代码模板、测试用例输入方式、语言运行环境。
- 洛谷帮助中心：传统题数据格式、输入输出格式约定。
- ICPC 文档：World Finals programming environment 与 judging notes。
