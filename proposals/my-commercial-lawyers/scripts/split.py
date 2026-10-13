# Crop one tall PDF page into equal page-sized sheets (no browser fragmentation).
import sys, copy
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject
src, n, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
r = PdfReader(src); pg = r.pages[0]
W = float(pg.mediabox.width); T = float(pg.mediabox.height); ph = W * 1810 / 1280  # one 1280x1810px page, in points
w = PdfWriter()
for i in range(n):
    p = w.add_page(pg)
    top = T - i * ph
    box = RectangleObject([0, top - ph, W, top])
    p.mediabox = box; p.cropbox = box; p.trimbox = box
w.add_metadata({'/Title': 'Growth proposal for My Commercial Lawyers | legalbuzz', '/Author': 'legalbuzz'})
w.compress_identical_objects()
w.write(out)
print('pages', n, 'page size', W, ph, 'pages in tall pdf', len(r.pages))
