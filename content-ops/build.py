#!/usr/bin/env python3
"""
コラム記事のビルドスクリプト（標準ライブラリのみ）
  content-ops/articles/*.json を読み、以下を生成・更新する
    - column-<slug>.html（記事ページ）
    - column.html（一覧ページ）
    - sitemap.xml
使い方: python3 content-ops/build.py
"""
import json, glob, os, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://lp.skyupinc.com'
AUTHOR = '砂川 洋一（株式会社スカイアップ 代表取締役）'
esc = html.escape

HEAD = '''<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}｜株式会社スカイアップ</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="{ogtype}">
  <meta property="og:locale" content="ja_JP">
  <meta property="og:site_name" content="株式会社スカイアップ">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/img/{ogimg}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#0b649f">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="assets/img/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=swap">
  <link rel="stylesheet" href="assets/css/style.css">
  <script src="config.js" defer></script>
  <script src="assets/js/site.js" defer></script>{extra_head}
</head>
<body data-page="column">
  <a class="skip-link" href="#main">本文へスキップ</a>
  <header class="site-header" id="site-header">
    <noscript><div class="header-inner"><a class="brand" href="index.html">株式会社スカイアップ</a></div></noscript>
  </header>
'''
FOOT = '''
  <footer class="site-footer" id="site-footer">
    <noscript><div class="container"><p>株式会社スカイアップ</p><p><a href="privacy.html">個人情報の取扱い</a></p></div></noscript>
  </footer>
</body>
</html>
'''

AUDIENCE = {
  'client': {'label': '企業の採用担当者向け', 'og': 'ogp.png'},
  'partner': {'label': '採用支援に関わりたい方向け', 'og': 'ogp-partners.png'},
}

def fmt_date(d):
    y, m, dd = d.split('-')
    return f'{int(y)}年{int(m)}月{int(dd)}日'

def cta(aud):
    if aud == 'partner':
        return '''<aside class="article-cta">
          <h2>採用支援パートナーを募集しています</h2>
          <p>エンジニア採用を中心とした採用代行（RPO）を、業務委託で一緒に担っていただける方を募集しています。</p>
          <div class="btns">
            <a class="btn btn-accent btn-arrow" href="partners.html#apply" data-cta="column-partner">応募フォームへ進む</a>
            <a class="btn btn-ghost" href="partners.html">募集内容を見る</a>
          </div>
        </aside>'''
    return '''<aside class="article-cta">
          <h2>まずは、30分の無料相談から</h2>
          <p>エンジニア採用の状況をお聞かせください。技術領域を踏まえて、進め方をご提案します（オンライン・無料）。</p>
          <div class="btns">
            <a class="btn btn-accent btn-arrow" href="index.html#contact" data-cta="column-client">30分無料相談を申し込む</a>
            <a class="btn btn-ghost" href="index.html">サービス内容を見る</a>
          </div>
        </aside>'''

def build():
    arts = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'content-ops/articles/*.json'))):
        a = json.load(open(f, encoding='utf-8'))
        if a.get('status') != 'published':
            continue
        arts.append(a)
    arts.sort(key=lambda a: a['date'], reverse=True)

    for a in arts:
        slug = a['slug']; url = f"{SITE}/column-{slug}.html"
        aud = AUDIENCE[a['audience']]
        ld = {
          '@context': 'https://schema.org', '@type': 'Article',
          'headline': a['title'], 'description': a['description'],
          'datePublished': a['date'], 'dateModified': a.get('updated', a['date']),
          'author': {'@type': 'Person', 'name': '砂川 洋一'},
          'publisher': {'@type': 'Organization', 'name': '株式会社スカイアップ'},
          'mainEntityOfPage': url, 'image': f"{SITE}/assets/img/{aud['og']}",
        }
        extra = '\n  <script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>'
        srcs = ''.join(f'<li><a href="{esc(s["url"])}" rel="noopener">{esc(s["title"])}</a></li>' for s in a.get('sources', []))
        tags = ''.join(f'<li class="tag">{esc(t)}</li>' for t in a.get('tags', []))
        page = HEAD.format(title=esc(a['title']), desc=esc(a['description']), url=url, ogtype='article',
                           SITE=SITE, ogimg=aud['og'], extra_head=extra)
        page += f'''
  <main id="main">
    <section class="page-hero" aria-labelledby="page-title">
      <div class="container">
        <nav class="breadcrumb" aria-label="パンくずリスト"><ol><li><a href="index.html">トップ</a></li><li><a href="column.html">コラム</a></li><li>{esc(a['title'])}</li></ol></nav>
        <p class="eyebrow">COLUMN / {esc(aud['label'])}</p>
        <h1 class="page-title" id="page-title">{esc(a['title'])}</h1>
        <p class="article-meta"><span>公開：<time datetime="{a['date']}">{fmt_date(a['date'])}</time></span><span>執筆：{esc(AUTHOR)}</span></p>
      </div>
    </section>
    <section class="section">
      <article class="container prose">
        <p class="article-lead">{a['lead']}</p>
{a['body_html']}
        {cta(a['audience'])}
        <div class="author-box"><strong>{esc(AUTHOR)}</strong>機械・電気・IT・組み込みの技術知見を持つパートナーとともに、エンジニア採用を中心とした採用代行（RPO）を行っています。</div>
        <section class="sources" aria-labelledby="src-title"><h2 id="src-title">参考資料</h2><ol>{srcs}</ol>
          <p>※記事中の数値は、各資料の公表時点のものです。</p></section>
      </article>
    </section>
  </main>
''' + FOOT
        open(os.path.join(ROOT, f'column-{slug}.html'), 'w', encoding='utf-8').write(page)

    # 一覧
    items = ''
    for a in arts:
        tags = ''.join(f'<li class="tag">{esc(t)}</li>' for t in a.get('tags', []))
        items += f'''
          <li><a class="card column-card" href="column-{a['slug']}.html">
            <span class="card-id">{fmt_date(a['date'])}｜{esc(AUDIENCE[a['audience']]['label'])}</span>
            <h2 class="card-title">{esc(a['title'])}</h2>
            <p class="card-text">{esc(a['description'])}</p>
            <ul class="tags" role="list">{tags}</ul>
          </a></li>'''
    if not items:
        items = '<li><p>記事は準備中です。</p></li>'
    page = HEAD.format(title='コラム', desc='エンジニア採用・採用代行（RPO）・採用支援の働き方について、採用市場の動きを交えて解説するコラムです。',
                       url=f'{SITE}/column.html', ogtype='website', SITE=SITE, ogimg='ogp.png', extra_head='')
    page += f'''
  <main id="main">
    <section class="page-hero" aria-labelledby="page-title">
      <div class="container">
        <p class="eyebrow">COLUMN</p>
        <h1 class="page-title" id="page-title">コラム</h1>
        <p class="article-meta">エンジニア採用と採用支援の「いま」を、現場の視点で解説します。</p>
      </div>
    </section>
    <section class="section section-alt">
      <div class="container">
        <ul class="column-list" role="list">{items}
        </ul>
      </div>
    </section>
  </main>
''' + FOOT
    open(os.path.join(ROOT, 'column.html'), 'w', encoding='utf-8').write(page)

    # sitemap
    urls = ['/', '/partners.html', '/column.html', '/privacy.html'] + [f"/column-{a['slug']}.html" for a in arts]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += ''.join(f'  <url><loc>{SITE}{u}</loc></url>\n' for u in urls) + '</urlset>\n'
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write(sm)
    print(f'built {len(arts)} article(s)')

if __name__ == '__main__':
    build()
