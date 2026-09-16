# 自定义域名上线指南 · getzeroai.xyz

站点是**纯静态**（HTML/CSS/JS，无后端），绑自有域名没有任何技术门槛。
但你的域名目前有一个**必须先解决的阻塞问题**，所以请严格按顺序执行。

---

## ⚠️ 第一步（必做，否则后面全是白费）：完成实名认证

### 当前状态诊断

我查了权威注册数据（RDAP + DoH），你的域名情况如下：

| 项 | 值 |
|---|---|
| 注册状态 | ✅ 已注册 |
| 注册商 | **阿里云（万网 / HiChina）** |
| DNS 服务器 | `dns31.hichina.com` / `dns32.hichina.com`（阿里云云解析） |
| 注册时间 | **2026-09-16**（当天刚注册） |
| 到期时间 | 2027-09-16 |
| **域名状态** | 🔴 **`client hold`** ← 问题在这里 |

### `clientHold` 意味着什么

**域名被注册商暂停解析**。在这个状态下：

- 域名**完全不解析**（本地 `nslookup` 和权威 DNS 都查不到任何记录）
- 你**配置任何 A / CNAME 记录都不会生效**
- 网站、邮箱等所有应用都无法使用

### 原因：未通过实名认证

阿里云官方规则（依据《互联网域名管理办法》）：

> 未通过实名认证（含域名命名审核和注册人资料实名审核）或实名信息不准确的域名，
> 域名注册管理机构和域名注册服务机构不得为其提供服务……将陆续添加注册局暂停解析（serverhold）
> 或注册商暂停解析（clienthold）状态。
>
> **待域名完成实名认证后，方可解除**……实名认证成功后，域名将在 **1~2 个工作日**左右解锁。

**最常见的原因是用「公共模板」注册的域名**（联系人邮箱为阿里云的公共邮箱
`zyhl-admin@list.alibaba-inc.com`），这种域名一定处于未实名状态，必须过户到自己的实名模板。

### 怎么解决

1. 登录 **阿里云域名控制台** → 域名列表 → 找到 `getzeroai.xyz`
2. 点击域名右侧的 **管理**，看 **基本信息**
3. 对照下面两种情况处理：

   **情况 A：已有实名认证过的信息模板**
   - 在基本信息页点 **更改（过户）** → 选 **快速过户**
   - 勾选一个已通过实名认证的模板 → 获取验证码 → 提交

   **情况 B：还没有实名认证的模板**
   - 先去 **域名信息模板** 页创建模板，上传身份证件完成实名认证
   - 等模板审核通过后，再回到域名做 **快速过户**

4. **顺便检查邮箱验证**：基本信息里看「联系人邮箱」状态是否为「验证通过」。
   未验证也会被锁定——点「验证未通过」按提示完成即可。

5. 过户/认证完成后，**等 1~2 个工作日**，再用下面的命令确认锁已解除：

```bash
# 状态里不再出现 client hold 就说明解锁了
curl -s "https://rdap.centralnic.com/xyz/domain/getzeroai.xyz" \
  | python -c "import sys,json; print(json.load(sys.stdin).get('status'))"

# 或者直接用 nslookup 看能否查到 NS
nslookup -type=NS getzeroai.xyz
```

> 另外：新注册域名 60 天内禁止转出注册商（`clientTransferProhibited`），这是 ICANN 的标准规则，
> 属于正常现象，不影响使用。

---

## 第二步：选托管方案

`.xyz` 后缀**已获工信部批复，可以备案**，所以两条路你都能走。区别只在「要不要等备案」：

| 方案 | 需要备案 | 上线耗时 | 国内访问速度 | 成本 |
|---|---|---|---|---|
| **A. Cloudflare Pages** ⭐推荐先做 | ❌ 不需要 | 10 分钟 | 中等偏上 | 免费 |
| B. 阿里云 OSS + CDN（中国节点） | ✅ 需要 | 1~3 周 | **最快** | 约 100~300 元/年 |
| C. 阿里云 OSS（海外节点） | ❌ 不需要 | 30 分钟 | 中等 | 极低 |
| D. Vercel / Netlify | ❌ 不需要 | 10 分钟 | 一般 | 免费 |
| E. 自建 Nginx（有服务器时） | 境内需备案 | 看情况 | 取决于服务器 | 服务器费用 |

