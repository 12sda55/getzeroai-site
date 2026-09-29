# -*- coding: utf-8 -*-
"""
getzeroai 学习站 · 整站结构校验

覆盖：门户首页 / 404 / springai 教程 / philosophy 教程
用法：python _tools/check_site.py
只读，不修改任何文件。

修复记录（v2）：
- 标签检查改用「栈扫描」，能正确处理跨行标签（如跨多行的字符串高亮）
- 跨页链接检查跳过以 / 开头的站点根绝对路径（404 页有意使用）
- 目录层级判断改用 os.path.dirname，不再用「是否含 /」这种脆弱写法
"""
import io
import os
import re
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

VERSION = "2026-09-28 16:30"

AREAS = [
    ('.', 2, 'home'),
    ('springai', 13, 'springai'),
    ('philosophy', 13, 'philosophy'),
    ('leetcode', 26, 'leetcode'),
]

TAGS = ['div', 'table', 'pre', 'ul', 'ol', 'a', 'strong', 'code', 'span', 'header', 'main', 'aside']
SELF_CLOSING = {'br', 'hr', 'img', 'input', 'meta', 'link'}

problems = 0


def collect():
    out = []
    for area, _, _ in AREAS:
        d = '.' if area == '.' else area
        for f in sorted(glob.glob(os.path.join(d, '*.html'))):
            out.append((f.replace(os.sep, '/'), io.open(f, encoding='utf-8').read()))
    return out


FILES = collect()


def report(title, items, ok_msg):
    global problems
    print(title)
    if items:
        for it in items[:12]:
            print('  ✗ %s' % it)
        if len(items) > 12:
            print('  … 另有 %d 处' % (len(items) - 12))
        problems += len(items)
    else:
        print('  %s' % ok_msg)


def scan_tags(s, tag):
    """栈扫描单个标签，返回 (未闭合数, 多余闭合数)"""
    pat = re.compile(r'<%s(?:\s[^>]*)?>|</%s>' % (tag, tag))
    stack = []
    extra = 0
    for m in pat.finditer(s):
        if m.group(0).startswith('</'):
            if stack:
                stack.pop()
            else:
                extra += 1
        else:
            stack.append(1)
    return len(stack), extra


print('=' * 64)
print('getzeroai 学习站 · 结构校验 v2（%d 个 HTML）' % len(FILES))
print('=' * 64)
print()

# ---------- 1. 标签平衡（栈扫描） ----------
bad = []
for path, s in FILES:
    body = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    for tag in TAGS:
        if tag in SELF_CLOSING:
            continue
        unclosed, extra = scan_tags(body, tag)
        if unclosed:
            bad.append('%-24s <%s> 未闭合 %d' % (path, tag, unclosed))
        if extra:
            bad.append('%-24s </%s> 多余 %d' % (path, tag, extra))
report('【1】标签平衡（栈扫描）', bad, '全部平衡 ✓')

# ---------- 2. 页内锚点 ----------
bad = []
for path, s in FILES:
    ids = set(re.findall(r'id="([^"]+)"', s))
    for h in sorted(set(re.findall(r'href="#([^"]+)"', s))):
        if h not in ids:
            bad.append('%s  #%s' % (path, h))
report('【2】页内锚点有效性', bad, '全部有效 ✓')

# ---------- 3. 跨页链接 ----------
bad = []
for path, s in FILES:
    base = os.path.dirname(path) or '.'
    for href in sorted(set(re.findall(r'href="([^"#]+\.html[^"]*)"', s))):
        if href.startswith(('http:', 'https:', '//', '/')):
            continue                     # 站点根绝对路径（404 有意使用）
        resolved = os.path.normpath(os.path.join(base, href.split('#')[0]))
        if not os.path.isfile(resolved):
            bad.append('%s  ->  %s' % (path, href))
report('【3】跨页链接可达性', bad, '全部可跳转 ✓')

# ---------- 4. assets 引用 ----------
bad = []
for path, s in FILES:
    if path.endswith('404.html'):
        continue                         # 404 用内联样式，有意不引用
    base = os.path.dirname(path)
    refs = re.findall(r'(?:href|src)="([^"]*assets/[^"]+)"', s)
    if not refs:
        bad.append('%s  未引用 assets' % path)
    for r in refs:
        if not os.path.isfile(os.path.normpath(os.path.join(base, r))):
            bad.append('%s  ->  %s 不存在' % (path, r))
report('【4】assets 引用可解析', bad, '全部正确 ✓')

# ---------- 5. 主题标记与页面数 ----------
bad = []
for area, expect_n, tut in AREAS:
    d = '.' if area == '.' else area
    files = sorted(glob.glob(os.path.join(d, '*.html')))
    if len(files) != expect_n:
        bad.append('%s  页面数 %d，期望 %d' % (d, len(files), expect_n))
    for f in files:
        s = io.open(f, encoding='utf-8').read()
        if ('data-tut="%s"' % tut) not in s:
            bad.append('%-24s 缺少 data-tut="%s"' % (f.replace(os.sep, '/'), tut))
report('【5】主题标记与页面数', bad, '三个区域全部正确 ✓')

# ---------- 6. 版本戳 ----------
bad = []
ts = re.compile(r'内容版本 ([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2})')
for path, s in FILES:
    m = ts.search(s)
    if not m:
        bad.append('%s  无版本戳' % path)
    elif m.group(1) != VERSION:
        bad.append('%s  %s（期望 %s）' % (path, m.group(1), VERSION))
report('【6】版本戳一致性（期望 %s）' % VERSION, bad, '全部一致 ✓')

# ---------- 7. 行尾符 ----------
bad = []
for p in ['*.html', '*.md', 'assets/*.css', 'assets/*.js',
          'springai/*.html', 'springai/*.md', 'philosophy/*.html', 'philosophy/*.md',
          'philosophy/_src/*', '_tools/*']:
    for f in glob.glob(p):
        if os.path.isfile(f) and b'\r\n' in open(f, 'rb').read():
            bad.append(f)
report('【7】行尾符统一 LF', bad, '全部 LF ✓')

# ---------- 8. 路径写法正确性 ----------
bad = []
for path, s in FILES:
    in_sub = len([p for p in path.split('/')[:-1] if p and p != '.']) > 0
    if in_sub and ('href="assets/' in s or 'src="assets/' in s):
        bad.append('%s  子目录页面应写 ../assets/' % path)
    if not in_sub and path != '404.html' and ('href="../assets/' in s or 'src="../assets/' in s):
        bad.append('%s  根目录页面不应写 ../assets/' % path)
    if 'springai-study-guide' in s:
        bad.append('%s  残留旧目录名' % path)
    if 'philosophy-ai-guide' in s:
        bad.append('%s  残留旧目录名' % path)
report('【8】路径写法与无残留旧名', bad, '全部正确 ✓')

# ---------- 汇总 ----------
print()
print('=' * 64)
print('结论：%s' % ('8 项全部通过 ✓' if problems == 0 else '共 %d 处问题，需修复' % problems))
print('=' * 64)

total = sum(len(s.encode('utf-8')) for _, s in FILES)
print('规模：%d 个 HTML，合计 %.1f KB' % (len(FILES), total / 1024))
