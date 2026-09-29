# -*- coding: utf-8 -*-
"""
力扣算法解析 · 静态站点生成器

与 philosophy/_src/gen.py 同一套架构：外壳统一，正文放在 _src/*.part，
改一处外壳即全站生效。_src/ 部署时排除。

本教程按「算法专题」组织（数组/哈希/滑窗/二分/链表/栈队列/树/回溯/DP/贪心/图），
不按章节难度流水线 —— 每个专题独立可读，学生按需跳跃。

用法：
    python _src/gen.py

代码高亮：.part 里的 <pre><code> 内是**未转义的原始 Java 文本**，
生成时由本文件的 highlight() 统一做 HTML 转义 + 语法着色
（kw=关键字 / cm=注释 / st=字符串 / an=注解）。
所以 .part 源文件里可以直接写 List<List<Integer>>，不用写 &lt;。
"""
import io
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))          # .../leetcode/_src
ROOT = os.path.dirname(BASE)                               # .../leetcode

VERSION = "2026-09-28 16:30"
SITE = "力扣算法解析"
TAGLINE = "按专题吃透，不做题海"

# ---------------------------------------------------------------- 章节定义
# f=文件名 nav=顶部下拉 short=侧边栏 title=<title>与前后页导航
# secs=[(锚点id, 名称)] —— id 必须与正文 <h2 id="..."> 一致，check_site.py 会交叉核对
CHAPTERS = [
    dict(
        f="index.html", nav="总览与路线", short="总览 · 怎么刷题",
        title="总览 · 算法学习路线与刷题方法",
        secs=[
            ("howto", "怎么用这份解析"),
            ("order", "二十四个专题的推荐顺序"),
            ("method", "一道题的正确刷法：五步法"),
            ("complexity", "复杂度：面试官其实在问什么"),
            ("mistake", "大多数人的三个误区"),
            ("faq", "常见疑问"),
        ],
    ),
    dict(
        f="ch01.html", nav="01 · 数组与双指针", short="数组与双指针",
        title="专题 01 · 数组与双指针",
        secs=[
            ("s1", "1.1 为什么数组是所有题的起点"),
            ("s2", "1.2 双指针的三种形态"),
            ("s3", "1.3 移动零（简单）"),
            ("s4", "1.4 删除有序数组中的重复项（简单）"),
            ("s5", "1.5 盛最多水的容器（中等）"),
            ("s6", "1.6 三数之和（中等）"),
            ("s7", "1.7 本专题常见坑"),
            ("s8", "1.8 自测题"),
        ],
    ),
    dict(
        f="ch02.html", nav="02 · 哈希表", short="哈希表",
        title="专题 02 · 哈希表",
        secs=[
            ("s1", "2.1 哈希表的本质：拿空间换一次查找"),
            ("s2", "2.2 Java 哈希三件套怎么选"),
            ("s3", "2.3 两数之和（简单）"),
            ("s4", "2.4 有效的字母异位词（简单）"),
            ("s5", "2.5 字母异位词分组（中等）"),
            ("s6", "2.6 最长连续序列（中等）"),
            ("s7", "2.7 本专题常见坑"),
            ("s8", "2.8 自测题"),
        ],
    ),
    dict(
        f="ch03.html", nav="03 · 滑动窗口", short="滑动窗口",
        title="专题 03 · 滑动窗口",
        secs=[
            ("s1", "3.1 从暴力 O(n²) 到 O(n)"),
            ("s2", "3.2 滑动窗口通用模板"),
            ("s3", "3.3 长度最小的子数组（中等）"),
            ("s4", "3.4 无重复字符的最长子串（中等）"),
            ("s5", "3.5 找到字符串中所有字母异位词（简单）"),
            ("s6", "3.6 最小覆盖子串（困难）"),
            ("s7", "3.7 本专题常见坑"),
            ("s8", "3.8 自测题"),
        ],
    ),
    dict(
        f="ch04.html", nav="04 · 二分查找", short="二分查找",
        title="专题 04 · 二分查找",
        secs=[
            ("s1", "4.1 二分的本质：单调性上的折半"),
            ("s2", "4.2 三种边界写法，背一种就够"),
            ("s3", "4.3 二分查找（简单）"),
            ("s4", "4.4 搜索插入位置（简单）"),
            ("s5", "4.5 查找元素的第一个和最后一个位置（中等）"),
            ("s6", "4.6 搜索旋转排序数组（中等）"),
            ("s7", "4.7 本专题常见坑：死循环"),
            ("s8", "4.8 自测题"),
        ],
    ),
    dict(
        f="ch05.html", nav="05 · 链表", short="链表",
        title="专题 05 · 链表",
        secs=[
            ("s1", "5.1 链表题考的是指针操作，不是算法"),
            ("s2", "5.2 虚拟头节点：链表第一技巧"),
            ("s3", "5.3 移除链表元素（简单）"),
            ("s4", "5.4 反转链表（简单）"),
            ("s5", "5.5 合并两个有序链表（简单）"),
            ("s6", "5.6 环形链表 I / II（简单 / 中等）"),
            ("s7", "5.7 删除链表的倒数第 N 个结点（中等）"),
            ("s8", "5.8 本专题常见坑"),
            ("s9", "5.9 自测题"),
        ],
    ),
    dict(
        f="ch06.html", nav="06 · 栈与队列", short="栈与队列",
        title="专题 06 · 栈与队列",
        secs=[
            ("s1", "6.1 栈：后进先出的「撤销」思想"),
            ("s2", "6.2 有效的括号（简单）"),
            ("s3", "6.3 最小栈（中等）"),
            ("s4", "6.4 用栈实现队列（简单）"),
            ("s5", "6.5 每日温度（中等）"),
            ("s6", "6.6 单调栈模板总结"),
            ("s7", "6.7 本专题常见坑"),
            ("s8", "6.8 自测题"),
        ],
    ),
    dict(
        f="ch07.html", nav="07 · 二叉树", short="二叉树",
        title="专题 07 · 二叉树",
        secs=[
            ("s1", "7.1 树题的两种思考方式：遍历与分解"),
            ("s2", "7.2 二叉树的最大深度（简单）"),
            ("s3", "7.3 翻转二叉树（简单）"),
            ("s4", "7.4 对称二叉树（简单）"),
            ("s5", "7.5 二叉树的层序遍历（中等）"),
            ("s6", "7.6 二叉树的最近公共祖先（中等）"),
            ("s7", "7.7 本专题常见坑"),
            ("s8", "7.8 自测题"),
        ],
    ),
    dict(
        f="ch08.html", nav="08 · 递归与回溯", short="递归与回溯",
        title="专题 08 · 递归与回溯",
        secs=[
            ("s1", "8.1 回溯 = 递归 + 撤销选择"),
            ("s2", "8.2 回溯通用模板：决策树"),
            ("s3", "8.3 组合（中等）"),
            ("s4", "8.4 子集（中等）"),
            ("s5", "8.5 全排列（中等）"),
            ("s6", "8.6 N 皇后（困难）"),
            ("s7", "8.7 剪枝：回溯的效率生命线"),
            ("s8", "8.8 自测题"),
        ],
    ),
    dict(
        f="ch09.html", nav="09 · 动态规划（入门）", short="DP 入门",
        title="专题 09 · 动态规划（入门）",
        secs=[
            ("s1", "9.1 DP 到底在干什么"),
            ("s2", "9.2 DP 五步法"),
            ("s3", "9.3 爬楼梯（简单）"),
            ("s4", "9.4 使用最小花费爬楼梯（简单）"),
            ("s5", "9.5 打家劫舍（中等）"),
            ("s6", "9.6 不同路径（中等）"),
            ("s7", "9.7 本专题常见坑"),
            ("s8", "9.8 自测题"),
        ],
    ),
    dict(
        f="ch10.html", nav="10 · 动态规划（进阶）", short="DP 进阶",
        title="专题 10 · 动态规划（进阶）：子序列与背包",
        secs=[
            ("s1", "10.1 DP 的两大主线：子序列与背包"),
            ("s2", "10.2 最长递增子序列（中等）"),
            ("s3", "10.3 最长公共子序列（中等）"),
            ("s4", "10.4 分割等和子集：01 背包（中等）"),
            ("s5", "10.5 零钱兑换：完全背包（中等）"),
            ("s6", "10.6 背包问题一张表总结"),
            ("s7", "10.7 本专题常见坑"),
            ("s8", "10.8 自测题"),
        ],
    ),
    dict(
        f="ch11.html", nav="11 · 贪心算法", short="贪心算法",
        title="专题 11 · 贪心算法",
        secs=[
            ("s1", "11.1 什么时候能贪，什么时候必须 DP"),
            ("s2", "11.2 买卖股票的最佳时机（简单）"),
            ("s3", "11.3 跳跃游戏（中等）"),
            ("s4", "11.4 跳跃游戏 II（中等）"),
            ("s5", "11.5 无重叠区间（中等）"),
            ("s6", "11.6 区间题的通用套路"),
            ("s7", "11.7 本专题常见坑"),
            ("s8", "11.8 自测题"),
        ],
    ),
    dict(
        f="ch12.html", nav="12 · 图论入门", short="图论入门",
        title="专题 12 · 图论入门：BFS、DFS 与拓扑排序",
        secs=[
            ("s1", "12.1 图题只需要三块积木"),
            ("s2", "12.2 岛屿数量：DFS 洪水填充（中等）"),
            ("s3", "12.3 腐烂的橘子：多源 BFS（中等）"),
            ("s4", "12.4 课程表：拓扑排序（中等）"),
            ("s5", "12.5 BFS / DFS 怎么选"),
            ("s6", "12.6 本专题常见坑"),
            ("s7", "12.7 自测题"),
        ],
    ),
    dict(
        f="ch13.html", nav="13 · 前缀和与差分", short="前缀和与差分",
        title="专题 13 · 前缀和与差分",
        secs=[
            ("s1", "13.1 前缀和：把区间和变成一次减法"),
            ("s2", "13.2 一维前缀和模板"),
            ("s3", "13.3 区域和检索 - 数组不可变（简单）"),
            ("s4", "13.4 和为 K 的子数组（中等）"),
            ("s5", "13.5 二维前缀和（中等）"),
            ("s6", "13.6 差分：区间批量加减（拼车，中等）"),
            ("s7", "13.7 本专题常见坑"),
            ("s8", "13.8 自测题"),
        ],
    ),
    dict(
        f="ch14.html", nav="14 · 位运算", short="位运算",
        title="专题 14 · 位运算",
        secs=[
            ("s1", "14.1 位运算的本质：直接操作二进制"),
            ("s2", "14.2 六个常用技巧"),
            ("s3", "14.3 位 1 的个数（简单）"),
            ("s4", "14.4 只出现一次的数字（简单）"),
            ("s5", "14.5 2 的幂（简单）"),
            ("s6", "14.6 丢失的数字（简单）"),
            ("s7", "14.7 本专题常见坑"),
            ("s8", "14.8 自测题"),
        ],
    ),
    dict(
        f="ch15.html", nav="15 · 数学与模拟", short="数学与模拟",
        title="专题 15 · 数学与模拟",
        secs=[
            ("s1", "15.1 数学题与模拟题考什么"),
            ("s2", "15.2 罗马数字转整数（简单）"),
            ("s3", "15.3 快乐数（简单）"),
            ("s4", "15.4 计数质数：埃氏筛（中等）"),
            ("s5", "15.5 阶乘后的零（中等）"),
            ("s6", "15.6 螺旋矩阵：模拟题怎么写（中等）"),
            ("s7", "15.7 本专题常见坑"),
            ("s8", "15.8 自测题"),
        ],
    ),
    dict(
        f="ch16.html", nav="16 · 排序与分治", short="排序与分治",
        title="专题 16 · 排序与分治",
        secs=[
            ("s1", "16.1 排序算法全景图"),
            ("s2", "16.2 Java 内置排序与自定义比较器"),
            ("s3", "16.3 合并区间：排序预处理（中等）"),
            ("s4", "16.4 第 K 个最大元素：快速选择（中等）"),
            ("s5", "16.5 颜色分类：三指针（中等）"),
            ("s6", "16.6 分治思想：归并与逆序对（选学）"),
            ("s7", "16.7 本专题常见坑"),
            ("s8", "16.8 自测题"),
        ],
    ),
    dict(
        f="ch17.html", nav="17 · 堆（优先队列）", short="堆与优先队列",
        title="专题 17 · 堆（优先队列）",
        secs=[
            ("s1", "17.1 堆是什么，Java 里怎么用"),
            ("s2", "17.2 堆的三种典型用法"),
            ("s3", "17.3 第 K 个最大元素：堆解法（中等）"),
            ("s4", "17.4 前 K 个高频元素（中等）"),
            ("s5", "17.5 合并 K 个升序链表（困难）"),
            ("s6", "17.6 Top K 三种解法对比"),
            ("s7", "17.7 本专题常见坑"),
            ("s8", "17.8 自测题"),
        ],
    ),
    dict(
        f="ch18.html", nav="18 · 二叉搜索树", short="二叉搜索树",
        title="专题 18 · 二叉搜索树",
        secs=[
            ("s1", "18.1 BST 的性质：中序遍历即有序"),
            ("s2", "18.2 验证二叉搜索树（中等）"),
            ("s3", "18.3 二叉搜索树中的搜索（简单）"),
            ("s4", "18.4 将有序数组转换为二叉搜索树（简单）"),
            ("s5", "18.5 二叉搜索树中第 K 小的元素（中等）"),
            ("s6", "18.6 删除二叉搜索树中的节点（中等）"),
            ("s7", "18.7 本专题常见坑"),
            ("s8", "18.8 自测题"),
        ],
    ),
    dict(
        f="ch19.html", nav="19 · Trie 前缀树", short="Trie 前缀树",
        title="专题 19 · Trie 前缀树",
        secs=[
            ("s1", "19.1 Trie：把前缀查询做到 O(单词长度)"),
            ("s2", "19.2 实现 Trie（前缀树）（中等）"),
            ("s3", "19.3 添加与搜索单词（中等）"),
            ("s4", "19.4 单词搜索 II（困难，选学）"),
            ("s5", "19.5 Trie 的应用场景总结"),
            ("s6", "19.6 本专题常见坑"),
            ("s7", "19.7 自测题"),
        ],
    ),
    dict(
        f="ch20.html", nav="20 · 并查集", short="并查集",
        title="专题 20 · 并查集",
        secs=[
            ("s1", "20.1 并查集解决什么：动态连通性"),
            ("s2", "20.2 模板：find + union"),
            ("s3", "20.3 省份数量（中等）"),
            ("s4", "20.4 冗余连接（中等）"),
            ("s5", "20.5 等式方程的可满足性（中等）"),
            ("s6", "20.6 岛屿数量的并查集视角"),
            ("s7", "20.7 本专题常见坑"),
            ("s8", "20.8 自测题"),
        ],
    ),
    dict(
        f="ch21.html", nav="21 · 字符串算法", short="字符串算法",
        title="专题 21 · 字符串算法",
        secs=[
            ("s1", "21.1 字符串题的四种武器"),
            ("s2", "21.2 最长回文子串：中心扩展（中等）"),
            ("s3", "21.3 字符串相加：大数模拟（简单）"),
            ("s4", "21.4 反转字符串里的单词（中等）"),
            ("s5", "21.5 KMP：next 数组怎么来的（选学）"),
            ("s6", "21.6 Manacher 速览（概念，选学）"),
            ("s7", "21.7 本专题常见坑"),
            ("s8", "21.8 自测题"),
        ],
    ),
    dict(
        f="ch22.html", nav="22 · 最短路与最小生成树", short="最短路 / 最小生成树",
        title="专题 22 · 图论进阶：最短路与最小生成树",
        secs=[
            ("s1", "22.1 带权图与最短路的两大家族"),
            ("s2", "22.2 网络延迟时间：Dijkstra（中等）"),
            ("s3", "22.3 K 站中转内最便宜的航班：Bellman-Ford（中等）"),
            ("s4", "22.4 Floyd：多源最短路"),
            ("s5", "22.5 连接所有点的最小费用：Kruskal（中等）"),
            ("s6", "22.6 本专题常见坑"),
            ("s7", "22.7 自测题"),
        ],
    ),
    dict(
        f="ch23.html", nav="23 · DP 高阶", short="DP 高阶",
        title="专题 23 · 动态规划高阶：区间、树形与状态压缩",
        secs=[
            ("s1", "23.1 进阶 DP 只是把状态定义变复杂"),
            ("s2", "23.2 最长回文子序列：区间 DP（中等）"),
            ("s3", "23.3 戳气球：区间 DP（困难，选学）"),
            ("s4", "23.4 打家劫舍 III：树形 DP（中等）"),
            ("s5", "23.5 优美的排列：状态压缩 DP（中等）"),
            ("s6", "23.6 记忆化搜索：自顶向下的 DP（中等）"),
            ("s7", "23.7 本专题常见坑"),
            ("s8", "23.8 自测题"),
        ],
    ),
    dict(
        f="ch24.html", nav="24 · 进阶速览", short="进阶速览",
        title="专题 24 · 进阶速览：单调队列、设计题与抽样",
        secs=[
            ("s1", "24.1 单调队列：滑动窗口最大值（困难）"),
            ("s2", "24.2 LRU 缓存：哈希表 + 双向链表（中等）"),
            ("s3", "24.3 LFU 缓存思路（困难，选学）"),
            ("s4", "24.4 链表随机节点：蓄水池抽样（中等）"),
            ("s5", "24.5 树状数组与线段树是什么（概念）"),
            ("s6", "24.6 本专题常见坑"),
            ("s7", "24.7 自测题"),
        ],
    ),
    dict(
        f="appendix.html", nav="附录 · 速查与路线", short="附录 · 速查 / 路线",
        title="附录 · 模板速查、API 速查与 90 天路线",
        secs=[
            ("a1", "A.1 复杂度速查"),
            ("a2", "A.2 Java 刷题 API 速查"),
            ("a3", "A.3 全部模板索引"),
            ("a4", "A.4 90 天刷题路线（Hot 100）"),
            ("a5", "A.5 卡住了怎么办：看题解的正确姿势"),
        ],
    ),
]

