# Photo-style render of the assembled mixer. Run after panels.py and case.py:
#   "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P render_blender.py
# Builds the scene from render_scene.json (panel outlines, holes, part positions) and ../stl, saves ../out/mixer_assembled.blend
# and renders ../out/render_hero.png and ../out/render_top.png. Knobs, caps and jack noses are stand-ins, not real models.
import bpy, bmesh, json, os, math
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'out')
S = json.load(open(os.path.join(HERE, 'render_scene.json')))
D, MM = 353.0, 0.001
Z_PLATE_TOP, Z_SHELF_TOP = 35.1, 48.1
P = lambda x, y, z: (x * MM, (D - y) * MM, z * MM)  # case coords (mm) -> Blender (m), front at y = 0

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

ALU = mat('brushed aluminium', (0.78, 0.79, 0.81), 0.9, 0.38)
PLA = mat('dark grey PLA', (0.045, 0.048, 0.055), 0.0, 0.55)
BLACK = mat('black plastic', (0.012, 0.012, 0.014), 0.0, 0.4)
RUBBER = mat('black rubber', (0.02, 0.02, 0.02), 0.0, 0.8)
NICKEL = mat('nickel', (0.75, 0.75, 0.73), 1.0, 0.2)
HOLE = mat('hole', (0.0, 0.0, 0.0), 0.0, 1.0)
WHITE = mat('print white', (0.9, 0.9, 0.9), 0.0, 0.6)
INK = mat('print ink', (0.02, 0.02, 0.025), 0.0, 0.5)
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

# ---------------- printed case ----------------
STL = os.path.join(HERE, '..', 'stl')
for f in sorted(os.listdir(STL)):
    if not f.endswith('.stl') or f.startswith('rear_foot'): continue
    bpy.ops.wm.stl_import(filepath=os.path.join(STL, f), global_scale=MM)
    o = bpy.context.selected_objects[0]
    link(o, BLACK if f.startswith(('armrest', 'esp32')) else PLA)

# ---------------- aluminium pieces with their holes ----------------
def prism(pts, z0, h, name='prism'):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    f = bm.faces.new([bm.verts.new(P(x, y, z0)) for x, y in pts])
    ext = bmesh.ops.extrude_face_region(bm, geom=[f])
    bmesh.ops.translate(bm, vec=Vector((0, 0, h * MM)), verts=[e for e in ext['geom'] if isinstance(e, bmesh.types.BMVert)])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); scene.collection.objects.link(o); o.data.materials.append(ALU)
    return o

def panel(name, z0, t):
    pc = S['pieces'][name]
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    vs = [bm.verts.new(P(x, y, z0)) for x, y in pc['outline']]
    face = bm.faces.new(vs); bmesh.ops.recalc_face_normals(bm, faces=[face])
    if face.normal.z < 0: face.normal_flip()
    ext = bmesh.ops.extrude_face_region(bm, geom=[face])
    bmesh.ops.translate(bm, vec=Vector((0, 0, t * MM)), verts=[e for e in ext['geom'] if isinstance(e, bmesh.types.BMVert)])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)  # the original face is now the bottom; make the solid consistent for the boolean
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); scene.collection.objects.link(o); link(o, ALU)
    cutters = []
    for c in pc['holes']:
        if c[0] == 'circle':
            cutters.append(cyl(c[1], c[2], z0 - 1, c[3], t + 2, ALU, 32))
        elif c[0] == 'rect':
            cutters.append(box(c[1], c[2], z0 - 1, c[3], c[4], t + 2, ALU))
        else:
            r, h = c[3] / 2, c[4] / 2 - c[3] / 2  # one capsule prism: overlapping pieces upset the boolean
            pts = [(c[1] + r * math.cos(a), c[2] - h - r * math.sin(a)) for a in [math.pi * i / 24 for i in range(25)]]
            pts += [(c[1] - r * math.cos(a), c[2] + h + r * math.sin(a)) for a in [math.pi * i / 24 for i in range(25)]]
            cutters.append(prism(pts, z0 - 1, t + 2))
    bpy.ops.object.select_all(action='DESELECT')
    for k in cutters: k.select_set(True)
    bpy.context.view_layer.objects.active = cutters[0]; bpy.ops.object.join()
    cut = bpy.context.object
    mod = o.modifiers.new('holes', 'BOOLEAN'); mod.operation = 'DIFFERENCE'; mod.object = cut; mod.solver = 'MANIFOLD'  # EXACT ate most of the notched plate
    bpy.context.view_layer.objects.active = o; bpy.ops.object.modifier_apply(modifier='holes')
    bpy.data.objects.remove(cut)
    bm = bmesh.new(); bm.from_mesh(o.data)  # clean the boolean's triangles: merge coplanar faces, consistent normals
    bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(0.5), verts=bm.verts, edges=bm.edges)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(o.data); bm.free()
    for f in o.data.polygons: f.use_smooth = False
    dx = o.dimensions.x / MM
    assert abs(dx - 407) < 0.5, f'{name}: boolean went wrong, width {dx:.1f} mm'
    return o

