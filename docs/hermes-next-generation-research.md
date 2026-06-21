# Следующее поколение клиента Hermes для REDNET

Документ фиксирует исследовательскую рамку для развития REDNET Control Center и портала вокруг Hermes Agent. Он не является инструкцией к немедленному изменению live-среды.

## Краткий вывод

Hermes силен как агентная оболочка с gateway, профилями, memory providers, hooks, plugins, skills и фоновыми задачами. Его не нужно "переписывать". REDNET должен стать вторым слоем: профессиональная панель режимов, диагностики, публикации, упаковки навыков, сервисного восстановления и научной координации.

Главная идея следующего поколения:

```text
Hermes = агент и gateway
REDNET = режимы, безопасность, диагностика, портал, skillbook, научная лаборатория, восстановление и упаковка
```

Такой подход дает максимум пользы и минимальный риск: мы не вмешиваемся в живой Hermes без окна обслуживания, но получаем управляемую систему вокруг него.

## Проверенные опорные факты

По официальной документации Hermes gateway является единым фоновым процессом: он подключает платформы, держит сессии, запускает cron и доставляет голосовые сообщения. В той же модели платформенные адаптеры направляют сообщения через per-chat session store к агенту, а планировщик gateway тикает примерно раз в минуту.

Документация также подтверждает полезные для REDNET элементы:

- Telegram и другие платформы поддерживают typing/streaming, файлы, изображения и разные уровни возможностей.
- Внутри чатов есть команды `/status`, `/background`, `/model`, `/platform`, `/sethome`, `/compress`, `/voice`, `/busy`, `/codex-runtime`.
- `/background` создает независимую фоновую сессию, а текущий чат остается свободным.
- `/busy queue|steer|interrupt` позволяет выбирать, что делать с сообщениями во время занятости агента.
- `/platform pause/resume/list` и circuit breaker позволяют останавливать конкретный адаптер без полного рестарта gateway.
- `/codex-runtime` может переключать OpenAI/Codex модели на app-server runtime в следующей сессии.
- Для локального слоя Ollama можно подключать Hermes к OpenAI-совместимому endpoint `http://127.0.0.1:11434/v1`; локальные модели требуют заметных ресурсов, поэтому в REDNET они должны быть сервисными, а не основным мозгом.
- Официальный слой features описывает skills, memory providers, hooks, plugins, profiles и provider routing как штатные точки расширения.
- Profiles дают изолированные рабочие режимы агента, а profile distributions позволяют распространять заранее подготовленные наборы конфигурации.
- Hooks полезны как событийный слой вокруг tool calls и workflow, но в REDNET они должны проходить через guard и журнал.
- Memory providers дают разные варианты памяти, но публичный Skillbook не должен содержать живые базы, сессии или переносимую личную память.

Источники:

- Hermes Messaging Gateway: https://hermes-agent.nousresearch.com/docs/user-guide/messaging
- Hermes Slash Commands Reference: https://hermes-agent.nousresearch.com/docs/reference/slash-commands
- Hermes Features Overview: https://hermes-agent.nousresearch.com/docs/user-guide/features/overview
- Hermes Memory Providers: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory
- Hermes Hooks: https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks
- Hermes Plugins: https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins
- Hermes Profiles: https://hermes-agent.nousresearch.com/docs/user-guide/features/profiles
- Ollama Hermes integration: https://docs.ollama.com/integrations/hermes

## Что это значит для REDNET

Наша стратегия не должна конкурировать с Hermes gateway. REDNET Control Center должен стать внешней профессиональной панелью наблюдения, пакетирования и осторожного сопровождения:

- показывать состояние gateway, платформ, OAuth, Telegram, прокси, Docker-агентов и сенсоров;
- не нажимать опасные кнопки без окна обслуживания;
- использовать штатные концепты Hermes: фоновые задачи, platform pause/resume, circuit breaker, busy queue/steer;
- дополнять Hermes своими слоями: Guardian, Путь Нави, Перерождение, локальный чат, нано-сенсор, Skillbook, cycle-close.

## Что в Hermes реализовано неидеально для нашей модели

Это не список претензий к Hermes, а карта мест, где REDNET добавляет инженерную ценность.

