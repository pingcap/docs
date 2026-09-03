---
title: 使用 Plan Replayer 排查 SQL 性能问题
summary: 了解如何从你的实例生成用于排查 SQL 性能问题的 Plan Replayer 文件，以及如何在有限时间内授予 TiDB Cloud Support 对该文件的访问权限。
---

# 使用 Plan Replayer 排查 SQL 性能问题

Plan Replayer 可帮助你将排查 SQL 执行计划所需的信息打包到一个文件中。该文件可以包含 TiDB 版本和配置、会话变量、SQL bindings、表结构、表统计信息、`EXPLAIN` 或 `EXPLAIN ANALYZE` 的输出，以及优化器内部信息。

在排查 TiDB Cloud Essential 或 Premium 实例上的 SQL 性能问题时，你可以使用 `PLAN REPLAYER DUMP` 为特定 SQL 语句生成一个 Plan Replayer 文件，并通过返回的 URL 下载该文件。Plan Replayer 文件适用于排查诸如意外的执行计划、计划回退、统计信息不准确，或仅偶发出现的问题计划等问题。

如果你需要 TiDB Cloud Support 协助排查 SQL 性能问题，可以在有限时间内临时授予 TiDB Cloud Support 访问 Plan Replayer 文件的权限。

> **Note:**
>
> Plan Replayer 文件不包含实际的表行数据，但可能包含 SQL 文本、表定义、优化器统计信息以及其他潜在的敏感信息。在授予 Support 访问权限之前，请先检查文件内容，并确认符合你所在组织的数据共享要求。

## 开始之前 {#before-you-start}

- 使用 SQL 客户端连接到目标 TiDB Cloud Essential 或 Premium 实例。
- 使用有权限执行所需 SQL 语句的账户。
- 确定你要排查的 SQL 语句、SQL digest 或 plan digest。
- 尽可能移除或掩码 SQL 文本中的敏感字面量。Plan Replayer 不包含表行数据，但 SQL 文本和 schema 名称仍可能包含敏感信息。

## 生成 Plan Replayer 文件 {#generate-a-plan-replayer-file}

本节介绍如何为特定 SQL 语句生成 Plan Replayer 文件。

### 为语句生成文件 {#generate-a-file-for-a-statement}

对你要排查的语句运行 `PLAN REPLAYER DUMP`。使用 `EXPLAIN` 捕获优化器估算的执行计划。

```sql
PLAN REPLAYER DUMP EXPLAIN
SELECT * FROM orders WHERE customer_id = 1001;
```

该语句会在 `File_token` 列中返回一个下载 URL。该 URL 是临时的。请妥善保存，并在其过期前下载 Plan Replayer ZIP 文件。

### 包含运行时信息 {#include-runtime-information}

当性能问题涉及实际执行行为时，使用 `EXPLAIN ANALYZE`，以便除执行计划外还包含运行时执行信息。

```sql
PLAN REPLAYER DUMP EXPLAIN ANALYZE
SELECT * FROM orders WHERE customer_id = 1001;
```

### 使用历史统计信息 {#use-historical-statistics}

如果已启用历史统计信息，并且性能问题发生在某个特定时间，可以使用 `WITH STATS AS OF TIMESTAMP` 请求该时间点可用的统计信息。TiDB 会使用指定时间戳之前最近可用的历史统计信息。

```sql
PLAN REPLAYER DUMP WITH STATS AS OF TIMESTAMP
'2026-08-31 12:00:00'
EXPLAIN SELECT * FROM orders WHERE customer_id = 1001;
```

如果排查需要，你也可以提供 Unix 时间戳。如果在指定时间之前没有可用的历史统计信息，TiDB 会使用最新可用的统计信息，并在生成的包中记录相关错误信息。

## 管理 TiDB Cloud Support 的访问权限 {#manage-access-from-tidb-cloud-support}

Support 访问权限在实例级别进行控制。该授权允许 TiDB Cloud Support 工程师在有限时间内访问已生成的 Plan Replayer 文件，以排查 SQL 性能问题。

### 授予 TiDB Cloud Support 权限 {#authorize-tidb-cloud-support}

如需授予 TiDB Cloud Support 临时访问为排查 SQL 性能问题而生成的 Plan Replayer 文件的权限，请执行以下步骤：

1. 在 [TiDB Cloud console](https://tidbcloud.com/) 中，进入目标 TiDB Cloud Essential 或 Premium 实例的概览页面。
2. 在左侧导航栏中，点击 **Settings** > **Security**。
3. 在 **Security** 页面中，找到 **SQL Plan Replayer Files Access Authorization** 区域并点击 **Authorize**。
4. 从下拉列表中选择一个覆盖预期排查时间窗口的访问时长。
5. 查看授权声明，并勾选确认复选框。
6. 点击 **Authorize** 以授予临时访问权限。

访问权限会立即生效，并在达到所选过期时间后自动被回收。

### 延长授权时间 {#extend-the-authorization-period}

如果授权时间即将过期，而问题仍在排查中，请前往目标 TiDB Cloud Essential 或 Premium 实例的 **Security** 页面，然后点击 **Extend Access** 以修改过期时间。

在你确认修改后，新的过期时间将生效。

### 回收访问权限 {#revoke-access}

当排查完成后，或者你不再希望 TiDB Cloud Support 访问 Plan Replayer 文件时，请前往目标 TiDB Cloud Essential 或 Premium 实例的 **Security** 页面，然后点击 **Revoke Access** 并确认该操作。

权限回收会立即生效。与诊断访问流程相关的文件也可能会根据产品的保留策略被删除。

## 最佳实践 {#best-practices}

为帮助保护敏感信息、尽量减少不必要的访问并提升支持效率，请遵循以下最佳实践：

- 尽量在接近排查时间点时生成 Plan Replayer 文件。
- 以实际可行为前提，授予 TiDB Cloud Support 尽可能短的访问时间。
- 在相关支持工单中包含 Plan Replayer 文件标识符。
- 问题解决后及时回收访问权限。

## 安全性与保留时间 {#security-and-retention}

Plan Replayer 旨在共享优化器和执行计划上下文，而无需导出实际表行数据。不过，SQL 文本、对象名称、表定义、配置、bindings 和统计信息都可能包含业务敏感信息。如果你需要与 TiDB Cloud Support 共享 Plan Replayer 文件，请使用最短必要的访问时长，并在排查完成后回收访问权限。

Plan Replayer 文件是临时的诊断产物。TiDB 可能会在其保留时间结束后自动删除已生成的文件。如果之前的文件已过期或不再可用，请重新生成一个新文件。

## 相关文档 {#related-documentation}

[使用 PLAN REPLAYER 保存和恢复集群现场信息](https://docs.pingcap.com/zh/tidb/stable/sql-plan-replayer/)