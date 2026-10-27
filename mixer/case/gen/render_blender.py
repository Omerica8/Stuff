# Photo-style render of the mixer. Run after panels.py, case.py and printed_top.py:
#   "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P render_blender.py
# CASE=1 (default): the assembled mixer with the printed case and top -> ../out/render_hero.png, render_top.png, mixer_assembled.blend
# CASE=0: the boards only, as they sit inside, with their KiCad 3D models (../glb, made by kicad-cli pcb export glb), ribbon
#         cables and modules -> ../out/render_boards_hero.png, render_boards_top.png, mixer_boards.blend
# Knobs, caps, jack noses and every part KiCad has no 3D model for are simple stand-ins, not real models.
import bpy, json, os, math
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'out')
S = json.load(open(os.path.join(HERE, 'render_scene.json')))
B = json.load(open(os.path.join(HERE, 'boards.json')))
CASE = os.environ.get('CASE', '1') != '0'
DETAIL = os.environ.get('DETAIL') == '1'      # the printed parts alone, no knobs or labels (renders render_case_*.png)
EXPLODE = DETAIL and os.environ.get('EXPLODE') == '1'
D, MM = 353.0, 0.001
Z_PLATE_TOP, Z_SHELF_TOP = 35.6, 49.6  # printed plate 2.5 mm on z 33.1, printed shelf 3 mm on z 46.6
P = lambda x, y, z: (x * MM, (D - y) * MM, z * MM)  # case coords (mm) -> Blender (m), front at y = 0
import sys; sys.path.insert(0, HERE)
from layout import BOARDS, to_case, footprint_box, size  # board placement shared with panels.py and case.py
ZT = {'mixer_strip': 22.6, 'mixer_stereo': 22.6, 'mixer_master': 22.6, 'controller': 25.6}  # PCB tops of the panel boards

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
rig = bpy.data.objects.new('mixer', None); scene.collection.objects.link(rig)

def mat(name, rgb, metal=0.0, rough=0.5, emit=0.0):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*rgb, 1); b.inputs['Metallic'].default_value = metal; b.inputs['Roughness'].default_value = rough
    if emit:
        b.inputs['Emission Color'].default_value = (*rgb, 1); b.inputs['Emission Strength'].default_value = emit
    return m

TOP = mat('light grey PLA (top)', (0.52, 0.53, 0.55), 0.0, 0.5)
PLA = mat('dark grey PLA', (0.045, 0.048, 0.055), 0.0, 0.55)
BLACK = mat('black plastic', (0.012, 0.012, 0.014), 0.0, 0.4)
RUBBER = mat('black rubber', (0.02, 0.02, 0.02), 0.0, 0.8)
NICKEL = mat('nickel', (0.75, 0.75, 0.73), 1.0, 0.2)
STEEL = mat('steel', (0.55, 0.56, 0.58), 1.0, 0.35)
HOLE = mat('hole', (0.0, 0.0, 0.0), 0.0, 1.0)
WHITE = mat('print white', (0.9, 0.9, 0.9), 0.0, 0.6)
INK = mat('print ink', (0.02, 0.02, 0.025), 0.0, 0.5)
POTBLUE = mat('pot body', (0.05, 0.08, 0.25), 0.3, 0.4)
RIBBON = mat('ribbon grey', (0.45, 0.46, 0.48), 0.0, 0.6)
STRIPE = mat('ribbon stripe', (0.6, 0.02, 0.02), 0.0, 0.6)
GREEN = mat('pcb green', (0.02, 0.18, 0.06), 0.0, 0.45)
CAPS = {'red': mat('cap red', (0.55, 0.03, 0.02)), 'green': mat('cap green', (0.05, 0.35, 0.12)), 'blue': mat('cap blue', (0.03, 0.12, 0.5)),
        'yellow': mat('cap yellow', (0.7, 0.5, 0.02)), 'white': mat('cap white', (0.85, 0.85, 0.82)), 'grey': mat('cap grey', (0.3, 0.3, 0.32)),
        'orange': mat('cap orange', (0.75, 0.22, 0.02))}

