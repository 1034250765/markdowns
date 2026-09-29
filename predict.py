"""用 merged_cow/best.pt 对 CVBD 全部图片推理, 生成个体级 YOLO 预标注 txt。

本脚本用合并模型推理生成每头牛一个框的预标注。

输入: yolo_data/images
输出: yolo_data/labels/<stem>.txt
格式: <cls> cx cy w h (归一化), cls=0 (cow)
分批推理 (batch=32, 非 stream), 沿用 推理参数 conf=0.25 imgsz=640。
"""

import time
from pathlib import Path

from ultralytics import YOLO


MODEL = "/data1/yxli/CODE/ultralytics/merged_cow/runs/merged_cow/weights/best.pt"

DATA_ROOT = Path("/data1/yxli/CODE/ultralytics/COWpredict/CVBD/yolo_data")
CONF = 0.25
IMGSZ = 640
DEVICE = "0"
BATCH = 32

def collect():
    """返回 [(img_path, out_txt_path), ...], 按 stem 排序。"""
    img_dir = DATA_ROOT / "images"
    lbl_dir = DATA_ROOT / "labels"
    lbl_dir.mkdir(parents=True, exist_ok=True)
    tasks = []
    for p in sorted(img_dir.iterdir()):
        if p.is_file() and p.suffix.lower() in (".jpg", ".jpeg", ".png"):
            out = lbl_dir / (p.stem + ".txt")
            tasks.append((str(p), out))
    return tasks

def main():
    model = YOLO(MODEL)

    t0 = time.time()

    tasks = collect()
    n = len(tasks)
    print(f"[infer] 全部: {n} 张, 分批 {BATCH}", flush=True)
    done = 0
    empty = 0
    boxes = 0
    for i in range(0, n, BATCH):
        chunk = tasks[i:i + BATCH]
        imgs = [c[0] for c in chunk]
        outs = [c[1] for c in chunk]
        results = model.predict(imgs, conf=CONF, imgsz=IMGSZ, device=DEVICE,
                                batch=len(imgs), stream=False, verbose=False,
                                save=False, save_txt=False, save_conf=False)

        for result, out in zip(results, outs):
            lines = []
            if result.boxes is not None and len(result.boxes) > 0:
                classes = result.boxes.cls.cpu().numpy().astype(int)
                boxes_xywhn = result.boxes.xywhn.cpu().numpy()
                for cls, box in zip(classes, boxes_xywhn):
                    lines.append(
                        f"{cls} {box[0]:.6f} {box[1]:.6f} "
                        f"{box[2]:.6f} {box[3]:.6f}"
                    )
                boxes += len(lines)
            else:
                empty += 1

            out.write_text(
                "\n".join(lines) + ("\n" if lines else ""),
                encoding="utf-8",
            )
            done += 1

        print(
            f"[infer] {done}/{n} 完成, 空框 {empty}, 框 {boxes}",
            flush=True,
        )

    print(
        f"[infer] 全部完成: {done} 张, 空框 {empty} 张, "
        f"总框 {boxes}, 总耗时 {time.time()-t0:.0f}s"
    )
    if done:
        print(
            f"[infer] 检出率: {(done-empty)/done*100:.2f}%, "
            f"平均每图 {boxes/done:.2f} 框"
        )
    print(f"[infer] 标注输出: {DATA_ROOT}/labels/")


if __name__ == "__main__":
    main()
