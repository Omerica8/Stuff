# Runs the fader helper with no window (.pyw files open with pythonw). Put a shortcut to this
# file in shell:startup to start it with Windows; stop it by ending "pythonw" in Task Manager.
import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).with_name("pc_fader.py")), run_name="__main__")
