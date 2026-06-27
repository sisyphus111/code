# 位运算

## 什么时候用

看到以下特征优先考虑位运算：
- 判断奇偶、2的幂
- 集合的表示和操作
- 状态压缩
- 位掩码、位标记
- 快速乘除2的幂
- 交换两个数（不用中间变量）
- 统计二进制中1的个数
- 找出唯一的数字

核心思路：**用二进制位表示状态，用位运算加速计算**。

## 核心要点

1. **基本运算**：
   - `&` 与：都为1才为1
   - `|` 或：有1就为1
   - `^` 异或：不同为1，相同为0
   - `~` 取反：0变1，1变0
   - `<<` 左移：乘以2
   - `>>` 右移：除以2

2. **关键性质**：
   - `a ^ a = 0`
   - `a ^ 0 = a`
   - `a & (a-1)` 去除最右边的1
   - `a & -a` 提取最右边的1（lowbit）

3. **常用技巧**：
   - 判断奇偶：`n & 1`
   - 乘2：`n << 1`
   - 除2：`n >> 1`
   - 判断2的幂：`n & (n-1) == 0`

## 例题演示

### 例题 1：基础位运算操作

**题目**：实现常见位运算技巧。

```cpp
#include <bits/stdc++.h>
using namespace std;

// 判断奇偶
bool is_odd(int n) {
    return n & 1;
}

// 判断是否为2的幂
bool is_power_of_two(int n) {
    return n > 0 && (n & (n - 1)) == 0;
}

// 获取第k位（从0开始）
int get_bit(int n, int k) {
    return (n >> k) & 1;
}

// 设置第k位为1
int set_bit(int n, int k) {
    return n | (1 << k);
}

// 清除第k位（设为0）
int clear_bit(int n, int k) {
    return n & ~(1 << k);
}

// 翻转第k位
int toggle_bit(int n, int k) {
    return n ^ (1 << k);
}

// 去除最右边的1
int remove_rightmost_one(int n) {
    return n & (n - 1);
}

// 提取最右边的1（lowbit）
int lowbit(int n) {
    return n & -n;
}

int main() {
    int n = 12;  // 1100
    
    cout << "n = " << n << " (二进制: " << bitset<8>(n) << ")\n";
    cout << "是否为奇数: " << is_odd(n) << "\n";
    cout << "是否为2的幂: " << is_power_of_two(n) << "\n";
    cout << "第2位: " << get_bit(n, 2) << "\n";
    cout << "设置第0位: " << set_bit(n, 0) << " (" << bitset<8>(set_bit(n, 0)) << ")\n";
    cout << "清除第2位: " << clear_bit(n, 2) << " (" << bitset<8>(clear_bit(n, 2)) << ")\n";
    cout << "翻转第0位: " << toggle_bit(n, 0) << " (" << bitset<8>(toggle_bit(n, 0)) << ")\n";
    cout << "去除最右边的1: " << remove_rightmost_one(n) << " (" << bitset<8>(remove_rightmost_one(n)) << ")\n";
    cout << "最右边的1: " << lowbit(n) << " (" << bitset<8>(lowbit(n)) << ")\n";
    
    return 0;
}
```

**输出示例**：
```
n = 12 (二进制: 00001100)
是否为奇数: 0
是否为2的幂: 0
第2位: 1
设置第0位: 13 (00001101)
清除第2位: 8 (00001000)
翻转第0位: 13 (00001101)
去除最右边的1: 8 (00001000)
最右边的1: 4 (00000100)
```

**复杂度**：所有操作都是 `O(1)`

---

### 例题 2：统计二进制中1的个数

**题目**：给定整数 n，统计其二进制表示中1的个数。

**思路**：不断去除最右边的1。

```cpp
#include <bits/stdc++.h>
using namespace std;

// 方法1：逐位检查
int count_ones_v1(int n) {
    int count = 0;
    while (n) {
        count += n & 1;
        n >>= 1;
    }
    return count;
}

// 方法2：Brian Kernighan 算法
int count_ones_v2(int n) {
    int count = 0;
    while (n) {
        n &= n - 1;  // 去除最右边的1
        count++;
    }
    return count;
}

// 方法3：内置函数
int count_ones_v3(int n) {
    return __builtin_popcount(n);
}

int main() {
    int n;
    cin >> n;
    
    cout << "二进制: " << bitset<32>(n) << "\n";
    cout << "1的个数: " << count_ones_v2(n) << "\n";
    
    return 0;
}
```

