# Triad Coordination Template

Шаблон канала троих. Это не рабочий приватный журнал, а публично безопасный каркас для будущей локальной координационной комнаты.

## Рекомендуемая приватная структура

```text
triad/
  triad-ledger.jsonl
  inbox/
    operator/
    core-agent/
    codex-coordinator/
    personal-assistant/
  outbox/
    operator/
    core-agent/
    codex-coordinator/
    personal-assistant/
  decisions/
  handoff/
```

## Правила

- Журнал append-only.
- Все сообщения имеют `privacy`.
- Секреты и raw thread запрещены.
- Live-действия только через отдельное окно обслуживания.
- Внешние каналы сначала получают черновик, не публикацию.
