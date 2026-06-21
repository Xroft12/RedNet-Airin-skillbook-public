# Установка REDNET Airin Skillbook

![Безопасный поток установки](assets/install-flow.svg)

Эта инструкция описывает безопасную установку skill-пакета из репозитория. По умолчанию всё начинается с `DryRun`: команда показывает, что будет сделано, но ничего не копирует.

## Что устанавливается

Installer `packages/hermes/rednet-airin-meta-skills/install.ps1` копирует только две папки навыков:

| Source | Target |
|---|---|
| `skills/rednet/` | `<HermesHome>/skills/rednet/` |
| `skills/rednet-meta/` | `<HermesHome>/skills/rednet-meta/` |

Справочные документы, протоколы, портал, research и sensor-prototype **не устанавливаются автоматически**. Они остаются в репозитории как документация и проверяемые примеры.

## Требования

- Windows PowerShell 5.1+ или PowerShell 7+.
- Установленный Hermes Agent или совместимое хранилище навыков.
- Доступ к локальной копии репозитория.
- Отдельное окно обслуживания для фактического `-Apply`.

## 1. Проверка без изменений

```powershell
powershell -ExecutionPolicy Bypass -File packages\hermes\rednet-airin-meta-skills\install.ps1 -DryRun
```

Ожидаемый смысл вывода:

- режим `DRY-RUN`;
- путь репозитория;
- целевой `Hermes target`;
- список skill-папок, которые были бы скопированы;
- строка `Dry-run complete. Nothing was copied.`

## 2. Выбор цели установки

| Сценарий | Команда |
|---|---|
| Стандартный Hermes на Windows | `...\install.ps1 -DryRun` |
| Именованный профиль | `...\install.ps1 -DryRun -Profile <profile-name>` |
| Явный путь HermesHome | `...\install.ps1 -DryRun -HermesHome <path>` |

Для реальной установки замените `-DryRun` на `-Apply` только после проверки diff/секретов и в отдельное окно обслуживания.

## 3. Фактическая установка

```powershell
powershell -ExecutionPolicy Bypass -File packages\hermes\rednet-airin-meta-skills\install.ps1 -Apply
```

Если целевой навык уже существует, installer пропустит его. Чтобы заменить существующие навыки с локальным backup:

```powershell
powershell -ExecutionPolicy Bypass -File packages\hermes\rednet-airin-meta-skills\install.ps1 -Apply -Force
```

При `-Force` существующая папка навыка переносится в `*.backup-YYYYMMDD-HHMMSS`, затем копируется новая версия.

## 4. Что installer не делает

Installer намеренно не выполняет опасные действия:

- не редактирует `config.yaml` и `.env`;
- не перезапускает Hermes Gateway;
- не открывает Telegram/OAuth/Google/VK-сессии;
- не меняет VPN/Tailscale/SSH/роутеры/маршруты;
- не копирует runtime-базы, логи, дневники и приватные материалы;
- не включает навыки автоматически в текущую сессию.

После установки перезагрузку навыков или новой Hermes-сессии выполняют вручную по правилам своего контура.

## 5. Проверка после установки

Минимально:

```powershell
powershell -ExecutionPolicy Bypass -File packages\hermes\rednet-airin-meta-skills\install.ps1 -DryRun
python scripts\validate-rednet-schemas.py
python scripts\validate-portal-readonly.py
```

Для самого Hermes после установки проверьте список навыков штатным способом выбранного профиля. Не перезапускайте gateway из этого репозитория.

## 6. Rollback

Если установка выполнялась с `-Force`, найдите созданную папку `*.backup-YYYYMMDD-HHMMSS` рядом с целевым навыком и восстановите её вручную после остановки соответствующего окна обслуживания.

Если установка была без `-Force`, существующие навыки не перезаписывались, поэтому rollback обычно не нужен.

## 7. Публичная безопасность

Перед будущей публикацией или release:

- пройти [docs/privacy-boundary.md](docs/privacy-boundary.md);
- пройти [docs/release-checklist.md](docs/release-checklist.md);
- проверить ссылки и схемы;
- убедиться, что в Git не попали `reports/cycles/`, `tmp/`, `backups/`, `portal/runtime/*.local.js`, raw `inbox/`, ledger/database dumps и архивы с приватным содержимым.
