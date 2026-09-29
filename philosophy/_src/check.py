# -*- coding: utf-8 -*-
"""站点结构校验：标签配对 / 锚点 / 内部链接 / 行尾符 / 版本戳。只读，不改文件。"""
import io, os, re, glob, sys

ROOT = r'D:/wx/philosophy-ai-guide'
os.chdir(ROOT)

PAIRS = ['div', 'table', 'pre', 'ul', 'ol', 'a', 'strong', 'code', 'span', 'p', 'tr', 'td', 'th', 'h4']
# 允许自闭合或可省略闭合的标签不检查
SKIP = {'p', 'tr', 'td', 'th', 'li'}

files = sorted(glob.glob('*.html'))
print('=== 1. 标签配对检查 ===')
bad_total = 0
for f in files:
    s = io.open(f, encoding='utf-8').read()
    # 去注释
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    problems = []
    for tag in PAIRS:
        if tag in SKIP:
            continue
        o = len(re.findall(r'<%s(?:\s|>)' % tag, s))
        c = len(re.findall(r'</%s>' % tag, s))
        if o != c:
            problems.append('%s %d/%d' % (tag, o, c))
    if problems:
        print('  ✗ %-16s %s' % (f, ', '.join(problems)))
        bad_total += len(problems)
print('  结论：%s' % ('全部配对 ✓' if bad_total == 0 else '%d 处不配对' % bad_total))

print()
print('=== 2. 锚点有效性（页内 # 链接是否有对应 id）===')
miss = 0
for f in files:
    s = io.open(f, encoding='utf-8').read()
    ids = set(re.findall(r'id="([^"]+)"', s))
    for h in set(re.findall(r'href="#([^"]+)"', s)):
        if h not in ids:
            print('  ✗ %-16s #%s 无对应 id' % (f, h))
            miss += 1
print('  结论：%s' % ('锚点全部有效 ✓' if miss == 0 else '%d 个失效锚点' % miss))

print()
print('=== 3. 跨页链接可达性 ===')
broken = 0
for f in files:
    s = io.open(f, encoding='utf-8').read()
    for href in set(re.findall(r'href="([^"#]+\.html[^"]*)"', s)):
        target = href.split('#')[0]
        if target and not os.path.isfile(target):
            print('  ✗ %-16s -> %s 不存在' % (f, target))
            broken += 1
print('  结论：%s' % ('全部可跳转 ✓' if broken == 0 else '%d 个死链' % broken))

print()
print('=== 4. 侧边栏子链接 vs 正文锚点交叉核对 ===')
# 每页 sb-sub 里的链接都应在正文有对应 id
cross = 0
for f in files:
    s = io.open(f, encoding='utf-8').read()
    ids = set(re.findall(r'id="([^"]+)"', s))
    # 该页侧边栏展开的 sb-sub
    m = re.search(r'<div class="sb-sub">(.*?)</div>', s, re.S)
    if not m:
        continue
    subs = re.findall(r'href="#([^"]+)"', m.group(1))
    for a in subs:
        if a not in ids:
            print('  ✗ %-16s 侧边栏含 #%s 但正文无此 id' % (f, a))
            cross += 1
print('  结论：%s' % ('侧边栏与正文一致 ✓' if cross == 0 else '%d 处不一致' % cross))

print()
print('=== 5. 版本戳 ===')
ts = 0
for f in files:
    s = io.open(f, encoding='utf-8').read()
    if '内容版本 2026-09-21 10:00' not in s:
        print('  ✗ %s 缺少或无正确版本戳' % f)
        ts += 1
print('  结论：%s' % ('13 页齐备 ✓' if ts == 0 else '%d 页有问题' % ts))

print()
print('=== 6. 行尾符 ===')
crlf = []
for pat in ['*.html', '*.md', 'assets/*.css', 'assets/*.js', '_src/*']:
    for p in glob.glob(pat):
        if os.path.isfile(p):
            if b'\r\n' in open(p, 'rb').read():
                crlf.append(p)
print('  结论：%s' % ('全部 LF ✓' if not crlf else 'CRLF: %s' % crlf))

print()
print('=== 7. 外部资源引用（应为相对路径）===')
abs_ref = 0
for f in files:
    s = io.open(f, encoding='utf-8').read()
    for m in re.findall(r'(?:href|src)="(/[^"]*)"', s):
        print('  ✗ %s 使用了绝对路径 %s' % (f, m))
        abs_ref += 1
print('  结论：%s' % ('全部相对路径 ✓' if abs_ref == 0 else '%d 处绝对路径' % abs_ref))

print()
print('=== 8. 规模统计 ===')
total = 0
for f in files:
    n = os.path.getsize(f)
    total += n
print('  13 页合计 %.1f KB，平均 %.1f KB/页' % (total / 1024, total / 1024 / len(files)))
