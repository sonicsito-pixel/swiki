if (typeof mermaid !== 'undefined') {
  mermaid.initialize({
    startOnLoad: false,
    theme: 'default',
    securityLevel: 'loose'
  });
}

const state = {
  pages: [],
  summary: null,
  graph: null,
  selectedPage: "questions/fone-core-resource-priority.md",
  nfsm: {
    loaded: false,
    pages: [],
    selectedPath: "",
    title: "신성통상 차세대 패션관리시스템 개발",
    obsidianVault: "신성통상 차세대 패션관리시스템 개발",
  },
};

const $ = (id) => document.getElementById(id);
const pendingRawOpen = new Set();

const TYPE_LABELS = {
  concept: "개념",
  entity: "대상",
  source: "원문 요약",
  question: "질문",
  resource: "리소스",
  registry: "자료 목록",
  dashboard: "대시보드",
  overview: "전체 개요",
  index: "목차",
  log: "작업 기록",
  "pending-ingest": "정리 대기열",
  "lint-report": "점검 보고서",
  page: "문서",
};

function typeLabel(type) {
  return TYPE_LABELS[type] || type || "문서";
}

const HIDDEN_WEB_PATHS = new Set([
  "index.md",
  "log.md",
  "obsidian-home.md",
  "overview.md",
  "pending-ingest.md",
  "source-registry.md",
  "concepts/persistent-knowledge-wiki.md",
  "entities/obsidian.md",
  "questions/how-should-this-wiki-start.md",
  "sources/sample-source-summary.md",
]);

const HIDDEN_WEB_TYPES = new Set(["dashboard", "index", "lint-report", "log", "pending-ingest", "registry"]);

function isUserVisible(page) {
  if (!page) return false;
  if (page.path.startsWith("_templates/")) return false;
  if (page.path.endsWith("/README.md")) return false;
  if (HIDDEN_WEB_PATHS.has(page.path)) return false;
  if (HIDDEN_WEB_TYPES.has(page.type)) return false;
  return true;
}

function visiblePages() {
  return state.pages.filter(isUserVisible);
}

function documentPages() {
  return visiblePages().filter((page) => page.type !== "resource");
}

function resourcePages() {
  return visiblePages().filter((page) => page.type === "resource");
}

function insightPages() {
  return documentPages().filter((page) => ["concept", "entity", "question", "source-summary"].includes(page.type));
}

async function api(path, options) {
  const res = await fetch(path, options);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

function setStatus(text) {
  $("serviceState").textContent = text;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function inlineMarkdown(text) {
  return escapeHtml(text)
    .replace(/\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]/g, (_, target, label) => {
      const title = label || target;
      const page = pageFromTarget(target);
      if (page && !isUserVisible(page)) return escapeHtml(title);
      const raw = page?.sourcePath ? ` <button type="button" class="raw-inline-link" data-source-path="${escapeHtml(page.sourcePath)}">로컬</button>` : "";
      return `<a href="#" class="wiki-link" data-target="${escapeHtml(target)}">${escapeHtml(title)}</a>${raw}`;
    })
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noreferrer">$1</a>')
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/`([^`]+)`/g, "<code>$1</code>");
}

function renderMarkdown(md) {
  const text = md.replace(/^---[\s\S]*?---\s*/, "");
  const lines = text.split(/\r?\n/);
  const html = [];
  let list = false;
  let table = [];
  let code = false; // false, 'mermaid', or 'normal'
  let codeLines = [];

  function flushList() {
    if (list) {
      html.push("</ul>");
      list = false;
    }
  }

  function flushTable() {
    if (!table.length) return;
    const rows = table
      .filter((row) => !/^\|\s*-/.test(row))
      .map((row, idx) => {
        const tag = idx === 0 ? "th" : "td";
        const cells = row
          .split("|")
          .slice(1, -1)
          .map((cell) => `<${tag}>${inlineMarkdown(cell.trim())}</${tag}>`)
          .join("");
        return `<tr>${cells}</tr>`;
      })
      .join("");
    html.push(`<table>${rows}</table>`);
    table = [];
  }

  for (const line of lines) {
    if (line.startsWith("```")) {
      flushList();
      flushTable();
      if (code) {
        if (code === "mermaid") {
          html.push(`<div class="mermaid">${escapeHtml(codeLines.join("\n"))}</div>`);
        } else {
          html.push(`<pre><code>${escapeHtml(codeLines.join("\n"))}</code></pre>`);
        }
        codeLines = [];
        code = false;
      } else {
        const type = line.slice(3).trim().toLowerCase();
        code = type === "mermaid" ? "mermaid" : "normal";
      }
      continue;
    }
    if (code) {
      codeLines.push(line);
      continue;
    }
    if (/^\|.+\|$/.test(line.trim())) {
      flushList();
      table.push(line.trim());
      continue;
    }
    flushTable();
    if (/^#\s+/.test(line)) {
      flushList();
      html.push(`<h1>${inlineMarkdown(line.replace(/^#\s+/, ""))}</h1>`);
    } else if (/^##\s+/.test(line)) {
      flushList();
      html.push(`<h2>${inlineMarkdown(line.replace(/^##\s+/, ""))}</h2>`);
    } else if (/^###\s+/.test(line)) {
      flushList();
      html.push(`<h3>${inlineMarkdown(line.replace(/^###\s+/, ""))}</h3>`);
    } else if (/^-\s+/.test(line)) {
      if (!list) {
        html.push("<ul>");
        list = true;
      }
      html.push(`<li>${inlineMarkdown(line.replace(/^-\s+/, ""))}</li>`);
    } else if (!line.trim()) {
      flushList();
    } else {
      flushList();
      html.push(`<p>${inlineMarkdown(line)}</p>`);
    }
  }
  flushList();
  flushTable();
  return html.join("\n");
}

