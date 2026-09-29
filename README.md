# getzeroai 学习站

一个纯静态的多教程站点。当前包含两套教程，**结构为继续扩展准备** ——
之后新整理的专题以同样的方式加进来，只需要新建一个目录 + 加一张卡片。

已在自有域名上运行（阿里云 OSS 中国香港节点，免备案）。

---

## 一、站点结构

```
D:\wx\springai\                ← 仓库根 = 站点根
├── index.html                 门户首页 · 教程索引（含搜索）
├── 404.html                   统一错误页（样式内联，见第三节）
├── assets/                    ★ 全站共用样式与脚本
│   ├── style.css               含「多教程主题」支持
│   ├── app.js                  侧边栏 / 复制 / 锚点高亮 / 阅读进度 / 自测题折叠
│   └── home.js                 门户搜索过滤
├── springai/                  教程一 · Spring AI 2.0 学习指南（13 页）
│   ├── index.html
│   ├── ch01.html … ch11.html
│   ├── appendix.html
│   ├── DEPLOY.md              部署说明
│   └── DOMAIN-SETUP.md        自定义域名上线记录
├── philosophy/                教程二 · 哲学 × AI 学习指南（13 页）
│   ├── index.html
│   ├── ch01.html … ch11.html
│   ├── appendix.html
│   ├── README.md              该教程的独立说明
│   └── _src/                  ★ 生成器与正文片段（部署时排除）
├── _tools/                    校验与维护脚本（部署时排除）
│   ├── check_site.py          整站结构校验（8 项）
│   └── set_version.py         统一更新内容版本戳
└── README.md                  本文件
```

**规模**：42 个 HTML（门户 2 + 三套教程 13/13/14），约 2 MB。

---

## 二、如何加一套新教程

这是本站在架构上唯一需要理解的地方。**四步，不会影响已有内容。**

### 1. 建目录

```
新教程/
├── index.html        教程首页（章节列表）
├── ch01.html ...
└── appendix.html     可选
```

页面可以直接从现有教程复制后改写 —— 它们共用同一套 `assets/style.css`。

### 2. 页面里要做的三件事

| 位置 | 写法 | 说明 |
|---|---|---|
| `<head>` | `<link rel="stylesheet" href="../assets/style.css">` | 上移一层到共用 assets |
| `<body>` | `<body data-tut="新教程id">` | **决定主题色**，见下 |
| 顶栏 | `<a class="tb-home" href="../index.html">⌂ 全部教程</a>` | 返回门户 |
| 面包屑 | `<a href="../index.html">首页</a> / <a href="index.html">教程名</a> / 第 N 章` | 三级定位 |
| 页脚 | `<span class="ver">内容版本 YYYY-MM-DD HH:MM</span>` | 见第五节 |
| 脚本 | `<script src="../assets/app.js"></script>` | 共用 |

### 3. 在 `assets/style.css` 里加主题色

找到 `多教程主题` 那段，加一行：

```css
body[data-tut="新教程id"] {
  --accent: #xxxxxx;          /* 主色 */
  --accent-soft: #xxxxxx;     /* 主色的浅色底 */
  --accent-2: #0d9488;        /* 渐变的第二色 */
  --logo-grad: linear-gradient(135deg, #主色, #0d9488);
  --hero-grad: linear-gradient(135deg, #浅色1, #浅色2, #浅色3);
}
```

**一套样式 + 一个 `data-tut` 属性就切换了整站主色**，不需要复制 CSS。
（门户用 `home` 中性色，让各教程的配色成为视觉焦点。）

### 4. 在门户 `index.html` 加一张卡片

复制现有 `.tut-card` 那段，改内容，**并填 `data-keywords`**：

```html
<a class="tut-card" data-tut="新教程id" href="新教程/index.html"
   data-keywords="关键词1 关键词2 英文关键词 概念名 工具名">
  ...
</a>
```

`data-keywords` 是**门户搜索能命中的范围** —— 用户搜「RAG」「伦理」「Agent」时，
靠这个字段定位到对应教程。把该教程的章节名、关键概念、英文术语都写进去。

### 5. 跑校验

```bash
python _tools/check_site.py
```

它从 `_tools/check_site.py` 顶部的 `AREAS` 读取「哪个目录应该有几十个页面、
用什么主题标记」，所以**记得去那里登记新教程**：

```python
AREAS = [
    ('.', 2, 'home'),
    ('springai', 13, 'springai'),
    ('philosophy', 13, 'philosophy'),
    ('leetcode', 14, 'leetcode'),   # ← 本次新增
]
```

---

## 三、门户与 404 的两处特别约定

### 404 页为什么样式内联

404 会在**任意路径层级**被触发。如果用 `<link rel="stylesheet" href="assets/style.css">`，
在 `/foo/bar` 下会被解析成 `/foo/assets/style.css` —— 二次 404，错误页自己都是坏的。
所以 404 的样式必须**内联**，链接必须用**站点根绝对路径**（`/springai/`）。

⚠️ **前提是站点部署在域名根目录**。若将来移到子路径（如 `example.com/guide/`），
需要把 404 里的四个链接改成带子路径前缀的形式。

### 门户搜索的快捷键

`/` 聚焦搜索框，`Esc` 清空。搜索是纯前端过滤，只匹配教程卡片，不发任何请求。

---

## 四、日常维护

