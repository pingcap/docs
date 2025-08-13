---
title: Manage Queries That Consume More Resources Than Expected (Runaway Queries)
summary: リソース管理機能を通じて、リソースを過剰に消費するクエリ (ランナウェイ クエリ) を制御および低下させる方法を紹介します。
---

# 予想よりも多くのリソースを消費するクエリ（ランナウェイクエリ）を管理する {#manage-queries-that-consume-more-resources-than-expected-runaway-queries}

> **注記：**
>
> この機能は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では利用できません。

ランナウェイクエリとは、予想よりも多くの時間やリソースを消費するクエリです。以下では、ランナウェイクエリを管理する機能を説明するために「ランナ**ウェイクエリ」という**用語を使用します。

-   バージョン7.2.0以降、リソース制御機能にランナウェイクエリの管理機能が導入されました。リソースグループに対してランナウェイクエリを特定するための条件を設定し、ランナウェイクエリによるリソースの枯渇や他のクエリへの影響を防ぐためのアクションを自動的に実行できます。3 または[`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md) [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md) `QUERY_LIMIT`フィールドを含めることで、リソースグループのランナウェイクエリを管理できます。
-   バージョン7.3.0以降、リソース制御機能にランナウェイ・ウォッチの手動管理が導入され、特定のSQL文またはダイジェストに対するランナウェイ・クエリを迅速に特定できるようになりました。ステートメント[`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md)実行することで、リソースグループ内のランナウェイ・クエリ・ウォッチリストを手動で管理できます。

リソース制御機能の詳細については、 [リソース制御を使用してリソースグループの制限とフロー制御を実現する](/tidb-resource-control-ru-groups.md)参照してください。

## <code>QUERY_LIMIT</code>パラメータ {#code-query-limit-code-parameters}

クエリが次のいずれかの制限を超えると、ランナウェイ クエリとして識別されます。

-   `EXEC_ELAPSED` : クエリ実行時間が制限を超えていないかどうかを確認します。このルールは、読み取りおよび書き込みDMLステートメントに適用されます。
-   `PROCESSED_KEYS` :コプロセッサーによって処理されるキーの数が制限を超えていないかどうかをチェックします。このルールは読み取りステートメントにのみ適用されます。
-   `RU` : ステートメントによって消費される読み取りおよび書き込み RU の合計数が制限を超えているかどうかを確認します。このルールは読み取りステートメントにのみ適用されます。

サポートされている操作（ `ACTION` ）：

-   `DRYRUN` ：アクションは実行されません。ランナウェイクエリのレコードが追加されます。これは主に、条件設定が適切かどうかを観察するために使用されます。
-   `COOLDOWN` : クエリの実行優先度が最低レベルに下げられます。クエリは最低優先度で実行を継続し、他の操作のリソースを占有しません。
-   `KILL` : 識別されたクエリは自動的に終了され、エラー`Query execution was interrupted, identified as runaway query`が報告されます。
-   `SWITCH_GROUP` : バージョン8.4.0で導入されたこのパラメータは、指定されたクエリを指定されたリソースグループに切り替えて実行を継続します。このクエリが完了すると、後続のSQL文は元のリソースグループで実行されます。指定されたリソースグループが存在しない場合、クエリは元のリソースグループに残ります。

システムリソースを枯渇させる過剰な同時実行のランナウェイクエリを回避するために、リソース制御機能では、ランナウェイクエリを迅速に識別して分離できる迅速な識別メカニズムを導入しています。 `WATCH`句を通じてこの機能を使用できます。クエリがランナウェイクエリとして識別されると、このメカニズムはクエリの一致する特徴 ( `WATCH`後のパラメータで定義) を抽出します。次の期間 ( `DURATION`で定義) に、ランナウェイクエリの一致する特徴が監視リストに追加され、TiDB インスタンスはクエリを監視リストと照合します。一致したクエリは、条件によって識別されるのを待つのではなく、直接ランナウェイクエリとしてマークされ、対応するアクションに従って分離されます。 `KILL`操作はクエリを終了し、エラー`Quarantined and interrupted because of being in runaway watch list`を報告します。

`WATCH`素早く識別するために一致させる方法は 3 つあります。

-   `EXACT` 、まったく同じ SQL テキストを持つ SQL ステートメントのみが迅速に識別されることを示します。
-   `SIMILAR` 、同じパターンを持つすべての SQL ステートメントが SQL ダイジェストに一致し、リテラル値が無視されることを示します。
-   `PLAN` 、同じパターンを持つすべての SQL ステートメントがプラン ダイジェストに一致することを示します。

