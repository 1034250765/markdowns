# -*- coding: utf-8 -*-
"""
通用 Markdown -> A4 打印级 HTML
特性：块级/行内 LaTeX -> MathML、图注成组、目录页码两遍回填、标题定位标记
用法：python md2pdf.py --src <md> --work <dir> --mode pass1|pass2 [--pagemap <json>]
"""
import os, re, sys, json, argparse, html as H, urllib.parse
from PIL import Image
import markdown
from markdown.extensions.toc import TocExtension
from latex2mathml.converter import convert as l2m

BUILD_DATE = '2026-10-14'
IMG_RE = re.compile(r'!\[([^\]]*)\]\(([^)\s]+)\)')
LINK_RE = re.compile(r'(?<!!)\[([^\]]*)\]\(([^)]+)\)')
CODE_SPAN = re.compile(r'(`+[^`]+`+)')
BOLD_RE = re.compile(r'\*\*(?!\s)(.+?)(?<!\s)\*\*')
INLINE_MATH_RE = re.compile(r'(?<!\$)\$([^$\n]{1,160})\$(?!\$)')
MATH_OK = re.compile(r"^[A-Za-z0-9\s\\{}_^,.()\[\]+\-*/=|<>:;'!~]*$")
YAML_RE = re.compile(r'^---\s*\n.*?\n---\s*\n', re.S)


# ---------------------------------------------------------------- 数学
def to_mathml(latex, display, errs):
    tex = latex.strip()
    tex = tex.replace('\\operatorname*', '\\operatorname')
    tex = re.sub(r'^\\displaystyle\s*', '', tex)
    try:
        m = l2m(tex)
    except Exception as e:
        errs.append((tex[:90], repr(e)[:90]))
        return '<code class="math-fail">%s</code>' % H.escape(tex)
    if display:
        m = m.replace('<math ', '<math display="block" ', 1)
    return m


# ---------------------------------------------------------------- 预处理
def preprocess(text, src_dir, slots, inlines, stats):
    lines = text.split('\n')
    out, in_code, in_math, math_buf, toc_done = [], False, False, [], False

    def emit_toc_slot():
        i = len(slots)
        slots.append(('TOC', None))
        out.append('<div class="rawslot" data-slot="%d"></div>' % i)

    for line in lines:
        if line.lstrip().startswith('```'):
            in_code = not in_code
            out.append(line)
            continue
        if in_code:
            out.append(line)
            continue

        if line.strip() == '$$':
            if not in_math:
                in_math, math_buf = True, []
            else:
                in_math = False
                i = len(slots)
                slots.append(('MATH', '<div class="math-display">%s</div>'
                              % to_mathml(' '.join(math_buf), True, stats['math_err'])))
                out.append('<div class="rawslot" data-slot="%d"></div>' % i)
                stats['block_math'] += 1
            continue
        if in_math:
            math_buf.append(line.strip())
            continue

        if line.strip() == '[TOC]':
            continue                                    # 目录统一重排在正文之前
        if not toc_done and re.match(r'^##\s', line):
            emit_toc_slot()
            toc_done = True

        line = re.sub(r'^(\s*)-\s\[ \]\s', lambda m: m.group(1) + '- \u2610 ', line)
        line = re.sub(r'^(\s*)-\s\[[xX]\]\s', lambda m: m.group(1) + '- \u2611 ', line)
        out.append(_inline(line, src_dir, inlines, stats))

    if not toc_done:                                     # 兜底：文档没有二级标题
        emit_toc_slot()
    return '\n'.join(out)


