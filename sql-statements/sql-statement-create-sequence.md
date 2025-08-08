---
title: CREATE SEQUENCE
summary: TiDB データベースの CREATE SEQUENCE の使用法の概要。
---

# シーケンスを作成 {#create-sequence}

`CREATE SEQUENCE`ステートメントは、TiDB にシーケンスオブジェクトを作成します。シーケンスは、テーブルや`View`のオブジェクトと同等のデータベースオブジェクトです。シーケンスは、カスタマイズされた方法でシリアル化された ID を生成するために使用されます。

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

## パラメータ {#parameters}

| パラメータ       | デフォルト値                       | 説明                                                                                                                                  |
| :---------- | :--------------------------- | :---------------------------------------------------------------------------------------------------------------------------------- |
| `TEMPORARY` | `false`                      | TiDB は現在`TEMPORARY`オプションをサポートしておらず、構文の互換性のみを提供しています。                                                                                |
| `INCREMENT` | `1`                          | シーケンスの増分を指定します。正または負の値を指定することで、シーケンスの増加方向を制御できます。                                                                                   |
| `MINVALUE`  | `1`または`-9223372036854775807` | シーケンスの最小値を指定します。1 &gt; `0` `INCREMENT`場合、デフォルト値は`1`です。7 &lt; `0` `INCREMENT`場合、デフォルト値は`-9223372036854775807`です。                     |
| `MAXVALUE`  | `9223372036854775806`または`-1` | シーケンスの最大値を指定します。1 &gt; `0` `INCREMENT`場合、デフォルト値は`9223372036854775806`です。7 &lt; `0` `INCREMENT`場合、デフォルト値は`-1`です。                     |
| `START`     | `MINVALUE`または`MAXVALUE`      | シーケンスの初期値を指定します。1 &gt; `0` `INCREMENT`場合、デフォルト値は`MINVALUE`です。7 &lt; `0` `INCREMENT`場合、デフォルト値は`MAXVALUE`です。                          |
| `CACHE`     | `1000`                       | TiDB 内のシーケンスのローカル キャッシュ サイズを指定します。                                                                                                  |
| `CYCLE`     | `NO CYCLE`                   | シーケンスを最小値（降順シーケンスの場合は最大値）から再開するかどうかを指定します。1 &gt; `0` `INCREMENT` 、デフォルト値は`MINVALUE`です。7 &lt; `INCREMENT` `0`場合、デフォルト値は`MAXVALUE`です。 |

## <code>SEQUENCE</code>関数 {#code-sequence-code-function}

次の式関数を通じてシーケンスを制御できます。

-   `NEXTVAL`または`NEXT VALUE FOR`

    基本的に、どちらもシーケンスオブジェクトの次の有効な値を取得する`NEXTVAL()`関数です。3 `NEXTVAL()`の関数の引数は、シーケンスの`identifier`の値です。

-   `LASTVAL`

    この関数は、このセッションで最後に使用された値を取得します。値が存在しない場合は`NULL`使用されます。この関数の引数は、シーケンスの`identifier`です。

-   `SETVAL`

    この関数は、シーケンスの現在の値の進行を設定します。この関数の最初のパラメータはシーケンスの`identifier` 、2番目のパラメータは`num`です。

> **注記：**
>
> TiDBにおけるシーケンスの実装において、 `SETVAL`関数はシーケンスの初期進行またはサイクル進行を変更できません。この関数は、この進行に基づいて次の有効な値を返すだけです。

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

-   このセッションでのシーケンス オブジェクトへの最後の呼び出しによって生成された値を取得するには、 `LASTVAL()`関数を使用します。

    ```sql
    SELECT LASTVAL(seq);
    ```

        +--------------+
        | LASTVAL(seq) |
        +--------------+
        |            1 |
        +--------------+
        1 row in set (0.02 sec)

-   シーケンス オブジェクトの現在の値 (または現在の位置) を設定するには、 `SETVAL()`関数を使用します。

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

-   `NEXTVAL()`使用して次の値を取得する場合、次の値はシーケンスによって定義された等差数列の規則に従います。

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

-   次の例では、値が指定されていないため、デフォルト値の`seq2`が使用されます。しかし、次の値`seq2`は上記の例で定義された範囲（ `CREATE SEQUENCE seq2 start 3 increment 2 minvalue 1 maxvalue 10 cache 3;` ）外であるため、エラーが返されます。

    ```sql
    INSERT into t values();
    ```

        ERROR 4135 (HY000): Sequence 'test.seq2' has run out

## MySQLの互換性 {#mysql-compatibility}

このステートメントはTiDBの拡張機能です。実装はMariaDBで利用可能なシーケンスをモデルにしています。

`SETVAL`関数を除くすべての関数は、MariaDB と同じ*数列規則*に従います。ここでの「数列規則」とは、シーケンス内の数値が、シーケンスによって定義された特定の等差数列規則に従うことを意味します。シーケンスの現在の値を設定するのに`SETVAL`使用できますが、シーケンスのそれ以降の値は元の数列規則に従います。

例えば：

    1, 3, 5, ...            // The sequence starts from 1 and increments by 2.
    select SETVAL(seq, 6)   // Sets the current value of a sequence to 6.
    7, 9, 11, ...           // Subsequent values still follow the progression rule.

`CYCLE`モードでは、最初のラウンドのシーケンスの初期値は`START`パラメータの値であり、後続のラウンドの初期値は`MinValue` ( `INCREMENT` &gt; 0) または`MaxValue` ( `INCREMENT` &lt; 0) の値です。

## 参照 {#see-also}

-   [シーケンスの変更](/sql-statements/sql-statement-alter-sequence.md)
-   [ドロップシーケンス](/sql-statements/sql-statement-drop-sequence.md)
-   [シーケンスの作成を表示](/sql-statements/sql-statement-show-create-sequence.md)
-   [シーケンス関数](/functions-and-operators/sequence-functions.md)
