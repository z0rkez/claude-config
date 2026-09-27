# claude-config

Конфиг Claude Code: хуки, скилы, агенты, фреймворк GSD, MCP-серверы, настройки.

## Установка

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/z0rkez/claude-config/main/install.sh)
```

Скрипт клонирует репозиторий в `~/.claude`, ставит gstack и ObsidianDataWeave, прописывает MCP-серверы в `~/.claude.json` и спрашивает недостающие API-ключи.

Личная часть (инструкции, память, настройки) лежит в отдельном приватном репозитории и подтягивается, если `gh` авторизован под владельцем. Без неё используется `settings.example.json`.

## Обновление

```bash
cd ~/.claude
python3 mcp.py export                                   # если менялись MCP-серверы
git add -A && git commit -m "..." && git push           # публичная часть
git --git-dir=.private.git add -f CLAUDE.md profile.md settings.json settings.local.json \
  hooks/private-guard.names projects/*/memory
git --git-dir=.private.git commit -m "..." && git --git-dir=.private.git push
```

`settings.example.json` это копия `settings.json` без `autoMode.environment`.

## Что не в git

| Что | Почему |
|---|---|
| `.credentials.json`, `secrets.env` | секреты |
| история чатов, `sessions/` | личное |
| `plugins/`, `skills/synced/` | ставятся автоматически |
| `skills/gstack` | клонируется из garrytan/gstack |
| `cache/`, `telemetry/`, `file-history/`, `*.bak*` | мусор |
