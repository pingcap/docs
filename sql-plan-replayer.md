---
title: Use PLAN REPLAYER to Save and Restore the On-Site Information of a Cluster
summary: Learn how to use PLAN REPLAYER to save and restore the on-site information of a cluster.
---

# PLAN REPLAYER を使用してクラスタのオンサイト情報を保存および復元する {#use-plan-replayer-to-save-and-restore-the-on-site-information-of-a-cluster}

TiDB クラスターの問題を特定してトラブルシューティングする場合、多くの場合、システムと実行計画に関する情報を提供する必要があります。より便利かつ効率的な方法で情報を取得し、クラスターの問題をトラブルシューティングできるように、TiDB v5.3.0 では`PLAN REPLAYER`コマンドが導入されました。このコマンドを使用すると、クラスターのオンサイト情報を簡単に保存および復元できるようになり、トラブルシューティングの効率が向上し、管理のために問題をより簡単にアーカイブできるようになります。

`PLAN REPLAYER`の特徴は以下の通りです。

-   オンサイトのトラブルシューティングで TiDB クラスターの情報を ZIP 形式のファイルにエクスポートしてstorage。
-   別の TiDB クラスターからエクスポートされた ZIP 形式のファイルをクラスターにインポートします。このファイルには、オンサイトのトラブルシューティングにおける後者の TiDB クラスターの情報が含まれています。

## <code>PLAN REPLAYER</code>使用してクラスター情報をエクスポートする {#use-code-plan-replayer-code-to-export-cluster-information}

`PLAN REPLAYER`を使用すると、TiDB クラスターのオンサイト情報を保存できます。エクスポートインターフェイスは次のとおりです。

```sql
PLAN REPLAYER DUMP EXPLAIN [ANALYZE] [WITH STATS AS OF TIMESTAMP expression] sql-statement;
```

TiDB は`sql-statement`に基づいて、次のオンサイト情報を整理してエクスポートします。

-   TiDBのバージョン
-   TiDB 構成
-   TiDB セッション変数
-   TiDB SQLバインディング
-   `sql-statement`のテーブル スキーマ
-   `sql-statement`のテーブルの統計
-   `EXPLAIN [ANALYZE] sql-statement`の結果
-   クエリ最適化のいくつかの内部手順

