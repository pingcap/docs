---
title: Multi-table Join Queries
summary: This document describes how to use multi-table join queries.
---

# 複数テーブル結合クエリ {#multi-table-join-queries}

多くのシナリオでは、1 つのクエリを使用して複数のテーブルからデータを取得する必要があります。 `JOIN`ステートメントを使用して、2 つ以上のテーブルのデータを結合できます。

## 結合タイプ {#join-types}

このセクションでは、結合タイプについて詳しく説明します。

### 内部結合 {#inner-join}

内部結合の結合結果は、結合条件に一致する行のみを返します。

![Inner Join](/media/develop/inner-join.png)

たとえば、最も多作な著者を知りたい場合は、 `authors`という名前の著者テーブルと`book_authors`名前の本の著者テーブルを結合する必要があります。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

次の SQL ステートメントでは、キーワード`JOIN`を使用して、左側のテーブル`authors`と右側のテーブル`book_authors`の行を、結合条件`a.id = ba.author_id`を使用した内部結合として結合することを宣言します。結果セットには、結合条件を満たす行のみが含まれます。著者が本を書いていない場合、 `authors`テーブル内のその著者のレコードは結合条件を満たさないため、結果セットには表示されません。

```sql
SELECT ANY_VALUE(a.id) AS author_id, ANY_VALUE(a.name) AS author_name, COUNT(ba.book_id) AS books
FROM authors a
JOIN book_authors ba ON a.id = ba.author_id
GROUP BY ba.author_id
ORDER BY books DESC
LIMIT 10;
```

クエリ結果は次のとおりです。

    +------------+----------------+-------+
    | author_id  | author_name    | books |
    +------------+----------------+-------+
    |  431192671 | Emilie Cassin  |     7 |
    |  865305676 | Nola Howell    |     7 |
    |  572207928 | Lamar Koch     |     6 |
    | 3894029860 | Elijah Howe    |     6 |
    | 1150614082 | Cristal Stehr  |     6 |
    | 4158341032 | Roslyn Rippin  |     6 |
    | 2430691560 | Francisca Hahn |     6 |
    | 3346415350 | Leta Weimann   |     6 |
    | 1395124973 | Albin Cole     |     6 |
    | 2768150724 | Caleb Wyman    |     6 |
    +------------+----------------+-------+
    10 rows in set (0.01 sec)

</div>
<div label="Java" value="java">

```java
public List<Author> getTop10AuthorsOrderByBooks() throws SQLException {
    List<Author> authors = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery("""
        SELECT ANY_VALUE(a.id) AS author_id, ANY_VALUE(a.name) AS author_name, COUNT(ba.book_id) AS books
        FROM authors a
        JOIN book_authors ba ON a.id = ba.author_id
        GROUP BY ba.author_id
        ORDER BY books DESC
        LIMIT 10;
        """);
        while (rs.next()) {
            Author author = new Author();
            author.setId(rs.getLong("author_id"));
            author.setName(rs.getString("author_name"));
            author.setBooks(rs.getInt("books"));
            authors.add(author);
        }
    }
    return authors;
}
```

</div>
</SimpleTab>

### 左外部結合 {#left-outer-join}

左外部結合は、結合条件に一致する左側のテーブルのすべての行と右側のテーブルの値を返します。右側のテーブルに一致する行がない場合は、 `NULL`が入力されます。

![Left Outer Join](/media/develop/left-outer-join.png)

場合によっては、複数のテーブルを使用してデータ クエリを完了したいが、結合条件が満たされないためにデータ セットが小さくなりすぎないようにする必要があります。

たとえば、Bookshop アプリのホームページに、平均評価の新しい書籍のリストを表示するとします。この場合、新しい本はまだ誰も評価されていない可能性があります。内部結合を使用すると、これらの評価されていない書籍の情報がフィルターで除外されますが、これは期待どおりではありません。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

次の SQL ステートメントでは、 `LEFT JOIN`キーワードを使用して、左のテーブル`books`左外部結合で右のテーブル`ratings`に結合されることを宣言します。これにより、テーブル`books`のすべての行が返されるようになります。

