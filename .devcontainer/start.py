"""Start both services when the Codespace starts, with no terminal commands."""
from pathlib import Path
import subprocess
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PYTHON = ROOT / '.codespaces-venv/bin/python'
LOGS = ROOT / '.codespaces-logs'
LOGS.mkdir(exist_ok=True)

def healthy(url):
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            return response.status == 200
    except Exception:
        return False

def start(name, args, url):
    if healthy(url):
        return
    with (LOGS / f'{name}.log').open('a') as log:
        process = subprocess.Popen([str(PYTHON), *args], cwd=ROOT,
                                   stdout=log, stderr=subprocess.STDOUT,
                                   start_new_session=True)
    for _ in range(90):
        if healthy(url):
            return
        if process.poll() is not None:
            raise RuntimeError(f'{name} stopped. See {LOGS / (name + ".log")}')
        time.sleep(1)
    raise RuntimeError(f'{name} did not start. See {LOGS / (name + ".log")}')

start('api', ['-m', 'uvicorn', 'api.main:app', '--app-dir', 'src',
              '--host', '127.0.0.1', '--port', '8000'],
      'http://127.0.0.1:8000/health')
start('dashboard', ['-m', 'streamlit', 'run', 'app/streamlit_app.py',
                    '--server.address=0.0.0.0', '--server.port=8501',
                    '--server.headless=true', '--browser.gatherUsageStats=false'],
      'http://127.0.0.1:8501/_stcore/health')
print('Dashboard ready. Open port 8501 in the Ports panel if it did not open automatically.')
