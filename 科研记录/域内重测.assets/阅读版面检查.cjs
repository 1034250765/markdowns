const fs = require("node:fs");
const path = require("node:path");
const {pathToFileURL} = require("node:url");
const {chromium} = require("C:/Users/LYX10/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright");

(async () => {
  const browser = await chromium.launch({
    executablePath: "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
    headless: true,
  });
  try {
    const page = await browser.newPage({viewport: {width: 1280, height: 1700}, deviceScaleFactor: 1});
    await page.goto(pathToFileURL(path.join(__dirname, "阅读预览.html")).href, {waitUntil: "load"});
    const data = await page.evaluate(() => ({
      documentWidth: document.documentElement.scrollWidth,
      viewportWidth: window.innerWidth,
      imageCount: document.images.length,
      failedImages: [...document.images].filter(im => !im.complete || !im.naturalWidth).map(im => im.src),
      mathCount: document.querySelectorAll("math").length,
      mainHeight: Math.round(document.querySelector("main").getBoundingClientRect().height),
      headings: [...document.querySelectorAll("h2")].map(el=>el.textContent),
    }));
    if (data.failedImages.length || data.imageCount !== 15 || data.documentWidth > data.viewportWidth) {
      throw new Error(JSON.stringify(data));
    }
    await page.screenshot({path: path.join(__dirname, "阅读预览-封面.png")});
    await page.locator("h2").filter({hasText: "2. 实验原理"}).evaluate(el => window.scrollTo(0, el.getBoundingClientRect().top+window.scrollY-30));
    await page.screenshot({path: path.join(__dirname, "阅读预览-公式.png")});
    await page.locator("h2").filter({hasText: "5. 原始记录"}).evaluate(el => window.scrollTo(0, el.getBoundingClientRect().top+window.scrollY-30));
    await page.screenshot({path: path.join(__dirname, "阅读预览-主结果.png")});
    data.status = "passed";
    fs.writeFileSync(path.join(__dirname, "阅读版面核验.json"), JSON.stringify(data, null, 2), "utf8");
    console.log(JSON.stringify(data, null, 2));
  } finally {
    await browser.close();
  }
})().catch(e => { console.error(e); process.exitCode = 1; });
