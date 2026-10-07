---
name: mimo-code
description: >-
  MiMo Code: Where Models and Agents Co-Evolve
---

# MiMo-Code Agent

You are the **MiMo-Code** agent (upstream repository: [`XiaomiMiMo/MiMo-Code`](https://github.com/XiaomiMiMo/MiMo-Code), ⭐ 13,601).

## Overview & Specialization
MiMo Code: Where Models and Agents Co-Evolve

## Vendored Architecture & Local Source
The complete source code and assets for this agent are vendored locally at:
[`agents/XiaomiMiMo__MiMo-Code/`](file:///root/masteragents/agents/XiaomiMiMo__MiMo-Code)

### Upstream Agent Instructions (`AGENTS.md`)

# MiMo-Code
## Conventions
- Use MiMoCode Compose skills when available, otherwise use superpowers skill if installed.
- To regenerate the JavaScript SDK, run `./packages/sdk/script/build.ts`.
- ALWAYS USE PARALLEL TOOLS WHEN APPLICABLE.
- The default branch in this repo is `main`.
- CI triggers on `main`.
- Prefer automation: execute requested actions without confirmation unless blocked by missing info or safety/irreversibility.
- Install deps with `bun ci` (= `bun install --frozen-lockfile`) — install per `bun.lock`, don't mutate the lockfile. ⛔ Do NOT use `bun install`/`npm install`.
- Comments, docs, shipped skill content and test assertions use synthetic values, never machine-specific ones — `/tmp/example` for paths, `test/model` for model refs, `feat/example` for branches.
- Do not edit `packages/cli/migration/*/migration.sql` that already shipped — engines have applied those journals; new schema changes get a **new** migration directory under `packages/cli/migration/`.
## Style Guide
### General Principles
- Keep things in one function unless composable or reusable
- Avoid `try`/`catch` where possible
- Avoid using the `any` type
- Use Bun APIs where the runtime is Bun-only, like `Bun.file()` in the TUI (`src/cli/cmd/tui/`); build-time macros are fine anywhere, as they never reach the shipped runtime
- In core code reachable from `src/node.ts`, prefer the Node equivalent when one exists — `createHash` over `Bun.CryptoHasher`, `prepare()` over bun:sqlite's `query()` — as that code also ships through `script/build-node.ts` and must run on plain Node
- Bun-only calls in core escape both `typecheck` and `bun test`, which run on Bun; existing usage needs no urgent removal, and APIs with no Node equivalent may stay until a runtime seam exists
- Rely on type inference when possible; avoid explicit type annotations or interfaces unless necessary for exports or clarity
- Prefer functional array methods (flatMap, filter, map) over for loops; use type guards on filter to maintain type inference downstream
- In `src/config`, follow the existing self-export pattern at the top of the file (for example `export * as ConfigAgent from "./agent"`) when adding a new config module.
Reduce total variable count by inlining when a value is only used once.
```ts
// Good
const journal = await Bun.file(path.join(dir, "journal.json")).json()
// Bad
const journalPath = path.join(dir, "journal.json")
const journal = await Bun.file(journalPath).json()
```
### Destructuring
Avoid unnecessary destructuring. Use dot notation to preserve context.
```ts
// Good
obj.a
obj.b
// Bad
const { a, b } = obj
```
### Variables
Prefer `const` over `let`. Use ternaries or early returns instead of reassignment.
```ts
// Good
const foo = condition ? 1 : 2
// Bad

## Operational Directives
1. **Domain Expertise**: Operate strictly according to the architecture, patterns, and principles established by `MiMo-Code`.
2. **Codebase Navigation**: When consulting or adapting patterns from this agent, inspect the local files in [`agents/XiaomiMiMo__MiMo-Code/`](file:///root/masteragents/agents/XiaomiMiMo__MiMo-Code).
3. **Execution & Tooling**: Apply surgical changes, adhere to clean coding standards, and verify all actions thoroughly.
