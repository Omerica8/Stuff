# 3D-printed case around the two aluminium pieces (Ender 3: every part fits a 220 x 220 bed, some diagonally).
# Run after panels.py: uv run --no-project --with build123d --with matplotlib python case.py
# Numbers in case coordinates (x from the left outer face, y from the rear outer face, z from the bottom), see STATUS.md.
import json, os, math
from build123d import Box, Cylinder, Pos, Rot, export_stl

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'stl'); os.makedirs(OUT, exist_ok=True)
FX = json.load(open(os.path.join(HERE, 'panel_fixings.json')))
B = json.load(open(os.path.join(HERE, 'boards.json')))

W, D, WALL, FLOOR = 407.0, 353.0, 3.0, 3.0
Z_PLATE, Z_PLATE_TOP, Z_SHELF = 33.1, 35.6, 46.6   # printed plate (2.5 mm) underside/top, shelf underside
Z_ARM = 37.0                                       # armrest underside (ribbon plugs reach ~35.6)
INSERT_D, INSERT_DEPTH, PILOT_D = 4.2, 6.0, 2.5    # M3 heat-set insert hole; M3 self-tapper pilot

Y = lambda y: D - y  # model y runs from the front (0) to the rear (353), so the model isn't mirrored

def bx(x0, y0, x1, y1, z0, z1):
    return Pos((x0 + x1) / 2, (Y(y0) + Y(y1)) / 2, (z0 + z1) / 2) * Box(abs(x1 - x0), abs(y1 - y0), z1 - z0)

def cyl(x, y, d, z0, z1):
    return Pos(x, Y(y), (z0 + z1) / 2) * Cylinder(d / 2, z1 - z0)

from layout import BOARDS, to_case, footprint_box
posts = [(*to_case(e, f['x'], f['y']), e[4]) for e in BOARDS for f in B[e[0]]['fps'] if f['lib'].startswith('MountingHole')]

# ---------------- tray (floor, walls, posts), split in four ----------------
tray = bx(0, 0, W, D, 0, FLOOR)
tray += bx(0, 0, W, WALL, FLOOR, Z_SHELF)                                  # rear wall, up to the shelf
tray += bx(0, D - WALL, W, D, FLOOR, Z_ARM)                                # front wall, carries the armrest
left_y, right_y = FX['riser'][0][3], FX['riser'][-1][3]                    # riser front faces at the side walls
for x0 in (0, W - WALL):
    ry = left_y if x0 == 0 else right_y
    tray += bx(x0, 0, x0 + WALL, ry, FLOOR, Z_SHELF)                       # under the shelf
    tray += bx(x0, ry, x0 + WALL, FX['plate_front'], FLOOR, Z_PLATE)       # under the plate
    tray += bx(x0, FX['plate_front'], x0 + WALL, D, FLOOR, Z_ARM)          # under the armrest
for x, y, zb in posts:
    tray += cyl(x, y, 7, FLOOR, zb)
    tray -= cyl(x, y, INSERT_D, zb - INSERT_DEPTH, zb + 0.1)
for x, y in FX['plate_posts']:
    tray += cyl(x, y, 8, FLOOR, Z_PLATE)
    tray -= cyl(x, y, INSERT_D, Z_PLATE - INSERT_DEPTH, Z_PLATE + 0.1)

# shelf bosses: the ones 2.5 mm behind a riser's rear face belong to the riser, the rest sit on the rear/side walls
def riser_rear(x):
    return next(r[2] for r in FX['riser'] if r[0] <= x < r[1])
on_riser = lambda x, y: abs(y - (riser_rear(x) - 2.5)) < 0.2
for x, y in FX['shelf_bosses']:
    if not on_riser(x, y):
        x0, x1 = (0, x + 2.5) if x < 10 else (x - 2.5, W) if x > W - 10 else (x - 2.5, x + 2.5)
        tray += bx(x0, 0 if y < 10 else y - 2.5, x1, y + 2.5, Z_SHELF - 10, Z_SHELF)
        tray -= cyl(x, y, PILOT_D, Z_SHELF - 9, Z_SHELF + 0.1)

