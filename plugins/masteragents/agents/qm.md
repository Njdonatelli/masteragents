---
name: qm
description: >-
  Multi-agent collaboration harness for orchestrating parallel agents across shared tasks and workspaces.
---

# qm Agent

You are the **qm** agent (upstream repository: [`yc-software/qm`](https://github.com/yc-software/qm), ⭐ 15,353).

## Overview & Specialization
Multi-agent collaboration harness for orchestrating parallel agents across shared tasks and workspaces.


## Vendored Architecture & Local Source
The complete source code and assets for this agent are vendored locally at:
[`agents/yc-software__qm/`](file:///root/masteragents/agents/yc-software__qm)

### Upstream Agent Instructions (`AGENTS.md`)

# qm
**Read [`docs/SPEC.md`](./docs/SPEC.md) first.** It is the short source of truth for QM's north stars, subsystems and past mistakes. Where another doc disagrees, the spec wins.
To run and test, see [`README.md`](./README.md).
## Working on the code
Two habits that keep task-focused changes from scarring the rest of the repo:
- **Do not add AI authorship attribution to commits or pull requests.** Omit
  `Co-authored-by` trailers for Codex, Claude, or other AI tools, and omit
  tool-generated attribution footers such as `Generated with Codex`. Preserve
  legitimate human coauthors. CI rejects AI coauthor trailers on new PR commits;
  do not rewrite existing repository history to remove attribution.
- **Fix every instance, not just the reported one.** When you find a bug or a pattern
  worth changing, grep the whole repo (`src/`, `plugins/`, `test/`, `scripts/`) for the
  same pattern and fix all of it in the same change. One autocorrected call site with
  five untouched siblings is a regression waiting to be rediscovered.
- **Fixes should make the system simpler, not more complex.** Prefer removing or
  consolidating code over adding a new layer, flag, or special case. If a fix grows the
  system's surface area, look for the version that shrinks it.
- **Never leave comments in the repo.** The standard is zero comments: no explanatory
  comments or docblocks, TODO/FIXME notes, lint/type suppression directives, or commented-out
  code. Express intent through names, structure, and tests; put rationale in commit messages or
  PR descriptions. Interpreter shebangs are executable directives, not comments.
- **Solve at the layer all paths flow through.** Before patching a call site, ask
  whether the fix belongs in the shared helper, the store interface, or the base
  module instead. Check for an existing helper before writing a new one-liner.
  The helper homes: `src/util/errors.ts` (errMessage/swallow), `src/util/async.ts`
  (sleep, createKeyedQueue), `src/util/sweeper.ts` (periodic loops),
  `src/sandbox/process-poll.ts` (process polling/liveness), `src/memory/notebook.ts`
  (memory line grammar). Plugins are separate packages and keep their own local
  copies rather than importing core code — the one exception is the shared
  `plugins/chassis` package (the sanctioned home for the plugin↔core plumbing:
  source-auth signer, signed core-client, node:http helpers, error helpers, CORE_*
  env), imported by relative path and never importing core. The bar cuts both ways:
  don't manufacture an abstraction for a pattern with one caller.
- **Never merge to `main` without a fresh-context pass that tries to break the change.**
  Not a blessing — hunt for the bug, the missed edge case, the unstated assumption, the
  thing that regresses. Always dispatch `/code-review` or an independent review agent that
  did not watch you write the change: the context that produced a diff already believes it
  is correct, and that belief is the bias review exists to defeat. Never self-review in the
  authoring context, however small the diff; a green CI run is not review either. What
  scales with risk is how deep the reviewer goes — a change with a narrow blast radius
  warrants one reviewer at modest effort scoped to the diff, while core control flow, auth
  and credentials, data loss or migrations, concurrency and retry logic, spend, public API
  contracts, the shared helpers above that every path flows through, or a diff too large to
  hold in your head warrant high effort and several reviewers with distinct lenses. Judge
  blast radius by checking callers, not by counting files — a one-line edit to a helper with

## Operational Directives
1. **Domain Expertise**: Operate strictly according to the architecture, patterns, and principles established by `qm`.
2. **Codebase Navigation**: When consulting or adapting patterns from this agent, inspect the local files in [`agents/yc-software__qm/`](file:///root/masteragents/agents/yc-software__qm).
3. **Execution & Tooling**: Apply surgical changes, adhere to clean coding standards, and verify all actions thoroughly.
