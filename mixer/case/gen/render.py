# Preview render of the printed parts plus the two aluminium pieces (flat, from the DXF outlines). uv run --with pyvista --with ezdxf
import os, glob, pyvista as pv, ezdxf
HERE = os.path.dirname(os.path.abspath(__file__)); D = 353.0
p = pv.Plotter(off_screen=True, window_size=(1600, 1100))
col = {'tray': '#9aa0a8', 'riser': '#d08a3c', 'armrest': '#33383f', 'esp32': '#33383f'}
for f in glob.glob(os.path.join(HERE, '..', 'stl', '*.stl')):
    n = os.path.basename(f)
    if n.startswith('rear_foot'): continue
    p.add_mesh(pv.read(f), color=col[n.split('_')[0]], smooth_shading=False)
for name, z, t in (('plate', 33.1, 2.0), ('shelf', 46.6, 1.5)):
    msp = ezdxf.readfile(os.path.join(HERE, '..', 'out', f'{name}.dxf')).modelspace()
    pts = [(x, D + y, 0) for x, y, *_ in next(iter(msp.query('LWPOLYLINE[layer=="OUTLINE"]'))).get_points()]
    poly = pv.MultipleLines(pts + [pts[0]]).delaunay_2d() if False else pv.PolyData(pts, faces=[len(pts)] + list(range(len(pts)))).triangulate()
    p.add_mesh(poly.extrude((0, 0, t), capping=True).translate((0, 0, z)), color='#d9dde2', opacity=0.85)
p.camera_position = [(-250, -420, 520), (203, 176, 20), (0, 0, 1)]
p.screenshot(os.path.join(HERE, '..', 'out', 'case_preview.png'))
