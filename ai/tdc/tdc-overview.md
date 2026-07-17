---
title: TiDB Cloud CLI (tdc) Overview
summary: Learn how the Preview tdc command-line interface manages TiDB Cloud Starter databases and TiDB Cloud Filesystem for users, scripts, and AI agents.
---

# TiDB Cloud CLI (tdc) Overview

tdc is a command-line interface for managing TiDB Cloud Starter databases and TiDB Cloud Filesystem. It provides deterministic JSON output, explicit permissions, scriptable configuration, and commands designed for both users and AI agents.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## What you can do with tdc

With tdc, you can:

- create, inspect, update, and delete TiDB Cloud Starter clusters;
- create and manage Starter branches;
- create read-only, read-write, and admin SQL users, format connection strings, and execute SQL;
- create and select multiple TiDB Cloud Filesystem resources in one profile;
- access Filesystem data directly or mount it through FUSE or WebDAV;
- use Filesystem layers, packs, Git workspaces, append-only journals, and delegated secrets;
- use JSON output and JMESPath queries in scripts and agent workflows.

tdc has a two-level command model:

```text
tdc <service> <operation>
```

Examples include `tdc db list-db-clusters`, `tdc fs copy-file`, and `tdc fs-journal verify-journal`. The top-level `tdc configure` and `tdc update` commands configure and maintain the CLI.

## tdc and Drive9

tdc installs a bundled [Drive9](https://github.com/mem9-ai/drive9) companion named `tdc-drive9`. tdc owns profile selection, TiDB Cloud credentials, region and Filesystem selection, output formatting, and tdc error behavior. The companion owns Filesystem data-plane semantics, FUSE and WebDAV mounts, layers, pack and unpack, Git workspace acceleration, journals, and vault operations.

You do not need to install, configure, or invoke Drive9 separately for normal tdc workflows.

## Start using tdc

- [Quick Start](/ai/tdc/tdc-quick-start.md)
- [Concepts and Architecture](/ai/tdc/concepts/tdc-concepts-and-architecture.md)

### Guides

- [Install, Configure, and Update tdc](/ai/tdc/guides/tdc-install-configure-update.md)
- [Manage TiDB Cloud Organizations](/ai/tdc/guides/tdc-organization.md)
- [Manage TiDB Cloud Starter Databases](/ai/tdc/guides/tdc-starter-database.md)
- [Manage TiDB Cloud Filesystem](/ai/tdc/guides/tdc-filesystem.md)
- [Use Git Workspaces on TiDB Cloud Filesystem](/ai/tdc/guides/tdc-filesystem-git.md)
- [Use Filesystem Journals](/ai/tdc/guides/tdc-filesystem-journal.md)
- [Use Filesystem Vault](/ai/tdc/guides/tdc-filesystem-vault.md)

### Examples

- [Use a Filesystem in an Agent Sandbox](/ai/tdc/examples/tdc-agent-sandbox-example.md)
- [Run a Daily tdc Workflow](/ai/tdc/examples/tdc-daily-workflow-example.md)
- [Query SQL with Explicit Roles](/ai/tdc/examples/tdc-query-sql-with-roles-example.md)
- [Share a Filesystem Across Machines](/ai/tdc/examples/tdc-share-filesystem-across-machines-example.md)
- [Prepare a Git Workspace for Agents](/ai/tdc/examples/tdc-git-workspace-for-agents-example.md)
- [Record an Agent Workflow in a Journal](/ai/tdc/examples/tdc-journal-agent-workflow-example.md)
- [Delegate Secrets to an Agent](/ai/tdc/examples/tdc-vault-agent-secrets-example.md)

### Reference

- [tdc CLI Reference](/ai/tdc/reference/tdc-cli-reference.md)
- [tdc Configuration and Credentials](/ai/tdc/reference/tdc-configuration-and-credentials.md)
- [tdc Regions, Security, and Limitations](/ai/tdc/reference/tdc-regions-security-and-limitations.md)
- [Troubleshoot tdc](/ai/tdc/reference/tdc-troubleshooting.md)

To report a problem or suggest an improvement, create an issue in the [tdc GitHub repository](https://github.com/tidbcloud/tdc/issues).
