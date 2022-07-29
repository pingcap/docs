---
title: CREATE SEQUENCE
summary: An overview of the usage of CREATE SEQUENCE for the TiDB database.
---

# シーケンスの作成 {#create-sequence}

`CREATE SEQUENCE`ステートメントは、TiDBにシーケンスオブジェクトを作成します。シーケンスは、テーブルおよび`View`オブジェクトと同等のデータベースオブジェクトです。このシーケンスは、カスタマイズされた方法でシリアル化されたIDを生成するために使用されます。

## あらすじ {#synopsis}

```ebnf+diagram
CreateSequenceStmt ::=
    'CREATE' 'SEQUENCE' IfNotExists TableName CreateSequenceOptionListOpt CreateTableOptionListOpt

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
|   'NOMINVALUE'
|   'NO' ( 'MINVALUE' | 'MAXVALUE' | 'CACHE' | 'CYCLE' )
|   'NOMAXVALUE'
|   'NOCACHE'
|   'CYCLE'
|   'NOCYCLE'
```

## 構文 {#syntax}

{{< copyable "" >}}

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
| `TEMPORARY` | `false`                      | TiDBは現在、 `TEMPORARY`オプションをサポートしておらず、構文互換性のみを提供しています。                                                                                 |
| `INCREMENT` | `1`                          | シーケンスの増分を指定します。その正または負の値は、シーケンスの成長方向を制御できます。                                                                                         |
| `MINVALUE`  | `1`または`-9223372036854775807` | シーケンスの最小値を指定します。 `INCREMENT` &gt; `0`の場合、デフォルト値は`1`です。 `INCREMENT` &lt; `0`の場合、デフォルト値は`-9223372036854775807`です。                      |
| `MAXVALUE`  | `9223372036854775806`または`-1` | シーケンスの最大値を指定します。 `INCREMENT` &gt; `0`の場合、デフォルト値は`9223372036854775806`です。 `INCREMENT` &lt; `0`の場合、デフォルト値は`-1`です。                      |
| `START`     | `MINVALUE`または`MAXVALUE`      | シーケンスの初期値を指定します。 `INCREMENT` &gt; `0`の場合、デフォルト値は`MINVALUE`です。 `INCREMENT` &lt; `0`の場合、デフォルト値は`MAXVALUE`です。                           |
| `CACHE`     | `1000`                       | TiDBのシーケンスのローカルキャッシュサイズを指定します。                                                                                                       |
| `CYCLE`     | `NO CYCLE`                   | シーケンスを最小値（または降順シーケンスの最大値）から再開するかどうかを指定します。 `INCREMENT` &gt; `0`の場合、デフォルト値は`MINVALUE`です。 `INCREMENT` &lt; `0`の場合、デフォルト値は`MAXVALUE`です。 |

## <code>SEQUENCE</code>関数 {#code-sequence-code-function}

次の式関数を使用してシーケンスを制御できます。

-   `NEXTVAL`または`NEXT VALUE FOR`

    基本的に、どちらもシーケンスオブジェクトの次の有効な値を取得する`nextval()`の関数です。 `nextval()`関数のパラメーターは、シーケンスの`identifier`です。

-   `LASTVAL`

    この関数は、このセッションで最後に使用された値を取得します。値が存在しない場合は、 `NULL`が使用されます。この関数のパラメーターは、シーケンスの`identifier`です。

-   `SETVAL`

    この関数は、シーケンスの現在の値の進行を設定します。この関数の最初のパラメーターは、シーケンスの`identifier`です。 2番目のパラメーターは`num`です。

> **ノート：**
>
> TiDBでのシーケンスの実装では、 `SETVAL`関数はこのシーケンスの初期進行またはサイクル進行を変更できません。この関数は、この進行に基づいて次の有効な値のみを返します。

## 例 {#examples}

-   デフォルトのパラメータでシーケンスオブジェクトを作成します。

    {{< copyable "" >}}

    ```sql
    CREATE SEQUENCE seq;
    ```

    ```
    Query OK, 0 rows affected (0.06 sec)
    ```

-   `nextval()`関数を使用して、シーケンスオブジェクトの次の値を取得します。

    {{< copyable "" >}}

    ```sql
    SELECT nextval(seq);
    ```

    ```
    +--------------+
    | nextval(seq) |
    +--------------+
    |            1 |
    +--------------+
    1 row in set (0.02 sec)
    ```

-   `lastval()`関数を使用して、このセッションのシーケンスオブジェクトへの最後の呼び出しによって生成された値を取得します。

    {{< copyable "" >}}

    ```sql
    SELECT lastval(seq);
    ```

    ```
    +--------------+
    | lastval(seq) |
    +--------------+
    |            1 |
    +--------------+
    1 row in set (0.02 sec)
    ```

