---
title: ADMIN CLEANUP INDEX
summary: An overview of the usage of ADMIN CLEANUP for the TiDB database.
---

# 管理者のクリーンアップインデックス {#admin-cleanup-index}

`ADMIN CLEANUP INDEX`ステートメントは、テーブルに一貫性のないデータとインデックスがある場合に、テーブルから冗長なインデックスを削除するために使用されます。この構文はまだ[外部キー制約](/foreign-key.md)をサポートしていないことに注意してください。

## あらすじ {#synopsis}

```ebnf+diagram
AdminCleanupStmt ::=
    'ADMIN' 'CLEANUP' ( 'INDEX' TableName IndexName | 'TABLE' 'LOCK' TableNameList )

TableNameList ::=
    TableName ( ',' TableName )*
```

## 例 {#examples}

何らかの理由により、データベース内の`tbl`テーブルにデータとインデックスの不整合があるとします (たとえば、災害復旧シナリオでクラスター内の一部の行データが失われます)。

```sql
SELECT * FROM tbl;
ERROR 1105 (HY000): inconsistent index idx handle count 3 isn't equal to value count 2

ADMIN CHECK INDEX tbl idx ;
ERROR 1105 (HY000): handle &kv.CommonHandle{encoded:[]uint8{0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xf8}, colEndOffsets:[]uint16{0xa}}, index:types.Datum{k:0x5, decimal:0x0, length:0x0, i:0, collation:"utf8mb4_bin", b:[]uint8{0x0}, x:interface {}(nil)} != record:<nil>
```

`SELECT`クエリのエラー メッセージから、 `tbl`テーブルには 2 行のデータと 3 行のインデックス データが含まれていることがわかります。これは、行とインデックスのデータが矛盾していることを意味します。同時に、少なくとも 1 つのインデックスがダングリング状態になります。この場合、 `ADMIN CLEANUP INDEX`ステートメントを使用して、ダングリング インデックスを削除できます。

```sql
ADMIN CLEANUP INDEX tbl idx;
```

実行結果は以下のようになります。

```sql
ADMIN CLEANUP INDEX tbl idx;
+---------------+
| REMOVED_COUNT |
+---------------+
|             1 |
+---------------+
```

`ADMIN CHECK INDEX`ステートメントを再度実行して、データとインデックスの一貫性をチェックし、データが通常の状態に復元されたかどうかを確認できます。

```sql
ADMIN CHECK INDEX tbl idx;
Query OK, 0 rows affected (0.01 sec)
```

<CustomContent platform="tidb">

> **注記：**
>
> レプリカの損失によりデータとインデックスが不整合になった場合:
>
> -   行データとインデックス データの両方が失われる可能性があります。一貫性を復元するには、 `ADMIN CLEANUP INDEX`と[`ADMIN RECOVER INDEX`](/sql-statements/sql-statement-admin-recover.md)ステートメントを一緒に使用します。
> -   `ADMIN CLEANUP INDEX`ステートメントは常に単一スレッドで実行されます。テーブルデータが大きい場合は、インデックスを再構築してインデックスデータを回復することをお勧めします。
> -   `ADMIN CLEANUP INDEX`ステートメントを実行すると、対応するテーブルまたはインデックスはロックされず、TiDB は他のセッションがテーブル レコードを同時に変更できるようになります。ただし、この場合、 `ADMIN CLEANUP INDEX`すべてのテーブル レコードを正しく処理できない可能性があります。したがって、 `ADMIN CLEANUP INDEX`を実行するときは、テーブルのデータを同時に変更しないようにしてください。
> -   TiDB のエンタープライズ エディションを使用している場合は、サポート エンジニアに[リクエストを送信する](/support.md)して支援を求めることができます。
>
> `ADMIN CLEANUP INDEX`ステートメントはアトミックではありません。ステートメントの実行中に中断された場合は、成功するまで再実行することをお勧めします。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> レプリカの損失によりデータとインデックスが不整合になった場合:
>
> -   行データとインデックス データの両方が失われる可能性があります。一貫性を復元するには、 `ADMIN CLEANUP INDEX`と[`ADMIN RECOVER INDEX`](/sql-statements/sql-statement-admin-recover.md)ステートメントを一緒に使用します。
> -   `ADMIN CLEANUP INDEX`ステートメントは常に単一スレッドで実行されます。テーブルデータが大きい場合は、インデックスを再構築してインデックスデータを回復することをお勧めします。
> -   `ADMIN CLEANUP INDEX`ステートメントを実行すると、対応するテーブルまたはインデックスはロックされず、TiDB は他のセッションがテーブル レコードを同時に変更できるようになります。ただし、この場合、 `ADMIN CLEANUP INDEX`すべてのテーブル レコードを正しく処理できない可能性があります。したがって、 `ADMIN CLEANUP INDEX`を実行するときは、テーブルのデータを同時に変更しないようにしてください。
> -   TiDB のエンタープライズ エディションを使用している場合は、サポート エンジニアに[リクエストを送信する](https://support.pingcap.com/hc/en-us)して支援を求めることができます。
>
> `ADMIN CLEANUP INDEX`ステートメントはアトミックではありません。ステートメントが実行中に中断された場合は、成功するまで再実行することをお勧めします。

</CustomContent>

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [`ADMIN CHECK TABLE/INDEX`](/sql-statements/sql-statement-admin-check-table-index.md)
-   [`ADMIN RECOVER INDEX`](/sql-statements/sql-statement-admin-recover.md)
