# -*- coding: utf-8 -*-
"""
打包部署包（只含要上传的文件）。

包含：index.html / 404.html / assets/ / springai/*.html / philosophy/*.html
排除：_tools/ · */_src/ · *.md · .git 等

用法：python _tools/package.py
产出：站点根目录的 getzeroai-site.zip
"""
import io
import os
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
OUT = 'getzeroai-site.zip'

INCLUDE_DIRS = ['assets', 'springai', 'philosophy', 'leetcode']
SKIP_DIR_NAMES = {'_src', '_tools', '.git', 'node_modules', '__pycache__', '.workbuddy'}


def collect():
    files = []
    # 根目录页面
    for f in ['index.html', '404.html']:
        if os.path.isfile(f):
            files.append(f)
    # 子目录
    for d in INCLUDE_DIRS:
        for root, dirs, fs in os.walk(d):
            dirs[:] = [x for x in dirs if x not in SKIP_DIR_NAMES]
            for f in fs:
                if f.lower().endswith('.md'):
                    continue          # 说明文档不上传
                files.append(os.path.join(root, f).replace(os.sep, '/'))
    return sorted(files)


files = collect()
total = 0
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for p in files:
        z.write(p, p)                 # 保持相对路径，解压后即是站点结构
        total += os.path.getsize(p)

print('打包完成 → %s' % OUT)
print('  文件数    : %d' % len(files))
print('  原始大小  : %.1f KB' % (total / 1024))
print('  压缩后    : %.1f KB' % (os.path.getsize(OUT) / 1024))
print()
print('压缩包内结构（顶层）：')
with zipfile.ZipFile(OUT) as z:
    tops = {}
    for n in z.namelist():
        key = n.split('/')[0] if '/' in n else '(根文件)'
        tops[key] = tops.get(key, 0) + 1
    for k in sorted(tops):
        print('    %-16s %d 个' % (k, tops[k]))
    print()
    print('根目录文件：')
    for n in sorted(z.namelist()):
        if '/' not in n:
            print('    %s' % n)

# 安全检查：确认没有混入源文件或文档
leak = [n for n in zipfile.ZipFile(OUT).namelist()
        if n.endswith('.md') or '_src' in n or '_tools' in n or n.endswith('.py')]
print()
print('安全检查：%s' % ('✓ 无源文件/文档混入' if not leak else '✗ 发现不该打包的：%s' % leak))
