import * as fs from "fs";
import path from "path";
import { buildDocsIndex } from "./docs-api-lib.js";

const args = process.argv.slice(2);
const outputArg = args[0] || "tmp/docs-api-index.json";
const rootArg = args[1] || process.cwd();

const outputPath = path.resolve(outputArg);
const outputDir = path.dirname(outputPath);

if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

const index = buildDocsIndex(rootArg);
fs.writeFileSync(outputPath, JSON.stringify(index, null, 2), "utf8");

console.log(
  `Docs API index generated: ${outputPath} (${index.totalDocs} docs, ${index.features.length} features)`
);

