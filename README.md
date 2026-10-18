# claude-config

Конфиг Claude Code: хуки, скилы, агенты, фреймворк GSD, MCP-серверы, настройки.
Работает на Linux, macOS и Windows.

## Установка

**Linux / macOS**
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/z0rkez/claude-config/main/install.sh)
```

**Windows (PowerShell)**
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
irm https://raw.githubusercontent.com/z0rkez/claude-config/main/install.ps1 | iex
```

Скрипт клонирует репозиторий в `~/.claude`, ставит gstack, прописывает MCP-серверы в `~/.claude.json` и спрашивает недостающие API-ключи.

Личная часть (инструкции, память, настройки) лежит в отдельном приватном репозитории и подтягивается, если `gh` авторизован под владельцем. Без неё используется `settings.example.json`.

## Требования

| | Linux/macOS | Windows |
|---|---|---|
| Обязательно | `git`, `python3` | `git`, `python` (3.x) |
| Для личной части | `gh` (GitHub CLI) | `gh` (GitHub CLI) |
| Уведомления | `libnotify` / `osascript` | встроенный WinForms |
| zaebal | `python3` | `python` |

> **Windows:** хуки вызываются через `python3`. Если в системе Python доступен как `python`, замени в `settings.json` строки `python3` на `python`.

## Обновление

```bash
cd ~/.claude
python3 mcp.py export                                   # если менялись MCP-серверы
git add -A && git commit -m "..." && git push           # публичная часть
git --git-dir=.private.git add -f CLAUDE.md profile.md settings.json settings.local.json \
  hooks/private-guard.names projects/*/memory
git --git-dir=.private.git commit -m "..." && git --git-dir=.private.git push
```

`settings.example.json` — копия `settings.json` без машино-специфичных настроек (прокси, SUDO_ASKPASS, autoMode.environment).

## Структура хуков

| Файл | Событие | Платформы |
|---|---|---|
| `hooks/session-anchor.py` | SessionStart | все |
| `hooks/private-guard.py` | PreToolUse Read/Glob/... | все |
| `hooks/bash-guard.py` | PreToolUse Bash | все |
| `hooks/notify.py` | Notification | Linux, macOS, Windows |
| `hooks/session-anchor.sh` | SessionStart | Linux (с waybar-статусом) |

## Что не в git

| Что | Почему |
|---|---|
| `.credentials.json`, `secrets.env` | секреты |
| история чатов, `sessions/` | личное |
| `plugins/`, `skills/synced/` | ставятся автоматически |
| `skills/gstack` | клонируется из garrytan/gstack |
| `cache/`, `telemetry/`, `file-history/`, `*.bak*` | мусор |
