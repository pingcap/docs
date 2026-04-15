import fs from "fs";
import path from "path";
import readline from "readline";
import { loadTemplateVariables, resolveDefaultSourceDir } from "./docs-api-lib.js";

const SOURCE_DIR = path.resolve(
  process.env.DOCS_SSH_SOURCE_DIR ||
    process.env.DOCS_API_SOURCE_DIR ||
    resolveDefaultSourceDir(process.cwd())
);
const IGNORED_DIRS = new Set([".git", "node_modules", "tmp", "media"]);
const TEMPLATE_VARIABLES = loadTemplateVariables(SOURCE_DIR);

const state = {
  cwd: "/",
};

function write(text = "") {
  process.stdout.write(`${text}\n`);
}

function writeErr(text = "") {
  process.stderr.write(`${text}\n`);
}

function tokenize(input = "") {
  const tokens = [];
  const re = /"([^"]*)"|'([^']*)'|[^\s]+/g;
  let match = re.exec(input);
  while (match) {
    tokens.push(match[1] ?? match[2] ?? match[0]);
    match = re.exec(input);
  }
  return tokens;
}

function ensureSafePath(absPath) {
  const root = SOURCE_DIR.toLowerCase();
  const next = absPath.toLowerCase();
  if (next === root) return;
  if (!next.startsWith(`${root}${path.sep.toLowerCase()}`)) {
    throw new Error("Access denied.");
  }
}

function toVirtualPath(inputPath = ".") {
  const source = inputPath.trim();
  const joined = source.startsWith("/")
    ? path.posix.normalize(source)
    : path.posix.normalize(path.posix.join(state.cwd, source));
  if (!joined.startsWith("/")) return `/${joined}`;
  return joined;
}

function toAbsolutePath(inputPath = ".") {
  const virtualPath = toVirtualPath(inputPath);
  const absPath = path.resolve(SOURCE_DIR, `.${virtualPath}`);
  ensureSafePath(absPath);
  return { absPath, virtualPath };
}

function formatMode(stat) {
  return stat.isDirectory() ? "d" : "-";
}

function cmdHelp() {
  write("TiDB Docs SSH Shell (read-only)");
  write("Commands:");
  write("  help");
  write("  pwd");
  write("  ls [path]");
  write("  cd <path>");
  write("  cat <file>");
  write("  find [path] [keyword]");
  write("  grep <keyword> [path]");
  write("  exit | quit");
}

function cmdPwd() {
  write(state.cwd);
}

function cmdLs(args) {
  const target = args[0] || ".";
  const { absPath } = toAbsolutePath(target);
  const stat = fs.statSync(absPath);

  if (stat.isFile()) {
    write(path.basename(absPath));
    return;
  }

  const rows = fs
    .readdirSync(absPath, { withFileTypes: true })
    .filter((entry) => !entry.name.startsWith("."))
    .sort((a, b) => {
      if (a.isDirectory() !== b.isDirectory()) return a.isDirectory() ? -1 : 1;
      return a.name.localeCompare(b.name);
    });

  rows.forEach((entry) => {
    const p = path.join(absPath, entry.name);
    const s = fs.statSync(p);
    write(`${formatMode(s)} ${entry.name}`);
  });
}

function cmdCd(args) {
  if (!args[0]) {
    state.cwd = "/";
    return;
  }
  const { absPath, virtualPath } = toAbsolutePath(args[0]);
  const stat = fs.statSync(absPath);
  if (!stat.isDirectory()) throw new Error("Not a directory.");
  state.cwd = virtualPath;
}

function replaceTemplateVariables(content) {
  return content.replace(/{{{\s*\.(.+?)\s*}}}/g, (match, keyPath) => {
    const value = keyPath
      .trim()
      .split(".")
      .reduce((acc, key) => (acc !== undefined && acc !== null ? acc[key] : ""), TEMPLATE_VARIABLES);
    if (value === undefined || value === null || value === "") return match;
    return String(value);
  });
}

function cmdCat(args) {
  if (!args[0]) throw new Error("Usage: cat <file>");
  const { absPath } = toAbsolutePath(args[0]);
  const stat = fs.statSync(absPath);
  if (!stat.isFile()) throw new Error("Not a file.");
  const raw = fs.readFileSync(absPath, "utf8");
  write(replaceTemplateVariables(raw));
}