**复杂度**：
- 方法1：`O(log n)` - 位数
- 方法2：`O(k)` - k 是1的个数
- 方法3：`O(1)` - 内置指令

**易错点**：负数的处理，需要用 `unsigned` 或处理符号位

---

### 例题 3：只出现一次的数字

**题目**：数组中每个元素都出现两次，只有一个元素出现一次，找出它。

**思路**：异或运算，`a ^ a = 0`，`a ^ 0 = a`。

```cpp
#include <bits/stdc++.h>
using namespace std;

int single_number(vector<int>& nums) {
    int res = 0;
    for (int num : nums) {
        res ^= num;
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
    
    cout << single_number(nums) << "\n";
    return 0;
}
```

**复杂度**：时间 `O(n)`，空间 `O(1)`

**易错点**：异或满足交换律和结合律

---

### 例题 4：只出现一次的数字 II

**题目**：数组中每个元素都出现三次，只有一个元素出现一次，找出它。

**思路**：统计每一位上1出现的次数，对3取模。

```cpp
#include <bits/stdc++.h>
using namespace std;

int single_number_ii(vector<int>& nums) {
    int res = 0;
    
    for (int i = 0; i < 32; ++i) {
        int count = 0;
        for (int num : nums) {
            count += (num >> i) & 1;
        }
        if (count % 3 != 0) {
            res |= (1 << i);
        }
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
    
    cout << single_number_ii(nums) << "\n";
    return 0;
}
```

**复杂度**：时间 `O(32n) = O(n)`，空间 `O(1)`

---

### 例题 5：两个数字只出现一次

**题目**：数组中有两个元素只出现一次，其他都出现两次，找出这两个数。

**思路**：先全部异或得到 `a ^ b`，然后按某一位分组。

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> single_number_iii(vector<int>& nums) {
    int xor_result = 0;
    for (int num : nums) {
        xor_result ^= num;
    }
    
    // 找到最右边的1（两个数在这一位不同）
    int rightmost_bit = xor_result & -xor_result;
    
    int num1 = 0, num2 = 0;
    for (int num : nums) {
        if (num & rightmost_bit) {
            num1 ^= num;
        } else {
            num2 ^= num;
        }
    }
    
    return {num1, num2};
}

int main() {
    int n;
    cin >> n;
    vector<int> nums(n);
    
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    
    auto result = single_number_iii(nums);
    cout << result[0] << " " << result[1] << "\n";
    
    return 0;
}
```

**复杂度**：时间 `O(n)`，空间 `O(1)`

**易错点**：用 `rightmost_bit` 分组，而不是用值的大小

---

### 例题 6：子集生成（状态压缩）

**题目**：给定集合 {1, 2, 3}，生成所有子集。

**思路**：用二进制位表示元素是否在子集中。

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<vector<int>> subsets(vector<int>& nums) {
    int n = nums.size();
    vector<vector<int>> result;
    
    // 遍历所有可能的状态：0 到 2^n - 1
    for (int mask = 0; mask < (1 << n); ++mask) {
        vector<int> subset;
        for (int i = 0; i < n; ++i) {
            if (mask & (1 << i)) {
                subset.push_back(nums[i]);
            }
        }
        result.push_back(subset);
    }
    
    return result;
}

int main() {
    vector<int> nums = {1, 2, 3};
    auto result = subsets(nums);
    
    cout << "所有子集:\n";
    for (const auto& subset : result) {
        cout << "[";
        for (int i = 0; i < subset.size(); ++i) {
            cout << subset[i];
            if (i < subset.size() - 1) cout << ", ";
        }
        cout << "]\n";
    }
    
    return 0;
}
```

**复杂度**：时间 `O(n * 2^n)`，空间 `O(2^n)`

**易错点**：`1 << n` 是 2^n，要加括号

---

### 例题 7：汉明距离

**题目**：两个整数之间的汉明距离是对应位不同的位置数量。

**思路**：异或后统计1的个数。

```cpp
#include <bits/stdc++.h>
using namespace std;

int hamming_distance(int x, int y) {
    int xor_result = x ^ y;
    int count = 0;
    
    while (xor_result) {
        xor_result &= xor_result - 1;
        count++;
    }
    
    return count;
}

// 或者用内置函数
int hamming_distance_v2(int x, int y) {
    return __builtin_popcount(x ^ y);
}

int main() {
    int x, y;
    cin >> x >> y;
    
    cout << "汉明距离: " << hamming_distance(x, y) << "\n";
    return 0;
}
```

