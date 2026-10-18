#!/usr/bin/env python3
"""Notification-хук: уведомление через нативный механизм платформы."""
import json
import os
import platform
import subprocess
import sys

ICON = os.path.expanduser("~/.claude/hooks/assets/clawd.png")
TEXT = {
    "permission_prompt": "Нужно разрешение",
    "idle_prompt": "Жду ответа",
    "elicitation_dialog": "Нужен ответ на вопрос",
    "auth_success": "Вход выполнен",
}

try:
    data = json.load(sys.stdin)
except Exception:
    data = {}

kind = data.get("notification_type", "")
msg = data.get("message", "")
body = TEXT.get(kind)
if not body:
    if "permission" in msg.lower():
        body = "Нужно разрешение"
    elif "waiting" in msg.lower():
        body = "Жду ответа"
    else:
        body = "Claude ждёт"

urgency = "critical" if body == "Нужно разрешение" else "normal"
system = platform.system()

if system == "Linux":
    subprocess.run([
        "notify-send", "-a", "Claude Code", "-i", ICON, "-u", urgency,
        "-h", "string:x-dunst-stack-tag:claude-code",
        body,
    ], check=False)
elif system == "Darwin":
    subprocess.run([
        "osascript", "-e",
        f'display notification "{body}" with title "Claude Code"',
    ], check=False)
elif system == "Windows":
    ps = (
        "Add-Type -AssemblyName System.Windows.Forms;"
        f'$n = New-Object System.Windows.Forms.NotifyIcon;'
        "$n.Icon = [System.Drawing.SystemIcons]::Information;"
        "$n.Visible = $true;"
        f'$n.ShowBalloonTip(3000, "Claude Code", "{body}", [System.Windows.Forms.ToolTipIcon]::Info);'
        "Start-Sleep -Milliseconds 3500; $n.Dispose()"
    )
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=False)
