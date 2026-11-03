/*
 * 共通スクリプト（ヘッダー/フッター描画・会社情報差し込み・フォーム埋め込み・GA4・構造化データ）
 * 会社情報や各種IDは /config.js で管理します。このファイルは通常編集不要です。
 */
(function () {
  'use strict';

  var cfg = window.SITE_CONFIG || {};
  var c = cfg.company || {};
  var page = document.body.getAttribute('data-page') || '';
  var isIndex = page === 'index';

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (ch) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch];
    });
  }
  function addressLine() {
    return [c.region, c.locality, c.street].filter(Boolean).join('') + (c.building ? ' ' + c.building : '');
  }
  function telHref() {
    return 'tel:' + String(c.tel || '').replace(/[^0-9+]/g, '');
  }
  // index.html 上では "#id"、他ページからは "index.html#id"
  function lp(hash) {
    return (isIndex ? '' : 'index.html') + hash;
  }

  /* ---------- ナビゲーション定義 ---------- */
  var NAV = {
    client: [
      { href: lp('#reasons'), label: '選ばれる理由' },
      { href: lp('#results'), label: '実績' },
      { href: lp('#services'), label: 'サービス' },
      { href: lp('#pricing'), label: '料金' },
      { href: lp('#faq'), label: 'よくある質問' },
      { href: 'partners.html', label: 'パートナー募集' }
    ],
    partner: [
      { href: '#target', label: '募集内容' },
      { href: '#style', label: '働き方' },
      { href: '#merits', label: '魅力' },
      { href: '#flow', label: '応募の流れ' },
      { href: 'index.html', label: '法人のお客様へ' }
    ]
  };
  var isPartner = page === 'partners';
  var nav = isPartner ? NAV.partner : NAV.client;
  var cta = isPartner
    ? { href: '#apply', label: '応募する', short: '応募する' }
    : { href: lp('#contact'), label: '30分無料相談', short: '無料相談' };

  /* ---------- ヘッダー ---------- */
  var header = document.getElementById('site-header');
  if (header) {
    var links = nav.map(function (n) {
      return '<li><a href="' + esc(n.href) + '">' + esc(n.label) + '</a></li>';
    }).join('');
    header.innerHTML =
      '<div class="header-inner">' +
        '<a class="brand" href="index.html" aria-label="' + esc(c.name) + ' トップへ">' +
          '<img class="brand-logo" src="assets/img/logo.png" alt="" width="628" height="148">' +
          '<span class="brand-sub">' + esc(c.name) + '</span>' +
        '</a>' +
        '<nav class="gnav" id="gnav" aria-label="メインメニュー"><ul>' + links + '</ul></nav>' +
        '<a class="btn btn-accent btn-sm header-cta" href="' + esc(cta.href) + '" data-cta="header">' +
          '<span class="only-pc">' + esc(cta.label) + '</span><span class="only-sp">' + esc(cta.short) + '</span></a>' +
        '<button class="menu-btn" type="button" aria-expanded="false" aria-controls="gnav">' +
          '<span class="menu-bars" aria-hidden="true"></span><span class="sr-only">メニューを開く</span></button>' +
      '</div>';

    var btn = header.querySelector('.menu-btn');
    var label = btn.querySelector('.sr-only');
    function setOpen(open) {
      header.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      label.textContent = open ? 'メニューを閉じる' : 'メニューを開く';
    }
    btn.addEventListener('click', function () {
      setOpen(!header.classList.contains('is-open'));
    });
    header.querySelector('.gnav').addEventListener('click', function (e) {
      if (e.target.closest('a')) setOpen(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setOpen(false);
    });
  }

  /* ---------- フッター ---------- */
  var footer = document.getElementById('site-footer');
  if (footer) {
    footer.innerHTML =
      (c.url ? '<div class="container"><a class="corp-banner" href="' + esc(c.url) + '" rel="noopener" data-cta="corporate">' +
        '<img src="assets/img/corporate-banner.jpg" alt="スカイアップがエンジニア転職に革命を SUPPORT YOUR DREAM" width="1400" height="371" loading="lazy">' +
        '<span class="corp-banner-text">株式会社スカイアップ 公式サイトへ</span></a></div>' : '') +
      '<div class="container footer-inner">' +
        '<div class="footer-company">' +
          '<img class="footer-logo" src="assets/img/logo-white.png" alt="" width="628" height="148">' +
          '<p class="footer-name">' + esc(c.name) + '</p>' +
          '<address>' +
            (c.postalCode ? '〒' + esc(c.postalCode) + '<br>' : '') +
            esc([c.region, c.locality, c.street].filter(Boolean).join('')) +
            (c.building ? '<br>' + esc(c.building) : '') +
            (c.tel ? '<br>TEL <a href="' + esc(telHref()) + '">' + esc(c.tel) + '</a>' : '') +
          '</address>' +
        '</div>' +
        '<nav class="footer-nav" aria-label="フッターメニュー"><ul>' +
          '<li><a href="index.html">採用代行・RPOサービス</a></li>' +
          '<li><a href="partners.html">パートナー募集</a></li>' +
          '<li><a href="privacy.html">個人情報の取扱い</a></li>' +
        '</ul></nav>' +
      '</div>' +
      '<p class="copyright"><small>&copy; ' + new Date().getFullYear() + ' ' + esc(c.name) + '</small></p>';
  }

  /* ---------- 会社情報の差し込み（data-company="name" など） ---------- */
  var fields = {
    name: c.name,
    tel: c.tel,
    url: c.url,
    postal: c.postalCode ? '〒' + c.postalCode : '',
    address: addressLine(),
    representative: c.representative
  };
  Array.prototype.forEach.call(document.querySelectorAll('[data-company]'), function (el) {
    var key = el.getAttribute('data-company');
    if (fields[key] != null) el.textContent = fields[key];
    if (key === 'tel' && el.tagName === 'A') el.setAttribute('href', telHref());
    if (key === 'url' && el.tagName === 'A') el.setAttribute('href', c.url);
  });

  /* ---------- Microsoft Forms 埋め込み ---------- */
  var forms = cfg.forms || {};
  Array.prototype.forEach.call(document.querySelectorAll('[data-form]'), function (box) {
    var key = box.getAttribute('data-form');
    var src = String(forms[key] || '').trim();
    if (/^https:\/\//.test(src)) {
      var f = document.createElement('iframe');
      f.src = src;
      f.title = box.getAttribute('data-form-title') || 'お申し込みフォーム';
      f.loading = 'lazy';
      f.height = forms.height || 1200;
      f.setAttribute('allowfullscreen', '');
      f.className = 'form-iframe';
      box.innerHTML = '';
      box.appendChild(f);
    } else {
      box.innerHTML =
        '<div class="form-pending" role="status">' +
          '<p class="form-pending-title">フォームは準備中です</p>' +
          (c.tel ? '<p>お急ぎの方はお電話でお問い合わせください。<br>TEL <a href="' + esc(telHref()) + '">' + esc(c.tel) + '</a></p>' : '') +
        '</div>';
    }
  });

  /* ---------- 構造化データ（Organization） ---------- */
  if (c.name) {
    var ld = {
      '@context': 'https://schema.org',
      '@type': 'Organization',
      name: c.name,
      url: c.url || undefined,
      telephone: c.tel || undefined,
      address: {
        '@type': 'PostalAddress',
        postalCode: c.postalCode,
        addressRegion: c.region,
        addressLocality: c.locality,
        streetAddress: [c.street, c.building].filter(Boolean).join(' '),
        addressCountry: 'JP'
      }
    };
    if (c.nameEn) ld.alternateName = c.nameEn;
    var s = document.createElement('script');
    s.type = 'application/ld+json';
    s.text = JSON.stringify(ld);
    document.head.appendChild(s);
  }

  /* ---------- Google Analytics 4（ID設定時のみ） ---------- */
  var gaId = ((cfg.analytics || {}).ga4MeasurementId || '').trim();
  if (/^G-[A-Z0-9]+$/.test(gaId)) {
    var g = document.createElement('script');
    g.async = true;
    g.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(gaId);
    document.head.appendChild(g);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', gaId);
    // CTAクリックをイベント送信（iframe内の送信完了は計測できないため、その手前を計測）
    document.addEventListener('click', function (e) {
      var a = e.target.closest('[data-cta]');
      if (a) window.gtag('event', 'cta_click', { cta_position: a.getAttribute('data-cta'), page_type: page });
    });
  }

  /* ---------- スマホ用 追従CTA ---------- */
  var bar = document.querySelector('.sticky-cta');
  if (bar && 'IntersectionObserver' in window) {
    var hero = document.querySelector('.hero');
    var goal = document.querySelector(bar.getAttribute('data-hide-near') || '#contact');
    var state = { hero: true, goal: false };
    var update = function () {
      bar.classList.toggle('is-visible', !state.hero && !state.goal);
    };
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.target === hero) state.hero = en.isIntersecting;
        if (en.target === goal) state.goal = en.isIntersecting;
      });
      update();
    });
    if (hero) io.observe(hero);
    if (goal) io.observe(goal);
  }
})();
