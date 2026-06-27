# 数学与数论

## 什么时候用

看到以下特征优先考虑数学与数论：
- 最大公约数（GCD）、最小公倍数（LCM）
- 质数判断、质因数分解、筛法
- 快速幂、矩阵快速幂
- 组合数、排列数、阶乘
- 模运算、逆元
- 欧拉函数、费马小定理
- 数位 DP、进制转换

核心思路：**利用数学性质和公式优化计算**。

## 核心要点

1. **GCD 用辗转相除法**：`gcd(a, b) = gcd(b, a % b)`
2. **质数判断**：试除法 `O(√n)`，筛法 `O(n log log n)`
3. **快速幂**：`O(log n)` 计算 `a^b`
4. **组合数**：预处理阶乘和逆元
5. **模运算**：加减乘取模，除法用逆元
6. **费马小定理**：`a^(p-1) ≡ 1 (mod p)`，p 为质数

## 例题演示

### 例题 1：最大公约数 GCD 与最小公倍数 LCM

**题目**：给定两个数，求 GCD 和 LCM。

**思路**：辗转相除法求 GCD，`LCM = a * b / GCD`。

```cpp
#include <bits/stdc++.h>
using namespace std;

int gcd(int a, int b) {
    return b == 0 ? a : gcd(b, a % b);
}

long long lcm(int a, int b) {
    return (long long)a * b / gcd(a, b);
}

int main() {
    int a, b;
    cin >> a >> b;
    
    cout << "GCD: " << gcd(a, b) << "\n";
    cout << "LCM: " << lcm(a, b) << "\n";
    
    return 0;
}
```

**C++ 内置函数**：
- `__gcd(a, b)` - GCC 内置
- `gcd(a, b)` - C++17 `<numeric>` 中

**复杂度**：`O(log min(a, b))`

**易错点**：计算 LCM 时先除后乘，避免溢出

---

### 例题 2：质数判断

**题目**：判断 n 是否为质数。

**思路**：试除法，只需要检查到 `√n`。

```cpp
#include <bits/stdc++.h>
using namespace std;

bool is_prime(int n) {
    if (n < 2) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;
    
    for (int i = 3; i * i <= n; i += 2) {
        if (n % i == 0) return false;
    }
    
    return true;
}

int main() {
    int n;
    cin >> n;
    cout << (is_prime(n) ? "YES" : "NO") << "\n";
    return 0;
}
```

**复杂度**：`O(√n)`

**优化**：只检查奇数，跳过偶数

---

### 例题 3：埃氏筛法 - 求 n 以内所有质数

**题目**：求 1 到 n 的所有质数。

**思路**：Sieve of Eratosthenes，标记质数的倍数。

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> sieve_of_eratosthenes(int n) {
    vector<bool> is_prime(n + 1, true);
    is_prime[0] = is_prime[1] = false;
    
    for (int i = 2; i * i <= n; ++i) {
        if (is_prime[i]) {
            for (int j = i * i; j <= n; j += i) {
                is_prime[j] = false;
            }
        }
    }
    
    vector<int> primes;
    for (int i = 2; i <= n; ++i) {
        if (is_prime[i]) {
            primes.push_back(i);
        }
    }
    
    return primes;
}

int main() {
    int n;
    cin >> n;
    
    auto primes = sieve_of_eratosthenes(n);
    
    cout << "质数个数: " << primes.size() << "\n";
    for (int p : primes) {
        cout << p << " ";
    }
    cout << "\n";
    
    return 0;
}
```

**复杂度**：`O(n log log n)`

**易错点**：从 `i * i` 开始标记，因为更小的倍数已经被标记过

---

### 例题 4：质因数分解

**题目**：将 n 分解为质因数。

**思路**：从 2 开始试除，记录每个质因数的个数。

```cpp
#include <bits/stdc++.h>
using namespace std;

map<int, int> prime_factorization(int n) {
    map<int, int> factors;
    
    for (int i = 2; i * i <= n; ++i) {
        while (n % i == 0) {
            factors[i]++;
            n /= i;
        }
    }
    
    if (n > 1) {
        factors[n]++;
    }
    
    return factors;
}

