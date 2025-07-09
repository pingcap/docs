---
title: CREATE RESOURCE GROUP
summary: TiDB での CREATE RESOURCE GROUP の使用方法を学習します。
---

# リソースグループの作成 {#create-resource-group}

`CREATE RESOURCE GROUP`ステートメントを使用してリソース グループを作成できます。

> **注記：**
>
> この機能は[{{{ .スターター }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)クラスターでは利用できません。

## 概要 {#synopsis}

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

リソースグループ名パラメータ（ `ResourceGroupName` ）はグローバルに一意である必要があります。

TiDB は次の`DirectResourceGroupOption`サポートします[リクエストユニット（RU）](/tidb-resource-control.md#what-is-request-unit-ru)は、CPU、IO、およびその他のシステム リソース用の TiDB 内の統一された抽象化単位です。

| オプション         | 説明                                                                                    | 例                                                                                                                                                                                                                                                                                                                                                               |
| ------------- | ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `RU_PER_SEC`  | 1秒あたりのRUバックフィル速度                                                                      | `RU_PER_SEC = 500` 、このリソース グループが 1 秒あたり 500 RU でバックフィルされることを示します。                                                                                                                                                                                                                                                                                               |
| `PRIORITY`    | TiKVで処理されるタスクの絶対的な優先度                                                                 | `PRIORITY = HIGH`優先度が高いことを示します。指定されていない場合は、デフォルト値は`MEDIUM`です。                                                                                                                                                                                                                                                                                                   |
| `BURSTABLE`   | `BURSTABLE`属性が設定されている場合、TiDB は、クォータを超えたときに、対応するリソース グループが使用可能なシステム リソースを使用することを許可します。 |                                                                                                                                                                                                                                                                                                                                                                 |
| `QUERY_LIMIT` | クエリ実行がこの条件を満たす場合、クエリはランナウェイ クエリとして識別され、対応するアクションが実行されます。                              | `QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=KILL, WATCH=EXACT DURATION='10m')` 、実行時間が60秒を超えた場合にクエリがランナウェイクエリと識別されることを示します。クエリは終了します。同じSQLテキストを持つすべてのSQL文は、今後10分以内に即時終了します。2または`QUERY_LIMIT=NULL` `QUERY_LIMIT=()`ランナウェイ制御が無効であることを意味します。6 [ランナウェイクエリ](/tidb-resource-control.md#manage-queries-that-consume-more-resources-than-expected-runaway-queries)参照してください。 |

> **注記：**
>
> -   `CREATE RESOURCE GROUP`文は、グローバル変数[`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660) `ON`に設定されている場合にのみ実行できます。TiDB は、クラスタの初期化中に`default`リソースグループを自動的に作成します。このリソースグループでは、デフォルト値`RU_PER_SEC`は`UNLIMITED` （ `INT`タイプの最大値である`2147483647`に相当）に設定され、 `BURSTABLE`モードになります。どのリソースグループにもバインドされていないすべてのリクエストは、この`default`リソースグループに自動的にバインドされます。別のリソースグループの新しい構成を作成する場合は、必要に応じて`default`リソースグループの設定を変更することをお勧めします。
> -   現在、 `BACKGROUND`構成の変更をサポートしているのは`default`リソース グループのみです。

## 例 {#examples}

2 つのリソース グループ`rg1`と`rg2`作成します。

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

MySQLも[リソースグループの作成](https://dev.mysql.com/doc/refman/8.0/en/create-resource-group.html)サポートしています。ただし、許容されるパラメータがTiDBと異なるため、互換性がありません。

## 参照 {#see-also}

-   [リソースグループの削除](/sql-statements/sql-statement-drop-resource-group.md)
-   [リソースグループの変更](/sql-statements/sql-statement-alter-resource-group.md)
-   [ユーザーリソースグループの変更](/sql-statements/sql-statement-alter-user.md#modify-the-resource-group-bound-to-the-user)
-   [リクエストユニット（RU）](/tidb-resource-control.md#what-is-request-unit-ru)
