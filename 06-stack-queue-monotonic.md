# 栈、队列、单调栈、单调队列

## 什么时候用

看到以下特征优先考虑栈和队列：
- **括号匹配、表达式求值**：用栈
- **函数调用、递归模拟**：用栈
- **最近更大/更小元素**：单调栈
- **滑动窗口最值**：单调队列
- **层序遍历、最短路径**：普通队列（BFS）
- 题目中出现"下一个更大"、"左边第一个小于"等字眼

核心思路：**栈是后进先出（LIFO），队列是先进先出（FIFO），单调性维护最值信息**。

## 核心模板

### 普通栈

```cpp
stack<int> stk;
stk.push(x);           // 入栈
int top = stk.top();   // 获取栈顶
stk.pop();             // 出栈
bool empty = stk.empty();
```

### 普通队列

```cpp
queue<int> q;
q.push(x);             // 入队
int front = q.front(); // 获取队首
q.pop();               // 出队
bool empty = q.empty();
```

### 单调栈模板（求下一个更大元素）

```cpp
// 从左到右遍历，维护递减栈
stack<int> stk;  // 存储下标
vector<int> next_greater(n, -1);

for (int i = 0; i < n; ++i) {
    while (!stk.empty() && arr[stk.top()] < arr[i]) {
        next_greater[stk.top()] = i;
        stk.pop();
    }
    stk.push(i);
}
```

### 单调队列模板（滑动窗口最大值）

```cpp
deque<int> dq;  // 存储下标，队首是最大值
vector<int> result;

for (int i = 0; i < n; ++i) {
    // 移除窗口外的元素
    while (!dq.empty() && dq.front() <= i - k) {
        dq.pop_front();
    }
    
    // 维护单调递减（队首最大）
    while (!dq.empty() && arr[dq.back()] <= arr[i]) {
        dq.pop_back();
    }
    
    dq.push_back(i);
    
    if (i >= k - 1) {
        result.push_back(arr[dq.front()]);
    }
}
```

## 例题演示

### 例题 1：有效的括号

**题目**：给定只包含 `()[]{}` 的字符串，判断是否有效。

**思路**：用栈保存左括号，遇到右括号时检查栈顶是否匹配。

```cpp
#include <bits/stdc++.h>
using namespace std;

bool isValid(string s) {
    stack<char> stk;
    unordered_map<char, char> pairs = {
        {')', '('},
        {']', '['},
        {'}', '{'}
    };
    
    for (char c : s) {
        if (c == '(' || c == '[' || c == '{') {
            stk.push(c);
        } else {
            if (stk.empty() || stk.top() != pairs[c]) {
                return false;
            }
            stk.pop();
        }
    }
    
    return stk.empty();
}

int main() {
    string s;
    cin >> s;
    cout << (isValid(s) ? "YES" : "NO") << "\n";
    return 0;
}
```

**复杂度**：时间 `O(n)`，空间 `O(n)`

**易错点**：
- 最后要检查栈是否为空，防止只有左括号的情况
- 遇到右括号时先检查栈是否为空

---

### 例题 2：每日温度

**题目**：给定每天的温度数组，返回每天需要等待多少天才能有更高的温度。

**思路**：单调栈，维护递减栈，当前温度比栈顶高时，栈顶元素找到了答案。

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> dailyTemperatures(vector<int>& temperatures) {
    int n = temperatures.size();
    vector<int> answer(n, 0);
    stack<int> stk;  // 存储下标
    
    for (int i = 0; i < n; ++i) {
        while (!stk.empty() && temperatures[stk.top()] < temperatures[i]) {
            int idx = stk.top();
            stk.pop();
            answer[idx] = i - idx;
        }
        stk.push(i);
    }
    
    return answer;
}

int main() {
    int n;
    cin >> n;
    vector<int> temps(n);
    for (int i = 0; i < n; ++i) {
        cin >> temps[i];
    }
    
    vector<int> result = dailyTemperatures(temps);
    for (int i = 0; i < n; ++i) {
        cout << result[i] << " \n"[i == n - 1];
    }
    
    return 0;
}
```

**复杂度**：时间 `O(n)`，空间 `O(n)`

**易错点**：
- 栈中存储下标而不是值，方便计算距离
- 每个元素最多入栈出栈各一次，所以是 `O(n)`

---

### 例题 3：柱状图中最大的矩形

**题目**：给定每个柱子的高度，求能勾勒出的矩形的最大面积。

**思路**：单调栈，对每个高度找左右第一个比它小的位置，宽度就是这两个位置之间。

```cpp
#include <bits/stdc++.h>
using namespace std;

