---
title: CREATE RESOURCE GROUP
summary: Learn the usage of CREATE RESOURCE GROUP in TiDB.
---

# リソースグループの作成 {#create-resource-group}

`CREATE RESOURCE GROUP`ステートメントを使用してリソース グループを作成できます。

> **注記：**
>
> この機能は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

## あらすじ {#synopsis}

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
```

リソース グループ名パラメーター ( `ResourceGroupName` ) はグローバルに一意である必要があります。

TiDB は次の`DirectResourceGroupOption`サポートします。ここで[リクエストユニット (RU)](/tidb-resource-control.md#what-is-request-unit-ru) 、CPU、IO、およびその他のシステム リソースに対する TiDB 内の統合抽象化ユニットです。

| オプション         | 説明                                                                                     | 例                                                                                                                                                                                                                                                                                                                                                                       |
| ------------- | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `RU_PER_SEC`  | 1 秒あたりの RU バックフィルの速度                                                                   | `RU_PER_SEC = 500` 、このリソース グループが 1 秒あたり 500 RU でバックフィルされていることを示します                                                                                                                                                                                                                                                                                                      |
| `PRIORITY`    | TiKV 上で処理されるタスクの絶対的な優先度                                                                | `PRIORITY = HIGH`優先度が高いことを示します。指定しない場合、デフォルト値は`MEDIUM`です。                                                                                                                                                                                                                                                                                                               |
| `BURSTABLE`   | `BURSTABLE`属性が設定されている場合、TiDB は、クォータを超過したときに、対応するリソース グループが利用可能なシステム リソースを使用することを許可します。 |                                                                                                                                                                                                                                                                                                                                                                         |
| `QUERY_LIMIT` | クエリの実行がこの条件を満たす場合、クエリは暴走クエリとして識別され、対応するアクションが実行されます。                                   | `QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=KILL, WATCH=EXACT DURATION='10m')` 、実行時間が 60 秒を超えた場合にクエリが暴走クエリとして識別されることを示します。クエリは終了します。同じ SQL テキストを持つすべての SQL ステートメントは、今後 10 分間に直ちに終了されます。 `QUERY_LIMIT=()`または`QUERY_LIMIT=NULL`暴走制御が有効になっていないことを意味します。 [暴走クエリ](/tidb-resource-control.md#manage-queries-that-consume-more-resources-than-expected-runaway-queries)を参照してください。 |

> **注記：**
>
> -   `CREATE RESOURCE GROUP`ステートメントは、グローバル変数[`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660) `ON`に設定されている場合にのみ実行できます。 TiDB は、クラスターの初期化中に`default`リソース グループを自動的に作成します。このリソース グループのデフォルト値`RU_PER_SEC`は`UNLIMITED` ( `INT`タイプの最大値、つまり`2147483647`に相当) であり、 `BURSTABLE`モードです。どのリソース グループにもバインドされていないすべてのリクエストは、この`default`リソース グループに自動的にバインドされます。別のリソース グループの新しい構成を作成する場合は、必要に応じて`default`リソース グループの構成を変更することをお勧めします。
> -   現在、 `default`リソース グループのみが`BACKGROUND`構成の変更をサポートしています。

## 例 {#examples}

2 つのリソース グループ`rg1`および`rg2`を作成します。

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

## MySQLの互換性 {#mysql-compatibility}

MySQL は[リソースグループの作成](https://dev.mysql.com/doc/refman/8.0/en/create-resource-group.html)もサポートします。ただし、受け入れられるパラメータが TiDB とは異なるため、互換性はありません。

## こちらも参照 {#see-also}

-   [リソースグループを削除](/sql-statements/sql-statement-drop-resource-group.md)
-   [リソースグループの変更](/sql-statements/sql-statement-alter-resource-group.md)
-   [ユーザーリソースグループの変更](/sql-statements/sql-statement-alter-user.md#modify-the-resource-group-bound-to-the-user)
-   [リクエストユニット (RU)](/tidb-resource-control.md#what-is-request-unit-ru)
