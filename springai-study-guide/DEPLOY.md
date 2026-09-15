# 部署说明 · Spring AI 2.0 学习指南

本站点是**纯静态站点**（HTML + CSS + JS，无后端、无数据库、无构建步骤），
所有页面都使用相对路径引用，因此可以部署到**任何**静态托管环境。

目录结构：

```
springai-study-guide/
├── index.html          入口页（总览 + 环境准备）
├── ch01.html ~ ch11.html
├── appendix.html
└── assets/
    ├── style.css
    └── app.js
```

---

## 方式一：一键分享（已部署）

当前已发布到云端沙箱，分享链接：

**https://e764c07406b043488dec6b4c2d844597.app.workbuddy.host**

直接用这个链接发给学生即可，无需任何配置。适合**临时分享、课堂演示、快速评审**。

---

## 方式二：GitHub Pages / Gitee Pages（推荐长期使用）

免费、稳定、可绑定域名，且天然支持版本管理（后续更新指南只需重新提交）。

### GitHub Pages

```bash
cd D:/wx/springai/springai-study-guide

# 1. 初始化仓库
git init
git add .
git commit -m "docs: Spring AI 2.0 学习指南"

# 2. 关联远程仓库（先在 GitHub 上创建空仓库 springai-guide）
git remote add origin https://github.com/<你的用户名>/springai-guide.git
git branch -M main
git push -u origin main

# 3. 开启 Pages
#    GitHub → 仓库 → Settings → Pages
#    Source 选择 "Deploy from a branch"
#    Branch 选择 main / (root) → Save

# 4. 约 1 分钟后访问
#    https://<你的用户名>.github.io/springai-guide/
```

### Gitee Pages（国内访问更快）

```bash
# 同样 push 到 Gitee 仓库，然后在网页端
# 服务 → Gitee Pages → 选择分支 → 启动
# 注意：Gitee Pages 需要实名认证后才能开启，且每次更新需手动点击"更新"
```

> **国内访问速度提示**：GitHub Pages 在部分网络环境下较慢。
> 面向国内学生，优先选 **Gitee Pages** 或下面的对象存储方案。

---

## 方式三：对象存储 + CDN（企业内训推荐）

腾讯云 COS / 阿里云 OSS，成本极低（几十 MB 静态文件，每月费用不到 1 元），速度快。

### 腾讯云 COS

```bash
# 1. 创建存储桶：控制台 → 对象存储 → 创建存储桶
#    地域：就近选择（如广州）
#    访问权限：公有读私有写

# 2. 上传文件（用 coscmd 工具，或控制台直接拖拽整个目录）
pip install coscmd
coscmd config -a <SecretId> -s <SecretKey> -b <BucketName> -r ap-guangzhou
cd D:/wx/springai/springai-study-guide
coscmd upload -r ./ /

# 3. 开启静态网站功能
#    存储桶 → 基础配置 → 静态网站 → 开启
#    索引文档填 index.html，错误文档也填 index.html

# 4. 访问地址
#    https://<BucketName>.cos-website.ap-guangzhou.myqcloud.com
```

### 阿里云 OSS

```bash
# 用 ossutil 或控制台拖拽上传，然后：
# 存储桶 → 数据管理 → 静态页面 → 默认首页填 index.html
```

### 加分项：绑定自定义域名 + CDN

在域名解析里把 `guide.你的域名.com` CNAME 到对象存储的访问域名，
再开启 CDN 加速即可。注意 CDN 缓存策略：HTML 建议设较短（如 10 分钟），
`assets/` 下的 CSS/JS 设较长（如 7 天）。

---

## 方式四：自建 Nginx（内网 / 局域网共享）

适合公司内网或学校机房，学生通过内网 IP 访问。

### 直接放到 Nginx 目录

