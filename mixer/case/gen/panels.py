# Builds the two aluminium top pieces from boards.json (made by dump_boards.py with KiCad's python).
# Run: uv run --no-project --with ezdxf --with reportlab python panels.py
# Case coordinates in mm: x from the left outer face, y from the rear outer face (toward the player), as in STATUS.md.
import json, math, os
import ezdxf
from shapely.geometry import Polygon, Point, box
from shapely.ops import unary_union
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'out')
os.makedirs(OUT, exist_ok=True)
B = json.load(open(os.path.join(HERE, 'boards.json')))

W = 407.0
MIN_WEB = float(os.environ.get('MIN_WEB', 1.5))  # metal left between cuts and to the edge; cutters ask for ~1x thickness
# Board placement: (board, case x of the board's left edge, case y of its rear edge)
PLACE = [('mixer_strip', 6, 5), ('mixer_strip', 37, 5), ('mixer_strip', 68, 5), ('mixer_strip', 99, 5),
         ('mixer_stereo', 130, 5), ('mixer_stereo', 161, 5), ('mixer_master', 192, 5), ('controller', 256, 230)]
# Riser walls (printed, hung from the shelf): (x from, x to, rear face y, front face y).
# Rear face clears the jack bodies under the shelf (Fab extents + 0.3); the plate's rear edge is the front face.
#   mono: NCJ6 flange ends local 28.6, PVA2 bodies start 30.8 (their cut-outs become notches in the plate edge)
#   stereo: NJ5 J9 ends 34.1, 3.5 mm J10 cut starts 39.8;  master left: NJ3 J10 ends 64.2;  master right: NJ3 J8/J9 end 46.6, J11 cut starts 52.3
RISER = [(0, 129.5, 33.9, 35.5), (129.5, 191.5, 39.4, 41.4), (191.5, 223, 69.5, 71.5), (223, 253, 51.9, 53.9), (253, W, 178, 180)]
PLATE_FRONT = 327.0  # ribbon plugs start behind this; the printed armrest covers the rest

def outline(shelf_piece):
    if shelf_piece:  # from the rear face (y 0) to each riser's front face, so the shelf rests on the riser
        pts = [(0, 0), (W, 0)]
        for x0, x1, _, yf in reversed(RISER):
            pts += [(x1, yf), (x0, yf)]
    else:  # from each riser's front face to the front edge
        pts = []
        for x0, x1, _, yf in RISER:
            pts += [(x0, yf), (x1, yf)]
        pts += [(W, PLATE_FRONT), (0, PLATE_FRONT)]
    return pts

def inside(poly, x, y):
    return Polygon(poly).buffer(0.01).contains(Point(x, y))

# A cut is ('circle', x, y, d) or ('rect', x, y, w, h) or ('slot', x, y, w, len) (slot along y, round ends)
plate, shelf, labels = [], [], []  # labels: (x, y, text, piece)

def fab_circles(f):
    return [g for g in f['fab'] if g[0] == 'c']

def fab_box(f):
    bs = [g for g in f['fab'] if g[0] == 'b']
    return min(g[1] for g in bs), min(g[2] for g in bs), max(g[3] for g in bs), max(g[4] for g in bs)

def label_text(v):
    v = v.replace('(dual)', '').replace('(du', '').strip()
    for p in ('A10K ', 'B10K ', 'C10K ', 'A50K ', 'B50K ', 'B100K ', 'A100K '):
        if v.startswith(p):
            v = v[len(p):]
    return v.strip()

