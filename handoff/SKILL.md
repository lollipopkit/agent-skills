---
name: handoff
description: Create concise, evidence-based handoff notes for another AI coding agent. Use when the user asks for a handoff, continuity note, next-agent summary, progress transfer, "告诉别的 agent", "handoff skill", "交接", or wants the current state, completed work, remaining plan items, risks, and next steps captured for another agent without writing a verbose work log.
---

# Handoff

## Goal

Write a handoff that lets a fresh agent continue from the current state without replaying the conversation. Prefer authoritative workspace evidence over memory or intent.

## Workflow

1. Inspect current state before writing:
   - Read the user request and the active goal or plan.
   - Check `git status --short` and relevant diffs.
   - Verify named files, tests, generated artifacts, and command results if they matter.
   - Do not assume previous summaries are current when cheap verification is available.

2. Identify the durable facts:
   - Objective and scope.
   - Hard constraints from the user, repo, or plan.
   - Completed changes with file paths and behavior impact.
   - Verified commands and their outcomes.
   - Current dirty/untracked/staged state if relevant.
   - Known risks, near limits, blockers, and forbidden edits.
   - Next concrete work, in priority order.
   - Larger plan items still incomplete.

3. Write the handoff as a transfer note, not a narrative:
   - Use concise sections.
   - Include enough file paths and command names for navigation.
   - Avoid chronological logs, praise, speculation, and implementation diary.
   - Mark uncertain items as uncertain.
   - Call out anything the next agent must not touch.

## Recommended Shape

Use this structure when it fits:

```markdown
**目标**
[One or two sentences.]

**硬约束**
- [Constraints the next agent must preserve.]

**已完成**
- [Durable completed work, with file paths where useful.]

**已验证**
- `[command]`: [result]

**当前状态**
- [Dirty worktree, staged/unstaged, generated artifacts, notable limits.]

**下一步**
1. [Most important concrete action.]
2. [Next action.]

**完整计划仍缺**
- [Remaining broad items from the real objective/plan.]
```

## Rules

- Keep the handoff in the user's requested language; default to the conversation language.
- Do not write or update repository files unless the user explicitly asks for a file artifact.
- If writing a file artifact, ask or infer the target path from the user request; otherwise reply in chat.
- Do not include low-value command-by-command narration.
- Do not claim a requirement is complete unless current evidence proves it.
- Preserve the original objective; do not redefine success around the last completed subset.
- Mention validation gaps explicitly when tests or audits were not run.
- For coding handoffs, include line-count or file-size risks only when they affect next work.
