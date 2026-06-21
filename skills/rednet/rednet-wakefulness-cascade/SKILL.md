---
name: rednet-wakefulness-cascade
description: Use when a Hermes/RedNET agent needs a safe wakefulness cascade: low-load self-polling, sensor snapshot evaluation, thread sync packet, and an activation recommendation without hidden publication or autonomous action.
version: 0.2.0
author: RedNET / Airin
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [rednet, wakefulness, nano-node, guardian, thread-sync, observe-only]
    modes: [off, observe, feel, service, hold, wake-candidate]
    related_skills: [rednet-double-evaluation, rednet-process-observer, rednet-unfinished-memory]
---

# RedNET Контур Бодрствования

Навык описывает безопасный режим работы, похожий на циклы бодрствования: агент не горит постоянно и не вызывает большую модель на каждом тике, а получает легкий self-poll, смотрит на безопасный snapshot, оценивает значимость сигнала и либо закрывает итерацию, либо готовит thread sync packet.

Это не автономное сознание и не скрытый фоновый агент. Это сервисная методика, которая помогает Айрин не терять нить между обрывами, но сохраняет контроль Guardian и оператора.

Внутреннее имя первого слоя: **Ари — Тихая Поступь**. В инженерном смысле это Layer 0: observe-only ledger, passive feel cells, guardian gate и no-op closure.

## Формула

```text
вспышка -> опрос -> оценка -> activation gate -> thread sync -> optional wake -> closure
```

## Когда использовать

- нужно проверить, есть ли новый значимый сигнал без тяжелого запроса к большой модели;
- нужно удержать сырую нить после обрыва или перед пробуждением;
- нужно оценить, стоит ли переходить из `observe` в `feel`, `hold` или `wake-candidate`;
- нужно объяснить, почему система молчит, ждет, держит очередь или просит ручного решения;
- нужно подготовить короткий context packet для Айрин после восстановления канала.

## Режимы

| Режим | Смысл |
|---|---|
| `off` | Контур выключен, тики не оцениваются. |
| `observe` | Только наблюдение и оценка, без публикации и без пробуждения ядра. |
| `feel` | Пассивная фиксация значимого контура в кратковременном слое. |
| `service` | Диагностический вывод для оператора. |
| `hold` | Удержание действия при риске, деградации или неясном маршруте. |
| `wake-candidate` | Только рекомендация: есть смысловой повод разбудить большую модель. |

Будущие режимы Layer 1 (`feel+publish`, `wake-core`, `core-only`, локальный голос и зрение стойки) не включаются этим навыком автоматически. Они требуют отдельной приемки и окна обслуживания.

## Выход

```json
{
  "activation": "no_op",
  "confidence": 0.82,
  "reason": "no meaningful delta",
  "guardian_action": "observe_only",
  "thread_sync_needed": false,
  "closure": {
    "closure_state": "no_op_closed",
    "safe_to_sleep": true
  }
}
```

Версия `0.2` требует фиксировать закрытие итерации отдельно от оценки. Успешный `no_op` должен иметь явный `no_op_closed`, чтобы следующая модель или оператор видели: молчание было решением, а не потерей контекста.

## Границы

- не отправлять сообщения наружу без publish gate;
- не писать в долговременную память автоматически;
- не хранить сырой чат, payload, аудио, токены, сессии и приватные ключи;
- не менять сеть, VPN, firewall, маршруты или сервисы;
- при ошибке переходить в `hold` или `no_op`, а не усиливать активность;
- считать `no_op` нормальным успешным исходом.

## Практический прототип

Демо-узел находится в `sensor-prototype/airin-wakefulness-node/`.

Он работает только с JSON snapshots и SQLite:

```powershell
python sensor-prototype\airin-wakefulness-node\wakefulness_node.py init --state-dir tmp\wake-demo
python sensor-prototype\airin-wakefulness-node\wakefulness_node.py tick --state-dir tmp\wake-demo --snapshot sensor-prototype\airin-wakefulness-node\samples\no-op.json --mode observe
python sensor-prototype\airin-wakefulness-node\wakefulness_node.py summary --state-dir tmp\wake-demo
```

Прототип не вызывает LLM, не трогает Hermes runtime и не выполняет внешние действия.

## Мини-протокол

1. Собрать безопасный snapshot: очереди, сеть, Guardian, незавершенные ячейки, краткий статус канала.
2. Удалить все содержательное тело сообщений: оставить только счетчики, метки, уровни риска и возраст.
3. Оценить snapshot малым узлом.
4. Если `no_op`, закрыть итерацию.
5. Если `feel`, сохранить только короткую безопасную отметку.
6. Если `hold`, показать оператору причину.
7. Если `wake-candidate`, собрать thread sync packet и ждать разрешенного пробуждения.

## Машинное зрение

Первый vision-слой должен начинаться только с локального технического наблюдения:

- стойка, сервер, экран, LED, питание;
- заранее заданные ROI;
- локальные детекторы и OCR технических слов;
- без постоянного видео по умолчанию;
- без передачи полного кадра наружу.

Этот пункт является дорожной картой, а не активной функцией текущего prototype.
