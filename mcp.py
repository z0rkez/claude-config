#!/usr/bin/env python3
"""MCP-серверы между ~/.claude.json и mcp-servers.json (секреты вне git).

  mcp.py export  ~/.claude.json -> mcp-servers.json, секреты -> ~/.claude/secrets.env
  mcp.py import  mcp-servers.json + secrets.env -> ~/.claude.json (недостающие спросит)
"""
import json
import re
import sys
from pathlib import Path

HOME = Path.home()
CLAUDE_JSON = HOME / ".claude.json"
REPO = Path(__file__).resolve().parent
SERVERS = REPO / "mcp-servers.json"
SECRETS = REPO / "secrets.env"
SECRET_RE = re.compile(r"KEY|TOKEN|SECRET|PASSWORD", re.I)
PLACEHOLDER = re.compile(r"^\$\{(\w+)\}$")


def load_env():
    env = {}
    if SECRETS.exists():
        for line in SECRETS.read_text().splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def save_env(env):
    SECRETS.write_text("".join(f"{k}={v}\n" for k, v in sorted(env.items())))
    SECRETS.chmod(0o600)


def export():
    servers = json.loads(CLAUDE_JSON.read_text()).get("mcpServers", {})
    env = load_env()
    for srv in servers.values():
        for k, v in srv.get("env", {}).items():
            if SECRET_RE.search(k) and not PLACEHOLDER.match(v):
                env[k] = v
                srv["env"][k] = "${%s}" % k
    SERVERS.write_text(json.dumps(servers, ensure_ascii=False, indent=2) + "\n")
    save_env(env)
    print(f"{len(servers)} серверов -> {SERVERS.name}, секретов: {len(env)}")


def import_():
    servers = json.loads(SERVERS.read_text())
    env = load_env()
    for name, srv in servers.items():
        for k, v in srv.get("env", {}).items():
            m = PLACEHOLDER.match(v)
            if not m:
                continue
            var = m.group(1)
            if var not in env:
                env[var] = input(f"{name}: {var} (пусто = пропустить): ").strip()
            srv["env"][k] = env[var]
    save_env(env)
    data = json.loads(CLAUDE_JSON.read_text()) if CLAUDE_JSON.exists() else {}
    data.setdefault("mcpServers", {}).update(servers)
    CLAUDE_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"{len(servers)} серверов записано в {CLAUDE_JSON}")


if __name__ == "__main__":
    {"export": export, "import": import_}[sys.argv[1] if len(sys.argv) > 1 else ""]()
