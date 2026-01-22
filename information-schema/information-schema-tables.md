---
title: TABLES
summary: 学习 `TABLES` information_schema 表。
---

# TABLES

`TABLES` 表提供了关于数据库中表的信息：


```sql
USE information_schema;
DESC tables;
```

```sql
+---------------------------+---------------+------+------+----------+-------+
| Field                     | Type          | Null | Key  | Default  | Extra |
+---------------------------+---------------+------+------+----------+-------+
| TABLE_CATALOG             | varchar(512)  | YES  |      | NULL     |       |
| TABLE_SCHEMA              | varchar(64)   | YES  |      | NULL     |       |
| TABLE_NAME                | varchar(64)   | YES  |      | NULL     |       |
| TABLE_TYPE                | varchar(64)   | YES  |      | NULL     |       |
| ENGINE                    | varchar(64)   | YES  |      | NULL     |       |
| VERSION                   | bigint(21)    | YES  |      | NULL     |       |
| ROW_FORMAT                | varchar(10)   | YES  |      | NULL     |       |
| TABLE_ROWS                | bigint(21)    | YES  |      | NULL     |       |
| AVG_ROW_LENGTH            | bigint(21)    | YES  |      | NULL     |       |
| DATA_LENGTH               | bigint(21)    | YES  |      | NULL     |       |
| MAX_DATA_LENGTH           | bigint(21)    | YES  |      | NULL     |       |
| INDEX_LENGTH              | bigint(21)    | YES  |      | NULL     |       |
| DATA_FREE                 | bigint(21)    | YES  |      | NULL     |       |
| AUTO_INCREMENT            | bigint(21)    | YES  |      | NULL     |       |
| CREATE_TIME               | datetime      | YES  |      | NULL     |       |
| UPDATE_TIME               | datetime      | YES  |      | NULL     |       |
| CHECK_TIME                | datetime      | YES  |      | NULL     |       |
| TABLE_COLLATION           | varchar(32)   | NO   |      | utf8_bin |       |
| CHECKSUM                  | bigint(21)    | YES  |      | NULL     |       |
| CREATE_OPTIONS            | varchar(255)  | YES  |      | NULL     |       |
| TABLE_COMMENT             | varchar(2048) | YES  |      | NULL     |       |
| TIDB_TABLE_ID             | bigint(21)    | YES  |      | NULL     |       |
| TIDB_ROW_ID_SHARDING_INFO | varchar(255)  | YES  |      | NULL     |       |
| TIDB_PK_TYPE              | varchar(64)   | YES  |      | NULL     |       |
| TIDB_PLACEMENT_POLICY_NAME | varchar(64)  | YES  |      | NULL     |       |
| TIDB_TABLE_MODE           | varchar(16)   | YES  |      | NULL     |       |
| TIDB_AFFINITY             | varchar(128)  | YES  |      | NULL     |       |
+---------------------------+---------------+------+------+----------+-------+
27 rows in set (0.00 sec)
```


```sql
SELECT * FROM tables WHERE table_schema='mysql' AND table_name='user'\G
```

```sql
*************************** 1. row ***************************
            TABLE_CATALOG: def
             TABLE_SCHEMA: mysql
               TABLE_NAME: user
               TABLE_TYPE: BASE TABLE
                   ENGINE: InnoDB
                  VERSION: 10
               ROW_FORMAT: Compact
               TABLE_ROWS: 0
           AVG_ROW_LENGTH: 0
              DATA_LENGTH: 0
          MAX_DATA_LENGTH: 0
             INDEX_LENGTH: 0
                DATA_FREE: 0
           AUTO_INCREMENT: NULL
              CREATE_TIME: 2020-07-05 09:25:51
              UPDATE_TIME: NULL
               CHECK_TIME: NULL
          TABLE_COLLATION: utf8mb4_bin
                 CHECKSUM: NULL
           CREATE_OPTIONS:
            TABLE_COMMENT:
            TIDB_TABLE_ID: 5
TIDB_ROW_ID_SHARDING_INFO: NULL
             TIDB_PK_TYPE: CLUSTERED
TIDB_PLACEMENT_POLICY_NAME: NULL
           TIDB_TABLE_MODE: Normal
             TIDB_AFFINITY: NULL
1 row in set (0.00 sec)
```

