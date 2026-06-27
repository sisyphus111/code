# 模拟与枚举

## 什么时候用

看到以下特征优先考虑模拟：
- 题目要求"按照规则执行过程"
- 涉及日期、时间、进制转换、格式化
- 矩阵旋转、翻转、遍历
- 游戏过程、排行榜、成绩统计
- 题目描述很长，但没有明显的算法关键词

核心思路：**把题意翻译成代码，保持清晰的状态管理**。

## 核心要点

1. **先列变量表**：每个变量代表什么，什么时候更新
2. **注意输出格式**：多空格、少换行是模拟题的高频失分点
3. **边界情况**：空输入、单元素、全相同、最大值
4. **多组数据要清空状态**

## 排序与比较

### 自定义排序

```cpp
struct Student {
    string name;
    int score;
    int age;
};

// 多关键字排序：分数降序，年龄升序，姓名升序
sort(students.begin(), students.end(), [](const Student& a, const Student& b) {
    if (a.score != b.score) return a.score > b.score;
    if (a.age != b.age) return a.age < b.age;
    return a.name < a.name;
});
```

### 稳定排序

当题目要求"相同情况下保持原序"，使用 `stable_sort`：

```cpp
stable_sort(a.begin(), a.end(), [](int x, int y) {
    return x < y;
});
```

## 例题演示

### 例题 1：日期差值计算

**题目**：给定两个日期 `YYYY-MM-DD`，计算相差天数。

**思路**：将日期转换为从某个基准点开始的天数，相减即可。

```cpp
#include <bits/stdc++.h>
using namespace std;

bool is_leap(int year) {
    return (year % 400 == 0) || (year % 4 == 0 && year % 100 != 0);
}

int days_in_month(int year, int month) {
    int days[] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    if (month == 2 && is_leap(year)) return 29;
    return days[month];
}

int to_days(int y, int m, int d) {
    int total = 0;
    // 从公元1年到y-1年的天数
    for (int year = 1; year < y; ++year) {
        total += is_leap(year) ? 366 : 365;
    }
    // 加上今年1月到m-1月的天数
    for (int month = 1; month < m; ++month) {
        total += days_in_month(y, month);
    }
    // 加上本月天数
    total += d;
    return total;
}

int main() {
    int y1, m1, d1, y2, m2, d2;
    scanf("%d-%d-%d", &y1, &m1, &d1);
    scanf("%d-%d-%d", &y2, &m2, &d2);
    
    int diff = abs(to_days(y2, m2, d2) - to_days(y1, m1, d1));
    printf("%d\n", diff);
    
    return 0;
}
```

**复杂度**：`O(y)` - 年份遍历，对于小范围年份可接受。

**易错点**：
- 闰年判断：400 整除或（4 整除且不被 100 整除）
- 月份天数：2 月需要特判闰年

---

### 例题 2：矩阵顺时针旋转 90 度

**题目**：给定 `n×n` 矩阵，原地旋转 90 度。

**思路**：先转置，再水平翻转。

```cpp
#include <bits/stdc++.h>
using namespace std;

void rotate(vector<vector<int>>& mat) {
    int n = mat.size();
    
    // 转置
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            swap(mat[i][j], mat[j][i]);
        }
    }
    
    // 水平翻转（每行反转）
    for (int i = 0; i < n; ++i) {
        reverse(mat[i].begin(), mat[i].end());
    }
}

int main() {
    int n;
    cin >> n;
    vector<vector<int>> mat(n, vector<int>(n));
    
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            cin >> mat[i][j];
        }
    }
    
    rotate(mat);
    
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            cout << mat[i][j] << " \n"[j == n - 1];
        }
    }
    
    return 0;
}
```

**复杂度**：`O(n²)`

**易错点**：
- 转置时 `j` 从 `i+1` 开始，避免重复交换
- 输出格式：行末不要多余空格

---

### 例题 3：成绩排名

**题目**：给定学生姓名和三科成绩，按总分降序排序，总分相同按姓名字典序升序。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Student {
    string name;
    int chinese, math, english;
    
    int total() const {
        return chinese + math + english;
    }
};