int largestRectangleArea(vector<int>& heights) {
    int n = heights.size();
    vector<int> left(n), right(n);
    stack<int> stk;
    
    // 找每个位置左边第一个小于它的位置
    for (int i = 0; i < n; ++i) {
        while (!stk.empty() && heights[stk.top()] >= heights[i]) {
            stk.pop();
        }
        left[i] = stk.empty() ? -1 : stk.top();
        stk.push(i);
    }
    
    // 清空栈，找右边第一个小于它的位置
    while (!stk.empty()) stk.pop();
    
    for (int i = n - 1; i >= 0; --i) {
        while (!stk.empty() && heights[stk.top()] >= heights[i]) {
            stk.pop();
        }
        right[i] = stk.empty() ? n : stk.top();
        stk.push(i);
    }
    
    int maxArea = 0;
    for (int i = 0; i < n; ++i) {
        int width = right[i] - left[i] - 1;
        maxArea = max(maxArea, heights[i] * width);
    }
    
    return maxArea;
}

int main() {
    int n;
    cin >> n;
    vector<int> heights(n);
    for (int i = 0; i < n; ++i) {
        cin >> heights[i];
    }
    
    cout << largestRectangleArea(heights) << "\n";
    return 0;
}
```

**复杂度**：时间 `O(n)`，空间 `O(n)`

**易错点**：
- 需要找严格小于的位置，所以条件是 `>=`
- 边界情况：左边没有更小的记为 -1，右边记为 n
- 宽度计算：`right[i] - left[i] - 1`

---

### 例题 4：滑动窗口最大值

**题目**：给定数组和窗口大小 k，返回每个窗口的最大值。

**思路**：单调队列，维护递减队列，队首始终是当前窗口最大值。

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> maxSlidingWindow(vector<int>& nums, int k) {
    deque<int> dq;  // 存储下标
    vector<int> result;
    
    for (int i = 0; i < nums.size(); ++i) {
        // 移除窗口外的元素
        while (!dq.empty() && dq.front() <= i - k) {
            dq.pop_front();
        }
        
        // 维护单调递减
        while (!dq.empty() && nums[dq.back()] <= nums[i]) {
            dq.pop_back();
        }
        
        dq.push_back(i);
        
        // 窗口形成后开始记录答案
        if (i >= k - 1) {
            result.push_back(nums[dq.front()]);
        }
    }
    
    return result;
}

int main() {
    int n, k;
    cin >> n >> k;
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    
    vector<int> result = maxSlidingWindow(nums, k);
    for (int i = 0; i < result.size(); ++i) {
        cout << result[i] << " \n"[i == result.size() - 1];
    }
    
    return 0;
}
```

**复杂度**：时间 `O(n)`，空间 `O(k)`

**易错点**：
- 队列中存储下标，方便判断是否在窗口内
- 维护递减队列时用 `<=` 而不是 `<`，保证队首是最大值
- 从第 k-1 个位置开始输出答案

---

### 例题 5：基本计算器（带括号）

**题目**：实现计算器，支持 `+`、`-`、`(`、`)` 和空格。

**思路**：用栈保存每层括号的结果和符号。

```cpp
#include <bits/stdc++.h>
using namespace std;

int calculate(string s) {
    stack<int> stk;
    int result = 0;
    int number = 0;
    int sign = 1;  // 1 表示正，-1 表示负
    
    for (int i = 0; i < s.length(); ++i) {
        char c = s[i];
        
        if (isdigit(c)) {
            number = number * 10 + (c - '0');
        } else if (c == '+') {
            result += sign * number;
            number = 0;
            sign = 1;
        } else if (c == '-') {
            result += sign * number;
            number = 0;
            sign = -1;
        } else if (c == '(') {
            // 保存当前结果和符号
            stk.push(result);
            stk.push(sign);
            // 重置
            result = 0;
            sign = 1;
        } else if (c == ')') {
            result += sign * number;
            number = 0;
            // 恢复之前的符号和结果
            result *= stk.top(); stk.pop();  // 符号
            result += stk.top(); stk.pop();  // 之前的结果
        }
    }
    
    if (number != 0) {
        result += sign * number;
    }
    
    return result;
}

int main() {
    string s;
    getline(cin, s);
    cout << calculate(s) << "\n";
    return 0;
}
```

**复杂度**：时间 `O(n)`，空间 `O(n)`

**易错点**：
- 遇到运算符或括号时，先处理之前累积的数字
- 括号内的结果要乘以括号前的符号
- 最后别忘了处理剩余的 number

---

### 例题 6：接雨水

**题目**：给定每个位置的高度，计算能接多少雨水。

**思路**：单调栈，维护递减栈，遇到更高的柱子时计算凹槽积水。

```cpp
#include <bits/stdc++.h>
using namespace std;

int trap(vector<int>& height) {
    int n = height.size();
    int water = 0;
    stack<int> stk;  // 存储下标
    
    for (int i = 0; i < n; ++i) {
        while (!stk.empty() && height[i] > height[stk.top()]) {
            int top = stk.top();
            stk.pop();
            
            if (stk.empty()) break;
            
            int left = stk.top();
            int width = i - left - 1;
            int h = min(height[left], height[i]) - height[top];
            water += width * h;
        }
        stk.push(i);
    }
    
    return water;
}

int main() {
    int n;
    cin >> n;
    vector<int> height(n);
    for (int i = 0; i < n; ++i) {
        cin >> height[i];
    }
    
    cout << trap(height) << "\n";
    return 0;
}
```

