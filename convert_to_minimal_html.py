#!/usr/bin/env python3
"""
将Markdown文件转换为极简HTML格式
"""

import re
import os
from pathlib import Path

# 文档结构定义
CHAPTERS = [
    ("01-simulation.md", "01 模拟与枚举"),
    ("02-hash-and-counting.md", "02 哈希表与计数"),
    ("03-two-pointers-sliding-window.md", "03 双指针与滑动窗口"),
    ("04-prefix-sum-difference.md", "04 前缀和与差分"),
    ("05-binary-search.md", "05 二分查找与二分答案"),
    ("06-stack-queue-monotonic.md", "06 栈、队列与单调结构"),
    ("07-heap-greedy.md", "07 堆与贪心"),
    ("08-dfs-backtrack.md", "08 DFS与回溯"),
    ("09-bfs-grid.md", "09 BFS与网格问题"),
    ("10-union-find.md", "10 并查集"),
    ("11-graph-traversal.md", "11 图的遍历与连通性"),
    ("12-shortest-path.md", "12 最短路径"),
    ("13-topological-sort.md", "13 拓扑排序与DAG"),
    ("14-dynamic-programming.md", "14 动态规划"),
    ("15-tree.md", "15 树"),
    ("16-advanced-data-structures.md", "16 高级数据结构"),
    ("17-math-number-theory.md", "17 数学与数论"),
    ("18-bit-manipulation.md", "18 位运算"),
]

SPECIAL_TOPICS = [
    ("io-handling.md", "输入输出处理"),
    ("cpp-stl.md", "C++ STL使用"),
    ("templates.md", "算法模板库"),
]

def escape_html(text):
    """转义HTML特殊字符"""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))

def convert_markdown_to_html(md_content):
    """将Markdown转换为HTML"""
    html_parts = []
    lines = md_content.split('\n')
    i = 0
    in_code_block = False
    code_lines = []
    in_list = False
    in_table = False
    table_lines = []

    while i < len(lines):
        line = lines[i]

        # 代码块处理
        if line.startswith('```'):
            if in_code_block:
                # 结束代码块
                code_content = '\n'.join(code_lines)
                html_parts.append(f'<pre><code>{escape_html(code_content)}</code></pre>')
                code_lines = []
                in_code_block = False
            else:
                # 开始代码块
                in_code_block = True
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        # 表格处理
        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(line)
            i += 1
            # 检查下一行是否还是表格
            if i < len(lines) and '|' in lines[i]:
                continue
            else:
                # 表格结束，生成HTML
                html_parts.append(convert_table(table_lines))
                in_table = False
                table_lines = []
                continue

        # 标题处理
        if line.startswith('# '):
            html_parts.append(f'<h1>{escape_html(line[2:])}</h1>')
        elif line.startswith('## '):
            html_parts.append(f'<h2>{escape_html(line[3:])}</h2>')
        elif line.startswith('### '):
            html_parts.append(f'<h3>{escape_html(line[4:])}</h3>')
        elif line.startswith('#### '):
            html_parts.append(f'<h4>{escape_html(line[5:])}</h4>')

        # 列表处理
        elif line.startswith('- ') or re.match(r'^\d+\. ', line):
            if not in_list:
                if line.startswith('- '):
                    html_parts.append('<ul>')
                else:
                    html_parts.append('<ol>')
                in_list = True

            if line.startswith('- '):
                content = process_inline_formatting(line[2:])
                html_parts.append(f'<li>{content}</li>')
            else:
                content = process_inline_formatting(re.sub(r'^\d+\. ', '', line))
                html_parts.append(f'<li>{content}</li>')

            # 检查下一行是否还是列表
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                if not (next_line.startswith('- ') or re.match(r'^\d+\. ', next_line)):
                    if line.startswith('- '):
                        html_parts.append('</ul>')
                    else:
                        html_parts.append('</ol>')
                    in_list = False
            else:
                if line.startswith('- '):
                    html_parts.append('</ul>')
                else:
                    html_parts.append('</ol>')
                in_list = False

        # 空行
        elif line.strip() == '':
            if in_list:
                html_parts.append('</ul>' if html_parts[-1].startswith('<li>') else '</ol>')
                in_list = False

        # 普通段落
        elif line.strip():
            content = process_inline_formatting(line)
            html_parts.append(f'<p>{content}</p>')

        i += 1

    return '\n'.join(html_parts)

def convert_table(table_lines):
    """转换表格"""
    if len(table_lines) < 2:
        return ''

    html = ['<table>']

    # 处理表头
    header = table_lines[0].strip().strip('|').split('|')
    html.append('<thead><tr>')
    for cell in header:
        html.append(f'<th>{escape_html(cell.strip())}</th>')
    html.append('</tr></thead>')

    # 跳过分隔行
    html.append('<tbody>')
    for line in table_lines[2:]:
        if '|' in line:
            cells = line.strip().strip('|').split('|')
            html.append('<tr>')
            for cell in cells:
                html.append(f'<td>{process_inline_formatting(cell.strip())}</td>')
            html.append('</tr>')
    html.append('</tbody>')
    html.append('</table>')

    return '\n'.join(html)

def process_inline_formatting(text):
    """处理行内格式：粗体、代码、链接等"""
    # 行内代码
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)

    # 粗体
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)

    # 斜体
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)

    # 链接
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', text)

    return text

