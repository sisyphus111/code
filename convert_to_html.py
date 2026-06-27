#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量将Markdown文件转换为HTML格式
使用与特辑文档相同的模板和样式
"""

import re
import os

# 题型章节映射（用于导航）
CHAPTERS = [
    ("01-simulation", "模拟与枚举"),
    ("02-hash-and-counting", "哈希表与计数"),
    ("03-two-pointers-sliding-window", "双指针与滑动窗口"),
    ("04-prefix-sum-difference", "前缀和与差分"),
    ("05-binary-search", "二分查找"),
    ("06-stack-queue-monotonic", "栈队列与单调性"),
    ("07-heap-greedy", "堆与贪心"),
    ("08-dfs-backtrack", "DFS与回溯"),
    ("09-bfs-grid", "BFS与网格"),
    ("10-union-find", "并查集"),
    ("11-graph-traversal", "图遍历"),
    ("12-shortest-path", "最短路径"),
    ("13-topological-sort", "拓扑排序"),
    ("14-dynamic-programming", "动态规划"),
    ("15-tree", "树"),
    ("16-advanced-data-structures", "高级数据结构"),
    ("17-math-number-theory", "数学与数论"),
    ("18-bit-manipulation", "位运算"),
]

# 配套文档映射
SUPPORT_DOCS = [
    ("templates", "算法模板库"),
    ("cpp-stl", "C++ STL使用指南"),
    ("io-handling", "输入输出处理"),
]

def escape_html(text):
    """转义HTML特殊字符"""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))

def parse_markdown(md_content):
    """解析Markdown内容，提取标题和内容"""
    lines = md_content.split('\n')
    title = "文档"
    sections = []
    current_section = None
    current_content = []
    in_code_block = False
    code_language = ""

    for line in lines:
        # 检测代码块
        if line.strip().startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_language = line.strip()[3:].strip()
                current_content.append(f'<pre><code class="language-{code_language}">')
            else:
                in_code_block = False
                current_content.append('</code></pre>')
            continue

        if in_code_block:
            current_content.append(escape_html(line))
            continue

        # 一级标题
        if line.startswith('# '):
            title = line[2:].strip()
            continue

        # 二级标题 - 新章节
        if line.startswith('## '):
            if current_section:
                sections.append({
                    'id': current_section['id'],
                    'title': current_section['title'],
                    'content': '\n'.join(current_content)
                })
            section_title = line[3:].strip()
            section_id = re.sub(r'[^\w\-]', '', section_title.lower().replace(' ', '-').replace('：', '').replace('/', '-'))
            current_section = {'id': section_id, 'title': section_title}
            current_content = [f'<h2 id="{section_id}">{escape_html(section_title)}</h2>']
            continue

        # 三级标题
        if line.startswith('### '):
            h3_title = line[4:].strip()
            h3_id = re.sub(r'[^\w\-]', '', h3_title.lower().replace(' ', '-'))
            current_content.append(f'<h3 id="{h3_id}">{escape_html(h3_title)}</h3>')
            continue

        # 四级标题
        if line.startswith('#### '):
            h4_title = line[5:].strip()
            current_content.append(f'<h4>{escape_html(h4_title)}</h4>')
            continue

        # 分隔线
        if line.strip() == '---':
            current_content.append('<hr>')
            continue

        # 列表项
        if line.strip().startswith('- ') or line.strip().startswith('* '):
            item = line.strip()[2:]
            # 处理粗体
            item = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', item)
            # 处理行内代码
            item = re.sub(r'`([^`]+)`', r'<code>\1</code>', item)
            if not current_content or not current_content[-1].startswith('<ul'):
                current_content.append('<ul>')
            current_content.append(f'<li>{item}</li>')
            continue

        # 有序列表
        if re.match(r'^\d+\.\s', line.strip()):
            item = re.sub(r'^\d+\.\s+', '', line.strip())
            item = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', item)
            item = re.sub(r'`([^`]+)`', r'<code>\1</code>', item)
            if not current_content or not current_content[-1].startswith('<ol'):
                current_content.append('<ol>')
            current_content.append(f'<li>{item}</li>')
            continue

        # 关闭列表
        if current_content and (current_content[-1] == '</li>'):
            if line.strip() == '':
                if len(current_content) > 1 and current_content[-2].startswith('<ul'):
                    current_content.append('</ul>')
                elif len(current_content) > 1 and current_content[-2].startswith('<ol'):
                    current_content.append('</ol>')

        # 表格
        if '|' in line and line.strip():
            if not current_content or not current_content[-1].startswith('<table'):
                current_content.append('<table>')
                current_content.append('<thead>')
                # 表头
                cells = [c.strip() for c in line.split('|')[1:-1]]
                current_content.append('<tr>')
                for cell in cells:
                    current_content.append(f'<th>{escape_html(cell)}</th>')
                current_content.append('</tr>')
                current_content.append('</thead>')
                current_content.append('<tbody>')
            elif re.match(r'^\|[\s\-:]+\|', line):
                # 分隔行，跳过
                continue
            else:
                # 表格数据行
                cells = [c.strip() for c in line.split('|')[1:-1]]
                current_content.append('<tr>')
                for cell in cells:
                    cell = re.sub(r'`([^`]+)`', r'<code>\1</code>', cell)
                    cell = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', cell)
                    current_content.append(f'<td>{cell}</td>')
                current_content.append('</tr>')
            continue

        # 关闭表格
        if current_content and current_content[-1] == '</tr>' and line.strip() == '':
            current_content.append('</tbody>')
            current_content.append('</table>')

        # 空行
        if line.strip() == '':
            continue

        # 普通段落
        text = line.strip()
        # 处理粗体
        text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
        # 处理行内代码
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        current_content.append(f'<p>{text}</p>')

    # 添加最后一个章节
    if current_section:
        sections.append({
            'id': current_section['id'],
            'title': current_section['title'],
            'content': '\n'.join(current_content)
        })

    return title, sections

def generate_toc(sections):
    """生成目录HTML"""
    toc_html = '<ul class="toc">\n'
    for section in sections:
        toc_html += f'    <li><a href="#{section["id"]}">{escape_html(section["title"])}</a></li>\n'
    toc_html += '</ul>'
    return toc_html

def get_navigation(current_file, is_support=False):
    """生成上一章/下一章导航"""
    nav_html = '<div class="chapter-nav">\n'

    if is_support:
        docs = SUPPORT_DOCS
    else:
        docs = CHAPTERS

    current_idx = -1
    for i, (file_prefix, _) in enumerate(docs):
        if current_file.startswith(file_prefix):
            current_idx = i
            break

    if current_idx > 0:
        prev_file, prev_title = docs[current_idx - 1]
        nav_html += f'    <a href="{prev_file}.html" class="prev-chapter">← {escape_html(prev_title)}</a>\n'

    if current_idx >= 0 and current_idx < len(docs) - 1:
        next_file, next_title = docs[current_idx + 1]
        nav_html += f'    <a href="{next_file}.html" class="next-chapter">{escape_html(next_title)} →</a>\n'

    nav_html += '</div>'
    return nav_html

def generate_html(title, sections, toc_html, nav_html):
    """生成完整HTML"""

    # 拼接所有内容
    main_content = '\n'.join([s['content'] for s in sections])

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape_html(title)} - 算法竞赛速成</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --bg-primary: #ffffff;
            --bg-secondary: #f8f9fa;
            --bg-code: #f6f8fa;
            --text-primary: #24292f;
            --text-secondary: #57606a;
            --border-color: #d0d7de;
            --accent-color: #0969da;
            --accent-hover: #0550ae;
            --sidebar-width: 280px;
            --header-height: 60px;
        }}

        body.dark-mode {{
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-code: #161b22;
            --text-primary: #c9d1d9;
            --text-secondary: #8b949e;
            --border-color: #30363d;
            --accent-color: #58a6ff;
            --accent-hover: #79c0ff;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: var(--text-primary);
            background-color: var(--bg-primary);
            transition: background-color 0.3s, color 0.3s;
        }}

        .progress-bar {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--accent-color) 0%, var(--accent-color) var(--scroll-progress, 0%), transparent var(--scroll-progress, 0%));
            z-index: 1001;
        }}

        header {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: var(--header-height);
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 20px;
            z-index: 1000;
        }}

        .header-title {{
            font-size: 20px;
            font-weight: 600;
            color: var(--text-primary);
        }}

        .header-controls {{
            display: flex;
            gap: 15px;
            align-items: center;
        }}

        .theme-toggle {{
            background: none;
            border: none;
            cursor: pointer;
            font-size: 24px;
            padding: 5px;
            transition: transform 0.2s;
        }}

        .theme-toggle:hover {{
            transform: scale(1.1);
        }}

        .sidebar {{
            position: fixed;
            left: 0;
            top: var(--header-height);
            bottom: 0;
            width: var(--sidebar-width);
            background: var(--bg-secondary);
            border-right: 1px solid var(--border-color);
            overflow-y: auto;
            padding: 20px;
            transition: transform 0.3s;
        }}

        .sidebar.collapsed {{
            transform: translateX(-100%);
        }}

        .sidebar-toggle {{
            position: fixed;
            left: var(--sidebar-width);
            top: calc(var(--header-height) + 20px);
            background: var(--accent-color);
            color: white;
            border: none;
            border-radius: 0 4px 4px 0;
            padding: 10px 8px;
            cursor: pointer;
            z-index: 999;
            transition: left 0.3s;
        }}

        .sidebar.collapsed + .sidebar-toggle {{
            left: 0;
        }}

        .sidebar h3 {{
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            color: var(--text-secondary);
            margin-bottom: 10px;
        }}

        .toc {{
            list-style: none;
        }}

        .toc li {{
            margin: 5px 0;
        }}

        .toc a {{
            color: var(--text-primary);
            text-decoration: none;
            display: block;
            padding: 6px 10px;
            border-radius: 6px;
            transition: background 0.2s;
        }}

        .toc a:hover {{
            background: var(--bg-primary);
        }}

        .toc a.active {{
            background: var(--accent-color);
            color: white;
        }}

        main {{
            margin-left: var(--sidebar-width);
            margin-top: var(--header-height);
            padding: 40px;
            max-width: 900px;
            transition: margin-left 0.3s;
        }}

        .sidebar.collapsed ~ main {{
            margin-left: 0;
        }}

        h1 {{
            font-size: 32px;
            margin-bottom: 10px;
            color: var(--text-primary);
        }}

        h2 {{
            font-size: 24px;
            margin-top: 40px;
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-primary);
        }}

        h3 {{
            font-size: 20px;
            margin-top: 24px;
            margin-bottom: 12px;
            color: var(--text-primary);
        }}

        h4 {{
            font-size: 18px;
            margin-top: 20px;
            margin-bottom: 10px;
            color: var(--text-primary);
        }}

        p {{
            margin: 16px 0;
            color: var(--text-primary);
        }}

        code {{
            background: var(--bg-code);
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace;
            font-size: 0.9em;
        }}

        pre {{
            background: var(--bg-code);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 16px;
            overflow-x: auto;
            margin: 16px 0;
        }}

        pre code {{
            background: none;
            padding: 0;
        }}

        ul, ol {{
            margin: 16px 0;
            padding-left: 32px;
        }}

        li {{
            margin: 8px 0;
        }}

        hr {{
            border: none;
            border-top: 1px solid var(--border-color);
            margin: 24px 0;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
        }}

        th, td {{
            border: 1px solid var(--border-color);
            padding: 8px 12px;
            text-align: left;
        }}

        th {{
            background: var(--bg-secondary);
            font-weight: 600;
        }}

        .chapter-nav {{
            display: flex;
            justify-content: space-between;
            margin: 40px 0;
            padding: 20px 0;
            border-top: 1px solid var(--border-color);
        }}

        .chapter-nav a {{
            color: var(--accent-color);
            text-decoration: none;
            padding: 10px 20px;
            border: 1px solid var(--accent-color);
            border-radius: 6px;
            transition: all 0.2s;
        }}

        .chapter-nav a:hover {{
            background: var(--accent-color);
            color: white;
        }}

        @media print {{
            .sidebar, .sidebar-toggle, .theme-toggle, .progress-bar {{
                display: none;
            }}
            main {{
                margin-left: 0;
                margin-top: 0;
            }}
        }}

        @media (max-width: 768px) {{
            .sidebar {{
                transform: translateX(-100%);
            }}
            .sidebar.show {{
                transform: translateX(0);
            }}
            main {{
                margin-left: 0;
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="progress-bar"></div>

    <header>
        <div class="header-title">{escape_html(title)}</div>
        <div class="header-controls">
            <button class="theme-toggle" onclick="toggleTheme()" title="切换主题">🌓</button>
        </div>
    </header>

    <nav class="sidebar" id="sidebar">
        <h3>目录</h3>
        {toc_html}
    </nav>

    <button class="sidebar-toggle" onclick="toggleSidebar()">☰</button>

    <main>
        <h1>{escape_html(title)}</h1>

        {main_content}

        {nav_html}
    </main>

    <script>
        // 主题切换
        function toggleTheme() {{
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
        }}

        // 加载保存的主题
        if (localStorage.getItem('theme') === 'dark') {{
            document.body.classList.add('dark-mode');
        }}

        // 侧边栏切换
        function toggleSidebar() {{
            document.getElementById('sidebar').classList.toggle('collapsed');
        }}

        // 进度条
        window.addEventListener('scroll', () => {{
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            document.documentElement.style.setProperty('--scroll-progress', scrolled + '%');
        }});

        // 目录高亮
        const sections = document.querySelectorAll('h2[id]');
        const tocLinks = document.querySelectorAll('.toc a');

        window.addEventListener('scroll', () => {{
            let current = '';
            sections.forEach(section => {{
                const sectionTop = section.offsetTop;
                if (scrollY >= sectionTop - 100) {{
                    current = section.getAttribute('id');
                }}
            }});

            tocLinks.forEach(link => {{
                link.classList.remove('active');
                if (link.getAttribute('href') === '#' + current) {{
                    link.classList.add('active');
                }}
            }});
        }});

        // 代码高亮
        hljs.highlightAll();
    </script>
</body>
</html>'''

    return html

def convert_file(md_file, output_dir='/Users/sisyphus_2/dev/summer_camp_coding'):
    """转换单个Markdown文件"""
    md_path = os.path.join(output_dir, md_file)

    # 读取Markdown内容
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 解析Markdown
    title, sections = parse_markdown(md_content)

    # 生成目录
    toc_html = generate_toc(sections)

    # 生成导航
    base_name = md_file.replace('.md', '')
    is_support = base_name in ['templates', 'cpp-stl', 'io-handling']
    nav_html = get_navigation(base_name, is_support)

    # 生成HTML
    html = generate_html(title, sections, toc_html, nav_html)

    # 写入文件
    html_file = md_file.replace('.md', '.html')
    html_path = os.path.join(output_dir, html_file)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return html_file

def main():
    """主函数"""
    output_dir = '/Users/sisyphus_2/dev/summer_camp_coding'

    # 转换所有题型文档
    print("开始转换题型文档...")
    for file_prefix, title in CHAPTERS:
        md_file = f"{file_prefix}.md"
        html_file = convert_file(md_file, output_dir)
        print(f"✓ {md_file} -> {html_file}")

    # 转换配套文档
    print("\n开始转换配套文档...")
    for file_prefix, title in SUPPORT_DOCS:
        md_file = f"{file_prefix}.md"
        html_file = convert_file(md_file, output_dir)
        print(f"✓ {md_file} -> {html_file}")

    print("\n✅ 所有文件转换完成！")

if __name__ == '__main__':
    main()
