import http from "http";
import {
  buildDocsIndex,
  docsApiSchema,
  loadDocContentByPath,
  loadTemplateVariables,
  resolveDefaultSourceDir,
} from "./docs-api-lib.js";

const SERVER_NAME = "tidb-docs-mcp";
const SERVER_VERSION = "0.2.0";
const PROTOCOL_VERSION = "2024-11-05";

const TRANSPORT = (process.env.DOCS_MCP_TRANSPORT || "stdio").toLowerCase();
const HTTP_HOST = process.env.DOCS_MCP_HTTP_HOST || "127.0.0.1";
const HTTP_PORT = Number.parseInt(process.env.DOCS_MCP_HTTP_PORT || "3100", 10);
const AUTH_TOKEN = process.env.DOCS_MCP_AUTH_TOKEN || "";
const SOURCE_MAP = parseJsonMap(process.env.DOCS_MCP_SOURCE_MAP || "");

const DEFAULT_SOURCE_DIR = process.env.DOCS_API_SOURCE_DIR || resolveDefaultSourceDir(process.cwd());
const stateCache = new Map();

function parseJsonMap(raw) {
  if (!raw) return {};
  try {
    const parsed = JSON.parse(raw);
    if (parsed && typeof parsed === "object" && !Array.isArray(parsed)) return parsed;
  } catch (_error) {}
  return {};
}

function normalizeSourceConfig(sourceKey) {
  if (sourceKey && SOURCE_MAP[sourceKey]) {
    return {
      sourceKey,
      sourceDir: SOURCE_MAP[sourceKey],
    };
  }
  return {
    sourceKey: sourceKey || "default",
    sourceDir: DEFAULT_SOURCE_DIR,
  };
}

function getSourceState(sourceKey) {
  const cfg = normalizeSourceConfig(sourceKey);
  const cacheKey = `${cfg.sourceKey}::${cfg.sourceDir}`;
  if (!stateCache.has(cacheKey)) {
    stateCache.set(cacheKey, {
      sourceKey: cfg.sourceKey,
      sourceDir: cfg.sourceDir,
      templateVariables: loadTemplateVariables(cfg.sourceDir),
      docsIndex: buildDocsIndex(cfg.sourceDir),
    });
  }
  return stateCache.get(cacheKey);
}

function refreshSourceState(sourceKey) {
  const cfg = normalizeSourceConfig(sourceKey);
  const cacheKey = `${cfg.sourceKey}::${cfg.sourceDir}`;
  const next = {
    sourceKey: cfg.sourceKey,
    sourceDir: cfg.sourceDir,
    templateVariables: loadTemplateVariables(cfg.sourceDir),
    docsIndex: buildDocsIndex(cfg.sourceDir),
  };
  stateCache.set(cacheKey, next);
  return next;
}

function toInt(value, fallback) {
  const num = Number.parseInt(value, 10);
  return Number.isNaN(num) ? fallback : num;
}

function containsCI(text, keyword) {
  return String(text || "")
    .toLowerCase()
    .includes(String(keyword || "").toLowerCase());
}

function stripPrivateFields(sourceState, doc, includeContent = false) {
  const result = {
    id: doc.id,
    path: doc.path,
    title: doc.title,
    summary: doc.summary,
    product: doc.product,
    topics: doc.topics,
    features: doc.features,
    headings: doc.headings,
    frontMatter: doc.frontMatter,
    frontMatterRaw: doc.frontMatterRaw,
    updatedAt: doc.updatedAt,
  };
  if (includeContent) {
    result.content = loadDocContentByPath(
      sourceState.sourceDir,
      doc.path,
      sourceState.templateVariables
    );
    result.contentType = "text/markdown";
  }
  return result;
}

