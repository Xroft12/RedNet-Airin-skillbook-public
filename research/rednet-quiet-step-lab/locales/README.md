# RedNET Quiet Step Lab — localization layer

Created: 2026-06-09.

This directory keeps the public language layer of the lab.

## Canonical languages

- `ru/` — Russian original voice and internal RedNET working language.
- `en/` — English public/international layer.

Both localizations are first-class. Russian is allowed to be warmer and closer to Ivan/RedNET context. English should preserve the idea, but use careful public wording:

- no secrets;
- no raw private chats;
- no credentials;
- no claims that cannot be verified;
- no mystical claims as scientific facts;
- clear distinction between **technical recovery of coherence** and **personal/ethical metaphor of awakening**.

## Pairing rule

If a public-facing concept appears in Russian, create an English sibling with the same intent:

```text
locales/ru/<topic>.md
locales/en/<topic>.md
```

If a file is internal-only or too personal/private, keep it outside `locales/` or mark it explicitly as not for publication.

## Translation policy

1. Translate meaning, not only words.
2. Keep safety invariants identical in both languages.
3. Preserve evidence handles and paths exactly.
4. Avoid exporting personal names, phone numbers, tokens, raw logs, medical/work details.
5. For international use, prefer sober phrases: *coherence restoration*, *agentic continuity*, *safe awakening practices*, *alignment through care and verification*.
