# Update Rules

Use these rules before storing a new preference.

## What Counts as Durable

Prefer to store a change when one of these is true:

- the user explicitly says the change should apply in the future
- the same preference appears repeatedly across tasks
- the stored rule clearly caused friction and the user corrected it
- the preference is framed as a stable default, not a temporary mood

## What Should Usually Stay Local

Do not store it as a long-term preference yet when:

- the user is reacting to one unusual task
- the request is tied to a one-off deadline or emotional context
- the user says "for this one" or otherwise scopes it locally
- the evidence is too ambiguous to tell style from circumstance

## Priority of Evidence

When signals conflict, rank them like this:

1. Explicit future-looking instruction from the user
2. Repeated observed behavior across tasks
3. Single explicit correction
4. Abstract self-description without examples

## Update Discipline

- Make the smallest patch that explains the new evidence.
- Replace list fields intentionally; they are not automatically merged item-by-item.
- Preserve old rules unless the new evidence actually disconfirms them.
- If a preference is probably changing but not fully stable, store it as an `open_question` or a `confidence_note`.

## Contradictions

When the old and new preferences conflict:

- follow the current chat first
- store the conflict explicitly if it may recur
- avoid deleting the old rule unless the user clearly supersedes it

## Good Memory Notes

A good change note answers three things:

- what changed
- what evidence triggered the change
- whether the confidence is high or provisional
