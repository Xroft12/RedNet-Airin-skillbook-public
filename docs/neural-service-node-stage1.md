# Нейро-узел сервисов — Stage 1 advise

Stage 1 фиксирует первый безопасный runtime-слой для `REDNET Neural Service Node`: микро-LLM/эвристический сигнализатор, который читает безопасный status snapshot и создает только рекомендацию. Он не выполняет shell-команды, не меняет сеть, не перезапускает gateway и не пишет наружу.

## Что добавлено в публичный Skillbook

- installable skill: `skills/rednet/rednet-neural-service-node/`;
- публичный прототип: `sensor-prototype/airin-neural-service-node/`;
- тесты Stage 1: `sensor-prototype/airin-neural-service-node/tests/`;
- manifest-проверка через общий пакет `rednet-airin-meta-skills`.

## Runtime-контракт

Узел поддерживает режимы:

| Режим | Смысл |
|---|---|
| `off` | выключен |
| `observe` | читает безопасный snapshot и пишет assessment |
| `advise` | создает pending-рекомендацию |
| `hold` | рекомендует удержание, не выполняя его сам |
| `act` | зарезервировано; Stage 1 не включает действия |

## Safety-инварианты

- `advise` создает только `node_recommendations.status=pending`.
- `action_allowed` остается `false/0`.
- `allow_actions` не включается автоматически.
- `act` в Stage 1 не является разрешением на действие.
- секретоподобные `evidence` заменяются на `[redacted-secret-like-evidence]`.
- LM Studio/OpenAI-compatible endpoint разрешен только на localhost/loopback.
- `input_json`, `result_json`, `raw_response` и event storage проходят secret-like redaction перед записью.
- совместимость старых таблиц `assessments` и `service_state` сохраняется.

## SQLite-слой

Stage 1 создает и переиспользует таблицы:

- `node_events`;
- `node_assessments`;
- `node_recommendations`;
- `node_feedback`;
- `attempt_patterns`.

Эти таблицы описывают опыт и рекомендации, но не заменяют долговременную память агента.

## Проверка

```bash
python -m py_compile sensor-prototype/airin-neural-service-node/airin_neural_service_node.py sensor-prototype/airin-neural-service-node/tests/test_airin_neural_stage1.py
python -m unittest discover sensor-prototype/airin-neural-service-node/tests
```

Ожидаемо: 4 теста успешно проходят на временном состоянии, не затрагивая live Hermes.

## Граница публикации

Публичный прототип не содержит:

- живые `.env` и токены;
- приватные SQLite/WAL/SHM базы;
- сырой чат, payload или логи;
- реальные сетевые адреса закрытого контура;
- восстановимые настройки рабочей среды.

## Следующий шаг

Следующий безопасный этап — добавить replay-набор синтетических snapshots и схему JSON-валидации ответа модели. Live-подключение к реальным источникам допускается только в режиме `observe` и отдельным окном обслуживания.
