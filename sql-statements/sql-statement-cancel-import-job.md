---
title: CANCEL IMPORT
summary: 关于 TiDB 中 CANCEL IMPORT 的用法概述。
---

# CANCEL IMPORT

`CANCEL IMPORT` 语句用于取消在 TiDB 中创建的数据导入任务。

## 所需权限

要取消数据导入任务，你需要是导入任务的创建者或拥有 `SUPER` 权限。

## 语法

```ebnf+diagram
CancelImportJobsStmt ::=
    'CANCEL' 'IMPORT' 'JOB' JobID
```

## 示例

要取消 ID 为 `1` 的导入任务，执行以下语句：

```sql
CANCEL IMPORT JOB 1;
```

输出结果如下：

```
Query OK, 0 rows affected (0.01 sec)
```

## MySQL 兼容性

此语句是 TiDB 对 MySQL 语法的扩展。

## 相关链接

* [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)
* [`SHOW IMPORT JOB`](/sql-statements/sql-statement-show-import-job.md)