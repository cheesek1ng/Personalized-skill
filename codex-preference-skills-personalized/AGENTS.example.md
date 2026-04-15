If `${CODEX_HOME:-$HOME/.codex}/state/preference-model-zh/session-brief.md` exists, always read it at the start of a new conversation before doing substantial work. Treat it as the token-efficient default user preference contract for the session.

Follow these rules when using the preference model:
- Prefer `session-brief.md`; read `profile.md` only when the brief is missing, stale, or clearly insufficient for the current task.
- Do not trigger a full preference interview by default. Use interview-style questioning only when the user explicitly asks for it or when a real ambiguity materially affects the result.
- Apply the stored defaults for tone, formatting, autonomy, and decision style unless the user gives a conflicting instruction in the current chat.
- Let the current chat override the stored model immediately when they conflict.
- Do not ask near-duplicate preference questions once a theme is already clear; infer nearby low-risk preferences from existing evidence when reasonable.
- Prefer learning the remaining edge cases gradually from real collaboration instead of restarting long onboarding loops.
- If the conversation reveals a stable new preference or a clear correction, finish the immediate task first, then ask once whether to update long-term memory with `preference-memory-zh`.