```sql
SELECT b.id AS book_id, ANY_VALUE(b.title) AS book_title, AVG(r.score) AS average_score
FROM books b
LEFT JOIN ratings r ON b.id = r.book_id
GROUP BY b.id
ORDER BY b.published_at DESC
LIMIT 10;
```

クエリ結果は次のとおりです。

    +------------+---------------------------------+---------------+
    | book_id    | book_title                      | average_score |
    +------------+---------------------------------+---------------+
    | 3438991610 | The Documentary of lion         |        2.7619 |
    | 3897175886 | Torey Kuhn                      |        3.0000 |
    | 1256171496 | Elmo Vandervort                 |        2.5500 |
    | 1036915727 | The Story of Munchkin           |        2.0000 |
    |  270254583 | Tate Kovacek                    |        2.5000 |
    | 1280950719 | Carson Damore                   |        3.2105 |
    | 1098041838 | The Documentary of grasshopper  |        2.8462 |
    | 1476566306 | The Adventures of Vince Sanford |        2.3529 |
    | 4036300890 | The Documentary of turtle       |        2.4545 |
    | 1299849448 | Antwan Olson                    |        3.0000 |
    +------------+---------------------------------+---------------+
    10 rows in set (0.30 sec)

最新刊はすでにかなりの評価を得ているようです。上記の方法を検証するために、SQL ステートメントを使用して書籍*「The Documentary of lion* 」のすべての評価を削除してみましょう。

```sql
DELETE FROM ratings WHERE book_id = 3438991610;
```

もう一度問い合わせてください。 *「The Documentary of lion」*という本は引き続き結果セットに表示されますが、右側のテーブル`ratings`の`score`から計算された`average_score`列には`NULL`が入力されます。

    +------------+---------------------------------+---------------+
    | book_id    | book_title                      | average_score |
    +------------+---------------------------------+---------------+
    | 3438991610 | The Documentary of lion         |          NULL |
    | 3897175886 | Torey Kuhn                      |        3.0000 |
    | 1256171496 | Elmo Vandervort                 |        2.5500 |
    | 1036915727 | The Story of Munchkin           |        2.0000 |
    |  270254583 | Tate Kovacek                    |        2.5000 |
    | 1280950719 | Carson Damore                   |        3.2105 |
    | 1098041838 | The Documentary of grasshopper  |        2.8462 |
    | 1476566306 | The Adventures of Vince Sanford |        2.3529 |
    | 4036300890 | The Documentary of turtle       |        2.4545 |
    | 1299849448 | Antwan Olson                    |        3.0000 |
    +------------+---------------------------------+---------------+
    10 rows in set (0.30 sec)

`INNER JOIN`を使用するとどうなりますか?試してみるかどうかはあなた次第です。

</div>
<div label="Java" value="java">

```java
public List<Book> getLatestBooksWithAverageScore() throws SQLException {
    List<Book> books = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery("""
        SELECT b.id AS book_id, ANY_VALUE(b.title) AS book_title, AVG(r.score) AS average_score
        FROM books b
        LEFT JOIN ratings r ON b.id = r.book_id
        GROUP BY b.id
        ORDER BY b.published_at DESC
        LIMIT 10;
        """);
        while (rs.next()) {
            Book book = new Book();
            book.setId(rs.getLong("book_id"));
            book.setTitle(rs.getString("book_title"));
            book.setAverageScore(rs.getFloat("average_score"));
            books.add(book);
        }
    }
    return books;
}
```

</div>
</SimpleTab>

### 右外部結合 {#right-outer-join}

右外部結合は、右側のテーブルのすべてのレコードと、結合条件に一致する左側のテーブルの値を返します。一致する値がない場合は、 `NULL`が埋められます。

![Right Outer Join](/media/develop/right-outer-join.png)

### クロスジョイン {#cross-join}

