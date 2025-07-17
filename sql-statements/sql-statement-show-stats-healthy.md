---
title: SHOW STATS_HEALTHY
summary: 关于 TiDB 数据库中 SHOW STATS_HEALTHY 的使用概述。
---

# SHOW STATS_HEALTHY

`SHOW STATS_HEALTHY` 语句显示统计信息的估算准确程度。健康百分比较低的表可能会生成次优的查询执行计划。

可以通过运行 [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md) 语句来改善表的健康状况。当健康度低于 [`tidb_auto_analyze_ratio`](/system-variables.md#tidb_auto_analyze_ratio) 阈值时，`ANALYZE` 会自动运行。

目前，`SHOW STATS_HEALTHY` 语句返回以下列：

| 列名 | 描述 |
| -------- | ------------- |
| `Db_name` | 数据库名称 |
| `Table_name` | 表名称 |
| `Partition_name` | 分区名称 |
| `Healthy` | 健康百分比（0 到 100 之间） |

## 概要

```ebnf+diagram
ShowStatsHealthyStmt ::=
    "SHOW" "STATS_HEALTHY" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 示例

加载示例数据并运行 `ANALYZE`：

```sql
CREATE TABLE t1 (
 id INT NOT NULL PRIMARY KEY auto_increment,
 b INT NOT NULL,
 pad VARBINARY(255),
 INDEX(b)
);

INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM dual;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
SELECT SLEEP(1);
ANALYZE TABLE t1;
SHOW STATS_HEALTHY; # 应该显示 100% 健康
```

```sql
...
mysql> SHOW STATS_HEALTHY;
+---------+------------+----------------+---------+
| Db_name | Table_name | Partition_name | Healthy |
+---------+------------+----------------+---------+
| test    | t1         |                |     100 |
+---------+------------+----------------+---------+
1 行结果（0.00 秒）
```

进行一次批量删除，删除大约 30% 的记录。检查统计信息的健康状况：

```sql
DELETE FROM t1 WHERE id BETWEEN 101010 AND 201010; # 删除大约 30% 的记录
SHOW STATS_HEALTHY; 
```

```sql
mysql> SHOW STATS_HEALTHY;
+---------+------------+----------------+---------+
| Db_name | Table_name | Partition_name | Healthy |
+---------+------------+----------------+---------+
| test    | t1         |                |      50 |
+---------+------------+----------------+---------+
1 行结果（0.00 秒）
```

## MySQL 兼容性

此语句为 TiDB 对 MySQL 语法的扩展。

## 相关链接

* [ANALYZE](/sql-statements/sql-statement-analyze-table.md)
* [统计信息简介](/statistics.md)