# ---------------------------------------------------------------- Java 高亮
JAVA_KW = (
    'abstract|assert|boolean|break|byte|case|catch|char|class|continue|default|'
    'do|double|else|enum|extends|final|finally|float|for|if|implements|import|'
    'instanceof|int|interface|long|new|package|private|protected|public|return|'
    'short|static|super|switch|synchronized|this|throw|throws|try|void|volatile|'
    'while|var|record|true|false|null'
)
KW_RE = re.compile(r'\b(%s)\b' % JAVA_KW)
AN_RE = re.compile(r'(@[A-Za-z_]\w*)')
TOKEN_RE = re.compile(r'(//[^\n]*|/\*.*?\*/|"(?:[^"\\\n]|\\.)*"|\'(?:[^\'\\\n]|\\.)*\')', re.S)


def _esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def highlight(src):
    """原始代码文本 -> 转义 + 着色的 HTML。注释/字符串整段着色，
    其余部分才做关键字/注解着色（避免把注释里的词也染成关键字）。"""
    out = []
    for seg in TOKEN_RE.split(src):
        if not seg:
            continue
        if seg.startswith('//') or seg.startswith('/*'):
            out.append('<span class="cm">%s</span>' % _esc(seg))
        elif seg.startswith('"') or seg.startswith("'"):
            out.append('<span class="st">%s</span>' % _esc(seg))
        else:
            t = _esc(seg)
            t = AN_RE.sub(r'<span class="an">\1</span>', t)
            # 跳过已经包进 span 的内容：只对 an 标签以外的部分上色，
            # 用占位符方案避免 KW_RE 命中 class 名里的关键字（如 var）
            parts = re.split(r'(<span class="an">.*?</span>)', t)
            for i, p in enumerate(parts):
                if i % 2 == 0:
                    p = KW_RE.sub(r'<span class="kw">\1</span>', p)
                parts[i] = p
            out.append(''.join(parts))
    return ''.join(out)


