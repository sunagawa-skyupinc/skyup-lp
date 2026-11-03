# 株式会社スカイアップ LP

採用代行/RPO の顧客向けLPと、パートナー募集LPの静的サイトです。
HTML / CSS / 最小限のJS のみで、**ビルド不要**。ファイルを置くだけで動きます。

---

## 1. ファイル構成

```
/
├── index.html          … 顧客向けLP（目的：30分無料相談の申込）
├── partners.html       … パートナー募集LP（目的：応募）
├── thanks.html         … 送信完了ページ（検索エンジンには非表示 noindex）
├── privacy.html        … 個人情報の取扱い（見出しのみ。本文は専門家確認後に記入）
├── config.js           … ★会社情報・フォームURL・GA4 ID をここで一括管理
├── assets/
│   ├── css/style.css   … 全ページ共通のスタイル（色は先頭の :root で一括管理）
│   ├── js/site.js      … ヘッダー/フッター描画、フォーム埋め込み、GA4、構造化データ
│   └── img/            … favicon・OGP画像（いずれも仮）
├── robots.txt / sitemap.xml
├── .nojekyll           … GitHub Pages 用（そのまま置いておく）
├── README.md
└── TODO.md             … 【要記入】箇所の一覧
```

### 共通部分の仕組み
- **ヘッダー・フッター**は `assets/js/site.js` が全ページに同じものを描画します。メニュー項目を変えたいときは `site.js` 冒頭の `NAV` を編集します。
- **会社情報**（社名・住所・電話・URL）は `config.js` だけを書き換えれば、フッター・個人情報ページ・送信完了ページ・構造化データ（Organization）すべてに反映されます。
- 本文中で会社情報を使いたい場合は `<span data-company="tel"></span>` のように書くと自動で差し込まれます（`name` / `tel` / `url` / `postal` / `address`）。

---

## 2. 文言の差し替え方

| 変えたいもの | 編集する場所 |
|---|---|
| 住所・電話・社名 | `config.js` の `company` |
| 各セクションの文章 | 各HTMLを直接編集（`<!-- ===== 2. 課題 ===== -->` のようにコメントで区切ってあります） |
| ページタイトル・説明文（検索結果に出る文） | 各HTMLの `<title>` と `<meta name="description">` |
| SNSでシェアされたときの表示 | 各HTMLの `og:title` / `og:description` / `og:image` |
| ブランドカラー | `assets/css/style.css` 先頭の `--color-primary` / `--color-accent` など |
| ロゴ | `site.js` の `brand-mark`（SVG）を画像タグに置き換え、`assets/img/favicon.svg` も差し替え |
| 画像差し替え枠 | `class="ph-frame"` の要素を `<img src="..." alt="内容を説明する文" width="..." height="...">` に置き換え |

注意点
- `【要記入】` の黄色マーカー（`class="todo"`）は、**公開前にすべて差し替え or 削除**してください。一覧は `TODO.md`。
- HTMLコメント（`<!-- -->`）は画面には出ませんが、**ブラウザの「ソースを表示」で誰でも読めます**。公開前に社内向けメモは削除してください。
- 文字列を編集するときは、`config.js` の `'` や `,` を消さないよう注意してください（消すと全ページのヘッダー/フッターが表示されなくなります）。

---

## 3. Microsoft Forms の埋め込み方

1. Microsoft Forms でフォームを作成（顧客向け「無料相談」用と、パートナー「応募」用の2つ）
2. 右上の「…」または「設定」→ **回答できるユーザー：「誰でも回答できます」** にする（社外の人が回答できるようにするため）
3. 「回答を収集」（または「共有」）→ **埋め込み `</>`** を選び、表示されたコードをコピー
4. コピーしたコードの `src="…"` の **中のURLだけ** を `config.js` に貼り付け

```js
forms: {
  consultation: 'https://forms.office.com/Pages/ResponsePage.aspx?id=XXXX&embed=true',
  partner:      'https://forms.office.com/Pages/ResponsePage.aspx?id=YYYY&embed=true',
  height: 1200,   // フォームが途中で切れる/余白が多い場合はここを調整
},
```

- URLが空 `''` のあいだは、フォームの位置に「フォームは準備中です」と電話番号が表示されます。
- フォーム内の質問項目にも、個人情報の取扱いへの同意欄を入れておくことを推奨します。