for name, bx, by in PLACE:
    ex0, ey0 = B[name]['edge'][0] + 0.05, B[name]['edge'][1] + 0.05
    T = lambda x, y: (bx + x - ex0, by + y - ey0)
    for f in B[name]['fps']:
        lib, px, py = f['lib'], f['x'], f['y']
        P = lambda dx, dy: T(px + dx, py + dy)
        lab = None
        if 'RD90' in lib:  # 9 mm pots: the Fab circle is the shaft
            c = max(fab_circles(f), key=lambda g: g[3]); x, y = T(c[1], c[2])
            plate.append(('circle', x, y, 7.5)); lab = (x, y + 8)
        elif 'PTA6043' in lib or 'Fader_45mm' in lib:  # screw holes = the two Fab circles
            c1, c2 = sorted(fab_circles(f), key=lambda g: g[2])[:2]
            (x1, y1), (x2, y2) = T(c1[1], c1[2]), T(c2[1], c2[2])
            travel = 60 if 'PTA60' in lib else 30  # controller "45 mm" fader = 45 mm body, 30 mm travel (PTA3043 outline)
            plate += [('slot', (x1 + x2) / 2, (y1 + y2) / 2, 5.0, travel + 5), ('circle', x1, y1, 2.4), ('circle', x2, y2, 2.4)]
            lab = ((x1 + x2) / 2, y2 + 6)
        elif 'PTA6044' in lib:  # custom dual: Fab box centre, M2 holes 71 apart (Bourns B dimension)
            x0, y0, x1, y1 = fab_box(f); x, y = T((x0 + x1) / 2, (y0 + y1) / 2)
            plate += [('slot', x, y, 5.0, 65), ('circle', x, y - 35.5, 2.4), ('circle', x, y + 35.5, 2.4)]
            lab = (x, y + 41.5)
        elif 'PVA2' in lib:  # body pokes 0.5 mm into the plate: body outline + 0.5
            x0, y0, x1, y1 = fab_box(f); x, y = T((x0 + x1) / 2, (y0 + y1) / 2)
            plate.append(('rect', x, y, x1 - x0 + 0.5, y1 - y0 + 0.5)); lab = (x, y + 7.5)
        elif lib == 'LED_D3.0mm':
            plate.append(('circle', *P(1.27, 0), 3.2))
        elif lib == 'LED_D5.0mm':
            plate.append(('circle', *P(1.27, 0), 5.1))
        elif 'WQP419GR' in lib:  # sits on the jack body, use an M6 washer under the nut
            x, y = P(0, 6.48); plate.append(('circle', x, y, 8.0)); lab = (x, y + 8)
        elif 'EC11' in lib:
            x, y = P(7.5, 2.5); plate.append(('circle', x, y, 7.5)); lab = (x, y + 8)
        elif 'SW_PUSH_6mm' in lib:
            x, y = P(3.25, 2.25); plate.append(('circle', x, y, 4.5))
        elif 'SW_Latch_7x7' in lib:
            x0, y0, x1, y1 = fab_box(f); x, y = T((x0 + x1) / 2, (y0 + y1) / 2)
            plate.append(('circle', x, y, 5.0)); lab = (x, y + 7)
        elif 'NCJ6FA' in lib or 'NC3MAAV' in lib:  # Neutrik D: Ø22.2 + 2 x M3 on the diagonal
            x, y = P(-7.62, 0) if 'NCJ6' in lib else P(3.81, 0)
            shelf += [('circle', x, y, 22.2), ('circle', x - 9.9, y - 9.9, 3.2), ('circle', x + 9.9, y + 9.9, 3.2)]
            lab = (x, y + 15)
        elif 'NJ3FD' in lib or 'NJ5FD' in lib:
            x, y = P(0, 5.72); shelf.append(('circle', x, y, 12.2)); lab = (x, y + 10)
        elif lib.startswith('MountingHole'):
            x, y = P(0, 0)
            if PLATE_FRONT - y > 5:  # M3 standoff from the board up to the plate (the H3 holes sit under the armrest)
                plate.append(('circle', x, y, 3.2))
            continue
        else:
            continue
        if lab and f['val']:
            labels.append((lab[0], lab[1], label_text(f['val']), 'shelf' if ('NCJ6' in lib or 'NC3M' in lib or 'NJ' in lib) else 'plate'))

# Controller: window over the ESP32 (BOOT/RESET reachable, printed lid), J1/J2 midline
ex0, ey0 = 100, 100
esp_x = 256 + (214.55 + 239.95) / 2 - ex0
plate.append(('rect', esp_x, 294, 30, 56))
labels.append((esp_x, 294, 'ESP32 (lid)', 'plate'))

