---
title: FLASHBACK CLUSTER
summary: TiDBデータベースにおけるFLASHBACK CLUSTERの使い方を学びましょう。
---

# フラッシュバック・クラスター {#flashback-cluster}

TiDB v6.4.0 では`FLASHBACK CLUSTER TO TIMESTAMP`構文が導入されました。これを使用すると、クラスタを特定の時点に復元できます。タイムスタンプを指定する際には、datetime 値を設定するか、time 関数を使用できます。datetime の形式は「2016-10-08 16:45:26.999」のようで、最小時間単位はミリ秒です。ただし、ほとんどの場合、時間単位を秒としてタイムスタンプを指定するだけで十分です。たとえば、「2016-10-08 16:45:26」のように指定します。

TiDBは、v6.5.6、v7.1.3、v7.5.1、v7.6.0以降で`FLASHBACK CLUSTER TO TSO`構文を導入しました。この構文を使用すると、 [TSO](/tso.md)使用してより正確なリカバリ時点を指定できるため、データリカバリの柔軟性が向上します。

> **警告：**
>
> `FLASHBACK CLUSTER TO [TIMESTAMP|TSO]`構文は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスには適用できません。予期しない結果を避けるため、 TiDB Cloud StarterおよびTiDB Cloud Essentialインスタンスではこのステートメントを実行しないでください。

> **警告：**
>
> -   リカバリ時点を指定する際は、ターゲットタイムスタンプまたはTSOの有効性を確認し、PDによって現在割り当てられている最大TSOを超える将来の時刻を指定しないようにしてください（Grafana PDパネルの`Current TSO`を参照）。そうしないと、同時処理の線形一貫性とトランザクション分離レベルが侵害され、深刻なデータ正当性の問題が発生する可能性があります。
> -   `FLASHBACK CLUSTER`の実行中、データクリーンアップ処理はトランザクションの一貫性を保証しません。 `FLASHBACK CLUSTER`が完了した後、TiDB の履歴バージョン読み取り機能 ([ステイル読み取り](/stale-read.md)または[`tidb_snapshot`](/read-historical-data.md)など) を使用する場合は、指定された履歴タイムスタンプ`FLASHBACK CLUSTER`の実行期間外であることを確認してください。FLASHBACK によって完全に復元されていないデータを含む履歴バージョンを読み取ると、同時処理の線形一貫性とトランザクション分離レベルが侵害され、深刻なデータ正当性の問題が発生する可能性があります。

<CustomContent platform="tidb">

