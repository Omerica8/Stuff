<!-- sources: kicad-mcp/ .claude/settings.json .githooks/ wiki/update.sh CLAUDE.md -->
# Tooling

## KiCad MCP (Omer's Windows PC)

- Server: mixelpixx/KiCAD-MCP-Server v2.8.2 at `C:\Users\pogam\kicad-mcp\server`, pinned in the private repo Omerica8/kicad-mcp-pinned. Registered in Claude Code as `kicad` (stdio).
- KiCad 10.0.7. Python: `C:\Program Files\KiCad\10.0\bin\python.exe`.
- Work in the git sandbox `C:\Users\pogam\kicad-mcp\kicad-sandbox`; its `.claude/settings.json` denies the JLCPCB/parts/datasheet tools. The server has no path confinement, so the sandbox and deny rules are the safety net.
- Remote Control must use `C:\Users\pogam\kicad-mcp` (not the home folder). Decision-card taps don't reach an RC session; Omer types answers there.
- Setup guide: [kicad-mcp/SETUP.md](../kicad-mcp/SETUP.md).

## Simulation and CAD

- ngspice (`apt install ngspice` in the cloud container) for `power_sim.cir` and `hpf.cir`; Python for `eq.py`, `mid.py`.
- OpenSCAD runs in the cloud container, not on Omer's PC.

## How this wiki stays current

- `wiki/update.sh` regenerates [files.md](files.md) and lists hand-written pages whose sources changed after the page was last committed. Each page names its sources in a `<!-- sources: ... -->` line at the top.
- A **SessionStart hook** (`.claude/settings.json`) runs it at the start of every Claude Code session, so stale pages show up in Claude's context and get fixed before answering.
- An optional **git post-commit hook** (`.githooks/post-commit`) prints the same stale list after each commit. Turn it on once per clone with `git config core.hooksPath .githooks`.
- Nothing calls an LLM automatically, so the automation costs nothing. Claude updates stale pages when it next works in the repo.
