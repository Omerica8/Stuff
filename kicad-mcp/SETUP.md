# KiCad MCP server setup (Windows)

Server: [mixelpixx/KiCAD-MCP-Server](https://github.com/mixelpixx/KiCAD-MCP-Server), tag **v2.8.2** (commit `670d2a9c48e1588f2e07edaf656b5e301fc55a50`). I read the repo on 2026-10-20 at `main` (`cbb59a6`).

## What the pasted plan gets wrong for this server

| Plan says | What the code actually does |
|---|---|
| No network calls | It has online tools: JLCPCB (`python/commands/jlcpcb.py`, `jlcpcb_downloader.py`), jlcsearch, PartReel parts registry (`src/tools/parts-registry.ts`), LCSC datasheets (`src/tools/datasheet.ts`). They only run when Claude calls those tools. |
| Subprocesses: kicad-cli, git, ngspice only | Also Java or Docker for Freerouting (`python/commands/freerouting.py`), 7-Zip (`python/utils/seven_zip.py`), and `ps`. |
| Hash-locked dependency file | None. `requirements.txt` uses `>=` ranges. Only the Node side is locked (`package-lock.json`). |
| A "build (write) profile" limited to one folder | No such setting exists. The server can write anywhere your user account can. |
| stdio, no network port | True. It runs as `node dist/index.js` over stdio. |

So steps 2 and 4 need the workarounds below. The real safety comes from the git sandbox plus Claude Code deny rules.

## 1. Pinned private copy

On GitHub, create an empty **private** repo, e.g. `Omerica8/kicad-mcp-pinned`. Then in PowerShell:

```powershell
cd $HOME\tools
git clone https://github.com/mixelpixx/KiCAD-MCP-Server.git kicad-mcp
cd kicad-mcp
git checkout v2.8.2
git remote rename origin upstream
git remote add origin https://github.com/Omerica8/kicad-mcp-pinned.git
git push -u origin HEAD:main
```

From here on, only pull upstream changes after reading the diff (`git fetch upstream; git diff v2.8.2 upstream/main`).

## 2. Install with locked dependencies

Node side (locked by `package-lock.json`):

```powershell
npm ci
npm run build
```

Python side: use KiCad's bundled Python so it can import KiCad's modules. Generate a hash-locked file once, commit it, and install from it:

```powershell
$py = "C:\Program Files\KiCad\9.0\bin\python.exe"   # adjust to your KiCad version
& $py -m pip install pip-tools
& $py -m piptools compile --generate-hashes -o requirements.lock requirements.txt
& $py -m pip install --require-hashes -r requirements.lock
git add requirements.lock; git commit -m "Lock Python deps with hashes"; git push
```

## 3. Register with Claude Code (stdio)

```powershell
claude mcp add kicad --scope user -e KICAD_PYTHON="C:\Program Files\KiCad\9.0\bin\python.exe" -- node "$HOME\tools\kicad-mcp\dist\index.js"
claude mcp list
```

## 4. Sandbox folder under git, plus deny rules

```powershell
mkdir $HOME\kicad-sandbox; cd $HOME\kicad-sandbox
git init
# put or create the controller's KiCad project here, then:
git add -A; git commit -m "Baseline"
```

Always start Claude Code from inside this folder. Since the server itself can't be confined, block its online tools there. Create `.claude\settings.json` in the sandbox:

```json
{
  "permissions": {
    "deny": [
      "mcp__kicad__download_jlcpcb_database",
      "mcp__kicad__search_jlcpcb_parts",
      "mcp__kicad__get_jlcpcb_part",
      "mcp__kicad__suggest_jlcpcb_alternatives",
      "mcp__kicad__search_parts_registry",
      "mcp__kicad__get_registry_part",
      "mcp__kicad__download_registry_part",
      "mcp__kicad__enrich_datasheets",
      "mcp__kicad__get_datasheet_url"
    ]
  }
}
```

Run `/mcp` inside Claude Code once to see the full tool list and add any other online tools you don't want. After each session, review with `git status` and `git diff`, and undo with `git restore .` (or `git reset --hard` to the last commit).

## 5. Enable the KiCad API

KiCad 9 or later: **Preferences > Preferences > Plugins**, tick **Enable KiCad API**, then restart KiCad. Keep KiCad open with the sandbox project loaded when you use the server.
