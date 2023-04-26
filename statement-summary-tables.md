---
title: Statement Summary Tables
summary: Learn about Statement Summary Table in TiDB.
---

# ステートメント要約表 {#statement-summary-tables}

SQL パフォーマンスの問題をより適切に処理するために、MySQL は`performance_schema`分の[ステートメント要約表](https://dev.mysql.com/doc/refman/5.7/en/performance-schema-statement-summary-tables.html)を提供して、SQL を統計で監視します。これらのテーブルの中で、 `events_statements_summary_by_digest` 、レイテンシー、実行時間、スキャンされた行、およびフル テーブル スキャンなどの豊富なフィールドを使用して、SQL の問題を特定するのに非常に役立ちます。

したがって、v4.0.0-rc.1 から、TiDB は`events_statements_summary_by_digest`に似た機能を持つシステム テーブルを`information_schema` ( `performance_schema`*ではなく*) で提供します。

-   [`statements_summary`](#statements_summary)
-   [`statements_summary_history`](#statements_summary_history)
-   [`cluster_statements_summary`](#statements_summary_evicted)
-   [`cluster_statements_summary_history`](#statements_summary_evicted)
-   [`statements_summary_evicted`](#statements_summary_evicted)

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> 次のテーブルは[Serverless Tierクラスター](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)では使用できませ`cluster_statements_summary_history` : `statements_summary` 、および`cluster_statements_summary` `statements_summary_history`

</CustomContent>

このドキュメントでは、これらのテーブルについて詳しく説明し、それらを使用して SQL パフォーマンスの問題をトラブルシューティングする方法を紹介します。

## <code>statements_summary</code> {#code-statements-summary-code}

`statements_summary`は`information_schema`のシステム テーブルです。 `statements_summary` SQL ダイジェストとプラン ダイジェストによって SQL ステートメントをグループ化し、各 SQL カテゴリの統計を提供します。

ここでの「SQL ダイジェスト」とは、スロー ログで使用されるのと同じ意味で、正規化された SQL ステートメントによって計算された一意の識別子です。正規化プロセスでは、定数の空白文字は無視され、大文字と小文字は区別されません。したがって、一貫した構文を持つステートメントは、同じダイジェストを持ちます。例えば：

{{< copyable "" >}}

```sql
SELECT * FROM employee WHERE id IN (1, 2, 3) AND salary BETWEEN 1000 AND 2000;
select * from EMPLOYEE where ID in (4, 5) and SALARY between 3000 and 4000;
```

正規化後、それらは両方とも次のカテゴリになります。

{{< copyable "" >}}

```sql
select * from employee where id in (...) and salary between ? and ?;
```

ここでの「プラン ダイジェスト」とは、正規化された実行プランによって計算された一意の識別子を指します。正規化プロセスでは、定数は無視されます。同じステートメントが異なる実行計画を持つ可能性があるため、同じ SQL ステートメントが異なるカテゴリーにグループ化される場合があります。同じカテゴリの SQL ステートメントには、同じ実行計画があります。

`statements_summary` SQL モニタリング メトリックの集計結果を格納します。一般に、各監視メトリックには最大値と平均値が含まれます。たとえば、実行レイテンシーメトリックは、 `AVG_LATENCY` (平均レイテンシー) と`MAX_LATENCY` (最大レイテンシー) の 2 つのフィールドに対応します。

監視メトリックが最新であることを確認するために、 `statements_summary`テーブルのデータは定期的にクリアされ、最近の集計結果のみが保持されて表示されます。定期的なデータ消去は、システム変数`tidb_stmt_summary_refresh_interval`によって制御されます。クリア直後にクエリを実行すると、表示されるデータが非常に少なくなる場合があります。

以下は、クエリ`statements_summary`のサンプル出力です。

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
> TiDB では、ステートメント サマリー テーブルのフィールドの時間単位はナノ秒 (ns) ですが、MySQL では時間単位はピコ秒 (ps) です。

## <code>statements_summary_history</code> {#code-statements-summary-history-code}

`statements_summary_history`のテーブル スキーマは`statements_summary`のテーブル スキーマと同じです。 `statements_summary_history`時間範囲の履歴データを保存します。履歴データを確認することで、異常をトラブルシューティングし、さまざまな時間範囲のモニタリング メトリックを比較できます。

フィールド`SUMMARY_BEGIN_TIME`と`SUMMARY_END_TIME`は、履歴時間範囲の開始時刻と終了時刻を表します。

## <code>statements_summary_evicted</code> {#code-statements-summary-evicted-code}

変数`tidb_stmt_summary_max_stmt_count`は、テーブル`statement_summary`がメモリに格納するステートメントの最大数を制御します。 `statement_summary`テーブルは LRU アルゴリズムを使用します。 SQL ステートメントの数が`tidb_stmt_summary_max_stmt_count`値を超えると、最長の未使用レコードがテーブルから削除されます。各期間中に排除された SQL ステートメントの数は、 `statements_summary_evicted`テーブルに記録されます。

`statements_summary_evicted`テーブルは、SQL レコードが`statement_summary`テーブルから削除された場合にのみ更新されます。 `statements_summary_evicted` 、エビクションが発生した期間と、エビクトされた SQL ステートメントの数のみを記録します。

## ステートメント要約用の<code>cluster</code>表 {#the-code-cluster-code-tables-for-statement-summary}

`statements_summary` 、および`statements_summary_evicted`の表`statements_summary_history` 、単一の TiDBサーバーのステートメントの要約のみを示しています。クラスター全体のデータをクエリするには、 `cluster_statements_summary` 、 `cluster_statements_summary_history` 、または`cluster_statements_summary_evicted`テーブルをクエリする必要があります。

`cluster_statements_summary`各 TiDBサーバーの`statements_summary`データを表示します。 `cluster_statements_summary_history`各 TiDBサーバーの`statements_summary_history`データを表示します。 `cluster_statements_summary_evicted`各 TiDBサーバーの`statements_summary_evicted`のデータを表示します。これらのテーブルは、 `INSTANCE`フィールドを使用して TiDBサーバーのアドレスを表します。その他のフィールドは、 `statements_summary` `statements_summary_history`および`statements_summary_evicted`と同じです。

## パラメータ構成 {#parameter-configuration}

次のシステム変数は、ステートメントの要約を制御するために使用されます。

-   `tidb_enable_stmt_summary` : ステートメント要約機能を有効にするかどうかを決定します。 `1` `enable`を表し、 `0` `disable`を意味します。この機能はデフォルトで有効になっています。この機能を無効にすると、システム テーブルの統計情報がクリアされます。次回この機能を有効にしたときに、統計が再計算されます。テストでは、この機能を有効にしてもパフォーマンスにほとんど影響がないことが示されています。
-   `tidb_stmt_summary_refresh_interval` : `statements_summary`テーブルが更新される間隔。時間の単位は秒です。デフォルト値は`1800`です。
-   `tidb_stmt_summary_history_size` : `statements_summary_history`テーブルに格納されている各 SQL ステートメント カテゴリのサイズ。これは、 `statement_summary_evicted`テーブルの最大レコード数でもあります。デフォルト値は`24`です。
-   `tidb_stmt_summary_max_stmt_count` : ステートメント要約テーブルに保管できる SQL ステートメントの数を制限します。デフォルト値は`3000`です。制限を超えると、最近使用されていない SQL ステートメントがクリアされます。これらのクリアされた SQL ステートメントは、 `statement_summary_evicted`テーブルに記録されます。
-   `tidb_stmt_summary_max_sql_length` : `DIGEST_TEXT`と`QUERY_SAMPLE_TEXT`の最長表示長を指定します。デフォルト値は`4096`です。
-   `tidb_stmt_summary_internal_query` : TiDB SQLステートメントをカウントするかどうかを決定します。 `1`数えることを意味し、 `0`数えないことを意味します。デフォルト値は`0`です。

> **ノート：**
>
> `tidb_stmt_summary_max_stmt_count`の制限を超えたために SQL ステートメントのカテゴリを削除する必要がある場合、TiDB は、すべての時間範囲のその SQL ステートメント カテゴリのデータを`statement_summary_history`テーブルから削除します。そのため、一定時間範囲内のSQL文のカテゴリ数が上限に達していなくても、 `statement_summary_history`のテーブルに格納されるSQL文の数は、実際のSQL文の数よりも少なくなります。この状況が発生してパフォーマンスに影響する場合は、値`tidb_stmt_summary_max_stmt_count`を増やすことをお勧めします。

ステートメントの要約構成の例を以下に示します。

{{< copyable "" >}}

```sql
set global tidb_enable_stmt_summary = true;
set global tidb_stmt_summary_refresh_interval = 1800;
set global tidb_stmt_summary_history_size = 24;
```

上記の構成が有効になると、30 分ごとに`statements_summary`テーブルがクリアされます。 `statements_summary_history`テーブルには、最近 12 時間にわたって生成されたデータが格納されます。

`statements_summary_evicted`テーブルは、SQL ステートメントがステートメントの要約から削除された最近の 24 期間を記録します。 `statements_summary_evicted`テーブルは 30 分ごとに更新されます。

> **ノート：**
>
> `tidb_stmt_summary_history_size` 、 `tidb_stmt_summary_max_stmt_count` 、および`tidb_stmt_summary_max_sql_length`構成アイテムは、メモリ使用量に影響します。ニーズ、SQL サイズ、SQL 数、およびマシン構成に基づいて、これらの構成を調整することをお勧めします。大きすぎる値を設定することはお勧めしません。 `tidb_stmt_summary_history_size` * `tidb_stmt_summary_max_stmt_count` * `tidb_stmt_summary_max_sql_length` * `3`を使用してメモリ使用量を計算できます。

### ステートメントの要約に適切なサイズを設定する {#set-a-proper-size-for-statement-summary}

システムが一定期間 (システムの負荷に応じて) 実行された後、 `statement_summary`テーブルをチェックして、SQL エビクションが発生したかどうかを確認できます。例えば：

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

上記の結果から、最大 59 の SQL カテゴリが削除されていることがわかります。これは、ステートメントの要約の適切なサイズが 59 レコードであることを示しています。

## 制限 {#limitation}

ステートメント要約テーブルには、次の制限があります。

上記のステートメント要約テーブルのすべてのデータは、TiDBサーバーを再起動すると失われます。これは、ステートメント サマリー テーブルがすべてメモリテーブルであり、データがstorageに保持されるのではなく、メモリにキャッシュされるためです。

## トラブルシューティングの例 {#troubleshooting-examples}

このセクションでは、ステートメントの要約機能を使用して SQL パフォーマンスの問題をトラブルシューティングする方法を示す 2 つの例を示します。

### サーバー側が原因で SQLレイテンシーが高くなる可能性はありますか? {#could-high-sql-latency-be-caused-by-the-server-end}

この例では、クライアントは`employee`テーブルに対するポイント クエリでパフォーマンスが低下しています。 SQL テキストに対してあいまい検索を実行できます。

{{< copyable "" >}}

```sql
SELECT avg_latency, exec_count, query_sample_text
    FROM information_schema.statements_summary
    WHERE digest_text LIKE 'select * from employee%';
```

`1ms`と`0.3ms`は`avg_latency`の通常の範囲内と見なされます。したがって、サーバー側が原因ではないと結論付けることができます。クライアントまたはネットワークでトラブルシューティングできます。

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

### 合計時間が最も長い SQL ステートメントのカテゴリはどれですか? {#which-categories-of-sql-statements-consume-the-longest-total-time}

QPS が 10:00 から 10:30 に大幅に減少した場合、履歴テーブルから、消費時間が最も長い SQL ステートメントの 3 つのカテゴリを見つけることができます。

{{< copyable "" >}}

```sql
SELECT sum_latency, avg_latency, exec_count, query_sample_text
    FROM information_schema.statements_summary_history
    WHERE summary_begin_time='2020-01-02 10:00:00'
    ORDER BY sum_latency DESC LIMIT 3;
```

結果は、次の 3 つのカテゴリの SQL ステートメントが合計で最も長い時間を費やしていることを示しており、優先度を高くして最適化する必要があります。

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

以下は、 `statements_summary`テーブルのフィールドの説明です。

基本フィールド:

-   `STMT_TYPE` : SQL ステートメントのタイプ。
-   `SCHEMA_NAME` : このカテゴリの SQL ステートメントが実行される現在のスキーマ。
-   `DIGEST` : このカテゴリの SQL ステートメントのダイジェスト。
-   `DIGEST_TEXT` : 正規化された SQL ステートメント。
-   `QUERY_SAMPLE_TEXT` : SQL カテゴリの元の SQL ステートメント。元のステートメントは 1 つだけ取得されます。
-   `TABLE_NAMES` : SQL ステートメントに含まれるすべてのテーブル。複数のテーブルがある場合は、それぞれをカンマで区切ります。
-   `INDEX_NAMES` : SQL ステートメントで使用されるすべての SQL インデックス。複数のインデックスがある場合は、それぞれをカンマで区切ります。
-   `SAMPLE_USER` : このカテゴリの SQL ステートメントを実行するユーザー。 1 人のユーザーのみが使用されます。
-   `PLAN_DIGEST` : 実行計画のダイジェスト。
-   `PLAN` : 元の実行計画。複数のステートメントがある場合は、1 つのステートメントのみのプランが採用されます。
-   `BINARY_PLAN` : バイナリ形式でエンコードされた元の実行計画。複数のステートメントがある場合は、1 つのステートメントのみのプランが採用されます。 `SELECT tidb_decode_binary_plan('xxx...')`ステートメントを実行して、特定の実行計画を解析します。
-   `PLAN_CACHE_HITS` : このカテゴリの SQL ステートメントがプラン キャッシュにヒットした合計回数。
-   `PLAN_IN_CACHE` : このカテゴリの SQL ステートメントの以前の実行がプラン キャッシュにヒットしたかどうかを示します。

実行時間に関連するフィールド:

-   `SUMMARY_BEGIN_TIME` : 現在の集計期間の開始時刻。
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
-   `AVG_MEM` : 使用された平均メモリ(バイト)。
-   `MAX_MEM` : 使用される最大メモリ(バイト)。
-   `AVG_DISK` : 使用された平均ディスク容量 (バイト)。
-   `MAX_DISK` : 使用されている最大ディスク容量 (バイト)。

TiKVコプロセッサータスクに関連するフィールド:

-   `SUM_COP_TASK_NUM` : 送信されたコプロセッサー要求の総数。
-   `MAX_COP_PROCESS_TIME` :コプロセッサー・タスクの最大実行時間。
-   `MAX_COP_PROCESS_ADDRESS` : 実行時間が最大のコプロセッサー・タスクのアドレス。
-   `MAX_COP_WAIT_TIME` :コプロセッサー・タスクの最大待ち時間。
-   `MAX_COP_WAIT_ADDRESS` : 待ち時間が最大のコプロセッサー・タスクのアドレス。
-   `AVG_PROCESS_TIME` : TiKV での SQL ステートメントの平均処理時間。
-   `MAX_PROCESS_TIME` : TiKV での SQL ステートメントの最大処理時間。
-   `AVG_WAIT_TIME` : TiKV での SQL ステートメントの平均待機時間。
-   `MAX_WAIT_TIME` : TiKV での SQL ステートメントの最大待機時間。
-   `AVG_BACKOFF_TIME` : SQL ステートメントで再試行が必要なエラーが発生した場合の再試行までの平均待機時間。
-   `MAX_BACKOFF_TIME` : SQL ステートメントで再試行が必要なエラーが発生した場合の再試行までの最大待機時間。
-   `AVG_TOTAL_KEYS` :コプロセッサーがスキャンしたキーの平均数。
-   `MAX_TOTAL_KEYS` :コプロセッサーがスキャンしたキーの最大数。
-   `AVG_PROCESSED_KEYS` :コプロセッサーが処理したキーの平均数。 `avg_total_keys`と比較して、 `avg_processed_keys`は古いバージョンの MVCC が含まれていません。 `avg_total_keys`と`avg_processed_keys`の大きな違いは、多くの古いバージョンが存在することを示しています。
-   `MAX_PROCESSED_KEYS` :コプロセッサーが処理したキーの最大数。

トランザクション関連のフィールド:

-   `AVG_PREWRITE_TIME` : プリライト フェーズの平均時間。
-   `MAX_PREWRITE_TIME` : プリライト フェーズの最長時間。
-   `AVG_COMMIT_TIME` : コミット フェーズの平均時間。
-   `MAX_COMMIT_TIME` : コミット フェーズの最長時間。
-   `AVG_GET_COMMIT_TS_TIME` : `commit_ts`を取得する平均時間。
-   `MAX_GET_COMMIT_TS_TIME` : `commit_ts`を取得する最長時間。
-   `AVG_COMMIT_BACKOFF_TIME` : コミット・フェーズ中にSQL文で再試行が必要なエラーが発生した場合の再試行までの平均待機時間。
-   `MAX_COMMIT_BACKOFF_TIME` : コミット・フェーズ中にSQL文で再試行が必要なエラーが発生した場合の再試行までの最大待機時間。
-   `AVG_RESOLVE_LOCK_TIME` : トランザクション間で発生したロックの競合を解決するための平均時間。
-   `MAX_RESOLVE_LOCK_TIME` : トランザクション間で発生したロックの競合を解決するための最長時間。
-   `AVG_LOCAL_LATCH_WAIT_TIME` : ローカル トランザクションの平均待機時間。
-   `MAX_LOCAL_LATCH_WAIT_TIME` : ローカル トランザクションの最大待機時間。
-   `AVG_WRITE_KEYS` : 書き込まれたキーの平均数。
-   `MAX_WRITE_KEYS` : 書き込まれたキーの最大数。
-   `AVG_WRITE_SIZE` : 書き込まれたデータの平均量 (バイト単位)。
-   `MAX_WRITE_SIZE` : 書き込まれたデータの最大量 (バイト単位)。
-   `AVG_PREWRITE_REGIONS` : 事前書き込みフェーズに含まれるリージョンの平均数。
-   `MAX_PREWRITE_REGIONS` : 事前書き込みフェーズ中のリージョンの最大数。
-   `AVG_TXN_RETRY` : トランザクション再試行の平均回数。
-   `MAX_TXN_RETRY` : トランザクション再試行の最大数。
-   `SUM_BACKOFF_TIMES` : このカテゴリの SQL ステートメントで再試行が必要なエラーが発生した場合の再試行の合計。
-   `BACKOFF_TYPES` : 再試行が必要なすべてのタイプのエラーと、各タイプの再試行回数。フィールドの形式は`type:number`です。複数のエラー タイプがある場合は、それぞれを`txnLock:2,pdRPC:1`のようにコンマで区切ります。
-   `AVG_AFFECTED_ROWS` : 影響を受ける行の平均数。
-   `PREV_SAMPLE_TEXT` : 現在の SQL ステートメントが`COMMIT`の場合、 `PREV_SAMPLE_TEXT`は`COMMIT`までの前のステートメントです。この場合、SQL ステートメントはダイジェストと`prev_sample_text`でグループ化されます。これは、異なる`prev_sample_text`の`COMMIT`ステートメントが異なる行にグループ化されることを意味します。現在の SQL ステートメントが`COMMIT`でない場合、 `PREV_SAMPLE_TEXT`フィールドは空の文字列です。

### <code>statements_summary_evicted</code>フィールドの説明 {#code-statements-summary-evicted-code-fields-description}

-   `BEGIN_TIME` : 開始時刻を記録します。
-   `END_TIME` : 終了時刻を記録します。
-   `EVICTED_COUNT` : 記録期間中に削除された SQL カテゴリの数。
