import * as fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import glob from "glob";

import { visit } from "unist-util-visit";

import { generateMdAstFromFile } from "./utils.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, "..");

const SPECIAL_IMPLICIT_TARGETS = new Set(["_index.md", "_docHome.md"]);
const EXCLUDED_TOC_FILES = new Set(["TOC-pingkai.md"]);

const CLOUD_TOC_FILES = [
  "TOC-tidb-cloud.md",
  "TOC-tidb-cloud-premium.md",
  "TOC-tidb-cloud-starter.md",
  "TOC-tidb-cloud-essential.md",
];

const PREFIX_TO_TOC = [
  { prefix: "ai/", toc: "TOC-ai.md" },
  { prefix: "api/", toc: "TOC-api.md" },
  { prefix: "develop/", toc: "TOC-develop.md" },
  { prefix: "releases/", toc: "TOC-tidb-releases.md" },
  { prefix: "tidb-cloud/releases/", toc: "TOC-tidb-cloud-releases.md" },
  { prefix: "best-practices/", toc: "TOC-best-practices.md" },
];

function isExternalUrl(url = "") {
  return (
    url.startsWith("//") || url.includes("://") || url.startsWith("mailto:")
  );
}

function stripQueryAndHash(url = "") {
  const q = url.split("?")[0];
  const [p, hash] = q.split("#");
  return { path: p, hash: hash || "" };
}

function isInternalDocLink(url = "") {
  if (!url) return false;
  if (isExternalUrl(url)) return false;
  if (!url.startsWith("/")) return false;
  if (url.startsWith("/media/")) return false;
  const { path: p } = stripQueryAndHash(url);
  return p.endsWith(".md") || p.endsWith(".mdx");
}

function extractUrlsFromMarkdownFile(absPath) {
  const buf = fs.readFileSync(absPath);
  const ast = generateMdAstFromFile(buf);
  const urls = [];
  visit(ast, ["link", "definition"], (node) => {
    if (typeof node.url === "string" && node.url.trim()) {
      urls.push(node.url.trim());
    }
  });
  return urls;
}

function readTocFiles() {
  const tocFiles = glob
    .sync("TOC*.md", { cwd: ROOT, nodir: true })
    .filter((f) => !EXCLUDED_TOC_FILES.has(f))
    .sort((a, b) => a.localeCompare(b));
  return tocFiles;
}

function buildTocIndex(tocFiles) {
  const tocToPages = new Map(); // tocFile -> Set(relPathWithoutLeadingSlash)
  const anyTocPages = new Set();

  for (const toc of tocFiles) {
    const tocAbs = path.join(ROOT, toc);
    const urls = extractUrlsFromMarkdownFile(tocAbs);
    const pages = new Set();

    for (const url of urls) {
      if (!isInternalDocLink(url)) continue;
      const { path: p } = stripQueryAndHash(url);
      const rel = p.replace(/^\/+/, "");
      pages.add(rel);
      anyTocPages.add(rel);
    }

    tocToPages.set(toc, pages);
  }

  return { tocToPages, anyTocPages };
}

function expectedSetForTarget(targetRel, tocToPages, anyTocPages) {
  if (
    targetRel === "_index.md" ||
    targetRel.endsWith("/_index.md") ||
    targetRel === "_docHome.md" ||
    targetRel.endsWith("/_docHome.md")
  ) {
    return { ok: true };
  }

  if (
    targetRel.startsWith("tidb-cloud/") &&
    !targetRel.startsWith("tidb-cloud/releases/")
  ) {
    const union = new Set();
    for (const toc of CLOUD_TOC_FILES) {
      const set = tocToPages.get(toc);
      if (!set) continue;
      for (const p of set) union.add(p);
    }
    return {
      ok: union.has(targetRel),
      expectedLabel: "any TiDB Cloud TOC",
    };
  }

  for (const { prefix, toc } of PREFIX_TO_TOC) {
    if (targetRel.startsWith(prefix)) {
      const set = tocToPages.get(toc) || new Set();
      return { ok: set.has(targetRel), expectedLabel: toc };
    }
  }

  // Default: the target appears in any TOC*.md
  return { ok: anyTocPages.has(targetRel), expectedLabel: "any TOC*.md" };
}

function main() {
  process.chdir(ROOT);

  const tocFiles = readTocFiles();
  if (tocFiles.length === 0) {
    console.error("TOC check error: no TOC*.md files found in repo root.");
    process.exit(1);
  }

  const { tocToPages, anyTocPages } = buildTocIndex(tocFiles);
  const buildScopePages = [...anyTocPages].sort((a, b) => a.localeCompare(b));

  const missingScopePages = [];
  const violations = [];

  for (const sourceRel of buildScopePages) {
    const sourceAbs = path.join(ROOT, sourceRel);
    if (!fs.existsSync(sourceAbs)) {
      missingScopePages.push(sourceRel);
      continue;
    }

    const urls = extractUrlsFromMarkdownFile(sourceAbs);
    for (const url of urls) {
      if (!isInternalDocLink(url)) continue;
      const { path: p } = stripQueryAndHash(url);
      const targetRel = p.replace(/^\/+/, "");

      if (SPECIAL_IMPLICIT_TARGETS.has(path.basename(targetRel))) {
        continue;
      }

      const { ok, expectedLabel } = expectedSetForTarget(
        targetRel,
        tocToPages,
        anyTocPages
      );
      if (!ok) {
        violations.push({ sourceRel, url, targetRel, expectedLabel });
      }
    }
  }

  if (missingScopePages.length > 0) {
    console.error(
      `TOC check error: ${missingScopePages.length} pages referenced by TOC*.md do not exist on disk.`
    );
    for (const p of missingScopePages.slice(0, 50)) {
      console.error(`- missing: ${p}`);
    }
    if (missingScopePages.length > 50) {
      console.error(`- ... and ${missingScopePages.length - 50} more`);
    }
  }

  if (violations.length > 0) {
    console.error(
      `TOC check error: ${violations.length} internal doc links point to targets not included in the expected TOC.`
    );
    for (const v of violations.slice(0, 100)) {
      console.error(
        `- ${v.sourceRel}: ${v.url} (target: ${v.targetRel}; expected: ${v.expectedLabel})`
      );
    }
    if (violations.length > 100) {
      console.error(`- ... and ${violations.length - 100} more`);
    }
  }

  if (missingScopePages.length > 0 || violations.length > 0) {
    process.exit(1);
  }

  console.log(
    `TOC check report: OK. Checked ${buildScopePages.length} in-scope pages (from TOC*.md) and found no TOC membership violations.`
  );
}

main();
