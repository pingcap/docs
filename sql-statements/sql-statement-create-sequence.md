---
title: CREATE SEQUENCE
summary: TiDB データベースの CREATE SEQUENCE の使用法の概要。
---

# シーケンスを作成 {#create-sequence}

`CREATE SEQUENCE`文は、TiDB にシーケンス オブジェクトを作成します。シーケンスは、テーブルおよび`View`オブジェクトと同等のデータベース オブジェクトです。シーケンスは、カスタマイズされた方法でシリアル化された ID を生成するために使用されます。

## 概要 {#synopsis}

```ebnf+diagram
CreateSequenceStmt ::=
    'CREATE' 'SEQUENCE' IfNotExists TableName CreateSequenceOptionListOpt

IfNotExists ::=
    ('IF' 'NOT' 'EXISTS')?

TableName ::=
    Identifier ('.' Identifier)?

CreateSequenceOptionListOpt ::=
    SequenceOption*

SequenceOptionList ::=
    SequenceOption

SequenceOption ::=
    ( 'INCREMENT' ( '='? | 'BY' ) | 'START' ( '='? | 'WITH' ) | ( 'MINVALUE' | 'MAXVALUE' | 'CACHE' ) '='? ) SignedNum
|   'COMMENT' '='? stringLit
|   'NOMINVALUE'
|   'NO' ( 'MINVALUE' | 'MAXVALUE' | 'CACHE' | 'CYCLE' )
|   'NOMAXVALUE'
|   'NOCACHE'
|   'CYCLE'
|   'NOCYCLE'
```

## 構文 {#syntax}

```sql
CREATE [TEMPORARY] SEQUENCE [IF NOT EXISTS] sequence_name
    [ INCREMENT [ BY | = ] increment ]
    [ MINVALUE [=] minvalue | NO MINVALUE | NOMINVALUE ]
    [ MAXVALUE [=] maxvalue | NO MAXVALUE | NOMAXVALUE ]
    [ START [ WITH | = ] start ]
    [ CACHE [=] cache | NOCACHE | NO CACHE]
    [ CYCLE | NOCYCLE | NO CYCLE]
    [table_options]
```

## パラメーター {#parameters}

| パラメーター      | デフォルト値                       | 説明                                                                                                                                   |
| :---------- | :--------------------------- | :----------------------------------------------------------------------------------------------------------------------------------- |
| `TEMPORARY` | `false`                      | TiDB は現在`TEMPORARY`オプションをサポートしておらず、構文の互換性のみを提供しています。                                                                                 |
| `INCREMENT` | `1`                          | シーケンスの増分を指定します。正または負の値により、シーケンスの成長方向を制御できます。                                                                                         |
| `MINVALUE`  | `1`または`-9223372036854775807` | シーケンスの最小値を指定します。 `INCREMENT` &gt; `0`の場合、デフォルト値は`1`です。 `INCREMENT` &lt; `0`の場合、デフォルト値は`-9223372036854775807`です。                      |
| `MAXVALUE`  | `9223372036854775806`または`-1` | シーケンスの最大値を指定します。 `INCREMENT` &gt; `0`の場合、デフォルト値は`9223372036854775806`です。 `INCREMENT` &lt; `0`の場合、デフォルト値は`-1`です。                      |
| `START`     | `MINVALUE`または`MAXVALUE`      | シーケンスの初期値を指定します。 `INCREMENT` &gt; `0`の場合、デフォルト値は`MINVALUE`です。 `INCREMENT` &lt; `0`の場合、デフォルト値は`MAXVALUE`です。                           |
| `CACHE`     | `1000`                       | TiDB 内のシーケンスのローカル キャッシュ サイズを指定します。                                                                                                   |
| `CYCLE`     | `NO CYCLE`                   | シーケンスが最小値（降順シーケンスの場合は最大値）から再開するかどうかを指定します。 `INCREMENT` &gt; `0`の場合、デフォルト値は`MINVALUE`です。 `INCREMENT` &lt; `0`の場合、デフォルト値は`MAXVALUE`です。 |

## <code>SEQUENCE</code>機能 {#code-sequence-code-function}

次の式関数を使用してシーケンスを制御できます。

-   `NEXTVAL`または`NEXT VALUE FOR`

    本質的には、どちらもシーケンス オブジェクトの次の有効な値を取得する`NEXTVAL()`の関数です。3 `NEXTVAL()`の関数のパラメーターは、シーケンスの`identifier`です。

-   `LASTVAL`

    この関数は、このセッションで最後に使用された値を取得します。値が存在しない場合は、 `NULL`使用されます。この関数のパラメーターは、シーケンスの`identifier`です。

-   `SETVAL`

    この関数は、シーケンスの現在の値の進行を設定します。この関数の最初のパラメーターはシーケンスの`identifier`で、2 番目のパラメーターは`num`です。

> **注記：**
>
> TiDB でのシーケンスの実装では、 `SETVAL`関数はこのシーケンスの初期進行またはサイクル進行を変更できません。この関数は、この進行に基づいて次の有効な値を返すだけです。

## 例 {#examples}

-   デフォルトのパラメータを使用してシーケンス オブジェクトを作成します。

    ```sql
    CREATE SEQUENCE seq;
    ```

        Query OK, 0 rows affected (0.06 sec)

