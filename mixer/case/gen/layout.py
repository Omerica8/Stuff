# Where every board sits in the case: the one source for panels.py, case.py and render_blender.py.
# Case coordinates in mm: x from the left outer face, y from the rear outer face, z from the bottom.
# rot 0: the board as drawn in KiCad, its top edge to the rear. rot 90: its top edge faces the right wall.
# Layout "option 1" (2026-10-27): 2 mic strips, MIDI hub along the rear wall, digital board turned so its ports face the right wall.
import json, os

D, W = 353.0, 407.0
B = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'boards.json')))

# (board, case x of the left edge, case y of the rear edge, rotation, PCB underside z)
BOARDS = [('mixer_strip', 6, 5, 0, 21.0), ('mixer_strip', 37, 5, 0, 21.0),
          ('mixer_stereo', 68, 5, 0, 21.0), ('mixer_stereo', 99, 5, 0, 21.0),
          ('mixer_master', 130, 5, 0, 21.0),
          ('controller', 194, 230, 0, 24.0),
          ('mixer_midi', 196, 5, 0, 9.0),        # 8 DIN + USB-A through the rear wall
          ('mixer_power', 215, 76, 0, 8.0),      # heatsinks (35 mm) under the shelf
          ('mixer_digital', 326, 76, 90, 9.0),   # USB-B, USB-C, 2 DIN through the right wall
          ('mixer_reverb', 348, 245, 90, 8.0)]   # under the plate, right of the controller

def size(name):
    x0, y0, x1, y1 = B[name]['edge']
    return x1 - x0 - 0.1, y1 - y0 - 0.1

def to_case(entry, kx, ky):
    """KiCad board coordinates (mm) -> case (x, y)."""
    name, bx, by, rot, _ = entry
    u, v = kx - (B[name]['edge'][0] + 0.05), ky - (B[name]['edge'][1] + 0.05)
    if rot == 0:
        return bx + u, by + v
    return bx + size(name)[1] - v, by + u  # rot 90: top edge (v = 0) to the right, left edge (u = 0) to the rear

def footprint_box(entry, f):
    """Case-coordinate bounding box of a footprint's Fab drawing."""
    bs = [g for g in f['fab'] if g[0] == 'b']
    pts = [to_case(entry, x, y) for g in bs for x, y in ((g[1], g[2]), (g[3], g[4]))]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)

if __name__ == '__main__':  # self-check: boards inside the walls and not overlapping where they share a height band
    from itertools import combinations
    boxes = []
    for e in BOARDS:
        (x0, y0), (x1, y1) = to_case(e, B[e[0]]['edge'][0] + .05, B[e[0]]['edge'][1] + .05), to_case(e, B[e[0]]['edge'][2] - .05, B[e[0]]['edge'][3] - .05)
        bx = (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))
        assert bx[0] >= 3 and bx[1] >= 3 and bx[2] <= W - 3 and bx[3] <= D - 3, (e[0], bx)
        boxes.append((e, bx))
        print(f'{e[0]:14} x {bx[0]:6.1f}-{bx[2]:6.1f}  y {bx[1]:6.1f}-{bx[3]:6.1f}  z {e[4]}')
    for (a, p), (b, q) in combinations(boxes, 2):
        if p[0] < q[2] and q[0] < p[2] and p[1] < q[3] and q[1] < p[3]:
            print('OVERLAP (plan view)', a[0], b[0])