panel('plate', Z_PLATE_TOP - 2.0, 2.0)
panel('shelf', Z_SHELF_TOP - 1.5, 1.5)

# ---------------- controls (stand-ins) ----------------
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
for p in S['parts']:
    k, c = p['kind'], p['cut']
    x, y = c[1], c[2]
    if k in ('pot', 'pot_dual'):
        knob(x, y, 15 if k == 'pot' else 17, 16, cap_colour(p['val']))
    elif k == 'encoder':
        cyl(x, y, Z_PLATE_TOP + 1, 14, 15, ALU); cyl(x, y, Z_PLATE_TOP + 15.9, 11, 0.2, BLACK)
    elif k == 'fader':
        travel = c[4] - 5
        fy = y - travel * 0.25                                            # three quarters up
        box(x, fy, Z_PLATE_TOP + 4, 12, 20, 9, BLACK); box(x, fy, Z_PLATE_TOP + 13, 12.2, 1.2, 0.2, WHITE)
        cyl(x, fy, Z_PLATE_TOP, 1.2, 4, NICKEL, 12)
    elif k == 'pva':
        w, l = c[3] - 1.5, c[4] - 1.5
        box(x, y, Z_PLATE_TOP - 0.5, w, l, 5.5, CAPS['red'] if '48' in p['val'] else CAPS['grey'])
    elif k == 'led3':
        if p['board'] == 'mixer_master' and p in meter:
            i = meter.index(p) % 10; col = (0.1, 1, 0.15) if i < 6 else (1, 0.75, 0.05) if i < 8 else (1, 0.05, 0.02)
            lit = i < 5
        else:
            col, lit = (1, 0.05, 0.02), False
        cyl(x, y, Z_PLATE_TOP - 0.5, 3, 1.6, mat(f'led {col} {lit}', col, 0, 0.2, 6 if lit else 0.0), 16)
    elif k == 'led5':
        cyl(x, y, Z_PLATE_TOP - 0.5, 5, 2.5, mat('led5 red lit', (1, 0.05, 0.02), 0, 0.2, 5), 24)
    elif k == 'jack35':
        cyl(x, y, Z_PLATE_TOP, 12, 0.6, NICKEL, 6); cyl(x, y, Z_PLATE_TOP + 0.6, 8, 2, NICKEL, 6); cyl(x, y, Z_PLATE_TOP + 2.65, 3.6, 0.1, HOLE, 16)
    elif k == 'tact':
        cyl(x, y, Z_PLATE_TOP, 7, 6, BLACK, 32)
    elif k == 'latch':
        cyl(x, y, Z_PLATE_TOP, 6, 5, CAPS['white'], 32)
    elif k == 'combo':
        cyl(x, y, Z_SHELF_TOP, 23.5, 4.2, BLACK); cyl(x, y, Z_SHELF_TOP + 4.25, 18, 0.1, HOLE)
        cyl(x, y + 3, Z_SHELF_TOP + 4.3, 6.5, 0.1, NICKEL, 24)
        box(x - 9, y - 6, Z_SHELF_TOP + 4.2, 4, 2, 0.6, NICKEL)          # latch tab
    elif k == 'xlr':
        cyl(x, y, Z_SHELF_TOP, 23, 1.2, NICKEL); cyl(x, y, Z_SHELF_TOP + 1.25, 17, 0.1, BLACK)
        for a in (90, 210, 330):
            cyl(x + 4.5 * math.cos(math.radians(a)), y + 4.5 * math.sin(math.radians(a)), Z_SHELF_TOP + 1.2, 1.6, 3, NICKEL, 12)
    elif k == 'trs':
        cyl(x, y, Z_SHELF_TOP, 15, 3.5, BLACK, 32); cyl(x, y, Z_SHELF_TOP + 3.55, 7, 0.1, HOLE, 24)

