// Print a guide's HTML to PDF with Chromium. Usage: node guides/pdf.cjs book.html out.pdf A4|Letter
const { chromium } = require('playwright');
const { pathToFileURL } = require('url');
(async () => {
  const [, , html, pdf, format] = process.argv;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(pathToFileURL(html).href, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.emulateMedia({ media: 'print' });
  await page.addStyleTag({ content: `@page { size: ${format === 'Letter' ? 'letter' : 'A4'}; }` });
  await page.pdf({ path: pdf, format, printBackground: true, preferCSSPageSize: true });
  await browser.close();
})();
