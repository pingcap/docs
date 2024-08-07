---
title: Paginate Results
summary: TiDB にページ分割結果機能を導入します。
---

# 結果をページ分けする {#paginate-results}

大きなクエリ結果をページングするには、「ページ区切り」方式で目的の部分を取得できます。

## クエリ結果をページ分割する {#paginate-query-results}

TiDB では、 `LIMIT`ステートメントを使用してクエリ結果をページ分割できます。例:

```sql
SELECT * FROM table_a t ORDER BY gmt_modified DESC LIMIT offset, row_count;
```

`offset`レコードの開始数を示し、 `row_count`ページあたりのレコード数を示します。TiDB は`LIMIT row_count OFFSET offset`構文もサポートしています。

ページネーションを使用する場合、データをランダムに表示する必要がない限り、 `ORDER BY`ステートメントを使用してクエリ結果を並べ替えることをお勧めします。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

たとえば、 [書店](/develop/dev-guide-bookshop-schema-design.md)アプリケーションのユーザーが最新の出版済み書籍をページ分けして表示できるようにするには、 `LIMIT 0, 10`ステートメントを使用します。このステートメントは、結果リストの最初のページを返します。ページあたり最大 10 件のレコードが含まれます。2 ページ目を取得するには、ステートメントを`LIMIT 10, 10`に変更できます。

```sql
SELECT *
FROM books
ORDER BY published_at DESC
LIMIT 0, 10;
```

</div>
<div label="Java" value="java">

アプリケーション開発では、バックエンド プログラムは、フロントエンドから`offset`のパラメータではなく、 `page_number`パラメータ (要求されているページ番号を意味します) と`page_size`パラメータ (ページあたりのレコード数を制御します) を受け取ります。そのため、クエリを実行する前にいくつかの変換を行う必要がありました。

```java
public List<Book> getLatestBooksPage(Long pageNumber, Long pageSize) throws SQLException {
    pageNumber = pageNumber < 1L ? 1L : pageNumber;
    pageSize = pageSize < 10L ? 10L : pageSize;
    Long offset = (pageNumber - 1) * pageSize;
    Long limit = pageSize;
    List<Book> books = new ArrayList<>();
    try (Connection conn = ds.getConnection()) {
        PreparedStatement stmt = conn.prepareStatement("""
        SELECT id, title, published_at
        FROM books
        ORDER BY published_at DESC
        LIMIT ?, ?;
        """);
        stmt.setLong(1, offset);
        stmt.setLong(2, limit);
        ResultSet rs = stmt.executeQuery();
        while (rs.next()) {
            Book book = new Book();
            book.setId(rs.getLong("id"));
            book.setTitle(rs.getString("title"));
            book.setPublishedAt(rs.getDate("published_at"));
            books.add(book);
        }
    }
    return books;
}
```

</div>
</SimpleTab>

## 単一フィールドの主キーテーブルのページングバッチ {#paging-batches-for-single-field-primary-key-tables}

通常、主キーまたは一意のインデックスを使用して結果を並べ替え、 `LIMIT`句の`offset`キーワードを使用して指定された行数でページを分割するページネーション SQL ステートメントを記述できます。次に、ページを独立したトランザクションにラップして、柔軟なページング更新を実現します。ただし、欠点も明らかです。主キーまたは一意のインデックスを並べ替える必要があるため、オフセットが大きいほど、特に大量のデータの場合は、より多くのコンピューティング リソースが消費されます。

以下に、より効率的なページング バッチ処理方法を紹介します。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

まず、データを主キーでソートし、ウィンドウ関数`row_number()`を呼び出して各行の行番号を生成します。次に、集計関数を呼び出して、指定されたページ サイズで行番号をグループ化し、各ページの最小値と最大値を計算します。

```sql
SELECT
    floor((t.row_num - 1) / 1000) + 1 AS page_num,
    min(t.id) AS start_key,
    max(t.id) AS end_key,
    count(*) AS page_size
FROM (
    SELECT id, row_number() OVER (ORDER BY id) AS row_num
    FROM books
) t
GROUP BY page_num
ORDER BY page_num;
```

結果は以下のようになります。

    +----------+------------+------------+-----------+
    | page_num | start_key  | end_key    | page_size |
    +----------+------------+------------+-----------+
    |        1 |     268996 |  213168525 |      1000 |
    |        2 |  213210359 |  430012226 |      1000 |
    |        3 |  430137681 |  647846033 |      1000 |
    |        4 |  647998334 |  848878952 |      1000 |
    |        5 |  848899254 | 1040978080 |      1000 |
    ...
    |       20 | 4077418867 | 4294004213 |      1000 |
    +----------+------------+------------+-----------+
    20 rows in set (0.01 sec)