# Shelf: 2.8" SPI TFT (ILI9341 module, 86 x 50 PCB) hung under the shelf over the digital board, cable to controller J4.
# shortcut: generic module numbers (active area 57.6 x 43.2, holes ~80 x 44), measure the real TFT before ordering the shelf.
TFT = (328, 42)
shelf.append(('rect', TFT[0], TFT[1], 60, 45))
for sx in (-40, 40):
    for sy in (-22, 22):
        shelf.append(('circle', TFT[0] + sx, TFT[1] + sy, 3.2))
labels.append((TFT[0], TFT[1] + 28, 'DISPLAY', 'shelf'))

# Fixing holes (M3). Plate: posts in the right region (the boards hold the rest through their standoffs, the armrest
# lip clamps the front edge). Shelf: M3 self-tappers into printed bosses on the rear wall, side walls and risers.
# Keep in step with case.py (PLATE_POSTS, SHELF_BOSSES).
PLATE_POSTS = [(258, 185), (300, 185), (402.5, 185)]
SHELF_BOSSES = [(4.5, 4.5), (98.5, 4.5), (222, 4.5), (300, 4.5), (402.5, 4.5), (4.5, 20), (402.5, 90),
                (36.5, 31.4), (67.5, 31.4), (98.5, 31.4), (160.5, 36.9), (197, 67), (231.7, 49.4), (300, 175.5), (380, 175.5)]
plate += [('circle', x, y, 3.4) for x, y in PLATE_POSTS]
shelf += [('circle', x, y, 3.4) for x, y in SHELF_BOSSES]
json.dump(dict(plate_posts=PLATE_POSTS, shelf_bosses=SHELF_BOSSES, riser=RISER, plate_front=PLATE_FRONT,
               esp_window=[esp_x, 294, 30, 56]), open(os.path.join(HERE, 'panel_fixings.json'), 'w'))

# ---- notches, merges and the self-check (>= 1 mm of metal everywhere) ----
def geom(c):
    if c[0] == 'circle': return Point(c[1], c[2]).buffer(c[3] / 2, 64)
    if c[0] == 'rect': return box(*extent(c))
    return Point(c[1], c[2] - c[4] / 2 + c[3] / 2).buffer(c[3] / 2, 64).union(Point(c[1], c[2] + c[4] / 2 - c[3] / 2).buffer(c[3] / 2, 64)).convex_hull

def extent(c):
    if c[0] == 'circle': return c[1] - c[3] / 2, c[2] - c[3] / 2, c[1] + c[3] / 2, c[2] + c[3] / 2
    return c[1] - c[3] / 2, c[2] - c[4] / 2, c[1] + c[3] / 2, c[2] + c[4] / 2

