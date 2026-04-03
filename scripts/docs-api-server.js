import * as fs from "fs";
import http from "http";
import path from "path";
import { buildDocsIndex, docsApiSchema } from "./docs-api-lib.js";

const PORT = Number.parseInt(process.env.DOCS_API_PORT || "3000", 10);
const HOST = process.env.DOCS_API_HOST || "127.0.0.1";
const ROOT_DIR = path.resolve(process.env.DOCS_API_ROOT || process.cwd());
const PREBUILT_INDEX = process.env.DOCS_API_INDEX_FILE;

const loadIndex = () => {
  if (PREBUILT_INDEX) {
    const filePath = path.resolve(PREBUILT_INDEX);
    if (fs.existsSync(filePath)) {
      return JSON.parse(fs.readFileSync(filePath, "utf8"));
    }
  }
  return buildDocsIndex(ROOT_DIR);
};

let docsIndex = loadIndex();

const toInt = (value, fallback) => {
  const num = Number.parseInt(value, 10);
  return Number.isNaN(num) ? fallback : num;
};

const containsCI = (text, keyword) =>
  text.toLowerCase().includes(keyword.toLowerCase());

const json = (res, statusCode, payload) => {
  res.writeHead(statusCode, { "Content-Type": "application/json; charset=utf-8" });
  res.end(JSON.stringify(payload, null, 2));
};

const filterDocs = (docs, query) => {
  const feature = query.get("feature");
  const topic = query.get("topic");
  const keyword = query.get("q");
  const pathFilter = query.get("path");
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
    rows = rows.filter((doc) => {
      return (
        containsCI(doc.path, keyword) ||
        containsCI(doc.title, keyword) ||
        containsCI(doc.summary, keyword)
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
    },
    data: paged,
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

  return json(res, 404, { error: "Not found." });
});

server.listen(PORT, HOST, () => {
  console.log(
    `Docs API server running at http://${HOST}:${PORT} (docs: ${docsIndex.totalDocs})`
  );
});