**复杂度**：时间 `O(log n)`，空间 `O(1)`

---

### 例题 8：位运算实现加法（不用+运算符）

**题目**：不使用 + 和 - 运算符，实现两数相加。

**思路**：
- `a ^ b` 得到无进位和
- `(a & b) << 1` 得到进位

```cpp
#include <bits/stdc++.h>
using namespace std;

int add(int a, int b) {
    while (b != 0) {
        int sum = a ^ b;          // 无进位和
        int carry = (a & b) << 1; // 进位
        a = sum;
        b = carry;
    }
    return a;
}

int main() {
    int a, b;
    cin >> a >> b;
    
    cout << a << " + " << b << " = " << add(a, b) << "\n";
    return 0;
}
```

**复杂度**：时间 `O(log n)`，空间 `O(1)`

**易错点**：负数处理需要特别注意

---

## 位运算技巧总结

### 常用操作

```cpp
// 判断奇偶
bool is_odd = n & 1;

// 快速乘除2的幂
int mul_2 = n << 1;    // n * 2
int div_2 = n >> 1;    // n / 2
int mul_4 = n << 2;    // n * 4

// 判断2的幂
bool is_power_of_2 = (n > 0) && (n & (n - 1)) == 0;

// 交换两个数（不用中间变量）
a ^= b;
b ^= a;
a ^= b;

// 取绝对值
int abs_val = (n ^ (n >> 31)) - (n >> 31);

// 取反加1 = 求相反数
int neg = ~n + 1;

// 两个数的平均值
int avg = (a + b) >> 1;  // 注意溢出

// 判断符号是否相同
bool same_sign = (a ^ b) >= 0;
```

### 集合操作

假设用整数表示集合，第 i 位为1表示元素 i 在集合中。

```cpp
int S = 0;  // 空集

// 添加元素 i
S |= (1 << i);

// 删除元素 i
S &= ~(1 << i);

// 判断元素 i 是否在集合中
bool contains = (S >> i) & 1;

// 翻转元素 i
S ^= (1 << i);

// 并集
int union_set = A | B;

// 交集
int intersection = A & B;

// 差集（A中有但B中没有）
int difference = A & ~B;

// 对称差（恰好在一个集合中）
int symmetric_diff = A ^ B;

// 清空最右边的1
S &= S - 1;

// 提取最右边的1
int rightmost = S & -S;

// 遍历集合中的所有元素
for (int i = 0; i < n; ++i) {
    if (S & (1 << i)) {
        // 元素 i 在集合中
    }
}

// 遍历所有子集
for (int subset = S; subset; subset = (subset - 1) & S) {
    // subset 是 S 的一个子集
}
```

## 常见陷阱

1. **运算符优先级**：
   - `&` 和 `|` 优先级低于比较运算符，要加括号
   - 错误：`if (n & 1 == 0)` 
   - 正确：`if ((n & 1) == 0)`

2. **左移溢出**：
   - `1 << 31` 可能溢出，用 `1LL << 31`
   - `1 << n` 当 n >= 32 时未定义

3. **负数右移**：
   - 算术右移（填充符号位）vs 逻辑右移（填充0）
   - C++ 中有符号数右移是算术右移

4. **符号位**：
   - 负数的补码表示要注意
   - `-n = ~n + 1`

5. **整数类型**：
   - `int` 通常32位，`long long` 64位
   - 位运算超出范围会截断

## 内置函数（GCC）

```cpp
// 统计1的个数
__builtin_popcount(x)      // int
__builtin_popcountll(x)    // long long

// 前导0的个数（左边）
__builtin_clz(x)           // int
__builtin_clzll(x)         // long long

// 后导0的个数（右边）
__builtin_ctz(x)           // int
__builtin_ctzll(x)         // long long

// 奇偶校验（1的个数的奇偶性）
__builtin_parity(x)        // int
__builtin_parityll(x)      // long long
```

## 适用场景总结

- **判断性质**：奇偶、2的幂、符号
- **快速运算**：乘除2、交换、求反
- **集合表示**：状态压缩 DP、子集枚举
- **数字处理**：去重、找唯一元素
- **优化空间**：用位表示状态，节省内存
- **哈希/校验**：位运算可以用于哈希函数
- **图论**：用位表示访问状态、连通性
