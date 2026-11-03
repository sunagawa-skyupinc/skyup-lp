/**
 * サイト共通設定（ここだけ書き換えれば全ページに反映されます）
 * ------------------------------------------------------------
 * - 会社情報（住所・電話など）はヘッダー/フッター/個人情報ページ/構造化データに使われます。
 * - 値を空文字 '' にすると、その項目は表示されません（フォームは「準備中」表示になります）。
 * - 文字列は必ず ' ' で囲み、行末の , を消さないでください。
 */
window.SITE_CONFIG = {
  company: {
    name: '株式会社スカイアップ',
    nameEn: '', // 英文社名（任意）。正式表記が決まっていれば記入【要記入】
    postalCode: '103-0011',
    region: '東京都',
    locality: '中央区',
    street: '日本橋大伝馬町13-7',
    building: '日本橋大富ビル3階',
    tel: '03-6403-9286',
    url: 'https://skyupinc.com',
    representative: '砂川 洋一', // 代表者氏名
  },

  site: {
    // 公開URL（末尾スラッシュなし）。構造化データに使います。独自ドメイン設定後に書き換え。
    url: 'https://lp.skyupinc.com', // TODO: 公開URL確定後に修正【要記入】
  },

  forms: {
    // Microsoft Forms の埋め込み用URL（iframe の src の中身）。未設定 '' のときは「準備中」と表示。
    // 例: 'https://forms.office.com/Pages/ResponsePage.aspx?id=XXXXXXXX&embed=true'
    consultation: '', // TODO: 顧客向け「30分無料相談」フォームURL【要記入】
    partner: '',      // TODO: パートナー応募フォームURL【要記入】
    height: 1200,     // iframe の高さ(px)。フォームの長さに合わせて調整
  },

  analytics: {
    // Google Analytics 4 の測定ID（例: 'G-XXXXXXXXXX'）。未設定 '' のときは読み込みません。
    ga4MeasurementId: '', // TODO: GA4 測定ID【要記入】
  },
};
