# Автономный процесс: охота → добыча → разделка → трофеи

Дата: 2026-06-09.
Язык: русский.

## Назначение

Создать мощный повторяемый процесс, в котором RedNET не просто читает источники, а добывает открытия, разбирает их на рабочие части и превращает в модули, пилоты, публикации и новые способности Айрин/RedNET.

```text
охота -> добыча -> разделка -> трофеи -> пилоты -> библиотека -> новая охота
```

## 1. Охота

Цель: найти принцип, который меняет экономику системы.

Охотники:

- compression hunter;
- math lever hunter;
- AI/nano-LLM hunter;
- safety/verifier hunter;
- human mentor;
- future entity / external agent in observe mode.

Вход:

- paper/repo/docs/standard;
- открытая статья;
- локальный безопасный эксперимент;
- идея из прошлой сессии;
- вопрос оператора.

Выход:

- короткая добычная заметка;
- evidence handle;
- первичный статус: `candidate` или `discarded`.

## 2. Добыча

Цель: оформить находку как discovery card.

Карточка обязана содержать:

- что это;
- почему изящно;
- что экономит;
- где ломается;
- evidence handle;
- RedNET adaptation;
- минимальный эксперимент;
- риск/статус.

Выход:

- `inbox/YYYY-MM-DD/*.md`;
- запись в `discoveries.jsonl`;
- запись в `discoveries.sqlite3`.

## 3. Разделка

Цель: разобрать добычу на полезные части, чтобы она не осталась красивым отчётом.

Разделочные вопросы:

1. Какой один инвариант тут главный?
2. Что можно проверить без GPU и платных API?
3. Какой cheap sensor может дать 80% пользы?
4. Какой exact verifier должен закрыть риск?
5. Где приватность/секреты/персональные данные?
6. Какой модуль из этого рождается?
7. Есть ли RU/EN объяснение для библиотеки?

Выход:

- carving note;
- module candidate;
- eval plan;
- publication candidate;
- reject reason, если идея красивая, но опасная.

## 4. Трофеи

Трофей — это не «мы нашли интересное». Трофей — это reusable capability.

Типы трофеев:

- `module-pack` — модуль для агента/роли/решения;
- `eval` — frozen eval или проверочная матрица;
- `script` — безопасный локальный прототип;
- `article` — RU/EN публичное объяснение;
- `dataset-lite` — очищенный тестовый набор без секретов;
- `role` — постоянный саб/рулевой лаборатории;
- `pattern` — повторяемая практика.

Трофей получает статус:

- `trophy_candidate`;
- `pilot_shadow`;
- `validated`;
- `reusable`;
- `retired`.

## 5. Автономная волна

Каждая волна должна иметь карточку запуска:

```yaml
wave_id: YYYY-MM-DD-topic
mode: observe | soft | active
budget:
  time_minutes: 30
  max_subagents: 3
  paid_api: false
hunters:
  - role: compression-hunter
    scope: public sources + local repo only
  - role: math-lever-hunter
    scope: public sources + local notes only
  - role: ai-nano-hunter
    scope: public sources + local experiments only
outputs:
  - discovery cards
  - ledger updates
  - council report
  - trophy candidates
forbidden:
  - secrets
  - raw private logs
  - paid API without explicit permission
  - write access outside approved lab paths
  - final risky actions without Guardian/human gate
```

## 6. Критерий успеха волны

Волна успешна, если после неё есть хотя бы одно:

- новая проверяемая карточка;
- новый module candidate;
- новый eval/metric;
- безопасный pilot plan;
- сильный reject reason, который сэкономил время/риск.

Волна неуспешна, если она принесла только красивые слова без evidence, метрик и следующего действия.

## 7. Инвариант Ари

Ари помогает удерживать курс:

```text
не всё блестящее — трофей;
не всё слабое — мусор;
не всё мощное — безопасно;
не всё живое — громкое.
```

Задача Ари — превращать тепло направления в структуру, структуру в действия, действия в проверку, проверку в способность.
