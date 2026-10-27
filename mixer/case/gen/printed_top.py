# Printed top (replaces the aluminium plate and shelf): splits both pieces into Ender 3 tiles with glued half-lap joints,
# adds nut recesses, the NJ3/NJ5 thin-web recesses, fader spacer bosses and XLR spacer pads. Run after panels.py:
#   uv run --no-project --with build123d --with shapely python printed_top.py
# Writes ../stl/top_plate_*.stl and ../stl/top_shelf_*.stl in assembly position (flip them top-down in the slicer).
import json, os, math
from shapely.geometry import Polygon, Point, LineString, box as sbox
from shapely.ops import unary_union
from build123d import Face, Wire, Vector, extrude, Pos, Cylinder, Box, export_stl

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'stl')
S = json.load(open(os.path.join(HERE, 'render_scene.json')))
D, LAP = 353.0, S['lap']
# Plate: underside stays 10.5 mm above the strip PCBs (z 33.1). 2.5 mm thick for stiffness; nut recesses bring the pot web
# back to 1.5 mm, so the M7 thread above it is 3.0 mm (a 2 mm plate would leave 2.5 mm).
# Shelf: underside stays 24.0 mm above the PCB (z 46.6), 3 mm thick (NCJ6FA-V takes up to 3 mm).
PIECE = {'plate': (33.1, 2.5), 'shelf': (46.6, 3.0)}
RECESS = {'pot': (13.0, 1.0), 'pot_dual': (13.0, 1.0), 'encoder': (13.0, 1.0), 'jack35': (11.0, 1.0),  # nut seats
          'trs': (18.0, 1.5)}  # NJ3FD-V / NJ5FD-V quick-fix cap needs a 1.2-1.5 mm panel: 1.5 mm web under an 18 mm recess

def hole_poly(c):
    if c[0] == 'circle': return Point(c[1], c[2]).buffer(c[3] / 2, 32)
    if c[0] == 'rect': return sbox(c[1] - c[3] / 2, c[2] - c[4] / 2, c[1] + c[3] / 2, c[2] + c[4] / 2)
    h = c[4] / 2 - c[3] / 2
    return LineString([(c[1], c[2] - h), (c[1], c[2] + h)]).buffer(c[3] / 2, 32)

def solid(poly, z0, h):
    out = None
    for p in getattr(poly, 'geoms', [poly]):
        if p.is_empty or p.area < 0.5: continue
        wire = lambda ring: Wire.make_polygon([Vector(x, D - y, 0) for x, y in list(ring.coords)[:-1]], close=True)
        f = Face(wire(p.exterior), [wire(r) for r in p.interiors])
        sld = Pos(0, 0, z0) * extrude(f, amount=h, dir=(0, 0, 1))
        out = sld if out is None else out + sld
    return out

def cyl(x, y, d, z0, z1):
    return Pos(x, D - y, (z0 + z1) / 2) * Cylinder(d / 2, z1 - z0)

sizes, report = {}, []
for n, (z0, t) in PIECE.items():
    pc = S['pieces'][n]
    holes = unary_union([hole_poly(c) for c in pc['holes']])
    body = Polygon(pc['outline']).difference(holes)
    names = list(pc['tiles'])
    # lap zones, one owner pair per point: a gets the bottom half, b the top half
    zones, taken = {}, Polygon()
    for a, b, seg in pc['joints']:
        z = LineString(seg).buffer(LAP, cap_style=2).intersection(Polygon(pc['tiles'][a]).union(Polygon(pc['tiles'][b]))).difference(taken)
        zones[(a, b)] = zones.get((a, b), Polygon()).union(z); taken = taken.union(z)
    parts = [p for p in S['parts']]
    for tname in names:
        R = Polygon(pc['tiles'][tname]).intersection(body)
        full = R.difference(taken)
        bottom = unary_union([z for (a, b), z in zones.items() if a == tname]).intersection(body).buffer(-0.1)
        top = unary_union([z for (a, b), z in zones.items() if b == tname]).intersection(body).buffer(-0.1)
        s = solid(full, z0, t)
        if not bottom.is_empty: s = s + solid(bottom, z0, t / 2)
        if not top.is_empty: s = s + solid(top, z0 + t / 2, t / 2)
        own = Polygon(pc['tiles'][tname]).intersection(Polygon(pc['outline'])).buffer(0.01)  # before holes: part centres sit in them
        for p in parts:
            k, c = p['kind'], p['cut']
            on_piece = (k in ('combo', 'xlr', 'trs')) == (n == 'shelf')
            if not on_piece or not own.contains(Point(c[1], c[2])): continue
            if k in RECESS:
                d, depth = RECESS[k]
                if taken.distance(Point(c[1], c[2])) < d / 2: report.append(f'{n}/{tname}: {k} recess at ({c[1]:.0f},{c[2]:.0f}) reaches a lap joint')
                s = s - cyl(c[1], c[2], d, z0 + t - depth, z0 + t + 1)
            if k == 'fader':  # printed spacers between the fader housing and the plate: 4 mm (60 mm PTA), 1 mm (controller)
                travel = c[4] - 5
                dy, h = (35.5, 4.0) if travel == 60 else (20.5, 1.0)
                for sy in (-dy, dy):
                    s = s + cyl(c[1], c[2] + sy, 6.0, z0 - h, z0) - cyl(c[1], c[2] + sy, 2.4, z0 - h - 1, z0 + t + 1)
            if k == 'xlr':  # the 2.7 mm flange spacer as a pad under the shelf (NC3MAAV flange sits 21.3 above the PCB)
                pad = Pos(c[1], D - c[2], z0 - 1.35) * Box(24, 24, 2.7)
                s = s + pad - cyl(c[1], c[2], 22.2, z0 - 3, z0 + 0.1)
                for sx in (-9.9, 9.9):
                    s = s - cyl(c[1] + sx, c[2] + sx, 3.2, z0 - 3, z0 + 0.1)
        bb = s.bounding_box()
        sizes[f'top_{n}_{tname}'] = (round(bb.size.X, 1), round(bb.size.Y, 1), round(bb.size.Z, 1))
        assert max(bb.size.X, bb.size.Y) <= 215, f'top_{n}_{tname} too big for the Ender 3: {sizes[f"top_{n}_{tname}"]}'
        export_stl(s, os.path.join(OUT, f'top_{n}_{tname}.stl'))
        print(f'top_{n}_{tname}', sizes[f'top_{n}_{tname}'])
print('\n'.join(report) if report else 'recesses clear of the joints')
old = json.load(open(os.path.join(OUT, 'sizes.json'))) if os.path.exists(os.path.join(OUT, 'sizes.json')) else {}
json.dump({**old, **sizes}, open(os.path.join(OUT, 'sizes.json'), 'w'), indent=1)
