---
title: Comment Syntax
summary: This document introduces the comment syntax supported by TiDB.
---

# コメントの構文 {#comment-syntax}

このドキュメントでは、TiDB でサポートされるコメント構文について説明します。

TiDB は 3 つのコメント スタイルをサポートしています。

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

    そして、このスタイルには`--`後に少なくとも 1 つの空白が必要です。

    ```sql
    SELECT 1+1--1;
    ```

        +--------+
        | 1+1--1 |
        +--------+
        |      3 |
        +--------+
        1 row in set (0.01 sec)

-   ブロックまたは複数の行をコメントするには`/* */`を使用します。

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

## MySQL 互換のコメント構文 {#mysql-compatible-comment-syntax}

MySQL と同様に、TiDB は C コメント スタイルのバリアントをサポートしています。

    /*! Specific code */

または

    /*!50110 Specific code */

このスタイルでは、TiDB はコメント内のステートメントを実行します。

例えば：

```sql
SELECT /*! STRAIGHT_JOIN */ col1 FROM table1,table2 WHERE ...
```

TiDB では、別のバージョンを使用することもできます。

```sql
SELECT STRAIGHT_JOIN col1 FROM table1,table2 WHERE ...
```

MySQL でサーバーのバージョン番号がコメントに指定されている場合 (例: `/*!50110 KEY_BLOCK_SIZE=1024 */` )、このコメントの内容は MySQL バージョンが 5.1.10 以上の場合にのみ処理されることを意味します。ただし、TiDB では、MySQL のバージョン番号は機能せず、コメント内のすべての内容が処理されます。

## TiDB 固有のコメント構文 {#tidb-specific-comment-syntax}

TiDB には独自のコメント構文 (つまり、TiDB 固有のコメント構文) があり、次の 2 つのタイプに分類できます。

-   `/*T! Specific code */` : この構文は TiDB によってのみ解析および実行でき、他のデータベースでは無視されます。
-   `/*T![feature_id] Specific code */` : この構文は、TiDB の異なるバージョン間の互換性を確保するために使用されます。 TiDB は、現在のバージョンで`feature_id`の対応する機能を実装している場合にのみ、このコメント内の SQL フラグメントを解析できます。たとえば、 `AUTO_RANDOM`機能が v3.1.1 で導入されたため、このバージョンの TiDB は`/*T![auto_rand] auto_random */` `auto_random`に解析できます。 `AUTO_RANDOM`機能は v3.0.0 には実装されていないため、上記の SQL ステートメントのフラグメントは無視されます。 **`/*T![`文字の中にスペースを残さないでください**。

## オプティマイザーのコメント構文 {#optimizer-comment-syntax}

別の種類のコメントは、オプティマイザー ヒントとして特別に処理されます。

```sql
SELECT /*+ hint */ FROM ...;
```

TiDB がサポートするオプティマイザー ヒントの詳細については、 [オプティマイザーのヒント](/optimizer-hints.md)を参照してください。

> **注記：**
>
> MySQL クライアントでは、TiDB 固有のコメント構文はコメントとして扱われ、デフォルトでクリアされます。 5.7.7 より前の MySQL クライアントでは、ヒントもコメントとして表示され、デフォルトでクリアされます。クライアントを起動するときは、 `--comments`オプションを使用することをお勧めします。たとえば、 `mysql -h 127.0.0.1 -P 4000 -uroot --comments` 。

詳細については、 [コメントの構文](https://dev.mysql.com/doc/refman/8.0/en/comments.html)を参照してください。
