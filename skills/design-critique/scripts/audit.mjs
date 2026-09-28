#!/usr/bin/env node
/**
 * Capture and measure a web page for design critique.
 *
 * Usage:
 *   node audit.mjs <url-or-html-file> [outdir] [--widths 375,768,1440] [--no-axe]
 *
 * Writes to outdir (default ./audit):
 *   {mobile,tablet,desktop}-fold.png   first-impression screenshots (viewport only)
 *   {mobile,tablet,desktop}-full.png   full-page screenshots
 *   desktop-dark-fold.png              prefers-color-scheme: dark
 *   report.json                        everything below (also printed to stdout)
 *
 * Per width: horizontal overflow, font sizes / families / text colors in use, off-4px-grid
 * spacing, tap targets under 24px, text failing WCAG contrast (against the nearest solid
 * background; text over images is listed separately for a manual check).
 * Once: axe-core violations (local `axe-core` package, else CDN), images without alt,
 * lazy-loaded images in the first viewport (LCP risk), heading outline problems, unlabeled
 * form controls, missing lang / viewport meta, animation without a prefers-reduced-motion rule.
 *
 * Needs Playwright: `npm i -D playwright && npx playwright install chromium`
 * (a global install also works). Optional: `npm i -D axe-core` for offline accessibility checks.
 */

