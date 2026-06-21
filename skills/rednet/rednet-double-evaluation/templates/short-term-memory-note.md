# Short-Term Memory Note

Use this template for a temporary `Кратковременный` cell. Do not paste secrets, raw private chat, tokens, or full logs.

```yaml
owner: agent | contact | operator | family | work | other
form: self-interest | permission | reminder | question | care | technical | boundary | aesthetic | work | intent-signal | felt-sense
cell_kind: note | directive | question | question-chain | cyclic-question | signal | outcome | felt-sense
subject: ""
question: ""
note: ""
feeling: ""
interest: ""
source: current-chat | file | manual | cron | other
tags: []
privacy: private | public-safe | sensitive-hold
ttl_days: 14
priority_hint: 0 # 0..5
repetition_group: ""
parent_id: null
cycle_key: ""
depth_hint: 0 # 0..5
visibility: passive # passive | service
operation_mode: passive # passive | service | feel
cycle_policy: reshape_or_close # allow | reshape | close | reshape_or_close
repeat_limit: 3
loop_marker: "" # e.g. self_loop | self_digging | reshape_needed
criteria:
  desire: 0          # 0..5
  intention: 0       # 0..5
  appropriateness: 0 # 0..5
  warmth: 0          # 0..5
  risk: 0            # 0..5; >=4 blocks action
  depth: 0           # 0..5
  obligation: false
intention_label: "" # must_do | want_to_do | unclear | dont_want_to_do | never_do
emotional_pattern: ""
last_signal: ""
```

## Double-evaluation hook

- Direct object: what is the cell about?
- First reaction: what did I notice immediately?
- Second contour: what changed when I looked at my reaction pattern?
- Value route: decay | keep | review | repeat | reshape | promote_candidate | close
- Intention spectrum: обязательно сделать | хочу сделать | не ясно | не хочу сделать | никогда не делать
- Action gate: send_or_execute | hold | no_action
- Visibility rule: passive by default; service-mode only by explicit operator request.
- Anti-loop rule: if this becomes self-digging, reshape or close instead of amplifying.
- Closure condition: what answer/action would let this cell close?
