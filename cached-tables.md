---
title: Cached Tables
summary: Learn the cached table feature in TiDB, which is used for rarely-updated small hotspot tables to improve read performance.
---

# キャッシュされたテーブル {#cached-tables}

v6.0.0 では、TiDB は頻繁にアクセスされるがめったに更新されない小さなホットスポット テーブル用のキャッシュ テーブル機能を導入しました。この機能を使用すると、テーブル全体のデータが TiDBサーバーのメモリにロードされ、TiDB は TiKV にアクセスせずにメモリからテーブル データを直接取得するため、読み取りパフォーマンスが向上します。

このドキュメントでは、キャッシュされたテーブルの使用シナリオ、例、および他の TiDB 機能との互換性制限について説明します。

## 利用シーン {#usage-scenarios}

キャッシュされたテーブル機能は、次の特性を持つテーブルに適しています。

-   テーブルのデータ量は少ないです。
-   テーブルは読み取り専用であるか、ほとんど更新されません。
-   テーブルは頻繁にアクセスされるため、読み取りパフォーマンスの向上が期待されます。

テーブルのデータ量が少ないにもかかわらず、データへのアクセスが頻繁に行われる場合、TiKV 内のリージョンにデータが集中し、ホットスポットリージョンとなり、パフォーマンスに影響を与えます。したがって、キャッシュされたテーブルの一般的な使用シナリオは次のとおりです。

-   アプリケーションが構成情報を読み取るコンフィグレーションテーブル。
-   金融セクターの為替レートの表。これらのテーブルは 1 日に 1 回だけ更新されますが、リアルタイムではありません。
-   銀行の支店またはネットワークの情報テーブル。めったに更新されません。

構成テーブルを例に挙げます。アプリケーションが再起動すると、構成情報がすべての接続にロードされるため、読み取りレイテンシーが長くなります。この場合、キャッシュされたテーブル機能を使用することでこの問題を解決できます。

## 例 {#examples}

このセクションでは、キャッシュされたテーブルの使用法を例を挙げて説明します。

### 通常のテーブルをキャッシュされたテーブルに設定する {#set-a-normal-table-to-a-cached-table}

テーブル`users`があるとします。

```sql
CREATE TABLE users (
    id BIGINT,
    name VARCHAR(100),
    PRIMARY KEY(id)
);
```

このテーブルをキャッシュされたテーブルに設定するには、 `ALTER TABLE`ステートメントを使用します。

```sql
ALTER TABLE users CACHE;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

### キャッシュされたテーブルを検証する {#verify-a-cached-table}

キャッシュされたテーブルを検証するには、 `SHOW CREATE TABLE`ステートメントを使用します。テーブルがキャッシュされている場合、返される結果には`CACHED ON`属性が含まれます。

```sql
SHOW CREATE TABLE users;
```

```sql
+-------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                                                                               |
+-------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| users | CREATE TABLE `users` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin /* CACHED ON */ |
+-------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

キャッシュされたテーブルからデータを読み取った後、TiDB はデータをメモリにロードします。 `trace`ステートメントを使用すると、データがメモリにロードされているかどうかを確認できます。キャッシュがロードされていない場合、返される結果には`regionRequest.SendReqCtx`属性が含まれます。これは、TiDB が TiKV からデータを読み取ることを示します。

```sql
TRACE SELECT * FROM users;
```

```sql
+------------------------------------------------+-----------------+------------+
| operation                                      | startTS         | duration   |
+------------------------------------------------+-----------------+------------+
| trace                                          | 17:47:39.969980 | 827.73µs   |
|   ├─session.ExecuteStmt                        | 17:47:39.969986 | 413.31µs   |
|   │ ├─executor.Compile                         | 17:47:39.969993 | 198.29µs   |
|   │ └─session.runStmt                          | 17:47:39.970221 | 157.252µs  |
|   │   └─TableReaderExecutor.Open               | 17:47:39.970294 | 47.068µs   |
|   │     └─distsql.Select                       | 17:47:39.970312 | 24.729µs   |
|   │       └─regionRequest.SendReqCtx           | 17:47:39.970454 | 189.601µs  |
|   ├─*executor.UnionScanExec.Next               | 17:47:39.970407 | 353.073µs  |
|   │ ├─*executor.TableReaderExecutor.Next       | 17:47:39.970411 | 301.106µs  |
|   │ └─*executor.TableReaderExecutor.Next       | 17:47:39.970746 | 6.57µs     |
|   └─*executor.UnionScanExec.Next               | 17:47:39.970772 | 17.589µs   |
|     └─*executor.TableReaderExecutor.Next       | 17:47:39.970776 | 6.59µs     |
+------------------------------------------------+-----------------+------------+
12 rows in set (0.01 sec)
```

