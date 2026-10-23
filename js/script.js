// ===== Search Toggle =====
const searchToggle = document.querySelector('.nav-search-toggle');
const searchOverlay = document.querySelector('.search-overlay');
const searchInput = document.querySelector('.search-overlay input');
const searchResultsEl = document.querySelector('.search-results');

function openSearch() {
  searchOverlay.classList.add('active');
  if (searchInput) {
    setTimeout(() => searchInput.focus(), 100);
  }
  document.body.style.overflow = 'hidden';
}

function closeSearch() {
  searchOverlay.classList.remove('active');
  if (searchResultsEl) {
    searchResultsEl.innerHTML = '';
  }
  document.body.style.overflow = '';
}

if (searchToggle && searchOverlay) {
  searchToggle.addEventListener('click', (e) => {
    e.preventDefault();
    openSearch();
  });
}

// Close search with Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && searchOverlay.classList.contains('active')) {
    closeSearch();
  }
});

// Close search when clicking outside or on the close text
if (searchOverlay) {
  searchOverlay.addEventListener('click', (e) => {
    if (e.target === searchOverlay) {
      closeSearch();
    }
  });
}
const searchClose = document.querySelector('.search-close');
if (searchClose) {
  searchClose.addEventListener('click', closeSearch);
}

// ===== Mobile Menu =====
const menuToggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.nav');

if (menuToggle && nav) {
  menuToggle.addEventListener('click', () => {
    const expanded = nav.classList.toggle('open');
    menuToggle.classList.toggle('active', expanded);
    menuToggle.setAttribute('aria-expanded', expanded);
    document.body.classList.toggle('nav-open', expanded);
  });
  // Close mobile menu when clicking a nav link
  nav.addEventListener('click', (e) => {
    if (e.target.tagName === 'A' && nav.classList.contains('open')) {
      nav.classList.remove('open');
      menuToggle.classList.remove('active');
      menuToggle.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('nav-open');
    }
  });
}

// ===== Dark Mode Toggle =====
const themeToggle = document.getElementById('theme-toggle');
const body = document.documentElement;

function applyTheme(theme) {
  if (theme === 'dark') {
    body.classList.add('dark-mode');
    if (themeToggle) themeToggle.textContent = '☀️';
  } else {
    body.classList.remove('dark-mode');
    if (themeToggle) themeToggle.textContent = '🌙';
  }
}

function initTheme() {
  const stored = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const initialTheme = stored || (prefersDark ? 'dark' : 'light');
  applyTheme(initialTheme);
}

function toggleTheme() {
  const isDark = body.classList.contains('dark-mode');
  const newTheme = isDark ? 'light' : 'dark';
  localStorage.setItem('theme', newTheme);
  applyTheme(newTheme);
}

if (themeToggle) {
  themeToggle.addEventListener('click', (e) => {
    e.preventDefault();
    toggleTheme();
  });
}

// ===== Static Site Search (Fuse.js) =====
let fuse = null;

async function loadSearchIndex() {
  // Try fetch first (works when served via HTTP)
  try {
    const response = await fetch('./search-index.json');
    if (response.ok) return await response.json();
  } catch (e) {
    // fetch fails on file:// protocol, fall through to XHR
  }

  // Fallback: XMLHttpRequest (works better with file:// protocol)
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', './search-index.json', true);
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4) {
        if ((xhr.status === 200 || xhr.status === 0) && xhr.responseText) {
          try {
            resolve(JSON.parse(xhr.responseText));
          } catch (e) {
            reject(new Error('Failed to parse search index'));
          }
        } else {
          reject(new Error('Failed to load search index'));
        }
      }
    };
    xhr.send();
  });
}