| Зона | Симптом | REDNET-решение |
|---|---|---|
| Визуальный статус | пользователь видит "не отвечает", но не понимает слой сбоя | карта: Telegram, gateway, модель, OAuth, сеть, очередь, breaker |
| Рестарты | легко начать хаотично перезапускать все подряд | режим обслуживания, stop gate, журнал действий |
| Профили | профили мощные, но пользователю трудно держать границы | паспорт профиля, namespace, память, разрешенные режимы |
| Память | разные memory providers могут смешать смысловые контуры | memory boundary и promotion candidate вместо автосмешивания |
| Hooks | могут стать скрытым источником поведения | реестр hooks, dry-run, audit log, выключатель |
| Plugins | полезны, но могут тащить лишние права | install manifest, capability map, allowlist |
| Messaging | Telegram/платформы деградируют не одинаково | platform breaker card и локальный fallback |
| Busy state | длинная задача выглядит как зависание | queue/steer/interrupt политика и потоковый статус |
| Background | фоновые задачи полезны, но требуют контроля | task ledger, лимиты, отчет завершения |
| Local models | соблазн сделать локальную LLM главным мозгом | только сервисный медленный путь: triage, классификация, объяснение |

## Наблюдения сообщества и практические боли

По обсуждениям вокруг Hermes и типичным open-source agent UX повторяются темы:

- людям нравится идея подключить Hermes к Telegram/Matrix/чатам, но они быстро сталкиваются с вопросами надежности, очередей и понятного статуса;
- "магический агент" без видимого состояния пугает: нужно показывать, что он делает, где занят и какой слой деградировал;
- профильность и плагины сильны, но без внешней панели легко потерять, какой профиль что читает и какие инструменты имеет;
- локальные модели полезны как приватный слой, но у маленьких моделей ограничена способность вести длинный исследовательский диалог;
- долгие tool calls и background work требуют отдельного UX, иначе пользователь считает систему зависшей.

Для REDNET это означает: следующий клиент должен быть не "красивее", а наблюдаемее, объяснимее и безопаснее.

## Приоритеты развития клиента

1. **Панель состояния без команд**
   - текущий gateway;
   - платформы;
   - model/provider;
   - OAuth/Codex;
   - Telegram proxy;
   - Docker-агенты;
   - сетевые слои Tailscale, Outline, VLESS;
   - сенсоры и нано-узлы.

2. **Управление режимами**
   - Дом;
   - Лаборатория;
   - Сервер;
   - Наблюдение;
   - Инцидент;
   - Публикация;
   - Тихий помощник.

3. **Безопасная работа с занятостью**
   - по умолчанию `queue` для длинных задач;
   - `steer` для мягкого уточнения без разрушения текущего хода;
   - `interrupt` только вручную;
   - очередь Telegram/фоновых задач до 100 как слой компенсации.

4. **Платформенные circuit breaker-карточки**
   - состояние платформы;
   - причина паузы;
   - последняя ошибка;
   - ручная рекомендация;
   - кнопка resume только в окне обслуживания.

5. **Сервисное восстановление**
   - локальный чат, когда Telegram деградирует;
   - семантический хвост Путь Нави;
   - session resume после restart_interrupted;
   - запрет хаотичных рестартов.

6. **Модельный слой**
   - основной Codex/OAuth контур не заменяется;
   - Qwen/локальные модели используются как приватные сервисные координаторы, классификаторы, объяснители и нано-узлы;
   - все ключи идут через окружение, а не в Skillbook.

7. **Профили и дистрибутивы**
   - для каждого агента: отдельный profile namespace;
   - manifest профиля: memory, tools, platforms, model route, privacy;
   - экспорт только очищенного profile package;
   - импорт только через dry-run и diff.

8. **Реестр hooks и plugins**
   - показывать каждый hook: событие, команда, риск, режим, журнал;
   - показывать plugin capabilities: чтение, запись, сеть, публикация, файлы;
   - запрещать скрытые hooks без карточки и выключателя.

9. **Сабагенты как научные сотрудники**
   - статус не "агент работает", а роль, вход, ожидаемый артефакт, дедлайн;
   - приемка результата: файл/карточка/тест/список рисков;
   - регистр провалов делегации, чтобы не делать вид, что сабагент помог.

10. **Портал API-университета**
    - каталог навыков;
    - прохождение активации;
    - проверка границ;
    - тестовый профиль;
    - пакет установки;
    - отчет о совместимости.

## Хитрые подходы

- Не делать “супер-кнопку починить все”. Вместо этого показывать диагноз, рекомендованный порядок и степень риска.
- Любой сетевой слой оформлять как модуль с режимами `off/observe/config-test/manual-window/incident-hold`.
- Для Telegram не только проверять Bot API, но и различать прием сообщений, отправку, model call, delivery, platform breaker и пользовательскую allowlist.
- Для OAuth отдельно показывать transport health, provider auth и model-runtime, потому что каждый слой может ломаться независимо.
- Для Docker-агентов показывать только статус и guard, пока нет отдельного окна обслуживания.
- Для VLESS в MVP проверять только профили и конфигурацию, не включать маршруты.
- Для локальных моделей использовать “медленный путь”: объяснение, классификация, triage, а не packet path и не живое управление.
- Для hooks использовать "двойную подпись": hook может быть установлен, но не активен, пока manifest и режим не совпали.
- Для memory promotion использовать candidate records: сначала кандидат, затем review, затем ручное принятие.
- Для профилей использовать "карантин импорта": новый профиль сначала открывается как read-only diff.
- Для Telegram использовать независимые проверки: polling/webhook, send, receive, queue, model call, delivery.
- Для длительных задач показывать "живую телеметрию мысли" без раскрытия приватных chain-of-thought: этап, инструмент, ожидание, следующая проверка.

