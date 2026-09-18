import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";

const inputs = [
  ["8-calves", "../_remote_8-calvesOOD_summary.json", "8-calves", "8-calvesOOD"],
  ["animals_10", "animals_10.json", "animals_10", "animals_10OOD"],
  ["CBPD_ODD", "CBPD_ODD.json", "CBPD_ODD", "CBPD_ODDOOD"],
  ["CID", "CID.json", "CID", "CIDOOD"],
  ["CImage", "CImage.json", "CImage", "CImageOOD"],
  ["COCO", "COCO.json", "COCO", "COCOOOD"],
  ["COLO", "COLO.json", "COLO", "COLOOOD"],
  ["Cows2021", "Cows2021.json", "Cows2021", "Cows2021OOD"],
  ["diarycow", "Dairy_Cow.json", "Dairy Cow", "diarycowOOD"],
  ["Google_Open_Images", "Google_Open_Images.json", "Google OI", "Google_Open_ImageOOD"],
  ["HCRD", "HCRD.json", "HCRD", "HCRDOOD"],
  ["MooTrack360", "MooTrack360.json", "MooTrack360", "MooTrack360OOD"],
  ["NWAFU_CD", "NWAFU.json", "NWAFU", "NWAFU_CDOOD"],
  ["XGain", "XGain.json", "XGain", "XGainOOD"],
];
const keys = inputs.map(([key]) => key);
const ids = keys.map((_, i) => String(i + 1).padStart(2, "0"));
const names = Object.fromEntries(inputs.map(([key, , name]) => [key, name]));
const normalize = key => key === "Cows2021_test" ? "Cows2021" : key;
const mean = values => values.length ? values.reduce((a, b) => a + b, 0) / values.length : null;
const median = values => {
  const sorted = [...values].sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
};
const close = (a, b) => assert.ok(Math.abs(a - b) < 1e-12, `${a} != ${b}`);
const revision = "20260729_exclude_confirmed_coco_google_train_eval";
const UNIFY_FILE = "../_remote_target_unify/results/summary.json";
const UNIFY_REMOTE = "/data1/yxli/CODE/ultralytics/OOD/TargetUnifyTests/results/yolo11m/summary.json";
const UNIFY_TARGET_MAP = {
  Cows2021_test: "Cows2021",
  Google_Open_Images_576: "Google_Open_Images",
  COCO_342: "COCO",
};

const records = {};
const provenance = [];
for (const [source, file, , folder] of inputs) {
  const raw = await readFile(new URL(file, import.meta.url));
  const data = JSON.parse(raw.toString("utf8"));
  assert.equal(data.id_dataset ?? "Cows2021", source);
  assert.equal(data.records.length, 14);
  records[source] = {};
  for (const record of data.records) {
    const target = normalize(record.dataset);
    assert.ok(keys.includes(target), `Unknown target: ${target}`);
    assert.ok(!records[source][target], `Duplicate: ${source}/${target}`);
    assert.equal(record.in_domain, source === target);
    for (const metric of ["precision", "recall", "map50", "map50_95"]) {
      assert.ok(Number.isFinite(record[metric]) && record[metric] >= 0 && record[metric] <= 1);
    }
    assert.ok(Number.isInteger(record.images) && record.images > 0);
    assert.equal(record.signature.imgsz, 640);
    records[source][target] = record;
  }
  const ood = keys.filter(target => target !== source).map(target => records[source][target]);
  assert.equal(data.aggregates.completed_ood_datasets, 13);
  close(mean(ood.map(r => r.map50_95)), data.aggregates.mean_ood_map50_95);
  close(mean(ood.map(r => r.retention_pct)), data.aggregates.mean_retention_pct);
  provenance.push({
    source, file, sha256: createHash("sha256").update(raw).digest("hex"),
    remote: `/data1/yxli/CODE/ultralytics/OOD/${folder}/results/yolo11m/summary.json`,
  });
}

// View unification (2026-09-18): override the Cows2021 / Google OI / COCO columns
// with the 39 TargetUnifyTests runs on the frozen unified views. The Cows2021
// self diagonal, COCO->Google and Google->COCO are reused from earlier
// same-view runs and are NOT part of the 39.
const unifyRaw = await readFile(new URL(UNIFY_FILE, import.meta.url));
const unifyData = JSON.parse(unifyRaw.toString("utf8"));
assert.equal(unifyData.records.length, 39);
let overridden = 0;
for (const record of unifyData.records) {
  const target = UNIFY_TARGET_MAP[record.target];
  const source = record.dataset;
  assert.ok(target, `Unknown unified target: ${record.target}`);
  assert.ok(keys.includes(source), `Unknown unified source: ${source}`);
  assert.ok(!(source === "Cows2021" && target === "Cows2021"),
    "Cows2021 self diagonal must stay the reused test-view run");
  for (const metric of ["precision", "recall", "map50", "map50_95"]) {
    assert.ok(Number.isFinite(record[metric]) && record[metric] >= 0 && record[metric] <= 1);
  }
  assert.equal(record.signature.imgsz, 640);
  assert.equal(record.signature.batch, 12);
  assert.equal(record.signature.conf, 0.001);
  assert.equal(record.signature.iou, 0.7);
  assert.equal(record.signature.max_det, 300);
  records[source][target] = {
    dataset: target,
    in_domain: source === target,
    images: record.images,
    precision: record.precision,
    recall: record.recall,
    map50: record.map50,
    map50_95: record.map50_95,
    signature: {
      imgsz: record.signature.imgsz,
      split: record.signature.split,
      revision_id: record.signature.revision_id,
    },
    unified: true,
  };
  overridden += 1;
}
assert.equal(overridden, 39);
provenance.push({
  source: "TargetUnifyTests", file: UNIFY_FILE,
  sha256: createHash("sha256").update(unifyRaw).digest("hex"),
  remote: UNIFY_REMOTE,
});

