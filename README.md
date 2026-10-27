# Stuff: Omer's audio projects

Home for all of Omer's audio hardware and software projects. The default branch is `mixer` and holds everything.

## Projects

| Project | Folders | State |
|---|---|---|
| FL Studio MIDI controller (ESP32-S3, faders, encoders, TFT) | [controller/](controller/), [firmware/](firmware/), [shopping/](shopping/) | PCB designed, firmware in steps |
| Full-size analog mixer (Yamaha MG10XU style) | [mixer/](mixer/) ([README](mixer/README.md)) | Boards and case in progress |

## Shared

| Folder | What's in it |
|---|---|
| [wiki/](wiki/) | Project wiki, start at [wiki/index.md](wiki/index.md) |
| [kicad-mcp/](kicad-mcp/) | Setup notes for running KiCad through MCP on Omer's PC |
| [uploads/](uploads/) | Reference photos, videos and spreadsheets Omer uploaded |

## Adding a new project

1. Give it its own top-level folder with a short kebab-case name (e.g. `guitar-pedal/`).
2. Put a `README.md` in it saying what it is and its current state.
3. Add a row to the Projects table above, and a line to [wiki/index.md](wiki/index.md).

Older versions of the controller outputs are in git history (removed from the tree on 2026-10-26).