async function initSearch() {
  if (!window.Fuse || !searchInput) return;

  try {
    const index = await loadSearchIndex();

    fuse = new Fuse(index, {
      keys: ['title', 'excerpt', 'tags'],
      threshold: 0.35,
      includeScore: true,
      minMatchCharLength: 2,
    });

    // Debounced search
    let searchTimeout;
    searchInput.addEventListener('input', (e) => {
      clearTimeout(searchTimeout);
      const query = e.target.value.trim();
      if (query.length < 2) {
        if (searchResultsEl) searchResultsEl.innerHTML = '';
        return;
      }
      searchTimeout = setTimeout(() => {
        if (!fuse) return;
        const results = fuse.search(query);
        renderSearchResults(results);
      }, 200);
    });
  } catch (err) {
    console.warn('Search initialization failed:', err);
    if (searchResultsEl) {
      searchResultsEl.innerHTML = '<div class="search-no-results">搜尋功能未就緒，請使用 HTTP 伺服器開啟此網站</div>';
    }
  }
}

function renderSearchResults(results) {
  if (!searchResultsEl) return;

  if (results.length === 0) {
    searchResultsEl.innerHTML = '<div class="search-no-results">找不到相關文章</div>';
    return;
  }

  const html = results.slice(0, 6).map(r => {
    const item = r.item;
    const heroImage = {"ai-algorithms.html": "ai-algorithms-guide.jpg", "ai-automation-tools-guide.html": "workflow-automation-guide.jpg", "ai-models.html": "frontier-llms-guide.jpg", "antigravity-2-vs-ide-vs-cli-vs-sdk.html": "antigravity-2-vs-ide-vs-cli-vs-sdk-guide.jpg", "antigravity-desktop-vs-ide-vs-agy.html": "antigravity-desktop-vs-ide-vs-agy-guide.jpg", "anythingllm-guide.html": "anythingllm-guide.jpg", "apache-vs-tomcat.html": "apache-tomcat-guide.jpg", "api-architecture-guide.html": "api-architecture-guide.jpg", "apple-services-ecosystem.html": "apple-ecosystem.jpg", "bluetooth-technology-guide.html": "bluetooth-technology-guide.jpg", "btop-monitor-guide.html": "btop-monitor-guide.jpg", "canva-tutorial.html": "canva-design-guide.jpg", "chip-wars-intel-amd-nvidia-asic.html": "chip-wars-guide.jpg", "claude-code-commands.html": "claude-code-guide.jpg", "claude-code-hooks-guide.html": "claude-code-guide.jpg", "claude-code-mcp-skill-guide.html": "claude-code-guide.jpg", "claude-model-families.html": "claude-model-guide.jpg", "claude-skill-mcp-plugin-deep.html": "claude-code-guide.jpg", "cloudflare-guide.html": "cloudflare-network-guide.jpg", "deepseek-ai-guide.html": "deepseek-ai-guide.jpg", "docker-compose-guide.html": "docker-guide.jpg", "docker-container-guide.html": "docker-guide.jpg", "gemini-model-guide.html": "gemini-model-guide.jpg", "git-commands.html": "git-commands-guide.jpg", "github-actions-guide.html": "github-actions.jpg", "google-antigravity-ide-guide.html": "google-antigravity-guide.jpg", "google-colab-guide.html": "google-colab-guide.jpg", "google-services-ecosystem.html": "google-ecosystem.jpg", "gpt-5-model-guide.html": "gpt5-model-guide.jpg", "grok-model-guide.html": "grok-model-guide.jpg", "hermes-agent-guide.html": "hermes-agent-guide.jpg", "hermes-desktop-vs-hermes-one.html": "hermes-agent-guide.jpg", "industrial-protocols-guide.html": "industrial-protocols-guide.jpg", "influxdb-guide.html": "influxdb-timeseries-guide.jpg", "java-nodejs-npm-guide.html": "nodejs-javascript-guide.jpg", "json-architecture-guide.html": "json-architecture-guide.jpg", "kubernetes-beginner-guide.html": "kubernetes-guide.jpg", "libre-hardware-monitor-guide.html": "libre-hardware-monitor-guide.jpg", "linux-commands.html": "linux-terminal-guide.jpg", "llama-cpp-gguf.html": "local-llm-inference-guide.jpg", "llm-naming-quantization-guide.html": "llm-quantization-guide.jpg", "lm-studio-local-llm.html": "local-llm-inference-guide.jpg", "mac-commands.html": "linux-terminal-guide.jpg", "microsoft-services-ecosystem.html": "microsoft-ecosystem.jpg", "n8n-workflow-automation.html": "workflow-automation-guide.jpg", "nas-storage-comparison.html": "nas-storage-guide.jpg", "node-js-commands.html": "nodejs-javascript-guide.jpg", "notion-guide.html": "notion-workspace-guide.jpg", "obsidian-guide.html": "obsidian-pkm-guide.jpg", "ollama-local-llm.html": "ollama-guide.jpg", "open-source-licenses.html": "open-source-licenses-guide.jpg", "openclaw-ai-assistant.html": "openclaw-agent-guide.jpg", "os-architecture-comparison.html": "os-diagram.jpg", "prompt-engineering-guide.html": "prompt-engineering-guide.jpg", "pyinstaller-python-packaging-guide.html": "pyinstaller-guide.jpg", "rag-technology-guide.html": "rag-guide.jpg", "react-introduction.html": "react-framework-guide.jpg", "rtx-spark-vs-dgx-spark-guide.html": "rtx-spark-vs-dgx-spark-guide.jpg", "slm-small-language-models-guide.html": "slm-guide.jpg", "spacex-aerospace-engineering-guide.html": "spacex-aerospace-guide.jpg", "storage-spec-performance-comparison.html": "storage-spec-performance-guide.jpg", "tesla-model-lineup-guide.html": "tesla_car_hero.jpg", "tesla-roadster-performance-thrust-rocket-guide.html": "tesla-roadster-trinity.jpg", "tmux-terminal-guide.html": "tmux-terminal-guide.jpg", "top-5-llms-2026.html": "frontier-llms-guide.jpg", "usb-history-evolution-guide.html": "usb-evolution-guide.jpg", "uv-guide.html": "python-uv-guide.jpg", "video-cable-display-interfaces-guide.html": "video-interfaces-guide.jpg", "virtual-machine-comparison.html": "virtual-machine-guide.jpg", "wireshark-network-analysis.html": "wireshark-packet-guide.jpg", "wsl-guide.html": "wsl-content.jpg", "zapier-make-n8n-comparison.html": "workflow-automation-guide.jpg"};
    let itemImg = item.image || (heroImage[item.url] ? ('./images/' + heroImage[item.url]) : './images/og-image.png');
    if (!itemImg.startsWith('./') && !itemImg.startsWith('/') && !itemImg.startsWith('http')) {
      itemImg = './' + itemImg;
    }
    return `
      <a href="${item.url}" class="search-result-item">
        <img src="${itemImg}" alt="" loading="lazy">
        <div>
          <span class="search-result-title">${item.title}</span>
          <span class="search-result-excerpt">${item.excerpt}</span>
        </div>
      </a>
    `;
  }).join('');

  searchResultsEl.innerHTML = html;
}

