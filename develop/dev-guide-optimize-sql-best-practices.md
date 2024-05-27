---
title: Performance Tuning Best Practices
summary: TiDB パフォーマンスをチューニングするためのベスト プラクティスを紹介します。
---

# 性能チューニングのベストプラクティス {#performance-tuning-best-practices}

このドキュメントでは、TiDB データベースの使用に関するベスト プラクティスをいくつか紹介します。

## DMLのベストプラクティス {#dml-best-practices}

このセクションでは、TiDB で DML を使用する場合のベスト プラクティスについて説明します。

### 複数行のステートメントを使用する {#use-multi-row-statements}

テーブルの複数の行を変更する必要がある場合は、複数行ステートメントを使用することをお勧めします。

```sql
INSERT INTO t VALUES (1, 'a'), (2, 'b'), (3, 'c');

DELETE FROM t WHERE id IN (1, 2, 3);
```

複数の単一行ステートメントを使用することはお勧めしません。

```sql
INSERT INTO t VALUES (1, 'a');
INSERT INTO t VALUES (2, 'b');
INSERT INTO t VALUES (3, 'c');

DELETE FROM t WHERE id = 1;
DELETE FROM t WHERE id = 2;
DELETE FROM t WHERE id = 3;
```

### <code>PREPARE</code>使用する {#use-code-prepare-code}

SQL ステートメントを複数回実行する必要がある場合は、SQL 構文を繰り返し解析するオーバーヘッドを回避するために、 `PREPARE`ステートメントを使用することをお勧めします。

<SimpleTab>
<div label="Golang">

```go
func BatchInsert(db *sql.DB) error {
    stmt, err := db.Prepare("INSERT INTO t (id) VALUES (?), (?), (?), (?), (?)")
    if err != nil {
        return err
    }
    for i := 0; i < 1000; i += 5 {
        values := []interface{}{i, i + 1, i + 2, i + 3, i + 4}
        _, err = stmt.Exec(values...)
        if err != nil {
            return err
        }
    }
    return nil
}
```

</div>

<div label="Java">

```java
public void batchInsert(Connection connection) throws SQLException {
    PreparedStatement statement = connection.prepareStatement(
            "INSERT INTO `t` (`id`) VALUES (?), (?), (?), (?), (?)");
    for (int i = 0; i < 1000; i ++) {
        statement.setInt(i % 5 + 1, i);

        if (i % 5 == 4) {
            statement.executeUpdate();
        }
    }
}
```

</div>
</SimpleTab>

`PREPARE`ステートメントを繰り返し実行しないでください。繰り返し実行すると、実行効率が向上しません。

### 必要な列のみをクエリする {#only-query-the-columns-you-need}

すべての列のデータが必要ない場合は、 `SELECT *`使用してすべての列のデータを返さないでください。次のクエリは非効率的です。

```sql
SELECT * FROM books WHERE title = 'Marian Yost';
```

必要な列のみをクエリする必要があります。例:

```sql
SELECT title, price FROM books WHERE title = 'Marian Yost';
```

### 一括削除を使用する {#use-bulk-delete}

大量のデータを削除する場合は[一括削除](/develop/dev-guide-delete-data.md#bulk-delete)使用することをお勧めします。

### 一括更新を使用する {#use-bulk-update}

大量のデータを更新する場合は[一括更新](/develop/dev-guide-update-data.md#bulk-update)使用することをお勧めします。

### 完全なテーブルデータには<code>DELETE</code>ではなく<code>TRUNCATE</code>使用します {#use-code-truncate-code-instead-of-code-delete-code-for-full-table-data}

テーブルからすべてのデータを削除する必要がある場合は、 `TRUNCATE`ステートメントを使用することをお勧めします。

```sql
TRUNCATE TABLE t;
```

完全なテーブルデータに`DELETE`使用することはお勧めしません。

```sql
DELETE FROM t;
```

## DDLのベストプラクティス {#ddl-best-practices}

このセクションでは、TiDB の DDL を使用する際のベスト プラクティスについて説明します。

### 主キーのベストプラクティス {#primary-key-best-practices}

[主キーを選択する際に従うべきルール](/develop/dev-guide-create-table.md#guidelines-to-follow-when-selecting-primary-key)参照してください。

## インデックスのベストプラクティス {#index-best-practices}

[インデックスのベストプラクティス](/develop/dev-guide-index-best-practice.md)参照。

### インデックスのベストプラクティスを追加する {#add-index-best-practices}

TiDB は、オンライン インデックス追加操作をサポートしています。1 または[インデックスを追加](/sql-statements/sql-statement-add-index.md) [インデックスの作成](/sql-statements/sql-statement-create-index.md)ステートメントを使用してインデックスを追加できます。テーブル内のデータの読み取りと書き込みはブロックされません。次のシステム変数を変更することで、インデックス追加操作の`re-organize`フェーズ中に同時実行性とバッチ サイズを調整できます。

-   [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)
-   [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)

オンライン アプリケーションへの影響を減らすために、インデックス追加操作のデフォルトの速度は遅くなっています。インデックス追加操作の対象列に読み取り負荷のみが含まれる場合、またはオンライン ワークロードに直接関連していない場合は、上記の変数の値を適切に増やして、インデックス追加操作を高速化できます。

```sql
SET @@global.tidb_ddl_reorg_worker_cnt = 16;
SET @@global.tidb_ddl_reorg_batch_size = 4096;
```

インデックス追加操作のターゲット列が頻繁に更新される場合 ( `UPDATE` 、 `INSERT` 、 `DELETE`を含む)、上記の変数を増やすと書き込み競合が増加し、オンライン ワークロードに影響します。したがって、再試行が頻繁に行われるため、インデックス追加操作の完了に時間がかかる場合があります。この場合、オンライン アプリケーションとの書き込み競合を回避するために、上記の変数の値を減らすことをお勧めします。

```sql
SET @@global.tidb_ddl_reorg_worker_cnt = 4;
SET @@global.tidb_ddl_reorg_batch_size = 128;
```

## トランザクションの競合 {#transaction-conflicts}

<CustomContent platform="tidb">

トランザクションの競合を特定して解決する方法については、 [ロック競合のトラブルシューティング](/troubleshoot-lock-conflicts.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

トランザクションの競合を特定して解決する方法については、 [ロック競合のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-lock-conflicts)参照してください。

</CustomContent>

## TiDB を使用したJavaアプリケーション開発のベスト プラクティス {#best-practices-for-developing-java-applications-with-tidb}

<CustomContent platform="tidb">

[TiDB を使用したJavaアプリケーション開発のベスト プラクティス](/best-practices/java-app-best-practices.md)参照。

</CustomContent>

<CustomContent platform="tidb-cloud">

[TiDB を使用したJavaアプリケーション開発のベスト プラクティス](https://docs.pingcap.com/tidb/stable/java-app-best-practices)参照。

</CustomContent>

### 参照 {#see-also}

<CustomContent platform="tidb">

-   [高度な同時書き込みのベストプラクティス](/best-practices/high-concurrency-best-practices.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [高度な同時書き込みのベストプラクティス](https://docs.pingcap.com/tidb/stable/high-concurrency-best-practices)

</CustomContent>
