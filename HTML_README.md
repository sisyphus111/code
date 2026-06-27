# 算法竞赛学习文档 - HTML版本

## 已创建的HTML文档

### 特辑文档（4个）

1. **special-exam-environment.html** - 机考环境全流程
   - 考场准备（IDE配置、常用设置、模板准备）
   - 在线环境介绍（洛谷、牛客、各高校OJ）
   - 调试技巧（assert、cerr、条件编译）
   - 时间分配策略（先易后难、部分分策略）
   - 常见环境问题（编译器版本、头文件、超时问题）

2. **special-io-mastery.html** - 输入输出专精
   - ACM/OI模式 vs LeetCode模式
   - 读到EOF、多组输入、整行读取
   - 输出格式陷阱（行末空格、精度、换行）
   - 快速IO技巧
   - 字符串流应用
   - 边界情况处理

3. **special-stl-advanced.html** - C++ STL深度使用
   - 容器性能对比（实测数据）
   - 常见误区（size()无符号、map[]副作用、迭代器失效）
   - 高级用法（lambda、结构化绑定、自定义比较器）
   - STL算法库（partition、nth_element等不常见但有用的）
   - 内存和性能优化

4. **special-debug-techniques.html** - 调试与对拍技巧
   - 打印调试技巧
   - 二分调试法
   - 对拍脚本编写
   - 随机数据生成
   - 边界用例构造

### 索引文档

5. **leetcode-hot100-index.html** - LeetCode Hot 100索引
   - Hot 100题目列表（按难度/类型分类）
   - 每题映射到对应的文档章节
   - 标注难度、考频、知识点
   - 可筛选、搜索功能

6. **index.html** - 主页索引
   - 所有文档的导航页面
   - 卡片式布局，方便访问
   - 分类展示特辑、题型、资源

## 功能特性

### 现代化设计
- ✅ 响应式布局（支持手机、平板、电脑）
- ✅ 侧边栏导航（固定，可展开/折叠）
- ✅ 代码高亮（使用highlight.js）
- ✅ 目录跳转（自动高亮当前章节）
- ✅ 夜间模式切换（自动保存偏好）
- ✅ 打印友好样式
- ✅ 顶部进度条（显示阅读进度）

### 交互功能
- 侧边栏可折叠
- 代码块自动高亮
- 平滑滚动
- 主题自动保存到localStorage
- LeetCode索引支持筛选和搜索

## 使用方法

### 本地浏览
1. 直接用浏览器打开 `index.html`
2. 点击卡片导航到相应文档

### 在线部署
可以将所有HTML文件部署到：
- GitHub Pages
- Netlify
- Vercel
- 任何静态网站托管服务

### 推荐浏览器
- Chrome / Edge（推荐）
- Firefox
- Safari

## 文档结构

```
summer_camp_coding/
├── index.html                          # 主页
├── special-exam-environment.html       # 机考环境
├── special-io-mastery.html            # 输入输出
├── special-stl-advanced.html          # STL深度
├── special-debug-techniques.html      # 调试技巧
├── leetcode-hot100-index.html         # LeetCode索引
├── 01-simulation.html                 # （待转换）
├── 02-hash-and-counting.html          # （待转换）
├── ...                                # 其他章节
├── templates.html                     # （待转换）
├── cpp-stl.html                       # （待转换）
└── io-handling.html                   # （待转换）
```

## 下一步工作

如果需要将现有的Markdown文档（01-18章节、templates.md等）转换为HTML格式：

1. 可以使用类似的Python脚本批量转换
2. 保持统一的样式和布局
3. 添加代码高亮和交互功能

## 技术栈

- **HTML5** - 语义化标记
- **CSS3** - 现代样式（CSS变量、Grid、Flexbox）
- **JavaScript** - 原生JS（无依赖框架）
- **Highlight.js** - 代码高亮（CDN加载）

## 样式特点

- 使用CSS变量实现主题切换
- GitHub风格的代码高亮
- 卡片式布局
- 渐变色英雄区块
- 悬停动画效果

## 浏览器兼容性

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 许可证

与原Markdown文档相同

## 更新日期

2026-06-28
