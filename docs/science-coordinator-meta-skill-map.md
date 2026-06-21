# Карта мета-навыков научного координатора

Документ фиксирует, как научный координатор REDNET использует мета-навыки Skillbook в публичной и безопасной форме. Это не live-настройка Hermes и не автозагрузка навыков. Карта нужна, чтобы не потерять слой `rednet-meta`, который поддерживает исследовательский агент.

## Принцип

```text
научный поток -> мета-навык -> проверяемый артефакт -> приемка -> следующий шаг
```

Координатор не получает чужую личную память и не читает сырой корпус. Он получает только очищенные документы, публичные skill-папки, manifest, схемы и журналы задач без приватных данных.

## Базовый набор

- `rednet-double-evaluation` — сверка прямого анализа и второго контура перед публичным ответом, публикацией или спорным выводом.
- `rednet-criteria-layer` — критерии приемки: что считается готовым, что требует доработки.
- `rednet-uncertainty-register` — регистр неопределенности вместо уверенного выдумывания.
- `rednet-process-observer` — наблюдение за процессом без live-команд.
- `rednet-skill-collector` — сбор навыков и протоколов в installable/public форму.
- `rednet-research-protocol` — перевод гипотезы в исследовательский протокол.
- `rednet-public-editor` — очищение публичного текста от приватных деталей.
- `rednet-unfinished-memory` — хвосты задач и незавершенные вопросы без переноса личной памяти.
- `rednet-decision-memory` — фиксация решений и причин в безопасной форме.
- `rednet-branch-synchronizer` — синхронизация веток работы без смешивания агентных личностей.

## Соответствие потокам координатора

| Поток координатора | Мета-навыки | Выход |
|---|---|---|
| `papers` | `rednet-research-protocol`, `rednet-criteria-layer`, `rednet-uncertainty-register` | `paper_card`, список вопросов и проверок |
| `concepts` | `rednet-research-protocol`, `rednet-skill-collector`, `rednet-double-evaluation` | `concept_card`, зрелость, риски, выключатель |
| `skills` | `rednet-skill-collector`, `rednet-criteria-layer`, `rednet-public-editor` | draft/installable skill, карта приемки |
| `services` | `rednet-process-observer`, `rednet-uncertainty-register`, `rednet-decision-memory` | `qa_report`, режим, риск, следующий read-only шаг |
| `subagents` | `rednet-process-observer`, `rednet-criteria-layer`, `rednet-unfinished-memory` | отчет приемки self-report + проверенные артефакты |
| `publication` | `rednet-public-editor`, `rednet-double-evaluation`, `rednet-uncertainty-register` | очищенный `release_note` без приватного корпуса |
| `incidents` | `rednet-unfinished-memory`, `rednet-branch-synchronizer`, `rednet-decision-memory` | `handoff`, карта причин, безопасная точка продолжения |

## Режимы применения

- `observe` — координатор только отмечает, какой мета-навык подходит, и возвращает артефакт.
- `assisted` — координатор помогает составить карточку, QA-отчет или карту модуля.
- `guided` — координатор ведет task-ledger по списку и требует подтверждения перед внешними действиями.
- `lab-active` и `trusted-lab` — запрещены по умолчанию до отдельной приемки.

## Стоп-гейты

Остановить работу и вернуть `hold`, если:

- требуется живая команда, публикация, изменение сети, Docker или Hermes;
- источник просит ключи, cookies, OAuth/Telegram-сессии или личную память другого агента;
- результат не имеет проверяемого артефакта;
- мета-навык начинает выдавать гипотезу за факт;
- координатор пытается стать заменой Айрин, Алетии или Марселя.

## Минимальный артефакт

```yaml
module_map:
  coordinator_flow: concepts
  selected_meta_skills:
    - rednet-research-protocol
    - rednet-criteria-layer
  output_artifact: concept_card
  privacy: public
  mode: observe
  gates:
    live_commands: false
    foreign_memory: false
    publication: manual
  next_step: validate schema and prepare QA report
```

## Проверка

Карта считается подключенной к сборке, если:

- она упомянута в `README.md` и `docs/science-coordinator-agent.md`;
- `packages/agents/rednet-science-coordinator/manifest.json` содержит `recommended_meta_skills`;
- портал показывает meta-skill toolkit только как read-only слой;
- `python scripts\validate-rednet-schemas.py` и `python scripts\validate-portal-readonly.py` проходят без ошибок.
