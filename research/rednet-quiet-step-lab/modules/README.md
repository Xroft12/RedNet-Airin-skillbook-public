# RedNET Quiet Step Lab — modules

`modules/` — слой индивидуальной сборки находок под конкретного агента, роль или решение.

Идея проекта: по итогам сессии добыча не должна оставаться только отчётом. Лучшие элементы собираются в модульные пакеты:

```text
discovery cards -> council/double-eval -> module manifest -> eval plan -> pilot -> reusable capability
```

## Типы модулей

- `agent-role` — роль/саб/рулевой лаборатории.
- `solution-pack` — готовая связка для конкретной задачи.
- `sensor` — дешёвый наблюдатель или классификатор.
- `verifier` — точная проверка, schema, hash, frozen eval.
- `storage` — CAS, compression, index, ledger.
- `router` — выбор пути: cache/small/large/human/block.
- `interface` — форма работы: карточка, dashboard, report, inbox.

## Жизненный цикл

1. `candidate` — идея выделена из карточек.
2. `designed` — есть module manifest и границы.
3. `eval_ready` — есть frozen eval / метрики.
4. `pilot_shadow` — работает в observe/shadow/read-only.
5. `pilot_active` — ограниченно включён после проверки.
6. `reusable` — можно подключать к новым агентам/решениям.
7. `retired` — выключен, но сохранён для истории.

## Инвариант безопасности

```text
Module may make work cheaper;
module may not erase verification, consent, privacy, or rollback.
```

## Структура

- `module-manifest.schema.json` — минимальная схема manifest.
- `templates/module-card.md` — шаблон человеческой карточки.
- `packs/` — первые модульные пакеты Wave 1.

## Первые пакеты

- `rednet-quiet-pi-cascade-eval-architect.md` — рулевая роль научной группы.
- `lab-scribe-gguf-3b.md` — локальный nano/small писарь карточек.
- `redpack-jsonl.md` — compression pack для JSONL/KB/logs.
- `hybrid-local-rag.md` — local RAG pack.
- `shadow-router.md` — риск/стоимость router в shadow mode.
