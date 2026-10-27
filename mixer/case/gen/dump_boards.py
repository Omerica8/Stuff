# Run with KiCad's python: dumps board outline + every footprint (ref, lib name, value, pos, rot, side, Fab geometry) to boards.json
import pcbnew, json, sys, os
SB = sys.argv[1]  # kicad-sandbox folder
t = pcbnew.ToMM
out = {}
for name in ['mixer_strip','mixer_stereo','mixer_master','controller','mixer_digital','mixer_power','mixer_reverb','mixer_midi']:
    b = pcbnew.LoadBoard(os.path.join(SB, name, name + '.kicad_pcb'))
    bb = b.GetBoardEdgesBoundingBox()
    fps = []
    for f in b.GetFootprints():
        p = f.GetPosition()
        fab = []
        for g in f.GraphicalItems():
            if isinstance(g, pcbnew.PCB_SHAPE) and g.GetLayer() == pcbnew.F_Fab:
                if g.GetShape() == pcbnew.SHAPE_T_CIRCLE:
                    c = g.GetCenter(); fab.append(['c', t(c.x), t(c.y), t(g.GetRadius())])
                else:
                    r = g.GetBoundingBox(); fab.append(['b', t(r.GetLeft()), t(r.GetTop()), t(r.GetRight()), t(r.GetBottom())])
        fps.append(dict(ref=f.GetReference(), lib=str(f.GetFPID().GetLibItemName()), val=f.GetValue(),
                        x=t(p.x), y=t(p.y), rot=f.GetOrientationDegrees(), back=f.IsFlipped(), fab=fab))
    out[name] = dict(edge=[t(bb.GetLeft()), t(bb.GetTop()), t(bb.GetRight()), t(bb.GetBottom())], fps=fps)
json.dump(out, open(sys.argv[2], 'w'), indent=0)
print({k: v['edge'] for k, v in out.items()})
