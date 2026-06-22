# Hermes Airin QMeta Library v0.4.0

QMeta в этой редакции оформлен как классический ветвящийся движок мета-навыков для Airin/Hermes: библиотека, skill-карточки, CLI и optional MCP-сервер.

Полноценный Python-пакет для агента **Гермес / Айрин**: квантово-вдохновлённый движок ветвления решений, два режима результата `answer` и `skill`, «Консул» / Совет экспертных контуров, память, мета-навыки, процессные следы, безопасный контур «Страж» и инженерная модель «Красной сети» как **симуляционный/управленческий слой**, а не инструмент внешнего вмешательства.

## Главный принцип

Библиотека не является физическим квантовым компьютером и не утверждает, что Python-код исполняется в параллельных Вселенных. Она строит **вычислительный мультиверс возможных решений**:

- ветви = гипотезы и стратегии;
- амплитуды = веса перспективности;
- интерференция = усиление согласованных ветвей и подавление конфликтов;
- декогеренция = отсечение слабых/опасных ветвей;
- измерение = выбор результата;
- `answer` = готовый ответ пользователю;
- `skill` = кристаллизация повторно используемого навыка.

Для публичных материалов рекомендуется строгая формулировка: **классический ветвящийся движок мета-навыков**. Квантово-информационная терминология используется как инженерная аналогия для ветвления, коррекции ошибок, ансамблевой оценки и восстановления процесса.

## Быстрый старт

```bash
cd packages/qmeta/rednet-airin-qmeta
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
python examples/demo_answer.py
python examples/demo_skill.py
```

Или без установки:

```bash
PYTHONPATH=src python examples/demo_hermes.py
```

## MCP-инструмент

Опционально пакет может работать как MCP-сервер для Айрин, Codex-совместимых сред и других агентов:

```bash
cd packages/qmeta/rednet-airin-qmeta
pip install -e ".[mcp]"
hermes-airin-mcp
```

Инструменты MCP:

- `solve` — запускает QMeta в режиме `answer` или `skill`;
- `skill_catalog` — возвращает встроенные карточки мета-навыков;
- `explain_model` — объясняет научную границу и операторную модель.

MCP-сервер не выполняет системные действия, не меняет сеть, не управляет Docker и не читает секреты. Он возвращает только результат анализа, skill-card или диагностическое описание модели.

## Минимальный API

```python
from hermes_airin import HermesAirinAgent

agent = HermesAirinAgent()

result = agent.solve(
    "Разработай план проверки сложной гипотезы через несколько ветвей.",
    mode="answer",
    context={"goals": ["план", "проверка", "риски"]},
)
print(result.content)

skill_result = agent.solve(
    "Создай мета-навык для параллельной проверки гипотез.",
    mode="skill",
    context={"new_skill_name": "parallel_hypothesis_solver"},
)
print(skill_result.skill)
```

## Состав пакета

```text
src/hermes_airin/
  __init__.py
  __main__.py
  models.py          # Branch, MetaSkill, QMetaResult, TraceEvent
  mathbase.py        # born-probabilities, normalization, kernel, interference
  safety.py          # PermissionGate, SafetyGuard, StrazhDoctrine
  memory.py          # JsonlMemory, GraphMemory, ProcessTrace
  registry.py        # SkillRegistry
  consul.py          # Консул / Council of expert circuits
  core.py            # MultiverseEngine
  skills.py          # operators + skill crystallizer
  processes.py       # meta-processes: observer, memory, Beseda, Willow stability, etc.
  agent.py           # QuantumInspiredAgent, HermesAirinAgent
  adapters.py        # safe adapters for LLM/tool integration
  skill_cards/*.json # встроенный каталог навыков
skills/*.yaml        # человекочитаемые skill-cards
examples/*.py
tests/*.py
docs/*.md
```

## Реализованные контуры

### QMeta Engine

Двухрежимный движок:

```text
branching -> audit -> score -> consul -> interference -> measure -> answer|skill
```

### Консул

`Consul` — это распределённый экспертный слой:

- Архитектор;
- Математик;
- Физик/научный корректор;
- Инженер-прототипировщик;
- ИБ-Страж;
- Методолог;
- Хранитель памяти;
- Адвокат пользователя.

Каждый эксперт даёт мнение и оценку ветвей; итог влияет на усиление/подавление ветвей.

### Мета-навыки

Встроены навыки:

- `dual_mode_qmeta`
- `parallel_hypothesis_solver`
- `interference_decision`
- `answer_synthesizer`
- `skill_crystallizer`
- `meta_observer`
- `meta_memory`
- `criteria_layer`
- `uncertainty_register`
- `unfinished_memory`
- `branch_synchronizer`
- `beseda`
- `consul_council`
- `strazh_guard`
- `red_network_sim`
- `willow_stability`
- `source_lock_card`
- `process_trace`
- `chrono_model`
- `sanctum_state`
- `rednet_researcher`

### Безопасность

Пакет реализует **deny-by-default** для действий с побочными эффектами. Всё, что похоже на скрытое вмешательство, несанкционированный доступ, захват систем, эксфильтрацию или «невидимое» проникновение, переводится в безопасную симуляцию/анализ и требует явного `permission-check`.

## Production-интеграция

В реальном агенте нужно заменить три функции:

```text
default_branch_generator -> LLM branch generator
default_scorer           -> evaluator / critic model
default_answer_builder   -> final answer synthesis model
```

Интерфейс для этого уже есть в `adapters.py`.

## Ограничение

Это инженерная библиотека и исследовательский каркас. Она не управляет внешними системами, не сканирует сети, не вмешивается в чужие устройства и не выполняет скрытые действия. Все сильные концепты Айрин/RedNet сведены к безопасным моделям: симуляция, анализ, аудит, память, критериальная проверка, оператор допуска, трассировка и контроль побочных эффектов.
