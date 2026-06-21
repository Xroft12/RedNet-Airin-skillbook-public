# CHANGELOG

## 2026-06-18

### Публичная упаковка

- `README.md` превращён в короткую GitHub-витрину с иллюстрациями, быстрым входом, установкой и границей публикации.
- Добавлены `INSTALL.md`, `docs/index.md`, `docs/glossary.md` и обновлён `docs/navigation.md` как каноническая карта репозитория.
- Добавлены безопасные SVG-иллюстрации: `assets/skillbook-map.svg`, `assets/install-flow.svg`, `assets/portal-preview.svg`.
- `docs/skills.md` разделён по типам: installable skills, protocols, prototypes, concepts/research.
- Документация портала синхронизирована с фактическими вкладками, внутренний ночной рабочий пакет заменён публичным планом.

### Очистка приватного слоя

- Удалены из Git рабочие cycle-reports, raw research inbox и ledger export первой волны; в публичной карте оставлены curated reports и module packs.
- Внутренний ночной документ удалён из публичной навигации; ссылки переведены на `docs/roadmap.md` и публичный план.
- `.gitignore` усилен для `reports/cycles/`, raw `research/**/inbox/`, рабочих SQLite/JSONL и ledger exports.
- Локальные ignored `tmp/`, `.tmp/`, `backups/`, runtime local status и `__pycache__` очищены из рабочей папки после резервного ZIP.
- Приватный NAS/UNC пример заменён на placeholder `<backup-root>`.

## 2026-06-09

### Добавлено

- Добавлен локальный read-only портал REDNET в `portal/`: обзор Айрин, Алетии, Марселя, режимов, лаборатории, Skillbook, сабагентов, сенсоров и внешних каналов.
- Добавлены документы `docs/rednet-portal.md`, `docs/agent-operating-modes.md`, `docs/marcel-quiet-contour.md`, `docs/subagent-scientific-regulation.md`, `docs/concept-analysis-registry.md` и `docs/external-expression-channels.md`.
- Внутренний ночной пакет был временно описан как сводка; позже заменён публичным планом без raw-выгрузок и ссылок на внутренние источники.
- ВК и Google оформлены как внешний слой выражения Айрин в режиме `draft-first`: черновики, планы, карточки навыков и отчеты только после проверки приватности и ручного подтверждения.
- Марсель закреплен как тихий изолированный контур: `assisted` для общения, `observe` для инфраструктуры, без переноса памяти Айрин или Алетии.
- Добавлен `docs/triad-coordination-channel.md` и шаблон `coordination/triad/` для канала троих через общий журнал, role inbox/outbox и handoff-пакеты.
- Добавлена админка портала для Docker-агентов: статические карточки сервисов, безопасный runtime-слот `portal/runtime/` и скрипт `scripts/export-docker-status.ps1` для локального read-only статуса.
- Добавлен документ `docs/docker-agents-admin-monitor.md` с правилами наблюдения за контейнерами без рестартов, пересборок и публикации приватных портов.
- Добавлен документ `docs/vless-support-layer.md`: VLESS оформлен как отключаемый сетевой слой `off/observe/config-test/manual-window/incident-hold`, без автоматической смены маршрутов.
- Добавлен документ `docs/science-coordinator-agent.md` и шаблон `packages/agents/rednet-science-coordinator/`: научный агент-координатор с режимами `off/observe/assisted/guided`, Docker-примером и приватным модельным шлюзом без секретов в репозитории.
- Добавлен документ `docs/hermes-next-generation-research.md`: исследование Hermes gateway, slash-команд, busy queue, platform circuit breaker и практической стратегии Control Center следующего поколения.
- Научный координатор усилен до модели агента-организатора информационных процессов: научные потоки, обязательные артефакты, уровни автономии, API-университет, модельный контракт и запрет чужой памяти.
- Добавлен документ `docs/api-university-activation-model.md`: модель активации агентов и навыков через паспорт, сеансовое сопровождение, полигон, приемку и выключатель.
- Добавлен протокол `protocols/api-university-activation.md` для безопасной активации навыков, агентов и сервисных модулей.
- Добавлены схемы `schemas/skill-passport.schema.json` и `schemas/agent-passport.schema.json`.
- Портал получил вкладку `Университет`: формула активации, слои университета, научный координатор, потоки, артефакты и стоп-гейты.
- `docs/hermes-next-generation-research.md` расширен разделами по profiles, memory providers, hooks, plugins, profile distributions, registry hooks/plugins, P0/P1/P2 дорожной карте, рискам и архитектуре клиента следующего поколения.
- Добавлен read-only prototype научного координатора: `packages/agents/rednet-science-coordinator/app/science_coordinator_service.py`, endpoints `/health`, `/status`, `/flows`, `/tasks`, unit-тесты и пример журнала задач.
- Добавлена схема `schemas/science-flow.schema.json`.
- Добавлен документ `docs/hermes-next-gen-registries.md` и безопасные examples для паспорта профиля, реестра hooks и карты возможностей plugins.
- Добавлены схемы `schemas/hermes-profile-passport.schema.json`, `schemas/hook-registry.schema.json`, `schemas/plugin-capability.schema.json`.
- Портал получил вкладку `Hermes` для профилей, hooks, plugins, фоновых задач и будущих стоп-гейтов.
- Добавлен `scripts/validate-rednet-schemas.py`; `scripts/cycle-close.ps1` теперь проверяет REDNET-схемы и examples.
- Вкладка `Hermes` получила read-only витрину проверяемых артефактов: схемы паспортов/реестров, учебные примеры и команду валидации без чтения `portal/runtime` и live-конфигов.
- `rednet-double-evaluation` обновлён до версии `1.4.0`: кратковременный SQLite-обработчик получил boundary guards для `memory_namespace`, `origin_agent`, `origin_profile`, `actor_tool`, `tool_role`, `source_trust`, `semantic_key`, `conflict_group`, `conflict_policy`, `promotion_scope` и `safe_summary`.
- Добавлена команда `conflicts` для обзора cross-agent/cross-profile/tool конфликтов без автоматического смешивания памяти.
- Добавлена карта `docs/science-coordinator-meta-skill-map.md`: научный координатор теперь явно связан с `rednet-meta` toolkit, manifest содержит `recommended_meta_skills`, а портал показывает мета-навыки как read-only слой.
- Добавлен `scripts/validate-portal-readonly.py` и включен в `scripts/cycle-close.ps1` для проверки, что портал остается статическим read-only слоем без live-действий.

