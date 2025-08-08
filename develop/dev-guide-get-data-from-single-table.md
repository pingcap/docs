---
title: Query Data from a Single Table
summary: このドキュメントでは、データベース内の単一のテーブルからデータをクエリする方法について説明します。
---

<!-- markdownlint-disable MD029 -->

# 単一のテーブルからデータをクエリする {#query-data-from-a-single-table}

このドキュメントでは、SQL とさまざまなプログラミング言語を使用して、データベース内の単一のテーブルからデータをクエリする方法について説明します。

## 始める前に {#before-you-begin}

次のコンテンツでは、 [書店](/develop/dev-guide-bookshop-schema-design.md)アプリケーションを例として、TiDB 内の単一のテーブルからデータをクエリする方法を示します。

データをクエリする前に、次の手順が完了していることを確認してください。

<CustomContent platform="tidb">

1.  TiDB クラスターを構築します ( [TiDB Cloud](/develop/dev-guide-build-cluster-in-cloud.md)または[TiUP](/production-deployment-using-tiup.md)使用を推奨)。

</CustomContent>

<CustomContent platform="tidb-cloud">

1.  [TiDB Cloud](/develop/dev-guide-build-cluster-in-cloud.md)使用して TiDB クラスターを構築します。

</CustomContent>

2.  [Bookshop アプリケーションのテーブル スキーマとサンプル データをインポートします。](/develop/dev-guide-bookshop-schema-design.md#import-table-structures-and-data) 。

<CustomContent platform="tidb">

3.  [TiDBに接続する](/develop/dev-guide-connect-to-tidb.md) 。

</CustomContent>

<CustomContent platform="tidb-cloud">

3.  [TiDBに接続する](/tidb-cloud/connect-to-tidb-cluster.md) 。

</CustomContent>

## 簡単なクエリを実行する {#execute-a-simple-query}

Bookshopアプリケーションのデータベースでは、 `authors`のテーブルに著者の基本情報が保存されています。3 `SELECT ... FROM ...`のステートメントを使用して、データベースからデータをクエリできます。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

MySQL クライアントで次の SQL ステートメントを実行します。

```sql
SELECT id, name FROM authors;
```

出力は次のようになります。

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

Javaでは、著者の基本情報を格納するためにクラス`Author`宣言できます。データベースの[データ型](/data-type-overview.md)と[値の範囲](/data-type-numeric.md)に応じて適切なJavaデータ型を選択する必要があります。例えば、次のようになります。

-   タイプ`Int`の変数を使用して、タイプ`int`のデータを保存します。
-   タイプ`Long`の変数を使用して、タイプ`bigint`のデータを保存します。
-   タイプ`Short`の変数を使用して、タイプ`tinyint`のデータを保存します。
-   タイプ`String`の変数を使用して、タイプ`varchar`のデータを保存します。

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

-   [JDBC ドライバーを使用して TiDB に接続する](/develop/dev-guide-connect-to-tidb.md#jdbc)後は`conn.createStatus()`で`Statement`オブジェクトを作成できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [JDBC ドライバーを使用して TiDB に接続する](/develop/dev-guide-choose-driver-or-orm.md#java-drivers)後は`conn.createStatus()`で`Statement`オブジェクトを作成できます。

</CustomContent>

-   次に、 `stmt.executeQuery("query_sql")`呼び出して、TiDB へのデータベース クエリ要求を開始します。
-   クエリ結果は`ResultSet`オブジェクトに保存されます。 `ResultSet`トラバースすることで、返された結果を`Author`オブジェクトにマッピングできます。

</div>
</SimpleTab>

## 結果をフィルタリングする {#filter-results}

クエリ結果をフィルタリングするには、 `WHERE`ステートメントを使用できます。

たとえば、次のコマンドは、すべての著者の中から 1998 年に生まれた著者を照会します。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

`WHERE`ステートメントにフィルター条件を追加します。

```sql
SELECT * FROM authors WHERE birth_year = 1998;
```

</div>
<div label="Java" value="java">

Javaでは、同じ SQL を使用して、動的パラメータを含むデータ クエリ要求を処理できます。

これは、パラメータをSQL文に連結することで実現できます。ただし、この方法はアプリケーションのセキュリティに潜在的[SQLインジェクション](https://en.wikipedia.org/wiki/SQL_injection)リスクをもたらします。

このようなクエリを処理するには、通常のステートメントの代わりに[準備された声明](/develop/dev-guide-prepared-statement.md)使用します。

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

## 結果を並べ替える {#sort-results}

クエリ結果を並べ替えるには、 `ORDER BY`ステートメントを使用できます。

たとえば、次の SQL 文は、 `authors`テーブルを`birth_year`番目の列に従って降順 ( `DESC` ) で並べ替えて、最も若い著者のリストを取得します。

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

この例では、 `LIMIT`文を実行することでクエリ時間が`0.23 sec`から`0.11 sec`に大幅に短縮されます。詳細については、 [TopNとLimit](/topn-limit-push-down.md)参照してください。

## 集計クエリ {#aggregate-queries}

全体的なデータ状況をよりよく理解するために、 `GROUP BY`ステートメントを使用してクエリ結果を集計できます。

たとえば、どの年に作家がより多く生まれたかを知りたい場合は、 `authors`テーブルを`birth_year`番目の列でグループ化し、各年についてカウントすることができます。

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

`COUNT`関数に加えて、TiDB は他の集計関数もサポートしています。詳細については、 [集計（GROUP BY）関数](/functions-and-operators/aggregate-group-by-functions.md)参照してください。

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>
