---
title: ALTER TABLE ... COMPACT
summary: An overview of the usage of ALTER TABLE ... COMPACT for the TiDB database.
---

# ALTER TABLE ... COMPACT {#alter-table-compact}

> **警告：**
>
> このステートメントはまだ実験的機能です。実稼働環境で使用することはお勧めしません。

読み取りパフォーマンスを向上させ、ディスク使用量を削減するために、TiDBはバックグラウンドのストレージノードでデータ圧縮を自動的にスケジュールします。圧縮中に、ストレージノードは物理データを再書き込みします。これには、削除された行のクリーンアップや、更新によって発生したデータの複数のバージョンのマージが含まれます。 `ALTER TABLE ... COMPACT`ステートメントを使用すると、バックグラウンドで圧縮がトリガーされるまで待たずに、特定のテーブルの圧縮をすぐに開始できます。

このステートメントの実行は、既存のSQLステートメントをブロックしたり、トランザクション、DDL、GCなどのTiDB機能に影響を与えたりすることはありません。 SQLステートメントで選択できるデータも変更されません。ただし、このステートメントを実行すると、IOおよびCPUリソースが消費されるため、SQL実行の待ち時間が長くなる可能性があります。

テーブルのすべてのレプリカが圧縮されると、圧縮ステートメントが終了して返されます。実行プロセス中に、 [`KILL`](/sql-statements/sql-statement-kill.md)ステートメントを実行することにより、圧縮を安全に中断できます。圧縮を中断しても、データの一貫性が損なわれたり、データが失われたりすることはなく、その後の手動またはバックグラウンドの圧縮にも影響しません。

このデータ圧縮ステートメントは現在、TiFlashレプリカでのみサポートされており、TiKVレプリカではサポートされていません。

## あらすじ {#synopsis}

```ebnf+diagram
AlterTableCompactStmt ::=
    'ALTER' 'TABLE' TableName 'COMPACT' 'TIFLASH' 'REPLICA'
```

## 例 {#examples}

### テーブル内のコンパクトなTiFlashレプリカ {#compact-tiflash-replicas-in-a-table}

以下は、例として`employees`のテーブルを取ります。これには、2つのTiFlashレプリカを持つ4つのパーティションがあります。

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

次のステートメントを実行して、 `employees`のテーブル内のすべてのパーティションの2つのTiFlashレプリカの圧縮をすぐに開始できます。

{{< copyable "" >}}

```sql
ALTER TABLE employees COMPACT TIFLASH REPLICA;
```

## 並行性 {#concurrency}

`ALTER TABLE ... COMPACT`ステートメントは、テーブル内のすべてのレプリカを同時に圧縮します。

オンラインビジネスへの重大な影響を回避するために、各TiFlashインスタンスは、デフォルトで一度に1つのテーブルのデータのみを圧縮します（バックグラウンドでトリガーされる圧縮を除く）。つまり、 `ALTER TABLE ... COMPACT`のステートメントを複数のテーブルで同時に実行すると、それらの実行は同時に実行されるのではなく、同じTiFlashインスタンスでキューに入れられます。

より高いリソース使用量でより大きなテーブルレベルの同時実行性を取得するために、TiFlash構成を変更できます[`manual_compact_pool_size`](/tiflash/tiflash-configuration.md) 。たとえば、 `manual_compact_pool_size`が2に設定されている場合、2つのテーブルの圧縮を同時に処理できます。

## MySQLの互換性 {#mysql-compatibility}

`ALTER TABLE ... COMPACT`構文はTiDB固有であり、標準SQL構文の拡張です。同等のMySQL構文はありませんが、MySQLクライアントまたはMySQLプロトコルに準拠するさまざまなデータベースドライバーを使用して、このステートメントを実行できます。

## BinlogとTiCDCの互換性 {#tidb-binlog-and-ticdc-compatibility}

`ALTER TABLE ... COMPACT`ステートメントは論理データの変更をもたらさないため、 BinlogまたはTiCDCによってダウンストリームに複製されません。

## も参照してください {#see-also}

-   [他の机](/sql-statements/sql-statement-alter-table.md)
-   [TIDBを殺す](/sql-statements/sql-statement-kill.md)
