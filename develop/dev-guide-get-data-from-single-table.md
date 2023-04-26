---
title: Query Data from a Single Table
summary: This document describes how to query data from a single table in a database.
---

<!-- markdownlint-disable MD029 -->

# 単一のテーブルからのデータのクエリ {#query-data-from-a-single-table}

このドキュメントでは、SQL とさまざまなプログラミング言語を使用して、データベース内の 1 つのテーブルからデータをクエリする方法について説明します。

## あなたが始める前に {#before-you-begin}

次のコンテンツでは、 [書店](/develop/dev-guide-bookshop-schema-design.md)アプリケーションを例として、TiDB の単一のテーブルからデータをクエリする方法を示します。

データのクエリを実行する前に、次の手順を完了していることを確認してください。

<CustomContent platform="tidb">

1.  TiDB クラスターを構築します ( [TiDB Cloud](/develop/dev-guide-build-cluster-in-cloud.md)または[TiUP](/production-deployment-using-tiup.md)を使用することをお勧めします)。

</CustomContent>

<CustomContent platform="tidb-cloud">

1.  [TiDB Cloud](/develop/dev-guide-build-cluster-in-cloud.md)を使用して TiDB クラスターを構築します。

</CustomContent>

2.  [Bookshop アプリケーションのテーブル スキーマとサンプル データをインポートする](/develop/dev-guide-bookshop-schema-design.md#import-table-structures-and-data) .

<CustomContent platform="tidb">

3.  [TiDB に接続する](/develop/dev-guide-connect-to-tidb.md) .

</CustomContent>

<CustomContent platform="tidb-cloud">

3.  [TiDB に接続する](/tidb-cloud/connect-to-tidb-cluster.md) .

</CustomContent>

## 簡単なクエリを実行する {#execute-a-simple-query}

Bookshop アプリケーションのデータベースでは、 `authors`テーブルに著者の基本情報が格納されます。 `SELECT ... FROM ...`ステートメントを使用して、データベースからデータを照会できます。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

MySQL クライアントで次の SQL ステートメントを実行します。

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
<div label="Java" value="java">

Javaでは、作成者の基本情報を格納するために、クラス`Author`を宣言できます。データベースの[データ型](/data-type-overview.md)と[値の範囲](/data-type-numeric.md)に従って、適切なJavaデータ型を選択する必要があります。例えば：

-   タイプ`Int`の変数を使用して、タイプ`int`のデータを格納します。
-   タイプ`Long`の変数を使用して、タイプ`bigint`のデータを格納します。
-   タイプ`Short`の変数を使用して、タイプ`tinyint`のデータを格納します。
-   タイプ`String`の変数を使用して、タイプ`varchar`のデータを格納します。

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

```java
public class AuthorDAO {

    // Omit initialization of instance variables.

    public List<Author> getAuthors() throws SQLException {
        List<Author> authors = new ArrayList<>();

        try (Connection conn = ds.getConnection()) {
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT id, name FROM authors");
            while (rs.next()) {
                Author author = new Author();
                author.setId(rs.getLong("id"));
                author.setName(rs.getString("name"));
                authors.add(author);
            }
        }
        return authors;
    }
}
```

<CustomContent platform="tidb">

-   [JDBC ドライバーを使用して TiDB に接続する](/develop/dev-guide-connect-to-tidb.md#jdbc)の後、 `conn.createStatus()`で`Statement`オブジェクトを作成できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [JDBC ドライバーを使用して TiDB に接続する](/develop/dev-guide-choose-driver-or-orm.md#java-drivers)の後、 `conn.createStatus()`で`Statement`オブジェクトを作成できます。

</CustomContent>

-   次に`stmt.executeQuery("query_sql")`を呼び出して、TiDB へのデータベース クエリ要求を開始します。
-   クエリ結果は`ResultSet`のオブジェクトに格納されます。 `ResultSet`トラバースすることで、返された結果を`Author`オブジェクトにマップできます。

</div>
</SimpleTab>

## 結果のフィルタリング {#filter-results}

クエリ結果をフィルタリングするには、 `WHERE`ステートメントを使用できます。

たとえば、次のコマンドは、すべての著者の中で 1998 年生まれの著者を照会します。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

`WHERE`ステートメントにフィルター条件を追加します。

```sql
SELECT * FROM authors WHERE birth_year = 1998;
```

</div>
<div label="Java" value="java">

Javaでは、同じ SQL を使用して、動的パラメーターを持つデータ クエリ要求を処理できます。

これは、パラメーターを SQL ステートメントに連結することによって実行できます。ただし、この方法は、アプリケーションのセキュリティに[SQL インジェクション](https://en.wikipedia.org/wiki/SQL_injection)リスクをもたらす可能性があります。

このようなクエリを処理するには、通常のステートメントの代わりに[作成済みステートメント](/develop/dev-guide-prepared-statement.md)を使用します。

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

## 結果の並べ替え {#sort-results}

クエリ結果を並べ替えるには、 `ORDER BY`ステートメントを使用できます。

たとえば、次の SQL ステートメントは、 `birth_year`列に従って`authors`テーブルを降順 ( `DESC` ) に並べ替えることで、最年少の著者のリストを取得します。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

```sql
SELECT id, name, birth_year
FROM authors
ORDER BY birth_year DESC;
```

</div>

<div label="Java" value="java">

```java
public List<Author> getAuthorsSortByBirthYear() throws SQLException {
    List<Author> authors = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery("""
            SELECT id, name, birth_year
            FROM authors
            ORDER BY birth_year DESC;
            """);

        while (rs.next()) {
            Author author = new Author();
            author.setId(rs.getLong("id"));
            author.setName(rs.getString("name"));
            author.setBirthYear(rs.getShort("birth_year"));
            authors.add(author);
        }
    }
    return authors;
}
```

</div>
</SimpleTab>

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

クエリ結果の数を制限するには、 `LIMIT`ステートメントを使用できます。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

```sql
SELECT id, name, birth_year
FROM authors
ORDER BY birth_year DESC
LIMIT 10;
```

</div>

<div label="Java" value="java">

```java
public List<Author> getAuthorsWithLimit(Integer limit) throws SQLException {
    List<Author> authors = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        PreparedStatement stmt = conn.prepareStatement("""
            SELECT id, name, birth_year
            FROM authors
            ORDER BY birth_year DESC
            LIMIT ?;
            """);
        stmt.setInt(1, limit);
        ResultSet rs = stmt.executeQuery();
        while (rs.next()) {
            Author author = new Author();
            author.setId(rs.getLong("id"));
            author.setName(rs.getString("name"));
            author.setBirthYear(rs.getShort("birth_year"));
            authors.add(author);
        }
    }
    return authors;
}
```

</div>
</SimpleTab>

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

`LIMIT`ステートメントを使用すると、この例ではクエリ時間が`0.23 sec`から`0.11 sec`に大幅に短縮されます。詳細については、 [TopN と制限](/topn-limit-push-down.md)を参照してください。

## 集計クエリ {#aggregate-queries}

全体的なデータ状況をよりよく理解するために、 `GROUP BY`ステートメントを使用してクエリ結果を集計できます。

たとえば、より多くの著者が生まれた年を知りたい場合は、 `authors`テーブルを`birth_year`列でグループ化し、各年をカウントできます。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

```sql
SELECT birth_year, COUNT (DISTINCT id) AS author_count
FROM authors
GROUP BY birth_year
ORDER BY author_count DESC;
```

</div>

<div label="Java" value="java">

```java
public class AuthorCount {
    private Short birthYear;
    private Integer authorCount;

    public AuthorCount() {}

     // Skip the getters and setters.
}

public List<AuthorCount> getAuthorCountsByBirthYear() throws SQLException {
    List<AuthorCount> authorCounts = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery("""
            SELECT birth_year, COUNT(DISTINCT id) AS author_count
            FROM authors
            GROUP BY birth_year
            ORDER BY author_count DESC;
            """);

        while (rs.next()) {
            AuthorCount authorCount = new AuthorCount();
            authorCount.setBirthYear(rs.getShort("birth_year"));
            authorCount.setAuthorCount(rs.getInt("author_count"));
            authorCounts.add(authorCount);
        }
    }
    return authorCount;
}
```

</div>
</SimpleTab>

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

`COUNT`関数に加えて、TiDB は他の集計関数もサポートしています。詳細については、 [集計 (GROUP BY) 関数](/functions-and-operators/aggregate-group-by-functions.md)を参照してください。
