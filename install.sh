#!/usr/bin/env bash
# Раскатка конфига Claude Code на новой машине.
# Требует: git, python3; для личной части gh, авторизованный как z0rkez.
set -euo pipefail

PUB=https://github.com/z0rkez/claude-config
PRIV=z0rkez/claude-private
DEST="$HOME/.claude"

# 1. Публичный репозиторий в ~/.claude (поверх существующего каталога, если он есть)
if [ ! -d "$DEST/.git" ]; then
  tmp=$(mktemp -d)
  git clone "$PUB" "$tmp/c"
  mkdir -p "$DEST"
  [ -f "$DEST/settings.json" ] && cp "$DEST/settings.json" "$DEST/settings.json.bak.install"
  cp -a "$tmp/c/." "$DEST/"
  rm -rf "$tmp"
else
  git -C "$DEST" pull --ff-only
fi

# 2. Личная часть: инструкции, память, настройки. Без доступа берутся публичные настройки
if command -v gh >/dev/null && gh repo view "$PRIV" >/dev/null 2>&1; then
  if [ ! -d "$DEST/.private.git" ]; then
    gh repo clone "$PRIV" "$DEST/.private.git" -- --bare
    git --git-dir="$DEST/.private.git" config core.bare false
    git --git-dir="$DEST/.private.git" config core.worktree "$DEST"
    git --git-dir="$DEST/.private.git" checkout -f
  else
    git --git-dir="$DEST/.private.git" pull --ff-only
  fi
else
  echo "Нет доступа к $PRIV, ставлю публичные настройки"
  [ -f "$DEST/settings.json" ] || cp "$DEST/settings.example.json" "$DEST/settings.json"
fi

# 3. Сторонние скилы, которые не лежат в репозитории
[ -d "$DEST/skills/gstack" ] || git clone --depth 1 https://github.com/garrytan/gstack "$DEST/skills/gstack"
[ -d "$HOME/projects/ObsidianDataWeave" ] || git clone https://github.com/howdeploy/ObsidianDataWeave "$HOME/projects/ObsidianDataWeave"

# 4. Ядро хука zaebal
mkdir -p "$HOME/.zaebal"
rm -rf "$HOME/.zaebal/core"
cp -r "$DEST/external/zaebal-core" "$HOME/.zaebal/core"

# 5. MCP-серверы в ~/.claude.json (ключи спросит, если нет secrets.env)
python3 "$DEST/mcp.py" import

# 6. Симлинк памяти в Obsidian
[ -d "$HOME/Notes" ] && [ -d "$DEST/projects/-home-zorkez/memory" ] && [ ! -e "$HOME/Notes/LLM WIKI" ] && \
  ln -s "$DEST/projects/-home-zorkez/memory" "$HOME/Notes/LLM WIKI"

echo "Готово. Вне репозитория: rtk (~/.local/bin/rtk), ~/projects/telegram-mcp, логин в Claude Code."