# display under the shelf window, lit
tx, ty = S['tft']
box(tx, ty, Z_SHELF_TOP - 4, 70, 52, 2.5, BLACK)
screen = box(tx, ty, Z_SHELF_TOP - 1.5, 58, 43.5, 0.05, mat('screen', (0.05, 0.25, 0.9), 0, 0.1, 2.5))

# printed overlay labels
for x, y, text, piece in S['labels']:
    cu = bpy.data.curves.new(text, 'FONT'); cu.body = text; cu.size = 2.4 * MM; cu.align_x = 'CENTER'; cu.align_y = 'CENTER'
    o = bpy.data.objects.new(text, cu); scene.collection.objects.link(o)
    o.location = P(x, y + 1.5, (Z_PLATE_TOP if piece == 'plate' else Z_SHELF_TOP) + 0.02); link(o, INK)

# ---------------- tilt on feet, floor, lights, cameras ----------------
rig.location = (0, 0, 8 * MM); rig.rotation_euler = (math.radians(10), 0, 0)
bpy.ops.wm.stl_import(filepath=os.path.join(STL, 'rear_foot_x2.stl'), global_scale=MM)
foot = bpy.context.selected_objects[0]; foot.data.materials.append(PLA)
for i, fx in enumerate((25, 382)):
    f = foot if i == 0 else foot.copy()
    if i: scene.collection.objects.link(f)
    f.location = (fx * MM, (D - 20) * math.cos(math.radians(10)) * MM, 0)
    cyl(fx, D - 20, -8, 14, 8, RUBBER).parent = None
for o in [o for o in scene.objects if o.parent is None and o.type == 'MESH' and o.name.startswith('Cylinder')]:
    o.location.z = 0.004  # front rubber feet sit on the floor

bpy.ops.mesh.primitive_plane_add(size=6, location=(0.2, 0.2, 0))
link(bpy.context.object, mat('table', (0.12, 0.115, 0.11), 0, 0.7)).parent = None

world = bpy.data.worlds.new('world'); scene.world = world; world.use_nodes = True
world.node_tree.nodes['Background'].inputs['Color'].default_value = (0.6, 0.62, 0.66, 1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.12
def light(name, kind, loc, energy, size=1.0, rot=(0, 0, 0)):
    l = bpy.data.lights.new(name, kind); l.energy = energy
    if kind == 'AREA': l.size = size
    o = bpy.data.objects.new(name, l); o.location = loc; o.rotation_euler = rot; scene.collection.objects.link(o)
    return o
key = light('key', 'AREA', (-0.4, -0.5, 0.9), 45, 1.2)
fill = light('fill', 'AREA', (0.9, -0.2, 0.6), 12, 1.0)
rim = light('rim', 'AREA', (0.2, 0.9, 0.9), 50, 2.5)  # big softbox behind: what the aluminium reflects toward the camera
target = bpy.data.objects.new('target', None); target.location = (0.205, 0.17, 0.07); scene.collection.objects.link(target)
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
top.constraints.clear(); top.rotation_euler = (math.radians(10), 0, 0); top.location = (0.2035, -0.076, 1.46)  # square to the tilted deck

scene.render.engine = 'CYCLES'; scene.cycles.samples = int(os.environ.get('SAMPLES', 96)); scene.cycles.use_denoising = True
scene.render.resolution_x, scene.render.resolution_y = 1920, 1200
scene.render.resolution_percentage = int(os.environ.get('PCT', 100))
only = os.environ.get('ONLY')
scene.view_settings.view_transform = 'AgX'
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, 'mixer_assembled.blend'))
for cam, fn in ((hero, 'render_hero.png'), (top, 'render_top.png')):
    if only and only not in fn: continue
    scene.camera = cam; scene.render.filepath = os.path.join(OUT, fn)
    bpy.ops.render.render(write_still=True)
print('RENDER DONE')
