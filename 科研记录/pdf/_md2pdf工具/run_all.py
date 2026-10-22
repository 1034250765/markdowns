# -*- coding: utf-8 -*-
"""批量把科研记录 Markdown 转成 A4 打印级 PDF（两遍编译 + 页脚页码）"""
import os, re, sys, json, subprocess
import pymupdf

BUILD = r'C:\Users\LYX10\AppData\Local\Temp\ls-pdf-build'
SRC_DIR = r'C:\Users\LYX10\Downloads\Typora\科研记录'
OUT_DIR = os.path.join(SRC_DIR, 'pdf')
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
FONT_FILE = r'C:\Windows\Fonts\Deng.ttf'
PY = sys.executable

DOCS = [
    'Label-Studio进行数据标注的分析与操作步骤',
    '域内重测',
    '用于测试的数据集拍摄环境与场景',
    '数据集整理与独立测试集评估',
    '三种模型测试',
    '多源留一域泛化',
    '27个牛类公开数据集详细档案',
]


def build(work, src, mode, pagemap=None):
    cmd = [PY, os.path.join(BUILD, 'md2pdf.py'), '--src', src, '--work', work, '--mode', mode]
    if pagemap:
        cmd += ['--pagemap', pagemap]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    if r.returncode:
        raise SystemExit('构建失败 %s\n%s\n%s' % (mode, r.stdout, r.stderr))
    print('   ', r.stdout.strip())


def chrome(work, html_name, pdf_name):
    html, pdf = os.path.join(work, html_name), os.path.join(work, pdf_name)
    if os.path.exists(pdf):
        os.remove(pdf)
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-first-run',
                    '--no-default-browser-check', '--allow-file-access-from-files',
                    '--user-data-dir=' + os.path.join(BUILD, 'chrome-profile'),
                    '--no-pdf-header-footer', '--virtual-time-budget=60000',
                    '--print-to-pdf=' + pdf, 'file:///' + html.replace('\\', '/')],
                   check=True, capture_output=True)
    return pdf


def scan(pdf):
    d = pymupdf.open(pdf)
    marks = {}
    for i, p in enumerate(d):
        t = re.sub(r'\s+', '', p.get_text())
        for m in re.finditer(r'LSMK(\d{4})END', t):
            marks[int(m.group(1))] = i + 1
    n = d.page_count
    d.close()
    return n, marks


def stamp(pdf_in, pdf_out, title):
    d = pymupdf.open(pdf_in)
    total = d.page_count
    font = pymupdf.Font(fontfile=FONT_FILE)
    foot = title if len(title) <= 30 else title[:29] + '…'
    for i, page in enumerate(d):
        r = page.rect
        y = r.height - 34
        page.draw_line(pymupdf.Point(42, y - 9), pymupdf.Point(r.width - 42, y - 9),
                       color=(0.85, 0.87, 0.89), width=0.5)
        page.insert_text((42, y + 1), foot, fontname='f0', fontfile=FONT_FILE,
                         fontsize=7.5, color=(0.55, 0.58, 0.62))
        label = '第 %d 页 / 共 %d 页' % (i + 1, total)
        w = font.text_length(label, fontsize=8.4)
        page.insert_text((r.width - 42 - w, y + 1), label, fontname='f0',
                         fontfile=FONT_FILE, fontsize=8.4, color=(0.32, 0.36, 0.40))
    try:
        d.subset_fonts()
    except Exception:
        pass
    d.save(pdf_out, garbage=4, deflate=True)
    d.close()


def run_one(idx, name):
    src = os.path.join(SRC_DIR, name + '.md')
    work = os.path.join(BUILD, 'doc%d' % idx)
    os.makedirs(work, exist_ok=True)
    print('\n[%d/%d] %s' % (idx, len(DOCS), name))

    build(work, src, 'pass1')
    meta = json.load(open(os.path.join(work, 'meta_pass1.json'), encoding='utf-8'))
    if meta['math_err'] or meta['missing_img']:
        print('   !! 公式失败 %s | 缺图 %s' % (meta['math_err'], meta['missing_img']))

    n1, marks = scan(chrome(work, 'build1.html', 'pass1.pdf'))
    heads = json.load(open(os.path.join(work, 'heads.json'), encoding='utf-8'))
    miss = [n for n in range(len(heads)) if n not in marks]
    if miss:
        raise SystemExit('   !! 定位标记缺失: %s' % miss)
    pagemap = {heads[k]: v for k, v in marks.items()}
    pm_path = os.path.join(work, 'pagemap.json')
    json.dump(pagemap, open(pm_path, 'w', encoding='utf-8'), ensure_ascii=False)

    build(work, src, 'pass2', pm_path)
    p2 = chrome(work, 'build2.html', 'pass2.pdf')
    n2, _ = scan(p2)
    if n2 != n1:
        raise SystemExit('   !! 分页不一致 pass1=%d pass2=%d' % (n1, n2))

    d = pymupdf.open(p2)
    left = any('LSMK' in re.sub(r'\s+', '', p.get_text()) for p in d)
    imgs = sum(len(p.get_images(full=True)) for p in d)
    d.close()

    out = os.path.join(OUT_DIR, name + '.pdf')
    stamp(p2, out, meta['title'])
    print('   -> %s | %d 页 | 图 %d | 残留标记 %s | %.1f MB'
          % (os.path.basename(out), n2, imgs, left, os.path.getsize(out) / 1048576))
    return out, n2


if __name__ == '__main__':
    os.makedirs(OUT_DIR, exist_ok=True)
    results = []
    for i, n in enumerate(DOCS, 1):
        results.append(run_one(i, n))
    print('\n===== 汇总 =====')
    for out, n in results:
        print('  %-52s %3d 页' % (os.path.basename(out), n))
