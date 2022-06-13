---
title: Prepared Statements
summary: Learn about how to use the TiDB prepared statements.
---

# プリペアドステートメント {#prepared-statements}

[プリペアドステートメント](/sql-statements/sql-statement-prepare.md)は、パラメーターのみが異なる複数のSQLステートメントをテンプレート化します。 SQLステートメントをパラメーターから分離します。これを使用して、SQLステートメントの次の側面を改善できます。

-   **セキュリティ**：パラメータとステートメントが分離されているため、 [SQLインジェクション](https://en.wikipedia.org/wiki/SQL_injection)の攻撃のリスクが回避されます。
-   **パフォーマンス**：ステートメントはTiDBサーバーで事前に解析されるため、パラメーターのみが後続の実行に渡され、SQLステートメント全体の解析、SQLステートメント文字列のスプライシング、およびネットワーク送信のコストを節約できます。

ほとんどのアプリケーションでは、SQLステートメントを列挙できます。限られた数のSQLステートメントを使用して、アプリケーション全体のデータクエリを完了することができます。したがって、プリペアドステートメントを使用することがベストプラクティスです。

## SQL構文 {#sql-syntax}

このセクションでは、プリペアドステートメントを作成、実行、および削除するためのSQL構文について説明します。

### プリペアドステートメントを作成する {#create-a-prepared-statement}

{{< copyable "" >}}

```sql
PREPARE {prepared_statement_name} FROM '{prepared_statement_sql}';
```

|            パラメータ名           |                 説明                |
| :-------------------------: | :-------------------------------: |
| `{prepared_statement_name}` |          プリペアドステートメントの名前          |
|  `{prepared_statement_sql}` | プレースホルダーとして疑問符が付いたプリペアドステートメントSQL |

詳細については、 [PREPAREステートメント](/sql-statements/sql-statement-prepare.md)を参照してください。

### プリペアドステートメントを使用する {#use-the-prepared-statement}

プリペアドステートメントは**ユーザー変数**のみをパラメーターとして使用できるため、 [`EXECUTE`ステートメント](/sql-statements/sql-statement-execute.md)がプリペアドステートメントを呼び出す前に、 [`SET`ステートメント](/sql-statements/sql-statement-set-variable.md)を使用して変数を設定します。

{{< copyable "" >}}

```sql
SET @{parameter_name} = {parameter_value};
EXECUTE {prepared_statement_name} USING @{parameter_name};
```

|            パラメータ名           |                                             説明                                             |
| :-------------------------: | :----------------------------------------------------------------------------------------: |
|      `{parameter_name}`     |                                           ユーザー変数名                                          |
|     `{parameter_value}`     |                                           ユーザー変数値                                          |
| `{prepared_statement_name}` | 前処理ステートメントの名前。これは、 [プリペアドステートメントを作成する](#create-a-prepared-statement)で定義された名前と同じである必要があります。 |

詳細については、 [`EXECUTE`ステートメント](/sql-statements/sql-statement-execute.md)を参照してください。

### プリペアドステートメントを削除します {#delete-the-prepared-statement}

{{< copyable "" >}}

```sql
DEALLOCATE PREPARE {prepared_statement_name};
```

|            パラメータ名           |                                             説明                                             |
| :-------------------------: | :----------------------------------------------------------------------------------------: |
| `{prepared_statement_name}` | 前処理ステートメントの名前。これは、 [プリペアドステートメントを作成する](#create-a-prepared-statement)で定義された名前と同じである必要があります。 |

詳細については、 [`DEALLOCATE`ステートメント](/sql-statements/sql-statement-deallocate.md)を参照してください。

## 例 {#examples}

このセクションでは、プリペアドステートメントの2つの例について説明します`SELECT`つのデータと`INSERT`のデータです。

### <code>SELECT</code>例 {#code-select-code-example}

たとえば、 [`bookshop`アプリケーション](/develop/dev-guide-bookshop-schema-design.md#books-table)の`id = 1`の本をクエリする必要があります。

<SimpleTab>

<div label="SQL" href="read-sql">

{{< copyable "" >}}

```sql
PREPARE `books_query` FROM 'SELECT * FROM `books` WHERE `id` = ?';
```

実行結果：

```
Query OK, 0 rows affected (0.01 sec)
```

{{< copyable "" >}}

```sql
SET @id = 1;
```

実行結果：

```
Query OK, 0 rows affected (0.04 sec)
```

{{< copyable "" >}}

```sql
EXECUTE `books_query` USING @id;
```

実行結果：

```
+---------+---------------------------------+--------+---------------------+-------+--------+
| id      | title                           | type   | published_at        | stock | price  |
+---------+---------------------------------+--------+---------------------+-------+--------+
| 1       | The Adventures of Pierce Wehner | Comics | 1904-06-06 20:46:25 |   586 | 411.66 |
+---------+---------------------------------+--------+---------------------+-------+--------+
1 row in set (0.05 sec)
```

</div>

<div label="Java" href="read-java">

{{< copyable "" >}}

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

[`books`テーブル](/develop/dev-guide-bookshop-schema-design.md#books-table)を例に`published_at = NOW()` `title = TiDB Developer Guide` `stock = 100`の挿入時刻）の`type = Science & Technology`を挿入する必要があり`price = 0.0` 。 `books`テーブルの**主キー**で`AUTO_RANDOM`属性を指定する必要はないことに注意してください。データの挿入の詳細については、 [データを挿入](/develop/dev-guide-insert-data.md)を参照してください。

<SimpleTab>

<div label="SQL" href="write-sql">

{{< copyable "" >}}

```sql
PREPARE `books_insert` FROM 'INSERT INTO `books` (`title`, `type`, `stock`, `price`, `published_at`) VALUES (?, ?, ?, ?, ?);';
```

実行結果：

```
Query OK, 0 rows affected (0.03 sec)
```

{{< copyable "" >}}

```sql
SET @title = 'TiDB Developer Guide';
SET @type = 'Science & Technology';
SET @stock = 100;
SET @price = 0.0;
SET @published_at = NOW();
```

実行結果：

```
Query OK, 0 rows affected (0.04 sec)
```

{{< copyable "" >}}

```sql
EXECUTE `books_insert` USING @title, @type, @stock, @price, @published_at;
```

実行結果：

```
Query OK, 1 row affected (0.03 sec)
```

</div>

<div label="Java" href="write-java">

{{< copyable "" >}}

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

ご覧のとおり、JDBCはプリペアドステートメントのライフサイクルを制御するのに役立ち、アプリケーションでプリペアドステートメントを手動で作成、使用、または削除する必要はありません。ただし、TiDBはMySQLと互換性があるため、クライアント側でMySQL JDBCドライバーを使用するためのデフォルト構成では、***サーバー側の***プリペアドステートメントオプションを有効にするのではなく、クライアント側のプリペアドステートメントを使用することに注意してください。

次の構成は、JDBCでTiDBサーバー側のプリペアドステートメントを使用するのに役立ちます。

|          パラメータ          |                意味                |            推奨シナリオ           | 推奨されるConfiguration / コンフィグレーション |
| :---------------------: | :------------------------------: | :-------------------------: | :-----------------------------: |
|   `useServerPrepStmts`  | サーバー側を使用してプリペアドステートメントを有効にするかどうか | プリペアドステートメントを複数回使用する必要がある場合 |              `true`             |
|     `cachePrepStmts`    |  クライアントがプリペアドステートメントをキャッシュするかどうか |  `useServerPrepStmts=true`時 |              `true`             |
| `prepStmtCacheSqlLimit` | プリペアドステートメントの最大サイズ（デフォルトでは256文字） |   プリペアドステートメントが256文字を超える場合  |  プリペアドステートメントの実際のサイズに従って構成されます  |
|   `prepStmtCacheSize`   |    プリペアドステートメントの最大数（デフォルトでは25）   |   プリペアドステートメントの数が25を超える場合   |   プリペアドステートメントの実際の数に応じて構成されます   |

以下は、JDBC接続文字列構成の一般的なシナリオです。ホスト： `127.0.0.1` 、ポート： `4000` 、ユーザー名： `root` 、パスワード：null、デフォルトデータベース： `test` ：

```
jdbc:mysql://127.0.0.1:4000/test?user=root&useConfigs=maxPerformance&useServerPrepStmts=true&prepStmtCacheSqlLimit=2048&prepStmtCacheSize=256&rewriteBatchedStatements=true&allowMultiQueries=true
```

データを挿入するときに他のJDBCパラメータを変更する必要がある場合は、 [行を挿入](/develop/dev-guide-insert-data.md#insert-rows)章も参照してください。

Javaの完全な例については、以下を参照してください。

-   [TiDBとJavaを使用してシンプルなCRUDアプリを構築する-JDBCを使用する](/develop/dev-guide-sample-application-java.md#step-2-get-the-code)
-   [TiDBとJavaを使用してシンプルなCRUDアプリを構築する-Hibernateを使用する](/develop/dev-guide-sample-application-java.md#step-2-get-the-code)
-   [SpringBootを使用してTiDBアプリケーションを構築する](/develop/dev-guide-sample-application-spring-boot.md)

</div>

</SimpleTab>
