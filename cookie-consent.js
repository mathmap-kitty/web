/* cookie-consent.js — mathmap cookie 管理與同意橫幅
 * 需在 <head> 最前面載入（GA4/Clarity 之前），才能阻擋追蹤。
 * 使用方式：
 *   <script src="cookie-consent.js"></script>
 * 若頁面無 GA4/Clarity，cookie 工具 API 仍可使用：
 *   Cookie.get('name')
 *   Cookie.set('name', 'value', {days: 30, path: '/'})
 *   Cookie.delete('name')
 *   Cookie.consented()
 */

(function () {
  'use strict';

  var CONSENT_KEY = 'mathmap_cookie_consent';
  var CONSENT_VALUE = 'accepted';
  var COOKIE_DAYS = 365;

  /* ---------- Cookie 工具 ---------- */
  function cookieGet(name) {
    var match = document.cookie.match(new RegExp('(?:^|; )' + encodeURIComponent(name) + '=([^;]*)'));
    return match ? decodeURIComponent(match[1]) : null;
  }

  function cookieSet(name, value, options) {
    options = options || {};
    var days = options.days != null ? options.days : COOKIE_DAYS;
    var expires = '';
    if (days) {
      var d = new Date();
      d.setTime(d.getTime() + days * 24 * 60 * 60 * 1000);
      expires = '; expires=' + d.toUTCString();
    }
    var path = options.path != null ? options.path : '/';
    var domain = options.domain ? '; domain=' + options.domain : '';
    var secure = options.secure ? '; secure' : '';
    var sameSite = '; SameSite=' + (options.sameSite || 'Lax');
    document.cookie = encodeURIComponent(name) + '=' + encodeURIComponent(value) + expires + '; path=' + path + domain + secure + sameSite;
  }

  function cookieDelete(name, options) {
    options = options || {};
    options.days = -1;
    cookieSet(name, '', options);
  }

  function hasConsented() {
    return cookieGet(CONSENT_KEY) === CONSENT_VALUE;
  }

  /* ---------- 阻擋追蹤 ---------- */
  function blockTracking() {
    /* GA4: 用 no-op 取代 gtag，GA4 script 仍會載入但不會送出任何資料 */
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
    window.dataLayer.push(['consent', 'default', {
      'ad_storage': 'denied',
      'analytics_storage': 'denied'
    }]);
    /* Clarity: 蓋掉 clarity 函數，等 consent 後再真正啟用 */
    if (!window.clarity) {
      window.clarity = function () {
        (window._clarityQueue = window._clarityQueue || []).push(arguments);
      };
    }
  }

  function enableTracking() {
    /* GA4: 發送更新後的 consent 事件 */
    if (window.gtag) {
      window.gtag('consent', 'update', {
        'ad_storage': 'granted',
        'analytics_storage': 'granted'
      });
    }
    /* Clarity replay */
    if (window._clarityQueue && window._clarityQueue.length) {
      var q = window._clarityQueue;
      window._clarityQueue = [];
      for (var i = 0; i < q.length; i++) {
        try { window.clarity.apply(null, q[i]); } catch (e) {}
      }
    }
  }

  /* ---------- 橫幅 UI ---------- */
  function injectBannerCSS() {
    if (document.getElementById('mathmap-cookie-css')) return;
    var style = document.createElement('style');
    style.id = 'mathmap-cookie-css';
    style.textContent = [
      '#mathmap-cookie-banner{',
      'position:fixed;bottom:0;left:0;right:0;z-index:9999;',
      'background:rgba(140,39,64,.97);color:#fff;',
      'font-family:"Microsoft JhengHei","PingFang TC","Noto Sans TC",system-ui,sans-serif;',
      'font-size:14px;line-height:1.65;padding:16px 20px;',
      'display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:14px;',
      'box-shadow:0 -4px 20px rgba(0,0,0,.25);animation:cb-in .35s ease',
      '}',
      '@keyframes cb-in{from{transform:translateY(100%);opacity:0}to{transform:translateY(0);opacity:1}}',
      '#mathmap-cookie-banner .cb-text{flex:1;min-width:200px;max-width:560px;font-size:13.5px;opacity:.95}',
      '#mathmap-cookie-banner .cb-text a{color:#ffd4e0;text-decoration:underline}',
      '#mathmap-cookie-banner .cb-btns{display:flex;gap:8px;flex-shrink:0}',
      '#mathmap-cookie-banner .cb-btns button{',
      'border:none;border-radius:22px;padding:8px 20px;font-size:14px;font-weight:700;',
      'cursor:pointer;font-family:inherit;transition:.15s',
      '}',
      '#mathmap-cookie-banner .cb-accept{background:#fff;color:#8c2740}',
      '#mathmap-cookie-banner .cb-accept:hover{background:#ffe6ee}',
      '#mathmap-cookie-banner .cb-decline{background:rgba(255,255,255,.18);color:#fff}',
      '#mathmap-cookie-banner .cb-decline:hover{background:rgba(255,255,255,.3)}',
      '@media(max-width:520px){',
      '#mathmap-cookie-banner{flex-direction:column;text-align:center;padding:14px 16px;gap:10px}',
      '#mathmap-cookie-banner .cb-text{max-width:100%}',
      '}'
    ].join('\n');
    document.head.appendChild(style);
  }

  function showBanner() {
    injectBannerCSS();
    var banner = document.createElement('div');
    banner.id = 'mathmap-cookie-banner';
    banner.innerHTML =
      '<div class="cb-text">' +
      '本網站使用 cookie 與瀏覽器儲存空間來記錄你的學習進度（已讀考點、複習清單、錯題），並以 Google Analytics 匿名分析使用行為以改善教材。點選「接受」即同意我們儲存這些資料。' +
      '</div>' +
      '<div class="cb-btns">' +
      '<button class="cb-accept">接受</button>' +
      '<button class="cb-decline">拒絕</button>' +
      '</div>';
    document.body.appendChild(banner);

    banner.querySelector('.cb-accept').addEventListener('click', function () {
      cookieSet(CONSENT_KEY, CONSENT_VALUE, { days: COOKIE_DAYS });
      enableTracking();
      banner.remove();
    });

    banner.querySelector('.cb-decline').addEventListener('click', function () {
      cookieSet(CONSENT_KEY, 'declined', { days: COOKIE_DAYS });
      banner.remove();
    });
  }

  /* ---------- 初始化 ---------- */
  if (hasConsented()) {
    window._mathmap_consented = true;
  } else {
    blockTracking();
  }

  function initBanner() {
    if (!cookieGet(CONSENT_KEY)) {
      showBanner();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initBanner);
  } else {
    initBanner();
  }

  /* ---------- 公開 API ---------- */
  window.Cookie = {
    get: cookieGet,
    set: cookieSet,
    delete: cookieDelete,
    consented: hasConsented
  };

})();