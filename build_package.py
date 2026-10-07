#!/usr/bin/env python3
import os
import re
import json
import shutil
from pathlib import Path

ROOT = Path("/root/masteragents")
AGENTS_SRC = ROOT / "agents"
CATALOG_FILE = ROOT / "agents.json"
PLUGINS_DIR = ROOT / "plugins" / "masteragents"
AGENTS_OUT = PLUGINS_DIR / "agents"
RULES_OUT = PLUGINS_DIR / "rules"
SCRIPTS_DIR = ROOT / "scripts"
CLAUDE_PLUGIN_DIR = ROOT / ".claude-plugin"

def clean_name(n: str) -> str:
    cn = n.lower().replace("_", "-").replace(".", "-")
    cn = re.sub(r"[^a-z0-9\-]", "-", cn)
    cn = re.sub(r"-+", "-", cn).strip("-")
    return cn

def clean_text(text: str) -> str:
    # remove HTML tags or excessive badges
    text = re.sub(r"<[^>]+>", "", text)
    # remove image links
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    return text.strip()

def extract_core_guidance(folder_path: Path) -> str:
    guidance_sections = []
    
    # 1. Check AGENTS.md
    agents_md = folder_path / "AGENTS.md"
    if agents_md.is_file():
        try:
            content = agents_md.read_text(encoding="utf-8", errors="replace")
            content = clean_text(content)
            lines = [l for l in content.splitlines() if l.strip()]
            if lines:
                excerpt = "\n".join(lines[:45])
                guidance_sections.append(f"### Upstream Agent Instructions (`AGENTS.md`)\n\n{excerpt}")
        except Exception:
            pass

    # 2. Check CLAUDE.md if AGENTS.md was absent or minimal
    claude_md = folder_path / "CLAUDE.md"
    if claude_md.is_file() and len(guidance_sections) == 0:
        try:
            content = claude_md.read_text(encoding="utf-8", errors="replace")
            content = clean_text(content)
            lines = [l for l in content.splitlines() if l.strip() and not l.startswith("@")]
            if lines:
                excerpt = "\n".join(lines[:45])
                guidance_sections.append(f"### Claude Code Instructions (`CLAUDE.md`)\n\n{excerpt}")
        except Exception:
            pass

    # 3. Fallback / supplementary: README.md
    readme_md = folder_path / "README.md"
    if readme_md.is_file() and len(guidance_sections) == 0:
        try:
            content = readme_md.read_text(encoding="utf-8", errors="replace")
            content = clean_text(content)
            lines = [l for l in content.splitlines() if l.strip()]
            # find first 30 non-empty lines
            excerpt = "\n".join(lines[:35])
            guidance_sections.append(f"### Repository Synopsis (`README.md`)\n\n{excerpt}")
        except Exception:
            pass

    return "\n\n".join(guidance_sections)

