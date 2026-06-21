# Установочный релиз мета-навыков

Этот документ описывает состав installable-слоя. Практические команды установки вынесены в [../INSTALL.md](../INSTALL.md).

## Что считается installable

| Компонент | Путь | Статус | Устанавливается installer? |
|---|---|---|---|
| Базовые REDNET-навыки | `skills/rednet/` | MVP / prototype / stage 1 | Да |
| Мета-навыки | `skills/rednet-meta/` | Установочные модули | Да |
| Manifest | `packages/hermes/rednet-airin-meta-skills/manifest.json` | Описание пакета | Нет, справочно |
| Installer | `packages/hermes/rednet-airin-meta-skills/install.ps1` | Dry-run по умолчанию | Запускается вручную |
| Протоколы | `protocols/` | Сопровождение и приёмка | Нет, справочно |
| Портал | `portal/` | Read-only витрина | Нет |
| Сенсорные прототипы | `sensor-prototype/` | Observe-only examples | Нет |
| Исследования | `research/` | Curated reports / module packs | Нет |

## Список навыков

Пакет содержит 18 installable-навыков:

- `rednet-double-evaluation`;
- `rednet-wakefulness-cascade`;
- `rednet-neural-service-node`;
- `rednet-export-parser`;
- `rednet-meta-event-extractor`;
- `rednet-criteria-layer`;
- `rednet-unfinished-memory`;
- `rednet-branch-synchronizer`;
- `rednet-meta-memory`;
- `rednet-intention-map`;
- `rednet-process-observer`;
- `rednet-uncertainty-register`;
- `rednet-decision-memory`;
- `rednet-beseda`;
- `rednet-skill-collector`;
- `rednet-utility-evaluator`;
- `rednet-public-editor`;
- `rednet-research-protocol`.

## Принцип безопасности

Релиз не устанавливает навыки в live Hermes автоматически. Он даёт:

- skill-папки;
- manifest;
- dry-run installer;
- протоколы;
- тестируемые observe-only прототипы.

Live-контуры и рабочая среда остаются вне области действия репозитория.

## Как проверить

```powershell
powershell -ExecutionPolicy Bypass -File packages\hermes\rednet-airin-meta-skills\install.ps1 -DryRun
python scripts\validate-rednet-schemas.py
python scripts\validate-portal-readonly.py
python -m unittest discover sensor-prototype\airin-signal-sensor\tests
python -m unittest discover sensor-prototype\airin-wakefulness-node\tests
python -m unittest discover sensor-prototype\airin-neural-service-node\tests
```

## Что не входит

- raw chat, дневники, private PDF/капсулы;
- Telegram/OAuth-сессии, cookies, токены и ключи;
- рабочие базы, cycle-reports, runtime-выгрузки;
- raw inbox/ledger/database exports;
- реальные сетевые маршруты и приватные UNC/NAS-пути;
- live Zeek/Suricata события или любые live-команды.

## Release artifacts

Сгенерированные ZIP/SHA лучше публиковать как GitHub Release artifacts. Если архив остаётся в репозитории, он должен проходить тот же secret scan, что и исходники.