def link(o, m=None):
    if m: o.data.materials.clear(); o.data.materials.append(m)
    o.parent = rig
    return o

def cyl(x, y, z0, d, h, m, verts=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=d / 2 * MM, depth=h * MM, location=P(x, y, z0 + h / 2))
    o = bpy.context.object
    if verts > 12: bpy.ops.object.shade_auto_smooth(angle=math.radians(40))
    return link(o, m)

def box(x, y, z0, w, l, h, m):  # w along x, l along case y
    bpy.ops.mesh.primitive_cube_add(size=1, location=P(x, y, z0 + h / 2))
    o = bpy.context.object; o.scale = (w * MM, l * MM, h * MM)
    return link(o, m)

def strip(a, b, width, thick, m):
    """Flat ribbon segment between two case points (x, y, z), lying flat, width across the run."""
    pa, pb = Vector(P(*a)), Vector(P(*b))
    bpy.ops.mesh.primitive_cube_add(size=1, location=(pa + pb) / 2)
    o = bpy.context.object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = (pb - pa).to_track_quat('X', 'Z')
    o.scale = ((pb - pa).length + width * MM * 0.05, width * MM, thick * MM)
    return link(o, m)

STL = os.path.join(HERE, '..', 'stl')
if CASE:
    # ---------------- printed case and printed top ----------------
    for f in sorted(os.listdir(STL)):
        if not f.endswith('.stl') or f.startswith('rear_foot'): continue
        bpy.ops.wm.stl_import(filepath=os.path.join(STL, f), global_scale=MM)
        o = bpy.context.selected_objects[0]
        link(o, TOP if f.startswith('top_') else BLACK if f.startswith(('armrest', 'esp32')) else
             mat('riser PLA', (0.6, 0.25, 0.04), 0, 0.5) if DETAIL and f.startswith('riser') else PLA)
        for poly in o.data.polygons: poly.use_smooth = False
        if EXPLODE:  # lift each layer and spread the tiles so every joint, boss and recess shows
            n = f[:-4]; c = o.matrix_world @ (sum((v.co for v in o.data.vertices), Vector()) / len(o.data.vertices))  # mesh is in mm, object scaled
            spread = {'tray': 18, 'top_plate': 18, 'top_shelf': 18}.get(next((k for k in ('tray', 'top_plate', 'top_shelf') if n.startswith(k)), ''), 0)
            lift = {'tray': 0, 'riser': 150, 'armrest': 60, 'esp32': 215, 'top_plate': 195, 'top_shelf': 255}[next(k for k in ('tray', 'riser', 'armrest', 'esp32', 'top_plate', 'top_shelf') if n.startswith(k))]
            o.location = Vector(((c.x - 0.2035) * spread / 100, (c.y - 0.1765) * spread / 100 - (0.07 if n.startswith('armrest') else 0), lift * MM))
    for x, y, text, piece in ([] if DETAIL else S['labels']):  # printed overlay labels (sticker or paint pen)
        cu = bpy.data.curves.new(text, 'FONT'); cu.body = text; cu.size = 2.4 * MM; cu.align_x = 'CENTER'; cu.align_y = 'CENTER'
        o = bpy.data.objects.new(text, cu); scene.collection.objects.link(o)
        o.location = P(x, y + 1.5, (Z_PLATE_TOP if piece == 'plate' else Z_SHELF_TOP) + 0.02); link(o, INK)
