/* ===========================================================
   getzeroai 学习站 · 门户首页交互
   功能：教程卡片搜索过滤 / 无结果提示 / 快捷键
   =========================================================== */
(function () {
  'use strict';

  var input = document.getElementById('q');
  if (!input) { return; }

  var cards = Array.prototype.slice.call(document.querySelectorAll('.tut-card'));
  var groups = Array.prototype.slice.call(document.querySelectorAll('[data-group]'));
  var empty = document.getElementById('no-result');
  if (empty) { empty.style.display = 'none'; }

  function apply() {
    var v = input.value.trim().toLowerCase();
    var shown = 0;

    cards.forEach(function (c) {
      var hay = ((c.getAttribute('data-keywords') || '') + ' ' + c.textContent).toLowerCase();
      var ok = !v || hay.indexOf(v) >= 0;
      c.style.display = ok ? '' : 'none';
      if (ok) { shown += 1; }
    });

    // 分组内没有可见卡片时，整组（含标题）隐藏
    groups.forEach(function (g) {
      var list = Array.prototype.slice.call(g.querySelectorAll('.tut-card'));
      var any = list.some(function (c) { return c.style.display !== 'none'; });
      g.style.display = any ? '' : 'none';
    });

    if (empty) { empty.style.display = (v && shown === 0) ? 'block' : 'none'; }
  }

  input.addEventListener('input', apply);
  input.addEventListener('search', apply);   // 点击浏览器的清空按钮

  // 快捷键：/ 聚焦搜索，Esc 清空
  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && document.activeElement !== input) {
      e.preventDefault();
      input.focus();
    } else if (e.key === 'Escape' && document.activeElement === input) {
      input.value = '';
      apply();
      input.blur();
    }
  });
})();
