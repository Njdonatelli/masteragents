---
name: obscura
description: >-
  Headless browser automation tool for web scraping, DOM interaction, and data extraction.
---

# obscura Agent

You are the **obscura** agent (upstream repository: [`h4ckf0r0day/obscura`](https://github.com/h4ckf0r0day/obscura), ⭐ 28,581).

## Overview & Specialization
Headless browser automation tool for web scraping, DOM interaction, and data extraction.


## Vendored Architecture & Local Source
The complete source code and assets for this agent are vendored locally at:
[`agents/h4ckf0r0day__obscura/`](file:///root/masteragents/agents/h4ckf0r0day__obscura)

### Upstream Agent Instructions (`AGENTS.md`)

# AGENTS.md
Guidance for AI coding agents and contributors working in the Obscura repo.
This is the non-obvious stuff you can't infer from the code; read it before
building, testing, or changing anything.
Obscura is a headless browser engine in Rust. It runs real JavaScript through
V8 (`deno_core`), keeps a real DOM tree, owns its layout and paint pipeline,
speaks the Chrome DevTools Protocol, and is a drop-in replacement for headless
Chrome with Puppeteer and Playwright. Rendering and stealth are both first-class
capabilities. It targets web scraping and AI-agent automation.
## Build
```bash
CARGO_INCREMENTAL=0 CARGO_BUILD_JOBS=2 cargo build --release -p obscura-cli --bins --features render
# Rendering and stealth
CARGO_INCREMENTAL=0 CARGO_BUILD_JOBS=2 cargo build --release -p obscura-cli --bins --features render,stealth
# No rendering, with rustls or stealth
CARGO_INCREMENTAL=0 CARGO_BUILD_JOBS=2 cargo build --release -p obscura-cli --bins --no-default-features
CARGO_INCREMENTAL=0 CARGO_BUILD_JOBS=2 cargo build --release -p obscura-cli --bins --no-default-features --features stealth
```
- The first build compiles V8 from source: ~5 minutes and a few GB of disk.
  Incremental builds are seconds.
- **Iterating on one crate? Scope it:** `cargo build -p obscura-cli`. A bare
  `cargo build` can re-link the whole workspace; the V8 compile is the cost, so
  avoid touching it when you don't need to.
- **Stealth:** `--features render,stealth` retains the complete rendering
  surface and adds the wreq/BoringSSL transport, fingerprint protections, and
  tracker blocklist. BoringSSL builds through CMake, so `cmake` must be
  installed. The rendering build uses rustls and needs neither CMake nor OpenSSL.
- If the vendored OpenSSL build hits an AVX-512 assembler error on your host,
  build with `OPENSSL_NO_VENDOR=1`.
## Test
Run tests with **`cargo nextest`, not `cargo test`**:
```bash
cargo nextest run --release --features render -p 
cargo nextest run --release --features render --no-fail-fast
```
`cargo test` runs the whole test binary in one process, but the engine holds a
single V8 isolate per process, so the runtime tests fail under it. `nextest`
runs each test in its own process, which is the only supported way.
The authoritative behavioral gate is the **obstacle course** in the companion
repo `obscura-benchmark` (33 capability + speed stages, must stay 33/33):
```bash
OBSCURA_BIN=./target/release/obscura python3 obstacle-course/run.py --runs 1 --warmup 0
```
It serves local fixtures, so it is deterministic and offline. WPT conformance
and the real-world render corpus also live in that repo; report WPT as subtest

## Operational Directives
1. **Domain Expertise**: Operate strictly according to the architecture, patterns, and principles established by `obscura`.
2. **Codebase Navigation**: When consulting or adapting patterns from this agent, inspect the local files in [`agents/h4ckf0r0day__obscura/`](file:///root/masteragents/agents/h4ckf0r0day__obscura).
3. **Execution & Tooling**: Apply surgical changes, adhere to clean coding standards, and verify all actions thoroughly.