```bash
# Linux
sudo cp -r D:/wx/springai/springai-study-guide /var/www/springai-guide

# /etc/nginx/conf.d/springai-guide.conf
server {
    listen       80;
    server_name  _;                 # 或写内网域名/主机名

    root  /var/www/springai-guide;
    index index.html;

    charset utf-8;                  # ★ 中文站点必须设置，否则可能乱码

    location / {
        try_files $uri $uri/ /index.html;
    }

    # 静态资源缓存
    location ~* \.(css|js|png|jpg|svg|woff2?)$ {
        expires 7d;
        add_header Cache-Control "public";
    }

    # 压缩（HTML 体积能压掉 70%+，加载更快）
    gzip on;
    gzip_types text/html text/css application/javascript;
    gzip_min_length 1k;
}

sudo nginx -t && sudo systemctl reload nginx
```

### 临时共享（零配置，最快）

如果只是想让同一个局域网里的人现在就看一眼：

```bash
cd D:/wx/springai/springai-study-guide
python -m http.server 8000 --bind 0.0.0.0
```

然后查本机内网 IP（Windows 下 `ipconfig`，看 IPv4 地址，如 `192.168.1.20`），
其他人访问 `http://192.168.1.20:8000` 即可。

> 注意：这种方式只在你的电脑开机且命令窗口运行时有效，关掉就访问不了。
> 另外用 `file://` 直接双击打开 HTML 也能看，但**某些浏览器会限制本地文件的脚本加载**，
> 建议还是用 HTTP 服务打开。

---

## 部署后自检清单

不管用哪种方式，发布后按这几条验一遍：

- [ ] 首页能打开，样式正常（说明 `assets/style.css` 加载成功）
- [ ] 点侧边栏能跳转到各章节（说明相对路径正确）
- [ ] 站内锚点能滚动到对应小节（如首页点「环境准备」）
- [ ] 代码块右上角出现「复制」按钮，点击能复制（说明 `assets/app.js` 加载成功）
- [ ] 自测题能展开/收起答案
- [ ] **手机上打开看一眼**（侧边栏会变成汉堡菜单，表格可能需要横向滚动）
- [ ] 抽查一个章节页（如 `ch05.html`）确认内容完整

批量检查子页面是否都能访问（把 URL 换成你自己的）：

```bash
BASE="https://你的域名"
for p in index.html ch01.html ch02.html ch03.html ch04.html ch05.html ch06.html \
         ch07.html ch08.html ch09.html ch10.html ch11.html appendix.html assets/style.css; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -m 10 "$BASE/$p")
  echo "$p -> $code"
done
# 期望全部是 200
```

---

## 关于后续更新

这份指南是**纯静态文件**，更新流程就是「改文件 → 重新上传/推送」：

- **GitHub / Gitee**：`git add . && git commit -m "更新" && git push`（Gitee Pages 需手动点更新）
- **对象存储**：重新执行 `coscmd upload -r ./ /` 覆盖上传
- **Nginx**：直接覆盖 `/var/www/springai-guide` 下的文件，不需要重启服务
- **沙箱链接**：需要重新部署才能同步最新内容

### 一个建议

如果这份指南会持续更新，**建议改用 GitHub/Gitee 托管**——
因为它天然带版本历史，你能随时看到「哪次改了什么、谁改的」，
也方便多人共同维护。对于要发给学生长期使用的资料，这一点很重要。

---

## 常见问题

**Q：为什么直接双击 HTML 文件有些功能不正常？**
浏览器对 `file://` 协议有安全限制，可能阻止 `assets/app.js` 的正常执行。
用 `python -m http.server` 起一个本地服务，或部署到线上即可。

**Q：部署后中文乱码怎么办？**
确认服务器返回的 `Content-Type` 带 `charset=utf-8`，
Nginx 里加 `charset utf-8;`，对象存储则确认文件本身以 UTF-8 编码保存。

**Q：能加密码或限制只能本校学生看吗？**
纯静态托管做不到真正的访问控制。可行方案：
① 用 Nginx 的 `auth_basic` 加简单密码；
② 对象存储开启防盗链 + 只在内网发布；
③ 如果要按用户鉴权，就需要后端了——那就超出静态站的范围。
