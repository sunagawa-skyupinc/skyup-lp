#!/usr/bin/env python3
"""
コラム原稿（簡単なMarkdown）→ WordPress貼り付け用HTML（インラインstyle付き）
使い方: python3 content-ops/to_html.py 原稿.md > 出力.html
対応する書き方:
  # タイトル            → 出力しない（WordPressのタイトル欄に入れる）
  カテゴリー：...        → 出力しない（2行目）
  > リード文             → 最初の囲み（薄い青）
  ## 見出し              → 青い線付きの見出し
  !! 強調したい一文       → グレーの囲み（複数行続けて可）
  - 箇条書き              → 枠付きリスト
  **太字**               → 太字
  [文字](URL)            → リンク
  :::cta                 → 最後の相談ボックス（以降 :::end まで。中の「- 」は箇条書き、[文字](URL) の行はボタン）
"""
import re, sys, html

BLUE = '#0b649f'
P = 'margin:0 0 16px;'
H2 = f'margin:48px 0 16px;padding:4px 0 4px 14px;border-left:5px solid {BLUE};font-size:22px;line-height:1.5;color:{BLUE};'

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', rf'<strong style="color:{BLUE};">\1</strong>', t)
    t = re.sub(r'\[(.+?)\]\((https?://[^)]+)\)', lambda m: f'<a href="{m.group(2).replace("&amp;","&").replace("&","&amp;")}" style="color:{BLUE};">{m.group(1)}</a>', t)
    return t

def convert(src):
    lines = src.splitlines()
    out = ['<div style="max-width:760px;margin:0 auto;font-size:16px;line-height:1.9;color:#17202e;">']
    i = 0
    def flush_list(items, boxed=True, color=None):
        st = 'margin:0 0 24px;padding:20px 24px 20px 44px;border:1px solid #d6dee8;border-radius:8px;' if boxed else 'margin:0 0 16px;padding:0 0 0 24px;'
        if color: st += f'color:{color};'
        o = [f'<ul style="{st}">']
        for k, it in enumerate(items):
            o.append(f'<li style="margin:0 0 {0 if k==len(items)-1 else 8}px;">{inline(it)}</li>')
        o.append('</ul>')
        return o
    while i < len(lines):
        l = lines[i].rstrip()
        if not l or l.startswith('# ') or l.startswith('カテゴリー：'):
            i += 1; continue
        if l.startswith('> '):
            out.append(f'<p style="margin:0 0 32px;padding:20px 24px;background:#eaf5fc;border-left:4px solid {BLUE};border-radius:0 6px 6px 0;">{inline(l[2:])}</p>')
        elif l.startswith('## '):
            out.append(f'<h2 style="{H2}">{inline(l[3:])}</h2>')
        elif l.startswith('!! '):
            box = []
            while i < len(lines) and lines[i].startswith('!! '):
                box.append(lines[i][3:]); i += 1
            out.append('<div style="margin:24px 0;padding:20px 24px;background:#f5f7fa;border-radius:8px;">')
            for k, b in enumerate(box):
                out.append(f'<p style="margin:0 0 {0 if k==len(box)-1 else 8}px;font-weight:bold;color:{BLUE};">{inline(b)}</p>')
            out.append('</div>'); continue
        elif l.startswith('- '):
            items = []
            while i < len(lines) and lines[i].startswith('- '):
                items.append(lines[i][2:]); i += 1
            out += flush_list(items); continue
        elif l.startswith(':::cta'):
            i += 1
            body = []
            while i < len(lines) and not lines[i].startswith(':::end'):
                body.append(lines[i].rstrip()); i += 1
            out.append(f'<div style="margin:56px 0 0;padding:28px 24px;background:{BLUE};border-radius:8px;color:#ffffff;">')
            first = True; items = []; btn = False
            for b in body + ['']:
                if b.startswith('- '):
                    items.append(b[2:]); continue
                if items:
                    out += flush_list(items, boxed=False, color='#ffffff'); items = []
                if not b: continue
                m = re.fullmatch(r'\[(.+?)\]\((https?://[^)]+)\)', b)
                if m and not btn:
                    url = m.group(2).replace('&', '&amp;')
                    out.append(f'<p style="margin:0 0 12px;"><a href="{url}" style="display:inline-block;padding:14px 28px;background:#f0a81c;color:#0a2f4d;font-weight:bold;text-decoration:none;border-radius:4px;">{html.escape(m.group(1))}</a></p>')
                    btn = True
                elif m:
                    url = m.group(2).replace('&', '&amp;')
                    out.append(f'<p style="margin:0;"><a href="{url}" style="color:#ffffff;text-decoration:underline;">{html.escape(m.group(1))}</a></p>')
                elif first:
                    out.append(f'<p style="margin:0 0 12px;font-size:20px;font-weight:bold;color:#ffffff;">{inline(b)}</p>'); first = False
                else:
                    out.append(f'<p style="margin:0 0 20px;color:#ffffff;">{inline(b)}</p>')
            out.append('</div>')
        else:
            out.append(f'<p style="{P}">{inline(l)}</p>')
        i += 1
    out.append('</div>')
    return '\n'.join(out)

if __name__ == '__main__':
    print(convert(open(sys.argv[1], encoding='utf-8').read()))
