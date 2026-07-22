---
title: tdc CLI Reference
summary: Reference global flags, output and query behavior, dry-run rules, help forms, errors, command families, and Filesystem aliases.
---

# tdc CLI Reference

This reference describes behavior shared across the tdc command surface.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc <command> [subcommand] [required flags] [optional flags] [global flags]
```

tdc accepts long flags only. A one-letter flag such as `-p` is rejected.

## Command tree

```text
tdc
├── configure
├── update
├── organization
│   └── list-projects
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
│   ├── list-file-systems
│   ├── describe-file-system
│   ├── set-default-file-system
│   ├── unset-default-file-system
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
│   ├── describe-layer
│   ├── diff-layer
│   ├── create-layer-checkpoint
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

For each command's inputs and examples, see the family references linked in [Command families](#command-families).

Required flags appear before optional flags in generated usage. Optional flags are enclosed in brackets:

```text
tdc db describe-db-cluster
  --db-cluster-id <string>
  [--output <string>]
  [--view <string>]
```

In the generated `Flags` and `Global Flags` sections, value types are enclosed in angle brackets and required flags include `(required)` after the flag name and type:

```text
--db-cluster-name <string> (required)   Starter DB cluster display name
--project-id <string>                   TiDB Cloud project ID
```

## Global flags

| Flag | Description |
| --- | --- |
| `--profile <string>` | Select a local profile; defaults to `default` |
| `--region <string>` | Override canonical placement for this command |
| `--output <string>` | Render `json` or `text`; default is `json` |
| `--query <string>` | Apply a JMESPath expression before rendering |
| `--debug` | Print redacted debug diagnostics |
| `--help` | Display help |
| `--version` | Display tdc version information |

## Output

Structured control-plane commands return JSON by default:

```bash
tdc db list-db-clusters
```

Use text output for terminal inspection:

```bash
tdc db list-db-clusters --output text
```

Raw byte-oriented commands such as `tdc fs read-file` and `tdc fs copy-file --to-stdout` write file content directly.

## JMESPath queries

`--query` runs after successful command execution and before output rendering:

```bash
tdc db list-db-clusters \
  --query 'clusters[].{id:id,name:display_name,state:state}'

tdc organization list-projects \
  --query 'projects[?type == `tidbx_virtual`].id' \
  --output text
```

An invalid expression fails without replacing the command result with partial output.

## Dry-run

Mutating control-plane commands declare `--dry-run`. The command validates local flags, profile, credentials, region, and request shape, then reports a plan without making the remote mutation.

```bash
tdc db delete-db-cluster \
  --db-cluster-id "<cluster-id>" \
  --dry-run
```

Read-only commands reject `--dry-run`. Dry-run is not a general global simulation flag and is available only where shown in command help.

## Help and version forms

Running `tdc` without a command returns exit code `2` and prints a compact command-tree synopsis to stderr:

```text
tdc [ERROR]: the following arguments are required: command

The TiDB Cloud Command Line Interface is a unified tool to manage your TiDB Cloud Filesystem (FS) and Starter services.

usage: tdc <command> [<subcommand>] [parameters]
To see help information, you can run:

  tdc help
  tdc <command> help
  tdc <command> <subcommand> help
```

Use an explicit help form to display commands and flags:

```bash
tdc help
tdc db help
tdc db create-db-cluster help
tdc --help
tdc db --help
tdc db create-db-cluster --help
tdc --version
tdc fs --version
```

`help` is a command for navigating the command tree. `--help` is the conventional flag on each command; both intentionally coexist.

## Errors and exit behavior

Human-readable errors start with a blank line and use a stable prefix:

```text
tdc [ERROR]: <message>
```

Errors are written to stderr and successful command output is written to stdout. Usage and configuration failures return a nonzero exit code before remote mutation. Runtime and remote API failures also return nonzero. An interrupted interactive configuration returns exit code `130`.

`--debug` can show redacted request and resolution context. It must not show API keys, FS tokens, DB passwords, SQL text, file contents, or connection strings.

## Command families

| Command | Purpose |
| --- | --- |
| [`tdc configure`](/ai/tdc/reference/tdc-install-configure-update.md) | Configure a local profile |
| [`tdc update`](/ai/tdc/reference/tdc-install-configure-update.md) | Check or apply release updates |
| [`tdc organization`](/ai/tdc/reference/tdc-organization.md) | Inspect projects |
| [`tdc db`](/ai/tdc/reference/tdc-starter-database.md) | Manage Starter clusters, branches, and SQL |
| [`tdc fs`](/ai/tdc/reference/tdc-filesystem.md) | Manage Filesystems, files, layers, packs, and mounts |
| [`tdc fs-git`](/ai/tdc/reference/tdc-filesystem-git.md) | Manage Git workspaces on mounted Filesystems |
| [`tdc fs-journal`](/ai/tdc/reference/tdc-filesystem-journal.md) | Manage verifiable journals |
| [`tdc fs-vault`](/ai/tdc/reference/tdc-filesystem-vault.md) | Manage secrets and delegated access |

For complete commands and flags, run:

```bash
tdc <family> help
tdc <family> <command> help
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

- [Install, Configure, and Update tdc](/ai/tdc/reference/tdc-install-configure-update.md)
- [tdc Configuration and Credentials](/ai/tdc/reference/tdc-configuration-and-credentials.md)
