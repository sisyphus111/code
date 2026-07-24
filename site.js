const chapters = [
    { file: "00-cpp-project-setup.html", label: "基础 01", title: "单文件 g++ 与多文件 CMake", group: "基础" },
    { file: "io-handling.html", label: "基础 02", title: "输入输出与 CLI 工具", group: "基础" },
    { file: "exception-handling.html", label: "基础 03", title: "异常处理与错误边界", group: "基础" },
    { file: "cpp-stl.html", label: "STL 00", title: "STL 板块总览与速查", group: "STL" },
    { file: "stl-value-semantics.html", label: "STL 01", title: "对象语义、构造与传参", group: "STL" },
    { file: "stl-sequence-containers.html", label: "STL 02", title: "序列容器的底层行为", group: "STL" },
    { file: "stl-associative-containers.html", label: "STL 03", title: "树容器与哈希容器", group: "STL" },
    { file: "stl-adapters-iterators.html", label: "STL 04", title: "适配器、迭代器与算法", group: "STL" },
    { file: "01-simulation.html", label: "01", title: "模拟与枚举", group: "算法" },
    { file: "02-hash-and-counting.html", label: "02", title: "哈希表与计数", group: "算法" },
    { file: "03-two-pointers-sliding-window.html", label: "03", title: "双指针与滑动窗口", group: "算法" },
    { file: "04-prefix-sum-difference.html", label: "04", title: "前缀和与差分", group: "算法" },
    { file: "05-binary-search.html", label: "05", title: "二分查找与二分答案", group: "算法" },
    { file: "06-stack-queue-monotonic.html", label: "06", title: "栈、队列与单调结构", group: "算法" },
    { file: "07-heap-greedy.html", label: "07", title: "堆与贪心", group: "算法" },
    { file: "08-dfs-backtrack.html", label: "08", title: "DFS 与回溯", group: "算法" },
    { file: "09-bfs-grid.html", label: "09", title: "BFS 与网格问题", group: "算法" },
    { file: "10-union-find.html", label: "10", title: "并查集", group: "算法" },
    { file: "11-graph-traversal.html", label: "11", title: "图的遍历与连通性", group: "算法" },
    { file: "12-shortest-path.html", label: "12", title: "最短路径", group: "算法" },
    { file: "13-topological-sort.html", label: "13", title: "拓扑排序与 DAG", group: "算法" },
    { file: "14-dynamic-programming.html", label: "14", title: "动态规划", group: "算法" },
    { file: "15-tree.html", label: "15", title: "树", group: "算法" },
    { file: "16-advanced-data-structures.html", label: "16", title: "高级数据结构", group: "算法" },
    { file: "17-math-number-theory.html", label: "17", title: "数学与数论", group: "算法" },
    { file: "18-bit-manipulation.html", label: "18", title: "位运算", group: "算法" },
    { file: "templates.html", label: "模板库", title: "可复制的 C++ 代码模板", group: "模板" },
    { file: "reference-constants.html", label: "附录 A", title: "常用常量与速查", group: "附录" },
    { file: "reference-io-math.html", label: "附录 B", title: "输出格式控制与常用库", group: "附录" },
];

const currentFile = window.location.pathname.split("/").pop() || "index.html";
const savedTheme = localStorage.getItem("theme");
const preferredTheme = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
document.documentElement.dataset.theme = savedTheme || preferredTheme;

function toggleTheme() {
    const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    localStorage.setItem("theme", next);
    updateThemeButton();
}

function updateThemeButton() {
    const button = document.querySelector(".theme-button");
    if (!button) return;
    const dark = document.documentElement.dataset.theme === "dark";
    button.textContent = dark ? "浅色" : "深色";
    button.setAttribute("aria-label", dark ? "切换到浅色模式" : "切换到深色模式");
    button.title = dark ? "切换到浅色模式" : "切换到深色模式";
}

