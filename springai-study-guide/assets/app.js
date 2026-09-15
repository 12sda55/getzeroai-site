/* ===========================================================
   Spring AI 2.0 学习指南 · 交互脚本
   功能：侧边栏折叠 / 代码复制 / 目录高亮 / 章节跳转 / 阅读进度
   =========================================================== */
(function () {
  'use strict';

  /* ---------- 1. 移动端侧边栏 ---------- */
  var menuBtn = document.querySelector('.menu-btn');
  var sidebar = document.querySelector('.sidebar');
  if (menuBtn && sidebar) {
    menuBtn.addEventListener('click', function () {
      sidebar.classList.toggle('open');
    });
    document.addEventListener('click', function (e) {
      if (window.innerWidth <= 900 &&
          sidebar.classList.contains('open') &&
          !sidebar.contains(e.target) && e.target !== menuBtn) {
        sidebar.classList.remove('open');
      }
    });
  }

  /* ---------- 2. 代码块：复制按钮 + 语言标签 ---------- */
  document.querySelectorAll('pre').forEach(function (pre) {
    var btn = document.createElement('button');
    btn.className = 'copy-btn';
    btn.type = 'button';
    btn.textContent = '复制';
    btn.addEventListener('click', function () {
      var code = pre.querySelector('code');
      var text = code ? code.innerText : pre.innerText;
      var done = function () {
        btn.textContent = '已复制';
        setTimeout(function () { btn.textContent = '复制'; }, 1400);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, function () { fallback(text, done); });
      } else {
        fallback(text, done);
      }
    });
    pre.appendChild(btn);
  });

  function fallback(text, done) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); done(); } catch (e) { /* 忽略 */ }
    document.body.removeChild(ta);
  }

  /* ---------- 3. 侧边栏高亮 ---------- */
  var path = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.sb-link').forEach(function (a) {
    var href = (a.getAttribute('href') || '').split('#')[0].split('/').pop();
    if (href && (href === path || (path === '' && href === 'index.html'))) {
      a.classList.add('active');
    }
  });
  document.querySelectorAll('.topbar .tb-link').forEach(function (a) {
    var href = (a.getAttribute('href') || '').split('#')[0].split('/').pop();
    if (href && href === path) { a.classList.add('active'); }
  });

  /* ---------- 4. 章节下拉跳转 ---------- */
  var sel = document.querySelector('.tb-select');
  if (sel) {
    sel.value = path;
    sel.addEventListener('change', function () {
      if (sel.value) { location.href = sel.value; }
    });
  }

  /* ---------- 5. 正文标题锚点高亮（滚动监听） ---------- */
  var heads = Array.prototype.slice.call(document.querySelectorAll('.main h2[id], .main h3[id]'));
  var subLinks = document.querySelectorAll('.sb-sub a');
  if (heads.length && subLinks.length) {
    var linkMap = {};
    subLinks.forEach(function (a) {
      var id = (a.getAttribute('href') || '').split('#')[1];
      if (id) { linkMap[id] = a; }
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var a = linkMap[en.target.id];
        if (!a) { return; }
        if (en.isIntersecting) {
          subLinks.forEach(function (x) { x.style.fontWeight = ''; x.style.color = ''; });
          a.style.fontWeight = '700';
          a.style.color = 'var(--accent)';
        }
      });
    }, { rootMargin: '-70px 0px -75% 0px', threshold: 0 });
    heads.forEach(function (h) { io.observe(h); });
  }

  /* ---------- 6. 阅读进度条 ---------- */
  var bar = document.createElement('div');
  bar.style.cssText = 'position:fixed;top:0;left:0;height:2px;width:0;z-index:99;' +
    'background:linear-gradient(90deg,#2563eb,#0d9488);transition:width .1s linear;';
  document.body.appendChild(bar);
  window.addEventListener('scroll', function () {
    var h = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.width = (h > 0 ? (window.scrollY / h) * 100 : 0) + '%';
  }, { passive: true });

  /* ---------- 7. 自测题折叠答案 ---------- */
  document.querySelectorAll('.qa').forEach(function (item) {
    var q = item.querySelector('.qa-q');
    var a = item.querySelector('.qa-a');
    if (!q || !a) { return; }
    a.style.display = 'none';
    q.style.cursor = 'pointer';
    q.style.fontWeight = '650';
    var mark = document.createElement('span');
    mark.textContent = '  ▾ 点击查看答案';
    mark.style.cssText = 'font-size:12px;color:var(--text-mute);font-weight:400;';
    q.appendChild(mark);
    q.addEventListener('click', function () {
      var open = a.style.display !== 'none';
      a.style.display = open ? 'none' : 'block';
      mark.textContent = open ? '  ▾ 点击查看答案' : '  ▴ 收起答案';
    });
  });
})();
