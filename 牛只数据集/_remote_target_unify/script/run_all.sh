#!/usr/bin/env bash
set -euo pipefail

project_root="/data1/yxli/CODE/ultralytics/OOD/TargetUnifyTests"
python_bin="/data1/yxli/miniconda3/envs/ultralytics/bin/python"
script="$project_root/script/evaluate_target_unify.py"
result_root="$project_root/results/yolo11m"

if [[ ! -x "$python_bin" ]]; then
  echo "Python not executable: $python_bin" >&2
  exit 1
fi
if [[ ! -f "$script" ]]; then
  echo "Evaluation script not found: $script" >&2
  exit 1
fi

mkdir -p "$result_root"
exec 9>"$result_root/evaluate.lock"
if ! flock -n 9; then
  echo "Another TargetUnifyTests evaluation is already running." >&2
  exit 1
fi

exec "$python_bin" -u "$script" "$@"
