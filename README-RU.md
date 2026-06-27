<div align="center">

<a href="docs/index.md">
  <img src="assets/rednet-banner.svg" alt="Баннер REDNET Airin Skillbook" width="920">
</a>

# REDNET Airin Skillbook

**Публично-безопасная книга навыков для QMeta, Airin/Hermes, воспроизводимых исследований, dry-run-инструментов и open-source сопровождения под заявки.**

[English version](README-EN.md) · [Маршрут ревьюера](docs/reviewer-path.ru.md) · [Документация](docs/index.md) · [Установка](INSTALL.md) · [Навыки](docs/skills.md) · [QMeta](docs/qmeta-scientific-model.md) · [Пакет заявок](grants/README-RU.md)

</div>

## Обзор

REDNET Airin Skillbook — публичный open-source репозиторий для исследований агентных процессов и повторно используемых мета-навыков. Он показывает систему навыков Airin/Hermes, модель QMeta, read-only портал, dry-run установку, релизную дисциплину и пакет заявок на доступы и гранты.

Репозиторий рассчитан на ревьюеров, сопровождающих open-source проекты, исследователей и потенциальных партнёров. В публичный слой входят документация, installable skill cards, синтетические примеры, схемы, протоколы и очищенные исследовательские сводки.

## Что такое QMeta

QMeta — классическая инженерная модель мета-навыков. Она не утверждает физическое квантовое вычисление, сознание модели, магические свойства или нелокальные эффекты. Квантово-информационные термины используются только как инженерные аналогии для ветвления, коррекции ошибок, ансамблевой оценки, пороговых режимов и трассируемой памяти решений.

```text
branching -> audit -> score -> council -> interference -> measure -> answer | skill
```

![Оператор QMeta](assets/qmeta-operator.svg)

## Почему репозиторий важен

Длинные агентные workflow часто теряют связность, смешивают факты с предположениями и создают результат, который трудно проверить позднее. REDNET Airin Skillbook решает эти проблемы через явные процессные контуры: ветвление, проверку критериев, dry-run first подход, read-only preview, публичную границу и повторно используемые skill cards.

## Маршрут ревьюера

1. [QMeta / Airin grant positioning](docs/qmeta-grant-positioning.ru-en.md)
2. [Черновики заявок OpenAI](grants/openai-applications.ru.md)
3. [Codex Open Source Fund note](grants/openai-codex-fund.md)
4. [Радар научных грантов](grants/scientific-grant-radar.ru.md)
5. [Граница публикации](docs/privacy-boundary.md)
6. [Научная модель QMeta](docs/qmeta-scientific-model.md)
7. [Сводка проверки закрытого архива](docs/closed-archive-audit-2026-06-27.ru-en.md)

## Карта репозитория

| Раздел | Назначение |
|---|---|
| `skills/` | Устанавливаемые и концептуальные навыки REDNET / Airin / Hermes. |
| `packages/qmeta/rednet-airin-qmeta/` | Python-пакет и optional MCP-сервер QMeta. |
| `research/rednet-quiet-step-lab/` | Исследовательский конвейер и module packs. |
| `portal/` | Статическая read-only PWA-витрина. |
| `docs/` | Архитектура, навигация, release checks и документы QMeta. |
| `grants/` | Пакет заявок на гранты и доступ к моделям. |
| `assets/` | Схемы, баннеры, иконки и визуальные карты. |

## Основные направления подачи

| Направление | Что запрашивается |
|---|---|
| OpenAI Codex for Open Source | ChatGPT Pro with Codex, API credits и поддержка maintainer workflow. |
| OpenAI Codex Open Source Fund | API credits для QMeta evaluations и open-source сопровождения. |
| OpenAI Trusted Access / defensive research support | Поддержка авторизованного code review, patch validation и maintainer checklists. |
| OpenAI Researcher Access Program | API credits для оценки QMeta на синтетических задачах. |

## Визуальные материалы

| Файл | Назначение |
|---|---|
| [rednet-banner.svg](assets/rednet-banner.svg) | Главный баннер репозитория. |
| [qmeta-operator.svg](assets/qmeta-operator.svg) | Схема оператора QMeta. |
| [airin-icon.svg](assets/airin-icon.svg) | Иконка визуальной идентичности Airin. |
| [skillbook-map.svg](assets/skillbook-map.svg) | Карта структуры репозитория. |
| [install-flow.svg](assets/install-flow.svg) | Схема безопасной установки. |

## Быстрый старт

```powershell
powershell -ExecutionPolicy Bypass -File packages\hermes\rednet-airin-meta-skills\install.ps1 -DryRun
```

```powershell
python -m http.server 8795
```

Открыть портал: `http://127.0.0.1:8795/portal/`.

## Статус

Репозиторий готовится как funding-grade public open-source showcase: понятный, двуязычный, проверяемый и безопасный для внешних ревьюеров.
