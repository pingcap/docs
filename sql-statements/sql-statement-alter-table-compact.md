---
title: ALTER TABLE ... COMPACT
summary: TiDB データベースの ALTER TABLE ... COMPACT の使用法の概要。
---

# ALTER TABLE ... COMPACT {#alter-table-compact}

読み取りパフォーマンスを向上させ、ディスク使用量を削減するために、TiDB はstorageノード上でバックグラウンドでデータ圧縮を自動的にスケジュールします。圧縮中、storageノードは物理データを書き換えます。これには、削除された行のクリーンアップや、更新によって発生した複数のデータバージョンのマージなどが含まれます。1 ステートメントを使用すると、 `ALTER TABLE ... COMPACT`グラウンドで圧縮がトリガーされるまで待たずに、特定のテーブルの圧縮を即座に開始できます。

この文を実行しても、既存のSQL文はブロックされず、トランザクション、DDL、GCといったTiDBの機能にも影響はありません。SQL文で選択可能なデータも変更されません。この文の実行は、IOリソースとCPUリソースを消費します。業務への悪影響を避けるため、リソースに余裕があるタイミングなど、適切なタイミングで実行するようご注意ください。

テーブルのすべてのレプリカが圧縮されると、圧縮ステートメントは終了し、結果が返されます。実行プロセス中に、 [`KILL`](/sql-statements/sql-statement-kill.md)ステートメントを実行することで、圧縮を安全に中断できます。圧縮を中断しても、データの整合性が損なわれたり、データが失われたりすることはありません。また、後続の手動圧縮やバックグラウンド圧縮にも影響はありません。

このデータ圧縮ステートメントは現在、 TiFlashレプリカに対してのみサポートされており、TiKV レプリカに対してはサポートされていません。

## 概要 {#synopsis}

```ebnf+diagram
AlterTableCompactStmt ::=
    'ALTER' 'TABLE' TableName 'COMPACT' ( 'PARTITION' PartitionNameList )? ( 'TIFLASH' 'REPLICA' )?
```

バージョン6.2.0以降、構文の`TIFLASH REPLICA`部分を省略できるようになりました。省略した場合、文の意味は変更されず、 TiFlashに対してのみ有効になります。

## 例 {#examples}

### テーブル内のコンパクトなTiFlashレプリカ {#compact-tiflash-replicas-in-a-table}

以下は、2 つのTiFlashレプリカを持つ 4 つのパーティションを持つ`employees`テーブルを例として示します。

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    hired DATE NOT NULL DEFAULT '1970-01-01',
    store_id INT
)
PARTITION BY LIST (store_id) (
    PARTITION pNorth VALUES IN (1, 2, 3, 4, 5),
    PARTITION pEast VALUES IN (6, 7, 8, 9, 10),
    PARTITION pWest VALUES IN (11, 12, 13, 14, 15),
    PARTITION pCentral VALUES IN (16, 17, 18, 19, 20)
);
ALTER TABLE employees SET TIFLASH REPLICA 2;
```

次のステートメントを実行すると、 `employees`テーブル内のすべてのパーティションの 2 つのTiFlashレプリカの圧縮を直ちに開始できます。

```sql
ALTER TABLE employees COMPACT TIFLASH REPLICA;
```

### テーブル内の指定されたパーティションのコンパクトTiFlashレプリカ {#compact-tiflash-replicas-of-specified-partitions-in-a-table}

以下は、2 つのTiFlashレプリカを持つ 4 つのパーティションを持つ`employees`テーブルを例として示します。

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    hired DATE NOT NULL DEFAULT '1970-01-01',
    store_id INT
)
PARTITION BY LIST (store_id) (
    PARTITION pNorth VALUES IN (1, 2, 3, 4, 5),
    PARTITION pEast VALUES IN (6, 7, 8, 9, 10),
    PARTITION pWest VALUES IN (11, 12, 13, 14, 15),
    PARTITION pCentral VALUES IN (16, 17, 18, 19, 20)
);

ALTER TABLE employees SET TIFLASH REPLICA 2;
```

