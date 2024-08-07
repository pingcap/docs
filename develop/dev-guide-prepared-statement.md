---
title: Prepared Statements
summary: TiDB 準備済みステートメントの使用方法について学習します。
---

# 準備された声明 {#prepared-statements}

[プリペアドステートメント](/sql-statements/sql-statement-prepare.md) 、パラメータのみが異なる複数の SQL ステートメントをテンプレート化します。SQL ステートメントとパラメータを分離します。これを使用して、SQL ステートメントの次の側面を改善できます。

-   **Security**: パラメータとステートメントが分離されているため、 [SQLインジェクション](https://en.wikipedia.org/wiki/SQL_injection)攻撃のリスクを回避できます。
-   **パフォーマンス**: ステートメントは TiDBサーバー上で事前に解析されるため、後続の実行ではパラメータのみが渡され、SQL ステートメント全体の解析、SQL ステートメント文字列の結合、およびネットワーク転送のコストが節約されます。

ほとんどのアプリケーションでは、SQL ステートメントを列挙できます。限られた数の SQL ステートメントを使用して、アプリケーション全体のデータ クエリを完了できます。そのため、プリペアドステートメントを使用するのがベスト プラクティスです。

## SQL構文 {#sql-syntax}

このセクションでは、プリペアドステートメントを作成、実行、および削除するための SQL 構文について説明します。

### プリペアドステートメントを作成する {#create-a-prepared-statement}

```sql
PREPARE {prepared_statement_name} FROM '{prepared_statement_sql}';
```

|            パラメータ名           |                説明                |
| :-------------------------: | :------------------------------: |
| `{prepared_statement_name}` |          プリペアドステートメントの名前         |
|  `{prepared_statement_sql}` | プレースホルダとして疑問符が付いたプリペアドステートメントSQL |

詳細については[PREPARE ステートメント](/sql-statements/sql-statement-prepare.md)参照してください。

### プリペアドステートメントを使用する {#use-the-prepared-statement}

プリペアドステートメントは、**ユーザー変数**のみをパラメーターとして使用できるため、 [`EXECUTE`ステートメント](/sql-statements/sql-statement-execute.md)プリペアドステートメントを呼び出す前に、 [`SET`ステートメント](/sql-statements/sql-statement-set-variable.md)を使用して変数を設定します。

```sql
SET @{parameter_name} = {parameter_value};
EXECUTE {prepared_statement_name} USING @{parameter_name};
```

|            パラメータ名           |                                          説明                                          |
| :-------------------------: | :----------------------------------------------------------------------------------: |
|      `{parameter_name}`     |                                        ユーザー変数名                                       |
|     `{parameter_value}`     |                                        ユーザー変数値                                       |
| `{prepared_statement_name}` | 前処理ステートメントの名前[プリペアドステートメントを作成する](#create-a-prepared-statement)で定義された名前と同じである必要があります。 |

詳細については[`EXECUTE`ステートメント](/sql-statements/sql-statement-execute.md)参照してください。

### プリペアドステートメントを削除する {#delete-the-prepared-statement}

```sql
DEALLOCATE PREPARE {prepared_statement_name};
```

|            パラメータ名           |                                          説明                                          |
| :-------------------------: | :----------------------------------------------------------------------------------: |
| `{prepared_statement_name}` | 前処理ステートメントの名前[プリペアドステートメントを作成する](#create-a-prepared-statement)で定義された名前と同じである必要があります。 |

詳細については[`DEALLOCATE`ステートメント](/sql-statements/sql-statement-deallocate.md)参照してください。

## 例 {#examples}

このセクションでは、準備されたステートメントの 2 つの例 ( `SELECT`データと`INSERT`データ) について説明します。

### <code>SELECT</code>例 {#code-select-code-example}

たとえば、 [`bookshop`アプリケーション](/develop/dev-guide-bookshop-schema-design.md#books-table)のうち`id = 1`を含む本をクエリする必要があります。

<SimpleTab groupId="language">

<div label="SQL" value="sql">

```sql
PREPARE `books_query` FROM 'SELECT * FROM `books` WHERE `id` = ?';
```

実行結果:

    Query OK, 0 rows affected (0.01 sec)

```sql
SET @id = 1;
```

実行結果:

    Query OK, 0 rows affected (0.04 sec)

```sql
EXECUTE `books_query` USING @id;
```

実行結果:

    +---------+---------------------------------+--------+---------------------+-------+--------+
    | id      | title                           | type   | published_at        | stock | price  |
    +---------+---------------------------------+--------+---------------------+-------+--------+
    | 1       | The Adventures of Pierce Wehner | Comics | 1904-06-06 20:46:25 |   586 | 411.66 |
    +---------+---------------------------------+--------+---------------------+-------+--------+
    1 row in set (0.05 sec)

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

[`books`](/develop/dev-guide-bookshop-schema-design.md#books-table)例にすると、 `title = TiDB Developer Guide` 、 `type = Science & Technology` 、 `stock = 100` 、 `price = 0.0` 、 `published_at = NOW()` (挿入時の現在時刻) を含む本を挿入する必要があります。 `books`テーブルの**主キー**に`AUTO_RANDOM`属性を指定する必要がないことに注意してください。データの挿入の詳細については、 [データの挿入](/develop/dev-guide-insert-data.md)を参照してください。

<SimpleTab groupId="language">

<div label="SQL" value="sql">

```sql
PREPARE `books_insert` FROM 'INSERT INTO `books` (`title`, `type`, `stock`, `price`, `published_at`) VALUES (?, ?, ?, ?, ?);';
```

実行結果:

    Query OK, 0 rows affected (0.03 sec)

```sql
SET @title = 'TiDB Developer Guide';
SET @type = 'Science & Technology';
SET @stock = 100;
SET @price = 0.0;
SET @published_at = NOW();
```

実行結果:

    Query OK, 0 rows affected (0.04 sec)

```sql
EXECUTE `books_insert` USING @title, @type, @stock, @price, @published_at;
```

実行結果:

    Query OK, 1 row affected (0.03 sec)

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

ご覧のとおり、JDBC を使用すると準備済みステートメントのライフ サイクルを制御でき、アプリケーションで準備済みステートメントを手動で作成、使用、または削除する必要がありません。ただし、TiDB は MySQL と互換性があるため、クライアント側で MySQL JDBCDriverを使用するためのデフォルト構成では、***サーバー側の***プリペアドステートメントオプションを有効にするのではなく、クライアント側のプリペアドステートメントを使用することに注意してください。

次の構成は、JDBC で TiDB サーバー側の準備済みステートメントを使用するのに役立ちます。

|          パラメータ          |                 手段                 |            推奨シナリオ           |          推奨コンフィグレーション         |
| :---------------------: | :--------------------------------: | :-------------------------: | :---------------------------: |
|   `useServerPrepStmts`  |   サーバー側を使用して準備済みステートメントを有効にするかどうか  | プリペアドステートメントを複数回使用する必要がある場合 |             `true`            |
|     `cachePrepStmts`    |   クライアントが準備されたステートメントをキャッシュするかどうか  |  `useServerPrepStmts=true`  |             `true`            |
| `prepStmtCacheSqlLimit` | プリペアドステートメントの最大サイズ（デフォルトでは 256 文字） |   プリペアドステートメントが256文字を超える場合  | プリペアドステートメントの実際のサイズに応じて構成されます |
|   `prepStmtCacheSize`   |    準備されたステートメントの最大数（デフォルトでは 25）    |   準備されたステートメントの数が25を超える場合   |  準備されたステートメントの実際の数に応じて構成されます  |

以下は、JDBC 接続文字列構成の一般的なシナリオです。ホスト: `127.0.0.1` 、ポート: `4000` 、ユーザー名: `root` 、パスワード: null、デフォルト データベース: `test` :

    jdbc:mysql://127.0.0.1:4000/test?user=root&useConfigs=maxPerformance&useServerPrepStmts=true&prepStmtCacheSqlLimit=2048&prepStmtCacheSize=256&rewriteBatchedStatements=true&allowMultiQueries=true

データを挿入するときに他の JDBC パラメータを変更する必要がある場合は、 [行を挿入する](/develop/dev-guide-insert-data.md#insert-rows)章も参照してください。

Javaの完全な例については、以下を参照してください。

-   [JDBC で TiDB に接続する](/develop/dev-guide-sample-application-java-jdbc.md)
-   [Hibernate で TiDB に接続する](/develop/dev-guide-sample-application-java-hibernate.md)
-   [Spring Boot で TiDB に接続する](/develop/dev-guide-sample-application-java-spring-boot.md)

</div>

</SimpleTab>

## 助けが必要？ {#need-help}

<CustomContent platform="tidb">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](/support.md)について質問します。

</CustomContent>

<CustomContent platform="tidb-cloud">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](https://support.pingcap.com/)について質問します。

</CustomContent>
