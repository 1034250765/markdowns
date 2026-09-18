import { readFile } from "node:fs/promises";

const draft = (await readFile(new URL("../文章初稿.md", import.meta.url))).toString("utf8");
const data = JSON.parse((await readFile(new URL("calculated_results.json", import.meta.url))).toString("utf8"));
const lines = draft.split(/\r?\n/);

const fmt = x => (x > 0 && x < 0.00005 ? x.toExponential(1) : x.toFixed(4));
const pct2 = x => (x > 0 && x < 0.005 ? `${x.toExponential(1)}%` : `${x.toFixed(2)}%`);
const cellOf = (s, t) => data.cells.find(c => c.source === s && c.target === t);

let bad = 0;
const fail = msg => { bad += 1; console.log("MISMATCH:", msg); };

// --- matrix tables ---
const order = data.order;
const draftMatrix = {};
let currentColumns = [];
for (const line of lines) {
  const header = line.match(/^\|\s*源数据集 \/ 目标编号\s*\|(.+)\|\s*$/);
  if (header) {
    currentColumns = header[1].split("|").map(x => x.trim());
    continue;
  }
  const row = line.match(/^\|\s*(\d{2}) ([^|]+?)\s*\|(.+)\|\s*$/);
  if (row && currentColumns.length) {
    const sourceIndex = Number(row[1]) - 1;
    const values = row[3].split("|").map(x => x.trim());
    if (values.length !== currentColumns.length) continue;
    values.forEach((value, i) => {
      const targetKey = order[Number(currentColumns[i]) - 1];
      draftMatrix[`${sourceIndex}|${targetKey}`] = value.replace(/\*\*/g, "");
    });
  }
}
for (let si = 0; si < order.length; si += 1) {
  for (const target of order) {
    const key = `${si}|${target}`;
    if (!(key in draftMatrix)) { fail(`missing matrix cell ${order[si]} -> ${target}`); continue; }
    const expected = fmt(cellOf(order[si], target).map50_95);
    if (draftMatrix[key] !== expected) fail(`matrix ${order[si]} -> ${target}: draft=${draftMatrix[key]} expected=${expected}`);
  }
}
console.log(`matrix cells checked: ${Object.keys(draftMatrix).length}`);

// --- row means table ---
const nameOf = Object.fromEntries(data.order.map(k => [k, data.rows.find(r => r.source === k) ? null : null]));
const sourceByDisplay = {
  "CImage": "CImage", "Google Open Images": "Google_Open_Images", "COCO cow subset": "COCO",
  "animals_10": "animals_10", "NWAFU Cattle Dataset": "NWAFU_CD", "Dairy Cow": "diarycow",
  "COLO": "COLO", "CBPD_ODD": "CBPD_ODD", "MooTrack360": "MooTrack360", "8-calves": "8-calves",
  "CID": "CID", "XGain": "XGain", "HCRD": "HCRD", "Cows2021": "Cows2021",
};
let roww = 0;
for (const row of data.rows) {
  const display = Object.entries(sourceByDisplay).find(([, key]) => key === row.source)[0];
  const line = lines.find(l => l.startsWith(`| ${display} `) && l.includes("|") && l.split("|").length === 6 && /\d\.\d{4}/.test(l));
  if (!line) { fail(`row-means row not found: ${display}`); continue; }
  const parts = line.split("|").map(x => x.trim());
  if (parts[2] !== fmt(row.id_map50_95)) fail(`row ${display} ID: draft=${parts[2]} expected=${fmt(row.id_map50_95)}`);
  if (parts[3] !== fmt(row.mean_ood_map50_95)) fail(`row ${display} OOD mean: draft=${parts[3]} expected=${fmt(row.mean_ood_map50_95)}`);
  if (parts[4] !== `${row.mean_source_retention_pct.toFixed(4)}%`) fail(`row ${display} retention: draft=${parts[4]} expected=${row.mean_source_retention_pct.toFixed(4)}%`);
  roww += 1;
}
console.log(`row-means rows checked: ${roww}`);

// --- column means table ---
let colw = 0;
for (const col of data.columns) {
  const display = Object.entries(sourceByDisplay).find(([, key]) => key === col.target)[0];
  const line = lines.find(l => l.startsWith(`| ${display} |`) && (l.includes("13/13") || l.includes("/13")));
  if (!line) { fail(`column-means row not found: ${display}`); continue; }
  const parts = line.split("|").map(x => x.trim());
  if (parts[3] !== fmt(col.mean_ood_map50_95)) fail(`column ${display} mean: draft=${parts[3]} expected=${fmt(col.mean_ood_map50_95)}`);
  if (parts[4] !== pct2(col.mean_target_retention_pct)) fail(`column ${display} retention: draft=${parts[4]} expected=${pct2(col.mean_target_retention_pct)}`);
  if (parts[5] !== `${col.valid_target_retention_n}/13`) fail(`column ${display} n: draft=${parts[5]}`);
  colw += 1;
}
console.log(`column-means rows checked: ${colw}`);

// --- group table ---
const GROUPS = {
  G1: ["8-calves", "COLO", "Cows2021", "diarycow", "MooTrack360", "XGain"],
  G2: ["CID", "HCRD", "NWAFU_CD"],
  G3: ["animals_10", "CBPD_ODD", "CImage", "COCO", "Google_Open_Images"],
};
const mean = a => a.reduce((x, y) => x + y, 0) / a.length;
const groupLabels = { G1: "G1 结构化监控", G2: "G2 受控/现场采集", G3: "G3 开放/混合来源" };
for (const gs of ["G1", "G2", "G3"]) {
  const line = lines.find(l => l.startsWith(`| ${groupLabels[gs]} |`) && l.split("|").length === 6);
  if (!line) { fail(`group row not found: ${gs}`); continue; }
  const parts = line.split("|").map(x => x.trim());
  ["G1", "G2", "G3"].forEach((gt, i) => {
    const pairs = [];
    for (const s of GROUPS[gs]) for (const t of GROUPS[gt]) if (s !== t) pairs.push(cellOf(s, t));
    const m = mean(pairs.map(c => c.map50_95));
    const ret = mean(pairs.map(c => c.source_retention_pct));
    const expected = `${m.toFixed(4)} / ${ret.toFixed(2)}%`;
    if (parts[i + 2] !== expected) fail(`group ${gs}->${gt}: draft=${parts[i + 2]} expected=${expected}`);
  });
}
console.log(bad === 0 ? "ALL CHECKS PASSED" : `${bad} mismatches`);
