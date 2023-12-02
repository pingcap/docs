---
title: ALTER TABLE ... COMPACT
summary: An overview of the usage of ALTER TABLE ... COMPACT for the TiDB database.
---

# ALTER TABLE ... コンパクト {#alter-table-compact}

読み取りパフォーマンスを向上させ、ディスク使用量を削減するために、TiDB はバックグラウンドでstorageノード上でデータ圧縮を自動的にスケジュールします。圧縮中に、storageノードは、削除された行のクリーンアップや、更新によって生じた複数のバージョンのデータのマージなど、物理データを再書き込みします。 `ALTER TABLE ... COMPACT`ステートメントを使用すると、バックグラウンドで圧縮がトリガーされるまで待たずに、特定のテーブルの圧縮をすぐに開始できます。

このステートメントの実行は、既存の SQL ステートメントをブロックしたり、トランザクション、DDL、GC などの TiDB 機能に影響を与えたりすることはありません。 SQL ステートメントで選択できるデータも変更されません。このステートメントを実行すると、一部の IO リソースと CPU リソースが消費されます。ビジネスへの悪影響を避けるために、リソースが利用可能な場合など、実行の適切なタイミングを選択するように注意してください。

テーブルのすべてのレプリカが圧縮されると、圧縮ステートメントは終了して返されます。実行プロセス中に、 [`KILL`](/sql-statements/sql-statement-kill.md)ステートメントを実行することで圧縮を安全に中断できます。圧縮を中断しても、データの一貫性が損なわれたり、データの損失が発生したりすることはなく、その後の手動またはバックグラウンドの圧縮にも影響しません。

このデータ圧縮ステートメントは現在、 TiFlashレプリカでのみサポートされており、TiKV レプリカではサポートされていません。

## あらすじ {#synopsis}

```ebnf+diagram
AlterTableCompactStmt ::=
    'ALTER' 'TABLE' TableName 'COMPACT' ( 'PARTITION' PartitionNameList )? ( 'TIFLASH' 'REPLICA' )?
```

v6.2.0 以降、構文の`TIFLASH REPLICA`部分は省略できるようになりました。省略した場合、ステートメントのセマンティクスは変更されず、 TiFlashに対してのみ有効になります。

## 例 {#examples}

### テーブル内のコンパクトTiFlashレプリカ {#compact-tiflash-replicas-in-a-table}

以下では、2 つのTiFlashレプリカを持つ 4 つのパーティションを持つ`employees`テーブルを例として取り上げます。

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

### テーブル内の指定されたパーティションのコンパクトTiFlashレプリカ {#compact-tiflash-replicas-of-specified-partitions-in-a-table}

以下では、2 つのTiFlashレプリカを持つ 4 つのパーティションを持つ`employees`テーブルを例として取り上げます。

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

次のステートメントを実行すると、テーブル`employees`のパーティション`pNorth`と`pEast`の 2 つのTiFlashレプリカの圧縮をただちに開始できます。

```sql
ALTER TABLE employees COMPACT PARTITION pNorth, pEast TIFLASH REPLICA;
```

## 同時実行性 {#concurrency}

`ALTER TABLE ... COMPACT`ステートメントは、テーブル内のすべてのレプリカを同時に圧縮します。

オンライン ビジネスへの重大な影響を避けるため、各TiFlashインスタンスは、デフォルトで一度に 1 つのテーブルのデータのみを圧縮します (バックグラウンドでトリガーされる圧縮を除く)。これは、複数のテーブルで`ALTER TABLE ... COMPACT`ステートメントを同時に実行すると、それらの実行は同時に実行されるのではなく、同じTiFlashインスタンスのキューに入れられることを意味します。

<CustomContent platform="tidb">

リソース使用量を増やしてテーブルレベルの同時実行性を高めるには、 TiFlash構成を変更します[`manual_compact_pool_size`](/tiflash/tiflash-configuration.md) 。たとえば、 `manual_compact_pool_size`を 2 に設定すると、2 つのテーブルのコンパクションを同時に処理できます。

</CustomContent>

## データ圧縮の進行状況を観察する {#observe-data-compaction-progress}

`INFORMATION_SCHEMA.TIFLASH_TABLES`テーブルの`TOTAL_DELTA_ROWS`列をチェックすることで、データ圧縮の進行状況を観察したり、テーブルの圧縮を開始するかどうかを決定したりできます。 `TOTAL_DELTA_ROWS`の値が大きいほど、より多くのデータを圧縮できます。 `TOTAL_DELTA_ROWS`が`0`の場合、テーブル内のすべてのデータは最良の状態にあり、圧縮する必要はありません。

<details><summary>例: 非パーティションテーブルの圧縮状態を確認する</summary>

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
> -   圧縮中にデータが更新された場合、圧縮が完了した後も`TOTAL_DELTA_ROWS`ゼロ以外の値になる可能性があります。これは正常であり、これらの更新が圧縮されていないことを示します。これらの更新を圧縮するには、 `ALTER TABLE ... COMPACT`ステートメントを再度実行します。
>
> -   `TOTAL_DELTA_ROWS`は行数ではなく、データのバージョンを示します。たとえば、行を挿入して削除すると、 `TOTAL_DELTA_ROWS` 2 ずつ増加します。

## 互換性 {#compatibility}

### MySQLの互換性 {#mysql-compatibility}

`ALTER TABLE ... COMPACT`構文は TiDB 固有であり、標準 SQL 構文の拡張です。同等の MySQL 構文はありませんが、MySQL クライアントまたは MySQL プロトコルに準拠するさまざまなデータベース ドライバーを使用してこのステートメントを実行できます。

### TiDB Binlogと TiCDC の互換性 {#tidb-binlog-and-ticdc-compatibility}

`ALTER TABLE ... COMPACT`ステートメントは論理データの変更をもたらさないため、TiDB Binlogまたは TiCDC によってダウンストリームにレプリケートされません。

## こちらも参照 {#see-also}

-   [他の机](/sql-statements/sql-statement-alter-table.md)
-   [タイブを殺す](/sql-statements/sql-statement-kill.md)
