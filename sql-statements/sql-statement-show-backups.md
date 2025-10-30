---
title: SHOW [BACKUPS|RESTORES] | TiDB SQL Statement Reference
summary: TiDB 数据库中 SHOW [BACKUPS|RESTORES] 的用法概述。
---

# SHOW [BACKUPS|RESTORES]

这些语句会显示在 TiDB 实例上执行的所有已排队、正在运行以及最近完成的 [`BACKUP`](/sql-statements/sql-statement-backup.md) 和 [`RESTORE`](/sql-statements/sql-statement-restore.md) 任务的列表。

这两个语句都需要 `SUPER` 权限才能执行。

使用 `SHOW BACKUPS` 查询 `BACKUP` 任务，使用 `SHOW RESTORES` 查询 `RESTORE` 任务。

> **Note:**
>
> 该功能在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。

通过 `br` 命令行工具启动的备份和恢复任务不会显示在这里。

## 语法

```ebnf+diagram
ShowBRIEStmt ::=
    "SHOW" ("BACKUPS" | "RESTORES") ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 示例

在一个连接中，执行以下语句：

```sql
BACKUP DATABASE `test` TO 's3://example-bucket/backup-01';
```

在备份完成之前，在新的连接中运行 `SHOW BACKUPS`：

```sql
SHOW BACKUPS;
```

```sql
+--------------------------------+---------+----------+---------------------+---------------------+-------------+------------+---------+
| Destination                    | State   | Progress | Queue_time          | Execution_time      | Finish_time | Connection | Message |
+--------------------------------+---------+----------+---------------------+---------------------+-------------+------------+---------+
| s3://example-bucket/backup-01/ | Backup  | 98.38    | 2020-04-12 23:09:03 | 2020-04-12 23:09:25 |        NULL |          4 | NULL    |
+--------------------------------+---------+----------+---------------------+---------------------+-------------+------------+---------+
1 row in set (0.00 sec)
```

上面结果的第一行描述如下：

| 列名 | 描述 |
| :-------- | :--------- |
| `Destination` | 目标 URL（已去除所有参数以避免泄露密钥） |
| `State` | 任务的状态 |
| `Progress` | 当前状态下的预计进度百分比 |
| `Queue_time` | 任务被排队的时间 |
| `Execution_time` | 任务开始执行的时间；对于排队中的任务，该值为 `0000-00-00 00:00:00` |
| `Finish_time` | 任务完成时的时间戳；对于排队和运行中的任务，该值为 `0000-00-00 00:00:00` |
| `Connection` | 执行该任务的连接 ID |
| `Message` | 详细信息 |

可能的状态有：

| State | 描述 |
| :-----|:------------|
| Backup | 正在进行备份 |
| Wait | 等待执行 |
| Checksum | 正在执行校验和操作 |

可以使用连接 ID 通过 [`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md) 语句取消备份/恢复任务。

```sql
KILL TIDB QUERY 4;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

### 过滤

使用 `LIKE` 子句，通过通配符表达式匹配目标 URL 来过滤任务。

```sql
SHOW BACKUPS LIKE 's3://%';
```

使用 `WHERE` 子句按列进行过滤。

```sql
SHOW BACKUPS WHERE `Progress` < 25.0;
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 参见

* [BACKUP](/sql-statements/sql-statement-backup.md)
* [RESTORE](/sql-statements/sql-statement-restore.md)