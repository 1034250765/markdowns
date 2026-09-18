import { readFile } from "node:fs/promises";

const data = JSON.parse((await readFile(new URL("calculated_results.json", import.meta.url))).toString("utf8"));
const cells = data.cells;

const GROUPS = {
  G1: ["8-calves", "COLO", "Cows2021", "diarycow", "MooTrack360", "XGain"],
  G2: ["CID", "HCRD", "NWAFU_CD"],
  G3: ["animals_10", "CBPD_ODD", "CImage", "COCO", "Google_Open_Images"],
};
const mean = a => a.reduce((x, y) => x + y, 0) / a.length;

const groupCell = (gs, gt, exclude = []) => {
  const pairs = [];
  for (const s of GROUPS[gs]) {
    for (const t of GROUPS[gt]) {
      if (s === t || exclude.includes(s) || exclude.includes(t)) continue;
      const c = cells.find(c => c.source === s && c.target === t);
      pairs.push(c);
    }
  }
  return {
    n: pairs.length,
    map: mean(pairs.map(c => c.map50_95)),
    sourceRetention: mean(pairs.map(c => c.source_retention_pct)),
    targetRetention: mean(pairs.map(c => c.target_retention_pct)),
  };
};

console.log("== full 3x3 (source-normalized retention) ==");
for (const gs of ["G1", "G2", "G3"]) {
  const row = ["G1", "G2", "G3"].map(gt => {
    const c = groupCell(gs, gt);
    return `${c.map.toFixed(4)} / ${c.sourceRetention.toFixed(2)}% (n=${c.n})`;
  });
  console.log(gs, "|", row.join(" | "));
}

console.log("\n== CBPD_ODD excluded from both sides ==");
for (const gs of ["G1", "G2", "G3"]) {
  const row = ["G1", "G2", "G3"].map(gt => {
    const c = groupCell(gs, gt, ["CBPD_ODD"]);
    return `${c.map.toFixed(4)} / ${c.sourceRetention.toFixed(2)}% (n=${c.n})`;
  });
  console.log(gs, "|", row.join(" | "));
}

console.log("\n== full 3x3 (target-normalized retention, reference) ==");
for (const gs of ["G1", "G2", "G3"]) {
  const row = ["G1", "G2", "G3"].map(gt => {
    const c = groupCell(gs, gt);
    return `${c.map.toFixed(4)} / ${c.targetRetention.toFixed(2)}%`;
  });
  console.log(gs, "|", row.join(" | "));
}
