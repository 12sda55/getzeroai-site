# -*- coding: utf-8 -*-
"""
统一更新全站内容版本戳。

版本戳是判断「用户看到的是否为最新」的唯一可靠依据，但它散落在：
  - 门户 index.html / 404.html
  - springai/*.html（13 页）
  - philosophy/*.html（13 页，由 gen.py 生成）
  - philosophy/_src/gen.py 的 VERSION 常量
  - _tools/check_site.py 的 VERSION 常量

手改容易漏，所以用这个脚本一次改完。

用法：
    python _tools/set_version.py "2026-09-24 15:30"
    python _tools/set_version.py --show        # 只查看当前各处的版本
"""
import io
import os
import re
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

PAT = re.compile(r'内容版本 ([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2})')

TARGETS = (
    ['*.html', 'springai/*.html', 'philosophy/*.html', 'leetcode/*.html']
    + ['philosophy/_src/gen.py', 'leetcode/_src/gen.py', '_tools/check_site.py']
)


def current():
    seen = {}
    for pat in TARGETS:
        for f in sorted(glob.glob(pat)):
            if not os.path.isfile(f):
                continue
            s = io.open(f, encoding='utf-8').read()
            if f.endswith('.py'):
                m = re.search(r'^VERSION = "([^"]+)"', s, re.M)
                if m:
                    seen.setdefault(m.group(1), []).append(f)
            else:
                for m in PAT.finditer(s):
                    seen.setdefault(m.group(1), []).append(f)
    return seen


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('--show', '-s'):
        print('当前版本分布：')
        for ver, files in sorted(current().items()):
            print('  %-18s %d 处：%s' % (ver, len(files), ', '.join(files[:4]) + (' …' if len(files) > 4 else '')))
        print()
        print('用法：python _tools/set_version.py "YYYY-MM-DD HH:MM"')
        return

    new = sys.argv[1].strip()
    if not re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$', new):
        print('版本格式应为 "YYYY-MM-DD HH:MM"，收到：%r' % new)
        sys.exit(1)

    changed = 0
    for pat in TARGETS:
        for f in sorted(glob.glob(pat)):
            if not os.path.isfile(f):
                continue
            s = io.open(f, encoding='utf-8').read()
            orig = s
            if f.endswith('.py'):
                s = re.sub(r'^(VERSION = ")[^"]+(")', r'\g<1>%s\g<2>' % new, s, flags=re.M)
            else:
                s = PAT.sub('内容版本 %s' % new, s)
            if s != orig:
                io.open(f, 'w', encoding='utf-8', newline='\n').write(s)
                changed += 1

    print('已把 %d 个文件的版本戳更新为 %s' % (changed, new))
    print()
    print('各处理想做法：')
    print('  1. 改 philosophy/_src/gen.py 的 VERSION，再跑 gen.py（否则重新生成会覆盖）')
    print('  2. 跑 _tools/check_site.py 确认第 6 项通过')


if __name__ == '__main__':
    main()
