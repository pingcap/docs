---
title: TiDB Cloud CLI Command Reference
summary: Reference global options, output and query behavior, dry-run rules, help forms, errors, command families, and Filesystem aliases.
---

# TiDB Cloud CLI Command Reference

This reference describes behavior shared across the `ti` command surface.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti <command> [subcommand] [required options] [optional options] [global options]
```

The `ti` executable accepts long flags only. A one-letter flag such as `-p` is rejected.

## Command tree

```text
ti
├── configure
├── update
├── db
│   ├── create-db-cluster
│   ├── list-db-clusters
│   ├── describe-db-cluster
│   ├── update-db-cluster
│   ├── delete-db-cluster
│   ├── create-db-cluster-branch
│   ├── list-db-cluster-branches
│   ├── describe-db-cluster-branch
│   ├── delete-db-cluster-branch
│   ├── create-db-sql-users
│   ├── format-db-connection-string
│   └── execute-sql-statement
├── fs
│   ├── create-file-system
│   ├── import-file-system-token
│   ├── generate-file-system-token
│   ├── generate-file-system-scoped-token
│   ├── list-file-system-tokens
│   ├── enable-file-system-token
│   ├── disable-file-system-token
│   ├── delete-file-system-token
│   ├── refresh-file-system-token
│   ├── list-file-systems
│   ├── describe-file-system
│   ├── check-file-system
│   ├── delete-file-system
│   ├── copy-file
│   ├── read-file
│   ├── list-files
│   ├── describe-file
│   ├── move-file
│   ├── delete-file
│   ├── create-directory
│   ├── chmod-file
│   ├── create-symlink
│   ├── create-hardlink
│   ├── search-file-content
│   ├── find-files
│   ├── create-layer
│   ├── list-layers
│   ├── fork-layer
│   ├── list-layer-chain
│   ├── describe-layer
│   ├── diff-layer
│   ├── create-layer-checkpoint
│   ├── delete-layer
│   ├── rollback-layer
│   ├── commit-layer
│   ├── pack-file-system
│   ├── unpack-file-system
│   ├── mount-file-system
│   ├── drain-file-system
│   └── unmount-file-system
├── fs-git
│   ├── clone-git-workspace
│   ├── hydrate-git-workspace
│   ├── add-git-worktree
│   └── remove-git-worktree
├── fs-journal
│   ├── create-journal
│   ├── append-journal-entries
│   ├── read-journal-entries
│   ├── search-journal-entries
│   └── verify-journal
└── fs-vault
    ├── create-secret
    ├── replace-secret
    ├── read-secret
    ├── list-secrets
    ├── delete-secret
    ├── create-grant
    ├── delete-grant
    ├── list-audit-events
    ├── run-with-secret
    ├── mount-vault
    └── unmount-vault
```

Every operation has a dedicated command page with syntax and examples. Expand **Command Reference** in the documentation navigation and select a command under `ti`, `db`, `fs`, `fs-git`, `fs-journal`, or `fs-vault`.

Required options appear before optional options in generated usage. Optional options are enclosed in brackets:

```text
ti db describe-db-cluster
  --db-cluster-id <string>
  [--output <string>]
  [--view <string>]
```

In command help, value types are enclosed in angle brackets and required options include `(required)` after the option name and type:

```text
--db-cluster-name <string> (required)   Starter DB cluster display name
--wait                                  Wait until the created cluster is active
```

## Global options

- `--debug`: Enable redacted debug output.
- `--output <string>`: Set the output format to `json` or `text`. \[default: json]
- `--profile <string>`: Select a local profile. \[default: default]
- `--query <string>`: Apply a JMESPath expression before rendering the output.
- `--region <string>`: Override the profile's canonical region code for the current command, for example, `aws-us-east-1`.

Command pages document `--help`, `--version`, and all command-specific options separately.

## Output

Structured control-plane commands return JSON by default:

```bash
ti db list-db-clusters --db-cluster-type starter
```

Use text output for terminal inspection:

```bash
ti db list-db-clusters --db-cluster-type starter --output text
```

Raw byte-oriented commands such as `ti fs read-file` and `ti fs copy-file --to-stdout` write file content directly.

## JMESPath queries

`--query` runs after successful command execution and before output rendering:

```bash
ti db list-db-clusters \
  --db-cluster-type starter \
  --query 'clusters[].{id:id,name:display_name,state:state}'
