# -*- coding: utf-8 -*-
"""
哲学 × AI 学习指南 · 静态站点生成器

为什么用生成器而不是手写 13 份 HTML：
顶栏 / 侧边栏 / 页脚导航在 13 个页面里是完全相同的，手写会在每次调整
导航时改 13 处（旧的技术站就吃过这个亏）。这里把外壳统一，正文放在
_src/*.part 里，改一处即全站生效。

用法：
    python _src/gen.py

产出：
    ../index.html, ../ch01.html ... ../ch11.html, ../appendix.html

部署时 _src/ 不需要上传（和 *.md 一样排除）。
"""
import io
import os

BASE = os.path.dirname(os.path.abspath(__file__))          # .../philosophy-ai-guide/_src
ROOT = os.path.dirname(BASE)                               # .../philosophy-ai-guide

VERSION = "2026-09-28 16:30"
SITE = "哲学 × AI 学习指南"
TAGLINE = "把哲学变成工程判断力"

# ---------------------------------------------------------------- 章节定义
# file, 顶部下拉短名, 侧边栏短名, 完整标题(用于 <title> 与前页导航), 小节 [(id, 名称)]
CHAPTERS = [
    dict(
        f="index.html", nav="总览与路线", short="总览 · 学习路线",
        title="总览 · 为什么工程师要读哲学",
        secs=[
            ("howto", "怎么用这份指南"),
            ("why", "为什么工程师该读哲学"),
            ("map", "哲学分支 × AI 问题 总映射"),
            ("route", "12 周学习路线"),
            ("depth", "三档阅读深度"),
            ("faq", "五个常见疑问"),
            ("ready", "0.7 开始之前"),
        ],
    ),
    dict(
        f="ch01.html", nav="01 · 哲学与 AI 的交界", short="哲学与 AI 的真实交界",
        title="第 1 章 · 哲学与 AI 的真实交界",
        secs=[
            ("s1", "1.1 一个反直觉的事实"),
            ("s2", "1.2 三类问题的分界"),
            ("s3", "1.3 十一个难题的哲学出处"),
            ("s4", "1.4 两类常见误解"),
            ("s5", "1.5 哲学给你的三种能力"),
            ("s6", "1.6 哲学不能给你什么"),
            ("s7", "1.7 动手：翻译你的项目"),
            ("s8", "1.8 自测题"),
        ],
    ),
    dict(
        f="ch02.html", nav="02 · 认识论 I", short="认识论 I · 知识、信念与不确定性",
        title="第 2 章 · 认识论 I：知识、信念与不确定性",
        secs=[
            ("s1", "2.1 认识论在问什么"),
            ("s2", "2.2 知识的经典定义与葛梯尔反例"),
            ("s3", "2.3 知识的三种来源"),
            ("s4", "2.4 确定性是如何失去的"),
            ("s5", "2.5 概率是信念的度量"),
            ("s6", "2.6 校准：模型说把握有多大"),
            ("s7", "2.7 什么时候该说不知道"),
            ("s8", "2.8 动手练习"),
            ("s9", "2.9 自测题"),
        ],
    ),
    dict(
        f="ch03.html", nav="03 · 认识论 II", short="认识论 II · 归纳与幻觉的根源",
        title="第 3 章 · 认识论 II：归纳问题与幻觉的根源",
        secs=[
            ("s1", "3.1 休谟的归纳问题"),
            ("s2", "3.2 归纳为什么无法被证明"),
            ("s3", "3.3 绿蓝悖论：更狠的一刀"),
            ("s4", "3.4 波普尔与可证伪性"),
            ("s5", "3.5 泛化就是归纳"),
            ("s6", "3.6 分布外为何必然失败"),
            ("s7", "3.7 幻觉的哲学根源"),
            ("s8", "3.8 奥卡姆剃刀与模型选择"),
            ("s9", "3.9 动手练习"),
            ("s10", "3.10 自测题"),
        ],
    ),
    dict(
        f="ch04.html", nav="04 · 心灵哲学 I", short="心灵哲学 I · 意识与中文房间",
        title="第 4 章 · 心灵哲学 I：意识、功能主义与中文房间",
        secs=[
            ("s1", "4.1 心身问题：400 年悬案"),
            ("s2", "4.2 笛卡尔二元论与它的麻烦"),
            ("s3", "4.3 图灵测试：把问题换成行为"),
            ("s4", "4.4 功能主义：心智是软件"),
            ("s5", "4.5 中文房间：塞尔的反击"),
            ("s6", "4.6 系统回复与它的代价"),
            ("s7", "4.7 困难问题与感质"),
            ("s8", "4.8 AI 有没有意识，为什么测不出"),
            ("s9", "4.9 动手练习"),
            ("s10", "4.10 自测题"),
        ],
    ),
    dict(
        f="ch05.html", nav="05 · 心灵哲学 II", short="心灵哲学 II · 意向性与符号接地",
        title="第 5 章 · 心灵哲学 II：意向性、表征与符号接地",
        secs=[
            ("s1", "5.1 意向性：心智的关于性"),
            ("s2", "5.2 符号接地问题"),
            ("s3", "5.3 德雷福斯的批判"),
            ("s4", "5.4 具身认知：没有身体就没有理解吗"),
            ("s5", "5.5 符号主义与连接主义之争"),
            ("s6", "5.6 LLM 的理解问题怎么判"),
            ("s7", "5.7 工具调用为什么更懂"),
            ("s8", "5.8 动手练习"),
            ("s9", "5.9 自测题"),
        ],
    ),
    dict(
        f="ch06.html", nav="06 · 语言与意义", short="语言与意义 · 从维特根斯坦到词向量",
        title="第 6 章 · 语言与意义：从维特根斯坦到词向量",
        secs=[
            ("s1", "6.1 指称论：名字如何指向东西"),
            ("s2", "6.2 弗雷格的涵义与指称"),
            ("s3", "6.3 维特根斯坦前期：图像论"),
            ("s4", "6.4 后期：意义即用法"),
            ("s5", "6.5 家族相似性"),
            ("s6", "6.6 蒯因与翻译的不确定性"),
            ("s7", "6.7 词向量与分布假设"),
            ("s8", "6.8 提示词工程的哲学读法"),
            ("s9", "6.9 动手练习"),
            ("s10", "6.10 自测题"),
        ],
    ),
    dict(
        f="ch07.html", nav="07 · 逻辑与推理边界", short="逻辑与推理的边界",
        title="第 7 章 · 逻辑与推理的边界：从弗雷格到哥德尔",
        secs=[
            ("s1", "7.1 形式化：从亚里士多德到弗雷格"),
            ("s2", "7.2 罗素悖论与类型论"),
            ("s3", "7.3 哥德尔不完备定理"),
            ("s4", "7.4 图灵机与停机问题"),
            ("s5", "7.5 形式系统的三条限制"),
            ("s6", "7.6 CoT 是推理还是模仿推理"),
            ("s7", "7.7 神经符号为何回归"),
            ("s8", "7.8 推理基准上的失败说明什么"),
            ("s9", "7.9 动手练习"),
            ("s10", "7.10 自测题"),
        ],
    ),
    dict(
        f="ch08.html", nav="08 · 伦理学 I", short="伦理学 I · 三大框架与 AI 对齐",
        title="第 8 章 · 伦理学 I：三大框架与 AI 对齐",
        secs=[
            ("s1", "8.1 规范伦理学的三大框架"),
            ("s2", "8.2 后果论：只看结果"),
            ("s3", "8.3 义务论：有些事不能做"),
            ("s4", "8.4 德性论：你是什么样的人"),
            ("s5", "8.5 电车难题到底有什么用"),
            ("s6", "8.6 价值对齐的哲学根源"),
            ("s7", "8.7 三种对齐路线的哲学假设"),
            ("s8", "8.8 价值观不是单一的"),
            ("s9", "8.9 责任归属"),
            ("s10", "8.10 动手练习"),
            ("s11", "8.11 自测题"),
        ],
    ),
    dict(
        f="ch09.html", nav="09 · 伦理学 II", short="伦理学 II · 情感陪伴 AI 的伦理",
        title="第 9 章 · 伦理学 II：情感陪伴 AI 的伦理",
        secs=[
            ("s1", "9.1 为什么单开一章"),
            ("s2", "9.2 情感是单向的，依恋是真的"),
            ("s3", "9.3 欺骗问题"),
            ("s4", "9.4 自主性与依赖"),
            ("s5", "9.5 脆弱人群"),
            ("s6", "9.6 他者伦理：列维纳斯"),
            ("s7", "9.7 陪伴产品的伦理设计清单"),
            ("s8", "9.8 演练：一款陪伴产品"),
            ("s9", "9.9 动手练习"),
            ("s10", "9.10 自测题"),
        ],
    ),
    dict(
        f="ch10.html", nav="10 · 现象学与具身认知", short="现象学与具身认知 · 沉浸与 BCI",
        title="第 10 章 · 现象学与具身认知：沉浸、临场与 BCI",
        secs=[
            ("s1", "10.1 现象学：回到事情本身"),
            ("s2", "10.2 胡塞尔：意向性与悬置"),
            ("s3", "10.3 海德格尔：上手与在手"),
            ("s4", "10.4 梅洛-庞蒂：身体是理解的媒介"),
            ("s5", "10.5 具身认知与生成主义"),
            ("s6", "10.6 临场感的现象学结构"),
            ("s7", "10.7 更真实不等于更好"),
            ("s8", "10.8 BCI 的哲学前提"),
            ("s9", "10.9 动手练习"),
            ("s10", "10.10 自测题"),
        ],
    ),
    dict(
        f="ch11.html", nav="11 · 落地方法", short="落地 · 把哲学变成工程决策",
        title="第 11 章 · 落地：把哲学变成工程决策",
        secs=[
            ("s1", "11.1 四个嵌入点"),
            ("s2", "11.2 需求阶段：问题重述"),
            ("s3", "11.3 设计评审的哲学清单"),
            ("s4", "11.4 评估指标的哲学校验"),
            ("s5", "11.5 上线前的对抗性审查"),
            ("s6", "11.6 思想实验作为设计工具"),
            ("s7", "11.7 怎么写伦理设计文档"),
            ("s8", "11.8 完整演练"),
            ("s9", "11.9 怎么持续跟上"),
            ("s10", "11.10 自测题"),
        ],
    ),
    dict(
        f="appendix.html", nav="附录 · 书单与速查", short="附录 · 书单 / 术语 / 映射",
        title="附录 · 书单、术语表与映射速查",
        secs=[
            ("a1", "A.1 分档书单"),
            ("a2", "A.2 术语表"),
            ("a3", "A.3 哲学家 × 技术问题"),
            ("a4", "A.4 常见误用与纠正"),
            ("a5", "A.5 思想实验速查"),
            ("a6", "A.6 怎么读哲学书"),
        ],
    ),
]


def topbar():
    opts = "\n".join(
        '    <option value="%s">%s</option>' % (c["f"], c["nav"]) for c in CHAPTERS
    )
    return """<header class="topbar">
  <button class="menu-btn" type="button" aria-label="菜单">☰</button>
  <a class="brand" href="index.html">
    <span class="logo">哲</span>
    <span>%s<small>%s</small></span>
  </a>
  <span class="spacer"></span>
  <select class="tb-select" aria-label="章节跳转">
%s
  </select>
  <a class="tb-link" href="appendix.html">书单</a>
  <a class="tb-link" href="ch11.html">落地清单</a>
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
    parts.append('    <div class="sb-title">十一章节</div>')
    for c in CHAPTERS[1:12]:
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
    for c in CHAPTERS[12:]:
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
            '  <a href="appendix.html"><div class="dir-label">→ 速查</div><div class="dir-name">附录 · 书单与映射表</div></a>'
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
<body data-tut="philosophy">

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
        label = "总览" if c["f"] == "index.html" else (
            "附录" if c["f"] == "appendix.html" else "第 %s 章" % c["f"][2:4].lstrip("0")
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
