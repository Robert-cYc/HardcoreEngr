/**
 * Backward-compatibility shim
 * Core logic has moved to script.js and enhancements.js
 */
if (typeof initTOC === 'function' && !document.querySelector('.article-layout')) {
  initTOC();
}
