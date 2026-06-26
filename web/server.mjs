import { createServer } from "node:http";
import { readFile, writeFile, mkdir, stat, readdir } from "node:fs/promises";
import { createReadStream, existsSync } from "node:fs";
import { extname, join, normalize, relative, resolve, sep } from "node:path";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";

const __dirname = fileURLToPath(new URL(".", import.meta.url));
const repoRoot = resolve(__dirname, "..");
const publicRoot = resolve(__dirname, "public");
const wikiRoot = resolve(repoRoot, "wiki");
const rawRoot = resolve(repoRoot, "raw");
const rawSourcesRoot = resolve(repoRoot, "raw", "sources");
const rawAssetsRoot = resolve(repoRoot, "raw", "assets");
const toolsRoot = resolve(repoRoot, "tools");
const linkedVaults = {
  nfsm: {
    id: "nfsm",
    title: "신성통상 차세대 패션관리시스템 개발",
    root: resolve("C:\\supersonic\\projects\\nfsm"),
    obsidianVault: "신성통상 차세대 패션관리시스템 개발",
  },
};
const portArgIndex = process.argv.findIndex((arg) => arg === "--port");
const portArg = portArgIndex >= 0 ? process.argv[portArgIndex + 1] : undefined;
const PORT = Number(portArg || process.env.PORT || 4173);

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
  ".md": "text/markdown; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
  ".csv": "text/csv; charset=utf-8",
  ".pdf": "application/pdf",
  ".ppt": "application/vnd.ms-powerpoint",
  ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
  ".xls": "application/vnd.ms-excel",
  ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  ".xlsm": "application/vnd.ms-excel.sheet.macroEnabled.12",
  ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  ".zip": "application/zip",
};

function send(res, status, body, headers = {}) {
  const payload = typeof body === "string" || Buffer.isBuffer(body) ? body : JSON.stringify(body);
  res.writeHead(status, {
    "content-type": typeof body === "object" && !Buffer.isBuffer(body) ? MIME[".json"] : "text/plain; charset=utf-8",
    "cache-control": "no-store",
    ...headers,
  });
  res.end(payload);
}

function json(res, status, body) {
  send(res, status, body, { "content-type": MIME[".json"] });
}

function safeResolve(root, requested = "") {
  const target = resolve(root, normalize(requested).replace(/^([/\\])+/, ""));
  if (target !== root && !target.startsWith(root + sep)) {
    throw new Error("Path escapes root");
  }
  return target;
}

async function readText(path) {
  return readFile(path, "utf8");
}

async function walk(root, predicate = () => true) {
  const out = [];
  async function visit(dir) {
    const entries = await readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
      const full = join(dir, entry.name);
      if (entry.isDirectory()) {
        if (!entry.name.startsWith(".")) await visit(full);
      } else if (predicate(full)) {
        out.push(full);
      }
    }
  }
  if (existsSync(root)) await visit(root);
  return out;
}

async function walkVault(root, predicate = () => true) {
  const out = [];
  const skipDirs = new Set([".git", ".claude", "node_modules", "dist", "build", ".next", ".cache"]);
  async function visit(dir) {
    const entries = await readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
      const full = join(dir, entry.name);
      if (entry.isDirectory()) {
        if (!entry.name.startsWith(".") && !skipDirs.has(entry.name)) await visit(full);
      } else if (predicate(full)) {
        out.push(full);
      }
    }
  }
  if (existsSync(root)) await visit(root);
  return out;
}

function parseFrontmatter(text) {
  const clean = text.replace(/^\uFEFF/, "");
  const matchBlock = clean.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!matchBlock) return {};
  const raw = matchBlock[1].trim();
  const meta = {};
  let current = null;
  for (const line of raw.split(/\r?\n/)) {
    const listMatch = line.match(/^\s*-\s+(.+)$/);
    if (listMatch && current) {
      if (!Array.isArray(meta[current])) meta[current] = [];
      meta[current].push(listMatch[1].trim());
      continue;
    }
    const match = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!match) continue;
    current = match[1];
    const value = match[2].trim();
    meta[current] = value === "" ? [] : value.replace(/^"|"$/g, "");
  }
  return meta;
}

