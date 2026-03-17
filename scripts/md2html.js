import { readFileSync, writeFileSync } from 'fs';
import { marked } from 'marked';
import puppeteer from 'puppeteer';

// Get markdown file path from command line arguments
const mdFile = process.argv[2];
const cssFile = process.argv[3];
const height = parseInt(process.argv[4]) || 2000; // Default height is 2000

if (!mdFile) {
    console.error('Please provide a markdown file path as argument');
    process.exit(1);
}
const pngFile = mdFile.replace(/\.md$/, '.png');

const md = readFileSync(mdFile, 'utf-8');
const html = marked.parse(md);
const css = readFileSync(cssFile, 'utf-8');
const fullHtml = `<!DOCTYPE html><html><head><style>${css}</style></head><body>${html}</body></html>`;
const htmlFile = mdFile.replace(/\.md$/, '.html');
writeFileSync(htmlFile, fullHtml);
console.log(`Generated HTML: ${htmlFile}`);

puppeteer.launch().then(async (browser) => {
    const page = await browser.newPage();
    await page.setViewport({ width: 1000, height: height });
    await page.setContent(fullHtml);
    await page.screenshot({ path: pngFile });
    await browser.close();
    console.log(`Generated PNG: ${pngFile}`);
}).catch(err => {
    console.error('❌ Failed to render PNG:', err);
    process.exit(1);
});