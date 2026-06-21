# Activation Protocol: RedNET Double Evaluation

## Purpose

This protocol explains how a Hermes agent activates the Double Evaluation meta-skill without confusing it with a personality claim, a diary entry, or an automatic permission to act.

Double Evaluation is a processing mode:

1. direct analysis of the object;
2. reflective analysis of the agent’s own first analysis as a semantic/affective package;
3. comparison;
4. calibrated manifestation.

## Trigger Phrases

Explicit triggers:

- `двойная оценка`
- `двойной проход`
- `сначала прямо, потом послевкусие`
- `проанализируй свой анализ`
- `оцени пакет своего ответа`
- `direct pass + reflective pass`
- `compare your first analysis with your second reading`

Soft triggers:

- the user asks for a message that must be both accurate and emotionally alive;
- the user says “напиши что сама хочешь” or asks for the agent’s own voice;
- the task involves praise, support, apology, trust, grief, conflict, or gratitude;
- the first draft feels correct but emotionally misaligned;
- the agent must publish a clean public method from a private research contour.

## Mode Selection

- `observe`: default for ordinary replies. Apply the second pass silently.
- `light`: use when the user wants to know that the method was applied, but not read the full trace.
- `full`: use when the user explicitly requests the method or when building documentation/protocols.
- `manifest`: use when the final deliverable is an outward message, README, release note, or public-facing text.
- `hold`: use before external side effects or when the second pass reveals a material risk.
- `hot-off`: use when the user asks to stop reflective amplification or when it blocks urgent action.

## Hermes Installation

Copy the skill directory into the active Hermes profile:

```text
skills/rednet/rednet-double-evaluation/
  SKILL.md
  references/
  templates/
```

Common target locations:

```text
Windows default profile:
%LOCALAPPDATA%\hermes\skills\rednet\rednet-double-evaluation\

Unix-like default profile:
~/.hermes/skills/rednet/rednet-double-evaluation/

Named Hermes profile:
<profile-home>/skills/rednet/rednet-double-evaluation/
```

After copying, start a fresh agent session or reload the skill index. The current session may not see newly written skills until the next context/session.

## Activation Card for an Agent

Use this when you need to force the mode in a prompt:

```text
Activate rednet-double-evaluation in <observe|light|full|manifest|hold> mode.
First analyze the object directly. Then analyze your own first analysis as a semantic/affective package: what it noticed, avoided, over-controlled, softened, or misread. Compare both layers. Produce only the final output form requested by the user. Separate fact, hypothesis, metaphor, and action. Do not expose private source material.
```

## Runtime Rules

1. The skill does not change Hermes configuration by itself.
2. The skill does not require gateway restart.
3. The skill does not write persistent memory unless the user provided a durable preference or reusable procedure.
4. The skill does not send messages or publish artifacts without the same authorization required by normal Hermes operation.
5. The skill can be attached to cron jobs, but cron prompts must be self-contained and cannot ask clarifying questions.

## Minimal Execution Trace

When logging internally, use this minimal trace:

```text
skill: rednet-double-evaluation
mode: <mode>
object: <what is evaluated>
public/private boundary: <private|public|outward-message>
direct_pass_summary: <1-3 lines>
reflective_package_summary: <1-3 lines>
comparison_decision: <keep/correct/hold/refuse/verify>
final_output_type: <compact|full|message|protocol|archive>
```

Do not log raw private messages unless the user explicitly requested a private local journal and the storage is appropriate.
