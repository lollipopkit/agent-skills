---
name: codex-clean-history
description: Clean Codex local history artifacts that can contain logs, prompts, user input text, command traces, and session transcripts while preserving memories and configuration. Use when the user asks to delete, purge, wipe, prune, reset, or preview Codex history/log/session/input records, especially `~/.codex/history.jsonl`, `~/.codex/sessions/`, `~/.codex/log/`, `~/.codex/logs_*.sqlite`, or shell snapshots, and explicitly not memories.
---

# Codex Clean History

## Quick Start

Use `scripts/clean_codex_history.py` to inspect or clean local Codex history artifacts. The script defaults to dry-run and preserves memory, configuration, authentication, rules, skills, plugins, cache, and goal/state databases.

```bash
python3 /path/to/codex-clean-history/scripts/clean_codex_history.py
python3 /path/to/codex-clean-history/scripts/clean_codex_history.py --apply
python3 /path/to/codex-clean-history/scripts/clean_codex_history.py --codex-home ~/.codex --days 30 --apply
```

## Workflow

1. Resolve Codex home from `--codex-home`, `$CODEX_HOME`, or `~/.codex`.
2. Run the script without `--apply` first and show the user the planned deletions.
3. If the user asked to actually clean, rerun with `--apply`.
4. If the user asks to keep recent history, pass `--days N` to remove only matching artifacts older than N days.
5. If the user asks to include or exclude specific categories, use the script flags instead of manually deleting files.

## Cleanup Scope

Default targets:

- `history.jsonl`
- `sessions/`
- `log/`
- `logs_*.sqlite`, including `-wal` and `-shm` sidecars
- `shell_snapshots/`
- temporary Codex files under `.tmp/` and `tmp/`

Never target these by default:

- `memories/`
- `memories_*.sqlite`, including sidecars
- `config.toml`
- `auth.json`
- `rules/`
- `skills/`
- `plugins/`
- `cache/`
- `goals_*.sqlite`
- `state_*.sqlite`
- `models_cache.json`
- `installation_id`
- `version.json`

## Safety Rules

- Prefer the script over ad hoc `rm` commands.
- Keep dry-run output in the response when the user asks what would be removed.
- Do not clean memories unless the user explicitly changes the requirement.
- If Codex is currently running, warn that open sessions may recreate log/session files after cleanup.
