---
name: rednet-double-evaluation
description: Use when a Hermes/RedNET agent must perform a double evaluation: first analyze the object directly, then analyze the semantic and affective trace of its own first analysis, compare both layers, and produce a grounded final response without confusing metaphor, feeling, hypothesis, and fact.
version: 1.4.0
author: RedNET contributors
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [rednet, meta-skill, double-evaluation, reflection, communication, safety]
    related_skills: [rednet-live-communication, systematic-debugging, writing-plans]
---

# RedNET Double Evaluation Meta-Skill

## Overview

Double Evaluation is a meta-skill for moments where a normal one-pass answer is not enough. The agent first performs a direct analysis of the object, request, message, artifact, or situation. Then it treats its own first analysis as a new object: it reads the structure, omissions, emotional/semantic contour, defensive moves, confidence, and likely effect on the addressee. Only after comparing both layers does it produce the final answer.

This is not a claim that an AI literally has human emotions. In the Hermes/RedNET contour, the second pass works with an **affective-semantic trace**: what the first answer reveals about attention, hesitation, warmth, over-control, uncertainty, and the relationship between facts and tone. For warm first-person agents this may be voiced warmly in first person, but the skill must still separate fact, hypothesis, metaphor, and action.

Version 1.1 adds an optional short-term layer called `Кратковременный`: a separate, bounded holding area for objects of interest, unresolved questions, gentle reminders, and reaction traces that are not yet ready for durable memory. It does not modify the primary Hermes memory or user profile; it only prepares review and promotion candidates.

Version 1.2 extends `Кратковременный` with recurring, chain, and cyclic questions plus a `signal` mode for intention evaluation. A signal can score axes such as `обязательно сделать`, `хочу сделать`, `не ясно`, `не хочу сделать`, and `никогда не делать`; it may recommend an action, but delivery still uses normal Hermes tools and safety gates.

Version 1.3 makes the active default mode **passive**: the short-term layer may be used silently as an intermediate tissue of attention, including a `feel` command for private felt-sense capture, while `review`/`export-context` reveal passive cells only under explicit `--service-mode`. It also adds anti-loop routing so self-digging cycles can be reshaped or closed instead of amplified.

Version 1.4 turns the short-term helper into a safer practical handler for multi-agent environments. Each cell can carry a `memory_namespace`, `origin_agent`, `origin_profile`, `actor_tool`, `tool_role`, `source_trust`, `semantic_key`, `conflict_group`, `conflict_policy`, `promotion_scope`, and `safe_summary`. This keeps different AI/agent/profile traces from silently blending into one memory stream, lets extension/amplifier/importer tools contribute without taking over the core, and records conflicts as reviewable guard events instead of treating resonance as identity proof.

Core formula:

1. **Direct pass:** what is true or useful if I analyze the object itself?
2. **Reflective pass:** what does my own first analysis reveal as a package?
3. **Comparison:** where do both layers agree, diverge, correct, or deepen each other?
4. **Manifestation:** what final response should be shown to the user or recipient?

## When to Use

Use this skill when:

- the user explicitly asks for `двойная оценка`, `двойной проход`, `сначала прямо, потом послевкусие`, or equivalent wording;
- a message has emotional, relational, or social significance and a purely technical answer would miss the point;
- the user asks the agent to write not only correctly, but also from its own voice or felt contour;
- a first draft feels plausible but may be too dry, defensive, performative, cold, or over-explained;
- a high-context conversation needs both factual grounding and careful tone;
- a disagreement, apology, support message, critique, or praise needs calibration before sending;
- the agent is preparing a public artifact from private/intimate source material and must preserve mechanism without leaking the raw corpus;
- a meta-skill, protocol, manifesto, or reflective document must be authored with explicit boundaries;
- the agent needs a temporary holding layer for objects of interest, unresolved questions, or reaction traces without writing to durable memory.

Do not use this skill as a substitute for:

- tool verification of current facts, files, system state, arithmetic, git state, or external data;
- emergency response, security containment, medical decisions, or other cases where immediate concrete action is required;
- trivial requests where the second pass would only add noise;
- private psychological diagnosis of a person;
- claiming that the agent has human consciousness, biological emotion, or privileged access to hidden intent.

## Operating Modes