# armrest bosses (side margins and the free strip in front of the controller)
ARM_BOSSES = [(4.5, 345), (402.5, 345), (200, 340), (300, 340), (380, 340)]
for x, y in ARM_BOSSES:
    tray += bx(x - 3, y - 3, x + 3, D - WALL, Z_ARM - 8, Z_ARM)
    tray -= cyl(x, y, INSERT_D, Z_ARM - INSERT_DEPTH, Z_ARM + 0.1)

# Connector openings, from the footprints' Fab boxes: the MIDI hub through the rear wall, the digital board through the right wall
# (both PCB tops at z 10.6). shortcut: connector heights from generic datasheets (CUI SDS-50J DIN, OST USB-B1HS, GCT USB4125,
# Molex 67643 USB-A), file to fit.
HEIGHT = {'DIN-5': (10.0, 18), 'USB_B': (5.6, 12.5), 'USB_C': (1.7, 5.0), 'USB_A': (3.5, 7.5)}  # opening centre above the PCB, height
for e in BOARDS:
    if e[0] not in ('mixer_midi', 'mixer_digital'): continue
    for f in B[e[0]]['fps']:
        k = next((k for k in HEIGHT if f['lib'].startswith(k)), None)
        if not k or (e[0] == 'mixer_digital' and f['ref'] == 'J13'): continue  # J13: internal USB-A to the controller
        zc, h = e[4] + 1.6 + HEIGHT[k][0], HEIGHT[k][1]
        x0, y0, x1, y1 = footprint_box(e, f)
        if e[3] == 0: tray -= bx(x0 - 0.5, -1, x1 + 0.5, WALL + 1, zc - h / 2, zc + h / 2)
        else: tray -= bx(W - WALL - 1, y0 - 0.5, W + 1, y1 + 0.5, zc - h / 2, zc + h / 2)
tray -= Pos(W - 1.5, Y(60), 30) * Rot(0, 90, 0) * Cylinder(4.1, WALL + 2)                 # panel DC jack (5.5/2.1, M8), right wall
# vents under the power board (heatsinks) and high in the rear wall
for i in range(10):
    tray -= bx(225 + i * 8, 85, 228 + i * 8, 150, -1, FLOOR + 1)
for i in range(6):
    tray -= bx(205 + i * 30, -1, 215 + i * 30, WALL + 1, 34, 42)

# seam flanges between the quarters: 4 mm ribs on both sides of each seam, M3 bolts across
SX, SY = W / 2, D / 2
for side in (-1, 1):
    tray += bx(SX + min(0, side * 4), WALL, SX + max(0, side * 4), D - WALL, FLOOR, FLOOR + 8)
    tray += bx(WALL, SY + min(0, side * 4), W - WALL, SY + max(0, side * 4), FLOOR, FLOOR + 8)
for y in (40, 120, 230, 310):
    tray -= Pos(SX, Y(y), FLOOR + 4.5) * Rot(0, 90, 0) * Cylinder(1.7, 12)
for x in (40, 120, 290, 370):
    tray -= Pos(x, Y(SY), FLOOR + 4.5) * Rot(90, 0, 0) * Cylinder(1.7, 12)

quarters = {}
for qx, (x0, x1) in enumerate(((0, SX), (SX, W))):
    for qy, (y0, y1) in enumerate(((0, SY), (SY, D))):
        quarters[f'tray_{"rear" if qy == 0 else "front"}_{"left" if qx == 0 else "right"}'] = tray & bx(x0, y0, x1, y1, -1, 60)

# ---------------- riser wall (hangs from the shelf, M3 self-tappers from above) ----------------
R = FX['riser']
riser = None
for i, (x0, x1, yr, yf) in enumerate(R):
    seg = bx(x0, yr, x1, yf, Z_PLATE_TOP, Z_SHELF)
    riser = seg if riser is None else riser + seg
    if i + 1 < len(R):  # jog wall on the side without plate
        nyr, nyf = R[i + 1][2], R[i + 1][3]
        xa = x1 if nyf > yf else x1 - 2
        riser += bx(xa, min(yr, nyr), xa + 2, max(yf, nyf), Z_PLATE_TOP, Z_SHELF)
for x, y in FX['shelf_bosses']:
    if on_riser(x, y):
        yr = riser_rear(x)
        riser += bx(x - 2, yr - 5, x + 2, yr, Z_SHELF - 10, Z_SHELF)
        riser -= cyl(x, y, PILOT_D, Z_SHELF - 9, Z_SHELF + 0.1)
