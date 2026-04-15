---
title: CREATE RESOURCE GROUP
summary: TiDBにおけるCREATE RESOURCE GROUPの使い方を学びましょう。
---

# リソースグループを作成する {#create-resource-group}

`CREATE RESOURCE GROUP`ステートメントを使用してリソース グループを作成できます。

> **注記：**
>
> この機能は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

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

リソースグループ名パラメータ（ `ResourceGroupName` ）は、グローバルに一意である必要があります。

TiDB は、次の`DirectResourceGroupOption`をサポートします。ここで[リクエストユニット（RU）](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru)は、CPU、IO、およびその他のシステム リソースに対する TiDB の統合抽象化ユニットです。

| オプション         | 説明                                                                                   | 例                                                                                                                                                                                                                                                                                                                |
| ------------- | ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `RU_PER_SEC`  | RUのバックフィル速度（1秒あたり）                                                                   | `RU_PER_SEC = 500`は、このリソースグループが毎秒500 RUでバックフィルされていることを示します。                                                                                                                                                                                                                                                      |
| `PRIORITY`    | TiKVで処理されるタスクの絶対的な優先順位                                                               | `PRIORITY = HIGH`は優先度が高いことを示します。指定しない場合、デフォルト値は`MEDIUM`です。                                                                                                                                                                                                                                                       |
| `BURSTABLE`   | `BURSTABLE`属性が設定されている場合、TiDBは、割り当て量を超過したときに、対応するリソースグループが利用可能なシステムリソースを使用することを許可します。 |                                                                                                                                                                                                                                                                                                                  |
| `QUERY_LIMIT` | クエリの実行がこの条件を満たした場合、そのクエリは暴走クエリとして識別され、対応するアクションが実行されます。                              | `QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=KILL, WATCH=EXACT DURATION='10m')`は、実行時間が 60 秒を超えた場合にクエリが暴走クエリとして識別されたことを示します。クエリは終了されます。同じ SQL テキストを持つすべての SQL ステートメントは、今後 10 分以内に直ちに終了します。 `QUERY_LIMIT=()`または`QUERY_LIMIT=NULL`は、暴走制御が有効になっていないことを意味します。 [暴走クエリ](/tidb-resource-control-runaway-queries.md)参照してください。 |

> **注記：**
>
> -   `CREATE RESOURCE GROUP`ステートメントは、グローバル変数[`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660)が`ON`に設定されている場合にのみ実行できます。 TiDB は、クラスタ初期化時に`default`リソース グループを自動的に作成します。 このリソース グループの`RU_PER_SEC`のデフォルト値は`UNLIMITED` ( `INT`型の最大値、つまり`2147483647`に相当) であり、 `BURSTABLE`モードです。いずれのリソースグループにも紐付けられていないすべてのリクエストは、自動的にこの`default`リソースグループに紐付けられます。別のリソースグループの新しい構成を作成する場合は、必要に応じて`default`リソースグループの構成を変更することをお勧めします。
> -   現在、 `default`リソース グループのみが`BACKGROUND`構成の変更をサポートしています。

## 例 {#examples}

`rg1`と`rg2` 2 つのリソース グループを作成します。

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

## MySQLとの互換性 {#mysql-compatibility}

MySQL は[リソースグループを作成する](https://dev.mysql.com/doc/refman/8.0/en/create-resource-group.html)もサポートしています。ただし、受け入れられるパラメータが TiDB とは異なるため、互換性はありません。

## 関連項目 {#see-also}

-   [リソースグループを削除する](/sql-statements/sql-statement-drop-resource-group.md)
-   [アルター・リソース・グループ](/sql-statements/sql-statement-alter-resource-group.md)
-   [ユーザーリソースグループの変更](/sql-statements/sql-statement-alter-user.md#modify-the-resource-group-bound-to-the-user)
-   [リクエストユニット（RU）](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru)