次に、 `WHERE id BETWEEN start_key AND end_key`ステートメントを使用して各スライスのデータをクエリします。データをより効率的に更新するには、データを変更するときに上記のスライス情報を使用できます。

1 ページ目にあるすべての書籍の基本情報を削除するには、上記の結果の`start_key`と`end_key`を 1 ページ目の値に置き換えます。

```sql
DELETE FROM books
WHERE
    id BETWEEN 268996 AND 213168525
ORDER BY id;
```

</div>
<div label="Java" value="java">

Javaで、ページのメタ情報を保存するクラスを`PageMeta`定義します。

```java
public class PageMeta<K> {
    private Long pageNum;
    private K startKey;
    private K endKey;
    private Long pageSize;

    // Skip the getters and setters.

}
```

ページ メタ情報リストを取得する`getPageMetaList()`メソッドを定義し、次にページ メタ情報に従ってデータを一括削除する`deleteBooksByPageMeta()`メソッドを定義します。

```java
public class BookDAO {
    public List<PageMeta<Long>> getPageMetaList() throws SQLException {
        List<PageMeta<Long>> pageMetaList = new ArrayList<>();
        try (Connection conn = ds.getConnection()) {
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("""
            SELECT
                floor((t.row_num - 1) / 1000) + 1 AS page_num,
                min(t.id) AS start_key,
                max(t.id) AS end_key,
                count(*) AS page_size
            FROM (
                SELECT id, row_number() OVER (ORDER BY id) AS row_num
                FROM books
            ) t
            GROUP BY page_num
            ORDER BY page_num;
            """);
            while (rs.next()) {
                PageMeta<Long> pageMeta = new PageMeta<>();
                pageMeta.setPageNum(rs.getLong("page_num"));
                pageMeta.setStartKey(rs.getLong("start_key"));
                pageMeta.setEndKey(rs.getLong("end_key"));
                pageMeta.setPageSize(rs.getLong("page_size"));
                pageMetaList.add(pageMeta);
            }
        }
        return pageMetaList;
    }

    public void deleteBooksByPageMeta(PageMeta<Long> pageMeta) throws SQLException {
        try (Connection conn = ds.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement("DELETE FROM books WHERE id >= ? AND id <= ?");
            stmt.setLong(1, pageMeta.getStartKey());
            stmt.setLong(2, pageMeta.getEndKey());
            stmt.executeUpdate();
        }
    }
}
```

次のステートメントは、ページ 1 のデータを削除します。

```java
List<PageMeta<Long>> pageMetaList = bookDAO.getPageMetaList();
if (pageMetaList.size() > 0) {
    bookDAO.deleteBooksByPageMeta(pageMetaList.get(0));
}
```

次のステートメントは、ページングによってすべての書籍データを一括して削除します。

```java
List<PageMeta<Long>> pageMetaList = bookDAO.getPageMetaList();
pageMetaList.forEach((pageMeta) -> {
    try {
        bookDAO.deleteBooksByPageMeta(pageMeta);
    } catch (SQLException e) {
        e.printStackTrace();
    }
});
```

</div>
</SimpleTab>

この方法は、頻繁なデータソート操作によるコンピューティングリソースの浪費を回避することで、バッチ処理の効率を大幅に向上させます。

## 複合主キーテーブルのページングバッチ {#paging-batches-for-composite-primary-key-tables}

### 非クラスタ化インデックステーブル {#non-clustered-index-table}

非クラスター化インデックス テーブル (「非インデックス構成テーブル」とも呼ばれます) の場合、内部フィールド`_tidb_rowid`をページ区切りキーとして使用でき、ページ区切り方法は単一フィールドの主キー テーブルの場合と同じです。

> **ヒント：**
>
> `SHOW CREATE TABLE users;`ステートメントを使用して、テーブルの主キーが[クラスター化インデックス](/clustered-indexes.md)使用しているかどうかを確認できます。

例えば：

```sql
SELECT
    floor((t.row_num - 1) / 1000) + 1 AS page_num,
    min(t._tidb_rowid) AS start_key,
    max(t._tidb_rowid) AS end_key,
    count(*) AS page_size
FROM (
    SELECT _tidb_rowid, row_number () OVER (ORDER BY _tidb_rowid) AS row_num
    FROM users
) t
GROUP BY page_num
ORDER BY page_num;
```

