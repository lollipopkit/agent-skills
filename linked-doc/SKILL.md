---
name: linked-doc
description: Maintain an evolving linked documentation library for project wikis, ADRs, design notes, research notes, release notes, and decision logs. Use when asked to create, grow, repair, reorganize, or verify a wiki/ADR knowledge base with Markdown pages, YAML frontmatter, Obsidian-style [[wikilinks]], source-backed citations, llmwiki/llm-wiki-compiler projects, or a durable project memory that should compound over time instead of being rewritten from scratch.
---

# Maintain Linked Doc Library

## Core Rule

Treat the documentation library as compiled project knowledge, not loose prose. Preserve source evidence, link related pages deliberately, and make every update incremental: add or correct the smallest set of source documents/pages needed, then run the library's own validation commands before claiming it is healthy.

For llmwiki projects, read `references/llmwiki-project-model.md` when you need exact directory conventions, CLI commands, citation syntax, schema rules, review queue behavior, or quality gates.

## Workflow

1. Inspect the repository before editing. Locate `sources/`, `wiki/`, `.llmwiki/`, `docs/adr/`, `docs/decisions/`, or existing Markdown conventions. If a specific file is mentioned, open it first.
2. Classify the request:
   - **Ingest/grow**: add raw source notes, ADRs, meeting notes, code-review findings, issue summaries, or external docs into the source area.
   - **Compile/update**: regenerate linked pages from sources using the local toolchain when available.
   - **Repair**: fix broken wikilinks, missing summaries, stale ADR status, malformed frontmatter, bad citations, duplicate concepts, or orphaned pages.
   - **Curate**: split/merge pages, add overview/map pages, normalize titles, or improve cross-links without inventing unsupported facts.
3. Prefer source-first changes. Put durable facts in source documents or ADRs, then let generated wiki pages update from those sources when the repo supports compilation.
4. Preserve generated boundaries. Do not hand-edit generated `wiki/` pages unless the project clearly treats them as hand-maintained or the user explicitly asks for a direct correction.
5. Keep titles and slugs stable. Rename pages only when the old title is wrong enough to justify updating every incoming `[[wikilink]]`.
6. Add bidirectional navigation where it helps retrieval: page-to-overview, overview-to-page, ADR-to-affected-component, component-to-ADR.
7. Validate with the repository's documented checks. For llmwiki projects, prefer `llmwiki next`, `llmwiki lint`, and `llmwiki eval`; use `compile --review` when generated changes need approval.

## Page Shape

Use this minimum Markdown page contract unless the project already has a stricter one:

```markdown
---
title: Human Readable Title
summary: One sentence that explains why this page exists.
kind: concept
sources:
  - source-note.md
createdAt: "2026-06-01T00:00:00.000Z"
updatedAt: "2026-06-01T00:00:00.000Z"
---

# Human Readable Title

Concise grounded explanation with a citation when the library supports it. ^[source-note.md:1-8]

Related: [[Another Page]], [[Project ADR Index]]
```

For ADR sources, use `assets/adr-source.template.md` as a starting point. For llmwiki schema initialization, use `assets/llmwiki-schema.template.json` only when the project needs explicit page-kind policy instead of defaults.

## Maintenance Rules

- Evidence beats memory. When correcting a page, trace the claim to a source file, ADR, issue, commit, or code location before rewriting it.
- Separate decisions from status. ADR pages record accepted/rejected/superseded decisions; progress or implementation status belongs in linked notes unless the project convention says otherwise.
- Do not erase history silently. When a decision changes, mark the old ADR as superseded and link to the replacement.
- Keep generated indexes generated. If an index is auto-built, update inputs and rerun generation instead of manually patching the index.
- Make links useful, not decorative. Add `[[wikilinks]]` for concepts a reader would reasonably traverse.
- Prefer small pages with strong links over giant catch-all documents, except for intentional overview/map pages.
- For multilingual docs, keep language pairs linked at the top and avoid mixing languages inside one page unless the project already does.

## Validation

For llmwiki-backed libraries:

```bash
llmwiki next
llmwiki compile --review
llmwiki review list
llmwiki lint
llmwiki eval
```

For non-llmwiki Markdown/ADR libraries, validate structurally:

```bash
rg -n "\[\[[^]]+\]\]" docs wiki
rg -n "status:|supersedes:|supersededBy:|sources:" docs wiki
```

Then inspect the affected pages directly. Report any validation command that could not run and why.