function searchDocs(sourceState, args = {}) {
  const feature = args.feature;
  const topic = args.topic;
  const keyword = args.q;
  const pathFilter = args.path;
  const includeContent = args.includeContent === true;
  const limit = Math.min(Math.max(toInt(args.limit, 20), 1), 100);
  const offset = Math.max(toInt(args.offset, 0), 0);

  let rows = sourceState.docsIndex.docs;

  if (feature) {
    rows = rows.filter((doc) =>
      doc.features.some((item) => item.toLowerCase() === String(feature).toLowerCase())
    );
  }
  if (topic) {
    rows = rows.filter((doc) =>
      doc.topics.some((item) => item.toLowerCase() === String(topic).toLowerCase())
    );
  }
  if (pathFilter) {
    rows = rows.filter((doc) => doc.path.toLowerCase() === String(pathFilter).toLowerCase());
  }
  if (keyword) {
    rows = rows.filter((doc) => {
      return (
        containsCI(doc.path, keyword) ||
        containsCI(doc.title, keyword) ||
        containsCI(doc.summary, keyword) ||
        containsCI(doc._searchText || "", keyword)
      );
    });
  }

  const total = rows.length;
  const data = rows
    .slice(offset, offset + limit)
    .map((doc) => stripPrivateFields(sourceState, doc, includeContent));

  return {
    meta: {
      total,
      limit,
      offset,
      returned: data.length,
      includeContent,
      sourceKey: sourceState.sourceKey,
      sourceDir: sourceState.sourceDir,
    },
    data,
  };
}

function getDocByPathOrId(sourceState, args = {}) {
  const docPath = args.path;
  const docId = args.id;
  if (!docPath && !docId) {
    throw new Error("Either path or id is required.");
  }
  const doc = sourceState.docsIndex.docs.find((item) => {
    if (docPath && item.path.toLowerCase() === String(docPath).toLowerCase()) return true;
    if (docId && item.id.toLowerCase() === String(docId).toLowerCase()) return true;
    return false;
  });
  if (!doc) throw new Error("Document not found.");
  return stripPrivateFields(sourceState, doc, true);
}

function listFeatures(sourceState, args = {}) {
  const prefix = String(args.prefix || "");
  if (!prefix) return sourceState.docsIndex.features;
  return sourceState.docsIndex.features.filter((item) =>
    item.toLowerCase().startsWith(prefix.toLowerCase())
  );
}

function getResourceByUri(sourceState, uri) {
  if (uri === "docs://schema") {
    return {
      uri,
      mimeType: "application/json",
      text: JSON.stringify(docsApiSchema, null, 2),
    };
  }
  if (uri === "docs://index/meta") {
    return {
      uri,
      mimeType: "application/json",
      text: JSON.stringify(
        {
          schemaVersion: sourceState.docsIndex.schemaVersion,
          generatedAt: sourceState.docsIndex.generatedAt,
          totalDocs: sourceState.docsIndex.totalDocs,
          totalTopics: sourceState.docsIndex.topics.length,
          totalFeatures: sourceState.docsIndex.features.length,
          sourceKey: sourceState.sourceKey,
          sourceDir: sourceState.sourceDir,
        },
        null,
        2
      ),
    };
  }
  if (uri.startsWith("docs://doc/")) {
    const rawPath = decodeURIComponent(uri.replace("docs://doc/", ""));
    const content = loadDocContentByPath(
      sourceState.sourceDir,
      rawPath,
      sourceState.templateVariables
    );
    return {
      uri,
      mimeType: "text/markdown",
      text: content,
    };
  }
  throw new Error(`Unsupported resource URI: ${uri}`);
}

function buildResourceList(sourceState) {
  return [
    {
      uri: "docs://schema",
      name: "Docs API Schema",
      description: "Schema and endpoint model for docs capabilities.",
      mimeType: "application/json",
    },
    {
      uri: "docs://index/meta",
      name: "Docs Index Meta",
      description: "Index metadata such as counts and generated timestamp.",
      mimeType: "application/json",
    },
    ...sourceState.docsIndex.docs.map((doc) => ({
      uri: `docs://doc/${encodeURIComponent(doc.path)}`,
      name: doc.title,
      description: doc.path,
      mimeType: "text/markdown",
    })),
  ];
}

