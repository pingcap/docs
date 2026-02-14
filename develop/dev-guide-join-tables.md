---
title: Multi-table Join Queries
summary: このドキュメントでは、複数テーブル結合クエリの使用方法について説明します。
aliases: ['/ja/tidb/stable/dev-guide-join-tables/','/ja/tidbcloud/dev-guide-join-tables/']
---

# 複数テーブルの結合クエリ {#multi-table-join-queries}

多くのシナリオでは、1つのクエリで複数のテーブルからデータを取得する必要があります。1 `JOIN`ステートメントを使用して、2つ以上のテーブルのデータを結合できます。

## 結合タイプ {#join-types}

このセクションでは、結合タイプについて詳しく説明します。

### 内部結合 {#inner-join}

内部結合の結合結果は、結合条件に一致する行のみを返します。

![Inner Join](/media/develop/inner-join.png)

たとえば、最も多作な著者を知りたい場合は、 `authors`という名前の著者テーブルと`book_authors`という名前の書籍著者テーブルを結合する必要があります。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

次のSQL文では、キーワード`JOIN`を使用して、左側のテーブル`authors`と右側のテーブル`book_authors`の行を結合条件`a.id = ba.author_id`で内部結合することを宣言します。結果セットには、結合条件を満たす行のみが含まれます。著者が書籍を執筆していない場合、テーブル`authors`の著者のレコードは結合条件を満たさないため、結果セットには表示されません。

```sql
SELECT ANY_VALUE(a.id) AS author_id, ANY_VALUE(a.name) AS author_name, COUNT(ba.book_id) AS books
FROM authors a
JOIN book_authors ba ON a.id = ba.author_id
GROUP BY ba.author_id
ORDER BY books DESC
LIMIT 10;
```

クエリの結果は次のとおりです。

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

左外部結合は、左テーブルのすべての行と、結合条件に一致する右テーブルの値を返します。右テーブルに一致する行がない場合、 `NULL`が代入されます。

![Left Outer Join](/media/develop/left-outer-join.png)

場合によっては、データクエリを完了するために複数のテーブルを使用したいが、結合条件が満たされないためにデータセットが小さくなりすぎないようにしたいことがあります。

例えば、Bookshopアプリのホームページに、平均的な評価が付いた新刊書籍のリストを表示したいとします。この場合、新刊書籍はまだ誰にも評価されていない可能性があります。Inner Joinを使用すると、これらの評価されていない書籍の情報がフィルター処理されてしまい、期待どおりの結果になりません。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

次の SQL ステートメントでは、キーワード`LEFT JOIN`を使用して、左側のテーブル`books`右側のテーブル`ratings`に左外部結合で結合されることを宣言し、 `books`テーブルのすべての行が返されるようにします。

```sql
SELECT b.id AS book_id, ANY_VALUE(b.title) AS book_title, AVG(r.score) AS average_score
FROM books b
LEFT JOIN ratings r ON b.id = r.book_id
GROUP BY b.id
ORDER BY b.published_at DESC
LIMIT 10;
```

クエリの結果は次のとおりです。

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

最近出版された本にはすでに多くの評価が付けられているようです。上記の方法を検証するために、SQL文を使って*「The Documentary of lion」*という本のすべての評価を削除してみましょう。

```sql
DELETE FROM ratings WHERE book_id = 3438991610;
```

再度クエリを実行します。結果セットには書籍*「The Documentary of lion」*がまだ表示されますが、右側の表`ratings`の`score`から計算された`average_score`列目は`NULL`で埋められます。

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

`INNER JOIN`使用するとどうなるでしょうか？試してみるのはあなた次第です。

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

右外部結合は、右テーブルのすべてのレコードと、結合条件に一致する左テーブルの値を返します。一致する値がない場合、 `NULL`が代入されます。

![Right Outer Join](/media/develop/right-outer-join.png)

### クロス結合 {#cross-join}

