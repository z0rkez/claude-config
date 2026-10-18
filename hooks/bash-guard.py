#!/usr/bin/env python3
"""PreToolUse Bash: блокирует разрушительные команды.

Список намеренно короткий: только то, что не откатить. Обычные rm внутри
проекта, git reset на ветке и прочее не трогаем.
"""

import json
import os
import re
import sys

_H = os.path.expanduser("~").replace("\\", "/")
HOME = rf"(?:~|\$HOME|\$\{{HOME\}}|{re.escape(_H)})"
# Цели, для которых rm -r* запрещён.
RM_TARGETS = rf"(?:/|/\*|{HOME}/?|{HOME}/\*|/home/?|/etc/?|/usr/?|/var/?|/boot/?|/opt/?|\*|\.\.|{HOME}/Notes/?|{HOME}/\.claude/?|{HOME}/projects/?)"

RULES = [
    (rf"\brm\s+(?:-[a-zA-Z]*r[a-zA-Z]*\s+)+(?:\S+\s+)*{RM_TARGETS}(?:\s|$|;|&|\|)", "rm -r по корню, дому, Notes, .claude или projects"),
    (r"\bgit\s+push\b(?!.*--force-with-lease).*(?:\s--force\b|\s-f\b)", "git push --force"),
    (r"\bgit\s+reset\s+--hard\b", "git reset --hard"),
    (r"\bgit\s+clean\s+-[a-zA-Z]*f", "git clean -f"),
    (r"\bmkfs(?:\.\w+)?\b", "mkfs"),
    (r"\bwipefs\b", "wipefs"),
    (r"\bdd\b.*\bof=/dev/", "dd на устройство"),
    (r">\s*/dev/(?:sd|nvme|mmcblk|vd)", "запись в блочное устройство"),
    (r"\bchmod\s+(?:-R|--recursive)\s+[0-7]{3,4}\s+/(?:\s|$)", "chmod -R на корень"),
    (r"\bchown\s+(?:-R|--recursive)\b.*\s/(?:\s|$)", "chown -R на корень"),
    (r"\b(?:curl|wget)\b[^|]*\|\s*(?:sudo\s+)?(?:ba|z|da)?sh\b", "curl | sh"),
    (r":\(\)\s*\{\s*:\|:&\s*\};:", "fork bomb"),
]

try:
    data = json.load(sys.stdin)
except ValueError:
    sys.exit(0)

cmd = data.get("tool_input", {}).get("command", "")
for pattern, label in RULES:
    if re.search(pattern, cmd):
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": (
                    f"bash-guard: заблокировано ({label}). Если это действительно "
                    "нужно, пользователь выполняет команду сам через «!»."
                ),
            }
        }, ensure_ascii=False))
        sys.exit(0)
