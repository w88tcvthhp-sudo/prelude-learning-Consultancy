// Renders the five Prelude PDF resources from their HTML sources.
//
//   node resources-src/build-resources.mjs
//
// Requires Node 18+ and Playwright with Chromium (npm i -D playwright && npx playwright install chromium).
// Chromium's print engine produces tagged PDFs (logical structure, selectable text) and
// bookmarks from the heading outline. Output goes to assets/resources/.
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';
import fs from 'node:fs';

let chromium;
try { ({ chromium } = await import('playwright')); }
catch { ({ chromium } = await import(process.env.PLAYWRIGHT_MODULE || '/opt/npm-tools/node_modules/playwright/index.mjs')); }

const here = path.dirname(fileURLToPath(import.meta.url));
const out = path.resolve(here, '..', 'assets', 'resources');
fs.mkdirSync(out, { recursive: true });

export const DOCS = [
  ['capability-readiness-playbook.html', 'prelude-capability-readiness-playbook.pdf'],
  ['capability-readiness-review-workbook.html', 'prelude-capability-readiness-review-workbook.pdf'],
  ['defence-tna-checklist.html', 'prelude-defence-tna-checklist.pdf'],
  ['learning-governance-health-check.html', 'prelude-learning-governance-health-check.pdf'],
  ['workforce-capability-assessment.html', 'prelude-workforce-capability-assessment.pdf'],
];

const only = process.argv.slice(2);
const browser = await chromium.launch();
const page = await browser.newPage();
for (const [src, pdf] of DOCS) {
  if (only.length && !only.some(o => src.includes(o))) continue;
  await page.goto(pathToFileURL(path.join(here, src)).href, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({
    path: path.join(out, pdf), printBackground: true, preferCSSPageSize: true,
    tagged: true, outline: true,
  });
  console.log('wrote assets/resources/' + pdf);
}
await browser.close();
