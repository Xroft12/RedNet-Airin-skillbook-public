const state = window.REDNET_PORTAL_STATE;

const tabs = [
  { id: "overview", title: "Обзор", icon: "M11 3h10v18H3V3h8Zm2 2v14h6V5h-6ZM5 5v6h6V5H5Zm0 8v6h6v-6H5Z" },
  { id: "repo", title: "Репозиторий", icon: "M4 4h7l2 2h7v14H4V4Zm2 4v10h12V8H6Zm2 2h8v2H8v-2Zm0 4h6v2H8v-2Z" },
  { id: "pwa", title: "PWA", icon: "M7 2h10a3 3 0 0 1 3 3v14a3 3 0 0 1-3 3H7a3 3 0 0 1-3-3V5a3 3 0 0 1 3-3Zm0 2a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1H7Zm3 13h4v2h-4v-2Z" },
  { id: "agents", title: "Контуры", icon: "M12 12a4 4 0 1 0-4-4 4 4 0 0 0 4 4Zm-8 9a8 8 0 0 1 16 0H4Z" },
  { id: "lab", title: "Лаборатория", icon: "M9 3h6v2l4.5 8A5.5 5.5 0 0 1 14.7 21H9.3a5.5 5.5 0 0 1-4.8-8L9 5V3Zm2 2.5L6.2 14A3.5 3.5 0 0 0 9.3 19h5.4a3.5 3.5 0 0 0 3.1-5L13 5.5V5h-2v.5Z" },
  { id: "university", title: "Университет", icon: "M4 5h16v3H4V5Zm2 5h3v9H6v-9Zm5 0h2v9h-2v-9Zm4 0h3v9h-3v-9ZM3 20h18v2H3v-2Z" },
  { id: "hermes", title: "Hermes", icon: "M4 4h16v5H4V4Zm2 2v1h12V6H6Zm-2 6h16v8H4v-8Zm3 2v2h3v-2H7Zm5 0v2h5v-2h-5Z" },
  { id: "roadmap", title: "План", icon: "M4 4h16v4H4V4Zm0 6h7v10H4V10Zm9 0h7v10h-7V10Z" },
  { id: "channels", title: "Каналы", icon: "M4 5h16v10H7l-3 4V5Zm2 2v7.2L6.8 13H18V7H6Z" },
  { id: "triad", title: "Канал троих", icon: "M12 3 3 8v8l9 5 9-5V8l-9-5Zm0 2.3L18 8.7l-6 3.3-6-3.3 6-3.4ZM5 10.4l6 3.3v6.1l-6-3.4v-6Zm14 0v6l-6 3.4v-6.1l6-3.3Z" },
  { id: "server", title: "Сервер", icon: "M4 4h16v6H4V4Zm0 10h16v6H4v-6Zm3-7v1h2V7H7Zm0 10v1h2v-1H7Z" },
  { id: "admin", title: "Админка", icon: "M5 4h14a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-5v2h3v2H7v-2h3v-2H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2Zm0 2v8h14V6H5Zm2 2h3v2H7V8Zm5 0h5v2h-5V8Zm-5 4h10v2H7v-2Z" },
  { id: "skillbook", title: "Skillbook", icon: "M5 4h11a3 3 0 0 1 3 3v13H8a3 3 0 0 1-3-3V4Zm3 14h9V7a1 1 0 0 0-1-1H7v11a1 1 0 0 0 1 1Z" },
  { id: "subagents", title: "Сотрудники", icon: "M7 11a3 3 0 1 1 3-3 3 3 0 0 1-3 3Zm10 0a3 3 0 1 1 3-3 3 3 0 0 1-3 3ZM2 21a5 5 0 0 1 10 0H2Zm10 0a5 5 0 0 1 10 0H12Z" },
  { id: "checks", title: "Проверки", icon: "M20 6 9 17l-5-5 1.4-1.4L9 14.2 18.6 4.6 20 6Z" }
];

const root = document.querySelector("#app");
const nav = document.querySelector("#tabs");

function badge(text, tone = "neutral") {
  return `<span class="badge badge-${tone}">${escapeHtml(text)}</span>`;
}

function icon(pathData) {
  return `<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="${pathData}"></path></svg>`;
}

function availabilityTone(agent) {
  return agent.availability === "online" ? "online" : "offline";
}

function availabilityText(agent) {
  return agent.availability === "online" ? "доступен" : "недоступен";
}

function statusTone(status) {
  const normalized = String(status).toLowerCase();
  if (["online", "active", "ok", "safe"].includes(normalized)) {
    return "online";
  }
  if (["observe", "planned", "manual", "guarded"].includes(normalized)) {
    return "quiet";
  }
  if (["disabled", "offline", "blocked"].includes(normalized)) {
    return "offline";
  }
  return "neutral";
}

