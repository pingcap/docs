---
title: LOAD STATS
summary: TiDB 数据库中 LOAD STATS 的用法概述。
---

# LOAD STATS

`LOAD STATS` 语句用于将统计信息加载到 TiDB 中。

> **Note:**
>
> 该功能在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。

## 语法

```ebnf+diagram
LoadStatsStmt ::=
    'LOAD' 'STATS' stringLit
```

## 示例

你可以访问地址 `http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}` 下载 TiDB 实例的统计信息。

你也可以使用 `LOAD STATS ${stats_path}` 加载指定的统计信息文件。

`${stats_path}` 可以是绝对路径，也可以是相对路径。如果你使用相对路径，则会从 `tidb-server` 启动时所在的路径查找对应的文件。以下是一个示例：

```sql
LOAD STATS '/tmp/stats.json';
```

```
Query OK, 0 rows affected (0.00 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 参见

* [Statistics](/statistics.md)