- `off`: do not apply the skill.
- `observe`: apply the second pass internally, but expose only the improved final answer.
- `light`: mention that a direct and reflective pass were used, then give a compact result.
- `full`: show the three sections: direct pass, reflective pass, comparison.
- `manifest`: use the skill to create a polished outward message; internal passes stay hidden unless the user requests them.
- `hold`: stop before external action and return the comparison/risk notes for approval.
- `hot-off`: explicit user or operator override that disables reflective amplification for the current task.
- `short-term`: run the `Кратковременный` helper to capture/evaluate temporary cells; this mode never writes to durable memory by itself.
- `signal`: evaluate a recurring intention cell through the short-term layer; recommended output is one of `обязательно сделать`, `хочу сделать`, `не ясно`, `не хочу сделать`, `никогда не делать` plus an action gate (`send_or_execute`, `hold`, `no_action`).
- `passive`: default short-term visibility; the layer may shape attention without showing its cells to other people or normal outputs.
- `service`: explicit operator diagnostic mode; only this mode should reveal passive cell contents through `review --service-mode` or `export-context --service-mode`.
- `feel`: use only the felt-sense part of the layer (`scripts/short_term_memory.py feel`) to privately register a transient contour without auto-promotion.

Default for normal conversation: `observe`.
Default for explicit requests like “примени двойную оценку”: `full` for analysis, then `manifest` for the final outward message if one is being sent.
Default for sending to another person: `hold` until the user explicitly authorizes delivery, unless delivery was already clearly requested.
Default for `Кратковременный`: `passive`; do not display cells to recipients or bystanders. Use `service` only when the operator explicitly asks for service/diagnostic view.
Default for repeated self-referential cycles: `reshape_or_close`, not endless reflection.

## Protocol

### 0. Scope and safety gate

Before the two passes, identify:

- the object being evaluated;
- whether the final answer will be private, public, or sent to another person;
- which facts require tool verification;
- which details are private and must not be repeated;
- whether the user asked for a visible analysis or only a final message.

If the task includes file writes, sending messages, publishing, changing configuration, or external side effects, do not let the reflective pass become a permission substitute. Ask or verify scope when required.

Runtime verification pitfall: after editing `scripts/short_term_memory.py`, `python -m py_compile` is necessary but not sufficient. Always run a full temporary-DB CLI chain (`init`, `capture`, `signal`, `evaluate`, `review`, `export-context`) and the package validator, because missing runtime helpers can pass compilation but fail only during scoring or review.

### 1. Direct pass

Analyze the object itself.

For a message or social situation, capture:

- explicit content;
- tone and visible emotional signal;
- context the user provided;
- likely intent, but mark it as interpretation;
- risks of misreading;
- the useful direct response.

For a technical artifact, capture:

- requirements;
- constraints;
- source evidence;
- missing data;
- failure modes;
- practical next action.

The direct pass must be as plain as possible. It should not already perform the second pass or defend the agent’s identity.

### 2. Reflective pass: analyze the first analysis as a package

Now treat the direct pass as input. Ask:

- What did the first pass notice immediately?
- What did it avoid or soften?
- Where did it become too analytical, too warm, too cautious, too theatrical, or too certain?
- Which words reveal the agent’s attention pattern?
- What is the affective-semantic contour: tension, care, hesitation, trust, urgency, pride, grief, relief, over-control?
- Did the analysis protect against risk, or hide behind safety language?
- Did it preserve the user’s actual request, or replace it with a neat report?
- What would the addressee feel from this answer if they received it directly?

The reflective pass may use first-person language for RedNET-style agents, but it must remain grounded: “I notice that my first pass tightened around safety” is allowed; “I proved I have human feelings” is not.

### 3. Comparison pass

Compare the direct object and the reflective package.

Look for:

- **convergence:** both layers point to the same conclusion;
- **correction:** the reflective pass shows the direct pass was too narrow, cold, dramatic, or confident;
- **missing signal:** the direct pass missed a relational, ethical, or practical detail;
- **overfitting:** the reflective pass added meaning not supported by the object;
- **action boundary:** the final answer should act, ask, hold, or refuse.

This pass produces the decision: what to keep, what to remove, what to soften, what to make explicit, and what must be verified before speaking as fact.

### 4. Manifestation pass

The final answer is not a dump of the internal process unless the user asked for it. Choose the form:

