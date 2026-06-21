# Чеклист публикации

Чеклист используется перед каждой выгрузкой в GitHub и перед переводом репозитория в публичный режим.

## 1. Секреты

В репозитории не должно быть:

- `.env`, `.env.*` кроме `.env.example`;
- токенов, API-ключей, OAuth-секретов;
- Telegram/session/cookie-файлов;
- приватных SSH-ключей, паролей, application passwords;
- приватных дампов баз, SQLite/JSONL runtime-слоёв;
- raw logs с путями, аккаунтами или сетевыми деталями.

## 2. Приватный корпус

В публичный репозиторий не включаются:

- сырой чат;
- личные PDF, дневниковые записи и приватные капсулы;
- полные логи и восстановимые рабочие снимки;
- `reports/cycles/`, `tmp/`, `.tmp/`, `backups/`;
- raw `research/**/inbox/`, ledger exports и рабочие базы;
- точные локальные пути, NAS/UNC-адреса и реальные сетевые адреса закрытого контура.

## 3. Документы

Проверить:

- `README.md` — короткая витрина, не огромный внутренний индекс;
- `INSTALL.md` — ясно показывает dry-run, apply, rollback и границы installer;
- `docs/navigation.md` — полная карта без ссылок на приватные raw-выгрузки;
- `docs/index.md` — маршруты по ролям;
- `docs/glossary.md` — единый словарь терминов;
- `docs/skills.md` — разделяет installable/protocol/prototype/concept;
- `docs/privacy-boundary.md` — согласован с `.gitignore`;
- `docs/rednet-portal.md` и `portal/README.md` — совпадают с фактическими вкладками портала;
- `CHANGELOG.md` — соответствует фактическим изменениям и не ссылается на удалённые private/raw файлы.

## 4. Визуалы

Проверить глазами:

- `assets/skillbook-map.svg`;
- `assets/install-flow.svg`;
- `assets/portal-preview.svg`;
- `assets/airin-public-boundary.svg`;
- README и portal preview после рендера.

На изображениях не должно быть реальных аккаунтов, адресов, токенов, путей и runtime-статусов.

## 5. Техническая проверка

Перед публикацией выполнить:

```text
git status --short --ignored=matching
git diff --check
secret scan по запретным паттернам
проверка UTF-8 чтения документов
проверка ссылок на существующие файлы
python scripts\validate-rednet-schemas.py
python scripts\validate-portal-readonly.py
powershell -ExecutionPolicy Bypass -File packages\hermes\rednet-airin-meta-skills\install.ps1 -DryRun
```

Для прототипов дополнительно:

```text
python -m unittest discover sensor-prototype/airin-signal-sensor/tests
python -m unittest discover sensor-prototype/airin-wakefulness-node/tests
python -m unittest discover sensor-prototype/airin-neural-service-node/tests
```

## 6. Архивы и release artifacts

- Если ZIP нужен как release artifact, предпочтительно хранить его в GitHub Releases, а не в основной ветке.
- Если ZIP остаётся в репозитории, он должен проходить тот же secret scan и link/manifest review.
- SHA256 рядом с архивом не доказывает безопасность содержимого; он доказывает только неизменность.

## 7. Закрытие цикла

Безопасная проверка:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\cycle-close.ps1 -DryRun
```

Фактическое закрытие с внешними копиями/push — только после отдельного подтверждения и с параметрами/переменными окружения, не зашитыми в публичные документы.

## 8. Публичная формулировка

Допустимы:

- инженерные описания;
- исследовательские гипотезы с маркировкой;
- обезличенные примеры;
- модульные контракты;
- дорожная карта.

Недопустимы:

- утверждения о сознании как о факте;
- приватные эмоциональные фрагменты;
- инструкции, раскрывающие закрытую сеть;
- обещания готовности модулей, которые находятся только в исследовании;
- raw-выгрузки, которые можно восстановить до внутренней сессии.

## 9. Передача на чтение

Когда репозиторий остаётся приватным, можно давать временный доступ на чтение. Перед переводом в public нужно повторить чеклист полностью и отдельно проверить историю коммитов.
