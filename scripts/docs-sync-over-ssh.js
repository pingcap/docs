import fs from "fs";
import path from "path";
import { spawnSync } from "child_process";

const REPO = process.env.DOCS_SYNC_REPO || "git@github.com:pingcap/docs.git";
const BRANCH = process.env.DOCS_SYNC_BRANCH || "master";
const TARGET_DIR = path.resolve(process.env.DOCS_SYNC_TARGET_DIR || "../docs-upstream");
const GIT_SSH_COMMAND = process.env.DOCS_SYNC_SSH_COMMAND || "";

function runGit(args, cwd = process.cwd()) {
  const env = { ...process.env };
  if (GIT_SSH_COMMAND) env.GIT_SSH_COMMAND = GIT_SSH_COMMAND;

  const result = spawnSync("git", args, {
    cwd,
    env,
    stdio: "inherit",
    shell: false,
  });

  if (result.status !== 0) {
    throw new Error(`git ${args.join(" ")} failed with exit code ${result.status ?? 1}`);
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
  runGit(["fetch", "--depth", "1", "origin", BRANCH], TARGET_DIR);
  runGit(["checkout", BRANCH], TARGET_DIR);
  runGit(["merge", "--ff-only", `origin/${BRANCH}`], TARGET_DIR);
}

function currentHead() {
  const result = spawnSync("git", ["rev-parse", "--short", "HEAD"], {
    cwd: TARGET_DIR,
    encoding: "utf8",
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
    `Docs synced via SSH: repo=${REPO}, branch=${BRANCH}, target=${TARGET_DIR}, head=${currentHead()}`
  );
} catch (error) {
  console.error(String(error.message || error));
  process.exit(1);
}