## Архитектура следующего поколения

```text
Пользователь
  -> Портал REDNET / Control Center
    -> режимный шлюз
      -> статус Hermes gateway
      -> профили и память
      -> платформы Telegram/Matrix/Webhook
      -> очередь и background
      -> hooks/plugins registry
      -> Docker agents monitor
      -> сенсоры observe-only
      -> публикационный контур
```

Важный принцип: портал и Control Center не становятся главным runtime. Они дают наблюдение, упаковку, диагностику, рекомендации и безопасный запуск через подтвержденное окно.

## Модель агентного клиента

Каждый агент получает паспорт:

```yaml
agent_id: string
profile_namespace: string
role: research|coordination|personal|service
mode: home|lab|server|observe|incident|publish|quiet-assistant
memory_boundary: own|shared-readonly|forbidden
platforms: []
model_route: primary|service|local-aux
allowed_tools: []
forbidden_tools: []
hooks: []
plugins: []
publish_gate: manual
live_actions: false
```

Такой паспорт делает Hermes-профили переносимыми и безопасными для будущих помощников по нишам.

## Что доработать в Control Center

P0:

- единый статусный экран: gateway, platforms, model, OAuth, Telegram, network, queue, breaker;
- экспорт диагностики для Алетии без секретов;
- запрет на live-кнопки вне окна обслуживания;
- VLESS/Outline/Tailscale как `off/observe/config-test/manual-window`;
- карта Docker-агентов: статус, режим, память, сеть, тома, restart policy.

P1:

- просмотр Hermes profiles и profile diff;
- registry hooks/plugins;
- карточки busy/background задач;
- локальный чат fallback;
- публикационный guard для GitHub/VK/Google;
- UI для installable skills: dry-run, diff, apply только вручную.

P2:

- визуальный конструктор профиля агента;
- API-университет активации навыка;
- test harness для агента;
- симулятор отказов Telegram/OAuth/network;
- наблюдаемость по OpenTelemetry/Phoenix/LangSmith-совместимой модели без утечки приватного текста.

## Что доработать в Hermes-пакете навыков

- у каждого навыка должен быть `SKILL.md`, `manifest`, `disable`, `test`, `privacy`;
- мета-навыки должны иметь "сеансовое сопровождение", а не только описание;
- навыки должны указывать, меняют ли они память, тон, маршрутизацию, публикацию, инструменты;
- каждый skill package должен быть пригоден для dry-run импорта;
- каждый skill должен иметь maturity: `draft`, `observe`, `mvp`, `stable`, `experimental`, `dangerous-disabled`.

## Модель рисков

| Риск | Причина | Защита |
|---|---|---|
| Смешивание личностей | перенос памяти/профиля | namespace и запрет cross-agent promotion |
| Скрытые действия | hooks/plugins без карты | registry + mode gate |
| Потеря связи | Telegram/OAuth/network деградация | local chat + queue + Path Navi |
| Хаотичное восстановление | многократные рестарты | incident mode + action ledger |
| Утечка секретов | публикация сырого пакета | secret scan + public/private boundary |
| Ложная автономия | маленькая LLM принимает решения | service-only route + Guardian |
| Слом live-сервиса | кнопки без окна | disabled actions + maintenance window |

## Следующая практическая итерация

- встроить в Control Center карту `/platform list` и circuit breaker-состояний;
- добавить карточку `/busy` режима gateway;
- сделать экспорт “пакет диагностики для Алетии” с отдельными блоками: сеть, OAuth, Telegram, Docker, сенсоры, Skillbook;
- добавить read-only Docker monitor в портал;
- синхронизировать портал и Control Center по одинаковым режимам и статусам;
- вынести live-действия в отдельный “режим обслуживания” с журналом и подтверждением.
- подготовить `profile-passport.schema.json`;
- подготовить `hook-registry.example.json`;
- подготовить UX-карточку API-университета: выбрать навык -> пройти активацию -> проверить границы -> получить пакет.

Практическое продолжение этой карты вынесено в `docs/hermes-next-gen-registries.md`: там зафиксированы паспорт Hermes-профиля, реестр hooks, карта возможностей plugins и безопасные examples для будущей страницы портала.
