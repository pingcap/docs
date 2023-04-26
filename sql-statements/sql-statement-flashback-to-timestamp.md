---
title: FLASHBACK CLUSTER TO TIMESTAMP
summary: Learn the usage of FLASHBACK CLUSTER TO TIMESTAMP in TiDB databases.
---

# タイムスタンプへのフラッシュバック クラスタ {#flashback-cluster-to-timestamp}

TiDB v6.4.0 では`FLASHBACK CLUSTER TO TIMESTAMP`構文が導入されています。これを使用して、クラスターを特定の時点に復元できます。

<CustomContent platform="tidb-cloud">

> **警告：**
>
> `FLASHBACK CLUSTER TO TIMESTAMP`構文は、 TiDB Cloud [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターには適用されません。予期しない結果を避けるため、Serverless Tierクラスターではこのステートメントを実行しないでください。

</CustomContent>

> **ノート：**
>
> `FLASHBACK CLUSTER TO TIMESTAMP`の動作原理は、特定の時点の古いデータを最新のタイムスタンプで書き込むことであり、現在のデータは削除しません。したがって、この機能を使用する前に、古いデータと現在のデータ用の十分なstorage容量があることを確認する必要があります.

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

-   `FLASHBACK`ステートメントで指定された時間は、ガベージ コレクション (GC) の有効期間内である必要があります。システム変数[`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) (デフォルト: `10m0s` ) は、以前のバージョンの行の保持時間を定義します。ガベージコレクションが実行された場所の現在の`safePoint`は、次のクエリで取得できます。

    ```sql
    SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
    ```

-   `FLASHBACK CLUSTER` SQL ステートメントを実行できるのは、 `SUPER`権限を持つユーザーだけです。

-   `FLASHBACK`文で指定した時刻から`FLASHBACK`文を実行する時刻までの間に、関連するテーブル構造を変更するDDL文があってはなりません。そのような DDL が存在する場合、TiDB はそれを拒否します。

-   `FLASHBACK CLUSTER TO TIMESTAMP`を実行する前に、TiDB は関連するすべての接続を切断し、 `FLASHBACK`ステートメントが完了するまでこれらのテーブルに対する読み取りおよび書き込み操作を禁止します。

-   `FLASHBACK CLUSTER TO TIMESTAMP`ステートメントは、実行後にキャンセルできません。 TiDB は成功するまで再試行を続けます。

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

`FLASHBACK`ステートメントで指定された時刻から`FLASHBACK`ステートメントが実行される時刻までにテーブル構造を変更する DDL ステートメントがある場合、 `FLASHBACK`ステートメントは失敗します。

```sql
mysql> SELECT now();
+---------------------+
| now()               |
+---------------------+
| 2022-10-09 16:40:51 |
+---------------------+
1 row in set (0.01 sec)

mysql> CREATE TABLE t(a int);
Query OK, 0 rows affected (0.12 sec)

mysql> FLASHBACK CLUSTER TO TIMESTAMP '2022-10-09 16:40:51';
ERROR 1105 (HY000): Detected schema change due to another DDL job during [2022-10-09 16:40:51 +0800 CST, now), can't do flashback
```

ログから、 `FLASHBACK`の実行進行状況を取得できます。次に例を示します。

```
[2022/10/09 17:25:59.316 +08:00] [INFO] [cluster.go:463] ["flashback cluster stats"] ["complete regions"=9] ["total regions"=10] []
```

## MySQL の互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。
