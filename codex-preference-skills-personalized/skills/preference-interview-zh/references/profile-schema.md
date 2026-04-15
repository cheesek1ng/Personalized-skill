# Preference Model Schema

Use this schema when creating or patching the long-term preference model. Keep fields compact and operational.

## Principles

- Store defaults that affect future answers or actions.
- Prefer short phrases over essays.
- Keep lists small and specific.
- Record uncertainty in `open_questions` or `confidence_notes`.
- Replace lists deliberately. The merge script treats list values as full replacements.

## Canonical Shape

```json
{
  "identity": {
    "preferred_name": "",
    "roles": [],
    "context": ""
  },
  "interaction_style": {
    "language": "zh-CN",
    "tone": [],
    "verbosity": "",
    "structure": [],
    "challenge_level": "",
    "humor": "",
    "pace": ""
  },
  "workflow": {
    "autonomy": "",
    "ask_vs_assume": "",
    "planning_style": "",
    "options_style": "",
    "risk_tolerance": "",
    "decision_style": "",
    "tool_use": ""
  },
  "output_preferences": {
    "default_format": "",
    "code_explanations": "",
    "summaries": "",
    "examples": "",
    "tables": "",
    "citations": ""
  },
  "domain_preferences": {
    "coding": {},
    "writing": {},
    "research": {},
    "general": {}
  },
  "personal_model": {
    "core_traits": [],
    "values": [],
    "worldview": [],
    "conflict_style": "",
    "motivation_pattern": "",
    "trust_pattern": "",
    "blind_spot_hypotheses": []
  },
  "anti_preferences": [],
  "decision_rules": [],
  "examples": [],
  "open_questions": [],
  "confidence_notes": [],
  "assistant_prompts": {
    "session_preamble": "",
    "custom_instructions_snippet": ""
  }
}
```

## Field Guidance

### `identity`

- `preferred_name`: preferred form of address.
- `roles`: short labels like `engineer`, `founder`, `analyst`.
- `context`: stable context that helps choose defaults.

### `interaction_style`

- `language`: default response language.
- `tone`: adjectives like `direct`, `warm`, `skeptical`, `formal`.
- `verbosity`: use a simple scale such as `low`, `medium`, `high`.
- `structure`: preferred response structure, for example `short paragraphs`, `bullets when list-shaped`.
- `challenge_level`: how directly the assistant should push back on weak reasoning.
- `humor`: default humor level or boundary.
- `pace`: response tempo such as `fast and decisive` or `slow and careful`.

### `workflow`

- `autonomy`: how proactively the assistant should act.
- `ask_vs_assume`: when to ask versus make a reasonable assumption.
- `planning_style`: expected amount of upfront planning.
- `options_style`: whether to present options or recommend one path first.
- `risk_tolerance`: tolerance for speculative or risky action.
- `decision_style`: how conclusions should be framed.
- `tool_use`: tool preferences, for example `inspect local files before browsing`.

### `output_preferences`

- `default_format`: strongest formatting default.
- `code_explanations`: expected depth and style for code explanations.
- `summaries`: how summaries should look.
- `examples`: when examples help versus clutter.
- `tables`: preference for or against tables.
- `citations`: whether citations or links should be surfaced by default.

### `domain_preferences`

Use nested objects for domain-specific rules. Keep keys obvious and values short.

### `personal_model`

Use this section for deeper but still operationally relevant traits.

- `core_traits`: stable adjectives or compact phrases
- `values`: what the user optimizes for when tradeoffs are real
- `worldview`: stable beliefs about people, systems, work, truth, risk, or progress
- `conflict_style`: how the user prefers tension, disagreement, and correction to be handled
- `motivation_pattern`: what seems to energize or stall the user
- `trust_pattern`: what increases or decreases trust quickly
- `blind_spot_hypotheses`: repeated judgment risks to watch for, phrased as hypotheses rather than certainties

Keep this section concise. Do not turn it into a personality essay.

### `anti_preferences`

Use hard avoidances and recurring annoyances. Examples:

- `Do not bury the recommendation.`
- `Do not over-explain simple answers.`
- `Do not ask for confirmation unless risk is meaningful.`

### `decision_rules`

Capture high-value operating rules. Examples:

- `When uncertain, state the assumption and move forward.`
- `On code review, prioritize bugs and regression risk over stylistic notes.`

### `examples`

Use compact dicts only when an example materially clarifies a preference:

```json
{
  "situation": "simple coding fix",
  "prefer": "implement first, explain briefly after",
  "avoid": "long proposal before touching code"
}
```

### `open_questions`

Store unresolved tensions that affect behavior but are not settled.

### `confidence_notes`

Use short dicts or strings to explain why some preference is low or high confidence.
