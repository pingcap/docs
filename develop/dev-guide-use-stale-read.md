---
title: Stale Read
summary: 特定の条件下でステイル読み取りを使用してクエリを高速化する方法を学習します。
aliases: ['/ja/tidb/stable/dev-guide-use-stale-read/','/ja/tidbcloud/dev-guide-use-stale-read/']
---

# ステイル読み取り {#stale-read}

ステイル読み取りは、TiDBがTiDBに保存されているデータの履歴バージョンを読み取るために適用するメカニズムです。このメカニズムを使用すると、特定の時刻または指定された時間範囲内で対応する履歴データを読み取ることができ、storageノード間のデータレプリケーションによって発生するレイテンシーを削減できます。Stale ステイル読み取りを使用する場合、TiDBはデータ読み取り用のレプリカをランダムに選択します。つまり、すべてのレプリカがデータ読み取りに利用可能になります。

実際には、 [使用シナリオ](/stale-read.md#usage-scenarios-of-stale-read)に基づいて、TiDB でステイル読み取り を有効にすることが適切かどうかを慎重に検討してください。アプリケーションが非リアルタイム データの読み取りを許容できない場合は、 ステイル読み取りを有効にしないでください。

TiDB は、ステートメント レベル、トランザクション レベル、セッション レベルの 3 つのレベルのステイル読み取りを提供します。

## 導入 {#introduction}

[書店](/develop/dev-guide-bookshop-schema-design.md)アプリケーションでは、次の SQL ステートメントを使用して、最近出版された書籍とその価格を照会できます。

```sql
SELECT id, title, type, price FROM books ORDER BY published_at DESC LIMIT 5;
```

結果は次のようになります。

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

現時点（2022-04-20 15:20:00）のリストでは、 *The Story of Droolius Caesar の*価格は 100.0 です。

同時に、販売者はその本が非常に人気があることに気づき、次の SQL ステートメントを使用して本の価格を 150.0 に引き上げました。

```sql
UPDATE books SET price = 150 WHERE id = 3181093216;
```

結果は次のようになります。

    Query OK, 1 row affected (0.00 sec)
    Rows matched: 1  Changed: 1  Warnings: 0

最新の書籍リストを照会すると、この本の価格が上昇したことがわかります。

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

最新のデータを使用する必要がない場合は、古いデータを返す可能性のあるステイル読み取りを使用してクエリを実行し、強力な一貫性のある読み取り中にデータ複製によって発生するレイテンシーを回避できます。

Bookshopアプリケーションでは、書籍のリアルタイム価格の表示は書籍一覧ページでは必須ではなく、書籍詳細ページと注文ページでのみ必要だと仮定します。Stale ステイル読み取りは、アプリケーション全体の改善に役立ちます。

## ステートメントレベル {#statement-level}

<SimpleTab groupId="language">
<div label="SQL" value="sql">

特定の時間より前の書籍の価格を照会するには、上記のクエリ ステートメントに`AS OF TIMESTAMP <datetime>`句を追加します。

```sql
SELECT id, title, type, price FROM books AS OF TIMESTAMP '2022-04-20 15:20:00' ORDER BY published_at DESC LIMIT 5;
```

結果は次のようになります。

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

正確な時間を指定することに加えて、次のことも指定できます。

-   `AS OF TIMESTAMP NOW() - INTERVAL 10 SECOND` 10 秒前の最新データを照会します。
-   `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS('2016-10-08 16:45:26', '2016-10-08 16:45:29')` `2016-10-08 16:45:26`から`2016-10-08 16:45:29`の間の最新データを照会します。
-   `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS(NOW() -INTERVAL 20 SECOND, NOW())` 20 秒以内に最新のデータを照会します。

指定するタイムスタンプまたは間隔は、現在の時刻より早すぎたり遅すぎたりしないようにしてください。また、 `NOW()`デフォルトで秒精度となります。より高い精度を実現するには、パラメータを追加することができます。例えば、 `NOW(3)`ミリ秒精度となります。詳細については、 [MySQLドキュメント](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_now)参照してください。

期限切れのデータはTiDBで[ガベージコレクション](/garbage-collection-overview.md)リサイクルされ、クリアされるまでの短い期間保持されます。この期間は[GC の有効期間 (デフォルト 10 分)](/system-variables.md#tidb_gc_life_time-new-in-v50)呼ばれます。GCが開始されると、現在の時刻からこの期間を差し引いた値が**GCセーフポイント**として使用されます。GCセーフポイントより前にデータを読み取ろうとすると、TiDBは次のエラーを報告します。

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

次の結果は、 ステイル読み取りによって返された価格が更新前の値である 100.00 であることを示しています。

    The latest book price (before update): 100.00
    The latest book price (after update): 150.00
    The latest book price (maybe stale): 100.00
    WARN: cannot set read timestamp to a future time.
    WARN: GC life time is shorter than transaction duration.

</div>
</SimpleTab>

## トランザクションレベル {#transaction-level}

`START TRANSACTION READ ONLY AS OF TIMESTAMP`ステートメントを使用すると、履歴時間に基づいて読み取り専用トランザクションを開始し、指定された履歴タイムスタンプから履歴データを読み取ります。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

例えば：

```sql
START TRANSACTION READ ONLY AS OF TIMESTAMP NOW() - INTERVAL 5 SECOND;
```

本の最新価格を照会すると、 *『The Story of Droolius Caesar』*の価格が更新前の値である 100.0 のままであることがわかります。

```sql
SELECT id, title, type, price FROM books ORDER BY published_at DESC LIMIT 5;
```

結果は次のようになります。

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

`COMMIT;`文目のトランザクションがコミットされた後、最新のデータを読み取ることができます。

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

トランザクションのヘルパー クラスを定義して、トランザクション レベルでステイル読み取りを有効にするコマンドをヘルパー メソッドとしてカプセル化することができます。

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

次に、 `BookDAO`クラスのトランザクションを通じてステイル読み取り機能を有効にするメソッドを定義します。クエリ文に`AS OF TIMESTAMP`追加する代わりに、このメソッドを使用してクエリを実行します。

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

結果は次のようになります。

    The latest book price (before update): 100.00
    The latest book price (after update): 150.00
    The latest book price (maybe stale): 100.00
    The latest book price (after the transaction commit): 150

</div>
</SimpleTab>

`SET TRANSACTION READ ONLY AS OF TIMESTAMP`ステートメントを使用すると、指定された履歴時間に基づいて、開いているトランザクションまたは次のトランザクションを読み取り専用トランザクションとして設定できます。トランザクションは、指定された履歴時間に基づいて履歴データを読み取ります。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

たとえば、次の`AS OF TIMESTAMP`ステートメントを使用して、進行中のトランザクションを読み取り専用モードに切り替え、5 秒前の履歴データを読み取ることができます。

```sql
SET TRANSACTION READ ONLY AS OF TIMESTAMP NOW() - INTERVAL 5 SECOND;
```

</div>
<div label="Java" value="java">

トランザクションのヘルパー クラスを定義して、トランザクション レベルでステイル読み取りを有効にするコマンドをヘルパー メソッドとしてカプセル化することができます。

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

次に、 `BookDAO`クラスのトランザクションを通じてステイル読み取り機能を有効にするメソッドを定義します。クエリ文に`AS OF TIMESTAMP`追加する代わりに、このメソッドを使用してクエリを実行します。

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

履歴データの読み取りをサポートするため、TiDBはv5.4以降、新しいシステム変数`tidb_read_staleness`を導入しました。この変数を使用して、現在のセッションで読み取り可能な履歴データの範囲を設定できます。データ型は`int` 、スコープは`SESSION`です。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

セッションでステイル読み取りを有効にする:

```sql
SET @@tidb_read_staleness="-5";
```

たとえば、値が`-5`に設定され、TiKV またはTiFlash に対応する履歴データがある場合、TiDB は 5 秒の時間範囲内で可能な限り新しいタイムスタンプを選択します。

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
-   [`AS OF TIMESTAMP`句を使用して履歴データを読み取る](/as-of-timestamp.md)
-   [`tidb_read_staleness`システム変数を使用して履歴データを読み取る](/tidb-read-staleness.md)

## ヘルプが必要ですか? {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに問い合わせてください。
-   [TiDB Cloudのサポートチケットを送信する](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDBセルフマネージドのサポートチケットを送信する](/support.md)
