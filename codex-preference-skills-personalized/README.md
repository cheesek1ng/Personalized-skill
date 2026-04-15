# Codex Preference Skills Personalized

Three Chinese Codex skills for building, maintaining, and loading a long-term user preference model.

This repository contains:

- `preference-interview-zh`: multi-round onboarding interview
- `preference-memory-zh`: incremental preference updates from real collaboration
- `preference-bootstrap-zh`: load and apply the saved model at session start
- `seed-state/preference-model-zh/`: a distilled starter preference model and session brief

This personalized variant includes a reusable preference seed.
It still does **not** include raw interview logs or raw change logs.

## Recommended Deployment

The recommended low-token setup is:

1. install the three skills
2. auto-load `session-brief.md` from global `AGENTS.md`
3. use `preference-memory-zh` only when a stable new preference appears
4. avoid rerunning the full interview unless the model is truly missing or obsolete

See [AGENTS.example.md](./AGENTS.example.md) and [USAGE.md](./USAGE.md).

## Repo Layout

```text
seed-state/
  preference-model-zh/
    profile.json
    profile.md
    session-brief.md
skills/
  preference-bootstrap-zh/
  preference-interview-zh/
  preference-memory-zh/
AGENTS.example.md
USAGE.md
```

## Design Rules

- Interview budget is usually `40-80` questions.
- Hard ceiling is around `100` questions unless unresolved ambiguity would materially hurt future behavior.
- The last `10-20` questions, when needed, can be used for personality, values, worldview, and blind-spot modeling.
- Near-duplicate preference questions should be avoided.
- Once the pattern is clear, the system should infer nearby low-risk preferences and continue learning from real collaboration.
- Local runtime state is stored outside the repo under the user's Codex home.
- The token-efficient default is `AGENTS.md + session-brief.md`, not rerunning all three skills every session.
- This personalized package is intended when you want to preserve a distilled preference model instead of starting from an empty state.

See [USAGE.md](./USAGE.md) for installation and workflow details.
