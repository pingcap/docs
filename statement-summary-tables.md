---
title: Statement Summary Tables
summary: TiDB のステートメント サマリー テーブルについて学習します。
---

# 明細書要約表 {#statement-summary-tables}

SQLパフォーマンスの問題をより適切に処理するために、MySQLは統計情報を使用してSQLを監視するためのテーブルを[明細書要約表](https://dev.mysql.com/doc/refman/8.0/en/performance-schema-statement-summary-tables.html) `performance_schema`提供しています。これらのテーブルのうち、 `events_statements_summary_by_digest`レイテンシー、実行時間、スキャンされた行数、フルテーブルスキャンなどの豊富なフィールドを備えており、SQLの問題を特定するのに非常に役立ちます。

したがって、v4.0.0-rc.1 以降、TiDB は機能面で`events_statements_summary_by_digest`に類似したシステム テーブルを`information_schema` ( `performance_schema`*ではありません*) で提供します。

-   [`statements_summary`](#statements_summary)
-   [`statements_summary_history`](#statements_summary_history)
-   [`cluster_statements_summary`](#statements_summary_evicted)
-   [`cluster_statements_summary_history`](#statements_summary_evicted)
-   [`statements_summary_evicted`](#statements_summary_evicted)

> **注記：**
>
> 上記のテーブルは、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では使用できません。

このドキュメントでは、これらのテーブルについて詳しく説明し、それらを使用して SQL パフォーマンスの問題をトラブルシューティングする方法を紹介します。

## <code>statements_summary</code> {#code-statements-summary-code}

`statements_summary`は`information_schema`のシステム テーブルです。4 `statements_summary` SQL ステートメントをリソース グループ、SQL ダイジェスト、プラン ダイジェスト別にグループ化し、各 SQL カテゴリの統計を提供します。

ここでの「SQLダイジェスト」は、スローログで使用されるものと同じ意味を持ち、正規化されたSQL文から算出される一意の識別子です。正規化プロセスでは、定数や空白文字は無視され、大文字と小文字は区別されません。したがって、構文が一致する文は同じダイジェストを持ちます。例：

```sql
SELECT * FROM employee WHERE id IN (1, 2, 3) AND salary BETWEEN 1000 AND 2000;
select * from EMPLOYEE where ID in (4, 5) and SALARY between 3000 and 4000;
```

正規化後、両方とも次のカテゴリに分類されます。

```sql
select * from employee where id in (...) and salary between ? and ?;
```

ここでの「プランダイジェスト」とは、正規化された実行プランから算出される一意の識別子を指します。正規化プロセスでは定数は無視されます。同じSQL文が異なる実行プランを持つ場合があるため、同じSQL文が異なるカテゴリにグループ化されることがあります。同じカテゴリのSQL文は同じ実行プランを持ちます。

`statements_summary` 、SQL 監視メトリックの集計結果が格納されます。通常、各監視メトリックには最大値と平均値が含まれます。例えば、実行レイテンシーメトリックは、 `AVG_LATENCY` （平均レイテンシー）と`MAX_LATENCY` （最大レイテンシー）の 2 つのフィールドに対応します。

監視メトリックを最新に保つため、 `statements_summary`テーブルのデータは定期的にクリアされ、最新の集計結果のみが保持・表示されます。定期的なデータクリアは`tidb_stmt_summary_refresh_interval`システム変数によって制御されます。クリア直後にクエリを実行した場合、表示されるデータが非常に少なくなる可能性があります。

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
> -   TiDB では、ステートメント サマリー テーブルのフィールドの時間単位はナノ秒 (ns) ですが、MySQL では時間単位はピコ秒 (ps) です。
> -   v7.5.1 および v7.6.0 以降では、 [資源管理](/tidb-resource-control-ru-groups.md)有効になっているクラスターの場合、 `statements_summary`リソース グループごとに集計されます。たとえば、異なるリソース グループで実行された同じステートメントは、異なるレコードとして収集されます。

## <code>statements_summary_history</code> {#code-statements-summary-history-code}

`statements_summary_history`のテーブルスキーマは`statements_summary`と同一です。5 `statements_summary_history`指定した時間範囲の履歴データを保存します。履歴データを確認することで、異常のトラブルシューティングや、異なる時間範囲の監視メトリクスの比較が可能になります。

フィールド`SUMMARY_BEGIN_TIME`と`SUMMARY_END_TIME` 、履歴時間範囲の開始時刻と終了時刻を表します。

## <code>statements_summary_evicted</code> {#code-statements-summary-evicted-code}

システム変数[`tidb_stmt_summary_max_stmt_count`](/system-variables.md#tidb_stmt_summary_max_stmt_count-new-in-v40) 、テーブル`statements_summary`と`statements_summary_history`メモリに格納できる SQL ダイジェストの総数を制限します。この制限を超えると、TiDB はテーブル`statements_summary`と`statements_summary_history`から最も使用頻度の低い SQL ダイジェストを削除します。

<CustomContent platform="tidb">

> **注記：**
>
> [`tidb_stmt_summary_enable_persistent`](#persist-statements-summary)有効にすると、 `statements_summary_history`テーブルのデータがディスクに永続化されます。この場合、 `tidb_stmt_summary_max_stmt_count` `statements_summary`テーブルがメモリに保存できる SQL ダイジェストの数のみを制限し、 `tidb_stmt_summary_max_stmt_count`を超えた場合にのみ、TiDB は`statements_summary`テーブルから最も使用頻度の低い SQL ダイジェストを削除します。

</CustomContent>

`statements_summary_evicted`テーブルは、エビクションが発生した期間と、その期間中にエビクションされた SQL ダイジェストの数を記録します。このテーブルは、 `tidb_stmt_summary_max_stmt_count`ワークロードに対して適切に設定されているかどうかを評価するのに役立ちます。このテーブルにレコードが含まれている場合、ある時点で SQL ダイジェストの数が`tidb_stmt_summary_max_stmt_count`超えたことを示します。

<CustomContent platform="tidb">

[TiDBダッシュボードのSQLステートメントページ](/dashboard/dashboard-statement-list.md#others)では、削除されたステートメントに関する情報が`Others`行目に表示されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

[診断ページのSQL文タブ](/tidb-cloud/tune-performance.md#statement-analysis)では、削除されたステートメントに関する情報が`Others`行目に表示されます。

</CustomContent>

## ステートメントサマリーの<code>cluster</code>テーブル {#the-code-cluster-code-tables-for-statement-summary}

`statements_summary` 、 `statements_summary_history` 、 `statements_summary_evicted`テーブルには、単一の TiDBサーバーのステートメントサマリーのみが表示されます。クラスター全体のデータをクエリするには、 `cluster_statements_summary` 、 `cluster_statements_summary_history` 、または`cluster_statements_summary_evicted`テーブルをクエリする必要があります。

`cluster_statements_summary`各 TiDBサーバーの`statements_summary`データを表示します。4 `cluster_statements_summary_history`各 TiDBサーバーの`statements_summary_history`データを表示します。8 `cluster_statements_summary_evicted`各 TiDBサーバーの`statements_summary_evicted`データを表示します。これらのテーブルでは、 `INSTANCE`番目のフィールドを使用して TiDBサーバーのアドレスを表します。その他のフィールドは`statements_summary` 、 `statements_summary_history` 、 `statements_summary_evicted`と同じです。

## パラメータ設定 {#parameter-configuration}

ステートメント サマリーを制御するために、次のシステム変数が使用されます。

-   `tidb_enable_stmt_summary` : ステートメントサマリー機能を有効にするかどうかを決定します。2 `1` `enable` 、 `0`は`disable`表します。この機能はデフォルトで有効になっています。この機能を無効にすると、システムテーブルの統計情報はクリアされます。統計情報は、次回この機能が有効になったときに再計算されます。テストの結果、この機能を有効にしてもパフォーマンスへの影響はほとんどないことが示されています。

-   `tidb_stmt_summary_refresh_interval` : テーブル`statements_summary`を更新する間隔。時間単位は秒（s）です。デフォルト値は`1800`です。

-   `tidb_stmt_summary_history_size` : テーブル`statements_summary_history`に格納される各SQL文カテゴリのサイズ。これはテーブル`statements_summary_evicted`の最大レコード数でもあります。デフォルト値は`24`です。

-   `tidb_stmt_summary_max_stmt_count` : テーブル`statements_summary`とテーブル`statements_summary_history`がメモリに格納できるSQLダイジェストの総数を制限します。デフォルト値は`3000`です。

    この制限を超えると、TiDBはテーブル`statements_summary`とテーブル`statements_summary_history`の両方から、最も最近使用されていないSQLダイジェストを削除します。これらの削除されたダイジェストは、テーブル[`statements_summary_evicted`](#statements_summary_evicted)にカウントされます。

    > **注記：**
    >
    > -   SQLダイジェストが削除されると、関連する全時間範囲のサマリーデータがテーブル`statements_summary`とテーブル`statements_summary_history`の両方から削除されます。その結果、特定の時間範囲内のSQLダイジェストの数が制限を超えていない場合でも、テーブル`statements_summary_history`のSQLダイジェストの数が実際のSQLダイジェストの数よりも少なくなる可能性があります。このような状況が発生し、パフォーマンスに影響する場合は、テーブル`tidb_stmt_summary_max_stmt_count`の値を増やすことをお勧めします。
    > -   TiDBセルフマネージドの場合、 [`tidb_stmt_summary_enable_persistent`](#persist-statements-summary)有効になっていると、 `statements_summary_history`テーブルのデータがディスクに永続化されます。この場合、 `tidb_stmt_summary_max_stmt_count` `statements_summary`テーブルがメモリに保存できるSQLダイジェストの数のみを制限し、 `tidb_stmt_summary_max_stmt_count`を超えた場合にのみ、TiDBは`statements_summary`テーブルから最も使用頻度の低いSQLダイジェストを削除します。

-   `tidb_stmt_summary_max_sql_length` : `DIGEST_TEXT`と`QUERY_SAMPLE_TEXT`うち最長の表示長を指定します。デフォルト値は`4096`です。

-   `tidb_stmt_summary_internal_query` : TiDB SQL文をカウントするかどうかを決定します。2 `1`カウントし、 `0`はカウントしないことを意味します。デフォルト値は`0`です。

ステートメント サマリー構成の例を次に示します。

```sql
set global tidb_stmt_summary_max_stmt_count = 3000;
set global tidb_enable_stmt_summary = true;
set global tidb_stmt_summary_refresh_interval = 1800;
set global tidb_stmt_summary_history_size = 24;
```

上記の設定が有効になると、テーブル`statements_summary`は30分ごとにクリアされ、テーブル`statements_summary_history`には最大3000種類のSQL文が格納されます。テーブル`statements_summary_history`には、各種類について過去24期間分のデータが格納されます。テーブル`statements_summary_evicted`には、SQL文がステートメントサマリーから削除された過去24期間分のデータが記録されます。テーブル`statements_summary_evicted`は30分ごとに更新されます。

> **注記：**
>
> -   SQLタイプが毎分出現する場合、 `statements_summary_history`直近12時間分のデータを保存します。SQLタイプが毎日00:00から00:30までしか出現しない場合、 `statements_summary_history`は直近24期間分のデータを保存します（各期間は1日）。したがって、 `statements_summary_history`直近24日間分のSQLタイプを保存します。
> -   `tidb_stmt_summary_history_size` `tidb_stmt_summary_max_stmt_count`設定項目はメモリ使用量に影響します。これらの設定は、ニーズ、SQLサイズ、SQL数、マシン構成に応じて調整することをお勧めします。あまり大きな値`tidb_stmt_summary_max_sql_length`設定することは推奨されません。メモリ使用量は`tidb_stmt_summary_history_size` * `tidb_stmt_summary_max_stmt_count` * `tidb_stmt_summary_max_sql_length` * `3`で計算できます。

### ステートメントサマリーの適切なサイズを設定する {#set-a-proper-size-for-statement-summary}

システムを一定時間（システム負荷によって異なります）稼働させた後、 `statement_summary`テーブルをチェックして、SQL のエビクションが発生しているかどうかを確認できます。例:

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

`statements_summary`テーブルがレコードでいっぱいになっていることがわかります。次に、 `statements_summary_evicted`番目のテーブルから削除されたデータを確認します。

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

上記の結果から、最大59個のSQLカテゴリが削除されていることがわかります。この場合、テーブル`statement_summary`のサイズを少なくとも59レコード分、つまり3059レコード以上に増やすことをお勧めします。

## 制限 {#limitation}

デフォルトでは、ステートメントサマリーテーブルはメモリに保存されます。TiDBサーバーが再起動すると、すべてのデータが失われます。

<CustomContent platform="tidb">

この問題に対処するため、TiDB v6.6.0では、デフォルトで無効になっている[ステートメントサマリーの永続性](#persist-statements-summary)機能を試験的に導入しました。この機能を有効にすると、履歴データはメモリに保存されなくなり、ディスクに直接書き込まれるようになります。これにより、TiDBサーバーを再起動しても履歴データは引き続き利用できます。

</CustomContent>

## 永続ステートメントの概要 {#persist-statements-summary}

<CustomContent platform="tidb-cloud">

このセクションは TiDB Self-Managed にのみ適用されます。TiDB TiDB Cloudの場合、 `tidb_stmt_summary_enable_persistent`パラメータの値はデフォルトで`false`設定されており、動的な変更はサポートされません。

</CustomContent>

> **警告：**
>
> ステートメントサマリーの永続化は実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

<CustomContent platform="tidb">

セクション[制限](#limitation)で説明したように、ステートメントサマリーテーブルはデフォルトでメモリに保存されます。TiDBサーバーが再起動すると、すべてのステートメントサマリーは失われます。v6.6.0以降、TiDBは設定項目[`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-new-in-v660)試験的に提供し、ユーザーがステートメントサマリーの永続性を有効または無効にできるようになりました。

</CustomContent>

<CustomContent platform="tidb-cloud">

セクション[制限](#limitation)で説明したように、ステートメントサマリーテーブルはデフォルトでメモリに保存されます。TiDBサーバーが再起動すると、すべてのステートメントサマリーは失われます。v6.6.0以降、TiDBは設定項目`tidb_stmt_summary_enable_persistent`試験的に提供し、ユーザーがステートメントサマリーの永続性を有効または無効にできるようになりました。

</CustomContent>

ステートメント サマリーの永続性を有効にするには、次の構成項目を TiDB 構成ファイルに追加します。

```toml
[instance]
tidb_stmt_summary_enable_persistent = true
# The following entries use the default values, which can be modified as needed.
# tidb_stmt_summary_filename = "tidb-statements.log"
# tidb_stmt_summary_file_max_days = 3
# tidb_stmt_summary_file_max_size = 64 # MiB
# tidb_stmt_summary_file_max_backups = 0
```

ステートメントサマリーの永続化を有効にすると、メモリには現在のリアルタイムデータのみが保持され、履歴データは保持されません。リアルタイムデータが履歴データとして更新されると、履歴データは[パラメータ設定](#parameter-configuration)セクションで説明した間隔`tidb_stmt_summary_refresh_interval`でディスクに書き込まれます。5または`cluster_statements_summary_history` `statements_summary_history`に対するクエリは、メモリ内データとディスク上のデータの両方を組み合わせた結果を返します。

<CustomContent platform="tidb">

> **注記：**
>
> -   ステートメントサマリーの永続化を有効にすると、メモリが履歴データを保持しなくなるため、セクション[パラメータ設定](#parameter-configuration)で説明した`tidb_stmt_summary_history_size`設定は適用されなくなります。代わりに、 [`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-new-in-v660) [`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-new-in-v660) 3つの設定を使用して[`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-new-in-v660)永続化のための履歴データの保持期間とサイズを制御します。
> -   `tidb_stmt_summary_refresh_interval`の値が小さいほど、ディスクに書き込まれる即時データが多くなります。ただし、これは冗長データもディスクに書き込まれることを意味します。

</CustomContent>

## トラブルシューティングの例 {#troubleshooting-examples}

このセクションでは、ステートメント サマリー機能を使用して SQL パフォーマンスの問題をトラブルシューティングする方法を示す 2 つの例を示します。

### 高い SQLレイテンシーはサーバー側で発生している可能性がありますか? {#could-high-sql-latency-be-caused-by-the-server-end}

この例では、クライアントはテーブル`employee`に対するポイントクエリでパフォーマンスが低下しています。SQLテキストに対してあいまい検索を実行できます。

```sql
SELECT avg_latency, exec_count, query_sample_text
    FROM information_schema.statements_summary
    WHERE digest_text LIKE 'select * from employee%';
```

`1ms`と`0.3ms` `avg_latency`の正常範囲内と考えられます。したがって、サーバー側が原因ではないと考えられます。クライアント側またはネットワーク側でトラブルシューティングを行うことができます。

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

10:00 から 10:30 にかけて QPS が大幅に減少した場合、履歴テーブルから、最も時間のかかる SQL 文の 3 つのカテゴリを見つけることができます。

```sql
SELECT sum_latency, avg_latency, exec_count, query_sample_text
    FROM information_schema.statements_summary_history
    WHERE summary_begin_time='2020-01-02 10:00:00'
    ORDER BY sum_latency DESC LIMIT 3;
```

結果から、次の 3 つのカテゴリの SQL 文が合計で最も長い時間を消費しており、優先度を高くして最適化する必要があることがわかります。

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

以下は`statements_summary`テーブル内のフィールドの説明です。

基本フィールド:

-   `STMT_TYPE` : SQL ステートメントの種類。
-   `SCHEMA_NAME` : このカテゴリの SQL ステートメントが実行される現在のスキーマ。
-   `DIGEST` : このカテゴリの SQL ステートメントのダイジェスト。
-   `DIGEST_TEXT` : 正規化された SQL ステートメント。
-   `QUERY_SAMPLE_TEXT` : SQLカテゴリの元のSQL文。元の文は1つだけ取得されます。
-   `TABLE_NAMES` : SQL文に関係するすべてのテーブル。複数のテーブルがある場合は、各テーブルはカンマで区切られます。
-   `INDEX_NAMES` : SQL文で使用されるすべてのSQLインデックス。複数のインデックスがある場合は、それぞれがカンマで区切られます。
-   `SAMPLE_USER` : このカテゴリのSQL文を実行するユーザー。1人のみ取得されます。
-   `PLAN_DIGEST` : 実行プランのダイジェスト。
-   `PLAN` : 元の実行プラン。複数のステートメントがある場合は、1つのステートメントのプランのみが採用されます。
-   `BINARY_PLAN` : バイナリ形式でエンコードされた元の実行プラン。複数のステートメントがある場合は、1つのステートメントのプランのみが採用されます。特定の実行プランを解析するには、 [`SELECT tidb_decode_binary_plan('xxx...')`](/functions-and-operators/tidb-functions.md#tidb_decode_binary_plan)ステートメントを実行します。
-   `PLAN_CACHE_HITS` : このカテゴリの SQL ステートメントがプラン キャッシュにヒットした合計回数。
-   `PLAN_IN_CACHE` : このカテゴリの SQL ステートメントの前回の実行がプラン キャッシュにヒットしたかどうかを示します。
-   `PLAN_CACHE_UNQUALIFIED` : このカテゴリの SQL ステートメントがプラン キャッシュにヒットできなかった回数。
-   `PLAN_CACHE_UNQUALIFIED_LAST_REASON` : このカテゴリの SQL ステートメントが前回プラン キャッシュにヒットできなかった理由。

実行時間に関連するフィールド:

-   `SUMMARY_BEGIN_TIME` : 現在の要約期間の開始時刻。
-   `SUMMARY_END_TIME` : 現在の要約期間の終了時刻。
-   `FIRST_SEEN` : このカテゴリの SQL 文が初めて表示された時刻。
-   `LAST_SEEN` : このカテゴリの SQL 文が最後に確認された時刻。

<CustomContent platform="tidb">

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
-   `MAX_DISK` : 使用される最大ディスク容量 (バイト)。
-   `AVG_TIDB_CPU_TIME` : このカテゴリのSQL文が消費するTiDBサーバーCPU時間の平均。2 [Top SQL](/dashboard/top-sql.md)が有効な場合にのみ意味のある値が表示されます。それ以外の場合は、値は常に`0`です。

</CustomContent>

<CustomContent platform="tidb-cloud">

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
-   `MAX_DISK` : 使用される最大ディスク容量 (バイト)。
-   `AVG_TIDB_CPU_TIME` : このカテゴリのSQL文が消費するTiDBサーバーCPU時間の平均。Top Top SQL機能が有効になっている場合にのみ意味のある値が表示されます。それ以外の場合は、値は常に`0`です。

</CustomContent>

TiKVコプロセッサータスクに関連するフィールド:

-   `SUM_COP_TASK_NUM` : 送信されたコプロセッサー要求の合計数。
-   `MAX_COP_PROCESS_TIME` :コプロセッサータスクの最大実行時間。
-   `MAX_COP_PROCESS_ADDRESS` : 実行時間が最大となるコプロセッサータスクのアドレス。
-   `MAX_COP_WAIT_TIME` :コプロセッサータスクの最大待機時間。
-   `MAX_COP_WAIT_ADDRESS` : 最大待機時間を持つコプロセッサータスクのアドレス。
-   `AVG_PROCESS_TIME` : TiKV 内の SQL ステートメントの平均処理時間。
-   `MAX_PROCESS_TIME` : TiKV での SQL ステートメントの最大処理時間。
-   `AVG_WAIT_TIME` : TiKV 内の SQL ステートメントの平均待機時間。
-   `MAX_WAIT_TIME` : TiKV での SQL ステートメントの最大待機時間。
-   `AVG_BACKOFF_TIME` : SQL ステートメントで再試行を必要とするエラーが発生した場合の再試行前の平均待機時間。
-   `MAX_BACKOFF_TIME` : SQL ステートメントで再試行を必要とするエラーが発生した場合の再試行前の最大待機時間。
-   `AVG_TOTAL_KEYS` :コプロセッサーがスキャンしたキーの平均数。
-   `MAX_TOTAL_KEYS` :コプロセッサーがスキャンしたキーの最大数。
-   `AVG_PROCESSED_KEYS` :コプロセッサーが処理したキーの平均数。2 と比較すると、 `avg_total_keys` `avg_processed_keys`は古いバージョンの MVCC は含まれていません。6 と`avg_total_keys` `avg_processed_keys`差が大きいことから、古いバージョンが多数存在することがわかります。
-   `MAX_PROCESSED_KEYS` :コプロセッサーが処理したキーの最大数。
-   `AVG_TIKV_CPU_TIME` : このカテゴリの SQL ステートメントが消費する TiKVサーバーCPU 時間の平均。

取引関連のフィールド:

-   `AVG_PREWRITE_TIME` : 事前書き込みフェーズの平均時間。
-   `MAX_PREWRITE_TIME` : 事前書き込みフェーズの最長時間。
-   `AVG_COMMIT_TIME` : コミット フェーズの平均時間。
-   `MAX_COMMIT_TIME` : コミット フェーズの最長時間。
-   `AVG_GET_COMMIT_TS_TIME` : `commit_ts`を取得する平均時間。
-   `MAX_GET_COMMIT_TS_TIME` : `commit_ts`を取得するのに要した最長時間。
-   `AVG_COMMIT_BACKOFF_TIME` : コミット フェーズ中に SQL ステートメントで再試行を必要とするエラーが発生した場合の再試行までの平均待機時間。
-   `MAX_COMMIT_BACKOFF_TIME` : コミット フェーズ中に SQL ステートメントで再試行を必要とするエラーが発生した場合の再試行前の最大待機時間。
-   `AVG_RESOLVE_LOCK_TIME` : トランザクション間で発生したロックの競合を解決するための平均時間。
-   `MAX_RESOLVE_LOCK_TIME` : トランザクション間で発生したロックの競合を解決するのに最も長い時間がかかりました。
-   `AVG_LOCAL_LATCH_WAIT_TIME` : ローカル トランザクションの平均待機時間。
-   `MAX_LOCAL_LATCH_WAIT_TIME` : ローカル トランザクションの最大待機時間。
-   `AVG_WRITE_KEYS` : 書き込まれたキーの平均数。
-   `MAX_WRITE_KEYS` : 書き込まれたキーの最大数。
-   `AVG_WRITE_SIZE` : 書き込まれたデータの平均量 (バイト単位)。
-   `MAX_WRITE_SIZE` : 書き込まれたデータの最大量（バイト単位）。
-   `AVG_PREWRITE_REGIONS` : 事前書き込みフェーズに関係する領域の平均数。
-   `MAX_PREWRITE_REGIONS` : 事前書き込みフェーズ中のリージョンの最大数。
-   `AVG_TXN_RETRY` : トランザクション再試行の平均回数。
-   `MAX_TXN_RETRY` : トランザクション再試行の最大回数。
-   `SUM_BACKOFF_TIMES` : このカテゴリの SQL 文で再試行が必要なエラーが発生した場合の再試行の合計。
-   `BACKOFF_TYPES` : 再試行が必要なすべてのエラーの種類と、各種類の再試行回数。フィールドの形式は`type:number`です。エラーの種類が複数ある場合は、それぞれをカンマで区切ります（例： `txnLock:2,pdRPC:1` ）。
-   `AVG_AFFECTED_ROWS` : 影響を受ける行の平均数。
-   `PREV_SAMPLE_TEXT` : 現在のSQL文が`COMMIT`場合、 `PREV_SAMPLE_TEXT`は`COMMIT`の前の文です。この場合、SQL文はダイジェストと`prev_sample_text`によってグループ化されます。つまり、 `prev_sample_text`が異なる`COMMIT`の文が異なる行にグループ化されます。現在のSQL文が`COMMIT`でない場合、 `PREV_SAMPLE_TEXT`フィールドは空文字列になります。

リソース制御に関連するフィールド:

-   `AVG_REQUEST_UNIT_WRITE` : SQL ステートメントによって消費される書き込み RU の平均数。
-   `MAX_REQUEST_UNIT_WRITE` : SQL ステートメントによって消費される書き込み RU の最大数。
-   `AVG_REQUEST_UNIT_READ` : SQL ステートメントによって消費される読み取り RU の平均数。
-   `MAX_REQUEST_UNIT_READ` : SQL ステートメントによって消費される読み取り RU の最大数。
-   `AVG_QUEUED_RC_TIME` : SQL ステートメントを実行するときに使用可能な RU を待機する平均時間。
-   `MAX_QUEUED_RC_TIME` : SQL ステートメントを実行するときに使用可能な RU の最大待機時間。
-   `RESOURCE_GROUP` : SQL ステートメントにバインドされたリソース グループ。

storageエンジンに関連するフィールド:

-   `STORAGE_KV` : v8.5.5 で導入され、このカテゴリの SQL ステートメントの前回の実行で TiKV からデータが読み取られたかどうかを示します。
-   `STORAGE_MPP` : v8.5.5 で導入され、このカテゴリの SQL ステートメントの前回の実行でTiFlashからデータを読み取ったかどうかを示します。

### <code>statements_summary_evicted</code>フィールドの説明 {#code-statements-summary-evicted-code-fields-description}

-   `BEGIN_TIME` : 開始時刻を記録します。
-   `END_TIME` : 終了時刻を記録します。
-   `EVICTED_COUNT` : 記録期間中に削除された SQL カテゴリの数。
