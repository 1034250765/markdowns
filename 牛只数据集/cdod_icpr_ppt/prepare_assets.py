from PIL import Image
import os

base = r'C:\Users\LYX10\Downloads\Typora\牛只数据集'
src = os.path.join(base, 'ppt_material')
dst = os.path.join(base, 'cdod_icpr_ppt', 'assets')
os.makedirs(dst, exist_ok=True)

def merge_grid(paths, out_name, cols=2, max_width=1100):
    imgs = [Image.open(p) for p in paths]
    w = max([img.width for img in imgs])
    h = max([img.height for img in imgs])
    rows = (len(imgs) + cols - 1) // cols
    canvas = Image.new('RGB', (w * cols, h * rows), (255, 255, 255))
    for i, img in enumerate(imgs):
        row = i // cols
        col = i % cols
        canvas.paste(img, (col * w, row * h))
    if canvas.width > max_width:
        scale = max_width / canvas.width
        canvas = canvas.resize((max_width, int(canvas.height * scale)), Image.Resampling.LANCZOS)
    out = os.path.join(dst, out_name)
    canvas.save(out)
    print('saved', out, canvas.size)

# Fig.1: same COCO image under 4 source training sets
merge_grid([
    os.path.join(src, 'page_03_img_1.png'),
    os.path.join(src, 'page_03_img_2.png'),
    os.path.join(src, 'page_03_img_3.png'),
    os.path.join(src, 'page_03_img_4.png'),
], 'fig1_cross_dataset_comparison.png')

# Representative examples: agnostic vs specific
merge_grid([
    os.path.join(src, 'page_06_img_1.png'),
    os.path.join(src, 'page_06_img_5.png'),
], 'fig2_agnostic_vs_specific.png', cols=2)

# Fig.4 qualitative: pick a few representative cases
# a few successful and failure cases
merge_grid([
    os.path.join(src, 'page_12_img_1.png'),  # O365->COCO failure
    os.path.join(src, 'page_12_img_2.png'),  # O365->O365 success
    os.path.join(src, 'page_12_img_3.png'),  # O365->City success
    os.path.join(src, 'page_12_img_19.png'), # COCO->BDD success
    os.path.join(src, 'page_12_img_20.png'), # COCO->BDD failure (night/glare)
    os.path.join(src, 'page_12_img_17.png'), # City->BDD success
], 'fig4_qualitative_cases.png', cols=3)

print('done')