function firstHeading(text, fallback) {
  const m = text.match(/^#\s+(.+)$/m);
  return m ? m[1].trim() : fallback;
}

function cleanMarkdownText(text) {
  return text
    .replace(/^---[\s\S]*?---/, "")
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/[#>*_\-\[\]()`|]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function excerpt(text, limit = 180) {
  const body = cleanMarkdownText(text);
  return body.length > limit ? `${body.slice(0, limit).trim()}...` : body;
}

function contextualExcerpt(text, query, limit = 220) {
  const body = cleanMarkdownText(text);
  if (!query) return excerpt(text, limit);
  const idx = body.toLowerCase().indexOf(query);
  if (idx < 0) return excerpt(text, limit);
  const start = Math.max(0, idx - 70);
  const snippet = body.slice(start, idx + limit).trim();
  return start > 0 ? `...${snippet}` : snippet;
}

function wikiRel(path) {
  return relative(wikiRoot, path).replaceAll("\\", "/");
}

function vaultConfig(id) {
  const config = linkedVaults[id];
  if (!config) throw new Error("연결된 vault를 찾을 수 없습니다.");
  if (!existsSync(config.root)) throw new Error(`vault 경로를 찾을 수 없습니다: ${config.root}`);
  return config;
}

function vaultRel(config, path) {
  return relative(config.root, path).replaceAll("\\", "/");
}

function enrichPage(page, meta) {
  if (meta.type === "resource" && meta.source_path) {
    const full = safeResolve(repoRoot, meta.source_path);
    return {
      ...page,
      sourcePath: meta.source_path,
      localPath: full,
      extension: meta.extension || "",
    };
  }
  return page;
}

async function listPages() {
  const files = await walk(wikiRoot, (file) => extname(file).toLowerCase() === ".md");
  const pages = [];
  for (const file of files) {
    const text = await readText(file);
    const meta = parseFrontmatter(text);
    const rel = wikiRel(file);
    const s = await stat(file);
    pages.push(enrichPage({
      path: rel,
      slug: rel.replace(/\.md$/i, ""),
      title: meta.title || firstHeading(text, rel),
      type: meta.type || "page",
      tags: Array.isArray(meta.tags) ? meta.tags : [],
      updated: meta.updated || meta.created || "",
      size: s.size,
      excerpt: excerpt(text),
    }, meta));
  }
  pages.sort((a, b) => a.path.localeCompare(b.path));
  return pages;
}

async function markdownPage(path) {
  const full = safeResolve(wikiRoot, path);
  if (extname(full).toLowerCase() !== ".md") throw new Error("Only markdown pages can be read");
  const text = await readText(full);
  const meta = parseFrontmatter(text);
  return enrichPage({
    path: wikiRel(full),
    title: meta.title || firstHeading(text, path),
    meta,
    markdown: text,
  }, meta);
}

async function listVaultPages(id) {
  const config = vaultConfig(id);
  const files = await walkVault(config.root, (file) => extname(file).toLowerCase() === ".md");
  const pages = [];
  for (const file of files) {
    const text = await readText(file);
    const meta = parseFrontmatter(text);
    const rel = vaultRel(config, file);
    const s = await stat(file);
    pages.push({
      vault: config.id,
      vaultTitle: config.title,
      obsidianVault: config.obsidianVault,
      path: rel,
      title: meta.title || firstHeading(text, rel),
      type: meta.type || rel.split("/")[0] || "page",
      updated: meta.updated || meta.created || "",
      size: s.size,
      excerpt: excerpt(text),
    });
  }
  pages.sort((a, b) => a.path.localeCompare(b.path));
  return {
    id: config.id,
    title: config.title,
    root: config.root,
    obsidianVault: config.obsidianVault,
    pages,
  };
}

async function vaultMarkdownPage(id, path) {
  const config = vaultConfig(id);
  const full = safeResolve(config.root, path);
  if (extname(full).toLowerCase() !== ".md") throw new Error("Markdown 문서만 읽을 수 있습니다.");
  const text = await readText(full);
  const meta = parseFrontmatter(text);
  return {
    vault: config.id,
    vaultTitle: config.title,
    obsidianVault: config.obsidianVault,
    path: vaultRel(config, full),
    title: meta.title || firstHeading(text, path),
    meta,
    markdown: text,
  };
}

async function getSummary() {
  const pages = await listPages();
  const registry = existsSync(join(wikiRoot, "source-registry.md"))
    ? await markdownPage("source-registry.md")
    : null;
  const pending = existsSync(join(wikiRoot, "pending-ingest.md"))
    ? await markdownPage("pending-ingest.md")
    : null;
  const log = existsSync(join(wikiRoot, "log.md")) ? await readText(join(wikiRoot, "log.md")) : "";
  const sourceCount = (registry?.markdown.match(/^\| \[\[/gm) || []).length;
  const pendingMatch = pending?.markdown.match(/pending_count:\s*(\d+)/);
  const pendingCount = pendingMatch ? Number(pendingMatch[1]) : 0;
  const typeCounts = pages.reduce((acc, p) => {
    acc[p.type] = (acc[p.type] || 0) + 1;
    return acc;
  }, {});
  const recentLog = log
    .split(/\n(?=## \[)/)
    .filter((block) => block.startsWith("## ["))
    .slice(0, 5)
    .map((block) => block.split(/\r?\n/)[0].replace(/^##\s+/, ""));
  return {
    repoRoot,
    pageCount: pages.length,
    sourceCount,
    pendingCount,
    typeCounts,
    recentLog,
    focus: [
      "sources/field-interview-master-data-summary.md",
      "concepts/store-master-data-cleanup.md",
      "concepts/product-master-data-cleanup.md",
      "questions/fone-core-resource-priority.md",
      "sources/asis-fone-folder-ingest.md",
      "concepts/fone-as-is-analysis.md",
      "concepts/master-data-governance.md",
      "concepts/plm-fone-integration.md",
      "concepts/wms-fone-inventory-integration.md",
      "concepts/sales-settlement-automation.md",
      "questions/fone-next-decisions.md",
      "resources/auto/fone-c348c1c5d9.md",
      "resources/auto/20260318-3e3ced425c.md",
      "resources/auto/fa-one-73077b7a31.md",
      "resources/auto/fa-one-5bc95be344.md",
      "resources/auto/20260327-process-86845c5311.md",
      "resources/auto/resource-2537e80af1.md",
      "resources/auto/as-is-to-be-761c70f811.md",
      "resources/auto/wms-faone-wms-3326b626da.md",
      "resources/auto/plm-83dc3fd156.md",
      "resources/auto/1-faone-ver1-7-40d88e9b38.md",
    ],
  };
}

async function search(q) {
  const query = (q || "").trim().toLowerCase();
  const pages = await listPages();
  if (!query) return pages.slice(0, 30).map((p) => ({ ...p, score: 0 }));
  const results = [];
  for (const page of pages) {
    const full = safeResolve(wikiRoot, page.path);
    const text = await readText(full);
    const haystack = `${page.title}\n${page.path}\n${text}`.toLowerCase();
    const count = haystack.split(query).length - 1;
    if (count > 0) {
      results.push({
        ...page,
        score: count,
        excerpt: contextualExcerpt(text, query) || page.excerpt,
      });
    }
  }
  return results.sort((a, b) => b.score - a.score || a.title.localeCompare(b.title)).slice(0, 80);
}

async function graph() {
  const pages = await listPages();
  const byStem = new Map(pages.map((p) => [p.path.replace(/\.md$/i, "").split("/").at(-1).toLowerCase(), p]));
  const edges = [];
  for (const page of pages) {
    const text = await readText(safeResolve(wikiRoot, page.path));
    const source = page.path;
    for (const m of text.matchAll(/\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]/g)) {
      const targetKey = m[1].trim().toLowerCase();
      const target = byStem.get(targetKey);
      if (target) edges.push({ source, target: target.path });
    }
  }
  return { nodes: pages, edges };
}

async function refreshIndex() {
  const script = join(toolsRoot, "wiki_auto_index.py");
  const python = process.env.PYTHON || "python";
  return new Promise((resolvePromise) => {
    const child = spawn(python, [script, "--no-log"], { cwd: repoRoot, shell: true });
    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (data) => (stdout += data.toString()));
    child.stderr.on("data", (data) => (stderr += data.toString()));
    child.on("close", (code) => resolvePromise({ code, stdout, stderr }));
  });
}

async function collectBody(req) {
  const chunks = [];
  for await (const chunk of req) chunks.push(chunk);
  return Buffer.concat(chunks);
}

function parseMultipart(buffer, contentType) {
  const boundaryMatch = contentType.match(/boundary=(?:"([^"]+)"|([^;]+))/i);
  if (!boundaryMatch) throw new Error("Missing multipart boundary");
  const boundary = Buffer.from(`--${boundaryMatch[1] || boundaryMatch[2]}`);
  const parts = [];
  let start = buffer.indexOf(boundary);
  while (start !== -1) {
    start += boundary.length;
    if (buffer[start] === 45 && buffer[start + 1] === 45) break;
    if (buffer[start] === 13 && buffer[start + 1] === 10) start += 2;
    const headerEnd = buffer.indexOf(Buffer.from("\r\n\r\n"), start);
    if (headerEnd === -1) break;
    const header = buffer.slice(start, headerEnd).toString("utf8");
    const next = buffer.indexOf(boundary, headerEnd + 4);
    if (next === -1) break;
    let body = buffer.slice(headerEnd + 4, next);
    if (body.at(-2) === 13 && body.at(-1) === 10) body = body.slice(0, -2);
    const name = header.match(/name="([^"]+)"/)?.[1] || "";
    const filename = header.match(/filename="([^"]*)"/)?.[1] || "";
    parts.push({ name, filename, body });
    start = next;
  }
  return parts;
}

function sanitizeFilename(name) {
  return name.replace(/[<>:"/\\|?*\x00-\x1F]/g, "_").replace(/\s+/g, " ").trim() || "uploaded-file";
}

async function upload(req) {
  const contentType = req.headers["content-type"] || "";
  const buffer = await collectBody(req);
  const parts = parseMultipart(buffer, contentType);
  const targetPart = parts.find((p) => p.name === "target");
  const fileParts = parts.filter((p) => p.name === "files" && p.filename);
  const targetRoot = targetPart?.body.toString("utf8") === "assets" ? rawAssetsRoot : rawSourcesRoot;
  const folder = join(targetRoot, "web-uploads", new Date().toISOString().slice(0, 10));
  await mkdir(folder, { recursive: true });
  const saved = [];
  for (const file of fileParts) {
    const filename = sanitizeFilename(file.filename);
    let dest = join(folder, filename);
    let n = 1;
    while (existsSync(dest)) {
      const ext = extname(filename);
      const base = filename.slice(0, filename.length - ext.length);
      dest = join(folder, `${base}-${n}${ext}`);
      n += 1;
    }
    await writeFile(dest, file.body);
    saved.push(relative(repoRoot, dest).replaceAll("\\", "/"));
  }
  const refresh = await refreshIndex();
  return { saved, refresh };
}

function parseJsonBody(buffer) {
  if (!buffer.length) return {};
  return JSON.parse(buffer.toString("utf8"));
}

function openWithDefaultApp(full) {
  const openers = {
    win32: ["rundll32.exe", ["url.dll,FileProtocolHandler", full]],
    darwin: ["open", [full]],
    linux: ["xdg-open", [full]],
  };
  const [command, args] = openers[process.platform] || openers.win32;
  const child = spawn(command, args, {
    detached: true,
    stdio: "ignore",
    windowsHide: true,
  });
  child.unref();
}

async function openLocalFile(req) {
  const payload = parseJsonBody(await collectBody(req));
  const sourcePath = String(payload.sourcePath || "");
  if (!sourcePath.startsWith("raw/")) {
    throw new Error("raw 폴더 안의 파일만 열 수 있습니다.");
  }
  const full = safeResolve(repoRoot, sourcePath);
  if (full !== rawRoot && !full.startsWith(rawRoot + sep)) {
    throw new Error("raw 폴더 밖의 파일은 열 수 없습니다.");
  }
  if (!existsSync(full)) {
    throw new Error("로컬 파일을 찾을 수 없습니다.");
  }
  const info = await stat(full);
  if (!info.isFile()) {
    throw new Error("파일만 열 수 있습니다.");
  }
  openWithDefaultApp(full);
  return { opened: true, sourcePath, localPath: full };
}

async function openVaultFile(req) {
  const payload = parseJsonBody(await collectBody(req));
  const id = String(payload.vault || "nfsm");
  const requestedPath = String(payload.path || "");
  const config = vaultConfig(id);
  const full = requestedPath ? safeResolve(config.root, requestedPath) : config.root;
  if (!existsSync(full)) {
    throw new Error("vault 파일 또는 폴더를 찾을 수 없습니다.");
  }
  openWithDefaultApp(full);
  return {
    opened: true,
    vault: config.id,
    path: requestedPath || "",
    localPath: full,
  };
}

async function handleApi(req, res, url) {
  try {
    if (url.pathname === "/api/summary") return json(res, 200, await getSummary());
    if (url.pathname === "/api/pages") return json(res, 200, await listPages());
    if (url.pathname === "/api/page") return json(res, 200, await markdownPage(url.searchParams.get("path") || "questions/fone-core-resource-priority.md"));
    if (url.pathname === "/api/search") return json(res, 200, await search(url.searchParams.get("q") || ""));
    if (url.pathname === "/api/graph") return json(res, 200, await graph());
    if (url.pathname === "/api/vault/nfsm/pages") return json(res, 200, await listVaultPages("nfsm"));
    if (url.pathname === "/api/vault/nfsm/page") return json(res, 200, await vaultMarkdownPage("nfsm", url.searchParams.get("path") || "README.md"));
    if (url.pathname === "/api/vault/nfsm/open" && req.method === "POST") return json(res, 200, await openVaultFile(req));
    if (url.pathname === "/api/refresh" && req.method === "POST") return json(res, 200, await refreshIndex());
    if (url.pathname === "/api/open-file" && req.method === "POST") return json(res, 200, await openLocalFile(req));
    if (url.pathname === "/api/upload" && req.method === "POST") return json(res, 200, await upload(req));
    return json(res, 404, { error: "API \uACBD\uB85C\uB97C \uCC3E\uC744 \uC218 \uC5C6\uC2B5\uB2C8\uB2E4." });
  } catch (error) {
    return json(res, 500, { error: error.message || String(error) });
  }
}

async function serveStatic(res, pathname) {
  const file = pathname === "/" ? "index.html" : pathname.slice(1);
  const full = safeResolve(publicRoot, file);
  if (!existsSync(full)) return send(res, 404, "\uD30C\uC77C\uC744 \uCC3E\uC744 \uC218 \uC5C6\uC2B5\uB2C8\uB2E4.");
  const type = MIME[extname(full).toLowerCase()] || "application/octet-stream";
  res.writeHead(200, {
    "content-type": type,
    "cache-control": "no-store",
  });
  createReadStream(full).pipe(res);
}
const server = createServer(async (req, res) => {
  const url = new URL(req.url || "/", `http://${req.headers.host || "localhost"}`);
  if (url.pathname.startsWith("/api/")) return handleApi(req, res, url);
  return serveStatic(res, url.pathname);
});

server.listen(PORT, () => {
  console.log(`LLM \uC704\uD0A4 \uC6F9 \uC11C\uBE44\uC2A4 \uC2E4\uD589 \uC911: http://localhost:${PORT}`);
});
