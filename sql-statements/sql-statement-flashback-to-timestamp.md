---
title: FLASHBACK CLUSTER TO TIMESTAMP
summary: Learn the usage of FLASHBACK CLUSTER TO TIMESTAMP in TiDB databases.
---

# フラッシュバッククラスターからタイムスタンプへ {#flashback-cluster-to-timestamp}

TiDB v6.4.0 では`FLASHBACK CLUSTER TO TIMESTAMP`構文が導入されています。これを使用して、クラスターを特定の時点に復元できます。

> **警告：**
>
> `FLASHBACK CLUSTER TO TIMESTAMP`構文は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターには適用されません。予期しない結果を避けるため、TiDB サーバーレス クラスターではこのステートメントを実行しないでください。

<CustomContent platform="tidb">

> **警告：**
>
> TiDB v7.1.0 でこの機能を使用すると、FLASHBACK 操作の完了後でも、一部のリージョンが FLASHBACK プロセスに残る場合があります。 v7.1.0 ではこの機能を使用しないことをお勧めします。詳細については、問題[#44292](https://github.com/pingcap/tidb/issues/44292)を参照してください。
>
> この問題が発生した場合は、 [TiDB スナップショットのバックアップと復元](/br/br-snapshot-guide.md)機能を使用してデータを復元できます。

</CustomContent>

> **注記：**
>
> `FLASHBACK CLUSTER TO TIMESTAMP`の動作原理は、特定の時点の古いデータを最新のタイムスタンプで書き込み、現在のデータは削除しません。したがって、この機能を使用する前に、古いデータと現在のデータを保存するのに十分なstorage領域があることを確認する必要があります。

## 構文 {#syntax}

```sql
FLASHBACK CLUSTER TO TIMESTAMP '2022-09-21 16:02:50';
```

### あらすじ {#synopsis}

```ebnf+diagram
FlashbackToTimestampStmt ::=
    "FLASHBACK" "CLUSTER" "TO" "TIMESTAMP" stringLit
```

## ノート {#notes}

-   `FLASHBACK`ステートメントで指定する時間は、ガベージ コレクション (GC) の有効期間内である必要があります。システム変数[`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) (デフォルト: `10m0s` ) は、以前のバージョンの行の保持時間を定義します。ガベージコレクションが実行された現在の`safePoint`の場所は、次のクエリで取得できます。

    ```sql
    SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
    ```

<CustomContent platform='tidb'>

-   `SUPER`権限を持つユーザーのみが`FLASHBACK CLUSTER` SQL ステートメントを実行できます。
-   `FLASHBACK CLUSTER` `ALTER TABLE ATTRIBUTE` 、 `ALTER TABLE REPLICA` 、 `CREATE PLACEMENT POLICY`などの PD 関連情報を変更する DDL ステートメントのロールバックをサポートしません。
-   `FLASHBACK`ステートメントで指定された時点で、完全に実行されていない DDL ステートメントがあってはなりません。そのような DDL が存在する場合、TiDB はそれを拒否します。
-   `FLASHBACK CLUSTER TO TIMESTAMP`を実行する前に、TiDB は関連するすべての接続を切断し、ステートメント`FLASHBACK CLUSTER`完了するまでこれらのテーブルに対する読み取りおよび書き込み操作を禁止します。
-   `FLASHBACK CLUSTER TO TIMESTAMP`ステートメントは実行後にキャンセルできません。 TiDB は成功するまで再試行を続けます。
-   `FLASHBACK CLUSTER`の実行中にデータをバックアップする必要がある場合は、 [復元する](/br/br-snapshot-guide.md)のみを使用し、 `FLASHBACK CLUSTER`の開始時刻よりも前の`BackupTS`を指定できます。さらに、 `FLASHBACK CLUSTER`の実行中に[ログのバックアップ](/br/br-pitr-guide.md)を有効にすると失敗します。したがって、 `FLASHBACK CLUSTER`が完了した後でログのバックアップを有効にするようにしてください。
-   `FLASHBACK CLUSTER`ステートメントによってメタデータ (テーブル構造、データベース構造) のロールバックが発生した場合、関連する変更は TiCDC によってレプリケートされませ**ん**。したがって、タスクを手動で一時停止し、 `FLASHBACK CLUSTER`の完了を待ち、アップストリームとダウンストリームのスキーマ定義を手動でレプリケートして、一貫性があることを確認する必要があります。その後、TiCDC 変更フィードを再作成する必要があります。

</CustomContent>

<CustomContent platform='tidb-cloud'>

-   `SUPER`権限を持つユーザーのみが`FLASHBACK CLUSTER` SQL ステートメントを実行できます。
-   `FLASHBACK CLUSTER` `ALTER TABLE ATTRIBUTE` 、 `ALTER TABLE REPLICA` 、 `CREATE PLACEMENT POLICY`などの PD 関連情報を変更する DDL ステートメントのロールバックをサポートしません。
-   `FLASHBACK`ステートメントで指定された時点で、完全に実行されていない DDL ステートメントがあってはなりません。そのような DDL が存在する場合、TiDB はそれを拒否します。
-   `FLASHBACK CLUSTER TO TIMESTAMP`を実行する前に、TiDB は関連するすべての接続を切断し、ステートメント`FLASHBACK CLUSTER`完了するまでこれらのテーブルに対する読み取りおよび書き込み操作を禁止します。
-   `FLASHBACK CLUSTER TO TIMESTAMP`ステートメントは実行後にキャンセルできません。 TiDB は成功するまで再試行を続けます。
-   `FLASHBACK CLUSTER`ステートメントによってメタデータ (テーブル構造、データベース構造) のロールバックが発生した場合、関連する変更は TiCDC によってレプリケートされませ**ん**。したがって、タスクを手動で一時停止し、 `FLASHBACK CLUSTER`の完了を待ち、アップストリームとダウンストリームのスキーマ定義を手動でレプリケートして、一貫性があることを確認する必要があります。その後、TiCDC 変更フィードを再作成する必要があります。

</CustomContent>

## 例 {#example}

次の例は、新しく挿入されたデータを復元する方法を示しています。

```sql
mysql> CREATE TABLE t(a INT);
Query OK, 0 rows affected (0.09 sec)

mysql> SELECT * FROM t;
Empty set (0.01 sec)

mysql> SELECT now();
+---------------------+
| now()               |
+---------------------+
| 2022-09-28 17:24:16 |
+---------------------+
1 row in set (0.02 sec)

mysql> INSERT INTO t VALUES (1);
Query OK, 1 row affected (0.02 sec)

mysql> SELECT * FROM t;
+------+
| a    |
+------+
|    1 |
+------+
1 row in set (0.01 sec)

mysql> FLASHBACK CLUSTER TO TIMESTAMP '2022-09-28 17:24:16';
Query OK, 0 rows affected (0.20 sec)

mysql> SELECT * FROM t;
Empty set (0.00 sec)
```

`FLASHBACK`ステートメントで指定された時間に完全に実行されていない DDL ステートメントがある場合、 `FLASHBACK`ステートメントは失敗します。

```sql
mysql> ALTER TABLE t ADD INDEX k(a);
Query OK, 0 rows affected (0.56 sec)

mysql> ADMIN SHOW DDL JOBS 1;
+--------+---------+-----------------------+------------------------+--------------+-----------+----------+-----------+---------------------+---------------------+---------------------+--------+
| JOB_ID | DB_NAME | TABLE_NAME            | JOB_TYPE               | SCHEMA_STATE | SCHEMA_ID | TABLE_ID | ROW_COUNT | CREATE_TIME         | START_TIME          | END_TIME            | STATE  |
+--------+---------+-----------------------+------------------------+--------------+-----------+----------+-----------+---------------------+---------------------+---------------------+--------+
|     84 | test    | t                     | add index /* ingest */ | public       |         2 |       82 |         0 | 2023-01-29 14:33:11 | 2023-01-29 14:33:11 | 2023-01-29 14:33:12 | synced |
+--------+---------+-----------------------+------------------------+--------------+-----------+----------+-----------+---------------------+---------------------+---------------------+--------+
1 rows in set (0.01 sec)

mysql> FLASHBACK CLUSTER TO TIMESTAMP '2023-01-29 14:33:12';
ERROR 1105 (HY000): Detected another DDL job at 2023-01-29 14:33:12 +0800 CST, can't do flashback
```

ログを通じて、 `FLASHBACK`の実行の進行状況を取得できます。以下は例です。

    [2022/10/09 17:25:59.316 +08:00] [INFO] [cluster.go:463] ["flashback cluster stats"] ["complete regions"=9] ["total regions"=10] []

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。
