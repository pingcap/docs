---
title: ALTER RESOURCE GROUP
summary: 了解在 TiDB 中 ALTER RESOURCE GROUP 的用法。
---

# ALTER RESOURCE GROUP

`ALTER RESOURCE GROUP` 语句用于修改数据库中的资源组。

> **Note:**
>
> 此功能在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 和 [Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。

## 语法

```ebnf+diagram
AlterResourceGroupStmt ::=
   "ALTER" "RESOURCE" "GROUP" IfExists ResourceGroupName ResourceGroupOptionList

IfExists ::=
    ('IF' 'EXISTS')?

ResourceGroupName ::=
    Identifier
|   "DEFAULT"

ResourceGroupOptionList ::=
    DirectResourceGroupOption
|   ResourceGroupOptionList DirectResourceGroupOption
|   ResourceGroupOptionList ',' DirectResourceGroupOption

DirectResourceGroupOption ::=
    "RU_PER_SEC" EqOpt LengthNum
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
|   "WATCH" EqOpt ResourceGroupRunawayWatchOption "DURATION" EqOpt stringLit

ResourceGroupRunawayWatchOption ::=
    EXACT
|   SIMILAR

ResourceGroupRunawayActionOption ::=
    DRYRUN
|   COOLDOWN
|   KILL
| "SWITCH_GROUP" '(' ResourceGroupName ')'

BackgroundOptionList ::=
    DirectBackgroundOption
|   BackgroundOptionList DirectBackgroundOption
|   BackgroundOptionList ',' DirectBackgroundOption

DirectBackgroundOption ::=
    "TASK_TYPES" EqOpt stringLit
|   "UTILIZATION_LIMIT" EqOpt LengthNum
```

TiDB 支持以下 `DirectResourceGroupOption`，其中 [请求单元（RU）](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru) 是 TiDB 中对 CPU、IO 及其他系统资源的统一抽象单位。

| 选项           | 描述                                                         | 示例                                                                                                   |
|----------------|--------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| `RU_PER_SEC`   | 每秒回填的 RU 速率                                           | `RU_PER_SEC = 500` 表示该资源组每秒回填 500 个 RU                                                      |
| `PRIORITY`     | 在 TiKV 上待处理任务的绝对优先级                             | `PRIORITY = HIGH` 表示优先级为高。如果未指定，默认值为 `MEDIUM`。                                       |
| `BURSTABLE`    | 如果设置了 `BURSTABLE` 属性，TiDB 允许对应资源组在超出配额时使用可用的系统资源。 |
| `QUERY_LIMIT`  | 当查询执行满足该条件时，查询会被识别为异常查询并执行相应操作。 | `QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=KILL, WATCH=EXACT DURATION='10m')` 表示当查询执行时间超过 60 秒时，该查询会被识别为异常查询并被终止。所有 SQL 文本相同的 SQL 语句将在接下来的 10 分钟内被立即终止。`QUERY_LIMIT=()` 或 `QUERY_LIMIT=NULL` 表示未启用异常查询控制。详见 [异常查询](/tidb-resource-control-runaway-queries.md)。 |
| `BACKGROUND`   | 配置后台任务。更多详情参见 [管理后台任务](/tidb-resource-control-background-tasks.md)。 | `BACKGROUND=(TASK_TYPES="br,stats", UTILIZATION_LIMIT=30)` 表示备份恢复和统计信息收集相关任务被调度为后台任务，且后台任务最多可消耗 TiKV 资源的 30%。 |

> **Note:**
>
> - 只有当全局变量 [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660) 设置为 `ON` 时，才能执行 `ALTER RESOURCE GROUP` 语句。
> - `ALTER RESOURCE GROUP` 语句支持增量变更，未指定的参数保持不变。但 `QUERY_LIMIT` 和 `BACKGROUND` 作为整体使用，不能部分修改。
> - 目前，仅 `default` 资源组支持修改 `BACKGROUND` 配置。

## 示例

创建名为 `rg1` 的资源组并修改其属性。

```sql
DROP RESOURCE GROUP IF EXISTS rg1;
```

```
Query OK, 0 rows affected (0.22 sec)
```

```sql
CREATE RESOURCE GROUP IF NOT EXISTS rg1
  RU_PER_SEC = 100
  BURSTABLE;
```

```sql
Query OK, 0 rows affected (0.08 sec)
```

```sql
SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1';
```

```sql
+------+------------+----------+-----------+-------------+------------+
| NAME | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT | BACKGROUND |
+------+------------+----------+-----------+-------------+------------+
| rg1  | 100        | MEDIUM   | NO        | NULL        | NULL       |
+------+------------+----------+-----------+-------------+------------+
1 rows in set (1.30 sec)
```

```sql
ALTER RESOURCE GROUP rg1
  RU_PER_SEC = 200
  PRIORITY = LOW
  QUERY_LIMIT = (EXEC_ELAPSED='1s' ACTION=COOLDOWN WATCH=EXACT DURATION '30s');
```

```sql
Query OK, 0 rows affected (0.08 sec)
```

```sql
SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1';
```

```sql
+------+------------+----------+-----------+----------------------------------------------------------------+------------+
| NAME | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT                                                    | BACKGROUND |
+------+------------+----------+-----------+----------------------------------------------------------------+------------+
| rg1  | 200        | LOW      | NO        | EXEC_ELAPSED='1s', ACTION=COOLDOWN, WATCH=EXACT DURATION='30s' | NULL       |
+------+------------+----------+-----------+----------------------------------------------------------------+------------+
1 rows in set (1.30 sec)
```

修改 `default` 资源组的 `BACKGROUND` 选项。

```sql
ALTER RESOURCE GROUP default BACKGROUND = (TASK_TYPES = "br,ddl", UTILIZATION_LIMIT=30);
```

```sql
Query OK, 0 rows affected (0.08 sec)
```

```sql
SELECT * FROM information_schema.resource_groups WHERE NAME ='default';
```

```sql
+---------+------------+----------+-----------+-------------+-------------------------------------------+
| NAME    | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT | BACKGROUND                                |
+---------+------------+----------+-----------+-------------+-------------------------------------------+
| default | UNLIMITED  | MEDIUM   | YES       | NULL        | TASK_TYPES='br,ddl', UTILIZATION_LIMIT=30 |
+---------+------------+----------+-----------+-------------+-------------------------------------------+
1 rows in set (1.30 sec)
```

## MySQL 兼容性

MySQL 也支持 [ALTER RESOURCE GROUP](https://dev.mysql.com/doc/refman/8.0/en/alter-resource-group.html)。但其可接受的参数与 TiDB 不同，因此两者不兼容。

## 另请参阅

* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-create-resource-group.md)
* [请求单元（RU）](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru)