> **警告：**
>
> TiDB v7.1.0 でこの機能を使用すると、FLASHBACK 操作の完了後も一部のリージョンが FLASHBACK プロセスに残る場合があります。v7.1.0 ではこの機能の使用を避けることをお勧めします。詳細については、問題[#44292](https://github.com/pingcap/tidb/issues/44292)を参照してください。
>
> この問題が発生した場合は、 [TiDBスナップショットのバックアップと復元](/br/br-snapshot-guide.md)機能を使用してデータを復元できます。

</CustomContent>

> **注記：**
>
> `FLASHBACK CLUSTER TO [TIMESTAMP|TSO]`の動作原理は、特定の時点の古いデータを最新のタイムスタンプで書き込むことであり、現在のデータは削除しません。そのため、この機能を使用する前に、古いデータと現在のデータのための十分なstorage容量があることを確認する必要があります。

## 構文 {#syntax}

```sql
FLASHBACK CLUSTER TO TIMESTAMP '2022-09-21 16:02:50';
FLASHBACK CLUSTER TO TSO 445494839813079041;
```

### あらすじ {#synopsis}

```ebnf+diagram
FlashbackToTimestampStmt
         ::= 'FLASHBACK' 'CLUSTER' 'TO' ('TIMESTAMP' stringLit | 'TSO' LengthNum)
```

## 注記 {#notes}

-   `FLASHBACK`ステートメントで指定する時間は、ガベージ コレクション (GC) の有効期間内である必要があります。システム変数[`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) (デフォルト: `10m0s` ) は、行の以前のバージョンの保持時間を定義します。ガベージコレクションが実行された現在の`safePoint`は、次のクエリで取得できます。

    ```sql
    SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
    ```

<CustomContent platform='tidb'>

-   `SUPER`権限を持つユーザーのみが`FLASHBACK CLUSTER` SQL ステートメントを実行できます。
-   `FLASHBACK CLUSTER`は、 `ALTER TABLE ATTRIBUTE` 、 `ALTER TABLE REPLICA` `CREATE PLACEMENT POLICY` 。
-   `FLASHBACK`ステートメントで指定された時点では、完全に実行されていない DDL ステートメントは存在してはなりません。そのような DDL が存在する場合、TiDB はそれを拒否します。
-   `FLASHBACK CLUSTER`を実行する前に、TiDB は関連するすべての接続を切断し、 `FLASHBACK CLUSTER`ステートメントが完了するまで、これらのテーブルに対する読み取りおよび書き込み操作を禁止します。
-   `FLASHBACK CLUSTER`ステートメントは、実行後にキャンセルすることはできません。TiDB は成功するまで再試行を続けます。
-   `FLASHBACK CLUSTER`の実行中にデータをバックアップする必要がある場合は、[バックアップと復元](/br/br-snapshot-guide.md)を使用し、 `BackupTS`の開始時刻より前の`FLASHBACK CLUSTER`を指定することのみが可能です。さらに、 `FLASHBACK CLUSTER`の実行中、[ログバックアップ](/br/br-pitr-guide.md)有効化は失敗します。したがって、 `FLASHBACK CLUSTER`が完了した後でログ バックアップを有効にしてみてください。
-   `FLASHBACK CLUSTER`ステートメントによってメタデータ (テーブル構造、データベース構造) のロールバックが発生した場合、関連する変更は TiCDC によって複製され**ません**。そのため、タスクを手動で一時停止し、 `FLASHBACK CLUSTER`の完了を待ってから、上流と下流のスキーマ定義を手動で複製して、それらが整合していることを確認する必要があります。その後、TiCDC 変更フィードを再作成する必要があります。

</CustomContent>

<CustomContent platform='tidb-cloud'>

-   `SUPER`権限を持つユーザーのみが`FLASHBACK CLUSTER` SQL ステートメントを実行できます。
-   `FLASHBACK CLUSTER`は、 `ALTER TABLE ATTRIBUTE` 、 `ALTER TABLE REPLICA` `CREATE PLACEMENT POLICY` 。
-   `FLASHBACK`ステートメントで指定された時点では、完全に実行されていない DDL ステートメントは存在してはなりません。そのような DDL が存在する場合、TiDB はそれを拒否します。
-   `FLASHBACK CLUSTER`を実行する前に、TiDB は関連するすべての接続を切断し、 `FLASHBACK CLUSTER`ステートメントが完了するまで、これらのテーブルに対する読み取りおよび書き込み操作を禁止します。
-   `FLASHBACK CLUSTER`ステートメントは、実行後にキャンセルすることはできません。TiDB は成功するまで再試行を続けます。
-   `FLASHBACK CLUSTER`ステートメントによってメタデータ (テーブル構造、データベース構造) のロールバックが発生した場合、関連する変更は TiCDC によって複製され**ません**。そのため、タスクを手動で一時停止し、 `FLASHBACK CLUSTER`の完了を待ってから、上流と下流のスキーマ定義を手動で複製して、それらが整合していることを確認する必要があります。その後、TiCDC 変更フィードを再作成する必要があります。

</CustomContent>

## 例 {#example}

次の例は、クラスターを特定のタイムスタンプにフラッシュバックして、新しく挿入されたデータを復元する方法を示しています。

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

次の例は、誤って削除されたデータを正確に復元するために、クラスタを特定のTSOにフラッシュバックする方法を示しています。

```sql
mysql> INSERT INTO t VALUES (1);
Query OK, 1 row affected (0.02 sec)

mysql> SELECT * FROM t;
+------+
| a    |
+------+
|    1 |
+------+
1 row in set (0.01 sec)


mysql> BEGIN;
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT @@tidb_current_ts;  -- Get the current TSO
+--------------------+
| @@tidb_current_ts  |
+--------------------+
| 446113975683252225 |
+--------------------+
1 row in set (0.00 sec)

mysql> ROLLBACK;
Query OK, 0 rows affected (0.00 sec)


mysql> DELETE FROM t;
Query OK, 1 rows affected (0.00 sec)


mysql> FLASHBACK CLUSTER TO TSO 446113975683252225;
Query OK, 0 rows affected (0.20 sec)

mysql> SELECT * FROM t;
+------+
| a    |
+------+
|    1 |
+------+
1 row in set (0.01 sec)
```

`FLASHBACK`ステートメントで指定された時点で DDL ステートメントが完全に実行されていない場合、 `FLASHBACK`ステートメントは失敗します。

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

ログを通して、 `FLASHBACK`の実行状況を取得できます。以下に例を示します。

    [2022/10/09 17:25:59.316 +08:00] [INFO] [cluster.go:463] ["flashback cluster stats"] ["complete regions"=9] ["total regions"=10] []

## MySQLとの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文に対するTiDBの拡張機能です。
