#!/usr/bin/env node
/**
 * Render HTML to PNG/PDF with headless Chromium (Playwright).
 *
 * Usage:
 *   # Exact-size graphic (social post, ad, thumbnail, text overlay): PNG is exactly WxH (x scale)
 *   node render.mjs post.html --size 1080x1080 --out post.png
 *   node render.mjs ad.html --size 300x250 --scale 2 --out ad@2x.png
 *
 *   # Responsive page at several widths (full-page screenshots: shot-390.png, shot-1440.png)
 *   node render.mjs index.html --widths 390,1440 --out shots/shot.png
 *
 *   # Light and dark themes (prefers-color-scheme), one element only, or a PDF
 *   node render.mjs index.html --widths 1440 --theme both --out shots/page.png
 *   node render.mjs card.html --selector .card --out card.png
 *   node render.mjs poster.html --size 1800x2400 --pdf --out poster.pdf
 *
 * Accepts a local file path or an http(s) URL. Waits for web fonts before capturing and warns
 * when content overflows the canvas (clipped text is the most common export bug).
 *
 * Needs Playwright: `npm i -D playwright && npx playwright install chromium`
 * (a global install also works).
 */

import { execSync } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import { createRequire } from 'node:module';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

async function loadPlaywright() {
  try {
    return await import('playwright');
  } catch {}
  try {
    const globalRoot = execSync('npm root -g', { stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim();
    return createRequire(path.join(globalRoot, 'noop.js'))('playwright');
  } catch {}
  console.error('Error: Playwright not found. Run: npm i -D playwright && npx playwright install chromium');
  process.exit(1);
}

function parseArgs(argv) {
  const args = { widths: [], height: 900, scale: 1, theme: 'light', out: 'render.png' };
  const rest = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const next = () => {
      if (i + 1 >= argv.length) throw new Error(`${a} needs a value`);
      return argv[++i];
    };
    if (a === '--size') {
      const [w, h] = next().toLowerCase().split('x').map(Number);
      if (!w || !h) throw new Error('--size must look like 1080x1080');
      args.size = { width: w, height: h };
    } else if (a === '--widths') args.widths = next().split(',').map(Number).filter(Boolean);
    else if (a === '--height') args.height = Number(next());
    else if (a === '--scale') args.scale = Number(next());
    else if (a === '--theme') args.theme = next();
    else if (a === '--selector') args.selector = next();
    else if (a === '--out') args.out = next();
    else if (a === '--pdf') args.pdf = true;
    else if (a === '--full-page') args.fullPage = true;
    else if (a === '-h' || a === '--help') args.help = true;
    else if (a.startsWith('--')) throw new Error(`unknown option ${a}`);
    else rest.push(a);
  }
  args.target = rest[0];
  if (!['light', 'dark', 'both'].includes(args.theme)) throw new Error('--theme must be light, dark, or both');
  return args;
}

function toUrl(target) {
  return /^https?:\/\//.test(target) ? target : pathToFileURL(path.resolve(target)).href;
}

function outputPath(base, { width, theme, multiWidth, multiTheme }) {
  const ext = path.extname(base) || '.png';
  let stem = base.slice(0, base.length - path.extname(base).length);
  if (multiWidth) stem += `-${width}`;
  if (multiTheme) stem += `-${theme}`;
  return stem + ext;
}

async function capture(browser, url, opts) {
  const { width, height, theme, scale, selector, fullPage, pdf, exact, out } = opts;
  const context = await browser.newContext({
    viewport: { width, height },
    deviceScaleFactor: scale,
    colorScheme: theme,
  });
  const page = await context.newPage();
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts && document.fonts.ready);

  const metrics = await page.evaluate(() => ({
    scrollWidth: document.documentElement.scrollWidth,
    scrollHeight: document.documentElement.scrollHeight,
    fallbackFonts: [...document.fonts].filter((f) => f.status === 'error').map((f) => f.family),
  }));
  const warnings = [];
  if (metrics.scrollWidth > width) warnings.push(`content is ${metrics.scrollWidth}px wide, wider than the ${width}px viewport`);
  if (exact && metrics.scrollHeight > height) warnings.push(`content is ${metrics.scrollHeight}px tall and will be clipped at ${height}px`);
  if (metrics.fallbackFonts.length) warnings.push(`web fonts failed to load: ${[...new Set(metrics.fallbackFonts)].join(', ')}`);

  mkdirSync(path.dirname(path.resolve(out)), { recursive: true });
  if (pdf) {
    await page.pdf({ path: out, width: `${width}px`, height: `${height}px`, printBackground: true, pageRanges: exact ? '1' : undefined });
  } else if (selector) {
    const el = page.locator(selector).first();
    if (!(await el.count())) throw new Error(`selector ${selector} matched nothing`);
    await el.screenshot({ path: out });
  } else {
    await page.screenshot({ path: out, fullPage: exact ? false : fullPage !== false });
  }
  await context.close();
  return { out, warnings };
}

async function main() {
  let args;
  try {
    args = parseArgs(process.argv.slice(2));
  } catch (e) {
    console.error(`Error: ${e.message}`);
    process.exit(2);
  }
  if (args.help || !args.target) {
    console.log('Usage: node render.mjs <file.html|url> [--size WxH | --widths 390,1440] [--height 900] ' +
      '[--scale 2] [--theme light|dark|both] [--selector CSS] [--pdf] [--out out.png]');
    process.exit(args.help ? 0 : 2);
  }

  const { chromium } = await loadPlaywright();
  const browser = await chromium.launch();
  const url = toUrl(args.target);
  const themes = args.theme === 'both' ? ['light', 'dark'] : [args.theme];
  const shots = args.size
    ? [{ width: args.size.width, height: args.size.height, exact: true }]
    : (args.widths.length ? args.widths : [1440]).map((w) => ({ width: w, height: args.height, exact: false }));

  let warned = false;
  try {
    for (const shot of shots) {
      for (const theme of themes) {
        const out = outputPath(args.out, {
          width: shot.width, theme, multiWidth: shots.length > 1, multiTheme: themes.length > 1,
        });
        const result = await capture(browser, url, {
          ...shot, theme, scale: args.scale, selector: args.selector,
          fullPage: args.fullPage || !shot.exact, pdf: args.pdf, out,
        });
        console.log(`Saved: ${result.out}`);
        for (const w of result.warnings) {
          warned = true;
          console.warn(`  warning: ${w}`);
        }
      }
    }
  } finally {
    await browser.close();
  }
  process.exit(warned ? 3 : 0);
}

main().catch((e) => {
  console.error(`Error: ${e.message}`);
  process.exit(1);
});
