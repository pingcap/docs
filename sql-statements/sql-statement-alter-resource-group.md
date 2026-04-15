---
title: ALTER RESOURCE GROUP
summary: TiDBにおけるALTER RESOURCE GROUPの使い方を学びましょう。
---

# アルター・リソース・グループ {#alter-resource-group}

`ALTER RESOURCE GROUP`ステートメントは、データベース内のリソース グループを変更するために使用されます。

> **注記：**
>
> この機能は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

## あらすじ {#synopsis}

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

TiDB は、次の`DirectResourceGroupOption`をサポートします。ここで[リクエストユニット（RU）](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru)は、CPU、IO、およびその他のシステム リソースに対する TiDB の統合抽象化ユニットです。

| オプション         | 説明                                                                                               | 例                                                                                                                                                                                                                                                                                                                |
| ------------- | ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `RU_PER_SEC`  | RUのバックフィル速度（1秒あたり）                                                                               | `RU_PER_SEC = 500`は、このリソースグループが毎秒500 RUでバックフィルされていることを示します。                                                                                                                                                                                                                                                      |
| `PRIORITY`    | TiKVで処理されるタスクの絶対的な優先順位                                                                           | `PRIORITY = HIGH`は優先度が高いことを示します。指定しない場合、デフォルト値は`MEDIUM`です。                                                                                                                                                                                                                                                       |
| `BURSTABLE`   | `BURSTABLE`属性が設定されている場合、TiDBは、割り当て量を超過したときに、対応するリソースグループが利用可能なシステムリソースを使用することを許可します。             |                                                                                                                                                                                                                                                                                                                  |
| `QUERY_LIMIT` | クエリの実行がこの条件を満たした場合、そのクエリは暴走クエリとして識別され、対応するアクションが実行されます。                                          | `QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=KILL, WATCH=EXACT DURATION='10m')`は、実行時間が 60 秒を超えた場合にクエリが暴走クエリとして識別されたことを示します。クエリは終了されます。同じ SQL テキストを持つすべての SQL ステートメントは、今後 10 分以内に直ちに終了します。 `QUERY_LIMIT=()`または`QUERY_LIMIT=NULL`は、暴走制御が有効になっていないことを意味します。 [暴走クエリ](/tidb-resource-control-runaway-queries.md)参照してください。 |
| `BACKGROUND`  | バックグラウンドタスクを設定します。詳細については、 [バックグラウンドタスクの管理](/tidb-resource-control-background-tasks.md)参照してください。 | `BACKGROUND=(TASK_TYPES="br,stats", UTILIZATION_LIMIT=30)`は、バックアップと復元、統計情報の収集に関連するタスクがバックグラウンドタスクとしてスケジュールされ、バックグラウンドタスクはTiKVリソースの最大30%を消費できることを示しています。                                                                                                                                                          |

> **注記：**
>
> -   `ALTER RESOURCE GROUP`ステートメントは、グローバル変数[`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660)が`ON`に設定されている場合にのみ実行できます。
> -   `ALTER RESOURCE GROUP`ステートメントは、指定されていないパラメーターを変更せずに、増分的な変更をサポートします。ただし、 `QUERY_LIMIT`と`BACKGROUND`は全体として使用されるため、部分的に変更することはできません。
> -   現在、 `default`リソース グループのみが`BACKGROUND`構成の変更をサポートしています。

## 例 {#examples}

`rg1`という名前のリソースグループを作成し、そのプロパティを変更します。

```sql
DROP RESOURCE GROUP IF EXISTS rg1;
```

    Query OK, 0 rows affected (0.22 sec)

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

`BACKGROUND`リソース グループの`default` } オプションを変更します。

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

## MySQLとの互換性 {#mysql-compatibility}

MySQL は[アルター・リソース・グループ](https://dev.mysql.com/doc/refman/8.0/en/alter-resource-group.html)もサポートしています。ただし、受け入れられるパラメータが TiDB とは異なるため、互換性はありません。

## 関連項目 {#see-also}

-   [リソースグループを削除する](/sql-statements/sql-statement-drop-resource-group.md)
-   [リソースグループを作成する](/sql-statements/sql-statement-create-resource-group.md)
-   [リクエストユニット（RU）](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru)