def create_html(title, content, prev_link=None, next_link=None):
    """创建完整的HTML页面"""

    # 导航链接
    nav_links = ['<a href="index.html">← 返回主页</a>']

    nav_top = f'''<div class="nav">
        <a href="index.html">← 返回主页</a>
    </div>'''

    nav_bottom_links = []
    if prev_link:
        nav_bottom_links.append(f'<a href="{prev_link[0]}">← {prev_link[1]}</a>')
    if next_link:
        nav_bottom_links.append(f'<a href="{next_link[0]}">{next_link[1]} →</a>')

    nav_bottom = ''
    if nav_bottom_links:
        nav_bottom = f'''<div class="nav">
        {' | '.join(nav_bottom_links)}
    </div>'''

    html_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - C++算法竞赛</title>
    <style>
        body {{
            max-width: 900px;
            margin: 40px auto;
            padding: 0 20px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            font-size: 16px;
            line-height: 1.6;
            color: #333;
        }}

        h1 {{ font-size: 32px; margin: 40px 0 20px; border-bottom: 2px solid #333; padding-bottom: 10px; }}
        h2 {{ font-size: 24px; margin: 30px 0 15px; }}
        h3 {{ font-size: 20px; margin: 20px 0 10px; }}
        h4 {{ font-size: 18px; margin: 20px 0 10px; }}

        p {{ margin: 10px 0; }}

        pre {{
            background: #f5f5f5;
            border: 1px solid #ddd;
            border-radius: 3px;
            padding: 15px;
            overflow-x: auto;
            font-size: 14px;
            line-height: 1.4;
            margin: 15px 0;
        }}

        code {{
            background: #f5f5f5;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: "SF Mono", Monaco, Consolas, monospace;
            font-size: 14px;
        }}

        pre code {{
            background: none;
            padding: 0;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}

        th, td {{
            border: 1px solid #ddd;
            padding: 8px 12px;
            text-align: left;
        }}

        th {{
            background: #f5f5f5;
            font-weight: 600;
        }}

        ul, ol {{
            margin: 10px 0;
            padding-left: 30px;
        }}

        li {{
            margin: 5px 0;
        }}

        a {{
            color: #0066cc;
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        strong {{
            font-weight: 600;
        }}

        .nav {{
            margin: 40px 0;
            padding: 15px 0;
            border-top: 1px solid #ddd;
            border-bottom: 1px solid #ddd;
        }}

        .nav a {{
            margin-right: 20px;
        }}

        @media print {{
            body {{ margin: 0; padding: 20px; }}
            .nav {{ display: none; }}
        }}
    </style>
</head>
<body>
    {nav_top}

    {content}

    {nav_bottom}
</body>
</html>'''

    return html_template

def create_index_page():
    """创建主页"""
    content = '''<h1>C++ 算法竞赛学习文档</h1>

    <p>面向研究生夏令营机试、保研机考的系统性学习材料。</p>

    <h2>核心章节</h2>
    <ol>'''

    for filename, title in CHAPTERS:
        html_name = filename.replace('.md', '.html')
        content += f'\n        <li><a href="{html_name}">{title}</a></li>'

    content += '''
    </ol>

    <h2>附录</h2>
    <ul>'''

    for filename, title in SPECIAL_TOPICS:
        html_name = filename.replace('.md', '.html')
        content += f'\n        <li><a href="{html_name}">{title}</a></li>'

    content += '''
    </ul>

    <h2>使用建议</h2>
    <p><strong>学习路径：</strong></p>
    <ol>
        <li>先看附录（输入输出、STL）了解基础</li>
        <li>按章节顺序学习（01→18）</li>
        <li>重点突破动态规划（第14章）</li>
        <li>考前复习使用算法模板库</li>
    </ol>

    <p><strong>练习方法：</strong></p>
    <ul>
        <li>每个例题自己敲一遍代码</li>
        <li>限时训练：2-3小时完成3-4题</li>
        <li>总结每个题型的识别特征</li>
        <li>反复练习不熟练的模板</li>
    </ul>'''

    return create_html('主页', content)

def main():
    """主函数"""
    base_dir = Path('/Users/sisyphus_2/dev/summer_camp_coding')

    # 创建主页
    print("创建主页...")
    index_html = create_index_page()
    with open(base_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    print("✓ index.html")

    # 转换所有章节
    all_docs = CHAPTERS + SPECIAL_TOPICS

    for idx, (filename, title) in enumerate(all_docs):
        md_path = base_dir / filename
        if not md_path.exists():
            print(f"⚠ 文件不存在: {filename}")
            continue

        print(f"转换: {filename}...")

        # 读取Markdown
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # 转换为HTML
        html_content = convert_markdown_to_html(md_content)

        # 确定上一页和下一页
        prev_link = None
        next_link = None

        if idx > 0:
            prev_file = all_docs[idx - 1][0].replace('.md', '.html')
            prev_title = all_docs[idx - 1][1]
            prev_link = (prev_file, prev_title)

        if idx < len(all_docs) - 1:
            next_file = all_docs[idx + 1][0].replace('.md', '.html')
            next_title = all_docs[idx + 1][1]
            next_link = (next_file, next_title)

        # 生成完整HTML
        full_html = create_html(title, html_content, prev_link, next_link)

        # 写入文件
        html_path = base_dir / filename.replace('.md', '.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(full_html)

        print(f"✓ {html_path.name}")

    print("\n转换完成！")
    print(f"共生成 {len(all_docs) + 1} 个HTML文件")

if __name__ == '__main__':
    main()