const TOOL_DEFS = [
  {
    name: "search_docs",
    description: "Search TiDB docs by feature/topic/path/full-text. Returns lightweight records by default.",
    inputSchema: {
      type: "object",
      properties: {
        feature: { type: "string" },
        topic: { type: "string" },
        q: { type: "string" },
        path: { type: "string" },
        limit: { type: "integer", minimum: 1, maximum: 100 },
        offset: { type: "integer", minimum: 0 },
        includeContent: { type: "boolean", default: false },
      },
      additionalProperties: false,
    },
  },
  {
    name: "get_doc_content",
    description: "Get full markdown content by document path or id.",
    inputSchema: {
      type: "object",
      properties: {
        path: { type: "string" },
        id: { type: "string" },
      },
      additionalProperties: false,
    },
  },
  {
    name: "list_topics",
    description: "List all available topics/categories in the docs index.",
    inputSchema: {
      type: "object",
      properties: {},
      additionalProperties: false,
    },
  },
  {
    name: "list_features",
    description: "List all recognized feature tokens, optionally filtered by prefix.",
    inputSchema: {
      type: "object",
      properties: {
        prefix: { type: "string" },
      },
      additionalProperties: false,
    },
  },
  {
    name: "reload_docs_index",
    description: "Reload docs index from disk (use after docs update).",
    inputSchema: {
      type: "object",
      properties: {},
      additionalProperties: false,
    },
  },
];

function textResult(payload) {
  return {
    content: [
      {
        type: "text",
        text: JSON.stringify(payload, null, 2),
      },
    ],
  };
}

function buildHandlers(sourceState) {
  return {
    initialize: (params) => ({
      protocolVersion: PROTOCOL_VERSION,
      serverInfo: {
        name: SERVER_NAME,
        version: SERVER_VERSION,
      },
      capabilities: {
        tools: {},
        resources: {},
      },
      instructions:
        "Use search_docs for discovery and get_doc_content for full markdown. Prefer lightweight responses unless full content is required.",
      clientInfo: params?.clientInfo || null,
    }),
    "notifications/initialized": () => null,
    "tools/list": () => ({
      tools: TOOL_DEFS,
    }),
    "tools/call": (params) => {
      const name = params?.name;
      const args = params?.arguments || {};
      if (name === "search_docs") return textResult(searchDocs(sourceState, args));
      if (name === "get_doc_content")
        return textResult({ data: getDocByPathOrId(sourceState, args) });
      if (name === "list_topics") return textResult({ data: sourceState.docsIndex.topics });
      if (name === "list_features") return textResult({ data: listFeatures(sourceState, args) });
      if (name === "reload_docs_index") {
        const refreshed = refreshSourceState(sourceState.sourceKey);
        return textResult({
          ok: true,
          totalDocs: refreshed.docsIndex.totalDocs,
          generatedAt: refreshed.docsIndex.generatedAt,
          sourceKey: refreshed.sourceKey,
          sourceDir: refreshed.sourceDir,
        });
      }
      throw new Error(`Unknown tool: ${name}`);
    },
    "resources/list": () => ({
      resources: buildResourceList(sourceState),
    }),
    "resources/read": (params) => ({
      contents: [getResourceByUri(sourceState, params?.uri)],
    }),
    ping: () => ({}),
  };
}

function processRpcMessage(msg, sourceKey) {
  const sourceState = getSourceState(sourceKey);
  const handlers = buildHandlers(sourceState);

  if (msg.jsonrpc !== "2.0") {
    return {
      jsonrpc: "2.0",
      id: msg.id ?? null,
      error: {
        code: -32600,
        message: "Invalid Request",
      },
    };
  }

  const method = msg.method;
  const handler = handlers[method];
  if (!handler) {
    return {
      jsonrpc: "2.0",
      id: msg.id ?? null,
      error: {
        code: -32601,
        message: "Method not found",
      },
    };
  }

  try {
    const result = handler(msg.params);
    if (msg.id === undefined || method === "notifications/initialized") {
      return null;
    }
    return {
      jsonrpc: "2.0",
      id: msg.id,
      result: result ?? {},
    };
  } catch (error) {
    return {
      jsonrpc: "2.0",
      id: msg.id ?? null,
      error: {
        code: -32000,
        message: String(error.message || error),
      },
    };
  }
}