const value = (source, target) => records[source][target].map50_95;
const diagonals = Object.fromEntries(keys.map(key => [key, value(key, key)]));

// Whole-column frozen views.
const COLUMN_VIEWS = { Cows2021: 2131, Google_Open_Images: 576, COCO: 342 };
for (const [column, images] of Object.entries(COLUMN_VIEWS)) {
  for (const source of keys) {
    assert.equal(records[source][column].images, images, `${source} -> ${column}`);
  }
}
assert.equal(records.Cows2021.Cows2021.signature.split, "test");
assert.equal(records.Cows2021.Cows2021.images, 2131);
assert.equal(records.COCO.Google_Open_Images.signature.revision_id, revision);
assert.equal(records.Google_Open_Images.COCO.signature.revision_id, revision);
// The other eleven columns keep matching views between incoming OOD and the diagonal.
for (const source of keys) {
  for (const target of keys) {
    if (source === target || target in COLUMN_VIEWS) continue;
    assert.equal(records[source][target].images, records[target][target].images,
      `${source} -> ${target} view mismatch`);
  }
}
// View compatibility was audited against resolved image paths and label hashes,
// not inferred merely from equal image counts. This script reuses that audit.
// The COCO and Google OI diagonals changed with the unified views (0.5190->0.5204,
// 0.4559->0.4534), so their old-file retention fields are only checked against
// the recomputed value below, not against the old per-file baseline.
const changedDiagonals = new Set(["COCO", "Google_Open_Images"]);
const cells = keys.flatMap(source => keys.map(target => {
  const r = records[source][target];
  if (!r.unified && !changedDiagonals.has(source)) {
    close(r.retention_pct, 100 * value(source, target) / diagonals[source]);
  }
  return {
    source, target, in_domain: source === target, images: r.images,
    precision: r.precision, recall: r.recall, map50: r.map50,
    map50_95: r.map50_95,
    source_retention_pct: 100 * value(source, target) / diagonals[source],
    target_retention_pct: 100 * r.map50_95 / diagonals[target],
    unified: r.unified ?? false,
    revision_id: r.signature.revision_id ?? null,
  };
}));
const cell = (source, target) => cells.find(c => c.source === source && c.target === target);
const ood = cells.filter(c => !c.in_domain);
assert.equal(cells.length, 196);
assert.equal(ood.length, 182);
assert.ok(ood.every(c => Number.isFinite(c.target_retention_pct)));
const rows = keys.map(source => {
  const subset = ood.filter(c => c.source === source);
  return {
    source, id_map50_95: diagonals[source],
    mean_ood_map50_95: mean(subset.map(c => c.map50_95)),
    median_ood_map50_95: median(subset.map(c => c.map50_95)),
    mean_source_retention_pct: mean(subset.map(c => c.source_retention_pct)),
    worst_map50_95: Math.min(...subset.map(c => c.map50_95)),
  };
});
const columns = keys.map(target => {
  const subset = ood.filter(c => c.target === target);
  return {
    target, id_map50_95: diagonals[target],
    ood_images: [...new Set(subset.map(c => c.images))],
    mean_ood_map50_95: mean(subset.map(c => c.map50_95)),
    mean_target_retention_pct: mean(subset.map(c => c.target_retention_pct)),
    valid_target_retention_n: subset.length,
    target_retention_sources: subset.map(c => c.source),
  };
});
const pairKeys = [
  ["CImage", "CID"], ["CImage", "HCRD"], ["COLO", "Cows2021"],
  ["MooTrack360", "8-calves"], ["CImage", "animals_10"],
  ["COCO", "Google_Open_Images"],
];
const pairs = pairKeys.map(([source, target]) => ({
  source, target,
  forward: value(source, target), reverse: value(target, source),
  asym: value(source, target) - value(target, source),
  forward_target_retention_pct: cell(source, target).target_retention_pct,
  reverse_target_retention_pct: cell(target, source).target_retention_pct,
}));
const result = {
  metric: "mAP@0.5:0.95", order: keys, provenance, cells, rows, columns, pairs,
  overall: { n: ood.length, mean: mean(ood.map(c => c.map50_95)), median: median(ood.map(c => c.map50_95)) },
  caveat: "Unified-view matrix: the Cows2021 (test 2131), Google OI (576) and COCO (342) columns were "
    + "re-evaluated on frozen unified views in TargetUnifyTests (39 runs, 2026-09-18); the other eleven "
    + "columns come from the original suite. 182/182 OOD cells have same-view target ID denominators.",
};
const fmt = x => x === null ? "N/A" : x > 0 && x < 0.00005 ? x.toExponential(1) : x.toFixed(4);
const pct = x => x === null ? "N/A" : x > 0 && x < 0.005 ? `${x.toExponential(1)}%` : `${x.toFixed(2)}%`;
const table = (headers, lines) => [
  `| ${headers.join(" | ")} |`,
  `| ${headers.map((_, i) => i ? "---:" : "---").join(" | ")} |`,
  ...lines.map(line => `| ${line.join(" | ")} |`),
].join("\n");
const matrixTable = (normalized, start) => {
  const targets = keys.slice(start, start + 7);
  return table(["Source / target", ...ids.slice(start, start + 7)], keys.map((source, i) => [
    `${ids[i]} ${names[source]}`,
    ...targets.map(target => {
      const c = cell(source, target);
      let text = normalized ? pct(c.target_retention_pct) : fmt(c.map50_95);
      if (!normalized && source === target) text = `**${text}**`;
      return text;
    }),
  ]));
};
const sections = [
  "# YOLO11m transfer matrix: reproducible tables",
  "Generated by `node build_matrix.mjs`. Rows are sources; columns are targets.",
  "Percentages use x100. N/A is excluded, never imputed as zero. Diagonals are excluded from all OOD means.",
  "Unified frozen views (39 re-evaluation runs in `TargetUnifyTests`, 2026-09-18): the Cows2021 column uses its `test` split (2131 images); the Google OI column uses the leakage-revised view (576); the COCO column uses the leakage-revised view (342). The Cows2021 diagonal, COCO->Google OI and Google OI->COCO are reused from earlier same-view runs. All other columns come from the original suite unchanged.",
  "All ordinary target val views were checked for resolved-image-path and label-content agreement on 2026-09-18. Historical content immutability cannot be proved by this current-state check.",
  "Positive values below display precision use scientific notation. Unrounded values and source hashes are in calculated_results.json.",
  "## Absolute matrix, targets 01-07", matrixTable(false, 0),
  "## Absolute matrix, targets 08-14", matrixTable(false, 7),
  "## Target-normalized retention, targets 01-07", matrixTable(true, 0),
  "## Target-normalized retention, targets 08-14", matrixTable(true, 7),
  "## Off-diagonal target column means",
  table(["Target", "OOD images", "ID mAP", "OOD column mean", "Target retention", "Valid n/13"],
    columns.map(c => [names[c.target], c.ood_images.join("/"), fmt(c.id_map50_95), fmt(c.mean_ood_map50_95), pct(c.mean_target_retention_pct), `${c.valid_target_retention_n}/13`])),
  "Every target column now uses one frozen view for all 13 incoming sources and its own diagonal; 182/182 OOD cells have same-view target ID denominators.",
  "## Representative directed pairs",
  table(["s / t", "s -> t", "t -> s", "Asym", "R_target(s,t)", "R_target(t,s)"],
    pairs.map(p => [`${names[p.source]} / ${names[p.target]}`, fmt(p.forward), fmt(p.reverse), `${p.asym >= 0 ? "+" : ""}${fmt(p.asym)}`, pct(p.forward_target_retention_pct), pct(p.reverse_target_retention_pct)])),
  "## Source row means",
  table(["Source", "ID mAP", "OOD mean", "Source retention", "OOD median", "Worst OOD"],
    [...rows].sort((a, b) => b.mean_ood_map50_95 - a.mean_ood_map50_95).map(r => [names[r.source], fmt(r.id_map50_95), fmt(r.mean_ood_map50_95), `${r.mean_source_retention_pct.toFixed(4)}%`, fmt(r.median_ood_map50_95), fmt(r.worst_map50_95)])),
  "## Source files",
  ...provenance.map(p => `- [${p.source}](${p.file}): \`${p.remote}\`; SHA-256 \`${p.sha256}\`.`),
];
await writeFile(new URL("calculated_results.json", import.meta.url), JSON.stringify(result, null, 2) + "\n");
await writeFile(new URL("calculated_tables.md", import.meta.url), sections.join("\n\n") + "\n");
console.log(JSON.stringify({ cells: cells.length, valid_ood_retention: 182, overall: result.overall, output: fileURLToPath(new URL("calculated_tables.md", import.meta.url)) }, null, 2));
