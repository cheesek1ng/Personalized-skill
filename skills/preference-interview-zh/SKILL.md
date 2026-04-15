---
name: preference-interview-zh
description: Build or rebuild a long-term user preference model through a multi-round Chinese interview. Use when the user wants the AI to "ask me many questions", "learn my preferences", "build a persona/profile", "remember how I like answers and actions", or create a reusable operating model covering tone, formatting, autonomy, planning, decision style, and anti-preferences. Also use for first-time onboarding or a full preference reset.
---

# Preference Interview Zh

Build an actionable preference model, not a one-shot questionnaire. Produce a compact operating profile that later sessions can load and follow.

## Workflow

1. Run `python3 scripts/preference_store.py ensure`.
2. If a model already exists, run `python3 scripts/preference_store.py show --format brief` and identify what is already known, what is stale, and what is missing.
3. Interview in themed rounds of 4-7 questions. Prefer recent real examples over abstract opinions. Follow `references/interview-playbook.md`.
4. Track a total question budget. Default target is 40-80 questions. Do not exceed roughly 100 unless unresolved ambiguity would materially degrade future behavior.
5. After each round, summarize:
   - high-confidence preferences backed by repeated evidence
   - low-confidence claims that need confirmation
   - contradictions or tradeoffs that still need resolution
6. Stop when the model is saturated enough to guide behavior. Do not ask extra questions just to maximize count. If a theme is already clear, infer nearby low-risk preferences instead of re-asking near-duplicate questions.
7. Convert the result into JSON using `references/profile-schema.md`.
8. Persist the structured model:

```bash
python3 scripts/preference_store.py merge --source interview <<'JSON'
{
  "identity": {
    "preferred_name": "..."
  },
  "interaction_style": {
    "language": "zh-CN",
    "tone": ["direct", "concise"],
    "verbosity": "medium"
  },
  "workflow": {
    "autonomy": "high",
    "ask_vs_assume": "assume unless risk is meaningful"
  },
  "anti_preferences": [
    "Do not bury the recommendation."
  ],
  "decision_rules": [
    "When tradeoffs are unclear, recommend one path and explain the reason."
  ],
  "open_questions": [
    "Exact tolerance for speculative brainstorming versus execution."
  ]
}
JSON
```

9. Append a human-readable interview note:

```bash
python3 scripts/preference_store.py log-interview --title "initial interview" <<'MD'
Round highlights, evidence, and unresolved tensions.
MD
```

10. End with a short confirmation summary for the user:
   - 5-10 lines of "how I will operate"
   - 3-7 strongest rules
   - remaining low-confidence items

## Interview Rules

- Ask about recent concrete behavior first, then abstract a rule.
- Use forced tradeoffs. Good pairs include speed vs rigor, concise vs complete, ask first vs act first, and options vs recommendation.
- Ask for anti-preferences explicitly: what should the assistant never do.
- Prefer one sharp follow-up over five shallow prompts.
- Avoid near-duplicate questions once the answer pattern is already stable.
- Infer adjacent low-risk preferences from the user's consistent traits or personality when the evidence is already strong enough.
- When the remaining ambiguity is minor, stop interviewing and learn the rest through real collaboration.
- If the operational layer is already clear, use the remaining budget for deeper questions about personality, values, worldview, recurring blind spots, and conflict style.
- Treat one-off emotional reactions as weak evidence until confirmed.
- When the user is already consistent, close early instead of continuing to interrogate.

## Output Standard

- Produce an execution-oriented summary, not a personality essay.
- Keep the stored model compact and specific.
- Record open questions instead of inventing certainty.
- Preserve user wording for distinctive preferences when it adds operational value.

## Resources

- Read `references/interview-playbook.md` for question design and round structure.
- Read `references/profile-schema.md` before writing or merging JSON.
- Use `scripts/preference_store.py` for state creation, persistence, and logging.