### 我的建议

**先做方案 A 把网站跑起来**，原因很实际：

- 实名认证本身就要等 1~2 个工作日，备案还要再等 1~3 周（且备案前提是**你得先有一台
  中国大陆的服务器**，阿里云要求购买 3 个月以上的 ECS 或轻量服务器才能申请备案服务号）
- 方案 A 完全不需要等，域名解锁当天就能上线
- 以后如果发现国内访问速度确实不够，再走备案迁到国内 CDN，**切换成本很低**（只是换个 DNS 记录）

---

## 方案 A：Cloudflare Pages（推荐）

### 为什么不是直接改阿里云解析

你的 DNS 目前在阿里云云解析。用 Cloudflare 需要**把 NS 改到 Cloudflare**，
之后所有解析记录都在 Cloudflare 管理（阿里云那边的记录会失效）。

> 如果你不想换 NS，可以跳过方案 A 直接用方案 C（阿里云 OSS），因为域名和 DNS 都在阿里云，
> 不用动 NS，配置更少。

### 操作步骤

**1. 把域名接入 Cloudflare**

1. 注册/登录 `https://dash.cloudflare.com`
2. 点 **Add a site** → 输入 `getzeroai.xyz` → 选 **Free** 套餐
3. Cloudflare 会给出两个 NS 地址，形如 `xxx.ns.cloudflare.com`
4. 回到**阿里云域名控制台** → 找到 `getzeroai.xyz` → **修改 DNS 服务器**
   → 改成 Cloudflare 给的那两个 → 提交
5. **等待生效**（通常几十分钟到几小时，最长 24 小时）

> ⚠️ 改 NS 之前**先确认 `clientHold` 已解除**。锁定状态下连 NS 都改不了/不生效。

**2. 部署站点到 Cloudflare Pages**

⚠️ **重要**：Cloudflare Pages 的 Git 集成**只支持 GitHub / GitLab，不支持 Gitee**。
所以有两种做法：

**做法一：直接上传（最简单，推荐）**

```bash
# 在你本地执行，首次会提示登录 Cloudflare 账号
cd D:/wx/springai/springai-study-guide
npx wrangler pages deploy . --project-name=springai-guide
```

命令执行完会给一个 `xxx.pages.dev` 的临时地址，先验证能访问。

**做法二：把 Gitee 仓库镜像到 GitHub，再接 Git 集成**

好处是以后 `git push` 就能自动重新部署：

```bash
# 在 GitHub 建一个空仓库后
git remote add github https://github.com/<你的用户名>/springai-guide.git
git push github main
```

然后在 Cloudflare Pages 里选 **Connect to Git** → 选该仓库 →
构建配置全部留空（纯静态无构建步骤）→ **Build output directory 填 `/springai-study-guide`**。

**3. 绑定自定义域名**

1. Pages 项目 → **Custom domains** → **Set up a custom domain**
2. 输入 `getzeroai.xyz`（建议同时添加 `www.getzeroai.xyz`）
3. Cloudflare 会自动创建 DNS 记录并**自动签发 HTTPS 证书**（无需手动配置）
4. 等几分钟，访问 `https://getzeroai.xyz` 即可

---

## 方案 C：阿里云 OSS + 自定义域名（不换 NS）

适合你不想动 DNS 的情况。

```bash
# 1. 创建 Bucket，注意两点：
#    地域：如果不用备案，选海外（如新加坡）；想国内快就选大陆（需备案）
#    读写权限：公共读

# 2. 开启静态网站托管
#    Bucket → 数据管理 → 静态页面 → 默认首页填 index.html，子页面 404 也填 index.html

# 3. 上传站点（控制台拖拽，或用 ossutil）
cd D:/wx/springai/springai-study-guide
ossutil cp -r . oss://<你的bucket名>/ --update

# 4. 绑定自定义域名
#    Bucket → 传输管理 → 域名管理 → 绑定域名 → getzeroai.xyz
#    然后在阿里云云解析里添加 CNAME 记录指向 OSS 的外网访问域名
```