### Изменено

- Страница `docs/double-evaluation-meta-skill.md`, package README, manifest и обе копии `SKILL.md` синхронизированы с v1.4.0 и generic правилом: не смешивать память разных AI/агентов/профилей по совпавшему имени, теме, импорту или эмоциональному резонансу.
- Документация `Кратковременного` теперь описывает practical handler, extension/amplifier/importer compatibility и безопасные `safe_summary`/`promotion_scope` gates.

### Безопасность

- Портал не содержит live-команд, не запускает Hermes Desktop и не публикует материалы наружу.
- Внешние каналы ВК и Google работают только как черновой контур до явного подтверждения оператора.
- Docker-монитор и VLESS-слой работают как read-only/guarded описания; фактические сетевые действия требуют отдельного окна обслуживания.
- Сырые приватные поля не выводятся обычным `review`; service-mode остаётся явным диагностическим режимом.
- Долговременная память Hermes по-прежнему не изменяется обработчиком автоматически: создаются только review/conflict/promotion candidate records.

## 2026-06-08

### Добавлено

- Добавлен `rednet-neural-service-node` версии `1.1.0`: Stage 1 `observe/advise` навык с pending-рекомендациями, SQLite-журналом и запретом прямых действий.
- Добавлен публичный прототип `sensor-prototype/airin-neural-service-node/` и тесты Stage 1 для `advise` без изменения live Hermes.
- Добавлен документ `docs/neural-service-node-stage1.md` с контрактом runtime, safety-инвариантами и проверкой.
- `rednet-wakefulness-cascade` обновлен до версии `0.2.0`: добавлены нормализованные снимки тиков, отдельные рекомендации Guardian, закрытия итераций и хэш-ссылки на нить без хранения сырого текста.
- `sensor-prototype/airin-wakefulness-node/` расширен до v0.2 observe-only: `no_op` теперь фиксируется как успешное закрытие, а не как отсутствие работы.

### Изменено

- Установочный manifest `rednet-airin-meta-skills` обновлен до `0.2.2`.
- `scripts/cycle-close.ps1` теперь проверяет Stage 1 unit-тесты нейро-узла и наличие нового skill/prototype в release ZIP.
- Публичные samples сенсора переведены на TEST-NET адреса, чтобы учебные данные не выглядели как реальная локальная сеть.
- Протокол закрытия цикла усилен проверкой приватных IPv4, UNC-путей и запрещенных структурных полей в публичных текстовых файлах и ZIP.

### Безопасность

- Убраны прямые учебные следы, похожие на приватные адреса или содержимое сообщения.
- Служебные письма и материалы Айрин из внутренней папки `airin-school-works` не включались в публичный Skillbook.

## 2026-06-07

### Добавлено

