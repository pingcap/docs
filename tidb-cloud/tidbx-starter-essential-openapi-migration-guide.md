---
title: TiDB Cloud API Migration Guide for {{{ .starter }}} and Essential
summary: Learn the minimum changes needed to keep your existing v1beta API calls working after TiDB Cloud introduces separate project types for TiDB X instances.
---

# TiDB Cloud API Migration Guide for {{{ .starter }}} and Essential

Starting from April 15, 2026, TiDB Cloud introduces separate project types for different resource types. For {{{ .starter }}} and Essential instances, you can now manage them either in TiDB X projects or at the organization level. For more information, see [Project Migration FAQ for TiDB X Instances](/tidb-cloud/tidbx-instance-move-faq.md).

This guide is intended for API callers who want to keep most existing `v1beta` calls working and make only the minimum changes to project lookup and cluster creation for {{{ .starter }}} and Essential instances.

Because of these project model changes, note the following API changes:

- `project_id` values for {{{ .starter }}} and Essential instances **can change** because these instances can be moved between projects. Do not hardcode `project_id` values.
- Project responses now include a `type` field. For possible values, see [Project type values](#project-type-values).

## Project API changes

### GET /api/v1beta/projects

`GET /api/v1beta/projects` now returns a `type` field for each project.

#### Project type values

| Value | Description |
|---|---|
| `dedicated` | A project that contains only TiDB Dedicated clusters. |
| `tidbx` | A project that contains only TiDB X instances (such as {{{ .starter }}} and Essential). |
| `tidbx_virtual` | The default organization-level project for TiDB X instances that are not assigned to any project. For each organization, there is only a single `tidbx_virtual` project. |

> **Note:**
>
> {{{ .starter }}} and Essential instances both use the `tidbx` project type.

**If you only read `id` and `name` from project responses**, you likely do not need to make any changes.

**If you need to distinguish between project types** (for example, to filter dedicated projects, TiDB X projects, or the TiDB X virtual project), start reading the `type` field.

### POST /api/v1beta/projects

If you create projects using `POST /api/v1beta/projects`, note the following:

- Only `dedicated` and `tidbx` are valid `type` values when creating a project.
- If `type` is omitted, the API creates a `dedicated` project by default.

## How to get a project ID for an existing instance

If you already have a {{{ .starter }}} or Essential instance and only need its current `project_id`, use the following approach instead of hardcoding the value.

1. Call the cluster details endpoint:

    ```http
    GET https://serverless.tidbapi.com/v1beta1/clusters/{clusterId}
    ```

2. Read `labels["tidb.cloud/project"]` from the response:

    ```json
    {
      "clusterId": "1048576",
      "labels": {
        "tidb.cloud/project": "2293484"
      }
    }
    ```

3. Use the retrieved `project_id` with your existing `v1beta` endpoints. For example:

    - `GET /api/v1beta/projects/{project_id}/clusters/{cluster_id}`
    - `DELETE /api/v1beta/projects/{project_id}/clusters/{cluster_id}`
    - `GET /api/v1beta/projects/{project_id}/clusters/{cluster_id}/imports`
    - `POST /api/v1beta/projects/{project_id}/clusters/{cluster_id}/imports`

> **Note:**
>
> This approach does not apply to cluster creation using `POST /api/v1beta/projects/{project_id}/clusters`. Note that `v1beta` supports creating only {{{ .starter }}} instances and Dedicated clusters. To create a {{{ .essential }}} instance, use the `v1beta1` API instead. For more information, see [TiDB Cloud API documentation](https://docs.pingcap.com/api/). When creating new {{{ .starter }}} or Essential instances, check your cluster creation workflow to ensure that it targets a `tidbx` project.

## Summary of required changes

| Scenario | Action required |
|---|---|
| You read only `id` and `name` from project responses | No changes needed. |
| You hardcode `project_id` for {{{ .starter }}} or Essential instances | Replace hardcoded values with a dynamic lookup using `labels["tidb.cloud/project"]`. |
| You create projects and need to target TiDB X instances | Pass `"type": "tidbx"` in the request body of `POST /api/v1beta/projects`. |
| You filter projects by type | Start reading the `type` field from `GET /api/v1beta/projects` responses. |