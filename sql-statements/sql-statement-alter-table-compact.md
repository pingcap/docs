---
title: ALTER TABLE ... COMPACT
summary: TiDB データベースに対する ALTER TABLE ... COMPACT の使用法の概要。
---

# ALTER TABLE ... COMPACT {#alter-table-compact}

読み取りパフォーマンスを向上させ、ディスク使用量を削減するために、TiDB はstorageノードでのデータ圧縮を`ALTER TABLE ... COMPACT`グラウンドで自動的にスケジュールします。圧縮中、storageノードは物理データを書き換えます。これには、削除された行のクリーンアップや、更新によって発生した複数のデータ バージョンをマージすることが含まれます。1 ステートメントを使用すると、バックグラウンドで圧縮がトリガーされるまで待たずに、特定のテーブルの圧縮をすぐに開始できます。

このステートメントを実行しても、既存の SQL ステートメントはブロックされず、トランザクション、DDL、GC などの TiDB 機能にも影響はありません。SQL ステートメントで選択できるデータも変更されません。このステートメントを実行すると、IO および CPU リソースが消費されます。ビジネスに悪影響を与えないように、リソースが利用可能なときなど、適切な実行タイミングを選択するように注意してください。

テーブルのすべてのレプリカが圧縮されると、圧縮ステートメントが終了して返されます。実行プロセス中に、 [`KILL`](/sql-statements/sql-statement-kill.md)ステートメントを実行することで、安全に圧縮を中断できます。圧縮を中断しても、データの一貫性が損なわれたり、データが失われたりすることはありません。また、後続の手動またはバックグラウンドの圧縮にも影響しません。

このデータ圧縮ステートメントは現在、 TiFlashレプリカに対してのみサポートされており、TiKV レプリカに対してはサポートされていません。

## 概要 {#synopsis}

```ebnf+diagram
AlterTableCompactStmt ::=
    'ALTER' 'TABLE' TableName 'COMPACT' ( 'PARTITION' PartitionNameList )? ( 'TIFLASH' 'REPLICA' )?
```

v6.2.0 以降では、構文の`TIFLASH REPLICA`部分を省略できます。省略した場合、ステートメントのセマンティクスは変更されず、 TiFlashに対してのみ有効になります。

## 例 {#examples}

### テーブル内のコンパクトなTiFlashレプリカ {#compact-tiflash-replicas-in-a-table}

以下は、2 つのTiFlashレプリカを持つ 4 つのパーティションを持つ`employees`テーブルを例にしています。

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

次のステートメントを実行すると、 `employees`テーブル内のすべてのパーティションの 2 つのTiFlashレプリカの圧縮をすぐに開始できます。

```sql
ALTER TABLE employees COMPACT TIFLASH REPLICA;
```

### テーブル内の指定されたパーティションのコンパクトなTiFlashレプリカ {#compact-tiflash-replicas-of-specified-partitions-in-a-table}

以下は、2 つのTiFlashレプリカを持つ 4 つのパーティションを持つ`employees`テーブルを例にしています。

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

次のステートメントを実行すると、 `employees`テーブル内の`pNorth`および`pEast`パーティションの 2 つのTiFlashレプリカの圧縮をすぐに開始できます。

```sql
ALTER TABLE employees COMPACT PARTITION pNorth, pEast TIFLASH REPLICA;
```

## 同時実行性 {#concurrency}

`ALTER TABLE ... COMPACT`ステートメントは、テーブル内のすべてのレプリカを同時に圧縮します。

オンライン ビジネスへの重大な影響を回避するために、各TiFlashインスタンスは、デフォルトでは一度に 1 つのテーブルのデータのみを圧縮します (バックグラウンドでトリガーされる圧縮を除く)。つまり、 `ALTER TABLE ... COMPACT`ステートメントを複数のテーブルで同時に実行する場合、それらの実行は同時に実行されるのではなく、同じTiFlashインスタンスでキューに入れられます。

<CustomContent platform="tidb">

リソース使用率を高めてテーブルレベルの同時実行性を高めるには、 TiFlash構成[`manual_compact_pool_size`](/tiflash/tiflash-configuration.md)を変更します。たとえば、 `manual_compact_pool_size` 2 に設定すると、2 つのテーブルの圧縮を同時に処理できます。

</CustomContent>

## データ圧縮の進行状況を観察する {#observe-data-compaction-progress}

`INFORMATION_SCHEMA.TIFLASH_TABLES`テーブルの`TOTAL_DELTA_ROWS`列をチェックすることで、データ圧縮の進行状況を確認したり、テーブルの圧縮を開始するかどうかを判断したりできます。 `TOTAL_DELTA_ROWS`の値が大きいほど、圧縮できるデータが多くなります。 `TOTAL_DELTA_ROWS`が`0`の場合、テーブル内のすべてのデータは最適な状態であり、圧縮する必要はありません。

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
> -   圧縮中にデータが更新された場合、圧縮が完了した後も`TOTAL_DELTA_ROWS` 0 以外の値のままである可能性があります。これは正常であり、これらの更新が圧縮されていないことを示しています。これらの更新を圧縮するには、 `ALTER TABLE ... COMPACT`ステートメントを再度実行します。
>
> -   `TOTAL_DELTA_ROWS`数ではなくデータのバージョンを示します。たとえば、行を挿入してから削除すると、 `TOTAL_DELTA_ROWS`は 2 増加します。

## 互換性 {#compatibility}

### MySQL 互換性 {#mysql-compatibility}

`ALTER TABLE ... COMPACT`構文は TiDB 固有のもので、標準 SQL 構文の拡張です。同等の MySQL 構文はありませんが、MySQL クライアントまたは MySQL プロトコルに準拠するさまざまなデータベース ドライバーを使用してこのステートメントを実行できます。

### TiDB Binlogと TiCDC の互換性 {#tidb-binlog-and-ticdc-compatibility}

`ALTER TABLE ... COMPACT`ステートメントでは論理データの変更は発生しないため、TiDB Binlogまたは TiCDC によってダウンストリームに複製されません。

## 参照 {#see-also}

-   [テーブルの変更](/sql-statements/sql-statement-alter-table.md)
-   [TIDBを殺せ](/sql-statements/sql-statement-kill.md)
