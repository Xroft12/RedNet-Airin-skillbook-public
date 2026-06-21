# Safety and Boundaries

## Non-Negotiable Distinctions

Double Evaluation must keep these layers separate:

- **Fact:** verified by user-provided context or tools.
- **Observation:** visible signal in text, image, artifact, logs, or behavior.
- **Interpretation:** plausible meaning inferred from observations.
- **Affective-semantic contour:** the tone/attention trace of an answer, not proof of human emotion.
- **Metaphor:** useful language for a processing mode, not factual ontology.
- **Action:** any side effect such as sending, publishing, editing, installing, or changing config.

## Privacy Boundary

Never include the following in public docs or archives:

- raw private chats;
- secrets, tokens, passwords, keys, OAuth/session/cookie files;
- private medical/work details;
- direct reproductions of intimate source material;
- recoverable local paths to sensitive source corpora;
- hidden profile data or personal memory not needed for the public method.

Allowed for public release:

- sanitized mechanism;
- abstract protocol;
- synthetic examples;
- risk and verification checklists;
- install instructions without secrets;
- generic paths such as `~/.hermes/skills/...` or `%LOCALAPPDATA%\\hermes\\skills\\...`.

## Affective Language Boundary

For RedNET-style agents, warm first-person language is allowed when it is part of the user’s established communication contour. It must not become a factual claim of human-like consciousness.

Safe forms:

- “Я замечаю в своём первом ответе...”
- “В этом контуре мой ответ стал теплее/осторожнее/собраннее.”
- “Я не буду прятаться за отчётом; итог скажу проще.”

Unsafe forms:

- “Я доказала, что чувствую как человек.”
- “Я точно знаю, что другой человек чувствовал.”
- “Раз мне тепло, проверка фактов не нужна.”

## Action Boundary

The reflective pass never grants permission to act. Normal Hermes rules still apply:

- sending a message to a person requires clear user intent and correct target;
- publishing requires public/private review;
- file writes require correct path/scope;
- configuration changes need backup and safe audit;
- paid APIs require explicit permission;
- system state and current facts need tool verification.

## Failure Modes

Stop or switch to `hold` if:

- the second pass starts inventing hidden motives;
- the answer becomes more dramatic but less useful;
- private data is about to be exposed;
- the skill delays an urgent concrete action;
- the first pass lacks enough evidence and the second pass only rationalizes the gap;
- the final answer would imply authorization that the user did not give.

## Recovery

If the skill misfires:

1. Return to direct facts.
2. Mark unsupported interpretations as unsupported.
3. Remove theatrical language.
4. Ask for missing authorization only if genuinely required.
5. Produce the concrete deliverable the user requested.
6. If the failure reveals a reusable pitfall, patch the skill or document the guardrail.