`trace`を再度実行すると、返された結果には`regionRequest.SendReqCtx`属性が含まれなくなりました。これは、TiDB が TiKV からデータを読み取るのではなく、代わりにメモリからデータを読み取ることを示します。

```sql
+----------------------------------------+-----------------+------------+
| operation                              | startTS         | duration   |
+----------------------------------------+-----------------+------------+
| trace                                  | 17:47:40.533888 | 453.547µs  |
|   ├─session.ExecuteStmt                | 17:47:40.533894 | 402.341µs  |
|   │ ├─executor.Compile                 | 17:47:40.533903 | 205.54µs   |
|   │ └─session.runStmt                  | 17:47:40.534141 | 132.084µs  |
|   │   └─TableReaderExecutor.Open       | 17:47:40.534202 | 14.749µs   |
|   ├─*executor.UnionScanExec.Next       | 17:47:40.534306 | 3.21µs     |
|   └─*executor.UnionScanExec.Next       | 17:47:40.534316 | 1.219µs    |
+----------------------------------------+-----------------+------------+
7 rows in set (0.00 sec)
```

`UnionScan`演算子はキャッシュされたテーブルの読み取りに使用されるため、キャッシュされたテーブルの実行計画に`UnionScan`から`explain`が表示されることに注意してください。

```sql
+-------------------------+---------+-----------+---------------+--------------------------------+
| id                      | estRows | task      | access object | operator info                  |
+-------------------------+---------+-----------+---------------+--------------------------------+
| UnionScan_5             | 1.00    | root      |               |                                |
| └─TableReader_7         | 1.00    | root      |               | data:TableFullScan_6           |
|   └─TableFullScan_6     | 1.00    | cop[tikv] | table:users   | keep order:false, stats:pseudo |
+-------------------------+---------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

### キャッシュされたテーブルにデータを書き込む {#write-data-to-a-cached-table}

キャッシュされたテーブルはデータの書き込みをサポートします。たとえば、レコードを`users`テーブルに挿入できます。

```sql
INSERT INTO users(id, name) VALUES(1001, 'Davis');
```

```sql
Query OK, 1 row affected (0.00 sec)
```

```sql
SELECT * FROM users;
```

```sql
+------+-------+
| id   | name  |
+------+-------+
| 1001 | Davis |
+------+-------+
1 row in set (0.00 sec)
```

> **注記：**
>
> キャッシュされたテーブルにデータを挿入すると、第 2 レベルの書き込みレイテンシーが発生する可能性があります。レイテンシーはグローバル環境変数[`tidb_table_cache_lease`](/system-variables.md#tidb_table_cache_lease-new-in-v600)によって制御されます。アプリケーションに基づいてレイテンシーが許容できるかどうかを確認することで、キャッシュされたテーブル機能を使用するかどうかを決定できます。たとえば、読み取り専用のシナリオでは、 `tidb_table_cache_lease`の値を増やすことができます。
>
> ```sql
> set @@global.tidb_table_cache_lease = 10;
> ```
>
> キャッシュされたテーブル機能は、キャッシュごとにリースを設定する必要がある複雑なメカニズムで実装されているため、キャッシュされたテーブルの書き込みレイテンシーは長くなります。複数の TiDB インスタンスがある場合、1 つのインスタンスは、他のインスタンスにデータがキャッシュされているかどうかを知りません。インスタンスがテーブル データを直接変更すると、他のインスタンスは古いキャッシュ データを読み取ります。正確性を保証するために、キャッシュされたテーブルの実装ではリース メカニズムを使用して、リースの期限が切れる前にデータが変更されないようにします。そのため、書き込みレイテンシーが長くなります。

キャッシュされたテーブルのメタデータは`mysql.table_cache_meta`のテーブルに保存されます。このテーブルには、キャッシュされたすべてのテーブルの ID、現在のロック ステータス ( `lock_type` )、およびロック リース情報 ( `lease` ) が記録されます。このテーブルは TiDB の内部でのみ使用されるため、変更することはお勧めできません。そうしないと、予期しないエラーが発生する可能性があります。

```sql
SHOW CREATE TABLE mysql.table_cache_meta\G
*************************** 1. row ***************************
       Table: table_cache_meta