int main() {
    int n;
    cin >> n;
    
    auto factors = prime_factorization(n);
    
    cout << n << " = ";
    bool first = true;
    for (auto [p, cnt] : factors) {
        if (!first) cout << " * ";
        cout << p;
        if (cnt > 1) cout << "^" << cnt;
        first = false;
    }
    cout << "\n";
    
    return 0;
}
```

**复杂度**：`O(√n)`

**易错点**：最后要检查 `n > 1`，剩余的 n 本身是质数

---

### 例题 5：快速幂

**题目**：计算 `a^b mod m`。

**思路**：二进制拆分，`a^b = a^(b/2) * a^(b/2) * a^(b%2)`。

```cpp
#include <bits/stdc++.h>
using namespace std;

long long fast_pow(long long a, long long b, long long mod) {
    long long res = 1;
    a %= mod;
    
    while (b > 0) {
        if (b & 1) {
            res = res * a % mod;
        }
        a = a * a % mod;
        b >>= 1;
    }
    
    return res;
}

int main() {
    long long a, b, mod;
    cin >> a >> b >> mod;
    
    cout << fast_pow(a, b, mod) << "\n";
    return 0;
}
```

**复杂度**：`O(log b)`

**易错点**：
- 每次乘法后都要取模
- `a` 也要先取模

---

### 例题 6：组合数 C(n, m)

**题目**：计算组合数 `C(n, m) = n! / (m! * (n-m)!)`。

**思路 1：预处理阶乘（n 较小时）**

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 1e6 + 5;
const int MOD = 1e9 + 7;

long long fact[MAXN], inv_fact[MAXN];

long long fast_pow(long long a, long long b, long long mod) {
    long long res = 1;
    a %= mod;
    while (b > 0) {
        if (b & 1) res = res * a % mod;
        a = a * a % mod;
        b >>= 1;
    }
    return res;
}

void init() {
    fact[0] = 1;
    for (int i = 1; i < MAXN; ++i) {
        fact[i] = fact[i - 1] * i % MOD;
    }
    
    inv_fact[MAXN - 1] = fast_pow(fact[MAXN - 1], MOD - 2, MOD);
    for (int i = MAXN - 2; i >= 0; --i) {
        inv_fact[i] = inv_fact[i + 1] * (i + 1) % MOD;
    }
}

long long comb(int n, int m) {
    if (m < 0 || m > n) return 0;
    return fact[n] * inv_fact[m] % MOD * inv_fact[n - m] % MOD;
}

int main() {
    init();
    
    int n, m;
    cin >> n >> m;
    
    cout << comb(n, m) << "\n";
    return 0;
}
```

**思路 2：递推（小范围）**

```cpp
long long comb_recursive(int n, int m) {
    if (m == 0 || m == n) return 1;
    
    vector<vector<long long>> C(n + 1, vector<long long>(m + 1, 0));
    
    for (int i = 0; i <= n; ++i) {
        C[i][0] = 1;
        for (int j = 1; j <= min(i, m); ++j) {
            C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % MOD;
        }
    }
    
    return C[n][m];
}
```

**复杂度**：
- 预处理：`O(n)`，查询 `O(1)`
- 递推：`O(nm)`

**易错点**：除法要用逆元，逆元用费马小定理：`a^(-1) = a^(p-2) mod p`

---

### 例题 7：欧拉函数 φ(n)

**题目**：求小于等于 n 且与 n 互质的数的个数。

**思路**：`φ(n) = n * ∏(1 - 1/p)`，p 为 n 的质因数。

```cpp
#include <bits/stdc++.h>
using namespace std;

int euler_phi(int n) {
    int res = n;
    
    for (int i = 2; i * i <= n; ++i) {
        if (n % i == 0) {
            res = res / i * (i - 1);
            while (n % i == 0) {
                n /= i;
            }
        }
    }
    
    if (n > 1) {
        res = res / n * (n - 1);
    }
    
    return res;
}

int main() {
    int n;
    cin >> n;
    cout << euler_phi(n) << "\n";
    return 0;
}
```

