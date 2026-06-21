<div align="center">

<a href="docs/index.md">
  <img src="assets/airin-skillbook-hero.svg" alt="REDNET Airin Skillbook — публично-безопасная книга навыков" width="920">
</a>

# REDNET Airin Skillbook

**Быстрые навыки. Тихие протоколы. Read-only портал. Публичная витрина без приватной истории.**

[Документация](docs/index.md) · [Установка](INSTALL.md) · [Навыки](docs/skills.md) · [Портал](portal/README.md) · [Граница приватности](docs/privacy-boundary.md)

[![режим](https://img.shields.io/badge/mode-public--safe%20snapshot-7fd7ff)](#статус)
[![установка](https://img.shields.io/badge/install-dry--run%20by%20default-99f6c8)](INSTALL.md)
[![портал](https://img.shields.io/badge/portal-read--only-ffd166)](portal/README.md)
[![секреты](https://img.shields.io/badge/secrets-not%20included-f87171)](docs/privacy-boundary.md)
[![язык](https://img.shields.io/badge/docs-ru-8ee8ff)](docs/index.md)

</div>

> **Коротко:** это не дамп рабочей среды и не дневник разработки. Это аккуратная GitHub-витрина REDNET / Airin: установочные `SKILL.md`, протоколы, схемы, read-only портал и проверяемые прототипы, которые можно изучать без доступа к приватному контуру.

## Содержание

- [Что это?](#что-это)
- [Скриншоты и визуальная витрина](#скриншоты-и-визуальная-витрина)
- [Возможности](#возможности)
- [Быстрый старт](#быстрый-старт)
- [Важные ссылки](#важные-ссылки)
- [Что внутри](#что-внутри)
- [Главные навыки](#главные-навыки)
- [Граница публикации](#граница-публикации)
- [Проверка перед релизом](#проверка-перед-релизом)
- [Статус](#статус)

## Что это?

**REDNET Airin Skillbook** — публично-безопасная книга навыков для агентных контуров REDNET / Airin. Репозиторий показывает идею, модули, правила установки, безопасные stop-gates и визуальную карту проекта, но не раскрывает токены, raw-память, приватные сессии или live-инфраструктуру.

Формат вдохновлён витринами dev-tool репозиториев: сверху — сильный hero, дальше — быстрые ссылки, честные бейджи, скриншоты, короткие benefits, затем установка и подробная карта.

## Скриншоты и визуальная витрина

| Read-only портал | Безопасный dry-run | Карта Skillbook |
|---|---|---|
| <img src="assets/screenshots/portal-home.png" alt="Скриншот read-only портала REDNET Airin Skillbook" width="360"> | <img src="assets/screenshots/dry-run-terminal.png" alt="Санитизированный dry-run terminal preview" width="360"> | <img src="assets/skillbook-map.svg" alt="Карта REDNET Airin Skillbook" width="360"> |
| [Открыть инструкцию портала](portal/README.md) | [Открыть установку](INSTALL.md) | [Открыть навигацию](docs/navigation.md) |

![Безопасный поток установки](assets/install-flow.svg)

## Возможности

- **Dry-run first:** установщик сначала показывает, что будет скопировано, и ничего не меняет без явного `-Apply`.
- **Read-only портал:** статическая PWA-витрина в `portal/` показывает структуру проекта, но не выполняет live-команды.
- **Публичная граница:** документы фиксируют, что можно публиковать, а что остаётся только в приватном контуре.
- **Модульные навыки:** skill-папки можно установить, отключить, перенести, проверить и удалить без структурного вреда.
- **Протоколы приёмки:** есть чеклисты release/privacy/install, чтобы не превращать витрину в небезопасный дамп.
- **Визуальная документация:** схемы и скриншоты лежат в `assets/` и проходят правило “без секретов и приватных путей”.

## Быстрый старт

### 1. Прочитать маршрут

Начни с [docs/index.md](docs/index.md): там есть роли читателя, установщика, ревьюера безопасности и контрибьютора.

### 2. Проверить установку без изменений

```powershell
powershell -ExecutionPolicy Bypass -File packages\hermes\rednet-airin-meta-skills\install.ps1 -DryRun
```

`-DryRun` — безопасный режим: он показывает будущие операции и не копирует файлы. Реальная установка описана отдельно в [INSTALL.md](INSTALL.md) и должна выполняться только после review.

### 3. Посмотреть портал локально

```powershell
python -m http.server 8795
```

Открыть: `http://127.0.0.1:8795/portal/`.

## Важные ссылки

| Раздел | Зачем открыть | Ссылка |
|---|---|---|
| 🚀 Старт | Главный маршрут по репозиторию и ролям. | [docs/index.md](docs/index.md) |
| 🛠️ Установка | Dry-run, ручная установка, rollback, проверка после установки. | [INSTALL.md](INSTALL.md) |
| 🧠 Навыки | Каталог installable skills и meta-skills. | [docs/skills.md](docs/skills.md) |
| 🧭 Навигация | Карта папок, документов и визуальных материалов. | [docs/navigation.md](docs/navigation.md) |
| 🛡️ Приватность | Что разрешено публиковать, а что нельзя. | [docs/privacy-boundary.md](docs/privacy-boundary.md) |
| 🖥️ Портал | Локальная read-only PWA-витрина. | [portal/README.md](portal/README.md) |

## Что внутри

| Раздел | Для чего | Ссылка |
|---|---|---|
| **Стартовая документация** | Что это за проект, как читать, где граница публикации. | [docs/index.md](docs/index.md), [docs/navigation.md](docs/navigation.md) |
| **Установка** | Dry-run, ручная установка, rollback, проверка после установки. | [INSTALL.md](INSTALL.md), [пакет Hermes](packages/hermes/rednet-airin-meta-skills/README.md) |
| **Навыки** | Установочные `SKILL.md`: базовые REDNET-навыки и `rednet-meta`. | [skills/README.md](skills/README.md), [docs/skills.md](docs/skills.md) |
| **Протоколы** | Приёмка, отключение, сопровождение manifest, session-guided activation. | [protocols/](protocols/) |
| **Портал** | Статическая локальная витрина без live-команд. | [portal/README.md](portal/README.md), [docs/rednet-portal.md](docs/rednet-portal.md) |
| **Пакеты и прототипы** | Manifest, установщик, observe-only сенсоры, science coordinator template. | [packages/](packages/), [sensor-prototype/](sensor-prototype/) |
| **Исследования** | Только curated summaries и module packs; raw inbox/ledger не публикуются. | [research/rednet-quiet-step-lab/README.md](research/rednet-quiet-step-lab/README.md) |
| **Публикация** | Чеклист перед будущим GitHub public/release. | [docs/release-checklist.md](docs/release-checklist.md), [docs/privacy-boundary.md](docs/privacy-boundary.md) |

## Главные навыки

| Навык | Тип | Для чего | Страница |
|---|---|---|---|
| `rednet-double-evaluation` | installable skill | Двойная оценка: прямой анализ + анализ собственного первого следа, затем сверка фактов/гипотез/метафор. | [SKILL.md](skills/rednet/rednet-double-evaluation/SKILL.md) |
| `rednet-wakefulness-cascade` | installable skill | Контур бодрствования: self-poll, safe snapshot, nano-evaluation, recommendation без скрытых действий. | [SKILL.md](skills/rednet/rednet-wakefulness-cascade/SKILL.md) |
| `rednet-neural-service-node` | installable skill | Observe/advise-only сервисный сигнализатор с JSON, SQLite-журналом и pending-рекомендациями. | [SKILL.md](skills/rednet/rednet-neural-service-node/SKILL.md) |
| `rednet-meta/*` | skill family | 15 мета-навыков для качества процесса: критерии, неопределённость, public editor, research protocol и др. | [skills/rednet-meta/README.md](skills/rednet-meta/README.md) |

Полная таблица: [docs/skills.md](docs/skills.md).

## Граница публикации

В публичный слой входят только:

- обезличенные описания, схемы и синтетические примеры;
- установочные навыки без секретов и без runtime-состояния;
- протоколы приёмки, отключения и проверки;
- read-only портал и проверяемые учебные прототипы.

В публичный слой **не входят**:

- сырой чат, дневники, приватные PDF/капсулы;
- `.env`, токены, ключи, OAuth/Telegram-сессии, cookies;
- локальные runtime-выгрузки, cycle-reports, raw inbox, ledger/database dumps;
- точные приватные пути, NAS/UNC-адреса, рабочие базы и восстановимые настройки;
- live Hermes, VPN/Tailscale/SSH/router actions и любые скрытые публикации.

Подробно: [docs/privacy-boundary.md](docs/privacy-boundary.md).

## Проверка публичной версии

Минимальный безопасный набор из корня репозитория:

```powershell
python scripts\validate-rednet-schemas.py
python scripts\validate-portal-readonly.py
powershell -ExecutionPolicy Bypass -File packages\hermes\rednet-airin-meta-skills\install.ps1 -DryRun
```

Эта публичная версия создана как свежий Git-репозиторий без приватной истории исходного контура. Для следующих релизов повторяются secret scan, link check и review содержимого архивов.

## Статус

Репозиторий опубликован как **public-safe snapshot**: в нём нет приватной Git-истории, raw-памяти, токенов, runtime-выгрузок, архивов с непроверенным содержимым и live-команд. Более чувствительные пакеты памяти остаются в приватном контуре до отдельного релиза.