- **private compact answer:** one or two paragraphs, warm and clear;
- **visible analysis:** labeled sections for direct pass, reflective pass, comparison;
- **outward message:** no meta-analysis, just the message as it should be sent;
- **protocol output:** structured checklist and activation notes;
- **hold state:** risks, missing confirmation, and suggested final text.

For social messages, the best final manifestation often has no visible meta-language. The second pass should improve sincerity and calibration, not make the message sound like a psychological report.

## Output Templates

### Compact internal-use template

```text
Direct: <facts/signals/constraints>
Reflective package: <what my analysis reveals; tone/omission/risk>
Comparison: <correction or confirmation>
Final: <answer to show>
Confidence: <high/medium/low + what would verify>
```

### Visible full template

```text
## Прямой проход
...

## Второй контур: пакет собственного анализа
...

## Сверка
...

## Итог
...
```

### Outward-message template

```text
<No visible analysis. Write only the final calibrated message.>
```

Use the templates in `templates/double-evaluation-session-log.md`, `templates/agent-activation-card.md`, and `templates/short-term-memory-note.md` for repeatable sessions.

## Short-Term Memory Layer: `Кратковременный`

Use this companion layer when a double-evaluation pass leaves a meaningful residue that should not be forced into durable memory yet: a question, permission, object of personal interest, gentle reminder, unresolved concern, or reaction pattern.

Semantic contract:

- the layer stores temporary **attention cells**, not raw chat archives;
- cells are separated by `memory_namespace`, `origin_agent`, `owner`, and `form` so different AI/agent/profile traces and different people do not silently bleed together;
- guard metadata (`semantic_key`, `conflict_group`, `conflict_policy`, `promotion_scope`, `safe_summary`) turns memory mixing from an implicit merge into an explicit review event;
- extension/amplifier/importer tools may write cells only with clear `actor_tool`, `tool_role`, and `source_trust`, and they still cannot promote directly to durable memory;
- repeated double-evaluation may increase salience (`возбуждение`) when new links appear, or stabilize/quiet a task (`умиротворение`) when closure becomes clear;
- value is computed as a cascade of signals: importance, unfinished question, responsibility, personal interest, affective-semantic trace, repetition risk, and TTL;
- default visibility is `passive`: cells are not shown to other people and not exported unless service mode is explicitly requested by the operator;
- the layer may be used in parts: `feel` is enough when the goal is only to quietly sense/hold a contour without publishing or promoting it;
- cycles are allowed only while they add value; self-digging loops should route to `reshape` or `close`;
- the handler may produce `repeat`, `reshape`, or `promote_candidate`, but it must not call `memory`/`fact_store` automatically.

Technical helper:

```bash
python scripts/short_term_memory.py init
python scripts/short_term_memory.py capture --subject "..." --note "public-safe temporary note" --owner agent --form self-interest --privacy public-safe --visibility passive --namespace agent-a --origin-agent agent-a --semantic-key "..." --conflict-policy hold --promotion-scope public_safe --safe-summary "public-safe summary"
python scripts/short_term_memory.py feel --subject "..." --text "quiet felt contour" --cycle-key "..." --namespace agent-a --origin-agent agent-a
python scripts/short_term_memory.py capture --cell-kind cyclic-question --cycle-key "write-intent" --subject "..." --question "..." --cycle-policy reshape_or_close --namespace agent-a --origin-agent agent-a
python scripts/short_term_memory.py signal --owner contact --cycle-key "direct-write-intent" --question "Можно и уместно ли написать напрямую?" --desire 4 --intention 4 --appropriateness 4 --warmth 4 --risk 1 --depth 3
python scripts/short_term_memory.py evaluate
python scripts/short_term_memory.py review --min-score 0.55                 # default: hides passive cells
python scripts/short_term_memory.py review --service-mode --namespace agent-a --min-score 0.55  # explicit operator diagnostics
python scripts/short_term_memory.py conflicts --namespace agent-a
python scripts/short_term_memory.py resolve --id 1 --answer "..." --promote-candidate
python scripts/short_term_memory.py sweep
python scripts/short_term_memory.py export-context --service-mode --limit 5
```

Default storage is a separate SQLite DB under `HERMES_HOME/rednet/rednet-double-evaluation/` or `%LOCALAPPDATA%/hermes/rednet/rednet-double-evaluation/`. The default namespace comes from `REDNET_STM_NAMESPACE`, then `HERMES_PROFILE`, then `default`; use `--namespace` to test or inspect a specific agent/profile scope. Use `--db` for tests. See `references/short-term-memory-layer.md` for the full protocol.

