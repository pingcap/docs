---
title: OpenAPI Lightweight Migration Guide for Starter and Essential
summary: Learn the minimum changes required to keep your existing v1beta API calls working after TiDB Cloud introduces separate project types for TiDB X instances.
---

# OpenAPI Migration Guide for Starter and Essential

This guide is for API callers that want to keep most existing `v1beta` calls working and only patch project lookup and cluster creation for Starter and Essential instances.

There are two changes to be aware of:

- `project_id` values for Starter and Essential instances **can change** because these instances can be moved between projects. Do not hardcode `project_id` values.
- Project responses now include a `type` field. See [Project type values](#project-type-values) for the possible values.

## Project API changes

### GET /api/v1beta/projects

`GET /api/v1beta/projects` now returns a `type` field for each project.

#### Project type values

| Value | Description |
|---|---|
| `dedicated` | A project that contains only TiDB Dedicated clusters. |
| `tidbx` | A project that contains only TiDB X instances (Starter, Essential, and Premium). |
| `tidbx_virtual` | The organization-level default project for TiDB X instances not assigned to any project. There is only one per organization. |

> **Note:**
>
> Starter and Essential instances both use the `tidbx` project type.

**If you only read `id` and `name` from project responses**, you likely do not need to make any changes.

**If you need to distinguish between project types** (for example, to filter for dedicated projects, TiDB X projects, or the default project), start reading the `type` field.

### POST /api/v1beta/projects

If you create projects using `POST /api/v1beta/projects`, note the following:

- Only `dedicated` and `tidbx` are valid values for `type` at creation time.
- If `type` is omitted, the API creates a `dedicated` project by default.

## How to get a project ID for an existing instance

If you already have a Starter or Essential instance and only need the current `project_id`, use the following approach instead of hardcoding a value.

**Step 1.** Call the cluster detail endpoint:

```http
GET https://serverless.tidbapi.com/v1beta1/clusters/{clusterId}
```

**Step 2.** Read `labels["tidb.cloud/project"]` from the response:

```json
{
  "clusterId": "1048576",
  "labels": {
    "tidb.cloud/project": "2293484"
  }
}
```

**Step 3.** Use the retrieved `project_id` with existing `v1beta` endpoints. For example:

- `GET /api/v1beta/projects/{project_id}/clusters/{cluster_id}`
- `DELETE /api/v1beta/projects/{project_id}/clusters/{cluster_id}`
- `GET /api/v1beta/projects/{project_id}/clusters/{cluster_id}/imports`
- `POST /api/v1beta/projects/{project_id}/clusters/{cluster_id}/imports`

> **Note:**
>
> This approach does not cover cluster creation using `POST /api/v1beta/projects/{project_id}/clusters`. Note that `v1beta` only supports creating Starter instances and Dedicated clusters. If you need to create an Essential instance, use the `v1beta1` API instead. For more information, see [TiDB Cloud API documentation](https://docs.pingcap.com/api/). For creating new Starter or Essential instances, see your cluster creation workflow to ensure you are targeting a `tidbx` project.

## Summary of required changes

| Scenario | Action required |
|---|---|
| You read `id` and `name` from project responses only | No changes needed. |
| You hardcode `project_id` for Starter or Essential instances | Replace hardcoded values with dynamic lookup via `labels["tidb.cloud/project"]`. |
| You create projects and need to target TiDB X instances | Pass `"type": "tidbx"` in the request body of `POST /api/v1beta/projects`. |
| You filter projects by type | Start reading the `type` field from `GET /api/v1beta/projects` responses. |
