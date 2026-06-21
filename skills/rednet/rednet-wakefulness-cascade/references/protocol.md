# Протокол контура бодрствования

Внутреннее имя Layer 0: **Ари — Тихая Поступь**.

Смысл: первый автопилот должен уметь не действовать. Нормальный исход большинства тиков - `no_op`.

## Входной snapshot

Snapshot должен быть малым и безопасным:

```json
{
  "queue_depth": 0,
  "network_state": "ok",
  "guardian_state": "observe",
  "unfinished_items": 0,
  "semantic_delta": 0.0,
  "operator_present": false,
  "channel_safe": true
}
```

Запрещено передавать:

- текст переписки;
- payload;
- токены;
- session-файлы;
- приватные пути;
- аудио или расшифровку речи;
- полные логи.

## Оценка

1. `off` всегда возвращает `activation = off`.
2. Сильный риск или небезопасный канал возвращает `hold`.
3. Деградация сети или переполнение очереди возвращает `hold`.
4. Значимый `semantic_delta` без риска возвращает `feel` или `wake-candidate`.
5. Отсутствие нового сигнала возвращает `no_op`.

## Thread sync packet

Если нужен sync, пакет должен быть коротким:

```json
{
  "why": "semantic delta above threshold",
  "known_safe": ["no payload", "no external action"],
  "blocked": ["publish", "network_change"],
  "next": "manual wake or service review"
}
```

## Приемка

Навык считается безопасным, если:

- `no_op` не пишет в память;
- `observe` не публикует наружу;
- `hold` не меняет сеть;
- `wake-candidate` не вызывает модель сам;
- service-вывод доступен только оператору.