次のステートメントを実行すると、テーブル`employees`のパーティション`pNorth`と`pEast`の 2 つのTiFlashレプリカの圧縮を直ちに開始できます。

```sql
ALTER TABLE employees COMPACT PARTITION pNorth, pEast TIFLASH REPLICA;
```

## 同時実行性 {#concurrency}

`ALTER TABLE ... COMPACT`ステートメントは、テーブル内のすべてのレプリカを同時に圧縮します。

オンラインビジネスへの重大な影響を避けるため、各TiFlashインスタンスは、デフォルトで一度に1つのテーブルのみのデータを圧縮します（バックグラウンドでトリガーされる圧縮を除く）。つまり、 `ALTER TABLE ... COMPACT`ステートメントを複数のテーブルに対して同時に実行した場合、それらの実行は同時に実行されるのではなく、同じTiFlashインスタンス上でキューに入れられます。

<CustomContent platform="tidb">

リソース使用率を高めながらテーブルレベルの同時実行性を高めるには、 TiFlash構成[`manual_compact_pool_size`](/tiflash/tiflash-configuration.md)変更します。例えば、 `manual_compact_pool_size` 2に設定すると、2つのテーブルのコンパクションを同時に処理できます。

</CustomContent>

## データ圧縮の進行状況を観察する {#observe-data-compaction-progress}

`INFORMATION_SCHEMA.TIFLASH_TABLES`テーブルの`TOTAL_DELTA_ROWS`列目を確認することで、データ圧縮の進行状況を確認したり、テーブルの圧縮を開始するかどうかを判断したりできます`TOTAL_DELTA_ROWS`の値が大きいほど、圧縮できるデータ量が多くなります。7 が`TOTAL_DELTA_ROWS` `0`場合、テーブル内のすべてのデータは最適な状態であり、圧縮する必要はありません。

<details><summary>例:パーティションテーブルの圧縮状態を確認する</summary>

```sql
USE test;

CREATE TABLE foo(id INT);

ALTER TABLE foo SET TIFLASH REPLICA 1;

SELECT TOTAL_DELTA_ROWS, TOTAL_STABLE_ROWS FROM INFORMATION_SCHEMA.TIFLASH_TABLES
    WHERE IS_TOMBSTONE = 0 AND
    `TIDB_DATABASE` = "test" AND `TIDB_TABLE` = "foo";
+------------------+-------------------+
| TOTAL_DELTA_ROWS | TOTAL_STABLE_ROWS |
+------------------+-------------------+
|                0 |                 0 |
+------------------+-------------------+

INSERT INTO foo VALUES (1), (3), (7);

SELECT TOTAL_DELTA_ROWS, TOTAL_STABLE_ROWS FROM INFORMATION_SCHEMA.TIFLASH_TABLES
    WHERE IS_TOMBSTONE = 0 AND
    `TIDB_DATABASE` = "test" AND `TIDB_TABLE` = "foo";
+------------------+-------------------+
| TOTAL_DELTA_ROWS | TOTAL_STABLE_ROWS |
+------------------+-------------------+
|                3 |                 0 |
+------------------+-------------------+
-- Newly written data can be compacted

ALTER TABLE foo COMPACT TIFLASH REPLICA;

SELECT TOTAL_DELTA_ROWS, TOTAL_STABLE_ROWS FROM INFORMATION_SCHEMA.TIFLASH_TABLES
    WHERE IS_TOMBSTONE = 0 AND
    `TIDB_DATABASE` = "test" AND `TIDB_TABLE` = "foo";
+------------------+-------------------+
| TOTAL_DELTA_ROWS | TOTAL_STABLE_ROWS |
+------------------+-------------------+
|                0 |                 3 |
+------------------+-------------------+
-- All data is in the best state and no compaction is needed
```

</details>

