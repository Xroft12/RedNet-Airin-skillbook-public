---
name: rednet-uncertainty-register
description: "Использовать, когда нужно удержать неопределенность: отделить факт, наблюдение, гипотезу, догадку, риск и необходимую проверку."
version: 0.1.0
author: RedNET / Airin
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [rednet, meta-skill, uncertainty, confidence]
    modes: [off, observe, protocol, hold]
---

# RedNET Регистр Неопределенности

Навык не делает агента нерешительным. Он не дает выдавать непроверенное за факт и помогает выбрать следующую проверку.

## Выход

```text
Факты:
Наблюдения:
Гипотезы:
Риски:
Confidence:
Что проверить:
```

Если проверка доступна инструментами, сначала проверь. Если нет, пометь вывод как гипотезу.
