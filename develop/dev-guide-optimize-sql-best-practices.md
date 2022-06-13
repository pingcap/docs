---
title: Performance Tuning Best Practices
summary: Introduces the best practices for tuning TiDB performance.
---

# 性能チューニングのベストプラクティス {#performance-tuning-best-practices}

このドキュメントでは、TiDBデータベースを使用するためのいくつかのベストプラクティスを紹介します。

## DMLのベストプラクティス {#dml-best-practices}

このセクションでは、TiDBでDMLを使用する場合のベストプラクティスについて説明します。

### 複数行のステートメントを使用する {#use-multi-row-statements}

テーブルの複数の行を変更する必要がある場合は、複数行のステートメントを使用することをお勧めします。

{{< copyable "" >}}

```sql
INSERT INTO t VALUES (1, 'a'), (2, 'b'), (3, 'c');

DELETE FROM t WHERE id IN (1, 2, 3);
```

複数の単一行ステートメントを使用することはお勧めしません。

{{< copyable "" >}}

```sql
INSERT INTO t VALUES (1, 'a');
INSERT INTO t VALUES (2, 'b');
INSERT INTO t VALUES (3, 'c');

DELETE FROM t WHERE id = 1;
DELETE FROM t WHERE id = 2;
DELETE FROM t WHERE id = 3;
```

### <code>PREPARE</code>を使用する {#use-code-prepare-code}

SQLステートメントを複数回実行する必要がある場合は、SQL構文を繰り返し解析するオーバーヘッドを回避するために、 `PREPARE`ステートメントを使用することをお勧めします。

<SimpleTab>
<div label="Golang">

{{< copyable "" >}}

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

{{< copyable "" >}}

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

`PREPARE`ステートメントを繰り返し実行しないでください。そうしないと、実行効率を向上させることができません。

### 必要な列のみをクエリする {#only-query-the-columns-you-need}

すべての列のデータが必要ない場合は、 `SELECT *`を使用してすべての列のデータを返さないでください。次のクエリは非効率的です。

{{< copyable "" >}}

```sql
SELECT * FROM books WHERE title = 'Marian Yost';
```

必要な列のみを照会する必要があります。例えば：

{{< copyable "" >}}

```sql
SELECT title, price FROM books WHERE title = 'Marian Yost';
```

### 一括削除を使用する {#use-bulk-delete}

大量のデータを削除する場合は、 [一括削除](/develop/dev-guide-delete-data.md#bulk-delete)を使用することをお勧めします。

### 一括更新を使用する {#use-bulk-update}

大量のデータを更新する場合は、 [一括更新](/develop/dev-guide-update-data.md#bulk-update)を使用することをお勧めします。

### 完全なテーブルデータには、 <code>DELETE</code>ではなく<code>TRUNCATE</code>を使用します {#use-code-truncate-code-instead-of-code-delete-code-for-full-table-data}

テーブルからすべてのデータを削除する必要がある場合は、次の`TRUNCATE`ステートメントを使用することをお勧めします。

{{< copyable "" >}}

```sql
TRUNCATE TABLE t;
```

完全なテーブルデータに`DELETE`を使用することはお勧めしません。

{{< copyable "" >}}

```sql
DELETE FROM t;
```

## DDLのベストプラクティス {#ddl-best-practices}

このセクションでは、TiDBのDDLを使用する際のベストプラクティスについて説明します。

### 主キーのベストプラクティス {#primary-key-best-practices}

[主キーを選択するときに従うべきルール](/develop/dev-guide-create-table.md#guidelines-to-follow-when-selecting-primary-key)を参照してください。

## インデックスのベストプラクティス {#index-best-practices}

[インデックスのベストプラクティス](/develop/dev-guide-index-best-practice.md)を参照してください。

### <code>ADD INDEX</code>の追加のベストプラクティス {#code-add-index-code-best-practices}

TiDBはオンライン`ADD INDEX`操作をサポートし、テーブル内のデータの読み取りと書き込みをブロックしません。次のシステム変数を変更することにより、 `ADD INDEX`の速度を調整できます。

-   [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)
-   [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)

オンラインアプリケーションへの影響を減らすために、デフォルトの速度`ADD INDEX`は遅いです。 `ADD INDEX`のターゲット列に読み取り負荷のみが含まれる場合、またはオンラインワークロードに直接関連しない場合は、上記の変数の値を適切に増やして、 `ADD INDEX`の操作を高速化できます。

{{< copyable "" >}}

```sql
SET @@global.tidb_ddl_reorg_worker_cnt = 16;
SET @@global.tidb_ddl_reorg_batch_size = 4096;
```

`ADD INDEX`のターゲット列が頻繁に更新される場合（ `UPDATE` 、および`INSERT`を含む）、上記の変数を増やすと、書き込みの競合が増え、オンラインワークロードに影響を与え`DELETE` 。したがって、 `ADD INDEX`は再試行が繰り返されるため、完了するまでに長い時間がかかる場合があります。この場合、オンラインアプリケーションとの書き込みの競合を避けるために、上記の変数の値を減らすことをお勧めします。

{{< copyable "" >}}

```sql
SET @@global.tidb_ddl_reorg_worker_cnt = 4;
SET @@global.tidb_ddl_reorg_batch_size = 128;
```

## トランザクションの競合 {#transaction-conflicts}

トランザクションの競合を見つけて解決する方法については、 [ロックの競合のトラブルシューティング](/troubleshoot-lock-conflicts.md)を参照してください。

## TiDBを使用してJavaアプリケーションを開発するためのベストプラクティス {#best-practices-for-developing-java-applications-with-tidb}

[TiDBを使用してJavaアプリケーションを開発するためのベストプラクティス](/best-practices/java-app-best-practices.md)を参照してください。

### も参照してください {#see-also}

-   [非常に同時の書き込みのベストプラクティス](/best-practices/high-concurrency-best-practices.md)
