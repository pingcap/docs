---
title: Query data from a single table
summary: This document describes how to query data from a single table in a database.
---

<!-- markdownlint-disable MD029 -->

# 単一のテーブルからデータをクエリする {#query-data-from-a-single-table}

このドキュメントでは、SQLおよびさまざまなプログラミング言語を使用して、データベース内の単一のテーブルからデータをクエリする方法について説明します。

## あなたが始める前に {#before-you-begin}

次のコンテンツでは、TiDBの単一のテーブルからデータをクエリする方法を示す例として[書店](/develop/dev-guide-bookshop-schema-design.md)のアプリケーションを取り上げます。

データをクエリする前に、次の手順を完了していることを確認してください。

1.  TiDBクラスタを構築します（ [TiDB Cloud](/develop/dev-guide-build-cluster-in-cloud.md)または[TiUP](/production-deployment-using-tiup.md)を使用することをお勧めします）。
2.  [Bookshopアプリケーションのテーブルスキーマとサンプルデータをインポートします](/develop/dev-guide-bookshop-schema-design.md#import-table-structures-and-data) 。
3.  [TiDBに接続する](/develop/dev-guide-connect-to-tidb.md) 。

## 簡単なクエリを実行する {#execute-a-simple-query}

Bookshopアプリケーションのデータベースでは、 `authors`テーブルに著者の基本情報が格納されています。 `SELECT ... FROM ...`ステートメントを使用して、データベースからデータを照会できます。

<SimpleTab>
<div label="SQL" href="simple-sql">

MySQLクライアントで次のSQLステートメントを実行します。

{{< copyable "" >}}

```sql
SELECT id, name FROM authors;
```

出力は次のとおりです。

```
+------------+--------------------------+
| id         | name                     |
+------------+--------------------------+
|       6357 | Adelle Bosco             |
|     345397 | Chanelle Koepp           |
|     807584 | Clementina Ryan          |
|     839921 | Gage Huel                |
|     850070 | Ray Armstrong            |
|     850362 | Ford Waelchi             |
|     881210 | Jayme Gutkowski          |
|    1165261 | Allison Kuvalis          |
|    1282036 | Adela Funk               |
...
| 4294957408 | Lyla Nitzsche            |
+------------+--------------------------+
20000 rows in set (0.05 sec)
```

</div>
<div label="Java" href="simple-java">

Javaでは、クラス`Author`を宣言することにより、作成者の基本情報を格納できます。データベースの[タイプ](/data-type-overview.md)と[値の範囲](/data-type-numeric.md)に応じて適切なJavaデータ型を選択する必要があります。例えば：

-   タイプ`Int`の変数を使用して、タイプ`int`のデータを格納します。
-   タイプ`Long`の変数を使用して、タイプ`bigint`のデータを格納します。
-   タイプ`Short`の変数を使用して、タイプ`tinyint`のデータを格納します。
-   タイプ`String`の変数を使用して、タイプ`varchar`のデータを格納します。
-   ..。

{{< copyable "" >}}

```java
public class Author {
    private Long id;
    private String name;
    private Short gender;
    private Short birthYear;
    private Short deathYear;

    public Author() {}

     // Skip the getters and setters.
}
```

{{< copyable "" >}}

```java
public class AuthorDAO {

    // Omit initialization of instance variables...

    public List<Author> getAuthors() throws SQLException {
        List<Author> authors = new ArrayList<>();

        try (Connection conn = ds.getConnection()) {
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT id, name FROM authors");
            while (rs.next()) {
                Author author = new Author();
                author.setId( rs.getLong("id"));
                author.setName(rs.getString("name"));
                authors.add(author);
            }
        }
        return authors;
    }
}
```

-   [JDBCドライバーを使用したTiDBへの接続](/develop/dev-guide-connect-to-tidb.md#jdbc)の後、 `conn.createStatus()`で`Statement`オブジェクトを作成できます。
-   次に、 `stmt.executeQuery("query_sql")`を呼び出して、TiDBへのデータベースクエリ要求を開始します。
-   クエリ結果は`ResultSet`のオブジェクトに保存されます。 `ResultSet`をトラバースすることにより、返された結果を`Author`オブジェクトにマップできます。

</div>
</SimpleTab>

## 結果をフィルタリングする {#filter-results}

`WHERE`ステートメントを使用して、クエリ結果をフィルタリングできます。

たとえば、次のコマンドは、すべての作成者の中で1998年に生まれた作成者を照会します。

<SimpleTab>
<div label="SQL" href="filter-sql">

`WHERE`ステートメントにフィルター条件を追加します。

{{< copyable "" >}}

```sql
SELECT * FROM authors WHERE birth_year = 1998;
```

</div>
<div label="Java" href="filter-java">

Javaでは、同じSQLを使用して、動的パラメーターを使用したデータ照会要求を処理できます。

これは、パラメーターをSQLステートメントに連結することで実行できます。ただし、この方法は、アプリケーションのセキュリティに潜在的な[SQLインジェクション](https://en.wikipedia.org/wiki/SQL_injection)のリスクをもたらします。

このようなクエリを処理するには、通常のステートメントの代わりに[プリペアドステートメント](/develop/dev-guide-prepared-statement.md)を使用します。

{{< copyable "" >}}

```java
public List<Author> getAuthorsByBirthYear(Short birthYear) throws SQLException {
    List<Author> authors = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        PreparedStatement stmt = conn.prepareStatement("""
        SELECT * FROM authors WHERE birth_year = ?;
        """);
        stmt.setShort(1, birthYear);
        ResultSet rs = stmt.executeQuery();
        while (rs.next()) {
            Author author = new Author();
            author.setId( rs.getLong("id"));
            author.setName(rs.getString("name"));
            authors.add(author);
        }
    }
    return authors;
}
```

</div>
</SimpleTab>

## 結果を並べ替える {#sort-results}

`ORDER BY`ステートメントを使用すると、クエリ結果を並べ替えることができます。

たとえば、次のSQLステートメントは、 `authors`のテーブルを`birth_year`列に従って降順（ `DESC` ）に並べ替えることにより、最年少の作成者のリストを取得します。

{{< copyable "" >}}

```sql
SELECT id, name, birth_year
FROM authors
ORDER BY birth_year DESC;
```

結果は次のとおりです。

```
+-----------+------------------------+------------+
| id        | name                   | birth_year |
+-----------+------------------------+------------+
| 83420726  | Terrance Dach          | 2000       |
| 57938667  | Margarita Christiansen | 2000       |
| 77441404  | Otto Dibbert           | 2000       |
| 61338414  | Danial Cormier         | 2000       |
| 49680887  | Alivia Lemke           | 2000       |
| 45460101  | Itzel Cummings         | 2000       |
| 38009380  | Percy Hodkiewicz       | 2000       |
| 12943560  | Hulda Hackett          | 2000       |
| 1294029   | Stanford Herman        | 2000       |
| 111453184 | Jeffrey Brekke         | 2000       |
...
300000 rows in set (0.23 sec)
```

## クエリ結果の数を制限する {#limit-the-number-of-query-results}

`LIMIT`ステートメントを使用して、クエリ結果の数を制限できます。

{{< copyable "" >}}

```sql
SELECT id, name, birth_year
FROM authors
ORDER BY birth_year DESC
LIMIT 10;
```

結果は次のとおりです。

```
+-----------+------------------------+------------+
| id        | name                   | birth_year |
+-----------+------------------------+------------+
| 83420726  | Terrance Dach          | 2000       |
| 57938667  | Margarita Christiansen | 2000       |
| 77441404  | Otto Dibbert           | 2000       |
| 61338414  | Danial Cormier         | 2000       |
| 49680887  | Alivia Lemke           | 2000       |
| 45460101  | Itzel Cummings         | 2000       |
| 38009380  | Percy Hodkiewicz       | 2000       |
| 12943560  | Hulda Hackett          | 2000       |
| 1294029   | Stanford Herman        | 2000       |
| 111453184 | Jeffrey Brekke         | 2000       |
+-----------+------------------------+------------+
10 rows in set (0.11 sec)
```

`LIMIT`ステートメントを使用すると、この例ではクエリ時間が`0.23 sec`から`0.11 sec`に大幅に短縮されます。詳細については、 [TopNとLimit](/topn-limit-push-down.md)を参照してください。

## クエリの集計 {#aggregate-queries}

データ全体の状況をよりよく理解するために、 `GROUP BY`ステートメントを使用してクエリ結果を集計できます。

たとえば、著者がさらに生まれた年を知りたい場合は、 `authors`のテーブルを`birth_year`の列でグループ化し、各年を数えることができます。

{{< copyable "" >}}

```sql
SELECT birth_year, COUNT (DISTINCT id) AS author_count
FROM authors
GROUP BY birth_year
ORDER BY author_count DESC;
```

結果は次のとおりです。

```
+------------+--------------+
| birth_year | author_count |
+------------+--------------+
|       1932 |          317 |
|       1947 |          290 |
|       1939 |          282 |
|       1935 |          289 |
|       1968 |          291 |
|       1962 |          261 |
|       1961 |          283 |
|       1986 |          289 |
|       1994 |          280 |
...
|       1972 |          306 |
+------------+--------------+
71 rows in set (0.00 sec)
```

`COUNT`関数に加えて、TiDBは他の集約関数もサポートします。詳細については、 [集約（GROUP BY）関数](/functions-and-operators/aggregate-group-by-functions.md)を参照してください。
