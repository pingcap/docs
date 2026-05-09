import fs from "fs";
import path from "path";
import { spawnSync } from "child_process";

const REPO = process.env.DOCS_SYNC_REPO || "git@github.com:pingcap/docs.git";
const BRANCH = process.env.DOCS_SYNC_BRANCH || "master";
const TARGET_DIR = path.resolve(process.env.DOCS_SYNC_TARGET_DIR || "../docs-upstream");
const GIT_SSH_COMMAND = process.env.DOCS_SYNC_SSH_COMMAND || "";
const COMMAND_TIMEOUT_MS = Number.parseInt(process.env.DOCS_SYNC_TIMEOUT_MS || "120000", 10);

const SSH_BIN = process.env.DOCS_SYNC_SSH_BIN || "ssh";
const SSH_KEY_PATH = process.env.DOCS_SYNC_SSH_KEY_PATH || "";
const SSH_PORT = process.env.DOCS_SYNC_SSH_PORT || "";
const SSH_STRICT_HOST_KEY_CHECKING =
  process.env.DOCS_SYNC_SSH_STRICT_HOST_KEY_CHECKING || "";
const SSH_USER_KNOWN_HOSTS_FILE = process.env.DOCS_SYNC_SSH_USER_KNOWN_HOSTS_FILE || "";
const SSH_EXTRA_OPTIONS = process.env.DOCS_SYNC_SSH_EXTRA_OPTIONS || "";

function quoteShellArg(value) {
  if (value === "") return "''";
  return `'${String(value).replaceAll("'", "'\"'\"'")}'`;
}

function parseExtraSshOptions(raw) {
  if (!raw.trim()) return [];
  return raw
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function buildGitSshCommand() {
  if (GIT_SSH_COMMAND) return GIT_SSH_COMMAND;

  const parts = [SSH_BIN];
  if (SSH_KEY_PATH) {
    parts.push("-i", SSH_KEY_PATH);
  }
  if (SSH_PORT) {
    parts.push("-p", SSH_PORT);
  }
  if (SSH_STRICT_HOST_KEY_CHECKING) {
    parts.push("-o", `StrictHostKeyChecking=${SSH_STRICT_HOST_KEY_CHECKING}`);
  }
  if (SSH_USER_KNOWN_HOSTS_FILE) {
    parts.push("-o", `UserKnownHostsFile=${SSH_USER_KNOWN_HOSTS_FILE}`);
  }
  for (const option of parseExtraSshOptions(SSH_EXTRA_OPTIONS)) {
    parts.push("-o", option);
  }
  return parts.map(quoteShellArg).join(" ");
}

const EFFECTIVE_GIT_SSH_COMMAND = buildGitSshCommand();

function runGit(args, cwd = process.cwd()) {
  const env = { ...process.env };
  env.GIT_SSH_COMMAND = EFFECTIVE_GIT_SSH_COMMAND;

  const result = spawnSync("git", args, {
    cwd,
    env,
    encoding: "utf8",
    stdio: "pipe",
    timeout: COMMAND_TIMEOUT_MS,
    shell: false,
  });

  const stdout = String(result.stdout || "");
  const stderr = String(result.stderr || "");
  if (stdout) process.stdout.write(stdout);
  if (stderr) process.stderr.write(stderr);

  if (result.error) {
    if (result.error.code === "ETIMEDOUT") {
      throw new Error(
        `git ${args.join(" ")} timed out after ${COMMAND_TIMEOUT_MS} ms`
      );
    }
    throw new Error(
      `git ${args.join(" ")} failed: ${String(result.error.message || result.error)}`
    );
  }

  if (result.status !== 0) {
    const detail = stderr.trim() || stdout.trim() || "no command output";
    throw new Error(
      `git ${args.join(" ")} failed with exit code ${result.status ?? 1}: ${detail}`
    );
  }
}

function cloneIfMissing() {
  if (fs.existsSync(TARGET_DIR) && fs.statSync(TARGET_DIR).isDirectory()) {
    return false;
  }

  const parentDir = path.dirname(TARGET_DIR);
  if (!fs.existsSync(parentDir)) fs.mkdirSync(parentDir, { recursive: true });

  runGit(["clone", "--depth", "1", "--branch", BRANCH, REPO, TARGET_DIR], process.cwd());
  return true;
}

function syncExistingRepo() {
  const gitDir = path.join(TARGET_DIR, ".git");
  if (!fs.existsSync(gitDir)) {
    throw new Error(`Target directory exists but is not a git repository: ${TARGET_DIR}`);
  }
  runGit(["fetch", "--depth", "1", "origin", BRANCH], TARGET_DIR);
  runGit(["checkout", BRANCH], TARGET_DIR);
  runGit(["merge", "--ff-only", `origin/${BRANCH}`], TARGET_DIR);
}

function currentHead() {
  const result = spawnSync("git", ["rev-parse", "--short", "HEAD"], {
    cwd: TARGET_DIR,
    encoding: "utf8",
    timeout: COMMAND_TIMEOUT_MS,
    shell: false,
  });
  if (result.status !== 0) return "unknown";
  return String(result.stdout || "").trim() || "unknown";
}

try {
  const cloned = cloneIfMissing();
  if (!cloned) {
    syncExistingRepo();
  }
  console.log(
    `Docs synced via SSH: repo=${REPO}, branch=${BRANCH}, target=${TARGET_DIR}, head=${currentHead()}, timeoutMs=${COMMAND_TIMEOUT_MS}`
  );
} catch (error) {
  console.error(String(error.message || error));
  process.exit(1);
}
