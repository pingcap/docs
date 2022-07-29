---
title: Statement Summary Tables
summary: Learn about Statement Summary Table in TiDB.
---

# ステートメント要約表 {#statement-summary-tables}

SQLのパフォーマンスの問題をより適切に処理するために、MySQLはSQLを統計で監視するために`performance_schema`の[ステートメント要約テーブル](https://dev.mysql.com/doc/refman/5.7/en/performance-schema-statement-summary-tables.html)を提供しています。これらのテーブルの中で、 `events_statements_summary_by_digest`は、レイテンシ、実行時間、スキャンされた行、全表スキャンなどの豊富なフィールドでSQLの問題を見つけるのに非常に役立ちます。

したがって、v4.0.0-rc.1以降、TiDBは、機能の点で`events_statements_summary_by_digest`と同様のシステムテーブルを`information_schema` （ `performance_schema`では*なく*）で提供します。

-   [`statements_summary`](#statements_summary)
-   [`statements_summary_history`](#statements_summary_history)
-   [`cluster_statements_summary`](#statements_summary_evicted)
-   [`cluster_statements_summary_history`](#statements_summary_evicted)
-   [`statements_summary_evicted`](#statements_summary_evicted)

このドキュメントでは、これらのテーブルについて詳しく説明し、SQLパフォーマンスの問題をトラブルシューティングするためにそれらを使用する方法を紹介します。

## <code>statements_summary</code> {#code-statements-summary-code}

`statements_summary`は`information_schema`のシステムテーブルです。 `statements_summary`は、SQLステートメントをSQLダイジェストとプランダイジェストでグループ化し、各SQLカテゴリの統計を提供します。

ここでの「SQLダイジェスト」とは、低速ログで使用されるものと同じ意味であり、正規化されたSQLステートメントによって計算される一意の識別子です。正規化プロセスでは、定数の空白文字は無視され、大文字と小文字は区別されません。したがって、構文が一貫しているステートメントのダイジェストは同じです。例えば：

{{< copyable "" >}}

```sql
SELECT * FROM employee WHERE id IN (1, 2, 3) AND salary BETWEEN 1000 AND 2000;
select * from EMPLOYEE where ID in (4, 5) and SALARY between 3000 and 4000;
```

正規化後、これらは両方とも次のカテゴリになります。

{{< copyable "" >}}

```sql
select * from employee where id in (...) and salary between ? and ?;
```

ここでの「プランダイジェスト」とは、正規化された実行プランによって計算された一意の識別子を指します。正規化プロセスは定数を無視します。同じSQLステートメントの実行プランが異なる場合があるため、同じSQLステートメントが異なるカテゴリにグループ化される場合があります。同じカテゴリのSQLステートメントの実行プランは同じです。

`statements_summary`は、SQL監視メトリックの集計結果を格納します。一般に、各監視メトリックには、最大値と平均値が含まれます。たとえば、実行待ち時間のメトリックは、 `AVG_LATENCY` （平均待ち時間）と`MAX_LATENCY` （最大待ち時間）の2つのフィールドに対応します。

監視メトリックが最新であることを確認するために、 `statements_summary`テーブルのデータは定期的にクリアされ、最近の集計結果のみが保持および表示されます。定期的なデータクリアは、 `tidb_stmt_summary_refresh_interval`のシステム変数によって制御されます。クリア直後にクエリを実行した場合、表示されるデータが非常に少ない可能性があります。

以下は、クエリ`statements_summary`の出力例です。

```
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
```

> **ノート：**
>
> TiDBでは、ステートメントサマリーテーブルのフィールドの時間単位はナノ秒（ns）ですが、MySQLでは時間単位はピコ秒（ps）です。

## <code>statements_summary_history</code> {#code-statements-summary-history-code}

`statements_summary_history`のテーブルスキーマは`statements_summary`のテーブルスキーマと同じです。 `statements_summary_history`は、時間範囲の履歴データを保存します。履歴データを確認することで、異常のトラブルシューティングを行い、さまざまな時間範囲の監視メトリックを比較できます。

フィールド`SUMMARY_BEGIN_TIME`と`SUMMARY_END_TIME`は、履歴時間範囲の開始時刻と終了時刻を表します。

## <code>statements_summary_evicted</code> {#code-statements-summary-evicted-code}

`tidb_stmt_summary_max_stmt_count`変数は、 `statement_summary`のテーブルがメモリに格納するステートメントの最大数を制御します。 `statement_summary`テーブルはLRUアルゴリズムを使用します。 SQLステートメントの数が`tidb_stmt_summary_max_stmt_count`の値を超えると、最長の未使用レコードがテーブルから削除されます。各期間中に削除されたSQLステートメントの数は、 `statements_summary_evicted`の表に記録されます。

`statements_summary_evicted`テーブルは、SQLレコードが`statement_summary`テーブルから削除された場合にのみ更新されます。 `statements_summary_evicted`は、削除が発生する期間と削除されたSQLステートメントの数のみを記録します。

## ステートメント要約の<code>cluster</code>テーブル {#the-code-cluster-code-tables-for-statement-summary}

`statements_summary` 、および`statements_summary_history`の表は、単一の`statements_summary_evicted`サーバーのステートメントの要約のみを示しています。クラスタ全体のデータをクエリするには、 `cluster_statements_summary` 、または`cluster_statements_summary_history`のテーブルをクエリする必要があり`cluster_statements_summary_evicted` 。

`cluster_statements_summary`は、各TiDBサーバーの`statements_summary`のデータを表示します。 `cluster_statements_summary_history`は、各TiDBサーバーの`statements_summary_history`のデータを表示します。 `cluster_statements_summary_evicted`は、各TiDBサーバーの`statements_summary_evicted`のデータを表示します。これらのテーブルは、 `INSTANCE`フィールドを使用してTiDBサーバーのアドレスを表します。その他のフィールドは`statements_summary`と同じです。

## パラメータ設定 {#parameter-configuration}

次のシステム変数は、ステートメントの要約を制御するために使用されます。

-   `tidb_enable_stmt_summary` ：ステートメント要約機能を有効にするかどうかを決定します。 `1`は`enable`を表し、 `0`は`disable`を意味します。この機能はデフォルトで有効になっています。この機能が無効になっている場合、システムテーブルの統計はクリアされます。統計は、次にこの機能が有効になったときに再計算されます。テストでは、この機能を有効にしてもパフォーマンスにほとんど影響がないことが示されています。
-   `tidb_stmt_summary_refresh_interval` ： `statements_summary`テーブルが更新される間隔。時間の単位は秒です。デフォルト値は`1800`です。
-   `tidb_stmt_summary_history_size` ： `statements_summary_history`テーブルに格納されている各SQLステートメントカテゴリのサイズ。これは、 `statement_summary_evicted`テーブルのレコードの最大数でもあります。デフォルト値は`24`です。
-   `tidb_stmt_summary_max_stmt_count` ：ステートメントサマリーテーブルに格納できるSQLステートメントの数を制限します。デフォルト値は`3000`です。制限を超えると、最近未使用のままになっているSQLステートメントがクリアされます。これらのクリアされたSQLステートメントは、 `statement_summary_evicted`の表に記録されます。
-   `tidb_stmt_summary_max_sql_length` ： `DIGEST_TEXT`と`QUERY_SAMPLE_TEXT`の最長表示長を指定します。デフォルト値は`4096`です。
-   `tidb_stmt_summary_internal_query` ： TiDB SQLステートメントをカウントするかどうかを決定します。 `1`はカウントすることを意味し、 `0`はカウントしないことを意味します。デフォルト値は`0`です。

> **ノート：**
>
> `tidb_stmt_summary_max_stmt_count`の制限を超えたためにSQLステートメントのカテゴリを削除する必要がある場合、TiDBはすべての時間範囲のそのSQLステートメントカテゴリのデータを`statement_summary_history`のテーブルから削除します。したがって、特定の時間範囲内のSQLステートメントカテゴリの数が制限に達していない場合でも、 `statement_summary_history`のテーブルに格納されているSQLステートメントの数は実際のSQLステートメントの数よりも少なくなります。この状況が発生してパフォーマンスに影響を与える場合は、 `tidb_stmt_summary_max_stmt_count`の値を増やすことをお勧めします。

ステートメントの要約構成の例を以下に示します。

{{< copyable "" >}}

```sql
set global tidb_enable_stmt_summary = true;
set global tidb_stmt_summary_refresh_interval = 1800;
set global tidb_stmt_summary_history_size = 24;
```

上記の設定が有効になった後、30分ごとに`statements_summary`のテーブルがクリアされます。 `statements_summary_history`のテーブルには、最近12時間に生成されたデータが格納されます。

`statements_summary_evicted`の表は、SQLステートメントがステートメントの要約から削除された最近の24期間を記録します。 `statements_summary_evicted`のテーブルは30分ごとに更新されます。

> **ノート：**
>
> `tidb_stmt_summary_history_size` 、および`tidb_stmt_summary_max_stmt_count`の構成項目は、メモリー使用量に影響し`tidb_stmt_summary_max_sql_length` 。ニーズ、SQLサイズ、SQLカウント、およびマシン構成に基づいて、これらの構成を調整することをお勧めします。大きすぎる値を設定することはお勧めしません。 `tidb_stmt_summary_history_size` * `tidb_stmt_summary_max_stmt_count` * `tidb_stmt_summary_max_sql_length` * `3`を使用してメモリ使用量を計算できます。

### ステートメントサマリーに適切なサイズを設定する {#set-a-proper-size-for-statement-summary}

システムが一定期間実行された後（システムの負荷に応じて）、 `statement_summary`のテーブルをチェックして、SQLエビクションが発生したかどうかを確認できます。例えば：

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

`statements_summary`のテーブルがレコードでいっぱいであることがわかります。次に、 `statements_summary_evicted`のテーブルから削除されたデータを確認します。

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

上記の結果から、最大59のSQLカテゴリが削除されていることがわかります。これは、ステートメントの要約の適切なサイズが59レコードであることを示しています。

## 制限 {#limitation}

ステートメントサマリーテーブルには、次の制限があります。

上記のステートメント要約テーブルのすべてのデータは、TiDBサーバーを再起動すると失われます。これは、ステートメントサマリーテーブルがすべてメモリテーブルであり、データがストレージに保持されるのではなく、メモリにキャッシュされるためです。

## トラブルシューティングの例 {#troubleshooting-examples}

このセクションでは、ステートメント要約機能を使用してSQLパフォーマンスの問題をトラブルシューティングする方法を示す2つの例を示します。

### サーバー側が原因でSQLの待ち時間が長くなる可能性はありますか？ {#could-high-sql-latency-be-caused-by-the-server-end}

この例では、クライアントは`employee`のテーブルでポイントクエリを実行するとパフォーマンスが低下します。 SQLテキストに対してあいまい検索を実行できます。

{{< copyable "" >}}

```sql
SELECT avg_latency, exec_count, query_sample_text
    FROM information_schema.statements_summary
    WHERE digest_text LIKE 'select * from employee%';
```

`1ms`と`0.3ms`は、通常の`avg_latency`の範囲内と見なされます。したがって、サーバー側が原因ではないと結論付けることができます。クライアントまたはネットワークでトラブルシューティングを行うことができます。

{{< copyable "" >}}

```sql
+-------------+------------+------------------------------------------+
| avg_latency | exec_count | query_sample_text                        |
+-------------+------------+------------------------------------------+
|     1042040 |          2 | select * from employee where name='eric' |
|      345053 |          3 | select * from employee where id=3100     |
+-------------+------------+------------------------------------------+
2 rows in set (0.00 sec)
```

### どのカテゴリのSQLステートメントが最も長い合計時間を消費しますか？ {#which-categories-of-sql-statements-consume-the-longest-total-time}

QPSが10:00から10:30に大幅に減少した場合は、履歴テーブルから、消費時間が最も長いSQLステートメントの3つのカテゴリを見つけることができます。

{{< copyable "" >}}

```sql
SELECT sum_latency, avg_latency, exec_count, query_sample_text
    FROM information_schema.statements_summary_history
    WHERE summary_begin_time='2020-01-02 10:00:00'
    ORDER BY sum_latency DESC LIMIT 3;
```

結果は、次の3つのカテゴリのSQLステートメントが合計で最も長い時間を消費することを示しています。これらは高い優先度で最適化する必要があります。

{{< copyable "" >}}

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

以下は、 `statements_summary`の表のフィールドの説明です。

基本フィールド：

-   `STMT_TYPE` ：SQLステートメントタイプ。
-   `SCHEMA_NAME` ：このカテゴリのSQLステートメントが実行される現在のスキーマ。
-   `DIGEST` ：このカテゴリのSQLステートメントのダイジェスト。
-   `DIGEST_TEXT` ：正規化されたSQLステートメント。
-   `QUERY_SAMPLE_TEXT` ：SQLカテゴリの元のSQLステートメント。元のステートメントは1つだけです。
-   `TABLE_NAMES` ：SQLステートメントに関係するすべてのテーブル。複数のテーブルがある場合は、それぞれをコンマで区切ります。
-   `INDEX_NAMES` ：SQLステートメントで使用されるすべてのSQLインデックス。複数のインデックスがある場合は、それぞれをコンマで区切ります。
-   `SAMPLE_USER` ：このカテゴリのSQLステートメントを実行するユーザー。 1人のユーザーのみが取得されます。
-   `PLAN_DIGEST` ：実行プランのダイジェスト。
-   `PLAN` ：元の実行プラン。複数のステートメントがある場合は、1つのステートメントのみの計画が採用されます。
-   `PLAN_CACHE_HITS` ：このカテゴリのSQLステートメントがプランキャッシュにヒットした合計回数。
-   `PLAN_IN_CACHE` ：このカテゴリのSQLステートメントの前回の実行がプランキャッシュにヒットしたかどうかを示します。

実行時間に関連するフィールド：

-   `SUMMARY_BEGIN_TIME` ：現在の要約期間の開始時刻。
-   `SUMMARY_END_TIME` ：現在の要約期間の終了時刻。
-   `FIRST_SEEN` ：このカテゴリのSQLステートメントが初めて表示される時刻。
-   `LAST_SEEN` ：このカテゴリのSQLステートメントが最後に表示された時刻。

TiDBサーバーに関連するフィールド：

-   `EXEC_COUNT` ：このカテゴリのSQLステートメントの合計実行時間。
-   `SUM_ERRORS` ：実行中に発生したエラーの合計。
-   `SUM_WARNINGS` ：実行中に発生した警告の合計。
-   `SUM_LATENCY` ：このカテゴリのSQLステートメントの合計実行待ち時間。
-   `MAX_LATENCY` ：このカテゴリのSQLステートメントの最大実行待ち時間。
-   `MIN_LATENCY` ：このカテゴリのSQLステートメントの最小実行待ち時間。
-   `AVG_LATENCY` ：このカテゴリのSQLステートメントの平均実行待ち時間。
-   `AVG_PARSE_LATENCY` ：パーサーの平均待ち時間。
-   `MAX_PARSE_LATENCY` ：パーサーの最大レイテンシー。
-   `AVG_COMPILE_LATENCY` ：コンパイラーの平均待ち時間。
-   `MAX_COMPILE_LATENCY` ：コンパイラーの最大待ち時間。
-   `AVG_MEM` ：使用された平均メモリ（バイト）。
-   `MAX_MEM` ：使用される最大メモリ（バイト）。
-   `AVG_DISK` ：使用された平均ディスク容量（バイト）。
-   `MAX_DISK` ：使用されている最大ディスク容量（バイト）。

TiKVコプロセッサータスクに関連するフィールド：

-   `SUM_COP_TASK_NUM` ：送信されたコプロセッサー要求の総数。
-   `MAX_COP_PROCESS_TIME` ：コプロセッサータスクの最大実行時間。
-   `MAX_COP_PROCESS_ADDRESS` ：最大実行時間のコプロセッサータスクのアドレス。
-   `MAX_COP_WAIT_TIME` ：コプロセッサータスクの最大待機時間。
-   `MAX_COP_WAIT_ADDRESS` ：最大待機時間のコプロセッサータスクのアドレス。
-   `AVG_PROCESS_TIME` ：TiKVでのSQLステートメントの平均処理時間。
-   `MAX_PROCESS_TIME` ：TiKVでのSQLステートメントの最大処理時間。
-   `AVG_WAIT_TIME` ：TiKVでのSQLステートメントの平均待機時間。
-   `MAX_WAIT_TIME` ：TiKVでのSQLステートメントの最大待機時間。
-   `AVG_BACKOFF_TIME` ：SQLステートメントで再試行が必要なエラーが発生した場合の再試行までの平均待機時間。
-   `MAX_BACKOFF_TIME` ：SQLステートメントで再試行が必要なエラーが発生した場合の再試行までの最大待機時間。
-   `AVG_TOTAL_KEYS` ：コプロセッサーがスキャンしたキーの平均数。
-   `MAX_TOTAL_KEYS` ：コプロセッサーがスキャンしたキーの最大数。
-   `AVG_PROCESSED_KEYS` ：コプロセッサーが処理したキーの平均数。 `avg_total_keys`と比較すると、 `avg_processed_keys`には古いバージョンのMVCCが含まれていません。 `avg_total_keys`と`avg_processed_keys`の大きな違いは、多くの古いバージョンが存在することを示しています。
-   `MAX_PROCESSED_KEYS` ：コプロセッサーが処理したキーの最大数。

トランザクション関連のフィールド：

-   `AVG_PREWRITE_TIME` ：プリライトフェーズの平均時間。
-   `MAX_PREWRITE_TIME` ：プリライトフェーズの最長時間。
-   `AVG_COMMIT_TIME` ：コミットフェーズの平均時間。
-   `MAX_COMMIT_TIME` ：コミットフェーズの最長時間。
-   `AVG_GET_COMMIT_TS_TIME` ： `commit_ts`を取得する平均時間。
-   `MAX_GET_COMMIT_TS_TIME` ： `commit_ts`を取得する最長時間。
-   `AVG_COMMIT_BACKOFF_TIME` ：コミットフェーズ中に再試行が必要なエラーがSQLステートメントで発生した場合の再試行までの平均待機時間。
-   `MAX_COMMIT_BACKOFF_TIME` ：コミットフェーズ中に再試行が必要なエラーがSQLステートメントで発生した場合の再試行までの最大待機時間。
-   `AVG_RESOLVE_LOCK_TIME` ：トランザクション間で発生したロックの競合を解決するための平均時間。
-   `MAX_RESOLVE_LOCK_TIME` ：トランザクション間で発生したロックの競合を解決するための最長時間。
-   `AVG_LOCAL_LATCH_WAIT_TIME` ：ローカルトランザクションの平均待機時間。
-   `MAX_LOCAL_LATCH_WAIT_TIME` ：ローカルトランザクションの最大待機時間。
-   `AVG_WRITE_KEYS` ：書き込まれたキーの平均数。
-   `MAX_WRITE_KEYS` ：書き込まれたキーの最大数。
-   `AVG_WRITE_SIZE` ：書き込まれたデータの平均量（バイト単位）。
-   `MAX_WRITE_SIZE` ：書き込まれるデータの最大量（バイト単位）。
-   `AVG_PREWRITE_REGIONS` ：プリライトフェーズに関係するリージョンの平均数。
-   `MAX_PREWRITE_REGIONS` ：プリライトフェーズ中のリージョンの最大数。
-   `AVG_TXN_RETRY` ：トランザクションの平均再試行回数。
-   `MAX_TXN_RETRY` ：トランザクションの最大再試行回数。
-   `SUM_BACKOFF_TIMES` ：このカテゴリのSQLステートメントで再試行が必要なエラーが発生した場合の再試行の合計。
-   `BACKOFF_TYPES` ：再試行が必要なすべてのタイプのエラーと各タイプの再試行回数。フィールドの形式は`type:number`です。複数のエラータイプがある場合は、それぞれが`txnLock:2,pdRPC:1`のようにコンマで区切られます。
-   `AVG_AFFECTED_ROWS` ：影響を受ける行の平均数。
-   `PREV_SAMPLE_TEXT` ：現在のSQLステートメントが`COMMIT`の場合、 `PREV_SAMPLE_TEXT`は`COMMIT`の前のステートメントです。この場合、SQLステートメントはダイジェストと`prev_sample_text`によってグループ化されます。これは、 `prev_sample_text`が異なる`COMMIT`のステートメントが異なる行にグループ化されることを意味します。現在のSQLステートメントが`COMMIT`でない場合、 `PREV_SAMPLE_TEXT`フィールドは空の文字列です。

### <code>statements_summary_evicted</code>フィールドの説明 {#code-statements-summary-evicted-code-fields-description}

-   `BEGIN_TIME` ：開始時刻を記録します。
-   `END_TIME` ：終了時刻を記録します。
-   `EVICTED_COUNT` ：レコード期間中に削除されたSQLカテゴリの数。
