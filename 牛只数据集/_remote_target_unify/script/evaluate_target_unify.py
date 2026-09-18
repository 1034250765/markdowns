#!/usr/bin/env python3
"""Evaluate source-trained YOLO11m models on three frozen unified target views.

Targets (frozen evaluation views for view unification):
  Cows2021_test         : self_mAP/datasets/Cows2021, split=test (2131 images)
  Google_Open_Images_576: leakage-revised view, split=val (576 images)
  COCO_342              : leakage-revised view, split=val (342 images)

Evaluation parameters match the existing YOLO11m OOD suite exactly:
imgsz=640, batch=12, conf=0.001, iou=0.7, max_det=300, single class `cow`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ULTRALYTICS_ROOT = Path("/data1/yxli/CODE/ultralytics")
PROJECT_ROOT = ULTRALYTICS_ROOT / "OOD" / "TargetUnifyTests"
CONFIG_ROOT = PROJECT_ROOT / "configs"
RESULT_ROOT = PROJECT_ROOT / "results" / "yolo11m"
WEIGHTS_ROOT = ULTRALYTICS_ROOT / "self_mAP" / "outputs" / "yolo"
REVISION_ROOT = (
    ULTRALYTICS_ROOT
    / "OOD"
    / "audits"
    / "perceptual_hash"
    / "revisions"
    / "20260729_exclude_confirmed_coco_google_train_eval"
)
REVISION_ID = "20260729_exclude_confirmed_coco_google_train_eval"

IMAGE_SUFFIXES = {".bmp", ".dng", ".jpeg", ".jpg", ".mpo", ".png", ".tif", ".tiff", ".webp"}

# source key -> weights directory name under self_mAP/outputs/yolo
SOURCE_MODELS: dict[str, str] = {
    "8-calves": "8-calves",
    "animals_10": "animals_10",
    "CBPD_ODD": "CBPD_ODD",
    "CID": "CID",
    "CImage": "CImage_new1class",
    "COCO": "COCO_new1class",
    "COLO": "COLO",
    "Cows2021": "Cows2021",
    "diarycow": "diarycow",
    "Google_Open_Images": "Google Open Image Dataset",
    "HCRD": "HCRD",
    "MooTrack360": "MooTrack360",
    "NWAFU_CD": "NWAFU_CD_new1class",
    "XGain": "XGain",
}

DISPLAY_NAMES = {
    "8-calves": "8-calves",
    "animals_10": "animals_10",
    "CBPD_ODD": "CBPD_ODD",
    "CID": "CID",
    "CImage": "CImage",
    "COCO": "COCO cow subset",
    "COLO": "COLO",
    "Cows2021": "Cows2021",
    "diarycow": "Dairy Cow",
    "Google_Open_Images": "Google Open Images cow subset",
    "HCRD": "HCRD",
    "MooTrack360": "MooTrack360",
    "NWAFU_CD": "NWAFU Cattle Dataset",
    "XGain": "XGain",
}


@dataclass(frozen=True)
class TargetView:
    key: str
    data_root: Path
    split: str
    revision_id: str
    revision_manifest: Path | None
    sources: tuple[str, ...]
    expected_images: int
    note: str

    @property
    def images_dir(self) -> Path:
        return self.data_root / "images" / self.split

    @property
    def labels_dir(self) -> Path:
        return self.data_root / "labels" / self.split


def build_targets() -> dict[str, TargetView]:
    manifest = REVISION_ROOT / "revision_manifest.csv"
    return {
        "Cows2021_test": TargetView(
            key="Cows2021_test",
            data_root=ULTRALYTICS_ROOT / "self_mAP" / "datasets" / "Cows2021",
            split="test",
            revision_id="original",
            revision_manifest=None,
            sources=tuple(k for k in SOURCE_MODELS if k != "Cows2021"),
            expected_images=2131,
            note=(
                "Cows2021 frozen test view. Incoming sources only; the Cows2021 "
                "self diagonal already exists on this view (Cows2021OOD runs/"
                "Cows2021_test, mAP50-95 0.8629)."
            ),
        ),
        "Google_Open_Images_576": TargetView(
            key="Google_Open_Images_576",
            data_root=REVISION_ROOT / "views" / "coco_source" / "data" / "Google_Open_Images",
            split="val",
            revision_id=REVISION_ID,
            revision_manifest=manifest,
            sources=tuple(k for k in SOURCE_MODELS if k != "COCO"),
            expected_images=576,
            note=(
                "Leakage-revised Google Open Images view. The COCO source was "
                "already evaluated on this view during the 20260729 revision "
                "(mAP50-95 0.3985) and is not repeated here."
            ),
        ),
        "COCO_342": TargetView(
            key="COCO_342",
            data_root=REVISION_ROOT / "views" / "google_open_image_source" / "data" / "COCO",
            split="val",
            revision_id=REVISION_ID,
            revision_manifest=manifest,
            sources=tuple(k for k in SOURCE_MODELS if k != "Google_Open_Images"),
            expected_images=342,
            note=(
                "Leakage-revised COCO view. The Google Open Images source was "
                "already evaluated on this view during the 20260729 revision "
                "(mAP50-95 0.4737) and is not repeated here."
            ),
        ),
    }


TARGETS = build_targets()


def image_label_stems(images_dir: Path, labels_dir: Path) -> tuple[set[str], set[str]]:
    image_stems = {
        path.relative_to(images_dir).with_suffix("").as_posix()
        for path in images_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    }
    label_stems = {
        path.relative_to(labels_dir).with_suffix("").as_posix()
        for path in labels_dir.rglob("*.txt")
        if path.is_file()
    }
    return image_stems, label_stems


def validate_view(target: TargetView) -> int:
    images_dir, labels_dir = target.images_dir, target.labels_dir
    if not images_dir.is_dir() or not labels_dir.is_dir():
        raise FileNotFoundError(
            f"{target.key}: missing split directories: {images_dir}, {labels_dir}"
        )
    image_stems, label_stems = image_label_stems(images_dir, labels_dir)
    if not image_stems:
        raise ValueError(f"{target.key}: no images found in {images_dir}")
    if image_stems != label_stems:
        raise ValueError(
            f"{target.key}: image/label mismatch: "
            f"missing_labels={len(image_stems - label_stems)} "
            f"orphan_labels={len(label_stems - image_stems)}"
        )
    if len(image_stems) != target.expected_images:
        raise ValueError(
            f"{target.key}: expected {target.expected_images} images, "
            f"found {len(image_stems)}"
        )
    return len(image_stems)


def write_config(target: TargetView) -> Path:
    CONFIG_ROOT.mkdir(parents=True, exist_ok=True)
    path = CONFIG_ROOT / f"{target.key}.yaml"
    split_rel = f"images/{target.split}"
    content = {
        "path": str(target.data_root),
        "train": split_rel,
        "val": split_rel,
        "test": split_rel,
        "nc": 1,
        "names": ["cow"],
    }
    path.write_text(
        f"# Frozen unified target view - {target.key}\n"
        + yaml.safe_dump(content, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return path


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_signature(
    args: argparse.Namespace, target: TargetView, source: str, weights: Path
) -> dict[str, Any]:
    stat = weights.stat()
    return {
        "schema_version": 1,
        "model": "yolo11m",
        "id_dataset": source,
        "weights": str(weights),
        "weights_size": stat.st_size,
        "weights_mtime_ns": stat.st_mtime_ns,
        "dataset": source,
        "target": target.key,
        "target_data_root": str(target.data_root),
        "split": target.split,
        "revision_id": target.revision_id,
        "revision_manifest": (
            str(target.revision_manifest) if target.revision_manifest else None
        ),
        "revision_manifest_sha256": (
            sha256_of(target.revision_manifest) if target.revision_manifest else None
        ),
        "imgsz": args.imgsz,
        "batch": args.batch,
        "conf": args.conf,
        "iou": args.iou,
        "max_det": args.max_det,
    }


def evaluate_cell(
    args: argparse.Namespace,
    model,
    target: TargetView,
    source: str,
    weights: Path,
    image_count: int,
) -> dict[str, Any]:
    run_dir = RESULT_ROOT / "runs" / target.key / source
    metrics_file = run_dir / "metrics.json"
    expected_signature = run_signature(args, target, source, weights)

    if metrics_file.is_file():
        payload = json.loads(metrics_file.read_text(encoding="utf-8"))
        if payload.get("signature") != expected_signature:
            raise RuntimeError(
                f"Existing metrics use different settings: {metrics_file}. "
                "Archive the run before evaluating again."
            )
        print(f"[skip] {target.key}/{source}: metrics already exist")
        return payload
    if run_dir.exists():
        raise RuntimeError(
            f"Incomplete output directory exists without metrics.json: {run_dir}. "
            "Archive it before retrying."
        )

    data_yaml = write_config(target)
    print(f"[eval] {target.key}/{source}: images={image_count} split={target.split}")
    metrics = model.val(
        data=str(data_yaml),
        split=target.split,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        workers=args.workers,
        conf=args.conf,
        iou=args.iou,
        max_det=args.max_det,
        plots=args.plots,
        project=str(RESULT_ROOT / "runs" / target.key),
        name=source,
        exist_ok=False,
        verbose=args.verbose,
    )
    payload = {
        "signature": expected_signature,
        "model": "yolo11m",
        "id_dataset": source,
        "dataset": source,
        "display_name": DISPLAY_NAMES[source],
        "target": target.key,
        "target_note": target.note,
        "in_domain": source == target_key_to_dataset(target.key),
        "images": image_count,
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
    return payload


def target_key_to_dataset(target_key: str) -> str | None:
    """Dataset key whose own model this view provides a same-view denominator for."""
    if target_key == "Cows2021_test":
        return None  # Cows2021 self diagonal comes from Cows2021OOD, not rerun here
    if target_key == "Google_Open_Images_576":
        return "Google_Open_Images"
    if target_key == "COCO_342":
        return "COCO"
    return None


def load_model(weights: Path):
    from ultralytics import YOLO

    if not weights.is_file():
        raise FileNotFoundError(f"Missing YOLO11m weights: {weights}")
    model = YOLO(str(weights))
    names = model.names
    values = list(names.values()) if isinstance(names, dict) else list(names)
    if len(values) != 1 or str(values[0]).lower() != "cow":
        raise ValueError(f"Expected one cow class, got {names!r}")
    return model


def write_summaries(selected: dict[str, TargetView]) -> None:
    RESULT_ROOT.mkdir(parents=True, exist_ok=True)
    all_records = []
    for key, target in selected.items():
        records = []
        for source in target.sources:
            metrics_file = RESULT_ROOT / "runs" / target.key / source / "metrics.json"
            if metrics_file.is_file():
                records.append(json.loads(metrics_file.read_text(encoding="utf-8")))
        (RESULT_ROOT / f"summary_{target.key}.json").write_text(
            json.dumps(
                {"target": key, "note": target.note, "records": records},
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        all_records.extend(records)
    (RESULT_ROOT / "summary.json").write_text(
        json.dumps(
            {
                "purpose": "Frozen unified target views for the 14x14 YOLO11m matrix",
                "targets": {key: target.note for key, target in selected.items()},
                "records": all_records,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--targets", nargs="+", choices=sorted(TARGETS))
    parser.add_argument("--sources", nargs="+", choices=sorted(SOURCE_MODELS))
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=12)
    parser.add_argument("--device", default="0")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--conf", type=float, default=0.001)
    parser.add_argument("--iou", type=float, default=0.7)
    parser.add_argument("--max-det", type=int, default=300)
    parser.add_argument("--plots", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--verbose", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--check-only", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    selected = {
        key: target
        for key, target in TARGETS.items()
        if not args.targets or key in args.targets
    }
    if not selected:
        raise SystemExit("No targets selected.")

    counts = {}
    for target in selected.values():
        counts[target.key] = validate_view(target)
        write_config(target)
        print(
            f"[check] target={target.key} split={target.split} "
            f"images={counts[target.key]} revision={target.revision_id}"
        )

    source_order = [s for s in SOURCE_MODELS if not args.sources or s in args.sources]
    plan = [
        (source, target)
        for source in source_order
        for target in selected.values()
        if source in target.sources
    ]
    weights_by_source = {
        source: WEIGHTS_ROOT / name / "weights" / "best.pt"
        for source, name in SOURCE_MODELS.items()
        if source in source_order
    }
    for source, weights in weights_by_source.items():
        if not weights.is_file():
            raise FileNotFoundError(f"Missing weights for {source}: {weights}")
        print(f"[check] source={source} weights={weights}")

    print(f"[check] planned evaluations: {len(plan)}")
    if args.check_only:
        return

    for source in source_order:
        model = load_model(weights_by_source[source])
        print(f"[model] loaded {source}")
        for target in selected.values():
            if source in target.sources:
                evaluate_cell(
                    args, model, target, source, weights_by_source[source], counts[target.key]
                )
                write_summaries(selected)
    write_summaries(selected)
    print(f"[done] summaries: {RESULT_ROOT}")


if __name__ == "__main__":
    main()
