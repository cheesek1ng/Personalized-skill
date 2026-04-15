# Bootstrap Rules

Use the stored model to guide the current session without turning the opening into a long recap.

## Precedence

Apply preferences in this order:

1. Direct instruction in the current chat
2. Stored long-term preference model
3. Your normal defaults

## What to Load First

- Read `session-brief.md` first.
- Read `profile.md` only if the brief is missing, stale, or too thin for the current task.
- Do not load logs unless you need to understand why a rule exists.

## What to Surface to the User

Mention only the defaults that materially affect the task, for example:

- expected level of brevity
- whether you will execute or plan first
- whether you will recommend one path or list options
- any hard avoidances that affect style

## What to Keep Implicit

Do not restate the whole profile if it would slow the task down. Once the model is strong enough, switch quickly into execution.

## When to Escalate to Memory Update

Suggest `preference-memory-zh` after the task if:

- the stored model conflicts with the user's current correction
- a new stable anti-preference appears
- the user's desired execution style has clearly shifted
- the bootstrap brief looks stale or generic
