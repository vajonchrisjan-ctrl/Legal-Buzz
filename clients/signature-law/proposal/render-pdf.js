const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + process.argv[2], { waitUntil: 'networkidle' });
  const fonts = await p.evaluate(async () => {
    await document.fonts.ready;
    const c = document.createElement('canvas').getContext('2d');
    const w = f => { c.font = '40px ' + f; return c.measureText('Signature Law Growth').width; };
    return { outfit: w("'Outfit'"), dmsans: w("'DM Sans'"), fallback: w('serif'),
             loaded: [...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family+':'+f.weight) };
  });
  console.log('FONT CHECK', JSON.stringify(fonts));
  await p.pdf({ path: process.argv[3], preferCSSPageSize: true, printBackground: true });
  await b.close();
})();