```

An invalid expression fails without replacing the command result with partial output.

## Dry-run

Mutating control-plane commands declare `--dry-run`. The command validates local flags, profile, credentials, region, and request shape, then reports a plan without making the remote mutation.

```bash
ti db delete-db-cluster \
  --db-cluster-id "<cluster-id>" \
  --dry-run
```

Read-only commands reject `--dry-run`. Dry-run is not a general global simulation flag and is available only where shown in command help.

## Help and version forms

Running `ti` without a command returns exit code `2` and prints a compact command-tree synopsis to stderr:

```text
ti [ERROR]: the following arguments are required: command

The TiDB Cloud Command Line Interface is a unified tool to manage your TiDB Cloud Filesystem (FS) and Starter services.

usage: ti <command> [<subcommand>] [parameters]
To see help information, you can run:

  ti help
  ti <command> help
  ti <command> <subcommand> help
```

Use an explicit help form to display commands and flags:

```bash
ti help
ti db help
ti db create-db-cluster help
ti --help
ti db --help
ti db create-db-cluster --help
ti --version
ti fs --version
```

`help` is a command for navigating the command tree. `--help` is the conventional flag on each command; both intentionally coexist.

## Errors and exit behavior

Human-readable errors start with a blank line and use a stable prefix:

```text
ti [ERROR]: <message>
```

Errors are written to stderr and successful command output is written to stdout. Usage and configuration failures return a nonzero exit code before remote mutation. Runtime and remote API failures also return nonzero. An interrupted interactive configuration returns exit code `130`.

`--debug` can show redacted request and resolution context. It must not show API keys, FS tokens, DB passwords, SQL text, file contents, or connection strings.

## Feature guides

The following task-oriented guides explain how commands work together. They are separate from the per-command reference pages.

| Guide | Purpose |
| --- | --- |
| [Install, Configure, and Update](/ai/ti/reference/ti-install-configure-update.md) | Install releases, configure profiles, update, and uninstall `ti` |
| [Starter Databases and SQL](/ai/ti/reference/ti-starter-database.md) | Manage Starter clusters, branches, and SQL |
| [Filesystem](/ai/ti/reference/ti-filesystem.md) | Manage Filesystems, files, layers, packs, and mounts |
| [Filesystem Git Workspaces](/ai/ti/reference/ti-filesystem-git.md) | Manage Git workspaces on mounted Filesystems |
| [Filesystem Journals](/ai/ti/reference/ti-filesystem-journal.md) | Manage verifiable journals |
| [Filesystem Vault](/ai/ti/reference/ti-filesystem-vault.md) | Manage secrets and delegated access |

For complete commands and options, run:

```bash
ti <family> help
ti <family> <command> help
```

## Filesystem alias mapping

| Alias | Canonical command |
| --- | --- |
| `cp` | `copy-file` |
| `cat` | `read-file` |
| `ls` | `list-files` |
| `stat` | `describe-file` |
| `mv` | `move-file` |
| `rm` | `delete-file` |
| `mkdir` | `create-directory` |
| `chmod` | `chmod-file` |
| `symlink` | `create-symlink` |
| `hardlink` | `create-hardlink` |
| `grep` | `search-file-content` |
| `find` | `find-files` |
| `mount` | `mount-file-system` |
| `drain` | `drain-file-system` |
| `umount` | `unmount-file-system` |

Aliases use the same long flags, authentication, output, query, and error behavior as canonical commands.

## Related documentation

- [Install, Configure, and Update TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md)
- [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md)
