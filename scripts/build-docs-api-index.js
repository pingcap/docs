import * as fs from "fs";
import path from "path";
import { buildDocsIndex, resolveDefaultSourceDir } from "./docs-api-lib.js";

const args = process.argv.slice(2);
const outputArg = args[0] || "tmp/docs-api-index.json";
const rootArg =
  args[1] || process.env.DOCS_API_SOURCE_DIR || resolveDefaultSourceDir(process.cwd());

const outputPath = path.resolve(outputArg);
const outputDir = path.dirname(outputPath);

if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

const sourceDir = path.resolve(rootArg);
const index = buildDocsIndex(sourceDir);
fs.writeFileSync(outputPath, JSON.stringify(index, null, 2), "utf8");

console.log(
  `Docs API index generated: ${outputPath} (${index.totalDocs} docs, ${index.features.length} features) from source: ${sourceDir}`
);
