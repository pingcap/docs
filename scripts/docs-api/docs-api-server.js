import * as fs from "fs";
import http from "http";
import path from "path";
import {
  buildDocsIndex,
  docsApiSchema,
  loadDocContentByPath,
  loadTemplateVariables,
  resolveDefaultSourceDir,
} from "./docs-api-lib.js";

const PORT = Number.parseInt(process.env.DOCS_API_PORT || "3000", 10);
const HOST = process.env.DOCS_API_HOST || "127.0.0.1";
const SOURCE_DIR = path.resolve(
  process.env.DOCS_API_SOURCE_DIR || resolveDefaultSourceDir(process.cwd())
);
const PREBUILT_INDEX = process.env.DOCS_API_INDEX_FILE;
const TEMPLATE_VARIABLES = loadTemplateVariables(SOURCE_DIR);

const loadIndex = () => {
  if (PREBUILT_INDEX) {
    const filePath = path.resolve(PREBUILT_INDEX);
    if (fs.existsSync(filePath)) {
      return JSON.parse(fs.readFileSync(filePath, "utf8"));
    }
  }
  return buildDocsIndex(SOURCE_DIR);
};

let docsIndex = loadIndex();

const toInt = (value, fallback) => {
  const num = Number.parseInt(value, 10);
  return Number.isNaN(num) ? fallback : num;
};

const containsCI = (text, keyword) =>
  text.toLowerCase().includes(keyword.toLowerCase());

const isTruthy = (value) => {
  if (!value) return false;
  return ["1", "true", "yes", "on"].includes(value.toLowerCase());
};

const json = (res, statusCode, payload) => {
  res.writeHead(statusCode, { "Content-Type": "application/json; charset=utf-8" });
  res.end(JSON.stringify(payload, null, 2));
};

const toPublicDoc = (doc, options = {}) => {
  const includeContent = options.includeContent === true;
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
    try {
      result.content = loadDocContentByPath(SOURCE_DIR, doc.path, TEMPLATE_VARIABLES);
      result.contentType = "text/markdown";
    } catch (error) {
      result.content = "";
      result.contentType = "text/markdown";
      result.contentError = String(error.message || error);
    }
  }
  return result;
};

const filterDocs = (docs, query) => {
  const feature = query.get("feature");
  const topic = query.get("topic");
  const keyword = query.get("q");
  const pathFilter = query.get("path");
  const includeContent = isTruthy(query.get("includeContent"));
  const limit = Math.min(Math.max(toInt(query.get("limit"), 20), 1), 100);
  const offset = Math.max(toInt(query.get("offset"), 0), 0);

  let rows = docs;

  if (feature) {
    rows = rows.filter((doc) =>
      doc.features.some((item) => item.toLowerCase() === feature.toLowerCase())
    );
  }
  if (topic) {
    rows = rows.filter((doc) =>
      doc.topics.some((item) => item.toLowerCase() === topic.toLowerCase())
    );
  }
  if (pathFilter) {
    rows = rows.filter((doc) => doc.path.toLowerCase() === pathFilter.toLowerCase());
  }
  if (keyword) {
    const loweredKeyword = keyword.toLowerCase();
    rows = rows.filter((doc) => {
      return (
        containsCI(doc.path, loweredKeyword) ||
        containsCI(doc.title, loweredKeyword) ||
        containsCI(doc.summary, loweredKeyword) ||
        containsCI(doc._searchText || "", loweredKeyword)
      );
    });
  }

  const total = rows.length;
  const paged = rows.slice(offset, offset + limit);

  return {
    meta: {
      total,
      limit,
      offset,
      returned: paged.length,
      includeContent,
    },
    data: paged.map((doc) => toPublicDoc(doc, { includeContent })),
  };
};

const server = http.createServer((req, res) => {
  if (!req.url) {
    return json(res, 400, { error: "Invalid request URL." });
  }

  const url = new URL(req.url, `http://${HOST}:${PORT}`);
  const pathname = url.pathname;

  if (req.method !== "GET") {
    return json(res, 405, { error: "Only GET is supported." });
  }

  if (pathname === "/healthz") {
    return json(res, 200, { ok: true });
  }
  if (pathname === "/schema") {
    return json(res, 200, docsApiSchema);
  }
  if (pathname === "/topics") {
    return json(res, 200, { data: docsIndex.topics });
  }
  if (pathname === "/features") {
    const prefix = url.searchParams.get("prefix");
    if (!prefix) {
      return json(res, 200, { data: docsIndex.features });
    }
    const filtered = docsIndex.features.filter((f) =>
      f.toLowerCase().startsWith(prefix.toLowerCase())
    );
    return json(res, 200, { data: filtered });
  }
  if (pathname === "/reload") {
    docsIndex = loadIndex();
    return json(res, 200, {
      ok: true,
      totalDocs: docsIndex.totalDocs,
      generatedAt: docsIndex.generatedAt,
    });
  }
  if (pathname === "/docs") {
    return json(res, 200, filterDocs(docsIndex.docs, url.searchParams));
  }
  if (pathname === "/docs/content") {
    const pathParam = url.searchParams.get("path");
    const idParam = url.searchParams.get("id");
    if (!pathParam && !idParam) {
      return json(res, 400, { error: "Either path or id is required." });
    }

    const doc = docsIndex.docs.find((item) => {
      if (pathParam && item.path.toLowerCase() === pathParam.toLowerCase()) return true;
      if (idParam && item.id.toLowerCase() === idParam.toLowerCase()) return true;
      return false;
    });

    if (!doc) {
      return json(res, 404, { error: "Document not found." });
    }

    return json(res, 200, { data: toPublicDoc(doc, { includeContent: true }) });
  }

  return json(res, 404, { error: "Not found." });
});

server.listen(PORT, HOST, () => {
  console.log(
    `Docs API server running at http://${HOST}:${PORT} (docs: ${docsIndex.totalDocs}, source: ${SOURCE_DIR})`
  );
});