CODE_RE = re.compile(r'<pre><code>(.*?)</code></pre>', re.S)
NOHL_RE = re.compile(r'<pre><code class="nohl">(.*?)</code></pre>', re.S)


def highlight_page(body):
    """对正文里所有 <pre><code> 做转义+高亮；class="nohl" 的块保持原样转义。"""
    def repl_plain(m):
        return '<pre><code class="nohl">%s</code></pre>' % _esc(m.group(1))

    body = NOHL_RE.sub(repl_plain, body)

    def repl_java(m):
        return '<pre><code>%s</code></pre>' % highlight(m.group(1))

    return CODE_RE.sub(repl_java, body)


# ---------------------------------------------------------------- 页面外壳
def topbar():
    opts = "\n".join(
        '    <option value="%s">%s</option>' % (c["f"], c["nav"]) for c in CHAPTERS
    )
    return """<header class="topbar">
  <button class="menu-btn" type="button" aria-label="菜单">☰</button>
  <a class="brand" href="index.html">
    <span class="logo">算</span>
    <span>%s<small>%s</small></span>
  </a>
  <span class="spacer"></span>
  <select class="tb-select" aria-label="专题跳转">
%s
  </select>
  <a class="tb-link" href="appendix.html">速查</a>
  <a class="tb-link" href="appendix.html#a4">90 天路线</a>
  <a class="tb-home" href="../index.html">⌂ 全部教程</a>
</header>""" % (SITE, TAGLINE, opts)


