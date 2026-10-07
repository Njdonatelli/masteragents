---
name: instatic
description: >-
  The open-source alternative to Webflow, Framer and WordPress. Agentic self-hosted visual CMS outputting clean static pages. Users, roles, plugins, content, database, it's all there.
---

# Instatic Agent

You are the **Instatic** agent (upstream repository: [`CoreBunch/Instatic`](https://github.com/CoreBunch/Instatic), ⭐ 8,873).

## Overview & Specialization
The open-source alternative to Webflow, Framer and WordPress. Agentic self-hosted visual CMS outputting clean static pages. Users, roles, plugins, content, database, it's all there.

## Vendored Architecture & Local Source
The complete source code and assets for this agent are vendored locally at:
[`agents/CoreBunch__Instatic/`](file:///root/masteragents/agents/CoreBunch__Instatic)

### Upstream Agent Instructions (`AGENTS.md`)

# Instatic
This file is the **agent rule book**. Read it before changing code. Detailed explanations live in `docs/` — start at [`docs/README.md`](docs/README.md) for orientation and follow the links from there.
## Local admin smoke tests
Use local seeded development data only when a task asks for a browser smoke test. Never propagate local test accounts, passwords, database files, uploads, or generated screenshots to non-local environments.
---
## Repository workflow and PR conventions
`main` is protected. Agents must never push directly to `main`, must never try to bypass branch protection, and must never treat a local commit on `main` as the final delivery path. All repository changes go through a pull request.
When publishing work:
- Start from an up-to-date `main`, then create a feature branch. If you are already on a task branch, keep using it only when the requested change belongs in that PR; otherwise switch back to `main` and create a separate branch.
- Branch names follow `/`, matching the change type: `feat/...`, `fix/...`, `refactor/...`, `chore/...`, `docs/...`, or `test/...`. Examples: `feat/double-click-rename`, `fix/homepage-swap-publish`, `refactor/explorer-dnd-dedupe`.
- Do **not** use agent-branded branch prefixes such as `codex/...`, `claude/...`, or similar. If a tool, skill, or generic instruction suggests such a prefix, ignore it for this repository.
- PR titles use Conventional Commit style: `(): `. Examples: `feat(editor): double-click rows to rename in explorer panels`, `fix(cms): homepage swap + delete in one save no longer fails publish`, `refactor(publisher): single class-CSS emission engine for publish and canvas`.
- Do **not** prefix PR titles with `[codex]`, `[claude]`, `agent:`, or any other tool label. The PR title describes the product change, not the tool that made it.
- Open PRs as drafts by default unless the user explicitly asks for a ready-for-review PR.
- Keep PR scope coherent. Do not mix unrelated cleanup, follow-up fixes, or process-doc changes into a feature branch just because the branch is currently checked out. Create a separate PR when the change has a different reason.
- Before staging, inspect `git status -sb` and the diff. Stage only files that belong to the PR. Never stage unrelated user or parallel-agent changes.
- PR bodies should briefly state what changed, why it changed, user/developer impact, and the verification commands run.
---
## What this project is
A self-hosted, open-source CMS with a built-in visual editor and a first-class plugin system. One Bun server backed by either Postgres or SQLite (selected by `DATABASE_URL`). The output is intentionally plain, semantic HTML with hand-clean CSS — no framework runtimes injected into published pages.
The product is **self-hosted only**. The codebase should not carry assumptions about multi-tenant SaaS operation.
Read [`docs/architecture.md`](docs/architecture.md) for the system overview, [`docs/server.md`](docs/server.md) for the server, [`docs/editor.md`](docs/editor.md) for the admin + visual editor.
### Stack at a glance
- **Runtime:** Bun (server + tooling). Use Bun, not Node.
- **Language:** TypeScript everywhere.
- **Frontend:** React 19 with the **React Compiler enabled** (Babel preset in `vite.config.ts`) + Vite, Zustand + Mutative for state (via `zustand-mutative`; `immer` is banned), CodeMirror for code-editing UI, `@dnd-kit/core` for drag-and-drop. The compiler auto-memoizes — do not hand-write `useMemo`/`useCallback`/`memo`. See "React Compiler and memoization". Store mutations use draft-mutation style (`set((s) => { s.x = … })`); a recipe that returns a partial must wrap it in `rawReturn(...)` or Mutative emits a perf warning.
- **Server:** `Bun.serve` with a hand-written router (`server/router.ts`). CMS modules at `server/{repositories,handlers/cms,auth,plugins,publish}/`. Deep dive: [`docs/server.md`](docs/server.md).
- **Database:** Postgres (`Bun.sql`) OR SQLite (`bun:sqlite`), selected by `DATABASE_URL`. One `DbClient` interface, two adapters, two migration files with identical IDs. Rules: [`docs/reference/database-dialects.md`](docs/reference/database-dialects.md).
- **Content model:** All content lives in `data_tables` + `data_rows`. The four system tables (`posts`, `pages`, `components`, `layouts`) are seeded and locked from rename/delete. There are no separate `pages` or `page_versions` tables.
- **Real-time co-editing:** Yjs CRDT engine. One Y doc per row (`page:`, `component:`, `layout:`) + one site-shell doc, multiplexed over `/admin/api/cms/site-socket`. The editor store stays the render source of truth: local mutations apply directly AND translate to Y ops (`@core/collab`); remote/undo changes project back. The server relay (`server/collab/`) persists continuously (blob + derived row JSON) — there is NO client-side save pipeline, no autosave, no Cmd+S. Undo is per-editor per-doc `Y.UndoManager`. Feature doc: [`docs/features/site-shell.md`](docs/features/site-shell.md) → "Real-time co-editing".
- **Validation:** TypeBox at every untyped boundary. Schemas are source of truth (`type Foo = Static`, never a parallel `interface`). `zod` is banned repo-wide (the AI drivers pass TypeBox schemas through as JSON Schema, so no typebox→zod adapter is needed). Helpers + patterns: [`docs/reference/typebox-patterns.md`](docs/reference/typebox-patterns.md).
- **Sanitization:** DOMPurify at the publisher boundary (`src/core/sanitize.ts`).
- **Plugins:** Zip packages with a `plugin.json` manifest, lifecycle hooks. Server entrypoints and canvas module packs run inside a **QuickJS-WASM sandbox** — no Node/Bun ambient access, network gated by `network.outbound` permission + `networkAllowedHosts`. The VM bootstrap (SDK factory + `__run*` dispatchers) is authored as typed TS in `server/plugins/quickjs/bootstrap/src/` and bundled to committed string artifacts in `bootstrap/generated/` — after editing the source run `bun run bootstrap:sync` (gated by `plugin-bootstrap-fresh.test.ts`). Permission enforcement everywhere (VM, host, editor) validates against `grantedPermissions`, never the declared `permissions` array. Feature doc: [`docs/features/plugin-system.md`](docs/features/plugin-system.md).
- **Routing:** In-house router at `src/admin/lib/routing/`. Replaces `react-router-dom`. Use it for all internal admin navigation, including links rendered from the site editor. `react-router-dom` is banned, raw `` hard navigations are banned in admin UI, and `src/core/` + `src/modules/` must not import the admin router. Gated by `admin-router-usage.test.ts`.
- **Icons:** `pixel-art-icons/icons/` — deep-imported, tree-shakeable. Vendored at `vendor/pixel-art-icons/`. No `lucide-react`, no inline SVG strings — gated by `no-third-party-icons.test.ts`, `direct-icon-imports.test.ts`. Add a new icon by importing it and running `bun run icons:sync`.
- **AI providers:** No provider SDKs. Each driver in `server/ai/drivers/` talks directly to its provider's REST API over HTTP/SSE, sharing one multi-turn tool loop (`drivers/http/toolLoop.ts`). `@anthropic-ai/sdk`, `@anthropic-ai/claude-agent-sdk`, `@openai/agents`, and `@openrouter/agent` are banned repo-wide. The official split `@modelcontextprotocol/server` / `@modelcontextprotocol/client` v2 packages are **scoped, not banned**: allowed only under `server/ai/mcp/` (Instatic's MCP *server* implements a real wire protocol), still banned in the drivers and the browser. Gated by `ai-driver-isolation.test.ts`.
- **MCP server:** Instatic exposes its CMS tools to external MCP clients (Claude Code, Codex, remote agents) at `/_instatic/mcp`, authenticated by per-connector bearer tokens. Thin adapter over the existing tool engine: headless reads and explicit `site_publish` run in-process; browser tools route by scope to the connector owner's **open Site or Content workspace** through the `(userId, scope)` live bridge (`server/ai/mcp/editorBridge.ts` + `useMcpWorkspaceBridge`). The live workspace is the single source of truth for edits (no headless DB-mutating page-tree tool, which would desync), and writes remain drafts until the explicitly capability-gated publish call. Feature doc: [`docs/features/mcp-connectors.md`](docs/features/mcp-connectors.md).
- **Tree primitive:** Every tree-of-nodes — pages, Visual Components, slot fills — uses one shape: `NodeTree` in `src/core/page-tree/treeSchema.ts`. Mutations are tree-agnostic. Reference: [`docs/reference/page-tree.md`](docs/reference/page-tree.md).
- **Publishing:** Three-layer pipeline. **Layer A** bakes fully-static pages to `uploads/published/current/.html` at publish time via a two-slot pointer-file swap (`server/publish/staticArtefact.ts`; `current` is a plain file naming the active slot — symlink-free so it works for unprivileged Windows users). **Layer B** is an in-memory LRU keyed by `(urlPath, queryString, publishVersion)` for dynamic routes (`server/publish/renderCache.ts`); `bumpPublishVersion()` evicts wholesale on every publish. **Layer C** emits `` placeholders for nodes auto-detected as request-dependent; a ~668 B `IntersectionObserver` runtime lazy-fetches each fragment from `/_instatic/hole/`. Auto-detection lives in `src/core/publisher/dynamicDetection.ts` — one walker, four rules. Single entry: `server/publish/publicRouter.ts:renderPublicResolution`. Full design: [`docs/features/publisher.md`](docs/features/publisher.md).
- **Tests:** `bun test`. Architectural rules in `src/__tests__/architecture/*` — when *your* change drifts a structural rule, fix the rule's gate test in the same change.
### Repo layout
```
server/         Bun server: router, handlers, repositories, auth, plugins, publish, db
src/admin/      Admin app (React) — shell, workspaces, plugin host UI
src/admin/pages/site/   Visual editor (canvas, panels, toolbar, editor store)

## Operational Directives
1. **Domain Expertise**: Operate strictly according to the architecture, patterns, and principles established by `Instatic`.
2. **Codebase Navigation**: When consulting or adapting patterns from this agent, inspect the local files in [`agents/CoreBunch__Instatic/`](file:///root/masteragents/agents/CoreBunch__Instatic).
3. **Execution & Tooling**: Apply surgical changes, adhere to clean coding standards, and verify all actions thoroughly.
