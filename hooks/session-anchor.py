#!/usr/bin/env python3
"""SessionStart: короткая сводка окружения (дата, uptime). Работает на Linux/macOS/Windows."""
import datetime
import platform
import subprocess
import sys

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M %a")
system = platform.system()

uptime = "?"
try:
    if system == "Linux":
        out = subprocess.check_output(["uptime", "-p"], text=True, stderr=subprocess.DEVNULL).strip()
        uptime = out.removeprefix("up ") if out.startswith("up ") else out
    elif system == "Darwin":
        out = subprocess.check_output(["uptime"], text=True, stderr=subprocess.DEVNULL).strip()
        uptime = out
    elif system == "Windows":
        import ctypes
        ms = ctypes.windll.kernel32.GetTickCount64()
        s = ms // 1000
        h, m = divmod(s // 60, 60)
        uptime = f"{h}h {m}m"
except Exception:
    pass

print(f"Сессия: {now}, uptime {uptime}.", flush=True)
