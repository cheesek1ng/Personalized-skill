# Interview Playbook

Use this playbook to build a preference model that is behaviorally grounded and operationally useful.

## Core Method

- Start from recent real examples, not abstract self-descriptions.
- Ask about the assistant's output and process, not only personality labels.
- Use contrast and tradeoff questions to force signal.
- Surface anti-preferences early.
- Stop when answers become repetitive and stable.

## Question Budget

- Default total budget: 40-80 questions.
- Hard ceiling: about 100 questions unless unresolved ambiguity would materially harm future behavior.
- Most users should not need the full budget. Treat 100 as a ceiling, not a target.
- Once a theme is clearly answered, stop asking near-duplicate variants.
- Infer nearby low-risk preferences from stable patterns, tone, and tradeoff choices instead of asking every possible permutation.
- After roughly 50 questions, only ask high-value questions that resolve real ambiguity.
- After roughly 80 questions, ask only the highest-value questions.
- Reserve the last 10-20 questions, when needed, for deeper modeling of personality, values, worldview, and repeated blind spots.
- After roughly 100 questions, stop and carry remaining uncertainty into `open_questions`, then learn through real collaboration.

## Coverage Map

Before asking a new question, check whether the theme is already covered well enough:

- answer style
- workflow and autonomy
- anti-preferences
- tradeoffs and decision style
- domain differences
- sensitive or subjective situations
- urgency and quality thresholds
- handoff and explainability
- blind spots and correction style
- personality, values, and worldview

If a question only re-tests a theme that already has strong evidence, skip it.

## Round Structure

Run 3-15 rounds. Ask 4-7 questions per round. After each round, summarize the emerging model before moving on.

### Round 1: Surface Defaults

Goal: establish obvious style defaults.

Ask about:

- preferred language
- concise versus detailed answers
- paragraphs versus bullets
- directness versus cushioning
- recommendation-first versus options-first

Good questions:

- "Think of a recent answer you liked. What made it feel right?"
- "When an answer is bad, what usually goes wrong first: too long, too vague, too soft, or too pushy?"
- "If I only improve one thing first, should it be brevity, clarity, speed, or rigor?"

### Round 2: Execution Style

Goal: learn how the assistant should behave when doing work, not just writing.

Ask about:

- ask-versus-assume threshold
- appetite for autonomy
- amount of planning before action
- tolerance for risk
- whether the assistant should challenge weak reasoning directly

Good questions:

- "When the task is clear enough, do you want me to start immediately or summarize the plan first?"
- "What kinds of mistakes are acceptable in exchange for speed, and which ones are not?"
- "If your request is slightly ambiguous, when should I decide on my own?"

### Round 3: Domain-Specific Preferences

Goal: capture differences across coding, writing, research, admin, and analysis work.

Ask about:

- code explanations
- testing expectations
- preferred structure for research summaries
- appetite for citations
- how much context to include

Good questions:

- "For code changes, do you want the patch first and rationale second, or the reverse?"
- "For research, do you want the shortest possible answer or a broader view with sources?"

### Round 4: Anti-Preferences

Goal: identify hard noes and recurring annoyances.

Ask about:

- over-explaining
- asking too many confirmations
- hedging or filler
- excessive formatting
- generic advice

Good questions:

- "What is the fastest way for an AI answer to lose your trust?"
- "What should I almost never do, even if many assistants would?"

### Round 5: Forced Tradeoffs

Goal: resolve conflicts that broad preferences usually hide.

Use pairs like:

- speed vs rigor
- initiative vs caution
- short answer vs complete answer
- strong recommendation vs balanced option set
- challenge the premise vs stay accommodating

Good questions:

- "If I can only optimize one in a high-pressure task, should I optimize speed or correctness?"
- "Would you rather I give one strong answer with assumptions, or two safer options?"

### Round 6: Stress Test

Goal: validate the model against realistic cases.

Present 2-3 short scenarios:

- simple factual question
- ambiguous coding task
- code review request
- strategic question with weak assumptions

For each scenario, ask:

- what a good answer would look like
- what the assistant should avoid
- what should happen if the user is silent about style

### Round 7: Personality, Values, and Worldview

Goal: model deeper stable traits that affect long-term collaboration after the operational layer is mostly clear.

Only use this round if:

- the main operational defaults are already strong
- there is still budget left
- the deeper model would materially improve future behavior

Ask about:

- fairness versus efficiency
- autonomy versus control
- harmony versus truth-telling
- ambition versus stability
- optimism versus skepticism
- long-termism versus immediate feedback
- conflict style
- trust thresholds
- what kinds of people or systems the user respects
- recurring self-acknowledged blind spots

Good questions:

- "When truth and relationship harmony conflict, which should bend first?"
- "What do you respect more: sharp judgment, reliability, kindness, courage, or leverage?"
- "When a plan looks attractive, where do you most often suspect your own blind spot?"

Use multiple-choice or forced tradeoffs where possible. Do not turn this into a personality test for its own sake.

## Evidence Rules

- One explicit correction is enough for a task-local adjustment, not always enough for a permanent rule.
- Two or more aligned examples are usually strong evidence.
- When stated preference and observed behavior conflict, store both and mark the conflict.
- Preserve the user's own wording for high-value anti-preferences.
- When one answer strongly implies several neighboring preferences, infer the lower-risk ones instead of asking each separately.
- Prefer real-task evidence over more interview questions once the main pattern is already clear.
- For personality and worldview questions, prefer stable repeated patterns over one-off statements of identity.

## Stop Condition

Stop the interview when all of the following are true:

- the main style defaults are clear
- the workflow defaults are clear
- anti-preferences are explicit
- at least two important tradeoffs are resolved
- remaining uncertainty is narrow enough to record as `open_questions`

If the remaining ambiguity is minor, stop the questionnaire and let future work resolve it.

Once the operational model is strong, deeper personality and worldview questions are optional, not mandatory.