-   シーケンス オブジェクトの次の値を取得するには、 `NEXTVAL()`関数を使用します。

    ```sql
    SELECT NEXTVAL(seq);
    ```

        +--------------+
        | NEXTVAL(seq) |
        +--------------+
        |            1 |
        +--------------+
        1 row in set (0.02 sec)

-   このセッションでシーケンス オブジェクトへの最後の呼び出しによって生成された値を取得するには、 `LASTVAL()`関数を使用します。

    ```sql
    SELECT LASTVAL(seq);
    ```

        +--------------+
        | LASTVAL(seq) |
        +--------------+
        |            1 |
        +--------------+
        1 row in set (0.02 sec)

-   `SETVAL()`関数を使用して、シーケンス オブジェクトの現在の値 (または現在の位置) を設定します。

    ```sql
    SELECT SETVAL(seq, 10);
    ```

        +-----------------+
        | SETVAL(seq, 10) |
        +-----------------+
        |              10 |
        +-----------------+
        1 row in set (0.01 sec)

-   `next value for`構文を使用して、シーケンスの次の値を取得することもできます。

    ```sql
    SELECT next value for seq;
    ```

        +--------------------+
        | next value for seq |
        +--------------------+
        |                 11 |
        +--------------------+
        1 row in set (0.00 sec)

-   デフォルトのカスタム パラメータを使用してシーケンス オブジェクトを作成します。

    ```sql
    CREATE SEQUENCE seq2 start 3 increment 2 minvalue 1 maxvalue 10 cache 3;
    ```

        Query OK, 0 rows affected (0.01 sec)

-   このセッションでシーケンス オブジェクトが使用されていない場合、 `LASTVAL()`関数は`NULL`値を返します。

    ```sql
    SELECT LASTVAL(seq2);
    ```

        +---------------+
        | LASTVAL(seq2) |
        +---------------+
        |          NULL |
        +---------------+
        1 row in set (0.01 sec)

-   シーケンス オブジェクトの`NEXTVAL()`関数の最初の有効な値は、 `START`パラメータの値です。

    ```sql
    SELECT NEXTVAL(seq2);
    ```

        +---------------+
        | NEXTVAL(seq2) |
        +---------------+
        |             3 |
        +---------------+
        1 row in set (0.00 sec)

-   `SETVAL()`関数はシーケンス オブジェクトの現在の値を変更できますが、次の値の等差数列の規則を変更することはできません。

    ```sql
    SELECT SETVAL(seq2, 6);
    ```

        +-----------------+
        | SETVAL(seq2, 6) |
        +-----------------+
        |               6 |
        +-----------------+
        1 row in set (0.00 sec)

-   `NEXTVAL()`を使用して次の値を取得する場合、次の値はシーケンスによって定義された等差数列の規則に従います。

    ```sql
    SELECT next value for seq2;
    ```

        +---------------------+
        | next value for seq2 |
        +---------------------+
        |                   7 |
        +---------------------+
        1 row in set (0.00 sec)

-   次の例のように、シーケンスの次の値を列のデフォルト値として使用できます。

    ```sql
    CREATE table t(a int default next value for seq2);
    ```

        Query OK, 0 rows affected (0.02 sec)

-   次の例では、値が指定されていないため、デフォルト値の`seq2`が使用されます。

    ```sql
    INSERT into t values();
    ```

        Query OK, 1 row affected (0.00 sec)

    ```sql
    SELECT * from t;
    ```

        +------+
        | a    |
        +------+
        |    9 |
        +------+
        1 row in set (0.00 sec)

-   次の例では、値が指定されていないため、デフォルト値の`seq2`が使用されます。ただし、次の値`seq2`は上記の例 ( `CREATE SEQUENCE seq2 start 3 increment 2 minvalue 1 maxvalue 10 cache 3;` ) で定義された範囲内ではないため、エラーが返されます。

    ```sql
    INSERT into t values();
    ```

        ERROR 4135 (HY000): Sequence 'test.seq2' has run out

## MySQL 互換性 {#mysql-compatibility}

このステートメントは TiDB の拡張機能です。実装は MariaDB で利用可能なシーケンスに基づいてモデル化されています。

`SETVAL`関数を除き、他のすべての関数はMariaDB と同じ*進行順序*を持ちます。ここでの「進行順序」とは、シーケンス内の数字がシーケンスによって定義された特定の等差数列の規則に従うことを意味します。シーケンスの現在の値を設定するには`SETVAL`使用できますが、シーケンスのそれ以降の値は元の進行順序の規則に従います。

例えば：

    1, 3, 5, ...            // The sequence starts from 1 and increments by 2.
    select SETVAL(seq, 6)   // Sets the current value of a sequence to 6.
    7, 9, 11, ...           // Subsequent values still follow the progression rule.

`CYCLE`モードでは、最初のラウンドのシーケンスの初期値は`START`パラメータの値であり、後続のラウンドの初期値は`MinValue` ( `INCREMENT` &gt; 0) または`MaxValue` ( `INCREMENT` &lt; 0) の値です。

## 参照 {#see-also}

-   [シーケンスの変更](/sql-statements/sql-statement-alter-sequence.md)
-   [ドロップシーケンス](/sql-statements/sql-statement-drop-sequence.md)
-   [表示シーケンスの作成](/sql-statements/sql-statement-show-create-sequence.md)
-   [シーケンス関数](/functions-and-operators/sequence-functions.md)