### 制約（事前に知っておいてほしいこと）
- **送信後に `thanks.html` へ自動で移動させることはできません**（確信度：中。Microsoft Forms は送信後の外部URLへのリダイレクト機能を持っていないと認識しています）。送信後はフォーム内の「完了メッセージ」が表示されます。完了メッセージの文面はForms側で設定してください。
  `thanks.html` は、将来リダイレクト可能なフォームに切り替えた場合や、完了メッセージ内にリンクを置く場合に使えるよう用意しています。
- **GA4で「送信完了」を計測できません**（iframe内は別サイトのため）。代わりに、CTAボタンのクリックを `cta_click` イベントとして送信しています。正確なCV数は Forms 側の回答数で確認してください。

---

## 4. Google Analytics 4

`config.js` の `analytics.ga4MeasurementId` に `G-XXXXXXXXXX` 形式のIDを入れると、全ページで計測が始まります。空のときは計測タグ自体を読み込みません。

※ 計測ツール（Cookie等）の利用については、個人情報の取扱いページでの記載内容を**専門家に確認**してください（電気通信事業法の外部送信規律への対応要否を含む）。

---

## 5. 公開手順

どちらの方法も「ビルドコマンドなし・公開ディレクトリはリポジトリ直下」です。

### ① リポジトリを Public にして GitHub Pages で公開
GitHub Pages は、無料プランでは Public リポジトリのみ利用できます。

1. GitHub のリポジトリ → **Settings → General → Danger Zone → Change visibility → Public**
   - ⚠ Public にすると、HTMLコメント・`TODO.md`・コミット履歴を含め、リポジトリの中身が誰でも見られます。社内向けメモが残っていないか確認してから切り替えてください。
2. **Settings → Pages**
   - Source：**Deploy from a branch**
   - Branch：`main` / フォルダ：`/ (root)` → Save
3. 数分後、`https://<ユーザー名>.github.io/skyup-lp/` で公開されます（パスはすべて相対指定なので、このURLでも崩れません）

### ② Private のまま Cloudflare Pages で公開
1. Cloudflare にログイン → **Workers & Pages → 作成 → Pages → Git に接続**
2. GitHub と連携し、`skyup-lp` リポジトリのみにアクセスを許可
3. ビルド設定
   - フレームワーク：**なし**
   - ビルドコマンド：**空欄**
   - ビルド出力ディレクトリ：**`/`**（空欄でも可）
   - 本番ブランチ：`main`
4. 「保存してデプロイ」→ `https://<プロジェクト名>.pages.dev` で公開されます
5. 以後、`main` に push するたびに自動で更新されます

※ Cloudflare の画面名称は変更されることがあります。見つからない場合は公式ドキュメントを参照してください。

---

## 6. 独自ドメイン（例：lp.skyupinc.com）の設定

### GitHub Pages の場合
1. **Settings → Pages → Custom domain** に `lp.skyupinc.com` を入力して Save
2. skyupinc.com の DNS を管理しているサービス（お名前.com、Cloudflare 等）で次のレコードを追加

   | 種類 | 名前 | 値 |
   |---|---|---|
   | CNAME | `lp` | `<GitHubユーザー名>.github.io` |

3. DNS反映後（数分〜最大48時間）、**Enforce HTTPS** にチェック
4. （推奨）**組織/アカウントの Settings → Pages → Verified domains** でドメイン所有を確認しておくと、ドメインの乗っ取りリスクを下げられます

### Cloudflare Pages の場合
1. Pages プロジェクト → **カスタムドメイン → カスタムドメインを設定** → `lp.skyupinc.com`
2. skyupinc.com の DNS が Cloudflare 管理なら自動で設定されます。他社管理の場合は次を追加

   | 種類 | 名前 | 値 |
   |---|---|---|
   | CNAME | `lp` | `<プロジェクト名>.pages.dev` |

3. Cloudflare 画面でステータスが「有効」になれば完了（HTTPS 証明書は自動発行）

### ドメイン確定後に必ず直すところ
`lp.skyupinc.com` 以外のURLで公開する場合は、次をすべて書き換えてください（一覧は `TODO.md`）。
- 各HTMLの `canonical` / `og:url` / `og:image`
- `config.js` の `site.url`
- `robots.txt` / `sitemap.xml`

---

## 7. 動作確認（ローカル）

```bash
python3 -m http.server 8000
```

ブラウザで `http://localhost:8000/` を開きます。
（HTMLファイルをダブルクリックで開くと、一部のアイコンが表示されない場合があります）