before_boards = set(bpy.data.objects)
if not CASE or DETAIL:
    # ---------------- boards with their KiCad 3D models ----------------
    for e in BOARDS:
        name, bx, by, rot, zb = e
        ex0, ey0 = B[name]['edge'][0] + 0.05, B[name]['edge'][1] + 0.05
        before = set(bpy.data.objects)
        bpy.ops.import_scene.gltf(filepath=os.path.join(HERE, '..', 'glb', f'{name}.glb'))
        for o in set(bpy.data.objects) - before:  # glb: metres, x = kicad x, y = -kicad y, z = 0 at the PCB underside
            if o.parent is None:
                if rot == 0:
                    o.location = ((bx - ex0) * MM, (D - by + ey0) * MM, zb * MM)
                else:  # top edge to the right wall: (gx, gy) -> (gy, -gx)
                    o.rotation_mode = 'XYZ'; o.rotation_euler = (0, 0, math.radians(-90))  # glTF roots import in quaternion mode
                    o.location = ((bx + size(name)[1] + ey0) * MM, (D - by + ex0) * MM, zb * MM)
                o.parent = rig
    entry = {e[0]: e for e in BOARDS}
    # stand-ins for parts KiCad has no model for (heatsinks), and the modules
    for f in B['mixer_power']['fps']:
        if f['lib'].startswith('Heatsink'):
            x0, y0, x1, y1 = footprint_box(entry['mixer_power'], f)
            box((x0 + x1) / 2, (y0 + y1) / 2, entry['mixer_power'][4] + 1.6, x1 - x0, y1 - y0, 35, BLACK)
    for f in B['mixer_reverb']['fps']:
        if 'Akizuki' in f['lib']:  # AE-FV-1-DIP module on its sockets
            x0, y0, x1, y1 = footprint_box(entry['mixer_reverb'], f); zr = entry['mixer_reverb'][4] + 1.6
            box((x0 + x1) / 2, (y0 + y1) / 2, zr + 8.5, x1 - x0, y1 - y0, 1.6, GREEN); box((x0 + x1) / 2, (y0 + y1) / 2, zr + 10.1, 5.3, 10.5, 1.8, BLACK)
    for e in BOARDS:  # MIDI DIN sockets (KiCad has no model for the CUI SDS-50J): body plus a socket face
        for f in B[e[0]]['fps']:
            if f['lib'].startswith('DIN-5'):
                x0, y0, x1, y1 = footprint_box(e, f)
                box((x0 + x1) / 2, (y0 + y1) / 2, e[4] + 1.6, x1 - x0, y1 - y0, 20.5, BLACK)
    for f in B['mixer_midi']['fps']:
        if f['ref'] == 'J10':  # Raspberry Pi Pico in its two 1x20 sockets (J10/J11)
            x0, y0, x1, y1 = footprint_box(entry['mixer_midi'], f)
            box((x0 + x1) / 2, y0 - 8.9 + 1.3, entry['mixer_midi'][4] + 1.6 + 8.5, 51, 21, 1.0, GREEN)
            box((x0 + x1) / 2, y0 - 8.9 + 1.3, entry['mixer_midi'][4] + 1.6 + 9.5, 7, 7, 0.9, BLACK)
    # ESP32-S3 DevKitC soldered on its pins (antenna to the rear, USB-C to the front)
    (ex, ey), ez = to_case(entry['controller'], (214.55 + 239.95) / 2, (138.61 + 191.95) / 2), 25.6 + 2.5
    box(ex, ey, ez, 26, 69, 1.6, BLACK); box(ex, ey - 22, ez + 1.6, 18, 25.5, 3.1, STEEL); box(ex, ey + 33, ez + 1.6, 9, 7.5, 3.2, STEEL)
    # ribbon cables: POWER (J2) and BUS (J3) daisy-chained across the audio boards, DIGITAL from master J4 to the digital board,
    # power board J2 to the POWER chain. shortcut: drawn straight between plugs, real cables will drape.
    plugs = {}
    for e in BOARDS:
        for f in B[e[0]]['fps']:
            if f['lib'].startswith('IDC-Header_2x05'):
                x0, y0, x1, y1 = footprint_box(e, f); zt = e[4] + 1.6
                box((x0 + x1) / 2, (y0 + y1) / 2, zt + 4, x1 - x0 + 0.5, y1 - y0 + 0.5, 9, BLACK)
                plugs.setdefault((e[0], f['ref']), []).append(((x0 + x1) / 2, (y0 + y1) / 2, zt + 13.5))
    def chain(points):
        for a, b in zip(points, points[1:]):
            strip(a, b, 12.7, 0.9, RIBBON)
            strip((a[0], a[1] - 5.6, a[2] + 0.05), (b[0], b[1] - 5.6, b[2] + 0.05), 1.3, 0.92, STRIPE)
    audio = [e[0] for e in BOARDS if e[0].startswith(('mixer_strip', 'mixer_stereo', 'mixer_master'))]
    for ref, lift in (('J2', 0.0), ('J3', 1.5)):  # both chains run along the same row: BUS rides over the POWER ribbon
        pts = []
        for name in dict.fromkeys(audio):
            pts += [(x, y, z + lift) for x, y, z in plugs.get((name, ref), [])]
        chain(sorted(pts))
    pw = plugs[('mixer_power', 'J2')][0]; mj2 = plugs[('mixer_master', 'J2')][0]
    chain([pw, (pw[0], 336, 22.5), (mj2[0] + 12, 336, 30), mj2])
    mj4 = plugs[('mixer_master', 'J4')][0]; dj4 = plugs[('mixer_digital', 'J4')][0]
    chain([mj4, (mj4[0], 345, 30), (342, 345, 20), (342, dj4[1] + 10, 20), dj4])