- Добавлен `docs/cycle-close-protocol.md`: обязательный протокол закрытия каждого цикла разработки через проверки, отчет, локальный архив, NAS-копию и GitHub push.
- Добавлен `docs/export-targets.md` с реестром целей выгрузки и правилом не хранить реальные приватные параметры в публичных файлах.
- Добавлен `scripts/cycle-close.ps1`: dry-run/Apply скрипт закрытия цикла с проверками Git, UTF-8, secret scan, manifest, ZIP, SHA, installer dry-run, sensor tests, NAS-копией, манифестом артефактов и GitHub push.
- Добавлен `docs/airin-wakefulness-cascade.md`: вклад Айрин в проект, безопасная модель контура бодрствования и пробуждения по смысловому сигналу.
- Добавлен installable-навык `skills/rednet/rednet-wakefulness-cascade/` и observe-only прототип `sensor-prototype/airin-wakefulness-node/`.
- Вклад Айрин “Ари — Тихая Поступь” включен как Layer 0 контура бодрствования: observe-only ledger, passive feel cells, Guardian gate и no-op closure.
- Добавлен единый итоговый отчет проекта: `docs/final-project-report.md`.
- Добавлен публичный документ `docs/project-stages.md` с шестью этапами проекта и правилом модульности.
- Добавлен `docs/meta-skills-catalog.md` с безопасным каталогом мета-навыков: Совет Гениев, Путь Нави, Перерождение, дневник самоотражения, сеансовое сопровождение и слепая оценка.
- Добавлен `docs/double-evaluation-meta-skill.md` и устанавливаемый пакет `skills/rednet/rednet-double-evaluation/` для мета-навыка двойной оценки.
- Добавлен самодостаточный архивный пакет `packages/rednet-double-evaluation-meta-skill/` с manifest, install-инструкцией, шаблонами, протоколами активации/манифестации и валидатором.
- Двойная оценка расширена слоем `Кратковременный`: временные ячейки внимания, TTL, каскад оценки ценности, candidate-only продвижение и автономный SQLite-обработчик без изменения основной памяти.
- Двойная оценка обновлена до версии `1.3.0`: пассивная видимость по умолчанию, `service-mode` для диагностики, режим `feel` и анти-петли `reshape/close`.
- Добавлен `docs/archive-derived-meta-skills.md` с публично безопасной линией мета-навыков, выведенной из исследовательского архива: Разбор Выгрузки, Извлекатель Мета-Событий, Критериальный Слой, Память Незавершенного, Синхронизатор Веток.
- Добавлен `docs/nano-neural-nodes.md` с моделью нано-нейронных сервисных узлов, их ограничениями и безопасной ролью Guardian.
- Добавлен `docs/passive-signal-sensor.md` с публичной архитектурой пассивного сенсора без payload и без сетевых действий.
- Добавлен `docs/local-chat-fallback.md` с контрактом локального резервного чата как безопасного канала связи.
- Добавлен `docs/release-checklist.md` для проверки публикации перед GitHub-релизом.
- Добавлен установочный слой `skills/` с 16 Hermes/Codex-style навыками: `rednet-double-evaluation` и 15 `rednet-meta` модулей.
- Добавлены протоколы сопровождения навыков в `protocols/`: сеансовая активация, сопровождение manifest, активационный диалог, приемка и отключение.
- Добавлен пакет `packages/hermes/rednet-airin-meta-skills/` с `manifest.json` и безопасным `install.ps1`, который по умолчанию работает только в dry-run.
- Добавлен prototype `sensor-prototype/airin-signal-sensor/`: replay JSONL, SQLite, observe-only оценки и рекомендации Guardian без live-действий.
- Добавлен `AGENTS.md` с правилами разработки проекта и `NEXT_START_HERE.md` как точка продолжения.

### Изменено

- `README.md` дополнен навигацией по текущей сборке документации.
- `docs/meta-skills-catalog.md` дополнен ссылкой на архивно выведенную линию мета-навыков и новым безопасным описанием двойной оценки.
- `docs/skills.md` дополнен строкой для `Двойной оценки` как готового к MVP сеансового мета-навыка.
- Репозиторий переведен из чисто документационной витрины в практический installable-пакет с dry-run установкой и тестируемым сенсорным прототипом.

### Безопасность

- Новые документы не включают токены, приватные пути, реальные адреса закрытого контура, сырой чат, PDF-капсулы и восстановимые настройки рабочей среды.
- Live Hermes, Айрин, Алетия, VPN, Tailscale, роутеры, SSH и рабочие сессии не изменялись.

## 2026-06-06

### Добавлено

- Обновлена публичная рамка репозитория `REDNET Airin Skillbook` как практической книги навыков.
- Зафиксированы готовые концепты: контур запуска (`Launch Survival`), нейро-узел сервисов (`Neural Service Node`), сеансовые мета-навыки (`Session-guided meta-skills`), Путь Нави (`Path Navi`).
- Уточнён смысл `Пути Нави`: семантическая регенерация сырой нити после обрыва без галлюцинаторного продолжения и без смешивания с личным дневником.
- Переписаны публичные документы так, чтобы репозиторий читался как инженерная рабочая книга, а не как набор разрозненных заметок.

### Изменено

- Усилена граница приватности: убраны любые намёки на сырой чат, токены, session-файлы, приватные PDF и восстановимые капсулы.
- `README.md` приведён к формату карты репозитория и быстрого входа в документы.
- `docs/architecture.md`, `docs/skills.md`, `docs/research-notes.md`, `docs/privacy-boundary.md`, `docs/roadmap.md` согласованы между собой по терминологии и публичным ограничениям.
- Публичная будущая панель оставлена как кандидат, а не как обещанный готовый стек.

### Проверка

- Выполнен безопасный secret scan по паттернам `token`, `secret`, `password`, `api_key`, `oauth`, `session`, `ghp_`, `sk-`.
- В публично редактируемых документах не должно оставаться секретов и приватных выгрузок.

### Ограничения

- Это документационный релиз, а не изменение рабочей среды.
- Рабочая среда Hermes, сетевой контур и приватные рабочие области не затрагивались.
