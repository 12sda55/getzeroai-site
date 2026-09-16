# 自定义域名上线指南 · getzeroai.xyz

> ## 🎉 站点已上线
>
> | | |
> |---|---|
> | 访问地址 | **http://www.getzeroai.xyz** ／ **http://getzeroai.xyz** |
> | 存储位置 | 阿里云 OSS `getzeroai-study-guide` @ **中国香港**（免备案） |
> | 验证结果 | 全站 **18/18** 项通过（含自定义 404 页）；`Content-Disposition` 已消失，HTML 正常渲染 |
> | 待办 | **配置 HTTPS 证书**（当前仅 HTTP） |
>
> 更新站点内容：重新上传覆盖即可，**不需要重启任何服务**。

---

## 一、当前状态（2026-09-16 12:36 复核）

| 检查项 | 结果 | 说明 |
|---|---|---|
| 域名注册 | ✅ 已注册 | 注册商：阿里云（万网）；2026-09-16 注册，2027-09-16 到期 |
| 实名认证 | ✅ **已通过** | 原 `client hold` 状态已解除 |
| 域名状态位 | ✅ 正常 | `server transfer prohibited` + `add period`，均为注册后保护位，不影响解析 |
| **全球解析** | ✅ **已生效** | `.xyz` 注册局（x/y/z.nic.xyz）与阿里云 NS 均返回 `NOERROR` |
| **CNAME 解析** | ✅ **已生效** | `www` 与 `@` 均指向 `getzeroai-study-guide.oss-cn-hongkong.aliyuncs.com` |
| DNS 服务器 | 阿里云云解析 | `dns31.hichina.com` / `dns32.hichina.com` |

> 从实名解锁到 DNS 委派生效约 **1.5 小时**（12:00 解除 → 12:23 生效），比官方说的 1~2 个工作日快得多。

---

## 二、实际部署记录

托管方案最终采用 **阿里云 OSS 中国香港 + 自定义域名**（免备案）。全部执行完毕：

| 步骤 | 状态 | 值 / 结果 |
|---|---|---|
| 开通 OSS 服务 | ✅ | 新账号必须先手动开通，否则 API 报 `UserDisable` |
| 创建 Bucket | ✅ | **`getzeroai-study-guide`** @ **`oss-cn-hongkong`** |
| 读写权限 | ✅ | `public-read`（公共读） |
| 静态网站托管 | ✅ | 默认首页 `index.html`，错误页 `404.html` |
| 上传站点 | ✅ | **16 个文件**，HTML/CSS/JS 的 `Content-Type` 均正确 |
| 内容校验 | ✅ | 16 个对象字节数与本机完全一致 |
| 域名归属验证 | ✅ | 跨账号，走 TXT 验证通过 |
| 绑定自定义域名 | ✅ | `getzeroai.xyz` + `www.getzeroai.xyz`，状态均 Enabled |
| **配置 CNAME 解析** | ✅ | `www` 与 `@` 均生效 |
| **全站可达性验证** | ✅ | **18/18 通过**，含自定义 404 页 |
| **HTTPS 证书** | ⏳ **待完成** | 当前仅 HTTP（见第五节） |

### ⚠️ 一个必须知道的前提：域名与 Bucket 不在同一个阿里云账号下

绑定自定义域名时曾报：

```
403  NeedVerifyDomainOwnership
```

说明 `getzeroai.xyz` 与存放站点的 OSS Bucket **分属两个不同的阿里云账号**
（若同账号，OSS 允许直接绑定、无需任何验证）。

**已通过 TXT 归属验证解决**。当时添加的两条 TXT 记录，**现在可以删除了**：

| 主机记录 | 记录类型 | 记录值 |
|---|---|---|
| `_dnsauth` | TXT | `1ad4197f384559d0e36163fae1c7aeb3` |
| `_dnsauth.www` | TXT | `389893778371f3baa0b6e4bb234b996a` |

> 跨账号意味着：**域名相关的所有解析操作，都要在域名所属的那个账号的控制台里做。**

---

## 三、CNAME 解析配置（已完成，存档备查）

`getzeroai.xyz` 与 `www.getzeroai.xyz` 已绑定到 OSS，并已配置 CNAME 记录。
实际使用的记录如下：