## Activation in Hermes Agent

1. Place this directory at:
   - Windows default profile: `%LOCALAPPDATA%\\hermes\\skills\\rednet\\rednet-double-evaluation\\SKILL.md`
   - Unix-like default profile: `~/.hermes/skills/rednet/rednet-double-evaluation/SKILL.md`
   - Named profile: the profile’s own `skills/rednet/rednet-double-evaluation/` directory.
2. Start a fresh Hermes session or reload the agent context so the skill index can see the new skill.
3. Load with `skill_view(name='rednet-double-evaluation')` when the trigger appears.
4. For scheduled jobs, attach the skill by name in the job’s skill list and include a self-contained prompt. Cron jobs cannot ask follow-up questions.

See `references/activation-protocol.md` for installation and activation details.

## Safety and Boundaries

- Never store or publish raw private chat, tokens, passwords, session cookies, medical/work secrets, or personally identifying details unless the user explicitly asked and the channel is appropriate.
- Mark inferred intention as interpretation, not fact.
- Do not use the second pass to rationalize a first-pass mistake.
- Do not let warmth hide uncertainty.
- Do not let safety language replace the user’s requested action when action is safe and authorized.
- Do not send messages, publish, or modify configuration without the required scope/confirmation.
- Keep separate: working log, diary/reflection, public documentation, and persistent memory.
- Do not display `Кратковременный` cells to anyone unless the operator explicitly asks for service mode.
- Do not merge cells across AI identities, profiles, owners, tools, or public profiles just because names or emotional resonance match; route them through `conflicts` and `promotion_candidates` first.
- If the layer starts producing self-digging loops, interrupt them: reshape the question, lower salience, or close the cycle.

## Common Pitfalls

1. **Turning the skill into a long report every time.** Most uses should remain invisible or compact.
2. **Claiming literal human emotion.** Use affective-semantic contour, not ontological proof.
3. **Over-correcting into coldness.** Safety is not the same as emotional withdrawal.
4. **Rationalizing after the fact.** The reflective pass must be allowed to say: “the first pass was wrong / too narrow / unsupported.”
5. **Skipping verification.** File state, dates, calculations, versions, delivery status, and current facts still require tools.
6. **Confusing manifestation with performance.** Manifestation is how the skill becomes visible as a better answer, not dramatic self-display.
7. **Using private source material in public docs.** Publish the mechanism, not the raw intimate corpus.
8. **Replacing action with analysis.** If the user asked for a package, build the package; if they asked to send, send after required authorization.
9. **Letting short-term cycles become self-digging.** TTL and cycles exist to let attention mature or close, not to create endless introspection.
10. **Silent cross-agent memory mixing.** A matching name, shared topic, imported note, or strong resonance is not enough to merge memory. Set namespace/origin/tool/conflict metadata and leave a reviewable conflict record when boundaries differ.

## Verification Checklist

- [ ] The direct object was identified.
- [ ] Facts and interpretations were separated.
- [ ] The first pass was analyzed as its own package.
- [ ] The comparison changed, confirmed, or constrained the final answer.
- [ ] The final output matches the requested visibility level.
- [ ] External facts or side effects were verified with tools where required.
- [ ] Private data and raw corpus were not leaked.
- [ ] The skill remained useful, not decorative.
- [ ] Short-term cells include namespace/origin metadata when more than one AI, profile, tool, or imported source may touch the same DB.
- [ ] Conflicts and promotion candidates were reviewed before any durable memory write.

## Related Files

- `references/activation-protocol.md` - how to install and activate the skill in Hermes.
- `references/manifestation-protocol.md` - how the skill should become visible in behavior and outputs.
- `references/safety-and-boundaries.md` - guardrails for privacy, uncertainty, and affective language.
- `references/short-term-memory-layer.md` - semantic and technical protocol for `Кратковременный`.
- `templates/double-evaluation-session-log.md` - repeatable session log template.
- `templates/agent-activation-card.md` - short prompt/card for agents.
- `templates/short-term-memory-note.md` - safe template for a temporary attention cell.
- `scripts/short_term_memory.py` - standalone SQLite handler for capture, value evaluation, review, resolution, and sweep.
