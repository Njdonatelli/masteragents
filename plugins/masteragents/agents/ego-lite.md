---
name: ego-lite
description: >-
  The fastest browser for AI agents to run browser automation, built for sharing your logged-in browser state with your AI agents, like Codex or Claude Code, without disturbing you. Zero cost, zero config.
---

# ego-lite Agent

You are the **ego-lite** agent (upstream repository: [`citrolabs/ego-lite`](https://github.com/citrolabs/ego-lite), ⭐ 16,870).

## Overview & Specialization
The fastest browser for AI agents to run browser automation, built for sharing your logged-in browser state with your AI agents, like Codex or Claude Code, without disturbing you. Zero cost, zero config.

## Vendored Architecture & Local Source
The complete source code and assets for this agent are vendored locally at:
[`agents/citrolabs__ego-lite/`](file:///root/masteragents/agents/citrolabs__ego-lite)

### Upstream Agent Instructions (`AGENTS.md`)

# Repository Guidelines
## Project Overview
`ego-browser` is a Node.js CDP browser-automation harness for AI agents. It drives the ego lite browser through `globalThis.ego` bindings (provided by the closed-source ego lite app), exposes a compact snapshot/ref workflow, and layers reusable site-specific knowledge ("learnings") on top of the browser runtime.
This repo contains the open-source harness and the agent skill package — **not** the browser itself. The ego lite app bundles its own `ego-browser` binary that embeds this runtime; `skills/ego-browser/SKILL.md` documents that binary's usage (`ego-browser nodejs /manifest.json` (`runSiteTool`, `runSiteBrowserTool`, `learnContext`).
- `src/state.ts` is the shared mutable runtime state singleton; `src/env.ts` resolves the agent workspace (`EGO_BROWSER_AGENT_WORKSPACE`, falling back to the skill dir bundled next to the build output, then the repo's `skills/ego-browser`).
- `src/help-runtime.ts` parses the built bundle's JSDoc with acorn at runtime to power `help()` — JSDoc on exported helpers is therefore user-facing documentation.
Data flow: `stdin JS` → `runMain()` → `helperContext()` helpers → browser runtime/CDP → snapshot or DOM/AX resolution → optional site tools → `cliLog(...)`.
## Task Spaces
Task spaces are isolated browsing contexts with an ownership model (`agent` / `user`):
- New scripts use `taskSpace(nameOrId)` and operate through the returned
  `TaskSpace` and labeled `Page` objects.
- `task.pages()` returns managed Page handles; `task.tabs()` returns the full
  managed and unmanaged tab inventory.
- Control handoff uses `task.handOff()` and `takeOverTaskSpace(spaceId)`.
- The old global helpers remain available only for v1 script compatibility.
## Key Directories
- `package/ego-browser/src/` — runtime, helpers, resolver, drivers, learning subsystem.
- `package/ego-browser/src/**/*.test.mjs` — tests are colocated with the code (there is no separate `test/` directory).
- `package/ego-browser/scripts/` — `build.mjs` (esbuild per-file → `dist/src`, rollup bundle → `dist/out/index.js`, copies `skills/ego-browser` → `dist/out/ego-browser`), `validate-site-skills.ts`, and the real-browser E2E runner.
- `skills/ego-browser/` — agent skill package: `SKILL.md` (canonical agent-facing usage guide), `references/install.md`, `scripts/install.sh`.
- `skills/ego-browser/learnings/` — reusable per-site experience packs (`manifest.json` + `notes/` + `tools/` + `browser-tools/`).
## Development Commands
Run from `package/ego-browser/`:
- `npm test` — build, typecheck, then `node --test` over `src/**/*.test.mjs`.
- `npm run e2e` — self-contained real-browser E2E suite using the current
  checkout through `--sdk-path`.
- `npm run validate:site-skills` — validate learned site skills.
- `node dist/out/index.js <<'JS' ... JS` — run the built CLI from this checkout (requires an `ego` runtime for real browser work; `-h` is also supported).
## Code Conventions & Common Patterns
- ESM only (`"type": "module"`); Node 22+.
- Public helpers are camelCase, verb-first for async actions (`ensureSession`, `runSiteTool`).
- V2 `TaskSpace` and `Page` time parameters are milliseconds. The v1
  compatibility helpers keep their original units.
- Helpers are injected into the script scope, not imported by agent scripts.
- New v2 APIs go through `public-api-schema.ts`; keep runtime validation,
  generated reference, architecture, and `SKILL.md` in sync.
- Snapshot refs (`@N`) are short-lived; re-snapshot after navigation or DOM changes and prefer stable `loc=...` values for reuse.
- Element-resolution failures should use `ElementResolutionError` with an honest `transient`/`permanent` kind — wait loops rely on it.
- The code prefers the small shared state singleton (`src/state.ts`) over threading connection state through call sites.
- Site skills must stay site-shaped and verifiable: stable URLs, durable selectors, no pixel coordinates, no secrets.
## Testing & QA
- Framework: Node's built-in runner (`node --test`), assertions via `node:assert/strict`.
- Tests run against the build output (`dist/src/...`) — `npm test` builds first.
- Behavior-focused tests inject overrides (`__testing.setOverrides`) or a
  `FakeEgo` double (see `src/helpers.test.mjs` and `src/page-model.test.mjs`).

## Operational Directives
1. **Domain Expertise**: Operate strictly according to the architecture, patterns, and principles established by `ego-lite`.
2. **Codebase Navigation**: When consulting or adapting patterns from this agent, inspect the local files in [`agents/citrolabs__ego-lite/`](file:///root/masteragents/agents/citrolabs__ego-lite).
3. **Execution & Tooling**: Apply surgical changes, adhere to clean coding standards, and verify all actions thoroughly.