| 主机记录 | 记录类型 | 记录值 | 状态 |
|---|---|---|---|
| `www` | `CNAME` | `getzeroai-study-guide.oss-cn-hongkong.aliyuncs.com` | ✅ 已生效 |
| `@` | `CNAME` | `getzeroai-study-guide.oss-cn-hongkong.aliyuncs.com` | ✅ 已生效 |

> **记录值是 `<Bucket名>.<外网访问域名>`**，不要只写 `oss-cn-hongkong.aliyuncs.com`（会少一层）。

**关于裸域名 `@` 加 CNAME**：阿里云官方文档提示，根域名上配置 CNAME 与必需的
SOA/NS 记录存在协议冲突（RFC 1034 §3.6.2），**部分运营商的 DNS 可能解析失败**。
实践中阿里云云解析通常允许添加且能正常工作；若控制台拒绝或解析不稳定，
就只保留 `www`，裸域名改用**显性 URL 转发**指向 `https://www.getzeroai.xyz`。

> **务必先完成域名绑定，再加 CNAME 记录**——顺序反了会访问到错误内容。
> 以后若解除绑定，记得同步删除这条 CNAME。

生效通常几分钟到几小时（取决于 TTL）。验证：

```bash
nslookup -type=CNAME www.getzeroai.xyz 223.5.5.5
curl -sI https://www.getzeroai.xyz | head -1
```

---

## 四、最后一步：配置 HTTPS 证书

OSS 绑定域名后默认**只有 HTTP**。要上 HTTPS：

1. 阿里云 → **数字证书管理服务** → 申请**免费证书**（DV 单域名，免费）
2. 签发后下载 **Nginx 格式**（得到 `.pem` + `.key`）
3. OSS → Bucket → **域名管理** → 目标域名 → **证书托管** → 上传证书
4. 之后用 `https://www.getzeroai.xyz` 访问

> ### ⚠️ 续期是这套方案里唯一需要长期维护的事
>
> 阿里云免费证书（「个人测试证书（免费版）」）**有效期 90 天，不支持续费，到期必须重新申请**，
> 每个自然年限 20 张 —— 也就是**一年要换 4 次**。
>
> **证书过期比不配证书更糟**：没有证书只是地址栏显示「不安全」；
> 证书过期会让浏览器弹出**红色拦截页**，学生根本进不去。
>
> 嫌手动换证麻烦的话，可评估走 **阿里云 ESA（边缘安全加速）** ——
> 它的免费证书**支持自动续签**（到期前 30 天自动续，Let's Encrypt 签发，
> 无需重新申请）。ESA 走 CNAME 接入，非大陆节点免备案。
>
> 选择免费证书的话，**务必设日历提醒，提前一周续**。

---

## 二、选哪条路

`.xyz` 已获工信部批复**可以备案**，所以两条路都能走。但既然你不想等，就要看**能不能免备案**。

**关键规则**（阿里云官方文档原文）：

> 若 Bucket 位于中国内地，绑定的域名必须完成 ICP 备案。
> 若 Bucket 位于**非中国内地节点（如中国香港、新加坡等），绑定的自定义域名无需 ICP 备案**。

| 方案 | 需备案 | 上线耗时 | 国内速度 | 改 NS | 成本 |
|---|---|---|---|---|---|
| **① 阿里云 OSS 中国香港 + 自定义域名** ⭐ | ❌ | 域名生效当天 | 中等偏上 | ❌ 不用 | 极低 |
| ② Cloudflare Pages | ❌ | 域名生效当天 | 一般 | ✅ 要改 | 免费 |
| ③ 阿里云 OSS 中国内地 + CDN | ✅ | 1~3 周 | 最快 | ❌ 不用 | 约 100~300 元/年 |
| ④ Vercel / Netlify | ❌ | 10 分钟 | 一般 | ✅ 要改 | 免费 |
| ⑤ 自建 Nginx | 境内需备案 | 看情况 | 取决于服务器 | ❌ | 服务器费用 |

### 为什么推荐 ①

- **不用改 NS**：域名和 DNS 都在阿里云，OSS 绑定域名后可直接**自动添加 CNAME 记录**
- **免 TXT 验证**：域名归属当前阿里云账号时，绑定域名可直接确认，不需要额外验证所有权
- **不用备案**：香港节点免备案
- **国内访问比 Cloudflare 稳**：面向国内学生，Cloudflare 免费版在大陆访问质量参差

