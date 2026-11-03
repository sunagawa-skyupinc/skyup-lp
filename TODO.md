# TODO：【要記入】・差し替えが必要な箇所の一覧

公開前にすべて対応してください。チェックが済んだら `[x]` に。
確認コマンド（残りを探す）：`grep -rn "要記入\|TODO" --include=*.html --include=*.js .`

## A. 設定（config.js）
- [ ] `forms.consultation`：顧客向け「30分無料相談」の Microsoft Forms 埋め込みURL
- [ ] `forms.partner`：パートナー応募の Microsoft Forms 埋め込みURL
- [ ] `forms.height`：フォームの長さに合わせて iframe の高さを調整
- [ ] `analytics.ga4MeasurementId`：GA4 測定ID（G-XXXXXXXXXX）
- [ ] `site.url`：公開URLの確定（仮：https://lp.skyupinc.com）
- [ ] `company.nameEn`：英文社名（任意。不要なら空のまま）

## B. URL・画像（公開URL確定後）
- [ ] 全HTMLの `canonical` / `og:url` / `og:image` のドメイン（index / partners / thanks / privacy）
- [ ] `robots.txt` / `sitemap.xml` のドメイン
- [ ] `assets/img/ogp.png`・`ogp-partners.png`：仮画像 → 本番OGP画像（1200×630）
- [ ] `assets/img/favicon.svg`・`favicon-32.png`・`apple-touch-icon.png`：仮 → ロゴ確定後に差し替え
- [ ] ヘッダーのロゴマーク（`assets/js/site.js` の `brand-mark`）：仮 → 正式ロゴ
- [ ] ブランドカラー（`assets/css/style.css` 先頭の `--color-*`）：仮 → 正式色

## C. index.html（顧客向けLP）
- [ ] 選ばれる理由 REASON 02：キャリアコンパスの概念図 → 実際の画面画像に差し替えるか判断（掲載可能な画面があれば）
- [ ] 導入の流れ STEP01：相談の実施方法（オンライン/対面）を明記するか
- [x] FAQ：一部委託／エンジニア以外／対応エリア（記入済み）
- [ ] FAQ（未決定のため非表示中。決まったら追加）
  - [ ] 無料相談の形式（オンライン／対面）
- [ ] 数字表記の統一：理由1は「約30名」、実績欄は「30名」（ご指示どおりの表記）。どちらかに揃えるか確認

## D. partners.html（パートナー募集LP）
- [ ] キャッチコピー確定（HTMLコメントに言い換え案2つあり）
- [ ] ファーストビューの画像差し替え枠（`ph-frame`）→ 画像 or 枠ごと削除
- [x] 働き方：契約形態・稼働場所・稼働量・報酬（記入済み）
- [ ] 支払条件（締め日・支払日）を決め、契約書で明示（フリーランス新法。**専門家確認推奨**）
- [ ] 魅力 02：勉強会「技術コンパスアカデミー」の参加条件・開催形式（**参加を義務づける書き方は避ける**）
- [ ] 案件の例：掲載許可が取れた案件のみ掲載（現在は非表示。partners.html 内のコメントを外すと復活）
- [ ] 契約形態に「準委任」と明記するか
- [ ] 業務委託の表現チェック（偽装請負と誤解されない表現か）→ **専門家確認推奨**

## E. thanks.html
- [ ] ご連絡までの目安（例：◯営業日以内）を書くか
- [ ] Microsoft Forms 側の「完了メッセージ」の文面（Forms の設定画面で入力）

## F. privacy.html（下書き作成済み。**公開前に専門家確認**）
- [ ] 代表者氏名
- [ ] Microsoft Forms のデータ保存先の国（安全管理措置に関係）
- [ ] 記載している安全管理措置（規程・アクセス制限など）が実態と合っているか
- [ ] 制定日（仮：2026年11月3日）

## G. 公開直前
- [ ] 画面上の黄色い【要記入】がゼロ
- [ ] HTMLコメント内の社内向けメモを削除（ソース表示で誰でも読めるため）
- [ ] スマホ実機（iPhone / Android）で表示確認
- [ ] フォームから実際にテスト送信し、Forms 側に届くことを確認
