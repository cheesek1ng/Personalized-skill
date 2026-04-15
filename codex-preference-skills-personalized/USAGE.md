# Usage

## What This Repo Contains

This repo ships:

- the reusable skill source
- a distilled preference seed under `seed-state/preference-model-zh/`

It does not ship:

- any saved interview logs
- any raw change logs

The included seed profile is meant to be copied into local runtime state.

## Install

1. Copy the three skill folders under `skills/` into your Codex skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/preference-interview-zh "${CODEX_HOME:-$HOME/.codex}/skills/"
cp -R skills/preference-memory-zh "${CODEX_HOME:-$HOME/.codex}/skills/"
cp -R skills/preference-bootstrap-zh "${CODEX_HOME:-$HOME/.codex}/skills/"
```

2. Optional: validate them with the built-in validator from your local Codex skill-creator installation.

3. Start using the skills in Codex.

## Install The Seed Profile

If you want to preserve the current distilled preference model, also copy:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/state/preference-model-zh"
cp seed-state/preference-model-zh/profile.json "${CODEX_HOME:-$HOME/.codex}/state/preference-model-zh/"
cp seed-state/preference-model-zh/profile.md "${CODEX_HOME:-$HOME/.codex}/state/preference-model-zh/"
cp seed-state/preference-model-zh/session-brief.md "${CODEX_HOME:-$HOME/.codex}/state/preference-model-zh/"
```

This package intentionally does not include:

- `interview-log.md`
- `change-log.md`

Only the distilled model is carried over.

## Runtime Files

When the skills run, they create local state under:

```text
${CODEX_HOME:-$HOME/.codex}/state/preference-model-zh/
```

Typical runtime files:

- `profile.json`
- `profile.md`
- `session-brief.md`
- `interview-log.md`
- `change-log.md`

Do not commit additional local runtime files to GitHub unless you explicitly want to publish them.

## Recommended Flow

### 1. Initial onboarding

Use `$preference-interview-zh` to build the initial model.

Expected behavior:

- ask in themed rounds
- usually stop within `40-80` questions
- avoid near-duplicate questions
- keep the overall ceiling around `100` questions unless a real ambiguity still matters
- infer some nearby low-risk preferences from stable patterns instead of asking every variant
- reserve the last `10-20` questions, when useful, for personality, values, worldview, and blind spots

### 2. Daily collaboration

Use the skills normally on real work. Once the broad pattern is clear, prefer learning from real collaboration over restarting questionnaire-style interviews.

### 3. Update the model

Use `$preference-memory-zh` when:

- the user explicitly says to remember a preference
- the same preference shows up repeatedly
- the stored default is clearly outdated

The memory skill should prefer small, evidence-backed updates.

### 4. Load the model in a new session

Use `$preference-bootstrap-zh` to read the saved model and apply it as the session default.

## Recommended Token-Efficient Mode

For daily use, prefer this setup:

1. keep `session-brief.md` short
2. auto-load it from global `AGENTS.md`
3. use `preference-memory-zh` only when a stable new preference appears
4. use `preference-interview-zh` only for first-time onboarding or major resets

This avoids spending tokens on repeatedly re-running the full preference stack.

## AGENTS.md Integration

Use [AGENTS.example.md](./AGENTS.example.md) as the starting point. The key behavior is that new sessions should load the saved brief automatically:

```text
<your CODEX_HOME>/state/preference-model-zh/session-brief.md
```

Keep the current chat higher priority than the saved model.

## Privacy

This repo includes a distilled preference seed. Before pushing to GitHub, confirm that you are comfortable publishing:

- `seed-state/preference-model-zh/profile.json`
- `seed-state/preference-model-zh/profile.md`
- `seed-state/preference-model-zh/session-brief.md`

It still excludes raw interview and change logs by default.

## Editing Guidance

If you keep evolving the skills:

- update the interview playbook before adding more questions
- prefer improving coverage and deduplication over making the questionnaire longer
- keep repeated preference learning in real work, not endless onboarding loops
- treat `100` questions as a ceiling, not a goal
- prefer `AGENTS.md + session-brief.md` over auto-triggering the whole stack every session