// Close search when navigating to a result
if (searchResultsEl) {
  searchResultsEl.addEventListener('click', (e) => {
    const link = e.target.closest('a[href]');
    if (link) {
      closeSearch();
    }
  });
}

// ===== Table of Contents & Scrollspy (article pages) =====
function initTOC() {
  const articleBody = document.querySelector('.article-body');
  if (!articleBody) return;

  const headings = articleBody.querySelectorAll('h2, h3');
  if (headings.length < 2) return; // Skip TOC for short articles without enough structure

  // Ensure each heading has a distinct ID for anchor navigation
  headings.forEach((heading, index) => {
    if (!heading.id) {
      heading.id = `toc-${index + 1}`;
    }
  });

  // Build TOC Nav Container
  const tocContainer = document.createElement('nav');
  tocContainer.className = 'toc';
  tocContainer.setAttribute('aria-label', '文章目錄導航');

  // TOC Header (Icon + Title + Chapter Count + Mobile Accordion Button)
  const tocHeader = document.createElement('div');
  tocHeader.className = 'toc-header';

  const titleWrap = document.createElement('div');
  titleWrap.className = 'toc-title-wrap';

  const iconSpan = document.createElement('span');
  iconSpan.className = 'toc-icon';
  iconSpan.textContent = '📑';

  const titleEl = document.createElement('span');
  titleEl.className = 'toc-title';
  titleEl.textContent = '文章目錄';

  const countBadge = document.createElement('span');
  countBadge.className = 'toc-count-badge';
  countBadge.textContent = `${headings.length} 個章節`;

  titleWrap.appendChild(iconSpan);
  titleWrap.appendChild(titleEl);
  titleWrap.appendChild(countBadge);

  const toggleBtn = document.createElement('button');
  toggleBtn.className = 'toc-toggle-btn';
  toggleBtn.setAttribute('aria-label', '切換目錄展開');
  toggleBtn.setAttribute('aria-expanded', 'false');

  const toggleText = document.createElement('span');
  toggleText.className = 'toc-toggle-text';
  toggleText.textContent = '展開';

  const toggleArrow = document.createElement('span');
  toggleArrow.className = 'toc-arrow';
  toggleArrow.textContent = '▾';

  toggleBtn.appendChild(toggleText);
  toggleBtn.appendChild(toggleArrow);

  tocHeader.appendChild(titleWrap);
  tocHeader.appendChild(toggleBtn);
  tocContainer.appendChild(tocHeader);

  // TOC List
  const tocList = document.createElement('ul');
  tocList.className = 'toc-list';

  headings.forEach((heading) => {
    const listItem = document.createElement('li');
    if (heading.tagName === 'H3') {
      listItem.classList.add('toc-sub');
    }

    const link = document.createElement('a');
    link.href = `#${heading.id}`;
    link.textContent = heading.textContent.trim();
    link.dataset.target = heading.id;

    listItem.appendChild(link);
    tocList.appendChild(listItem);
  });

  tocContainer.appendChild(tocList);

  // Wrap article body in modern two-column layout
  const articleParent = articleBody.parentNode;
  const nextSibling = articleBody.nextSibling;

  const wrapper = document.createElement('div');
  wrapper.className = 'article-layout';

  const mainContent = document.createElement('div');
  mainContent.className = 'article-main';

  // Move articleBody into mainContent
  mainContent.appendChild(articleBody);

  // Main content on left, TOC on right
  wrapper.appendChild(mainContent);
  wrapper.appendChild(tocContainer);

  if (nextSibling) {
    articleParent.insertBefore(wrapper, nextSibling);
  } else {
    articleParent.appendChild(wrapper);
  }

  // Mobile Collapsible State Management (< 1100px)
  function syncMobileState() {
    if (window.innerWidth < 1100) {
      if (!tocContainer.classList.contains('is-expanded')) {
        tocContainer.classList.add('is-collapsed');
        toggleText.textContent = '展開';
        toggleBtn.setAttribute('aria-expanded', 'false');
      }
    } else {
      tocContainer.classList.remove('is-collapsed');
      toggleBtn.setAttribute('aria-expanded', 'true');
    }
  }
  syncMobileState();

  toggleBtn.addEventListener('click', () => {
    const isCollapsed = tocContainer.classList.contains('is-collapsed');
    if (isCollapsed) {
      tocContainer.classList.remove('is-collapsed');
      tocContainer.classList.add('is-expanded');
      toggleText.textContent = '收合';
      toggleBtn.setAttribute('aria-expanded', 'true');
    } else {
      tocContainer.classList.add('is-collapsed');
      tocContainer.classList.remove('is-expanded');
      toggleText.textContent = '展開';
      toggleBtn.setAttribute('aria-expanded', 'false');
    }
  });

  // Smooth click interaction
  const tocLinks = tocList.querySelectorAll('a');
  tocLinks.forEach((link) => {
    link.addEventListener('click', (e) => {
      const targetId = link.dataset.target;
      const targetEl = document.getElementById(targetId);
      if (targetEl) {
        e.preventDefault();
        targetEl.scrollIntoView({ behavior: 'smooth' });
        history.pushState(null, '', `#${targetId}`);
        setActiveHeading(targetId);

        // Auto collapse on mobile after selecting section
        if (window.innerWidth < 1100) {
          tocContainer.classList.add('is-collapsed');
          tocContainer.classList.remove('is-expanded');
          toggleText.textContent = '展開';
          toggleBtn.setAttribute('aria-expanded', 'false');
        }
      }
    });
  });

  // 60fps RequestAnimationFrame Scrollspy
  const headingList = Array.from(headings);
  function setActiveHeading(activeId) {
    let matchedLink = null;
    tocLinks.forEach((link) => {
      if (link.dataset.target === activeId) {
        link.classList.add('active');
        matchedLink = link;
      } else {
        link.classList.remove('active');
      }
    });

    // Auto-scroll TOC container if link is out of view on desktop
    if (matchedLink && window.innerWidth >= 1100 && tocContainer.scrollHeight > tocContainer.clientHeight) {
      const linkTop = matchedLink.offsetTop;
      const linkHeight = matchedLink.offsetHeight;
      const tocScroll = tocContainer.scrollTop;
      const tocHeight = tocContainer.clientHeight;

      if (linkTop < tocScroll + 40 || linkTop + linkHeight > tocScroll + tocHeight - 40) {
        tocContainer.scrollTo({
          top: linkTop - (tocHeight / 2) + (linkHeight / 2),
          behavior: 'smooth'
        });
      }
    }
  }

  let ticking = false;
  function updateScrollspy() {
    const scrollY = window.scrollY;
    const viewportHeight = window.innerHeight;
    const docHeight = document.documentElement.scrollHeight;

    // Bottom of the page: activate the last heading
    if (scrollY + viewportHeight >= docHeight - 80) {
      if (headingList.length > 0) {
        setActiveHeading(headingList[headingList.length - 1].id);
      }
      ticking = false;
      return;
    }

    // Offset line: 140px below top of viewport
    const offsetLine = 140;
    let currentActiveId = null;

    for (let i = 0; i < headingList.length; i++) {
      const h = headingList[i];
      const rect = h.getBoundingClientRect();
      if (rect.top <= offsetLine) {
        currentActiveId = h.id;
      } else {
        break;
      }
    }

    if (!currentActiveId && headingList.length > 0) {
      const firstRect = headingList[0].getBoundingClientRect();
      if (firstRect.top < viewportHeight * 0.5) {
        currentActiveId = headingList[0].id;
      }
    }

    if (currentActiveId) {
      setActiveHeading(currentActiveId);
    }

    ticking = false;
  }

  function onScroll() {
    if (!ticking) {
      window.requestAnimationFrame(updateScrollspy);
      ticking = true;
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', () => {
    syncMobileState();
    onScroll();
  }, { passive: true });

  // Initial calculation
  updateScrollspy();
}

