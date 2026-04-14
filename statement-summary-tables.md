---
title: Statement Summary Tables
summary: TiDBのステートメントサマリーテーブルについて学びましょう。
---

# 明細書概要表 {#statement-summary-tables}

SQL のパフォーマンス問題をより適切に処理するために、MySQL は、統計情報を使用して SQL を監視するための`performance_schema`の[明細書概要表](https://dev.mysql.com/doc/refman/8.0/en/performance-schema-statement-summary-tables.html)を提供しています。これらのテーブルの中でも、 `events_statements_summary_by_digest`は、レイテンシー、実行時間、スキャンされた行数、フルテーブルスキャンなどの豊富なフィールドを備えているため、SQL の問題を特定する際に非常に役立ちます。

したがって、v4.0.0-rc.1 以降、TiDB は`information_schema`と機能面で類似したシステム テーブルを`performance_schema` } `events_statements_summary_by_digest`*ではなく*) で提供します。

-   [`statements_summary`](#statements_summary)
-   [`statements_summary_history`](#statements_summary_history)
-   [`cluster_statements_summary`](#statements_summary_evicted)
-   [`cluster_statements_summary_history`](#statements_summary_evicted)
-   [`statements_summary_evicted`](#statements_summary_evicted)

> **注記：**
>
> 上記の表は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスでは利用できません。

このドキュメントでは、これらのテーブルの詳細を説明し、SQLのパフォーマンス問題のトラブルシューティングにそれらを使用する方法を紹介します。

## <code>statements_summary</code> {#code-statements-summary-code}

`statements_summary`は`information_schema`内のシステム テーブルです。 `statements_summary`は、SQL ステートメントをリソース グループ、SQL ダイジェスト、およびプラン ダイジェストごとにグループ化し、各 SQL カテゴリの統計情報を提供します。

ここでいう「SQLダイジェスト」とは、スローログで使用されるものと同じ意味で、正規化されたSQLステートメントから計算される一意の識別子です。正規化プロセスでは定数や空白文字は無視され、大文字と小文字は区別されません。したがって、構文が一貫しているステートメントは同じダイジェストを持ちます。例：

```sql
SELECT * FROM employee WHERE id IN (1, 2, 3) AND salary BETWEEN 1000 AND 2000;
select * from EMPLOYEE where ID in (4, 5) and SALARY between 3000 and 4000;
```

正規化後、両者は以下のカテゴリに分類されます。

```sql
select * from employee where id in (...) and salary between ? and ?;
```

ここでいう「プランダイジェスト」とは、正規化された実行プランによって計算される一意の識別子を指します。正規化処理では定数は無視されます。同じSQL文でも実行プランが異なる場合があるため、異なるカテゴリに分類されることがあります。同じカテゴリのSQL文は、同じ実行プランを持ちます。

`statements_summary`は、SQL モニタリング メトリックの集計結果が格納されます。一般的に、各モニタリング メトリックには、最大値と平均値が含まれます。たとえば、実行レイテンシーメトリックは、 `AVG_LATENCY` (平均レイテンシー) と`MAX_LATENCY` (最大レイテンシー) の 2 つのフィールドに対応します。

監視メトリクスが最新の状態であることを確認するため、 `statements_summary`テーブルのデータは定期的にクリアされ、最新の集計結果のみが保持されて表示されます。定期的なデータクリアは、 `tidb_stmt_summary_refresh_interval`システム変数によって制御されます。クリア直後にクエリを実行すると、表示されるデータが非常に少なくなる場合があります。

以下は`statements_summary`をクエリした際の出力例です。

       SUMMARY_BEGIN_TIME: 2020-01-02 11:00:00
         SUMMARY_END_TIME: 2020-01-02 11:30:00
                STMT_TYPE: Select
              SCHEMA_NAME: test
                   DIGEST: 0611cc2fe792f8c146cc97d39b31d9562014cf15f8d41f23a4938ca341f54182
              DIGEST_TEXT: select * from employee where id = ?
              TABLE_NAMES: test.employee
              INDEX_NAMES: NULL
              SAMPLE_USER: root
               EXEC_COUNT: 3
              SUM_LATENCY: 1035161
              MAX_LATENCY: 399594
              MIN_LATENCY: 301353
              AVG_LATENCY: 345053
        AVG_PARSE_LATENCY: 57000
        MAX_PARSE_LATENCY: 57000
      AVG_COMPILE_LATENCY: 175458
      MAX_COMPILE_LATENCY: 175458
      ...........
                  AVG_MEM: 103
                  MAX_MEM: 103
                  AVG_DISK: 65535
                  MAX_DISK: 65535
        AVG_AFFECTED_ROWS: 0
               FIRST_SEEN: 2020-01-02 11:12:54
                LAST_SEEN: 2020-01-02 11:25:24
        QUERY_SAMPLE_TEXT: select * from employee where id=3100
         PREV_SAMPLE_TEXT:
              PLAN_DIGEST: f415b8d52640b535b9b12a9c148a8630d2c6d59e419aad29397842e32e8e5de3
                     PLAN:  Point_Get_1     root    1       table:employee, handle:3100

> **注記：**
>
> -   TiDBでは、ステートメントサマリーテーブルのフィールドの時間単位はナノ秒（ns）ですが、MySQLではピコ秒（ps）です。
> -   v7.5.1 および v7.6.0 以降、 が有効に[リソース制御](/tidb-resource-control-ru-groups.md)ているクラスターでは、 `statements_summary`リソース グループごとに集約されます。たとえば、異なるリソース グループで実行された同じステートメントは、異なるレコードとして収集されます。

## <code>statements_summary_history</code> {#code-statements-summary-history-code}

`statements_summary_history`のテーブルスキーマは`statements_summary`と同一です。 `statements_summary_history`は、特定の期間の履歴データを保存します。履歴データを確認することで、異常のトラブルシューティングや、異なる期間の監視メトリクスの比較を行うことができます。

`SUMMARY_BEGIN_TIME`フィールドと`SUMMARY_END_TIME`フィールドは、履歴期間の開始時刻と終了時刻を表します。

## <code>statements_summary_evicted</code> {#code-statements-summary-evicted-code}

[`tidb_stmt_summary_max_stmt_count`](/system-variables.md#tidb_stmt_summary_max_stmt_count-new-in-v40)システム変数は`statements_summary`テーブルと`statements_summary_history`テーブルがメモリに格納できる SQL ダイジェストの総数を制限します。この制限を超えると、TiDB は`statements_summary`テーブルと`statements_summary_history`テーブルの両方から、最も使用頻度の低い SQL ダイジェストを削除します。

<CustomContent platform="tidb">

> **注記：**
>
> [`tidb_stmt_summary_enable_persistent`](#persist-statements-summary)有効になっている場合、 `statements_summary_history`テーブルのデータはディスクに永続化されます。この場合、 `tidb_stmt_summary_max_stmt_count` 、 `statements_summary`テーブルがメモリに格納できる SQL ダイジェストの数のみを制限し、{{B-PLACEHOLDER-5-PLACEHOLDER- `tidb_stmt_summary_max_stmt_count` `statements_summary`から最も使用頻度の低い SQL ダイジェストのみを削除します。

</CustomContent>

`statements_summary_evicted`テーブルには、SQL ダイジェストが削除された期間と、その期間中に削除された SQL ダイジェストの数が記録されます。このテーブルは`tidb_stmt_summary_max_stmt_count`ワークロードに対して適切に構成されているかどうかを評価するのに役立ちます。このテーブルにレコードが含まれている場合、SQL ダイジェストの数が、ある時点で`tidb_stmt_summary_max_stmt_count`を超えたことを示しています。

<CustomContent platform="tidb">

[TiDBダッシュボードのSQLステートメントページ](/dashboard/dashboard-statement-list.md#others)では、削除されたステートメントに関する情報が`Others`行に表示されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

[診断ページの「SQLステートメント」タブ](/tidb-cloud/tune-performance.md#statement-analysis)では、削除されたステートメントに関する情報が`Others`行に表示されます。

</CustomContent>

## ステートメントサマリーの<code>cluster</code>テーブル {#the-code-cluster-code-tables-for-statement-summary}

`statements_summary` 、 `statements_summary_history` 、および`statements_summary_evicted`テーブルには、単一の TiDBサーバーのステートメントの概要のみが表示されます。クラスタ全体のデータを照会するには、 `cluster_statements_summary` 、 `cluster_statements_summary_history` 、または`cluster_statements_summary_evicted`テーブルを照会する必要があります。

`cluster_statements_summary`には、各 TiDBサーバーの`statements_summary`データが表示されます。 `cluster_statements_summary_history`には、各 TiDBサーバーの`statements_summary_history`データが表示されます。 `cluster_statements_summary_evicted`には、各 TiDBサーバーの`statements_summary_evicted`データが表示されます。これらのテーブルでは`INSTANCE`フィールドを使用して TiDBサーバーのアドレスを表します。その他のフィールドは`statements_summary` 、 `statements_summary_history` 、および`statements_summary_evicted`と同じです。

## パラメータ設定 {#parameter-configuration}

明細書の要約を制御するために、以下のシステム変数が使用されます。

-   `tidb_enable_stmt_summary` : 明細サマリー機能を有効にするかどうかを決定します。 `1`は`enable`を表し、 `0`は`disable`を意味します。この機能はデフォルトで有効になっています。この機能が無効になっている場合、システム テーブルの統計情報はクリアされます。統計情報は、次回この機能が有効になったときに再計算されます。テストの結果、この機能を有効にしてもパフォーマンスへの影響はほとんどないことがわかっています。

-   `tidb_stmt_summary_refresh_interval` : `statements_summary`テーブルが更新される間隔。時間の単位は秒 (s) です。デフォルト値は`1800`です。

-   `tidb_stmt_summary_history_size` : `statements_summary_history`テーブルに格納される各 SQL ステートメントカテゴリのサイズ。これは`statements_summary_evicted`テーブルの最大レコード数でもあります。デフォルト値は`24`です。

-   `tidb_stmt_summary_max_stmt_count` : `statements_summary`テーブルと`statements_summary_history`テーブルがメモリに格納できる SQL ダイジェストの総数を制限します。デフォルト値は`3000`です。

    この制限を超えると、TiDB は`statements_summary`テーブルと`statements_summary_history`テーブルの両方から、最も使用頻度の低い SQL ダイジェストを削除します。削除されたダイジェストは、 [`statements_summary_evicted`](#statements_summary_evicted)テーブルにカウントされます。

    > **注記：**
    >
    > -   SQLダイジェストが削除されると、関連するすべての時間範囲のサマリーデータが`statements_summary`テーブルと`statements_summary_history`テーブルの両方から削除されます。その結果、特定の時間範囲内のSQLダイジェストの数が制限を超えない場合でも、 `statements_summary_history`テーブルのSQLダイジェストの数が実際のSQLダイジェストの数よりも少なくなる可能性があります。このような状況が発生し、パフォーマンスに影響する場合は、 `tidb_stmt_summary_max_stmt_count`の値を増やすことをお勧めします。
    > -   TiDB Self-Managed の場合、 [`tidb_stmt_summary_enable_persistent`](#persist-statements-summary)が有効になっていると、 `statements_summary_history`テーブルのデータがディスクに永続化されます。この場合、 `tidb_stmt_summary_max_stmt_count` `statements_summary`テーブルがメモリに格納できる SQL ダイジェストの数のみを制限し、 `statements_summary` -E}} を超えると、TiDB は`tidb_stmt_summary_max_stmt_count`のみを削除します。

-   `tidb_stmt_summary_max_sql_length` : `DIGEST_TEXT`と`QUERY_SAMPLE_TEXT`の最長表示長を指定します。デフォルト値は`4096`です。

-   `tidb_stmt_summary_internal_query` : TiDB SQLステートメントをカウントするかどうかを決定します。 `1`はカウントすることを意味し、 `0`カウントしないことを意味します。デフォルト値は`0`です。

ステートメントサマリーの設定例を以下に示します。

```sql
set global tidb_stmt_summary_max_stmt_count = 3000;
set global tidb_enable_stmt_summary = true;
set global tidb_stmt_summary_refresh_interval = 1800;
set global tidb_stmt_summary_history_size = 24;
```

前述の設定が有効になると、 `statements_summary`テーブルは 30 分ごとにクリアされ、 `statements_summary_history`テーブルには最大 3000 種類の SQL ステートメントが格納されます。各タイプについて、 `statements_summary_history`テーブルには直近 24 期間のデータが格納されます。 `statements_summary_evicted`テーブルには、ステートメント サマリーから SQL ステートメントが削除された直近 24 期間が記録されます。 `statements_summary_evicted`テーブルは 30 分ごとに更新されます。

> **注記：**
>
> -   SQL タイプが毎分出現する場合、 `statements_summary_history`には直近 12 時間分のデータが格納されます。SQL タイプが毎日 00:00 から 00:30 の間にのみ出現する場合、 `statements_summary_history`には直近 24 期間分のデータが格納されます。各期間は 1 日です。したがって、 `statements_summary_history`にはこの SQL タイプに関する直近 24 日分のデータが格納されます。
> -   `tidb_stmt_summary_history_size` 、 `tidb_stmt_summary_max_stmt_count` 、および`tidb_stmt_summary_max_sql_length`構成項目はメモリ使用量に影響します。これらの構成は、ニーズ、SQLサイズ、SQL数、およびマシン構成に基づいて調整することをお勧めします。大きすぎる値を設定することはお勧めしません。メモリ使用量は`tidb_stmt_summary_history_size` * `tidb_stmt_summary_max_stmt_count` * `tidb_stmt_summary_max_sql_length` * `3` 。

### 明細書の要約に適切なサイズを設定してください。 {#set-a-proper-size-for-statement-summary}

システムが一定時間稼働した後（システム負荷に応じて）、 `statement_summary`テーブルを確認して、SQL の削除が発生したかどうかを確認できます。例:

```sql
select @@global.tidb_stmt_summary_max_stmt_count;
select count(*) from information_schema.statements_summary;
```

```sql
+-------------------------------------------+
| @@global.tidb_stmt_summary_max_stmt_count |
+-------------------------------------------+
| 3000                                      |
+-------------------------------------------+
1 row in set (0.001 sec)

+----------+
| count(*) |
+----------+
|     3001 |
+----------+
1 row in set (0.001 sec)
```

`statements_summary`テーブルにはレコードが満載されていることがわかります。次に、 `statements_summary_evicted`テーブルから削除されたデータを確認してください。

```sql
select * from information_schema.statements_summary_evicted;
```

```sql
+---------------------+---------------------+---------------+
| BEGIN_TIME          | END_TIME            | EVICTED_COUNT |
+---------------------+---------------------+---------------+
| 2020-01-02 16:30:00 | 2020-01-02 17:00:00 |            59 |
+---------------------+---------------------+---------------+
| 2020-01-02 16:00:00 | 2020-01-02 16:30:00 |            45 |
+---------------------+---------------------+---------------+
2 row in set (0.001 sec)
```

上記の結果から、最大で59個のSQLカテゴリが削除されることがわかります。この場合、 `statement_summary`テーブルのサイズを少なくとも59レコード増やすことをお勧めします。つまり、サイズを少なくとも3059レコードまで増やす必要があります。

## 制限 {#limitation}

デフォルトでは、ステートメントのサマリーテーブルはメモリに保存されます。TiDBサーバーが再起動すると、すべてのデータが失われます。

<CustomContent platform="tidb">

この問題を解決するため、TiDB v6.6.0では、デフォルトでは無効になっている[声明要約の持続性](#persist-statements-summary)機能を試験的に導入しました。この機能を有効にすると、履歴データはメモリに保存されず、直接ディスクに書き込まれます。これにより、TiDBサーバーが再起動しても履歴データは保持されます。

</CustomContent>

## 持続ステートメントの概要 {#persist-statements-summary}

<CustomContent platform="tidb-cloud">

このセクションは、TiDB Self-Managed にのみ適用されます。TiDB Cloudの場合、 `tidb_stmt_summary_enable_persistent`パラメータの値はデフォルトで`false`であり、動的な変更はサポートされていません。

</CustomContent>

> **警告：**
>
> 明細書の要約を永続化する機能は実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される場合があります。バグを発見した場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告してください。

<CustomContent platform="tidb">

で説明したように、ステートメントサマリーテーブルは[制限](#limitation)でメモリに保存されます。TiDBサーバーが再起動すると、すべてのステートメントサマリーが失われます。バージョン6.6.0以降、TiDBはステートメントサマリーの永続化を有効または無効にするための設定項目[`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-new-in-v660)試験的に提供しています。

</CustomContent>

<CustomContent platform="tidb-cloud">

[制限](#limitation)で説明されているように、ステートメントサマリーテーブルはデフォルトでメモリに保存されます。TiDBサーバーが再起動すると、すべてのステートメントサマリーが失われます。v6.6.0以降、TiDBは実験的に設定項目`tidb_stmt_summary_enable_persistent`を提供し、ユーザーがステートメントサマリーの永続化を有効または無効にできるようにしています。

</CustomContent>

ステートメントのサマリーを永続化するには、TiDB構成ファイルに次の構成項目を追加します。

```toml
[instance]
tidb_stmt_summary_enable_persistent = true
# The following entries use the default values, which can be modified as needed.
# tidb_stmt_summary_filename = "tidb-statements.log"
# tidb_stmt_summary_file_max_days = 3
# tidb_stmt_summary_file_max_size = 64 # MiB
# tidb_stmt_summary_file_max_backups = 0
```

ステートメントサマリーの永続化が有効になると、メモリには現在のリアルタイムデータのみが保持され、履歴データは保持されません。リアルタイムデータが履歴データとして更新されると、履歴データは、[パラメータ設定](#parameter-configuration)セクションで説明されている`tidb_stmt_summary_refresh_interval`間隔でディスクに書き込まれます。 `statements_summary_history`テーブルまたは`cluster_statements_summary_history`テーブルに対するクエリは、メモリ内データとディスク上のデータを組み合わせた結果を返します。

<CustomContent platform="tidb">

> **注記：**
>
> -   ステートメントサマリーの永続化が有効になっている場合、メモリが履歴データを保持しないため、[パラメータ設定](#parameter-configuration)セクションで説明されている`tidb_stmt_summary_history_size`構成は無効になります。代わりに、永続化のための履歴データの保持期間とサイズを制御するために、次の 3 つの構成が使用されます[`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-new-in-v660) 、 [`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-new-in-v660) 、および[`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-new-in-v660) 。
> -   `tidb_stmt_summary_refresh_interval`の値が小さいほど、ディスクに書き込まれるデータ量は多くなります。しかし、これは同時に、ディスクに書き込まれる冗長なデータ量も多くなることを意味します。

</CustomContent>

## トラブルシューティングの例 {#troubleshooting-examples}

このセクションでは、ステートメントサマリー機能を使用してSQLのパフォーマンス問題をトラブルシューティングする方法を示す2つの例を紹介します。

### SQLレイテンシーが高いのは、サーバー側の問題が原因でしょうか？ {#could-high-sql-latency-be-caused-by-the-server-end}

この例では、クライアントは`employee`テーブルに対するポイントクエリでパフォーマンスが低下しています。SQL テキストに対してあいまい検索を実行できます。

```sql
SELECT avg_latency, exec_count, query_sample_text
    FROM information_schema.statements_summary
    WHERE digest_text LIKE 'select * from employee%';
```

`1ms`と`0.3ms` `avg_latency`の正常範囲内にあると考えられます。したがって、サーバー側が原因ではないと結論付けられます。クライアント側またはネットワーク側でトラブルシューティングを行ってください。

```sql
+-------------+------------+------------------------------------------+
| avg_latency | exec_count | query_sample_text                        |
+-------------+------------+------------------------------------------+
|     1042040 |          2 | select * from employee where name='eric' |
|      345053 |          3 | select * from employee where id=3100     |
+-------------+------------+------------------------------------------+
2 rows in set (0.00 sec)
```

### どのカテゴリのSQL文が最も長い処理時間を要しますか？ {#which-categories-of-sql-statements-consume-the-longest-total-time}

10:00から10:30にかけてQPSが大幅に低下した場合、履歴テーブルから処理時間が最も長い3つのSQLステートメントのカテゴリを特定できます。

```sql
SELECT sum_latency, avg_latency, exec_count, query_sample_text
    FROM information_schema.statements_summary_history
    WHERE summary_begin_time='2020-01-02 10:00:00'
    ORDER BY sum_latency DESC LIMIT 3;
```

結果によると、以下の3つのカテゴリのSQL文が合計で最も長い時間を消費しており、これらは高い優先順位で最適化する必要がある。

```sql
+-------------+-------------+------------+-----------------------------------------------------------------------+
| sum_latency | avg_latency | exec_count | query_sample_text                                                     |
+-------------+-------------+------------+-----------------------------------------------------------------------+
|     7855660 |     1122237 |          7 | select avg(salary) from employee where company_id=2013                |
|     7241960 |     1448392 |          5 | select * from employee join company on employee.company_id=company.id |
|     2084081 |     1042040 |          2 | select * from employee where name='eric'                              |
+-------------+-------------+------------+-----------------------------------------------------------------------+
3 rows in set (0.00 sec)
```

## フィールドの説明 {#fields-description}

### <code>statements_summary</code>フィールドの説明 {#code-statements-summary-code-fields-description}

以下は`statements_summary`テーブルのフィールドの説明です。

基本フィールド:

-   `STMT_TYPE` : SQL ステートメントの種類。
-   `SCHEMA_NAME` : このカテゴリの SQL ステートメントが実行される現在のスキーマ。
-   `DIGEST` : このカテゴリの SQL ステートメントの要約。
-   `DIGEST_TEXT` : 正規化された SQL ステートメント。
-   `QUERY_SAMPLE_TEXT` : SQLカテゴリの元のSQLステートメント。元のステートメントは1つだけ取得されます。
-   `TABLE_NAMES` : SQL ステートメントに関係するすべてのテーブル。テーブルが複数ある場合は、それぞれをカンマで区切ります。
-   `INDEX_NAMES` : SQL文で使用されるすべてのSQLインデックス。インデックスが複数ある場合は、それぞれをカンマで区切ります。
-   `SAMPLE_USER` : このカテゴリの SQL ステートメントを実行するユーザー。1 人のユーザーのみが対象となります。
-   `PLAN_DIGEST` : 実行計画の概要。
-   `PLAN` : 元の実行プラン。複数のステートメントがある場合は、1つのステートメントのプランのみが使用されます。
-   `BINARY_PLAN` : バイナリ形式でエンコードされた元の実行プラン。複数のステートメントがある場合は、1つのステートメントのプランのみが使用されます。特定の実行プランを解析するには、 [`SELECT tidb_decode_binary_plan('xxx...')`](/functions-and-operators/tidb-functions.md#tidb_decode_binary_plan)ステートメントを実行してください。
-   `PLAN_CACHE_HITS` : このカテゴリの SQL ステートメントがプラン キャッシュにヒットした合計回数。
-   `PLAN_IN_CACHE` : このカテゴリの SQL ステートメントの以前の実行がプラン キャッシュにヒットしたかどうかを示します。
-   `PLAN_CACHE_UNQUALIFIED` : このカテゴリの SQL ステートメントがプラン キャッシュにヒットしなかった回数。
-   `PLAN_CACHE_UNQUALIFIED_LAST_REASON` : このカテゴリの SQL ステートメントが前回プラン キャッシュにヒットしなかった理由。

実行時間に関連するフィールド：

-   `SUMMARY_BEGIN_TIME` : 現在の集計期間の開始時刻。
-   `SUMMARY_END_TIME` : 現在の集計期間の終了時刻。
-   `FIRST_SEEN` : このカテゴリの SQL ステートメントが初めて出現する時刻。
-   `LAST_SEEN` : このカテゴリの SQL ステートメントが最後に表示される時刻。

<CustomContent platform="tidb">

TiDBサーバーに関連するフィールド：

-   `EXEC_COUNT` : このカテゴリの SQL ステートメントの合計実行時間。
-   `SUM_ERRORS` : 実行中に発生したエラーの合計。
-   `SUM_WARNINGS` : 実行中に発生した警告の合計。
-   `SUM_LATENCY` : このカテゴリの SQL ステートメントの合計実行レイテンシー。
-   `MAX_LATENCY` : このカテゴリの SQL ステートメントの最大実行レイテンシー。
-   `MIN_LATENCY` : このカテゴリの SQL ステートメントの最小実行レイテンシー。
-   `AVG_LATENCY` : このカテゴリの SQL ステートメントの平均実行レイテンシー。
-   `AVG_PARSE_LATENCY` : パーサーの平均レイテンシー。
-   `MAX_PARSE_LATENCY` : パーサーの最大レイテンシー。
-   `AVG_COMPILE_LATENCY` : コンパイラの平均レイテンシー。
-   `MAX_COMPILE_LATENCY` : コンパイラの最大レイテンシー。
-   `AVG_MEM` : 平均メモリ使用量（バイト）。
-   `MAX_MEM` : 使用される最大メモリ（バイト）。
-   `AVG_DISK` : 平均ディスク使用量（バイト）。
-   `MAX_DISK` : 使用される最大ディスク容量 (バイト)。
-   `AVG_TIDB_CPU_TIME` : このカテゴリの SQL ステートメントが消費する TiDBサーバーのCPU 時間の平均値。Top [Top SQL](/dashboard/top-sql.md)機能が有効になっている場合にのみ意味のある値が表示されます。それ以外の場合は、値は常に`0`になります。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDBサーバーに関連するフィールド：

-   `EXEC_COUNT` : このカテゴリの SQL ステートメントの合計実行時間。
-   `SUM_ERRORS` : 実行中に発生したエラーの合計。
-   `SUM_WARNINGS` : 実行中に発生した警告の合計。
-   `SUM_LATENCY` : このカテゴリの SQL ステートメントの合計実行レイテンシー。
-   `MAX_LATENCY` : このカテゴリの SQL ステートメントの最大実行レイテンシー。
-   `MIN_LATENCY` : このカテゴリの SQL ステートメントの最小実行レイテンシー。
-   `AVG_LATENCY` : このカテゴリの SQL ステートメントの平均実行レイテンシー。
-   `AVG_PARSE_LATENCY` : パーサーの平均レイテンシー。
-   `MAX_PARSE_LATENCY` : パーサーの最大レイテンシー。
-   `AVG_COMPILE_LATENCY` : コンパイラの平均レイテンシー。
-   `MAX_COMPILE_LATENCY` : コンパイラの最大レイテンシー。
-   `AVG_MEM` : 平均メモリ使用量（バイト）。
-   `MAX_MEM` : 使用される最大メモリ（バイト）。
-   `AVG_DISK` : 平均ディスク使用量（バイト）。
-   `MAX_DISK` : 使用される最大ディスク容量 (バイト)。
-   `AVG_TIDB_CPU_TIME` : このカテゴリの SQL ステートメントが消費する TiDBサーバーのCPU 時間の平均値。Top Top SQL機能が有効になっている場合にのみ意味のある値が表示されます。それ以外の場合は、値は常に`0`になります。

</CustomContent>

TiKVコプロセッサータスクに関連するフィールド：

-   `SUM_COP_TASK_NUM` : 送信されたコプロセッサー要求の総数。
-   `MAX_COP_PROCESS_TIME` :コプロセッサータスクの最大実行時間。
-   `MAX_COP_PROCESS_ADDRESS` : 実行時間が最大となるコプロセッサータスクのアドレス。
-   `MAX_COP_WAIT_TIME` :コプロセッサータスクの最大待機時間。
-   `MAX_COP_WAIT_ADDRESS` : 待ち時間が最大となるコプロセッサータスクのアドレス。
-   `AVG_PROCESS_TIME` : TiKV における SQL ステートメントの平均処理時間。
-   `MAX_PROCESS_TIME` : TiKV における SQL ステートメントの最大処理時間。
-   `AVG_WAIT_TIME` : TiKV における SQL ステートメントの平均待機時間。
-   `MAX_WAIT_TIME` : TiKV における SQL ステートメントの最大待機時間。
-   `AVG_BACKOFF_TIME` : SQL ステートメントで再試行が必要なエラーが発生した場合の、再試行までの平均待機時間。
-   `MAX_BACKOFF_TIME` : SQL ステートメントで再試行が必要なエラーが発生した場合に、再試行するまでの最大待機時間。
-   `AVG_TOTAL_KEYS` :コプロセッサーがスキャンしたキーの平均数。
-   `MAX_TOTAL_KEYS` :コプロセッサーがスキャンしたキーの最大数。
-   `AVG_PROCESSED_KEYS` :コプロセッサーが処理したキーの平均数。 `avg_total_keys`と比較すると、 `avg_processed_keys`には MVCC の古いバージョンは含まれていません。 `avg_total_keys`と`avg_processed_keys`の間に大きな差があることから、古いバージョンが多数存在することがわかります。
-   `MAX_PROCESSED_KEYS` :コプロセッサーが処理したキーの最大数。
-   `AVG_TIKV_CPU_TIME` : このカテゴリの SQL ステートメントが消費する TiKVサーバーのCPU 時間の平均値。

取引関連フィールド：

-   `AVG_PREWRITE_TIME` : プリライトフェーズの平均時間。
-   `MAX_PREWRITE_TIME` : プリライトフェーズの最長時間。
-   `AVG_COMMIT_TIME` : コミットフェーズの平均時間。
-   `MAX_COMMIT_TIME` : コミットフェーズの最長時間。
-   `AVG_GET_COMMIT_TS_TIME` : `commit_ts`を取得する平均時間。
-   `MAX_GET_COMMIT_TS_TIME` : `commit_ts`を取得する最長時間。
-   `AVG_COMMIT_BACKOFF_TIME` : コミットフェーズ中に再試行が必要なエラーがSQLステートメントで発生した場合の、再試行までの平均待機時間。
-   `MAX_COMMIT_BACKOFF_TIME` : コミットフェーズ中に再試行が必要なエラーがSQLステートメントで発生した場合、再試行までの最大待機時間。
-   `AVG_RESOLVE_LOCK_TIME` : トランザクション間で発生したロック競合の解決にかかる平均時間。
-   `MAX_RESOLVE_LOCK_TIME` : ロック競合の解決に最も時間がかかったのはトランザクション間です。
-   `AVG_LOCAL_LATCH_WAIT_TIME` : ローカル取引の平均待ち時間。
-   `MAX_LOCAL_LATCH_WAIT_TIME` : ローカル取引の最大待ち時間。
-   `AVG_WRITE_KEYS` : 入力されたキーの平均数。
-   `MAX_WRITE_KEYS` : 書き込まれたキーの最大数。
-   `AVG_WRITE_SIZE` : 書き込まれたデータの平均量（バイト単位）。
-   `MAX_WRITE_SIZE` : 書き込まれるデータの最大量（バイト単位）。
-   `AVG_PREWRITE_REGIONS` : プリライトフェーズに関与する領域の平均数。
-   `MAX_PREWRITE_REGIONS` : プリライトフェーズ中の領域の最大数。
-   `AVG_TXN_RETRY` : トランザクションの再試行回数の平均値。
-   `MAX_TXN_RETRY` : トランザクションの再試行の最大回数。
-   `SUM_BACKOFF_TIMES` : このカテゴリの SQL ステートメントで再試行が必要なエラーが発生した場合の再試行回数の合計。
-   `BACKOFF_TYPES` : 再試行が必要なすべてのエラーの種類と、各種類の再試行回数。フィールドの形式は`type:number`です。エラーの種類が複数ある場合は、それぞれをカンマで区切ります。例: `txnLock:2,pdRPC:1` 。
-   `AVG_AFFECTED_ROWS` : 影響を受けた行の平均数。
-   `PREV_SAMPLE_TEXT` : 現在の SQL ステートメントが`COMMIT`の場合、 `PREV_SAMPLE_TEXT`は`COMMIT`の前のステートメントです。この場合、SQL ステートメントはダイジェストと`prev_sample_text`でグループ化されます。つまり、 `COMMIT`が異なる`prev_sample_text`ステートメントは、異なる行にグループ化されます。現在の SQL ステートメントが`COMMIT`でない場合、 `PREV_SAMPLE_TEXT`フィールドは空の文字列になります。

リソース制御に関連する分野：

-   `AVG_REQUEST_UNIT_WRITE` : SQL ステートメントによって消費される書き込み RU の平均数。
-   `MAX_REQUEST_UNIT_WRITE` : SQL ステートメントによって消費される書き込み RU の最大数。
-   `AVG_REQUEST_UNIT_READ` : SQL ステートメントによって消費される読み取り RU の平均数。
-   `MAX_REQUEST_UNIT_READ` : SQL ステートメントによって消費される読み取り RU の最大数。
-   `AVG_QUEUED_RC_TIME` : SQL ステートメントを実行する際に、利用可能な RU を待つ平均時間。
-   `MAX_QUEUED_RC_TIME` : SQL ステートメントを実行する際に、使用可能な RU の最大待機時間。
-   `RESOURCE_GROUP` : SQL ステートメントにバインドされたリソース グループ。

storageエンジンに関連する分野：

-   `STORAGE_KV` : v8.5.5 で導入され、このカテゴリの SQL ステートメントの以前の実行が TiKV からデータを読み取ったかどうかを示します。
-   `STORAGE_MPP` : v8.5.5 で導入され、このカテゴリの SQL ステートメントの以前の実行がTiFlashからデータを読み取ったかどうかを示します。

### <code>statements_summary_evicted</code>フィールドの説明 {#code-statements-summary-evicted-code-fields-description}

-   `BEGIN_TIME` : 開始時刻を記録します。
-   `END_TIME` : 終了時刻を記録します。
-   `EVICTED_COUNT` : 記録期間中に排除された SQL カテゴリの数。
