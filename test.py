import os
import subprocess

def run_every_startup():
    script = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.Popen([script])

run_every_startup()