下列语句等价：

```sql
SELECT table_name FROM INFORMATION_SCHEMA.TABLES
  WHERE table_schema = 'db_name'
  [AND table_name LIKE 'wild']

SHOW TABLES
  FROM db_name
  [LIKE 'wild']
```

`TABLES` 表中各列的说明如下：

* `TABLE_CATALOG`：表所属 catalog 的名称。该值始终为 `def`。
* `TABLE_SCHEMA`：表所属 schema 的名称。
* `TABLE_NAME`：表名。
* `TABLE_TYPE`：表的类型。
* `ENGINE`：存储引擎的类型。当前值为 `InnoDB`。
* `VERSION`：版本。默认值为 `10`。
* `ROW_FORMAT`：行格式。当前值为 `Compact`。
* `TABLE_ROWS`：统计信息中的表行数。
* `AVG_ROW_LENGTH`：表的平均行长度。`AVG_ROW_LENGTH` = `DATA_LENGTH` / `TABLE_ROWS`。
* `DATA_LENGTH`：数据长度。`DATA_LENGTH` = `TABLE_ROWS` × 元组中各列存储长度之和。不计入 TiKV 副本。
* `MAX_DATA_LENGTH`：最大数据长度。当前值为 `0`，表示数据长度没有上限。
* `INDEX_LENGTH`：索引长度。`INDEX_LENGTH` = `TABLE_ROWS` × 索引元组中各列长度之和。不计入 TiKV 副本。
* `DATA_FREE`：数据碎片。当前值为 `0`。
* `AUTO_INCREMENT`：自增主键当前步长。
* `CREATE_TIME`：表的创建时间。
* `UPDATE_TIME`：表的修改（如：修改行）时间。
* `CHECK_TIME`：表的检查时间。
* `TABLE_COLLATION`：表中字符串的排序规则。
* `CHECKSUM`：校验和。
* `CREATE_OPTIONS`：创建选项。
* `TABLE_COMMENT`：表的注释和说明。

表中的大部分信息与 MySQL 相同。以下列为 TiDB 新增定义：

* `TIDB_TABLE_ID`：表示表的内部 ID。该 ID 在 TiDB 集群中唯一。
* `TIDB_ROW_ID_SHARDING_INFO`：表示表的分片（动词或动名词）类型。可能的取值如下：
    - `"NOT_SHARDED"`：该表未分片（动词或动名词）。
    - `"NOT_SHARDED(PK_IS_HANDLE)"`：定义了整数型主键作为 row id 的表未分片（动词或动名词）。
    - `"PK_AUTO_RANDOM_BITS={bit_number}"`：定义了整数型主键作为 row id 且主键带有 `AUTO_RANDOM` 属性的表已分片（动词或动名词）。
    - `"SHARD_BITS={bit_number}"`：通过 `SHARD_ROW_ID_BITS={bit_number}` 进行分片（动词或动名词）的表。
    - `NULL`：系统表或视图，无法分片（动词或动名词）。
* `TIDB_PK_TYPE`：表的主键类型。可能的取值包括 `CLUSTERED`（聚簇主键）和 `NONCLUSTERED`（非聚簇主键）。
* `TIDB_PLACEMENT_POLICY_NAME`：应用于该表的 placement policy 名称。
* `TIDB_TABLE_MODE`：表的模式，例如 `Normal`、`Import` 或 `Restore`。
* `TIDB_AFFINITY`：表的 affinity 级别。非分区表为 `table`，分区表为 `partition`，未启用 affinity 时为 `NULL`。