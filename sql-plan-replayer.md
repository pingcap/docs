---
title: Use PLAN REPLAYER to Save and Restore the On-Site Information of a Cluster
summary: PLAN REPLAYER を使用してクラスターのオンサイト情報を保存および復元する方法を学びます。
---

# PLAN REPLAYERを使用してクラスタのオンサイト情報を保存および復元する {#use-plan-replayer-to-save-and-restore-the-on-site-information-of-a-cluster}

TiDB クラスターの問題を特定してトラブルシューティングする場合、多くの場合、システムと実行プランに関する情報を提供する必要があります。より便利かつ効率的に情報を取得し、クラスターの問題をトラブルシューティングできるように、TiDB v5.3.0 では`PLAN REPLAYER`コマンドが導入されています。このコマンドを使用すると、クラスターのオンサイト情報を簡単に保存および復元でき、トラブルシューティングの効率が向上し、管理のために問題をより簡単にアーカイブできるようになります。

`PLAN REPLAYER`の特徴は以下の通りです。

-   オンサイトトラブルシューティング時の TiDB クラスターの情報を ZIP 形式のファイルにエクスポートしてstorage。
-   別の TiDB クラスターからエクスポートされた ZIP 形式のファイルをクラスターにインポートします。このファイルには、オンサイト トラブルシューティング時の後者の TiDB クラスターの情報が含まれています。

## <code>PLAN REPLAYER</code>使用してクラスター情報をエクスポートする {#use-code-plan-replayer-code-to-export-cluster-information}

`PLAN REPLAYER`使用すると、TiDB クラスターのオンサイト情報を保存できます。エクスポート インターフェイスは次のとおりです。

```sql
PLAN REPLAYER DUMP [WITH STATS AS OF TIMESTAMP expression] EXPLAIN [ANALYZE] sql-statement;
```

TiDB は`sql-statement`に基づいて、次のオンサイト情報を整理してエクスポートします。

-   TiDB バージョン
-   TiDB 構成
-   TiDBセッション変数
-   TiDB SQLバインディング
-   `sql-statement`のテーブルスキーマ
-   `sql-statement`の表の統計
-   `EXPLAIN [ANALYZE] sql-statement`の結果
-   クエリ最適化の内部手順

