# Локальный портал REDNET

![Превью портала](../assets/portal-preview.svg)

`portal/` — статический read-only портал и PWA-оболочка для обзора Skillbook: структура репозитория, контуры, лаборатория, API-университет, Hermes next-gen, установка, проверки и stop-gates.

Портал — не панель live-управления. Он не запускает процессы, не рестартует агентов, не меняет сеть и не публикует материалы наружу.

## Запуск и PWA

Открыть файл напрямую можно, но PWA-функции (`manifest`, service worker, offline cache, установка на экран) работают только через `localhost` или HTTPS:

```text
portal/index.html
```

Или поднять локальный сервер из корня репозитория:

```powershell
python -m http.server 8795
```

Затем открыть:

```text
http://127.0.0.1:8795/portal/
```

После открытия через `localhost` браузер сможет предложить установку PWA. Оболочка состоит из:

- `manifest.webmanifest` — имя, цвета, standalone-режим, shortcuts и иконки;
- `sw.js` — offline-first кэш только локальных файлов портала;
- `icons/` — SVG/PNG и maskable-иконка приложения.

Опциональный локальный runtime-статус Docker подключается только явно через query-параметр:

```text
http://127.0.0.1:8795/portal/?runtime=local#admin
```

Файл `portal/runtime/docker-status.local.js` остаётся локальным и игнорируется Git.

## Вкладки

| Вкладка | Что показывает | Режим |
|---|---|---|
| Обзор | Назначение Skillbook, внутренний hero, статус PWA и быстрые входы. | read-only |
| Репозиторий | Слои, точки входа, gates и снимок структуры. | read-only |
| PWA | Manifest, service worker, offline cache, иконки и acceptance. | offline-first/read-only |
| Контуры | Роли, разрешения, запреты, границы памяти. | read-only |
| Лаборатория | Концепты, зрелость, выходы. | read-only |
| Университет | Модель активации навыков и агентов. | read-only |
| Hermes | Схемы профилей, hooks, plugins, фоновые задачи. | read-only |
| План | Публичная roadmap-сводка без private slices. | read-only |
| Каналы | Draft-first внешние каналы. | draft-first |
| Канал троих | Handoff/ledger как статусная модель без raw private ledger. | read-only |
| Сервер | Обобщённая инфраструктурная карта без команд. | read-only |
| Админка | Локальный Docker-status preview; live-команды выключены. | read-only |
| Skillbook | Карта skills/protocols/packages. | read-only |
| Сотрудники | Роли сабагентов и ожидаемые артефакты. | read-only |
| Проверки | Acceptance checklist. | read-only |

## Границы

- Портал не запускает Hermes Desktop.
- Портал не меняет VPN, Tailscale, Docker, Ubuntu, NAS, роутеры или рабочие сессии.
- Все опасные действия отображаются только как заблокированные или требующие окна обслуживания.
- В портал не добавляются токены, ключи, OAuth/Telegram-сессии, raw thread, дневники, runtime-базы и приватные капсулы.
- Runtime-файл `portal/runtime/docker-status.local.js` локален, игнорируется Git и подключается только при `?runtime=local`.
- PWA service worker кэширует только локальные файлы портала и не является каналом live-управления.

## Проверка

```powershell
python scripts\validate-portal-readonly.py
```

После визуальных правок портал нужно открыть глазами и сверить, что нет приватных данных, битых вкладок и live-кнопок.
