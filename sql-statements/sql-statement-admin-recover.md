---
title: ADMIN RECOVER INDEX
summary: An overview of the usage of ADMIN RECOVER INDEX for the TiDB database.
---

# 管理者リカバリインデックス {#admin-recover-index}

行データとインデックスデータに不整合がある場合、 `ADMIN RECOVER INDEX`ステートメントを使用して、冗長化されたインデックスに基づいて整合性を回復できます。この構文はまだ[外部キー制約](/foreign-key.md)をサポートしていないことに注意してください。

## あらすじ {#synopsis}

```ebnf+diagram
AdminCleanupStmt ::=
    'ADMIN' 'RECOVER' 'INDEX' TableName IndexName
```

## 例 {#examples}

何らかの理由により、データベース内の`tbl`テーブルに行データとインデックスが矛盾していると仮定します (たとえば、ディザスタ リカバリ シナリオでクラスタ内の一部の行データが失われるなど)。

```sql
SELECT * FROM tbl;
ERROR 1105 (HY000): inconsistent index idx handle count 2 isn't equal to value count 3

ADMIN CHECK INDEX tbl idx ;
ERROR 1105 (HY000): handle &kv.CommonHandle{encoded:[]uint8{0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xf8}, colEndOffsets:[]uint16{0xa}}, index:types.Datum{k:0x5, decimal:0x0, length:0x0, i:0, collation:"utf8mb4_bin", b:[]uint8{0x0}, x:interface {}(nil)} != record:<nil>
```

`SELECT`クエリのエラー メッセージから、 `tbl`テーブルには 3 行のデータと 2 行のインデックス データが含まれていることがわかります。これは、行データとインデックス データが矛盾していることを意味します。同時に、少なくとも 1 行のデータには対応するインデックスがありません。この場合、 `ADMIN RECOVER INDEX`ステートメントを使用して、欠落しているインデックスを補うことができます。

```sql
ADMIN RECOVER INDEX tbl idx;
```

実行結果は以下のようになります。

```sql
ADMIN RECOVER INDEX tbl idx;
+-------------+------------+
| ADDED_COUNT | SCAN_COUNT |
+-------------+------------+
|           1 |          3 |
+-------------+------------+
1 row in set (0.00 sec)
```

`ADMIN CHECK INDEX`ステートメントを再度実行して、データとインデックスの整合性をチェックし、データが通常の状態に復元されたかどうかを確認できます。

```sql
ADMIN CHECK INDEX tbl idx;
Query OK, 0 rows affected (0.01 sec)
```

<CustomContent platform="tidb">

> **注記：**
>
> レプリカの損失によりデータとインデックスが不整合になった場合:
>
> -   行データとインデックス データの両方が失われる可能性があります。この問題に対処するには、 [`ADMIN CLEANUP INDEX`](/sql-statements/sql-statement-admin-cleanup.md)と`ADMIN RECOVER INDEX`ステートメントを一緒に使用して、行データとインデックス データの整合性を回復します。
> -   `ADMIN RECOVER INDEX`ステートメントは常に単一スレッドで実行されます。テーブルデータが大きい場合は、インデックスを再構築してインデックスデータを回復することをお勧めします。
> -   `ADMIN RECOVER INDEX`ステートメントを実行すると、対応するテーブルまたはインデックスはロックされず、TiDB は他のセッションがテーブル レコードを同時に変更できるようになります。ただし、この場合、 `ADMIN RECOVER INDEX`すべてのテーブル レコードを正しく処理できない可能性があります。したがって、 `ADMIN RECOVER INDEX`を実行するときは、テーブルのデータを同時に変更しないようにしてください。
> -   TiDB のエンタープライズ エディションを使用している場合は、サポート エンジニアに[リクエストを送信する](/support.md)して支援を求めることができます。
>
> `ADMIN RECOVER INDEX`ステートメントはアトミックではありません。ステートメントが実行中に中断された場合は、成功するまで再実行することをお勧めします。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> レプリカの損失によりデータとインデックスが不整合になった場合:
>
> -   行データとインデックス データの両方が失われる可能性があります。この問題に対処するには、 [`ADMIN CLEANUP INDEX`](/sql-statements/sql-statement-admin-cleanup.md)と`ADMIN RECOVER INDEX`ステートメントを一緒に使用して、行データとインデックス データの整合性を回復します。
> -   `ADMIN RECOVER INDEX`ステートメントは常に単一スレッドで実行されます。テーブルデータが大きい場合は、インデックスを再構築してインデックスデータを回復することをお勧めします。
> -   `ADMIN RECOVER INDEX`ステートメントを実行すると、対応するテーブルまたはインデックスはロックされず、TiDB は他のセッションがテーブル レコードを同時に変更できるようになります。ただし、この場合、 `ADMIN RECOVER INDEX`すべてのテーブル レコードを正しく処理できない可能性があります。したがって、 `ADMIN RECOVER INDEX`を実行するときは、テーブルのデータを同時に変更しないようにしてください。
> -   TiDB のエンタープライズ エディションを使用している場合は、サポート エンジニアに[リクエストを送信する](https://support.pingcap.com/hc/en-us)して支援を求めることができます。
>
> `ADMIN RECOVER INDEX`ステートメントはアトミックではありません。ステートメントが実行中に中断された場合は、成功するまで再実行することをお勧めします。

</CustomContent>

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [`ADMIN CHECK TABLE/INDEX`](/sql-statements/sql-statement-admin-check-table-index.md)
-   [`ADMIN CLEANUP INDEX`](/sql-statements/sql-statement-admin-cleanup.md)
