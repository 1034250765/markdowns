const { chromium } = require("C:/Users/LYX10/.workbuddy/plugins/cache/experts/ppt-implement/1.0.13/skills/ppt-implement/scripts/export/node_modules/playwright");
const fs = require("fs");
const path = require("path");

const OUT = "C:/Users/LYX10/Downloads/Typora/论文精读/fusion_or_confusion_ppt/frontend/public/assets/images/posters/pages";

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe" });
  const page = await browser.newPage({ viewport: { width: 1440, height: 810 }, deviceScaleFactor: 1.5 });
  const total = 26;
  for (let i = 1; i <= total; i++) {
    await page.goto(`http://127.0.0.1:5173/?page=${i}`, { waitUntil: "networkidle" });
    await page.addStyleTag({ content: ".slide > div { transform: none !important; } .nav-btn, .progress-bar, .page-indicator { display: none !important; }" });
    await page.waitForTimeout(700);
    const slide = await page.$(".slide.active > div");
    if (!slide) { console.log(`page ${i}: no active slide`); continue; }
    const file = path.join(OUT, `page-${i}.png`);
    await slide.screenshot({ path: file });
    console.log(`saved ${file}`);
  }
  await browser.close();
})();