`WATCH`の`DURATION`オプションは識別項目の有効期間を示し、デフォルトでは無期限です。

監視項目を追加した後、 `QUERY_LIMIT`設定が変更または削除されても、対応する機能と`ACTION`変更または削除されません。監視項目を削除するには`QUERY WATCH REMOVE`使用します。

`QUERY_LIMIT`のパラメータは次のとおりです。

| パラメータ            | 説明                                                                       | 注記                                                                                           |
| ---------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- |
| `EXEC_ELAPSED`   | クエリ実行時間がこの値を超えると、暴走クエリとして識別されます。                                         | EXEC_ELAPSED = `60s` 、クエリの実行に 60 秒以上かかる場合、クエリがランナウェイ クエリとして識別されることを意味します。                    |
| `PROCESSED_KEYS` | コプロセッサーによって処理されるキーの数がこの値を超えると、クエリは暴走クエリとして識別されます。                        | `PROCESSED_KEYS = 1000` 、コプロセッサーによって処理されるキーの数が 1000 を超える場合に、クエリがランナウェイ クエリとして識別されることを意味します。  |
| `RU`             | クエリによって消費される読み取りおよび書き込みRUの合計数がこの値を超えると、このクエリはランナウェイクエリとして識別されます。         | `RU = 1000` 、クエリによって消費される読み取り RU と書き込み RU の合計数が 1000 を超える場合に、クエリがランナウェイ クエリとして識別されることを意味します。 |
| `ACTION`         | 暴走クエリが特定された場合に実行されるアクション                                                 | オプションの値は`DRYRUN` 、 `COOLDOWN` 、 `KILL` 、 `SWITCH_GROUP`です。                                   |
| `WATCH`          | 特定されたランナウェイクエリを迅速に照合します。一定時間内に同一または類似のクエリが再度検出された場合、対応するアクションが直ちに実行されます。 | オプション。たとえば、 `WATCH=SIMILAR DURATION '60s'` 、 `WATCH=EXACT DURATION '1m'` 、 `WATCH=PLAN`などです。 |

> **注記：**
>
> ランナウェイクエリを特定のリソースグループに厳密に制限したい場合は、 `SWITCH_GROUP`と[`QUERY WATCH`](#query-watch-parameters)ステートメントを併用することをお勧めします。5 `QUERY_LIMIT` 、クエリが条件を満たした場合にのみ対応する`ACTION`操作をトリガーするため、このようなシナリオでは`SWITCH_GROUP`クエリを適切なタイミングで対象のリソースグループに切り替えられない可能性があります。

## 例 {#examples}

1.  1 秒あたり 500 RU のクォータを持つリソース グループ`rg1`を作成し、60 秒を超えるクエリをランナウェイ クエリとして定義し、ランナウェイ クエリの優先順位を下げます。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg1 RU_PER_SEC = 500 QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=COOLDOWN);
    ```

2.  `rg1`リソース グループを変更してランナウェイ クエリを終了し、次の 10 分以内に同じパターンのクエリをランナウェイ クエリとして直ちにマークします。

    ```sql
    ALTER RESOURCE GROUP rg1 QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=KILL, WATCH=SIMILAR DURATION='10m');
    ```

3.  ランナウェイ クエリ チェックをキャンセルするには、 `rg1`リソース グループを変更します。

    ```sql
    ALTER RESOURCE GROUP rg1 QUERY_LIMIT=NULL;
    ```

## <code>QUERY WATCH</code>パラメータ {#code-query-watch-code-parameters}

`QUERY WATCH`のあらすじについては[`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md)ご覧ください。

パラメータは次のとおりです。

-   `RESOURCE GROUP`リソースグループを指定します。このステートメントによって追加されたランナウェイクエリの一致する特徴は、リソースグループのウォッチリストに追加されます。このパラメータは省略可能です。省略した場合、 `default`リソースグループに適用されます。

-   `ACTION`の意味は`QUERY LIMIT`と同じです。このパラメータは省略可能です。省略した場合、識別後の対応するアクションは、リソースグループ内の`QUERY LIMIT`で設定された`ACTION`採用し、 `QUERY LIMIT`設定によってアクションは変更されません。リソースグループ内に`ACTION`が設定されていない場合は、エラーが報告されます。