function walkFiles(startAbsPath, onFile) {
  const st = fs.statSync(startAbsPath);
  if (st.isFile()) {
    onFile(startAbsPath);
    return;
  }
  const entries = fs.readdirSync(startAbsPath, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.name.startsWith(".")) continue;
    if (entry.isDirectory() && IGNORED_DIRS.has(entry.name)) continue;
    const p = path.join(startAbsPath, entry.name);
    if (entry.isDirectory()) {
      walkFiles(p, onFile);
    } else if (entry.isFile()) {
      onFile(p);
    }
  }
}

function toDisplayPath(absPath) {
  const rel = path.relative(SOURCE_DIR, absPath).replaceAll("\\", "/");
  return `/${rel}`;
}

function cmdFind(args) {
  const base = args[0] || ".";
  const keyword = (args[1] || "").toLowerCase();
  const { absPath } = toAbsolutePath(base);
  const rows = [];

  walkFiles(absPath, (filePath) => {
    const display = toDisplayPath(filePath);
    if (!keyword || display.toLowerCase().includes(keyword)) {
      rows.push(display);
    }
  });

  rows.sort((a, b) => a.localeCompare(b)).forEach((row) => write(row));
}

function cmdGrep(args) {
  const keyword = args[0];
  if (!keyword) throw new Error("Usage: grep <keyword> [path]");
  const base = args[1] || ".";
  const keywordLower = keyword.toLowerCase();
  const { absPath } = toAbsolutePath(base);
  let hitCount = 0;

  walkFiles(absPath, (filePath) => {
    if (!filePath.endsWith(".md")) return;
    let content;
    try {
      content = fs.readFileSync(filePath, "utf8");
    } catch (_error) {
      return;
    }
    const lines = content.split(/\r?\n/);
    lines.forEach((line, index) => {
      if (line.toLowerCase().includes(keywordLower)) {
        hitCount += 1;
        write(`${toDisplayPath(filePath)}:${index + 1}:${line}`);
      }
    });
  });

  if (hitCount === 0) write("(no matches)");
}

function runCommand(line) {
  const tokens = tokenize(line);
  if (tokens.length === 0) return true;

  const [cmd, ...args] = tokens;
  if (cmd === "help") {
    cmdHelp();
    return true;
  }
  if (cmd === "pwd") {
    cmdPwd();
    return true;
  }
  if (cmd === "ls") {
    cmdLs(args);
    return true;
  }
  if (cmd === "cd") {
    cmdCd(args);
    return true;
  }
  if (cmd === "cat") {
    cmdCat(args);
    return true;
  }
  if (cmd === "find") {
    cmdFind(args);
    return true;
  }
  if (cmd === "grep") {
    cmdGrep(args);
    return true;
  }
  if (cmd === "exit" || cmd === "quit") {
    return false;
  }
  throw new Error(`Unsupported command: ${cmd}`);
}

function runSingle(commandLine) {
  try {
    runCommand(commandLine);
    process.exit(0);
  } catch (error) {
    writeErr(String(error.message || error));
    process.exit(1);
  }
}

function startInteractive() {
  write(`TiDB Docs SSH Shell connected (root=${SOURCE_DIR})`);
  write("Type `help` for available commands.");

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    prompt: "docs> ",
  });

  rl.prompt();

  rl.on("line", (line) => {
    try {
      const keepGoing = runCommand(line.trim());
      if (!keepGoing) {
        rl.close();
        return;
      }
    } catch (error) {
      writeErr(String(error.message || error));
    }
    rl.prompt();
  });

  rl.on("close", () => process.exit(0));
}

const cliCommand = (() => {
  const args = process.argv.slice(2);
  const commandIndex = args.findIndex((item) => item === "-c" || item === "--command");
  if (commandIndex >= 0 && args[commandIndex + 1]) {
    return args[commandIndex + 1];
  }
  if (process.env.SSH_ORIGINAL_COMMAND) {
    return process.env.SSH_ORIGINAL_COMMAND;
  }
  return "";
})();

if (cliCommand) {
  runSingle(cliCommand);
} else {
  startInteractive();
}