function pageFromTarget(target) {
  const normalized = target.trim().toLowerCase();
  const exact = state.pages.find((p) => p.path.replace(/\.md$/i, "").toLowerCase() === normalized);
  if (exact) return exact;
  return state.pages.find((p) => p.path.split("/").at(-1).replace(/\.md$/i, "").toLowerCase() === normalized);
}

function pathFromTarget(target) {
  return pageFromTarget(target)?.path || `${target}.md`;
}

function rawAction(page) {
  if (!page?.sourcePath) return "";
  return `<button type="button" class="raw-link" data-source-path="${escapeHtml(page.sourcePath)}" title="${escapeHtml(page.localPath || page.sourcePath)}">로컬 파일 열기</button>`;
}

function rawLinkFromEvent(event) {
  if (!(event.target instanceof Element)) return null;
  return event.target.closest(".raw-link, .raw-inline-link, .raw-file-link");
}

async function openRawFile(link) {
  const sourcePath = link.dataset.sourcePath;
  if (!sourcePath || pendingRawOpen.has(sourcePath)) return;
  pendingRawOpen.add(sourcePath);
  link.disabled = true;
  try {
    setStatus("로컬 파일 여는 중");
    await api("/api/open-file", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ sourcePath }),
    });
    setStatus("로컬 파일 열기 요청됨");
  } catch (error) {
    setStatus(error.message);
  } finally {
    link.disabled = false;
    setTimeout(() => pendingRawOpen.delete(sourcePath), 800);
  }
}

function attachRawLinks() {
  // Raw file buttons are handled by the delegated click listener in bindEvents().
}

async function loadPage(path) {
  const page = await api(`/api/page?path=${encodeURIComponent(path)}`);
  state.selectedPage = page.path;
  $("docTitle").textContent = page.title;
  $("docPath").textContent = page.path;
  const docBody = $("docBody");
  docBody.innerHTML = renderMarkdown(page.markdown);
  docBody.scrollTop = 0;
  const vault = encodeURIComponent("llm_wiki");
  const file = encodeURIComponent(page.path);
  $("obsidianLink").href = `obsidian://open?vault=${vault}&file=${file}`;
  $("rawFileLink").style.display = page.sourcePath ? "inline-flex" : "none";
  $("rawFileLink").dataset.sourcePath = page.sourcePath || "";
  $("rawFileLink").title = page.localPath || page.sourcePath || "";
  attachRawLinks($("rawFileLink").parentElement);
  attachWikiLinks($("docBody"));
  attachRawLinks($("docBody"));

  // Mermaid 렌더링 트리거
  if (typeof mermaid !== 'undefined') {
    try {
      if (typeof mermaid.run === 'function') {
        await mermaid.run({
          nodes: document.querySelectorAll('.mermaid')
        });
      } else if (typeof mermaid.init === 'function') {
        mermaid.init(undefined, document.querySelectorAll('.mermaid'));
      }
    } catch (error) {
      console.error("Mermaid 렌더링 에러:", error);
    }
  }
}

async function loadNfsmPages(force = false) {
  if (state.nfsm.loaded && !force) {
    renderNfsmList();
    return;
  }
  try {
    $("nfsmMeta").textContent = "프로젝트 문서 불러오는 중";
    $("nfsmList").innerHTML = "";
    const vault = await api("/api/vault/nfsm/pages");
    state.nfsm.loaded = true;
    state.nfsm.pages = vault.pages || [];
    state.nfsm.title = vault.title || state.nfsm.title;
    state.nfsm.obsidianVault = vault.obsidianVault || state.nfsm.obsidianVault;
    renderNfsmList();
    if (!state.nfsm.selectedPath && state.nfsm.pages.length) {
      const first = state.nfsm.pages.find((page) => page.path === "README.md") || state.nfsm.pages[0];
      await loadNfsmPage(first.path);
    }
    if (!state.nfsm.pages.length) {
      $("nfsmMeta").textContent = "연결된 vault에서 Markdown 문서를 찾지 못했습니다.";
      $("nfsmBody").innerHTML = `<p>연결 경로를 확인해주세요: <code>C:\\supersonic\\projects\\nfsm</code></p>`;
    }
  } catch (error) {
    state.nfsm.loaded = false;
    $("nfsmMeta").textContent = `프로젝트 WIKI를 불러오지 못했습니다: ${error.message}`;
    $("nfsmBody").innerHTML = `<p>NFSM vault 연결을 확인해주세요.</p><pre><code>${escapeHtml(error.message)}</code></pre>`;
    setStatus(error.message);
  }
}