**批量计算（筛法）**：

```cpp
vector<int> euler_phi_sieve(int n) {
    vector<int> phi(n + 1);
    for (int i = 0; i <= n; ++i) phi[i] = i;
    
    for (int i = 2; i <= n; ++i) {
        if (phi[i] == i) {  // i 是质数
            for (int j = i; j <= n; j += i) {
                phi[j] = phi[j] / i * (i - 1);
            }
        }
    }
    
    return phi;
}
```

**复杂度**：单次 `O(√n)`，筛法 `O(n log log n)`

---

### 例题 8：扩展欧几里得算法

**题目**：求解 `ax + by = gcd(a, b)`，求 x 和 y。

**思路**：递归求解。

```cpp
#include <bits/stdc++.h>
using namespace std;

int exgcd(int a, int b, int& x, int& y) {
    if (b == 0) {
        x = 1;
        y = 0;
        return a;
    }
    
    int d = exgcd(b, a % b, y, x);
    y -= a / b * x;
    return d;
}

int main() {
    int a, b;
    cin >> a >> b;
    
    int x, y;
    int d = exgcd(a, b, x, y);
    
    cout << "gcd(" << a << ", " << b << ") = " << d << "\n";
    cout << a << " * " << x << " + " << b << " * " << y << " = " << d << "\n";
    
    return 0;
}
```

**应用**：求逆元、线性同余方程

**复杂度**：`O(log min(a, b))`

---

## 常见陷阱

1. **整数溢出**：
   - `a * b` 可能溢出，先除后乘：`a / gcd(a, b) * b`
   - 快速幂中每次都要取模
2. **除法取模**：不能直接除，要用逆元
3. **质数判断**：不要忘记 2 是质数
4. **筛法优化**：从 `i * i` 开始标记
5. **组合数溢出**：大数要取模，用逆元
6. **欧拉函数**：`φ(1) = 1`
7. **模运算**：
   - `(a + b) % m = (a % m + b % m) % m`
   - `(a * b) % m = (a % m * b % m) % m`
   - `(a - b) % m = ((a % m - b % m) + m) % m`

## 常用公式

### GCD 性质
- `gcd(a, b) = gcd(b, a % b)`
- `gcd(a, b) * lcm(a, b) = a * b`
- `gcd(ka, kb) = k * gcd(a, b)`

### 组合数性质
- `C(n, m) = C(n-1, m-1) + C(n-1, m)`
- `C(n, m) = C(n, n-m)`
- `C(n, 0) = C(n, n) = 1`

### 欧拉函数性质
- `φ(1) = 1`
- `φ(p) = p - 1`（p 为质数）
- `φ(p^k) = p^k - p^(k-1)`
- 若 `gcd(a, b) = 1`，则 `φ(ab) = φ(a) * φ(b)`

### 费马小定理
- 若 p 为质数，`a^(p-1) ≡ 1 (mod p)`
- 逆元：`a^(-1) ≡ a^(p-2) (mod p)`

## 模运算技巧

```cpp
// 加法
int add(int a, int b, int mod) {
    return (a + b) % mod;
}

// 减法
int sub(int a, int b, int mod) {
    return ((a - b) % mod + mod) % mod;
}

// 乘法
long long mul(long long a, long long b, long long mod) {
    return (a * b) % mod;
}

// 除法（需要逆元）
long long div(long long a, long long b, long long mod) {
    return a * fast_pow(b, mod - 2, mod) % mod;
}
```

## 适用场景总结

- **GCD/LCM**：公约数、公倍数问题
- **质数判断**：素数相关问题
- **筛法**：批量求质数、欧拉函数
- **快速幂**：大指数幂运算、矩阵快速幂
- **组合数**：排列组合、概率计算
- **欧拉函数**：互质数个数、欧拉定理
- **扩展欧几里得**：求逆元、线性同余方程
- **费马小定理**：逆元、欧拉定理
