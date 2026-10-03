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
 *  7. 社群分享按鈕 + 複製連結 Toast（.article-body 頁）
 *  8. 延伸閱讀推薦（.article-body 頁，從 search-index.json 取標籤相近文章）
 *  9. 科技新知分類 + 關鍵字過濾（tech-news.html）
 * 10. 指令手冊即時過濾搜尋框（linux/mac/git/node 等 .cmd-table 頁面）
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

  /* ---------- 7. 社群分享按鈕 + 複製連結 Toast ---------- */
  function initShareButtons() {
    var articleBody = document.querySelector('.article-body');
    if (!articleBody) return;

    // 取標題
    var title = document.title || document.querySelector('h1') && document.querySelector('h1').textContent || '';
    var url = window.location.href;

    // Toast 容器
    var toast = document.createElement('div');
    toast.id = 'share-toast';
    toast.setAttribute('aria-live', 'polite');
    toast.style.cssText = [
      'position:fixed', 'bottom:5rem', 'left:50%', 'transform:translateX(-50%) translateY(20px)',
      'background:#1a1a2e', 'color:#e5e7eb', 'padding:0.6rem 1.4rem',
      'border-radius:999px', 'font-size:0.92rem', 'font-weight:600',
      'box-shadow:0 4px 20px rgba(0,0,0,0.3)', 'opacity:0',
      'transition:all 0.3s ease', 'z-index:9999', 'pointer-events:none',
      'white-space:nowrap'
    ].join(';');
    document.body.appendChild(toast);

    function showToast(msg) {
      toast.textContent = msg;
      toast.style.opacity = '1';
      toast.style.transform = 'translateX(-50%) translateY(0)';
      setTimeout(function () {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(-50%) translateY(20px)';
      }, 2200);
    }

    // Share bar
    var shareBar = document.createElement('div');
    shareBar.className = 'share-bar';
    shareBar.setAttribute('aria-label', '分享文章');
    shareBar.innerHTML = [
      '<span class="share-label">分享：</span>',
      '<a class="share-btn share-x" href="https://twitter.com/intent/tweet?text=' +
        encodeURIComponent(title) + '&url=' + encodeURIComponent(url) +
        '" target="_blank" rel="noopener" aria-label="分享到 X (Twitter)">',
      '  <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.746l7.73-8.835L1.254 2.25H8.08l4.259 5.63zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>',
      '  分享</a>',
      '<button class="share-btn share-copy" type="button" aria-label="複製文章連結">',
      '  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="14" height="14" x="8" y="8" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>',
      '  複製連結</button>'
    ].join('');

    // Style injection
    var style = document.createElement('style');
    style.textContent = [
      '.share-bar{display:flex;align-items:center;flex-wrap:wrap;gap:0.5rem;margin:2.5rem 0 1.5rem;padding:1.25rem 1.5rem;',
      'background:var(--bg-alt);border:1px solid var(--border);border-radius:10px;}',
      '.share-label{font-size:0.88rem;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.06em;margin-right:0.25rem;}',
      '.share-btn{display:inline-flex;align-items:center;gap:0.4rem;padding:0.4rem 0.9rem;border-radius:6px;',
      'font-size:0.9rem;font-weight:600;cursor:pointer;transition:all 0.18s ease;text-decoration:none;',
      'background:var(--bg);border:1.5px solid var(--border);color:var(--text);}',
      '.share-btn:hover{border-color:var(--accent);color:var(--accent);transform:translateY(-1px);}',
      '.share-x:hover{border-color:#000;color:#000;}',
      '.dark-mode .share-x:hover{border-color:#e5e7eb;color:#e5e7eb;}'
    ].join('');
    document.head.appendChild(style);

    // Copy link handler
    shareBar.querySelector('.share-copy').addEventListener('click', function () {
      copyText(url).then(function () {
        showToast('✓ 連結已複製到剪貼簿！');
      });
    });

    // Insert after article-footer or at end of article body
    var articleFooter = document.querySelector('.article-footer');
    if (articleFooter) {
      articleFooter.parentNode.insertBefore(shareBar, articleFooter);
    } else {
      articleBody.parentNode.insertBefore(shareBar, articleBody.nextSibling);
    }
  }

  /* ---------- 8. 延伸閱讀推薦 ---------- */
  function initRelatedArticles() {
    var articleBody = document.querySelector('.article-body');
    if (!articleBody) return;

    var currentUrl = window.location.pathname.split('/').pop() || 'index.html';

    // Load search index
    function loadIndex(cb) {
      try {
        fetch('./search-index.json')
          .then(function (r) { return r.ok ? r.json() : Promise.reject(); })
          .then(cb)
          .catch(function () { cb(null); });
      } catch (e) { cb(null); }
    }

    loadIndex(function (index) {
      if (!index) return;

      // Find current article
      var current = null;
      index.forEach(function (art) { if (art.url === currentUrl) current = art; });
      if (!current || !current.tags || !current.tags.length) return;

      var myTags = new Set(current.tags);

      // Score other articles by tag overlap
      var scored = index
        .filter(function (art) { return art.url !== currentUrl; })
        .map(function (art) {
          var score = (art.tags || []).filter(function (t) { return myTags.has(t); }).length;
          return { art: art, score: score };
        })
        .filter(function (x) { return x.score > 0; })
        .sort(function (a, b) { return b.score - a.score })
        .slice(0, 3);

      if (!scored.length) return;

      // Image map (same as renderSearchResults)
      var heroImageMap = {"cloudflare-guide.html":"picsum-cloudflare-guide-1200-400.jpg","prompt-engineering-guide.html":"picsum-prompt-engineering-1200-400.jpg","gpt-5-model-guide.html":"picsum-gpt5-1200-400.jpg","grok-model-guide.html":"picsum-grok-1200-400.jpg","gemini-model-guide.html":"picsum-gemini-models-1200-400.jpg","claude-model-families.html":"picsum-claude-models-1200-400.jpg","kubernetes-beginner-guide.html":"picsum-kubernetes-1200-400.jpg","zapier-make-n8n-comparison.html":"picsum-zapier-comparison-1200-400.jpg","hermes-agent-guide.html":"picsum-hermes-1200-400.jpg","openclaw-ai-assistant.html":"picsum-openclaw-1200-400.jpg","wireshark-network-analysis.html":"picsum-wireshark-1200-400.jpg","node-js-commands.html":"picsum-nodejs-1200-400.jpg","linux-commands.html":"picsum-linux-1200-400.jpg","mac-commands.html":"picsum-macmini-1200-400.jpg","claude-code-commands.html":"picsum-claude-code-1200-400.jpg","lm-studio-local-llm.html":"picsum-lmstudio-1200-400.jpg","ollama-local-llm.html":"picsum-ollama-1200-400.jpg","llama-cpp-gguf.html":"picsum-llamacpp-1200-400.jpg","n8n-workflow-automation.html":"picsum-n8n-1200-400.jpg","docker-container-guide.html":"picsum-docker-1200-400.jpg","ai-models.html":"picsum-aimodels-1200-400.jpg","deepseek-ai-guide.html":"picsum-deepseek-1200-400.jpg","btop-monitor-guide.html":"picsum-btop-1200-400.jpg","obsidian-guide.html":"picsum-obsidian-1200-400.jpg","notion-guide.html":"picsum-notion-1200-400.jpg","index.html":"og-image.png","about.html":"picsum-megan-ai-150-150.jpg","articles.html":"og-image.png","claude-code-mcp-skill-guide.html":"picsum-mcp-skill-1200-400.jpg","tmux-terminal-guide.html":"picsum-tmux-1200-400.jpg","google-antigravity-ide-guide.html":"picsum-antigravity-1200-400.jpg","claude-code-hooks-guide.html":"picsum-claude-hooks-1200-400.jpg","docker-compose-guide.html":"picsum-docker-compose-1200-400.jpg","uv-guide.html":"picsum-uv-1200-400.jpg"};

      var style = document.createElement('style');
      style.textContent = [
        '.related-articles{margin:3rem 0 2rem;padding-top:2rem;border-top:1px solid var(--border);}',
        '.related-articles h3{font-size:1.3rem;font-weight:700;margin-bottom:1.25rem;color:var(--text);}',
        '.related-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:1rem;}',
        '.related-card{display:flex;flex-direction:column;background:var(--bg-alt);border:1px solid var(--border);',
        'border-radius:10px;overflow:hidden;text-decoration:none;transition:all 0.2s ease;}',
        '.related-card:hover{border-color:var(--accent);transform:translateY(-3px);box-shadow:0 8px 24px rgba(37,99,235,0.12);}',
        '.related-card img{width:100%;aspect-ratio:16/9;object-fit:cover;}',
        '.related-card-body{padding:0.75rem 1rem 1rem;}',
        '.related-card-title{font-size:0.95rem;font-weight:600;color:var(--text);line-height:1.4;}'
      ].join('');
      document.head.appendChild(style);

      var section = document.createElement('div');
      section.className = 'related-articles';
      section.innerHTML = '<h3>📖 延伸閱讀</h3><div class="related-grid">' +
        scored.map(function (x) {
          var art = x.art;
          var img = heroImageMap[art.url] || 'og-image.png';
          return '<a href="./' + art.url + '" class="related-card">' +
            '<img src="images/' + img + '" alt="" loading="lazy">' +
            '<div class="related-card-body"><div class="related-card-title">' + (art.title || art.url) + '</div></div>' +
            '</a>';
        }).join('') + '</div>';

      var shareBar = document.querySelector('.share-bar');
      if (shareBar) {
        shareBar.parentNode.insertBefore(section, shareBar);
      } else {
        var articleFooter = document.querySelector('.article-footer');
        if (articleFooter) articleFooter.parentNode.insertBefore(section, articleFooter);
        else articleBody.parentNode.insertBefore(section, articleBody.nextSibling);
      }
    });
  }

  /* ---------- 9. 科技新知 – 分類 + 關鍵字過濾 ---------- */
  function initNewsFilter() {
    var newsContent = document.getElementById('news-content');
    if (!newsContent) return;

    // Only run on tech-news page
    var isNewsPage = window.location.pathname.indexOf('tech-news') !== -1 ||
      document.querySelector('.news-hero') !== null;
    if (!isNewsPage) return;

    // Wait until news is rendered (observe DOM changes)
    var observer = new MutationObserver(function (mutations, obs) {
      var sections = newsContent.querySelectorAll('.news-section');
      if (!sections.length) return;
      obs.disconnect();
      buildNewsFilter(sections);
    });
    observer.observe(newsContent, { childList: true, subtree: true });
  }

  function buildNewsFilter(sections) {
    var newsContent = document.getElementById('news-content');
    var heroSection = document.querySelector('.news-hero');

    // Style
    var style = document.createElement('style');
    style.textContent = [
      '.news-filter-bar{display:flex;flex-wrap:wrap;gap:0.75rem;align-items:center;',
      'margin-bottom:1.5rem;padding:1rem 0;border-bottom:1px solid var(--border);}',
      '.news-filter-tabs{display:flex;flex-wrap:wrap;gap:0.4rem;}',
      '.news-filter-tab{padding:0.3rem 0.9rem;border-radius:999px;border:1.5px solid var(--border);',
      'background:var(--bg-alt);color:var(--text-muted);font-size:0.88rem;font-weight:500;',
      'cursor:pointer;transition:all 0.18s ease;}',
      '.news-filter-tab:hover,.news-filter-tab.active{background:var(--accent);border-color:var(--accent);color:#fff;}',
      '.news-keyword-input{flex:1;min-width:160px;max-width:260px;padding:0.35rem 0.9rem;',
      'border:1.5px solid var(--border);border-radius:999px;background:var(--bg-alt);',
      'color:var(--text);font-size:0.9rem;outline:none;transition:border-color 0.18s;}',
      '.news-keyword-input:focus{border-color:var(--accent);}',
      '.news-item[data-hidden="true"]{display:none;}'
    ].join('');
    document.head.appendChild(style);

    // Collect category names
    var categories = [{ key: 'all', label: '✦ 全部' }];
    sections.forEach(function (sec) {
      var h2 = sec.querySelector('h2');
      if (h2) categories.push({ key: h2.textContent.trim(), label: h2.textContent.trim() });
    });

    // Build filter bar
    var bar = document.createElement('div');
    bar.className = 'news-filter-bar';
    bar.innerHTML = '<div class="news-filter-tabs">' +
      categories.map(function (c, i) {
        return '<button class="news-filter-tab' + (i === 0 ? ' active' : '') + '" data-cat="' + c.key + '">' + c.label + '</button>';
      }).join('') +
      '</div>' +
      '<input class="news-keyword-input" type="text" placeholder="關鍵字過濾…" aria-label="新聞關鍵字過濾">';

    if (heroSection && heroSection.parentNode) {
      heroSection.parentNode.insertBefore(bar, newsContent);
    } else {
      newsContent.parentNode.insertBefore(bar, newsContent);
    }

    var tabs = bar.querySelectorAll('.news-filter-tab');
    var input = bar.querySelector('.news-keyword-input');
    var activeCategory = 'all';
    var keyword = '';

    function applyFilter() {
      sections.forEach(function (sec) {
        var h2 = sec.querySelector('h2');
        var secName = h2 ? h2.textContent.trim() : '';
        var catMatch = activeCategory === 'all' || secName === activeCategory;
        if (!catMatch) { sec.style.display = 'none'; return; }
        sec.style.display = '';
        var items = sec.querySelectorAll('.news-item');
        items.forEach(function (item) {
          var text = item.textContent.toLowerCase();
          item.setAttribute('data-hidden', keyword && text.indexOf(keyword) === -1 ? 'true' : 'false');
        });
      });
    }

    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        tabs.forEach(function (t) { t.classList.remove('active'); });
        tab.classList.add('active');
        activeCategory = tab.getAttribute('data-cat');
        applyFilter();
      });
    });

    var kwTimer;
    input.addEventListener('input', function () {
      clearTimeout(kwTimer);
      kwTimer = setTimeout(function () {
        keyword = input.value.trim().toLowerCase();
        applyFilter();
      }, 200);
    });
  }

  /* ---------- 10. 指令手冊即時過濾 ---------- */
  function initCheatsheetFilter() {
    // Only on pages with .cmd-table
    var tables = document.querySelectorAll('.cmd-table');
    if (!tables.length) return;

    var style = document.createElement('style');
    style.textContent = [
      '.cheatsheet-filter-wrap{margin:1.5rem 0 0.75rem;}',
      '.cheatsheet-filter{width:100%;max-width:480px;padding:0.5rem 1.1rem;',
      'border:2px solid var(--border);border-radius:8px;background:var(--bg-alt);',
      'color:var(--text);font-size:1rem;outline:none;transition:border-color 0.18s ease;}',
      '.cheatsheet-filter:focus{border-color:var(--accent);}',
      '.cheatsheet-filter::placeholder{color:var(--text-muted);}',
      '.cmd-section{margin-bottom:2.5rem;}',
      'tr[data-hidden="true"]{display:none;}',
      '.no-cmd-results{display:none;padding:2rem;text-align:center;color:var(--text-muted);font-size:1.1rem;}',
      '.no-cmd-results.visible{display:block;}'
    ].join('');
    document.head.appendChild(style);

    // Build filter input (insert before first table's container or the table itself)
    var firstTable = tables[0];
    var insertTarget = firstTable.closest('section') || firstTable;

    var wrap = document.createElement('div');
    wrap.className = 'cheatsheet-filter-wrap';
    var input = document.createElement('input');
    input.type = 'search';
    input.className = 'cheatsheet-filter';
    input.placeholder = '🔍 即時搜尋指令（例如：ls、grep、docker run）';
    input.setAttribute('aria-label', '搜尋指令');
    wrap.appendChild(input);

    var noResults = document.createElement('div');
    noResults.className = 'no-cmd-results';
    noResults.textContent = '😕 找不到符合的指令';
    wrap.appendChild(noResults);

    insertTarget.parentNode.insertBefore(wrap, insertTarget);

    var timer;
    input.addEventListener('input', function () {
      clearTimeout(timer);
      timer = setTimeout(function () {
        var kw = input.value.trim().toLowerCase();
        var anyVisible = false;

        tables.forEach(function (table) {
          var rows = table.querySelectorAll('tbody tr');
          rows.forEach(function (row) {
            var text = row.textContent.toLowerCase();
            var show = !kw || text.indexOf(kw) !== -1;
            row.setAttribute('data-hidden', show ? 'false' : 'true');
            if (show) anyVisible = true;
          });
        });

        noResults.classList.toggle('visible', !!kw && !anyVisible);
      }, 150);
    });
  }

  /* ---------- 啟動 ---------- */
  function init() {
    initTerminalTyping();
    initCopyButtons();
    initHighlight();
    initReading();
    initBackToTop();
    initCardGlow();
    initShareButtons();
    initRelatedArticles();
    initNewsFilter();
    initCheatsheetFilter();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