> ⚠️ **一个必须知道的坑**：OSS 的**默认域名**访问 HTML 时会强制下载
> （官方文档：*使用 OSS 默认域名访问时，OSS 会为安全起见强制添加 `Content-Disposition: attachment` 下载头*）。
> **只有绑定了自定义域名，HTML 才会在浏览器里正常渲染。** 所以「绑定域名」这步不能省。

---

## 三、方案 ①：阿里云 OSS 中国香港（推荐）

### 1. 开通 OSS 并创建 Bucket

1. 控制台 → **对象存储 OSS** → 开通（按量付费即可，无需买资源包）
2. **Bucket 列表** → 创建 Bucket：

| 配置项 | 值 | 原因 |
|---|---|---|
| Bucket 名称 | `getzeroai-study-guide` | 名称**全网唯一**（不是按账号隔离），通用名极易撞名 |
| **地域** | **中国香港** | ★ 关键：香港节点才能**免备案**绑自定义域名 |
| 存储类型 | 标准存储 | 网站要低延迟读取 |
| **读写权限** | **公共读** | ★ 静态网站必须公共读，否则访客 403 |
| 版本控制 / 加密 / 日志 | 按需，默认即可 | |

### 2. 开启静态网站托管

Bucket → **数据管理 → 静态页面**：

- **默认首页**：`index.html`
- **默认 404 页**：`index.html`（或单独做个 404 页）
- **子目录首页**：开启

> 不开这一步，访问 `https://www.getzeroai.xyz/` 会报 404——因为 OSS 不知道根路径该返回哪个文件。

### 3. 上传站点

**方式 A：控制台拖拽**（最简单）
把 `getzeroai-site.zip` 解压后，把里面的**全部内容**（`index.html`、`assets/`、各 `ch*.html`）直接拖进 Bucket 根目录。

> ⚠️ 一定要传到**根目录**，不要多套一层文件夹，否则访问首页会 404。
> 判断标准：Bucket 根目录下能直接看到 `index.html`。

**方式 B：ossutil 命令行**（后续更新更方便）

```bash
# 安装 ossutil 后先配置（需要 AccessKey）
ossutil config

# 上传（--update 只传有变化的文件，重复执行很安全）
cd D:/wx/springai/springai-study-guide
ossutil cp -r . oss://getzeroai-study-guide/ --update
```

> 注意：`DEPLOY.md`、`DOMAIN-SETUP.md` 这类说明文档**不必上传**（访客不需要看），
> 可以加 `--exclude "*.md"` 排除。

### 4. 绑定自定义域名

Bucket → **Bucket 配置 → 域名管理 → 绑定域名**：

1. 输入 `www.getzeroai.xyz` → 因域名属于当前账号，可直接 **确认绑定**
2. 勾选 **自动添加 CNAME 记录**（同账号时可自动写入阿里云云解析）

> **为什么用 `www` 而不是裸域名？**
> 阿里云官方文档明确指出：在**根域名（`@`）上配置 CNAME 记录不符合 DNS 协议规范**
> ——根域名必须有 SOA 和 NS 记录，CNAME 会与之冲突（RFC 1034 §3.6.2），
> 部分运营商的 DNS 可能无法正确解析。**建议用 `www` 等子域名绑定 OSS。**
>
> 裸域名怎么处理见下面第 6 步。

### 5. 配置 HTTPS 证书

OSS 绑定域名后默认只有 HTTP。要上 HTTPS：

1. 阿里云 → **数字证书管理服务** → 申请**免费证书**（DV 单域名，免费）
2. 签发后下载 **Nginx / Apache 格式**（拿到 `.pem` + `.key`）
3. OSS → 域名管理 → 目标域名 → **证书托管** → 上传证书
4. 之后可用 `https://www.getzeroai.xyz` 访问

> 免费证书有效期 3 个月，**到期需重新签发并替换**——建议在日历上设个提醒。
> 嫌麻烦也可以在 OSS 域名管理里直接选「阿里云 SSL 证书」自动关联。

### 6. 让裸域名也能访问

`getzeroai.xyz` 不能用 CNAME，两种做法：

- **做法 A（推荐）**：在阿里云云解析给 `@` 加一条 **显性 URL 转发** → `https://www.getzeroai.xyz`
  （需要域名已备案才能用；没备案的话用做法 B）
