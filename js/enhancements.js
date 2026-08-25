/**
 * enhancements.js — 網站體驗升級
 *
 * 全部功能都有 feature detection，頁面沒有對應元素就自動跳過：
 *  1. 程式碼複製按鈕（.article-body pre）
 *  2. 語法高亮（動態載入 highlight.js，CDN 失敗則靜默略過）
 *  3. 閱讀進度條（.article-body；目錄由 script.js 的 initTOC 負責）
 *  4. 回到頂部按鈕（所有頁面）
 *  5. 文章卡片滑鼠發光（.article-card）
 *  6. 首頁終端機打字動畫（#terminal-typing，指令清單放 data-commands）
 */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 1. 程式碼複製按鈕 ---------- */
  function initCopyButtons() {
    document.querySelectorAll('.article-body pre').forEach(function (pre) {
      var code = pre.querySelector('code');
      if (!code || pre.querySelector('.copy-btn')) return;

      var btn = document.createElement('button');
      btn.className = 'copy-btn';
      btn.type = 'button';
      btn.setAttribute('aria-label', '複製程式碼');
      btn.textContent = '複製';

      btn.addEventListener('click', function () {
        copyText(code.innerText).then(function () {
          btn.textContent = '✓ 已複製';
          btn.classList.add('copied');
          setTimeout(function () {
            btn.textContent = '複製';
            btn.classList.remove('copied');
          }, 1500);
        });
      });

      // 包一層 wrapper 讓按鈕固定在右上角，不跟著程式碼横向捲動
      var wrapper = document.createElement('div');
      wrapper.className = 'code-block';
      pre.parentNode.insertBefore(wrapper, pre);
      wrapper.appendChild(pre);
      wrapper.appendChild(btn);
    });
  }

  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    // 非 secure context (如本機 file://) 的 fallback
    return new Promise(function (resolve) {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy'); } catch (e) { /* no-op */ }
      ta.remove();
      resolve();
    });
  }

  /* ---------- 2. 語法高亮 ---------- */
  function initHighlight() {
    var HLJS_CDN = 'https://cdn.jsdelivr.net/npm/@highlightjs/cdn-assets@11.9.0/highlight.min.js';

    function highlightAll() {
      if (!window.hljs) return;
      window.hljs.configure({ ignoreUnescapedHTML: true });
      document.querySelectorAll('.article-body pre code').forEach(function (block) {
        try { window.hljs.highlightElement(block); } catch (e) { /* no-op */ }
      });
    }

    if (window.hljs) { highlightAll(); return; }
    var s = document.createElement('script');
    s.src = HLJS_CDN;
    s.onload = highlightAll;
    s.onerror = function () { /* CDN 掛了就跳過高亮，其他功能不受影響 */ };
    document.head.appendChild(s);
  }

  /* ---------- 3. 閱讀進度條（目錄由 script.js 的 initTOC 提供）---------- */
  function initReading() {
    var body = document.querySelector('.article-body');
    if (!body) return;

    var bar = document.createElement('div');
    bar.className = 'reading-progress';
    bar.setAttribute('aria-hidden', 'true');
    document.body.appendChild(bar);

    function updateBar() {
      var doc = document.documentElement;
      var total = doc.scrollHeight - window.innerHeight;
      var pct = total > 0 ? Math.min(1, window.scrollY / total) : 0;
      bar.style.transform = 'scaleX(' + pct + ')';
    }

    window.addEventListener('scroll', updateBar, { passive: true });
    window.addEventListener('resize', updateBar);
    updateBar();
  }

  /* ---------- 4. 回到頂部按鈕 ---------- */
  function initBackToTop() {
    var btn = document.createElement('button');
    btn.className = 'back-to-top';
    btn.type = 'button';
    btn.setAttribute('aria-label', '回到頁首');
    btn.innerHTML =
      '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
      'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      '<path d="M12 19V5M5 12l7-7 7 7"/></svg>';

    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
    });

    document.body.appendChild(btn);

    function toggle() {
      btn.classList.toggle('visible', window.scrollY > 400);
    }
    window.addEventListener('scroll', toggle, { passive: true });
    toggle();
  }

  /* ---------- 5. 文章卡片滑鼠發光 ---------- */
  function initCardGlow() {
    if (reduceMotion) return; // 減少動態效果時不出現光暈
    document.querySelectorAll('.article-card').forEach(function (card) {
      card.addEventListener('pointermove', function (e) {
        var r = card.getBoundingClientRect();
        card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        card.style.setProperty('--my', (e.clientY - r.top) + 'px');
      });
    });
  }

  /* ---------- 6. 終端機打字動畫 ---------- */
  function initTerminalTyping() {
    var el = document.getElementById('terminal-typing');
    if (!el) return;

    var commands = el.getAttribute('data-commands');
    commands = commands
      ? commands.split('|')
      : ['claude "幫我修好這個 bug"', 'git push origin main', 'brew install btop'];

    if (reduceMotion) { // 不做動畫，直接顯示第一行
      el.textContent = commands[0];
      return;
    }

    var li = 0, ci = 0, deleting = false;

    function tick() {
      var line = commands[li];
      ci += deleting ? -1 : 1;
      el.textContent = line.slice(0, ci);

      var delay = deleting ? 28 : 65 + Math.random() * 60;
      if (!deleting && ci === line.length) {
        delay = 1900;           // 打完整行停久一點
        deleting = true;
      } else if (deleting && ci === 0) {
        deleting = false;
        li = (li + 1) % commands.length;
        delay = 480;            // 換下一行前稍停
      }
      setTimeout(tick, delay);
    }

    tick();
  }

  /* ---------- 啟動 ---------- */
  function init() {
    initTerminalTyping();
    initCopyButtons();
    initHighlight();
    initReading();
    initBackToTop();
    initCardGlow();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
