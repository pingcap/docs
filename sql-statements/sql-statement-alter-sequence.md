---
title: ALTER SEQUENCE
summary: TiDB データベースの ALTER SEQUENCE の使用法の概要。
---

# シーケンスの変更 {#alter-sequence}

`ALTER SEQUENCE`ステートメントは、TiDB内のシーケンスオブジェクトを変更します。シーケンスは、 `Table`および`View`のオブジェクトと同等のデータベースオブジェクトです。シーケンスは、カスタマイズされた方法でシリアル化されたIDを生成するために使用されます。

## 概要 {#synopsis}

```ebnf+diagram
CreateSequenceStmt ::=
    'ALTER' 'SEQUENCE' TableName CreateSequenceOptionListOpt

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
|   'RESTART' ( ( '='? | 'WITH' ) SignedNum )?
```

## 構文 {#syntax}

```sql
ALTER SEQUENCE sequence_name
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
| `INCREMENT` | `1`                          | シーケンスの増分を指定します。正または負の値を指定することで、シーケンスの増加方向を制御できます。                                                                                   |
| `MINVALUE`  | `1`または`-9223372036854775807` | シーケンスの最小値を指定します。1 &gt; `0` `INCREMENT`場合、デフォルト値は`1`です。7 &lt; `0` `INCREMENT`場合、デフォルト値は`-9223372036854775807`です。                     |
| `MAXVALUE`  | `9223372036854775806`または`-1` | シーケンスの最大値を指定します。1 &gt; `0` `INCREMENT`場合、デフォルト値は`9223372036854775806`です。7 &lt; `0` `INCREMENT`場合、デフォルト値は`-1`です。                     |
| `START`     | `MINVALUE`または`MAXVALUE`      | シーケンスの初期値を指定します。1 &gt; `0` `INCREMENT`場合、デフォルト値は`MINVALUE`です。7 &lt; `0` `INCREMENT`場合、デフォルト値は`MAXVALUE`です。                          |
| `CACHE`     | `1000`                       | TiDB 内のシーケンスのローカル キャッシュ サイズを指定します。                                                                                                  |
| `CYCLE`     | `NO CYCLE`                   | シーケンスを最小値（降順シーケンスの場合は最大値）から再開するかどうかを指定します。1 &gt; `0` `INCREMENT` 、デフォルト値は`MINVALUE`です。7 &lt; `INCREMENT` `0`場合、デフォルト値は`MAXVALUE`です。 |

> **注記：**
>
> `START`値を変更しても、 `ALTER SEQUENCE ... RESTART`実行するまで生成された値には影響しません。

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

`s1`という名前のシーケンスを作成します。

```sql
CREATE SEQUENCE s1;
```

    Query OK, 0 rows affected (0.15 sec)

次の SQL ステートメントを 2 回実行して、シーケンスから次の 2 つの値を取得します。

```sql
SELECT NEXTVAL(s1);
```

    +-------------+
    | NEXTVAL(s1) |
    +-------------+
    |           1 |
    +-------------+
    1 row in set (0.01 sec)

```sql
SELECT NEXTVAL(s1);
```

    +-------------+
    | NEXTVAL(s1) |
    +-------------+
    |           2 |
    +-------------+
    1 row in set (0.00 sec)

シーケンスの増分を`2`に変更します。

```sql
ALTER SEQUENCE s1 INCREMENT=2;
```

    Query OK, 0 rows affected (0.18 sec)

ここで、シーケンスから次の 2 つの値を再度取得します。

```sql
SELECT NEXTVAL(s1);
```

    +-------------+
    | NEXTVAL(s1) |
    +-------------+
    |        1001 |
    +-------------+
    1 row in set (0.02 sec)

```sql
SELECT NEXTVAL(s1);
```

    +-------------+
    | NEXTVAL(s1) |
    +-------------+
    |        1003 |
    +-------------+
    1 row in set (0.00 sec)

出力からわかるように、 `ALTER SEQUENCE`ステートメントの後に値が 2 増加します。

シーケンスの他のパラメータを変更することもできます。例えば、シーケンスの`MAXVALUE`次のように変更できます。

```sql
CREATE SEQUENCE s2 MAXVALUE=10;
```

    Query OK, 0 rows affected (0.17 sec)

```sql
ALTER SEQUENCE s2 MAXVALUE=100;
```

    Query OK, 0 rows affected (0.15 sec)

```sql
SHOW CREATE SEQUENCE s2\G
```

    *************************** 1. row ***************************
           Sequence: s2
    Create Sequence: CREATE SEQUENCE `s2` start with 1 minvalue 1 maxvalue 100 increment by 1 cache 1000 nocycle ENGINE=InnoDB
    1 row in set (0.00 sec)

## MySQLの互換性 {#mysql-compatibility}

このステートメントはTiDBの拡張機能です。実装はMariaDBで利用可能なシーケンスをモデルにしています。

`SETVAL`関数を除くすべての関数は、MariaDB と同じ*数列規則*に従います。ここでの「数列規則」とは、シーケンス内の数値が、シーケンスによって定義された特定の等差数列規則に従うことを意味します。シーケンスの現在の値を設定するのに`SETVAL`使用できますが、シーケンスのそれ以降の値は元の数列規則に従います。

例えば：

    1, 3, 5, ...            // The sequence starts from 1 and increments by 2.
    SELECT SETVAL(seq, 6)   // Sets the current value of a sequence to 6.
    7, 9, 11, ...           // Subsequent values still follow the progression rule.

`CYCLE`モードでは、最初のラウンドのシーケンスの初期値は`START`パラメータの値であり、後続のラウンドの初期値は`MinValue` ( `INCREMENT` &gt; 0) または`MaxValue` ( `INCREMENT` &lt; 0) の値です。

## 参照 {#see-also}

-   [シーケンスを作成](/sql-statements/sql-statement-create-sequence.md)
-   [ドロップシーケンス](/sql-statements/sql-statement-drop-sequence.md)
-   [シーケンスの作成を表示](/sql-statements/sql-statement-show-create-sequence.md)
-   [シーケンス関数](/functions-and-operators/sequence-functions.md)
