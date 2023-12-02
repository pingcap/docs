---
title: Performance Tuning Best Practices
summary: Introduces the best practices for tuning TiDB performance.
---

# 性能チューニングのベストプラクティス {#performance-tuning-best-practices}

このドキュメントでは、TiDB データベースを使用するためのベスト プラクティスをいくつか紹介します。

## DML のベスト プラクティス {#dml-best-practices}

このセクションでは、TiDB で DML を使用する場合のベスト プラクティスについて説明します。

### 複数行のステートメントを使用する {#use-multi-row-statements}

テーブルの複数の行を変更する必要がある場合は、複数行のステートメントを使用することをお勧めします。

```sql
INSERT INTO t VALUES (1, 'a'), (2, 'b'), (3, 'c');

DELETE FROM t WHERE id IN (1, 2, 3);
```

複数の単一行ステートメントを使用することはお勧めできません。

```sql
INSERT INTO t VALUES (1, 'a');
INSERT INTO t VALUES (2, 'b');
INSERT INTO t VALUES (3, 'c');

DELETE FROM t WHERE id = 1;
DELETE FROM t WHERE id = 2;
DELETE FROM t WHERE id = 3;
```

### <code>PREPARE</code>を使用する {#use-code-prepare-code}

SQL ステートメントを複数回実行する必要がある場合は、SQL 構文を繰り返し解析するオーバーヘッドを避けるために`PREPARE`ステートメントを使用することをお勧めします。

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

`PREPARE`ステートメントを繰り返し実行しないでください。そうしないと実行効率が向上しません。

### 必要な列のみをクエリします {#only-query-the-columns-you-need}

すべての列のデータが必要ない場合は、すべての列のデータを返すために`SELECT *`を使用しないでください。次のクエリは非効率的です。

```sql
SELECT * FROM books WHERE title = 'Marian Yost';
```

必要な列のみをクエリする必要があります。例えば：

```sql
SELECT title, price FROM books WHERE title = 'Marian Yost';
```

### 一括削除を使用する {#use-bulk-delete}

大量のデータを削除する場合は、 [一括削除](/develop/dev-guide-delete-data.md#bulk-delete)を使用することをお勧めします。

### 一括更新を使用する {#use-bulk-update}

大量のデータを更新する場合は、 [一括更新](/develop/dev-guide-update-data.md#bulk-update)を使用することをお勧めします。

### テーブル全体のデータには<code>DELETE</code>ではなく<code>TRUNCATE</code>使用してください {#use-code-truncate-code-instead-of-code-delete-code-for-full-table-data}

テーブルからすべてのデータを削除する必要がある場合は、 `TRUNCATE`ステートメントを使用することをお勧めします。

```sql
TRUNCATE TABLE t;
```

完全なテーブル データに`DELETE`を使用することはお勧めできません。

```sql
DELETE FROM t;
```

## DDL のベスト プラクティス {#ddl-best-practices}

このセクションでは、TiDB の DDL を使用する際のベスト プラクティスについて説明します。

### 主キーのベスト プラクティス {#primary-key-best-practices}

[主キーを選択するときに従うべきルール](/develop/dev-guide-create-table.md#guidelines-to-follow-when-selecting-primary-key)参照してください。

## インデックスのベストプラクティス {#index-best-practices}

[インデックスのベストプラクティス](/develop/dev-guide-index-best-practice.md)を参照してください。

### インデックスのベスト プラクティスを追加する {#add-index-best-practices}

TiDB は、オンラインのインデックス追加操作をサポートしています。 [インデックスの追加](/sql-statements/sql-statement-add-index.md)または[インデックスの作成](/sql-statements/sql-statement-create-index.md)ステートメントを使用してインデックスを追加できます。テーブル内のデータの読み取りと書き込みはブロックされません。次のシステム変数を変更することで、インデックス追加操作の`re-organize`フェーズ中に同時実行性とバッチ サイズを調整できます。

-   [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)
-   [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)

オンライン アプリケーションへの影響を軽減するために、インデックス追加操作のデフォルトの速度は遅くなります。インデックス追加操作のターゲット列が読み取り負荷のみを伴う場合、またはオンライン ワークロードに直接関係しない場合は、上記の変数の値を適切に増やしてインデックス追加操作を高速化できます。

```sql
SET @@global.tidb_ddl_reorg_worker_cnt = 16;
SET @@global.tidb_ddl_reorg_batch_size = 4096;
```

インデックス追加操作のターゲット列が頻繁に更新される場合 ( `UPDATE` 、 `INSERT` 、 `DELETE`を含む)、上記の変数を増やすと書き込み競合が増加し、オンライン ワークロードに影響します。したがって、再試行が繰り返されるため、インデックスの追加操作が完了するまでに時間がかかる可能性があります。この場合、オンライン アプリケーションとの書き込み競合を避けるために、上記の変数の値を減らすことをお勧めします。

```sql
SET @@global.tidb_ddl_reorg_worker_cnt = 4;
SET @@global.tidb_ddl_reorg_batch_size = 128;
```

## トランザクションの競合 {#transaction-conflicts}

<CustomContent platform="tidb">

トランザクションの競合を特定して解決する方法については、 [ロックの競合のトラブルシューティング](/troubleshoot-lock-conflicts.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

トランザクションの競合を特定して解決する方法については、 [ロックの競合のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-lock-conflicts)を参照してください。

</CustomContent>

## TiDB を使用したJavaアプリケーション開発のベスト プラクティス {#best-practices-for-developing-java-applications-with-tidb}

<CustomContent platform="tidb">

[TiDB を使用したJavaアプリケーション開発のベスト プラクティス](/best-practices/java-app-best-practices.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[TiDB を使用したJavaアプリケーション開発のベスト プラクティス](https://docs.pingcap.com/tidb/stable/java-app-best-practices)を参照してください。

</CustomContent>

### こちらも参照 {#see-also}

<CustomContent platform="tidb">

-   [高度な同時書き込みのベスト プラクティス](/best-practices/high-concurrency-best-practices.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [高度な同時書き込みのベスト プラクティス](https://docs.pingcap.com/tidb/stable/high-concurrency-best-practices)

</CustomContent>