function statusLabel(status) {
  const labels = {
    online: "доступен",
    active: "активен",
    ok: "ок",
    safe: "безопасно",
    observe: "наблюдение",
    planned: "план",
    manual: "ручной",
    guarded: "подтверждение",
    disabled: "отключено",
    offline: "нет связи",
    blocked: "блок"
  };
  return labels[String(status).toLowerCase()] || status;
}

function dockerDisplay(agent) {
  const service = String(agent.service || "").toLowerCase();
  const mapped = { ...agent };
  if (service.includes("personal-assistant")) {
    mapped.label = "Личный помощник";
    mapped.mode = "помощь / наблюдение";
    mapped.guard = "изолированная память, без лабораторных действий";
  } else if (service.includes("science-coordinator")) {
    mapped.label = "Научный координатор";
    mapped.mode = "координация / наблюдение";
    mapped.guard = "координация без живых команд";
  } else if (service.includes("qwen")) {
    mapped.label = "Qwen-шлюз";
    mapped.mode = "приватный модельный шлюз";
    mapped.guard = "не публиковать tokens/session/cookies";
  } else if (service.includes("dashboard")) {
    mapped.label = "Сервисная панель";
    mapped.mode = "панель без команд";
    mapped.guard = "без управляющих команд из портала";
  } else if (service.includes("home-automation")) {
    mapped.label = "Домашняя автоматизация";
    mapped.mode = "внешний сервис";
    mapped.guard = "не смешивать с агентской памятью";
  } else if (service.includes("automation")) {
    mapped.label = "Автоматизации";
    mapped.mode = "сервис сценариев";
    mapped.guard = "только статус без секретов";
  }
  if (String(mapped.endpoint || "").includes("port redacted")) {
    mapped.endpoint = "порт скрыт";
  } else if (String(mapped.endpoint || "").toLowerCase() === "internal") {
    mapped.endpoint = "внутренний";
  }
  return mapped;
}

function agentBoundary(agent) {
  const boundary = agent.boundary || {};
  const items = [
    boundary.namespace,
    boundary.memory,
    boundary.network,
    boundary.actionAllowed === false ? "действия запрещены" : ""
  ].filter(Boolean);
  return items.length ? `<div class="chip-row">${items.map((item) => `<code>${escapeHtml(item)}</code>`).join("")}</div>` : "";
}

