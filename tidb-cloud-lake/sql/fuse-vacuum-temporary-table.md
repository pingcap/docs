---
title: FUSE_VACUUM_TEMPORARY_TABLE
summary: 临时表通常会在会话结束时自动清理（详见 CREATE TEMP TABLE）。但是，由于查询节点崩溃或会话异常终止等事件，此过程可能失败，从而留下孤立的临时文件。
---

# FUSE_VACUUM_TEMPORARY_TABLE

## 概述 {#overview}

临时表通常会在会话结束时自动清理（详见 [CREATE TEMP TABLE](/tidb-cloud-lake/sql/create-temp-table.md)）。但是，由于查询节点崩溃或会话异常终止等事件，此过程可能失败，从而留下孤立的临时文件。

`FUSE_VACUUM_TEMPORARY_TABLE()` 用于手动删除这些遗留文件，以回收存储空间。

**何时使用此函数：**

- 在已知系统故障或会话异常终止之后。
- 当你怀疑孤立的临时数据正在占用存储空间时。
- 在容易出现此类问题的环境中，作为周期性维护任务使用。

## 操作安全性 {#operational-safety}

`FUSE_VACUUM_TEMPORARY_TABLE()` 函数被设计为一种安全且可靠的操作。

- **仅针对临时数据：** 它只会识别并删除属于临时表的孤立数据文件和元信息文件。
- **不会影响普通表：** 该函数不会影响任何常规的持久化表及其数据。其作用域严格限定为清理未被引用的临时表残留内容。

## 语法 {#syntax}

```sql
FUSE_VACUUM_TEMPORARY_TABLE();
```

## 示例 {#examples}

```sql
SELECT * FROM FUSE_VACUUM_TEMPORARY_TABLE();

┌────────┐
│ result │
├────────┤
│ Ok     │
└────────┘
```