---
title: Statement Summary Tables
summary: TiDB のステートメント サマリー テーブルについて学習します。
---

# ステートメント要約表 {#statement-summary-tables}

SQL パフォーマンスの問題をより適切に処理するために、MySQL は統計を使用して SQL を監視するための`performance_schema`のテーブルのうち[ステートメント要約表](https://dev.mysql.com/doc/refman/8.0/en/performance-schema-statement-summary-tables.html)を提供しています。これらのテーブルのうち、 `events_statements_summary_by_digest` 、レイテンシー、実行時間、スキャンされた行、完全なテーブル スキャンなどの豊富なフィールドを備えており、SQL の問題を見つけるのに非常に役立ちます。

したがって、v4.0.0-rc.1 以降、TiDB は機能面で`events_statements_summary_by_digest`に類似したシステム テーブルを`information_schema` ( `performance_schema`*ではなく*) で提供します。

-   [`statements_summary`](#statements_summary)
-   [`statements_summary_history`](#statements_summary_history)
-   [`cluster_statements_summary`](#statements_summary_evicted)
-   [`cluster_statements_summary_history`](#statements_summary_evicted)
-   [`statements_summary_evicted`](#statements_summary_evicted)

> **注記：**
>
> 上記のテーブルは[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

このドキュメントでは、これらのテーブルについて詳しく説明し、それらを使用して SQL パフォーマンスの問題をトラブルシューティングする方法を紹介します。

## <code>statements_summary</code> {#code-statements-summary-code}

`statements_summary`は`information_schema`のシステム テーブルです。4 `statements_summary` SQL ステートメントをリソース グループ、SQL ダイジェスト、プラン ダイジェスト別にグループ化し、各 SQL カテゴリの統計情報を提供します。

ここでの「SQL ダイジェスト」は、スロー ログで使用されるものと同じ意味であり、正規化された SQL ステートメントを通じて計算される一意の識別子です。正規化プロセスでは、定数の空白文字は無視され、大文字と小文字は区別されません。したがって、一貫した構文を持つステートメントには同じダイジェストがあります。例:

```sql
SELECT * FROM employee WHERE id IN (1, 2, 3) AND salary BETWEEN 1000 AND 2000;
select * from EMPLOYEE where ID in (4, 5) and SALARY between 3000 and 4000;
```

正規化後、両方とも次のカテゴリに分類されます。

```sql
select * from employee where id in (...) and salary between ? and ?;
```

ここでの「プラン ダイジェスト」とは、正規化された実行プランを通じて計算された一意の識別子を指します。正規化プロセスでは定数は無視されます。同じ SQL ステートメントが異なる実行プランを持つ可能性があるため、同じステートメントが異なるカテゴリにグループ化されることがあります。同じカテゴリの SQL ステートメントには同じ実行プランがあります。

`statements_summary`には、SQL 監視メトリックの集計結果が格納されます。通常、各監視メトリックには最大値と平均値が含まれます。たとえば、実行レイテンシーメトリックは、 `AVG_LATENCY` (平均レイテンシー) と`MAX_LATENCY` (最大レイテンシー) の 2 つのフィールドに対応します。

監視メトリックが最新であることを確認するために、 `statements_summary`テーブルのデータは定期的にクリアされ、最新の集計結果のみが保持され、表示されます。定期的なデータのクリアは、 `tidb_stmt_summary_refresh_interval`システム変数によって制御されます。クリア直後にクエリを実行すると、表示されるデータが非常に少なくなる可能性があります。

以下はクエリ`statements_summary`の出力例です。

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
> -   TiDB では、ステートメント サマリー テーブル内のフィールドの時間単位はナノ秒 (ns) ですが、MySQL では時間単位はピコ秒 (ps) です。
> -   v7.5.1 および v7.6.0 以降では、 [リソース管理](/tidb-resource-control.md)有効になっているクラスターの場合、 `statements_summary`リソース グループごとに集計されます。たとえば、異なるリソース グループで実行された同じステートメントは、異なるレコードとして収集されます。

## <code>statements_summary_history</code> {#code-statements-summary-history-code}

`statements_summary_history`のテーブル スキーマは`statements_summary`と同じです。5 `statements_summary_history` 、時間範囲の履歴データを保存します。履歴データを確認することで、異常をトラブルシューティングしたり、異なる時間範囲の監視メトリックを比較したりできます。

フィールド`SUMMARY_BEGIN_TIME`と`SUMMARY_END_TIME` 、履歴時間範囲の開始時刻と終了時刻を表します。

## <code>statements_summary_evicted</code> {#code-statements-summary-evicted-code}

`tidb_stmt_summary_max_stmt_count`変数は、 `statement_summary`テーブル`statement_summary`メモリに保存するステートメントの最大数を制御します。5 テーブルは LRU アルゴリズムを使用します。SQL ステートメントの数が`tidb_stmt_summary_max_stmt_count`値を超えると、最も長い未使用レコードがテーブルから削除されます。各期間中に削除された SQL ステートメントの数は、 `statements_summary_evicted`テーブルに記録されます。

`statements_summary_evicted`テーブルは、SQL レコードが`statement_summary`テーブルから削除された場合にのみ更新されます。5 `statements_summary_evicted`には、削除が発生した期間と削除された SQL ステートメントの数のみが記録されます。

## ステートメントサマリーの<code>cluster</code>テーブル {#the-code-cluster-code-tables-for-statement-summary}

`statements_summary` 、 `statements_summary_history` 、および`statements_summary_evicted`テーブルには、単一の TiDBサーバーのステートメントの概要のみが表示されます。クラスター全体のデータをクエリするには、 `cluster_statements_summary` 、 `cluster_statements_summary_history` 、または`cluster_statements_summary_evicted`テーブルをクエリする必要があります。

`cluster_statements_summary`は各 TiDBサーバーの`statements_summary`データを表示します。 `cluster_statements_summary_history`は各 TiDBサーバーの`statements_summary_history`のデータを表示します。 `cluster_statements_summary_evicted`各 TiDBサーバーの`statements_summary_evicted`データを表示します。 これらのテーブルでは、 `INSTANCE`フィールドを使用して TiDBサーバーのアドレスを表します。 その他のフィールドは、 `statements_summary` 、 `statements_summary_history` 、および`statements_summary_evicted`と同じです。

## パラメータ設定 {#parameter-configuration}

ステートメント サマリーを制御するために、次のシステム変数が使用されます。

-   `tidb_enable_stmt_summary` : ステートメント サマリー機能を有効にするかどうかを決定します。 `1`は`enable`を表し、 `0` `disable`を意味します。この機能はデフォルトで有効になっています。この機能を無効にすると、システム テーブルの統計はクリアされます。統計は、次回この機能が有効になったときに再計算されます。テストでは、この機能を有効にしてもパフォーマンスにほとんど影響がないことがわかっています。
-   `tidb_stmt_summary_refresh_interval` : `statements_summary`が更新される間隔。時間単位は秒 (s) です。デフォルト値は`1800`です。
-   `tidb_stmt_summary_history_size` : `statements_summary_history`テーブルに格納される各 SQL ステートメント カテゴリのサイズ。これは`statements_summary_evicted`テーブルの最大レコード数でもあります。デフォルト値は`24`です。

<CustomContent platform="tidb">

-   `tidb_stmt_summary_max_stmt_count` : ステートメント サマリー テーブルに保存できる SQL ステートメントの数を制限します。デフォルト値は`3000`です。制限を超えると、TiDB は最近使用されていない SQL ステートメントをクリアします。これらのクリアされた SQL ステートメントは、 `DIGEST`が`NULL`に設定された行として表され、 `statements_summary_evicted`テーブルに記録されます。 [TiDBダッシュボードのSQLステートメントページ](/dashboard/dashboard-statement-list.md#others)では、これらの行の情報が`Others`として表示されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   `tidb_stmt_summary_max_stmt_count` : ステートメント サマリー テーブルに保存できる SQL ステートメントの数を制限します。デフォルト値は`3000`です。制限を超えると、TiDB は最近使用されていない SQL ステートメントをクリアします。これらのクリアされた SQL ステートメントは、 `DIGEST`が`NULL`に設定された行として表され、 `statements_summary_evicted`テーブルに記録されます。 [TiDBダッシュボードのSQLステートメントページ](https://docs.pingcap.com/tidb/stable/dashboard-statement-list#others)では、これらの行の情報が`Others`として表示されます。

</CustomContent>

-   `tidb_stmt_summary_max_sql_length` : `DIGEST_TEXT`と`QUERY_SAMPLE_TEXT`の最長表示長を指定します。デフォルト値は`4096`です。
-   `tidb_stmt_summary_internal_query` : TiDB SQLステートメントをカウントするかどうかを決定します。 `1`カウントすることを意味し、 `0`カウントしないことを意味します。デフォルト値は`0`です。

> **注記：**
>
> `tidb_stmt_summary_max_stmt_count`制限を超えたために SQL 文のカテゴリを削除する必要がある場合、TiDB は`statement_summary_history`テーブルからすべての時間範囲のその SQL 文カテゴリのデータを削除します。したがって、特定の時間範囲の SQL 文カテゴリの数が制限に達していなくても、 `statement_summary_history`テーブルに格納される SQL 文の数は実際の SQL 文の数よりも少なくなります。このような状況が発生してパフォーマンスに影響する場合は、 `tidb_stmt_summary_max_stmt_count`の値を増やすことをお勧めします。

ステートメント サマリー構成の例を次に示します。

```sql
set global tidb_stmt_summary_max_stmt_count = 3000;
set global tidb_enable_stmt_summary = true;
set global tidb_stmt_summary_refresh_interval = 1800;
set global tidb_stmt_summary_history_size = 24;
```

上記の構成が有効になると、 `statements_summary`テーブルは 30 分ごとにクリアされ、 `statements_summary_history`テーブルには最大 3000 種類の SQL ステートメントが格納されます。5 テーブルには、タイプ`statements_summary_history`に最近の 24 期間のデータが格納されます`statements_summary_evicted`テーブルには、ステートメント サマリーから SQL ステートメントが削除された最近の 24 期間が記録されます`statements_summary_evicted`テーブルは 30 分ごとに更新されます。

> **注記：**
>
> -   SQL タイプが 1 分ごとに表示される場合、 `statements_summary_history`最新の 12 時間のデータが格納されます。SQL タイプが毎日 00:00 から 00:30 までのみ表示される場合、 `statements_summary_history`最新の 24 期間のデータが格納されます (各期間は 1 日)。したがって、 `statements_summary_history`この SQL タイプに関する最新の 24 日間のデータが格納されます。
> -   `tidb_stmt_summary_history_size` 、 `tidb_stmt_summary_max_stmt_count` 、および`tidb_stmt_summary_max_sql_length`構成項目は、メモリ使用量に影響します。これらの構成は、ニーズ、SQL サイズ、SQL 数、およびマシン構成に基づいて調整することをお勧めします。あまり大きな値を設定することはお勧めしません。メモリ使用量は、 `tidb_stmt_summary_history_size` * `tidb_stmt_summary_max_stmt_count` * `tidb_stmt_summary_max_sql_length` * `3`を使用して計算できます。

### ステートメントサマリーの適切なサイズを設定する {#set-a-proper-size-for-statement-summary}

システムを一定期間実行した後 (システム負荷によって異なります)、 `statement_summary`テーブルをチェックして、SQL の削除が発生したかどうかを確認できます。例:

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

`statements_summary`テーブルがレコードでいっぱいになっていることがわかります。次に、 `statements_summary_evicted`テーブルから削除されたデータを確認します。

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

上記の結果から、最大 59 個の SQL カテゴリが削除されていることがわかります。この場合、 `statement_summary`テーブルのサイズを少なくとも 59 レコード増やすことをお勧めします。つまり、サイズを少なくとも 3059 レコードに増やすことを意味します。

## 制限 {#limitation}

デフォルトでは、ステートメント サマリー テーブルはメモリに保存されます。TiDBサーバーが再起動すると、すべてのデータが失われます。

<CustomContent platform="tidb">

この問題に対処するため、TiDB v6.6.0 では、デフォルトで無効になっている[ステートメントサマリーの永続性](#persist-statements-summary)機能を実験的に導入しました。この機能を有効にすると、履歴データはメモリに保存されなくなり、ディスクに直接書き込まれます。このようにして、TiDBサーバーを再起動しても履歴データは引き続き利用できます。

</CustomContent>

## 永続ステートメントの概要 {#persist-statements-summary}

<CustomContent platform="tidb-cloud">

このセクションは、TiDB Self-Hosted にのみ適用されます。TiDB TiDB Cloudの場合、 `tidb_stmt_summary_enable_persistent`パラメータの値はデフォルトで`false`であり、動的な変更はサポートされません。

</CustomContent>

> **警告：**
>
> ステートメント サマリーの永続化は実験的機能です。本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告できます。

<CustomContent platform="tidb">

セクション[制限](#limitation)で説明したように、ステートメント サマリー テーブルはデフォルトでメモリに保存されます。TiDBサーバーが再起動すると、すべてのステートメント サマリーが失われます。v6.6.0 以降、TiDB は、ユーザーがステートメント サマリーの永続性を有効または無効にできるように、構成項目[`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-new-in-v660)を試験的に提供します。

</CustomContent>

<CustomContent platform="tidb-cloud">

セクション[制限](#limitation)で説明したように、ステートメント サマリー テーブルはデフォルトでメモリに保存されます。TiDBサーバーが再起動すると、すべてのステートメント サマリーが失われます。v6.6.0 以降、TiDB は、ユーザーがステートメント サマリーの永続性を有効または無効にできるように、構成項目`tidb_stmt_summary_enable_persistent`を試験的に提供しています。

</CustomContent>

ステートメント サマリーの永続性を有効にするには、TiDB 構成ファイルに次の構成項目を追加します。

```toml
[instance]
tidb_stmt_summary_enable_persistent = true
# The following entries use the default values, which can be modified as needed.
# tidb_stmt_summary_filename = "tidb-statements.log"
# tidb_stmt_summary_file_max_days = 3
# tidb_stmt_summary_file_max_size = 64 # MiB
# tidb_stmt_summary_file_max_backups = 0
```

ステートメント サマリーの永続性を有効にすると、メモリには現在のリアルタイム データのみが保持され、履歴データは保持されません。リアルタイム データが履歴データとして更新されると、履歴データはセクション[パラメータ設定](#parameter-configuration)で説明した間隔`tidb_stmt_summary_refresh_interval`でディスクに書き込まれます。5 または`cluster_statements_summary_history`テーブルに対するクエリでは、 `statements_summary_history`内データとディスク上のデータの両方を組み合わせた結果が返されます。

<CustomContent platform="tidb">

> **注記：**
>
> -   ステートメント サマリーの永続化が有効になっている場合、メモリが履歴データを保持しないため、 [パラメータ設定](#parameter-configuration)セクションで説明した`tidb_stmt_summary_history_size`構成は有効になりません。代わりに、 [`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-new-in-v660) 、 [`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-new-in-v660) 、および[`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-new-in-v660) 3 つの構成を使用して、永続化のための履歴データの保持期間とサイズを制御します。
> -   `tidb_stmt_summary_refresh_interval`の値が小さいほど、ディスクに書き込まれる即時データが多くなります。ただし、これは、ディスクに書き込まれる冗長データも多くなることも意味します。

</CustomContent>

## トラブルシューティングの例 {#troubleshooting-examples}

このセクションでは、ステートメント サマリー機能を使用して SQL パフォーマンスの問題をトラブルシューティングする方法を示す 2 つの例を示します。

### 高い SQLレイテンシーはサーバー側で発生している可能性がありますか? {#could-high-sql-latency-be-caused-by-the-server-end}

この例では、クライアントは`employee`テーブルに対するポイント クエリでパフォーマンスが低下していることを示しています。SQL テキストに対してあいまい検索を実行できます。

```sql
SELECT avg_latency, exec_count, query_sample_text
    FROM information_schema.statements_summary
    WHERE digest_text LIKE 'select * from employee%';
```

`1ms`と`0.3ms` `avg_latency`の正常範囲内であると考えられます。したがって、サーバー側が原因ではないという結論が下されます。クライアントまたはネットワークでトラブルシューティングを行うことができます。

```sql
+-------------+------------+------------------------------------------+
| avg_latency | exec_count | query_sample_text                        |
+-------------+------------+------------------------------------------+
|     1042040 |          2 | select * from employee where name='eric' |
|      345053 |          3 | select * from employee where id=3100     |
+-------------+------------+------------------------------------------+
2 rows in set (0.00 sec)
```

### どのカテゴリの SQL ステートメントが最も長い合計時間を消費しますか? {#which-categories-of-sql-statements-consume-the-longest-total-time}

QPS が 10:00 から 10:30 にかけて大幅に減少した場合、履歴テーブルから、最も時間のかかる SQL ステートメントの 3 つのカテゴリを見つけることができます。

```sql
SELECT sum_latency, avg_latency, exec_count, query_sample_text
    FROM information_schema.statements_summary_history
    WHERE summary_begin_time='2020-01-02 10:00:00'
    ORDER BY sum_latency DESC LIMIT 3;
```

結果から、次の 3 つのカテゴリの SQL ステートメントが合計で最も長い時間を消費しており、優先度を高くして最適化する必要があることがわかります。

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

以下は、 `statements_summary`テーブル内のフィールドの説明です。

基本フィールド:

-   `STMT_TYPE` : SQL ステートメントのタイプ。
-   `SCHEMA_NAME` : このカテゴリの SQL ステートメントが実行される現在のスキーマ。
-   `DIGEST` : このカテゴリの SQL ステートメントのダイジェスト。
-   `DIGEST_TEXT` : 正規化された SQL ステートメント。
-   `QUERY_SAMPLE_TEXT` : SQL カテゴリの元の SQL ステートメント。元のステートメントは 1 つだけ取得されます。
-   `TABLE_NAMES` : SQL ステートメントに関係するすべてのテーブル。テーブルが複数ある場合は、各テーブルはコンマで区切られます。
-   `INDEX_NAMES` : SQL ステートメントで使用されるすべての SQL インデックス。複数のインデックスがある場合は、それぞれがコンマで区切られます。
-   `SAMPLE_USER` : このカテゴリの SQL ステートメントを実行するユーザー。取得されるユーザーは 1 人だけです。
-   `PLAN_DIGEST` : 実行プランのダイジェスト。
-   `PLAN` : 元の実行プラン。複数のステートメントがある場合は、1 つのステートメントのプランのみが採用されます。
-   `BINARY_PLAN` : バイナリ形式でエンコードされた元の実行プラン。複数のステートメントがある場合は、1 つのステートメントのプランのみが取得されます。特定の実行プランを解析するには、 `SELECT tidb_decode_binary_plan('xxx...')`ステートメントを実行します。
-   `PLAN_CACHE_HITS` : このカテゴリの SQL ステートメントがプラン キャッシュにヒットした合計回数。
-   `PLAN_IN_CACHE` : このカテゴリの SQL ステートメントの前回の実行がプラン キャッシュにヒットしたかどうかを示します。

実行時間に関連するフィールド:

-   `SUMMARY_BEGIN_TIME` : 現在の要約期間の開始時刻。
-   `SUMMARY_END_TIME` : 現在の集計期間の終了時刻。
-   `FIRST_SEEN` : このカテゴリの SQL ステートメントが初めて表示された時刻。
-   `LAST_SEEN` : このカテゴリの SQL ステートメントが最後に表示された時刻。

TiDBサーバーに関連するフィールド:

-   `EXEC_COUNT` : このカテゴリの SQL ステートメントの合計実行時間。
-   `SUM_ERRORS` : 実行中に発生したエラーの合計。
-   `SUM_WARNINGS` : 実行中に発生した警告の合計。
-   `SUM_LATENCY` : このカテゴリの SQL ステートメントの合計実行待機レイテンシー。
-   `MAX_LATENCY` : このカテゴリの SQL ステートメントの最大実行レイテンシー。
-   `MIN_LATENCY` : このカテゴリの SQL ステートメントの最小実行レイテンシー。
-   `AVG_LATENCY` : このカテゴリの SQL ステートメントの平均実行レイテンシー。
-   `AVG_PARSE_LATENCY` : パーサーの平均レイテンシー。
-   `MAX_PARSE_LATENCY` : パーサーの最大レイテンシー。
-   `AVG_COMPILE_LATENCY` : コンパイラの平均レイテンシー。
-   `MAX_COMPILE_LATENCY` : コンパイラの最大レイテンシー。
-   `AVG_MEM` : 使用された平均メモリ(バイト)。
-   `MAX_MEM` : 使用される最大メモリ（バイト）。
-   `AVG_DISK` : 使用された平均ディスク容量 (バイト)。
-   `MAX_DISK` : 使用される最大ディスク容量 (バイト)。

TiKVコプロセッサータスクに関連するフィールド:

-   `SUM_COP_TASK_NUM` : 送信されたコプロセッサー要求の合計数。
-   `MAX_COP_PROCESS_TIME` :コプロセッサータスクの最大実行時間。
-   `MAX_COP_PROCESS_ADDRESS` : 実行時間が最大となるコプロセッサータスクのアドレス。
-   `MAX_COP_WAIT_TIME` :コプロセッサータスクの最大待機時間。
-   `MAX_COP_WAIT_ADDRESS` : 最大待機時間を持つコプロセッサータスクのアドレス。
-   `AVG_PROCESS_TIME` : TiKV での SQL ステートメントの平均処理時間。
-   `MAX_PROCESS_TIME` : TiKV での SQL ステートメントの最大処理時間。
-   `AVG_WAIT_TIME` : TiKV 内の SQL ステートメントの平均待機時間。
-   `MAX_WAIT_TIME` : TiKV での SQL ステートメントの最大待機時間。
-   `AVG_BACKOFF_TIME` : SQL ステートメントで再試行を必要とするエラーが発生した場合の再試行までの平均待機時間。
-   `MAX_BACKOFF_TIME` : SQL ステートメントで再試行を必要とするエラーが発生した場合の再試行までの最大待機時間。
-   `AVG_TOTAL_KEYS` :コプロセッサーがスキャンしたキーの平均数。
-   `MAX_TOTAL_KEYS` :コプロセッサーがスキャンしたキーの最大数。
-   `AVG_PROCESSED_KEYS` :コプロセッサーが処理したキーの平均数。 `avg_total_keys`と比較すると、 `avg_processed_keys` MVCC の古いバージョンは含まれません。 `avg_total_keys`と`avg_processed_keys`の大きな差は、多くの古いバージョンが存在することを示しています。
-   `MAX_PROCESSED_KEYS` :コプロセッサーが処理したキーの最大数。

取引関連フィールド:

-   `AVG_PREWRITE_TIME` : 事前書き込みフェーズの平均時間。
-   `MAX_PREWRITE_TIME` : 事前書き込みフェーズの最長時間。
-   `AVG_COMMIT_TIME` : コミット フェーズの平均時間。
-   `MAX_COMMIT_TIME` : コミット フェーズの最長時間。
-   `AVG_GET_COMMIT_TS_TIME` : `commit_ts`取得する平均時間。
-   `MAX_GET_COMMIT_TS_TIME` : `commit_ts`を取得するのに最も時間がかかった。
-   `AVG_COMMIT_BACKOFF_TIME` : コミット フェーズ中に SQL ステートメントで再試行を必要とするエラーが発生した場合の再試行までの平均待機時間。
-   `MAX_COMMIT_BACKOFF_TIME` : コミット フェーズ中に SQL ステートメントで再試行を必要とするエラーが発生した場合の再試行までの最大待機時間。
-   `AVG_RESOLVE_LOCK_TIME` : トランザクション間で発生したロック競合を解決するための平均時間。
-   `MAX_RESOLVE_LOCK_TIME` : トランザクション間で発生したロック競合を解決するのに最長時間かかりました。
-   `AVG_LOCAL_LATCH_WAIT_TIME` : ローカルトランザクションの平均待機時間。
-   `MAX_LOCAL_LATCH_WAIT_TIME` : ローカルトランザクションの最大待機時間。
-   `AVG_WRITE_KEYS` : 書き込まれたキーの平均数。
-   `MAX_WRITE_KEYS` : 書き込まれたキーの最大数。
-   `AVG_WRITE_SIZE` : 書き込まれたデータの平均量 (バイト単位)。
-   `MAX_WRITE_SIZE` : 書き込まれたデータの最大量（バイト単位）。
-   `AVG_PREWRITE_REGIONS` : 事前書き込みフェーズに関与するリージョンの平均数。
-   `MAX_PREWRITE_REGIONS` : 事前書き込みフェーズ中のリージョンの最大数。
-   `AVG_TXN_RETRY` : トランザクションの平均再試行回数。
-   `MAX_TXN_RETRY` : トランザクション再試行の最大回数。
-   `SUM_BACKOFF_TIMES` : このカテゴリの SQL 文で再試行が必要なエラーが発生した場合の再試行の合計。
-   `BACKOFF_TYPES` : 再試行を必要とするすべてのエラーの種類と、各種類の再試行回数。フィールドの形式は`type:number`です。エラーの種類が複数ある場合は、それぞれが`txnLock:2,pdRPC:1`のようにカンマで区切られます。
-   `AVG_AFFECTED_ROWS` : 影響を受ける行の平均数。
-   `PREV_SAMPLE_TEXT` : 現在の SQL 文が`COMMIT`の場合、 `PREV_SAMPLE_TEXT`は`COMMIT`の前の文です。この場合、SQL 文はダイジェストと`prev_sample_text`でグループ化されます。つまり、 `prev_sample_text`が異なる`COMMIT`の文が異なる行にグループ化されます。現在の SQL 文が`COMMIT`でない場合、 `PREV_SAMPLE_TEXT`フィールドは空の文字列になります。

リソース制御に関連するフィールド:

-   `AVG_REQUEST_UNIT_WRITE` : SQL ステートメントによって消費される書き込み RU の平均数。
-   `MAX_REQUEST_UNIT_WRITE` : SQL ステートメントによって消費される書き込み RU の最大数。
-   `AVG_REQUEST_UNIT_READ` : SQL ステートメントによって消費される読み取り RU の平均数。
-   `MAX_REQUEST_UNIT_READ` : SQL ステートメントによって消費される読み取り RU の最大数。
-   `AVG_QUEUED_RC_TIME` : SQL ステートメントを実行するときに使用可能な RU の平均待機時間。
-   `MAX_QUEUED_RC_TIME` : SQL ステートメントを実行するときに使用可能な RU の最大待機時間。
-   `RESOURCE_GROUP` : SQL ステートメントにバインドされたリソース グループ。

### <code>statements_summary_evicted</code>フィールドの説明 {#code-statements-summary-evicted-code-fields-description}

-   `BEGIN_TIME` : 開始時刻を記録します。
-   `END_TIME` : 終了時刻を記録します。
-   `EVICTED_COUNT` : 記録期間中に削除された SQL カテゴリの数。
