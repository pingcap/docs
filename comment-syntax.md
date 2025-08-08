---
title: Comment Syntax
summary: このドキュメントでは、TiDB でサポートされているコメント構文について説明します。
---

# コメント構文 {#comment-syntax}

このドキュメントでは、TiDB でサポートされているコメント構文について説明します。

TiDB は次の 3 つのコメント スタイルをサポートしています。

-   行をコメント化するには`#`使用します。

    ```sql
    SELECT 1+1;     # comments
    ```

        +------+
        | 1+1  |
        +------+
        |    2 |
        +------+
        1 row in set (0.00 sec)

-   行をコメント化するには`--`使用します。

    ```sql
    SELECT 1+1;     -- comments
    ```

        +------+
        | 1+1  |
        +------+
        |    2 |
        +------+
        1 row in set (0.00 sec)

    このスタイルでは、 `--`後に少なくとも 1 つの空白が必要です。

    ```sql
    SELECT 1+1--1;
    ```

        +--------+
        | 1+1--1 |
        +--------+
        |      3 |
        +--------+
        1 row in set (0.01 sec)

-   ブロックまたは複数行をコメント化するには`/* */`使用します。

    ```sql
    SELECT 1 /* this is an in-line comment */ + 1;
    ```

        +--------+
        | 1  + 1 |
        +--------+
        |      2 |
        +--------+
        1 row in set (0.01 sec)

    ```sql
    SELECT 1+
    /*
    /*> this is a
    /*> multiple-line comment
    /*> */
        1;
    ```

        +-------------------+
        | 1+
                1 |
        +-------------------+
        |                 2 |
        +-------------------+
        1 row in set (0.001 sec)

## MySQL互換のコメント構文 {#mysql-compatible-comment-syntax}

MySQL と同じように、TiDB は C コメント スタイルのバリエーションをサポートしています。

    /*! Specific code */

または

    /*!50110 Specific code */

このスタイルでは、TiDB はコメント内のステートメントを実行します。

例えば：

```sql
SELECT /*! STRAIGHT_JOIN */ col1 FROM table1,table2 WHERE ...
```

TiDB では、別のバージョンも使用できます。

```sql
SELECT STRAIGHT_JOIN col1 FROM table1,table2 WHERE ...
```

MySQLでは、コメントにサーバーのバージョン番号（例： `/*!50110 KEY_BLOCK_SIZE=1024 */` ）を指定した場合、このコメントの内容はMySQLのバージョンが5.1.10以上の場合にのみ処理されます。しかし、TiDBではMySQLのバージョン番号は機能せず、コメント内のすべての内容が処理されます。

## TiDB固有のコメント構文 {#tidb-specific-comment-syntax}

TiDB には独自のコメント構文 (つまり、TiDB 固有のコメント構文) があり、次の 2 種類に分けられます。

-   `/*T! Specific code */` : この構文は TiDB によってのみ解析および実行され、他のデータベースでは無視されます。
-   `/*T![feature_id] Specific code */` : この構文は、TiDBの異なるバージョン間の互換性を確保するために使用されます。TiDBは、現在のバージョンで`feature_id`の対応する機能を実装している場合にのみ、このコメント内のSQLフラグメントを解析できます。例えば、 `AUTO_RANDOM`機能はv3.1.1で導入されているため、このバージョンのTiDBは`/*T![auto_rand] auto_random */`を`auto_random`に解析できます。10 `AUTO_RANDOM`機能はv3.0.0では実装されていないため、上記のSQL文フラグメントは無視されます。/* **`/*T![`文字内にスペースを入れないでください**。

## オプティマイザコメント構文 {#optimizer-comment-syntax}

別の種類のコメントは、オプティマイザーヒントとして特別に扱われます。

```sql
SELECT /*+ hint */ FROM ...;
```

TiDB がサポートするオプティマイザヒントの詳細については、 [オプティマイザーヒント](/optimizer-hints.md)参照してください。

> **注記：**
>
> MySQLクライアントでは、TiDB固有のコメント構文はコメントとして扱われ、デフォルトでクリアされます。5.7.7より前のMySQLクライアントでは、ヒントもコメントとして扱われ、デフォルトでクリアされます。クライアント起動時には、 `--comments`オプションを使用することをお勧めします。例えば、 `mysql -h 127.0.0.1 -P 4000 -uroot --comments`指定します。

詳細については[コメント構文](https://dev.mysql.com/doc/refman/8.0/en/comments.html)参照してください。
