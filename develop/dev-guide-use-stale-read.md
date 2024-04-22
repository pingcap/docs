---
title: Stale Read
summary: TiDBのステイル読み取りは、データの履歴バージョンを読み取るためのメカニズムです。特定の時刻や時間範囲内で履歴データを読み取ることができ、データレプリケーションによるレイテンシーを節約できます。ただし、リアルタイムデータの読み取りが必要な場合は慎重に検討してください。ステートメント、トランザクション、セッションの3つのレベルでステイル読み取りを提供しています。データの読み取りをサポートするために、新しいシステム変数`tidb_read_staleness`を導入しました。
---

# ステイル読み取り {#stale-read}

ステイル読み取り は、TiDB に保存されているデータの履歴バージョンを読み取るために TiDB が適用するメカニズムです。このメカニズムを使用すると、特定の時刻または指定された時間範囲内で対応する履歴データを読み取ることができるため、storageノード間のデータ レプリケーションによって生じるレイテンシーを節約できます。 ステイル読み取りを使用している場合、TiDB はデータ読み取り用のレプリカをランダムに選択します。これは、すべてのレプリカがデータ読み取りに使用できることを意味します。

実際には、 [使用シナリオ](/stale-read.md#usage-scenarios-of-stale-read)に基づいて TiDB でステイル読み取り を有効にすることが適切かどうかを慎重に検討してください。アプリケーションが非リアルタイム データの読み取りを許容できない場合は、 ステイル読み取り を有効にしないでください。

TiDB は、ステートメント レベル、トランザクション レベル、セッション レベルの 3 つのレベルのステイル読み取りを提供します。

## 導入 {#introduction}

[書店](/develop/dev-guide-bookshop-schema-design.md)アプリケーションでは、次の SQL ステートメントを使用して、最新の出版された書籍とその価格をクエリできます。

```sql
SELECT id, title, type, price FROM books ORDER BY published_at DESC LIMIT 5;
```

結果は次のとおりです。

    +------------+------------------------------+-----------------------+--------+
    | id         | title                        | type                  | price  |
    +------------+------------------------------+-----------------------+--------+
    | 3181093216 | The Story of Droolius Caesar | Novel                 | 100.00 |
    | 1064253862 | Collin Rolfson               | Education & Reference |  92.85 |
    | 1748583991 | The Documentary of cat       | Magazine              | 159.75 |
    |  893930596 | Myrl Hills                   | Education & Reference | 356.85 |
    | 3062833277 | Keven Wyman                  | Life                  | 477.91 |
    +------------+------------------------------+-----------------------+--------+
    5 rows in set (0.02 sec)

現時点(2022-04-20 15:20:00)のリストでは、*ドロリウス・シーザー物語*の価格は100.0です。

同時に、売り手はその本が非常に人気があることを知り、次の SQL ステートメントを通じて本の価格を 150.0 に値上げしました。

```sql
UPDATE books SET price = 150 WHERE id = 3181093216;
```

結果は次のとおりです。

    Query OK, 1 row affected (0.00 sec)
    Rows matched: 1  Changed: 1  Warnings: 0

最新の書籍リストをクエリすると、この書籍の価格が上昇していることがわかります。

    +------------+------------------------------+-----------------------+--------+
    | id         | title                        | type                  | price  |
    +------------+------------------------------+-----------------------+--------+
    | 3181093216 | The Story of Droolius Caesar | Novel                 | 150.00 |
    | 1064253862 | Collin Rolfson               | Education & Reference |  92.85 |
    | 1748583991 | The Documentary of cat       | Magazine              | 159.75 |
    |  893930596 | Myrl Hills                   | Education & Reference | 356.85 |
    | 3062833277 | Keven Wyman                  | Life                  | 477.91 |
    +------------+------------------------------+-----------------------+--------+
    5 rows in set (0.01 sec)

最新のデータを使用する必要がない場合は、 ステイル読み取り を使用してクエリを実行すると、古いデータが返される可能性があり、強整合性読み取り中のデータ レプリケーションによって発生するレイテンシーを回避できます。

Bookshop アプリケーションでは、書籍のリアルタイム価格は書籍リスト ページでは必要なく、書籍の詳細ページと注文ページでのみ必要であると仮定します。 ステイル読み取り を使用すると、アプリケーション全体を改善できます。

## ステートメントレベル {#statement-level}

<SimpleTab groupId="language">
<div label="SQL" value="sql">

特定の時刻より前の本の価格をクエリするには、上記のクエリ ステートメントに`AS OF TIMESTAMP <datetime>`句を追加します。

```sql
SELECT id, title, type, price FROM books AS OF TIMESTAMP '2022-04-20 15:20:00' ORDER BY published_at DESC LIMIT 5;
```

結果は次のとおりです。

    +------------+------------------------------+-----------------------+--------+
    | id         | title                        | type                  | price  |
    +------------+------------------------------+-----------------------+--------+
    | 3181093216 | The Story of Droolius Caesar | Novel                 | 100.00 |
    | 1064253862 | Collin Rolfson               | Education & Reference |  92.85 |
    | 1748583991 | The Documentary of cat       | Magazine              | 159.75 |
    |  893930596 | Myrl Hills                   | Education & Reference | 356.85 |
    | 3062833277 | Keven Wyman                  | Life                  | 477.91 |
    +------------+------------------------------+-----------------------+--------+
    5 rows in set (0.01 sec)

正確な時刻を指定するだけでなく、次のことも指定できます。

-   `AS OF TIMESTAMP NOW() - INTERVAL 10 SECOND` 10 秒前の最新データをクエリします。
-   `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS('2016-10-08 16:45:26', '2016-10-08 16:45:29')` `2016-10-08 16:45:26`から`2016-10-08 16:45:29`までの最新のデータをクエリします。
-   `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS(NOW() -INTERVAL 20 SECOND, NOW())` 20 秒以内の最新データをクエリします。

指定するタイムスタンプまたは間隔は、現在時刻より早すぎたり遅すぎたりすることはできないことに注意してください。さらに、デフォルトの`NOW()`秒精度になります。より高い精度を実現するには、ミリ秒の精度に`NOW(3)`使用するなど、パラメーターを追加できます。詳細については、 [MySQL ドキュメント](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_now)を参照してください。

期限切れのデータは TiDB で[ガベージコレクション](/garbage-collection-overview.md)によってリサイクルされ、データは消去されるまで短期間保持されます。この期間を[GC ライフタイム (デフォルトは 10 分)](/system-variables.md#tidb_gc_life_time-new-in-v50)と呼びます。 GC が開始されると、現在時刻から期間を引いた時間が**GC セーフ ポイント**として使用されます。 GC セーフ ポイントの前にデータを読み取ろうとすると、TiDB は次のエラーを報告します。

    ERROR 9006 (HY000): GC life time is shorter than transaction duration...

指定されたタイムスタンプが将来の時刻である場合、TiDB は次のエラーを報告します。

    ERROR 9006 (HY000): cannot set read timestamp to a future time.

</div>
<div label="Java" value="java">

```java
public class BookDAO {

    // Omit some code...

    public List<Book> getTop5LatestBooks() throws SQLException {
        List<Book> books = new ArrayList<>();
        try (Connection conn = ds.getConnection()) {
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("""
            SELECT id, title, type, price FROM books ORDER BY published_at DESC LIMIT 5;
            """);
            while (rs.next()) {
                Book book = new Book();
                book.setId(rs.getLong("id"));
                book.setTitle(rs.getString("title"));
                book.setType(rs.getString("type"));
                book.setPrice(rs.getDouble("price"));
                books.add(book);
            }
        }
        return books;
    }

    public void updateBookPriceByID(Long id, Double price) throws SQLException {
        try (Connection conn = ds.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement("""
            UPDATE books SET price = ? WHERE id = ?;
            """);
            stmt.setDouble(1, price);
            stmt.setLong(2, id);
            int affects = stmt.executeUpdate();
            if (affects == 0) {
                throw new SQLException("Failed to update the book with id: " + id);
            }
        }
    }

    public List<Book> getTop5LatestBooksWithStaleRead(Integer seconds) throws SQLException {
        List<Book> books = new ArrayList<>();
        try (Connection conn = ds.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement("""
            SELECT id, title, type, price FROM books AS OF TIMESTAMP NOW() - INTERVAL ? SECOND ORDER BY published_at DESC LIMIT 5;
            """);
            stmt.setInt(1, seconds);
            ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                Book book = new Book();
                book.setId(rs.getLong("id"));
                book.setTitle(rs.getString("title"));
                book.setType(rs.getString("type"));
                book.setPrice(rs.getDouble("price"));
                books.add(book);
            }
        } catch (SQLException e) {
            if ("HY000".equals(e.getSQLState()) && e.getErrorCode() == 1105) {
                System.out.println("WARN: cannot set read timestamp to a future time.");
            } else if ("HY000".equals(e.getSQLState()) && e.getErrorCode() == 9006) {
                System.out.println("WARN: GC life time is shorter than transaction duration.");
            } else {
                throw e;
            }
        }
        return books;
    }
}
```

```java
List<Book> top5LatestBooks = bookDAO.getTop5LatestBooks();

if (top5LatestBooks.size() > 0) {
    System.out.println("The latest book price (before update): " + top5LatestBooks.get(0).getPrice());

    Book book = top5LatestBooks.get(0);
    bookDAO.updateBookPriceByID(book.getId(), book.price + 10);

    top5LatestBooks = bookDAO.getTop5LatestBooks();
    System.out.println("The latest book price (after update): " + top5LatestBooks.get(0).getPrice());

    // Use the stale read.
    top5LatestBooks = bookDAO.getTop5LatestBooksWithStaleRead(5);
    System.out.println("The latest book price (maybe stale): " + top5LatestBooks.get(0).getPrice());

    // Try to stale read the data at the future time.
    bookDAO.getTop5LatestBooksWithStaleRead(-5);

    // Try to stale read the data before 20 minutes.
    bookDAO.getTop5LatestBooksWithStaleRead(20 * 60);
}
```

次の結果は、 ステイル読み取りによって返される価格が 100.00 (更新前の値) であることを示しています。

    The latest book price (before update): 100.00
    The latest book price (after update): 150.00
    The latest book price (maybe stale): 100.00
    WARN: cannot set read timestamp to a future time.
    WARN: GC life time is shorter than transaction duration.

</div>
</SimpleTab>

## トランザクションレベル {#transaction-level}

`START TRANSACTION READ ONLY AS OF TIMESTAMP`ステートメントを使用すると、履歴時刻に基づいて読み取り専用トランザクションを開始でき、指定された履歴タイムスタンプから履歴データを読み取ります。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

例えば：

```sql
START TRANSACTION READ ONLY AS OF TIMESTAMP NOW() - INTERVAL 5 SECOND;
```

この本の最新の価格をクエリすると、 *The Story of Droolius Caesar*の価格が更新前の値である 100.0 のままであることがわかります。

```sql
SELECT id, title, type, price FROM books ORDER BY published_at DESC LIMIT 5;
```

結果は次のとおりです。

    +------------+------------------------------+-----------------------+--------+
    | id         | title                        | type                  | price  |
    +------------+------------------------------+-----------------------+--------+
    | 3181093216 | The Story of Droolius Caesar | Novel                 | 100.00 |
    | 1064253862 | Collin Rolfson               | Education & Reference |  92.85 |
    | 1748583991 | The Documentary of cat       | Magazine              | 159.75 |
    |  893930596 | Myrl Hills                   | Education & Reference | 356.85 |
    | 3062833277 | Keven Wyman                  | Life                  | 477.91 |
    +------------+------------------------------+-----------------------+--------+
    5 rows in set (0.01 sec)

`COMMIT;`ステートメントのトランザクションがコミットされた後、最新のデータを読み取ることができます。

    +------------+------------------------------+-----------------------+--------+
    | id         | title                        | type                  | price  |
    +------------+------------------------------+-----------------------+--------+
    | 3181093216 | The Story of Droolius Caesar | Novel                 | 150.00 |
    | 1064253862 | Collin Rolfson               | Education & Reference |  92.85 |
    | 1748583991 | The Documentary of cat       | Magazine              | 159.75 |
    |  893930596 | Myrl Hills                   | Education & Reference | 356.85 |
    | 3062833277 | Keven Wyman                  | Life                  | 477.91 |
    +------------+------------------------------+-----------------------+--------+
    5 rows in set (0.01 sec)

</div>
<div label="Java" value="java">

トランザクションのヘルパー クラスを定義できます。このクラスは、ヘルパー メソッドとしてトランザクション レベルでステイル読み取りを有効にするコマンドをカプセル化します。

```java
public static class StaleReadHelper {

    public static void startTxnWithStaleRead(Connection conn, Integer seconds) throws SQLException {
        conn.setAutoCommit(false);
        PreparedStatement stmt = conn.prepareStatement(
            "START TRANSACTION READ ONLY AS OF TIMESTAMP NOW() - INTERVAL ? SECOND;"
        );
        stmt.setInt(1, seconds);
        stmt.execute();
    }

}
```

次に、 `BookDAO`クラスのトランザクションを通じてステイル読み取り機能を有効にするメソッドを定義します。クエリ ステートメントに`AS OF TIMESTAMP`追加する代わりに、メソッドを使用してクエリを実行します。

```java
public class BookDAO {

    // Omit some code...

    public List<Book> getTop5LatestBooksWithTxnStaleRead(Integer seconds) throws SQLException {
        List<Book> books = new ArrayList<>();
        try (Connection conn = ds.getConnection()) {
            // Start a read only transaction.
            TxnHelper.startTxnWithStaleRead(conn, seconds);

            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("""
            SELECT id, title, type, price FROM books ORDER BY published_at DESC LIMIT 5;
            """);
            while (rs.next()) {
                Book book = new Book();
                book.setId(rs.getLong("id"));
                book.setTitle(rs.getString("title"));
                book.setType(rs.getString("type"));
                book.setPrice(rs.getDouble("price"));
                books.add(book);
            }

            // Commit transaction.
            conn.commit();
        } catch (SQLException e) {
            if ("HY000".equals(e.getSQLState()) && e.getErrorCode() == 1105) {
                System.out.println("WARN: cannot set read timestamp to a future time.");
            } else if ("HY000".equals(e.getSQLState()) && e.getErrorCode() == 9006) {
                System.out.println("WARN: GC life time is shorter than transaction duration.");
            } else {
                throw e;
            }
        }
        return books;
    }
}
```

```java
List<Book> top5LatestBooks = bookDAO.getTop5LatestBooks();

if (top5LatestBooks.size() > 0) {
    System.out.println("The latest book price (before update): " + top5LatestBooks.get(0).getPrice());

    Book book = top5LatestBooks.get(0);
    bookDAO.updateBookPriceByID(book.getId(), book.price + 10);

    top5LatestBooks = bookDAO.getTop5LatestBooks();
    System.out.println("The latest book price (after update): " + top5LatestBooks.get(0).getPrice());

    // Use the stale read.
    top5LatestBooks = bookDAO.getTop5LatestBooksWithTxnStaleRead(5);
    System.out.println("The latest book price (maybe stale): " + top5LatestBooks.get(0).getPrice());

    // After the stale read transaction is committed.
    top5LatestBooks = bookDAO.getTop5LatestBooks();
    System.out.println("The latest book price (after the transaction commit): " + top5LatestBooks.get(0).getPrice());
}
```

結果は次のとおりです。

    The latest book price (before update): 100.00
    The latest book price (after update): 150.00
    The latest book price (maybe stale): 100.00
    The latest book price (after the transaction commit): 150

</div>
</SimpleTab>

`SET TRANSACTION READ ONLY AS OF TIMESTAMP`ステートメントを使用すると、指定された履歴時刻に基づいて、開かれたトランザクションまたは次のトランザクションを読み取り専用トランザクションに設定できます。トランザクションは、指定された履歴時間に基づいて履歴データを読み取ります。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

たとえば、次の`AS OF TIMESTAMP`ステートメントを使用すると、進行中のトランザクションを読み取り専用モードに切り替え、5 秒前の履歴データを読み取ることができます。

```sql
SET TRANSACTION READ ONLY AS OF TIMESTAMP NOW() - INTERVAL 5 SECOND;
```

</div>
<div label="Java" value="java">

トランザクションのヘルパー クラスを定義できます。このクラスは、ヘルパー メソッドとしてトランザクション レベルでステイル読み取りを有効にするコマンドをカプセル化します。

```java
public static class TxnHelper {

    public static void setTxnWithStaleRead(Connection conn, Integer seconds) throws SQLException {
        PreparedStatement stmt = conn.prepareStatement(
            "SET TRANSACTION READ ONLY AS OF TIMESTAMP NOW() - INTERVAL ? SECOND;"
        );
        stmt.setInt(1, seconds);
        stmt.execute();
    }

}
```

次に、 `BookDAO`クラスのトランザクションを通じてステイル読み取り機能を有効にするメソッドを定義します。クエリ ステートメントに`AS OF TIMESTAMP`追加する代わりに、メソッドを使用してクエリを実行します。

```java
public class BookDAO {

    // Omit some code...

    public List<Book> getTop5LatestBooksWithTxnStaleRead2(Integer seconds) throws SQLException {
        List<Book> books = new ArrayList<>();
        try (Connection conn = ds.getConnection()) {
            StaleReadHelper.setTxnWithStaleRead(conn, seconds);

            // Start a read only transaction.
            conn.setAutoCommit(false);

            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("""
            SELECT id, title, type, price FROM books ORDER BY published_at DESC LIMIT 5;
            """);
            while (rs.next()) {
                Book book = new Book();
                book.setId(rs.getLong("id"));
                book.setTitle(rs.getString("title"));
                book.setType(rs.getString("type"));
                book.setPrice(rs.getDouble("price"));
                books.add(book);
            }

            // Commit transaction.
            conn.commit();
        } catch (SQLException e) {
            if ("HY000".equals(e.getSQLState()) && e.getErrorCode() == 1105) {
                System.out.println("WARN: cannot set read timestamp to a future time.");
            } else if ("HY000".equals(e.getSQLState()) && e.getErrorCode() == 9006) {
                System.out.println("WARN: GC life time is shorter than transaction duration.");
            } else {
                throw e;
            }
        }
        return books;
    }
}
```

</div>
</SimpleTab>

## セッションレベル {#session-level}

履歴データの読み取りをサポートするために、TiDB は v5.4 以降、新しいシステム変数`tidb_read_staleness`を導入しました。これを使用して、現在のセッションで読み取りを許可される履歴データの範囲を設定できます。データ型は`int`で、スコープは`SESSION`です。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

セッションでステイル読み取りを有効にします。

```sql
SET @@tidb_read_staleness="-5";
```

たとえば、値が`-5`に設定されており、TiKV またはTiFlashに対応する履歴データがある場合、TiDB は 5 秒の時間範囲内でできるだけ新しいタイムスタンプを選択します。

セッションでステイル読み取りを無効にします。

```sql
set @@tidb_read_staleness="";
```

</div>
<div label="Java" value="java">

```java
public static class StaleReadHelper{

    public static void enableStaleReadOnSession(Connection conn, Integer seconds) throws SQLException {
        PreparedStatement stmt = conn.prepareStatement(
            "SET @@tidb_read_staleness= ?;"
        );
        stmt.setString(1, String.format("-%d", seconds));
        stmt.execute();
    }

    public static void disableStaleReadOnSession(Connection conn) throws SQLException {
        PreparedStatement stmt = conn.prepareStatement(
            "SET @@tidb_read_staleness=\"\";"
        );
        stmt.execute();
    }

}
```

</div>
</SimpleTab>

## 続きを読む {#read-more}

-   [ステイル読み取りの使用シナリオ](/stale-read.md)
-   [`AS OF TIMESTAMP`句を使用した履歴データの読み取り](/as-of-timestamp.md)
-   [`tidb_read_staleness`システム変数を使用した履歴データの読み取り](/tidb-read-staleness.md)
