---
title: SQL 执行计划管理（SPM）
summary: 了解 TiDB 中的 SQL 执行计划管理。
---

# SQL 执行计划管理（SPM） {#sql-plan-management-spm}

SQL 执行计划管理是一组通过执行 SQL 绑定手动干预 SQL 执行计划的功能。这些功能包括 SQL 绑定、基线捕获和基线演化。

## SQL 绑定 {#sql-binding}

SQL 绑定是 SPM 的基础。[优化器 Hint](/optimizer-hints.md) 文档介绍了如何通过 Hint 选择特定的执行计划。然而，有时你需要在不修改 SQL 语句的情况下干预执行计划的选择。通过 SQL 绑定，你可以在不修改 SQL 语句的情况下选择指定的执行计划。

<CustomContent platform="tidb">

> **Note:**
>
> 要使用 SQL 绑定，你需要拥有 `SUPER` 权限。如果 TiDB 提示你权限不足，请参见 [权限管理](/privilege-management.md) 添加所需权限。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 要使用 SQL 绑定，你需要拥有 `SUPER` 权限。如果 TiDB 提示你权限不足，请参见 [权限管理](https://docs.pingcap.com/tidb/stable/privilege-management) 添加所需权限。

</CustomContent>

### 创建绑定 {#create-a-binding}

你可以根据 SQL 语句或历史执行计划为 SQL 语句创建绑定。

#### 根据 SQL 语句创建绑定 {#create-a-binding-according-to-a-sql-statement}

```sql
CREATE [GLOBAL | SESSION] BINDING [FOR BindableStmt] USING BindableStmt;
```

该语句可在 GLOBAL 或 SESSION 级别绑定 SQL 执行计划。目前，TiDB 支持的可绑定 SQL 语句（BindableStmt）包括 `SELECT`、`DELETE`、`UPDATE` 以及带有 `SELECT` 子查询的 `INSERT` / `REPLACE`。以下是示例：

```sql
CREATE GLOBAL BINDING USING SELECT /*+ use_index(orders, orders_book_id_idx) */ * FROM orders;
CREATE GLOBAL BINDING FOR SELECT * FROM orders USING SELECT /*+ use_index(orders, orders_book_id_idx) */ * FROM orders;
```

> **Note:**
>
> 绑定的优先级高于手动添加的 Hint。因此，当你执行包含 Hint 的语句且存在对应绑定时，控制优化器行为的 Hint 不会生效。但其他类型的 Hint 仍然有效。

具体来说，有两类语句由于语法冲突无法绑定执行计划，创建绑定时会报语法错误。示例如下：

```sql
-- 第一类：使用 `JOIN` 关键字但未通过 `USING` 关键字指定关联列的笛卡尔积语句。
CREATE GLOBAL BINDING for
    SELECT * FROM orders o1 JOIN orders o2
USING
    SELECT * FROM orders o1 JOIN orders o2;

-- 第二类：包含 `USING` 关键字的 `DELETE` 语句。
CREATE GLOBAL BINDING for
    DELETE FROM users USING users JOIN orders ON users.id = orders.user_id
USING
    DELETE FROM users USING users JOIN orders ON users.id = orders.user_id;
```

你可以通过等价语句绕过语法冲突。例如，可以按如下方式重写上述语句：

```sql
-- 第一类语句重写：删除 `JOIN` 关键字，改用逗号分隔。
CREATE GLOBAL BINDING for
    SELECT * FROM orders o1, orders o2
USING
    SELECT * FROM orders o1, orders o2;

-- 第二类语句重写：去除 `DELETE` 语句中的 `USING` 关键字。
CREATE GLOBAL BINDING for
    DELETE users FROM users JOIN orders ON users.id = orders.user_id
USING
    DELETE users FROM users JOIN orders ON users.id = orders.user_id;
```

> **Note:**
>
> 当为带有 `SELECT` 子查询的 `INSERT` / `REPLACE` 语句创建执行计划绑定时，需要在 `SELECT` 子查询中指定要绑定的优化器 Hint，而不是在 `INSERT` / `REPLACE` 关键字后指定。否则，优化器 Hint 不会按预期生效。

以下是两个示例：

```sql
-- Hint 在以下语句中生效。
CREATE GLOBAL BINDING for
    INSERT INTO orders SELECT * FROM pre_orders WHERE status = 'VALID' AND created <= (NOW() - INTERVAL 1 HOUR)
USING
    INSERT INTO orders SELECT /*+ use_index(@sel_1 pre_orders, idx_created) */ * FROM pre_orders WHERE status = 'VALID' AND created <= (NOW() - INTERVAL 1 HOUR);

-- Hint 在以下语句中无法生效。
CREATE GLOBAL BINDING for
    INSERT INTO orders SELECT * FROM pre_orders WHERE status = 'VALID' AND created <= (NOW() - INTERVAL 1 HOUR)
USING
    INSERT /*+ use_index(@sel_1 pre_orders, idx_created) */ INTO orders SELECT * FROM pre_orders WHERE status = 'VALID' AND created <= (NOW() - INTERVAL 1 HOUR);
```

如果在创建执行计划绑定时未指定作用域，则默认作用域为 SESSION。TiDB 优化器会对绑定的 SQL 语句进行标准化处理，并存储在系统表中。在处理 SQL 查询时，如果标准化后的语句与系统表中的某个绑定 SQL 语句匹配，且系统变量 `tidb_use_plan_baselines` 设置为 `on`（默认值为 `on`），TiDB 会为该语句使用对应的优化器 Hint。如果存在多个可匹配的执行计划，优化器会选择代价最低的一个进行绑定。

`标准化` 是指将 SQL 语句中的常量转换为变量参数，并为查询中引用的表显式指定数据库名，同时对 SQL 语句中的空格和换行进行规范化处理。示例如下：

```sql
SELECT * FROM users WHERE balance >    100
-- 标准化后，上述语句如下：
SELECT * FROM bookshop . users WHERE balance > ?
```

> **Note:**
>
> 在标准化过程中，`IN` 谓词中的 `?` 会被标准化为 `...`。
>
> 例如：
>
> ```sql
> SELECT * FROM books WHERE type IN ('Novel')
> SELECT * FROM books WHERE type IN ('Novel','Life','Education')
> -- 标准化后，上述语句如下：
> SELECT * FROM bookshop . books WHERE type IN ( ... )
> SELECT * FROM bookshop . books WHERE type IN ( ... )
> ```
>
> 标准化后，不同长度的 `IN` 谓词会被识别为同一条语句，因此只需为这些谓词创建一个绑定即可。
>
> 例如：
>
> ```sql
> CREATE TABLE t (a INT, KEY(a));
> CREATE BINDING FOR SELECT * FROM t WHERE a IN (?) USING SELECT /*+ use_index(t, idx_a) */ * FROM t WHERE a in (?);
>
> SELECT * FROM t WHERE a IN (1);
> SELECT @@LAST_PLAN_FROM_BINDING;
> +--------------------------+
> | @@LAST_PLAN_FROM_BINDING |
> +--------------------------+
> |                        1 |
> +--------------------------+
>
> SELECT * FROM t WHERE a IN (1, 2, 3);
> SELECT @@LAST_PLAN_FROM_BINDING;
> +--------------------------+
> | @@LAST_PLAN_FROM_BINDING |
> +--------------------------+
> |                        1 |
> +--------------------------+
> ```
>
> 在 TiDB v7.4.0 之前创建的绑定可能包含 `IN (?)`。升级到 v7.4.0 或更高版本后，这些绑定会被修改为 `IN (...)`。
>
> 例如：
>
> ```sql
> -- 在 v7.3.0 上创建绑定
> mysql> CREATE GLOBAL BINDING FOR SELECT * FROM t WHERE a IN (1) USING SELECT /*+ use_index(t, idx_a) */ * FROM t WHERE a IN (1);
> mysql> SHOW GLOBAL BINDINGS;
> +-----------------------------------------------+------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
> | Original_sql                                  | Bind_sql                                                               | Default_db | Status  | Create_time             | Update_time             | Charset | Collation          | Source | Sql_digest                                                       | Plan_digest |
> +-----------------------------------------------+------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
> | select * from `test` . `t` where `a` in ( ? ) | SELECT /*+ use_index(`t` `idx_a`)*/ * FROM `test`.`t` WHERE `a` IN (1) | test       | enabled | 2024-09-03 15:39:02.695 | 2024-09-03 15:39:02.695 | utf8mb4 | utf8mb4_general_ci | manual | 8b9c4e6ab8fad5ba29b034311dcbfc8a8ce57dde2e2d5d5b65313b90ebcdebf7 |             |
> +-----------------------------------------------+------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
>
> -- 升级到 v7.4.0 或更高版本后
> mysql> SHOW GLOBAL BINDINGS;
> +-------------------------------------------------+------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
> | Original_sql                                    | Bind_sql                                                               | Default_db | Status  | Create_time             | Update_time             | Charset | Collation          | Source | Sql_digest                                                       | Plan_digest |
> +-------------------------------------------------+------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
> | select * from `test` . `t` where `a` in ( ... ) | SELECT /*+ use_index(`t` `idx_a`)*/ * FROM `test`.`t` WHERE `a` IN (1) | test       | enabled | 2024-09-03 15:35:59.861 | 2024-09-03 15:35:59.861 | utf8mb4 | utf8mb4_general_ci | manual | da38bf216db4a53e1a1e01c79ffa42306419442ad7238480bb7ac510723c8bdf |             |
> +-------------------------------------------------+------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
> ```

当某条 SQL 语句在 GLOBAL 和 SESSION 作用域下都存在绑定执行计划时，优化器在遇到 SESSION 绑定时会忽略 GLOBAL 作用域下的绑定执行计划，因此 SESSION 作用域下的绑定会屏蔽 GLOBAL 作用域下的绑定。

例如：

```sql
-- 创建 GLOBAL 绑定，并指定在该绑定中使用 `sort merge join`。
CREATE GLOBAL BINDING for
    SELECT * FROM t1, t2 WHERE t1.id = t2.id
USING
    SELECT /*+ merge_join(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;

-- 该 SQL 语句的执行计划使用 GLOBAL 绑定中指定的 `sort merge join`。
explain SELECT * FROM t1, t2 WHERE t1.id = t2.id;

-- 创建另一个 SESSION 绑定，并指定在该绑定中使用 `hash join`。
CREATE BINDING for
    SELECT * FROM t1, t2 WHERE t1.id = t2.id
USING
    SELECT /*+ hash_join(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;

-- 该语句的执行计划使用 SESSION 绑定中指定的 `hash join`，而不是 GLOBAL 绑定中指定的 `sort merge join`。
explain SELECT * FROM t1, t2 WHERE t1.id = t2.id;
```

当第一次执行 `SELECT` 语句时，优化器通过 GLOBAL 作用域下的绑定为语句添加 `sm_join(t1, t2)` Hint，`explain` 结果中的执行计划顶层节点为 MergeJoin。当第二次执行 `SELECT` 语句时，优化器使用 SESSION 作用域下的绑定而不是 GLOBAL 作用域下的绑定，为语句添加 `hash_join(t1, t2)` Hint，`explain` 结果中的执行计划顶层节点为 HashJoin。

每个标准化 SQL 语句同一时刻只能有一个通过 `CREATE BINDING` 创建的绑定。当为同一标准化 SQL 语句创建多个绑定时，最后创建的绑定会被保留，之前所有的绑定（包括手动创建和演化的）都会被标记为已删除。但 session 绑定和 global 绑定可以共存，不受此逻辑影响。

此外，创建绑定时，TiDB 要求 session 处于数据库上下文中，即客户端连接时已指定数据库或已执行 `use ${database}`。

原始 SQL 语句和绑定语句在标准化和去除 Hint 后的文本必须一致，否则绑定会失败。示例如下：

-   该绑定可以成功创建，因为参数化和去除 Hint 后的文本一致：`SELECT * FROM test . t WHERE a > ?`

    ```sql
    CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index  (idx) WHERE a > 2
    ```

-   该绑定会失败，因为原始 SQL 语句处理后为 `SELECT * FROM test . t WHERE a > ?`，而绑定 SQL 语句处理后为 `SELECT * FROM test . t WHERE b > ?`。

    ```sql
    CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index(idx) WHERE b > 2
    ```

> **Note:**
>
> 对于 `PREPARE` / `EXECUTE` 语句以及通过二进制协议执行的查询，需要为实际的查询语句创建执行计划绑定，而不是为 `PREPARE` / `EXECUTE` 语句创建绑定。

#### 根据历史执行计划创建绑定 {#create-a-binding-according-to-a-historical-execution-plan}

如果你希望将 SQL 语句的执行计划固定为历史执行计划，可以通过 Plan Digest 将该历史执行计划绑定到 SQL 语句上，这比根据 SQL 语句绑定更为便捷。此外，你还可以一次性为多条 SQL 语句绑定执行计划。更多细节和示例，参见 [`CREATE [GLOBAL|SESSION] BINDING`](/sql-statements/sql-statement-create-binding.md)。

使用该功能时需注意：

-   该功能会根据历史执行计划生成 Hint，并用生成的 Hint 进行绑定。由于历史执行计划存储在 [语句概要表](/statement-summary-tables.md) 中，使用该功能前需先开启 [`tidb_enable_stmt_summary`](/system-variables.md#tidb_enable_stmt_summary-new-in-v304) 系统变量。
-   对于 TiFlash 查询、三表及以上的 Join 查询、包含子查询的查询，自动生成的 Hint 不够充分，可能导致计划未被完全绑定。此时创建绑定会有告警。
-   如果历史执行计划对应的 SQL 语句带有 Hint，则 Hint 会被添加到绑定中。例如，执行 `SELECT /*+ max_execution_time(1000) */ * FROM t` 后，使用其 Plan Digest 创建的绑定会包含 `max_execution_time(1000)`。

该绑定方式的 SQL 语句如下：

```sql
CREATE [GLOBAL | SESSION] BINDING FROM HISTORY USING PLAN DIGEST StringLiteralOrUserVariableList;
```

上述语句通过 Plan Digest 将执行计划绑定到 SQL 语句。默认作用域为 SESSION。所创建绑定的适用 SQL 语句、优先级、作用域和生效条件与[根据 SQL 语句创建的绑定](#create-a-binding-according-to-a-sql-statement)一致。

使用该绑定方式时，需先在 `statements_summary` 中获取目标历史执行计划对应的 Plan Digest，然后通过 Plan Digest 创建绑定。具体步骤如下：

1.  在 `statements_summary` 中获取目标执行计划对应的 Plan Digest。

    例如：

    ```sql
    CREATE TABLE t(id INT PRIMARY KEY , a INT, KEY idx_a(a));
    SELECT /*+ IGNORE_INDEX(t, idx_a) */ * FROM t WHERE a = 1;
    SELECT * FROM INFORMATION_SCHEMA.STATEMENTS_SUMMARY WHERE QUERY_SAMPLE_TEXT = 'SELECT /*+ IGNORE_INDEX(t, idx_a) */ * FROM t WHERE a = 1'\G
    ```

    以下为 `statements_summary` 查询结果的部分示例：

        SUMMARY_BEGIN_TIME: 2022-12-01 19:00:00
        ...........
              DIGEST_TEXT: select * from `t` where `a` = ?
        ...........
              PLAN_DIGEST: 4e3159169cc63c14b139a4e7d72eae1759875c9a9581f94bb2079aae961189cb
                     PLAN:  id                  task        estRows operator info                           actRows execution info                                                                                                                                             memory      disk
                            TableReader_7       root        10      data:Selection_6                        0       time:4.05ms, loops:1, cop_task: {num: 1, max: 598.6µs, proc_keys: 0, rpc_num: 2, rpc_time: 609.8µs, copr_cache_hit_ratio: 0.00, distsql_concurrency: 15}   176 Bytes   N/A
                            └─Selection_6       cop[tikv]   10      eq(test.t.a, 1)                         0       tikv_task:{time:560.8µs, loops:0}                                                                                                                          N/A         N/A
                              └─TableFullScan_5 cop[tikv]   10000   table:t, keep order:false, stats:pseudo 0       tikv_task:{time:560.8µs, loops:0}                                                                                                                          N/A         N/A
              BINARY_PLAN: 6QOYCuQDCg1UYWJsZVJlYWRlcl83Ev8BCgtTZWxlY3Rpb25fNhKOAQoPBSJQRnVsbFNjYW5fNSEBAAAAOA0/QSkAAQHwW4jDQDgCQAJKCwoJCgR0ZXN0EgF0Uh5rZWVwIG9yZGVyOmZhbHNlLCBzdGF0czpwc2V1ZG9qInRpa3ZfdGFzazp7dGltZTo1NjAuOMK1cywgbG9vcHM6MH1w////CQMEAXgJCBD///8BIQFzCDhVQw19BAAkBX0QUg9lcSgBfCAudC5hLCAxKWrmYQAYHOi0gc6hBB1hJAFAAVIQZGF0YTo9GgRaFAW4HDQuMDVtcywgCbYcMWKEAWNvcF8F2agge251bTogMSwgbWF4OiA1OTguNsK1cywgcHJvY19rZXlzOiAwLCBycGNfBSkAMgkMBVcQIDYwOS4pEPBDY29wcl9jYWNoZV9oaXRfcmF0aW86IDAuMDAsIGRpc3RzcWxfY29uY3VycmVuY3k6IDE1fXCwAXj///////////8BGAE=

    在本例中，可以看到对应执行计划的 Plan Digest 为 `4e3159169cc63c14b139a4e7d72eae1759875c9a9581f94bb2079aae961189cb`。

2.  使用 Plan Digest 创建绑定：

    ```sql
    CREATE BINDING FROM HISTORY USING PLAN DIGEST '4e3159169cc63c14b139a4e7d72eae1759875c9a9581f94bb2079aae961189cb';
    ```

要验证创建的绑定是否生效，可以[查看绑定](#view-bindings)：

```sql
SHOW BINDINGS\G
```

    *************************** 1. row ***************************
    Original_sql: select * from `test` . `t` where `a` = ?
        Bind_sql: SELECT /*+ use_index(@`sel_1` `test`.`t` ) ignore_index(`t` `idx_a`)*/ * FROM `test`.`t` WHERE `a` = 1
           ...........
      Sql_digest: 6909a1bbce5f64ade0a532d7058dd77b6ad5d5068aee22a531304280de48349f
     Plan_digest:
    1 row in set (0.01 sec)

    ERROR:
    No query specified

```sql
SELECT * FROM t WHERE a = 1;
SELECT @@LAST_PLAN_FROM_BINDING;
```

    +--------------------------+
    | @@LAST_PLAN_FROM_BINDING |
    +--------------------------+
    |                        1 |
    +--------------------------+
    1 row in set (0.00 sec)

### 移除绑定 {#remove-a-binding}

你可以根据 SQL 语句或 SQL Digest 移除绑定。

#### 根据 SQL 语句移除绑定 {#remove-a-binding-according-to-a-sql-statement}

```sql
DROP [GLOBAL | SESSION] BINDING FOR BindableStmt;
```

该语句可在 GLOBAL 或 SESSION 级别移除指定的执行计划绑定。默认作用域为 SESSION。

一般来说，SESSION 作用域下的绑定主要用于测试或特殊场景。若希望绑定在所有 TiDB 实例中生效，需要使用 GLOBAL 绑定。已创建的 SESSION 绑定会屏蔽对应的 GLOBAL 绑定，直到 SESSION 结束，即使在 SESSION 关闭前已删除 SESSION 绑定。在这种情况下，所有绑定都不生效，计划由优化器选择。

以下示例基于[创建绑定](#create-a-binding)中的例子，SESSION 绑定屏蔽了 GLOBAL 绑定：

```sql
-- 删除 SESSION 作用域下创建的绑定。
drop session binding for SELECT * FROM t1, t2 WHERE t1.id = t2.id;

-- 再次查看 SQL 执行计划。
explain SELECT * FROM t1,t2 WHERE t1.id = t2.id;
```

在上述示例中，SESSION 作用域下被删除的绑定屏蔽了 GLOBAL 作用域下的对应绑定。优化器不会为语句添加 `sm_join(t1, t2)` Hint，`explain` 结果中的执行计划顶层节点不会被该 Hint 固定为 MergeJoin，而是由优化器根据代价估算独立选择。

#### 根据 SQL Digest 移除绑定 {#remove-a-binding-according-to-sql-digest}

除了根据 SQL 语句移除绑定外，还可以根据 SQL Digest 移除绑定。更多细节和示例，参见 [`DROP [GLOBAL|SESSION] BINDING`](/sql-statements/sql-statement-drop-binding.md)。

```sql
DROP [GLOBAL | SESSION] BINDING FOR SQL DIGEST StringLiteralOrUserVariableList;
```

该语句可在 GLOBAL 或 SESSION 级别移除对应 SQL Digest 的执行计划绑定。默认作用域为 SESSION。你可以通过[查看绑定](#view-bindings)获取 SQL Digest。

> **Note:**
>
> 执行 `DROP GLOBAL BINDING` 会删除当前 tidb-server 实例缓存中的绑定，并将系统表中对应行的状态改为 'deleted'。该语句不会直接删除系统表中的记录，因为其他 tidb-server 实例需要读取 'deleted' 状态以删除各自缓存中的对应绑定。对于这些系统表中状态为 'deleted' 的记录，每 100 个 `bind-info-lease`（默认值为 `3s`，共 `300s`）间隔，后台线程会触发回收和清理操作，清理 `update_time` 早于 10 个 `bind-info-lease` 的绑定（以确保所有 tidb-server 实例都已读取 'deleted' 状态并更新缓存）。

### 修改绑定状态 {#change-binding-status}

#### 根据 SQL 语句修改绑定状态 {#change-binding-status-according-to-a-sql-statement}

```sql
SET BINDING [ENABLED | DISABLED] FOR BindableStmt;
```

你可以通过该语句修改绑定的状态。默认状态为 ENABLED。生效作用域默认为 GLOBAL，且不可修改。

执行该语句时，只能将绑定状态从 `Disabled` 改为 `Enabled`，或从 `Enabled` 改为 `Disabled`。如果没有可供状态变更的绑定，会返回警告信息：`There are no bindings can be set the status. Please check the SQL text`。注意，处于 `Disabled` 状态的绑定不会被任何查询使用。

#### 根据 <code>sql_digest</code> 修改绑定状态 {#change-binding-status-according-to-code-sql-digest-code}

除了根据 SQL 语句修改绑定状态外，还可以根据 `sql_digest` 修改绑定状态：

```sql
SET BINDING [ENABLED | DISABLED] FOR SQL DIGEST 'sql_digest';
```

通过 `sql_digest` 可变更的绑定状态及其效果与[根据 SQL 语句修改绑定状态](#change-binding-status-according-to-a-sql-statement)一致。如果没有可供状态变更的绑定，会返回警告信息 `can't find any binding for 'sql_digest'`。

### 查看绑定 {#view-bindings}

```sql
SHOW [GLOBAL | SESSION] BINDINGS [ShowLikeOrWhere]
```

该语句按绑定更新时间从新到旧输出 GLOBAL 或 SESSION 级别的执行计划绑定。默认作用域为 SESSION。目前 `SHOW BINDINGS` 输出 11 列，如下所示：

| Column Name  | Note                                                                                                                                                                                                                                                     |
| :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| original_sql | 参数化后的原始 SQL 语句                                                                                                                                                                                                                                 |
| bind_sql     | 带有 Hint 的绑定 SQL 语句                                                                                                                                                                                                                               |
| default_db   | 默认数据库                                                                                                                                                                                                                                               |
| status       | 状态，包括 `enabled`（自 v6.0 起替代 `using` 状态）、`disabled`、`deleted`、`invalid`、`rejected` 和 `pending verify`                                                                                             |
| create_time  | 创建时间                                                                                                                                                                                                                                                 |
| update_time  | 更新时间                                                                                                                                                                                                                                                 |
| charset      | 字符集                                                                                                                                                                                                                                                   |
| collation    | 排序规则                                                                                                                                                                                                                                                |
| source       | 绑定的创建方式，包括 `manual`（根据 SQL 语句创建）、`history`（根据历史执行计划创建）、`capture`（TiDB 自动捕获）、`evolve`（TiDB 自动演化）                                                                      |
| sql_digest   | 标准化 SQL 语句的摘要                                                                                                                                                                                                                                   |
| plan_digest  | 执行计划的摘要                                                                                                                                                                                                                                           |

### 绑定排查 {#troubleshoot-a-binding}

你可以通过以下任一方式排查绑定：

-   使用系统变量 [`last_plan_from_binding`](/system-variables.md#last_plan_from_binding-new-in-v40) 显示上次执行语句所用的执行计划是否来自绑定。

    ```sql
    -- 创建全局绑定
    CREATE GLOBAL BINDING for
        SELECT * FROM t
    USING
        SELECT /*+ USE_INDEX(t, idx_a) */ * FROM t;

    SELECT * FROM t;
    SELECT @@[SESSION.]last_plan_from_binding;
    ```

    ```sql
    +--------------------------+
    | @@last_plan_from_binding |
    +--------------------------+
    |                        1 |
    +--------------------------+
    1 row in set (0.00 sec)
    ```

-   使用 `explain format = 'verbose'` 语句查看 SQL 语句的查询计划。如果 SQL 语句使用了绑定，可以通过 `show warnings` 查看该 SQL 语句使用了哪个绑定。

    ```sql
    -- 创建全局绑定

    CREATE GLOBAL BINDING for
        SELECT * FROM t
    USING
        SELECT /*+ USE_INDEX(t, idx_a) */ * FROM t;

    -- 使用 explain format = 'verbose' 查看 SQL 语句的执行计划

    explain format = 'verbose' SELECT * FROM t;

    -- 通过 `show warnings` 查看查询中使用的绑定。

    show warnings;
    ```

    ```sql
    +-------+------+--------------------------------------------------------------------------+
    | Level | Code | Message                                                                  |
    +-------+------+--------------------------------------------------------------------------+
    | Note  | 1105 | Using the bindSQL: SELECT /*+ USE_INDEX(`t` `idx_a`)*/ * FROM `test`.`t` |
    +-------+------+--------------------------------------------------------------------------+
    1 row in set (0.01 sec)

    ```

### 绑定缓存 {#cache-bindings}

每个 TiDB 实例都有一个最近最少使用（LRU）的绑定缓存。缓存容量由系统变量 [`tidb_mem_quota_binding_cache`](/system-variables.md#tidb_mem_quota_binding_cache-new-in-v600) 控制。你可以查看 TiDB 实例中缓存的绑定。

要查看绑定的缓存状态，可执行 `SHOW binding_cache status` 语句。该语句的生效作用域默认为 GLOBAL，且不可修改。该语句返回缓存中可用绑定数、系统中可用绑定总数、所有缓存绑定的内存使用量以及缓存的总内存。

```sql

SHOW binding_cache status;
```

```sql
+-------------------+-------------------+--------------+--------------+
| bindings_in_cache | bindings_in_table | memory_usage | memory_quota |
+-------------------+-------------------+--------------+--------------+
|                 1 |                 1 | 159 Bytes    | 64 MB        |
+-------------------+-------------------+--------------+--------------+
1 row in set (0.00 sec)
```

## 利用语句概要表获取需要绑定的查询 {#utilize-the-statement-summary-table-to-obtain-queries-that-need-to-be-bound}

[语句概要](/statement-summary-tables.md) 记录了最近的 SQL 执行信息，如延迟、执行次数及对应的查询计划。你可以通过查询语句概要表获取合格的 `plan_digest`，然后[根据这些历史执行计划创建绑定](/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan)。

以下示例查询过去两周内执行次数超过 10 次、且存在多个执行计划但未绑定 SQL 的 `SELECT` 语句。它按执行次数排序，并将前 100 条查询绑定到其最快的计划。

```sql
WITH stmts AS (                                                -- 获取所有信息
  SELECT * FROM INFORMATION_SCHEMA.CLUSTER_STATEMENTS_SUMMARY
  UNION ALL
  SELECT * FROM INFORMATION_SCHEMA.CLUSTER_STATEMENTS_SUMMARY_HISTORY
),
best_plans AS (
  SELECT plan_digest, `digest`, avg_latency,
  CONCAT('create global binding from history using plan digest "', plan_digest, '"') as binding_stmt
  FROM stmts t1
  WHERE avg_latency = (SELECT min(avg_latency) FROM stmts t2   -- 查询延迟最低的计划
                       WHERE t2.`digest` = t1.`digest`)
)

SELECT any_value(digest_text) as query,
       SUM(exec_count) as exec_count,
       plan_hint, binding_stmt
FROM stmts, best_plans
WHERE stmts.`digest` = best_plans.`digest`
  AND summary_begin_time > DATE_SUB(NOW(), interval 14 day)    -- 过去两周内执行过
  AND stmt_type = 'Select'                                     -- 只考虑 select 语句
  AND schema_name NOT IN ('INFORMATION_SCHEMA', 'mysql')       -- 非内部查询
  AND plan_in_binding = 0                                      -- 尚未绑定
GROUP BY stmts.`digest`
  HAVING COUNT(DISTINCT(stmts.plan_digest)) > 1                -- 该查询不稳定，有多个计划
         AND SUM(exec_count) > 10                              -- 高频，执行次数超过 10 次
ORDER BY SUM(exec_count) DESC LIMIT 100;                       -- 前 100 条高频查询
```

通过设置一定的过滤条件获取符合要求的查询后，可以直接执行对应 `binding_stmt` 列中的语句来创建绑定。

    +---------------------------------------------+------------+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+
    | query                                       | exec_count | plan_hint                                                                   | binding_stmt                                                                                                            |
    +---------------------------------------------+------------+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+
    | select * from `t` where `a` = ? and `b` = ? |        401 | use_index(@`sel_1` `test`.`t` `a`), no_order_index(@`sel_1` `test`.`t` `a`) | create global binding from history using plan digest "0d6e97fb1191bbd08dddefa7bd007ec0c422b1416b152662768f43e64a9958a6" |
    | select * from `t` where `b` = ? and `c` = ? |        104 | use_index(@`sel_1` `test`.`t` `b`), no_order_index(@`sel_1` `test`.`t` `b`) | create global binding from history using plan digest "80c2aa0aa7e6d3205755823aa8c6165092c8521fb74c06a9204b8d35fc037dd9" |
    +---------------------------------------------+------------+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+

## 跨库绑定 {#cross-database-binding}

自 v7.6.0 起，你可以在 TiDB 中通过在绑定创建语法中使用通配符 `*` 表示数据库名来创建跨库绑定。在创建跨库绑定前，需要先开启 [`tidb_opt_enable_fuzzy_binding`](/system-variables.md#tidb_opt_enable_fuzzy_binding-new-in-v760) 系统变量。

你可以使用跨库绑定简化在数据按类别分库存储、各数据库对象定义一致且应用逻辑类似的场景下固定执行计划的流程。以下是一些常见用例：

-   在 TiDB 上运行 SaaS 或 PaaS 服务时，每个租户的数据分别存储在不同数据库中，便于数据维护和管理
-   单实例分库分表迁移到 TiDB 后保留原有库表结构，即原实例中的数据按库分类存储

在这些场景下，跨库绑定可以有效缓解因用户数据和负载分布不均、变化快导致的 SQL 性能问题。SaaS 服务商可以通过跨库绑定将大数据量应用验证过的执行计划固定下来，避免小数据量应用快速增长带来的潜在性能问题。

创建跨库绑定时，只需在创建绑定时用 `*` 表示数据库名。例如：

```sql
CREATE GLOBAL BINDING USING SELECT /*+ use_index(t, idx_a) */ * FROM t; -- 创建 GLOBAL 作用域标准绑定
CREATE GLOBAL BINDING USING SELECT /*+ use_index(t, idx_a) */ * FROM *.t; -- 创建 GLOBAL 作用域跨库绑定
SHOW GLOBAL BINDINGS;
```

输出如下：

```sql
+----------------------------+---------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+--------+------------------------------------------------------------------+-------------+
| Original_sql               | Bind_sql                                          | Default_db | Status  | Create_time             | Update_time             | Charset | Collation       | Source | Sql_digest                                                       | Plan_digest |
+----------------------------+---------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+--------+------------------------------------------------------------------+-------------+
| select * from `test` . `t` | SELECT /*+ use_index(`t` `idx_a`)*/ * FROM `test`.`t` | test       | enabled | 2023-12-29 14:19:01.332 | 2023-12-29 14:19:01.332 | utf8    | utf8_general_ci | manual | 8b193b00413fdb910d39073e0d494c96ebf24d1e30b131ecdd553883d0e29b42 |             |
| select * from `*` . `t`    | SELECT /*+ use_index(`t` `idx_a`)*/ * FROM `*`.`t`    |            | enabled | 2023-12-29 14:19:02.232 | 2023-12-29 14:19:02.232 | utf8    | utf8_general_ci | manual | 8b193b00413fdb910d39073e0d494c96ebf24d1e30b131ecdd553883d0e29b42 |             |
+----------------------------+---------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+--------+------------------------------------------------------------------+-------------+
```

在 `SHOW GLOBAL BINDINGS` 输出中，跨库绑定的 `Default_db` 字段值为空，`Original_sql` 和 `Bind_sql` 字段中的数据库名用 `*` 表示。该绑定适用于所有数据库下的 `select * from t` 查询，而不仅限于某个特定数据库。

对于同一查询，跨库绑定和标准绑定可以共存。TiDB 的绑定匹配顺序为：SESSION 作用域标准绑定 > SESSION 作用域跨库绑定 > GLOBAL 作用域标准绑定 > GLOBAL 作用域跨库绑定。

除创建语法外，跨库绑定的删除和状态变更语法与标准绑定一致。以下为详细用例。

1.  创建数据库 `db1` 和 `db2`，并在每个数据库中创建两张表：

    ```sql
    CREATE DATABASE db1;
    CREATE TABLE db1.t1 (a INT, KEY(a));
    CREATE TABLE db1.t2 (a INT, KEY(a));
    CREATE DATABASE db2;
    CREATE TABLE db2.t1 (a INT, KEY(a));
    CREATE TABLE db2.t2 (a INT, KEY(a));
    ```

2.  开启跨库绑定功能：

    ```sql
    SET tidb_opt_enable_fuzzy_binding=1;
    ```

3.  创建跨库绑定：

    ```sql
    CREATE GLOBAL BINDING USING SELECT /*+ use_index(t1, idx_a), use_index(t2, idx_a) */ * FROM *.t1, *.t2;
    ```

4.  执行查询并验证绑定是否生效：

    ```sql
    SELECT * FROM db1.t1, db1.t2;
    SELECT @@LAST_PLAN_FROM_BINDING;
    +--------------------------+
    | @@LAST_PLAN_FROM_BINDING |
    +--------------------------+
    |                        1 |
    +--------------------------+

    SELECT * FROM db2.t1, db2.t2;
    SELECT @@LAST_PLAN_FROM_BINDING;
    +--------------------------+
    | @@LAST_PLAN_FROM_BINDING |
    +--------------------------+
    |                        1 |
    +--------------------------+

    SELECT * FROM db1.t1, db2.t2;
    SELECT @@LAST_PLAN_FROM_BINDING;
    +--------------------------+
    | @@LAST_PLAN_FROM_BINDING |
    +--------------------------+
    |                        1 |
    +--------------------------+

    USE db1;
    SELECT * FROM t1, db2.t2;
    SELECT @@LAST_PLAN_FROM_BINDING;
    +--------------------------+
    | @@LAST_PLAN_FROM_BINDING |
    +--------------------------+
    |                        1 |
    +--------------------------+
    ```

5.  查看绑定：

    ```sql
    SHOW GLOBAL BINDINGS;
    +----------------------------------------------+------------------------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
    | Original_sql                                 | Bind_sql                                                                                 | Default_db | Status  | Create_time             | Update_time             | Charset | Collation          | Source | Sql_digest                                                       | Plan_digest |
    +----------------------------------------------+------------------------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
    | select * from ( `*` . `t1` ) join `*` . `t2` | SELECT /*+ use_index(`t1` `idx_a`) use_index(`t2` `idx_a`)*/ * FROM (`*` . `t1`) JOIN `*` . `t2` |            | enabled | 2023-12-29 14:22:28.144 | 2023-12-29 14:22:28.144 | utf8    | utf8_general_ci    | manual | ea8720583e80644b58877663eafb3579700e5f918a748be222c5b741a696daf4 |             |
    +----------------------------------------------+------------------------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
    ```

6.  删除跨库绑定：

    ```sql
    DROP GLOBAL BINDING FOR SQL DIGEST 'ea8720583e80644b58877663eafb3579700e5f918a748be222c5b741a696daf4';
    SHOW GLOBAL BINDINGS;
    Empty set (0.00 sec)
    ```

## 基线捕获 {#baseline-capturing}

用于[防止升级时执行计划回退](#prevent-regression-of-execution-plans-during-an-upgrade)的场景，该功能会捕获满足捕获条件的查询并为其创建绑定。

计划基线指的是优化器可用于执行某条 SQL 语句的一组可接受的计划。通常，TiDB 只有在确认某个计划性能良好后才会将其加入计划基线。此处的计划包含优化器重现执行计划所需的所有相关细节（如 SQL 计划标识、Hint 集合、绑定值和优化器环境）。

### 开启捕获 {#enable-capturing}

要开启基线捕获，将 `tidb_capture_plan_baselines` 设置为 `on`。默认值为 `off`。

> **Note:**
>
> 由于自动绑定创建功能依赖于 [语句概要](/statement-summary-tables.md)，使用自动绑定前请确保已开启语句概要。

开启自动绑定创建后，每隔一个 `bind-info-lease`（默认值为 `3s`），会遍历语句概要中的历史 SQL 语句，对出现次数不少于两次的 SQL 语句自动创建绑定。对于这些 SQL 语句，TiDB 会自动绑定语句概要中记录的执行计划。

但 TiDB 不会自动捕获以下类型 SQL 语句的绑定：

-   `EXPLAIN` 和 `EXPLAIN ANALYZE` 语句。
-   TiDB 内部执行的 SQL 语句，如自动加载统计信息时的 `SELECT` 查询。
-   已包含 `Enabled` 或 `Disabled` 绑定的语句。
-   被捕获条件过滤掉的语句。

> **Note:**
>
> 目前，绑定会为查询语句生成一组 Hint 以固定某个执行计划。这样，同一查询的执行计划不会发生变化。对于大多数 OLTP 查询（包括使用同一索引或 Join 算法（如 HashJoin 和 IndexJoin）的查询），TiDB 能保证绑定前后计划一致。但由于 Hint 的局限性，对于某些复杂查询（如三表及以上的 Join、MPP 查询和复杂 OLAP 查询），TiDB 无法保证计划一致性。

对于 `PREPARE` / `EXECUTE` 语句以及通过二进制协议执行的查询，TiDB 会自动为实际的查询语句捕获绑定，而不是为 `PREPARE` / `EXECUTE` 语句捕获绑定。

> **Note:**
>
> 由于 TiDB 内部有部分嵌入式 SQL 语句用于保证某些功能的正确性，基线捕获默认会自动屏蔽这些 SQL 语句。

### 过滤绑定 {#filter-out-bindings}

该功能允许你配置黑名单，过滤掉不希望捕获绑定的查询。黑名单有三种维度：表名、频率和用户名。

#### 用法 {#usage}

将过滤条件插入系统表 `mysql.capture_plan_baselines_blacklist`，过滤条件会立即在整个集群生效。

```sql
-- 按表名过滤
INSERT INTO mysql.capture_plan_baselines_blacklist(filter_type, filter_value) VALUES('table', 'test.t');

-- 通过通配符按库名和表名过滤
INSERT INTO mysql.capture_plan_baselines_blacklist(filter_type, filter_value) VALUES('table', 'test.table_*');
INSERT INTO mysql.capture_plan_baselines_blacklist(filter_type, filter_value) VALUES('table', 'db_*.table_*');

-- 按频率过滤
INSERT INTO mysql.capture_plan_baselines_blacklist(filter_type, filter_value) VALUES('frequency', '2');

-- 按用户名过滤
INSERT INTO mysql.capture_plan_baselines_blacklist(filter_type, filter_value) VALUES('user', 'user1');
```

| **Dimension name** | **Description**                                                                                                                                                                                                     | Remarks                                                                                                                                                                                                                                                              |
| :----------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| table              | 按表名过滤。每条过滤规则格式为 `db.table`。支持的过滤语法包括[普通表名](/table-filter.md#plain-table-names)和[通配符](/table-filter.md#wildcards)。                         | 不区分大小写。若表名包含非法字符，日志会返回警告信息 `[sql-bind] failed to load mysql.capture_plan_baselines_blacklist`。                                                                                                 |
| frequency          | 按频率过滤。默认情况下，执行次数大于 1 的 SQL 语句会被捕获。你可以设置较高的频率，仅捕获高频语句。                                                                             | 频率小于 1 被视为非法，日志会返回警告信息 `[sql-bind] frequency threshold is less than 1, ignore it`。若插入多条频率过滤规则，以最大频率为准。                                                                              |
| user               | 按用户名过滤。被黑名单用户执行的语句不会被捕获。                                                                                                                               | 若多用户执行同一语句且用户名均在黑名单中，则该语句不会被捕获。                                                                                                                        |

> **Note:**
>
> -   修改黑名单需要 super 权限。
>
> -   若黑名单中包含非法过滤项，TiDB 会在日志中返回警告信息 `[sql-bind] unknown capture filter type, ignore it`。

### 防止升级时执行计划回退 {#prevent-regression-of-execution-plans-during-an-upgrade}

在升级 TiDB 集群前，你可以通过基线捕获防止执行计划回退，操作步骤如下：

1.  开启基线捕获并保持其运行。

    > **Note:**
    >
    > 测试数据显示，长期开启基线捕获对集群负载性能有轻微影响。建议尽可能长时间开启基线捕获，以便捕获重要计划（出现两次及以上）。

2.  升级 TiDB 集群。升级后，TiDB 会使用已捕获的绑定保证执行计划一致性。

3.  升级后按需删除绑定。

    -   通过 [`SHOW GLOBAL BINDINGS`](#view-bindings) 语句检查绑定来源。

        在输出结果中，通过 `Source` 字段判断绑定是捕获（`capture`）还是手动创建（`manual`）。

    -   判断是否保留捕获的绑定：

            -- 查看绑定生效时的计划
            SET @@SESSION.TIDB_USE_PLAN_BASELINES = true;
            EXPLAIN FORMAT='VERBOSE' SELECT * FROM t1 WHERE ...;

            -- 查看绑定失效时的计划
            SET @@SESSION.TIDB_USE_PLAN_BASELINES = false;
            EXPLAIN FORMAT='VERBOSE' SELECT * FROM t1 WHERE ...;

        -   若执行计划一致，可安全删除绑定。

        -   若执行计划不一致，需要排查原因（如检查统计信息）。此时需保留绑定以保证计划一致性。

## 基线演化 {#baseline-evolution}

基线演化是 TiDB v4.0 引入的 SPM 重要特性。

随着数据的更新，原先绑定的执行计划可能不再最优。基线演化功能可以自动优化绑定的执行计划。

此外，基线演化在一定程度上也能避免统计信息变化带来的执行计划抖动。

### 用法 {#usage}

通过以下语句开启自动绑定演化：

```sql
SET GLOBAL tidb_evolve_plan_baselines = ON;
```

`tidb_evolve_plan_baselines` 的默认值为 `off`。

<CustomContent platform="tidb">

> **Warning:**
>
> -   基线演化为实验特性，可能存在未知风险，**不建议**在生产环境中使用。
> -   该变量会被强制设置为 `off`，直到基线演化功能正式 GA。如果你尝试开启该功能，会返回错误。如果你已在生产环境中使用该功能，请尽快关闭。如发现绑定状态异常，请[联系 PingCAP 或社区](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Warning:**
>
> -   基线演化为实验特性，可能存在未知风险，**不建议**在生产环境中使用。
> -   该变量会被强制设置为 `off`，直到基线演化功能正式 GA。如果你尝试开启该功能，会返回错误。如果你已在生产环境中使用该功能，请尽快关闭。如发现绑定状态异常，请[联系 TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

</CustomContent>

开启自动绑定演化功能后，如果优化器选择的最优执行计划不在绑定执行计划中，优化器会将该计划标记为待验证的执行计划。每隔一个 `bind-info-lease`（默认值为 `3s`），会选择一个待验证的执行计划，与绑定执行计划中代价最小的计划进行实际执行时间对比。如果待验证计划的执行时间更短（当前判定标准为执行时间不超过绑定计划的 2/3），则将该计划标记为可用绑定。以下示例描述了上述过程。

假设表 `t` 定义如下：

```sql
CREATE TABLE t(a INT, b INT, KEY(a), KEY(b));
```

对表 `t` 执行如下查询：

```sql
SELECT * FROM t WHERE a < 100 AND b < 100;
```

在上述表中，满足 `a < 100` 条件的行很少。但由于某些原因，优化器错误地选择了全表扫描而不是使用索引 `a` 的最优执行计划。你可以先通过以下语句创建绑定：

```sql
CREATE GLOBAL BINDING for SELECT * FROM t WHERE a < 100 AND b < 100 USING SELECT * FROM t use index(a) WHERE a < 100 AND b < 100;
```

再次执行上述查询时，优化器会选择索引 `a`（受绑定影响），以减少查询时间。

假设随着对表 `t` 的插入和删除，满足 `a < 100` 条件的行数增多，满足 `b < 100` 条件的行数减少。此时，绑定下使用索引 `a` 可能不再是最优计划。

基线演化可以解决此类问题。当优化器识别到表数据变化时，会为该查询生成使用索引 `b` 的执行计划。但由于当前计划存在绑定，该查询计划不会被采用和执行，而是存储在后台演化列表中。在演化过程中，如果该计划验证后执行时间明显短于当前使用索引 `a` 的计划，则会将索引 `b` 加入可用绑定列表。此后再次执行该查询时，优化器首先生成使用索引 `b` 的执行计划，并确认该计划在绑定列表中，然后采用并执行该计划，以适应数据变化后的查询性能。

为减少自动演化对集群的影响，可通过以下配置：

-   设置 `tidb_evolve_plan_task_max_time` 限制每个执行计划的最大执行时间，默认值为 `600s`。实际验证过程中，最大执行时间也会被限制为不超过待验证计划的两倍。
-   设置 `tidb_evolve_plan_task_start_time`（默认 `00:00 +0000`）和 `tidb_evolve_plan_task_end_time`（默认 `23:59 +0000`）限制时间窗口。

### 注意事项 {#notes}

由于基线演化会自动创建新绑定，当查询环境发生变化时，自动创建的绑定可能存在多种行为选择。请注意以下事项：

-   基线演化仅对至少有一个全局绑定的标准化 SQL 语句进行演化。

-   由于创建新绑定会删除之前所有绑定（针对同一标准化 SQL 语句），手动创建新绑定后，自动演化的绑定会被删除。

-   演化过程中会保留所有与计算过程相关的 Hint，包括：

    | Hint                      | Description                                                             |
    | :------------------------ | :---------------------------------------------------------------------- |
    | `memory_quota`            | 查询可用的最大内存。                                                    |
    | `use_toja`                | 优化器是否将子查询转换为 Join。                                         |
    | `use_cascades`            | 是否使用 cascades 优化器。                                              |
    | `no_index_merge`          | 优化器是否将 Index Merge 作为读表选项。                                 |
    | `read_consistent_replica` | 读表时是否强制开启 Follower Read。                                      |
    | `max_execution_time`      | 查询的最长持续时间。                                                    |

-   `read_from_storage` 是一个特殊 Hint，用于指定读表时从 TiKV 还是 TiFlash 读取数据。由于 TiDB 提供隔离读，隔离条件变化时，该 Hint 对演化计划影响较大。因此，若初始绑定中存在该 Hint，TiDB 会忽略其所有演化绑定。

## 升级检查清单 {#upgrade-checklist}

在集群升级过程中，SQL 执行计划管理（SPM）可能导致兼容性问题，进而导致升级失败。为确保升级顺利，你需要在升级前检查以下内容：

-   从 v5.2.0 之前的版本（即 v4.0、v5.0 和 v5.1）升级到当前版本时，升级前需确保已禁用 `tidb_evolve_plan_baselines`。禁用方法如下：

    ```sql
    -- 检查旧版本中 `tidb_evolve_plan_baselines` 是否已禁用

    SELECT @@global.tidb_evolve_plan_baselines;

    -- 若 `tidb_evolve_plan_baselines` 仍为启用状态，则禁用之

    SET GLOBAL tidb_evolve_plan_baselines = OFF;
    ```

-   从 v4.0 升级到当前版本前，需要检查所有可用 SQL 绑定对应的查询在新版本中的语法是否正确。如有语法错误，需删除对应 SQL 绑定。操作步骤如下：

    ```sql
    -- 检查待升级版本中所有可用 SQL 绑定对应的查询

    SELECT bind_sql FROM mysql.bind_info WHERE status = 'using';

    -- 在新版本测试环境中验证上述 SQL 查询结果

    bind_sql_0;
    bind_sql_1;
    ...

    -- 若出现语法错误（ERROR 1064 (42000): You have an error in your SQL syntax），则删除对应绑定
    -- 若出现其他错误（如表不存在），说明语法兼容，无需其他操作
    ```
