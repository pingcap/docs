import * as fs from "fs";
import path from "path";

const DOC_IGNORE_DIRS = new Set(["node_modules", ".git", "media", "tmp"]);
const DOC_IGNORE_FILES = new Set(["api/docs-json-api.md"]);

const MAX_SUMMARY_LENGTH = 220;

const toPosixPath = (filePath) => filePath.replaceAll("\\", "/");

const safeString = (value) => (typeof value === "string" ? value : "");

const slugify = (input = "") =>
  input
    .toLowerCase()
    .trim()
    .replace(/[`~!@#$%^&*()+=[\]{}|\\:;"'<>,.?/]+/g, "")
    .replace(/\s+/g, "-");

const getValueByPath = (obj, keyPath) => {
  return (
    keyPath
      .split(".")
      .reduce((acc, key) => (acc !== undefined && acc !== null ? acc[key] : ""), obj) ?? ""
  );
};

const replaceTemplateVariables = (content, variables = {}) => {
  const variablePattern = /{{{\s*\.(.+?)\s*}}}/g;
  return content.replace(variablePattern, (match, variablePath) => {
    const value = getValueByPath(variables, variablePath.trim());
    if (value === undefined || value === null || value === "") {
      return match;
    }
    return String(value);
  });
};

const parseScalar = (raw) => {
  const value = raw.trim();
  if (value === "true") return true;
  if (value === "false") return false;
  if (/^-?\d+$/.test(value)) return Number.parseInt(value, 10);
  if (/^-?\d+\.\d+$/.test(value)) return Number.parseFloat(value);
  if (
    (value.startsWith('"') && value.endsWith('"')) ||
    (value.startsWith("'") && value.endsWith("'"))
  ) {
    return value.slice(1, -1);
  }
  return value;
};

const parseSimpleYaml = (raw = "") => {
  const result = {};
  let currentArrayKey = null;

  raw.split(/\r?\n/).forEach((line) => {
    if (!line.trim() || line.trim().startsWith("#")) {
      return;
    }

    const kvMatch = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (kvMatch) {
      const key = kvMatch[1];
      const value = kvMatch[2];
      if (!value.trim()) {
        result[key] = [];
        currentArrayKey = key;
      } else {
        result[key] = parseScalar(value);
        currentArrayKey = null;
      }
      return;
    }

    const listMatch = line.match(/^\s*-\s*(.*)$/);
    if (listMatch && currentArrayKey) {
      result[currentArrayKey].push(parseScalar(listMatch[1]));
      return;
    }

    currentArrayKey = null;
  });

  return result;
};

const extractFrontMatter = (content) => {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
  if (!match) {
    return {
      raw: "",
      data: {},
    };
  }
  return {
    raw: match[1],
    data: parseSimpleYaml(match[1]),
  };
};

const stripFrontMatter = (content) =>
  content.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n?/, "");

const stripInlineMarkdown = (text) =>
  text
    .replace(/`([^`]+)`/g, "$1")
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, "$1")
    .replace(/[*_~>#]/g, "")
    .replace(/\s+/g, " ")
    .trim();

const collectMarkdownFiles = (rootDir) => {
  const results = [];
  const walk = (dir) => {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.isDirectory()) {
        if (entry.name.startsWith(".") || DOC_IGNORE_DIRS.has(entry.name)) continue;
        walk(path.join(dir, entry.name));
        continue;
      }
      if (!entry.isFile()) continue;
      if (!entry.name.endsWith(".md")) continue;
      const absPath = path.join(dir, entry.name);
      const relativePath = toPosixPath(path.relative(rootDir, absPath));
      if (DOC_IGNORE_FILES.has(relativePath)) continue;
      results.push(absPath);
    }
  };
  walk(rootDir);
  return results;
};

const parseHeadingsAndSummary = (content) => {
  const lines = stripFrontMatter(content).split(/\r?\n/);
  const headings = [];
  let summary = "";
  let inCodeBlock = false;
  let paragraphBuffer = [];

  const flushParagraph = () => {
    if (summary || paragraphBuffer.length === 0) {
      paragraphBuffer = [];
      return;
    }
    const text = stripInlineMarkdown(paragraphBuffer.join(" ").trim());
    if (text) {
      summary = truncate(text);
    }
    paragraphBuffer = [];
  };

  for (const rawLine of lines) {
    const line = rawLine.trim();

    if (line.startsWith("```")) {
      inCodeBlock = !inCodeBlock;
      continue;
    }
    if (inCodeBlock) continue;

    const headingMatch = line.match(/^(#{1,6})\s+(.*)$/);
    if (headingMatch) {
      flushParagraph();
      const level = headingMatch[1].length;
      const text = stripInlineMarkdown(headingMatch[2]);
      if (text) {
        headings.push({
          level,
          text,
          slug: slugify(text),
        });
      }
      continue;
    }

    if (!line) {
      flushParagraph();
      continue;
    }

    if (
      line.startsWith("- ") ||
      line.startsWith("* ") ||
      line.startsWith("> ") ||
      line.startsWith("|") ||
      /^\d+\.\s+/.test(line)
    ) {
      continue;
    }

    paragraphBuffer.push(line);
  }

  flushParagraph();
  return { headings, summary };
};

const inferProduct = (docPath) => {
  if (docPath.startsWith("tidb-cloud/")) return "tidb-cloud";
  if (docPath.startsWith("dm/")) return "dm";
  if (docPath.startsWith("br/")) return "br";
  if (docPath.startsWith("ticdc/")) return "ticdc";
  if (docPath.startsWith("tiflash/")) return "tiflash";
  if (docPath.startsWith("tiup/")) return "tiup";
  return "tidb";
};

const extractFeatures = (content, frontMatterData) => {
  const features = new Set();
  const varRegex = /\b[a-z]+(?:_[a-z0-9]+){2,}\b/g;
  for (const match of content.matchAll(varRegex)) {
    const token = match[0];
    if (
      token.startsWith("tidb_") ||
      token.startsWith("tikv_") ||
      token.startsWith("pd_") ||
      token.startsWith("tiflash_")
    ) {
      features.add(token);
    }
  }

  const fmFeatureKeys = ["feature", "features", "tag", "tags"];
  fmFeatureKeys.forEach((key) => {
    const value = frontMatterData[key];
    if (Array.isArray(value)) {
      value.forEach((item) => {
        if (typeof item === "string" && item.trim()) {
          features.add(item.trim());
        }
      });
      return;
    }
    if (typeof value === "string" && value.trim()) {
      features.add(value.trim());
    }
  });

  return [...features];
};

const truncate = (text, limit = MAX_SUMMARY_LENGTH) => {
  if (!text) return "";
  if (text.length <= limit) return text;
  return `${text.slice(0, limit - 3)}...`;
};

const normalizeTopics = (docPath, frontMatterData) => {
  const segments = docPath
    .replace(/\.md$/, "")
    .split("/")
    .map((segment) => segment.trim())
    .filter(Boolean);
  const topics = new Set(segments.slice(0, -1));

  const fmTopicKeys = ["topic", "topics", "category", "categories"];
  fmTopicKeys.forEach((key) => {
    const value = frontMatterData[key];
    if (Array.isArray(value)) {
      value.forEach((item) => {
        if (typeof item === "string" && item.trim()) topics.add(item.trim());
      });
      return;
    }
    if (typeof value === "string" && value.trim()) {
      topics.add(value.trim());
    }
  });

  return [...topics];
};

const parseMarkdownDoc = (rootDir, absPath, variables) => {
  const relativePath = toPosixPath(path.relative(rootDir, absPath));
  const originalRaw = fs.readFileSync(absPath, "utf8");
  const raw = replaceTemplateVariables(originalRaw, variables);
  const { data: frontMatter, raw: frontMatterRaw } = extractFrontMatter(raw);
  const { headings, summary } = parseHeadingsAndSummary(raw);
  let title = safeString(frontMatter.title);
  if (!title) {
    const h1 = headings.find((item) => item.level === 1);
    if (h1) title = h1.text;
  }

  if (!title) {
    title = path.basename(relativePath, ".md");
  }

  const docStat = fs.statSync(absPath);
  const features = extractFeatures(raw, frontMatter).sort();
  const topics = normalizeTopics(relativePath, frontMatter).sort();

  return {
    id: relativePath.replace(/\.md$/, ""),
    path: relativePath,
    title,
    summary,
    product: inferProduct(relativePath),
    topics,
    features,
    headings,
    frontMatter,
    frontMatterRaw,
    updatedAt: docStat.mtime.toISOString(),
  };
};

export const buildDocsIndex = (rootDir = process.cwd()) => {
  const normalizedRoot = path.resolve(rootDir);
  const variablesPath = path.join(normalizedRoot, "variables.json");
  let variables = {};
  if (fs.existsSync(variablesPath)) {
    try {
      variables = JSON.parse(fs.readFileSync(variablesPath, "utf8"));
    } catch (error) {
      console.warn(
        `Warning: failed to parse variables.json at ${variablesPath}, continuing without variable replacement.`
      );
    }
  }

  const mdFiles = collectMarkdownFiles(normalizedRoot);

  const docs = mdFiles
    .map((absPath) => parseMarkdownDoc(normalizedRoot, absPath, variables))
    .sort((a, b) => a.path.localeCompare(b.path));

  const topicSet = new Set();
  const featureSet = new Set();
  docs.forEach((doc) => {
    doc.topics.forEach((topic) => topicSet.add(topic));
    doc.features.forEach((feature) => featureSet.add(feature));
  });

  return {
    schemaVersion: "1.0.0",
    generatedAt: new Date().toISOString(),
    totalDocs: docs.length,
    topics: [...topicSet].sort(),
    features: [...featureSet].sort(),
    docs,
  };
};

export const resolveDefaultSourceDir = (baseDir = process.cwd()) => {
  const normalizedBase = path.resolve(baseDir);
  const siblingDocsStaging = path.resolve(normalizedBase, "..", "docs-staging");
  if (fs.existsSync(siblingDocsStaging) && fs.statSync(siblingDocsStaging).isDirectory()) {
    return siblingDocsStaging;
  }
  return normalizedBase;
};

export const docsApiSchema = {
  schemaVersion: "1.0.0",
  endpoints: {
    "/docs": {
      method: "GET",
      query: {
        feature: "Exact feature token filter, case-insensitive.",
        topic: "Topic/category filter, case-insensitive.",
        q: "Keyword match in path/title/summary, case-insensitive.",
        path: "Exact document path filter, case-insensitive.",
        limit: "Page size. Default 20, max 100.",
        offset: "Pagination offset. Default 0.",
      },
      response: {
        meta: {
          total: "Matched document count before pagination.",
          limit: "Applied page size.",
          offset: "Applied offset.",
          returned: "Number of docs in data.",
        },
        data: "Array<DocRecord>",
      },
    },
    "/topics": {
      method: "GET",
      response: "Array<string>",
    },
    "/features": {
      method: "GET",
      query: {
        prefix: "Optional prefix filter.",
      },
      response: "Array<string>",
    },
    "/schema": {
      method: "GET",
      response: "This schema document.",
    },
    "/healthz": {
      method: "GET",
      response: "{ ok: true }",
    },
  },
  docRecord: {
    id: "string",
    path: "string",
    title: "string",
    summary: "string",
    product: "string",
    topics: "string[]",
    features: "string[]",
    headings: "Array<{level:number,text:string,slug:string}>",
    frontMatter: "object",
    frontMatterRaw: "string",
    updatedAt: "ISO-8601 string",
  },
};
