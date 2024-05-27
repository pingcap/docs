---
title: Common Table Expression
summary: SQL ステートメントをより効率的に記述するのに役立つ TiDB の CTE 機能を学習します。
---

# 共通テーブル式 {#common-table-expression}

一部のトランザクション シナリオでは、アプリケーションの複雑さにより、最大 2,000 行の単一の SQL ステートメントを記述する必要がある場合があります。ステートメントには、多数の集計と複数レベルのサブクエリのネストが含まれる可能性があります。このような長い SQL ステートメントを維持することは、開発者にとって悪夢になる可能性があります。

このような長い SQL ステートメントを回避するには、 [ビュー](/develop/dev-guide-use-views.md)使用してクエリを簡略化するか、 [一時テーブル](/develop/dev-guide-use-temporary-tables.md)を使用して中間クエリ結果をキャッシュします。

このドキュメントでは、クエリ結果を再利用するためのより便利な方法である、TiDB の共通テーブル式 (CTE) 構文を紹介します。

TiDB v5.1 以降、TiDB は ANSI SQL99 標準の CTE と再帰をサポートしています。CTE を使用すると、複雑なアプリケーション ロジックの SQL ステートメントをより効率的に記述でき、コードの保守がはるかに簡単になります。

## 基本的な使い方 {#basic-use}

共通テーブル式 (CTE) は、SQL ステートメント内で複数回参照できる一時的な結果セットであり、ステートメントの読みやすさと実行効率を向上させます。CTE を使用するには、 [`WITH`](/sql-statements/sql-statement-with.md)ステートメントを適用できます。

共通テーブル式は、非再帰 CTE と再帰 CTE の 2 つのタイプに分類できます。

### 非再帰的 CTE {#non-recursive-cte}

非再帰 CTE は次の構文を使用して定義できます。

```sql
WITH <query_name> AS (
    <query_definition>
)
SELECT ... FROM <query_name>;
```

たとえば、最年長の著者 50 人がそれぞれ何冊の本を書いたかを知りたい場合は、次の手順を実行します。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

[一時テーブル](/develop/dev-guide-use-temporary-tables.md)の文を次のように変更します。

```sql
WITH top_50_eldest_authors_cte AS (
    SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
    FROM authors a
    ORDER BY age DESC
    LIMIT 50
)
SELECT
    ANY_VALUE(ta.id) AS author_id,
    ANY_VALUE(ta.age) AS author_age,
    ANY_VALUE(ta.name) AS author_name,
    COUNT(*) AS books
FROM top_50_eldest_authors_cte ta
LEFT JOIN book_authors ba ON ta.id = ba.author_id
GROUP BY ta.id;
```

結果は以下のようになります。

    +------------+------------+---------------------+-------+
    | author_id  | author_age | author_name         | books |
    +------------+------------+---------------------+-------+
    | 1238393239 |         80 | Araceli Purdy       |     1 |
    |  817764631 |         80 | Ivory Davis         |     3 |
    | 3093759193 |         80 | Lysanne Harris      |     1 |
    | 2299112019 |         80 | Ray Macejkovic      |     4 |
    ...
    +------------+------------+---------------------+-------+
    50 rows in set (0.01 sec)

</div>
<div label="Java" value = "java">

```java
public List<Author> getTop50EldestAuthorInfoByCTE() throws SQLException {
    List<Author> authors = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery("""
            WITH top_50_eldest_authors_cte AS (
                SELECT a.id, a.name, (IFNULL(a.death_year, YEAR(NOW())) - a.birth_year) AS age
                FROM authors a
                ORDER BY age DESC
                LIMIT 50
            )
            SELECT
                ANY_VALUE(ta.id) AS author_id,
                ANY_VALUE(ta.name) AS author_name,
                ANY_VALUE(ta.age) AS author_age,
                COUNT(*) AS books
            FROM top_50_eldest_authors_cte ta
            LEFT JOIN book_authors ba ON ta.id = ba.author_id
            GROUP BY ta.id;
        """);
        while (rs.next()) {
            Author author = new Author();
            author.setId(rs.getLong("author_id"));
            author.setName(rs.getString("author_name"));
            author.setAge(rs.getShort("author_age"));
            author.setBooks(rs.getInt("books"));
            authors.add(author);
        }
    }
    return authors;
}
```

