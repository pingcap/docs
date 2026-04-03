import {
  buildDocsIndex,
  docsApiSchema,
  loadDocContentByPath,
  loadTemplateVariables,
  resolveDefaultSourceDir,
} from "./docs-api-lib.js";

const SERVER_NAME = "tidb-docs-mcp";
const SERVER_VERSION = "0.1.0";
const PROTOCOL_VERSION = "2024-11-05";

const SOURCE_DIR =
  process.env.DOCS_API_SOURCE_DIR || resolveDefaultSourceDir(process.cwd());

const templateVariables = loadTemplateVariables(SOURCE_DIR);
let docsIndex = buildDocsIndex(SOURCE_DIR);

const toInt = (value, fallback) => {
  const num = Number.parseInt(value, 10);
  return Number.isNaN(num) ? fallback : num;
};

const containsCI = (text, keyword) =>
  String(text || "")
    .toLowerCase()
    .includes(String(keyword || "").toLowerCase());

const stripPrivateFields = (doc, includeContent = false) => {
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
    result.content = loadDocContentByPath(SOURCE_DIR, doc.path, templateVariables);
    result.contentType = "text/markdown";
  }
  return result;
};

const searchDocs = (args = {}) => {
  const feature = args.feature;
  const topic = args.topic;
  const keyword = args.q;
  const pathFilter = args.path;
  const includeContent = args.includeContent === true;
  const limit = Math.min(Math.max(toInt(args.limit, 20), 1), 100);
  const offset = Math.max(toInt(args.offset, 0), 0);

  let rows = docsIndex.docs;

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
    .map((doc) => stripPrivateFields(doc, includeContent));

  return {
    meta: {
      total,
      limit,
      offset,
      returned: data.length,
      includeContent,
      sourceDir: SOURCE_DIR,
    },
    data,
  };
};

const getDocByPathOrId = (args = {}) => {
  const docPath = args.path;
  const docId = args.id;
  if (!docPath && !docId) {
    throw new Error("Either path or id is required.");
  }
  const doc = docsIndex.docs.find((item) => {
    if (docPath && item.path.toLowerCase() === String(docPath).toLowerCase()) return true;
    if (docId && item.id.toLowerCase() === String(docId).toLowerCase()) return true;
    return false;
  });
  if (!doc) throw new Error("Document not found.");
  return stripPrivateFields(doc, true);
};

const listFeatures = (args = {}) => {
  const prefix = String(args.prefix || "");
  if (!prefix) return docsIndex.features;
  return docsIndex.features.filter((item) => item.toLowerCase().startsWith(prefix.toLowerCase()));
};

const reloadIndex = () => {
  docsIndex = buildDocsIndex(SOURCE_DIR);
  return {
    ok: true,
    totalDocs: docsIndex.totalDocs,
    generatedAt: docsIndex.generatedAt,
    sourceDir: SOURCE_DIR,
  };
};

const getResourceByUri = (uri) => {
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
          schemaVersion: docsIndex.schemaVersion,
          generatedAt: docsIndex.generatedAt,
          totalDocs: docsIndex.totalDocs,
          totalTopics: docsIndex.topics.length,
          totalFeatures: docsIndex.features.length,
          sourceDir: SOURCE_DIR,
        },
        null,
        2
      ),
    };
  }
  if (uri.startsWith("docs://doc/")) {
    const rawPath = decodeURIComponent(uri.replace("docs://doc/", ""));
    const content = loadDocContentByPath(SOURCE_DIR, rawPath, templateVariables);
    return {
      uri,
      mimeType: "text/markdown",
      text: content,
    };
  }
  throw new Error(`Unsupported resource URI: ${uri}`);
};

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

const buildResourceList = () => [
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
  ...docsIndex.docs.map((doc) => ({
    uri: `docs://doc/${encodeURIComponent(doc.path)}`,
    name: doc.title,
    description: doc.path,
    mimeType: "text/markdown",
  })),
];

const textResult = (payload) => {
  return {
    content: [
      {
        type: "text",
        text: JSON.stringify(payload, null, 2),
      },
    ],
  };
};

const handlers = {
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
    if (name === "search_docs") return textResult(searchDocs(args));
    if (name === "get_doc_content") return textResult({ data: getDocByPathOrId(args) });
    if (name === "list_topics") return textResult({ data: docsIndex.topics });
    if (name === "list_features") return textResult({ data: listFeatures(args) });
    if (name === "reload_docs_index") return textResult(reloadIndex());
    throw new Error(`Unknown tool: ${name}`);
  },
  "resources/list": () => ({
    resources: buildResourceList(),
  }),
  "resources/read": (params) => ({
    contents: [getResourceByUri(params?.uri)],
  }),
  "ping": () => ({}),
};

let inputBuffer = Buffer.alloc(0);

const writeMessage = (message) => {
  const json = JSON.stringify(message);
  const header = `Content-Length: ${Buffer.byteLength(json, "utf8")}\r\n\r\n`;
  process.stdout.write(header + json);
};

const writeError = (id, code, message) => {
  writeMessage({
    jsonrpc: "2.0",
    id: id ?? null,
    error: {
      code,
      message,
    },
  });
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

    let message;
    try {
      message = JSON.parse(body);
    } catch (error) {
      writeError(null, -32700, "Parse error");
      continue;
    }
    handleMessage(message);
  }
};

const handleMessage = (msg) => {
  if (msg.jsonrpc !== "2.0") {
    return writeError(msg.id, -32600, "Invalid Request");
  }
  const method = msg.method;
  const handler = handlers[method];
  if (!handler) {
    if (msg.id !== undefined) writeError(msg.id, -32601, "Method not found");
    return;
  }
  try {
    const result = handler(msg.params);
    if (msg.id !== undefined && method !== "notifications/initialized") {
      writeMessage({
        jsonrpc: "2.0",
        id: msg.id,
        result: result ?? {},
      });
    }
  } catch (error) {
    if (msg.id !== undefined) {
      writeError(msg.id, -32000, String(error.message || error));
    }
  }
};

process.stdin.on("data", (chunk) => {
  inputBuffer = Buffer.concat([inputBuffer, chunk]);
  parseMessages();
});

process.stdin.on("end", () => {
  process.exit(0);
});

process.stderr.write(
  `[${SERVER_NAME}] ready (source=${SOURCE_DIR}, docs=${docsIndex.totalDocs})\n`
);
