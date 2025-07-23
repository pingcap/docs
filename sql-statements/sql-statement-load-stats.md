---
title: LOAD STATS
summary: 关于 TiDB 数据库中 LOAD STATS 使用情况的概述。
---

# LOAD STATS

`LOAD STATS` 语句用于将统计信息加载到 TiDB 中。

> **Note:**
>
> 该功能在 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

## 概述

```ebnf+diagram
LoadStatsStmt ::=
    'LOAD' 'STATS' stringLit
```

## 示例

你可以访问地址 `http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}` 来下载 TiDB 实例的统计信息。

你也可以使用 `LOAD STATS ${stats_path}` 来加载特定的统计信息文件。

`${stats_path}` 可以是绝对路径或相对路径。如果使用相对路径，则从 `tidb-server` 启动的路径开始查找对应的文件。示例如下：

```sql
LOAD STATS '/tmp/stats.json';
```

```
Query OK, 0 rows affected (0.00 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 相关链接

* [Statistics](/statistics.md)