-   `QueryWatchTextOption`パラメータには、 `SQL DIGEST` 、 `PLAN DIGEST` 、 `SQL TEXT` 3 つのオプションがあります。
    -   `SQL DIGEST`は`SIMILAR`と同じです。以下のパラメータは、文字列、ユーザー定義変数、または文字列を返すその他の式を受け入れます。文字列の長さは、TiDBのダイジェスト定義と同じ64文字である必要があります。
    -   `PLAN DIGEST`は`PLAN`と同じです。次のパラメータはダイジェスト文字列です。
    -   `SQL TEXT`入力SQLを生の文字列（ `EXACT` ）として一致するか、または次のパラメータに応じてそれを解析して`SQL DIGEST` （ `SIMILAR` ）または`PLAN DIGEST` （ `PLAN` ）にコンパイルします。

-   デフォルトのリソース グループのランナウェイ クエリ監視リストに一致する機能を追加します (事前にデフォルトのリソース グループに`QUERY LIMIT`設定する必要があります)。

    ```sql
    QUERY WATCH ADD ACTION KILL SQL TEXT EXACT TO 'select * from test.t2';
    ```

-   SQLをSQLダイジェストに解析することで、リソースグループ`rg1`ランナウェイクエリ監視リストに一致する機能を追加します。3 `ACTION`指定されていない場合は、リソースグループ`rg1`に既に設定されているオプション`ACTION`使用されます。

    ```sql
    QUERY WATCH ADD RESOURCE GROUP rg1 SQL TEXT SIMILAR TO 'select * from test.t2';
    ```

-   SQL を SQL ダイジェストに解析して、 `rg1`リソース グループのランナウェイ クエリ監視リストに一致する機能を追加し、 `ACTION`を`SWITCH_GROUP(rg2)`として指定します。

    ```sql
    QUERY WATCH ADD RESOURCE GROUP rg1 ACTION SWITCH_GROUP(rg2) SQL TEXT SIMILAR TO 'select * from test.t2';
    ```

-   `PLAN DIGEST`使用して`rg1`リソース グループのランナウェイ クエリ監視リストに一致する機能を追加し、 `ACTION` `KILL`として指定します。

    ```sql
    QUERY WATCH ADD RESOURCE GROUP rg1 ACTION KILL PLAN DIGEST 'd08bc323a934c39dc41948b0a073725be3398479b6fa4f6dd1db2a9b115f7f57';
    ```

-   `INFORMATION_SCHEMA.RUNAWAY_WATCHES`クエリしてウォッチ アイテム ID を取得し、ウォッチ アイテムを削除します。

    ```sql
    SELECT * from information_schema.runaway_watches ORDER BY id\G
    ```

    ```sql
    *************************** 1. row ***************************
                     ID: 1
    RESOURCE_GROUP_NAME: default
             START_TIME: 2024-09-09 03:35:31
               END_TIME: 2024-09-09 03:45:31
                  WATCH: Exact
            WATCH_TEXT: SELECT variable_name, variable_value FROM mysql.global_variables
                 SOURCE: 127.0.0.1:4000
                ACTION: Kill
                RULE: ProcessedKeys = 666(10)
    1 row in set (0.00 sec)
    ```

    ```sql
    QUERY WATCH REMOVE 1;
    ```

## 可観測性 {#observability}

ランナウェイ クエリに関する詳細情報は、次のシステム テーブルと`INFORMATION_SCHEMA`から取得できます。

-   `mysql.tidb_runaway_queries`テーブルには、過去 7 日間に特定されたすべてのランナウェイクエリの履歴レコードが含まれています。例として、1 つの行を見てみましょう。

    ```sql
    MySQL [(none)]> SELECT * FROM mysql.tidb_runaway_queries LIMIT 1\G
    *************************** 1. row ***************************
    resource_group_name: default
         start_time: 2024-09-09 17:43:42
            repeats: 2
         match_type: watch
             action: kill
         sample_sql: select sleep(2) from t
         sql_digest: 4adbc838b86c573265d4b39a3979d0a362b5f0336c91c26930c83ab187701a55
        plan_digest: 5d094f78efbce44b2923733b74e1d09233cb446318293492901c5e5d92e27dbc
        tidb_server: 127.0.0.1:4000
    ```

    フィールドの説明:

    -   `start_time` 、ランナウェイ クエリが識別された時間を示します。
    -   `repeats` 、 `start_time`以降にランナウェイクエリが識別された回数を示します。
    -   `match_type` 、ランナウェイクエリの識別方法を示します。値は次のいずれかになります。
        -   `identify`ランナウェイクエリの条件に一致することを意味します。
        -   `watch` 、監視リスト内のクイック識別ルールに一致することを意味します。

-   `information_schema.runaway_watches`表には、ランナウェイクエリのクイック識別ルールの記録が含まれています。詳細については、 [`RUNAWAY_WATCHES`](/information-schema/information-schema-runaway-watches.md)参照してください。