履歴統計が[有効化](/system-variables.md#tidb_enable_historical_stats)の場合、 `PLAN REPLAYER`ステートメントで時間を指定して、対応する時間の履歴統計を取得できます。日時を直接指定することも、タイムスタンプを指定することもできます。 TiDB は、指定された時刻より前の履歴統計を検索し、その中の最新の統計をエクスポートします。

指定された時刻より前の履歴統計がない場合、TiDB は最新の統計をエクスポートします。これは、時刻が指定されていない場合の動作と一致します。さらに、TiDB は、エクスポートされた`ZIP`ファイル内の`errors.txt`ファイルにエラー メッセージを出力。

> **注記：**
>
> `PLAN REPLAYER`はテーブルデータをエクスポート**しません**。

### クラスタ情報のエクスポート例 {#examples-of-exporting-cluster-information}

```sql
use test;
create table t(a int, b int);
insert into t values(1,1), (2, 2), (3, 3);
analyze table t;

plan replayer dump explain select * from t;
plan replayer dump with stats as of timestamp '2023-07-17 12:00:00' explain select * from t;
plan replayer dump with stats as of timestamp '442012134592479233' explain select * from t;
```

`PLAN REPLAYER DUMP` 、上記のテーブル情報を`ZIP`ファイルにパッケージ化し、実行結果としてファイル識別子を返します。

> **注記：**
>
> `ZIP`ファイルは TiDB クラスターに最大 1 時間保存されます。 1 時間後、TiDB はそれを削除します。

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

あるいは、セッション変数[`tidb_last_plan_replayer_token`](/system-variables.md#tidb_last_plan_replayer_token-new-in-v630)を使用して、最後の`PLAN REPLAYER DUMP`回の実行結果を取得することもできます。

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

SQL文が複数ある場合、 `PLAN REPLAYER DUMP`の実行結果をファイルで取得できます。このファイルでは、複数の SQL ステートメントの結果が`;`で区切られています。

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

ファイルは MySQL クライアントではダウンロードできないため、ファイルをダウンロードするには TiDB HTTP インターフェイスとファイル識別子を使用する必要があります。

```shell
http://${tidb-server-ip}:${tidb-server-status-port}/plan_replayer/dump/${file_token}
```

`${tidb-server-ip}:${tidb-server-status-port}`は、クラスター内の任意の TiDBサーバーのアドレスです。例えば：

```shell
curl http://127.0.0.1:10080/plan_replayer/dump/replayer_JOGvpu4t7dssySqJfTtS4A==_1635750890568691080.zip > plan_replayer.zip
```

## <code>PLAN REPLAYER</code>使用してクラスター情報をインポートする {#use-code-plan-replayer-code-to-import-cluster-information}

> **警告：**
>
> TiDB クラスターのオンサイト情報を別のクラスターにインポートすると、後者のクラスターの TiDB セッション変数、SQL バインディング、テーブル スキーマ、および統計が変更されます。

`PLAN REPLAYER`を使用してエクスポートされた既存の`ZIP`ファイルでは、 `PLAN REPLAYER`インポート インターフェイスを使用して、クラスターのオンサイト情報を他の TiDB クラスターに復元できます。構文は次のとおりです。

```sql
PLAN REPLAYER LOAD 'file_name';
```

上記のステートメントでは、 `file_name`はエクスポートされる`ZIP`ファイルの名前です。

例えば：

```sql
PLAN REPLAYER LOAD 'plan_replayer.zip';
```

クラスター情報がインポートされると、必要なテーブル スキーマ、統計、および実行計画の構築に影響を与えるその他の情報が TiDB クラスターにロードされます。次の方法で実行計画を表示し、統計を確認できます。

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

シーンがロードされて復元された後、クラスターの実行計画を診断して改善できます。

## <code>PLAN REPLAYER CAPTURE</code>使用してターゲット プランをキャプチャする {#use-code-plan-replayer-capture-code-to-capture-target-plans}

一部のシナリオで TiDB の実行プランを見つける場合、ターゲット SQL ステートメントとターゲット実行プランはクエリにたまにしか表示されないため、 `PLAN REPLAYER`使用してステートメントとプランを直接キャプチャすることはできません。このような場合、 `PLAN REPLAYER CAPTURE`を使用すると、ターゲット SQL ステートメントとターゲット プランのオプティマイザー情報を取得しやすくなります。

`PLAN REPLAYER CAPTURE`には次の主な機能があります。

-   対象のSQL文と対象の実行プランのダイジェストを事前にTiDBクラスターに登録し、対象のクエリとのマッチングを開始します。
-   ターゲット クエリが正常に一致すると、オプティマイザ関連の情報を直接取得し、ZIP ファイルとしてエクスポートします。
-   一致した SQL および実行プランごとに、情報は 1 回だけ取得されます。
-   システム テーブルを通じて、進行中の一致タスクと生成されたファイルを表示します。
-   履歴ファイルを定期的にクリーンアップします。

### <code>PLAN REPLAYER CAPTURE</code>を有効にする {#enable-code-plan-replayer-capture-code}

`PLAN REPLAYER CAPTURE`はシステム変数[`tidb_enable_plan_replayer_capture`](/system-variables.md#tidb_enable_plan_replayer_capture)によって制御されます。 `PLAN REPLAYER CAPTURE`を有効にするには、システム変数の値を`ON`に設定します。

### <code>PLAN REPLAYER CAPTURE</code>を使用する {#use-code-plan-replayer-capture-code}

次のステートメントを使用して、ターゲット SQL ステートメントのダイジェストと実行プランを TiDB クラスターに登録できます。

```sql
PLAN REPLAYER CAPTURE 'sql_digest' 'plan_digest';
```

ターゲット SQL ステートメントに複数の実行プランがあり、すべての実行プランをキャプチャしたい場合は、次のステートメントを使用してすべての実行プランを一度に登録できます。

```sql
PLAN REPLAYER CAPTURE 'sql_digest' '*';
```

### キャプチャタスクをビュー {#view-the-capture-tasks}

次のステートメントを使用して、TiDB クラスター内の`PLAN REPLAYER CAPTURE`進行中のキャプチャ タスクを表示できます。

```sql
mysql> PLAN PLAYER CAPTURE 'example_sql' 'example_plan';
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

`PLAN REPLAYER CAPTURE`が結果を正常に取得したら、次の SQL ステートメントを使用して、ファイルのダウンロードに使用されたトークンを表示できます。

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

`PLAN REPLAYER CAPTURE`のファイルのダウンロード方法は`PLAN REPLAYER`と同様です。詳細は[クラスタ情報のエクスポート例](#examples-of-exporting-cluster-information)を参照してください。

> **注記：**
>
> `PLAN REPLAYER CAPTURE`の結果ファイルは、TiDB クラスターに最大 1 週間保持されます。 1 週間後、TiDB はファイルを削除します。

## <code>PLAN REPLAYER CONTINUOUS CAPTURE</code>を使用する {#use-code-plan-replayer-continuous-capture-code}

`PLAN REPLAYER CONTINUOUS CAPTURE`を有効にすると、TiDB は`SQL DIGEST`と`PLAN DIGEST`に従って`PLAN REPLAYER`メソッドを使用してアプリケーションの SQL ステートメントを非同期的に記録します。同じ DIGEST を共有する SQL ステートメントと実行プランの場合、 `PLAN REPLAYER CONTINUOUS CAPTURE`それらを繰り返し記録しません。

### <code>PLAN REPLAYER CONTINUOUS CAPTURE</code>を有効にする {#enable-code-plan-replayer-continuous-capture-code}

`PLAN REPLAYER CONTINUOUS CAPTURE`はシステム変数[`tidb_enable_plan_replayer_continuous_capture`](/system-variables.md#tidb_enable_plan_replayer_continuous_capture-new-in-v700)によって制御されます。 `PLAN REPLAYER CONTINUOUS CAPTURE`を有効にするには、システム変数の値を`ON`に設定します。

### キャプチャ結果をビュー {#view-the-capture-results}

`PLAN REPLAYER CONTINUOUS CAPTURE`の攻略結果の見方は[`PLAN REPLAYER CAPTURE`のキャプチャ結果の確認](#view-the-capture-results)と同様です。
