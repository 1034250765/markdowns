#!/usr/bin/env python3
"""Evaluate the original COCO-pretrained YOLO11m on the Cows2021 test view (2131).

Extends the PretrainedYOLO11mBaseline protocol (labels 0->19, classes=[19],
COCO 80-class config) to the frozen Cows2021 test split, so the baseline row
matches the unified Cows2021 column view of the 14x14 matrix.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import yaml

ULTRALYTICS_ROOT = Path("/data1/yxli/CODE/ultralytics")
PROJECT_ROOT = ULTRALYTICS_ROOT / "OOD" / "TargetUnifyTests"
DATA_ROOT = PROJECT_ROOT / "data" / "pretrained_baseline_Cows2021_test"
CONFIG_ROOT = PROJECT_ROOT / "configs"
RESULT_ROOT = PROJECT_ROOT / "results" / "yolo11m_pretrained_cows2021_test"
SOURCE_ROOT = ULTRALYTICS_ROOT / "self_mAP" / "datasets" / "Cows2021"
WEIGHTS = ULTRALYTICS_ROOT / "self_mAP" / "models" / "yolo11m.pt"
COW_CLASS_ID = 19
SPLIT = "test"
EXPECTED_IMAGES = 2131

IMAGE_SUFFIXES = {".bmp", ".dng", ".jpeg", ".jpg", ".mpo", ".png", ".tif", ".tiff", ".webp"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def prepare_view() -> int:
    source_images = SOURCE_ROOT / "images" / SPLIT
    source_labels = SOURCE_ROOT / "labels" / SPLIT
    images = sorted(
        path for path in source_images.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    )
    labels = sorted(path for path in source_labels.rglob("*.txt") if path.is_file())
    image_stems = {path.relative_to(source_images).with_suffix("").as_posix() for path in images}
    label_stems = {path.relative_to(source_labels).with_suffix("").as_posix() for path in labels}
    if not images or image_stems != label_stems:
        raise ValueError(
            f"image/label mismatch: images={len(images)} labels={len(labels)} "
            f"missing={len(image_stems - label_stems)} orphan={len(label_stems - image_stems)}"
        )
    if len(images) != EXPECTED_IMAGES:
        raise ValueError(f"expected {EXPECTED_IMAGES} images, found {len(images)}")

    view_images = DATA_ROOT / "images" / SPLIT
    view_labels = DATA_ROOT / "labels" / SPLIT
    if view_images.exists() or view_labels.exists():
        # Idempotent reuse: the view was already prepared by a previous run;
        # validate it matches the source stems instead of recreating it.
        view_image_stems = {
            path.relative_to(view_images).with_suffix("").as_posix()
            for path in view_images.rglob("*")
            if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
        }
        view_label_stems = {
            path.relative_to(view_labels).with_suffix("").as_posix()
            for path in view_labels.rglob("*.txt")
            if path.is_file()
        }
        if view_image_stems != image_stems or view_label_stems != label_stems:
            raise RuntimeError(f"existing view does not match the source: {DATA_ROOT}")
        for label_file in view_labels.rglob("*.txt"):
            for raw_line in label_file.read_text(encoding="utf-8").splitlines():
                line = raw_line.strip()
                if line and line.split()[0] != str(COW_CLASS_ID):
                    raise RuntimeError(f"existing view label not class {COW_CLASS_ID}: {label_file}")
        print(f"[check] view reused: images={len(view_image_stems)} labels={len(view_label_stems)}")
        return len(images)
    view_images.mkdir(parents=True)
    view_labels.mkdir(parents=True)
    boxes = 0
    for source_image in images:
        (view_images / source_image.name).symlink_to(source_image.resolve())
    for source_label in labels:
        transformed = []
        for line_number, raw_line in enumerate(
            source_label.read_text(encoding="utf-8").splitlines(), 1
        ):
            line = raw_line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) != 5 or parts[0] != "0":
                raise ValueError(
                    f"{source_label}:{line_number}: expected YOLO class 0, got {line!r}"
                )
            transformed.append(" ".join([str(COW_CLASS_ID), *parts[1:]]))
            boxes += 1
        (view_labels / source_label.name).write_text(
            "\n".join(transformed) + ("\n" if transformed else ""), encoding="utf-8"
        )
    print(f"[check] view prepared: images={len(images)} labels={len(labels)} boxes={boxes}")
    return len(images)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=12)
    parser.add_argument("--device", default="0")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--conf", type=float, default=0.001)
    parser.add_argument("--iou", type=float, default=0.7)
    parser.add_argument("--max-det", type=int, default=300)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()

    count = prepare_view()

    metrics_file = RESULT_ROOT / "metrics.json"
    signature = {
        "schema_version": 1,
        "model": "original_yolo11m_coco_pretrained",
        "weights": str(WEIGHTS),
        "weights_sha256": sha256_file(WEIGHTS),
        "dataset": "Cows2021",
        "view": "Cows2021_test_2131",
        "split": SPLIT,
        "evaluated_classes": [COW_CLASS_ID],
        "imgsz": args.imgsz,
        "batch": args.batch,
        "conf": args.conf,
        "iou": args.iou,
        "max_det": args.max_det,
    }
    if metrics_file.is_file():
        payload = json.loads(metrics_file.read_text(encoding="utf-8"))
        if payload.get("signature") != signature:
            raise RuntimeError(f"Existing metrics use different settings: {metrics_file}")
        print(f"[skip] metrics already exist: {metrics_file}")
        return
    if args.check_only:
        print("[check] ready")
        return

    from ultralytics import YOLO

    model = YOLO(str(WEIGHTS))
    names = {int(key): str(value) for key, value in model.names.items()}
    if len(names) != 80 or names[COW_CLASS_ID].lower() != "cow":
        raise ValueError(f"Expected COCO class {COW_CLASS_ID} to be cow, got {model.names!r}")

    CONFIG_ROOT.mkdir(parents=True, exist_ok=True)
    config = CONFIG_ROOT / "pretrained_baseline_Cows2021_test.yaml"
    content = {
        "path": str(DATA_ROOT),
        "train": f"images/{SPLIT}",
        "val": f"images/{SPLIT}",
        "test": f"images/{SPLIT}",
        "nc": len(names),
        "names": names,
    }
    config.write_text(
        "# Original COCO-pretrained YOLO11m baseline on Cows2021 test (2131); cow is COCO class 19.\n"
        + yaml.safe_dump(content, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    print(f"[eval] pretrained baseline -> Cows2021 test: images={count}")
    metrics = model.val(
        data=str(config),
        split=SPLIT,
        classes=[COW_CLASS_ID],
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        workers=args.workers,
        conf=args.conf,
        iou=args.iou,
        max_det=args.max_det,
        plots=False,
        project=str(RESULT_ROOT),
        name="val",
        exist_ok=True,
        verbose=False,
    )
    payload = {
        "signature": signature,
        "model": "original_yolo11m_coco_pretrained",
        "dataset": "Cows2021",
        "display_name": "Cows2021",
        "view": "Cows2021_test_2131",
        "images": count,
        "precision": float(metrics.box.mp),
        "recall": float(metrics.box.mr),
        "map50": float(metrics.box.map50),
        "map50_95": float(metrics.box.map),
        "speed_ms_per_image": {key: float(value) for key, value in metrics.speed.items()},
        "save_dir": str(metrics.save_dir),
    }
    metrics_file.parent.mkdir(parents=True, exist_ok=True)
    metrics_file.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"[done] {metrics_file}")


if __name__ == "__main__":
    main()