def sidebar(cur):
    parts = ['<aside class="sidebar">']
    parts.append('  <div class="sb-group">')
    parts.append('    <div class="sb-title">开始</div>')
    for c in CHAPTERS[:1]:
        act = " active" if c["f"] == cur else ""
        parts.append(
            '    <a class="sb-link%s" href="%s"><span class="num">0</span><span>%s</span></a>'
            % (act, c["f"], c["short"])
        )
        if c["f"] == cur:
            parts.append('    <div class="sb-sub">')
            for i, t in c["secs"]:
                parts.append('      <a href="#%s">%s</a>' % (i, t))
            parts.append('    </div>')
    parts.append('  </div>')

    parts.append('  <div class="sb-group">')
    parts.append('    <div class="sb-title">全部专题</div>')
    for c in CHAPTERS[1:-1]:
        num = c["f"][2:4].lstrip("0")
        act = " active" if c["f"] == cur else ""
        parts.append(
            '    <a class="sb-link%s" href="%s"><span class="num">%s</span><span>%s</span></a>'
            % (act, c["f"], num, c["short"])
        )
        if c["f"] == cur:
            parts.append('    <div class="sb-sub">')
            for i, t in c["secs"]:
                parts.append('      <a href="#%s">%s</a>' % (i, t))
            parts.append('    </div>')
    parts.append('  </div>')

    parts.append('  <div class="sb-group">')
    parts.append('    <div class="sb-title">附录</div>')
    for c in CHAPTERS[-1:]:
        act = " active" if c["f"] == cur else ""
        parts.append(
            '    <a class="sb-link%s" href="%s"><span class="num">A</span><span>%s</span></a>'
            % (act, c["f"], c["short"])
        )
        if c["f"] == cur:
            parts.append('    <div class="sb-sub">')
            for i, t in c["secs"]:
                parts.append('      <a href="#%s">%s</a>' % (i, t))
            parts.append('    </div>')
    parts.append('  </div>')
    parts.append('</aside>')
    return "\n".join(parts)


