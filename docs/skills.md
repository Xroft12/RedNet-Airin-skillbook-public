# Навыки и мета-навыки

Этот каталог разделяет четыре разные сущности, которые раньше легко смешивались:

1. **Installable skill** — можно копировать в skill storage.
2. **Protocol** — процедура сопровождения, приёмки или отключения.
3. **Prototype** — проверяемый observe-only код/пример, не live runtime.
4. **Concept / research** — идея, модель или отчёт, не обещание готовой функции.

## Быстрые ссылки

| Нужно | Ссылка |
|---|---|
| Полная карта репозитория | [navigation.md](navigation.md) |
| Установка | [../INSTALL.md](../INSTALL.md) |
| Индекс `skills/` | [../skills/README.md](../skills/README.md) |
| Индекс `rednet-meta` | [../skills/rednet-meta/README.md](../skills/rednet-meta/README.md) |
| Пакет Hermes | [../packages/hermes/rednet-airin-meta-skills/README.md](../packages/hermes/rednet-airin-meta-skills/README.md) |

## Installable skills

| Навык | Линия | Режимы | Назначение | Страница |
|---|---|---|---|---|
| `rednet-double-evaluation` | core | `observe`, `light`, `full`, `hold`, `service` | Второй проход по собственному первому анализу: отделить факты, гипотезы, метафоры и действие. | [SKILL.md](../skills/rednet/rednet-double-evaluation/SKILL.md) |
| `rednet-wakefulness-cascade` | core | `off`, `observe`, `feel`, `service`, `hold` | Каскад бодрствования: snapshot и recommendation без скрытой активности. | [SKILL.md](../skills/rednet/rednet-wakefulness-cascade/SKILL.md) |
| `rednet-neural-service-node` | core | `off`, `observe`, `advise`, `hold` | Сервисный сигнализатор: строгий JSON, журнал и pending-рекомендации без прямых действий. | [SKILL.md](../skills/rednet/rednet-neural-service-node/SKILL.md) |
| `rednet-export-parser` | meta | `off`, `observe`, `full`, `hold` | Разбирает длинную выгрузку в хронологию, решения, поворотные точки и границы. | [SKILL.md](../skills/rednet-meta/rednet-export-parser/SKILL.md) |
| `rednet-meta-event-extractor` | meta | `off`, `observe`, `full`, `hold` | Извлекает моменты рождения правил мышления, памяти, оценки и будущих навыков. | [SKILL.md](../skills/rednet-meta/rednet-meta-event-extractor/SKILL.md) |
| `rednet-criteria-layer` | meta | `off`, `observe`, `full`, `hold` | Удерживает критерии качества, приёмки, стиля и безопасной границы. | [SKILL.md](../skills/rednet-meta/rednet-criteria-layer/SKILL.md) |
| `rednet-unfinished-memory` | meta | `off`, `observe`, `full`, `hold` | Фиксирует незавершённые пункты, хвосты и следующий шаг без превращения их в вечную память. | [SKILL.md](../skills/rednet-meta/rednet-unfinished-memory/SKILL.md) |
| `rednet-branch-synchronizer` | meta | `off`, `observe`, `full`, `hold` | Read-only синхронизация выводов между ветками/агентами без смешивания ролей. | [SKILL.md](../skills/rednet-meta/rednet-branch-synchronizer/SKILL.md) |
| `rednet-meta-memory` | meta | `off`, `observe`, `protocol`, `hold` | Собирает память как систему действия: читаемый слой, процессный отчёт, индекс смыслов. | [SKILL.md](../skills/rednet-meta/rednet-meta-memory/SKILL.md) |
| `rednet-intention-map` | meta | `off`, `observe`, `protocol`, `hold` | Отделяет явную просьбу от скрытого критерия, ожидания и риска промаха. | [SKILL.md](../skills/rednet-meta/rednet-intention-map/SKILL.md) |
| `rednet-process-observer` | meta | `off`, `observe`, `protocol`, `hold` | Наблюдает ход длинной работы: курс, ошибки, проверки, потерянные детали. | [SKILL.md](../skills/rednet-meta/rednet-process-observer/SKILL.md) |
| `rednet-uncertainty-register` | meta | `off`, `observe`, `protocol`, `hold` | Разделяет факт, наблюдение, гипотезу, догадку, риск и нужную проверку. | [SKILL.md](../skills/rednet-meta/rednet-uncertainty-register/SKILL.md) |
| `rednet-decision-memory` | meta | `off`, `observe`, `protocol`, `hold` | Фиксирует устойчивые решения и запреты без записи временного настроения как правила. | [SKILL.md](../skills/rednet-meta/rednet-decision-memory/SKILL.md) |
| `rednet-beseda` | meta | `off`, `observe`, `dialogue`, `hold` | Бережная беседа: сильные вопросы, собственная позиция, уточнение смысла. | [SKILL.md](../skills/rednet-meta/rednet-beseda/SKILL.md) |
| `rednet-skill-collector` | meta | `off`, `observe`, `protocol`, `hold` | Превращает повторяемые идеи в проверяемые карточки навыков. | [SKILL.md](../skills/rednet-meta/rednet-skill-collector/SKILL.md) |
| `rednet-utility-evaluator` | meta | `off`, `observe`, `protocol`, `hold` | Проверяет полезность навыка: до/после, эффект, риски, помехи, решение оставить/выключить. | [SKILL.md](../skills/rednet-meta/rednet-utility-evaluator/SKILL.md) |
| `rednet-public-editor` | meta | `off`, `observe`, `protocol`, `hold` | Переводит приватный материал в публичный текст без утечек и восстановимых данных. | [SKILL.md](../skills/rednet-meta/rednet-public-editor/SKILL.md) |
| `rednet-research-protocol` | meta | `off`, `observe`, `protocol`, `hold` | Оформляет исследование воспроизводимо: корпус, метод, выводы, ограничения, приёмка. | [SKILL.md](../skills/rednet-meta/rednet-research-protocol/SKILL.md) |