import { execSync } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const globalRequire = (() => {
  try {
    const root = execSync('npm root -g', { stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim();
    return createRequire(path.join(root, 'noop.js'));
  } catch {
    return null;
  }
})();
const localRequire = createRequire(path.join(process.cwd(), 'noop.js'));

function load(name) {
  for (const req of [localRequire, globalRequire]) {
    try {
      if (req) return req(name);
    } catch {}
  }
  return null;
}

const NAMES = { 375: 'mobile', 390: 'mobile', 768: 'tablet', 1024: 'tablet', 1280: 'desktop', 1440: 'desktop' };

function parseArgs(argv) {
  const args = { widths: [375, 768, 1440], axe: true, positional: [] };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--widths') args.widths = argv[++i].split(',').map(Number).filter(Boolean);
    else if (argv[i] === '--no-axe') args.axe = false;
    else if (argv[i] === '-h' || argv[i] === '--help') args.help = true;
    else args.positional.push(argv[i]);
  }
  [args.target, args.out = 'audit'] = args.positional;
  return args;
}

/* Runs inside the page. Keep it self-contained. */
function measure() {
  const visible = [...document.querySelectorAll('body, body *')].filter((e) => e.getClientRects().length);
  const cs = (e) => getComputedStyle(e);
  const hasText = (e) => [...e.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
  const count = (f) => visible.reduce((m, e) => { const v = f(e); if (v) m[v] = (m[v] || 0) + 1; return m; }, {});

  const parse = (c) => {
    const m = c.match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const [r, g, b, a = 1] = m[1].split(/[\s,/]+/).filter(Boolean).map(Number);
    return { r, g, b, a };
  };
  const lum = ({ r, g, b }) => {
    const f = (v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  };
  const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
  const blend = (top, bottom) => ({
    r: top.r * top.a + bottom.r * (1 - top.a),
    g: top.g * top.a + bottom.g * (1 - top.a),
    b: top.b * top.a + bottom.b * (1 - top.a),
    a: 1,
  });
  const background = (el) => {
    const layers = [];
    for (let e = el; e; e = e.parentElement) {
      const s = cs(e);
      if (s.backgroundImage !== 'none') return { overImage: true };
      const c = parse(s.backgroundColor);
      if (c && c.a > 0) { layers.push(c); if (c.a >= 1) break; }
    }
    let base = { r: 255, g: 255, b: 255, a: 1 };
    for (const layer of layers.reverse()) base = blend(layer, base);
    return { color: base };
  };

  const contrastFailures = [];
  const textOverImages = [];
  for (const e of visible) {
    if (!hasText(e)) continue;
    const s = cs(e);
    if (s.visibility === 'hidden' || Number(s.opacity) === 0) continue;
    const fg = parse(s.color);
    if (!fg) continue;
    const bg = background(e);
    const text = e.textContent.trim().replace(/\s+/g, ' ').slice(0, 40);
    if (bg.overImage) { if (textOverImages.length < 10) textOverImages.push(text); continue; }
    const size = parseFloat(s.fontSize);
    const large = size >= 24 || (size >= 18.66 && Number(s.fontWeight) >= 700);
    const r = ratio(blend(fg, bg.color), bg.color);
    const required = large ? 3 : 4.5;
    if (r < required && contrastFailures.length < 20) {
      contrastFailures.push({ text, ratio: Math.round(r * 100) / 100, required, color: s.color, fontSize: s.fontSize });
    }
  }

  return {
    horizontalOverflow: document.documentElement.scrollWidth > innerWidth,
    fontSizes: count((e) => hasText(e) && cs(e).fontSize),
    fontFamilies: count((e) => hasText(e) && cs(e).fontFamily.split(',')[0].trim()),
    textColors: count((e) => hasText(e) && cs(e).color),
    offGridSpacing: count((e) => {
      const v = ['marginTop', 'marginBottom', 'paddingTop', 'paddingLeft', 'rowGap', 'columnGap']
        .map((p) => parseFloat(cs(e)[p])).find((n) => n > 2 && n % 4);
      return v && `${v}px`;
    }),
    smallTargets: [...document.querySelectorAll('a, button, input, select, textarea, [role=button]')]
      .map((e) => [e, e.getBoundingClientRect()])
      .filter(([, r]) => r.width && (r.width < 24 || r.height < 24))
      .slice(0, 10)
      .map(([e, r]) => `${e.tagName.toLowerCase()} "${(e.innerText || e.getAttribute('aria-label') || '').trim().slice(0, 30)}" ${Math.round(r.width)}x${Math.round(r.height)}`),
    contrastFailures,
    textOverImages,
  };
}

/* Runs inside the page once, at desktop width. */
function structure() {
  const headings = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map((h) => Number(h.tagName[1]));
  const skipped = headings.filter((lvl, i) => i > 0 && lvl > headings[i - 1] + 1).length;
  const controls = [...document.querySelectorAll('input:not([type=hidden]):not([type=submit]):not([type=button]), select, textarea')];
  const unlabeled = controls.filter((c) => !(c.labels && c.labels.length) && !c.getAttribute('aria-label') && !c.getAttribute('aria-labelledby'));
  const lazyAboveFold = [...document.querySelectorAll('img[loading=lazy]')]
    .filter((img) => img.getBoundingClientRect().top < innerHeight).map((img) => img.currentSrc || img.src);

  let hasAnimation = false;
  let hasReducedMotionRule = false;
  for (const sheet of document.styleSheets) {
    let rules;
    try { rules = sheet.cssRules; } catch { continue; }
    const walk = (list) => {
      for (const rule of list) {
        if (/prefers-reduced-motion/.test(rule.conditionText || rule.media?.mediaText || '')) hasReducedMotionRule = true;
        const st = rule.style;
        if (st) {
          const moving = (d) => (d || '').split(',').some((v) => parseFloat(v) > 0);
          if ((st.animationName && st.animationName !== 'none') || moving(st.transitionDuration) || moving(st.animationDuration)) hasAnimation = true;
        }
        if (rule.cssRules) walk(rule.cssRules);
      }
    };
    walk(rules);
  }

  return {
    lang: document.documentElement.getAttribute('lang') || null,
    viewportMeta: !!document.querySelector('meta[name=viewport]'),
    title: document.title || null,
    h1Count: headings.filter((l) => l === 1).length,
    skippedHeadingLevels: skipped,
    imagesMissingAlt: [...document.querySelectorAll('img:not([alt])')].map((i) => i.currentSrc || i.src).slice(0, 10),
    unlabeledControls: unlabeled.map((c) => c.outerHTML.slice(0, 80)).slice(0, 10),
    lazyImagesAboveFold: lazyAboveFold,
    animationWithoutReducedMotion: hasAnimation && !hasReducedMotionRule,
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || !args.target) {
    console.log('Usage: node audit.mjs <url-or-html-file> [outdir] [--widths 375,768,1440] [--no-axe]');
    process.exit(args.help ? 0 : 2);
  }
  const pw = load('playwright') || (await import('playwright').catch(() => null));
  if (!pw) {
    console.error('Error: Playwright not found. Run: npm i -D playwright && npx playwright install chromium');
    process.exit(1);
  }
  const url = /^https?:\/\//.test(args.target) ? args.target : pathToFileURL(path.resolve(args.target)).href;
  mkdirSync(args.out, { recursive: true });

  const browser = await pw.chromium.launch();
  const report = { target: args.target, widths: {} };
  const widest = Math.max(...args.widths);
  try {
    for (const width of args.widths) {
      const name = NAMES[width] || `w${width}`;
      const height = width < 600 ? 812 : width < 1100 ? 1024 : 900;
      const page = await browser.newPage({ viewport: { width, height } });
      await page.goto(url, { waitUntil: 'networkidle' });
      await page.evaluate(() => document.fonts && document.fonts.ready);
      await page.screenshot({ path: path.join(args.out, `${name}-fold.png`) });
      await page.screenshot({ path: path.join(args.out, `${name}-full.png`), fullPage: true });
      report.widths[name] = { width, ...(await page.evaluate(measure)) };

      if (width === widest) {
        report.structure = await page.evaluate(structure);
        await page.emulateMedia({ colorScheme: 'dark' });
        await page.screenshot({ path: path.join(args.out, `${name}-dark-fold.png`) });
        report.darkMode = { contrastFailures: (await page.evaluate(measure)).contrastFailures };
        await page.emulateMedia({ colorScheme: 'light' });

        if (args.axe) {
          try {
            const axe = load('axe-core');
            await page.addScriptTag(axe ? { content: axe.source } : { url: 'https://cdn.jsdelivr.net/npm/axe-core@4/axe.min.js' });
            report.axe = await page.evaluate(async () => (await window.axe.run()).violations.map((v) => ({
              id: v.id, impact: v.impact, help: v.help, count: v.nodes.length, first: v.nodes[0]?.target.join(' '),
            })));
          } catch (e) {
            report.axe = `axe-core unavailable (offline? try npm i -D axe-core): ${e.message.split('\n')[0]}`;
          }
        }
      }
      await page.close();
    }
  } finally {
    await browser.close();
  }

  const json = JSON.stringify(report, null, 1);
  writeFileSync(path.join(args.out, 'report.json'), json);
  console.log(json);
}

main().catch((e) => {
  console.error(`Error: ${e.message}`);
  process.exit(1);
});
