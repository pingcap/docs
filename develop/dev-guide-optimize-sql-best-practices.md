---
title: Performance Tuning Best Practices
summary: TiDB パフォーマンスをチューニングするためのベスト プラクティスを紹介します。
aliases: ['/ja/tidb/stable/dev-guide-optimize-sql-best-practices/','/ja/tidbcloud/dev-guide-optimize-sql-best-practices/']
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

SQL ステートメントを複数回実行する必要がある場合は、SQL 構文を繰り返し解析することによるオーバーヘッドを回避するために、 `PREPARE`ステートメントを使用することをお勧めします。

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

`PREPARE`文を繰り返し実行しないでください。繰り返し実行すると、実行効率が向上しません。

### 必要な列のみをクエリする {#only-query-the-columns-you-need}

すべての列のデータが必要ない場合は、 `SELECT *`使用してすべての列のデータを取得しないでください。次のクエリは非効率的です。

```sql
SELECT * FROM books WHERE title = 'Marian Yost';
```

必要な列のみをクエリしてください。例:

```sql
SELECT title, price FROM books WHERE title = 'Marian Yost';
```

### 一括削除を使用する {#use-bulk-delete}

大量のデータを削除する場合は[一括削除](/develop/dev-guide-delete-data.md#bulk-delete)使用することをお勧めします。

### 一括更新を使用する {#use-bulk-update}

大量のデータを更新する場合は[一括更新](/develop/dev-guide-update-data.md#bulk-update)使用することをお勧めします。

### テーブルデータ全体を取得するには、 <code>DELETE</code>ではなく<code>TRUNCATE</code>使用します。 {#use-code-truncate-code-instead-of-code-delete-code-for-full-table-data}

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

[主キーを選択する際に従うべきルール](/develop/dev-guide-create-table.md#guidelines-to-follow-when-selecting-primary-key)を参照してください。

## インデックスのベストプラクティス {#index-best-practices}

[インデックスのベストプラクティス](/develop/dev-guide-index-best-practice.md)参照。

### インデックスのベストプラクティスを追加する {#add-index-best-practices}

TiDBはオンラインのインデックス追加操作をサポートしています。1 [インデックスを追加](/sql-statements/sql-statement-add-index.md)または[インデックスの作成](/sql-statements/sql-statement-create-index.md)文でインデックスを追加できます。テーブルへのデータの読み取りと書き込みはブロックされません。以下のシステム変数を変更することで、インデックス追加操作のフェーズ`re-organize`における同時実行性とバッチサイズを調整できます。

-   [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)
-   [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)

オンラインアプリケーションへの影響を軽減するため、インデックス追加操作のデフォルトの速度は低速に設定されています。インデックス追加操作の対象列が読み取り負荷のみ、またはオンラインワークロードに直接関連していない場合は、上記の変数の値を適切に増やすことで、インデックス追加操作を高速化できます。

```sql
SET @@global.tidb_ddl_reorg_worker_cnt = 16;
SET @@global.tidb_ddl_reorg_batch_size = 4096;
```

インデックス追加操作の対象列が頻繁に更新される場合（ `UPDATE` `DELETE` ）、上記の変数の値を増やすと書き込み競合が増加し、オンラインワークロードに影響を与えます。そのため、再試行`INSERT`頻繁に発生するため、インデックス追加操作の完了に時間がかかる可能性があります。このような場合は、オンラインアプリケーションとの書き込み競合を回避するために、上記の変数の値を減らすことをお勧めします。

```sql
SET @@global.tidb_ddl_reorg_worker_cnt = 4;
SET @@global.tidb_ddl_reorg_batch_size = 128;
```

## トランザクションの競合 {#transaction-conflicts}

トランザクションの競合を見つけて解決する方法については、 [ロック競合のトラブルシューティング](/troubleshoot-lock-conflicts.md)参照してください。

## TiDB を使用したJavaアプリケーション開発のベスト プラクティス {#best-practices-for-developing-java-applications-with-tidb}

[TiDB を使用したJavaアプリケーション開発のベスト プラクティス](/develop/java-app-best-practices.md)参照。

### 参照 {#see-also}

-   [高同時書き込みのベストプラクティス](/best-practices/high-concurrency-best-practices.md)

## ヘルプが必要ですか? {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに問い合わせてください。
-   [TiDB Cloudのサポートチケットを送信する](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDBセルフマネージドのサポートチケットを送信する](/support.md)
