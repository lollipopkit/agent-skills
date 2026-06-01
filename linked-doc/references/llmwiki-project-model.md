# llmwiki Project Model

Use this reference when maintaining a linked documentation library built with `llm-wiki-compiler` / `llmwiki`.

## Directory Contract

- `sources/`: raw source documents. Add durable project facts here first when the wiki is generated.
- `wiki/concepts/`: compiled concept/entity/comparison/overview pages.
- `wiki/queries/`: saved query answers, included in retrieval and indexes.
- `wiki/index.md`: generated table of contents. Do not hand-maintain unless the project has no generator.
- `.llmwiki/schema.json`: optional page-kind and cross-link policy.
- `.llmwiki/candidates/`: review queue from `llmwiki compile --review`.
- `.llmwiki/eval/`: eval reports, history, thresholds, and citation judgement cache.

## Page Frontmatter

Generated pages commonly carry:

```yaml
---
title: Knowledge Compilation
summary: Techniques for compiling scattered source material into linked reference pages.
kind: concept
sources:
  - architecture-notes.md
confidence: 0.82
provenanceState: merged
contradictedBy:
  - slug: older-design-note
createdAt: "2026-04-05T12:00:00Z"
updatedAt: "2026-04-05T12:00:00Z"
---
```

Allowed built-in `kind` values are `concept`, `entity`, `comparison`, and `overview`. Defaults treat all pages as `concept` when no schema exists.

## Links and Citations

- Wikilinks use Obsidian-style `[[Page Title]]` or `[[page-slug|Display Title]]`.
- Paragraph citations use `^[source.md]`.
- Claim-level citations use line ranges: `^[source.md:42-58]` or `^[source.md#L42-L58]`.
- Put citations at the end of prose paragraphs or sentences, not on headings, list items, or code blocks.
- Do not cite YAML frontmatter as evidence for substantive claims.
- Leave true inference uncited so lint/eval can surface inferred paragraphs.

## Commands

Use `llmwiki next` first when project state is unclear. It is read-only and recommends the next action.

Common lifecycle:

```bash
llmwiki ingest <source>
llmwiki compile
llmwiki compile --review
llmwiki review list
llmwiki review show <id>
llmwiki review approve <id>
llmwiki review reject <id>
llmwiki lint
llmwiki eval
llmwiki context "<prompt>" --json
llmwiki view --open
```

Use `compile --review` for uncertain or high-blast-radius updates. Candidates land in `.llmwiki/candidates/`; approving refreshes `wiki/`, index/MOC, and embeddings. Source state for multi-candidate source updates is deferred until the final sibling candidate is approved.

## Schema Guidance

Use schema only when the library needs explicit policy. Good triggers:

- ADR libraries need `overview` map pages and stronger cross-link minimums.
- Entity pages should link to decisions, systems, owners, or related components.
- Comparison pages should link to all compared alternatives.

Starter schema shape:

```json
{
  "version": 1,
  "defaultKind": "concept",
  "kinds": {
    "concept": { "minWikilinks": 0 },
    "entity": { "minWikilinks": 1 },
    "comparison": { "minWikilinks": 2 },
    "overview": { "minWikilinks": 3 }
  },
  "seedPages": []
}
```

## Quality Gates

Run `llmwiki lint` after structural changes. Important rules include broken wikilinks, orphaned pages, missing summaries, duplicate concepts, empty pages, malformed or missing citations, low confidence, contradicted pages, and excess uncited inferred paragraphs.

Run `llmwiki eval` when the user asks for quality, regression checks, CI readiness, or proof that the documentation library remains trustworthy. Eval reports health score, citation coverage/precision, corpus stats, optional citation support, and trend deltas.

## ADR Library Pattern

For project ADRs, prefer this source-first flow:

1. Add or update an ADR source note with status, context, decision, consequences, supersedes/supersededBy links, and affected components.
2. Link related components and concepts with `[[wikilinks]]`.
3. Compile with `llmwiki compile --review`.
4. Inspect candidates for unsupported claims and stale links.
5. Approve candidates, then run `llmwiki lint`.

Keep ADR pages factual and stable. Put implementation progress, checklists, and handoff notes in separate linked pages unless the project explicitly wants them inside the ADR.