-   `setval()`関数を使用して、シーケンスオブジェクトの現在の値（または現在の位置）を設定します。

    {{< copyable "" >}}

    ```sql
    SELECT setval(seq, 10);
    ```

    ```
    +-----------------+
    | setval(seq, 10) |
    +-----------------+
    |              10 |
    +-----------------+
    1 row in set (0.01 sec)
    ```

-   `next value for`構文を使用して、シーケンスの次の値を取得することもできます。

    {{< copyable "" >}}

    ```sql
    SELECT next value for seq;
    ```

    ```
    +--------------------+
    | next value for seq |
    +--------------------+
    |                 11 |
    +--------------------+
    1 row in set (0.00 sec)
    ```

-   デフォルトのカスタムパラメータを使用してシーケンスオブジェクトを作成します。

    {{< copyable "" >}}

    ```sql
    CREATE SEQUENCE seq2 start 3 increment 2 minvalue 1 maxvalue 10 cache 3;
    ```

    ```
    Query OK, 0 rows affected (0.01 sec)
    ```

-   このセッションでシーケンスオブジェクトが使用されていない場合、 `lastval()`関数は`NULL`の値を返します。

    {{< copyable "" >}}

    ```sql
    SELECT lastval(seq2);
    ```

    ```
    +---------------+
    | lastval(seq2) |
    +---------------+
    |          NULL |
    +---------------+
    1 row in set (0.01 sec)
    ```

-   シーケンスオブジェクトの`nextval()`関数の最初の有効な値は、 `START`パラメーターの値です。

    {{< copyable "" >}}

    ```sql
    SELECT nextval(seq2);
    ```

    ```
    +---------------+
    | nextval(seq2) |
    +---------------+
    |             3 |
    +---------------+
    1 row in set (0.00 sec)
    ```

-   `setval()`関数はシーケンスオブジェクトの現在の値を変更できますが、次の値の等差数列ルールを変更することはできません。

    {{< copyable "" >}}

    ```sql
    SELECT setval(seq2, 6);
    ```

    ```
    +-----------------+
    | setval(seq2, 6) |
    +-----------------+
    |               6 |
    +-----------------+
    1 row in set (0.00 sec)
    ```

-   `nextval()`を使用して次の値を取得すると、次の値はシーケンスで定義された等差数列規則に従います。

    {{< copyable "" >}}

    ```sql
    SELECT next value for seq2;
    ```

    ```
    +---------------------+
    | next value for seq2 |
    +---------------------+
    |                   7 |
    +---------------------+
    1 row in set (0.00 sec)
    ```

-   次の例のように、シーケンスの次の値を列のデフォルト値として使用できます。

    {{< copyable "" >}}

    ```sql
    CREATE table t(a int default next value for seq2);
    ```

    ```
    Query OK, 0 rows affected (0.02 sec)
    ```

-   次の例では、値が指定されていないため、デフォルト値の`seq2`が使用されます。

    {{< copyable "" >}}

    ```sql
    INSERT into t values();
    ```

    ```
    Query OK, 1 row affected (0.00 sec)
    ```

    {{< copyable "" >}}

    ```sql
    SELECT * from t;
    ```

    ```
    +------+
    | a    |
    +------+
    |    9 |
    +------+
    1 row in set (0.00 sec)
    ```

-   次の例では、値が指定されていないため、デフォルト値の`seq2`が使用されます。ただし、次の値`seq2`は、上記の例（ `CREATE SEQUENCE seq2 start 3 increment 2 minvalue 1 maxvalue 10 cache 3;` ）で定義された範囲内にないため、エラーが返されます。

    {{< copyable "" >}}

    ```sql
    INSERT into t values();
    ```

    ```
    ERROR 4135 (HY000): Sequence 'test.seq2' has run out
    ```

## MySQLの互換性 {#mysql-compatibility}

このステートメントはTiDB拡張です。実装は、MariaDBで利用可能なシーケンスをモデルにしています。

`SETVAL`の関数を除いて、他のすべての関数はMariaDBと同じ*進行*をします。ここで「進行」とは、シーケンス内の数値が、シーケンスによって定義された特定の等差数列規則に従うことを意味します。 `SETVAL`を使用してシーケンスの現在の値を設定できますが、シーケンスの後続の値は元の進行ルールに従います。

例えば：

```
1, 3, 5, ...            // The sequence starts from 1 and increments by 2.
select setval(seq, 6)   // Sets the current value of a sequence to 6.
7, 9, 11, ...           // Subsequent values still follow the progression rule.
```

`CYCLE`モードでは、最初のラウンドのシーケンスの初期値は`START`パラメーターの値であり、後続のラウンドの初期値は`MinValue` （ `INCREMENT` &gt; 0）または`MaxValue` （ `INCREMENT` &lt;0）の値です。

## も参照してください {#see-also}

-   [ドロップシーケンス](/sql-statements/sql-statement-drop-sequence.md)
-   [CREATESEQUENCEを表示する](/sql-statements/sql-statement-show-create-sequence.md)
