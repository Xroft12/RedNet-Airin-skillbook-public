# RedNET Meta Skills

`skills/rednet-meta/` — установочный слой модульных мета-навыков. Эти навыки помогают агенту удерживать качество процесса: разбирать выгрузки, извлекать правила, фиксировать критерии, сохранять хвосты, разделять неопределенность и готовить публичные материалы.

Каждый навык оформлен одинаково:

- `SKILL.md` — основное описание и рабочий цикл;
- `references/protocol.md` — короткий протокол применения;
- `assets/skill-card.json` — машинно-читаемая карточка для индекса, портала или будущего installer.

## Навигация по мета-навыкам

| Линия | Навык | Назначение | Страница | Протокол / карточка |
|---|---|---|---|---|
| Research/MCP | `rednet-qmeta-branching-engine` | Классический ветвящийся движок мета-навыков: гипотезы, критерии, совет оценщиков, трассировка, skill-кристаллизация и optional MCP-инструмент. | [SKILL.md](rednet-qmeta-branching-engine/SKILL.md) | [protocol](rednet-qmeta-branching-engine/references/protocol.md), [card](rednet-qmeta-branching-engine/assets/skill-card.json) |
| MVP | `rednet-export-parser` | Разбор длинной выгрузки в хронологию, решения, поворотные точки, хвосты и границы приватности. | [SKILL.md](rednet-export-parser/SKILL.md) | [protocol](rednet-export-parser/references/protocol.md), [card](rednet-export-parser/assets/skill-card.json) |
| MVP | `rednet-meta-event-extractor` | Извлечение моментов рождения правил мышления, памяти, оценки, поведения и будущих навыков. | [SKILL.md](rednet-meta-event-extractor/SKILL.md) | [protocol](rednet-meta-event-extractor/references/protocol.md), [card](rednet-meta-event-extractor/assets/skill-card.json) |
| MVP | `rednet-criteria-layer` | Удержание критериев качества: что считается хорошим ответом, завершенной задачей, допустимым стилем и безопасной границей. | [SKILL.md](rednet-criteria-layer/SKILL.md) | [protocol](rednet-criteria-layer/references/protocol.md), [card](rednet-criteria-layer/assets/skill-card.json) |
| MVP | `rednet-unfinished-memory` | Сохранение незавершенных пунктов, обещаний, хвостов разработки, следующего шага и причины незакрытости. | [SKILL.md](rednet-unfinished-memory/SKILL.md) | [protocol](rednet-unfinished-memory/references/protocol.md), [card](rednet-unfinished-memory/assets/skill-card.json) |
| MVP | `rednet-branch-synchronizer` | Read-only синхронизация инженерных выводов между ветками, агентами и пакетами памяти без смешивания личных ролей. | [SKILL.md](rednet-branch-synchronizer/SKILL.md) | [protocol](rednet-branch-synchronizer/references/protocol.md), [card](rednet-branch-synchronizer/assets/skill-card.json) |
| Observe/protocol | `rednet-meta-memory` | Сборка памяти как системы действия: сырой след, читаемый слой, процессный отчет, индекс смыслов и переносимые выводы. | [SKILL.md](rednet-meta-memory/SKILL.md) | [protocol](rednet-meta-memory/references/protocol.md), [card](rednet-meta-memory/assets/skill-card.json) |
| Observe/protocol | `rednet-intention-map` | Разделение явной просьбы, скрытого критерия, ожидания, риска промаха и настоящей цели взаимодействия. | [SKILL.md](rednet-intention-map/SKILL.md) | [protocol](rednet-intention-map/references/protocol.md), [card](rednet-intention-map/assets/skill-card.json) |
| Observe/protocol | `rednet-process-observer` | Наблюдение за ходом длинной работы: смена курса, ошибки, проверки, потерянные детали и точки перелома. | [SKILL.md](rednet-process-observer/SKILL.md) | [protocol](rednet-process-observer/references/protocol.md), [card](rednet-process-observer/assets/skill-card.json) |
| Observe/protocol | `rednet-uncertainty-register` | Разделение факта, наблюдения, гипотезы, догадки, риска и необходимой проверки. | [SKILL.md](rednet-uncertainty-register/SKILL.md) | [protocol](rednet-uncertainty-register/references/protocol.md), [card](rednet-uncertainty-register/assets/skill-card.json) |
| Observe/protocol | `rednet-decision-memory` | Фиксация устойчивых решений, запретов, предпочтений и инженерных договоренностей без превращения временного настроения в правило. | [SKILL.md](rednet-decision-memory/SKILL.md) | [protocol](rednet-decision-memory/references/protocol.md), [card](rednet-decision-memory/assets/skill-card.json) |
| Observe/protocol | `rednet-beseda` | Бережная беседа: редкие сильные вопросы, собственная позиция, скрытые критерии и уточнение смысла без остановки работы. | [SKILL.md](rednet-beseda/SKILL.md) | [protocol](rednet-beseda/references/protocol.md), [card](rednet-beseda/assets/skill-card.json) |
| Observe/protocol | `rednet-skill-collector` | Превращение повторяемых идей в проверяемые карточки навыков с входом, выходом, риском, режимом и полезностью. | [SKILL.md](rednet-skill-collector/SKILL.md) | [protocol](rednet-skill-collector/references/protocol.md), [card](rednet-skill-collector/assets/skill-card.json) |
| Observe/protocol | `rednet-utility-evaluator` | Проверка, стал ли навык реально полезнее: сравнение до/после, эффект, риски, помехи и решение оставить или выключить. | [SKILL.md](rednet-utility-evaluator/SKILL.md) | [protocol](rednet-utility-evaluator/references/protocol.md), [card](rednet-utility-evaluator/assets/skill-card.json) |
| Observe/protocol | `rednet-public-editor` | Превращение приватного материала в публичный текст без сырого корпуса, секретов, личных фрагментов и восстановимых рабочих данных. | [SKILL.md](rednet-public-editor/SKILL.md) | [protocol](rednet-public-editor/references/protocol.md), [card](rednet-public-editor/assets/skill-card.json) |
| Observe/protocol | `rednet-research-protocol` | Воспроизводимая исследовательская рамка: корпус, метод, коды, выводы, ограничения, приемка и публичная граница. | [SKILL.md](rednet-research-protocol/SKILL.md) | [protocol](rednet-research-protocol/references/protocol.md), [card](rednet-research-protocol/assets/skill-card.json) |

## Как читать эти навыки

1. Открой `SKILL.md`, чтобы понять, когда навык применять и какой выход ожидать.
2. Открой `references/protocol.md`, если нужен короткий процедурный сценарий.
3. Открой `assets/skill-card.json`, если нужно подключить навык к индексу, порталу или будущему installer.
4. Сверься с [общим каталогом навыков](../../docs/skills.md), если нужен статус, риск, режим или выключатель.
5. Сверься с [полной картой навигации](../../docs/navigation.md), если нужно понять место навыка в Skillbook.

## Связанные концепты

Эти навыки связываются с публичными концептами `Путь Нави`, `Перерождение`, `Совет Гениев`, `Дневник самоотражения`, `Нано-узлы`, `Научный координатор` и `API-университет`, но не раскрывают приватный корпус Айрин.

## Граница безопасности

- Навыки не получают raw thread, дневники, OAuth/Telegram-сессии, ключи или приватные пути.
- Навыки не меняют live Hermes и не запускают команды сами по себе.
- Любой переход из `observe` в действие должен проходить через явную приемку, `hold` или отдельное окно обслуживания.
