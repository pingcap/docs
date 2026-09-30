---
title: TiDB Cloud CLI (`ti`) Command Reference
summary: Reference TiDB Cloud CLI command groups, syntax, global options, output, dry-run behavior, help forms, and errors.
---

# TiDB Cloud CLI (`ti`) Command Reference

This page describes the command structure and behavior shared by [TiDB Cloud CLI (`ti`)](/ai/ti/ti-overview.md) commands. For the syntax and options of an individual command, select its command group or use the documentation navigation.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti <command> [options] [global options]
ti <command-group> <command> [options] [global options]
```

For example:

```bash
ti configure --profile staging
ti db list-db-clusters --db-cluster-type starter
```

The `ti` executable accepts long options only. A one-letter option such as `-p` is rejected.

In generated usage, specify required options before optional options, and use square brackets to enclose optional options:

```text
ti db describe-db-cluster
  --db-cluster-id <string>
  [--output <string>]
  [--view <string>]
```

Value types are enclosed in angle brackets. In command help, `(required)` follows the name and type of each required option:

```text
--db-cluster-name <string> (required)   Starter DB cluster display name
--wait                                  Wait until the created cluster is active
```

## Commands and command groups

Use the following table to find the reference for a top-level command or command group. Each command page includes its syntax, options, and examples.

| Command or command group | Purpose | Reference |
| --- | --- | --- |
| `configure` | Configure local profiles, API keys, and the default region. | [`ti configure`](/ai/ti/reference/ti-configure.md) |
| `update` | Check for and install TiDB Cloud CLI updates. | [`ti update`](/ai/ti/reference/ti-update.md) |
| `db` | Manage TiDB Cloud Starter instances, branches, SQL users, connections, and SQL statements. | [`ti db` commands](/ai/ti/reference/ti-starter-database.md) |
| `fs` | Manage file system resources, AI providers, tokens, data, layers, and mounts. | [`ti fs` commands](/ai/ti/reference/ti-filesystem.md) |
| `fs-git` | Manage Git workspaces on mounted file systems. | [`ti fs-git` commands](/ai/ti/reference/ti-filesystem-git.md) |
| `fs-journal` | Manage verifiable file system journals. | [`ti fs-journal` commands](/ai/ti/reference/ti-filesystem-journal.md) |
| `fs-vault` | Manage file system Vault secrets and delegated access. | [`ti fs-vault` commands](/ai/ti/reference/ti-filesystem-vault.md) |

To list available commands in the terminal, run `ti help` or `ti <command-group> help`.

## Global options

- `--debug`: Enable redacted debug output.
- `--output <string>`: Set the output format to `json` or `text`. \[default: json]
- `--profile <string>`: Select a local profile. \[default: default]
- `--query <string>`: Apply a JMESPath expression before rendering the output.
- `--region <string>`: Override the profile's default region code for the current command, for example, `aws-us-east-1`.

Command pages document `--help`, `--version`, and all command-specific options separately.

## Output

Commands that return structured data use JSON by default:

```bash
ti db list-db-clusters --db-cluster-type starter
```

Use text output for a human-readable representation:

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

Mutating control-plane commands that support `--dry-run` validate local options, the profile, credentials, the region, and the request shape, and then report a plan without making the remote mutation.

```bash
ti db delete-db-cluster \
  --db-cluster-id "<cluster-id>" \
  --dry-run
```

Read-only commands reject `--dry-run`. The option is not a global simulation option and is available only where shown in command help.

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

Use an explicit help form to display commands and options:

```bash
ti help
ti db help
ti db create-db-cluster help
ti --help
ti --version
```

`help` is a command for navigating the command hierarchy. `--help` is available on each command; both forms intentionally coexist. The `--version` option is also available at each command level and reports the version of the same `ti` executable.

## Errors and exit behavior

Human-readable errors start with a blank line and use a stable prefix:

```text
ti [ERROR]: <message>
```

Errors are written to stderr and successful command output is written to stdout. Usage and configuration failures return a nonzero exit code before remote mutation. Runtime and remote API failures also return nonzero. An interrupted interactive configuration returns exit code `130`.

`--debug` can show redacted request and resolution context. It must not show API keys, file system tokens, DB passwords, SQL text, file contents, or connection strings.

## Related documentation

For configuration, security, compatibility, and troubleshooting details, see the following documents:

| Document | Purpose |
| --- | --- |
| [Install, Configure, and Update TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md) | Install releases, configure profiles, update, and uninstall `ti` |
| [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md) | Understand profiles, precedence rules, credentials, and local state |
| [TiDB Cloud CLI Regions, Security, and Limitations](/ai/ti/reference/ti-regions-security-and-limitations.md) | Review supported regions, credential boundaries, platform support, and limitations |
| [Migrate from `tdc` to TiDB Cloud CLI](/ai/ti/reference/ti-migrate-from-tdc.md) | Migrate local state and environment variables from `tdc` v0.1.x |
| [Troubleshoot TiDB Cloud CLI](/ai/ti/reference/ti-troubleshooting.md) | Diagnose configuration, authentication, routing, and command failures |

## Release notes

For the latest changes to TiDB Cloud CLI (`ti`), see the [TiDB Cloud CLI (`ti`) Release Notes](https://github.com/tidbcloud/ti-cli/releases).