# ---------------- controls (stand-ins); with CASE=0 they get bodies down to their boards ----------------
def cap_colour(val):
    v = val.upper()
    if 'GAIN' in v: return 'red'
    if any(k in v for k in ('HIGH', 'MID', 'LOW')): return 'green' if 'MID' not in v else 'blue'
    if 'AUX' in v or 'MONITOR' in v: return 'yellow'
    if 'FX' in v: return 'orange'
    if 'PAN' in v or 'BAL' in v: return 'white'
    return 'grey'

def knob(x, y, d, h, colour, z0=Z_PLATE_TOP + 1.0):
    cyl(x, y, z0, d, h * 0.75, BLACK)                                  # skirt and body
    cyl(x, y, z0 + h * 0.75, d * 0.82, h * 0.25, CAPS[colour])          # coloured top
    box(x, y - d * 0.22, z0 + h - 0.1, 0.9, d * 0.38, 0.4, WHITE)        # pointer line (pointing to the rear = 12 o'clock)

meter = sorted([p for p in S['parts'] if p['kind'] == 'led3' and p['board'] == 'mixer_master'], key=lambda p: (p['cut'][1], -p['cut'][2]))
BODIES = not CASE or DETAIL  # part bodies down to the boards, when the boards are shown
for p in S['parts']:
    k, c = p['kind'], p['cut']
    x, y = c[1], c[2]
    zt = ZT.get(p['board'], 22.6)
    if k in ('pot', 'pot_dual'):
        knob(x, y, 15 if k == 'pot' else 17, 16, cap_colour(p['val']))
        if BODIES:
            box(x, y, zt, 9.8, 11, 10, POTBLUE); cyl(x, y, zt + 10, 7, 5, NICKEL, 24); cyl(x, y, zt + 15, 6, Z_PLATE_TOP + 1 - zt - 15, STEEL, 24)
    elif k == 'encoder':
        cyl(x, y, Z_PLATE_TOP + 1, 14, 15, NICKEL); cyl(x, y, Z_PLATE_TOP + 15.9, 11, 0.2, BLACK)
        if BODIES:
            box(x, y, zt, 12, 13, 4.5, STEEL); cyl(x, y, zt + 4.5, 7, 7, NICKEL, 24); cyl(x, y, zt + 11.5, 6, Z_PLATE_TOP + 1 - zt - 11.5, STEEL, 24)
    elif k == 'fader':
        travel = c[4] - 5
        fy = y - travel * 0.25                                            # three quarters up
        box(x, fy, Z_PLATE_TOP + 4, 12, 20, 9, BLACK); box(x, fy, Z_PLATE_TOP + 13, 12.2, 1.2, 0.2, WHITE)
        cyl(x, fy, Z_PLATE_TOP, 1.2, 4, NICKEL, 12)
        if BODIES:
            box(x, y, zt, 9, travel + 15, 6.5, STEEL); box(x, fy, zt + 6.5, 1.2, 4, Z_PLATE_TOP + 4 - zt - 6.5, STEEL)
    elif k == 'pva':
        w, l = c[3] - 1.5, c[4] - 1.5
        box(x, y, Z_PLATE_TOP - 0.5, w, l, 5.5, CAPS['red'] if '48' in p['val'] else CAPS['grey'])
        if BODIES: box(x, y, zt, c[3] - 0.5, c[4] - 0.5, 11, WHITE)
    elif k in ('led3', 'led5'):
        if k == 'led3' and p in meter:
            i = meter.index(p) % 10; col = (0.1, 1, 0.15) if i < 6 else (1, 0.75, 0.05) if i < 8 else (1, 0.05, 0.02)
            lit = i < 5
        else:
            col, lit = (1, 0.05, 0.02), k == 'led5'
        d = 3 if k == 'led3' else 5
        cyl(x, y, Z_PLATE_TOP - 0.5, d, 1.6 if k == 'led3' else 2.5, mat(f'led {col} {lit}', col, 0, 0.2, 6 if lit else 0.0), 16)
        if BODIES: cyl(x, y, zt, d, Z_PLATE_TOP - 0.5 - zt, mat(f'led body {col}', col, 0, 0.15), 16)
    elif k == 'jack35':
        cyl(x, y, Z_PLATE_TOP, 12, 0.6, NICKEL, 6); cyl(x, y, Z_PLATE_TOP + 0.6, 8, 2, NICKEL, 6); cyl(x, y, Z_PLATE_TOP + 2.65, 3.6, 0.1, HOLE, 16)
        if BODIES: box(x, y - 2, zt, 9, 10.5, 10.4, BLACK); cyl(x, y, zt + 10.4, 6, Z_PLATE_TOP - zt - 10.4, NICKEL, 24)
    elif k == 'tact':
        cyl(x, y, Z_PLATE_TOP, 7, 6, BLACK, 32)
    elif k == 'latch':
        cyl(x, y, Z_PLATE_TOP, 6, 5, CAPS['white'], 32)
    elif k == 'combo':
        cyl(x, y, Z_SHELF_TOP, 23.5, 4.2, BLACK); cyl(x, y, Z_SHELF_TOP + 4.25, 18, 0.1, HOLE)
        cyl(x, y + 3, Z_SHELF_TOP + 4.3, 6.5, 0.1, NICKEL, 24)
        box(x - 9, y - 6, Z_SHELF_TOP + 4.2, 4, 2, 0.6, NICKEL)          # latch tab
        if BODIES: box(x, y, zt, 26, 31, Z_SHELF_TOP - zt, BLACK)
    elif k == 'xlr':
        cyl(x, y, Z_SHELF_TOP, 23, 1.2, NICKEL); cyl(x, y, Z_SHELF_TOP + 1.25, 17, 0.1, BLACK)
        for a in (90, 210, 330):
            cyl(x + 4.5 * math.cos(math.radians(a)), y + 4.5 * math.sin(math.radians(a)), Z_SHELF_TOP + 1.2, 1.6, 3, NICKEL, 12)
        if BODIES: box(x, y, zt, 26, 31, Z_SHELF_TOP - zt, BLACK)
    elif k == 'trs':
        cyl(x, y, Z_SHELF_TOP, 15, 3.5, BLACK, 32); cyl(x, y, Z_SHELF_TOP + 3.55, 7, 0.1, HOLE, 24)
        if BODIES: box(x, y, zt, 13, 15, Z_SHELF_TOP - zt, BLACK)

