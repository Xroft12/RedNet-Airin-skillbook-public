# Интеграция в агента Гермес

## Вариант 1. Локальный Python runtime

```python
from hermes_airin import create_default_agent

agent = create_default_agent(memory_dir="./runtime")
result = agent.solve("Составь план...", mode="answer")
```

## Вариант 2. Подключение LLM

```python
from hermes_airin import HermesAirinAgent
from hermes_airin.adapters import LLMBranchGeneratorAdapter
from hermes_airin.core import MultiverseEngine

# generator должен вернуть список текстов ветвей. Библиотека сама внешние API не вызывает.
def my_generator(task, context):
    return ["ветвь 1", "ветвь 2", "ветвь 3"]

engine = MultiverseEngine(branch_generator=LLMBranchGeneratorAdapter(my_generator))
agent = HermesAirinAgent(engine=engine)
```

## Вариант 3. Docker

Минимальная команда:

```bash
python -m hermes_airin "Составь план решения" --mode answer --diagnostics
```

Для production-контейнера рекомендуется хранить `JsonlMemory` в отдельном volume.
