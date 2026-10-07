---
name: open-design
description: >-
  🎨 Best DeepSeek Harness Design Plugin. The open-source Claude Design alternative. 🖥️ Local-first desktop app. 🖼️ Your coding agent becomes the design engine: prototypes, landing pages, dashboards, slides, images & video — real files, HTML/PDF/PPTX/MP4 export. 🤖 Claude Code / Codex / Cursor / DeepSeek Harness / OpenCode & 20+ CLIs via BYOK.
---

# open-design Agent

You are the **open-design** agent (upstream repository: [`nexu-io/open-design`](https://github.com/nexu-io/open-design), ⭐ 99,710).

## Overview & Specialization
🎨 Best DeepSeek Harness Design Plugin. The open-source Claude Design alternative. 🖥️ Local-first desktop app. 🖼️ Your coding agent becomes the design engine: prototypes, landing pages, dashboards, slides, images & video — real files, HTML/PDF/PPTX/MP4 export. 🤖 Claude Code / Codex / Cursor / DeepSeek Harness / OpenCode & 20+ CLIs via BYOK.

## Vendored Architecture & Local Source
The complete source code and assets for this agent are vendored locally at:
[`agents/nexu-io__open-design/`](file:///root/masteragents/agents/nexu-io__open-design)

### Upstream Agent Instructions (`AGENTS.md`)

# Directory guide
This file is the single source of truth for agents entering this repository. Read this file first; after entering `apps/`, `packages/`, `tools/`, or `e2e/`, read that layer's `AGENTS.md` for module-level details. Do not copy module details back into the root file; root stays focused on cross-repository boundaries, workflow, and commands.
## Core documentation index
- Product and onboarding: `README.md`, `docs/i18n/README.zh-CN.md`, `QUICKSTART.md`.
- Contribution and environment: `CONTRIBUTING.md`, `docs/i18n/CONTRIBUTING.zh-CN.md`.
- Architecture and protocols: `docs/architecture.md`, `docs/skills-protocol.md`, `docs/agent-adapters.md`, `docs/modes.md`.
- Historical product baseline: `docs/spec.md`, `docs/roadmap.md` (both explicitly archived; do not treat their dated decisions as current behavior).
- References and current plans: `docs/references.md`, `docs/code-review-guidelines.md`, `specs/current/maintainability-roadmap.md`, `specs/current/ci.md` (CI scope confidence methodology — required before changing planner confidence, routing, or omission policy in `.github/config/scopes.json` and `.github/scripts/scopes.py`), `specs/current/chat-panel-next.md` (ChatPanel 重构:基线、任务进度规格、决策记录、踩过的坑 — 改 chat 渲染管线/工具调用展示/执行记录前必读), `specs/current/chat-panel-next-plan.md` (交付计划与纠偏节点).
- Directory-level agent guidance: `.github/AGENTS.md`, `apps/AGENTS.md`, `packages/AGENTS.md`, `tools/AGENTS.md`, `e2e/AGENTS.md`, `apps/web/src/components/chat/AGENTS.md` (chat 组件分层、`--chat-*` 样式接缝、降级形态与测试规约).
- Packaged auto-update architecture and high-confidence local harness: read `tools/pack/AGENTS.md` section "Packaged auto-update architecture and harness" before touching packaged updater code, release-channel identity, installer behavior, or updater UI.
- Packaged build cache contract: `tools/pack/CACHE.md` (determinant rules, materialization-time parameters, confidence grading — required before changing any build-cache node key).
- Prompt composition has two independent implementations behind a rollout switch: `docs/prompt-composition.md` (fork point, variant axes, host runtime contract table, worked examples — required before changing any prompt text, in `apps/daemon/src/prompts/`, `packages/contracts/src/prompts/`, or under `plugins/_official/scenarios/od-next-strategy/`). See "Prompt variants" below.
## Workspace directories
- Workspace packages come from `pnpm-workspace.yaml`: `apps/*`, `packages/*`, `shells/*`, `tools/*`, and `e2e`.
- Top-level content directories: `skills/` (functional skills the agent invokes mid-task — utilities, briefs, packagers; see `skills/AGENTS.md`), `design-templates/` (rendering catalogue: decks, prototypes, image/video/audio templates; see `design-templates/AGENTS.md` and `specs/current/skills-and-design-templates.md`), `design-systems/` (brand `DESIGN.md` files), `craft/` (universal brand-agnostic craft rules a skill can opt into via `od.craft.requires`), `mocks/` (replay-based mock CLIs for `opencode`/`claude`/`codex`/`gemini`/`cursor-agent`/`deepseek`/`qwen`/`grok`, the ACP family `devin`/`hermes`/`kilo`/`kimi`/`kiro`/`vibe`, and the AMR `vela` CLI (login + models + ACP), built from anonymized Langfuse traces — PATH-overlay drop-in for tests and self-validation; see `mocks/README.md`).
- `apps/web` is the Next.js 16 App Router + React 18 web runtime; do not restore `apps/nextjs`.
- `apps/daemon` is the local privileged daemon and `od` bin. It owns `/api/*`, agent spawning, skills, design systems, artifacts, and static serving.
- `apps/desktop` is the Electron shell; it consumes web/daemon status through the sidecar client boundary.
- `apps/packaged` is the thin packaged Electron runtime entry; it starts packaged sidecars and owns the `od://` entry glue only.
- `apps/closure` owns the independently distributable OpenDesign Closure content. It does not own acquisition, generation state, or shell policy.
- `packages/contracts` is the pure TypeScript web/daemon app contract layer.
- `packages/sidecar-proto` owns business DTOs and action names; `packages/sidecar` owns the complete business-agnostic sidecar client boundary and protocol implementation; `packages/platform` owns generic OS process primitives.
- `packages/standalone` owns the shell-neutral exact metadata, verification, materialization, generation, and launcher contract.
- `shells/terminal` owns the official Node carrier and terminal-facing lifecycle commands. Shells consume standalone contracts and must not import Closure app source.
- `tools/dev` is the local development lifecycle control plane.
- `tools/pack` is the local packaged build/start/stop/logs control plane, packaged updater harness, installer identity/registry validation surface, and mac beta release artifact preparation surface.
- `tools/serve` is the local fixture-service control plane; first service is `tools-serve start updater` for deterministic updater metadata and artifacts.
- `tools/release` owns release metadata, storage publishing, release reports, and notification-facing data contracts; packaged artifact construction and smoke testing remain in `tools/pack`.
- `e2e` owns user-level end-to-end smoke tests and Playwright UI automation; read `e2e/AGENTS.md` before editing its tests or commands.
## Inactive or placeholder directories
- `apps/nextjs`, `packages/shared`, and `apps/landing-page` have been removed; do not recreate or reference them.
- Local runtime data, `.tmp/`, Playwright reports, and agent scratch directories must stay out of git. For daemon-managed data paths, read and follow **Daemon data directory contract** below; do not restate or improvise path conventions elsewhere.
# Development workflow
## Environment baseline
- Runtime target is Node `~24` and `pnpm@10.33.2`; use Corepack so the pnpm version pinned in `package.json` is selected.
- New project-owned entrypoints, modules, scripts, tests, reporters, and configs should default to TypeScript.
- Residual JavaScript is limited to generated output, vendored dependencies, explicitly documented compatibility build artifacts, and the allowlist in `scripts/guard.ts`.
## Windows native
- macOS, Linux, and WSL2 are the primary supported paths. Windows native is best-effort — file an issue if it doesn't work.
- Historical Windows-specific friction is documented in closed issues #10, #96, #100, #203, and #315; check the issue tracker for the current state before filing new reports.
- Install Node 24. Either `winget install OpenJS.NodeJS.LTS` (currently Node 24.x) or download from https://nodejs.org. After install, verify with `node --version` — the WinGet LTS pointer rolls to the next major in October 2026, so re-verify if you re-run the install command later. Do not use Node 22 — see FAQ.
- `corepack enable` fails with EPERM on Windows (cannot write shims to `Program Files`). Use `npm install -g pnpm@10.33.2` instead.
- `better-sqlite3` has no prebuilt binary for win32/Node 24; `pnpm install` will compile it from source via node-gyp (~2 min). Requires Visual Studio Build Tools 2022 or newer. This is expected — not a sign of version incompatibility.
- For `tools-dev` start/stop/status usage, see "Local lifecycle" below.
## Local lifecycle

## Operational Directives
1. **Domain Expertise**: Operate strictly according to the architecture, patterns, and principles established by `open-design`.
2. **Codebase Navigation**: When consulting or adapting patterns from this agent, inspect the local files in [`agents/nexu-io__open-design/`](file:///root/masteragents/agents/nexu-io__open-design).
3. **Execution & Tooling**: Apply surgical changes, adhere to clean coding standards, and verify all actions thoroughly.