Create Table: CREATE TABLE `table_cache_meta` (
  `tid` bigint(11) NOT NULL DEFAULT '0',
  `lock_type` enum('NONE','READ','INTEND','WRITE') NOT NULL DEFAULT 'NONE',
  `lease` bigint(20) NOT NULL DEFAULT '0',
  `oldReadLease` bigint(20) NOT NULL DEFAULT '0',
  PRIMARY KEY (`tid`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.00 sec)
```

### キャッシュされたテーブルを通常のテーブルに戻す {#revert-a-cached-table-to-a-normal-table}

> **注記：**
>
> キャッシュされたテーブルで DDL ステートメントを実行すると失敗します。キャッシュされたテーブルに対して DDL ステートメントを実行する前に、まずキャッシュ属性を削除し、キャッシュされたテーブルを通常のテーブルに戻す必要があります。

```sql
TRUNCATE TABLE users;
```

```sql
ERROR 8242 (HY000): 'Truncate Table' is unsupported on cache tables.
```

```sql
mysql> ALTER TABLE users ADD INDEX k_id(id);
```

```sql
ERROR 8242 (HY000): 'Alter Table' is unsupported on cache tables.
```

キャッシュされたテーブルを通常のテーブルに戻すには、 `ALTER TABLE t NOCACHE`を使用します。

```sql
ALTER TABLE users NOCACHE;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

## キャッシュされたテーブルのサイズ制限 {#size-limit-of-cached-tables}

TiDB はテーブル全体のデータをメモリにロードし、キャッシュされたデータは変更後に無効になり、再ロードする必要があるため、キャッシュされたテーブルは小さなテーブルを使用するシナリオにのみ適しています。

現在、TiDB ではキャッシュされたテーブルのサイズ制限は 64 MB です。テーブルデータが64MBを超える場合、 `ALTER TABLE t CACHE`の実行は失敗します。

## 他の TiDB 機能との互換性制限 {#compatibility-restrictions-with-other-tidb-features}

キャッシュされたテーブルは次の機能をサポート**しません**。

-   パーティション化されたテーブルに対する`ALTER TABLE t ADD PARTITION`操作の実行はサポートされていません。
-   一時テーブルに対する`ALTER TABLE t CACHE`操作の実行はサポートされていません。
-   ビューに対する`ALTER TABLE t CACHE`操作の実行はサポートされていません。
-   ステイル読み取りはサポートされていません。
-   キャッシュされたテーブルに対する直接 DDL 操作はサポートされていません。 DDL 操作を実行する前に、まず`ALTER TABLE t NOCACHE`を使用してキャッシュされたテーブルを通常のテーブルに戻す必要があります。

キャッシュされたテーブルは、次のシナリオでは使用でき**ません**。

-   履歴データを読み取るようにシステム変数`tidb_snapshot`を設定します。
-   変更中、キャッシュされたデータは、データが再ロードされるまで無効になります。

## TiDB 移行ツールとの互換性 {#compatibility-with-tidb-migration-tools}

キャッシュされたテーブルは、MySQL 構文の TiDB 拡張機能です。 TiDB だけが`ALTER TABLE ... CACHE`ステートメントを認識できます。 TiDB 移行ツールは、バックアップ &amp; リストア (BR)、TiCDC、およびDumplingのキャッシュされたテーブルをサポート**しません**。これらのツールは、キャッシュされたテーブルを通常のテーブルとして扱います。

つまり、キャッシュされたテーブルをバックアップおよび復元すると、通常のテーブルになります。ダウンストリーム クラスターが別の TiDB クラスターであり、キャッシュ テーブル機能を引き続き使用したい場合は、ダウンストリーム テーブルで`ALTER TABLE ... CACHE`を実行することで、ダウンストリーム クラスターでキャッシュ テーブルを手動で有効にすることができます。

## こちらも参照 {#see-also}

-   [他の机](/sql-statements/sql-statement-alter-table.md)
-   [システム変数](/system-variables.md)