結合条件が定数の場合、2つのテーブル間の内部結合は[クロス結合](https://en.wikipedia.org/wiki/Join_(SQL)#Cross_join)と呼ばれます。クロス結合は、左側のテーブルのすべてのレコードを右側のテーブルのすべてのレコードに結合します。左側のテーブルのレコード数が`m`で、右側のテーブルのレコード数が`n`の場合、結果セットには`m \* n`レコードが生成されます。

### 左セミ結合 {#left-semi-join}

TiDBはSQL構文レベルでは`LEFT SEMI JOIN table_name`サポートしていません。ただし、実行プランレベルでは、 [サブクエリ関連の最適化](/subquery-optimization.md)書き換えられた同等のJOINクエリに対して`semi join`デフォルトの結合方法として使用します。

## 暗黙的な結合 {#implicit-join}

明示的に結合を宣言する`JOIN`文がSQL標準に追加される前は、 `FROM t1, t2`句を用いてSQL文で2つ以上のテーブルを結合し、 `WHERE t1.id = t2.id`句を用いて結合条件を指定することができました。これは、内部結合を用いてテーブルを結合する暗黙的な結合と理解できます。

## 関連するアルゴリズムを結合する {#join-related-algorithms}

TiDB は、次の一般的なテーブル結合アルゴリズムをサポートしています。

-   [インデックス結合](/explain-joins.md#index-join)
-   [ハッシュ結合](/explain-joins.md#hash-join)
-   [マージ結合](/explain-joins.md#merge-join)

オプティマイザは、結合対象テーブルのデータ量などの要因に基づいて、適切な結合アルゴリズムを選択します。クエリが結合にどのアルゴリズムを使用しているかは、 `EXPLAIN`ステートメントで確認できます。

TiDB のオプティマイザーが最適な結合アルゴリズムに従って実行されない場合は、 [オプティマイザヒント](/optimizer-hints.md)使用して、TiDB がより適切な結合アルゴリズムを使用するように強制できます。

例えば、上記の左結合クエリの例が、オプティマイザによって選択されないハッシュ結合アルゴリズムを使用した方が高速に実行されると仮定すると、キーワード`SELECT`後にヒント`/*+ HASH_JOIN(b, r) */`を追加できます。テーブルに別名がある場合は、ヒントでも別名を使用することに注意してください。

```sql
EXPLAIN SELECT /*+ HASH_JOIN(b, r) */ b.id AS book_id, ANY_VALUE(b.title) AS book_title, AVG(r.score) AS average_score
FROM books b
LEFT JOIN ratings r ON b.id = r.book_id
GROUP BY b.id
ORDER BY b.published_at DESC
LIMIT 10;
```

結合アルゴリズムに関連するヒント:

-   [MERGE_JOIN(t1_name [, tl_name ...])](/optimizer-hints.md#merge_joint1_name--tl_name-)
-   [INL_JOIN(t1_name [, tl_name ...])](/optimizer-hints.md#inl_joint1_name--tl_name-)
-   [INL_HASH_JOIN(t1_name [, tl_name ...])](/optimizer-hints.md#inl_hash_join)
-   [HASH_JOIN(t1_name [, tl_name ...])](/optimizer-hints.md#hash_joint1_name--tl_name-)

## 注文を結合する {#join-orders}

実際のビジネスシナリオでは、複数のテーブルを結合する文が非常に一般的です。結合の実行効率は、結合する各テーブルの順序に左右されます。TiDBは、結合したテーブルの再配置アルゴリズムを使用して、複数のテーブルを結合する順序を決定します。

オプティマイザによって選択された結合順序が予想どおりに最適でない場合は、 `STRAIGHT_JOIN`使用して、TiDB が`FROM`句で使用されるテーブルの順序でクエリを結合するように強制できます。

```sql
EXPLAIN SELECT *
FROM authors a STRAIGHT_JOIN book_authors ba STRAIGHT_JOIN books b
WHERE b.id = ba.book_id AND ba.author_id = a.id;
```

この結合したテーブルの再配置アルゴリズムの実装の詳細と制限の詳細については、 [結合したテーブルの再配置アルゴリズムの紹介](/join-reorder.md)参照してください。

## 参照 {#see-also}

-   [テーブル結合を使用するステートメントを説明する](/explain-joins.md)
-   [結合したテーブルの再配置の概要](/join-reorder.md)

## ヘルプが必要ですか? {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに問い合わせてください。
-   [TiDB Cloudのサポートチケットを送信する](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDBセルフマネージドのサポートチケットを送信する](/support.md)