int main() {
    int n;
    cin >> n;
    vector<Student> students(n);
    
    for (int i = 0; i < n; ++i) {
        cin >> students[i].name 
            >> students[i].chinese 
            >> students[i].math 
            >> students[i].english;
    }
    
    sort(students.begin(), students.end(), [](const Student& a, const Student& b) {
        int ta = a.total(), tb = b.total();
        if (ta != tb) return ta > tb;
        return a.name < b.name;
    });
    
    for (const auto& s : students) {
        cout << s.name << " " << s.total() << "\n";
    }
    
    return 0;
}
```

**复杂度**：`O(n log n)`

**易错点**：
- 比较函数必须严格弱序：不能写 `a.total() >= b.total()`
- 相同情况的处理要完整

---

### 例题 4：螺旋矩阵生成

**题目**：生成 `n×n` 螺旋矩阵，从 1 开始顺时针填充。

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<vector<int>> spiral_matrix(int n) {
    vector<vector<int>> mat(n, vector<int>(n));
    
    int num = 1;
    int top = 0, bottom = n - 1, left = 0, right = n - 1;
    
    while (num <= n * n) {
        // 上边：从左到右
        for (int j = left; j <= right && num <= n * n; ++j) {
            mat[top][j] = num++;
        }
        ++top;
        
        // 右边：从上到下
        for (int i = top; i <= bottom && num <= n * n; ++i) {
            mat[i][right] = num++;
        }
        --right;
        
        // 下边：从右到左
        for (int j = right; j >= left && num <= n * n; --j) {
            mat[bottom][j] = num++;
        }
        --bottom;
        
        // 左边：从下到上
        for (int i = bottom; i >= top && num <= n * n; --i) {
            mat[i][left] = num++;
        }
        ++left;
    }
    
    return mat;
}

int main() {
    int n;
    cin >> n;
    auto mat = spiral_matrix(n);
    
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            cout << mat[i][j] << " \n"[j == n - 1];
        }
    }
    
    return 0;
}
```

**复杂度**：`O(n²)`

**易错点**：
- 每个方向填充后要更新边界
- 条件 `num <= n * n` 防止越界

---

### 例题 5：字符串解析 - IP 地址验证

**题目**：判断给定字符串是否为合法 IPv4 地址。

**思路**：按 `.` 分割，检查每段是否为 0-255 的数字。

```cpp
#include <bits/stdc++.h>
using namespace std;

bool is_valid_ip(const string& s) {
    if (s.empty()) return false;
    
    vector<string> parts;
    stringstream ss(s);
    string part;
    
    while (getline(ss, part, '.')) {
        parts.push_back(part);
    }
    
    if (parts.size() != 4) return false;
    
    for (const string& p : parts) {
        if (p.empty() || p.size() > 3) return false;
        
        // 不能有前导零，除非是单个 "0"
        if (p.size() > 1 && p[0] == '0') return false;
        
        // 检查是否全是数字
        for (char c : p) {
            if (!isdigit(c)) return false;
        }
        
        // 转换为数字检查范围
        int num = stoi(p);
        if (num < 0 || num > 255) return false;
    }
    
    return true;
}

int main() {
    string ip;
    cin >> ip;
    cout << (is_valid_ip(ip) ? "YES" : "NO") << "\n";
    return 0;
}
```

**复杂度**：`O(n)` - n 为字符串长度

**易错点**：
- 前导零判断：`01.1.1.1` 是非法的
- 空段判断：`1..1.1` 是非法的
- 数字范围：0-255

---

## 常见陷阱

1. **int 溢出**：涉及乘法、累加时用 `long long`
2. **下标越界**：循环边界、数组访问前检查
3. **输出格式**：
   - 行末不要多余空格：`cout << val << " \n"[j == n - 1]`
   - 题目要求换行就换行，不要多也不要少
4. **多组测试数据**：记得清空 `vector`、`map`、标志位
5. **浮点比较**：用 `abs(a - b) < 1e-9` 而不是 `a == b`

## 调试技巧

1. **造边界样例**：空、单元素、全相同、最大值
2. **手动模拟小样例**：在纸上跑一遍过程
3. **分段验证**：先输出中间状态，确认每步正确
4. **用 `assert` 检查不变量**：`assert(i >= 0 && i < n)`
