---
title: CREATE RESOURCE GROUP
summary: 了解在 TiDB 中如何使用 CREATE RESOURCE GROUP。
---

# CREATE RESOURCE GROUP

你可以使用 `CREATE RESOURCE GROUP` 语句来创建资源组。

> **Note:**
>
> 该功能在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。

## 语法

```ebnf+diagram
CreateResourceGroupStmt ::=
   "CREATE" "RESOURCE" "GROUP" IfNotExists ResourceGroupName ResourceGroupOptionList

IfNotExists ::=
    ('IF' 'NOT' 'EXISTS')?

ResourceGroupName ::=
    Identifier
|   "DEFAULT"

ResourceGroupOptionList ::=
    DirectResourceGroupOption
|   ResourceGroupOptionList DirectResourceGroupOption
|   ResourceGroupOptionList ',' DirectResourceGroupOption

DirectResourceGroupOption ::=
    "RU_PER_SEC" EqOpt stringLit
|   "PRIORITY" EqOpt ResourceGroupPriorityOption
|   "BURSTABLE"
|   "BURSTABLE" EqOpt Boolean
|   "QUERY_LIMIT" EqOpt '(' ResourceGroupRunawayOptionList ')'
|   "QUERY_LIMIT" EqOpt '(' ')'
|   "QUERY_LIMIT" EqOpt "NULL"
|   "BACKGROUND" EqOpt '(' BackgroundOptionList ')'
|   "BACKGROUND" EqOpt '(' ')'
|   "BACKGROUND" EqOpt "NULL"

ResourceGroupPriorityOption ::=
    LOW
|   MEDIUM
|   HIGH

ResourceGroupRunawayOptionList ::=
    DirectResourceGroupRunawayOption
|   ResourceGroupRunawayOptionList DirectResourceGroupRunawayOption
|   ResourceGroupRunawayOptionList ',' DirectResourceGroupRunawayOption

DirectResourceGroupRunawayOption ::=
    "EXEC_ELAPSED" EqOpt stringLit
|   "PROCESSED_KEYS" EqOpt intLit
|   "RU" EqOpt intLit
|   "ACTION" EqOpt ResourceGroupRunawayActionOption
|   "WATCH" EqOpt ResourceGroupRunawayWatchOption WatchDurationOption

WatchDurationOption ::=
    ("DURATION" EqOpt stringLit | "DURATION" EqOpt "UNLIMITED")?

ResourceGroupRunawayWatchOption ::=
    EXACT
|   SIMILAR
|   PLAN

ResourceGroupRunawayActionOption ::=
    DRYRUN
|   COOLDOWN
|   KILL
| "SWITCH_GROUP" '(' ResourceGroupName ')'
```

资源组名称参数（`ResourceGroupName`）必须在全局范围内唯一。

TiDB 支持以下 `DirectResourceGroupOption`，其中 [Request Unit (RU)](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru) 是 TiDB 中对 CPU、IO 及其他系统资源的统一抽象单位。

| 选项         | 描述                                   | 示例                    |
|--------------|----------------------------------------|-------------------------|
| `RU_PER_SEC` | 每秒回填 RU 的速率                     | `RU_PER_SEC = 500` 表示该资源组每秒回填 500 个 RU    |
| `PRIORITY`   | 在 TiKV 上处理任务的绝对优先级          | `PRIORITY = HIGH` 表示优先级为高。如果未指定，默认值为 `MEDIUM`。 |
| `BURSTABLE`  | 如果设置了 `BURSTABLE` 属性，TiDB 允许对应的资源组在超出配额时使用可用的系统资源。 |
| `QUERY_LIMIT`| 当查询执行满足该条件时，查询会被识别为异常查询并执行相应操作。 | `QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=KILL, WATCH=EXACT DURATION='10m')` 表示当查询执行时间超过 60 秒时，该查询会被识别为异常查询并被终止。所有 SQL 文本相同的 SQL 语句将在接下来的 10 分钟内被立即终止。`QUERY_LIMIT=()` 或 `QUERY_LIMIT=NULL` 表示未启用异常查询控制。详见 [异常查询](/tidb-resource-control-runaway-queries.md)。 |

> **Note:**
>
> - 只有当全局变量 [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660) 设置为 `ON` 时，才能执行 `CREATE RESOURCE GROUP` 语句。
> TiDB 在集群初始化时会自动创建一个 `default` 资源组。对于该资源组，`RU_PER_SEC` 的默认值为 `UNLIMITED`（等同于 `INT` 类型的最大值，即 `2147483647`），并且处于 `BURSTABLE` 模式。所有未绑定到任何资源组的请求会自动绑定到该 `default` 资源组。当你为其他资源组创建新配置时，建议根据需要修改 `default` 资源组的配置。
> - 当前仅支持在 `default` 资源组上修改 `BACKGROUND` 配置。

## 示例

创建两个资源组 `rg1` 和 `rg2`。

```sql
DROP RESOURCE GROUP IF EXISTS rg1;
```

```sql
Query OK, 0 rows affected (0.22 sec)
```

```sql
CREATE RESOURCE GROUP IF NOT EXISTS rg1
  RU_PER_SEC = 100
  PRIORITY = HIGH
  BURSTABLE;
```

```sql
Query OK, 0 rows affected (0.08 sec)
```

```sql
CREATE RESOURCE GROUP IF NOT EXISTS rg2
  RU_PER_SEC = 200 QUERY_LIMIT=(EXEC_ELAPSED='100ms', ACTION=KILL);
```

```sql
Query OK, 0 rows affected (0.08 sec)
```

```sql
SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1' or NAME = 'rg2';
```

```sql
+------+------------+----------+-----------+---------------------------------+
| NAME | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT                     |
+------+------------+----------+-----------+---------------------------------+
| rg1  | 100        | HIGH     | YES       | NULL                            |
| rg2  | 200        | MEDIUM   | NO        | EXEC_ELAPSED=100ms, ACTION=KILL |
+------+------------+----------+-----------+---------------------------------+
2 rows in set (1.30 sec)
```

## MySQL 兼容性

MySQL 也支持 [CREATE RESOURCE GROUP](https://dev.mysql.com/doc/refman/8.0/en/create-resource-group.html)。但其可接受的参数与 TiDB 不同，因此两者不兼容。

## 另请参阅

* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
* [ALTER RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [ALTER USER RESOURCE GROUP](/sql-statements/sql-statement-alter-user.md#modify-the-resource-group-bound-to-the-user)
* [Request Unit (RU)](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru)