// ===== Marquee: Fetch Random Motivational Quotes =====
// Uses the free Quotable API to fetch a random quote on each page load.
// Falls back to a built-in list if the API is unavailable.
const defaultQuotes = [
  { content: "Talk is cheap. Show me the code.", author: "Linus Torvalds", translation: "閒談少說，show me the code。" },
  { content: "Stay hungry, stay foolish.", author: "Steve Jobs", translation: "保持飢餵，保持愚公。" },
  { content: "Code is like humor. You know it's good when it's clean.", author: "Cory House", translation: "程式碼就像笑話，乾淨的時候才好笑。" },
  { content: "Make it work, make it right, make it fast.", author: "Kent Beck", translation: "先讓它動；再讓它正確；最後再讓它快。" },
  { content: "Premature optimization is the root of all evil.", author: "Donald Knuth", translation: "提早最佳化是萬惡之源。" },
  { content: "Programs must be written for people to read, and only incidentally for machines to execute.", author: "Harold Abelson", translation: "程序的可讀性比機器執行更重要。" },
  { content: "The best code is no code at all.", author: "Dave Thomas", translation: "最好的程式碼就是沒有程式碼。" },
  { content: "Any fool can write code that a computer can understand. Good programmers write code that humans can understand.", author: "Martin Fowler", translation: "任何人都能寫出電腦能懂的程式，但好工程師寫的是人也能懂的程式。" },
  { content: "The best error message is the one that never happens.", author: "Thomas Fuchs", translation: "最好的錯誤提示是永遠不會發生錯誤的那一個。" },
  { content: "Debugging is like being the detective in a crime movie where the murderer is your code.", author: "Filipe Fortes", translation: "除錯就像偵探片，兇手就是你的程式碼。" },
  { content: "First, solve the problem. Then, write the code.", author: "John Johnson", translation: "先解決問題，再寫程式。" },
  { content: "Simplicity is the soul of efficiency.", author: "Austin Freeman", translation: "簡單是效率的靈魂。" },
  { content: "It works on my machine!", author: "Every developer ever", translation: "在我電腦上跑的好好的！" },
  { content: "The best way to predict the future is to invent it.", author: "Alan Kay", translation: "預測未來最好的方法就是創造它。" },
  { content: "Walking on tip-toes and ignoring the details will never help you become a better programmer.", author: "Edsger Dijkstra", translation: "忽略細節只會讓你變不成更好的工程師。" },
  { content: "Your most unhappy customers are the ones who will tell you what they want.", author: "Jeff Bezos", translation: "最不滿意的客戶會告訴你他們真正想要什麼。" },
  { content: "Done is better than perfect.", author: "Sheryl Sandberg", translation: "完成比完美更重要。" },
  { content: "If you can't explain it simply, you don't understand it well enough.", author: "Albert Einstein", translation: "如果解釋不簡單，那你還不夠懂。" },
  { content: "I have not failed. I've just found 10,000 ways that won't work.", author: "Thomas Edison", translation: "我沒有失敗，只是發現了 10000 種不行的方法。" },
  { content: "The only way to learn a programming language is by writing code.", author: "Bjarne Stroustrup", translation: "學會一門語言唯一的方法是寫出程式碼來。" },
  { content: "Programs are meant to be read more than written.", author: "Mark Zuckerberg", translation: "程式碼被閱讀的次數遠多於被撰寫。" },
  { content: "Any sufficiently advanced technology is indistinguishable from magic.", author: "Arthur C. Clarke", translation: "任何足夠先進的技術都與魔法無法區分。" },
  { content: "Code every day. Keep it simple. Build for tomorrow.", author: "John Resig", translation: "天天寫程式，保持簡單，為明天設計。" },
  { content: "Premature pessimization is the root of mediocre performance.", author: "Rob Pike", translation: "提早悲觀是普通效能的根源。" },
  { content: "If the code doesn't work, change something.", author: "Unknown", translation: "如果程式碼不動，改點什麼。" },
  { content: "A program is like a spell - cast it carefully.", author: "Unknown", translation: "程式就像咒語，小心施法。" },
  { content: "There is no spoon.", author: "The Matrix", translation: "沒有湯匙。" },
  { content: "May the Force be with you.", author: "Star Wars", translation: "願力量與你同在。" },
  { content: "I'll be back.", author: "The Terminator", translation: "我會回來。" },
  { content: "Houston, we have a problem.", author: "Apollo 13", translation: "休斯頓，我們遇到了問題。" },
  { content: "Why so serious?", author: "The Dark Knight", translation: "怎麼這麼認真？" },
  { content: "I see dead people.", author: "The Sixth Sense", translation: "我看到死人了。" },
  { content: "Life is like a box of chocolates.", author: "Forrest Gump", translation: "人生就像盒巧克力。" },
  { content: "Why did it have to be snakes?", author: "Indiana Jones", translation: "為什麼偏是眼鏡蛇？" },
  { content: "I feel the need... the need for speed!", author: "Top Gun", translation: "我感覺到需要速度！" },
  { content: "It's alive! It's alive!", author: "Frankenstein", translation: "它活了！它活了！" },
  { content: "Elementary, my dear Watson.", author: "Sherlock Holmes", translation: "基本法，華生。" },
  { content: "There's no place like home.", author: "The Wizard of Oz", translation: "沒有地方像家了。" },
  { content: "I'm gonna make him an offer he can't refuse.", author: "The Godfather", translation: "我要給他一個拒絕不了的提議。" },
  { content: "Here's looking at you, kid.", author: "Casablanca", translation: "祝你好運，孩子。" },
  { content: "Bond. James Bond.", author: "James Bond", translation: "邦德，詹姆斯邦德。" },
  { content: "Frankly, my dear, I don't give a damn.", author: "Gone with the Wind", translation: "老實說，我不在乎。" },
  { content: "Rosebud.", author: "Citizen Kane", translation: "玫瑰銀翅膀。" },
  { content: "You can't handle the truth!", author: "A Few Good Men", translation: "你受不了真相！" },
  { content: "Nobody puts Baby in a corner.", author: "Dirty Dancing", translation: "誰也把寶貝女孩放到角落。" },
  { content: "They're here!", author: "Poltergeist", translation: "他們來了！" },
  { content: "Why are you so obsessed with swans?", author: "Black Swan", translation: "為什麼那麼 obsessed 天鵝？" },
  { content: "Just keep swimming.", author: "Finding Nemo", translation: "就只好好游泳。" },
  { content: "To infinity and beyond!", author: "Toy Story", translation: "飛到極限，衝過天際！" },
  { content: "I am the king of the world!", author: "Titanic", translation: "我是世界之王！" },
  { content: "You had me at hello.", author: "Jerry Maguire", translation: "你只要說 hello，我就上鉤了。" },
  { content: "It's not the years, honey. It's the mileage.", author: "Indiana Jones", translation: "老蔡，重要的不是年龄，是里程數。" },
  { content: "They may take our lives, but they'll never take our freedom!", author: "Braveheart", translation: "他們可以奪走我們的生命，但不能奪走我們的自由！" },
  { content: "I see you.", author: "Avatar", translation: "我看到你了。" },
  { content: "Wakanda forever!", author: "Black Panther", translation: "瓦坎達 forever！" },
  { content: "I am inevitable.", author: "Avengers: Endgame", translation: "我是不可避免的。" },
  { content: "I'm not superstitious, but I am a little stitious.", author: "Michael Scott", translation: "我不是迷信，但我有點怕事兒。" },
  { content: "Why do I keep going to weddings? I don't know why, I don't know why.", author: "Michael Scott", translation: "為什麼我老是去參加婚禮？我不知道，真不知道。" },
  { content: "I am Beyonce, always.", author: "Michael Scott", translation: "我永遠都是碧妹絲。" },
  { content: "Bears, beets, Battlestar Galactica.", author: "Michael Scott", translation: "熊、甜菜、浩星戰記。" },
  { content: "I'm an early bird and a night owl, so I'm wise and I'm tired.", author: "Michael Scott", translation: "我早睡晚上的，所以很聰明也很累。" },
  { content: "Would I rather be feared or loved? Easy: both.", author: "Michael Scott", translation: "難題：寧可被害怕還是被愛？簡單：兩者皆取。" },
];

