---
title: TiDB Docs over SSH
summary: Use a read-only SSH shell to browse and search TiDB documentation, and sync docs from Git over SSH.
---

# TiDB Docs over SSH

This guide shows how to expose TiDB documentation through a read-only SSH shell.

With this setup, you can:

- browse docs files over SSH
- search docs content using shell commands
- sync docs from a Git repository over SSH

## Prerequisites

Before you begin, ensure you have the following:

- **Node.js 18 or later**
- **Git with SSH access** to your docs repository (for sync)
- **The docs repository cloned locally**

## Quick start

From the repository root, start the docs SSH shell:

```bash
npm run docs-ssh:shell
```

You can then run read-only commands in interactive mode.

## Supported commands

The SSH shell supports the following commands:

- `help`
- `pwd`
- `ls [path]`
- `cd <path>`
- `cat <file>`
- `find [path] [keyword]`
- `grep <keyword> [path]`
- `exit` or `quit`

## Run a single command

For automation or remote execution, run one command and exit:

```bash
node scripts/docs-ssh-shell.js --command "ls /ai/integrations"
```

You can also run content search:

```bash
node scripts/docs-ssh-shell.js --command "grep TiDB /ai/integrations/tidb-docs-mcp-server.md"
```

## Sync docs from Git over SSH

Use the following command to clone or fast-forward sync docs:

```bash
npm run docs-sync:ssh
```

You can configure the sync target with environment variables:

- `DOCS_SYNC_REPO`: SSH Git URL. Default: `git@github.com:pingcap/docs.git`
- `DOCS_SYNC_BRANCH`: branch to sync. Default: `master`
- `DOCS_SYNC_TARGET_DIR`: local target directory. Default: `../docs-upstream`
- `DOCS_SYNC_SSH_COMMAND`: custom SSH command for Git, such as identity file options

Example:

```bash
DOCS_SYNC_REPO=git@github.com:pingcap/docs.git \
DOCS_SYNC_BRANCH=master \
DOCS_SYNC_TARGET_DIR=/srv/tidb/docs-upstream \
npm run docs-sync:ssh
```

## Expose as an SSH endpoint

You can attach the shell to `sshd` using `ForceCommand`.

Example `sshd_config` snippet:

```sshconfig
Match User tidbdocs
  ForceCommand /usr/bin/node /srv/tidb/docs/scripts/docs-ssh-shell.js
  PermitTTY yes
  X11Forwarding no
  AllowTcpForwarding no
```

After this configuration, users can connect and run the docs shell through SSH.

## Use with Cursor and Claude Code

You can use the SSH endpoint in two patterns:

- interactive shell session
- one-command execution

### Interactive shell session

Connect to the docs SSH endpoint and run commands manually:

```bash
ssh tidbdocs@<your-host>
```

Then run commands such as:

```bash
ls /ai/integrations
grep TiDB /ai/integrations/tidb-docs-mcp-server.md
cat /ai/integrations/tidb-docs-over-ssh.md
```

### One-command execution

Run a single command from your local terminal and return output directly:

```bash
ssh tidbdocs@<your-host> "grep TiDB /ai/integrations/tidb-docs-mcp-server.md"
```

You can copy this pattern into your Cursor terminal or Claude Code terminal whenever you need fast doc lookup.

## Command cheat sheet

Use the following command patterns for common doc lookup tasks.

### Find a system variable

```bash
ssh tidbdocs@<your-host> "grep tidb_enable_dist_task /system-variables.md"
```

### Find docs related to performance tuning

```bash
ssh tidbdocs@<your-host> "find / tuning"
```

### Find release notes for a specific version

```bash
ssh tidbdocs@<your-host> "find /release-notes 8.5"
```

### Search a keyword in all AI integration docs

```bash
ssh tidbdocs@<your-host> "grep MCP /ai/integrations"
```

### Open one specific doc quickly

```bash
ssh tidbdocs@<your-host> "cat /ai/integrations/tidb-docs-mcp-server.md"
```

### Verify available files in a directory

```bash
ssh tidbdocs@<your-host> "ls /ai/integrations"
```

## Security notes

- The shell is read-only and only supports a fixed command set.
- Paths are restricted to the configured docs root directory.
- Commands outside the allowlist are rejected.

## Troubleshooting

- **`Unsupported command`**
  - Use only commands listed in **Supported commands**.
- **`Access denied`**
  - Check whether the requested path is outside the docs root.
- **`git ... failed` when syncing**
  - Verify SSH keys, repository permissions, and branch name.

## See also

- [TiDB Docs MCP Server](/ai/integrations/tidb-docs-mcp-server.md)
- [TiDB MCP Server](/ai/integrations/tidb-mcp-server.md)