function renderNfsmList() {
  const q = ($("nfsmFilter")?.value || "").trim().toLowerCase();
  const pages = state.nfsm.pages.filter((page) => `${page.title} ${page.path} ${page.excerpt}`.toLowerCase().includes(q));
  $("nfsmList").innerHTML = pages
    .map((page) => `<div class="page-item" data-path="${escapeHtml(page.path)}"><strong>${escapeHtml(page.title)}</strong><span>${escapeHtml(page.type)} · ${escapeHtml(page.path)}</span></div>`)
    .join("") || `<div class="empty-note">검색 조건에 맞는 프로젝트 문서가 없습니다.</div>`;
  $("nfsmList").querySelectorAll(".page-item").forEach((el) => {
    el.addEventListener("click", () => loadNfsmPage(el.dataset.path).catch((error) => setStatus(error.message)));
  });
  $("nfsmMeta").textContent = `${pages.length}개 표시 · 전체 ${state.nfsm.pages.length}개 Markdown 문서`;
}

async function loadNfsmPage(path) {
  const page = await api(`/api/vault/nfsm/page?path=${encodeURIComponent(path)}`);
  state.nfsm.selectedPath = page.path;
  $("nfsmTitle").textContent = page.title;
  $("nfsmPath").textContent = page.path;
  const body = $("nfsmBody");
  body.innerHTML = renderMarkdown(page.markdown);
  body.scrollTop = 0;
  const vault = encodeURIComponent(page.obsidianVault || state.nfsm.obsidianVault);
  const file = encodeURIComponent(page.path);
  $("nfsmObsidianLink").href = `obsidian://open?vault=${vault}&file=${file}`;
  $("openNfsmFile").dataset.path = page.path;
  attachNfsmLinks(body);
}

async function openNfsmPath(path = "") {
  await api("/api/vault/nfsm/open", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ vault: "nfsm", path }),
  });
  setStatus(path ? "프로젝트 파일 열기 요청됨" : "프로젝트 폴더 열기 요청됨");
}

function nfsmPageFromTarget(target) {
  const normalized = decodeURIComponent(target || "")
    .replace(/\\/g, "/")
    .replace(/\.md$/i, "")
    .toLowerCase();
  const currentDir = state.nfsm.selectedPath.split("/").slice(0, -1).join("/");
  const relative = currentDir ? `${currentDir}/${normalized}` : normalized;
  return state.nfsm.pages.find((page) => page.path.replace(/\.md$/i, "").toLowerCase() === normalized)
    || state.nfsm.pages.find((page) => page.path.replace(/\.md$/i, "").toLowerCase() === relative)
    || state.nfsm.pages.find((page) => page.path.split("/").at(-1).replace(/\.md$/i, "").toLowerCase() === normalized.split("/").at(-1));
}

function attachNfsmLinks(root) {
  root.querySelectorAll(".wiki-link").forEach((link) => {
    link.addEventListener("click", (event) => {
      const page = nfsmPageFromTarget(link.dataset.target);
      if (!page) return;
      event.preventDefault();
      loadNfsmPage(page.path).catch((error) => setStatus(error.message));
    });
  });
  root.querySelectorAll("a[href]").forEach((link) => {
    const href = link.getAttribute("href") || "";
    if (/^(https?:|obsidian:|file:|#)/i.test(href) || !/\.md(?:#.*)?$/i.test(href)) return;
    link.addEventListener("click", (event) => {
      const clean = href.replace(/#.*$/, "");
      const page = nfsmPageFromTarget(clean);
      if (!page) return;
      event.preventDefault();
      loadNfsmPage(page.path).catch((error) => setStatus(error.message));
    });
  });
}

function attachWikiLinks(root) {
  root.querySelectorAll(".wiki-link").forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      const path = pathFromTarget(link.dataset.target);
      showView("wiki");
      loadPage(path).catch((error) => setStatus(error.message));
    });
  });
}

function showView(name) {
  document.querySelectorAll(".view").forEach((el) => el.classList.remove("active"));
  $(`${name}View`).classList.add("active");
  document.querySelectorAll(".nav-item").forEach((el) => el.classList.toggle("active", el.dataset.view === name));
  if (name === "nfsm") loadNfsmPages().catch((error) => setStatus(error.message));
  if (name === "graph") setTimeout(drawGraph, 30);
}

function setCollapsibleState(button, expanded) {
  const target = $(button.dataset.target);
  if (!target) return;
  target.classList.toggle("collapsed", !expanded);
  button.setAttribute("aria-expanded", String(expanded));
  button.textContent = expanded ? "접기" : "펼치기";
}

function setCollapsibleTarget(targetId, expanded) {
  const button = document.querySelector(`.collapse-toggle[data-target="${targetId}"]`);
  if (!button) return;
  setCollapsibleState(button, expanded);
}

function setSidebarCollapsed(collapsed, persist = true) {
  document.body.classList.toggle("sidebar-collapsed", collapsed);
  const button = $("sidebarToggle");
  if (button) {
    button.setAttribute("aria-expanded", String(!collapsed));
    button.textContent = collapsed ? "›" : "‹";
    button.title = collapsed ? "왼쪽 메뉴 펼치기" : "왼쪽 메뉴 접기";
    button.setAttribute("aria-label", button.title);
  }
  if (persist) localStorage.setItem("llmWikiSidebarCollapsed", collapsed ? "1" : "0");
}

