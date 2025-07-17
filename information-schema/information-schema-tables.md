---
title: TABLES
summary: 了解 `TABLES` information_schema 表。
---

# TABLES

`TABLES` 表提供关于数据库中表的信息：


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
| TABLE_COLLATION           | varchar(32)   | NO   |      | utf8mb4_bin |   |
| CHECKSUM                  | bigint(21)    | YES  |      | NULL     |       |
| CREATE_OPTIONS            | varchar(255)  | YES  |      | NULL     |       |
| TABLE_COMMENT             | varchar(2048) | YES  |      | NULL     |       |
| TIDB_TABLE_ID             | bigint(21)    | YES  |      | NULL     |       |
| TIDB_ROW_ID_SHARDING_INFO | varchar(255)  | YES  |      | NULL     |       |
+---------------------------+---------------+------+------+----------+-------+
23 rows in set (0.00 sec)
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
1 row in set (0.00 sec)
```

以下语句等价：

```sql
SELECT table_name FROM INFORMATION_SCHEMA.TABLES
  WHERE table_schema = 'db_name'
  [AND table_name LIKE 'wild']

SHOW TABLES
  FROM db_name
  [LIKE 'wild']
```

`TABLES` 表中列的描述如下：

* `TABLE_CATALOG`：表所属的目录名称。值始终为 `def`。
* `TABLE_SCHEMA`：表所属的模式（schema）名称。
* `TABLE_NAME`：表的名称。
* `TABLE_TYPE`：表的类型。
* `ENGINE`：存储引擎类型。当前值为 `InnoDB`。
* `VERSION`：版本。默认值为 `10`。
* `ROW_FORMAT`：行格式。当前值为 `Compact`。
* `TABLE_ROWS`：统计的表中的行数。
* `AVG_ROW_LENGTH`：表的平均行长度。`AVG_ROW_LENGTH` = `DATA_LENGTH` / `TABLE_ROWS`。
* `DATA_LENGTH`：数据长度。`DATA_LENGTH` = `TABLE_ROWS` \* 该行中所有列存储长度的总和。未考虑 TiKV 的副本。
* `MAX_DATA_LENGTH`：最大数据长度。当前值为 `0`，表示数据长度没有上限。
* `INDEX_LENGTH`：索引长度。`INDEX_LENGTH` = `TABLE_ROWS` \* 索引中所有列长度的总和。未考虑 TiKV 的副本。
* `DATA_FREE`：数据碎片。当前值为 `0`。
* `AUTO_INCREMENT`：当前自增主键的步长。
* `CREATE_TIME`：表的创建时间。
* `UPDATE_TIME`：表的更新时间。
* `CHECK_TIME`：表的检查时间。
* `TABLE_COLLATION`：表中字符串的字符集排序规则。
* `CHECKSUM`：校验和。
* `CREATE_OPTIONS`：创建选项。
* `TABLE_COMMENT`：表的备注和说明。

大部分信息与 MySQL 相同，只有两个列是由 TiDB 新定义的：

* `TIDB_TABLE_ID`：表示表的内部 ID。该 ID 在 TiDB 集群中是唯一的。
* `TIDB_ROW_ID_SHARDING_INFO`：表示表的分片类型。可能的值如下：
    - `"NOT_SHARDED"`：表未分片。
    - `"NOT_SHARDED(PK_IS_HANDLE)"`：定义了整数主键作为行 ID 的表未分片。
    - `"PK_AUTO_RANDOM_BITS={bit_number}"`：定义了整数主键作为行 ID 的表，由于主键被赋予 `AUTO_RANDOM` 属性而进行分片。
    - `"SHARD_BITS={bit_number}"`：使用 `SHARD_ROW_ID_BITS={bit_number}` 进行分片的表。
    - NULL：系统表或视图，不能进行分片。