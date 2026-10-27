# Project wiki

Two linked builds by Omer, all on the `mixer` branch of Omerica8/Stuff:

1. **FL Studio MIDI controller**: ESP32-S3 with 4 faders, 4 encoders, a 2.8" TFT and buttons, sending USB MIDI to FL Studio.
2. **Full-size analog mixer** (Yamaha MG10XU style): 4 mic strips, 2 stereo strips, master, power, digital (USB audio + MIDI) and reverb boards. The controller becomes the mixer's MIDI section.

| Page | What's in it |
|---|---|
| [architecture.md](architecture.md) | How the system fits together: signal flow, buses, power, grounding, USB |
| [boards.md](boards.md) | Each PCB: size, state, connectors and pinouts, where its files are |
| [firmware.md](firmware.md) | Controller firmware steps, pin map, MIDI map, FL Studio API limits |
| [parts.md](parts.md) | Key parts, long-lead items, where BOMs and shopping lists are |
| [case.md](case.md) | Enclosure plan and the numbers it depends on |
| [decisions.md](decisions.md) | Dated decision log and what's still open |
| [tooling.md](tooling.md) | KiCad MCP setup, generators, OpenSCAD, how this wiki updates itself |
| [files.md](files.md) | Generated list of every doc and source file (don't edit by hand) |

The READMEs and PARTS.md files next to each design stay the source of truth. These pages summarise them and point to them. When a page and its source disagree, the source wins, and the page needs updating.