結果は以下のようになります。

    +----------+-----------+---------+-----------+
    | page_num | start_key | end_key | page_size |
    +----------+-----------+---------+-----------+
    |        1 |         1 |    1000 |      1000 |
    |        2 |      1001 |    2000 |      1000 |
    |        3 |      2001 |    3000 |      1000 |
    |        4 |      3001 |    4000 |      1000 |
    |        5 |      4001 |    5000 |      1000 |
    |        6 |      5001 |    6000 |      1000 |
    |        7 |      6001 |    7000 |      1000 |
    |        8 |      7001 |    8000 |      1000 |
    |        9 |      8001 |    9000 |      1000 |
    |       10 |      9001 |    9990 |       990 |
    +----------+-----------+---------+-----------+
    10 rows in set (0.00 sec)

### クラスター化インデックステーブル {#clustered-index-table}

クラスター化インデックス テーブル (「インデックス構成テーブル」とも呼ばれます) の場合、 `concat`関数を使用して複数の列の値をキーとして連結し、ウィンドウ関数を使用してページング情報を照会できます。

この時点ではキーは文字列であり、 `min`と`max`集計関数を介してスライス内の正しい`start_key`と`end_key`を取得するには、文字列の長さが常に同じであることを確認する必要があることに注意してください。文字列連結のフィールドの長さが固定されていない場合は、 `LPAD`関数を使用してパディングできます。

たとえば、 `ratings`テーブル内のデータのページング バッチを次のように実装できます。

以下の文を使用してメタ情報テーブルを作成します。 `bigint`種類の`book_id`と`user_id`を連結したキーは同じ長さに変換できないため、 `LPAD`関数を使用して、 `bigint`の最大ビット 19 に合わせて長さを`0`で埋めます。

```sql
SELECT
    floor((t1.row_num - 1) / 10000) + 1 AS page_num,
    min(mvalue) AS start_key,
    max(mvalue) AS end_key,
    count(*) AS page_size
FROM (
    SELECT
        concat('(', LPAD(book_id, 19, 0), ',', LPAD(user_id, 19, 0), ')') AS mvalue,
        row_number() OVER (ORDER BY book_id, user_id) AS row_num
    FROM ratings
) t1
GROUP BY page_num
ORDER BY page_num;
```

> **注記：**
>
> 上記の SQL 文は`TableFullScan`として実行されます。データ量が多いとクエリが遅くなるため、 [TiFlashを使用する](/tiflash/tiflash-overview.md#use-tiflash)で高速化できます。

結果は以下のようになります。

    +----------+-------------------------------------------+-------------------------------------------+-----------+
    | page_num | start_key                                 | end_key                                   | page_size |
    +----------+-------------------------------------------+-------------------------------------------+-----------+
    |        1 | (0000000000000268996,0000000000092104804) | (0000000000140982742,0000000000374645100) |     10000 |
    |        2 | (0000000000140982742,0000000000456757551) | (0000000000287195082,0000000004053200550) |     10000 |
    |        3 | (0000000000287196791,0000000000191962769) | (0000000000434010216,0000000000237646714) |     10000 |
    |        4 | (0000000000434010216,0000000000375066168) | (0000000000578893327,0000000002167504460) |     10000 |
    |        5 | (0000000000578893327,0000000002457322286) | (0000000000718287668,0000000001502744628) |     10000 |
    ...
    |       29 | (0000000004002523918,0000000000902930986) | (0000000004147203315,0000000004090920746) |     10000 |
    |       30 | (0000000004147421329,0000000000319181561) | (0000000004294004213,0000000003586311166) |      9972 |
    +----------+-------------------------------------------+-------------------------------------------+-----------+
    30 rows in set (0.28 sec)

ページ 1 のすべての評価レコードを削除するには、上記の結果の`start_key`と`end_key`をページ 1 の値に置き換えます。

```sql
SELECT * FROM ratings
WHERE
    (book_id > 268996 AND book_id < 140982742)
    OR (
        book_id = 268996 AND user_id >= 92104804
    )
    OR (
        book_id = 140982742 AND user_id <= 374645100
    )
ORDER BY book_id, user_id;
```

## 助けが必要？ {#need-help}

<CustomContent platform="tidb">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](/support.md)について質問します。

</CustomContent>

<CustomContent platform="tidb-cloud">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](https://support.pingcap.com/)について質問します。

</CustomContent>
