---
title: CREATE TRANSIENT TABLE
summary: 创建一个不为 Time Travel 存储历史数据的表。
---

# CREATE TRANSIENT TABLE

创建一个不为 Time Travel 存储历史数据的表。

Transient table 用于保存临时性数据，这类数据不需要数据保护或恢复机制。Dataebend 不会为 transient table 保存历史数据，因此你无法使用 Time Travel 功能查询 transient table 的先前版本。例如，SELECT 语句中的 [AT](/tidb-cloud-lake/sql/at.md) 子句不适用于 transient table。请注意，你仍然可以 [删除](/tidb-cloud-lake/sql/drop-table.md) 和 [恢复删除](/tidb-cloud-lake/sql/undrop-table.md) transient table。

> **Note:**
>
> 对 transient table 的并发修改（包括写操作）可能会导致数据损坏，使数据无法读取。该缺陷正在修复中。在问题修复之前，请避免对 transient table 进行并发修改。

## 语法 {#syntax}

```sql
CREATE [ OR REPLACE ] TRANSIENT TABLE
       [ IF NOT EXISTS ]
       [ <database_name>. ]<table_name>
       ...
```

省略的部分遵循 [CREATE TABLE](/tidb-cloud-lake/sql/create-table.md) 的语法。

## 示例 {#examples}

以下示例创建了一个名为 `visits` 的 transient table：

```sql
CREATE TRANSIENT TABLE visits (
  visitor_id BIGINT
);
```