- **做法 B**：直接把 `@` 也绑定到 OSS（阿里云控制台通常允许），
  或让访客统一走 `www.getzeroai.xyz`

> 如果懒得折腾，初期只发布 `www.getzeroai.xyz` 给学生也完全可以。

### 7. 更新站点内容

每次改完内容，重新上传覆盖即可，**不需要重启任何服务**：

```bash
cd D:/wx/springai/springai-study-guide
ossutil cp -r . oss://getzeroai-study-guide/ --update --exclude "*.md"
# 用本仓库的脚本更省事（自动设 Content-Type 与 Cache-Control）：
# python oss.py upload getzeroai-study-guide D:/wx/springai/springai-study-guide
```

> ### ⚠️ 必须给对象设置 `Cache-Control`，否则会出现「明明更新了却看不到」
>
> **OSS 默认不给对象设置 `Cache-Control`**，响应头里只有 `ETag` 和 `Last-Modified`。
> 浏览器遇到这种响应会启用**启发式缓存**，可能长时间不回源 —— 于是新版本传上去了，
> 用户却一直看到旧的。
>
> 上传时带上 `Cache-Control: no-cache`：
>
> ```bash
> ossutil cp -r . oss://getzeroai-study-guide/ --update \
>   --exclude "*.md" --meta "Cache-Control:no-cache"
> ```
>
> 配 `no-cache` 后浏览器每次都发条件请求：内容变了才重下，没变返回 **304**（开销极小）。
> 本站文件少，全站 `no-cache` 最省心；若资源变多，可改为给静态资源文件名加内容哈希。
> **但不要把 HTML 设成长缓存。**

### 8. 排查「更新了但看不到」

**用内容指纹判断，别靠肉眼**：

```bash
# 本地与线上各算 md5，用时间戳 + no-cache 请求头穿透缓存
curl -s -H "Cache-Control: no-cache" \
  -o /tmp/live.html "http://www.getzeroai.xyz/index.html?t=$(date +%s)"
md5sum /tmp/live.html
md5sum D:/wx/springai/springai-study-guide/index.html
```

判读：

| 情况 | 结论 |
|---|---|
| md5 一致，但仍看到旧内容 | **客户端/中间层缓存**，不是部署问题 → 强制刷新（`Ctrl+F5`）或清缓存 |
| md5 不一致 | 确实没传上去 → 重新执行上传，检查是否传错了 Bucket 或层级 |

> **本站有两个可访问地址**，排查时要分清看的是哪个：
> - `http://www.getzeroai.xyz` —— 正式地址（OSS），**以此为准**
> - 各平台的临时沙箱预览地址 —— 需单独重新部署才会更新
>
> 如果后续挂了 CDN，还要额外**刷新 CDN 缓存**。

---

## 四、方案 ②：Cloudflare Pages（不想用 OSS 时的备选）

**优点**：完全免费、自动 HTTPS、自动 CDN、Git 推送可自动部署。
**代价**：必须**把 NS 改到 Cloudflare**，之后阿里云云解析的记录全部失效。

### 步骤

1. **接入 Cloudflare**：`https://dash.cloudflare.com` → Add a site → `getzeroai.xyz` → Free 套餐
   → 拿到两个 NS（形如 `xxx.ns.cloudflare.com`）
2. **改 NS**：阿里云域名控制台 → `getzeroai.xyz` → 修改 DNS 服务器 → 替换为 Cloudflare 的两个 NS
   > ⚠️ **改 NS 前先确认域名已解锁且委派生效**，否则改了也不生效。
   > ⚠️ 改 NS 后**务必在 Cloudflare 里核对 MX 等记录**（Cloudflare 会尝试自动导入，但可能漏），
   > 漏了域名邮箱会收不到信。
3. **部署站点**（Git 集成不支持 Gitee，二选一）：

```bash
# 做法一：wrangler 直传（最简单，首次会提示登录）
cd D:/wx/springai/springai-study-guide
npx wrangler pages deploy . --project-name=springai-guide

# 做法二：镜像到 GitHub 后接 Git 集成，之后 push 即自动部署
git remote add github https://github.com/<你的用户名>/springai-guide.git
git push github main
# 然后在 Pages 里 Connect to Git，Build output directory 填 /springai-study-guide
```

