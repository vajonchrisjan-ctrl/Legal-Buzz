#!/bin/bash
cd /tmp/claude-0/-home-user-Legal-Buzz/f7bb2d48-6446-56fa-85f1-2b4044611aea/scratchpad
python3 -I scripts/assemble.py >/dev/null && node scripts/render-pdf.js "$PWD/proposal/proposal.html" "$PWD/proposal/draft.pdf" >/dev/null
echo "pages: $(pdfinfo proposal/draft.pdf | awk '/Pages/{print $2}')"
rm -rf proposal/png && mkdir proposal/png && pdftoppm -r 40 -png proposal/draft.pdf proposal/png/p >/dev/null 2>&1
python3 -I - <<'PY'
import glob
from PIL import Image
import numpy as np
for f in sorted(glob.glob('proposal/png/p-*.png')):
    im=np.array(Image.open(f).convert('L')); h=im.shape[0]
    rows=np.where(((im[:int(h*0.925)]<245).sum(axis=1)>2))[0]
    pct=rows.max()/h*100 if len(rows) else 0
    print(f"p{f.split('-')[-1][:2]} {pct:5.1f}%{'   <-- STRANDED' if pct<32 and not f.endswith('01.png') else ''}")
PY
