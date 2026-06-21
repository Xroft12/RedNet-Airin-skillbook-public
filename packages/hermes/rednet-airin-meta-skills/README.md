# REDNET Airin Meta Skills Package

Установочный пакет для Hermes/Codex-style навыков проекта REDNET Airin Skillbook.

Текущая версия manifest: `0.2.2`.

![Поток установки](../../../assets/install-flow.svg)

## Что входит в source package

| Слой | Путь | Роль |
|---|---|---|
| Базовые навыки | `../../../skills/rednet/` | 3 installable skills. |
| Мета-навыки | `../../../skills/rednet-meta/` | 15 installable meta-skills. |
| Manifest | `manifest.json` | Состав пакета, режимы и проверки. |
| Installer | `install.ps1` | Dry-run/apply копирование skill-папок. |

Протоколы, портал, сенсорные прототипы и research входят в репозиторий как справочные материалы, но этот installer их не копирует.

## Dry-run

По умолчанию installer ничего не копирует:

```powershell
powershell -ExecutionPolicy Bypass -File packages\hermes\rednet-airin-meta-skills\install.ps1 -DryRun
```

## Установка

Только в окно обслуживания:

```powershell
powershell -ExecutionPolicy Bypass -File packages\hermes\rednet-airin-meta-skills\install.ps1 -Apply
```

Если навык уже существует, installer пропустит его. Для безопасной замены с созданием backup-папки:

```powershell
powershell -ExecutionPolicy Bypass -File packages\hermes\rednet-airin-meta-skills\install.ps1 -Apply -Force
```

## Цели установки

| Сценарий | Опция |
|---|---|
| Windows default | `%LOCALAPPDATA%\hermes\skills\...` |
| Named profile | `-Profile <name>` → `~\.hermes\profiles\<name>\skills\...` |
| Custom target | `-HermesHome <path>` |

## Границы

Installer:

- не редактирует `config.yaml`;
- не перезапускает Hermes Gateway;
- не открывает Hermes Desktop;
- не трогает Telegram/OAuth-сессии;
- не копирует `docs/`, `research/`, `portal/`, runtime DB/logs или приватные материалы;
- не включает навыки автоматически в текущей сессии.

## Проверка

```powershell
powershell -ExecutionPolicy Bypass -File packages\hermes\rednet-airin-meta-skills\install.ps1 -DryRun
python scripts\validate-rednet-schemas.py
python scripts\validate-portal-readonly.py
```

Полная инструкция: [../../../INSTALL.md](../../../INSTALL.md).