履歴統計が[有効](/system-variables.md#tidb_enable_historical_stats)場合、 `PLAN REPLAYER`ステートメントで時間を指定して、対応する時間の履歴統計を取得できます。時間と日付を直接指定することも、タイムスタンプを指定することもできます。TiDB は、指定された時間より前の履歴統計を検索し、その中から最新のものをエクスポートします。

指定された時間より前の履歴統計がない場合、TiDB は最新の統計をエクスポートします。これは、時間が指定されていない場合の動作と一致します。また、TiDB は、エクスポートされた`ZIP`ファイル内に`errors.txt`ファイルのエラー メッセージを出力。

> **注記：**
>
> `PLAN REPLAYER`テーブル データをエクスポート**しません**。

### クラスター情報のエクスポートの例 {#examples-of-exporting-cluster-information}

```sql
use test;
create table t(a int, b int);
insert into t values(1,1), (2, 2), (3, 3);
analyze table t;

plan replayer dump explain select * from t;
plan replayer dump with stats as of timestamp '2023-07-17 12:00:00' explain select * from t;
plan replayer dump with stats as of timestamp '442012134592479233' explain select * from t;
```

`PLAN REPLAYER DUMP`上記のテーブル情報を`ZIP`ファイルにパッケージ化し、実行結果としてファイル識別子を返します。

> **注記：**
>
> `ZIP`ファイルは最大 1 時間 TiDB クラスターに保存されます。1 時間経過すると、TiDB によって削除されます。

```sql
MySQL [test]> plan replayer dump explain select * from t;
```

```sql
+------------------------------------------------------------------+
| Dump_link                                                        |
+------------------------------------------------------------------+
| replayer_JOGvpu4t7dssySqJfTtS4A==_1635750890568691080.zip |
+------------------------------------------------------------------+
1 row in set (0.015 sec)
```

あるいは、セッション変数[`tidb_last_plan_replayer_token`](/system-variables.md#tidb_last_plan_replayer_token-new-in-v630)使用して、最後の`PLAN REPLAYER DUMP`の実行の結果を取得することもできます。

```sql
SELECT @@tidb_last_plan_replayer_token;
```

```sql
+-----------------------------------------------------------+
| @@tidb_last_plan_replayer_token                           |
+-----------------------------------------------------------+
| replayer_Fdamsm3C7ZiPJ-LQqgVjkA==_1663304195885090000.zip |
+-----------------------------------------------------------+
1 row in set (0.00 sec)
```

SQL文が複数ある場合、 `PLAN REPLAYER DUMP`の実行結果をファイルで取得することができます。このファイルでは複数のSQL文の結果が`;`つに区切られています。

```sql
plan replayer dump explain 'sqls.txt';
```

```sql
Query OK, 0 rows affected (0.03 sec)
```

```sql
SELECT @@tidb_last_plan_replayer_token;
```

```sql
+-----------------------------------------------------------+
| @@tidb_last_plan_replayer_token                           |
+-----------------------------------------------------------+
| replayer_LEDKg8sb-K0u24QesiH8ig==_1663226556509182000.zip |
+-----------------------------------------------------------+
1 row in set (0.00 sec)
```

ファイルは MySQL クライアントではダウンロードできないため、TiDB HTTP インターフェイスとファイル識別子を使用してファイルをダウンロードする必要があります。

```shell
http://${tidb-server-ip}:${tidb-server-status-port}/plan_replayer/dump/${file_token}
```

`${tidb-server-ip}:${tidb-server-status-port}`クラスター内の任意の TiDBサーバーのアドレスです。例:

```shell
curl http://127.0.0.1:10080/plan_replayer/dump/replayer_JOGvpu4t7dssySqJfTtS4A==_1635750890568691080.zip > plan_replayer.zip
```

## <code>PLAN REPLAYER</code>使用してクラスター情報をインポートする {#use-code-plan-replayer-code-to-import-cluster-information}

> **警告：**
>
> TiDB クラスターのオンサイト情報を別のクラスターにインポートすると、後者のクラスターの TiDB セッション変数、SQL バインディング、テーブル スキーマ、および統計が変更されます。

`PLAN REPLAYER`使用してエクスポートされた既存の`ZIP`ファイルを使用すると、 `PLAN REPLAYER`インポート インターフェイスを使用して、クラスターのオンサイト情報を他の TiDB クラスターに復元できます。構文は次のとおりです。

```sql
PLAN REPLAYER LOAD 'file_name';
```

上記のステートメントでは、 `file_name`インポートする`ZIP`ファイルの名前です。

例えば：

```sql
PLAN REPLAYER LOAD 'plan_replayer.zip';
```

> **注記：**
>
> auto analyzeを無効にする必要があります。そうしないと、インポートされた統計が分析によって上書きされます。

[`tidb_enable_auto_analyze`](/system-variables.md#tidb_enable_auto_analyze-new-in-v610)システム変数を`OFF`に設定することで、auto analyzeを無効にすることができます。

```sql
set @@global.tidb_enable_auto_analyze = OFF;
```

クラスター情報がインポートされると、必要なテーブル スキーマ、統計、および実行プランの構築に影響するその他の情報が TiDB クラスターにロードされます。次の方法で実行プランを表示し、統計を確認できます。

```sql
mysql> desc t;
+-------+---------+------+------+---------+-------+
| Field | Type    | Null | Key  | Default | Extra |
+-------+---------+------+------+---------+-------+
| a     | int(11) | YES  |      | NULL    |       |
| b     | int(11) | YES  |      | NULL    |       |
+-------+---------+------+------+---------+-------+
2 rows in set (0.01 sec)

mysql> explain select * from t where a = 1 or b =1;
+-------------------------+---------+-----------+---------------+--------------------------------------+
| id                      | estRows | task      | access object | operator info                        |
+-------------------------+---------+-----------+---------------+--------------------------------------+
| TableReader_7           | 0.01    | root      |               | data:Selection_6                     |
| └─Selection_6           | 0.01    | cop[tikv] |               | or(eq(test.t.a, 1), eq(test.t.b, 1)) |
|   └─TableFullScan_5     | 6.00    | cop[tikv] | table:t       | keep order:false, stats:pseudo       |
+-------------------------+---------+-----------+---------------+--------------------------------------+
3 rows in set (0.00 sec)

mysql> show stats_meta;
+---------+------------+----------------+---------------------+--------------+-----------+
| Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count |
+---------+------------+----------------+---------------------+--------------+-----------+
| test    | t          |                | 2022-08-26 15:52:07 |            3 |         6 |
+---------+------------+----------------+---------------------+--------------+-----------+
1 row in set (0.04 sec)
```

シーンが読み込まれて復元されたら、クラスターの実行プランを診断して改善できます。

> **注記：**
>
> `mysql`コマンドライン クライアントを使用していて`ERROR 2068 (HY000): LOAD DATA LOCAL INFILE file request rejected due to restrictions on access.`遭遇した場合は、接続文字列に`--local-infile=true`を追加できます。

## <code>PLAN REPLAYER CAPTURE</code>使用してターゲットプランをキャプチャします {#use-code-plan-replayer-capture-code-to-capture-target-plans}

いくつかのシナリオで TiDB の実行プランを検索する場合、ターゲット SQL ステートメントとターゲット実行プランがクエリ内にたまにしか表示されないため、 `PLAN REPLAYER`使用してステートメントとプランを直接キャプチャすることはできません。このような場合は、 `PLAN REPLAYER CAPTURE`使用して、ターゲット SQL ステートメントとターゲット プランのオプティマイザー情報を取得できます。

`PLAN REPLAYER CAPTURE`は主に次の機能があります。

-   対象SQL文と対象実行プランのダイジェストを事前にTiDBクラスタに登録し、対象クエリとのマッチングを開始します。
-   ターゲット クエリが正常に一致すると、そのオプティマイザー関連情報を直接キャプチャし、ZIP ファイルとしてエクスポートします。
-   一致した SQL と実行プランごとに、情報は 1 回だけキャプチャされます。
-   システム テーブルを通じて、進行中の一致するタスクと生成されたファイルを表示します。
-   履歴ファイルを定期的にクリーンアップします。

### <code>PLAN REPLAYER CAPTURE</code>を有効にする {#enable-code-plan-replayer-capture-code}

`PLAN REPLAYER CAPTURE`システム変数[`tidb_enable_plan_replayer_capture`](/system-variables.md#tidb_enable_plan_replayer_capture)によって制御されます。4 `PLAN REPLAYER CAPTURE`有効にするには、システム変数の値を`ON`に設定します。

### <code>PLAN REPLAYER CAPTURE</code>使用する {#use-code-plan-replayer-capture-code}

次のステートメントを使用して、ターゲット SQL ステートメントと実行プランのダイジェストを TiDB クラスターに登録できます。

```sql
PLAN REPLAYER CAPTURE 'sql_digest' 'plan_digest';
```

対象の SQL ステートメントに複数の実行プランがあり、すべての実行プランを取得する場合は、次のステートメントを使用してすべての実行プランを一度に登録できます。

```sql
PLAN REPLAYER CAPTURE 'sql_digest' '*';
```

### キャプチャタスクをビュー {#view-the-capture-tasks}

次のステートメントを使用して、TiDB クラスター内の`PLAN REPLAYER CAPTURE`の進行中のキャプチャ タスクを表示できます。

```sql
mysql> PLAN REPLAYER CAPTURE 'example_sql' 'example_plan';
Query OK, 1 row affected (0.01 sec)

mysql> SELECT * FROM mysql.plan_replayer_task;
+-------------+--------------+---------------------+
| sql_digest  | plan_digest  | update_time         |
+-------------+--------------+---------------------+
| example_sql | example_plan | 2023-01-28 11:58:22 |
+-------------+--------------+---------------------+
1 row in set (0.01 sec)
```

### キャプチャ結果をビュー {#view-the-capture-results}

`PLAN REPLAYER CAPTURE`正常に結果を取得したら、次の SQL ステートメントを使用して、ファイルのダウンロードに使用されたトークンを表示できます。

```sql
mysql> SELECT * FROM mysql.plan_replayer_status;
+------------------------------------------------------------------+------------------------------------------------------------------+------------+-----------------------------------------------------------+---------------------+-------------+-----------------+
| sql_digest                                                       | plan_digest                                                      | origin_sql | token                                                     | update_time         | fail_reason | instance        |
+------------------------------------------------------------------+------------------------------------------------------------------+------------+-----------------------------------------------------------+---------------------+-------------+-----------------+
| 086e3fbd2732f7671c17f299d4320689deeeb87ba031240e1e598a0ca14f808c | 042de2a6652a6d20afc629ff90b8507b7587a1c7e1eb122c3e0b808b1d80cc02 |            | replayer_Utah4nkz2sIEzkks7tIRog==_1668746293523179156.zip | 2022-11-18 12:38:13 | NULL        | 172.16.4.4:4022 |
| b5b38322b7be560edb04f33f15b15a885e7c6209a22b56b0804622e397199b54 | 1770efeb3f91936e095f0344b629562bf1b204f6e46439b7d8f842319297c3b5 |            | replayer_Z2mUXNHDjU_WBmGdWQqifw==_1668746293560115314.zip | 2022-11-18 12:38:13 | NULL        | 172.16.4.4:4022 |
| 96d00c0b3f08795fe94e2d712fa1078ab7809faf4e81d198f276c0dede818cf9 | 8892f74ac2a42c2c6b6152352bc491b5c07c73ac3ed66487b2c990909bae83e8 |            | replayer_RZcRHJB7BaCccxFfOIAhWg==_1668746293578282450.zip | 2022-11-18 12:38:13 | NULL        | 172.16.4.4:4022 |
+------------------------------------------------------------------+------------------------------------------------------------------+------------+-----------------------------------------------------------+---------------------+-------------+-----------------+
3 rows in set (0.00 sec)
```

`PLAN REPLAYER CAPTURE`のファイルのダウンロード方法は`PLAN REPLAYER`と同様です。詳細は[クラスター情報のエクスポートの例](#examples-of-exporting-cluster-information)参照してください。

> **注記：**
>
> `PLAN REPLAYER CAPTURE`の結果ファイルは、TiDB クラスターに最大 1 週間保存されます。1 週間後、TiDB はファイルを削除します。

### キャプチャタスクを削除する {#remove-the-capture-tasks}

キャプチャ タスクが不要になった場合は、 `PLAN REPLAYER CAPTURE REMOVE`ステートメントを使用して削除できます。例:

```sql
mysql> PLAN REPLAYER CAPTURE '077a87a576e42360c95530ccdac7a1771c4efba17619e26be50a4cfd967204a0' '4838af52c1e07fc8694761ad193d16a689b2128bc5ced9d13beb31ae27b370ce';
Query OK, 0 rows affected (0.01 sec)

mysql> SELECT * FROM mysql.plan_replayer_task;
+------------------------------------------------------------------+------------------------------------------------------------------+---------------------+
| sql_digest                                                       | plan_digest                                                      | update_time         |
+------------------------------------------------------------------+------------------------------------------------------------------+---------------------+
| 077a87a576e42360c95530ccdac7a1771c4efba17619e26be50a4cfd967204a0 | 4838af52c1e07fc8694761ad193d16a689b2128bc5ced9d13beb31ae27b370ce | 2024-05-21 11:26:10 |
+------------------------------------------------------------------+------------------------------------------------------------------+---------------------+
1 row in set (0.01 sec)

mysql> PLAN REPLAYER CAPTURE REMOVE '077a87a576e42360c95530ccdac7a1771c4efba17619e26be50a4cfd967204a0' '4838af52c1e07fc8694761ad193d16a689b2128bc5ced9d13beb31ae27b370ce';
Query OK, 0 rows affected (0.01 sec)

mysql> SELECT * FROM mysql.plan_replayer_task;
Empty set (0.01 sec)
```

## <code>PLAN REPLAYER CONTINUOUS CAPTURE</code>を使用する {#use-code-plan-replayer-continuous-capture-code}

`PLAN REPLAYER CONTINUOUS CAPTURE`有効にすると、TiDB は`SQL DIGEST`と`PLAN DIGEST`に従って`PLAN REPLAYER`方法でアプリケーションの SQL 文を非同期的に記録します。同じ DIGEST を共有する SQL 文と実行プランについては、 `PLAN REPLAYER CONTINUOUS CAPTURE`それらを繰り返し記録しません。

### <code>PLAN REPLAYER CONTINUOUS CAPTURE</code>を有効にする {#enable-code-plan-replayer-continuous-capture-code}

`PLAN REPLAYER CONTINUOUS CAPTURE`システム変数[`tidb_enable_plan_replayer_continuous_capture`](/system-variables.md#tidb_enable_plan_replayer_continuous_capture-new-in-v700)によって制御されます。4 `PLAN REPLAYER CONTINUOUS CAPTURE`有効にするには、システム変数の値を`ON`に設定します。

### キャプチャ結果をビュー {#view-the-capture-results}

`PLAN REPLAYER CONTINUOUS CAPTURE`のキャプチャ結果の閲覧方法は[`PLAN REPLAYER CAPTURE`のキャプチャ結果の表示](#view-the-capture-results)と同様です。
