---
title: ADMIN CLEANUP INDEX
summary: An overview of the usage of ADMIN CLEANUP for the TiDB database.
---

# 管理者クリーンアップ インデックス {#admin-cleanup-index}

`ADMIN CLEANUP INDEX`ステートメントは、テーブルに一貫性のないデータとインデックスがある場合にテーブルから冗長なインデックスを削除するために使用されます。この構文はまだ外部キー制約をサポートしていないことに注意してください。

## あらすじ {#synopsis}

```ebnf+diagram
AdminCleanupStmt ::=
    'ADMIN' 'CLEANUP' ( 'INDEX' TableName IndexName | 'TABLE' 'LOCK' TableNameList )

TableNameList ::=
    TableName ( ',' TableName )*
```

## 例 {#examples}

データベース内の`tbl`テーブルのデータとインデックスが何らかの理由で矛盾しているとします (たとえば、災害復旧シナリオでクラスター内の一部の行データが失われるなど)。

```sql
SELECT * FROM tbl;
ERROR 1105 (HY000): inconsistent index idx handle count 3 isn't equal to value count 2

ADMIN CHECK INDEX tbl idx ;
ERROR 1105 (HY000): handle &kv.CommonHandle{encoded:[]uint8{0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xf8}, colEndOffsets:[]uint16{0xa}}, index:types.Datum{k:0x5, decimal:0x0, length:0x0, i:0, collation:"utf8mb4_bin", b:[]uint8{0x0}, x:interface {}(nil)} != record:<nil>
```

`SELECT`クエリのエラー メッセージから、 `tbl`テーブルには 2 行のデータと 3 行のインデックス データが含まれていることがわかります。これは、行データとインデックス データに一貫性がないことを意味します。同時に、少なくとも 1 つのインデックスがダングリング状態になります。この場合、 `ADMIN CLEANUP INDEX`ステートメントを使用してダングリング インデックスを削除できます。

```sql
ADMIN CLEANUP INDEX tbl idx;
```

実行結果は次のとおりです。

```sql
ADMIN CLEANUP INDEX tbl idx;
+---------------+
| REMOVED_COUNT |
+---------------+
|             1 |
+---------------+
```

`ADMIN CHECK INDEX`ステートメントを再度実行して、データとインデックスの整合性を確認し、データが正常な状態に復元されたかどうかを確認できます。

```sql
ADMIN CHECK INDEX tbl idx;
Query OK, 0 rows affected (0.01 sec)
```

> **ノート：**
>
> レプリカが失われたためにデータとインデックスに一貫性がない場合:
>
> -   行データと索引データの両方が失われる可能性があります。一貫性を回復するには、 `ADMIN CLEANUP INDEX`ステートメントと[`ADMIN RECOVER INDEX`](/sql-statements/sql-statement-admin-recover.md)ステートメントを一緒に使用します。
> -   `ADMIN CLEANUP INDEX`ステートメントは、常に単一のスレッドで実行されます。テーブルデータが大きい場合は、インデックスを再構築してインデックスデータを回復することをお勧めします。
> -   `ADMIN CLEANUP INDEX`ステートメントを実行すると、対応するテーブルまたはインデックスはロックされず、TiDB は他のセッションが同時にテーブル レコードを変更できるようにします。ただし、この場合、 `ADMIN CLEANUP INDEX`ではすべてのテーブル レコードを正しく処理できない可能性があります。したがって、 `ADMIN CLEANUP INDEX`を実行するときは、同時にテーブル データを変更することは避けてください。
> -   TiDB のエンタープライズ エディションを使用している場合は、サポート エンジニアに[リクエストを提出する](https://support.pingcap.com/hc/en-us)して支援を受けることができます。
>
> `ADMIN CLEANUP INDEX`ステートメントはアトミックではありません。実行中にステートメントが中断された場合は、成功するまで再度実行することをお勧めします。

## MySQL の互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## こちらもご覧ください {#see-also}

-   [`ADMIN CHECK TABLE/INDEX`](/sql-statements/sql-statement-admin-check-table-index.md)
-   [`ADMIN RECOVER INDEX`](/sql-statements/sql-statement-admin-recover.md)