<details><summary>例:パーティションテーブルの圧縮状態を確認する</summary>

```sql
USE test;

CREATE TABLE employees
    (id INT NOT NULL, store_id INT)
    PARTITION BY LIST (store_id) (
        PARTITION pNorth VALUES IN (1, 2, 3, 4, 5),
        PARTITION pEast VALUES IN (6, 7, 8, 9, 10),
        PARTITION pWest VALUES IN (11, 12, 13, 14, 15),
        PARTITION pCentral VALUES IN (16, 17, 18, 19, 20)
    );

ALTER TABLE employees SET TIFLASH REPLICA 1;

INSERT INTO employees VALUES (1, 1), (6, 6), (10, 10);

SELECT PARTITION_NAME, TOTAL_DELTA_ROWS, TOTAL_STABLE_ROWS
    FROM INFORMATION_SCHEMA.TIFLASH_TABLES t, INFORMATION_SCHEMA.PARTITIONS p
    WHERE t.IS_TOMBSTONE = 0 AND t.TABLE_ID = p.TIDB_PARTITION_ID AND
    p.TABLE_SCHEMA = "test" AND p.TABLE_NAME = "employees";
+----------------+------------------+-------------------+
| PARTITION_NAME | TOTAL_DELTA_ROWS | TOTAL_STABLE_ROWS |
+----------------+------------------+-------------------+
| pNorth         |                1 |                 0 |
| pEast          |                2 |                 0 |
| pWest          |                0 |                 0 |
| pCentral       |                0 |                 0 |
+----------------+------------------+-------------------+
-- Some partitions can be compacted

ALTER TABLE employees COMPACT TIFLASH REPLICA;

SELECT PARTITION_NAME, TOTAL_DELTA_ROWS, TOTAL_STABLE_ROWS
    FROM INFORMATION_SCHEMA.TIFLASH_TABLES t, INFORMATION_SCHEMA.PARTITIONS p
    WHERE t.IS_TOMBSTONE = 0 AND t.TABLE_ID = p.TIDB_PARTITION_ID AND
    p.TABLE_SCHEMA = "test" AND p.TABLE_NAME = "employees";
+----------------+------------------+-------------------+
| PARTITION_NAME | TOTAL_DELTA_ROWS | TOTAL_STABLE_ROWS |
+----------------+------------------+-------------------+
| pNorth         |                0 |                 1 |
| pEast          |                0 |                 2 |
| pWest          |                0 |                 0 |
| pCentral       |                0 |                 0 |
+----------------+------------------+-------------------+
-- Data in all partitions is in the best state and no compaction is needed
```

</details>

> **注記：**
>
> -   圧縮中にデータが更新された場合、圧縮完了後も`TOTAL_DELTA_ROWS` 0以外の値のままになることがあります。これは正常な動作であり、これらの更新が圧縮されていないことを示しています。これらの更新を圧縮するには、 `ALTER TABLE ... COMPACT`ステートメントを再度実行してください。
>
> -   `TOTAL_DELTA_ROWS`は行数ではなくデータバージョンを示します。例えば、行を挿入してから削除した場合、 `TOTAL_DELTA_ROWS` 2ずつ増加します。

## 互換性 {#compatibility}

### MySQLの互換性 {#mysql-compatibility}

`ALTER TABLE ... COMPACT`構文はTiDB固有のもので、標準SQL構文の拡張です。MySQLには同等の構文はありませんが、MySQLクライアントまたはMySQLプロトコルに準拠した各種データベースドライバを使用してこの文を実行できます。

### TiCDC の互換性 {#ticdc-compatibility}

`ALTER TABLE ... COMPACT`ステートメントでは論理データの変更は発生しないため、TiCDC によってダウンストリームに複製されません。

## 参照 {#see-also}

-   [テーブルの変更](/sql-statements/sql-statement-alter-table.md)
-   [TIDBを殺せ](/sql-statements/sql-statement-kill.md)
