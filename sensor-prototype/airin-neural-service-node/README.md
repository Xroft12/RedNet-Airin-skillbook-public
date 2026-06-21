# Airin Neural Service Node — Stage 1 advise

Публичный прототип сервисного нейро-узла Айрин. Он предназначен для проверки режима `observe/advise`: узел читает безопасный status snapshot, нормализует признаки, пишет SQLite-журнал и создает только рекомендацию со статусом `pending`.

Прототип не является live runtime и не должен сам менять Hermes, маршруты, VPN, Tailscale, SSH, gateway или внешние каналы.

## Состав

- `airin_neural_service_node.py` — самодостаточный Python runtime для Stage 1.
- `tests/test_airin_neural_stage1.py` — тесты safety-инвариантов Stage 1.

## Режимы

- `off` — узел выключен.
- `observe` — оценка состояния и запись безопасной диагностики.
- `advise` — создание рекомендации `pending`, без исполнения.
- `hold` — рекомендация удержания, без изменения внешних сервисов.
- `act` — зарезервировано; в Stage 1 `allow_actions` остается выключенным.

## Safety-инварианты Stage 1

- `advise` создает только запись в `node_recommendations`.
- `action_allowed` остается `false/0`.
- shell/network/gateway-действия не выполняются.
- режим `act` не включает `allow_actions` автоматически.
- секретоподобные строки в `evidence` заменяются на `[redacted-secret-like-evidence]`.
- старые таблицы `assessments` и `service_state` сохраняются для совместимости.

## Таблицы SQLite

- `node_events`
- `node_assessments`
- `node_recommendations`
- `node_feedback`
- `attempt_patterns`

## Проверка

Из корня репозитория:

```bash
python -m py_compile sensor-prototype/airin-neural-service-node/airin_neural_service_node.py sensor-prototype/airin-neural-service-node/tests/test_airin_neural_stage1.py
python -m unittest discover sensor-prototype/airin-neural-service-node/tests
```

Ожидаемо: 4 теста проходят успешно.

## Безопасный smoke без live-состояния

Для ручного smoke можно временно направить состояние в `tmp/`, который не публикуется:

```bash
LOCALAPPDATA="$PWD/tmp/neural-demo" python sensor-prototype/airin-neural-service-node/airin_neural_service_node.py init
LOCALAPPDATA="$PWD/tmp/neural-demo" python sensor-prototype/airin-neural-service-node/airin_neural_service_node.py set-mode advise --reason "public safe smoke"
LOCALAPPDATA="$PWD/tmp/neural-demo" python sensor-prototype/airin-neural-service-node/airin_neural_service_node.py advise --source public-smoke
LOCALAPPDATA="$PWD/tmp/neural-demo" python sensor-prototype/airin-neural-service-node/airin_neural_service_node.py status
```

Если LM Studio недоступен, узел должен перейти на эвристическую оценку, а не выполнять действия.

## Публичная граница

В репозиторий не включаются реальные конфиги, живые SQLite/WAL/SHM базы, токены, логи, приватные адреса, payload и рабочие сессии. Этот прототип — только безопасная проверяемая оболочка Stage 1.