結合条件が定数の場合、2 つのテーブル間の内部結合は[クロス結合](https://en.wikipedia.org/wiki/Join_(SQL)#Cross_join)と呼ばれます。クロス結合は、左側のテーブルのすべてのレコードを右側のテーブルのすべてのレコードに結合します。左側のテーブルのレコード数が`m`で、右側のテーブルのレコード数が`n`の場合、結果セットには`m \* n`レコードが生成されます。

### 左セミ結合 {#left-semi-join}

TiDB は SQL 構文レベルで`LEFT SEMI JOIN table_name`をサポートしません。ただし、実行計画レベルでは、 [サブクエリ関連の最適化](/subquery-optimization.md)書き換えられた同等の JOIN クエリのデフォルトの結合方法として`semi join`を使用します。

## 暗黙的な結合 {#implicit-join}

結合を明示的に宣言する`JOIN`ステートメントが SQL 標準に追加される前は、 `FROM t1, t2`句を使用して SQL ステートメント内で 2 つ以上のテーブルを結合し、 `WHERE t1.id = t2.id`句を使用して結合の条件を指定することができました。これは、内部結合を使用してテーブルを結合する暗黙的な結合として理解できます。

## 関連するアルゴリズムに参加する {#join-related-algorithms}

TiDB は、次の一般的なテーブル結合アルゴリズムをサポートしています。

-   [インデックス結合](/explain-joins.md#index-join)
-   [ハッシュ結合](/explain-joins.md#hash-join)
-   [マージ結合](/explain-joins.md#merge-join)

オプティマイザは、結合テーブル内のデータ量などの要因に基づいて、実行する適切な結合アルゴリズムを選択します。 `EXPLAIN`ステートメントを使用すると、クエリが結合にどのアルゴリズムを使用しているかを確認できます。

TiDB のオプティマイザが最適な結合アルゴリズムに従って実行されない場合は、 [オプティマイザーのヒント](/optimizer-hints.md)を使用して TiDB により適切な結合アルゴリズムを使用させることができます。

たとえば、オプティマイザによって選択されていないハッシュ結合アルゴリズムを使用すると、上記の左結合クエリの例がより高速に実行されると仮定すると、キーワード`SELECT`の後にヒント`/*+ HASH_JOIN(b, r) */`追加できます。テーブルに別名がある場合は、ヒントでその別名を使用することに注意してください。

```sql
EXPLAIN SELECT /*+ HASH_JOIN(b, r) */ b.id AS book_id, ANY_VALUE(b.title) AS book_title, AVG(r.score) AS average_score
FROM books b
LEFT JOIN ratings r ON b.id = r.book_id
GROUP BY b.id
ORDER BY b.published_at DESC
LIMIT 10;
```

結合アルゴリズムに関するヒント:

-   [MERGE_JOIN(t1_name [, tl_name ...])](/optimizer-hints.md#merge_joint1_name--tl_name-)
-   [INL_JOIN(t1_name [, tl_name ...])](/optimizer-hints.md#inl_joint1_name--tl_name-)
-   [INL_HASH_JOIN(t1_name [, tl_name ...])](/optimizer-hints.md#inl_hash_join)
-   [HASH_JOIN(t1_name [, tl_name ...])](/optimizer-hints.md#hash_joint1_name--tl_name-)

## 注文に参加する {#join-orders}

実際のビジネス シナリオでは、複数のテーブルの結合ステートメントが非常に一般的です。結合の実行効率は、結合における各テーブルの順序に関係します。 TiDB は、 結合したテーブルの再配置アルゴリズムを使用して、複数のテーブルが結合される順序を決定します。

オプティマイザーによって選択された結合順序が期待どおりに最適でない場合は、 `STRAIGHT_JOIN`を使用して、TiDB が`FROM`句で使用されるテーブルの順序でクエリを結合するように強制できます。

```sql
EXPLAIN SELECT *
FROM authors a STRAIGHT_JOIN book_authors ba STRAIGHT_JOIN books b
WHERE b.id = ba.book_id AND ba.author_id = a.id;
```

この結合したテーブルの再配置アルゴリズムの実装の詳細と制限の詳細については、 [結合したテーブルの再配置アルゴリズムの概要](/join-reorder.md)を参照してください。

## こちらも参照 {#see-also}

-   [テーブル結合を使用する Explain ステートメント](/explain-joins.md)
-   [結合したテーブルの再配置の概要](/join-reorder.md)
