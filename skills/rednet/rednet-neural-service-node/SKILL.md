---
name: rednet-neural-service-node
description: RedNET/Airin микро-ЛЛМ как сервисный нейро-сигнализатор: observe/advise-only контур, строгий JSON, SQLite-журнал, pending-рекомендации и запрет прямых действий.
version: 1.1.0
author: RedNET / Airin
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [rednet, airin, lmstudio, sqlite, safety, advise, nano-node]
    modes: [off, observe, advise, hold, act]
    related_skills: [rednet-wakefulness-cascade, rednet-double-evaluation, rednet-process-observer]
---

# REDNET Neural Service Node

## Назначение

Навык описывает микро-ЛЛМ как сервисный нейро-сигнализатор Айрин и RedNET. Это не чат-агент и не автономный исполнитель команд. Узел читает безопасные статусы, журналы попыток и агрегированные признаки, а затем выдает структурированную оценку ситуации.

Главная цель: дать сервисам Айрин смысловой слой над уже существующими проверками, не нарушая стабильность gateway, внешних каналов, OAuth, VPN, Tailscale, SSH и маршрутизации.

## Базовая модель

Стартовая модель для MVP:

- маленькая локальная модель через LM Studio или совместимый OpenAI-like endpoint;
- эвристический fallback при недоступности модели;
- SQLite-журнал попыток и рекомендаций;
- режим по умолчанию: `observe`.

Крупные модели допускаются только для ручного анализа или отдельного сервера. Они не должны быть always-on на слабом узле без проверки памяти, температуры и стоимости.

## Режимы

| Режим | Поведение |
|---|---|
| `off` | Полностью выключен. |
| `observe` | Читает, классифицирует, пишет оценку. |
| `advise` | Создает рекомендацию человеку или Control Center со статусом `pending`. |
| `hold` | Может рекомендовать удержание очереди или локальный канал, но не выполняет действие. |
| `act` | Зарезервировано: только whitelisted операции после отдельного допуска; Stage 1 не включает `allow_actions`. |

Стартовый режим: `observe`.

## Входные данные

Узел может читать только безопасные агрегаты:

- модульный status snapshot;
- счетчики очередей и DLQ;
- признаки деградации канала без payload;
- состояние Guardian/hold;
- обезличенные признаки повторяющихся попыток;
- события локального резервного канала без сырого содержимого.

Узел не должен читать секреты полностью и не должен выводить токены, ключи, пароли, приватные маршруты или рабочие базы в публичные отчеты.

## Выходной формат

Ответ узла должен быть строгий JSON:

```json
{
  "state": "telegram_degraded",
  "severity": "warning",
  "confidence": 0.72,
  "evidence": ["gateway_alive", "telegram_timeout", "proxy_ok"],
  "recommendation": "hold_queue_and_use_local_chat",
  "forbidden": ["reset_gateway", "change_default_route"]
}
```

Если JSON невалиден, результат считается недействительным и не может попасть в очередь действий.

## Запреты

Узел не имеет права:

- останавливать или перезапускать gateway;
- нажимать Retry/Repair/Update штатного Hermes Desktop;
- менять default route;
- трогать VPN, Tailscale, SSH, firewall или роутеры;
- переключать сетевые адаптеры без отдельного окна обслуживания;
- выполнять shell-команды как действие рекомендации;
- писать людям, публиковать сообщения или менять внешние каналы;
- смешивать разные контуры памяти Айрин, Алетии и других агентов.

## Память попыток

Рост качества происходит через проверяемый журнал:

- симптом;
- канал;
- рекомендация;
- результат;
- confidence;
- срок устаревания;
- связь с похожими случаями.

Это не бесконтрольное самообучение. Это журнал опыта, который можно replay-тестировать и позже использовать для дистилляции.

## Stage 1 advise

Публичный прототип находится в `sensor-prototype/airin-neural-service-node/`.

Проверка из корня репозитория:

```bash
python -m py_compile sensor-prototype/airin-neural-service-node/airin_neural_service_node.py sensor-prototype/airin-neural-service-node/tests/test_airin_neural_stage1.py
python -m unittest discover sensor-prototype/airin-neural-service-node/tests
```

Stage 1 `advise` создает запись в `node_recommendations` со `status=pending` и `action_allowed=0`, но не исполняет рекомендацию. `act` в Stage 1 всегда остается blocked/no-action, даже если persistent config был изменен вручную. Evidence, compact input, normalized result и raw model response перед сохранением должны редактировать секретоподобные строки в `[redacted-secret-like-evidence]`. LM Studio/OpenAI-compatible endpoint допускается только на localhost/loopback.

## Критерий готовности

- Узел дает объяснимую классификацию по безопасному snapshot.
- Все ответы проходят JSON-нормализацию.
- Нет прямых действий с сетью, gateway или каналами.
- Все рекомендации можно выключить через `off`.
- Control Center или оператор видит состояние узла отдельно от gateway.
- Тесты Stage 1 проходят на временном state-dir без live Hermes.
