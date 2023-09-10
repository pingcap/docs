---
title: Prepared Statements
summary: Learn about how to use the TiDB prepared statements.
---

# 準備されたステートメント {#prepared-statements}

[プリペアドステートメント](/sql-statements/sql-statement-prepare.md)パラメータのみが異なる複数の SQL ステートメントをテンプレート化します。 SQL ステートメントをパラメーターから分離します。これを使用すると、SQL ステートメントの次の側面を改善できます。

-   **Security**: パラメータとステートメントが分離されているため、 [SQLインジェクション](https://en.wikipedia.org/wiki/SQL_injection)攻撃のリスクが回避されます。
-   **パフォーマンス**: ステートメントは TiDBサーバー上で事前に解析されるため、後続の実行にはパラメーターのみが渡され、SQL ステートメント全体の解析、SQL ステートメント文字列の結合、およびネットワーク送信のコストが節約されます。

ほとんどのアプリケーションでは、SQL ステートメントを列挙できます。限られた数の SQL ステートメントを使用して、アプリケーション全体のデータ クエリを実行できます。したがって、プリペアドステートメントを使用することがベスト プラクティスです。

## SQL 構文 {#sql-syntax}

このセクションでは、プリペアドステートメントを作成、実行、および削除するための SQL 構文について説明します。

### プリペアドステートメントを作成する {#create-a-prepared-statement}

```sql
PREPARE {prepared_statement_name} FROM '{prepared_statement_sql}';
```

|            パラメータ名           |                説明                |
| :-------------------------: | :------------------------------: |
| `{prepared_statement_name}` |          プリペアドステートメントの名前         |
|  `{prepared_statement_sql}` | プレースホルダーとして疑問符を付けプリペアドステートメントSQL |

詳細については[PREPARE 文](/sql-statements/sql-statement-prepare.md)参照してください。

### プリペアドステートメントを使用する {#use-the-prepared-statement}

プリペアドステートメントは**ユーザー変数を**パラメータとしてのみ使用できるため、 [`EXECUTE`文](/sql-statements/sql-statement-execute.md)がプリペアドステートメントを呼び出す前に、 [`SET`ステートメント](/sql-statements/sql-statement-set-variable.md)を使用して変数を設定します。

```sql
SET @{parameter_name} = {parameter_value};
EXECUTE {prepared_statement_name} USING @{parameter_name};
```

|            パラメータ名           |                                          説明                                          |
| :-------------------------: | :----------------------------------------------------------------------------------: |
|      `{parameter_name}`     |                                        ユーザー変数名                                       |
|     `{parameter_value}`     |                                       ユーザー変数の値                                       |
| `{prepared_statement_name}` | 前処理ステートメントの名前[プリペアドステートメントを作成する](#create-a-prepared-statement)で定義された名前と同じである必要があります。 |

詳細については[`EXECUTE`文](/sql-statements/sql-statement-execute.md)参照してください。

### プリペアドステートメントを削除します {#delete-the-prepared-statement}

```sql
DEALLOCATE PREPARE {prepared_statement_name};
```

|            パラメータ名           |                                          説明                                          |
| :-------------------------: | :----------------------------------------------------------------------------------: |
| `{prepared_statement_name}` | 前処理ステートメントの名前[プリペアドステートメントを作成する](#create-a-prepared-statement)で定義された名前と同じである必要があります。 |

詳細については[`DEALLOCATE`文](/sql-statements/sql-statement-deallocate.md)参照してください。

## 例 {#examples}

このセクションでは、プリペアド ステートメントの 2 つの例 ( `SELECT`データと`INSERT`データ) について説明します。

### <code>SELECT</code>例 {#code-select-code-example}

たとえば、 [`bookshop`アプリケーション](/develop/dev-guide-bookshop-schema-design.md#books-table)のうち`id = 1`を含む書籍をクエリする必要があります。

<SimpleTab groupId="language">
  <div label="SQL" value="sql">
    ```sql
    PREPARE `books_query` FROM 'SELECT * FROM `books` WHERE `id` = ?';
    ```

    実行結果:

    ```
    Query OK, 0 rows affected (0.01 sec)
    ```

    ```sql
    SET @id = 1;
    ```

    実行結果:

    ```
    Query OK, 0 rows affected (0.04 sec)
    ```

    ```sql
    EXECUTE `books_query` USING @id;
    ```

    実行結果:

    ```
    +---------+---------------------------------+--------+---------------------+-------+--------+
    | id      | title                           | type   | published_at        | stock | price  |
    +---------+---------------------------------+--------+---------------------+-------+--------+
    | 1       | The Adventures of Pierce Wehner | Comics | 1904-06-06 20:46:25 |   586 | 411.66 |
    +---------+---------------------------------+--------+---------------------+-------+--------+
    1 row in set (0.05 sec)
    ```
  </div>

  <div label="Java" value="java">
    ```java
    // ds is an entity of com.mysql.cj.jdbc.MysqlDataSource
    try (Connection connection = ds.getConnection()) {
        PreparedStatement preparedStatement = connection.prepareStatement("SELECT * FROM `books` WHERE `id` = ?");
        preparedStatement.setLong(1, 1);

        ResultSet res = preparedStatement.executeQuery();
        if(!res.next()) {
            System.out.println("No books in the table with id 1");
        } else {
            // got book's info, which id is 1
            System.out.println(res.getLong("id"));
            System.out.println(res.getString("title"));
            System.out.println(res.getString("type"));
        }
    } catch (SQLException e) {
        e.printStackTrace();
    }
    ```
  </div>
</SimpleTab>

### <code>INSERT</code>例 {#code-insert-code-example}

例として[`books`テーブル](/develop/dev-guide-bookshop-schema-design.md#books-table)を使用すると、 `title = TiDB Developer Guide` 、 `type = Science & Technology` 、 `stock = 100` 、 `price = 0.0` 、および`published_at = NOW()` (挿入の現在の時刻) を持つ本を挿入する必要があります。 `books`テーブルの**主キー**に`AUTO_RANDOM`属性を指定する必要がないことに注意してください。データの挿入の詳細については、 [データの挿入](/develop/dev-guide-insert-data.md)を参照してください。

<SimpleTab groupId="language">
  <div label="SQL" value="sql">
    ```sql
    PREPARE `books_insert` FROM 'INSERT INTO `books` (`title`, `type`, `stock`, `price`, `published_at`) VALUES (?, ?, ?, ?, ?);';
    ```

    実行結果:

    ```
    Query OK, 0 rows affected (0.03 sec)
    ```

    ```sql
    SET @title = 'TiDB Developer Guide';
    SET @type = 'Science & Technology';
    SET @stock = 100;
    SET @price = 0.0;
    SET @published_at = NOW();
    ```

    実行結果:

    ```
    Query OK, 0 rows affected (0.04 sec)
    ```

    ```sql
    EXECUTE `books_insert` USING @title, @type, @stock, @price, @published_at;
    ```

    実行結果:

    ```
    Query OK, 1 row affected (0.03 sec)
    ```
  </div>

  <div label="Java" value="java">
    ```java
    try (Connection connection = ds.getConnection()) {
        String sql = "INSERT INTO `books` (`title`, `type`, `stock`, `price`, `published_at`) VALUES (?, ?, ?, ?, ?);";
        PreparedStatement preparedStatement = connection.prepareStatement(sql);

        preparedStatement.setString(1, "TiDB Developer Guide");
        preparedStatement.setString(2, "Science & Technology");
        preparedStatement.setInt(3, 100);
        preparedStatement.setBigDecimal(4, new BigDecimal("0.0"));
        preparedStatement.setTimestamp(5, new Timestamp(Calendar.getInstance().getTimeInMillis()));

        preparedStatement.executeUpdate();
    } catch (SQLException e) {
        e.printStackTrace();
    }
    ```

    ご覧のとおり、JDBC はプリペアド ステートメントのライフ サイクルの制御に役立ち、アプリケーションでプリペアド ステートメントを手動で作成、使用、または削除する必要はありません。ただし、TiDB は MySQL と互換性があるため、クライアント側で MySQL JDBC Driverを使用するためのデフォルト設定では、***サーバー側の***プリペアドステートメントオプションが有効ではなく、クライアント側のプリペアドステートメントが使用されることに注意してください。

    次の構成は、JDBC で TiDB サーバー側のプリペアド ステートメントを使用するのに役立ちます。

    |          パラメータ          |                  手段                 |            推奨シナリオ           |        推奨されるコンフィグレーション        |
    | :---------------------: | :---------------------------------: | :-------------------------: | :---------------------------: |
    |   `useServerPrepStmts`  |   サーバー側を使用してプリペアドステートメントを有効にするかどうか  | プリペアドステートメントを複数回使用する必要がある場合 |             `true`            |
    |     `cachePrepStmts`    |   クライアントが準備されたステートメントをキャッシュするかどうか   |  `useServerPrepStmts=true`時 |             `true`            |
    | `prepStmtCacheSqlLimit` | プリペアドステートメントの最大サイズ (デフォルトでは 256 文字) |  プリペアドステートメントが 256 文字を超える場合 | プリペアドステートメントの実際のサイズに応じて構成されます |
    |   `prepStmtCacheSize`   |    準備されたステートメントの最大数 (デフォルトでは 25)    |  準備されたステートメントの数が 25 を超える場合  |   実際の準備済みステートメントの数に応じて構成されます  |

    以下は、JDBC 接続文字列構成の一般的なシナリオです。ホスト: `127.0.0.1` 、ポート: `4000` 、ユーザー名: `root` 、パスワード: null、デフォルトのデータベース: `test` :

    ```
    jdbc:mysql://127.0.0.1:4000/test?user=root&useConfigs=maxPerformance&useServerPrepStmts=true&prepStmtCacheSqlLimit=2048&prepStmtCacheSize=256&rewriteBatchedStatements=true&allowMultiQueries=true
    ```

    データの挿入時に他の JDBC パラメータを変更する必要がある場合は、第[行を挿入する](/develop/dev-guide-insert-data.md#insert-rows)章を参照してください。

    Javaの完全な例については、以下を参照してください。

    -   [JDBC を使用して TiDB に接続する](/develop/dev-guide-sample-application-java-jdbc.md)
    -   [Hibernate で TiDB に接続する](/develop/dev-guide-sample-application-java-hibernate.md)
    -   [Spring Boot を使用して TiDB に接続する](/develop/dev-guide-sample-application-java-spring-boot.md)
  </div>
</SimpleTab>
