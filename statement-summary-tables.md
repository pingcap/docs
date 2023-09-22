---
title: Statement Summary Tables
summary: Learn about Statement Summary Table in TiDB.
---

# ステートメント概要テーブル {#statement-summary-tables}

SQL パフォーマンスの問題をより適切に処理するために、MySQL は統計を使用して SQL を監視する`performance_schema`分の[ステートメント概要テーブル](https://dev.mysql.com/doc/refman/5.7/en/performance-schema-statement-summary-tables.html)を提供しています。これらのテーブルのうち、 `events_statements_summary_by_digest` 、レイテンシー、実行時間、スキャンされた行数、テーブル全体のスキャンなどの豊富なフィールドを備えており、SQL の問題を特定するのに非常に役立ちます。

したがって、v4.0.0-rc.1 以降、TiDB は機能の点で`events_statements_summary_by_digest`に似たシステム テーブルを`information_schema` ( `performance_schema`*ではなく*) で提供します。

-   [`statements_summary`](#statements_summary)
-   [`statements_summary_history`](#statements_summary_history)
-   [`cluster_statements_summary`](#statements_summary_evicted)
-   [`cluster_statements_summary_history`](#statements_summary_evicted)
-   [`statements_summary_evicted`](#statements_summary_evicted)

<CustomContent platform="tidb-cloud">

> **注記：**
>
> 次のテーブルは[TiDB サーバーレスクラスター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)では使用できませ`cluster_statements_summary_history` : `statements_summary` 、および`cluster_statements_summary` `statements_summary_history`

</CustomContent>

このドキュメントでは、これらのテーブルについて詳しく説明し、それらを使用して SQL パフォーマンスの問題をトラブルシューティングする方法を紹介します。

## <code>statements_summary</code> {#code-statements-summary-code}

`statements_summary`は`information_schema`のシステムテーブルです。 `statements_summary` SQL ダイジェストとプラン ダイジェストごとに SQL ステートメントをグループ化し、各 SQL カテゴリの統計を提供します。

ここでの「SQL ダイジェスト」は、スロー ログで使用されるものと同じものを意味し、正規化された SQL ステートメントによって計算される一意の識別子です。正規化プロセスでは、定数の空白文字は無視され、大文字と小文字は区別されません。したがって、一貫した構文を持つステートメントは同じダイジェストを持ちます。例えば：

```sql
SELECT * FROM employee WHERE id IN (1, 2, 3) AND salary BETWEEN 1000 AND 2000;
select * from EMPLOYEE where ID in (4, 5) and SALARY between 3000 and 4000;
```

正規化後は、両方とも次のカテゴリに分類されます。

```sql
select * from employee where id in (...) and salary between ? and ?;
```

ここでの「プラン ダイジェスト」とは、正規化された実行プランを通じて計算された一意の識別子を指します。正規化プロセスでは定数は無視されます。同じ SQL ステートメントは、異なる実行プランを持つ可能性があるため、異なるカテゴリにグループ化される場合があります。同じカテゴリの SQL ステートメントには同じ実行プランがあります。

`statements_summary`は、SQL 監視メトリックの集計結果が格納されます。一般に、各監視メトリクスには最大値と平均値が含まれます。たとえば、実行レイテンシーメトリックは、 `AVG_LATENCY` (平均レイテンシー) と`MAX_LATENCY` (最大レイテンシー) の 2 つのフィールドに対応します。

監視メトリクスが最新であることを確認するために、テーブル`statements_summary`のデータは定期的にクリアされ、最近の集計結果のみが保持されて表示されます。定期的なデータのクリアは、システム変数`tidb_stmt_summary_refresh_interval`によって制御されます。クリア直後にクエリを実行すると、表示されるデータが非常に少なくなる可能性があります。

以下は、 `statements_summary`をクエリした場合の出力例です。

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
> TiDB では、ステートメント概要テーブルのフィールドの時間単位はナノ秒 (ns) ですが、MySQL では時間単位はピコ秒 (ps) です。

## <code>statements_summary_history</code> {#code-statements-summary-history-code}

`statements_summary_history`のテーブル スキーマは`statements_summary`のテーブル スキーマと同じです。 `statements_summary_history`時間範囲の履歴データを保存します。履歴データを確認することで、異常のトラブルシューティングを行ったり、さまざまな時間範囲の監視メトリクスを比較したりできます。

フィールド`SUMMARY_BEGIN_TIME`と`SUMMARY_END_TIME`は、履歴時間範囲の開始時刻と終了時刻を表します。

## <code>statements_summary_evicted</code> {#code-statements-summary-evicted-code}

`tidb_stmt_summary_max_stmt_count`変数は、 `statement_summary`テーブルがメモリに格納するステートメントの最大数を制御します。 `statement_summary`テーブルでは LRU アルゴリズムが使用されます。 SQL ステートメントの数が`tidb_stmt_summary_max_stmt_count`値を超えると、最も長く未使用のレコードがテーブルから削除されます。各期間中に削除された SQL ステートメントの数が`statements_summary_evicted`テーブルに記録されます。

`statements_summary_evicted`テーブルは、SQL レコードが`statement_summary`テーブルから削除された場合にのみ更新されます。 `statements_summary_evicted`は、エビクションが発生した期間とエビクションされた SQL ステートメントの数のみが記録されます。

## ステートメントの概要の<code>cluster</code>テーブル {#the-code-cluster-code-tables-for-statement-summary}

表`statements_summary` `statements_summary_history`および`statements_summary_evicted`には、単一の TiDBサーバーのステートメントの概要のみが示されています。クラスター全体のデータをクエリするには、 `cluster_statements_summary` 、 `cluster_statements_summary_history` 、または`cluster_statements_summary_evicted`テーブルをクエリする必要があります。

`cluster_statements_summary`各 TiDBサーバーの`statements_summary`データを表示します。 `cluster_statements_summary_history`各 TiDBサーバーの`statements_summary_history`データを表示します。 `cluster_statements_summary_evicted`各 TiDBサーバーの`statements_summary_evicted`のデータが表示されます。これらのテーブルでは、 `INSTANCE`フィールドを使用して TiDBサーバーのアドレスを表します。その他のフィールドは`statements_summary` 、 `statements_summary_history` 、 `statements_summary_evicted`と同じです。

## パラメータ設定 {#parameter-configuration}

次のシステム変数は、ステートメントの概要を制御するために使用されます。

-   `tidb_enable_stmt_summary` : ステートメント要約機能を有効にするかどうかを決定します。 `1` `enable`を表し、 `0` `disable`を意味します。この機能はデフォルトで有効になっています。この機能が無効になっている場合、システム テーブルの統計はクリアされます。統計は、次回この機能が有効になったときに再計算されます。テストの結果、この機能を有効にしてもパフォーマンスにはほとんど影響がないことがわかりました。
-   `tidb_stmt_summary_refresh_interval` : `statements_summary`テーブルが更新される間隔。時間の単位は秒(s)です。デフォルト値は`1800`です。
-   `tidb_stmt_summary_history_size` : `statements_summary_history`テーブルに格納される各 SQL ステートメント カテゴリのサイズ。これは`statement_summary_evicted`テーブルの最大レコード数でもあります。デフォルト値は`24`です。
-   `tidb_stmt_summary_max_stmt_count` : ステートメントサマリーテーブルに保存できる SQL ステートメントの数を制限します。デフォルト値は`3000`です。制限を超えると、最近未使用のままになっていた SQL ステートメントがクリアされます。これらのクリアされた SQL ステートメントは`statement_summary_evicted`テーブルに記録されます。
-   `tidb_stmt_summary_max_sql_length` : `DIGEST_TEXT`と`QUERY_SAMPLE_TEXT`の最長の表示長を指定します。デフォルト値は`4096`です。
-   `tidb_stmt_summary_internal_query` : TiDB SQLステートメントをカウントするかどうかを決定します。 `1`カウントすることを意味し、 `0`カウントしないことを意味します。デフォルト値は`0`です。

> **注記：**
>
> `tidb_stmt_summary_max_stmt_count`制限を超えたために SQL ステートメントのカテゴリを削除する必要がある場合、TiDB はすべての時間範囲のその SQL ステートメント カテゴリのデータを`statement_summary_history`テーブルから削除します。そのため、一定の時間範囲におけるSQL文カテゴリ数が制限値に達していなくても、テーブル`statement_summary_history`に格納されるSQL文数は実際のSQL文数よりも少なくなります。この状況が発生してパフォーマンスに影響を与える場合は、 `tidb_stmt_summary_max_stmt_count`の値を増やすことをお勧めします。

ステートメント要約構成の例を以下に示します。

```sql
set global tidb_stmt_summary_max_stmt_count = 3000;
set global tidb_enable_stmt_summary = true;
set global tidb_stmt_summary_refresh_interval = 1800;
set global tidb_stmt_summary_history_size = 24;
```

前述の構成が有効になると、 `statements_summary`テーブルは 30 分ごとにクリアされ、 `statements_summary_history`テーブルには最大 3000 種類の SQL ステートメントが保存されます。タイプごとに、 `statements_summary_history`テーブルに最近の 24 期間のデータが保存されます。 `statements_summary_evicted`表には、SQL ステートメントがステートメントの概要から削除された最近の 24 期間が記録されます。 `statements_summary_evicted`テーブルは 30 分ごとに更新されます。

> **注記：**
>
> -   SQL タイプが 1 分ごとに表示される場合、 `statements_summary_history`は最新 12 時間のデータが保存されます。 SQL タイプが毎日 00:00 から 00:30 までにのみ表示される場合、 `statements_summary_history`は、各期間を 1 日として、最新の 24 期間のデータが保存されます。したがって、 `statements_summary_history`は、この SQL タイプの最新 24 日間のデータが保存されます。
> -   `tidb_stmt_summary_history_size` 、 `tidb_stmt_summary_max_stmt_count` 、および`tidb_stmt_summary_max_sql_length`構成項目はメモリ使用量に影響します。ニーズ、SQL サイズ、SQL 数、マシン構成に基づいてこれらの構成を調整することをお勧めします。あまり大きな値を設定することはお勧めできません。メモリ使用量は`tidb_stmt_summary_history_size` * `tidb_stmt_summary_max_stmt_count` * `tidb_stmt_summary_max_sql_length` * `3`を使用して計算できます。

### ステートメントの要約に適切なサイズを設定する {#set-a-proper-size-for-statement-summary}

システムが一定期間実行された後 (システム負荷に応じて)、 `statement_summary`テーブルをチェックして SQL エビクションが発生したかどうかを確認できます。例えば：

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

`statements_summary`テーブルがレコードでいっぱいであることがわかります。次に、 `statements_summary_evicted`テーブルから削除されたデータを確認します。

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

前述の結果から、最大 59 の SQL カテゴリが削除されることがわかります。この場合、 `statement_summary`テーブルのサイズを少なくとも 59 レコード増やすことをお勧めします。これは、サイズを少なくとも 3059 レコードに増やすことを意味します。

## 制限 {#limitation}

デフォルトでは、ステートメント概要テーブルはメモリに保存されます。 TiDBサーバーが再起動すると、すべてのデータが失われます。

<CustomContent platform="tidb">

この問題に対処するために、TiDB v6.6.0 では実験的に[ステートメントの概要の永続化](#persist-statements-summary)機能が導入されていますが、この機能はデフォルトでは無効になっています。この機能を有効にすると、履歴データはメモリに保存されなくなり、ディスクに直接書き込まれます。このようにして、TiDBサーバーが再起動しても履歴データは引き続き使用できます。

</CustomContent>

## 永続化ステートメントの概要 {#persist-statements-summary}

<CustomContent platform="tidb-cloud">

このセクションは、TiDB セルフホスト型にのみ適用されます。 TiDB Cloudの場合、 `tidb_stmt_summary_enable_persistent`パラメーターの値はデフォルトで`false`であり、動的変更はサポートされていません。

</CustomContent>

> **警告：**
>
> ステートメントの概要の永続化は実験的機能です。本番環境で使用することはお勧めできません。この機能は予告なく変更または削除される場合があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。

<CustomContent platform="tidb">

[制限](#limitation)セクションで説明したように、ステートメント概要テーブルはデフォルトでメモリに保存されます。 TiDBサーバーが再起動すると、すべてのステートメントの概要が失われます。 v6.6.0 以降、TiDB は実験的に構成項目[`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-new-in-v660)を提供し、ユーザーがステートメントの概要の永続性を有効または無効にできるようにします。

</CustomContent>

<CustomContent platform="tidb-cloud">

[制限](#limitation)セクションで説明したように、ステートメント概要テーブルはデフォルトでメモリに保存されます。 TiDBサーバーが再起動すると、すべてのステートメントの概要が失われます。 v6.6.0 以降、TiDB は実験的に構成項目`tidb_stmt_summary_enable_persistent`を提供し、ユーザーがステートメントの概要の永続性を有効または無効にできるようにします。

</CustomContent>

ステートメントの概要の永続性を有効にするには、次の構成項目を TiDB 構成ファイルに追加できます。

```toml
[instance]
tidb_stmt_summary_enable_persistent = true
# The following entries use the default values, which can be modified as needed.
# tidb_stmt_summary_filename = "tidb-statements.log"
# tidb_stmt_summary_file_max_days = 3
# tidb_stmt_summary_file_max_size = 64 # MiB
# tidb_stmt_summary_file_max_backups = 0
```

ステートメントの概要の永続性が有効になった後、メモリには現在のリアルタイム データのみが保持され、履歴データは保持されません。リアルタイム データが履歴データとして更新されると、履歴データは[パラメータ設定](#parameter-configuration)セクションで説明した`tidb_stmt_summary_refresh_interval`の間隔でディスクに書き込まれます。 `statements_summary_history`または`cluster_statements_summary_history`テーブルに対するクエリは、メモリ内データとディスク上のデータの両方を組み合わせた結果を返します。

<CustomContent platform="tidb">

> **注記：**
>
> -   ステートメントの概要の永続化が有効になっている場合、メモリに履歴データが保持されないため、 [パラメータ設定](#parameter-configuration)セクションで説明されている`tidb_stmt_summary_history_size`設定は有効になりません。代わりに、永続化のための履歴データの保持期間とサイズを制御するために、 [`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-new-in-v660) 、 [`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-new-in-v660) 、および[`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-new-in-v660)の 3 つの構成が使用されます。
> -   `tidb_stmt_summary_refresh_interval`の値が小さいほど、より多くの即時データがディスクに書き込まれます。ただし、これは、より多くの冗長データがディスクに書き込まれることも意味します。

</CustomContent>

## トラブルシューティングの例 {#troubleshooting-examples}

このセクションでは、ステートメントの要約機能を使用して SQL パフォーマンスの問題をトラブルシューティングする方法を示す 2 つの例を示します。

### SQLレイテンシーが長いのはサーバー側が原因でしょうか? {#could-high-sql-latency-be-caused-by-the-server-end}

この例では、クライアントは`employee`テーブルに対するポイント クエリでパフォーマンスの低下を示しています。 SQL テキストに対してあいまい検索を実行できます。

```sql
SELECT avg_latency, exec_count, query_sample_text
    FROM information_schema.statements_summary
    WHERE digest_text LIKE 'select * from employee%';
```

`1ms`と`0.3ms` 、正常範囲の`avg_latency`内とみなされます。したがって、サーバー側が原因ではないと結論付けることができます。クライアントまたはネットワークのトラブルシューティングを行うことができます。

```sql
+-------------+------------+------------------------------------------+
| avg_latency | exec_count | query_sample_text                        |
+-------------+------------+------------------------------------------+
|     1042040 |          2 | select * from employee where name='eric' |
|      345053 |          3 | select * from employee where id=3100     |
+-------------+------------+------------------------------------------+
2 rows in set (0.00 sec)
```

### SQL ステートメントのどのカテゴリが合計時間を最も長く消費しますか? {#which-categories-of-sql-statements-consume-the-longest-total-time}

QPS が 10:00 から 10:30 に大幅に減少した場合、履歴テーブルから最も長い時間を消費した SQL ステートメントの 3 つのカテゴリを見つけることができます。

```sql
SELECT sum_latency, avg_latency, exec_count, query_sample_text
    FROM information_schema.statements_summary_history
    WHERE summary_begin_time='2020-01-02 10:00:00'
    ORDER BY sum_latency DESC LIMIT 3;
```

結果は、次の 3 つのカテゴリの SQL ステートメントが合計で最も長い時間を費やしており、高い優先度で最適化する必要があることを示しています。

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

以下は、 `statements_summary`のテーブルのフィールドの説明です。

基本フィールド:

-   `STMT_TYPE` : SQL ステートメントのタイプ。
-   `SCHEMA_NAME` : このカテゴリの SQL ステートメントが実行される現在のスキーマ。
-   `DIGEST` : このカテゴリの SQL ステートメントのダイジェスト。
-   `DIGEST_TEXT` : 正規化された SQL ステートメント。
-   `QUERY_SAMPLE_TEXT` : SQL カテゴリの元の SQL ステートメント。元のステートメントは 1 つだけ採用されます。
-   `TABLE_NAMES` : SQL ステートメントに関係するすべてのテーブル。複数のテーブルがある場合は、それぞれをカンマで区切ります。
-   `INDEX_NAMES` : SQL ステートメントで使用されるすべての SQL インデックス。複数のインデックスがある場合は、それぞれをカンマで区切ります。
-   `SAMPLE_USER` : このカテゴリの SQL ステートメントを実行するユーザー。 1 人のユーザーのみが取得されます。
-   `PLAN_DIGEST` : 実行計画のダイジェスト。
-   `PLAN` : 元の実行計画。複数のステートメントがある場合は、1 つのステートメントのみの計画が採用されます。
-   `BINARY_PLAN` : バイナリ形式でエンコードされた元の実行プラン。複数のステートメントがある場合は、1 つのステートメントのみの計画が採用されます。 `SELECT tidb_decode_binary_plan('xxx...')`ステートメントを実行して、特定の実行プランを解析します。
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
-   `SUM_LATENCY` : このカテゴリの SQL ステートメントの合計実行レイテンシー。
-   `MAX_LATENCY` : このカテゴリの SQL ステートメントの最大実行レイテンシー。
-   `MIN_LATENCY` : このカテゴリの SQL ステートメントの最小実行レイテンシー。
-   `AVG_LATENCY` : このカテゴリの SQL ステートメントの平均実行レイテンシー。
-   `AVG_PARSE_LATENCY` : パーサーの平均レイテンシー。
-   `MAX_PARSE_LATENCY` : パーサーの最大レイテンシー。
-   `AVG_COMPILE_LATENCY` : コンパイラの平均レイテンシー。
-   `MAX_COMPILE_LATENCY` : コンパイラの最大レイテンシー。
-   `AVG_MEM` : 使用される平均メモリ(バイト)。
-   `MAX_MEM` : 使用される最大メモリ(バイト)。
-   `AVG_DISK` : 使用される平均ディスク容量 (バイト)。
-   `MAX_DISK` : 使用される最大ディスク容量 (バイト)。

TiKVコプロセッサータスクに関連するフィールド:

-   `SUM_COP_TASK_NUM` : 送信されたコプロセッサー要求の総数。
-   `MAX_COP_PROCESS_TIME` :コプロセッサータスクの最大実行時間。
-   `MAX_COP_PROCESS_ADDRESS` : 最大実行時間のコプロセッサータスクのアドレス。
-   `MAX_COP_WAIT_TIME` :コプロセッサータスクの最大待ち時間。
-   `MAX_COP_WAIT_ADDRESS` : 最大待機時間のコプロセッサータスクのアドレス。
-   `AVG_PROCESS_TIME` : TiKV における SQL ステートメントの平均処理時間。
-   `MAX_PROCESS_TIME` : TiKV での SQL ステートメントの最大処理時間。
-   `AVG_WAIT_TIME` : TiKV における SQL ステートメントの平均待ち時間。
-   `MAX_WAIT_TIME` : TiKV における SQL ステートメントの最大待ち時間。
-   `AVG_BACKOFF_TIME` : SQL ステートメントで再試行が必要なエラーが発生した場合、再試行までの平均待ち時間。
-   `MAX_BACKOFF_TIME` : SQL ステートメントで再試行が必要なエラーが発生した場合に、再試行するまでの最大待ち時間。
-   `AVG_TOTAL_KEYS` :コプロセッサーがスキャンしたキーの平均数。
-   `MAX_TOTAL_KEYS` :コプロセッサーがスキャンしたキーの最大数。
-   `AVG_PROCESSED_KEYS` :コプロセッサーが処理したキーの平均数。 `avg_total_keys`と比較して、 `avg_processed_keys`は古いバージョンの MVCC が含まれていません。 `avg_total_keys`と`avg_processed_keys`の大きな違いは、古いバージョンが多数存在することを示しています。
-   `MAX_PROCESSED_KEYS` :コプロセッサーが処理したキーの最大数。

トランザクション関連フィールド:

-   `AVG_PREWRITE_TIME` : プリライトフェーズの平均時間。
-   `MAX_PREWRITE_TIME` : プリライトフェーズの最長時間。
-   `AVG_COMMIT_TIME` : コミットフェーズの平均時間。
-   `MAX_COMMIT_TIME` : コミットフェーズの最長時間。
-   `AVG_GET_COMMIT_TS_TIME` : `commit_ts`を取得するまでの平均時間。
-   `MAX_GET_COMMIT_TS_TIME` : `commit_ts`を取得するまでの最長時間。
-   `AVG_COMMIT_BACKOFF_TIME` : SQL ステートメントでコミット フェーズ中に再試行が必要なエラーが発生した場合の、再試行までの平均待ち時間。
-   `MAX_COMMIT_BACKOFF_TIME` : SQL ステートメントでコミット フェーズ中に再試行が必要なエラーが発生した場合、再試行までの最大待機時間。
-   `AVG_RESOLVE_LOCK_TIME` : トランザクション間で発生したロックの競合を解決するまでの平均時間。
-   `MAX_RESOLVE_LOCK_TIME` : トランザクション間で発生したロックの競合を解決するのに最も長い時間がかかりました。
-   `AVG_LOCAL_LATCH_WAIT_TIME` : ローカルトランザクションの平均待ち時間。
-   `MAX_LOCAL_LATCH_WAIT_TIME` : ローカルトランザクションの最大待ち時間。
-   `AVG_WRITE_KEYS` : 書き込まれたキーの平均数。
-   `MAX_WRITE_KEYS` : 書き込まれるキーの最大数。
-   `AVG_WRITE_SIZE` : 書き込まれたデータの平均量 (バイト単位)。
-   `MAX_WRITE_SIZE` : 書き込まれるデータの最大量 (バイト単位)。
-   `AVG_PREWRITE_REGIONS` : 事前書き込みフェーズに含まれるリージョンの平均数。
-   `MAX_PREWRITE_REGIONS` : 事前書き込みフェーズ中の領域の最大数。
-   `AVG_TXN_RETRY` : トランザクションの平均再試行回数。
-   `MAX_TXN_RETRY` : トランザクションの最大再試行回数。
-   `SUM_BACKOFF_TIMES` : このカテゴリの SQL ステートメントで再試行が必要なエラーが発生した場合の再試行の合計。
-   `BACKOFF_TYPES` : 再試行が必要なすべてのタイプのエラーと、タイプごとの再試行回数。フィールドの形式は`type:number`です。複数のエラー タイプがある場合は、 `txnLock:2,pdRPC:1`のように、それぞれをカンマで区切ります。
-   `AVG_AFFECTED_ROWS` : 影響を受ける行の平均数。
-   `PREV_SAMPLE_TEXT` : 現在の SQL ステートメントが`COMMIT`の場合、 `PREV_SAMPLE_TEXT`は`COMMIT`の前のステートメントです。この場合、SQL ステートメントはダイジェストと`prev_sample_text`によってグループ化されます。これは、 `prev_sample_text`が異なる`COMMIT`のステートメントが異なる行にグループ化されることを意味します。現在の SQL ステートメントが`COMMIT`はない場合、 `PREV_SAMPLE_TEXT`フィールドは空の文字列になります。

### <code>statements_summary_evicted</code>フィールドの説明 {#code-statements-summary-evicted-code-fields-description}

-   `BEGIN_TIME` : 開始時刻を記録します。
-   `END_TIME` : 終了時刻を記録します。
-   `EVICTED_COUNT` : 記録期間中に削除される SQL カテゴリの数。
