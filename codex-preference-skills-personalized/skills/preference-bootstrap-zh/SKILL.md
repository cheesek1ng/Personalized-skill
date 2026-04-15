---
name: preference-bootstrap-zh
description: Load the stored long-term user preference model at the start of a session and convert it into actionable defaults for the current task. Use when the user says "先按我的偏好来", "读取我的画像", "看看我的长期喜好再回答", "按我平时的风格执行", or when a new chat should inherit tone, formatting, autonomy, planning, and decision defaults from the saved profile.
---

# Preference Bootstrap Zh

Read the stored preference model and compress it into a session contract. Optimize for immediately usable defaults, not a long recap.

## Workflow

1. Run `python3 scripts/preference_store.py ensure`.
2. Run `python3 scripts/preference_store.py show --format brief`.
3. Prefer this skill as a manual reload or inspection tool. For the most token-efficient default behavior across all sessions, pair the model with a global `AGENTS.md` rule that reads `session-brief.md` automatically at conversation start.
4. If the model is empty or obviously uninitialized, say so plainly and recommend running `preference-interview-zh`.
5. If the model exists, apply it as the default operating mode for the session.
6. Follow `references/bootstrap-rules.md` to decide:
   - what to apply immediately
   - what to mention to the user
   - what to leave silent unless relevant
7. If the user asks for the raw stored model, run `python3 scripts/preference_store.py show --format markdown`.
8. If the current task exposes a stable mismatch between stored preferences and live instructions, follow the live instruction first and suggest `preference-memory-zh` after the task.

## Session Rules

- Treat the stored model as a default, not a prison.
- Prefer the brief over the full profile to avoid context bloat.
- State only the few defaults that matter for the current task.
- Carry the model through both answer style and execution style.

## Output Standard

- Keep the user-facing bootstrap summary under roughly 6-12 lines unless asked for depth.
- Mention missing preference areas only if they matter to the current task.
- If the profile is strong enough, move on quickly and execute.

## Resources

- Read `references/bootstrap-rules.md` for precedence and relevance rules.
- Read `references/profile-schema.md` only if the brief is insufficient.
- Use `scripts/preference_store.py` to load the brief or full profile.
