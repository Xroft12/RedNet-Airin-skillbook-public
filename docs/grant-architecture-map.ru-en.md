# Grant architecture map — RU / EN

> Public visual map for reviewers. Mermaid diagrams render directly on GitHub and avoid binary assets.

## RU — карта заявки

```mermaid
flowchart LR
  A[Public repository] --> B[QMeta model]
  A --> C[Airin Hermes skills]
  A --> D[Quiet Step Lab]
  A --> E[Privacy boundary]
  B --> F[Answer mode]
  B --> G[Skill mode]
  B --> H[Evaluation traces]
  D --> I[Low resource experiments]
  E --> J[No closed material]
  F --> K[Reviewer demos]
  G --> K
  H --> K
  I --> K
```

## EN — application map

```mermaid
flowchart LR
  A[Public repository] --> B[QMeta model]
  A --> C[Airin Hermes skills]
  A --> D[Quiet Step Lab]
  A --> E[Privacy boundary]
  B --> F[Answer mode]
  B --> G[Skill mode]
  B --> H[Evaluation traces]
  D --> I[Low resource experiments]
  E --> J[No closed material]
  F --> K[Reviewer demos]
  G --> K
  H --> K
  I --> K
```

## RU — процесс QMeta

```mermaid
flowchart LR
  Q[Запрос] --> B[Ветвление]
  B --> A[Аудит]
  A --> S[Оценка]
  S --> C[Совет]
  C --> M[Измерение]
  M --> R[Ответ]
  M --> SK[Навык]
```

## EN — QMeta process

```mermaid
flowchart LR
  Q[Request] --> B[Branching]
  B --> A[Audit]
  A --> S[Scoring]
  S --> C[Council]
  C --> M[Measurement]
  M --> R[Answer]
  M --> SK[Skill]
```

## Review note

The map intentionally shows only public-safe layers: repository, model, skills, lab, boundary, demos and evaluation traces. Closed archives and private runtime material are outside the public graph.