function createHeader() {
    const header = document.createElement("header");
    header.className = "site-header";
    header.innerHTML = `
        <div class="site-header__inner">
            <a class="brand" href="index.html">
                <span class="brand__mark">C++</span>
                <span class="brand__text">夏令营机试手册</span>
            </a>
            <nav class="site-nav" aria-label="主导航">
                <a href="index.html">首页</a>
                <a href="index.html#foundations">学习材料</a>
                <a href="templates.html">代码模板</a>
                <a href="index.html#references">速查</a>
                <button class="theme-button" type="button" onclick="toggleTheme()"></button>
            </nav>
        </div>`;
    return header;
}

function createChapterSelect(current) {
    const select = document.createElement("select");
    select.className = "chapter-select";
    select.setAttribute("aria-label", "跳转到章节");
    for (const groupName of ["模板", "基础", "STL", "算法", "附录"]) {
        const group = document.createElement("optgroup");
        group.label = groupName;
        for (const chapter of chapters.filter((item) => item.group === groupName)) {
            const option = document.createElement("option");
            option.value = chapter.file;
            option.textContent = `${chapter.label} · ${chapter.title}`;
            option.selected = chapter.file === current?.file;
            group.append(option);
        }
        select.append(group);
    }
    select.addEventListener("change", () => {
        window.location.href = select.value;
    });
    return select;
}

function slugHeading(text, index) {
    const ascii = text
        .trim()
        .toLowerCase()
        .replace(/[^a-z0-9\u4e00-\u9fff]+/g, "-")
        .replace(/^-|-$/g, "");
    return ascii || `section-${index + 1}`;
}

function decorateContent(article, current) {
    for (const paragraph of article.querySelectorAll("p")) {
        if (paragraph.textContent.trim() === "---") {
            paragraph.replaceWith(document.createElement("hr"));
        }
    }

    const heading = article.querySelector("h1");
    if (heading && current) {
        const kicker = document.createElement("div");
        kicker.className = "article-kicker";
        kicker.textContent = `${current.group} · ${current.label}`;
        heading.before(kicker);
    }

    for (const pre of article.querySelectorAll("pre")) {
        const wrapper = document.createElement("div");
        wrapper.className = "code-block";
        pre.before(wrapper);
        wrapper.append(pre);

        const button = document.createElement("button");
        button.className = "copy-button";
        button.type = "button";
        button.textContent = "复制";
        button.setAttribute("aria-label", "复制代码");
        button.addEventListener("click", async () => {
            try {
                await navigator.clipboard.writeText(pre.textContent);
                button.textContent = "已复制";
                window.setTimeout(() => { button.textContent = "复制"; }, 1200);
            } catch {
                button.textContent = "复制失败";
            }
        });
        wrapper.append(button);
    }

    for (const table of article.querySelectorAll("table")) {
        const wrapper = document.createElement("div");
        wrapper.className = "table-wrap";
        table.before(wrapper);
        wrapper.append(table);
    }
}

function createSidebar(article, current, currentIndex) {
    const aside = document.createElement("aside");
    aside.className = "doc-sidebar";

    const chapterCard = document.createElement("div");
    chapterCard.className = "sidebar-card";
    const chapterTitle = document.createElement("p");
    chapterTitle.className = "sidebar-title";
    chapterTitle.textContent = "章节跳转";
    chapterCard.append(chapterTitle, createChapterSelect(current));

    const progress = document.createElement("div");
    progress.className = "chapter-progress";
    progress.title = `全站第 ${currentIndex + 1} / ${chapters.length} 节`;
    progress.innerHTML = `<span style="width:${((currentIndex + 1) / chapters.length) * 100}%"></span>`;
    chapterCard.append(progress);
    aside.append(chapterCard);

    const headings = [...article.querySelectorAll("h2")];
    if (headings.length) {
        const tocCard = document.createElement("div");
        tocCard.className = "sidebar-card toc-card";
        const tocTitle = document.createElement("p");
        tocTitle.className = "sidebar-title";
        tocTitle.textContent = "本页目录";
        const toc = document.createElement("nav");
        toc.className = "toc";
        toc.setAttribute("aria-label", "本页目录");
        headings.forEach((heading, index) => {
            heading.id ||= slugHeading(heading.textContent, index);
            const link = document.createElement("a");
            link.href = `#${heading.id}`;
            link.textContent = heading.textContent;
            toc.append(link);
        });
        tocCard.append(tocTitle, toc);
        aside.append(tocCard);
    }
    return aside;
}