function setWikiListCollapsed(collapsed, persist = true) {
  document.body.classList.toggle("wiki-list-collapsed", collapsed);
  const button = $("wikiListToggle");
  if (button) {
    button.setAttribute("aria-expanded", String(!collapsed));
    $("wikiListPanel")?.setAttribute("aria-hidden", String(collapsed));
    button.querySelector(".split-toggle-icon").textContent = collapsed ? "›" : "‹";
    button.title = collapsed ? "문서 목록 펼치기" : "문서 목록 접기";
    button.setAttribute("aria-label", button.title);
  }
  if (persist) localStorage.setItem("llmWikiListCollapsed", collapsed ? "1" : "0");
}

function restoreLayoutState() {
  setSidebarCollapsed(localStorage.getItem("llmWikiSidebarCollapsed") === "1", false);
  setWikiListCollapsed(localStorage.getItem("llmWikiListCollapsed") === "1", false);
}

function bindCollapsibles() {
  document.querySelectorAll(".collapse-toggle").forEach((button) => {
    setCollapsibleState(button, false);
  });
}

document.addEventListener("click", (event) => {
  const button = event.target instanceof Element ? event.target.closest(".collapse-toggle") : null;
  if (!button) return;
  const expanded = button.getAttribute("aria-expanded") === "true";
  setCollapsibleState(button, !expanded);
});

function renderStats() {
  const docs = documentPages();
  const resources = resourcePages();
  const insights = insightPages();
  const focusResources = state.summary.focus
    .map((path) => state.pages.find((page) => page.path === path))
    .filter((page) => page?.type === "resource").length;
  $("metricResources").textContent = resources.length;
  $("metricPages").textContent = docs.length;
  $("metricPending").textContent = insights.length;
  const stats = [
    ["열 수 있는 자료", resources.length, "로컬 파일로 바로 여는 원본"],
    ["읽기 좋은 요약", docs.length, "흐름을 파악하기 위한 정리"],
    ["이어진 맥락", insights.length, "개념, 대상, 질문"],
    ["추천 자료", focusResources, "먼저 보면 좋은 핵심 원본"],
  ];
  $("statsGrid").innerHTML = stats
    .map(([label, value, hint]) => `<div class="stat"><b>${value}</b><span>${label}</span><small>${hint}</small></div>`)
    .join("");
}

function renderFocus() {
  $("focusList").innerHTML = state.summary.focus
    .map((path) => {
      const page = state.pages.find((p) => p.path === path);
      if (!isUserVisible(page)) return "";
      return `<div class="item" data-path="${page.path}"><strong>${escapeHtml(page.title)}</strong><span>${escapeHtml(page.excerpt)}</span>${rawAction(page)}</div>`;
    })
    .join("");
  $("focusList").querySelectorAll(".item").forEach((el) => {
    el.addEventListener("click", (event) => {
      if (event.target.closest("a,button")) return;
      showView("wiki");
      loadPage(el.dataset.path);
    });
  });
  attachRawLinks($("focusList"));
  $("recentLog").innerHTML = insightPages()
    .filter((page) => page.type !== "resource")
    .slice(0, 10)
    .map((page) => `<div class="item" data-path="${page.path}"><strong>${escapeHtml(page.title)}</strong><span>${escapeHtml(typeLabel(page.type))} · ${escapeHtml(page.excerpt)}</span></div>`)
    .join("");
  $("recentLog").querySelectorAll(".item").forEach((el) => {
    el.addEventListener("click", () => {
      showView("wiki");
      loadPage(el.dataset.path);
    });
  });
}

function renderPageList() {
  const type = $("typeFilter").value;
  const q = $("pageFilter").value.toLowerCase();
  const pages = documentPages().filter((p) => (!type || p.type === type) && `${p.title} ${p.path}`.toLowerCase().includes(q));
  $("pageList").innerHTML = pages
    .map((p) => `<div class="page-item" data-path="${p.path}"><strong>${escapeHtml(p.title)}</strong><span>${escapeHtml(typeLabel(p.type))} · ${escapeHtml(p.path)}</span>${rawAction(p)}</div>`)
    .join("");
  $("pageList").querySelectorAll(".page-item").forEach((el) => el.addEventListener("click", (event) => {
    if (event.target.closest("a,button")) return;
    loadPage(el.dataset.path);
  }));
  attachRawLinks($("pageList"));
}

function renderTypeFilter() {
  const types = [...new Set(documentPages().map((p) => p.type))].sort();
  $("typeFilter").innerHTML = `<option value="">전체 유형</option>` + types.map((type) => `<option value="${type}">${typeLabel(type)}</option>`).join("");
}

async function renderRegistry() {
  const q = ($("resourceFilter")?.value || "").toLowerCase();
  const resources = resourcePages()
    .filter((page) => `${page.title} ${page.sourcePath || ""} ${page.extension || ""}`.toLowerCase().includes(q))
    .sort((a, b) => a.title.localeCompare(b.title));
  $("registryTable").innerHTML = resources
    .map((page) => `<div class="resource-card" data-path="${page.path}">
      <strong>${escapeHtml(page.title)}</strong>
      <span>${escapeHtml(page.extension || "파일")} · ${escapeHtml(page.sourcePath || page.path)}</span>
      ${rawAction(page)}
    </div>`)
    .join("");
  $("registryTable").querySelectorAll(".resource-card").forEach((el) => {
    el.addEventListener("click", (event) => {
      if (event.target.closest("button")) return;
      showView("wiki");
      loadPage(el.dataset.path);
    });
  });
  attachRawLinks($("registryTable"));
}

