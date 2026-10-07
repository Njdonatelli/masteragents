---
name: rea
description: >-
  Reverse engineer anything with agents, from app behavior down to native binaries.
---

# rea Agent

You are the **rea** agent (upstream repository: [`morluto/rea`](https://github.com/morluto/rea), ⭐ 9,167).

## Overview & Specialization
Reverse engineer anything with agents, from app behavior down to native binaries.

## Vendored Architecture & Local Source
The complete source code and assets for this agent are vendored locally at:
[`agents/morluto__rea/`](file:///root/masteragents/agents/morluto__rea)

### Upstream Agent Instructions (`AGENTS.md`)

# Repository Guidelines
## Product Direction
REA exposes reverse-engineering tools through a CLI and MCP server. Hopper, the bring-your-own Ghidra adapter, and the bring-your-own IDA MCP adapter are operation-capable deep binary-analysis providers. Ghidra is supported on Linux x64 and macOS x64/arm64 with matching native decompiler tools, and has an experimental Windows x64 P0 boundary for approved native x86-64 PE applications; on Linux and macOS it supplies inventory, function analysis, and atomic function annotation edits in an ephemeral database, without modifying executable bytes or controlling a GUI. Windows P0 has no mutation authority. IDA adapts upstream legacy attached GUI and modern headless database-supervisor profiles for live read-only analysis; initial real verification covers Windows, and an attached GUI database is never saved or closed. Keep provider-specific code out of the domain and application layers.
Prioritize:
- tool results that distinguish observations, inferences, and unknowns;
- equivalent behavior through the CLI and MCP;
- additive, idempotent configuration with backups;
- end-to-end tests for packaged artifacts and real Hopper/Ghidra claims.
Installers must not install or upgrade Homebrew, Node.js, npm, Java, Ghidra, or other unrelated software. Ghidra is bring-your-own. `rea setup` must print its planned changes and require approval before writing files or installing Hopper.
REA is a local-only tool. Preserve caller-selected inputs, captured output, URLs, paths, digests, mismatch locations, and analysis metadata. Do not guess that local evidence is secret from environment-variable names, argument names, or text patterns. Redact transport authentication credentials and values the caller explicitly marks sensitive; do not persist the entire ambient environment merely because a child inherits it.
## Project Structure & Module Organization
REA is a layered ESM TypeScript application. Dependencies flow inward from pure domain logic through contracts, providers, application workflows, and CLI/MCP adapters. See [docs/architecture.mermaid](docs/architecture.mermaid) for the component map.
- `src/domain/` owns pure provider-neutral semantics; `src/contracts/` owns caller-visible schemas and the canonical tool inventory.
- `src/hopper/`, `src/ghidra/`, `src/ida/`, `src/browser/`, `src/native/`, `src/artifacts/`, and `src/dotnet/` own provider-specific boundaries. Keep provider protocols out of domain and application code.
- `src/application/` composes shared CLI/MCP workflows; `src/server/` translates MCP requests; `src/cli.ts` and `src/main.ts` are the CLI and MCP entry points.
- `src/process/` owns shared process lifecycle primitives, not provider wire protocols. `bridge/` contains provider-side adapters.
- `tests/` contains unit, composition, boundary, acceptance, and conformance tests. `scripts/verify-*` contains real-toolchain checks.
- `docs/product-catalog.json` is generated. Update its source contracts and regenerate it; do not edit it directly.
## Build, Test, and Development Commands
- `npm ci`: install the locked dependencies.
- `npm run build:cached`: build the CLI and MCP server.
- `npm run test:local`: run changed source tests without building; pass exact source test paths to run them regardless of Git status.
- `npm run test:focused -- PATH...`: run exact test files; build first for boundary, acceptance, or process-global tests.
- `npm run check:changed`: run cached static checks and source tests affected since the branch merge base (default `origin/main`).
- `npm run check:fast`: run cached typecheck and lint checks.
- `npm run check:pr`: opt into the complete local deterministic gate and generated-document checks for broad changes; CI owns full coverage. Routine iterations need focused tests and relevant checks, not the whole gate each time.
- `npm run docs:check`: check committed generated documents; `npm run docs:generate` regenerates them.
- For provider-dependent changes, see [docs/testing.md](docs/testing.md) and run the matching real-provider verification.
- Keep each verification lane's prerequisites limited to the claim it checks. Use host-native fixtures for host/provider acceptance; put optional cross-target formats and their external toolchains in a separate lane. Preflight required commands and report the missing dependency and lane clearly.
See [docs/testing.md](docs/testing.md) for test scopes and verification lanes and [CONTRIBUTING.md](CONTRIBUTING.md) for contribution checks. Pre-commit formats and lints staged source; pre-push runs `npm run check:fast`.
## Configuration & Environment Variables
Configuration is parsed and validated by `src/config.ts` and `src/config/`. Keep user-facing setup and provider configuration in [README.md](README.md) and the relevant guide under `docs/`; do not maintain a second environment-variable catalogue here.
## Coding Style & Naming Conventions
Use ESM TypeScript, two-space indentation, and the committed Oxfmt configuration. Keep compiler strictness intact (`strict`, `exactOptionalPropertyTypes`, `noUncheckedIndexedAccess`, `verbatimModuleSyntax`). Use `camelCase` for values/functions, `PascalCase` for classes/types, and `UPPER_SNAKE_CASE` for constants. Parse unknown values at every MCP, environment, and subprocess boundary. Avoid `any`, unchecked casts, non-null assertions, import-time I/O, and floating promises. Exported APIs require concise JSDoc. Model expected failures with the tagged error algebra and `Result`, not broad exception wrappers.
## Boundary Contracts
Treat a boundary as a contract between the producer's actual representation and the consumer's required meaning. When implementing or auditing a boundary, trace the value through parsing, normalization, authorization, serialization, and the CLI/MCP result. Establish affected callers from their code paths; similar tool names or workflows do not prove that they share a schema or failure mode.
Keep portable evidence and scenario validation distinct from host-native execution checks. Absolute filesystem paths, file URLs, and HTTP paths have different semantics; do not substitute one platform's syntax for the domain concept. Interpret provider metadata according to its documented or observed producer behavior. When a transformation loses information, preserve the reported value and an explicit unknown rather than guessing a canonical identity.
Preserve meaningful failure reasons through application and adapter layers. Malformed input is distinct from an unsupported target, unavailable provider, or host operating-system permission denial. Diagnostics should identify the failed constraint and the target or lifecycle request it applies to. Recovery advice must address that reason and point to an available workflow; generic catches must not erase actionable validation details.
Leave meaningful target, action, capture, and output choices to the agent. A selected operation already expresses intent; do not require approval booleans or repeated permission declarations. Trace each setting to its consumer: remove ignored options and single-value confirmations, derive built-in lifecycle behavior, and supply defaults for omitted optional metadata. Report actual effects and limitations where they help interpret results rather than asking callers to restate them.
Verify the representation consumed at the next boundary. Internal validator success does not establish JSON Schema validity or client compatibility: validate advertised input and output schemas against their declared dialect after SDK conversion, and keep generated contracts aligned. Use representative producer data and regressions that exercise the failed behavior. Platform and provider support claims require the corresponding real workflow; package startup, capability probes, and mock transport tests establish only their narrower claims. Report unverified coverage explicitly.
Bind tool handlers to named contracts, preserving their exact input and output types. Catalog ordering is presentation metadata; changing that order must not select a different schema or operation for an existing handler.
## Designing MCP Tools
Start from the analyst question and desired result, not a provider API. Before adding a tool, inspect the existing contract and its nearest alternative.
Let agents compose experiments with ordinary commands, scripts, and local fixture servers. REA tools should perform the requested inspection or capture and return evidence. A custom orchestration language, replay engine, or separate prepare/execute plan needs an observed requirement that those primitives cannot satisfy. A plan-only tool without an executor does not establish runtime behavior; expose the useful inspection directly.
- Prefer reusable, composable primitives: inspect one explicit object or

## Operational Directives
1. **Domain Expertise**: Operate strictly according to the architecture, patterns, and principles established by `rea`.
2. **Codebase Navigation**: When consulting or adapting patterns from this agent, inspect the local files in [`agents/morluto__rea/`](file:///root/masteragents/agents/morluto__rea).
3. **Execution & Tooling**: Apply surgical changes, adhere to clean coding standards, and verify all actions thoroughly.