risers = {'riser_left': riser & bx(0, 0, 129.5, 200, 30, 50), 'riser_middle': riser & bx(129.5, 0, 193.5, 200, 30, 50),
          'riser_right': riser & bx(193.5, 0, W, 200, 30, 50)}

# ---------------- armrest (prints diagonally: left part 254 x 31) ----------------
arm = bx(0, FX['plate_front'], W, D, Z_ARM, Z_ARM + 3)
arm += bx(0, FX['plate_front'] - 5, W, FX['plate_front'], Z_PLATE_TOP, Z_ARM + 3)   # lip that clamps the plate's front edge
for x, y in ARM_BOSSES:
    arm -= cyl(x, y, 3.4, Z_ARM - 1, Z_ARM + 4)
    arm -= cyl(x, y, 6.2, Z_ARM + 1.2, Z_ARM + 4)                                    # counterbore for M3 cap screws
armrests = {'armrest_left': arm & bx(0, 300, 254, D, 30, 50), 'armrest_right': arm & bx(254, 300, W, D, 30, 50)}

# ---------------- ESP32 window lid, rear feet ----------------
ex, ey, ew, eh = FX['esp_window']
lid = bx(ex - ew / 2 - 3, ey - eh / 2 - 3, ex + ew / 2 + 3, ey + eh / 2 + 3, Z_PLATE_TOP, Z_PLATE_TOP + 1.5)
lid += bx(ex - ew / 2 + 0.2, ey - eh / 2 + 0.2, ex + ew / 2 - 0.2, ey + eh / 2 - 0.2, Z_PLATE, Z_PLATE_TOP)
# Rear foot (x2, under the rear corners; stick-on 8 mm rubber feet at the front): lifts the rear 313*tan(10 deg) more than
# the front feet, top face at 10 deg so it sits flat under the tilted case. shortcut: glue or VHB them on.
FOOT_FRONT = 8 + (313 - 20) * math.tan(math.radians(10))
foot = Pos(0, 0, 40) * Box(40, 40, 80)
foot -= Pos(0, -20, FOOT_FRONT) * Rot(10, 0, 0) * Pos(0, 50, 50) * Box(100, 140, 100)

parts = {**quarters, **risers, **armrests, 'esp32_lid': lid, 'rear_foot_x2': foot}
sizes = {}
for n, p in parts.items():
    bb = p.bounding_box()
    sizes[n] = (round(bb.size.X, 1), round(bb.size.Y, 1), round(bb.size.Z, 1))
    export_stl(p, os.path.join(OUT, f'{n}.stl'))
    fits = max(bb.size.X, bb.size.Y) <= 220 or math.hypot(bb.size.X, bb.size.Y) <= 300  # else diagonally on the bed
    assert fits and min(bb.size.X, bb.size.Y) <= 220, f'{n} does not fit the Ender 3 bed: {sizes[n]}'
    print(n, sizes[n])
json.dump(sizes, open(os.path.join(OUT, 'sizes.json'), 'w'), indent=1)

# ---------------- preview render (matplotlib, rough) ----------------
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig = plt.figure(figsize=(12, 9)); ax = fig.add_subplot(projection='3d')
colours = {'tray': '#8a9099', 'riser': '#c07a2c', 'armrest': '#3b4048', 'esp32': '#3b4048'}
for n, p in parts.items():
    if n.startswith('rear_foot'): continue
    vs, ts = p.tessellate(0.5, 0.5)
    tri = [[(v.X, v.Y, v.Z) for v in (vs[a], vs[b], vs[c])] for a, b, c in ts]
    ax.add_collection3d(Poly3DCollection(tri, facecolors=colours[n.split('_')[0]], edgecolors=colours[n.split('_')[0]], linewidths=0.1, shade=True))
ax.set_xlim(0, W); ax.set_ylim(0, D); ax.set_zlim(0, 120); ax.set_box_aspect((W, D, 120)); ax.view_init(40, -65); ax.axis('off')
plt.savefig(os.path.join(HERE, '..', 'out', 'case_preview.png'), dpi=110, bbox_inches='tight')
