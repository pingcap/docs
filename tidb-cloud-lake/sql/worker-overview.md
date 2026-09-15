---
title: Worker
summary: 启用 cloud control 的部署中与 Worker 相关的 SQL 命令。
---

# Worker

启用 cloud control 的部署中与 Worker 相关的 SQL 命令。

> **Note:**
>
> Worker 管理命令需要 cloud control。如果未配置 `cloud_control_grpc_server_address`，则在运行这些命令时，{{{ .lake }}} 会返回 `CloudControlNotEnabled` 错误。

## 支持的语句 {#supported-statements}

| 语句 | 用途 |
|-----------|---------|
| `CREATE WORKER` | 创建一个 worker，并可选择指定键值选项列表 |
| `ALTER WORKER` | 修改 worker 的标签或选项，或更改 worker 状态 |
| `DROP WORKER` | 删除一个 worker |
| `SHOW WORKERS` | 列出当前租户中的 workers |

## 命令参考 {#command-reference}

| 命令 | 说明 |
|---------|-------------|
| [CREATE WORKER](/tidb-cloud-lake/sql/create-worker.md) | 创建 worker 定义 |
| [ALTER WORKER](/tidb-cloud-lake/sql/alter-worker.md) | 修改 worker 的标签、选项或状态 |
| [DROP WORKER](/tidb-cloud-lake/sql/drop-worker.md) | 移除 worker 定义 |
| [SHOW WORKERS](/tidb-cloud-lake/sql/show-workers.md) | 列出 workers 及其元信息 |
| [示例](/tidb-cloud-lake/sql/worker-examples.md) | 展示已验证的 worker SQL 示例 |

## 注意事项 {#notes}

- 选项名称不区分大小写。{{{ .lake }}} 会在规划期间将其规范化为小写。
- `SHOW WORKERS` 返回 `name`、`tags`、`options`、`created_at` 和 `updated_at` 列。
- `ALTER WORKER` 支持 `SET TAG`、`UNSET TAG`、`SET`、`UNSET`、`SUSPEND` 和 `RESUME`。
- `CREATE WORKER` 不支持 `TAG` 子句。