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
    const heroImage = {"gpt-5-model-guide.html": "picsum-gpt5-1200-400.jpg", "grok-model-guide.html": "picsum-grok-1200-400.jpg", "gemini-model-guide.html": "picsum-gemini-models-1200-400.jpg", "claude-model-families.html": "picsum-claude-models-1200-400.jpg", "kubernetes-beginner-guide.html": "picsum-kubernetes-1200-400.jpg", "zapier-make-n8n-comparison.html": "picsum-zapier-comparison-1200-400.jpg", "hermes-agent-guide.html": "picsum-hermes-1200-400.jpg", "openclaw-ai-assistant.html": "picsum-openclaw-1200-400.jpg", "wireshark-network-analysis.html": "picsum-wireshark-1200-400.jpg", "node-js-commands.html": "picsum-nodejs-1200-400.jpg", "linux-commands.html": "picsum-linux-1200-400.jpg", "mac-commands.html": "picsum-macmini-1200-400.jpg", "claude-code-commands.html": "picsum-claude-code-1200-400.jpg", "lm-studio-local-llm.html": "picsum-lmstudio-1200-400.jpg", "ollama-local-llm.html": "picsum-ollama-1200-400.jpg", "llama-cpp-gguf.html": "picsum-llamacpp-1200-400.jpg", "n8n-workflow-automation.html": "picsum-n8n-1200-400.jpg", "docker-container-guide.html": "picsum-docker-1200-400.jpg", "ai-models.html": "picsum-aimodels-1200-400.jpg", "deepseek-ai-guide.html": "picsum-deepseek-1200-400.jpg", "btop-monitor-guide.html": "picsum-btop-1200-400.jpg", "obsidian-guide.html": "picsum-obsidian-1200-400.jpg", "notion-guide.html": "picsum-notion-1200-400.jpg", "index.html": "og-image.png", "about.html": "picsum-megan-ai-150-150.jpg", "articles.html": "og-image.png", "claude-code-mcp-skill-guide.html": "picsum-mcp-skill-1200-400.jpg"}[item.url] || 'images/og-image.png';
    return `
      <a href="${item.url}" class="search-result-item">
        <img src="images/${heroImage}" alt="" loading="lazy">
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

// ===== Table of Contents (article pages) =====
function initTOC() {
  const articleBody = document.querySelector('.article-body');
  if (!articleBody) return;

  const headings = articleBody.querySelectorAll('h2, h3');
  if (headings.length < 3) return; // Skip TOC for short articles

  // Ensure each heading has an ID for anchor links
  headings.forEach((heading, index) => {
    if (!heading.id) {
      heading.id = `toc-${index}`;
    }
  });

  // Build TOC
  const tocContainer = document.createElement('nav');
  tocContainer.className = 'toc';
  tocContainer.setAttribute('aria-label', '文章目錄');

  const tocTitle = document.createElement('h4');
  tocTitle.textContent = '文章目錄';
  tocContainer.appendChild(tocTitle);

  const tocList = document.createElement('ul');
  tocList.className = 'toc-list';

  headings.forEach((heading, index) => {
    const listItem = document.createElement('li');
    if (heading.tagName === 'H3') {
      listItem.classList.add('toc-sub');
    }

    const link = document.createElement('a');
    link.href = `#${heading.id}`;
    link.textContent = heading.textContent;
    link.dataset.target = heading.id;

    listItem.appendChild(link);
    tocList.appendChild(listItem);
  });

  tocContainer.appendChild(tocList);

  // Wrap article body in a grid layout with TOC sidebar
  const articleParent = articleBody.parentNode;
  const nextSibling = articleBody.nextSibling;

  const wrapper = document.createElement('div');
  wrapper.className = 'article-layout';
  wrapper.appendChild(tocContainer);

  const mainContent = document.createElement('div');
  mainContent.className = 'article-main';

  // Move articleBody into mainContent (detaches from original parent)
  mainContent.appendChild(articleBody);
  wrapper.appendChild(mainContent);

  // Insert the layout wrapper at the original position
  if (nextSibling) {
    articleParent.insertBefore(wrapper, nextSibling);
  } else {
    articleParent.appendChild(wrapper);
  }

  // Re-select headings in the new structure for scroll highlight
  const newHeadings = wrapper.querySelectorAll('.article-main h2, .article-main h3');
  const tocLinks = wrapper.querySelectorAll('.toc-list a');

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        const id = entry.target.id;
        const link = wrapper.querySelector(`a[href="#${id}"]`);
        if (entry.isIntersecting && link) {
          tocLinks.forEach((l) => l.classList.remove('active'));
          link.classList.add('active');
        }
      });
    },
    { rootMargin: '-20% 0px -70% 0px' }
  );

  newHeadings.forEach((h) => {
    if (h.id) observer.observe(h);
  });
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
