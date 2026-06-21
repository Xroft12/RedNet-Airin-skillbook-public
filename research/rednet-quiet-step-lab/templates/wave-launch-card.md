# Wave launch card

```yaml
wave_id: YYYY-MM-DD-topic
locale: ru | en | bilingual
mode: observe | soft | active
owner: Ari / Airin / RedNET
objective: one sentence
budget:
  time_minutes: 30
  max_subagents: 3
  paid_api: false
hunters:
  - role: compression-hunter
    scope: public sources + local repo only
    expected_output: discovery cards
  - role: math-lever-hunter
    scope: public sources + local notes only
    expected_output: discovery cards
  - role: ai-nano-hunter
    scope: public sources + local experiments only
    expected_output: discovery cards
forbidden:
  - secrets
  - raw private logs
  - paid API without explicit permission
  - write access outside approved lab paths
  - final risky actions without Guardian/human gate
success_criteria:
  - verifiable discovery card
  - module candidate
  - eval/metric
  - safe pilot plan
  - strong reject reason
outputs:
  - inbox/YYYY-MM-DD/*.md
  - data/discoveries.jsonl
  - council/*.md
  - reports/*.md
  - modules/packs/*.md or trophy candidates
```

## Human note

Why this wave matters:

- 

What must not be lost:

- 

What would count as a real trophy:

- 
