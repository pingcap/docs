---
title: SQL Prepared Execution Plan Cache
summary: 了解 TiDB 中的 SQL Prepared 执行计划缓存。
---

# SQL Prepared 执行计划缓存

TiDB 支持对 `Prepare` 和 `Execute` 查询的执行计划进行缓存。这包括两种形式的预处理语句：

- 使用 `COM_STMT_PREPARE` 和 `COM_STMT_EXECUTE` 协议特性。
- 使用 SQL 语句 `PREPARE` 和 `EXECUTE`。

TiDB 优化器对这两类查询的处理方式相同：在准备阶段，参数化的查询会被解析成 AST（抽象语法树）并缓存；在后续执行时，执行计划会根据存储的 AST 和具体参数值生成。

当启用执行计划缓存时，在第一次执行时，每个 `Prepare` 语句会检查当前查询是否可以使用执行计划缓存，如果可以，则将生成的执行计划放入由 LRU（最近最少使用）链表实现的缓存中。在随后的 `Execute` 查询中，会从缓存中获取执行计划并进行可用性检查。如果检查成功，则跳过生成执行计划的步骤；否则，重新生成执行计划并保存到缓存中。

TiDB 还支持对某些非 `PREPARE` 语句的执行计划缓存，类似于 `Prepare`/`Execute` 语句。更多详情请参考 [Non-prepared plan cache](/sql-non-prepared-plan-cache.md)。

在当前版本的 TiDB 中，如果一个 `Prepare` 语句满足以下任意条件，则该查询或计划不会被缓存：