```bash
cd D:/wx/springai

# 校验整站（8 项：标签平衡 / 锚点 / 死链 / assets / 主题 / 版本戳 / 行尾符 / 路径）
python _tools/check_site.py

# 查看当前版本戳分布
python _tools/set_version.py --show

# 统一改版本戳（会同时改 gen.py 与 check_site.py 里的常量）
python _tools/set_version.py "2026-09-24 15:30"

# 哲学教程：改正文后要重新生成（_src/*.part 是源，.html 是产物）
cd philosophy/_src && python gen.py

# 力扣教程：同上（gen.py 里含 Java 语法高亮，代码块在 .part 里写原始字符）
cd leetcode/_src && python gen.py
```

### 内容版本戳

每个页面页脚有一行 `内容版本 YYYY-MM-DD HH:MM`。**每次更新内容都要改**。

它是判断「用户看到的是否为最新」的**唯一可靠依据** —— 浏览器缓存、
CDN 未刷新、看错地址都会造成「更新了却看不到」，有版本戳就能一眼分辨是哪种。

因为散落在 28 个页面 + 2 个 py 文件里，手改必漏，所以用 `set_version.py` 统一改。

---

## 五、部署注意（重要）

### 1. 要上传什么

```
✅ 要传：index.html / 404.html / assets/ / springai/ / philosophy/ / leetcode/
❌ 不传：_tools/ / */_src/ / *.md
```

### 2. 缓存策略（否则「更新了看不到」）

**对象存储默认不给对象设 `Cache-Control`**，浏览器会启用启发式缓存并长时间不回源。
上传时对所有对象显式加：

```
Cache-Control: no-cache
```

配 `no-cache` 后浏览器每次发条件请求：内容变了才重下，没变返回 304。
**这是「更新了却看不到」的头号原因**，务必别漏。

### 3. 静态网站托管设置

| 项 | 值 |
|---|---|
| 默认首页 | `index.html` |
| 默认 404 页 | `404.html` |
| 索引文档 | **不要开启**（会让目录列出文件） |

### 4. 目录形 URL 的跳转对象

阿里云 OSS 静态网站托管**不会**把 `/springai/` 解析为 `/springai/index.html`，
而是回退到默认首页（门户），造成 URL 与内容不一致。已上传 2 个轻量跳转对象解决「无尾斜杠」的情形：

```
springai    → /springai/index.html
philosophy  → /philosophy/index.html
leetcode    → /leetcode/index.html
```

⚠️ **「带尾斜杠」的 `/springai/` 无法用对象解决** —— OSS 见到 `/` 结尾就走目录索引逻辑、
绕过该 key（试过上传 `springai/` 对象，静态托管不生效，已删除）。要彻底解决需要
CDN + 边缘路由改写。实际影响很小：门户内的链接都写完整路径（`springai/index.html`），
正常浏览不会遇到；手动输 `/springai`（无斜杠）也能正确跳转。

### 5. 自定义域名

站点已在 `getzeroai.xyz`（OSS 中国香港，免备案）。
详见 `springai/DOMAIN-SETUP.md`（含域名归属验证、CNAME、HTTPS 的完整记录）。

---

## 六、内容约定

### 通用

- 站点为**纯静态**：页面间只用**相对路径**；子目录页面引用 assets 用 `../assets/`
- 换行符统一 **LF**
- 每页页脚必须有**内容版本戳**
- 改完跑 `check_site.py`，8 项全绿再提交

### 教程结构

两套教程都遵循同一节奏，读者会形成预期：

- **每章固定结构**：学习目标卡 → 概念详解 → 示例/代码 → 排错表 →
  可折叠自测题（`.qa`）→ 验收标准（`.goal`）→ 上一节/下一节导航
- **哲学教程额外要求**：每个哲学概念必须落到一个具体的技术判断上（「工程锚点」），
  不做泛泛的思想史介绍
- **技术教程额外要求**：代码以 **Spring AI 2.0.1 + Spring Boot 4.1** 为基准，
  示例可直接复制运行
- **算法教程额外要求**：每题必有「思路推导」（从暴力到最优的推理链），
  代码为 Java 且逐行注释；`.part` 里代码块写原始字符（`<`、`>` 直接写），
  由 `leetcode/_src/gen.py` 的 highlight() 统一转义着色

### 版本纪律

- Spring Boot 4 已废弃的 starter 不要用（如 `spring-boot-starter-web` → 应为 `spring-boot-starter-webmvc`）
- 遇到小版本 API 漂移，标注「以官方文档 / IDE 补全为准」，不编造键名

---

## 七、构建历程与踩过的坑

| 坑 | 现象 | 解法 |
|---|---|---|
| OSS 桶名全局唯一 | 报「bucket does not belong to you」 | 其实是**权限不足**也会返回这句，不要当成「名字被占用」 |
| OSS 默认域名强制下载 | 访问 HTML 变成下载文件 | 必须绑**自定义域名**才会正常渲染 |
| 未设 Cache-Control | 更新后用户看不到新内容 | 上传时显式加 `no-cache` |
| 跨账号绑域名 | 报 `NeedVerifyDomainOwnership` | 加 `_dnsauth` TXT 记录做归属验证 |
| 根域名配 CNAME | 与 SOA/NS 冲突 | 用 `www` 子域；裸域名用显性 URL 转发 |
| 手写多页导航 | 改一处要改 13 处 | 哲学教程改用 `_src/gen.py` 生成 |
| `<span>` 漏闭合 | 代码高亮污染后续所有内容 | `check_site.py` 第 1 项用**栈扫描**抓（简单计数抓不到跨行的情况） |