function createPageNav(currentIndex) {
    const nav = document.createElement("nav");
    nav.className = "page-nav";
    nav.setAttribute("aria-label", "章节翻页");
    const previous = currentIndex > 0 ? chapters[currentIndex - 1] : null;
    const next = currentIndex < chapters.length - 1 ? chapters[currentIndex + 1] : null;

    const makeLink = (chapter, direction) => {
        const link = document.createElement("a");
        if (chapter) {
            link.href = chapter.file;
            link.innerHTML = `<span class="page-nav__label">${direction === "previous" ? "← 上一节" : "下一节 →"}</span><span class="page-nav__title">${chapter.label} · ${chapter.title}</span>`;
        } else {
            link.href = "index.html";
            link.innerHTML = `<span class="page-nav__label">${direction === "previous" ? "← 返回" : "完成学习"}</span><span class="page-nav__title">回到课程主页</span>`;
        }
        return link;
    };
    nav.append(makeLink(previous, "previous"), makeLink(next, "next"));
    return nav;
}

function buildDocumentPage(contentNodes, current, currentIndex) {
    const main = document.createElement("main");
    main.className = "page-shell";
    const grid = document.createElement("div");
    grid.className = "page-grid";
    const article = document.createElement("article");
    article.className = "article";
    if (current?.file === "templates.html") {
        article.classList.add("template-library");
    }
    article.append(...contentNodes);
    decorateContent(article, current);
    grid.append(article, createSidebar(article, current, currentIndex));
    main.append(grid, createPageNav(currentIndex));
    return main;
}

function activateToc() {
    const links = [...document.querySelectorAll(".toc a")];
    if (!links.length || !("IntersectionObserver" in window)) return;
    const byId = new Map(links.map((link) => [decodeURIComponent(link.hash.slice(1)), link]));
    const observer = new IntersectionObserver((entries) => {
        for (const entry of entries) {
            if (!entry.isIntersecting) continue;
            links.forEach((link) => link.classList.remove("is-active"));
            byId.get(entry.target.id)?.classList.add("is-active");
        }
    }, { rootMargin: "-90px 0px -72% 0px" });
    document.querySelectorAll(".article h2").forEach((heading) => observer.observe(heading));
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".theme-toggle, .nav").forEach((element) => element.remove());
    const header = createHeader();
    document.body.prepend(header);

    const contentNodes = [...document.body.children].filter(
        (element) => element !== header && element.tagName !== "SCRIPT"
    );
    const isHome = currentFile === "index.html";
    if (isHome) {
        const main = document.createElement("main");
        main.className = "page-shell home-shell";
        main.append(...contentNodes);
        document.body.append(main);
    } else {
        const currentIndex = chapters.findIndex((chapter) => chapter.file === currentFile);
        const current = chapters[currentIndex];
        if (current) {
            document.body.append(buildDocumentPage(contentNodes, current, currentIndex));
        } else {
            const main = document.createElement("main");
            main.className = "page-shell";
            main.append(...contentNodes);
            document.body.append(main);
        }
    }

    const footer = document.createElement("footer");
    footer.className = "site-footer";
    footer.textContent = "C++ 夏令营机试学习手册";
    document.body.append(footer);
    updateThemeButton();
    activateToc();
});
