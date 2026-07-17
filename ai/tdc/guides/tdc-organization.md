---
title: Manage TiDB Cloud Organizations with tdc
summary: List accessible TiDB Cloud projects and understand regular and virtual project types used by tdc.
---

# Manage TiDB Cloud Organizations with tdc

Use `tdc organization` to inspect the projects accessible to the configured TiDB Cloud API key.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Prerequisites

Run `tdc configure` with a TiDB Cloud API key that can list organization projects.

## List projects

```bash
tdc organization list-projects
```

The JSON response includes project IDs, names, and `type` values:

- `tidbx` identifies a regular project;
- `tidbx_virtual` identifies a virtual project used as the default Starter project.

Request a page size or continue with a returned page token:

```bash
tdc organization list-projects --page-size 50
tdc organization list-projects --page-size 50 --page-token "<next-page-token>"
```

Render a terminal-oriented table or select fields:

```bash
tdc organization list-projects --output text
tdc organization list-projects --query 'projects[].{id:id,name:name,type:type}'
```

## Default virtual project

`tdc configure` calls the same project-listing API. Configuration succeeds only when it finds exactly one accessible `tidbx_virtual` project, and saves its ID in the selected profile:

```toml
[default]
region_code = "aws-us-east-1"
project_id = "..."
```

`tdc db create-db-cluster` uses this project when `--project-id` is omitted. Pass an explicit project ID to override it for one cluster:

```bash
tdc db create-db-cluster \
  --db-cluster-name project-specific-cluster \
  --db-cluster-type starter \
  --project-id "<project-id>"
```

## What's next

- [Manage TiDB Cloud Starter Databases](/ai/tdc/guides/tdc-starter-database.md)
- [tdc Configuration and Credentials](/ai/tdc/reference/tdc-configuration-and-credentials.md)