def _inline(line, src_dir, inlines, stats):
    parts = CODE_SPAN.split(line)                        # 奇数位是行内代码，原样保留
    res = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            res.append(part)
            continue

        def _img(m):
            alt, src = m.group(1), m.group(2)
            p = os.path.join(src_dir, src)
            if not os.path.exists(p):
                stats['missing_img'].append(src)
            return '![%s](%s)' % (alt, file_uri(p))
        part = IMG_RE.sub(_img, part)

        def _mth(m):
            tex = m.group(1)
            if not MATH_OK.match(tex):                   # 不像公式（如 $env:...）就留着
                return m.group(0)
            k = len(inlines)
            inlines.append(to_mathml(tex, False, stats['math_err']))
            stats['inline_math'] += 1
            return '@@IM%d@@' % k
        part = INLINE_MATH_RE.sub(_mth, part)

        # 中文紧邻的 **粗体** 无法按 CommonMark 侧翼规则闭合，故预转换
        part = BOLD_RE.sub(r'<strong>\1</strong>', part)

        def _link(m):
            label, url = m.group(1), m.group(2)
            if url.startswith(('http://', 'https://')):
                return ('<a href="%s">%s</a><span class="urltxt">%s</span>'
                        % (H.escape(url, True), label, url))
            return '<span class="inref">%s</span>' % label
        part = LINK_RE.sub(_link, part)
        res.append(part)
    return ''.join(res)


def file_uri(p):
    p = os.path.abspath(p).replace('\\', '/')
    return 'file:///' + urllib.parse.quote(p, safe=':/')


