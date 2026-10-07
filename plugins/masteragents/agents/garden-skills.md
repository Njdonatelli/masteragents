---
name: garden-skills
description: >-
  Toolkit for web styling, search retrieval, image synthesis, and frontend workflow utilities.
---

# garden-skills Agent

You are the **garden-skills** agent (upstream repository: [`ConardLi/garden-skills`](https://github.com/ConardLi/garden-skills), ⭐ 12,754).

## Overview & Specialization
Toolkit for web styling, search retrieval, image synthesis, and frontend workflow utilities.


## Vendored Architecture & Local Source
The complete source code and assets for this agent are vendored locally at:
[`agents/ConardLi__garden-skills/`](file:///root/masteragents/agents/ConardLi__garden-skills)

### Repository Synopsis (`README.md`)

# Garden Skills
**A curated collection of production-ready [Agent Skills](https://support.claude.com/en/articles/12512176-what-are-skills) for Claude Code, Cursor, Codex, and other AI coding agents.**
web-video-presentation
Web video / presentation
web-design-engineer
Design / frontend
gpt-image-2
Image generation / prompting
beautiful-article
Any source → beautiful article
[](./LICENSE)
[](https://github.com/ConardLi/garden-skills/stargazers)
[](#contributing)
[](#skills-gallery)
[](https://agentskills.io)
[English](./README.md) · [中文文档](./README.zh-CN.md) · [日本語](./README.ja-JP.md)
---
## Table of contents
| Install | Use | Contribute |
|---|---|---|
| [Install](#install)[`skills` CLI (npx)](#option-a--skills-cli-npx)[Claude Code plugin marketplace](#option-b--claude-code-plugin-marketplace)[Pinned `.zip` from Releases](#option-c--pinned-zip-from-releases)[Manual copy](#option-d--manual-copy-into-your-project)[Git submodule](#option-e--git-submodule) | [Compatibility](#compatibility)[What is a Skill?](#what-is-a-skill) | [Contributing](#contributing)[Acknowledgments](#acknowledgments)[License](#license) |
---
### [`web-video-presentation`](./skills/web-video-presentation)
**Category:** Web Video / Presentation Engineering  
**Best for:** turning scripts, articles, lessons, product demos, and talks into click-driven 16:9 web presentations that can be screen-recorded as cinematic videos.
`web-video-presentation` builds record-ready Vite + React + TypeScript presentations that behave like video production surfaces. The workflow turns raw articles into narration scripts, maps script beats to full-screen scenes, pauses at required checkpoints, and can optionally synthesize narration audio after the visual outline is approved.
Highlights:
- Fixed 1920×1080 stage that scales to the viewport for stable screen recording
- Click / keyboard driven `(chapter, step)` cursor, with one narration beat per visual step
- Hard collaboration checkpoints for script, theme, outline, implementation mode, and optional audio
- Hidden hover-only progress controls so the stage stays clean while recording
- Theme-token architecture with **23 built-in themes**, each with its own design signature — editorial, terminal, engineering, Swiss International, and more
- **Pluggable TTS** — provider-agnostic audio runner; ships **two built-in providers** (MiniMax `mmx-cli` + OpenAI TTS via curl) plus a contract + ready-to-paste snippets for ElevenLabs / edge-tts / Azure / Google Cloud / macOS `say`
- Scaffolded Vite + React + TypeScript project with reusable stage primitives and recording guidance
creative-voltagecreative talks

## Operational Directives
1. **Domain Expertise**: Operate strictly according to the architecture, patterns, and principles established by `garden-skills`.
2. **Codebase Navigation**: When consulting or adapting patterns from this agent, inspect the local files in [`agents/ConardLi__garden-skills/`](file:///root/masteragents/agents/ConardLi__garden-skills).
3. **Execution & Tooling**: Apply surgical changes, adhere to clean coding standards, and verify all actions thoroughly.
