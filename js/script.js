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
  { content: "Make it work, make it right, make it fast.", author: "Kent Beck" },
  { content: "Premature optimization is the root of all evil.", author: "Donald Knuth" },
  { content: "Programs must be written for people to read, and only incidentally for machines to execute.", author: "Harold Abelson" },
  { content: "The best code is no code at all.", author: "Dave Thomas" },
  { content: "Any fool can write code that a computer can understand. Good programmers write code that humans can understand.", author: "Martin Fowler" },
  { content: "The best error message is the one that never happens.", author: "Thomas Fuchs" },
  { content: "Debugging is like being the detective in a crime movie where the murderer is your code.", author: "Filipe Fortes" },
  { content: "First, solve the problem. Then, write the code.", author: "John Johnson" },
  { content: "Simplicity is the soul of efficiency.", author: "Austin Freeman" },
  { content: "It works on my machine!", author: "Every developer ever" },
  { content: "The best way to predict the future is to invent it.", author: "Alan Kay" },
  { content: "Walking on tip-toes and ignoring the details will never help you become a better programmer.", author: "Edsger Dijkstra" },
  { content: "Your most unhappy customers are the ones who will tell you what they want.", author: "Jeff Bezos" },
  { content: "Done is better than perfect.", author: "Sheryl Sandberg" },
  { content: "If you can't explain it simply, you don't understand it well enough.", author: "Albert Einstein" },
  { content: "I have not failed. I've just found 10,000 ways that won't work.", author: "Thomas Edison" },
  { content: "The only way to learn a programming language is by writing code.", author: "Bjarne Stroustrup" },
  { content: "Programs are meant to be read more than written.", author: "Mark Zuckerberg" },
  { content: "Any sufficiently advanced technology is indistinguishable from magic.", author: "Arthur C. Clarke" },
  { content: "Code every day. Keep it simple. Build for tomorrow.", author: "John Resig" },
  { content: "Premature pessimization is the root of mediocre performance.", author: "Rob Pike" },
  { content: "If the code doesn't work, change something.", author: "Unknown" },
  { content: "A program is like a spell - cast it carefully.", author: "Unknown" },
  { content: "There is no spoon.", author: "The Matrix" },
  { content: "May the Force be with you.", author: "Star Wars" },
  { content: "I'll be back.", author: "The Terminator" },
  { content: "Houston, we have a problem.", author: "Apollo 13" },
  { content: "Why so serious?", author: "The Dark Knight" },
  { content: "I see dead people.", author: "The Sixth Sense" },
  { content: "Life is like a box of chocolates.", author: "Forrest Gump" },
  { content: "Why did it have to be snakes?", author: "Indiana Jones" },
  { content: "I feel the need... the need for speed!", author: "Top Gun" },
  { content: "It's alive! It's alive!", author: "Frankenstein" },
  { content: "Elementary, my dear Watson.", author: "Sherlock Holmes" },
  { content: "There's no place like home.", author: "The Wizard of Oz" },
  { content: "I'm gonna make him an offer he can't refuse.", author: "The Godfather" },
  { content: "Here's looking at you, kid.", author: "Casablanca" },
  { content: "Bond. James Bond.", author: "James Bond" },
  { content: "Frankly, my dear, I don't give a damn.", author: "Gone with the Wind" },
  { content: "Rosebud.", author: "Citizen Kane" },
  { content: "You can't handle the truth!", author: "A Few Good Men" },
  { content: "Nobody puts Baby in a corner.", author: "Dirty Dancing" },
  { content: "They're here!", author: "Poltergeist" },
  { content: "Why are you so obsessed with swans?", author: "Black Swan" },
  { content: "Just keep swimming.", author: "Finding Nemo" },
  { content: "To infinity and beyond!", author: "Toy Story" },
  { content: "I am the king of the world!", author: "Titanic" },
  { content: "You had me at hello.", author: "Jerry Maguire" },
  { content: "It's not the years, honey. It's the mileage.", author: "Indiana Jones" },
  { content: "They may take our lives, but they'll never take our freedom!", author: "Braveheart" },
  { content: "I see you.", author: "Avatar" },
  { content: "Wakanda forever!", author: "Black Panther" },
  { content: "I am inevitable.", author: "Avengers: Endgame" },
  { content: "I'm not superstitious, but I am a little stitious.", author: "Michael Scott" },
  { content: "Why do I keep going to weddings? I don't know why, I don't know why.", author: "Michael Scott" },
  { content: "I am Beyonce, always.", author: "Michael Scott" },
  { content: "Bears, beets, Battlestar Galactica.", author: "Michael Scott" },
  { content: "I'm an early bird and a night owl, so I'm wise and I'm tired.", author: "Michael Scott" },
  { content: "Would I rather be feared or loved? Easy: both.", author: "Michael Scott" },
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
