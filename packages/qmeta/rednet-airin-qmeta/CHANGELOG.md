# Changelog

## 0.4.0

- Добавлен optional MCP-сервер `hermes-airin-mcp`.
- Добавлены функции инструментального слоя: `qmeta_solve`, `qmeta_skill_catalog`, `qmeta_explain_model`.
- Введен публичный термин `BranchingMetaEngine`; прежнее имя `MultiverseEngine` сохранено как совместимый alias.
- Уточнена научная граница: QMeta является классической инженерной моделью ветвления, а не физическим квантовым вычислением.
- Добавлены тесты MCP-функций.
- Усилена релизная упаковка: wheel/sdist включают `docs`, `skills`, `config`, `examples`, `manifest.json`, `CHANGELOG.md` и `TEST_REPORT.md`.

## 0.3.0

- Полноценный пакет `hermes_airin`.
- Реализованы режимы `answer` и `skill`.
- Добавлен `Consul` / Совет экспертных контуров.
- Добавлены процессы: MetaObserver, CriteriaLayer, UncertaintyRegister, Beseda, WillowStability, SanctumState, RedNetworkSim.
- Добавлены `SafetyGuard`, `PermissionGate`, `StrazhDoctrine`.
- Добавлены skill-cards JSON/YAML, примеры, тесты и документация.
