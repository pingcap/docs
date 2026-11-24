// Check internal links in many Markdown files with a single Node.js process.
//
// Called by verify-links.sh. Starting one markdown-link-check process per file
// costs about 0.2 s of CPU time per file, which dominated the CI job time.
//
// Usage: find . -name '*.md' -print0 | node scripts/verify-links.js <config.json>
//
// Output for files with dead links is written to stdout, using the same
// "FILE: <path>" header as the markdown-link-check CLI. The exit code is 1 if
// any file has dead links, and 0 otherwise.

import * as fs from "fs";
import path from "path";
import { createRequire } from "module";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const ROOT = path.resolve(path.dirname(__filename), "..");
const CONCURRENCY = 16;
const VERBOSE = !!process.env.VERBOSE;

// Only load the repo-local version installed from package-lock.json.
const localRequire = createRequire(path.join(ROOT, "node_modules", "package.json"));
const markdownLinkCheck = localRequire("markdown-link-check");

// markdown-link-extractor calls `marked.use({ walkTokens })` on every call, and
// marked keeps every registered walkTokens hook. In a long-running process, this
// makes each file slower than the previous one. Reset the marked defaults before
// each file so that only one hook is active.
let resetMarked = () => {};
try {
  const mlcRequire = createRequire(localRequire.resolve("markdown-link-check"));
  const extractorRequire = createRequire(mlcRequire.resolve("markdown-link-extractor"));
  const { marked } = extractorRequire("marked");
  resetMarked = () => marked.setOptions(marked.getDefaults());
} catch (e) {
  console.error(`warning: cannot reset marked defaults (${e.message}); link check may be slow.`);
}

const config = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const files = fs.readFileSync(0, "utf8").split("\0").filter(Boolean);

function report(file, err, results) {
  const lines = [`FILE: ${file}`];
  if (err) {
    lines.push("ERROR: something went wrong!", String(err.stack || err));
    return { failed: true, text: lines.join("\n") + "\n" };
  }
  const dead = results.filter((r) => r.status === "dead");
  if (VERBOSE) {
    for (const r of results) lines.push(`[${r.status}] ${r.link} → Status: ${r.statusCode}`);
  }
  lines.push("", `${results.length} links checked.`);
  if (dead.length > 0) {
    lines.push("", `ERROR: ${dead.length} dead links found!`);
    for (const r of dead) lines.push(`[✖] ${r.link} → Status: ${r.statusCode}`);
  }
  return { failed: dead.length > 0, text: lines.join("\n") + "\n\n" };
}

function check(file) {
  return new Promise((resolve) => {
    let markdown;
    try {
      markdown = fs.readFileSync(file, "utf8");
    } catch (err) {
      resolve(report(file, err));
      return;
    }
    const opts = {
      ...config,
      quiet: true,
      baseUrl: "file://" + path.dirname(path.resolve(file)),
    };
    resetMarked();
    markdownLinkCheck(markdown, opts, (err, results) => resolve(report(file, err, results || [])));
  });
}

let next = 0;
let failed = 0;
async function worker() {
  while (next < files.length) {
    const result = await check(files[next++]);
    if (result.failed) {
      failed++;
      process.stdout.write(result.text);
    } else if (VERBOSE) {
      process.stderr.write(result.text);
    }
  }
}

await Promise.all(Array.from({ length: CONCURRENCY }, worker));
process.exitCode = failed > 0 ? 1 : 0;
