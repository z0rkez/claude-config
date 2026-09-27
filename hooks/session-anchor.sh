#!/usr/bin/env bash
# SessionStart: короткая сводка окружения в контекст (дата, обход блокировок, uptime).
# Вывод идёт в контекст, поэтому одна-две строки, без лишнего.

date_s=$(date '+%Y-%m-%d %H:%M %a')
up=$(uptime -p 2>/dev/null | sed 's/^up //')
bypass=$(python3 ~/.config/waybar/scripts/bypass-status.py 2>/dev/null \
    | python3 -c 'import json,sys; print(json.load(sys.stdin)["tooltip"].replace("\n", ", "))' 2>/dev/null)

echo "Сессия: ${date_s}, uptime ${up:-?}. ${bypass:-Обход: статус недоступен}."
