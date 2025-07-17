---
title: MySQL 兼容性
summary: 了解 TiDB 与 MySQL 的兼容性，以及不支持和不同的功能。
---

# MySQL 兼容性

<CustomContent platform="tidb">

TiDB 与 MySQL 协议以及 MySQL 5.7 和 MySQL 8.0 的常用功能和语法具有高度兼容性。MySQL 生态系统中的工具（PHPMyAdmin、Navicat、MySQL Workbench、DBeaver 以及 [更多](/develop/dev-guide-third-party-support.md#gui)）和 MySQL 客户端都可以用于 TiDB。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB 与 MySQL 协议以及 MySQL 5.7 和 MySQL 8.0 的常用功能和语法具有高度兼容性。MySQL 生态系统中的工具（PHPMyAdmin、Navicat、MySQL Workbench、DBeaver 以及 [更多](https://docs.pingcap.com/tidb/stable/dev-guide-third-party-support#gui)）和 MySQL 客户端都可以用于 TiDB。

</CustomContent>

然而，MySQL 的一些功能在 TiDB 中不被支持。这可能是因为存在更好的解决方案（例如使用 JSON 代替 XML 函数）或当前需求与实现难度不符（例如存储过程和函数）。此外，一些功能在分布式系统中实现起来可能较为困难。

<CustomContent platform="tidb">

需要注意的是，TiDB 不支持 MySQL 的复制协议。相反，提供了专门的工具用于与 MySQL 进行数据复制：

- 从 MySQL 复制数据：[TiDB Data Migration (DM)](/dm/dm-overview.md) 是一款支持从 MySQL 或 MariaDB 完整迁移和增量复制数据到 TiDB 的工具。
- 复制数据到 MySQL：[TiCDC](/ticdc/ticdc-overview.md) 是一款通过拉取 TiKV 变更日志实现 TiDB 增量数据复制的工具。TiCDC 使用 [MySQL sink](/ticdc/ticdc-overview.md#replication-consistency) 将 TiDB 的增量数据复制到 MySQL。

</CustomContent>

<CustomContent platform="tidb">

> **Note:**
>
> 本页描述了 MySQL 与 TiDB 之间的一般差异。关于安全方面的 MySQL 兼容性，详见 [Security Compatibility with MySQL](/security-compatibility-with-mysql.md)。

</CustomContent>

你可以在 [TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&utm_medium=mysql_compatibility) 试用 TiDB 的功能。

## 不支持的功能

+ 存储过程和函数
+ 触发器
+ 事件
+ 用户定义函数
+ `FULLTEXT` 语法和索引 [#1793](https://github.com/pingcap/tidb/issues/1793)
+ `SPATIAL`（也称为 `GIS`/`GEOMETRY`）函数、数据类型和索引 [#6347](https://github.com/pingcap/tidb/issues/6347)
+ 除 `ascii`、`latin1`、`binary`、`utf8`、`utf8mb4` 和 `gbk` 之外的字符集
+ 优化器跟踪
+ XML 函数
+ X-Protocol [#1109](https://github.com/pingcap/tidb/issues/1109)
+ 列级权限 [#9766](https://github.com/pingcap/tidb/issues/9766)
+ `XA` 语法（TiDB 内部使用两阶段提交，但不通过 SQL 接口暴露）
+ `CREATE TABLE tblName AS SELECT stmt` 语法 [#4754](https://github.com/pingcap/tidb/issues/4754)
+ `CHECK TABLE` 语法 [#4673](https://github.com/pingcap/tidb/issues/4673)
+ `CHECKSUM TABLE` 语法 [#1895](https://github.com/pingcap/tidb/issues/1895)
+ `REPAIR TABLE` 语法
+ `OPTIMIZE TABLE` 语法
+ `HANDLER` 语句
+ `CREATE TABLESPACE` 语句
+ "Session Tracker: Add GTIDs context to the OK packet"
+ Descending Index [#2519](https://github.com/pingcap/tidb/issues/2519)
+ `SKIP LOCKED` 语法 [#18207](https://github.com/pingcap/tidb/issues/18207)
+ Lateral derived tables [#40328](https://github.com/pingcap/tidb/issues/40328)
+ JOIN ON 子查询 [#11414](https://github.com/pingcap/tidb/issues/11414)

## 与 MySQL 的差异

### 自增 ID

+ 在 TiDB 中，自增列的值（ID）在全局范围内唯一，并在单个 TiDB 服务器内递增。为了在多个 TiDB 服务器之间实现 ID 的递增，可以使用 [`AUTO_INCREMENT` MySQL 兼容模式](/auto-increment.md#mysql-compatibility-mode)。但需要注意的是，ID 不一定是连续分配的，因此建议避免混用默认值和自定义值，以防遇到 `Duplicated Error` 错误。

+ 你可以使用系统变量 `tidb_allow_remove_auto_inc` 来允许或禁止移除 `AUTO_INCREMENT` 列属性。若要移除该属性，可以使用 `ALTER TABLE MODIFY` 或 `ALTER TABLE CHANGE` 语法。

+ TiDB 不支持添加 `AUTO_INCREMENT` 列属性，一旦移除，无法恢复。

+ 对于 TiDB v6.6.0 及之前版本，TiDB 中的自增列行为与 MySQL InnoDB 相同，要求它们为主键或索引前缀。从 v7.0.0 开始，TiDB 移除了此限制，允许更灵活的表主键定义。[#40580](https://github.com/pingcap/tidb/issues/40580)

更多详情请参见 [`AUTO_INCREMENT`](/auto-increment.md)。

> **Note:**
>
> + 如果在创建表时未指定主键，TiDB 会使用 `_tidb_rowid` 来标识行。该值的分配与自增列（如果存在）共享一个分配器。如果你将自增列设为主键，TiDB 会使用此列来标识行。在这种情况下，可能会出现：

```sql
mysql> CREATE TABLE t(id INT UNIQUE KEY AUTO_INCREMENT);
Query OK, 0 rows affected (0.05 sec)

mysql> INSERT INTO t VALUES();
Query OK, 1 rows affected (0.00 sec)

mysql> INSERT INTO t VALUES();
Query OK, 1 rows affected (0.00 sec)

mysql> INSERT INTO t VALUES();
Query OK, 1 rows affected (0.00 sec)

mysql> SELECT _tidb_rowid, id FROM t;
+-------------+------+
| _tidb_rowid | id   |
+-------------+------+
|           2 |    1 |
|           4 |    3 |
|           6 |    5 |
+-------------+------+
3 rows in set (0.01 sec)
```

如上所示，由于共享分配器，`id` 每次递增 2。在 [MySQL 兼容模式](/auto-increment.md#mysql-compatibility-mode)中，此行为会改变，不再使用共享分配器，因此不会跳号。

<CustomContent platform="tidb">

> **Note:**
>
> `AUTO_INCREMENT` 属性可能会在生产环境中引发热点问题。详情请参见 [Troubleshoot HotSpot Issues](/troubleshoot-hot-spot-issues.md)。建议使用 [`AUTO_RANDOM`](/auto-random.md) 代替。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> `AUTO_INCREMENT` 属性可能会在生产环境中引发热点问题。详情请参见 [Troubleshoot HotSpot Issues](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#handle-auto-increment-primary-key-hotspot-tables-using-auto_random)。建议使用 [`AUTO_RANDOM`](/auto-random.md) 代替。

</CustomContent>

### 性能模式

<CustomContent platform="tidb">

TiDB 利用 [Prometheus 和 Grafana](/tidb-monitoring-api.md) 组合存储和查询性能监控指标。在 TiDB 中，大多数 [性能模式表](/performance-schema/performance-schema.md) 不会返回任何结果。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 TiDB Cloud 中查看性能指标，可以在 TiDB Cloud 控制台的集群概览页面查看，或使用 [第三方监控集成](/tidb-cloud/third-party-monitoring-integrations.md)。大多数 [性能模式表](/performance-schema/performance-schema.md) 在 TiDB 中返回空结果。

</CustomContent>

### 查询执行计划

TiDB 中的查询执行计划（`EXPLAIN`/`EXPLAIN FOR`）的输出格式、内容和权限设置与 MySQL 有显著差异。

在 TiDB 中，MySQL 的系统变量 `optimizer_switch` 是只读的，不会影响查询计划。虽然可以使用类似 MySQL 的语法添加优化提示，但可用的提示和其实现可能不同。

更多信息请参见 [Understand the Query Execution Plan](/explain-overview.md)。

### 内置函数

TiDB 支持大部分 MySQL 的内置函数，但并非全部。你可以使用 [`SHOW BUILTINS`](/sql-statements/sql-statement-show-builtins.md) 来获取可用函数的列表。

### DDL 操作

在 TiDB 中，所有支持的 DDL 变更都可以在线进行。然而，与 MySQL 相比，TiDB 在 DDL 操作上存在一些主要限制：

* 使用单个 `ALTER TABLE` 语句修改多个表结构对象（如列或索引）时，不支持对同一对象进行多次变更。例如，执行 `ALTER TABLE t1 MODIFY COLUMN c1 INT, DROP COLUMN c1` 时，会报 `Unsupported operate same column/index` 错误。
* 不支持用单个 `ALTER TABLE` 语句修改多个 TiDB 特有的 schema 对象，如 `TIFLASH REPLICA`、`SHARD_ROW_ID_BITS` 和 `AUTO_ID_CACHE`。
* TiDB 不支持通过 `ALTER TABLE` 改变某些数据类型。例如，不支持将 `DECIMAL` 类型改为 `DATE` 类型。如果不支持此类数据类型变更，会报 `Unsupported modify column: type %d not match origin %d` 错误。更多详情请参见 [`ALTER TABLE`](/sql-statements/sql-statement-modify-column.md)。
* `ALGORITHM={INSTANT,INPLACE,COPY}` 语法在 TiDB 中仅作为断言，不会影响 `ALTER` 的算法。详见 [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md)。
* 不支持添加/删除 `CLUSTERED` 类型的主键。关于 `CLUSTERED` 主键的更多信息，请参见 [clustered index](/clustered-indexes.md)。
* 不支持不同类型的索引（`HASH|BTREE|RTREE|FULLTEXT`），指定时会被解析后忽略。
* TiDB 支持 `HASH`、`RANGE`、`LIST` 和 `KEY` 分区类型。不支持的分区类型会返回 `Warning: Unsupported partition type %s, treat as normal table`，其中 `%s` 为具体不支持的分区类型。
* Range、Range COLUMNS、List 和 List COLUMNS 分区表支持 `ADD`、`DROP`、`TRUNCATE` 和 `REORGANIZE` 操作。其他分区操作会被忽略。
* Hash 和 Key 分区表支持 `ADD`、`COALESCE` 和 `TRUNCATE` 操作。其他分区操作会被忽略。
* 不支持以下分区语法：

    - `SUBPARTITION`
    - `{CHECK|OPTIMIZE|REPAIR|IMPORT|DISCARD|REBUILD} PARTITION`

    更多关于分区的内容，请参见 [Partitioning](/partitioned-table.md)。

### 表统计信息分析

在 TiDB 中，[Statistics Collection](/statistics.md#manual-collection) 与 MySQL 不同，它会完全重建表的统计信息，这是一项资源消耗较大的操作，耗时较长。而 MySQL/InnoDB 执行的是相对轻量且短暂的操作。

更多信息请参见 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)。

### `SELECT` 语法的限制

TiDB 不支持以下 `SELECT` 语法：

- `SELECT ... INTO @variable`
- `SELECT .. GROUP BY expr` 不会像 MySQL 5.7 那样隐含 `GROUP BY expr ORDER BY expr`。

更多详情请参见 [`SELECT`](/sql-statements/sql-statement-select.md)。

### `UPDATE` 语句

详见 [`UPDATE`](/sql-statements/sql-statement-update.md)。

### 视图

TiDB 中的视图不可更新，不支持 `UPDATE`、`INSERT` 和 `DELETE` 等写操作。

### 临时表

更多信息请参见 [TiDB 本地临时表与 MySQL 临时表的兼容性](/temporary-tables.md#compatibility-with-mysql-temporary-tables)。

### 字符集和排序规则

* 了解 TiDB 支持的字符集和排序规则，请参见 [Character Set and Collation Overview](/character-set-and-collation.md)。

* 关于 GBK 字符集的 MySQL 兼容性信息，详见 [GBK compatibility](/character-set-gbk.md#mysql-compatibility)。

* TiDB 继承表中使用的字符集作为国家字符集。

### 存储引擎

TiDB 允许创建使用其他存储引擎的表。尽管如此，TiDB 所描述的元数据是针对 InnoDB 存储引擎的，以确保兼容性。

<CustomContent platform="tidb">

使用 [`--store`](/command-line-flags-for-tidb-configuration.md#--store) 选项指定存储引擎时，必须启动 TiDB 服务器。此存储引擎抽象功能类似于 MySQL。

</CustomContent>

### SQL 模式

TiDB 支持大部分 [SQL 模式](/sql-mode.md)：

- 兼容模式（如 `Oracle` 和 `PostgreSQL`）会被解析但忽略。MySQL 5.7 中已弃用，MySQL 8.0 中已移除。
- `ONLY_FULL_GROUP_BY` 模式与 MySQL 5.7 存在细微 [语义差异](/functions-and-operators/aggregate-group-by-functions.md#differences-from-mysql)。
- MySQL 中的 `NO_DIR_IN_CREATE` 和 `NO_ENGINE_SUBSTITUTION` 模式在兼容性方面被接受，但不适用于 TiDB。

### 默认值差异

TiDB 与 MySQL 5.7 和 MySQL 8.0 在默认值上存在差异：

- 默认字符集：
    - TiDB 的默认值为 `utf8mb4`。
    - MySQL 5.7 的默认值为 `latin1`。
    - MySQL 8.0 的默认值为 `utf8mb4`。
- 默认排序规则：
    - TiDB 的默认排序规则为 `utf8mb4_bin`。
    - MySQL 5.7 的默认排序规则为 `utf8mb4_general_ci`。
    - MySQL 8.0 的默认排序规则为 `utf8mb4_0900_ai_ci`。
- 默认 SQL 模式：
    - TiDB 的默认 SQL 模式包括：`ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`。
    - MySQL 的默认 SQL 模式：
        - MySQL 5.7 的默认值与 TiDB 相同。
        - MySQL 8.0 的默认值包括：`ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION`。
- `lower_case_table_names` 的默认值：
    - TiDB 的默认值为 `2`，且目前只支持 `2`。
    - MySQL 默认值如下：
        - 在 Linux 上：`0`，表示按创建表或数据库时指定的大小写存储，名称比较区分大小写。
        - 在 Windows 上：`1`，表示表名存储为小写，名称比较不区分大小写。MySQL 在存储和查找时会将所有表名转换为小写。此行为也适用于数据库名和表别名。
        - 在 macOS 上：`2`，表示按创建时指定的大小写存储，但在查找时会转换为小写，名称比较不区分大小写。
- `explicit_defaults_for_timestamp` 的默认值：
    - TiDB 的默认值为 `ON`，且目前只支持 `ON`。
    - MySQL 默认值：
        - MySQL 5.7：`OFF`。
        - MySQL 8.0：`ON`。

### 日期和时间

TiDB 支持命名时区，考虑如下：

+ TiDB 使用系统中已安装的所有时区规则（通常为 `tzdata` 包）进行计算。这使得可以使用所有时区名称，无需导入时区表数据。导入时区表数据不会改变计算规则。
+ 目前，MySQL 默认使用本地时区，然后依赖系统内置的当前时区规则（例如夏令时开始时）进行计算。若未 [导入时区表数据](https://dev.mysql.com/doc/refman/8.0/en/time-zone-support.html#time-zone-installation)，MySQL 无法通过名称指定时区。

### 类型系统差异

MySQL 支持但 TiDB **不支持** 以下列类型：

- `SQL_TSI_*`（包括 SQL_TSI_MONTH、SQL_TSI_WEEK、SQL_TSI_DAY、SQL_TSI_HOUR、SQL_TSI_MINUTE 和 SQL_TSI_SECOND，但不包括 SQL_TSI_YEAR）

### 正则表达式

关于 TiDB 与 MySQL 正则表达式兼容性的信息，包括 `REGEXP_INSTR()`、`REGEXP_LIKE()`、`REGEXP_REPLACE()` 和 `REGEXP_SUBSTR()`，请参见 [Regular expression compatibility with MySQL](/functions-and-operators/string-functions.md#regular-expression-compatibility-with-mysql)。

### 不兼容的已弃用功能

TiDB 不实现 MySQL 中已弃用的特定功能，包括：

- 指定浮点类型的精度。MySQL 8.0 [弃用](https://dev.mysql.com/doc/refman/8.0/en/floating-point-types.html) 了此功能，建议使用 `DECIMAL` 类型。
- `ZEROFILL` 属性。MySQL 8.0 [弃用](https://dev.mysql.com/doc/refman/8.0/en/numeric-type-attributes.html)，建议在应用中用补零方式处理。

### `CREATE RESOURCE GROUP`、`DROP RESOURCE GROUP` 和 `ALTER RESOURCE GROUP` 语句

创建、修改和删除资源组的相关语句参数支持与 MySQL 不同。详情请参见：

- [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md)
- [`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md)
- [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md)

## 与 MySQL InnoDB 的悲观事务（锁）差异

关于 TiDB 和 MySQL InnoDB 在悲观事务（锁）方面的差异，详见 [Differences from MySQL InnoDB](/pessimistic-transaction.md#differences-from-mysql-innodb)。