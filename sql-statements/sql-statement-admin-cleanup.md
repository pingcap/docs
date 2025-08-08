---
title: ADMIN CLEANUP INDEX
summary: TiDB データベースの ADMIN CLEANUP の使用法の概要。
---

# 管理者クリーンアップインデックス {#admin-cleanup-index}

`ADMIN CLEANUP INDEX`文は、テーブルに不整合なデータとインデックスがある場合に、テーブルから冗長なインデックスを削除するために使用されます。この構文は[外部キー制約](/foreign-key.md)まだサポートしていないことに注意してください。

## 概要 {#synopsis}

```ebnf+diagram
AdminCleanupStmt ::=
    'ADMIN' 'CLEANUP' ( 'INDEX' TableName IndexName | 'TABLE' 'LOCK' TableNameList )

TableNameList ::=
    TableName ( ',' TableName )*
```

## 例 {#examples}

何らかの理由により、データベース内の`tbl`テーブルに不整合なデータとインデックスがあるとします (たとえば、災害復旧シナリオでクラスター内の一部の行データが失われるなど)。

```sql
SELECT * FROM tbl;
ERROR 1105 (HY000): inconsistent index idx handle count 3 isn't equal to value count 2

ADMIN CHECK INDEX tbl idx ;
ERROR 1105 (HY000): handle &kv.CommonHandle{encoded:[]uint8{0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xf8}, colEndOffsets:[]uint16{0xa}}, index:types.Datum{k:0x5, decimal:0x0, length:0x0, i:0, collation:"utf8mb4_bin", b:[]uint8{0x0}, x:interface {}(nil)} != record:<nil>
```

クエリ`SELECT`のエラーメッセージから、テーブル`tbl`には2行のデータと3行のインデックスデータが含まれていることがわかります。これは、行とインデックスのデータが不整合であることを意味します。同時に、少なくとも1つのインデックスがダングリング状態にあります。この場合、 `ADMIN CLEANUP INDEX`ステートメントを使用してダングリングインデックスを削除できます。

```sql
ADMIN CLEANUP INDEX tbl idx;
```

実行結果は以下のとおりです。

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
> -   行データとインデックスデータの両方が失われている可能性があります。一貫性を回復するには、 `ADMIN CLEANUP INDEX`と[`ADMIN RECOVER INDEX`](/sql-statements/sql-statement-admin-recover.md)ステートメントを一緒に使用してください。
> -   `ADMIN CLEANUP INDEX`ステートメントは常に単一スレッドで実行されます。テーブルデータが大きい場合は、インデックスを再構築してインデックスデータを回復することをお勧めします。
> -   `ADMIN CLEANUP INDEX`文を実行すると、対応するテーブルまたはインデックスはロックされず、TiDB は他のセッションによるテーブルレコードの同時変更を許可します。ただし、この場合、 `ADMIN CLEANUP INDEX`ではすべてのテーブルレコードを正しく処理できない可能性があります。したがって、 `ADMIN CLEANUP INDEX`を実行する際は、テーブルデータの同時変更を避けてください。
> -   TiDB のエンタープライズ エディションを使用する場合は、 [リクエストを送信する](/support.md)サポート エンジニアに問い合わせて支援を受けることができます。
>
> `ADMIN CLEANUP INDEX`文はアトミックではありません。実行中に文が中断された場合は、成功するまで再度実行することをお勧めします。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> レプリカの損失によりデータとインデックスが不整合になった場合:
>
> -   行データとインデックスデータの両方が失われている可能性があります。一貫性を回復するには、 `ADMIN CLEANUP INDEX`と[`ADMIN RECOVER INDEX`](/sql-statements/sql-statement-admin-recover.md)ステートメントを一緒に使用してください。
> -   `ADMIN CLEANUP INDEX`ステートメントは常に単一スレッドで実行されます。テーブルデータが大きい場合は、インデックスを再構築してインデックスデータを回復することをお勧めします。
> -   `ADMIN CLEANUP INDEX`文を実行すると、対応するテーブルまたはインデックスはロックされず、TiDB は他のセッションによるテーブルレコードの同時変更を許可します。ただし、この場合、 `ADMIN CLEANUP INDEX`ではすべてのテーブルレコードを正しく処理できない可能性があります。したがって、 `ADMIN CLEANUP INDEX`を実行する際は、テーブルデータの同時変更を避けてください。
> -   TiDB のエンタープライズ エディションを使用する場合は、 [リクエストを送信する](https://tidb.support.pingcap.com/)サポート エンジニアに問い合わせて支援を受けることができます。
>
> `ADMIN CLEANUP INDEX`文はアトミックではありません。実行中に文が中断された場合は、成功するまで再度実行することをお勧めします。

</CustomContent>

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [`ADMIN CHECK TABLE/INDEX`](/sql-statements/sql-statement-admin-check-table-index.md)
-   [`ADMIN RECOVER INDEX`](/sql-statements/sql-statement-admin-recover.md)