# 2.8" display under the shelf window, lit
tx, ty = S['tft']
box(tx, ty, 42.5, 86, 50, 1.6, mat('tft pcb', (0.45, 0.03, 0.03))); box(tx - 4, ty, 44.1, 69.2, 50, 2.5, BLACK)
box(tx - 4, ty, 46.6, 57.6, 43.2, 0.05, mat('screen', (0.05, 0.25, 0.9), 0, 0.1, 2.5))

if EXPLODE:  # boards, parts and display ride together on their own layer between the tray and the top
    layer = bpy.data.objects.new('boards layer', None); scene.collection.objects.link(layer); layer.parent = rig
    layer.location.z = 30 * MM
    for o in set(bpy.data.objects) - before_boards:
        if o.parent is rig and o is not layer: o.parent = layer

# ---------------- feet (with the case), floor, lights, cameras ----------------
if CASE and not DETAIL:
    rig.location = (0, 0, 8 * MM); rig.rotation_euler = (math.radians(10), 0, 0)
    bpy.ops.wm.stl_import(filepath=os.path.join(STL, 'rear_foot_x2.stl'), global_scale=MM)
    foot = bpy.context.selected_objects[0]; foot.data.materials.append(PLA)
    for i, fx in enumerate((25, 382)):
        f = foot if i == 0 else foot.copy()
        if i: scene.collection.objects.link(f)
        f.location = (fx * MM, (D - 20) * math.cos(math.radians(10)) * MM, 0)
        rf = cyl(fx, D - 20, -8, 14, 8, RUBBER); rf.parent = None; rf.location.z = 0.004  # front rubber feet

