# Карта навигации REDNET Airin Skillbook

![Карта Skillbook](../assets/skillbook-map.svg)

Эта страница — канонический индекс репозитория. README остаётся короткой витриной, а здесь собраны все основные маршруты.

## Быстрый вход

| Нужно | Куда идти | Что там есть |
|---|---|---|
| Понять проект | [README](../README.md) | Короткая витрина и основные команды. |
| Читать документацию по ролям | [docs/index.md](index.md) | Маршруты для читателя, установщика, ревьюера и контрибьютора. |
| Проверить публичную границу | [privacy-boundary.md](privacy-boundary.md) | Что можно публиковать, что остаётся приватным. |
| Установить навыки безопасно | [../INSTALL.md](../INSTALL.md) | Dry-run, apply, rollback, verify. |
| Найти конкретный навык | [../skills/README.md](../skills/README.md) | Прямые ссылки на `SKILL.md`, протоколы и карточки. |
| Посмотреть портал | [../portal/README.md](../portal/README.md) | Локальный read-only UI без live-команд. |
| Подготовить публикацию | [release-checklist.md](release-checklist.md) | Secret scan, links, visuals, history review. |

## Документация

| Раздел | Страницы |
|---|---|
| Проект и граница | [Архитектура](architecture.md), [граница приватности](privacy-boundary.md), [словарь](glossary.md), [этапы](project-stages.md), [дорожная карта](roadmap.md) |
| Навыки | [Каталог навыков](skills.md), [каталог мета-навыков](meta-skills-catalog.md), [double evaluation](double-evaluation-meta-skill.md), [archive-derived meta-skills](archive-derived-meta-skills.md) |
| Нано-узлы и сенсоры | [nano-neural-nodes](nano-neural-nodes.md), [neural service node stage 1](neural-service-node-stage1.md), [wakefulness cascade](airin-wakefulness-cascade.md), [passive signal sensor](passive-signal-sensor.md) |
| Портал и режимы | [портал](rednet-portal.md), [режимы агентов](agent-operating-modes.md), [сабагенты](subagent-scientific-regulation.md), [реестр концептов](concept-analysis-registry.md) |
| Сервисные слои | [локальный резервный чат](local-chat-fallback.md), [external expression channels](external-expression-channels.md), [Docker monitor](docker-agents-admin-monitor.md), [VLESS layer](vless-support-layer.md) |
| API / координатор | [API-университет](api-university-activation-model.md), [научный координатор](science-coordinator-agent.md), [карта мета-навыков координатора](science-coordinator-meta-skill-map.md) |
| Hermes next generation | [исследование клиента](hermes-next-generation-research.md), [реестры](hermes-next-gen-registries.md), [schemas](../schemas/), [examples](../examples/hermes-next-gen/) |
| Релиз | [installable release](installable-skills-release.md), [export targets](export-targets.md), [cycle close](cycle-close-protocol.md), [CHANGELOG](../CHANGELOG.md), [NEXT_START_HERE](../NEXT_START_HERE.md) |

## Installable skills

| Навык | Назначение | Страница | Протокол / карточка |
|---|---|---|---|
| `rednet-double-evaluation` | Двойная оценка первого и второго слоя анализа. | [SKILL.md](../skills/rednet/rednet-double-evaluation/SKILL.md) | [activation](../skills/rednet/rednet-double-evaluation/references/activation-protocol.md), [safety](../skills/rednet/rednet-double-evaluation/references/safety-and-boundaries.md), [short-term](../skills/rednet/rednet-double-evaluation/references/short-term-memory-layer.md) |
| `rednet-wakefulness-cascade` | Self-poll → snapshot → nano-eval → recommendation без скрытых действий. | [SKILL.md](../skills/rednet/rednet-wakefulness-cascade/SKILL.md) | [protocol](../skills/rednet/rednet-wakefulness-cascade/references/protocol.md), [card](../skills/rednet/rednet-wakefulness-cascade/assets/skill-card.json) |
| `rednet-neural-service-node` | Observe/advise-only сервисный сигнализатор. | [SKILL.md](../skills/rednet/rednet-neural-service-node/SKILL.md) | [protocol](../skills/rednet/rednet-neural-service-node/references/protocol.md), [card](../skills/rednet/rednet-neural-service-node/assets/skill-card.json) |
| `rednet-meta/*` | 15 модульных мета-навыков процесса. | [rednet-meta index](../skills/rednet-meta/README.md) | `references/protocol.md`, `assets/skill-card.json` внутри каждого навыка |

## Пакеты, портал, прототипы

| Зона | Что внутри |
|---|---|
| [packages/hermes/rednet-airin-meta-skills](../packages/hermes/rednet-airin-meta-skills/README.md) | Manifest, PowerShell installer, dry-run/apply/force. |
| [packages/rednet-double-evaluation-meta-skill](../packages/rednet-double-evaluation-meta-skill/README.md) | Отдельный пакет `rednet-double-evaluation` с docs, installer и validator. |
| [packages/agents/rednet-science-coordinator](../packages/agents/rednet-science-coordinator/README.md) | Шаблон агента-научного координатора с тестами и `.env.example`. |
| [portal](../portal/README.md) | Статическая локальная read-only витрина. |
| [sensor-prototype/airin-signal-sensor](../sensor-prototype/airin-signal-sensor/README.md) | Replay+SQLite observe-only sensor. |
| [sensor-prototype/airin-wakefulness-node](../sensor-prototype/airin-wakefulness-node/README.md) | Observe-only wakefulness node. |
| [sensor-prototype/airin-neural-service-node](../sensor-prototype/airin-neural-service-node/README.md) | Stage 1 pending recommendations without direct action. |
| [coordination/triad](../coordination/triad/README.md) | Handoff schema и координационный канал без raw private ledger. |
| [assets](../assets/README.md) | SVG-схемы и визуальные материалы без приватных данных. |

## Исследовательская лаборатория

| Раздел | Что публикуется |
|---|---|
| [Quiet Step Lab](../research/rednet-quiet-step-lab/README.md) | Публичная рамка лаборатории малых модулей. |
| [LAB_MAP](../research/rednet-quiet-step-lab/LAB_MAP.md) | Карта curated-слоёв лаборатории. |
| [PROCESS](../research/rednet-quiet-step-lab/PROCESS.md) | Процесс hunt → harvest → carve → trophies. |
| [modules](../research/rednet-quiet-step-lab/modules/README.md) | Module packs и reusable capabilities. |
| [pipelines RU](../research/rednet-quiet-step-lab/pipelines/HUNT-HARVEST-CARVE-TROPHIES.ru.md) | Русский pipeline исследования. |
| [reports/wave1 digest](../research/rednet-quiet-step-lab/reports/2026-06-09-wave1-digest.md) | Очищенный дайджест волны. |

Raw `inbox/`, ledger exports, SQLite/JSONL базы и локальные зеркала не являются частью публичной карты.

## Проверки

```powershell
python scripts\validate-rednet-schemas.py
python scripts\validate-portal-readonly.py
powershell -ExecutionPolicy Bypass -File packages\hermes\rednet-airin-meta-skills\install.ps1 -DryRun
```

Перед будущей публикацией дополнительно проверить историю Git, архивы/ZIP, изображения и untracked-файлы.