## Protocols

| Протокол | Для чего | Ссылка |
|---|---|---|
| Session-guided activation | Включить навык в рамках сессии без смешивания с личной памятью. | [protocol](../protocols/session-guided-activation.md) |
| Acceptance and disable | Приёмка, выключатель, rollback и критерии остановки. | [protocol](../protocols/acceptance-and-disable.md) |
| Manifest change support | Сопровождать изменения manifest без потери совместимости. | [protocol](../protocols/manifest-change-support.md) |
| API University activation | Будущая активация через паспорт, полигон и приёмку. | [protocol](../protocols/api-university-activation.md) |
| Skill awakening dialogue | Диалоговая проверка навыка без приватного корпуса. | [protocol](../protocols/skill-awakening-dialogue.md) |

## Prototypes

| Прототип | Режим | Что проверяет | Ссылка |
|---|---|---|---|
| Airin signal sensor | observe-only | Replay+SQLite признаки без payload и без сетевых действий. | [README](../sensor-prototype/airin-signal-sensor/README.md) |
| Airin wakefulness node | observe-only | Self-poll/snapshot/recommendation без LLM-вызовов. | [README](../sensor-prototype/airin-wakefulness-node/README.md) |
| Airin neural service node | observe/advise-only | Pending-рекомендации и redaction guard без прямых действий. | [README](../sensor-prototype/airin-neural-service-node/README.md) |
| Science coordinator | template | Отдельный агент-координатор с API и тестами. | [README](../packages/agents/rednet-science-coordinator/README.md) |
| Portal | read-only | Статическая витрина без live-команд. | [README](../portal/README.md) |

## Concepts / research

| Концепт | Публичная формулировка | Где читать |
|---|---|---|
| Путь Нави | Семантическое восстановление рабочей связности после обрыва без утверждения скрытой памяти. | [architecture.md](architecture.md) |
| Перерождение | Handoff/restore как проверяемая процедура, не перенос личной памяти. | [meta-skills-catalog.md](meta-skills-catalog.md) |
| Нано-узлы | Малые сервисные модули как sensors/verifiers, а не автономный decision maker. | [nano-neural-nodes.md](nano-neural-nodes.md) |
| API-университет | Пакет активации: паспорт, границы, полигон, приёмка, выключатель. | [api-university-activation-model.md](api-university-activation-model.md) |
| Quiet Step Lab | Лаборатория малых модулей и curated reports. | [research README](../research/rednet-quiet-step-lab/README.md) |

## Правило режимов

- `off` — слой выключен.
- `observe` — слой только анализирует.
- `advise` — создаёт рекомендацию, но не действует.
- `hold` — stop-gate до проверки или окна обслуживания.
- `protocol/full` — ведёт рабочий цикл только по явному применению.
- `service/feel` — пассивный сервисный сигнал без автоматической записи в долговременную память.

## Что считается готовым к публикации

Навык готов к публичному чтению, если у него есть:

- назначение и вход;
- режимы и выключатель;
- выход/артефакт;
- границы приватности;
- проверка или dry-run;
- ссылка на протокол/карточку, если они есть;
- отсутствие raw/private corpus и восстановимых настроек.