bpy.ops.mesh.primitive_plane_add(size=6, location=(0.2, 0.2, 0))
bpy.context.object.data.materials.append(mat('table', (0.12, 0.115, 0.11), 0, 0.7))

world = bpy.data.worlds.new('world'); scene.world = world; world.use_nodes = True
world.node_tree.nodes['Background'].inputs['Color'].default_value = (0.6, 0.62, 0.66, 1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.12
def light(name, kind, loc, energy, size=1.0):
    l = bpy.data.lights.new(name, kind); l.energy = energy
    if kind == 'AREA': l.size = size
    o = bpy.data.objects.new(name, l); o.location = loc; scene.collection.objects.link(o)
    return o
key = light('key', 'AREA', (-0.4, -0.5, 0.9), 45, 1.2)
fill = light('fill', 'AREA', (0.9, -0.2, 0.6), 14, 1.0)
rim = light('rim', 'AREA', (0.2, 0.9, 0.9), 50, 2.5)
target = bpy.data.objects.new('target', None); target.location = (0.205, 0.17, 0.07 if CASE else 0.03); scene.collection.objects.link(target)
for o in (key, fill, rim):
    t = o.constraints.new('TRACK_TO'); t.target = target

def camera(name, loc, lens=None, ortho=None):
    cd = bpy.data.cameras.new(name)
    if ortho: cd.type = 'ORTHO'; cd.ortho_scale = ortho
    else: cd.lens = lens
    cd.clip_end = 50
    o = bpy.data.objects.new(name, cd); o.location = loc; scene.collection.objects.link(o)
    t = o.constraints.new('TRACK_TO'); t.target = target
    return o

hero = camera('hero', (-0.12, -0.52, 0.42), lens=40)
top = camera('top', (0, 0, 0), ortho=0.6)
top.constraints.clear()
if CASE: top.rotation_euler = (math.radians(10), 0, 0); top.location = (0.2035, -0.076, 1.46)  # square to the tilted deck
else: top.location = (0.2035, 0.1765, 1.5)

scene.render.engine = 'CYCLES'; scene.cycles.samples = int(os.environ.get('SAMPLES', 96)); scene.cycles.use_denoising = True
scene.render.resolution_x, scene.render.resolution_y = 1920, 1200
scene.render.resolution_percentage = int(os.environ.get('PCT', 100))
only = os.environ.get('ONLY')
scene.view_settings.view_transform = 'AgX'
tag = '' if CASE else 'boards_'
shots = ((hero, f'render_{tag}hero.png'), (top, f'render_{tag}top.png'))
if DETAIL:
    target.location = (0.2035, 0.17, 0.13 if EXPLODE else 0.02)
    shots = ((camera('exploded', (-0.38, -0.62, 0.62), lens=33), 'render_case_exploded.png'),) if EXPLODE else             ((camera('front', (-0.15, -0.5, 0.38), lens=40), 'render_case_front.png'), (camera('rear', (0.72, 0.82, 0.32), lens=40), 'render_case_rear.png'))
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, 'mixer_case_detail.blend' if DETAIL else 'mixer_assembled.blend' if CASE else 'mixer_boards.blend'))
for cam, fn in shots:
    if only and only not in fn: continue
    scene.camera = cam; scene.render.filepath = os.path.join(OUT, fn)
    bpy.ops.render.render(write_still=True)
print('RENDER DONE')