**复杂度**：时间 `O(n)`，空间 `O(n)`

**易错点**：
- 需要三个位置才能形成凹槽：左边界、底部、右边界
- 弹出底部后，栈如果为空说明没有左边界
- 高度是两边较矮的减去底部高度

---

### 例题 7：队列实现栈

**题目**：用两个队列实现栈的所有操作。

**思路**：push 时直接入队，pop 时将 n-1 个元素移到另一个队列，最后一个就是栈顶。

```cpp
#include <bits/stdc++.h>
using namespace std;

class MyStack {
private:
    queue<int> q1, q2;
    
public:
    void push(int x) {
        q1.push(x);
    }
    
    int pop() {
        // 将 q1 的前 n-1 个元素移到 q2
        while (q1.size() > 1) {
            q2.push(q1.front());
            q1.pop();
        }
        
        int top = q1.front();
        q1.pop();
        
        // 交换 q1 和 q2
        swap(q1, q2);
        
        return top;
    }
    
    int top() {
        while (q1.size() > 1) {
            q2.push(q1.front());
            q1.pop();
        }
        
        int topVal = q1.front();
        q2.push(topVal);
        q1.pop();
        
        swap(q1, q2);
        
        return topVal;
    }
    
    bool empty() {
        return q1.empty();
    }
};

int main() {
    MyStack stk;
    int n;
    cin >> n;
    
    for (int i = 0; i < n; ++i) {
        string op;
        cin >> op;
        
        if (op == "push") {
            int x;
            cin >> x;
            stk.push(x);
        } else if (op == "pop") {
            cout << stk.pop() << "\n";
        } else if (op == "top") {
            cout << stk.top() << "\n";
        } else if (op == "empty") {
            cout << (stk.empty() ? "true" : "false") << "\n";
        }
    }
    
    return 0;
}
```

**复杂度**：push `O(1)`，pop 和 top `O(n)`

**易错点**：
- pop 和 top 操作后要交换两个队列
- top 操作也要把元素重新放回队列

---

### 例题 8：去除重复字母（字典序最小）

**题目**：给定字符串，去除重复字母使得每个字母只出现一次，并且字典序最小。

**思路**：单调栈 + 贪心，如果当前字符比栈顶小且栈顶后面还会出现，就弹出栈顶。

```cpp
#include <bits/stdc++.h>
using namespace std;

string removeDuplicateLetters(string s) {
    vector<int> count(26, 0);
    vector<bool> inStack(26, false);
    
    // 统计每个字符出现次数
    for (char c : s) {
        count[c - 'a']++;
    }
    
    string result;
    
    for (char c : s) {
        count[c - 'a']--;
        
        if (inStack[c - 'a']) continue;
        
        // 如果当前字符比结果末尾小，且末尾字符后面还会出现，就移除末尾
        while (!result.empty() && c < result.back() && count[result.back() - 'a'] > 0) {
            inStack[result.back() - 'a'] = false;
            result.pop_back();
        }
        
        result.push_back(c);
        inStack[c - 'a'] = true;
    }
    
    return result;
}

int main() {
    string s;
    cin >> s;
    cout << removeDuplicateLetters(s) << "\n";
    return 0;
}
```

**复杂度**：时间 `O(n)`，空间 `O(1)`（只有 26 个字母）

**易错点**：
- 需要记录每个字符剩余出现次数
- 需要标记字符是否已在结果中
- 弹出栈顶时要更新 inStack 标记

---

## 常见陷阱

1. **栈/队列空判断**：在访问 top()/front() 之前必须检查是否为空
2. **单调栈存下标还是值**：通常存下标，方便计算距离和访问原数组
3. **单调性的方向**：
   - 求下一个更大：维护递减栈（从栈底到栈顶递减）
   - 求下一个更小：维护递增栈
4. **滑动窗口边界**：移除队首时检查 `dq.front() <= i - k` 而不是 `< i - k`
5. **括号匹配**：最后要检查栈是否为空

## 适用场景总结

| 问题类型 | 数据结构 | 时间复杂度 |
|---------|---------|-----------|
| 括号匹配 | 栈 | O(n) |
| 表达式求值 | 栈 | O(n) |
| 下一个更大/更小元素 | 单调栈 | O(n) |
| 滑动窗口最值 | 单调队列 | O(n) |
| 柱状图最大矩形 | 单调栈 | O(n) |
| 接雨水 | 单调栈 | O(n) |
| 层序遍历 | 普通队列 | O(n) |

**核心技巧**：
- 栈用于"最近"、"匹配"、"嵌套"问题
- 单调栈/队列将暴力 O(n²) 优化到 O(n)
- 单调性的维护：想清楚什么时候弹出，什么时候保留