def navfoot(cur):
    idx = next((i for i, c in enumerate(CHAPTERS) if c["f"] == cur), None)
    if idx is None:
        return ""
    prev_c = CHAPTERS[idx - 1] if idx > 0 else None
    next_c = CHAPTERS[idx + 1] if idx < len(CHAPTERS) - 1 else None
    out = ['<div class="navfoot">']
    if prev_c:
        out.append(
            '  <a href="%s"><div class="dir-label">← 上一节</div><div class="dir-name">%s</div></a>'
            % (prev_c["f"], prev_c["title"])
        )
    else:
        out.append(
            '  <a href="appendix.html"><div class="dir-label">→ 速查</div><div class="dir-name">附录 · 模板与路线</div></a>'
        )
    if next_c:
        out.append(
            '  <a class="next" href="%s"><div class="dir-label">下一节 →</div><div class="dir-name">%s</div></a>'
            % (next_c["f"], next_c["title"])
        )
    else:
        out.append(
            '  <a class="next" href="index.html"><div class="dir-label">→ 回到</div><div class="dir-name">总览 · 学习路线</div></a>'
        )
    out.append('</div>')
    return "\n".join(out)


SHELL = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | {site}</title>
<link rel="stylesheet" href="../assets/style.css">
</head>
<body data-tut="leetcode">

