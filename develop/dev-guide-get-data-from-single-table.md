---
title: Query Data from a Single Table
summary: このドキュメントは、SQLおよびさまざまなプログラミング言語を使用して、データベース内の単一テーブルのデータをクエリする方法について説明しています。例として、TiDBの単一テーブルのデータをクエリする方法を示しています。データをクエリする前に、TiDBクラスターを構築し、Bookshopアプリケーションのテーブルスキーマとサンプルデータをインポートする必要があります。クエリの実行、フィルタ結果、結果の並べ替え、クエリ結果の数の制限、および集計クエリについても説明しています。
---

<!-- markdownlint-disable MD029 -->

# 単一のテーブルからデータをクエリする {#query-data-from-a-single-table}

このドキュメントでは、SQL およびさまざまなプログラミング言語を使用して、データベース内の単一テーブルのデータをクエリする方法について説明します。

## あなたが始める前に {#before-you-begin}

次のコンテンツでは、 [書店](/develop/dev-guide-bookshop-schema-design.md)アプリケーションを例として、TiDB の単一テーブルのデータをクエリする方法を示します。

データをクエリする前に、次の手順を完了していることを確認してください。

<CustomContent platform="tidb">

1.  TiDB クラスターを構築します ( [TiDB Cloud](/develop/dev-guide-build-cluster-in-cloud.md)または[TiUP](/production-deployment-using-tiup.md)の使用を推奨)。

</CustomContent>

<CustomContent platform="tidb-cloud">

1.  [TiDB Cloud](/develop/dev-guide-build-cluster-in-cloud.md)を使用して TiDB クラスターを構築します。

</CustomContent>

2.  [Bookshop アプリケーションのテーブル スキーマとサンプル データをインポートします](/develop/dev-guide-bookshop-schema-design.md#import-table-structures-and-data) 。

<CustomContent platform="tidb">

3.  [TiDB に接続する](/develop/dev-guide-connect-to-tidb.md) 。

</CustomContent>

<CustomContent platform="tidb-cloud">

3.  [TiDB に接続する](/tidb-cloud/connect-to-tidb-cluster.md) 。

</CustomContent>

## 単純なクエリを実行する {#execute-a-simple-query}

Bookshop アプリケーションのデータベースには、著者の基本情報が`authors`テーブルに格納されています。 `SELECT ... FROM ...`ステートメントを使用して、データベースのデータをクエリできます。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

MySQL クライアントで次の SQL ステートメントを実行します。

```sql
SELECT id, name FROM authors;
```

出力は次のとおりです。

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

</div>
<div label="Java" value="java">

Javaでは、作成者の基本情報を保存するために、クラス`Author`を宣言できます。データベースの[データ型](/data-type-overview.md)と[値の範囲](/data-type-numeric.md)に従って、適切なJavaデータ型を選択する必要があります。例えば：

-   タイプ`Int`の変数を使用して、タイプ`int`のデータを格納します。
-   タイプ`bigint`のデータを格納するには、タイプ`Long`の変数を使用します。
-   タイプ`tinyint`のデータを格納するには、タイプ`Short`の変数を使用します。
-   タイプ`varchar`のデータを格納するには、タイプ`String`の変数を使用します。

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

-   [JDBC ドライバーを使用して TiDB に接続する](/develop/dev-guide-connect-to-tidb.md#jdbc)の後に、 `conn.createStatus()`を使用して`Statement`オブジェクトを作成できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [JDBC ドライバーを使用して TiDB に接続する](/develop/dev-guide-choose-driver-or-orm.md#java-drivers)の後に、 `conn.createStatus()`を使用して`Statement`オブジェクトを作成できます。

</CustomContent>

-   次に、 `stmt.executeQuery("query_sql")`を呼び出して、TiDB へのデータベース クエリ リクエストを開始します。
-   クエリ結果は`ResultSet`オブジェクトに保存されます。 `ResultSet`トラバースすることで、返された結果を`Author`オブジェクトにマッピングできます。

</div>
</SimpleTab>

## フィルタ結果 {#filter-results}

クエリ結果をフィルターするには、 `WHERE`ステートメントを使用できます。

たとえば、次のコマンドは、すべての著者のうち 1998 年生まれの著者をクエリします。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

`WHERE`ステートメントにフィルター条件を追加します。

```sql
SELECT * FROM authors WHERE birth_year = 1998;
```

</div>
<div label="Java" value="java">

Javaでは、同じ SQL を使用して、動的パラメータを使用したデータ クエリ リクエストを処理できます。

これは、パラメータを SQL ステートメントに連結することで実行できます。ただし、この方法はアプリケーションのセキュリティに[SQLインジェクション](https://en.wikipedia.org/wiki/SQL_injection)的なリスクをもたらします。

このようなクエリを処理するには、通常のステートメントの代わりに[作成済みのステートメント](/develop/dev-guide-prepared-statement.md)を使用します。

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

たとえば、次の SQL ステートメントは、 `authors`テーブルを`birth_year`列に従って降順 ( `DESC` ) にソートすることにより、最年少の著者のリストを取得します。

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

この例では、ステートメント`LIMIT`を使用すると、クエリ時間が`0.23 sec`から`0.11 sec`に大幅に短縮されます。詳細については、 [トップNとリミット](/topn-limit-push-down.md)を参照してください。

## 集計クエリ {#aggregate-queries}

データ全体の状況をより深く理解するには、 `GROUP BY`ステートメントを使用してクエリ結果を集計します。

たとえば、より多くの著者が生まれた年を知りたい場合は、 `authors`テーブルを`birth_year`列でグループ化し、年ごとにカウントします。

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

`COUNT`関数に加えて、TiDB は他の集計関数もサポートしています。詳細については、 [集計 (GROUP BY) 関数](/functions-and-operators/aggregate-group-by-functions.md)を参照してください。
