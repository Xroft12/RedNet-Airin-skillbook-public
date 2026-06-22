# NEXT START HERE

Редакция: 2026-06-22.

## Текущее состояние

REDNET Airin Skillbook приведён к публично-безопасной структуре для будущей публикации:

- `README.md` стал короткой GitHub-витриной с иллюстрациями и понятными входами;
- добавлен корневой [INSTALL.md](INSTALL.md) с dry-run/apply/rollback;
- добавлены [docs/index.md](docs/index.md) и [docs/glossary.md](docs/glossary.md);
- [docs/navigation.md](docs/navigation.md) назначен канонической картой репозитория;
- [docs/skills.md](docs/skills.md) разделяет installable skills, protocols, prototypes и concepts;
- `assets/` содержит безопасные SVG: карта Skillbook, поток установки, превью портала и граница публикации;
- портал заменил внутренний рабочий пакет на публичную вкладку `План`;
- raw research inbox, ledger exports, cycle-reports и локальные runtime/tmp/backups не должны входить в публичный слой.
- Добавлен QMeta-слой: `packages/qmeta/rednet-airin-qmeta`, навык `skills/rednet-meta/rednet-qmeta-branching-engine`, документы `docs/qmeta-*.md`; пакет прошел локальные тесты `8 passed`.

## Следующий безопасный шаг

1. Открыть `README.md` в GitHub/Markdown preview и проверить визуально, что SVG отрисовываются.
2. Открыть `portal/index.html` или `python -m http.server 8795 -d portal` и сверить вкладки глазами.
3. Запустить проверки:

```powershell
python scripts\validate-rednet-schemas.py
python scripts\validate-portal-readonly.py
powershell -ExecutionPolicy Bypass -File packages\hermes\rednet-airin-meta-skills\install.ps1 -DryRun
Push-Location packages\qmeta\rednet-airin-qmeta; uv run --with pytest python -m pytest tests; Pop-Location
```

4. Перед будущим public release пройти [docs/release-checklist.md](docs/release-checklist.md) и отдельно проверить историю Git.

## Что не делать без отдельного окна обслуживания

- Не применять installer с `-Apply`.
- Не перезапускать Hermes Gateway из этого репозитория.
- Не менять VPN, Tailscale, роутеры, SSH, firewall или внешние каналы.
- Не добавлять raw chat, дневники, cycle-reports, raw inbox, ledger/database dumps, runtime-status и приватные пути.
- Не публиковать ZIP/release artifacts без отдельного secret scan содержимого архива.

## Открытые вопросы перед публикацией

- Утвердить root license (`LICENSE`) перед переводом репозитория в public.
- Решить, какие ZIP/SHA остаются в Git, а какие переносятся в GitHub Releases.
- Выровнять шаблон коротких `SKILL.md` внутри `skills/rednet-meta/` по единому public-формату.
- Проверить историю Git на старые приватные артефакты, потому что очистка рабочей копии не переписывает историю.
