---
title: Query Data from a Single Table
summary: このドキュメントでは、データベース内の単一のテーブルからデータを照会する方法について説明します。
aliases: ['/ja/tidb/stable/dev-guide-get-data-from-single-table/','/ja/tidb/dev/dev-guide-get-data-from-single-table/','/ja/tidbcloud/dev-guide-get-data-from-single-table/']
---

<!-- markdownlint-disable MD029 -->

# 単一テーブルからデータをクエリする {#query-data-from-a-single-table}

このドキュメントでは、SQLおよび各種プログラミング言語を使用して、データベース内の単一テーブルからデータを照会する方法について説明します。

## 始める前に {#before-you-begin}

以下の内容は、TiDB の単一テーブルからデータをクエリする方法を示すために、 [書店](/develop/dev-guide-bookshop-schema-design.md)アプリケーションを例として使用します。

データを照会する前に、以下の手順を完了していることを確認してください。

<SimpleTab groupId="platform">
<div label="TiDB Cloud" value="tidb-cloud">

1.  [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。
2.  [Bookshopアプリケーションのテーブルスキーマとサンプルデータをインポートします。](/develop/dev-guide-bookshop-schema-design.md#import-table-structures-and-data)
3.  [TiDBに接続する](/develop/dev-guide-connect-to-tidb.md)。

</div>
<div label="TiDB Self-Managed" value="tidb">

1.  [TiDBセルフマネージドクラスタをデプロイ](/production-deployment-using-tiup.md)。
2.  [Bookshopアプリケーションのテーブルスキーマとサンプルデータをインポートします。](/develop/dev-guide-bookshop-schema-design.md#import-table-structures-and-data)
3.  [TiDBに接続する](/develop/dev-guide-connect-to-tidb.md)。

</div>
</SimpleTab>

## 簡単なクエリを実行します {#execute-a-simple-query}

Bookshopアプリケーションのデータベースでは、 `authors`テーブルに著者の基本情報が格納されています。 `SELECT ... FROM ...`ステートメントを使用して、データベースからデータを照会できます。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

MySQLクライアントで以下のSQL文を実行してください。

```sql
SELECT id, name FROM authors;
```

出力は以下のとおりです。

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

Javaでは、著者の基本情報を格納するために、クラス`Author`[価格帯](/data-type-numeric.md)[データ型](/data-type-overview.md)応じて適切なJavaデータ型を選択する必要があります。例：

-   `Int`型のデータを格納するには、 `int`型の変数を使用します。
-   `Long`型のデータを格納するには、 `bigint`型の変数を使用します。
-   `Short`型のデータを格納するには、 `tinyint`型の変数を使用します。
-   `String`型のデータを格納するには、 `varchar`型の変数を使用します。

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

[JDBCドライバを使用してTiDBに接続する](/develop/dev-guide-sample-application-java-jdbc.md)後、 `Statement`を使用して`conn.createStatement()`オブジェクトを作成し、 `stmt.executeQuery("query_sql")`を呼び出して TiDB へのデータベース クエリ リクエストを開始できます。

クエリ結果は`ResultSet`オブジェクトに格納されます。 `ResultSet`を走査することで、返された結果を`Author`オブジェクトにマッピングできます。

</div>
</SimpleTab>

## 結果を絞り込む {#filter-results}

クエリ結果をフィルタリングするには、 `WHERE`ステートメントを使用できます。

例えば、以下のコマンドは、すべての著者の中から1998年生まれの著者を抽出します。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

`WHERE`ステートメントにフィルタ条件を追加します。

```sql
SELECT * FROM authors WHERE birth_year = 1998;
```

</div>
<div label="Java" value="java">

Javaでは、同じSQLを使用して、動的なパラメータを持つデータクエリ要求を処理できます。

これは、パラメータを SQL ステートメントに連結することで実行できます。ただし、この方法では、アプリケーションのセキュリティに[SQLインジェクション](https://en.wikipedia.org/wiki/SQL_injection)インジェクションの潜在的なリスクが生じます。

このようなクエリに対処するには、通常のステートメントの代わりに[準備された声明](/develop/dev-guide-prepared-statement.md)を使用します。

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

例えば、次の SQL ステートメントは、 `authors`テーブルを降順 ( `DESC` ) にソートすることにより、 `birth_year`リストを取得します。

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

結果は以下のとおりです。

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

結果は以下のとおりです。

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

この例では、 `LIMIT`ステートメントを使用すると、クエリ時間が`0.23 sec`から`0.11 sec`に大幅に短縮されます。詳細については、 [TopNとLimit](/topn-limit-push-down.md)参照してください。

## 集計クエリ {#aggregate-queries}

データの全体的な状況をよりよく理解するために、 `GROUP BY`ステートメントを使用してクエリ結果を集計できます。

例えば、どの年に作家の出生数が多いかを知りたい場合は、 `authors`テーブルを`birth_year`列でグループ化し、各年ごとにカウントすることができます。

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

結果は以下のとおりです。

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

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
