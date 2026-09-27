#!/usr/bin/env python3
"""PreToolUse: блокирует любое обращение к приватной папке хранилища.

Ищет имя папки во всех строковых аргументах вызова (путь, паттерн, команда,
запрос). Обход: touch ~/.claude/hooks/private-guard.off (снять после).
"""

import json
import os
import sys

NAMES = os.path.expanduser("~/.claude/hooks/private-guard.names")
try:
    PRIVATE = tuple(l.strip().lower() for l in open(NAMES) if l.strip())
except OSError:
    PRIVATE = ()
OFF = os.path.expanduser("~/.claude/hooks/private-guard.off")


def strings(v):
    if isinstance(v, str):
        yield v
    elif isinstance(v, dict):
        for x in v.values():
            yield from strings(x)
    elif isinstance(v, list):
        for x in v:
            yield from strings(x)


if os.path.exists(OFF):
    sys.exit(0)

try:
    data = json.load(sys.stdin)
except ValueError:
    sys.exit(0)

hit = next((s for s in strings(data.get("tool_input", {}))
            if any(p in s.lower() for p in PRIVATE)), None)
if hit is None:
    sys.exit(0)

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": (
            "Приватная папка закрыта хуком private-guard. Не обходить. "
            "Если пользователь сам попросил открыть файл оттуда, попроси его "
            "выполнить: touch ~/.claude/hooks/private-guard.off"
        ),
    }
}, ensure_ascii=False))
