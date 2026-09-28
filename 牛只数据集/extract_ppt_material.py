import fitz, os, json
pdf_path = r'C:\Users\LYX10\Downloads\Typora\牛只数据集\2601.09497.pdf'
out_dir = r'C:\Users\LYX10\Downloads\Typora\牛只数据集\ppt_material'
os.makedirs(out_dir, exist_ok=True)

doc = fitz.open(pdf_path)
texts = []
for i, page in enumerate(doc):
    texts.append(f'## Page {i+1}\n\n{page.get_text()}')
    # extract images
    for img_idx, img in enumerate(page.get_images(full=True)):
        xref = img[0]
        pix = fitz.Pixmap(doc, xref)
        if pix.n > 4:
            pix = fitz.Pixmap(fitz.csRGB, pix)
        img_path = os.path.join(out_dir, f'page_{i+1:02d}_img_{img_idx+1}.png')
        pix.save(img_path)
        pix = None
with open(os.path.join(out_dir, 'paper_text.md'), 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(texts))
print('extracted', len(texts), 'pages')
print('images in', out_dir)