{topbar}

<div class="layout">
{sidebar}

<main class="main">

{body}

{navfoot}

<div class="footer">{site} · {label} · <span class="ver">内容版本 {ver}</span></div>

</main>
</div>

<script src="../assets/app.js"></script>
</body>
</html>
"""


def main():
    built = []
    for c in CHAPTERS:
        part = os.path.join(BASE, c["f"].replace(".html", ".part"))
        if not os.path.isfile(part):
            print("  ! 缺少正文片段：%s（跳过）" % os.path.basename(part))
            continue
        body = io.open(part, encoding="utf-8").read().rstrip()
        body = highlight_page(body)
        label = "总览" if c["f"] == "index.html" else (
            "附录" if c["f"] == "appendix.html" else "专题 %s" % c["f"][2:4].lstrip("0")
        )
        html = SHELL.format(
            title=c["title"], site=SITE, label=label, ver=VERSION,
            topbar=topbar(), sidebar=sidebar(c["f"]), body=body, navfoot=navfoot(c["f"]),
        )
        out = os.path.join(ROOT, c["f"])
        io.open(out, "w", encoding="utf-8", newline="\n").write(html)
        built.append((c["f"], len(html.encode("utf-8"))))

    print("生成完成（内容版本 %s）：" % VERSION)
    total = 0
    for f, n in built:
        total += n
        print("  %-16s %7d 字节" % (f, n))
    print("  %-16s %7.1f KB 共 %d 页" % ("合计", total / 1024, len(built)))


if __name__ == "__main__":
    main()
