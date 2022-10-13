---
title: ALTER TABLE ... COMPACT
summary: An overview of the usage of ALTER TABLE ... COMPACT for the TiDB database.
---

# ALTER TABLE ... コンパクト {#alter-table-compact}

読み取りパフォーマンスを向上させ、ディスク使用量を削減するために、TiDB はバックグラウンドでストレージ ノードのデータ圧縮を自動的にスケジュールします。圧縮中、ストレージ ノードは物理データを書き換えます。これには、削除された行のクリーンアップや、更新によって発生した複数のバージョンのデータのマージが含まれます。 `ALTER TABLE ... COMPACT`ステートメントを使用すると、圧縮がバックグラウンドでトリガーされるまで待たずに、特定のテーブルの圧縮をすぐに開始できます。

このステートメントの実行は、既存の SQL ステートメントをブロックしたり、トランザクション、DDL、GC などの TiDB 機能に影響を与えたりしません。 SQL文で選択できるデータも変更されません。このステートメントを実行すると、一部の IO および CPU リソースが消費されます。ビジネスに悪影響を及ぼさないように、リソースが使用可能になったときなど、実行の適切なタイミングを慎重に選択してください。

テーブルのすべてのレプリカが圧縮されると、圧縮ステートメントが終了して返されます。実行プロセス中に、 [`KILL`](/sql-statements/sql-statement-kill.md)ステートメントを実行することで圧縮を安全に中断できます。圧縮を中断しても、データの一貫性が損なわれたり、データが失われたりすることはなく、その後の手動またはバックグラウンドの圧縮にも影響しません。

このデータ圧縮ステートメントは現在、TiKV レプリカではなく、TiFlash レプリカでのみサポートされています。

## あらすじ {#synopsis}

```ebnf+diagram
AlterTableCompactStmt ::=
    'ALTER' 'TABLE' TableName 'COMPACT' ( 'TIFLASH' 'REPLICA' )?
```

v6.2.0 以降、構文の`TIFLASH REPLICA`の部分を省略できます。省略した場合、ステートメントのセマンティックは変更されず、TiFlash に対してのみ有効になります。

## 例 {#examples}

### テーブル内のコンパクトな TiFlash レプリカ {#compact-tiflash-replicas-in-a-table}

以下は、2 つの TiFlash レプリカを持つ 4 つのパーティションを持つ`employees`のテーブルを例として取り上げています。

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

次のステートメントを実行して、 `employees`のテーブル内のすべてのパーティションの 2 つの TiFlash レプリカの圧縮をすぐに開始できます。

{{< copyable "" >}}

```sql
ALTER TABLE employees COMPACT TIFLASH REPLICA;
```

## 同時実行 {#concurrency}

`ALTER TABLE ... COMPACT`ステートメントは、テーブル内のすべてのレプリカを同時に圧縮します。

オンライン ビジネスへの重大な影響を回避するために、各 TiFlash インスタンスは、デフォルトで一度に 1 つのテーブルのデータのみを圧縮します (バックグラウンドでトリガーされる圧縮を除く)。つまり、複数のテーブルで同時に`ALTER TABLE ... COMPACT`ステートメントを実行すると、それらの実行は同時に実行されるのではなく、同じ TiFlash インスタンスでキューに入れられます。

<CustomContent platform="tidb">

リソース使用量を増やしてテーブル レベルの同時実行性を高めるには、TiFlash 構成を変更します[`manual_compact_pool_size`](/tiflash/tiflash-configuration.md) 。たとえば、 `manual_compact_pool_size`を 2 に設定すると、2 つのテーブルのコンパクションを同時に処理できます。

</CustomContent>

## MySQL の互換性 {#mysql-compatibility}

`ALTER TABLE ... COMPACT`構文は TiDB 固有のもので、標準 SQL 構文の拡張です。同等の MySQL 構文はありませんが、MySQL クライアントまたは MySQL プロトコルに準拠するさまざまなデータベース ドライバーを使用して、このステートメントを実行できます。

## TiDB Binlogと TiCDC の互換性 {#tidb-binlog-and-ticdc-compatibility}

`ALTER TABLE ... COMPACT`ステートメントは論理データの変更をもたらさないため、TiDB Binlogまたは TiCDC によってダウンストリームに複製されません。

## こちらもご覧ください {#see-also}

-   [他の机](/sql-statements/sql-statement-alter-table.md)
-   [キルタイド](/sql-statements/sql-statement-kill.md)