def build(name, cuts, pts):
    """Merges side-by-side switch cut-outs, turns rect cuts at the edge into notches, returns (outline polygon, hole cuts, problems)."""
    rects = [c for c in cuts if c[0] == 'rect']; cuts = [c for c in cuts if c[0] != 'rect']
    merged = True
    while merged:
        merged = False
        for i, a in enumerate(rects):
            for b in rects[i + 1:]:
                if 0 < geom(a).distance(geom(b)) < 1 or geom(a).intersects(geom(b)):
                    x0, y0, x1, y1 = box(*extent(a)).union(box(*extent(b))).bounds
                    rects = [r for r in rects if r not in (a, b)] + [('rect', (x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0)]
                    merged = True; break
            if merged: break
    poly = Polygon(pts); notches = []
    for r in rects:
        if geom(r).distance(poly.exterior) < MIN_WEB:
            x0, y0, x1, y1 = extent(r); notches.append(box(x0, y0 - 5, x1, y1) if abs(y0 - poly.bounds[1]) < 40 else box(x0, y0, x1, y1 + 5))
        else:
            cuts.append(r)
    if notches: poly = poly.difference(unary_union(notches))
    bad = []
    for c in cuts:
        g = geom(c)
        if not poly.contains(g) or g.distance(poly.exterior) < MIN_WEB:
            bad.append(f'{name}: {c[0]} at ({c[1]:.1f},{c[2]:.1f}) is within 1 mm of the edge')
    for i, a in enumerate(cuts):
        for b in cuts[i + 1:]:
            gap = geom(a).distance(geom(b))
            neutrik = {a[3], b[3]} == {22.2, 3.2} and a[0] == b[0] == 'circle'  # Neutrik's own D cut-out leaves 1.3 mm here
            if gap < MIN_WEB and not neutrik:
                bad.append(f'{name}: cuts at ({a[1]:.1f},{a[2]:.1f}) and ({b[1]:.1f},{b[2]:.1f}) are {gap:.2f} mm apart')
    return list(poly.exterior.coords)[:-1], cuts, bad

PIECES, problems = {}, []
for n, cuts, shelf_piece, desc in (('plate', plate, False, '2.0 mm aluminium control plate'), ('shelf', shelf, True, '1.5 mm aluminium jack shelf')):
    poly, holes, bad = build(n, cuts, outline(shelf_piece))
    PIECES[n] = (holes, poly, desc); problems += bad

# ---- DXF (y flipped so the drawing reads as seen from above, player at the bottom) ----
def write_dxf(n, cuts, poly):
    d = ezdxf.new('R2010', setup=True); d.units = ezdxf.units.MM; m = d.modelspace()
    d.layers.add('OUTLINE', color=7); d.layers.add('CUT', color=1); d.layers.add('LABELS', color=3)
    m.add_lwpolyline([(x, -y) for x, y in poly], close=True, dxfattribs={'layer': 'OUTLINE'})
    for c in cuts:
        if c[0] == 'circle':
            m.add_circle((c[1], -c[2]), c[3] / 2, dxfattribs={'layer': 'CUT'})
        elif c[0] == 'rect':
            x0, y0, x1, y1 = extent(c)
            m.add_lwpolyline([(x0, -y0), (x1, -y0), (x1, -y1), (x0, -y1)], close=True, dxfattribs={'layer': 'CUT'})
        else:  # slot with round ends (bulge 1 = half circle)
            r, h = c[3] / 2, c[4] / 2 - c[3] / 2
            x, y = c[1], -c[2]
            m.add_lwpolyline([(x - r, y - h, 0, 0, 0), (x - r, y + h, 0, 0, -1), (x + r, y + h, 0, 0, 0), (x + r, y - h, 0, 0, -1)],
                             format='xyseb', close=True, dxfattribs={'layer': 'CUT'})
    for x, y, t, pc in labels:
        if pc == n:
            m.add_text(t, height=2.5, dxfattribs={'layer': 'LABELS'}).set_placement((x, -y), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    d.saveas(os.path.join(OUT, f'{n}.dxf'))

# ---- PDF drawing helpers (reportlab, origin bottom-left, so y flips) ----
def draw_piece(cv, n, cuts, poly, ox, oy, s, labels_on=True):
    """ox, oy: page point of case (0,0); s: points per mm."""
    X = lambda x: ox + x * s; Y = lambda y: oy - y * s
    p = cv.beginPath(); p.moveTo(X(poly[0][0]), Y(poly[0][1]))
    for x, y in poly[1:]: p.lineTo(X(x), Y(y))
    p.close(); cv.setLineWidth(0.5); cv.drawPath(p)
    cv.setLineWidth(0.35)
    for c in cuts:
        if c[0] == 'circle':
            cv.circle(X(c[1]), Y(c[2]), c[3] / 2 * s)
            cv.line(X(c[1]) - 1.5, Y(c[2]), X(c[1]) + 1.5, Y(c[2])); cv.line(X(c[1]), Y(c[2]) - 1.5, X(c[1]), Y(c[2]) + 1.5)
        elif c[0] == 'rect':
            x0, y0, x1, y1 = extent(c); cv.rect(X(x0), Y(y1), (x1 - x0) * s, (y1 - y0) * s)
        else:
            cv.roundRect(X(c[1] - c[3] / 2), Y(c[2] + c[4] / 2), c[3] * s, c[4] * s, c[3] / 2 * s)
    if labels_on:
        cv.setFont('Helvetica', max(2.2 * s, 4))
        for x, y, t, pc in labels:
            if pc == n:
                cv.drawCentredString(X(x), Y(y) - 1, t)

def overview():
    cv = canvas.Canvas(os.path.join(OUT, 'panels_overview.pdf'), pagesize=(letter[1], letter[0]))
    pw, ph = letter[1], letter[0]
    for n, (cuts, poly, desc) in PIECES.items():
        s = min((pw - 60) / W, (ph - 110) / max(y for _, y in poly))
        cv.setFont('Helvetica-Bold', 12); cv.drawString(30, ph - 30, f'{desc} ({n}.dxf), seen from above, player at the bottom')
        cv.setFont('Helvetica', 8)
        cv.drawString(30, ph - 44, 'Case coordinates: x from the left outer face, y from the rear outer face. Generated from the KiCad boards by case/gen/panels.py.')
        cv.drawString(30, ph - 55, 'Sizes marked "to verify" in case/PANEL.md come from datasheets of generic parts: check them with the 1:1 paper print first.')
        draw_piece(cv, n, cuts, poly, 30, ph - 70, s)
        cv.showPage()
    cv.save()

def tiled():
    """1:1 print on US Letter, 10 mm overlap, trim marks, a 100 mm check bar on every tile."""
    cv = canvas.Canvas(os.path.join(OUT, 'panels_1to1_letter.pdf'), pagesize=letter)
    pw, ph = letter; mg = 12 * mm; tw, th = pw / mm - 2 * mg / mm, ph / mm - 2 * mg / mm - 14  # usable mm
    for n, (cuts, poly, desc) in PIECES.items():
        ymin = min(y for _, y in poly); H = max(y for _, y in poly) - ymin
        nx, ny = math.ceil((W - 10) / (tw - 10)), math.ceil((H - 10) / (th - 10))
        for j in range(ny):
            for i in range(nx):
                x0, y0 = i * (tw - 10), ymin + j * (th - 10)
                cv.saveState()
                p = cv.beginPath(); p.rect(mg, mg, tw * mm, th * mm); cv.clipPath(p, stroke=0)
                draw_piece(cv, n, cuts, poly, mg - x0 * mm, mg + th * mm + y0 * mm, mm)
                cv.restoreState()
                cv.setLineWidth(0.2); cv.setDash(2, 2); cv.rect(mg, mg, tw * mm, th * mm); cv.setDash()
                # overlap guides: glue the next tile on these lines
                cv.setFont('Helvetica', 7)
                if i < nx - 1: cv.line(mg + (tw - 10) * mm, mg, mg + (tw - 10) * mm, mg + th * mm)
                if j < ny - 1: cv.line(mg, mg + 10 * mm, mg + tw * mm, mg + 10 * mm)
                cv.setFont('Helvetica-Bold', 10)
                cv.drawString(mg, ph - mg + 2, f'{n.upper()}  tile row {j + 1}/{ny}, column {i + 1}/{nx}   (print at 100% / "Actual size", no scaling)')
                cv.setLineWidth(1); bx, by = mg, ph - mg - 10 * mm
                cv.line(bx, by, bx + 100 * mm, by); cv.line(bx, by - 2 * mm, bx, by + 2 * mm); cv.line(bx + 100 * mm, by - 2 * mm, bx + 100 * mm, by + 2 * mm)
                cv.setFont('Helvetica', 7); cv.drawString(bx + 102 * mm, by - 2, 'this bar must measure exactly 100 mm')
                cv.drawString(mg, mg - 9, f'case x {x0:.0f} to {x0 + tw:.0f} mm, y {y0:.0f} to {y0 + th:.0f} mm. Overlap 10 mm: line up the solid guide line with the next tile\'s edge.')
                cv.showPage()
    cv.save()

for n, (cuts, poly, _) in PIECES.items():
    write_dxf(n, cuts, poly)
overview(); tiled()
print(f'plate: {len(plate)} cuts, shelf: {len(shelf)} cuts, {len(labels)} labels')
print('\n'.join(problems) if problems else 'self-check: OK')