- 查询包含 `SELECT`、`UPDATE`、`INSERT`、`DELETE`、`Union`、`Intersect` 和 `Except` 以外的 SQL 语句。
- 查询访问临时表，或包含生成列的表，或使用静态模式（即 [`tidb_partition_prune_mode`](/system-variables.md#tidb_partition_prune_mode-new-in-v51) 设置为 `static`）访问分区表。
- 查询包含非相关子查询，例如 `SELECT * FROM t1 WHERE t1.a > (SELECT 1 FROM t2 WHERE t2.b < 1)`。
- 查询包含在执行计划中带有 `PhysicalApply` 操作符的相关子查询，例如 `SELECT * FROM t1 WHERE t1.a > (SELECT a FROM t2 WHERE t1.b > t2.b)`。
- 查询包含 `ignore_plan_cache` 或 `set_var` 提示，例如 `SELECT /*+ ignore_plan_cache() */ * FROM t` 或 `SELECT /*+ set_var(max_execution_time=1) */ * FROM t`。
- 查询包含除 `?` 以外的变量（包括系统变量或用户定义变量），例如 `select * from t where a>? and b>@x`。
- 查询包含无法缓存的函数：`database()`、`current_user`、`current_role`、`user`、`connection_id`、`last_insert_id`、`row_count`、`version` 和 `like`。
- 查询使用变量作为 `LIMIT` 参数（如 `LIMIT ?` 和 `LIMIT 10, ?`），且变量值大于 10000。
- 查询在 `Order By` 后包含 `?`，如 `Order By ?`。此类查询根据 `?` 指定的列排序。如果针对不同列的查询使用相同的执行计划，结果会出错。因此，这类查询不缓存。但如果是常见的查询，例如 `Order By a+?`，则会缓存。
- 查询在 `Group By` 后包含 `?`，如 `Group By?`。此类查询根据 `?` 指定的列分组。如果针对不同列的查询使用相同的执行计划，结果会出错。因此，这类查询不缓存。但如果是常见的查询，例如 `Group By a+?`，则会缓存。
- 查询在定义 `Window Frame` 窗口函数时包含 `?`，如 `(partition by year order by sale rows ? preceding)`。如果 `?` 出现在窗口函数的其他位置，查询也会被缓存。
- 查询包含用于比较 `int` 和 `string` 的参数，例如 `c_int >= ?` 或 `c_int in (?, ?)`，其中 `?` 表示字符串类型，如 `set @x='123'`。为了确保查询结果与 MySQL 兼容，参数需要在每次查询中调整，因此此类查询不缓存。
- 计划尝试访问 `TiFlash`。
- 在大多数情况下，包含 `TableDual` 的计划不会被缓存，除非当前的 `Prepare` 语句没有参数。
- 查询访问 TiDB 系统视图，如 `information_schema.columns`。不建议使用 `Prepare` 和 `Execute` 语句访问系统视图。

TiDB 对查询中的 `?` 数量有限制。如果查询中包含超过 65535 个 `?`，会报错 `Prepared statement contains too many placeholders`。

LRU 链表设计为会话级缓存，因为 `Prepare`/`Execute` 不能跨会话执行。链表的每个元素是一个键值对，值为执行计划，键由以下部分组成：

- 执行 `Execute` 时所在的数据库名
- `Prepare` 语句的标识符，即 `PREPARE` 关键字后的名称
- 当前的 schema 版本，每次成功执行 DDL 语句后更新
- 执行 `Execute` 时的 SQL 模式
- 当前时区，即 `time_zone` 系统变量的值
- `sql_select_limit` 系统变量的值

任何上述信息的变化（例如切换数据库、重命名 `Prepare` 语句、执行 DDL 语句或修改 SQL 模式/`time_zone` 的值），或 LRU 缓存的淘汰机制，都会导致执行时的执行计划缓存未命中。

从缓存中获取执行计划后，TiDB 会首先检查执行计划是否仍然有效。如果当前 `Execute` 语句在显式事务中执行，且引用的表在事务预排序语句中被修改，且缓存的执行计划不包含 `UnionScan` 操作符，则不能执行。

验证通过后，会根据当前参数值调整执行计划的扫描范围，然后用以执行数据查询。

关于执行计划缓存和查询性能，有几点值得注意：

- 无论执行计划是否被缓存，都受 SQL 绑定的影响。对于未缓存的执行计划（第一次 `Execute`），会受到现有 SQL 绑定的影响；对于已缓存的执行计划，如果创建了新的 SQL 绑定，这些计划会变得无效。
- 缓存的计划不受统计信息变化、优化规则变化和表达式的阻塞推送影响。
- 考虑到 `Execute` 的参数不同，执行计划缓存禁止某些与特定参数值密切相关的激进查询优化方法，以确保适应性。这可能导致某些参数值下的查询计划不是最优的。例如，查询的过滤条件为 `where a > ? And a < ?`，第一次 `Execute` 时参数分别为 `2` 和 `1`，考虑到下一次执行时参数可能为 `1` 和 `2`，优化器不会生成针对当前参数值的最优 `TableDual` 执行计划；
- 如果不考虑缓存失效和淘汰，执行计划缓存会对各种参数值应用，理论上也会导致某些值的执行计划不是最优的。例如，过滤条件为 `where a < ?`，第一次执行时参数为 `1`，优化器会生成最优的 `IndexScan` 执行计划并缓存。在后续执行中，如果值变为 `10000`，可能 `TableScan` 计划更优。但由于使用了执行计划缓存，之前生成的 `IndexScan` 被用来执行。因此，执行计划缓存更适合查询简单（编译比例高）且执行计划相对固定的应用场景。

从 v6.1.0 版本开始，执行计划缓存默认开启。你可以通过系统变量 [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610) 控制预处理计划缓存。

> **Note:**
>
> [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610) 系统变量只控制 `Prepare`/`Execute` 查询的执行计划缓存，不影响普通查询。普通查询的执行计划缓存请参考 [SQL Non-Prepared Execution Plan Cache](/sql-non-prepared-plan-cache.md)。

启用执行计划缓存功能后，你可以使用会话级系统变量 [`last_plan_from_cache`](/system-variables.md#last_plan_from_cache-new-in-v40) 查看上一次 `Execute` 是否使用了缓存的执行计划，例如：


```sql
MySQL [test]> create table t(a int);
Query OK, 0 rows affected (0.00 sec)
MySQL [test]> prepare stmt from 'select * from t where a = ?';
Query OK, 0 rows affected (0.00 sec)
MySQL [test]> set @a = 1;
Query OK, 0 rows affected (0.00 sec)

-- 第一次执行会生成执行计划并保存到缓存中。
MySQL [test]> execute stmt using @a;
Empty set (0.00 sec)
MySQL [test]> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
| 0                      |
+------------------------+
1 row in set (0.00 sec)

-- 第二次执行命中缓存。
MySQL [test]> execute stmt using @a;
Empty set (0.00 sec)
MySQL [test]> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
| 1                      |
+------------------------+
1 row in set (0.00 sec)
```

如果你发现某组 `Prepare`/`Execute` 由于执行计划缓存导致行为异常，可以使用 `ignore_plan_cache()` SQL 提示跳过当前语句的执行计划缓存。以下为示例：


```sql
MySQL [test]> prepare stmt from 'select /*+ ignore_plan_cache() */ * from t where a = ?';
Query OK, 0 rows affected (0.00 sec)
MySQL [test]> set @a = 1;
Query OK, 0 rows affected (0.00 sec)
MySQL [test]> execute stmt using @a;
Empty set (0.00 sec)
MySQL [test]> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
| 0                      |
+------------------------+
1 row in set (0.00 sec)
MySQL [test]> execute stmt using @a;
Empty set (0.00 sec)
MySQL [test]> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
| 0                      |
+------------------------+
1 row in set (0.00 sec)
```

## 预处理计划缓存的诊断

### 使用 `SHOW WARNINGS` 进行诊断

某些查询或计划无法缓存。你可以使用 `SHOW WARNINGS` 语句检查查询或计划是否被缓存。如果未缓存，可以在结果中查看失败原因。例如：

```sql
mysql> PREPARE st FROM 'SELECT * FROM t WHERE a > (SELECT MAX(a) FROM t)';  -- 查询包含子查询，无法缓存。

Query OK, 0 rows affected, 1 warning (0.01 sec)

mysql> SHOW WARNINGS;  -- 检查查询计划无法缓存的原因。

+---------+------+-----------------------------------------------+
| Level   | Code | Message                                       |
+---------+------+-----------------------------------------------+
| Warning | 1105 | skip plan-cache: sub-queries are un-cacheable |
+---------+------+-----------------------------------------------+
1 row in set (0.00 sec)

mysql> prepare st from 'select * from t where a<?';

Query OK, 0 rows affected (0.00 sec)

mysql> set @a='1';

Query OK, 0 rows affected (0.00 sec)

mysql> execute st using @a;  -- 优化将非 INT 类型转换为 INT 类型，参数变化可能导致执行计划变化，因此不缓存。

Empty set, 1 warning (0.01 sec)

mysql> SHOW WARNINGS;

+---------+------+----------------------------------------------+
| Level   | Code | Message                                      |
+---------+------+----------------------------------------------+
| Warning | 1105 | skip plan-cache: '1' may be converted to INT |
+---------+------+----------------------------------------------+
1 row in set (0.00 sec)
```

### 使用 `Statements Summary` 进行诊断

`Statements Summary` 表中包含两个字段，`plan_cache_unqualified` 和 `plan_cache_unqualified_last_reason`，分别表示对应查询无法使用计划缓存的次数和原因。你可以利用这两个字段进行诊断：

```sql
mysql> SELECT digest_text, plan_cache_unqualified, plan_cache_unqualified_last_reason FROM information_schema.statements_summary WHERE plan_cache_unqualified > 0 ORDER BY plan_cache_unqualified DESC
LIMIT 10;

+---------------------------------+------------------------+----------------------------------------+
| digest_text                     | plan_cache_unqualified | plan_cache_unqualified_last_reason     |
+---------------------------------+------------------------+----------------------------------------+
| select * from `t` where `a` < ? |                     10 | '1' may be converted to INT            |
| select * from `t` order by ?    |                      4 | query has 'order by ?' is un-cacheable |
| select database ( ) from `t`    |                      2 | query has 'database()' is un-cacheable |
...
+---------------------------------+------------------------+----------------------------------------+
10 row in set (0.01 sec)
```

## 内存管理：预处理计划缓存

<CustomContent platform="tidb">

使用预处理计划缓存会带来内存开销。你可以在 Grafana 的 [**Plan Cache Memory Usage**](/grafana-tidb-dashboard.md) 监控面板中查看所有会话在每个 TiDB 实例中缓存的执行计划总内存消耗。

> **Note:**
>
> 由于 Golang 的内存回收机制和一些未统计的内存结构，Grafana 中显示的内存并不等于实际堆内存使用。经过测试，Grafana 显示的内存与实际堆内存的偏差约为 ±20%。

你可以在 Grafana 中使用 [**Plan Cache Plan Num**](/grafana-tidb-dashboard.md) 面板查看每个 TiDB 实例中缓存的执行计划总数。

以下为 Grafana 中 **Plan Cache Memory Usage** 和 **Plan Cache Plan Num** 面板的示例：

![grafana_panels](/media/planCache-memoryUsage-planNum-panels.png)

从 v7.1.0 版本开始，你可以通过配置系统变量 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710) 来控制每个会话中最大缓存计划数。不同环境建议值如下，可根据监控面板调整：


</CustomContent>

<CustomContent platform="tidb-cloud">

使用预处理计划缓存会带来一些内存开销。在内部测试中，每个缓存计划平均消耗 100 KiB 内存。由于计划缓存目前处于 `SESSION` 级别，总内存消耗大约为 `会话数 * 每个会话的平均缓存计划数 * 100 KiB`。

例如，当前 TiDB 实例有 50 个会话并发，每个会话大约有 100 个缓存计划，总内存消耗大约为 `50 * 100 * 100 KiB` = `512 MB`。

你可以通过配置系统变量 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710) 来控制每个会话中最大缓存计划数。不同环境建议值如下：