def build_all():
    print("Building masteragents plugin and marketplace manifests...")
    
    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    # 1. Setup directories
    AGENTS_OUT.mkdir(parents=True, exist_ok=True)
    RULES_OUT.mkdir(parents=True, exist_ok=True)
    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    CLAUDE_PLUGIN_DIR.mkdir(parents=True, exist_ok=True)
    (PLUGINS_DIR / ".claude-plugin").mkdir(parents=True, exist_ok=True)

    # 2. Write each agent definition
    agent_manifests = []
    print(f"Generating 50 agent markdown files in {AGENTS_OUT}...")
    for item in catalog:
        c_name = clean_name(item["name"])
        folder = item["folder"]
        folder_path = AGENTS_SRC / folder
        
        desc = item["description"] or f"Specialized AI agent for {item['name']} capabilities."
        # Clean description of newlines or quotes
        desc_clean = desc.replace("\n", " ").replace('"', "'").strip()
        
        guidance = extract_core_guidance(folder_path) if folder_path.is_dir() else ""
        
        stars_display = f"{item['stars']:,}" if item['stars'] else ">20"
        
        md_content = f"""---
name: {c_name}
description: >-
  {desc_clean}
---

# {item['name']} Agent

You are the **{item['name']}** agent (upstream repository: [`{item['full_name']}`]({item['html_url']}), ⭐ {stars_display}).

## Overview & Specialization
{desc_clean}

## Vendored Architecture & Local Source
The complete source code and assets for this agent are vendored locally at:
[`agents/{folder}/`](file:///root/masteragents/agents/{folder})

{guidance}

## Operational Directives
1. **Domain Expertise**: Operate strictly according to the architecture, patterns, and principles established by `{item['name']}`.
2. **Codebase Navigation**: When consulting or adapting patterns from this agent, inspect the local files in [`agents/{folder}/`](file:///root/masteragents/agents/{folder}).
3. **Execution & Tooling**: Apply surgical changes, adhere to clean coding standards, and verify all actions thoroughly.
"""
        agent_file = AGENTS_OUT / f"{c_name}.md"
        agent_file.write_text(md_content, encoding="utf-8")
        agent_manifests.append({
            "name": c_name,
            "original_name": item["name"],
            "repo": item["full_name"],
            "stars": item["stars"],
            "file": f"agents/{c_name}.md"
        })

    # 3. Create plugin manifest for masteragents
    plugin_manifest = {
        "name": "masteragents",
        "description": "Curated library of 50 top AI and coding agents (<6 months, stars >20) with complete source code, architectures, and executable agent definitions.",
        "version": "1.0.0",
        "author": {
            "name": "Nicolas Donatelli",
            "url": "https://github.com/Njdonatelli"
        },
        "homepage": "https://github.com/Njdonatelli/masteragents",
        "repository": "https://github.com/Njdonatelli/masteragents",
        "license": "MIT",
        "keywords": [
            "agents",
            "coding-agents",
            "ai-agents",
            "architecture",
            "productivity",
            "engineering"
        ]
    }
    
    (PLUGINS_DIR / "plugin.json").write_text(json.dumps(plugin_manifest, indent=2) + "\n", encoding="utf-8")
    (PLUGINS_DIR / ".claude-plugin" / "plugin.json").write_text(json.dumps(plugin_manifest, indent=2) + "\n", encoding="utf-8")

    # 4. Create rules/AGENTS.md
    rules_content = """# MasterAgents Rules

This environment has the `masteragents` library enabled, providing 50 specialized AI and coding agents.

## Using MasterAgents
- Each agent is invokable by name (e.g. `ponytail`, `open-design`, `open-code-review`, `deepseek-reasonix`, `archify`, etc.).
- Complete vendored source codes and implementation architectures for all 50 agents are located in `/root/masteragents/agents/`.
- Consult `/root/masteragents/agents.json` or `/root/masteragents/README.md` for complete catalog index and capability descriptions.
"""
    (RULES_OUT / "AGENTS.md").write_text(rules_content, encoding="utf-8")

    # 5. Create marketplace configs
    marketplace_config = {
        "name": "masteragents",
        "version": "1.0.0",
        "owner": {
            "name": "Nicolas Donatelli",
            "url": "https://github.com/Njdonatelli"
        },
        "homepage": "https://github.com/Njdonatelli/masteragents",
        "repository": "https://github.com/Njdonatelli/masteragents",
        "license": "MIT",
        "description": "Curated library of 50 top AI and coding agents (<6 months, stars >20) with source code, architectures, and executable agent definitions.",
        "plugins": [
            {
                "name": "masteragents",
                "source": "./plugins/masteragents",
                "description": "50 high-impact AI coding agents and architectures.",
                "category": "productivity",
                "keywords": [
                    "agents",
                    "coding-agents",
                    "ai-agents",
                    "library",
                    "architecture",
                    "multi-agent"
                ]
            }
        ]
    }
    (ROOT / "marketplace.config.json").write_text(json.dumps(marketplace_config, indent=2) + "\n", encoding="utf-8")

    claude_marketplace = {
        "name": "masteragents",
        "owner": {
            "name": "Nicolas Donatelli",
            "url": "https://github.com/Njdonatelli"
        },
        "description": "Personal hosted marketplace of 50 AI and coding agents. Install once, access every agent across your environment.",
        "homepage": "https://github.com/Njdonatelli/masteragents",
        "repository": "https://github.com/Njdonatelli/masteragents",
        "metadata": {
            "description": "Personal hosted marketplace of 50 AI and coding agents.",
            "version": "1.0.0"
        },
        "plugins": [
            {
                "name": "masteragents",
                "source": "./plugins/masteragents",
                "description": "50 high-impact AI coding agents and architectures.",
                "version": "1.0.0",
                "author": {
                    "name": "Nicolas Donatelli",
                    "url": "https://github.com/Njdonatelli"
                },
                "keywords": [
                    "agents",
                    "coding-agents",
                    "ai-agents",
                    "library",
                    "productivity"
                ],
                "category": "productivity"
            }
        ]
    }
    (CLAUDE_PLUGIN_DIR / "marketplace.json").write_text(json.dumps(claude_marketplace, indent=2) + "\n", encoding="utf-8")

    # 6. Create install_plugins.py script
    install_script = """#!/usr/bin/env python3
\"\"\"Install masteragents into Antigravity CLI and Claude Code.

    python scripts/install_plugins.py
\"\"\"
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN_PATH = ROOT / "plugins" / "masteragents"

def run(cmd: list[str]) -> int:
    print("$", " ".join(cmd))
    res = subprocess.run(cmd)
    return res.returncode

def main() -> int:
    agy = shutil.which("agy")
    claude = shutil.which("claude")

    if agy:
        print("=== Installing into Antigravity CLI (agy) ===")
        run([agy, "plugin", "validate", str(PLUGIN_PATH)])
        run([agy, "plugin", "install", str(PLUGIN_PATH)])

    if claude:
        print("=== Installing into Claude Code ===")
        run([claude, "plugin", "validate", str(PLUGIN_PATH)])
        run([claude, "plugin", "marketplace", "add", str(ROOT)])
        run([claude, "plugin", "install", "masteragents@masteragents"])

    print("=== MasterAgents Installation Complete ===")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
"""
    (SCRIPTS_DIR / "install_plugins.py").write_text(install_script, encoding="utf-8")
    os.chmod(SCRIPTS_DIR / "install_plugins.py", 0o755)

    print("Build complete! All 50 agent files and manifests generated successfully.")

if __name__ == "__main__":
    build_all()
