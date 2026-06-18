const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ deviceScaleFactor: 2 });
  const page = await context.newPage();

  const filePath = 'file:///d:/cc.claude/ADHD/Report_GlassFactory_USA_v4.html';
  await page.goto(filePath, { waitUntil: 'networkidle', timeout: 30000 });

  await page.waitForFunction(() => {
    const canvases = document.querySelectorAll('canvas');
    if (canvases.length === 0) return false;
    return Array.from(canvases).every(c => c.width > 100 && c.height > 100);
  }, { timeout: 15000 });

  await page.waitForTimeout(3000);

  await page.pdf({
    path: 'd:/cc.claude/ADHD/Report_GlassFactory_USA_v4.pdf',
    width: '360mm',
    height: '203mm',
    margin: { top: '14mm', bottom: '14mm', left: '16mm', right: '16mm' },
    printBackground: true,
    displayHeaderFooter: false,
    preferCSSPageSize: true,
    scale: 1,
  });

  console.log('PDF generated (16:9 landscape): Report_GlassFactory_USA_v4.pdf');
  await browser.close();
})();