async function runSearch(q) {
  const query = q.trim();
  if (!query) {
    $("searchMeta").textContent = "검색 전";
    $("searchResults").innerHTML = "";
    setCollapsibleTarget("searchResults", false);
    return;
  }
  const results = (await api(`/api/search?q=${encodeURIComponent(query)}`)).filter(isUserVisible);
  $("searchMeta").textContent = `${results.length}건`;
  $("searchResults").innerHTML = results
    .map((p) => `<div class="item" data-path="${p.path}"><strong>${escapeHtml(p.title)}</strong><span>${escapeHtml(p.excerpt)}</span>${rawAction(p)}</div>`)
    .join("");
  setCollapsibleTarget("searchResults", true);
  $("searchResults").querySelectorAll(".item").forEach((el) => {
    el.addEventListener("click", (event) => {
      if (event.target.closest("a,button")) return;
      showView("wiki");
      loadPage(el.dataset.path);
    });
  });
  attachRawLinks($("searchResults"));
}

function graphType(node) {
  if (node.path.startsWith("concepts/")) return "concept";
  if (node.path.startsWith("entities/")) return "entity";
  if (node.path.startsWith("sources/")) return "source";
  if (node.path.startsWith("questions/")) return "question";
  return node.type || "page";
}

function shouldShowGraphNode(node) {
  if (!isUserVisible(node)) return false;
  if (node.path.startsWith("resources/auto/")) return false;
  if (node.path.startsWith("_templates/")) return false;
  if (node.path.endsWith("/README.md")) return false;
  if (["log", "registry", "pending-ingest"].includes(node.type)) return false;
  return true;
}

function truncateLabel(text, max = 16) {
  return text.length > max ? `${text.slice(0, max - 1)}…` : text;
}

function groupLimit(group) {
  return {
    concept: 10,
    entity: 10,
    question: 8,
    source: 8,
    page: 4,
    overview: 2,
    index: 1,
    dashboard: 1,
  }[group] || 4;
}

function graphNodeRank(node) {
  const groupWeight = {
    concept: 5,
    entity: 5,
    question: 4,
    source: 3,
    page: 2,
    overview: 1,
    index: 1,
    dashboard: 1,
  }[node.group] || 1;
  const focusWeight = state.summary?.focus?.includes(node.path) ? 5 : 0;
  return node.degree * 10 + groupWeight + focusWeight;
}

function pickCoreGraphNodes(nodes) {
  const picked = [];
  const byGroup = new Map();
  const sorted = [...nodes].sort((a, b) => graphNodeRank(b) - graphNodeRank(a) || a.title.localeCompare(b.title));
  for (const node of sorted) {
    if (node.degree <= 0 && !["overview", "index", "dashboard"].includes(node.group)) continue;
    const count = byGroup.get(node.group) || 0;
    if (count >= groupLimit(node.group)) continue;
    picked.push(node);
    byGroup.set(node.group, count + 1);
  }
  return picked.slice(0, 36);
}

function pickCoreGraphEdges(edges, visiblePaths) {
  return edges
    .filter((edge) => visiblePaths.has(edge.source) && visiblePaths.has(edge.target))
    .sort((a, b) => {
      const ar = graphNodeRank(a.sourceNode) + graphNodeRank(a.targetNode);
      const br = graphNodeRank(b.sourceNode) + graphNodeRank(b.targetNode);
      return br - ar;
    })
    .slice(0, 52);
}

function buildGraphLayout(nodes, edges, width, height) {
  const center = { x: width * 0.5, y: height * 0.52 };
  const anchors = {
    overview: { x: width * 0.5, y: height * 0.13 },
    index: { x: width * 0.5, y: height * 0.13 },
    dashboard: { x: width * 0.5, y: height * 0.13 },
    source: { x: width * 0.18, y: height * 0.5 },
    concept: { x: width * 0.46, y: height * 0.44 },
    entity: { x: width * 0.76, y: height * 0.42 },
    question: { x: width * 0.58, y: height * 0.78 },
    page: { x: width * 0.28, y: height * 0.78 },
  };

  nodes.forEach((node, index) => {
    const anchor = anchors[node.group] || center;
    const angle = (index * 2.399963229728653) % (Math.PI * 2);
    const spread = 34 + (index % 6) * 20;
    node.x = anchor.x + Math.cos(angle) * spread;
    node.y = anchor.y + Math.sin(angle) * spread;
    node.vx = 0;
    node.vy = 0;
  });

  for (let step = 0; step < 180; step += 1) {
    for (let i = 0; i < nodes.length; i += 1) {
      const a = nodes[i];
      for (let j = i + 1; j < nodes.length; j += 1) {
        const b = nodes[j];
        const dx = a.x - b.x || 0.1;
        const dy = a.y - b.y || 0.1;
        const distance2 = Math.max(120, dx * dx + dy * dy);
        const force = 2400 / distance2;
        const fx = dx * force;
        const fy = dy * force;
        a.vx += fx;
        a.vy += fy;
        b.vx -= fx;
        b.vy -= fy;
      }
    }

    for (const edge of edges) {
      const a = edge.sourceNode;
      const b = edge.targetNode;
      const dx = b.x - a.x;
      const dy = b.y - a.y;
      const distance = Math.max(1, Math.hypot(dx, dy));
      const desired = 170;
      const force = (distance - desired) * 0.009;
      const fx = (dx / distance) * force;
      const fy = (dy / distance) * force;
      a.vx += fx;
      a.vy += fy;
      b.vx -= fx;
      b.vy -= fy;
    }

    for (const node of nodes) {
      const anchor = anchors[node.group] || center;
      node.vx += (anchor.x - node.x) * 0.009;
      node.vy += (anchor.y - node.y) * 0.009;
      node.x += node.vx;
      node.y += node.vy;
      node.vx *= 0.72;
      node.vy *= 0.72;
      node.x = Math.max(112, Math.min(width - 150, node.x));
      node.y = Math.max(82, Math.min(height - 74, node.y));
    }
  }
}

