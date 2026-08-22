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

// Close search when clicking outside
if (searchOverlay) {
  searchOverlay.addEventListener('click', (e) => {
    if (e.target === searchOverlay) {
      closeSearch();
    }
  });
}

// ===== Mobile Menu (future-ready) =====
const menuToggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.nav');

if (menuToggle && nav) {
  menuToggle.addEventListener('click', () => {
    nav.classList.toggle('open');
  });
}

// ===== Dark Mode Toggle =====
const themeToggle = document.getElementById('theme-toggle');
const body = document.body;

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

async function initSearch() {
  if (!window.Fuse || !searchInput) return;

  try {
    const response = await fetch('./search-index.json');
    const index = await response.json();

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
        const results = fuse.search(query);
        renderSearchResults(results);
      }, 200);
    });
  } catch (err) {
    console.warn('Search index not found:', err);
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
    const seed = encodeURIComponent(item.title.substring(0, 20).replace(/\s+/g, ''));
    return `
      <a href="${item.url}" class="search-result-item">
        <img src="https://picsum.photos/seed/${seed}/50/32" alt="" loading="lazy">
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
  { content: "Talk is cheap. Show me the code.", author: "Linus Torvalds" },
  { content: "Stay hungry, stay foolish.", author: "Steve Jobs" },
  { content: "Code is like humor. You know it's good when it's clean.", author: "Cory House" },
  { content: "First, solve the problem. Then, write the code.", author: "John Johnson" },
  { content: "Simplicity is the soul of efficiency.", author: "Austin Freeman" },
  { content: "The best error message is the one that never happens.", author: "Thomas Fuchs" },
  { content: "Premature optimization is the root of all evil.", author: "Donald Knuth" },
  { content: "Make it work, make it right, make it fast.", author: "Kent Beck" },
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

async function initMarquee() {
  const container = document.querySelector('.marquee-content');
  if (!container) return;

  const quote = await fetchQuote();
  container.textContent = `❝ ${quote.content} ❞ —  ${quote.author}`;
}

// ===== Init =====
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initSearch();
  initTOC();
  initMarquee();
});