function dockerIsolation(agent) {
  const display = (value) => ({
    isolated: "изолированный",
    template: "шаблон",
    private: "приватный",
    unset: "не указан",
    present: "есть",
    none: "нет",
    redacted: "скрыто",
    "unless-stopped": "unless-stopped"
  }[String(value)] || value);
  const parts = [
    agent.composeProject ? `проект: ${display(agent.composeProject)}` : "",
    agent.network ? `сеть: ${display(agent.network)}` : "",
    agent.volumes ? `тома: ${display(agent.volumes)}` : "",
    agent.restartPolicy ? `рестарт: ${display(agent.restartPolicy)}` : "",
    agent.actionAllowed === false ? "команды запрещены" : ""
  ].filter(Boolean);
  return parts.length ? parts.join("; ") : "границы не указаны";
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function list(items) {
  return `<ul>${items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`;
}

function table(headers, rows) {
  return `
    <div class="table-wrap">
      <table>
        <thead><tr>${headers.map((h) => `<th>${escapeHtml(h)}</th>`).join("")}</tr></thead>
        <tbody>
          ${rows.map((row) => `<tr>${row.map((cell) => `<td>${cell}</td>`).join("")}</tr>`).join("")}
        </tbody>
      </table>
    </div>
  `;
}

function renderOverview() {
  const online = state.agents.filter((agent) => agent.availability === "online").length;
  const offline = state.agents.length - online;
  const cta = state.project.cta || [];
  return `
    <section class="band">
      <div class="hero-panel">
        <div>
          <p class="eyebrow">локальный портал без команд</p>
          <h2>${escapeHtml(state.project.name)}</h2>
          <p>${escapeHtml(state.project.focus)}</p>
          <p class="muted">${escapeHtml(state.project.tagline || state.project.publicSurface)}</p>
          <div class="hero-actions">
            ${cta.map((item, index) => `
              <a class="hero-link ${index === 0 ? "primary" : ""}" href="${escapeHtml(item.href)}">${escapeHtml(item.label)}</a>
            `).join("")}
          </div>
        </div>
        <div class="metric-row">
          <div class="metric">
            <strong>${state.repository.trackedFiles}</strong>
            <span>файла в снимке репозитория</span>
          </div>
          <div class="metric">
            <strong>${state.repository.layers.length}</strong>
            <span>ключевых слоёв</span>
          </div>
          <div class="metric">
            <strong>${state.pwa.files.length}</strong>
            <span>PWA-файлов</span>
          </div>
        </div>
      </div>
      <div class="pillar-grid">
        ${[
          ["Проект", state.repository.mission, "миссия"],
          ["Репозиторий", state.repository.statusNote, state.repository.snapshot],
          ["PWA", state.pwa.cache, state.pwa.mode],
          ["Безопасность", state.project.safety, "read-only"]
        ].map((item) => `
          <article class="card pillar-card">
            <div class="card-top">
              <span class="agent-mark">${escapeHtml(item[0].slice(0, 1))}</span>
              ${badge(item[2], item[2].includes("read") ? "safe" : "quiet")}
            </div>
            <h3>${escapeHtml(item[0])}</h3>
            <p>${escapeHtml(item[1])}</p>
          </article>
        `).join("")}
      </div>
      <div class="status-grid">
        ${state.agents.map((agent) => `
          <article class="card agent-card ${agent.availability}">
            <div class="card-top">
              <span class="agent-mark">${escapeHtml(agent.publicLabel.slice(0, 1))}</span>
              ${badge(availabilityText(agent), availabilityTone(agent))}
            </div>
            <h3>${escapeHtml(agent.publicLabel)}</h3>
            <p>${escapeHtml(agent.role)}</p>
            <div class="meta-line">
              <span>${escapeHtml(agent.mode)}</span>
              <span>${escapeHtml(agent.state)}</span>
            </div>
          </article>
        `).join("")}
      </div>
      <div class="notice">${escapeHtml(state.project.publicSurface)}</div>
    </section>
  `;
}

function renderRepository() {
  return `
    <section class="band">
      <div class="section-head">
        <p class="eyebrow">структура и точки входа</p>
        <h2>${escapeHtml(state.repository.title)}</h2>
        <p>${escapeHtml(state.repository.mission)}</p>
        <p class="muted">${escapeHtml(state.repository.statusNote)}</p>
      </div>
      <div class="repo-grid">
        ${state.repository.layers.map((layer) => `
          <article class="card repo-card">
            <div class="card-top">
              <span class="agent-mark">${escapeHtml(layer.label.slice(0, 1).toUpperCase())}</span>
              ${badge(layer.path, "neutral")}
            </div>
            <h3>${escapeHtml(layer.label)}</h3>
            <p>${escapeHtml(layer.detail)}</p>
            <code>${escapeHtml(layer.path)}</code>
          </article>
        `).join("")}
      </div>
      <article class="wide-card two-column">
        <div>
          <div class="card-top inline">
            <h3>Главные входы</h3>
            ${badge(`${state.repository.trackedFiles} tracked`, "active")}
          </div>
          <p class="muted">Файлы, с которых удобно понимать проект и проверять его перед релизом.</p>
        </div>
        <div class="timeline">
          ${state.repository.entrypoints.map((item, index) => `
            <div class="timeline-item">
              <span class="timeline-index">${index + 1}</span>
              <div>
                <strong><code>${escapeHtml(item.file)}</code></strong>
                <p class="muted">${escapeHtml(item.purpose)}</p>
              </div>
            </div>
          `).join("")}
        </div>
      </article>
      <article class="card">
        <div class="card-top">
          <span class="agent-mark">G</span>
          ${badge("release gates", "guarded")}
        </div>
        <h3>Границы репозитория</h3>
        ${list(state.repository.gates)}
      </article>
    </section>
  `;
}

function renderPwa() {
  return `
    <section class="band">
      <div class="section-head">
        <p class="eyebrow">установка как приложение</p>
        <h2>${escapeHtml(state.pwa.title)}</h2>
        <p>${escapeHtml(state.pwa.install)}</p>
      </div>
      <div class="pwa-grid">
        ${[
          ["App shell", state.pwa.cache, "offline"],
          ["Граница", state.pwa.boundary, "safe"],
          ["Manifest", "Название, theme-color, standalone display, short_name и набор иконок.", "manifest"],
          ["Service Worker", "Кэширует локальные ассеты и отдаёт index.html как offline fallback.", "sw.js"]
        ].map((item) => `
          <article class="card">
            <div class="card-top">
              <span class="agent-mark">${escapeHtml(item[0].slice(0, 1))}</span>
              ${badge(item[2], item[2] === "safe" ? "safe" : "quiet")}
            </div>
            <h3>${escapeHtml(item[0])}</h3>
            <p>${escapeHtml(item[1])}</p>
          </article>
        `).join("")}
      </div>
      ${table(
        ["Файл", "Назначение"],
        state.pwa.files.map((file) => [
          `<code>${escapeHtml(file)}</code>`,
          escapeHtml(file.endsWith(".png") || file.endsWith(".svg") ? "иконка приложения" : file === "sw.js" ? "offline cache" : "описание PWA")
        ])
      )}
      <article class="card">
        <div class="card-top">
          <span class="agent-mark">✓</span>
          ${badge("acceptance", "active")}
        </div>
        <h3>Проверки PWA</h3>
        ${list(state.pwa.checks)}
      </article>
    </section>
  `;
}

function renderAgents() {
  return `
    <section class="band">
      <div class="section-head">
        <p class="eyebrow">границы ролей</p>
        <h2>Агенты</h2>
      </div>
      <div class="agent-list">
        ${state.agents.map((agent) => `
          <article class="wide-card">
            <div>
              <div class="card-top inline">
                <h3>${escapeHtml(agent.publicLabel)}</h3>
                ${badge(availabilityText(agent), availabilityTone(agent))}
              </div>
              <p>${escapeHtml(agent.role)}</p>
              <p class="muted">${escapeHtml(agent.autonomy)}</p>
              ${agentBoundary(agent)}
            </div>
            <div>
              <h4>Разрешено</h4>
              ${list(agent.allowed)}
            </div>
            <div>
              <h4>Запрещено</h4>
              ${list(agent.blocked)}
            </div>
          </article>
        `).join("")}
      </div>
    </section>
  `;
}

function renderLab() {
  return `
    <section class="band">
      <div class="section-head">
        <p class="eyebrow">концепты</p>
        <h2>Лаборатория</h2>
        <p>Каждый концепт должен иметь назначение, режимы, вход, выход, риск, выключатель, тест и зрелость.</p>
      </div>
      ${table(
        ["Концепт", "Зрелость", "Режимы", "Выход"],
        state.concepts.map((c) => [
          escapeHtml(c.name),
          badge(c.maturity, c.maturity.includes("прототип") || c.maturity.includes("Stage") ? "active" : "neutral"),
          `<code>${escapeHtml(c.modes)}</code>`,
          escapeHtml(c.output)
        ])
      )}
    </section>
  `;
}

function renderUniversity() {
  return `
    <section class="band">
      <div class="section-head">
        <p class="eyebrow">активация и полигон</p>
        <h2>${escapeHtml(state.university.title)}</h2>
        <p>${escapeHtml(state.university.purpose)}</p>
      </div>
      <article class="wide-card two-column">
        <div>
          <div class="card-top inline">
            <h3>Формула</h3>
            ${badge(state.university.mode, "quiet")}
          </div>
          <p class="formula">${escapeHtml(state.university.activationFormula)}</p>
        </div>
        <div>
          <h3>${escapeHtml(state.scienceCoordinator.title)}</h3>
          <p>${escapeHtml(state.scienceCoordinator.role)}</p>
          <p class="muted">${escapeHtml(state.scienceCoordinator.style)}</p>
          <div class="chip-row">
            <code>${escapeHtml(state.scienceCoordinator.defaultMode)}</code>
            <code>${escapeHtml(state.scienceCoordinator.state)}</code>
          </div>
        </div>
      </article>
      <div class="section-gap"></div>
      ${table(
        ["Слой", "Выход", "Защита"],
        state.university.layers.map((layer) => [
          escapeHtml(layer.name),
          escapeHtml(layer.output),
          escapeHtml(layer.guard)
        ])
      )}
      <div class="split-block">
        <article class="card">
          <div class="card-top">
            <span class="agent-mark">П</span>
            ${badge("потоки", "active")}
          </div>
          <h3>Потоки координатора</h3>
          ${table(
            ["Поток", "Выход"],
            state.scienceCoordinator.flows.map((flow) => [
              escapeHtml(flow.name),
              escapeHtml(flow.output)
            ])
          )}
        </article>
        <article class="card">
          <div class="card-top">
            <span class="agent-mark">Г</span>
            ${badge("границы", "guarded")}
          </div>
          <h3>Проверки</h3>
          ${list(state.university.checks)}
          <h3>Нельзя</h3>
          ${list(state.scienceCoordinator.blocked)}
        </article>
      </div>
      <div class="section-gap"></div>
      <div class="status-grid">
        ${state.scienceCoordinator.artifacts.map((artifact) => `
          <article class="card compact-card">
            <div class="card-top">
              <span class="agent-mark">${escapeHtml(artifact.slice(0, 1).toUpperCase())}</span>
              ${badge("артефакт", "neutral")}
            </div>
            <h3>${escapeHtml(artifact)}</h3>
            <p class="muted">Результат считается завершенным только когда его можно проверить как файл, карточку, отчет или запись приемки.</p>
          </article>
        `).join("")}
      </div>
    </section>
  `;
}

function renderHermes() {
  return `
    <section class="band">
      <div class="section-head">
        <p class="eyebrow">профили и реестры</p>
        <h2>${escapeHtml(state.hermesNextGen.title)}</h2>
        <p>${escapeHtml(state.hermesNextGen.purpose)}</p>
      </div>
      <article class="wide-card two-column">
        <div>
          <div class="card-top inline">
            <h3>Принцип</h3>
            ${badge(state.hermesNextGen.mode, "quiet")}
          </div>
          <p>${escapeHtml(state.hermesNextGen.principle)}</p>
        </div>
        <div>
          <h3>Проверки</h3>
          ${list(state.hermesNextGen.checks)}
        </div>
      </article>
      <div class="section-gap"></div>
      ${table(
        ["Слой", "Статус", "Выход", "Защита"],
        state.hermesNextGen.layers.map((layer) => [
          escapeHtml(layer.name),
          badge(layer.status, layer.status === "схема" ? "active" : "neutral"),
          escapeHtml(layer.output),
          escapeHtml(layer.guard)
        ])
      )}
      <div class="split-block">
        <article class="card">
          <div class="card-top">
            <span class="agent-mark">П</span>
            ${badge("приоритеты", "active")}
          </div>
          <h3>Дорожная карта</h3>
          ${table(
            ["Уровень", "Задача"],
            state.hermesNextGen.priorities.map((priority) => [
              `<code>${escapeHtml(priority.level)}</code>`,
              escapeHtml(priority.item)
            ])
          )}
        </article>
        <article class="card">
          <div class="card-top">
            <span class="agent-mark">Ф</span>
            ${badge("примеры", "quiet")}
          </div>
          <h3>Файлы полигона</h3>
          <div class="chip-row">
            ${state.hermesNextGen.examples.map((item) => `<code>${escapeHtml(item)}</code>`).join("")}
          </div>
          <p class="muted">Это безопасные примеры. Они не являются живой конфигурацией Hermes и не включают hooks или plugins.</p>
        </article>
      </div>
      <div class="section-gap"></div>
      <article class="wide-card">
        <div class="card-top inline">
          <h3>${escapeHtml(state.hermesNextGen.artifactViewer.title)}</h3>
          ${badge(state.hermesNextGen.artifactViewer.mode, "quiet")}
        </div>
        <p>${escapeHtml(state.hermesNextGen.artifactViewer.scope)}</p>
        <p class="muted">Команда проверки: <code>${escapeHtml(state.hermesNextGen.artifactViewer.validationCommand)}</code></p>
      </article>
      <div class="split-block">
        <article class="card">
          <div class="card-top">
            <span class="agent-mark">С</span>
            ${badge("схемы", "active")}
          </div>
          <h3>Паспорта и реестры</h3>
          ${table(
            ["Артефакт", "Файл", "Что доказывает"],
            state.hermesNextGen.artifactViewer.schemas.map((item) => [
              escapeHtml(item.name),
              `<code>${escapeHtml(item.file)}</code>`,
              escapeHtml(item.proves)
            ])
          )}
        </article>
        <article class="card">
          <div class="card-top">
            <span class="agent-mark">П</span>
            ${badge("примеры", "quiet")}
          </div>
          <h3>Учебные примеры</h3>
          ${table(
            ["Пример", "Схема", "Статус"],
            state.hermesNextGen.artifactViewer.examples.map((item) => [
              `<code>${escapeHtml(item.file)}</code><br><span class="muted">${escapeHtml(item.name)}</span>`,
              `<code>${escapeHtml(item.schema)}</code>`,
              badge(item.status, "online")
            ])
          )}
        </article>
      </div>
    </section>
  `;
}

function renderRoadmap() {
  return `
    <section class="band">
      <div class="section-head">
        <p class="eyebrow">публичная дорожная карта</p>
        <h2>${escapeHtml(state.roadmap.title)}</h2>
        <p>${escapeHtml(state.roadmap.status)}</p>
      </div>
      <article class="wide-card two-column">
        <div>
          <h3>Формула публикации</h3>
          <p class="formula">${escapeHtml(state.roadmap.formula)}</p>
        </div>
        <div>
          <h3>Фазы</h3>
          ${list(state.roadmap.phases)}
        </div>
      </article>
      <div class="section-gap"></div>
      ${table(
        ["Ticket", "Назначение"],
        state.roadmap.tickets.map((ticket) => [
          `<code>${escapeHtml(ticket)}</code>`,
          escapeHtml(ticketPurpose(ticket))
        ])
      )}
    </section>
  `;
}

function ticketPurpose(ticket) {
  const purposes = {
    public_landing: "короткий README с иллюстрациями и тремя входами: читать, установить, открыть портал",
    install_guide: "единый INSTALL.md с dry-run, apply, rollback и границами installer",
    privacy_boundary: "запрет raw-выгрузок, секретов, приватных путей и восстановимых настроек",
    skill_catalog: "каталог, где installable skills отделены от протоколов, прототипов и концептов",
    portal_visual_review: "визуальная сверка read-only портала и synthetic preview",
    link_check: "проверка Markdown-ссылок без 404",
    secret_scan: "поиск токенов, приватных путей, raw inbox и ledger/database dumps",
    release_artifacts_policy: "решение, какие ZIP/SHA остаются в repo, а какие уходят в GitHub Releases"
  };
  return purposes[ticket] || "следующий рабочий ticket";
}

function renderChannels() {
  return `
    <section class="band">
      <div class="section-head">
        <p class="eyebrow">внешний голос</p>
        <h2>ВК и Google</h2>
        <p>Основной агент может выражать работу через внешние каналы только как подготовку черновиков и планов до ручного подтверждения.</p>
      </div>
      <div class="status-grid">
        ${state.channels.map((channel) => `
          <article class="card">
            <div class="card-top">
              <span class="agent-mark">${escapeHtml(channel.name.slice(0, 1))}</span>
              ${badge(channel.mode, channel.name === "GitHub" ? "active" : "quiet")}
            </div>
            <h3>${escapeHtml(channel.name)}</h3>
            <p>${escapeHtml(channel.purpose)}</p>
            <p><strong>Порог выпуска:</strong> ${escapeHtml(channel.publishGate)}</p>
            <p class="muted"><strong>Нельзя:</strong> ${escapeHtml(channel.blocked)}</p>
          </article>
        `).join("")}
      </div>
    </section>
  `;
}

function renderTriad() {
  return `
    <section class="band">
      <div class="section-head">
        <p class="eyebrow">координационная комната</p>
        <h2>${escapeHtml(state.triad.title)}</h2>
        <p>${escapeHtml(state.triad.purpose)}</p>
      </div>
      <div class="status-grid">
        <article class="card">
          <div class="card-top">
            <span class="agent-mark">L</span>
            ${badge(state.triad.mode, "quiet")}
          </div>
          <h3>Журнал</h3>
          <p>${escapeHtml(state.triad.storage)}</p>
          <p class="muted">Портал показывает только безопасные счетчики и статусы.</p>
        </article>
        <article class="card">
          <div class="card-top">
            <span class="agent-mark">S</span>
            ${badge(state.triad.portalMode, "neutral")}
          </div>
          <h3>Статусы</h3>
          <div class="chip-row">${state.triad.statuses.map((status) => `<code>${escapeHtml(status)}</code>`).join("")}</div>
        </article>
        <article class="card">
          <div class="card-top">
            <span class="agent-mark">G</span>
            ${badge("guards", "active")}
          </div>
          <h3>Границы</h3>
          ${list(state.triad.guards)}
        </article>
      </div>
    </section>
  `;
}

function renderServer() {
  return `
    <section class="band">
      <div class="section-head">
        <p class="eyebrow">инфраструктура</p>
        <h2>Сервер</h2>
        <p>Ubuntu, Docker, NAS и сервисы показываются как состояние и план проверки. Live-действия требуют отдельного окна обслуживания.</p>
      </div>
      ${table(
        ["Контур", "MVP", "Граница"],
        [
          ["Ubuntu", "статус без команд и ссылки на отчеты", "без рестартов"],
          ["Docker", "карточки контейнеров и бэкапов", "без пересборки из портала"],
          ["NAS", "статус наличия резервной копии", "без приватных UNC-путей в публичной версии"],
          ["Сенсоры", "Replay/SQLite и наблюдение", "без живого пути пакетов"]
        ].map((r) => r.map(escapeHtml))
      )}
    </section>
  `;
}

function renderAdmin() {
  const runtime = window.REDNET_DOCKER_STATUS;
  const dockerAgents = Array.isArray(runtime?.services) && runtime.services.length
    ? runtime.services
    : state.admin.dockerAgents;
  const runtimeNote = runtime
    ? `Последний локальный статус выполнения: ${escapeHtml(runtime.generatedAt || "без времени")}`
    : "Локальный статус выполнения не подключен. Статическая карта остается безопасной и пригодной для планирования.";

  return `
    <section class="band">
      <div class="section-head">
        <p class="eyebrow">локальная админка</p>
        <h2>${escapeHtml(state.admin.title)}</h2>
        <p>${escapeHtml(state.admin.purpose)}</p>
        <p class="muted">${runtimeNote}</p>
      </div>
      <div class="status-grid admin-actions">
        ${state.admin.buttons.map((button) => `
          <article class="card compact-card">
            <div class="card-top">
              <span class="agent-mark">${escapeHtml(button.title.slice(0, 1))}</span>
              ${badge(statusLabel(button.state), statusTone(button.state))}
            </div>
            <h3>${escapeHtml(button.title)}</h3>
            <p>${escapeHtml(button.action)}</p>
          </article>
        `).join("")}
      </div>
      ${table(
        ["Сервис", "Среда", "Статус", "Режим", "Точка", "Изоляция", "Защита"],
        dockerAgents.map(dockerDisplay).map((agent) => [
          escapeHtml(agent.label),
          `<code>${escapeHtml(agent.runtime)}</code>`,
          badge(statusLabel(agent.status), statusTone(agent.status)),
          escapeHtml(agent.mode),
          `<code>${escapeHtml(agent.endpoint)}</code>`,
          escapeHtml(dockerIsolation(agent)),
          escapeHtml(agent.guard)
        ])
      )}
      <div class="split-block">
        <article class="card">
          <div class="card-top">
            <span class="agent-mark">N</span>
            ${badge("сеть", "active")}
          </div>
          <h3>Сетевые слои</h3>
        ${table(
            ["Технология", "Статус", "Режим", "Защита"],
            state.admin.networkLayers.map((layer) => [
              escapeHtml(layer.name),
              badge(statusLabel(layer.status), statusTone(layer.status)),
              escapeHtml(layer.mode),
              escapeHtml(layer.guard)
            ])
          )}
        </article>
        <article class="card">
          <div class="card-top">
            <span class="agent-mark">D</span>
            ${badge("проверка", "quiet")}
          </div>
          <h3>Как обновлять монитор</h3>
          <p>Скрипт ${escapeHtml(state.admin.generatedBy)} формирует локальный файл состояния для портала. Он не публикуется и не содержит секретов.</p>
          <p class="muted">Все опасные операции вынесены за пределы портала и требуют отдельного окна обслуживания.</p>
        </article>
      </div>
    </section>
  `;
}

function renderSkillbook() {
  return `
    <section class="band">
      <div class="section-head">
        <p class="eyebrow">модули</p>
        <h2>Skillbook</h2>
        <p>Пакеты навыков устанавливаются модульно, проверочный запуск по умолчанию, без изменения живого Hermes.</p>
      </div>
      ${table(
        ["Слой", "Назначение", "Статус"],
        [
          ["skills/", "готовые Hermes/Codex-style навыки", "пакет"],
          ["protocols/", "сеансовое сопровождение и отключение", "пакет"],
          ["sensor-prototype/", "сенсоры только наблюдения", "прототип"],
          ["packages/hermes/", "манифест и проверочный установщик", "пакет"],
          ["docs/", "публичная рамка и отчеты", "документация"]
        ].map((r) => r.map(escapeHtml))
      )}
      <div class="section-gap"></div>
      <article class="wide-card two-column">
        <div>
          <h3>${escapeHtml(state.metaSkills.title)}</h3>
          <div class="chip-row">
            ${badge(state.metaSkills.mode, "quiet")}
            <code>${escapeHtml(state.metaSkills.count)} навыков</code>
          </div>
          <p>Слой <code>rednet-meta</code> подключен к научному координатору как карта рекомендаций, без автозагрузки и без live-команд.</p>
        </div>
        <div class="chip-row">
          <code>${escapeHtml(state.metaSkills.package)}</code>
          <code>${escapeHtml(state.metaSkills.map)}</code>
        </div>
      </article>
      <div class="split-block">
        <article class="card">
          <div class="card-top">
            <span class="agent-mark">М</span>
            ${badge("toolkit", "active")}
          </div>
          <h3>Группы мета-навыков</h3>
          <div class="meta-skill-list">
            ${state.metaSkills.groups.map((group) => `
              <div class="meta-skill-row">
                <strong>${escapeHtml(group.name)}</strong>
                <code>${escapeHtml(group.skills)}</code>
                <span class="muted">${escapeHtml(group.output)}</span>
              </div>
            `).join("")}
          </div>
        </article>
        <article class="card">
          <div class="card-top">
            <span class="agent-mark">G</span>
            ${badge("guards", "guarded")}
          </div>
          <h3>Границы</h3>
          ${list(state.metaSkills.guards)}
        </article>
      </div>
    </section>
  `;
}

function renderSubagents() {
  return `
    <section class="band">
      <div class="section-head">
        <p class="eyebrow">научные сотрудники</p>
        <h2>Сабагенты</h2>
        <p>Сабагент возвращает артефакт: карточку, отчет, тест, протокол, список рисков или решение.</p>
      </div>
      ${table(
        ["Роль", "Артефакт", "Защита"],
        state.subagents.map((s) => [escapeHtml(s.role), escapeHtml(s.output), escapeHtml(s.guard)])
      )}
    </section>
  `;
}

function renderChecks() {
  return `
    <section class="band">
      <div class="section-head">
        <p class="eyebrow">приемка</p>
        <h2>Проверки</h2>
      </div>
      <div class="check-list">
        ${state.checks.map((check) => `<div class="check-item"><span></span>${escapeHtml(check)}</div>`).join("")}
      </div>
    </section>
  `;
}

const renderers = {
  overview: renderOverview,
  repo: renderRepository,
  pwa: renderPwa,
  agents: renderAgents,
  lab: renderLab,
  university: renderUniversity,
  hermes: renderHermes,
  roadmap: renderRoadmap,
  channels: renderChannels,
  triad: renderTriad,
  server: renderServer,
  admin: renderAdmin,
  skillbook: renderSkillbook,
  subagents: renderSubagents,
  checks: renderChecks
};

function setTab(id, focusContent = false) {
  const renderer = renderers[id] || renderOverview;
  document.querySelectorAll(".tab").forEach((button) => {
    const active = button.dataset.tab === id;
    button.classList.toggle("active", active);
    button.setAttribute("aria-selected", String(active));
  });
  root.innerHTML = renderer();
  window.location.hash = id;
  if (focusContent) {
    root.focus({ preventScroll: true });
  }
}

function maybeLoadRuntimeStatus() {
  const params = new URLSearchParams(window.location.search);
  if (params.get("runtime") !== "local") {
    return Promise.resolve();
  }
  return new Promise((resolve) => {
    const script = document.createElement("script");
    script.src = "runtime/docker-status.local.js";
    script.async = true;
    script.onload = resolve;
    script.onerror = resolve;
    document.head.appendChild(script);
  });
}

function updatePwaStatus(message, tone = "") {
  const status = document.querySelector("#pwaStatus");
  if (!status) {
    return;
  }
  status.textContent = message;
  status.classList.toggle("is-ready", tone === "ready");
  status.classList.toggle("is-offline", tone === "offline");
}

function initPwa() {
  const installButton = document.querySelector("#installPwa");
  let deferredPrompt = null;

  const updateOnlineState = () => {
    if (!navigator.onLine) {
      updatePwaStatus("offline режим", "offline");
    } else if (navigator.serviceWorker?.controller) {
      updatePwaStatus("PWA offline-ready", "ready");
    } else {
      updatePwaStatus("PWA доступна", "");
    }
  };

  window.addEventListener("online", updateOnlineState);
  window.addEventListener("offline", updateOnlineState);

  window.addEventListener("beforeinstallprompt", (event) => {
    event.preventDefault();
    deferredPrompt = event;
    if (installButton) {
      installButton.hidden = false;
    }
  });

  installButton?.addEventListener("click", async () => {
    if (!deferredPrompt) {
      updatePwaStatus("установка через меню браузера", "");
      return;
    }
    deferredPrompt.prompt();
    await deferredPrompt.userChoice;
    deferredPrompt = null;
    installButton.hidden = true;
    updatePwaStatus("PWA установлена/открыта", "ready");
  });

  if (!("serviceWorker" in navigator)) {
    updatePwaStatus("SW не поддержан", "offline");
    return;
  }

  if (window.location.protocol === "file:") {
    updatePwaStatus("PWA через localhost", "");
    return;
  }

  navigator.serviceWorker.register("sw.js")
    .then(() => navigator.serviceWorker.ready)
    .then(() => updatePwaStatus("PWA offline-ready", "ready"))
    .catch(() => updatePwaStatus("PWA только online", ""))
    .finally(updateOnlineState);
}

function init() {
  nav.innerHTML = tabs.map((tab) => `
    <button class="tab" type="button" role="tab" aria-selected="false" data-tab="${tab.id}">${icon(tab.icon)}<span>${escapeHtml(tab.title)}</span></button>
  `).join("");
  nav.setAttribute("role", "tablist");
  nav.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-tab]");
    if (button) {
      setTab(button.dataset.tab, true);
    }
  });
  window.addEventListener("hashchange", () => {
    const next = window.location.hash.slice(1);
    if (tabs.some((tab) => tab.id === next)) {
      setTab(next);
    }
  });
  const initial = tabs.some((tab) => `#${tab.id}` === window.location.hash)
    ? window.location.hash.slice(1)
    : "overview";
  setTab(initial);
  initPwa();
}

maybeLoadRuntimeStatus().then(init);
