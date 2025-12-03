---
title: MySQL 兼容性
summary: 了解 TiDB 与 MySQL 的兼容性，以及不支持和存在差异的特性。
---

# MySQL 兼容性

<CustomContent platform="tidb">

TiDB 高度兼容 MySQL 协议，以及 MySQL 5.7 和 MySQL 8.0 的常用特性和语法。MySQL 的生态工具（PHPMyAdmin、Navicat、MySQL Workbench、DBeaver 以及 [更多](/develop/dev-guide-third-party-support.md#gui)）和 MySQL 客户端均可用于 TiDB。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB 高度兼容 MySQL 协议，以及 MySQL 5.7 和 MySQL 8.0 的常用特性和语法。MySQL 的生态工具（PHPMyAdmin、Navicat、MySQL Workbench、DBeaver 以及 [更多](https://docs.pingcap.com/tidb/stable/dev-guide-third-party-support#gui)）和 MySQL 客户端均可用于 TiDB。

</CustomContent>

然而，TiDB 并不支持 MySQL 的部分特性。这可能是因为现在有更好的方式来解决相关问题（例如使用 JSON 替代 XML 函数），或者当前需求较少且实现成本较高（如存储过程和函数）。此外，某些特性在分布式系统中实现难度较大。

<CustomContent platform="tidb">

需要注意的是，TiDB 不支持 MySQL 的复制协议。相应地，TiDB 提供了专用工具与 MySQL 进行数据同步：

- 从 MySQL 迁移数据： [TiDB Data Migration (DM)](/dm/dm-overview.md) 是一款支持从 MySQL 或 MariaDB 到 TiDB 的全量数据迁移和增量数据同步的工具。
- 向 MySQL 同步数据： [TiCDC](/ticdc/ticdc-overview.md) 是一款通过拉取 TiKV 变更日志实现 TiDB 增量数据同步的工具。TiCDC 使用 [MySQL sink](/ticdc/ticdc-overview.md#replication-consistency) 将 TiDB 的增量数据同步到 MySQL。

</CustomContent>

<CustomContent platform="tidb">

> **Note:**
>
> 本页面描述了 MySQL 与 TiDB 之间的一般性差异。关于安全性方面的兼容性，详见 [与 MySQL 的安全性兼容性](/security-compatibility-with-mysql.md)。

</CustomContent>

你可以在 [TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&utm_medium=mysql_compatibility) 上体验 TiDB 的相关特性。

## 不支持的特性

+ 存储过程和函数
+ 触发器
+ 事件
+ 用户自定义函数
+ `FULLTEXT` 语法和索引 [#1793](https://github.com/pingcap/tidb/issues/1793)

    >**Note:**
    >
    > 目前，仅部分 AWS 区域的 TiDB Cloud Starter 和 TiDB Cloud Essential 集群支持 [`FULLTEXT` 语法和索引](https://docs.pingcap.com/tidbcloud/vector-search-full-text-search-sql)。TiDB 自建版和 TiDB Cloud Dedicated 支持解析 `FULLTEXT` 语法，但不支持使用 `FULLTEXT` 索引。

+ `SPATIAL`（也称为 `GIS`/`GEOMETRY`）函数、数据类型和索引 [#6347](https://github.com/pingcap/tidb/issues/6347)
+ 除 `ascii`、`latin1`、`binary`、`utf8`、`utf8mb4` 和 `gbk` 之外的字符集
+ 优化器追踪
+ XML 函数
+ X-Protocol [#1109](https://github.com/pingcap/tidb/issues/1109)
+ 列级权限 [#9766](https://github.com/pingcap/tidb/issues/9766)
+ `XA` 语法（TiDB 内部使用两阶段提交，但未通过 SQL 接口暴露）
+ `CREATE TABLE tblName AS SELECT stmt` 语法 [#4754](https://github.com/pingcap/tidb/issues/4754)
+ `CHECK TABLE` 语法 [#4673](https://github.com/pingcap/tidb/issues/4673)
+ `CHECKSUM TABLE` 语法 [#1895](https://github.com/pingcap/tidb/issues/1895)
+ `REPAIR TABLE` 语法
+ `OPTIMIZE TABLE` 语法
+ `HANDLER` 语句
+ `CREATE TABLESPACE` 语句
+ "Session Tracker: Add GTIDs context to the OK packet"
+ 降序索引 [#2519](https://github.com/pingcap/tidb/issues/2519)
+ `SKIP LOCKED` 语法 [#18207](https://github.com/pingcap/tidb/issues/18207)
+ Lateral 派生表 [#40328](https://github.com/pingcap/tidb/issues/40328)
+ JOIN ON 子查询 [#11414](https://github.com/pingcap/tidb/issues/11414)

## 与 MySQL 的差异

### 自增 ID

+ 在 TiDB 中，自增列的值（ID）在单个 TiDB 实例内是全局唯一且递增的。若需在多 TiDB 实例间实现递增，可以使用 [`AUTO_INCREMENT` MySQL 兼容模式](/auto-increment.md#mysql-compatibility-mode)。但分配的 ID 不一定严格连续，因此建议避免混用默认值和自定义值，以防出现 `Duplicated Error` 错误。

+ 你可以通过 `tidb_allow_remove_auto_inc` 系统变量来允许或禁止移除 `AUTO_INCREMENT` 列属性。移除列属性时，可使用 `ALTER TABLE MODIFY` 或 `ALTER TABLE CHANGE` 语法。

+ TiDB 不支持新增 `AUTO_INCREMENT` 列属性，且一旦移除后无法恢复。

+ 在 TiDB v6.6.0 及之前版本，自增列行为与 MySQL InnoDB 一致，要求其为主键或索引前缀。从 v7.0.0 起，TiDB 移除了该限制，允许更灵活的表主键定义。[#40580](https://github.com/pingcap/tidb/issues/40580)

更多细节参见 [`AUTO_INCREMENT`](/auto-increment.md)。

> **Note:**
>
> + 如果在建表时未指定主键，TiDB 会使用 `_tidb_rowid` 作为行标识。该值的分配与自增列（如存在）共用一个分配器。如果指定自增列为主键，TiDB 会使用该列作为行标识。在这种情况下，可能会出现如下情况：

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

如上所示，由于共用分配器，`id` 每次递增 2。该行为在 [MySQL 兼容模式](/auto-increment.md#mysql-compatibility-mode) 下会发生变化，此时不再共用分配器，因此不会跳号。

<CustomContent platform="tidb">

> **Note:**
>
> `AUTO_INCREMENT` 属性在生产环境中可能导致热点问题。详见 [热点问题排查](/troubleshoot-hot-spot-issues.md)。推荐使用 [`AUTO_RANDOM`](/auto-random.md) 代替。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> `AUTO_INCREMENT` 属性在生产环境中可能导致热点问题。详见 [热点问题排查](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#handle-auto-increment-primary-key-hotspot-tables-using-auto_random)。推荐使用 [`AUTO_RANDOM`](/auto-random.md) 代替。

</CustomContent>

### 性能模式（Performance schema）

<CustomContent platform="tidb">

TiDB 结合了 [Prometheus 和 Grafana](/tidb-monitoring-api.md) 用于存储和查询性能监控指标。在 TiDB 中，大多数 [performance schema 表](/performance-schema/performance-schema.md) 不返回任何结果。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 TiDB Cloud 中，你可以在 TiDB Cloud 控制台的集群总览页面查看性能指标，或使用 [第三方监控集成](/tidb-cloud/third-party-monitoring-integrations.md)。在 TiDB 中，大多数 [performance schema 表](/performance-schema/performance-schema.md) 返回空结果。

</CustomContent>

### 查询执行计划

TiDB 中查询执行计划（`EXPLAIN`/`EXPLAIN FOR`）的输出格式、内容和权限设置与 MySQL 有较大差异。

在 TiDB 中，MySQL 系统变量 `optimizer_switch` 为只读，对查询计划无影响。虽然优化器 Hint 语法与 MySQL 类似，但可用的 Hint 及其实现可能不同。

更多信息参见 [理解查询执行计划](/explain-overview.md)。

### 内置函数

TiDB 支持大多数 MySQL 的内置函数，但并非全部。你可以使用 [`SHOW BUILTINS`](/sql-statements/sql-statement-show-builtins.md) 语句获取可用函数列表。

### DDL 操作

在 TiDB 中，所有支持的 DDL 变更均可在线完成。但与 MySQL 相比，TiDB 在 DDL 操作上有以下主要限制：

* 使用单条 `ALTER TABLE` 语句修改同一张表的多个 schema 对象（如列或索引）时，不支持对同一对象进行多次变更。例如，执行 `ALTER TABLE t1 MODIFY COLUMN c1 INT, DROP COLUMN c1` 会报错 `Unsupported operate same column/index`。
* 不支持通过单条 `ALTER TABLE` 语句同时修改多个 TiDB 特有的 schema 对象，如 `TIFLASH REPLICA`、`SHARD_ROW_ID_BITS` 和 `AUTO_ID_CACHE`。
* TiDB 不支持通过 `ALTER TABLE` 修改某些数据类型。例如，不支持将 `DECIMAL` 类型修改为 `DATE` 类型。若不支持的数据类型变更，TiDB 会报错 `Unsupported modify column: type %d not match origin %d`。详情参见 [`ALTER TABLE`](/sql-statements/sql-statement-modify-column.md)。
* `ALGORITHM={INSTANT,INPLACE,COPY}` 语法在 TiDB 中仅作为断言存在，不会改变 `ALTER` 算法。详见 [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md)。
* 不支持对 `CLUSTERED` 类型的主键进行添加/删除。关于 `CLUSTERED` 类型主键的更多信息，参见 [聚簇索引](/clustered-indexes.md)。
* 不支持不同类型的索引（`HASH|BTREE|RTREE|FULLTEXT`），指定时会被解析并忽略。
* TiDB 支持 `HASH`、`RANGE`、`LIST` 和 `KEY` 分区类型。对于不支持的分区类型，TiDB 返回 `Warning: Unsupported partition type %s, treat as normal table`，其中 `%s` 为具体不支持的分区类型。
* Range、Range COLUMNS、List 和 List COLUMNS 分区表支持 `ADD`、`DROP`、`TRUNCATE` 和 `REORGANIZE` 操作。其他分区操作会被忽略。
* Hash 和 Key 分区表支持 `ADD`、`COALESCE` 和 `TRUNCATE` 操作。其他分区操作会被忽略。
* 分区表不支持以下语法：

    - `SUBPARTITION`
    - `{CHECK|OPTIMIZE|REPAIR|IMPORT|DISCARD|REBUILD} PARTITION`

    更多分区相关内容，参见 [分区表](/partitioned-table.md)。

### 表分析

在 TiDB 中，[统计信息收集](/statistics.md#manual-collection) 与 MySQL 不同，会完全重建表的统计信息，因此资源消耗更大，耗时更长。而 MySQL/InnoDB 执行的是相对轻量、耗时较短的操作。

更多信息参见 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)。

### `SELECT` 语法限制

TiDB 不支持以下 `SELECT` 语法：

- `SELECT ... INTO @variable`
- `SELECT .. GROUP BY expr` 不像 MySQL 5.7 那样隐式等同于 `GROUP BY expr ORDER BY expr`。

更多细节参见 [`SELECT`](/sql-statements/sql-statement-select.md) 语句参考。

### `UPDATE` 语句

参见 [`UPDATE`](/sql-statements/sql-statement-update.md) 语句参考。

### 视图

TiDB 中的视图不可更新，不支持 `UPDATE`、`INSERT`、`DELETE` 等写操作。

### 临时表

更多信息参见 [TiDB 本地临时表与 MySQL 临时表的兼容性](/temporary-tables.md#compatibility-with-mysql-temporary-tables)。

### 字符集与排序规则

* 了解 TiDB 支持的字符集与排序规则，参见 [字符集与排序规则概述](/character-set-and-collation.md)。

* 关于 GBK 字符集的 MySQL 兼容性，参见 [GBK 兼容性](/character-set-gbk.md#mysql-compatibility)。

* TiDB 继承表中使用的字符集作为国家字符集。

### 存储引擎

TiDB 支持使用不同的存储引擎创建表。尽管如此，TiDB 描述的元数据仍为 InnoDB 存储引擎，以保证兼容性。

<CustomContent platform="tidb">

通过 [`--store`](/command-line-flags-for-tidb-configuration.md#--store) 选项指定存储引擎时，需要启动 TiDB 服务器。该存储引擎抽象特性与 MySQL 类似。

</CustomContent>

### SQL 模式

TiDB 支持大多数 [SQL 模式](/sql-mode.md)：

- 兼容性模式，如 `Oracle` 和 `PostgreSQL`，会被解析但被忽略。兼容性模式在 MySQL 5.7 中已废弃，在 MySQL 8.0 中已移除。
- `ONLY_FULL_GROUP_BY` 模式与 MySQL 5.7 存在 [语义差异](/functions-and-operators/aggregate-group-by-functions.md#differences-from-mysql)。
- MySQL 的 `NO_DIR_IN_CREATE` 和 `NO_ENGINE_SUBSTITUTION` SQL 模式为兼容性而接受，但在 TiDB 中无实际作用。

### 默认差异

TiDB 与 MySQL 5.7 和 MySQL 8.0 的默认值存在如下差异：

- 默认字符集：
    - TiDB 默认值为 `utf8mb4`。
    - MySQL 5.7 默认值为 `latin1`。
    - MySQL 8.0 默认值为 `utf8mb4`。
- 默认排序规则：
    - TiDB 默认排序规则为 `utf8mb4_bin`。
    - MySQL 5.7 默认排序规则为 `utf8mb4_general_ci`。
    - MySQL 8.0 默认排序规则为 `utf8mb4_0900_ai_ci`。
- 默认 SQL 模式：
    - TiDB 默认 SQL 模式包含：`ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`。
    - MySQL 默认 SQL 模式：
        - MySQL 5.7 的默认 SQL 模式与 TiDB 相同。
        - MySQL 8.0 的默认 SQL 模式包含：`ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION`。
- `lower_case_table_names` 的默认值：
    - TiDB 的默认值为 `2`，且目前仅支持 `2`。
    - MySQL 的默认值如下：
        - Linux 上为 `0`，表示表名和数据库名在磁盘上按 `CREATE TABLE` 或 `CREATE DATABASE` 语句指定的大小写存储，名称比较区分大小写。
        - Windows 上为 `1`，表示表名在磁盘上以小写存储，名称比较不区分大小写。MySQL 在存储和查找时会将所有表名转换为小写。该行为同样适用于数据库名和表别名。
        - macOS 上为 `2`，表示表名和数据库名在磁盘上按 `CREATE TABLE` 或 `CREATE DATABASE` 语句指定的大小写存储，但 MySQL 在查找时会将其转换为小写，名称比较不区分大小写。
- `explicit_defaults_for_timestamp` 的默认值：
    - TiDB 的默认值为 `ON`，且目前仅支持 `ON`。
    - MySQL 的默认值如下：
        - MySQL 5.7：`OFF`。
        - MySQL 8.0：`ON`。

### 日期与时间

TiDB 支持命名时区，具体说明如下：

+ TiDB 使用系统当前安装的所有时区规则（通常为 `tzdata` 包）进行计算，因此可以直接使用所有时区名称，无需导入时区表数据。导入时区表数据不会改变计算规则。
+ 目前，MySQL 默认使用本地时区，然后依赖系统内置的当前时区规则（例如夏令时开始时）进行计算。若未 [导入时区表数据](https://dev.mysql.com/doc/refman/8.0/en/time-zone-support.html#time-zone-installation)，MySQL 无法通过名称指定时区。

### 类型系统差异

以下列类型为 MySQL 支持但 TiDB **不支持**：

- `SQL_TSI_*`（包括 SQL_TSI_MONTH、SQL_TSI_WEEK、SQL_TSI_DAY、SQL_TSI_HOUR、SQL_TSI_MINUTE 和 SQL_TSI_SECOND，但不包括 SQL_TSI_YEAR）

### 正则表达式

关于 TiDB 正则表达式与 MySQL 的兼容性，包括 `REGEXP_INSTR()`、`REGEXP_LIKE()`、`REGEXP_REPLACE()` 和 `REGEXP_SUBSTR()`，参见 [正则表达式与 MySQL 的兼容性](/functions-and-operators/string-functions.md#regular-expression-compatibility-with-mysql)。

### 由于废弃特性导致的不兼容

TiDB 未实现 MySQL 中已废弃的部分特性，包括：

- 浮点类型指定精度。MySQL 8.0 [已废弃](https://dev.mysql.com/doc/refman/8.0/en/floating-point-types.html) 该特性，推荐使用 `DECIMAL` 类型。
- `ZEROFILL` 属性。MySQL 8.0 [已废弃](https://dev.mysql.com/doc/refman/8.0/en/numeric-type-attributes.html) 该特性，推荐在应用层对数值进行补零。

### `CREATE RESOURCE GROUP`、`DROP RESOURCE GROUP` 和 `ALTER RESOURCE GROUP` 语句

以下用于创建、修改和删除资源组的语句，其支持的参数与 MySQL 不同。详情参见以下文档：

- [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md)
- [`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md)
- [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md)

## TiDB 与 MySQL InnoDB 悲观事务（锁）的差异

关于 TiDB 与 MySQL InnoDB 在悲观事务（锁）方面的差异，参见 [与 MySQL InnoDB 的差异](/pessimistic-transaction.md#differences-from-mysql-innodb)。