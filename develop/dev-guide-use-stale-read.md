---
title: Stale Read
summary: Learn how to use Stale Read to accelerate queries under certain conditions.
---

# 古い読み取り {#stale-read}

Stale Readは、TiDBがTiDBに保存されているデータの履歴バージョンを読み取るために適用するメカニズムです。このメカニズムを使用すると、特定の時間または指定した時間範囲内で対応する履歴データを読み取ることができるため、ストレージノード間のデータレプリケーションによって発生する遅延を節約できます。スティールリードを使用している場合、TiDBはデータ読み取り用のレプリカをランダムに選択します。これは、すべてのレプリカがデータ読み取りに使用できることを意味します。

実際には、 [使用シナリオ](/stale-read.md#usage-scenarios-of-stale-read)に基づいてTiDBでStaleReadを有効にすることが適切かどうかを慎重に検討してください。アプリケーションが非リアルタイムデータの読み取りに耐えられない場合は、StaleReadを有効にしないでください。

TiDBは、ステートメントレベル、トランザクションレベル、およびセッションレベルの3つのレベルの古い読み取りを提供します。

## 序章 {#introduction}

[書店](/develop/dev-guide-bookshop-schema-design.md)のアプリケーションでは、次のSQLステートメントを使用して、最新の出版された書籍とその価格を照会できます。

{{< copyable "" >}}

```sql
SELECT id, title, type, price FROM books ORDER BY published_at DESC LIMIT 5;
```

結果は次のとおりです。

```
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
```

この時点（2022-04-20 15:20:00）のリストでは、 *The Story ofDrooliusCaesar*の価格は100.0です。

同時に、売り手はその本が非常に人気があることを発見し、次のSQLステートメントを通じて本の価格を150.0に引き上げました。

{{< copyable "" >}}

```sql
UPDATE books SET price = 150 WHERE id = 3181093216;
```

結果は次のとおりです。

```
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0
```

最新の書籍リストを照会すると、この書籍の価格が上昇していることがわかります。

```
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
```

最新のデータを使用する必要がない場合は、古いデータを返す可能性のあるStale Readを使用してクエリを実行し、一貫性の高い読み取り中にデータレプリケーションによって発生する遅延を回避できます。

Bookshopアプリケーションでは、本のリアルタイム価格は本のリストページでは必要なく、本の詳細と注文ページでのみ必要であると想定しています。 Stale Readは、アプリケーション全体を改善するために使用できます。

## ステートメントレベル {#statement-level}

<SimpleTab>
<div label="SQL">

特定の時間より前の本の価格を照会するには、上記の照会ステートメントに`AS OF TIMESTAMP <datetime>`節を追加します。

{{< copyable "" >}}

```sql
SELECT id, title, type, price FROM books AS OF TIMESTAMP '2022-04-20 15:20:00' ORDER BY published_at DESC LIMIT 5;
```

結果は次のとおりです。

```
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
```

正確な時刻を指定することに加えて、以下を指定することもできます。

-   `AS OF TIMESTAMP NOW() - INTERVAL 10 SECOND`は、10秒前の最新データを照会します。
-   `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS('2016-10-08 16:45:26', '2016-10-08 16:45:29')`は、 `2016-10-08 16:45:26`から`2016-10-08 16:45:29`までの最新データを照会します。
-   `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS(NOW() -INTERVAL 20 SECOND, NOW())`は、20秒以内に最新のデータを照会します。

指定されたタイムスタンプまたは間隔は、現在の時刻より早すぎたり遅すぎたりしてはならないことに注意してください。

期限切れのデータはTiDBで[ガベージコレクション](/garbage-collection-overview.md)ずつリサイクルされ、データはクリアされる前に短期間保持されます。期間は[GCライフタイム（デフォルトは10分）](/system-variables.md#tidb_gc_life_time-new-in-v50)と呼ばれます。 GCが開始すると、現在の時刻から期間を引いたものが**GCセーフポイント**として使用されます。 GC Safe Pointの前にデータを読み取ろうとすると、TiDBは次のエラーを報告します。

```
ERROR 9006 (HY000): GC life time is shorter than transaction duration...
```

指定されたタイムスタンプが将来の時刻である場合、TiDBは次のエラーを報告します。

```
ERROR 9006 (HY000): cannot set read timestamp to a future time.
```

</div>
<div label="Java">

{{< copyable "" >}}

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

{{< copyable "" >}}

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

次の結果は、Stale Readによって返される価格が100.00であることを示しています。これは、更新前の値です。

```
The latest book price (before update): 100.00
The latest book price (after update): 150.00
The latest book price (maybe stale): 100.00
WARN: cannot set read timestamp to a future time.
WARN: GC life time is shorter than transaction duration.
```

</div>
</SimpleTab>

## トランザクションレベル {#transaction-level}

`START TRANSACTION READ ONLY AS OF TIMESTAMP`ステートメントを使用すると、履歴時間に基づいて読み取り専用トランザクションを開始できます。これにより、指定された履歴タイムスタンプから履歴データが読み取られます。

<SimpleTab>
<div label="SQL">

例えば：

{{< copyable "" >}}

```sql
START TRANSACTION READ ONLY AS OF TIMESTAMP NOW() - INTERVAL 5 SECOND;
```

この本の最新の価格を照会すると、 *The Story of Droolius Caesar*の価格がまだ100.0であることがわかります。これは、更新前の値です。

{{< copyable "" >}}

```sql
SELECT id, title, type, price FROM books ORDER BY published_at DESC LIMIT 5;
```

結果は次のとおりです。

```
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
```

`COMMIT;`ステートメントのトランザクションがコミットされた後、最新のデータを読み取ることができます。

```
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
```

</div>
<div label="Java">

トランザクションのヘルパークラスを定義できます。これは、コマンドをカプセル化して、トランザクションレベルでヘルパーメソッドとしてStaleReadを有効にします。

{{< copyable "" >}}

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

次に、 `BookDAO`クラスのトランザクションを介して古い読み取り機能を有効にするメソッドを定義します。クエリステートメントに`AS OF TIMESTAMP`を追加する代わりに、メソッドを使用してクエリを実行します。

{{< copyable "" >}}

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

{{< copyable "" >}}

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

```
The latest book price (before update): 100.00
The latest book price (after update): 150.00
The latest book price (maybe stale): 100.00
The latest book price (after the transaction commit): 150
```

</div>
</SimpleTab>

`SET TRANSACTION READ ONLY AS OF TIMESTAMP`ステートメントを使用すると、開いたトランザクションまたは次のトランザクションを、指定した履歴時間に基づいて読み取り専用トランザクションに設定できます。トランザクションは、提供された履歴時間に基づいて履歴データを読み取ります。

<SimpleTab>
<div label="SQL">

たとえば、次の`AS OF TIMESTAMP`のステートメントを使用して、進行中のトランザクションを読み取り専用モードに切り替え、5秒前の履歴データを読み取ることができます。

```sql
SET TRANSACTION READ ONLY AS OF TIMESTAMP NOW() - INTERVAL 5 SECOND;
```

</div>
<div label="Java">

トランザクションのヘルパークラスを定義できます。これは、コマンドをカプセル化して、トランザクションレベルでヘルパーメソッドとしてStaleReadを有効にします。

{{< copyable "" >}}

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

次に、 `BookDAO`クラスのトランザクションを介して古い読み取り機能を有効にするメソッドを定義します。クエリステートメントに`AS OF TIMESTAMP`を追加する代わりに、メソッドを使用してクエリを実行します。

{{< copyable "" >}}

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

履歴データの読み取りをサポートするために、TiDBはv5.4以降に新しいシステム変数`tidb_read_staleness`を導入しました。これを使用して、現在のセッションが読み取ることを許可される履歴データの範囲を設定できます。そのデータ型は`int`で、スコープは`SESSION`です。

<SimpleTab>
<div label="SQL">

セッションで古い読み取りを有効にします。

{{< copyable "" >}}

```sql
SET @@tidb_read_staleness="-5";
```

たとえば、値が`-5`に設定されていて、TiKVに対応する履歴データがある場合、TiDBは5秒の時間範囲内で可能な限り新しいタイムスタンプを選択します。

セッションで古い読み取りを無効にします。

{{< copyable "" >}}

```sql
set @@tidb_read_staleness="";
```

</div>
<div label="Java">

{{< copyable "" >}}

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

-   [古い読み取りの使用シナリオ](/stale-read.md)
-   [`AS OF TIMESTAMP`句を使用して履歴データを読み取る](/as-of-timestamp.md)
-   [`tidb_read_staleness`システム変数を使用して履歴データを読み取る](/tidb-read-staleness.md)
