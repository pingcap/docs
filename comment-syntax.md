---
title: Comment Syntax
summary: This document introduces the comment syntax supported by TiDB.
---

# コメント構文 {#comment-syntax}

このドキュメントでは、TiDBでサポートされているコメント構文について説明します。

TiDBは、次の3つのコメントスタイルをサポートしています。

-   `#`を使用して、行にコメントを付けます。

    {{< copyable "" >}}

    ```sql
    SELECT 1+1;     # comments
    ```

    ```
    +------+
    | 1+1  |
    +------+
    |    2 |
    +------+
    1 row in set (0.00 sec)
    ```

-   `--`を使用して、行にコメントを付けます。

    {{< copyable "" >}}

    ```sql
    SELECT 1+1;     -- comments
    ```

    ```
    +------+
    | 1+1  |
    +------+
    |    2 |
    +------+
    1 row in set (0.00 sec)
    ```

    そして、このスタイルでは、1の後に少なくとも`--`つの空白が必要です。

    {{< copyable "" >}}

    ```sql
    SELECT 1+1--1;
    ```

    ```
    +--------+
    | 1+1--1 |
    +--------+
    |      3 |
    +--------+
    1 row in set (0.01 sec)
    ```

-   `/* */`を使用して、ブロックまたは複数行にコメントを付けます。

    {{< copyable "" >}}

    ```sql
    SELECT 1 /* this is an in-line comment */ + 1;
    ```

    ```
    +--------+
    | 1  + 1 |
    +--------+
    |      2 |
    +--------+
    1 row in set (0.01 sec)
    ```

    {{< copyable "" >}}

    ```sql
    SELECT 1+
    /*
    /*> this is a
    /*> multiple-line comment
    /*> */
        1;
    ```

    ```
    +-------------------+
    | 1+
            1 |
    +-------------------+
    |                 2 |
    +-------------------+
    1 row in set (0.001 sec)
    ```

## MySQL互換のコメント構文 {#mysql-compatible-comment-syntax}

MySQLと同じように、TiDBはCコメントスタイルのバリアントをサポートします。

```
/*! Specific code */
```

また

```
/*!50110 Specific code */
```

このスタイルでは、TiDBはコメント内のステートメントを実行します。

例えば：

```sql
SELECT /*! STRAIGHT_JOIN */ col1 FROM table1,table2 WHERE ...
```

TiDBでは、別のバージョンを使用することもできます。

```sql
SELECT STRAIGHT_JOIN col1 FROM table1,table2 WHERE ...
```

MySQLでサーバーのバージョン番号がコメントに指定されている場合（たとえば`/*!50110 KEY_BLOCK_SIZE=1024 */` ）、このコメントの内容は、MySQLのバージョンが5.1.10以上の場合にのみ処理されることを意味します。ただし、TiDBでは、MySQLのバージョン番号が機能せず、コメントのすべてのコンテンツが処理されます。

## TiDB固有のコメント構文 {#tidb-specific-comment-syntax}

TiDBには独自のコメント構文（つまり、TiDB固有のコメント構文）があり、次の2つのタイプに分けることができます。

-   `/*T! Specific code */` ：この構文は、TiDBによってのみ解析および実行でき、他のデータベースでは無視されます。
-   `/*T![feature_id] Specific code */` ：この構文は、異なるバージョンのTiDB間の互換性を確保するために使用されます。 TiDBは、現在のバージョンで`feature_id`の対応する機能を実装している場合にのみ、このコメントのSQLフラグメントを解析できます。たとえば、v3.1.1で`AUTO_RANDOM`機能が導入されたため、このバージョンのTiDBは`/*T![auto_rand] auto_random */`を`auto_random`に解析できます。 `AUTO_RANDOM`機能はv3.0.0に実装されていないため、上記のSQLステートメントフラグメントは無視されます。 **`/*T![`文字の中にスペースを残さないでください**。

## オプティマイザーコメント構文 {#optimizer-comment-syntax}

別のタイプのコメントは、オプティマイザーのヒントとして特別に扱われます。

{{< copyable "" >}}

```sql
SELECT /*+ hint */ FROM ...;
```

TiDBがサポートするオプティマイザヒントの詳細については、 [オプティマイザーのヒント](/optimizer-hints.md)を参照してください。

> **ノート**
>
> MySQLクライアントでは、TiDB固有のコメント構文はコメントとして扱われ、デフォルトでクリアされます。 5.7.7より前のMySQLクライアントでは、ヒントはコメントとしても表示され、デフォルトでクリアされます。クライアントを起動するときは、 `--comments`オプションを使用することをお勧めします。たとえば、 `mysql -h 127.0.0.1 -P 4000 -uroot --comments` 。

詳細については、 [コメント構文](https://dev.mysql.com/doc/refman/5.7/en/comments.html)を参照してください。