let hoveredNode = null;
let canvasNodes = [];

function handleGraphMouseMove(event) {
  const canvas = $("graphCanvas");
  if (!canvas || !canvasNodes.length) return;
  const rect = canvas.getBoundingClientRect();
  
  // 마우스 위치 계산 (CSS 픽셀 단위)
  const mx = event.clientX - rect.left;
  const my = event.clientY - rect.top;
  
  let found = null;
  for (let i = canvasNodes.length - 1; i >= 0; i--) {
    const node = canvasNodes[i];
    const dx = mx - node.x;
    const dy = my - node.y;
    const dist = Math.hypot(dx, dy);
    if (dist <= (node.radius || 10) + 5) {
      found = node;
      break;
    }
  }
  
  if (found !== hoveredNode) {
    hoveredNode = found;
    canvas.style.cursor = hoveredNode ? "pointer" : "default";
    drawGraph();
  }
}

function handleGraphMouseLeave() {
  if (hoveredNode) {
    hoveredNode = null;
    const canvas = $("graphCanvas");
    if (canvas) canvas.style.cursor = "default";
    drawGraph();
  }
}

async function handleGraphClick(event) {
  const canvas = $("graphCanvas");
  if (!canvas || !canvasNodes.length) return;
  const rect = canvas.getBoundingClientRect();
  const mx = event.clientX - rect.left;
  const my = event.clientY - rect.top;
  
  let clicked = null;
  for (let i = canvasNodes.length - 1; i >= 0; i--) {
    const node = canvasNodes[i];
    const dx = mx - node.x;
    const dy = my - node.y;
    const dist = Math.hypot(dx, dy);
    if (dist <= (node.radius || 10) + 5) {
      clicked = node;
      break;
    }
  }
  
  if (clicked) {
    showView("wiki");
    try {
      setStatus("문서 로드 중");
      await loadPage(clicked.path);
      setStatus("준비됨");
    } catch (err) {
      setStatus(err.message);
    }
  }
}

function drawRoundLabelCustom(ctx, text, x, y, bgFill, textFill, borderFill, isFontBold = false) {
  const box = roundLabelBox(ctx, text, x, y, isFontBold);
  drawRoundLabelBox(ctx, text, box, bgFill, textFill, borderFill, isFontBold);
}

function roundLabelBox(ctx, text, x, y, isFontBold = false) {
  const paddingX = 8;
  ctx.font = isFontBold
    ? 'bold 12px "Segoe UI", "Malgun Gothic", Arial, sans-serif'
    : '12px "Segoe UI", "Malgun Gothic", Arial, sans-serif';
  const metrics = ctx.measureText(text);
  const boxWidth = metrics.width + paddingX * 2;
  const boxHeight = 22;
  const canvasWidth = ctx.canvas.getBoundingClientRect().width || ctx.canvas.width;
  const left = Math.max(8, Math.min(canvasWidth - boxWidth - 8, x + 8));
  const top = y - boxHeight / 2;
  return { left, top, width: boxWidth, height: boxHeight, paddingX };
}

function boxesOverlap(a, b, gap = 4) {
  return a.left < b.left + b.width + gap
    && a.left + a.width + gap > b.left
    && a.top < b.top + b.height + gap
    && a.top + a.height + gap > b.top;
}

function drawRoundLabelBox(ctx, text, box, bgFill, textFill, borderFill, isFontBold = false) {
  ctx.save();
  ctx.font = isFontBold
    ? 'bold 12px "Segoe UI", "Malgun Gothic", Arial, sans-serif'
    : '12px "Segoe UI", "Malgun Gothic", Arial, sans-serif';
  
  ctx.fillStyle = bgFill;
  ctx.strokeStyle = borderFill;
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.roundRect(box.left, box.top, box.width, box.height, 6);
  ctx.fill();
  ctx.stroke();
  
  ctx.fillStyle = textFill;
  ctx.textBaseline = "middle";
  ctx.fillText(text, box.left + box.paddingX, box.top + 11);
  ctx.restore();
}