</div>
</SimpleTab>

著者「Ray Macejkovic」は 4 冊の本を執筆したことがわかります。CTE クエリを使用すると、次のようにして、これら 4 冊の本の順序と評価情報をさらに取得できます。

```sql
WITH books_authored_by_rm AS (
    SELECT *
    FROM books b
    LEFT JOIN book_authors ba ON b.id = ba.book_id
    WHERE author_id = 2299112019
), books_with_average_ratings AS (
    SELECT
        b.id AS book_id,
        AVG(r.score) AS average_rating
    FROM books_authored_by_rm b
    LEFT JOIN ratings r ON b.id = r.book_id
    GROUP BY b.id
), books_with_orders AS (
    SELECT
        b.id AS book_id,
        COUNT(*) AS orders
    FROM books_authored_by_rm b
    LEFT JOIN orders o ON b.id = o.book_id
    GROUP BY b.id
)
SELECT
    b.id AS `book_id`,
    b.title AS `book_title`,
    br.average_rating AS `average_rating`,
    bo.orders AS `orders`
FROM
    books_authored_by_rm b
    LEFT JOIN books_with_average_ratings br ON b.id = br.book_id
    LEFT JOIN books_with_orders bo ON b.id = bo.book_id
;
```

結果は以下のようになります。

    +------------+-------------------------+----------------+--------+
    | book_id    | book_title              | average_rating | orders |
    +------------+-------------------------+----------------+--------+
    |  481008467 | The Documentary of goat |         2.0000 |     16 |
    | 2224531102 | Brandt Skiles           |         2.7143 |     17 |
    | 2641301356 | Sheridan Bashirian      |         2.4211 |     12 |
    | 4154439164 | Karson Streich          |         2.5833 |     19 |
    +------------+-------------------------+----------------+--------+
    4 rows in set (0.06 sec)

この SQL ステートメントでは、 `,`で区切られた 3 つの CTE ブロックが定義されています。

まず、CTE ブロック`books_authored_by_rm`で著者 (ID は`2299112019` ) が書いた本を調べます。次に、 `books_with_average_ratings`と`books_with_orders`でこれらの本の平均評価と順位をそれぞれ調べます。最後に、 `JOIN`ステートメントで結果を集計します。

`books_authored_by_rm`のクエリは 1 回だけ実行され、その後 TiDB はその結果をキャッシュするための一時領域を作成することに注意してください。 `books_with_average_ratings`と`books_with_orders`のクエリが`books_authored_by_rm`を参照する場合、TiDB はこの一時領域から直接結果を取得します。

> **ヒント：**
>
> デフォルトの CTE クエリの効率が良くない場合は、ヒント[`MERGE()`](/optimizer-hints.md#merge)を使用して CTE サブクエリを外部クエリに拡張し、効率を向上させることができます。

### 再帰CTE {#recursive-cte}

再帰 CTE は次の構文を使用して定義できます。

```sql
WITH RECURSIVE <query_name> AS (
    <query_definition>
)
SELECT ... FROM <query_name>;
```

典型的な例は、再帰 CTE を使用して[フィボナッチ数列](https://en.wikipedia.org/wiki/Fibonacci_number)のセットを生成することです。

```sql
WITH RECURSIVE fibonacci (n, fib_n, next_fib_n) AS
(
  SELECT 1, 0, 1
  UNION ALL
  SELECT n + 1, next_fib_n, fib_n + next_fib_n FROM fibonacci WHERE n < 10
)
SELECT * FROM fibonacci;
```

結果は以下のようになります。

    +------+-------+------------+
    | n    | fib_n | next_fib_n |
    +------+-------+------------+
    |    1 |     0 |          1 |
    |    2 |     1 |          1 |
    |    3 |     1 |          2 |
    |    4 |     2 |          3 |
    |    5 |     3 |          5 |
    |    6 |     5 |          8 |
    |    7 |     8 |         13 |
    |    8 |    13 |         21 |
    |    9 |    21 |         34 |
    |   10 |    34 |         55 |
    +------+-------+------------+
    10 rows in set (0.00 sec)

## 続きを読む {#read-more}

-   [と](/sql-statements/sql-statement-with.md)