4. **绑定域名**：Pages → Custom domains → 添加 `getzeroai.xyz` 和 `www.getzeroai.xyz`
   → Cloudflare 自动加 DNS 记录并**自动签发 HTTPS 证书**

---

## 五、将来想让国内访问更快：走备案（方案 ③）

备案的门槛不是钱，而是**你得先有一台中国大陆的服务器**：

1. 购买阿里云/腾讯云 **ECS 或轻量应用服务器**，**有效期需 ≥ 3 个月**（否则拿不到备案服务号）
2. 在云厂商**备案控制台**提交：主体信息（身份证）+ 域名 `getzeroai.xyz` + 该服务器
3. 等管局审核（一般 **1~3 周**，期间可能电话核验）
4. 备案通过后，把 OSS 换成**中国内地节点**，或用 **CDN 加速**（大陆节点）

> ⚠️ **备案通过之前**，不要把域名解析到中国大陆的服务器提供访问，否则可能被拦截。
> 期间可以先指向香港节点（本文方案 ①），**互不影响**。
>
> 个人备案的网站不得涉及经营性业务——教学站点属个人分享，通常没问题。

---

## 六、上线自检清单

DNS 生效 + 部署完成后，逐条核对：

- [ ] `nslookup -type=NS getzeroai.xyz 223.5.5.5` 能返回 NS（域名已委派）
- [ ] OSS 已开启**静态网站托管**，默认首页为 `index.html`
- [ ] Bucket 读写权限为**公共读**
- [ ] 站点文件在 Bucket **根目录**（根目录直接可见 `index.html`）
- [ ] OSS 已**绑定自定义域名**（否则 HTML 会被强制下载而不是渲染）
- [ ] `https://www.getzeroai.xyz` 能打开，且地址栏有锁
- [ ] 首页样式正常（`assets/style.css` 加载成功）
- [ ] 点侧边栏能跳到各章节（相对路径正确）
- [ ] 代码块右上角有「复制」按钮（`assets/app.js` 加载成功）
- [ ] 自测题能展开/收起
- [ ] 抽查内页，如 `https://www.getzeroai.xyz/ch05.html`
- [ ] **手机打开看一眼**（侧边栏应变汉堡菜单、宽表格可横向滚动）

批量探测所有页面（换域名即用）：

```bash
BASE="https://www.getzeroai.xyz"
for p in index.html ch01.html ch02.html ch03.html ch04.html ch05.html ch06.html \
         ch07.html ch08.html ch09.html ch10.html ch11.html appendix.html assets/style.css; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -m 10 "$BASE/$p")
  echo "$p -> $code"
done
# 期望全部 200；出现 404 多半是上传时多套了一层目录
```

---

## 七、常见问题

**Q：为什么不能直接把 OSS 默认域名发给学生？**
A：默认域名访问 HTML 会**强制下载**（OSS 为安全默认加了 `Content-Disposition: attachment`），
学生下载到的是一堆源码而不是网页。绑定自定义域名后 OSS 不再加这个头，才能正常渲染。

**Q：域名刚解锁，为什么还是打不开？**
A：注册局写 zone 文件需要时间，通常几小时，阿里云官方说法 1~2 个工作日。
这期间**可以正常做配置**（建 Bucket、传文件、绑域名），DNS 一生效站点就自动可访问。

**Q：绑定域名时提示要验证所有权？**
A：域名归属当前阿里云账号时可直接绑定、无需验证。若提示需要验证，按控制台提示
加一条 TXT 记录（`_dnsauth`）即可，验证通过后该 TXT 记录可以删掉。

**Q：换域名或换 Bucket 后链接失效？**
A：OSS 默认域名随地域变化，基于旧域名的链接会全部失效。
用自定义域名就不会有这个问题——换 Bucket 时把域名重新绑定即可。

**Q：能只用子域名吗？**
A：可以。只绑 `guide.getzeroai.xyz` 之类的子域名，主域名留着做别的用途，互不影响。

**Q：需要防盗链吗？**
A：教学站点内容公开，一般不用。若担心流量被刷，可在 OSS 配 **Referer 防盗链**白名单，
并给 Bucket 设置**流量告警**。

**Q：现在能用 Gitee Pages 吗？**
A：Gitee Pages 的开启接口**未对外开放**（实测 API 返回 405），只能网页端手动开启，
且需要账号完成实名认证。相比之下 OSS 这条路更省事、可控性也更好。
