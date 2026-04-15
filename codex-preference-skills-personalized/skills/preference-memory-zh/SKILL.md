---
name: preference-memory-zh
description: Update and maintain the long-term user preference model from corrections, repeated behavior, and explicit feedback. Use when the user says "以后都这样", "记住这个偏好", "别再这样回答", "以后默认按这个格式", or when current-chat evidence should change stored defaults for tone, formatting, autonomy, planning, decision style, or anti-preferences.
---

# Preference Memory Zh

Maintain the profile as a durable operating memory. Prefer small, evidence-backed updates over broad rewrites.

## Workflow

1. Run `python3 scripts/preference_store.py ensure`.
2. Run `python3 scripts/preference_store.py show --format brief` to inspect the active defaults.
3. Decide whether the new signal is:
   - a durable preference
   - a task-local override
   - too ambiguous to store yet
4. Follow `references/update-rules.md` before changing anything.
5. If needed, ask 1-3 confirmation questions to resolve ambiguity. Do not run another full interview unless the stored model is clearly wrong or obsolete.
6. Create a minimal JSON patch with only the changed fields.
7. Persist the update:

```bash
python3 scripts/preference_store.py merge --source update --note "post-conversation correction" <<'JSON'
{
  "interaction_style": {
    "verbosity": "low"
  },
  "output_preferences": {
    "default_format": "short paragraphs first; bullets only when list-shaped"
  },
  "anti_preferences": [
    "Do not open with filler acknowledgement."
  ]
}
JSON
```

8. Append a change note:

```bash
python3 scripts/preference_store.py log-change --title "memory update" <<'MD'
What changed, why it changed, and what evidence supported the update.
MD
```

9. Tell the user what was updated, what was not updated, and why.

## Memory Rules

- Prefer observed behavior over self-description when they conflict.
- Prefer repeated evidence over one-off feedback.
- Store stable defaults, not temporary mood.
- Keep anti-preferences explicit and short.
- Once the model is already strong, prefer learning from real collaboration over restarting long interview loops.
- Treat personality, values, worldview, and blind-spot notes as higher-bar memory. Store them only when the evidence is stable enough to affect future behavior.
- When evidence is mixed, record the tension in `open_questions` or `confidence_notes` instead of pretending the model is clean.

## Output Standard

- Show a concise before/after summary of the changed rules.
- Keep updates surgical.
- Protect the model from drift caused by one unusual task.

## Resources

- Read `references/update-rules.md` before deciding whether to store a new preference.
- Read `references/profile-schema.md` before writing JSON patches.
- Use `scripts/preference_store.py` for merge, inspection, and change logging.
