---
title: SQL Plan Management (SPM)
summary: 了解 TiDB 中的 SQL 计划管理。
---

# SQL Plan Management (SPM) {#sql-plan-management-spm}

SQL Plan Management 是一组执行 SQL 绑定以手动干预 SQL 执行计划的功能。这些功能包括 SQL 绑定、基线捕获和基线演化。

## SQL binding {#sql-binding}

SQL 绑定是 SPM 的基础。[Optimizer Hints](/optimizer-hints.md) 文档介绍了如何通过提示选择特定的执行计划。然而，有时你需要在不修改 SQL 语句的情况下干预执行选择。通过 SQL 绑定，你可以在不修改 SQL 语句的前提下，选择指定的执行计划。

<CustomContent platform="tidb">

> **Note:**
>
> 要使用 SQL 绑定，你需要拥有 `SUPER` 权限。如果 TiDB 提示你权限不足，请参见 [Privilege Management](/privilege-management.md) 添加所需权限。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 要使用 SQL 绑定，你需要拥有 `SUPER` 权限。如果 TiDB 提示你权限不足，请参见 [Privilege Management](https://docs.pingcap.com/tidb/stable/privilege-management) 添加所需权限。

</CustomContent>

### 创建绑定 {#create-a-binding}

你可以根据 SQL 语句或历史执行计划为某个 SQL 语句创建绑定。

#### 根据 SQL 语句创建绑定 {#create-a-binding-according-to-a-sql-statement}

```sql
CREATE [GLOBAL | SESSION] BINDING [FOR BindableStmt] USING BindableStmt;
```

此语句在 GLOBAL 或 SESSION 级别绑定 SQL 执行计划。目前，TiDB 支持的可绑定 SQL 语句（BindableStmt）包括 `SELECT`、`DELETE`、`UPDATE` 和带有 `SELECT` 子查询的 `INSERT` / `REPLACE`。示例如下：

```sql
CREATE GLOBAL BINDING USING SELECT /*+ use_index(orders, orders_book_id_idx) */ * FROM orders;
CREATE GLOBAL BINDING FOR SELECT * FROM orders USING SELECT /*+ use_index(orders, orders_book_id_idx) */ * FROM orders;
```

> **Note:**
>
> 绑定的优先级高于手动添加的 hints。因此，当你在执行包含 hints 的语句时，如果存在对应的绑定，控制优化器行为的 hints 不会生效，但其他类型的 hints 仍然有效。

具体而言，由于语法冲突，以下两类语句不能绑定到执行计划，绑定创建时会报语法错误。示例如下：

```sql
-- 类型一：使用 `JOIN` 关键字且未指定关联列（未使用 `USING`）获取笛卡尔积的语句。
CREATE GLOBAL BINDING for
    SELECT * FROM orders o1 JOIN orders o2
USING
    SELECT * FROM orders o1 JOIN orders o2;

-- 类型二：包含 `USING` 关键字的 `DELETE` 语句。
CREATE GLOBAL BINDING for
    DELETE FROM users USING users JOIN orders ON users.id = orders.user_id
USING
    DELETE FROM users USING users JOIN orders ON users.id = orders.user_id;
```

你可以通过等价语句绕过语法冲突。例如，可以将上述语句改写为：

```sql
-- 类型一语句的改写：删除 `JOIN` 关键字，用逗号替代。
CREATE GLOBAL BINDING for
    SELECT * FROM orders o1, orders o2
USING
    SELECT * FROM orders o1, orders o2;

-- 类型二语句的改写：删除 `DELETE` 语句中的 `USING` 关键字。
CREATE GLOBAL BINDING for
    DELETE users FROM users JOIN orders ON users.id = orders.user_id
USING
    DELETE users FROM users JOIN orders ON users.id = orders.user_id;
```

> **Note:**
>
> 在为带有 `SELECT` 子查询的 `INSERT` / `REPLACE` 语句创建执行计划绑定时，需要在 `SELECT` 子查询中指定你想绑定的 optimizer hints，而不能在 `INSERT` / `REPLACE` 关键字后指定，否则 hints 不会生效。

示例：

```sql
-- hint 在以下语句中生效。
CREATE GLOBAL BINDING for
    INSERT INTO orders SELECT * FROM pre_orders WHERE status = 'VALID' AND created <= (NOW() - INTERVAL 1 HOUR)
USING
    INSERT INTO orders SELECT /*+ use_index(@sel_1 pre_orders, idx_created) */ * FROM pre_orders WHERE status = 'VALID' AND created <= (NOW() - INTERVAL 1 HOUR);

-- hint 在以下语句中无法生效。
CREATE GLOBAL BINDING for
    INSERT INTO orders SELECT * FROM pre_orders WHERE status = 'VALID' AND created <= (NOW() - INTERVAL 1 HOUR)
USING
    INSERT /*+ use_index(@sel_1 pre_orders, idx_created) */ INTO orders SELECT * FROM pre_orders WHERE status = 'VALID' AND created <= (NOW() - INTERVAL 1 HOUR);
```

如果在创建执行计划绑定时未指定作用域，默认作用域为 SESSION。TiDB 优化器会对绑定的 SQL 语句进行规范化，并存储在系统表中。在处理 SQL 查询时，如果规范化后的语句与系统表中的绑定 SQL 语句匹配，且系统变量 `tidb_use_plan_baselines` 设置为 `on`（默认值为 `on`），则 TiDB 会为该语句使用对应的 optimizer hints。如果存在多个匹配的执行计划，优化器会选择成本最低的一个绑定。

`规范化` 是将 SQL 语句中的常量转换为变量参数，并明确指定查询中引用的表所在的数据库，同时对 SQL 语句中的空格和换行进行标准化处理的过程。示例如下：

```sql
SELECT * FROM users WHERE balance >    100
-- 规范化后，语句变为：
SELECT * FROM bookshop . users WHERE balance > ?
```

> **Note:**
>
> 在规范化过程中，`IN` 谓词中的 `?` 会被规范为 `...`。
>
> 例如：
>
> ```sql
> SELECT * FROM books WHERE type IN ('Novel')
> SELECT * FROM books WHERE type IN ('Novel','Life','Education')
> -- 规范化后，语句变为：
> SELECT * FROM bookshop . books WHERE type IN ( ... )
> SELECT * FROM bookshop . books WHERE type IN ( ... )
> ```
>
> 规范化后，不同长度的 `IN` 谓词会被识别为相同的语句，因此只需创建一个绑定，适用于所有这些谓词。
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
> 在 TiDB 7.4.0 之前的集群中创建的绑定可能包含 `IN (?)`。升级到 7.4.0 或更高版本后，这些绑定会被修改为 `IN (...)`。
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
> ```
>
> -- 升级到 7.4.0 或更高版本后
> mysql> SHOW GLOBAL BINDINGS;
> +-------------------------------------------------+------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
> | Original_sql                                    | Bind_sql                                                               | Default_db | Status  | Create_time             | Update_time             | Charset | Collation          | Source | Sql_digest                                                       | Plan_digest |
> +-------------------------------------------------+------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
> | select * from `test` . `t` where `a` in ( ... ) | SELECT /*+ use_index(`t` `idx_a`)*/ * FROM `test`.`t` WHERE `a` IN (1) | test       | enabled | 2024-09-03 15:35:59.861 | 2024-09-03 15:35:59.861 | utf8mb4 | utf8mb4_general_ci | manual | da38bf216db4a53e1a1e01c79ffa42306419442ad7238480bb7ac510723c8bdf |             |
> +-------------------------------------------------+------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
> ```
>
> 当 SQL 语句在 GLOBAL 和 SESSION 作用域中都存在绑定执行计划时，由于优化器在遇到 SESSION 绑定时会忽略 GLOBAL 作用域中的绑定执行计划，因此 SESSION 作用域中的绑定会屏蔽 GLOBAL 作用域中的执行计划。

示例：

```sql
-- 创建一个 GLOBAL 绑定，并指定使用 `sort merge join`。
CREATE GLOBAL BINDING for
    SELECT * FROM t1, t2 WHERE t1.id = t2.id
USING
    SELECT /*+ merge_join(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;

-- 该 SQL 语句的执行计划会使用 GLOBAL 绑定中指定的 `sort merge join`。
explain SELECT * FROM t1, t2 WHERE t1.id = t2.id;

-- 创建另一个 SESSION 绑定，并指定使用 `hash join`。
CREATE BINDING for
    SELECT * FROM t1, t2 WHERE t1.id = t2.id
USING
    SELECT /*+ hash_join(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;

-- 在此语句的执行计划中，将使用 SESSION 绑定中指定的 `hash join`，而不是 GLOBAL 绑定中指定的 `sort merge join`。
explain SELECT * FROM t1, t2 WHERE t1.id = t2.id;
```

当第一个 `SELECT` 语句执行时，优化器会通过 GLOBAL 作用域中的绑定在语句中添加 `sm_join(t1, t2)` hints。`explain` 结果中的执行计划顶层节点为 MergeJoin。当第二个 `SELECT` 语句执行时，优化器会使用 SESSION 作用域中的绑定，而不是 GLOBAL 作用域中的绑定，并在语句中添加 `hash_join(t1, t2)` hints。`explain` 结果中的执行计划顶层节点为 HashJoin。

每个标准化的 SQL 语句一次只能创建一个绑定。当为同一标准化 SQL 语句创建多个绑定时，最后创建的绑定会被保留，之前的所有绑定（包括已创建和演化的）都被标记为已删除。但会话绑定和全局绑定可以共存，不受此限制。

此外，创建绑定时，TiDB 要求会话处于某个数据库上下文中，即连接时指定了数据库或执行了 `use ${database}`。

原始 SQL 语句和绑定语句在规范化和去除 hints 后必须完全一致，否则绑定会失败。示例：

-  该绑定可以成功创建，因为参数化和 hints 去除前后文本相同：`SELECT * FROM test . t WHERE a > ?`

    ```sql
    CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index  (idx) WHERE a > 2
    ```

-  该绑定会失败，因为原始 SQL 语句被处理为 `SELECT * FROM test . t WHERE a > ?`，而绑定的 SQL 被处理为 `SELECT * FROM test . t WHERE b > ?`。

    ```sql
    CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index(idx) WHERE b > 2
    ```

> **Note:**
>
> 对于 `PREPARE` / `EXECUTE` 语句以及通过二进制协议执行的查询，你需要为实际的查询语句创建执行计划绑定，而不是为 `PREPARE` / `EXECUTE` 语句创建。

#### 根据历史执行计划创建绑定 {#create-a-binding-according-to-a-historical-execution-plan}

为了让某个 SQL 语句的执行计划固定为历史执行计划，可以使用 Plan Digest 将该历史执行计划绑定到 SQL 语句上，这比根据 SQL 语句绑定更方便。此外，还可以一次性为多个 SQL 语句绑定执行计划。更多细节和示例请参见 [`CREATE [GLOBAL|SESSION] BINDING`](/sql-statements/sql-statement-create-binding.md)。

使用此功能时，请注意以下事项：

-  该功能根据历史执行计划生成 hints，并使用生成的 hints 进行绑定。由于历史执行计划存储在 [Statement Summary Tables](/statement-summary-tables.md) 中，使用此功能前需要先启用 [`tidb_enable_stmt_summary`](/system-variables.md#tidb_enable_stmt_summary-new-in-v304) 系统变量。
-  对于 TiFlash 查询、包含三个及以上表的 Join 查询，以及包含子查询的查询，自动生成的 hints 可能不足，导致计划未能完全绑定。在此情况下，创建绑定时会发出警告。
-  如果历史执行计划对应带 hints 的 SQL 语句，绑定中会加入这些 hints。例如，执行 `SELECT /*+ max_execution_time(1000) */ * FROM t` 后，基于其 Plan Digest 创建的绑定会包含 `max_execution_time(1000)`。

此绑定方法的 SQL 语句如下：

```sql
CREATE [GLOBAL | SESSION] BINDING FROM HISTORY USING PLAN DIGEST StringLiteralOrUserVariableList;
```

此语句通过 Plan Digest 将执行计划绑定到 SQL 语句，默认作用域为 SESSION。创建的绑定的适用 SQL 语句、优先级、作用域和生效条件与【根据 SQL 语句创建绑定】相同。

使用此绑定方法时，首先需要在 `statements_summary` 中获取目标历史执行计划对应的 Plan Digest，然后用 Plan Digest 创建绑定。具体步骤如下：

1.  获取目标执行计划在 `statements_summary` 中对应的 Plan Digest。

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

    在此示例中，可以看到对应 Plan Digest 的执行计划为 `4e3159169cc63c14b139a4e7d72eae1759875c9a9581f94bb2079aae961189cb`。

2.  使用 Plan Digest 创建绑定：

    ```sql
    CREATE BINDING FROM HISTORY USING PLAN DIGEST '4e3159169cc63c14b139a4e7d72eae1759875c9a9581f94bb2079aae961189cb';
    ```

验证绑定是否生效，可以【查看绑定】：

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

### 删除绑定 {#remove-a-binding}

你可以根据 SQL 语句或 SQL Digest 删除绑定。

#### 根据 SQL 语句删除绑定 {#remove-a-binding-according-to-a-sql-statement}

```sql
DROP [GLOBAL | SESSION] BINDING FOR BindableStmt;
```

此语句在 GLOBAL 或 SESSION 级别删除指定的执行计划绑定。默认作用域为 SESSION。

一般情况下，SESSION 作用域中的绑定主要用于测试或特殊场景。若要让绑定在所有 TiDB 进程中生效，需要使用 GLOBAL 绑定。创建的 SESSION 绑定会屏蔽对应的 GLOBAL 绑定，直到会话结束，即使在会话结束前删除了 SESSION 绑定。在这种情况下，不会有绑定生效，执行计划由优化器选择。

以下示例基于【创建绑定】中的示例，说明 SESSION 绑定屏蔽 GLOBAL 绑定：

```sql
-- 删除在 SESSION 作用域中创建的绑定。
drop session binding for SELECT * FROM t1, t2 WHERE t1.id = t2.id;

-- 再次查看 SQL 执行计划。
explain SELECT * FROM t1,t2 WHERE t1.id = t2.id;
```

上述示例中，删除的 SESSION 作用域绑定屏蔽了对应的 GLOBAL 绑定。优化器不会在语句中添加 `sm_join(t1, t2)` hints。`explain` 结果中的执行计划顶层节点不会被此 hints 固定为 MergeJoin，而是由优化器根据成本估算自主选择。

#### 根据 SQL Digest 删除绑定 {#remove-a-binding-according-to-sql-digest}

除了根据 SQL 语句删除绑定外，还可以根据 SQL Digest 删除绑定。更多细节和示例请参见 [`DROP [GLOBAL|SESSION] BINDING`](/sql-statements/sql-statement-drop-binding.md)。

```sql
DROP [GLOBAL | SESSION] BINDING FOR SQL DIGEST StringLiteralOrUserVariableList;
```

此语句删除对应 SQL Digest 的执行计划绑定，作用域为 GLOBAL 或 SESSION，默认为 SESSION。可以通过【查看绑定】获取 SQL Digest。

> **Note:**
>
> 执行 `DROP GLOBAL BINDING` 会删除当前 tidb-server 实例缓存中的绑定，并将系统表中对应行的状态改为 'deleted'。此操作不会直接删除系统表中的记录，因为其他 tidb-server 实例需要读取到 'deleted' 状态后，才会在其缓存中删除对应绑定。对于状态为 'deleted' 的系统表记录，每隔 100 个 `bind-info-lease`（默认值为 `3s`，总共 `300s`）的后台线程会触发回收和清理操作，删除 `update_time` 在 10 个 `bind-info-lease` 之前的绑定（确保所有 tidb-server 实例都已读取到 'deleted' 状态并更新缓存）。

### 更改绑定状态 {#change-binding-status}

#### 根据 SQL 语句更改绑定状态 {#change-binding-status-according-to-a-sql-statement}

```sql
SET BINDING [ENABLED | DISABLED] FOR BindableStmt;
```

你可以执行此语句更改绑定的状态。默认状态为 ENABLED。作用域默认为 GLOBAL，且不可修改。

执行时，只能将绑定状态从 `Disabled` 改为 `Enabled`，或从 `Enabled` 改为 `Disabled`。如果没有可更改状态的绑定，会返回警告信息 `There are no bindings can be set the status. Please check the SQL text`。注意，状态为 `Disabled` 的绑定不会被任何查询使用。

#### 根据 `<code>sql_digest</code>` 更改绑定状态 {#change-binding-status-according-to-code-sql-digest-code}

除了根据 SQL 语句更改绑定状态外，还可以根据 `sql_digest` 更改：

```sql
SET BINDING [ENABLED | DISABLED] FOR SQL DIGEST 'sql_digest';
```

可以更改的绑定状态与【根据 SQL 语句更改绑定状态】的效果相同。如果没有对应的绑定，返回警告信息 `can't find any binding for 'sql_digest'`。

### 查看绑定 {#view-bindings}

```sql
SHOW [GLOBAL | SESSION] BINDINGS [ShowLikeOrWhere]
```

此语句按照绑定更新时间的最新到最旧顺序输出 GLOBAL 或 SESSION 作用域中的执行计划绑定。目前，`SHOW BINDINGS` 输出 11 列，具体如下：

| 列名 | 说明 |
| :--- | :--- |
| original_sql | 规范化后带参数化的原始 SQL 语句 |
| bind_sql | 带 hints 的绑定 SQL 语句 |
| default_db | 默认数据库 |
| status | 状态，包括 `enabled`（替代 v6.0 中的 `using` 状态）、`disabled`、`deleted`、`invalid`、`rejected` 和 `pending verify` |
| create_time | 创建时间 |
| update_time | 更新时间 |
| charset | 字符集 |
| collation | 排序规则 |
| source | 绑定的创建方式，包括 `manual`（根据 SQL 语句创建）、`history`（根据历史执行计划创建）、`capture`（由 TiDB 自动捕获）和 `evolve`（由 TiDB 自动演化） |
| sql_digest | 规范化 SQL 语句的 digest |
| plan_digest | 执行计划的 digest |

### 排查绑定问题 {#troubleshoot-a-binding}

你可以通过以下方法排查绑定问题：

-   使用系统变量 [`last_plan_from_binding`](/system-variables.md#last_plan_from_binding-new-in-v40) 查看上次执行语句使用的执行计划是否来自绑定。

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
    1 行，耗时 0.00 秒
    ```

-   使用 `explain format = 'verbose'` 查看 SQL 语句的执行计划。如果 SQL 使用了绑定，可以运行 `show warnings` 查看使用了哪个绑定。

    ```sql
    -- 创建全局绑定

    CREATE GLOBAL BINDING for
        SELECT * FROM t
    USING
        SELECT /*+ USE_INDEX(t, idx_a) */ * FROM t;

    -- 使用 explain format = 'verbose' 查看 SQL 执行计划

    explain format = 'verbose' SELECT * FROM t;

    -- 运行 `show warnings` 查看绑定信息。

    show warnings;
    ```

    ```sql
    +-------+------+--------------------------------------------------------------------------+
    | Level | Code | Message                                                                  |
    +-------+------+--------------------------------------------------------------------------+
    | Note  | 1105 | Using the bindSQL: SELECT /*+ USE_INDEX(`t` `idx_a`)*/ * FROM `test`.`t` |
    +-------+------+--------------------------------------------------------------------------+
    1 行，耗时 0.01 秒
    ```

### 缓存绑定 {#cache-bindings}

每个 TiDB 实例都拥有一个最近最少使用（LRU）缓存，用于存放绑定。缓存容量由系统变量 [`tidb_mem_quota_binding_cache`](/system-variables.md#tidb_mem_quota_binding_cache-new-in-v600) 控制。你可以查看 TiDB 实例中缓存的绑定。

查看绑定缓存状态，运行 `SHOW binding_cache status`。此语句的作用域默认为 GLOBAL，且不可修改。返回值包括：缓存中的可用绑定数、系统中所有可用绑定总数、所有缓存绑定的内存使用情况，以及缓存的总内存。

```sql

SHOW binding_cache status;
```

```sql
+-------------------+-------------------+--------------+--------------+
| bindings_in_cache | bindings_in_table | memory_usage | memory_quota |
+-------------------+-------------------+--------------+--------------+
|                 1 |                 1 | 159 Bytes    | 64 MB        |
+-------------------+-------------------+--------------+--------------+
1 行，耗时 0.00 秒
```

## 利用语句摘要表获取需要绑定的查询 {#utilize-the-statement-summary-table-to-obtain-queries-that-need-to-be-bound}

[Statement summary](/statement-summary-tables.md) 记录了近期 SQL 执行信息，如延迟、执行次数和对应的查询计划。你可以查询语句摘要表，获取符合条件的 `plan_digest`，然后【根据这些历史执行计划创建绑定】(/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan)。

以下示例查询在过去两周内执行次数超过 10 次、且有多个执行计划但未绑定 SQL 的 `SELECT` 语句。按执行次数排序，绑定前 100 个查询到其最快的执行计划。

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
  AND summary_begin_time > DATE_SUB(NOW(), interval 14 day)    -- 过去两周内执行
  AND stmt_type = 'Select'                                     -- 只考虑 select
  AND schema_name NOT IN ('INFORMATION_SCHEMA', 'mysql')       -- 非内部查询
  AND plan_in_binding = 0                                      -- 尚未绑定
GROUP BY stmts.`digest`
  HAVING COUNT(DISTINCT(stmts.plan_digest)) > 1                -- 该查询不稳定，有多个计划
         AND SUM(exec_count) > 10                              -- 高频次，且执行超过 10 次
ORDER BY SUM(exec_count) DESC LIMIT 100;                       -- 前 100 高频次查询
```

通过应用特定过滤条件，获得符合条件的查询后，可以直接执行对应 `binding_stmt` 列中的语句，创建绑定。

    +---------------------------------------------+------------+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+
    | query                                       | exec_count | plan_hint                                                                   | binding_stmt                                                                                                            |
    +---------------------------------------------+------------+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+
    | select * from `t` where `a` = ? and `b` = ? |        401 | use_index(@`sel_1` `test`.`t` `a`), no_order_index(@`sel_1` `test`.`t` `a`) | create global binding from history using plan digest "0d6e97fb1191bbd08dddefa7bd007ec0c422b1416b152662768f43e64a9958a6" |
    | select * from `t` where `b` = ? and `c` = ? |        104 | use_index(@`sel_1` `test`.`t` `b`), no_order_index(@`sel_1` `test`.`t` `b`) | create global binding from history using plan digest "80c2aa0aa7e6d3205755823aa8c6165092c8521fb74c06a9204b8d35fc037dd9" |
    +---------------------------------------------+------------+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+

## 跨库绑定 {#cross-database-binding}

从 v7.6.0 开始，你可以在 TiDB 中通过在绑定创建语法中使用通配符 `*` 来表示数据库名，从而创建跨库绑定。在创建跨库绑定之前，需要先启用 [`tidb_opt_enable_fuzzy_binding`](/system-variables.md#tidb_opt_enable_fuzzy_binding-new-in-v760) 系统变量。

你可以使用跨库绑定简化在数据分类存储在不同数据库、且每个数据库维护相同对象定义、执行类似应用逻辑场景下的执行计划固定操作。常见用例包括：

-   在 TiDB 上运行 SaaS 或 PaaS 服务，每个租户的数据存储在不同数据库中，便于数据维护和管理
-   在单实例中进行数据库分片，迁移到 TiDB 后保持原有数据库 schema，即原实例中的数据按数据库分类存储

在这些场景中，跨库绑定能有效缓解因用户数据和工作负载分布不均、变化迅速带来的 SQL 性能问题。SaaS 提供商可以用跨库绑定固定经过应用验证的大数据量的执行计划，从而避免因小数据量应用快速增长带来的潜在性能问题。

创建跨库绑定时，只需在创建绑定时用 `*` 表示数据库名。例如：

```sql
CREATE GLOBAL BINDING USING SELECT /*+ use_index(t, idx_a) */ * FROM t; -- 创建 GLOBAL 作用域标准绑定。
CREATE GLOBAL BINDING USING SELECT /*+ use_index(t, idx_a) */ * FROM *.t; -- 创建 GLOBAL 作用域跨库绑定。
SHOW GLOBAL BINDINGS;
```

输出示例如下：

```sql
+----------------------------+---------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+--------+------------------------------------------------------------------+-------------+
| Original_sql               | Bind_sql                                          | Default_db | Status  | Create_time             | Update_time             | Charset | Collation       | Source | Sql_digest                                                       | Plan_digest |
+----------------------------+---------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+--------+------------------------------------------------------------------+-------------+
| select * from `test` . `t` | SELECT /*+ use_index(`t` `idx_a`)*/ * FROM `test`.`t` | test       | enabled | 2023-12-29 14:19:01.332 | 2023-12-29 14:19:01.332 | utf8    | utf8_general_ci | manual | 8b193b00413fdb910d39073e0d494c96ebf24d1e30b131ecdd553883d0e29b42 |             |
| select * from `*` . `t`    | SELECT /*+ use_index(`t` `idx_a`)*/ * FROM `*`.`t`    |            | enabled | 2023-12-29 14:19:02.232 | 2023-12-29 14:19:02.232 | utf8    | utf8_general_ci | manual | 8b193b00413fdb910d39073e0d494c96ebf24d1e30b131ecdd553883d0e29b42 |             |
+----------------------------+---------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+--------+------------------------------------------------------------------+-------------+
```

在 `SHOW GLOBAL BINDINGS` 输出中，跨库绑定的 `Default_db` 字段为空，`Original_sql` 和 `Bind_sql` 字段中的数据库名用 `*` 表示。此绑定适用于所有数据库中的 `select * from t` 查询，而不限于某个特定数据库。

对于同一查询，跨库绑定和标准绑定可以同时存在。TiDB 按照以下顺序匹配绑定：SESSION 作用域的标准绑定 > SESSION 作用域的跨库绑定 > GLOBAL 作用域的标准绑定 > GLOBAL 作用域的跨库绑定。

除了创建语法外，跨库绑定与标准绑定共享相同的删除和状态变更语法。示例如下：

1.  创建数据库 `db1` 和 `db2`，在每个数据库中创建两个表：

    ```sql
    CREATE DATABASE db1;
    CREATE TABLE db1.t1 (a INT, KEY(a));
    CREATE TABLE db1.t2 (a INT, KEY(a));
    CREATE DATABASE db2;
    CREATE TABLE db2.t1 (a INT, KEY(a));
    CREATE TABLE db2.t2 (a INT, KEY(a));
    ```

2.  启用跨库绑定功能：

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
    空集 (0.00 秒)
    ```

## 基线捕获 {#baseline-capturing}

用于【防止升级过程中执行计划回归】，此功能会捕获满足捕获条件的查询，并为这些查询创建绑定。

计划基线指一组被优化器接受的执行计划，用于执行 SQL 语句。通常，TiDB 只有在确认执行效果良好后才会将计划加入基线。这里的计划包括所有计划相关的细节（如 SQL 计划标识符、hint 集、绑定值和优化器环境），以便重现执行计划。

### 启用捕获 {#enable-capturing}

要启用基线捕获，将 `tidb_capture_plan_baselines` 设置为 `on`。默认值为 `off`。

> **Note:**
>
> 由于自动绑定创建功能依赖于 [Statement Summary](/statement-summary-tables.md)，使用自动绑定前请确保已启用 Statement Summary。

启用自动绑定后，会每隔 `bind-info-lease`（默认 `3s`）遍历一次 Statement Summary 中的历史 SQL 语句，为至少出现两次的 SQL 自动绑定执行计划。

但 TiDB 不会自动捕获以下类型的 SQL 绑定：

-   `EXPLAIN` 和 `EXPLAIN ANALYZE` 语句。
-   TiDB 内部执行的 SQL 语句，例如用于自动加载统计信息的 `SELECT` 查询。
-   包含 `Enabled` 或 `Disabled` 绑定的语句。
-   被捕获条件过滤掉的语句。

> **Note:**
>
> 当前，绑定会生成一组 hints 来固定由查询语句生成的执行计划。这样，对于同一查询，执行计划不会变化。对于大部分 OLTP 查询，包括使用相同索引或 Join 算法（如 HashJoin 和 IndexJoin）的查询，TiDB 保证绑定前后计划的一致性。但由于 hints 的限制，TiDB 不能保证某些复杂查询（如多于两个表的 Join、MPP 查询和复杂 OLAP 查询）的计划一致性。

对于 `PREPARE` / `EXECUTE` 语句以及通过二进制协议执行的查询，TiDB 会自动捕获实际查询语句的绑定，而不是 `PREPARE` / `EXECUTE` 语句。

> **Note:**
>
> 由于 TiDB 内置一些 SQL 语句以确保某些功能的正确性，基线捕获默认会屏蔽这些 SQL 语句。

### 过滤绑定 {#filter-out-bindings}

此功能允许你配置黑名单，过滤掉不希望捕获的查询绑定。黑名单支持三个维度：表名、频率和用户名。

#### 使用方法 {#usage}

将过滤条件插入系统表 `mysql.capture_plan_baselines_blacklist`，过滤条件立即在整个集群生效。

```sql
-- 按表名过滤
INSERT INTO mysql.capture_plan_baselines_blacklist(filter_type, filter_value) VALUES('table', 'test.t');

-- 通过通配符按数据库名和表名过滤
INSERT INTO mysql.capture_plan_baselines_blacklist(filter_type, filter_value) VALUES('table', 'test.table_*');
INSERT INTO mysql.capture_plan_baselines_blacklist(filter_type, filter_value) VALUES('table', 'db_*.table_*');

-- 按频率过滤
INSERT INTO mysql.capture_plan_baselines_blacklist(filter_type, filter_value) VALUES('frequency', '2');

-- 按用户名过滤
INSERT INTO mysql.capture_plan_baselines_blacklist(filter_type, filter_value) VALUES('user', 'user1');
```

| **维度名** | **说明** | 备注 |
| :--- | :--- | :--- |
| table | 按表名过滤。每条规则格式为 `db.table`。支持的语法包括 [Plain table names](/table-filter.md#plain-table-names) 和 [Wildcards](/table-filter.md#wildcards)。 | 不区分大小写。若表名包含非法字符，日志会返回警告 `[sql-bind] failed to load mysql.capture_plan_baselines_blacklist`。 |
| frequency | 按频率过滤。默认捕获多次执行的 SQL 语句。可以设置较高的频率以捕获频繁执行的语句。 | 设置频率为小于 1 的值视为非法，日志会返回警告 `[sql-bind] frequency threshold is less than 1, ignore it`。若插入多个频率过滤规则，取最高频率的规则生效。 |
| user | 按用户名过滤。被黑名单用户执行的语句不会被捕获。 | 若多个用户执行相同语句，且其用户名都在黑名单中，则该语句不会被捕获。 |

> **Note:**
>
> -  修改黑名单需要拥有超级权限。
> -  黑名单中存在非法过滤条件时，TiDB 会在日志中返回警告 `[sql-bind] unknown capture filter type, ignore it`。

### 防止升级过程中执行计划回归 {#prevent-regression-of-execution-plans-during-an-upgrade}

在升级 TiDB 集群前，可以使用基线捕获防止执行计划回归，步骤如下：

1.  启用基线捕获并保持开启。

    > **Note:**
    >
    > 测试数据表明，长期开启基线捕获会对集群负载性能产生轻微影响，因此建议尽可能长时间开启，以捕获重要的执行计划（出现两次或以上）。

2.  升级 TiDB 集群。升级后，TiDB 会使用捕获的绑定确保执行计划一致性。

3.  升级完成后，根据需要删除绑定。

    -   通过运行【查看绑定】中的 [`SHOW GLOBAL BINDINGS`](#view-bindings) 查看绑定来源。

        在输出中，检查 `Source` 字段，判断绑定是被捕获（`capture`）还是手动创建（`manual`）。

    -   判断是否保留捕获的绑定：

            -- 查看启用绑定的执行计划
            SET @@SESSION.TIDB_USE_PLAN_BASELINES = true;
            EXPLAIN FORMAT='VERBOSE' SELECT * FROM t1 WHERE ...;

            -- 查看禁用绑定的执行计划
            SET @@SESSION.TIDB_USE_PLAN_BASELINES = false;
            EXPLAIN FORMAT='VERBOSE' SELECT * FROM t1 WHERE ...;

        -   若执行计划一致，可以安全删除绑定。

        -   若执行计划不一致，需要排查原因，例如检查统计信息。在此情况下，应保留绑定以确保计划一致。

## 基线演化 {#baseline-evolution}

基线演化是 TiDB v4.0 引入的 SPM 重要特性。

随着数据更新，之前绑定的执行计划可能不再最优。基线演化功能可以自动优化绑定的执行计划。

此外，基线演化在一定程度上也能避免因统计信息变化带来的执行计划抖动。

### 使用方法 {#usage}

使用以下语句启用自动绑定演化：

```sql
SET GLOBAL tidb_evolve_plan_baselines = ON;
```

`tidb_evolve_plan_baselines` 的默认值为 `off`。

<CustomContent platform="tidb">

> **Warning:**
>
> -  基线演化是实验性功能，存在未知风险，不建议在生产环境中使用。
> -  该变量会被强制设置为 `off`，直到基线演化功能正式上线（GA）。如果尝试启用此功能，会返回错误。若已在生产环境中使用此功能，应尽快禁用。如发现绑定状态不符合预期，请【获取支持】(/support.md) 或社区帮助。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Warning:**
>
> -  基线演化是实验性功能，存在未知风险，不建议在生产环境中使用。
> -  该变量会被强制设置为 `off`，直到基线演化功能正式上线（GA）。如果尝试启用此功能，会返回错误。若已在生产环境中使用此功能，应尽快禁用。如发现绑定状态不符合预期，请【联系 TiDB Cloud 支持】(/tidb-cloud/tidb-cloud-support.md)。

</CustomContent>

启用自动绑定演化后，如果优化器选择的最优执行计划不在绑定执行计划中，优化器会将该计划标记为待验证状态。每隔 `bind-info-lease`（默认 `3s`）时间间隔，从待验证计划中选取一个，并与绑定中成本最低的执行计划（以实际执行时间为准）进行比较。如果待验证计划的执行时间更短（当前比较标准为待验证计划的执行时间不超过绑定计划的 2/3），则将其标记为可用绑定。示意如下：

假设表 `t` 定义如下：

```sql
CREATE TABLE t(a INT, b INT, KEY(a), KEY(b));
```

对表 `t` 执行如下查询：

```sql
SELECT * FROM t WHERE a < 100 AND b < 100;
```

在上述表中，满足 `a < 100` 条件的行较少，但由于某些原因，优化器误选了全表扫描而非使用索引 `a` 的最优执行计划。你可以先用以下语句创建绑定：

```sql
CREATE GLOBAL BINDING for SELECT * FROM t WHERE a < 100 AND b < 100 USING SELECT * FROM t use index(a) WHERE a < 100 AND b < 100;
```

再次执行该查询时，优化器会选择索引 `a`（受上述绑定影响）以缩短查询时间。

假设随着插入和删除，满足 `a < 100` 条件的行数不断增加，满足 `b < 100` 条件的行数不断减少，此时使用索引 `a` 的绑定可能不再是最优计划。

基线演化可以解决此类问题。当优化器识别到表中的数据变化时，会生成使用索引 `b` 的执行计划，但由于存在当前计划的绑定，不会采用此计划，而是存入后台演化列表。在演化过程中，如果验证发现该计划的执行时间明显短于当前使用索引 `a` 的执行计划，则会将索引 `b` 添加到可用绑定列表中。之后再次执行查询时，优化器会优先生成使用索引 `b` 的执行计划，并确保该计划在绑定列表中，然后采用并执行此计划以减少数据变化后的查询时间。

为了降低自动演化对集群的影响，可以配置：

-   设置 `tidb_evolve_plan_task_max_time`，限制每个执行计划的最大执行时间，默认 `600s`。在实际验证中，最大执行时间也限制为不超过验证计划时间的两倍。
-   设置 `tidb_evolve_plan_task_start_time`（默认为 `00:00 +0000`）和 `tidb_evolve_plan_task_end_time`（默认为 `23:59 +0000`），限制时间窗口。

### 注意事项 {#notes}

由于基线演化会自动创建新绑定，当查询环境变化时，自动创建的绑定可能具有多种行为选择。请注意以下事项：

-  只对至少有一个全局绑定的标准化 SQL 语句进行演化。
-  由于创建新绑定会删除所有之前的绑定（针对同一标准化 SQL 语句），自动演化生成的绑定在手动创建新绑定后会被删除。
-  演化过程中会保留所有与计算过程相关的 hints，具体如下：

    | hints | 描述 |
    | :------------------------ | :---------------------------------------------------------------------- |
    | `memory_quota` | 查询最大可用内存。 |
    | `use_toja` | 是否将子查询转为 Join。 |
    | `use_cascades` | 是否使用级联优化器。 |
    | `no_index_merge` | 是否使用 Index Merge 作为读取表的选项。 |
    | `read_consistent_replica` | 是否强制启用 Follower 读。 |
    | `max_execution_time` | 查询最长执行时间。 |

-  `read_from_storage` 是一个特殊 hints，用于指定读取数据时是否从 TiKV 还是 TiFlash 读取。由于 TiDB 提供隔离读，当隔离条件变化时，此 hints 对演化执行计划影响较大。因此，若在最初创建的绑定中存在此 hints，TiDB 会忽略所有演化绑定。

## 升级检查清单 {#upgrade-checklist}

在集群升级过程中，SQL Plan Management（SPM）可能引发兼容性问题，导致升级失败。为确保升级顺利进行，你需要在升级前进行以下检查：

-   从低于 v5.2.0（即 v4.0、v5.0 和 v5.1）版本升级到当前版本时，确保在升级前已禁用 `tidb_evolve_plan_baselines`。

    ```sql
    -- 检查在早期版本中 `tidb_evolve_plan_baselines` 是否已禁用。

    SELECT @@global.tidb_evolve_plan_baselines;

    -- 若仍启用，则禁用。

    SET GLOBAL tidb_evolve_plan_baselines = OFF;
    ```

-   在从 v4.0 升级到当前版本前，需检查所有对应 SQL 绑定的语法在新版本中是否正确。如存在语法错误，应删除对应的 SQL 绑定。操作步骤如下：

    ```sql
    -- 检查待升级版本中对应的 SQL 绑定的 SQL 语句。

    SELECT bind_sql FROM mysql.bind_info WHERE status = 'using';

    -- 在新版本的测试环境中验证上述 SQL 语句的结果。

    bind_sql_0;
    bind_sql_1;
    ...

    -- 若存在语法错误（ERROR 1064 (42000): You have an error in your SQL syntax），应删除对应绑定。
    -- 若出现其他错误（如找不到表），说明语法兼容，无需操作。
    ```
