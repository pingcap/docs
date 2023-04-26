---
title: Temporary Tables
summary: Learn how to create, view, query, and delete temporary tables.
---

# 一時テーブル {#temporary-tables}

一時テーブルは、クエリ結果を再利用するための手法と考えることができます。

[書店](/develop/dev-guide-bookshop-schema-design.md)アプリケーションで最年長の著者について知りたい場合は、最年長の著者のリストを使用する複数のクエリを作成できます。

たとえば、次のステートメントを使用して、テーブル`authors`から最年長の上位 50 名の著者を取得できます。

```sql
SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
FROM authors a
ORDER BY age DESC
LIMIT 50;
```

結果は次のとおりです。

```
+------------+---------------------+------+
| id         | name                | age  |
+------------+---------------------+------+
| 4053452056 | Dessie Thompson     |   80 |
| 2773958689 | Pedro Hansen        |   80 |
| 4005636688 | Wyatt Keeling       |   80 |
| 3621155838 | Colby Parker        |   80 |
| 2738876051 | Friedrich Hagenes   |   80 |
| 2299112019 | Ray Macejkovic      |   80 |
| 3953661843 | Brandi Williamson   |   80 |
...
| 4100546410 | Maida Walsh         |   80 |
+------------+---------------------+------+
50 rows in set (0.01 sec)
```

後続のクエリの便宜のために、このクエリの結果をキャッシュする必要があります。storageに汎用テーブルを使用する場合、異なるセッション間でテーブル名が重複する問題を回避する方法と、中間結果を時間内にクリーンアップする必要があることに注意する必要があります。これらのテーブルはバッチ クエリの後で使用されない可能性があるためです。

## 一時テーブルを作成する {#create-a-temporary-table}

中間結果をキャッシュするために、一時テーブル機能が TiDB v5.3.0 で導入されました。 TiDB は、セッション終了後にローカル一時テーブルを自動的に削除します。これにより、中間結果の増加による管理上の問題を心配する必要がなくなります。

### 一時テーブルの種類 {#types-of-temporary-tables}

TiDB の一時テーブルは、ローカル一時テーブルとグローバル一時テーブルの 2 種類に分けられます。

-   ローカル一時テーブルの場合、テーブルの定義とテーブル内のデータは、現在のセッションにのみ表示されます。このタイプは、セッション内の中間データを一時的に格納するのに適しています。
-   グローバル一時テーブルの場合、テーブル定義は TiDB クラスター全体に表示され、テーブル内のデータは現在のトランザクションにのみ表示されます。このタイプは、トランザクションの中間データを一時的に格納するのに適しています。

### ローカル一時テーブルを作成する {#create-a-local-temporary-table}

ローカル一時テーブルを作成する前に、現在のデータベース ユーザーに権限を`CREATE TEMPORARY TABLES`追加する必要があります。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

`CREATE TEMPORARY TABLE <table_name>`ステートメントを使用して一時テーブルを作成できます。デフォルトのタイプは、現在のセッションにのみ表示されるローカル一時テーブルです。

```sql
CREATE TEMPORARY TABLE top_50_eldest_authors (
    id BIGINT,
    name VARCHAR(255),
    age INT,
    PRIMARY KEY(id)
);
```

一時テーブルを作成したら、 `INSERT INTO table_name SELECT ...`ステートメントを使用して、上記のクエリの結果を作成したばかりの一時テーブルに挿入できます。

```sql
INSERT INTO top_50_eldest_authors
SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
FROM authors a
ORDER BY age DESC
LIMIT 50;
```

結果は次のとおりです。

```
Query OK, 50 rows affected (0.03 sec)
Records: 50  Duplicates: 0  Warnings: 0
```

</div>
<div label="Java" value="java">

```java
public List<Author> getTop50EldestAuthorInfo() throws SQLException {
    List<Author> authors = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        Statement stmt = conn.createStatement();
        stmt.executeUpdate("""
            CREATE TEMPORARY TABLE top_50_eldest_authors (
                id BIGINT,
                name VARCHAR(255),
                age INT,
                PRIMARY KEY(id)
            );
        """);

        stmt.executeUpdate("""
            INSERT INTO top_50_eldest_authors
            SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
            FROM authors a
            ORDER BY age DESC
            LIMIT 50;
        """);

        ResultSet rs = stmt.executeQuery("""
            SELECT id, name FROM top_50_eldest_authors;
        """);

        while (rs.next()) {
            Author author = new Author();
            author.setId(rs.getLong("id"));
            author.setName(rs.getString("name"));
            authors.add(author);
        }
    }
    return authors;
}
```

</div>
</SimpleTab>

### グローバル一時テーブルを作成する {#create-a-global-temporary-table}

<SimpleTab groupId="language">
<div label="SQL" value="sql">

グローバル一時テーブルを作成するには、 `GLOBAL`キーワードを追加して`ON COMMIT DELETE ROWS`で終了します。これは、現在のトランザクションの終了後にテーブルが削除されることを意味します。

```sql
CREATE GLOBAL TEMPORARY TABLE IF NOT EXISTS top_50_eldest_authors_global (
    id BIGINT,
    name VARCHAR(255),
    age INT,
    PRIMARY KEY(id)
) ON COMMIT DELETE ROWS;
```

