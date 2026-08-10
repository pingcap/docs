---
title: TiDB Cloud Organization CLI Command Reference
summary: Reference the `ti organization` command tree, project listing inputs, output, and examples.
---

# TiDB Cloud Organization CLI Command Reference

Use `ti organization` to inspect the projects accessible to the configured TiDB Cloud API key.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Command tree

```text
ti organization
└── list-projects
```

`list-projects` requires a configured TiDB Cloud API key. It accepts `--page-size` and `--page-token` for pagination, plus the global output and query flags.

## Prerequisites

Run `ti configure` with a TiDB Cloud API key that can list organization projects.

## List projects

```bash
ti organization list-projects
```

The JSON response includes project IDs, names, and `type` values:

- `tidbx` identifies a regular project;
- `tidbx_virtual` identifies a virtual project used as the default Starter project.

Request a page size or continue with a returned page token:

```bash
ti organization list-projects --page-size 50
ti organization list-projects --page-size 50 --page-token "<next-page-token>"
```

Render a terminal-oriented table or select fields:

```bash
ti organization list-projects --output text
ti organization list-projects --query 'projects[].{id:id,name:name,type:type}'
```

## Default virtual project

`ti configure` calls the same project-listing API. Configuration succeeds only when it finds exactly one accessible `tidbx_virtual` project, and saves its ID in the selected profile:

```toml
[default]
region_code = "aws-us-east-1"
project_id = "..."
```

`ti db create-db-cluster` uses this project when `--project-id` is omitted. If the saved ID is removed, cluster creation omits the project label and TiDB Cloud selects the account's default project. Pass an explicit project ID to override either default for one cluster:

```bash
ti db create-db-cluster \
  --db-cluster-type starter \
  --db-cluster-name project-specific-cluster \
  --project-id "<project-id>"
```

## What's next

- [TiDB Cloud Starter CLI Command Reference](/ai/ti/reference/ti-starter-database.md)
- [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md)