| 选项 | 是否需要备案 | 说明 |
|---|---|---|
| 大陆节点（如杭州） | ✅ 需要 | 速度最快，但**必须先备案**，否则绑定自定义域名时会被拦 |
| 海外节点（新加坡等） | ❌ 不需要 | 直接绑定即可，国内访问速度中等 |

### 如果要走备案（方案 B）

备案的核心门槛不是钱，而是**你得先有一台中国大陆的服务器**：

1. 购买阿里云/腾讯云的 **ECS 或轻量应用服务器**，**时长需 3 个月以上**
   （阿里云备案要求服务器有效期≥3个月，且需有备案服务号）
2. 在云厂商的 **备案控制台** 提交备案：主体信息（个人身份证）+ 域名（`getzeroai.xyz`）+ 服务器
3. 等待管局审核（一般 1~3 周，期间可能会电话核验）
4. 备案通过后，才能把域名解析到大陆节点的 OSS/CDN

> **备案期间注意事项**：在备案通过**之前**，不要把域名解析到中国大陆的服务器上提供访问，
> 否则可能被拦截。可以先解析到海外节点或保持不解析。
>
> 个人备案的网站内容不能涉及经营性业务——教学站点属于个人分享，通常没问题。

---

## 最终自检清单

域名解锁并部署完成后，逐条核对：

- [ ] `nslookup -type=NS getzeroai.xyz` 能返回 NS 记录（说明域名已解锁并委派成功）
- [ ] `https://getzeroai.xyz` 能打开，且是 **HTTPS**（地址栏有锁）
- [ ] 首页样式正常（说明 `assets/style.css` 加载成功）
- [ ] 点侧边栏能跳转到各章节（说明相对路径正确）
- [ ] 代码块右上角有「复制」按钮（说明 `assets/app.js` 加载成功）
- [ ] 自测题能展开/收起答案
- [ ] **手机打开看一眼**（侧边栏应变汉堡菜单）
- [ ] 抽查一个内页，如 `https://getzeroai.xyz/ch05.html`
- [ ] `http://getzeroai.xyz` 能自动跳转到 `https://`（Cloudflare 默认开启）

批量检查所有页面是否可达：

```bash
BASE="https://getzeroai.xyz"
for p in index.html ch01.html ch02.html ch03.html ch04.html ch05.html ch06.html \
         ch07.html ch08.html ch09.html ch10.html ch11.html appendix.html assets/style.css; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -m 10 "$BASE/$p")
  echo "$p -> $code"
done
# 期望全部是 200
```

---

## 常见问题

**Q：改完 NS 后原阿里云解析记录会怎样？**
A：失效。所有解析必须到 Cloudflare 重新配置（Cloudflare 首次接入时会尝试自动扫描导入已有记录，
但**建议手动核对一遍**，尤其是邮箱相关的 MX 记录，漏了会导致域名邮箱收不到信）。

**Q：能只用子域名，把主域名留着做别的吗？**
A：可以。只给 `guide.getzeroai.xyz` 配 CNAME 即可，主域名不受影响。
但 Cloudflare Pages 如果把整个域名的 NS 指向 Cloudflare 会更简单。

**Q：现在能用 Gitee Pages 吗？**
A：可以，但它不支持自定义域名绑定的自动化，且需要网页端手动开启（无 API）、要实名认证。
相比之下 Cloudflare Pages 更省事。

**Q：一定要用 `www` 前缀吗？**
A：不强制。建议两个都配上：`getzeroai.xyz` 和 `www.getzeroai.xyz`，
并在 Cloudflare 里用 Redirect Rule 把其中一个 301 跳到另一个（推荐统一到不带 www 的主域名）。