function drawGraph() {
  const canvas = $("graphCanvas");
  if (!state.graph || !canvas) return;
  const ctx = canvas.getContext("2d");
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();
  const cssWidth = Math.max(320, Math.floor(rect.width || 1200));
  const cssHeight = Math.max(520, Math.floor(rect.height || 580));
  canvas.width = Math.floor(cssWidth * dpr);
  canvas.height = Math.floor(cssHeight * dpr);
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  const width = cssWidth;
  const height = cssHeight;

  // 1. 세련된 배경색 채우기
  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = "#f8fafb"; 
  ctx.fillRect(0, 0, width, height);

  // 2. 배경 격자(Grid) 그리기 - 테크니컬하고 정돈된 느낌
  ctx.save();
  ctx.strokeStyle = "rgba(28, 42, 50, 0.035)";
  ctx.lineWidth = 1;
  const gridSize = 40;
  for (let x = 0; x < width; x += gridSize) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, height);
    ctx.stroke();
  }
  for (let y = 0; y < height; y += gridSize) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(width, y);
    ctx.stroke();
  }
  ctx.restore();

  const nodes = state.graph.nodes.filter(shouldShowGraphNode).map((node) => ({
    ...node,
    group: graphType(node),
    degree: 0,
  }));
  const byPath = new Map(nodes.map((node) => [node.path, node]));
  const edges = state.graph.edges
    .filter((edge) => byPath.has(edge.source) && byPath.has(edge.target))
    .map((edge) => {
      const sourceNode = byPath.get(edge.source);
      const targetNode = byPath.get(edge.target);
      sourceNode.degree += 1;
      targetNode.degree += 1;
      return { ...edge, sourceNode, targetNode };
    });
  
  const visibleNodes = pickCoreGraphNodes(nodes);
  const visiblePaths = new Set(visibleNodes.map((node) => node.path));
  const visibleEdges = pickCoreGraphEdges(edges, visiblePaths);

  $("graphMeta").textContent = `표시 노드 ${visibleNodes.length}개 · 핵심 연결 ${visibleEdges.length}개`;
  $("graphLegend").innerHTML = [
    ["concept", "개념"],
    ["entity", "대상"],
    ["source", "원문"],
    ["question", "질문"],
    ["page", "운영"],
  ]
    .map(([type, label]) => `<span><i class="legend-dot ${type}"></i>${label}</span>`)
    .join("");

  buildGraphLayout(visibleNodes, visibleEdges, width, height);
  canvasNodes = visibleNodes;

  // 호버 강조 노드 셋업
  const highlightPaths = new Set();
  if (hoveredNode) {
    highlightPaths.add(hoveredNode.path);
    visibleEdges.forEach((edge) => {
      if (edge.source === hoveredNode.path) highlightPaths.add(edge.target);
      if (edge.target === hoveredNode.path) highlightPaths.add(edge.source);
    });
  }

  const colors = {
    concept: "#166b58",
    entity: "#245d7d",
    source: "#9f611f",
    question: "#7b517f",
    overview: "#4c5961",
    index: "#4c5961",
    dashboard: "#4c5961",
    page: "#61717a",
  };

  const degreeMax = Math.max(1, ...visibleNodes.map((node) => node.degree));

  // 3. Edges 그리기
  ctx.save();
  for (const edge of visibleEdges) {
    const a = edge.sourceNode;
    const b = edge.targetNode;
    
    let isHighlighted = false;
    let opacity = 0.075;
    let lineWidth = 1;
    
    if (hoveredNode) {
      if (edge.source === hoveredNode.path || edge.target === hoveredNode.path) {
        isHighlighted = true;
        opacity = 0.72;
        lineWidth = 1.8;
      } else {
        opacity = 0.018;
      }
    }
    
    ctx.strokeStyle = isHighlighted ? "rgba(36, 93, 125, " + opacity + ")" : "rgba(92, 108, 118, " + opacity + ")";
    ctx.lineWidth = lineWidth;
    
    ctx.beginPath();
    ctx.moveTo(a.x, a.y);
    const midX = (a.x + b.x) / 2;
    const midY = (a.y + b.y) / 2 - 12;
    ctx.quadraticCurveTo(midX, midY, b.x, b.y);
    ctx.stroke();
  }
  ctx.restore();

  // 4. Nodes 그리기
  visibleNodes
    .sort((a, b) => a.degree - b.degree)
    .forEach((node) => {
      const radius = 6 + (node.degree / degreeMax) * 14;
      node.radius = radius;

      let opacity = 1.0;
      if (hoveredNode && !highlightPaths.has(node.path)) {
        opacity = 0.22;
      }

      ctx.save();
      ctx.shadowColor = "rgba(28, 42, 50, 0.12)";
      ctx.shadowBlur = 6;
      ctx.shadowOffsetY = 3;

      ctx.beginPath();
      ctx.fillStyle = colors[node.group] || colors.page;
      ctx.globalAlpha = opacity;
      ctx.arc(node.x, node.y, radius, 0, Math.PI * 2);
      ctx.fill();
      
      ctx.lineWidth = hoveredNode && hoveredNode.path === node.path ? 3 : 2;
      ctx.strokeStyle = hoveredNode && hoveredNode.path === node.path ? "#172229" : "#ffffff";
      ctx.stroke();
      ctx.restore();
    });

  // 5. Node Labels 그리기
  const labelBudget = visibleNodes
    .filter((node) => node.degree > 1)
    .sort((a, b) => graphNodeRank(b) - graphNodeRank(a))
    .slice(0, 12);
  const labelPaths = new Set(labelBudget.map((node) => node.path));
  const placedLabelBoxes = [];
  [...visibleNodes]
    .sort((a, b) => graphNodeRank(b) - graphNodeRank(a))
    .forEach((node) => {
    const isHovered = hoveredNode && hoveredNode.path === node.path;
    const isNeighbor = hoveredNode && highlightPaths.has(node.path);
    const shouldDrawLabel = !hoveredNode
      ? labelPaths.has(node.path)
      : (isHovered || isNeighbor);
      
    if (!shouldDrawLabel) return;
    
    let opacity = 1.0;
    if (hoveredNode && !highlightPaths.has(node.path)) {
      opacity = 0.22;
    }
    
    ctx.save();
    ctx.globalAlpha = opacity;
    const label = truncateLabel(node.title, isHovered ? 30 : (node.group === "source" ? 16 : 18));
    
    const bgFill = isHovered ? "rgba(23, 34, 41, 0.96)" : "rgba(255, 255, 255, 0.94)";
    const textFill = isHovered ? "#ffffff" : "#172026";
    const borderFill = isHovered ? "#172229" : "rgba(190, 202, 209, 0.8)";
    
    const labelX = node.x < width * 0.82 ? node.x + node.radius : node.x - node.radius - 150;
    const box = roundLabelBox(ctx, label, labelX, node.y, isHovered);
    if (!isHovered && placedLabelBoxes.some((placed) => boxesOverlap(box, placed))) {
      ctx.restore();
      return;
    }
    placedLabelBoxes.push(box);
    drawRoundLabelBox(ctx, label, box, bgFill, textFill, borderFill, isHovered);
    ctx.restore();
  });

  // 6. 그룹 제목/레이아웃 위치 표기
  const groupLabels = [
    ["원문", width * 0.14, height * 0.14],
    ["개념", width * 0.43, height * 0.14],
    ["대상", width * 0.75, height * 0.14],
    ["질문", width * 0.56, height * 0.93],
  ];
  ctx.save();
  ctx.font = '700 12px "Malgun Gothic", Arial, sans-serif';
  ctx.fillStyle = "rgba(78, 92, 101, 0.5)";
  groupLabels.forEach(([label, x, y]) => {
    ctx.fillText(label, x, y);
  });
  ctx.restore();
}

