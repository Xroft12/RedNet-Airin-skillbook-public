# Closed archive audit — 2026-06-27 — RU / EN

> Public-safe audit summary. The closed archive was inspected only to extract safe architecture ideas. Raw closed files were not copied into the public layer.

## RU — результат проверки

Проверены два архива:

- `RedNet-Airin-skillbook-public-main.zip` — публичная версия: 317 файлов.
- `REDNET-AIRIN-SKILLBOOK-master.zip` — закрытая версия: 597 файлов.

Сравнение показало:

- 391 файл есть только в закрытой версии;
- 111 файлов есть только в публичной версии;
- главная недостающая линия закрытой версии — `RedNET Fast Memory`, портативные memory-пакеты, отчёты локальных прогонов и исследовательские карточки Quiet Step Lab.

## RU — что нельзя переносить напрямую

Закрытая версия содержит индикаторы чувствительности: личные имена, контактные форматы, сетевые строки, рабочие настройки, локальные отчёты, переносимые bundle-архивы и повторяющиеся служебные журналы. Поэтому прямое копирование закрытого дерева в публичный репозиторий запрещено.

## RU — что можно перенести безопасно

В публичный слой можно переносить только очищенные идеи:

1. **RedNET Fast Memory** как исследовательскую архитектуру: локальная память, read-only режим, dry-run install, deterministic analysis, digest, safety gates.
2. **Airin subconscious skill** как мета-навык подготовки контекста: collect -> analyze -> digest -> limited context.
3. **Quiet Step Lab cards** как агрегированный module pack без raw inbox.
4. **Night plan 2026-06-09** как public architecture snapshot: redactor, scope-router, InsightCandidate, double evaluation, reaction controller.
5. **Release discipline**: smoke tests, manifest, sha checks, rollback, public/private boundary.

## EN — audit result

Two archives were inspected:

- `RedNet-Airin-skillbook-public-main.zip` — public version: 317 files.
- `REDNET-AIRIN-SKILLBOOK-master.zip` — closed version: 597 files.

Comparison result:

- 391 files exist only in the closed version;
- 111 files exist only in the public version;
- the main missing line is `RedNET Fast Memory`, portable memory bundles, local run reports, and Quiet Step Lab research cards.

## EN — what must not be copied directly

The closed version contains sensitivity indicators: personal names, contact-like formats, network strings, live settings, local reports, portable bundle archives, and repeated operational logs. Directly copying the closed tree into the public repository is not allowed.

## EN — what can be safely carried over

Only sanitized ideas can be moved to the public layer:

1. **RedNET Fast Memory** as a research architecture: local memory, read-only mode, dry-run install, deterministic analysis, digest, and safety gates.
2. **Airin subconscious skill** as a context-preparation meta-skill: collect -> analyze -> digest -> limited context.
3. **Quiet Step Lab cards** as an aggregated module pack without raw inbox material.
4. **Night plan 2026-06-09** as a public architecture snapshot: redactor, scope-router, InsightCandidate, double evaluation, reaction controller.
5. **Release discipline**: smoke tests, manifest, sha checks, rollback, public/private boundary.

## Decision

Do not copy closed code, bundles, reports, or raw memory materials into the public repository. Instead, publish curated bilingual summaries, safe architecture maps, synthetic examples, and grant-facing descriptions.