</CustomContent>

- 当 TiDB 服务器实例的内存阈值 <= 64 GiB 时，设置 `tidb_session_plan_cache_size` 为 `50`。
- 当 TiDB 服务器实例的内存阈值 > 64 GiB 时，设置 `tidb_session_plan_cache_size` 为 `100`。

从 v7.1.0 版本开始，你可以通过配置系统变量 [`tidb_plan_cache_max_plan_size`](/system-variables.md#tidb_plan_cache_max_plan_size-new-in-v710) 来控制可缓存计划的最大大小。默认值为 2 MB。如果计划大小超过此值，则不会缓存。

当 TiDB 服务器的未使用内存低于某个阈值时，会触发计划缓存的内存保护机制，从而驱逐部分缓存计划。

你可以通过配置系统变量 `tidb_prepared_plan_cache_memory_guard_ratio` 来控制阈值。默认值为 0.1，意味着当 TiDB 服务器的未用内存少于总内存的 10%（即使用了 90% 内存）时，触发内存保护机制。

<CustomContent platform="tidb">

由于内存限制，计划缓存可能会有未命中的情况。你可以在 Grafana 的 [`Plan Cache Miss OPS`](/grafana-tidb-dashboard.md) 指标中查看状态。

</CustomContent>

<CustomContent platform="tidb-cloud">

由于内存限制，计划缓存可能会有未命中的情况。

</CustomContent>

## 清除执行计划缓存

你可以通过执行 `ADMIN FLUSH [SESSION | INSTANCE] PLAN_CACHE` 语句清除执行计划缓存。

在此语句中，`[SESSION | INSTANCE]` 指定是清除当前会话还是整个 TiDB 实例的计划缓存。如果未指定范围，默认作用于 `SESSION` 缓存。

以下为清除 `SESSION` 执行计划缓存的示例：


```sql
MySQL [test]> create table t (a int);
Query OK, 0 rows affected (0.00 sec)

MySQL [test]> prepare stmt from 'select * from t';
Query OK, 0 rows affected (0.00 sec)

MySQL [test]> execute stmt;
Empty set (0.00 sec)

MySQL [test]> execute stmt;
Empty set (0.00 sec)

MySQL [test]> select @@last_plan_from_cache; -- 选择缓存的计划
+------------------------+
| @@last_plan_from_cache |
+------------------------+
|                      1 |
+------------------------+
1 row in set (0.00 sec)

MySQL [test]> admin flush session plan_cache; -- 清除当前会话的缓存计划
Query OK, 0 rows affected (0.00 sec)

MySQL [test]> execute stmt;
Empty set (0.00 sec)

MySQL [test]> select @@last_plan_from_cache; -- 缓存的计划已被清除，无法再次选择
+------------------------+
| @@last_plan_from_cache |
+------------------------+
|                      0 |
+------------------------+
1 row in set (0.00 sec)
```

目前，TiDB 不支持清除 `GLOBAL` 执行计划缓存。这意味着你不能清除整个 TiDB 集群的缓存计划。如果尝试清除 `GLOBAL` 执行计划缓存，会报错：


```sql
MySQL [test]> admin flush global plan_cache;
ERROR 1105 (HY000): Do not support the 'admin flush global scope.'
```

## 忽略 `COM_STMT_CLOSE` 命令和 `DEALLOCATE PREPARE` 语句

为了减少 SQL 语句的语法解析成本，建议你只运行一次 `prepare stmt`，然后多次运行 `execute stmt`，最后再运行 `deallocate prepare`：


```sql
MySQL [test]> prepare stmt from '...'; -- 只准备一次
MySQL [test]> execute stmt using ...;  -- 只执行一次
MySQL [test]> ...
MySQL [test]> execute stmt using ...;  -- 多次执行
MySQL [test]> deallocate prepare stmt; -- 释放预处理语句
```

在实际操作中，你可能习惯在每次运行 `execute stmt` 后都执行 `deallocate prepare`，如下所示：


```sql
MySQL [test]> prepare stmt from '...'; -- 只准备一次
MySQL [test]> execute stmt using ...;
MySQL [test]> deallocate prepare stmt; -- 执行后释放
MySQL [test]> prepare stmt from '...'; -- 预处理两次
MySQL [test]> execute stmt using ...;
MySQL [test]> deallocate prepare stmt; -- 释放预处理语句
```

在这种做法中，第一次执行获得的执行计划不能被第二次执行所复用。

为解决此问题，你可以将系统变量 [`tidb_ignore_prepared_cache_close_stmt`](/system-variables.md#tidb_ignore_prepared_cache_close_stmt-new-in-v600) 设置为 `ON`，让 TiDB 忽略关闭 `prepare stmt` 的命令：


```sql
mysql> set @@tidb_ignore_prepared_cache_close_stmt=1;  -- 开启变量
Query OK, 0 rows affected (0.00 sec)

mysql> prepare stmt from 'select * from t'; -- 只准备一次
Query OK, 0 rows affected (0.00 sec)

mysql> execute stmt;                        -- 只执行一次
Empty set (0.00 sec)

mysql> deallocate prepare stmt;             -- 第一次执行后释放
Query OK, 0 rows affected (0.00 sec)

mysql> prepare stmt from 'select * from t'; -- 预处理两次
Query OK, 0 rows affected (0.00 sec)

mysql> execute stmt;                        -- 预处理两次
Empty set (0.00 sec)

mysql> select @@last_plan_from_cache;       -- 复用上次的计划
+------------------------+
| @@last_plan_from_cache |
+------------------------+
|                      1 |
+------------------------+
1 row in set (0.00 sec)
```

### 监控

<CustomContent platform="tidb">

在 [TiDB 页面中的 Grafana 仪表盘](/grafana-tidb-dashboard.md) 的 **Executor** 部分，有 “Queries Using Plan Cache OPS” 和 “Plan Cache Miss OPS” 图表。这些图表可以用来检查 TiDB 和应用是否正确配置，以确保 SQL 计划缓存正常工作。同一页面的 **Server** 部分提供了 “Prepared Statement Count” 图表。如果应用使用了预处理语句，该图表会显示非零值，这是 SQL 计划缓存正常工作的前提。

![`sql_plan_cache`](/media/performance/sql_plan_cache.png)

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [**Monitoring**](/tidb-cloud/built-in-monitoring.md) 页面中，可以查看 `Queries Using Plan Cache OPS` 指标，以获取所有 TiDB 实例中每秒使用或未命中计划缓存的查询数。

</CustomContent>