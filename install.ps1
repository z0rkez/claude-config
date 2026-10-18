# Установка конфига Claude Code на Windows (PowerShell 5.1+).
# Требует: git, python; для личной части — gh, авторизованный как z0rkez.
# Запуск: Set-ExecutionPolicy Bypass -Scope Process -Force; .\install.ps1
#   или одной строкой:
#   irm https://raw.githubusercontent.com/z0rkez/claude-config/main/install.ps1 | iex
$ErrorActionPreference = "Stop"

$PUB  = "https://github.com/z0rkez/claude-config"
$PRIV = "z0rkez/claude-private"
$DEST = "$env:USERPROFILE\.claude"

# 1. Публичный репозиторий
if (-not (Test-Path "$DEST\.git")) {
    $tmp = New-TemporaryFile | ForEach-Object { Remove-Item $_; $_.FullName }
    git clone $PUB $tmp
    if (Test-Path $DEST) {
        if (Test-Path "$DEST\settings.json") {
            Copy-Item "$DEST\settings.json" "$DEST\settings.json.bak.install"
        }
        Get-ChildItem $tmp | Copy-Item -Destination $DEST -Recurse -Force
    } else {
        Move-Item $tmp $DEST
    }
} else {
    git -C $DEST pull --ff-only
}

# 2. Личная часть
$hasGH = Get-Command gh -ErrorAction SilentlyContinue
if ($hasGH -and (gh repo view $PRIV 2>$null)) {
    if (-not (Test-Path "$DEST\.private.git")) {
        gh repo clone $PRIV "$DEST\.private.git" -- --bare
        git --git-dir="$DEST\.private.git" config core.bare false
        git --git-dir="$DEST\.private.git" config core.worktree $DEST
        git --git-dir="$DEST\.private.git" checkout -f
    } else {
        git --git-dir="$DEST\.private.git" pull --ff-only
    }
} else {
    Write-Host "Нет доступа к $PRIV, ставлю публичные настройки"
    if (-not (Test-Path "$DEST\settings.json")) {
        Copy-Item "$DEST\settings.example.json" "$DEST\settings.json"
    }
}

# 3. Сторонние скилы
if (-not (Test-Path "$DEST\skills\gstack")) {
    git clone --depth 1 https://github.com/garrytan/gstack "$DEST\skills\gstack"
}

# 4. Ядро хука zaebal
$ZaebalDest = "$env:USERPROFILE\.zaebal"
New-Item -ItemType Directory -Force -Path $ZaebalDest | Out-Null
if (Test-Path "$ZaebalDest\core") { Remove-Item "$ZaebalDest\core" -Recurse -Force }
Copy-Item "$DEST\external\zaebal-core" "$ZaebalDest\core" -Recurse

# 5. MCP-серверы
python "$DEST\mcp.py" import

Write-Host "Готово. Не в репозитории: rtk, ~/projects/telegram-mcp, логин в Claude Code."