async function refreshAll() {
  setStatus("불러오는 중");
  state.summary = await api("/api/summary");
  state.pages = await api("/api/pages");
  state.graph = await api("/api/graph");
  renderStats();
  renderFocus();
  renderTypeFilter();
  renderPageList();
  await loadPage(state.selectedPage);
  await renderRegistry();
  await runSearch("");
  setStatus("준비됨");
}

function bindEvents() {
  restoreLayoutState();
  document.querySelectorAll(".nav-item").forEach((button) => button.addEventListener("click", () => showView(button.dataset.view)));
  bindCollapsibles();
  $("sidebarToggle")?.addEventListener("click", () => setSidebarCollapsed(!document.body.classList.contains("sidebar-collapsed")));
  $("wikiListToggle")?.addEventListener("click", () => setWikiListCollapsed(!document.body.classList.contains("wiki-list-collapsed")));
  
  const canvas = $("graphCanvas");
  if (canvas) {
    canvas.addEventListener("mousemove", handleGraphMouseMove);
    canvas.addEventListener("click", handleGraphClick);
    canvas.addEventListener("mouseleave", handleGraphMouseLeave);
  }
  document.addEventListener("click", (event) => {
    const link = rawLinkFromEvent(event);
    if (!link) return;
    event.preventDefault();
    event.stopPropagation();
    openRawFile(link);
  });
  $("typeFilter").addEventListener("change", renderPageList);
  $("pageFilter").addEventListener("input", renderPageList);
  $("globalSearch").addEventListener("input", (event) => runSearch(event.target.value));
  $("nfsmFilter")?.addEventListener("input", renderNfsmList);
  $("refreshNfsmVault")?.addEventListener("click", () => loadNfsmPages(true).catch((error) => setStatus(error.message)));
  $("openNfsmVault")?.addEventListener("click", () => openNfsmPath("").catch((error) => setStatus(error.message)));
  $("openNfsmFile")?.addEventListener("click", () => openNfsmPath($("openNfsmFile").dataset.path || "").catch((error) => setStatus(error.message)));
  $("resourceFilter")?.addEventListener("input", renderRegistry);
  $("registryReload")?.addEventListener("click", renderRegistry);
  $("refreshBtn")?.addEventListener("click", async () => {
    setStatus("새로고침 중");
    const result = await api("/api/refresh", { method: "POST" });
    setStatus(result.code === 0 ? "목록 갱신됨" : "갱신 실패");
    await refreshAll();
  });
}

bindEvents();
refreshAll().catch((error) => {
  console.error(error);
  setStatus(error.message);
});
