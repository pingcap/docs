---
title: {{{ .starter }}} 和 Essential 的项目 API 迁移指南
summary: 了解在 TiDB Cloud 为 TiDB X 实例引入独立项目类型后，为保持现有 v1beta API 调用正常工作所需的最少变更。
---

# {{{ .starter }}} 和 Essential 的项目 API 迁移指南

从 2026 年 4 月 15 日起，TiDB Cloud 为不同资源类型引入独立的项目类型。对于 {{{ .starter }}} 和 Essential 实例，你现在既可以在 TiDB X 项目中管理它们，也可以在组织级别管理它们。更多信息，请参见[TiDB X 实例的项目迁移常见问题](/tidb-cloud/tidbx-instance-move-faq.md)。

本指南面向希望让大多数现有 `v1beta` 调用继续工作，并且仅对 {{{ .starter }}} 和 Essential 实例的项目查找与集群创建进行最少改动的 API 调用方。

由于这些项目模型变更，请注意以下 API 变化：

- {{{ .starter }}} 和 Essential 实例的 `project_id` 值**可能会变化**，因为这些实例可以在 TiDB Cloud 控制台中在项目之间移动。请勿将 `project_id` 值硬编码。
- 项目响应现在包含一个 `type` 字段。有关可能的取值，请参见[项目类型取值](#project-type-values)。

## 项目 API 变更 {#project-api-changes}

### GET /api/v1beta/projects {#get-api-v1beta-projects}

`GET /api/v1beta/projects` 现在会为每个项目返回一个 `type` 字段。

#### 项目类型取值 {#project-type-values}

| Value | Description |
|---|---|
| `dedicated` | 仅包含 TiDB Cloud Dedicated 集群的项目。 |
| `tidbx` | 仅包含 TiDB X 实例（例如 {{{ .starter }}} 和 Essential）的项目。 |
| `tidbx_virtual` | 未分配到任何项目的 TiDB X 实例的默认组织级项目。每个组织只有一个 `tidbx_virtual` 项目。 |

> **Note:**
>
> {{{ .starter }}} 和 Essential 实例都使用 `tidbx` 项目类型。

**如果你的应用程序只从项目响应中读取 `id` 和 `name` 字段**，则无需进行任何更改。

**如果你的应用程序需要区分项目类型**（例如，筛选 dedicated 项目、TiDB X 项目或 TiDB X 虚拟项目），请开始读取 `type` 字段。

### POST /api/v1beta/projects {#post-api-v1beta-projects}

如果你使用 `POST /api/v1beta/projects` 创建项目，请注意以下事项：

- 创建项目时，只有 `dedicated` 和 `tidbx` 是有效的 `type` 取值。
- 如果省略 `type`，API 默认会创建一个 `dedicated` 项目。

## 如何获取现有实例的项目 ID {#how-to-get-a-project-id-for-an-existing-instance}

如果你已经有一个 {{{ .starter }}} 或 Essential 实例，并且只需要它当前的 `project_id`，请使用以下方法，而不是将该值硬编码。

1. 调用集群详情端点：

    ```http
    GET https://serverless.tidbapi.com/v1beta1/clusters/{clusterId}
    ```

2. 从响应中读取 `labels["tidb.cloud/project"]`：

    ```json
    {
      "clusterId": "1048576",
      "labels": {
        "tidb.cloud/project": "2293484"
      }
    }
    ```

3. 将获取到的 `project_id` 与现有的 `v1beta` 端点一起使用。例如：

    - `GET /api/v1beta/projects/{project_id}/clusters/{cluster_id}`
    - `DELETE /api/v1beta/projects/{project_id}/clusters/{cluster_id}`
    - `GET /api/v1beta/projects/{project_id}/clusters/{cluster_id}/imports`
    - `POST /api/v1beta/projects/{project_id}/clusters/{cluster_id}/imports`

> **Note:**
>
> - 此方法不适用于使用 `POST /api/v1beta/projects/{project_id}/clusters` 创建集群的场景。
> - `v1beta` 仅支持创建 {{{ .starter }}} 实例和 TiDB Cloud Dedicated 集群。要创建 {{{ .essential }}} 实例，请改用 `v1beta1` API。更多信息，请参见 [TiDB Cloud API documentation](https://docs.pingcap.com/api/)。
> - 创建新的 {{{ .starter }}} 或 Essential 实例时，请检查你的集群创建工作流，以确保其目标是 `tidbx` 项目。

## 所需变更摘要 {#summary-of-required-changes}

| Scenario | Action required |
|---|---|
| You read only `id` and `name` from project responses | 无需更改。 |
| You hardcode `project_id` for {{{ .starter }}} or Essential instances | 使用 `labels["tidb.cloud/project"]` 的动态查找替换硬编码值。 |
| You create projects and need to target TiDB X instances | 在 `POST /api/v1beta/projects` 的请求体中传入 `"type": "tidbx"`。 |
| You filter projects by type | 开始从 `GET /api/v1beta/projects` 响应中读取 `type` 字段。 |

请提供保持所有格式和结构不变的翻译内容。