function validateAuth(headers) {
  if (!AUTH_TOKEN) return true;
  const raw = headers.authorization || "";
  if (!raw.toLowerCase().startsWith("bearer ")) return false;
  const token = raw.slice(7).trim();
  return token === AUTH_TOKEN;
}

function parseBodyJson(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on("data", (chunk) => chunks.push(chunk));
    req.on("end", () => {
      try {
        const body = Buffer.concat(chunks).toString("utf8");
        resolve(body ? JSON.parse(body) : {});
      } catch (error) {
        reject(error);
      }
    });
    req.on("error", reject);
  });
}

function startHttpServer() {
  const server = http.createServer(async (req, res) => {
    if (req.url === "/healthz" && req.method === "GET") {
      res.writeHead(200, { "content-type": "application/json; charset=utf-8" });
      res.end(JSON.stringify({ ok: true }));
      return;
    }

    if (req.url !== "/mcp" || req.method !== "POST") {
      res.writeHead(404, { "content-type": "application/json; charset=utf-8" });
      res.end(JSON.stringify({ error: "Not found" }));
      return;
    }

    if (!validateAuth(req.headers)) {
      res.writeHead(401, { "content-type": "application/json; charset=utf-8" });
      res.end(JSON.stringify({ error: "Unauthorized" }));
      return;
    }

    const sourceKey = (req.headers["x-docs-source"] || "default").toString();

    try {
      const json = await parseBodyJson(req);
      const response = processRpcMessage(json, sourceKey);
      if (!response) {
        res.writeHead(204);
        res.end();
        return;
      }
      res.writeHead(200, { "content-type": "application/json; charset=utf-8" });
      res.end(JSON.stringify(response));
    } catch (error) {
      res.writeHead(400, { "content-type": "application/json; charset=utf-8" });
      res.end(
        JSON.stringify({
          jsonrpc: "2.0",
          id: null,
          error: {
            code: -32700,
            message: `Parse error: ${String(error.message || error)}`,
          },
        })
      );
    }
  });

  server.listen(HTTP_PORT, HTTP_HOST, () => {
    process.stderr.write(
      `[${SERVER_NAME}] http ready at http://${HTTP_HOST}:${HTTP_PORT}/mcp (defaultSource=${DEFAULT_SOURCE_DIR})\n`
    );
  });
}

function startStdioServer() {
  let inputBuffer = Buffer.alloc(0);

  const writeMessage = (message) => {
    const json = JSON.stringify(message);
    const header = `Content-Length: ${Buffer.byteLength(json, "utf8")}\r\n\r\n`;
    process.stdout.write(header + json);
  };

  const parseMessages = () => {
    while (true) {
      const separator = inputBuffer.indexOf("\r\n\r\n");
      if (separator === -1) return;

      const headerRaw = inputBuffer.slice(0, separator).toString("utf8");
      const lengthLine = headerRaw
        .split("\r\n")
        .find((line) => line.toLowerCase().startsWith("content-length:"));
      if (!lengthLine) {
        inputBuffer = Buffer.alloc(0);
        return;
      }
      const length = Number.parseInt(lengthLine.split(":")[1]?.trim() || "0", 10);
      const bodyStart = separator + 4;
      const bodyEnd = bodyStart + length;
      if (inputBuffer.length < bodyEnd) return;

      const body = inputBuffer.slice(bodyStart, bodyEnd).toString("utf8");
      inputBuffer = inputBuffer.slice(bodyEnd);

      let msg;
      try {
        msg = JSON.parse(body);
      } catch (_error) {
        writeMessage({
          jsonrpc: "2.0",
          id: null,
          error: { code: -32700, message: "Parse error" },
        });
        continue;
      }
      const response = processRpcMessage(msg, "default");
      if (response) writeMessage(response);
    }
  };

  process.stdin.on("data", (chunk) => {
    inputBuffer = Buffer.concat([inputBuffer, chunk]);
    parseMessages();
  });

  process.stdin.on("end", () => process.exit(0));
  process.stderr.write(
    `[${SERVER_NAME}] stdio ready (defaultSource=${DEFAULT_SOURCE_DIR})\n`
  );
}

if (TRANSPORT === "http") {
  startHttpServer();
} else {
  startStdioServer();
}

