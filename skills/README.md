# Установочные навыки

`skills/` — installable-слой REDNET Airin Skillbook. Здесь лежат только переносимые skill-папки: каждая должна устанавливаться, отключаться и проверяться отдельно.

## Контракт папки навыка

Минимальная структура:

```text
skills/<category>/<skill-name>/
  SKILL.md
  references/protocol.md      # если нужен короткий сценарий применения
  assets/skill-card.json      # если навык индексируется порталом/manifest
  templates/                  # только публичные шаблоны
  scripts/                    # только безопасные helper scripts
```

`SKILL.md` должен отвечать на вопросы:

1. Когда применять навык?
2. Какой вход он принимает?
3. Какой артефакт/выход должен вернуть?
4. Какие режимы и stop-gates существуют?
5. Что нельзя делать без явного окна обслуживания?
6. Чем проверить результат?

## Быстрая карта

| Раздел | Что внутри | Куда перейти |
|---|---|---|
| `rednet/` | 3 базовых REDNET-навыка: double evaluation, wakefulness cascade, neural service node. | [Базовые навыки](#базовые-rednet-навыки) |
| `rednet-meta/` | 15 мета-навыков процесса: parsing, criteria, uncertainty, public editor, research protocol и др. | [rednet-meta/README](rednet-meta/README.md) |
| Документация | Каталог с типами: installable, protocol, prototype, concept. | [../docs/skills.md](../docs/skills.md) |
| Установка | Dry-run/apply/rollback. | [../INSTALL.md](../INSTALL.md) |

## Базовые REDNET-навыки

| Навык | Назначение | Режимы / статус | Страница | Протокол / карточка |
|---|---|---|---|---|
| `rednet-double-evaluation` | Двойная оценка: прямой анализ объекта, затем анализ собственного первого анализа и сверка слоёв. | `observe`, `light`, `full`, `hold`; MVP+ | [SKILL.md](rednet/rednet-double-evaluation/SKILL.md) | [activation](rednet/rednet-double-evaluation/references/activation-protocol.md), [safety](rednet/rednet-double-evaluation/references/safety-and-boundaries.md), [short-term](rednet/rednet-double-evaluation/references/short-term-memory-layer.md) |
| `rednet-wakefulness-cascade` | Контур бодрствования: self-poll, safe snapshot, nano-evaluation, thread sync и рекомендация без скрытых действий. | `off`, `observe`, `feel`, `service`, `hold`; Prototype MVP | [SKILL.md](rednet/rednet-wakefulness-cascade/SKILL.md) | [protocol](rednet/rednet-wakefulness-cascade/references/protocol.md), [skill-card](rednet/rednet-wakefulness-cascade/assets/skill-card.json) |
| `rednet-neural-service-node` | Микро-ЛЛМ/эвристический сервисный сигнализатор: observe/advise-only, строгий JSON, SQLite-журнал, pending-рекомендации. | `off`, `observe`, `advise`, `hold`; Stage 1 advise | [SKILL.md](rednet/rednet-neural-service-node/SKILL.md) | [protocol](rednet/rednet-neural-service-node/references/protocol.md), [skill-card](rednet/rednet-neural-service-node/assets/skill-card.json) |

## Мета-навыки `rednet-meta`

Полная таблица вынесена в [rednet-meta/README.md](rednet-meta/README.md), чтобы корень `skills/` оставался install-facing, а не дублировал весь каталог.

Главные группы:

| Группа | Навыки | Что удерживают |
|---|---|---|
| Вход и извлечение | `rednet-export-parser`, `rednet-meta-event-extractor` | Структуру выгрузки, хронологию, события рождения правил. |
| Качество процесса | `rednet-criteria-layer`, `rednet-process-observer`, `rednet-utility-evaluator` | Критерии, ход работы, полезность результата. |
| Память и решения | `rednet-unfinished-memory`, `rednet-decision-memory`, `rednet-meta-memory` | Хвосты, устойчивые решения, переносимые выводы. |
| Неопределённость и цель | `rednet-uncertainty-register`, `rednet-intention-map`, `rednet-double-evaluation` | Факты/гипотезы, намерения, второй проход. |
| Публикация и исследование | `rednet-public-editor`, `rednet-research-protocol`, `rednet-skill-collector` | Public-safe редактирование, исследовательский протокол, упаковка навыков. |
| Связность | `rednet-branch-synchronizer`, `rednet-beseda` | Read-only синхронизацию веток и бережный диалог. |

## Установка

Сначала dry-run:

```powershell
powershell -ExecutionPolicy Bypass -File packages\hermes\rednet-airin-meta-skills\install.ps1 -DryRun
```

Фактическая установка — только в окно обслуживания:

```powershell
powershell -ExecutionPolicy Bypass -File packages\hermes\rednet-airin-meta-skills\install.ps1 -Apply
```

Подробно: [../INSTALL.md](../INSTALL.md).

## Публичная граница

В `skills/` нельзя добавлять:

- raw chat, дневники, приватные PDF/капсулы;
- `.env`, ключи, cookies, OAuth/Telegram-сессии;
- runtime SQLite/JSONL базы и логи;
- реальные сетевые адреса закрытого контура;
- инструкции, которые сами выполняют live-действия без stop-gate.