グローバル一時テーブルにデータを挿入する場合、トランザクションの開始を`BEGIN`で明示的に宣言する必要があります。そうしないと、 `INSERT INTO`ステートメントの実行後にデータがクリアされます。自動コミット モードでは、 `INSERT INTO`ステートメントの実行後にトランザクションが自動的にコミットされ、トランザクションが終了するとグローバル一時テーブルがクリアされるためです。

</div>
<div label="Java" value="java">

グローバル一時テーブルを使用する場合は、最初に自動コミット モードをオフにする必要があります。 Javaでは、これを`conn.setAutoCommit(false);`ステートメントで実行でき、トランザクションを`conn.commit();`で明示的にコミットできます。トランザクション中にグローバル一時テーブルに追加されたデータは、トランザクションがコミットまたはキャンセルされた後にクリアされます。

```java
public List<Author> getTop50EldestAuthorInfo() throws SQLException {
    List<Author> authors = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        conn.setAutoCommit(false);

        Statement stmt = conn.createStatement();
        stmt.executeUpdate("""
            CREATE GLOBAL TEMPORARY TABLE IF NOT EXISTS top_50_eldest_authors (
                id BIGINT,
                name VARCHAR(255),
                age INT,
                PRIMARY KEY(id)
            ) ON COMMIT DELETE ROWS;
        """);

        stmt.executeUpdate("""
            INSERT INTO top_50_eldest_authors
            SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
            FROM authors a
            ORDER BY age DESC
            LIMIT 50;
        """);

        ResultSet rs = stmt.executeQuery("""
            SELECT id, name FROM top_50_eldest_authors;
        """);

        conn.commit();
        while (rs.next()) {
            Author author = new Author();
            author.setId(rs.getLong("id"));
            author.setName(rs.getString("name"));
            authors.add(author);
        }
    }
    return authors;
}
```

</div>
</SimpleTab>

## 一時テーブルをビュー {#view-temporary-tables}

`SHOW [FULL] TABLES`ステートメントを使用すると、既存のグローバル一時テーブルのリストを表示できますが、リストにローカル一時テーブルは表示されません。今のところ、TiDB には、一時テーブル情報を格納するための同様の`information_schema.INNODB_TEMP_TABLE_INFO`システム テーブルがありません。

たとえば、グローバル一時テーブル`top_50_eldest_authors_global`はテーブル リストに表示されますが、 `top_50_eldest_authors`テーブルは表示されません。

```
+-------------------------------+------------+
| Tables_in_bookshop            | Table_type |
+-------------------------------+------------+
| authors                       | BASE TABLE |
| book_authors                  | BASE TABLE |
| books                         | BASE TABLE |
| orders                        | BASE TABLE |
| ratings                       | BASE TABLE |
| top_50_eldest_authors_global  | BASE TABLE |
| users                         | BASE TABLE |
+-------------------------------+------------+
9 rows in set (0.00 sec)
```

## 一時テーブルのクエリ {#query-a-temporary-table}

一時テーブルの準備ができたら、通常のデータ テーブルとしてクエリを実行できます。

```sql
SELECT * FROM top_50_eldest_authors;
```

[複数テーブルの結合クエリ](/develop/dev-guide-join-tables.md)を介して、一時テーブルからクエリへのデータを参照できます。

```sql
EXPLAIN SELECT ANY_VALUE(ta.id) AS author_id, ANY_VALUE(ta.age), ANY_VALUE(ta.name), COUNT(*) AS books
FROM top_50_eldest_authors ta
LEFT JOIN book_authors ba ON ta.id = ba.author_id
GROUP BY ta.id;
```

[意見](/develop/dev-guide-use-views.md)とは異なり、一時テーブルをクエリすると、データ挿入で使用された元のクエリを実行する代わりに、一時テーブルから直接データが取得されます。場合によっては、これによりクエリのパフォーマンスが向上する可能性があります。

## 一時テーブルをドロップする {#drop-a-temporary-table}

セッションのローカル一時テーブルは、**セッションの**終了後に、データとテーブル スキーマの両方と共に自動的に削除されます。トランザクション内のグローバル一時テーブルは、<strong>トランザクション</strong>の終了時に自動的にクリアされますが、テーブル スキーマは残っているため、手動で削除する必要があります。

ローカル一時テーブルを手動で削除するには、 `DROP TABLE`または`DROP TEMPORARY TABLE`構文を使用します。例えば：

```sql
DROP TEMPORARY TABLE top_50_eldest_authors;
```

グローバル一時テーブルを手動で削除するには、 `DROP TABLE`または`DROP GLOBAL TEMPORARY TABLE`構文を使用します。例えば：

```sql
DROP GLOBAL TEMPORARY TABLE top_50_eldest_authors_global;
```

## 制限 {#limitation}

TiDB の一時テーブルの制限については、 [他の TiDB 機能との互換性の制限](/temporary-tables.md#compatibility-restrictions-with-other-tidb-features)を参照してください。

## 続きを読む {#read-more}

-   [一時テーブル](/temporary-tables.md)