# ---------------------------------------------------------------- 后处理
def postprocess(body, slots, toc_html, markers, work):
    for i, (kind, content) in enumerate(slots):
        ph = '<div class="rawslot" data-slot="%d"></div>' % i
        body = body.replace(ph, content if kind == 'MATH' else toc_html)

    body = body.replace('<blockquote>', '<blockquote class="meta">', 1)

    # 导语段（元信息之后、正文之前，首个非图注段落）-> 结论条
    mb = re.search(r'</blockquote>', body)
    if mb:
        hd, tl = body[:mb.end()], body[mb.end():]
        h2 = re.search(r'<h2\b', tl)
        seg, rest = (tl[:h2.start()], tl[h2.start():]) if h2 else (tl, '')
        for m in re.finditer(r'<p>(.*?)</p>', seg, re.S):
            inner = m.group(1)
            if inner.lstrip().startswith('<em>'):
                continue
            if len(re.sub(r'<[^>]+>', '', inner).strip()) < 30:
                continue
            seg = seg[:m.start()] + '<p class="callout">' + seg[m.start() + 3:]
            break
        body = hd + seg + rest

    # 图 + 图注成组（支持连续多图共用一条图注）
    IMG_TAG = re.compile(r'<img[^>]*?/?>')
    FIG_RUN = re.compile(r'(?:<p>\s*<img[^>]*?/?>\s*</p>\s*)+(?:<p>\s*<em>(.*?)</em>\s*</p>)?', re.S)

    def fig(m):
        block, cap = m.group(0), m.group(1)
        tags = IMG_TAG.findall(block)
        res = []
        for k, tag in enumerate(tags):
            cls = ''
            s = re.search(r'src="([^"]+)"', tag)
            if s:
                p = urllib.parse.unquote(urllib.parse.urlparse(s.group(1)).path).lstrip('/')
                try:
                    w, h = Image.open(p).size
                    if abs(w - h) < w * 0.12:
                        cls = ' class="fig-illus"'
                except Exception:
                    pass
            if k == len(tags) - 1 and cap:
                res.append('<figure%s>%s<figcaption>%s</figcaption></figure>' % (cls, tag, cap))
            else:
                res.append('<figure%s>%s</figure>' % (cls, tag))
        return ''.join(res)
    body = FIG_RUN.sub(fig, body)

    # 短代码块不跨页
    body = re.sub(r'<pre>.*?</pre>',
                  lambda m: m.group(0).replace('<pre>', '<pre class="keep">', 1)
                  if m.group(0).count('\n') <= 20 else m.group(0),
                  body, flags=re.S)

    # 正文首章另起一页
    body = re.sub(r'<h2 ', '<h2 class="page-break" ', body, count=1)

    heads = []
    if markers:
        c = [0]

        def mark(m):
            tag, attrs, content = m.group(1), m.group(2), m.group(3)
            n = c[0]; c[0] += 1
            hid = re.search(r'id="([^"]*)"', attrs)
            heads.append(hid.group(1) if hid else '')
            return ('<%s%s>%s<span class="pm">LSMK%04dEND</span></%s>'
                    % (tag, attrs, content, n, tag))
        body = re.sub(r'<(h[23])\b([^>]*)>(.*?)</\1>', mark, body, flags=re.S)
        json.dump(heads, open(os.path.join(work, 'heads.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False)
    return body


def build_toc(tokens, pagemap):
    rows = []

    def walk(items):
        for it in items:
            lv = it['level']
            if lv >= 2:
                pg = str(pagemap.get(it['id'], '')) if pagemap else ''
                rows.append('<div class="toc-item lv%d"><a class="toc-t" href="#%s">%s</a>'
                            '<span class="toc-dots"></span><span class="toc-pg">%s</span></div>'
                            % (min(lv, 3), it['id'], it['name'], pg or '&nbsp;'))
            if it.get('children'):
                walk(it['children'])
    walk(tokens)
    return '<div class="toc"><div class="toc-h">目　录</div>%s</div>' % ''.join(rows), len(rows)


# ---------------------------------------------------------------- CSS
CSS = r"""
@page { size: A4; margin: 17mm 15mm 17mm 15mm; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: "Microsoft YaHei", "微软雅黑", "PingFang SC", "Hiragino Sans GB", sans-serif;
  font-size: 10.5pt; line-height: 1.78; color: #1b1b1b; margin: 0;
  text-align: justify; -webkit-font-smoothing: antialiased; }
h1.doc-title { font-size: 19pt; font-weight: 700; text-align: center; color: #1F3864;
  line-height: 1.4; margin: 2mm 0 0; letter-spacing: .3px; }
h1.doc-title::after { content: ""; display: block; width: 34mm; height: 2.6px;
  background: #1F9D96; margin: 5.5mm auto 0; }
h2 { font-size: 14pt; font-weight: 700; color: #1F3864; line-height: 1.45;
  margin: 9mm 0 3.5mm; padding: 1mm 0 1mm 3.4mm; border-left: 4.5px solid #1F9D96;
  break-after: avoid; break-inside: avoid; }
h3 { font-size: 11.6pt; font-weight: 700; color: #23425f; line-height: 1.5;
  margin: 6mm 0 2.4mm; break-after: avoid; }
h2.page-break { break-before: page; }
p { margin: 0 0 2.6mm; }
strong { color: #14283f; }
em { color: #33475b; }
a { color: #14539a; text-decoration: none; border-bottom: .6px dotted #9dc0e6; }
span.inref { color: #3d4c5c; }
span.urltxt { color: #8a8f96; font-size: 8.2pt; word-break: break-all; margin-left: .6em; }
ul, ol { margin: 2.6mm 0; padding-left: 7mm; }
li { margin: 1.1mm 0; }
hr { border: none; border-top: 1px solid #d9dee4; margin: 6mm 0; }
blockquote { margin: 4mm 0; padding: 3mm 4mm; background: #f4f7fa;
  border-left: 3.5px solid #a8bccf; color: #2c3947; font-size: 9.6pt; line-height: 1.72;
  break-inside: avoid; }
blockquote.meta { background: #f7f9fb; border-left-color: #1F3864; }
blockquote.meta p { margin: 0 0 1.2mm; }
blockquote.meta p:last-child { margin-bottom: 0; }
p.callout { background: #eef8f7; border-left: 4.5px solid #1F9D96;
  padding: 3.2mm 4mm; margin: 4.5mm 0 4mm; break-inside: avoid; }
pre { background: #f6f8fa; border: 1px solid #e1e6ec; border-left: 3.5px solid #1F9D96;
  border-radius: 3px; padding: 3mm 3.6mm; margin: 3.2mm 0;
  font-family: Consolas, "Cascadia Mono", "Courier New", monospace;
  font-size: 8.9pt; line-height: 1.56; color: #1c2530;
  white-space: pre-wrap; word-break: break-word; text-align: left; }
pre.keep { break-inside: avoid; }
code { font-family: Consolas, "Cascadia Mono", monospace; font-size: .9em;
  background: #f0f2f5; color: #b0316a; padding: .4px 3px; border-radius: 2px; }
pre code { background: none; color: inherit; padding: 0; font-size: 1em; }
code.math-fail { color: #a33; background: #fdf3f3; }
figure { margin: 5mm 0 5.5mm; text-align: center; break-inside: avoid; }
figure img { max-width: 100%; max-height: 196mm; }
figure.fig-illus img { max-width: 120mm; }
figcaption { font-size: 8.9pt; color: #5d6773; line-height: 1.65;
  margin-top: 2.2mm; text-align: center; text-indent: 0; }
img { max-width: 100%; }
math { font-family: "Cambria Math", "Latin Modern Math", "STIX Two Math", serif;
  font-size: 11.5pt; }
.math-display { text-align: center; margin: 4mm 0; padding: 1mm 0;
  break-inside: avoid; line-height: 1.9; }
p math { font-size: 10.8pt; }
table { width: 100%; border-collapse: collapse; margin: 3mm 0; font-size: 9.4pt; }
th, td { border: 1px solid #cfd6dd; padding: 1.6mm 2.2mm; text-align: left; }
th { background: #eef2f7; color: #1F3864; }
.toc { margin: 5mm 0 2mm; }
.toc-h { font-size: 13pt; font-weight: 700; color: #1F3864; text-align: center;
  letter-spacing: 4px; margin-bottom: 3.4mm; break-after: avoid; }
.toc-item { display: flex; align-items: flex-end; font-size: 9.6pt;
  line-height: 1.5; margin: .55mm 0; break-inside: avoid; }
.toc-item.lv2 { font-weight: 700; color: #1F3864; margin-top: 1.6mm; }
.toc-item.lv3 { padding-left: 7mm; color: #3b4756; }
.toc-item.lv2 .toc-t { color: #1F3864; }
.toc-t { color: #1e2f43; border: none; }
.toc-dots { flex: 1; border-bottom: 1px dotted #b9c2cc; margin: 0 2mm 1.1mm; }
.toc-pg { color: #33475b; min-width: 8mm; text-align: right;
  font-variant-numeric: tabular-nums; }
.pm { font-size: 1px; color: #ffffff; }
.colophon { margin-top: 8mm; padding-top: 3mm; border-top: 1px solid #e2e6ea;
  font-size: 8pt; color: #8c949c; text-align: center; }
"""

TPL = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>%s</title>
<style>%s</style></head><body>
%s
<div class="colophon">由源文件 <code>%s</code> 转换生成 · %s</div>
</body></html>"""


# ---------------------------------------------------------------- 主流程
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--mode', default='pass1')
    ap.add_argument('--pagemap')
    a = ap.parse_args()

    pagemap = json.load(open(a.pagemap, encoding='utf-8')) if a.pagemap else None
    src_dir = os.path.dirname(os.path.abspath(a.src))
    raw = open(a.src, encoding='utf-8').read()
    raw = YAML_RE.sub('', raw, count=1) if raw.lstrip().startswith('---') else raw

    stats = {'block_math': 0, 'inline_math': 0, 'math_err': [], 'missing_img': []}
    slots, inlines = [], []
    text = preprocess(raw, src_dir, slots, inlines, stats)

    md = markdown.Markdown(extensions=['extra', 'sane_lists', TocExtension(toc_depth='1-3')])
    body = md.convert(text)
    body = body.replace('<h1 id=', '<h1 class="doc-title" id=', 1)

    title = ''
    t = re.search(r'<h1[^>]*>(.*?)</h1>', body, re.S)
    if t:
        title = re.sub(r'<[^>]+>', '', t.group(1)).strip()

    toc_html, n_toc = build_toc(md.toc_tokens, pagemap)
    body = postprocess(body, slots, toc_html, markers=(a.mode == 'pass1'), work=a.work)
    for i, h in enumerate(inlines):
        body = body.replace('@@IM%d@@' % i, h)

    out_html = os.path.join(a.work, 'build1.html' if a.mode == 'pass1' else 'build2.html')
    open(out_html, 'w', encoding='utf-8').write(
        TPL % (H.escape(title), CSS, body, os.path.basename(a.src), BUILD_DATE))

    json.dump({'title': title, 'toc': n_toc, 'block_math': stats['block_math'],
               'inline_math': stats['inline_math'], 'math_err': stats['math_err'],
               'missing_img': stats['missing_img']},
              open(os.path.join(a.work, 'meta_%s.json' % a.mode), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print('[%s] %s | 目录%d 块公式%d 行内公式%d 公式失败%d 缺图%d'
          % (a.mode, title, n_toc, stats['block_math'], stats['inline_math'],
             len(stats['math_err']), len(stats['missing_img'])))


if __name__ == '__main__':
    main()