async function fetchQuote() {
  try {
    const res = await fetch('https://api.quotable.io/random', { cache: 'no-store' });
    if (!res.ok) throw new Error('API error');
    const data = await res.json();
    return { content: data.content, author: data.author };
  } catch (err) {
    console.warn('Quote API failed, using fallback:', err);
    return defaultQuotes[Math.floor(Math.random() * defaultQuotes.length)];
  }
}

function renderQuote(container, quote) {
  container.style.opacity = '0';
  setTimeout(() => {
    if (quote.translation) {
      container.textContent = `❝ ${quote.content} ❞ — ${quote.author}  |  ❝ ${quote.translation} ❞`;
    } else {
      container.textContent = `❝ ${quote.content} ❞ —  ${quote.author}`;
    }
    // Restart scroll animation so the new motto enters from the right
    container.style.animation = 'none';
    container.offsetHeight; // trigger reflow
    container.style.animation = '';
    container.style.opacity = '1';
  }, 400);
}

async function initMarquee() {
  const container = document.querySelector('.marquee-content');
  if (!container) return;

  // Show initial motto
  const quote = await fetchQuote();
  renderQuote(container, quote);

  // Rotate to the next motto every 25s (matching animation duration)
  setInterval(async () => {
    const nextQuote = await fetchQuote();
    renderQuote(container, nextQuote);
  }, 25000);
}

// ===== Init =====
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initSearch();
  initTOC();
  initMarquee();
});
