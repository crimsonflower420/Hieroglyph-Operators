/* Theme (Light / Auto / Dark) and language (JA / EN) toggles. */
(function () {
  var THEME = 'ho-theme', LANG = 'ho-lang', root = document.documentElement;
  function applyTheme() {
    var t = localStorage.getItem(THEME);
    var pref = (t === 'light' || t === 'dark') ? t : 'auto';
    var theme = pref === 'auto' ? (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light') : pref;
    root.setAttribute('data-theme', theme); root.setAttribute('data-theme-preference', pref);
    root.style.colorScheme = theme;
    document.querySelectorAll('.theme-toggle input').forEach(function (i) { i.checked = i.value === pref; });
  }
  function applyLang(l) {
    root.lang = l; root.setAttribute('data-lang', l);
    document.querySelectorAll('.lang-toggle input').forEach(function (i) { i.checked = i.value === l; });
    var t = document.querySelector('meta[name="title-' + l + '"]');
    if (t) document.title = t.content;
  }
  document.addEventListener('DOMContentLoaded', function () {
    applyTheme(); applyLang(root.getAttribute('data-lang') || 'ja');
    document.querySelectorAll('.theme-toggle input').forEach(function (i) {
      i.addEventListener('change', function () {
        if (i.value === 'auto') localStorage.removeItem(THEME); else localStorage.setItem(THEME, i.value);
        applyTheme();
      });
    });
    document.querySelectorAll('.lang-toggle input').forEach(function (i) {
      i.addEventListener('change', function () { localStorage.setItem(LANG, i.value); applyLang(i.value); });
    });
    matchMedia('(prefers-color-scheme: dark)').addEventListener('change', applyTheme);
  });
})();
/* On narrow screens the nav scrolls sideways; keep the current page in view. */
document.addEventListener('DOMContentLoaded', function () {
  var ul = document.querySelector('nav.primary ul'), cur = document.querySelector('nav.primary [aria-current]');
  if (ul && cur && ul.scrollWidth > ul.clientWidth) ul.scrollLeft = Math.max(0, cur.parentNode.offsetLeft - ul.clientWidth / 2 + cur.offsetWidth / 2);
});
