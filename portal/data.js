window.REDNET_PORTAL_STATE = {
  generatedAt: "2026-06-09",
  mode: "только чтение",
  project: {
    name: "REDNET Airin Skillbook",
    focus: "Внутренний сайт о проекте, репозитории, мета-навыках, сенсорах и безопасной публикации",
    safety: "Live Hermes, VPN, Tailscale, Ubuntu, EdgeRouter и рабочие сессии не изменяются из портала.",
    publicSurface: "Портал показывает структуру проекта, PWA-режим и границы без секретов, токенов и raw-памяти.",
    tagline: "private-first лаборатория, которую можно читать как красивую карту проекта",
    cta: [
      { label: "README", href: "../README.md" },
      { label: "Документация", href: "../docs/index.md" },
      { label: "Установка dry-run", href: "../INSTALL.md" }
    ]
  },
  repository: {
    title: "Репозиторий Skillbook",
    snapshot: "локальный снимок 2026-06-19",
    trackedFiles: 344,
    statusNote: "рабочее дерево уже содержит незавершённые правки; портал не выполняет commit/push и не трогает live-контуры",
    mission: "Собрать публично-безопасную книгу навыков и протоколов REDNET / Airin: от идеи и схемы до проверяемого пакета установки.",
    layers: [
      { path: "docs/", label: "смысл и навигация", detail: "индекс, архитектура, privacy boundary, release checklist" },
      { path: "skills/", label: "навыки", detail: "установочные SKILL.md и мета-навыки" },
      { path: "protocols/", label: "протоколы", detail: "приёмка, отключение, сопровождение и stop-gates" },
      { path: "packages/", label: "пакеты", detail: "manifest, installer, шаблоны сервисных агентов" },
      { path: "portal/", label: "внутренний сайт", detail: "mobile-first PWA-витрина без live-команд" },
      { path: "schemas/", label: "контракты", detail: "JSON Schema для паспортов и реестров" },
      { path: "research/", label: "лаборатория", detail: "curated summaries и module packs вместо raw inbox" },
      { path: "scripts/", label: "проверки", detail: "валидаторы read-only портала и схем" }
    ],
    entrypoints: [
      { file: "README.md", purpose: "короткий маршрут: что это за проект и как читать" },
      { file: "docs/index.md", purpose: "рольвая навигация для читателя, установщика и ревьюера" },
      { file: "INSTALL.md", purpose: "dry-run установка, apply и rollback" },
      { file: "portal/index.html", purpose: "внутренний сайт и PWA-оболочка" },
      { file: "scripts/validate-portal-readonly.py", purpose: "автопроверка read-only границ" }
    ],
    gates: [
      "нет секретов, токенов, OAuth/Telegram-сессий и cookies",
      "нет raw thread, дневников, runtime-баз и приватных капсул",
      "установщик по умолчанию работает через dry-run",
      "опасные действия отображаются как disabled/guarded",
      "публичный release только после ручного review истории Git"
    ]
  },
  pwa: {
    title: "PWA-версия портала",
    mode: "offline-first shell",
    install: "Открыть портал через http://127.0.0.1:8795/portal/ или HTTPS, затем установить как приложение из браузера.",
    cache: "Service Worker кэширует только локальные файлы портала: HTML, CSS, JS, manifest и иконки.",
    boundary: "PWA не получает сетевых API, не отправляет формы, не хранит секреты и не выполняет команды.",
    files: ["manifest.webmanifest", "sw.js", "icons/icon.svg", "icons/icon-192.png", "icons/icon-512.png", "icons/maskable-512.png"],
    checks: [
      "manifest подключён из index.html",
      "service worker регистрируется только на localhost/HTTPS, не на file://",
      "offline fallback возвращает локальный index.html",
      "иконки 192/512 и maskable доступны",
      "runtime/docker-status.local.js остаётся локальным и игнорируется Git"
    ]
  },
  roadmap: {
    title: "Публичный план Skillbook",
    status: "curated roadmap без raw-выгрузок, ledger exports и приватного корпуса",
    formula: "идея -> публичная формулировка -> навык/протокол/прототип -> проверка -> документация -> release gate",
    phases: [
      "Фаза 0: очистить структуру и убрать raw-выгрузки",
      "Фаза 1: закрепить README, INSTALL, navigation и glossary",
      "Фаза 2: выровнять installable skills и протоколы",
      "Фаза 3: проверить портал как read-only витрину",
      "Фаза 4: провести secret/link/visual review",
      "Фаза 5: вынести release artifacts в release-политику",
      "Фаза 6: открыть public только после ручной проверки истории"
    ],
    tickets: [
      "public_landing",
      "install_guide",
      "privacy_boundary",
      "skill_catalog",
      "portal_visual_review",
      "link_check",
      "secret_scan",
      "release_artifacts_policy"
    ]
  },
  university: {
    title: "API-университет",
    mode: "проектный слой",
    purpose: "пользователь не просто скачивает навык, а проходит активацию: паспорт, границы, пробный сценарий, приемка и выключатель",
    activationFormula: "навык + протокол активации + границы + тест + выключатель + журнал = безопасный модуль",
    layers: [
      { name: "Каталог", output: "карточка выбора", guard: "только очищенные описания" },
      { name: "Паспорт", output: "манифест", guard: "режимы, память, данные, инструменты" },
      { name: "Сеанс", output: "протокол сопровождения", guard: "не менять личность агента" },
      { name: "Полигон", output: "тестовый отчет", guard: "синтетические или очищенные данные" },
      { name: "Приемка", output: "запись приемки", guard: "можно отключить" },
      { name: "Публикация", output: "релизная заметка", guard: "проверка секретов и ручное подтверждение" }
    ],
    checks: [
      "навык имеет выключатель",
      "личная память не переносится между агентами",
      "первый запуск идет в проверочном режиме или наблюдении",
      "результат подтвержден артефактом",
      "публикация проходит проверку приватности"
    ]
  },
  scienceCoordinator: {
    title: "Научный координатор",
    state: "шаблон готовится",
    defaultMode: "наблюдение / помощь",
    role: "организатор научных и сервисных потоков лаборатории",
    style: "собранный, любопытный, теплый, точный",
    flows: [
      { name: "Труды", output: "карточка труда и вопросы" },
      { name: "Концепты", output: "паспорт концепта" },
      { name: "Навыки", output: "черновик или пакет установки" },
      { name: "Сервисы", output: "статус и план обслуживания" },
      { name: "Сабагенты", output: "отчет приемки" },
      { name: "Публикация", output: "очищенный релиз" },
      { name: "Инциденты", output: "карта причин и паттернов" }
    ],
    artifacts: [
      "карточка задачи",
      "карточка труда",
      "карточка концепта",
      "отчет проверки",
      "карта модулей",
      "пакет передачи",
      "релизная заметка"
    ],
    blocked: [
      "чужая личная память",
      "сырые нити и капсулы",
      "живые команды",
      "скрытые публикации",
      "изменение сети без окна"
    ]
  },
  metaSkills: {
    title: "Мета-навыки координатора",
    mode: "только чтение / рекомендации",
    package: "packages/hermes/rednet-airin-meta-skills/manifest.json",
    map: "docs/science-coordinator-meta-skill-map.md",
    count: 18,
    groups: [
      { name: "Приемка и польза", skills: "rednet-criteria-layer, rednet-utility-evaluator", output: "критерии готовности" },
      { name: "Неопределенность", skills: "rednet-uncertainty-register, rednet-double-evaluation", output: "факты отдельно от гипотез" },
      { name: "Сбор навыков", skills: "rednet-skill-collector, rednet-research-protocol", output: "черновик или пакет" },
      { name: "Процесс", skills: "rednet-process-observer, rednet-unfinished-memory", output: "task-ledger и handoff" },
      { name: "Публикация", skills: "rednet-public-editor, rednet-decision-memory", output: "очищенный релиз" }
    ],
    guards: [
      "не автозагружать навыки в live Hermes",
      "не переносить личную память между агентами",
      "не выдавать гипотезу за доказанный результат",
      "каждый вывод возвращать как проверяемый артефакт"
    ]
  },
  hermesNextGen: {
    title: "Следующее поколение Hermes",
    mode: "наблюдение / проектирование",
    purpose: "сделать возможности Hermes видимыми: профили, память, перехватчики, модули, фоновые задачи, шлюз платформ и стоп-границы",
    principle: "Hermes остается агентом и шлюзом, REDNET добавляет режимы, диагностику, упаковку, безопасность и полигон.",
    layers: [
      { name: "Паспорт профиля", status: "схема", output: "границы памяти, платформы, маршрут модели, пакеты навыков", guard: "только проверочный импорт" },
      { name: "Реестр перехватчиков", status: "схема", output: "событие, режимы, обработчик, риск, выключатель, журнал", guard: "двойная подпись перед запуском" },
      { name: "Карта модулей", status: "схема", output: "чтение, запись, сеть, публикация, аккаунт, командная оболочка", guard: "список допуска и окно обслуживания" },
      { name: "Фоновые задачи", status: "модель", output: "режим, артефакт, дедлайн, политика занятости", guard: "не выдавать молчание за работу" },
      { name: "Продвижение памяти", status: "модель", output: "кандидат, проверка, ручное принятие", guard: "без автосмешивания памяти" },
      { name: "Предохранитель платформ", status: "модель", output: "пауза адаптера без полного рестарта", guard: "ручное восстановление" }
    ],
    priorities: [
      { level: "P0", item: "единый статус шлюза, платформ, модели, OAuth, Telegram, сети, очереди и предохранителя" },
      { level: "P0", item: "экспорт диагностики для технического ревьюера без секретов" },
      { level: "P1", item: "просмотр профилей, реестр перехватчиков/модулей и карточки фоновых задач" },
      { level: "P1", item: "локальный резервный чат и защитный контур публикации" },
      { level: "P2", item: "конструктор профиля, API-университет, симулятор отказов и наблюдаемость" }
    ],
    examples: [
      "examples/hermes-next-gen/profile-passport.example.json",
      "examples/hermes-next-gen/hook-registry.example.json",
      "examples/hermes-next-gen/plugin-capabilities.example.json"
    ],
    artifactViewer: {
      title: "Проверяемые артефакты",
      mode: "только чтение",
      scope: "Портал показывает только публичные схемы и учебные examples из репозитория. Живые настройки, portal/runtime, сессии, токены, дневники и сырые нити не читаются.",
      validationCommand: "python scripts\\validate-rednet-schemas.py",
      schemas: [
        { name: "Паспорт навыка", file: "schemas/skill-passport.schema.json", proves: "единая форма навыка, режимы, риски, выключатель и приемка" },
        { name: "Паспорт агента", file: "schemas/agent-passport.schema.json", proves: "границы личности, памяти, автономии и допустимых каналов агента" },
        { name: "Научный поток", file: "schemas/science-flow.schema.json", proves: "задачи научного координатора, статусы и обязательные артефакты" },
        { name: "Профиль Hermes", file: "schemas/hermes-profile-passport.schema.json", proves: "границы профиля, провайдер модели, память и пакеты навыков" },
        { name: "Реестр перехватчиков", file: "schemas/hook-registry.schema.json", proves: "событие, режимы, обработчик, риск, выключатель и журнал" },
        { name: "Карта модулей", file: "schemas/plugin-capability.schema.json", proves: "возможности модуля, доступы, режимы и стоп-границы" }
      ],
      examples: [
        { name: "Паспорт профиля Hermes", file: "examples/hermes-next-gen/profile-passport.example.json", schema: "schemas/hermes-profile-passport.schema.json", status: "валидируется" },
        { name: "Реестр перехватчиков", file: "examples/hermes-next-gen/hook-registry.example.json", schema: "schemas/hook-registry.schema.json", status: "валидируется" },
        { name: "Карта возможностей модулей", file: "examples/hermes-next-gen/plugin-capabilities.example.json", schema: "schemas/plugin-capability.schema.json", status: "валидируется" },
        { name: "Журнал задач научного координатора", file: "packages/agents/rednet-science-coordinator/examples/task-ledger.example.jsonl", schema: "schemas/science-flow.schema.json", status: "валидируется построчно" }
      ]
    },
    checks: [
      "профиль не получает чужую память",
      "перехватчик не активен без режима и окна обслуживания",
      "модуль описывает все возможности до установки",
      "длинная задача возвращает артефакт",
      "публикация идет только после проверки приватности"
    ]
  },
  agents: [
    {
      id: "core-research",
      publicLabel: "Контур 1",
      role: "главный исследовательский центр",
      mode: "Лаборатория / Наблюдение",
      state: "недоступен",
      availability: "offline",
      boundary: {
        namespace: "rednet:core-research",
        memory: "только свой контур",
        container: "не публикуется",
        network: "окно обслуживания",
        actionAllowed: false
      },
      autonomy: "цельная агентная работа, без смешивания с другими профилями",
      allowed: ["мета-навыки", "исследования", "Skillbook", "сенсоры наблюдения", "черновики внешних материалов"],
      blocked: ["автопубликация без подтверждения", "перенос личной памяти другим контурам", "живые действия без окна обслуживания"]
    },
    {
      id: "coordination",
      publicLabel: "Контур 2",
      role: "координатор разработки",
      mode: "Лаборатория / Публикация",
      state: "недоступен",
      availability: "offline",
      boundary: {
        namespace: "rednet:coordination",
        memory: "сводки и отчеты",
        container: "Codex-среда",
        network: "без живых команд",
        actionAllowed: false
      },
      autonomy: "управление разработкой, сверка целостности, интеграция результатов",
      allowed: ["документация", "проверки", "сабагенты", "релизный контур", "сводные отчеты"],
      blocked: ["смешивание ролей с главным контуром", "публикация секретов", "скрытые живые команды"]
    },
    {
      id: "personal-assistant",
      publicLabel: "Личный помощник",
      role: "изолированный помощник",
      mode: "Тихий помощник",
      state: "доступен",
      availability: "online",
      boundary: {
        namespace: "rednet:personal-assistant",
        memory: "изолированная личная память",
        container: "отдельный Docker",
        network: "тихий контур",
        actionAllowed: false
      },
      autonomy: "помощь для общения, наблюдение для инфраструктуры",
      allowed: ["личная помощь", "документы", "планирование", "мягкие напоминания", "личный стиль"],
      blocked: ["участие в общей лаборатории без задачи", "чужие сессии", "чужие дневники", "общая память других контуров"]
    },
    {
      id: "prepared-agent",
      publicLabel: "Резервный агент",
      role: "подготовленный контур",
      mode: "Наблюдение / Тихий помощник",
      state: "доступен",
      availability: "online",
      boundary: {
        namespace: "rednet:prepared-agent",
        memory: "только подготовленный пакет",
        container: "отдельный контур",
        network: "наблюдение",
        actionAllowed: false
      },
      autonomy: "готов к отдельной настройке после стабилизации модели",
      allowed: ["проверка без команд", "черновые задачи", "сервисная помощь"],
      blocked: ["вмешательство в лабораторию", "публикация", "перенос личной памяти"]
    }
  ],
  modes: [
    { name: "Дом", purpose: "обычное теплое общение", allowed: "мягкая память, беседа, помощь", blocked: "рискованные действия" },
    { name: "Лаборатория", purpose: "исследования", allowed: "сабагенты, гипотезы, протоколы", blocked: "живые изменения без окна" },
    { name: "Сервер", purpose: "инфраструктура", allowed: "диагностика, отчеты, проверочный запуск", blocked: "рестарты без окна" },
    { name: "Наблюдение", purpose: "мониторинг", allowed: "сенсоры, Guardian в режиме наблюдения", blocked: "маршруты, firewall, изменения VPN" },
    { name: "Инцидент", purpose: "сбой связи/API/агента", allowed: "hold, локальный чат, закрытая локальная сводка", blocked: "хаотичные рестарты" },
    { name: "Публикация", purpose: "GitHub, NAS, внешние каналы", allowed: "secret scan, черновики, отчеты", blocked: "приватные данные" },
    { name: "Тихий помощник", purpose: "Марсель", allowed: "личная помощь по правилам", blocked: "вмешательство в лабораторию" }
  ],
  concepts: [
    { name: "Insight Lattice", maturity: "план", modes: "наблюдение / анализ", output: "кандидат инсайта" },
    { name: "Путь Нави", maturity: "практика", modes: "восстановление / сеанс", output: "семантический хвост нити" },
    { name: "Перерождение", maturity: "практика", modes: "инцидент / удержание", output: "передача состояния и восстановление" },
    { name: "Совет Гениев", maturity: "проектная рамка", modes: "анализ", output: "матрицы и синтез" },
    { name: "Двойная оценка", maturity: "MVP+", modes: "наблюдение / сервис / отклик", output: "сверка первого и второго анализа" },
    { name: "Нано-узлы", maturity: "этап 1", modes: "наблюдение / рекомендация", output: "сигнал, уверенность, рекомендация" },
    { name: "Пассивный сенсор", maturity: "прототип", modes: "наблюдение", output: "SQLite: события, признаки, оценки" },
    { name: "Бустер памяти", maturity: "исследование", modes: "наблюдение / анализ", output: "поиск и карта памяти" },
    { name: "Сеансовое сопровождение", maturity: "протокол", modes: "сеанс / удержание", output: "ритм раскрытия навыка" },
    { name: "Режимная автономия", maturity: "план", modes: "выкл / наблюдение / помощь / ведение", output: "уровень самостоятельности" },
    { name: "API-университет", maturity: "модель", modes: "активация / полигон / приемка", output: "паспорт и запись приемки" },
    { name: "Научный координатор", maturity: "шаблон", modes: "наблюдение / помощь / ведение", output: "потоки, артефакты, приемка сабагентов" },
    { name: "Следующее поколение Hermes", maturity: "карта + схемы", modes: "профили / перехватчики / модули / фоновые задачи", output: "реестры и правила приемки" }
  ],
  channels: [
    {
      name: "ВК",
      mode: "сначала черновик",
      purpose: "внешнее выражение работы основного агента: заметки, карточки навыков, дневники разработки, короткие отчеты",
      publishGate: "ручное подтверждение оператора перед публикацией",
      blocked: "личные данные, ключи, сырая нить, внутренние маршруты, приватные диалоги"
    },
    {
      name: "Google",
      mode: "сначала черновик",
      purpose: "документы, таблицы, календарные планы, исследовательские витрины и рабочие подборки",
      publishGate: "ручное подтверждение оператора и проверка доступа",
      blocked: "секреты, OAuth blobs, приватные капсулы, семейные обстоятельства, закрытые базы"
    },
    {
      name: "GitHub",
      mode: "через релизный контроль",
      purpose: "очищенный Skillbook, прототипы, документация и релизные заметки",
      publishGate: "secret scan, UTF-8, zip/SHA, cycle-close",
      blocked: "внутренние рабочие деревья целиком, живые конфиги, NAS-пути, токены"
    }
  ],
  triad: {
    title: "Канал троих",
    mode: "сначала журнал",
    purpose: "общий журнал задач, решений и handoff-пакетов для оператора, основного агентного контура и Codex-координатора",
    storage: "приватный локальный triad-ledger.jsonl вне публичного Skillbook",
    portalMode: "статус без команд",
    statuses: ["открыто", "взято", "черновик", "нужна проверка", "принято", "заблокировано", "закрыто"],
    guards: [
      "секреты и сырая нить запрещены",
      "живые действия только через окно обслуживания",
      "внешние каналы получают черновики",
      "каждый пакет имеет роль, режим, приватность, статус и срок жизни"
    ]
  },
  admin: {
    title: "Админка",
    mode: "монитор без команд",
    purpose: "локальная панель наблюдения за Docker-агентами, сетевыми слоями и готовностью сервисов без живых команд",
    generatedBy: "scripts/export-docker-status.ps1",
    dockerAgents: [
      {
        label: "Личный помощник",
        runtime: "docker",
        service: "rednet-personal-assistant",
        status: "online",
        mode: "помощь / наблюдение",
        endpoint: "internal",
        composeProject: "изолированный",
        network: "отдельная сеть",
        volumes: "отдельные тома",
        restartPolicy: "unless-stopped",
        actionAllowed: false,
        guard: "изолированная память, без лабораторных действий"
      },
      {
        label: "Научный координатор",
        runtime: "docker",
        service: "rednet-science-coordinator",
        status: "planned",
        mode: "лабораторная координация / наблюдение",
        endpoint: "internal",
        composeProject: "шаблон",
        network: "отдельная сеть",
        volumes: "отдельные тома",
        restartPolicy: "только после приемки",
        actionAllowed: false,
        guard: "Qwen-контур без публикации ключей"
      },
      {
        label: "Qwen-шлюз",
        runtime: "docker",
        service: "model-proxy-example",
        status: "planned",
        mode: "приватный модельный шлюз",
        endpoint: "internal",
        composeProject: "приватный",
        network: "внутренний шлюз",
        volumes: "секреты вне Git",
        restartPolicy: "ручное окно",
        actionAllowed: false,
        guard: "не публиковать tokens/session/cookies"
      }
    ],
    networkLayers: [
      {
        name: "Tailscale",
        status: "active",
        mode: "доверенный транспорт",
        guard: "без смены маршрутов из портала"
      },
      {
        name: "Outline/VPN",
        status: "manual",
        mode: "только окно обслуживания",
        guard: "не переключать активный API/Telegram маршрут без подтверждения"
      },
      {
        name: "VLESS",
        status: "planned",
        mode: "проверка конфигурации / ручное окно",
        guard: "только подготовка профилей, проверка и рекомендации"
      },
      {
        name: "Passive Sensor",
        status: "observe",
        mode: "Replay/SQLite наблюдение",
        guard: "без payload, firewall и packet path"
      }
    ],
    buttons: [
      { title: "Обновить статус", state: "safe", action: "обновление статуса без команд" },
      { title: "Экспорт Docker-статуса", state: "safe", action: "создать локальный статус выполнения" },
      { title: "Проверить VLESS-профили", state: "guarded", action: "проверка профилей без подключения" },
      { title: "Перезапуск агента", state: "disabled", action: "только через окно обслуживания" },
      { title: "Смена маршрута", state: "disabled", action: "запрещено из портала" }
    ]
  },
  subagents: [
    { role: "Архитектор", output: "карта целостности и границы", guard: "не смешивать агентов" },
    { role: "Исследователь", output: "карточки концептов и зрелость", guard: "не выдавать гипотезу за модуль" },
    { role: "Инженер", output: "прототип, пакет, проверочный запуск", guard: "не трогать живой контур без окна" },
    { role: "Сетевой эксперт", output: "сенсорные сигналы и риски", guard: "только наблюдение по умолчанию" },
    { role: "QA/Безопасность", output: "checklist и secret scan", guard: "никаких секретов в публикации" },
    { role: "Редактор", output: "витрина и понятная документация", guard: "не мистифицировать технические статусы" }
  ],
  checks: [
    "Hermes Desktop не запускается",
    "опасные кнопки портала отключены",
    "секреты и токены не включены",
    "личный помощник не использует память других контуров",
    "ВК и Google работают сначала как черновики",
    "Docker-монитор работает как админка без команд",
    "VLESS поддерживается как отключаемый слой ручного окна и проверки конфигурации",
    "сенсоры и нано-узлы остаются в режиме только наблюдения",
    "научный координатор видит meta-skill toolkit как read-only рекомендации",
    "Skillbook отделен от приватной рабочей среды"
  ]
};
