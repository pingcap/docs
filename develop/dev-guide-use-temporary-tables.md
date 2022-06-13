---
title: Temporary Tables
summary: Learn how to create, view, query, and delete temporary tables.
---

# 一時テーブル {#temporary-tables}

一時テーブルは、クエリ結果を再利用するための手法と考えることができます。

[書店](/develop/dev-guide-bookshop-schema-design.md)のアプリケーションの最年長の著者について何か知りたい場合は、最年長の著者のリストを使用する複数のクエリを作成できます。

たとえば、次のステートメントを使用して、 `authors`のテーブルから上位50人の最年長の著者を取得できます。

{{< copyable "" >}}

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

後続のクエリの便宜のために、このクエリの結果をキャッシュする必要があります。ストレージに一般テーブルを使用する場合、これらのテーブルはバッチクエリの後で使用されない可能性があるため、異なるセッション間でのテーブル名の重複の問題を回避する方法と、中間結果を時間内にクリーンアップする必要があることに注意する必要があります。

## 一時テーブルを作成する {#create-a-temporary-table}

中間結果をキャッシュするために、一時テーブル機能がTiDBv5.3.0に導入されました。 TiDBは、セッションの終了後にローカルの一時テーブルを自動的に削除します。これにより、中間結果の増加によって引き起こされる管理上の問題について心配する必要がなくなります。

### 一時テーブルの種類 {#types-of-temporary-tables}

TiDBの一時テーブルは、ローカル一時テーブルとグローバル一時テーブルの2つのタイプに分けられます。

-   ローカル一時テーブルの場合、テーブル定義とテーブル内のデータは、現在のセッションにのみ表示されます。このタイプは、セッションに中間データを一時的に保存するのに適しています。
-   グローバル一時テーブルの場合、テーブル定義はTiDBクラスタ全体に表示され、テーブル内のデータは現在のトランザクションにのみ表示されます。このタイプは、トランザクションで中間データを一時的に保存するのに適しています。

### ローカル一時テーブルを作成する {#create-a-local-temporary-table}

ローカル一時テーブルを作成する前に、現在のデータベースユーザーに`CREATE TEMPORARY TABLES`の権限を追加する必要があります。

<SimpleTab>
<div label="SQL" href="local-sql">

`CREATE TEMPORARY TABLE <table_name>`ステートメントを使用して一時テーブルを作成できます。デフォルトのタイプはローカル一時テーブルで、現在のセッションにのみ表示されます。

{{< copyable "" >}}

```sql
CREATE TEMPORARY TABLE top_50_eldest_authors (
    id BIGINT,
    name VARCHAR(255),
    age INT,
    PRIMARY KEY(id)
);
```

一時テーブルを作成したら、 `INSERT INTO table_name SELECT ...`ステートメントを使用して、上記のクエリの結果を作成した一時テーブルに挿入できます。

{{< copyable "" >}}

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
<div label="Java" href="local-java">

{{< copyable "" >}}

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

<SimpleTab>
<div label="SQL" href="global-sql">

グローバル一時テーブルを作成するには、 `GLOBAL`キーワードを追加し、 `ON COMMIT DELETE ROWS`で終了します。これは、現在のトランザクションが終了した後にテーブルが削除されることを意味します。

{{< copyable "" >}}

```sql
CREATE GLOBAL TEMPORARY TABLE IF NOT EXISTS top_50_eldest_authors_global (
    id BIGINT,
    name VARCHAR(255),
    age INT,
    PRIMARY KEY(id)
) ON COMMIT DELETE ROWS;
```

グローバル一時テーブルにデータを挿入するときは、 `BEGIN`を介してトランザクションの開始を明示的に宣言する必要があります。それ以外の場合は、 `INSERT INTO`ステートメントの実行後にデータがクリアされます。自動コミットモードでは、 `INSERT INTO`ステートメントの実行後にトランザクションが自動的にコミットされ、トランザクションが終了するとグローバル一時テーブルがクリアされるためです。

</div>
<div label="Java" href="global-java">

グローバル一時テーブルを使用する場合は、最初に自動コミットモードをオフにする必要があります。 Javaでは、これは`conn.setAutoCommit(false);`ステートメントで実行でき、トランザクションは`conn.commit();`で明示的にコミットできます。トランザクション中にグローバル一時テーブルに追加されたデータは、トランザクションがコミットまたはキャンセルされた後にクリアされます。

{{< copyable "" >}}

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

## 一時テーブルを表示する {#view-temporary-tables}

`SHOW [FULL] TABLES`ステートメントを使用すると、既存のグローバル一時テーブルのリストを表示できますが、リストにローカル一時テーブルを表示することはできません。現在のところ、TiDBには、一時テーブル情報を格納するための同様の`information_schema.INNODB_TEMP_TABLE_INFO`システムテーブルがありません。

たとえば、グローバル一時テーブル`top_50_eldest_authors_global`はテーブルリストに表示されますが、 `top_50_eldest_authors`テーブルは表示されません。

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

## 一時テーブルをクエリする {#query-a-temporary-table}

一時テーブルの準備ができたら、通常のデータテーブルとしてクエリを実行できます。

{{< copyable "" >}}

```sql
SELECT * FROM top_50_eldest_authors;
```

[マルチテーブル結合クエリ](/develop/dev-guide-join-tables.md)を介して、一時テーブルからクエリにデータを参照できます。

{{< copyable "" >}}

```sql
EXPLAIN SELECT ANY_VALUE(ta.id) AS author_id, ANY_VALUE(ta.age), ANY_VALUE(ta.name), COUNT(*) AS books
FROM top_50_eldest_authors ta
LEFT JOIN book_authors ba ON ta.id = ba.author_id
GROUP BY ta.id;
```

[見る](/develop/dev-guide-use-views.md)とは異なり、一時テーブルをクエリすると、データ挿入で使用された元のクエリを実行する代わりに、一時テーブルから直接データが取得されます。場合によっては、これによりクエリのパフォーマンスが向上することがあります。

## 一時テーブルを削除します {#drop-a-temporary-table}

セッション内のローカル一時テーブルは、データとテーブルスキーマの両方とともに、**セッション**の終了後に自動的に削除されます。トランザクション内のグローバル一時テーブルは、<strong>トランザクション</strong>の終了時に自動的にクリアされますが、テーブルスキーマは残り、手動で削除する必要があります。

ローカル一時テーブルを手動で削除するには、 `DROP TABLE`または`DROP TEMPORARY TABLE`構文を使用します。例えば：

{{< copyable "" >}}

```sql
DROP TEMPORARY TABLE top_50_eldest_authors;
```

グローバル一時テーブルを手動で削除するには、 `DROP TABLE`または`DROP GLOBAL TEMPORARY TABLE`構文を使用します。例えば：

{{< copyable "" >}}

```sql
DROP GLOBAL TEMPORARY TABLE top_50_eldest_authors_global;
```

## 制限 {#limitation}

TiDBの一時テーブルの制限については、 [他のTiDB機能との互換性の制限](/temporary-tables.md#compatibility-restrictions-with-other-tidb-features)を参照してください。

## 続きを読む {#read-more}

-   [一時テーブル](/temporary-tables.md)
