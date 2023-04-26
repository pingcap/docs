---
title: Comparisons between Functions and Syntax of Oracle and TiDB
summary: Learn the comparisons between functions and syntax of Oracle and TiDB.
---

# Oracle と TiDB の関数と構文の比較 {#comparisons-between-functions-and-syntax-of-oracle-and-tidb}

このドキュメントでは、Oracle と TiDB の関数と構文の比較について説明します。 Oracle関数に基づいて対応する TiDB関数を見つけ、Oracle と TiDB の構文の違いを理解するのに役立ちます。

> **ノート：**
>
> このドキュメントの関数と構文は、Oracle 12.2.0.1.0 および TiDB v5.4.0 に基づいています。他のバージョンでは異なる場合があります。

## 関数比較 {#comparisons-of-functions}

次の表は、いくつかの Oracle と TiDB の関数の比較を示しています。

| 関数                       | オラクルの構文                                                                                                           | TiDB 構文                                                                                                                              | ノート                                                                                                                                                                        |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 値を特定の型としてキャストする          | `TO_NUMBER(key)`</li><li> `TO_CHAR(key)`                                                                          | `CONVERT(key,dataType)`                                                                                                              | TiDB は、値を次の型のいずれかとしてキャストすることをサポートしています: `BINARY` 、 `CHAR` 、 `DATE` 、 `DATETIME` 、 `TIME` 、 `SIGNED INTEGER` 、 `UNSIGNED INTEGER` 、および`DECIMAL` 。                           |
| 日付を文字列に変換する              | `TO_CHAR(SYSDATE,'yyyy-MM-dd hh24:mi:ss')`</li><li> `TO_CHAR(SYSDATE,'yyyy-MM-dd')`                               | `DATE_FORMAT(NOW(),'%Y-%m-%d %H:%i:%s')`</li><li> `DATE_FORMAT(NOW(),'%Y-%m-%d')`                                                    | TiDB のフォーマット文字列は大文字と小文字が区別されます。                                                                                                                                            |
| 文字列を日付に変換する              | `TO_DATE('2021-05-28 17:31:37','yyyy-MM-dd hh24:mi:ss')`</li><li> `TO_DATE('2021-05-28','yyyy-MM-dd hh24:mi:ss')` | `STR_TO_DATE('2021-05-28 17:31:37','%Y-%m-%d %H:%i:%s')`</li><li> `STR_TO_DATE('2021-05-28','%Y-%m-%d%T')`                           | TiDB のフォーマット文字列は大文字と小文字が区別されます。                                                                                                                                            |
| 現在のシステム時刻を秒精度で取得する       | `SYSDATE`                                                                                                         | `NOW()`                                                                                                                              |                                                                                                                                                                            |
| 現在のシステム時刻をマイクロ秒の精度で取得します | `SYSTIMESTAMP`                                                                                                    | `CURRENT_TIMESTAMP(6)`                                                                                                               |                                                                                                                                                                            |
| 2 つの日付間の日数を取得する          | `date1 - date2`                                                                                                   | `DATEDIFF(date1, date2)`                                                                                                             |                                                                                                                                                                            |
| 2 つの日付の間の月数を取得する         | `MONTHS_BETWEEN(ENDDATE,SYSDATE)`                                                                                 | `TIMESTAMPDIFF(MONTH,SYSDATE,ENDDATE)`                                                                                               | Oracle の`MONTHS_BETWEEN()`と TiDB の`TIMESTAMPDIFF()`の結果は異なります。 `TIMESTAMPDIFF()`整数を返します。 2 つの関数のパラメーターが入れ替わっていることに注意してください。                                                 |
| 日付に`n`日を加算する             | `DATEVAL + n`                                                                                                     | `DATE_ADD(dateVal,INTERVAL n DAY)`                                                                                                   | `n`負の値にすることができます。                                                                                                                                                          |
| 日付に`n`月を加算する             | `ADD_MONTHS(dateVal,n)`                                                                                           | `DATE_ADD(dateVal,INTERVAL n MONTH)`                                                                                                 | `n`負の値にすることができます。                                                                                                                                                          |
| デートの日を取得する               | `TRUNC(SYSDATE)`                                                                                                  | `CAST(NOW() AS DATE)`</li><li> `DATE_FORMAT(NOW(),'%Y-%m-%d')`                                                                       | TiDB では、 `CAST`と`DATE_FORMAT`同じ結果を返します。                                                                                                                                    |
| 日付の月を取得する                | `TRUNC(SYSDATE,'mm')`                                                                                             | `DATE_ADD(CURDATE(),interval - day(CURDATE()) + 1 day)`                                                                              |                                                                                                                                                                            |
| 値を切り捨てる                  | `TRUNC(2.136) = 2`<br/> `TRUNC(2.136,2) = 2.13`                                                                   | `TRUNCATE(2.136,0) = 2`<br/> `TRUNCATE(2.136,2) = 2.13`                                                                              | データの精度は維持されます。丸めずに対応する小数点以下を切り捨てます。                                                                                                                                        |
| シーケンス内の次の値を取得する          | `sequence_name.NEXTVAL`                                                                                           | `NEXTVAL(sequence_name)`                                                                                                             |                                                                                                                                                                            |
| ランダムなシーケンス値を取得する         | `SYS_GUID()`                                                                                                      | `UUID()`                                                                                                                             | TiDB は Universal Unique Identifier (UUID) を返します。                                                                                                                           |
| 左結合または右結合                | `SELECT * FROM a, b WHERE a.id = b.id(+);`<br/>`SELECT * FROM a, b WHERE a.id(+) = b.id;`                         | `SELECT * FROM a LEFT JOIN b ON a.id = b.id;`<br/>`SELECT * FROM a RIGHT JOIN b ON a.id = b.id;`                                     | 相関クエリでは、TiDB は (+) を使用した左結合または右結合をサポートしていません。代わりに`LEFT JOIN`または`RIGHT JOIN`を使用できます。                                                                                        |
| `NVL()`                  | `NVL(key,val)`                                                                                                    | `IFNULL(key,val)`                                                                                                                    | フィールドの値が`NULL`の場合は`val`を返します。それ以外の場合は、フィールドの値を返します。                                                                                                                        |
| `NVL2()`                 | `NVL2(key, val1, val2)`                                                                                           | `IF(key is NULL, val1, val2)`                                                                                                        | フィールドの値が`NULL`でない場合は`val1`を返します。それ以外の場合は`val2`を返します。                                                                                                                       |
| `DECODE()`               | `DECODE(key,val1,val2,val3)`</li><li> `DECODE(value,if1,val1,if2,val2,...,ifn,valn,val)`                          | `IF(key=val1,val2,val3)`</li><li> `CASE WHEN value=if1 THEN val1 WHEN value=if2 THEN val2,...,WHEN value=ifn THEN valn ELSE val END` | フィールドの値が`val1`の場合は`val2`を返します。それ以外の場合は`val3`を返します。</li><li>フィールドの値が条件 1 ( `if1` ) を満たす場合、 `val1`を返します。条件 2 ( `if2` ) を満たす場合は`val2`を返します。条件 3 ( `if3` ) を満たす場合は`val3`を返します。 |
| 文字列`a`と`b`を連結する          | `'a' || 'b'`                                                                                                      | `CONCAT('a','b')`                                                                                                                    |                                                                                                                                                                            |
| 文字列の長さを取得する              | `LENGTH(str)`                                                                                                     | `CHAR_LENGTH(str)`                                                                                                                   |                                                                                                                                                                            |
| 指定された部分文字列を取得する          | `SUBSTR('abcdefg',0,2) = 'ab'`<br/> `SUBSTR('abcdefg',1,2) = 'ab'`                                                | `SUBSTRING('abcdefg',0,2) = ''`<br/>`SUBSTRING('abcdefg',1,2) = 'ab'`                                                                | Oracle では、開始位置 0 は 1 と同じ効果があります。</li><li> TiDB では、開始位置 0 は空の文字列を返します。先頭から部分文字列を取得する場合は、開始位置を 1 にする必要があります。                                                                 |
| 部分文字列の位置を取得する            | `INSTR('abcdefg','b',1,1)`                                                                                        | `INSTR('abcdefg','b')`                                                                                                               | `'abcdefg'`の最初の文字から検索し、 `'b'`が最初に出現する位置を返します。                                                                                                                              |
| 部分文字列の位置を取得する            | `INSTR('stst','s',1,2)`                                                                                           | `LENGTH(SUBSTRING_INDEX('stst','s',2)) + 1`                                                                                          | `'stst'`の最初の文字から検索し、2 番目に出現する`'s'`の位置を返します。                                                                                                                                |
| 部分文字列の位置を取得する            | `INSTR('abcabc','b',2,1)`                                                                                         | `LOCATE('b','abcabc',2)`                                                                                                             | `abcabc`の 2 文字目から検索し、最初に`b`が出現する位置を返します。                                                                                                                                   |
| 列の値を連結する                 | `LISTAGG(CONCAT(E.dimensionid,'---',E.DIMENSIONNAME),'***') within GROUP(ORDER BY DIMENSIONNAME)`                 | `GROUP_CONCAT(CONCAT(E.dimensionid,'---',E.DIMENSIONNAME) ORDER BY DIMENSIONNAME SEPARATOR '***')`                                   | 指定した列の値を区切り文字`***`で 1 つの行に連結します。                                                                                                                                           |
| ASCII コードを文字に変換する        | `CHR(n)`                                                                                                          | `CHAR(n)`                                                                                                                            | Oracle の Tab ( `CHR(9)` )、LF ( `CHR(10)` )、および CR ( `CHR(13)` ) 文字は、TiDB の`CHAR(9)` 、 `CHAR(10)` 、および`CHAR(13)`に対応します。                                                     |

## 構文の比較 {#comparisons-of-syntax}

このセクションでは、Oracle と TiDB の構文の違いについて説明します。

### 文字列構文 {#string-syntax}

Oracle では、文字列は一重引用符 (&#39;&#39;) でのみ囲むことができます。たとえば`'a'` 。

TiDB では、文字列を一重引用符 (&#39;&#39;) または二重引用符 (&quot;&quot;) で囲むことができます。たとえば、 `'a'`と`"a"`です。

### <code>NULL</code>と空の文字列の違い {#difference-between-code-null-code-and-an-empty-string}

Oracle は`NULL`と空の文字列`''`を区別しません。つまり、 `NULL`は`''`と同等です。

TiDB は`NULL`と空の文字列`''`を区別します。

### <code>INSERT</code>ステートメントで同じテーブルを読み書きする {#read-and-write-to-the-same-table-in-an-code-insert-code-statement}

Oracle は、 `INSERT`のステートメントで同じテーブルへの読み取りと書き込みをサポートしています。例えば：

```sql
INSERT INTO table1 VALUES (feild1,(SELECT feild2 FROM table1 WHERE...))
```

TiDB は、 `INSERT`ステートメントでの同じテーブルへの読み取りと書き込みをサポートしていません。例えば：

```sql
INSERT INTO table1 VALUES (feild1,(SELECT T.fields2 FROM table1 T WHERE...))
```

### クエリから最初の n 行を取得する {#get-the-first-n-rows-from-a-query}

Oracle では、クエリから最初の n 行を取得するには、 `ROWNUM <= n`句を使用できます。たとえば`ROWNUM <= 10` 。

TiDB では、クエリから最初の n 行を取得するには、 `LIMIT n`句を使用できます。たとえば`LIMIT 10` 。 `LIMIT`の SQL ステートメントを実行する Hibernate Query Language (HQL) はエラーになります。 Hibernate ステートメントを SQL ステートメントに変更する必要があります。

### <code>UPDATE</code>ステートメントで複数のテーブルを更新する {#update-multiple-tables-in-an-code-update-code-statement}

Oracle では、複数のテーブルを更新する場合、特定のフィールド更新関係をリストする必要はありません。例えば：

```sql
UPDATE test1 SET(test1.name,test1.age) = (SELECT test2.name,test2.age FROM test2 WHERE test2.id=test1.id)
```

TiDB では、複数のテーブルを更新する場合、特定のフィールド更新関係をすべて`SET`にリストする必要があります。例えば：

```sql
UPDATE test1,test2 SET test1.name=test2.name,test1.age=test2.age WHERE test1.id=test2.id
```

### 派生テーブルのエイリアス {#derived-table-alias}

Oracle では、複数のテーブルをクエリする場合、派生テーブルにエイリアスを追加する必要はありません。例えば：

```sql
SELECT * FROM (SELECT * FROM test)
```

TiDB では、複数のテーブルにクエリを実行する場合、すべての派生テーブルに独自のエイリアスが必要です。例えば：

```sql
SELECT * FROM (SELECT * FROM test) t
```

### セット操作 {#set-operations}

Oracle では、最初のクエリ結果に含まれるが 2 番目のクエリ結果には含まれない行を取得するには、 `MINUS`セット操作を使用できます。例えば：

```sql
SELECT * FROM t1 MINUS SELECT * FROM t2
```

TiDB は`MINUS`操作をサポートしていません。 `EXCEPT`セット運用ができます。例えば：

```sql
SELECT * FROM t1 EXCEPT SELECT * FROM t2
```

### コメント構文 {#comment-syntax}

Oracle では、コメント構文は`--Comment`です。

TiDB では、コメント構文は`-- Comment`です。 TiDB では`--`後に空白があることに注意してください。

### ページネーション {#pagination}

Oracle では、 `OFFSET m ROWS`を使用して`m`行をスキップし、 `FETCH NEXT n ROWS ONLY`を使用して`n`行をフェッチできます。例えば：

```sql
SELECT * FROM tables OFFSET 0 ROWS FETCH NEXT 2000 ROWS ONLY
```

TiDB では、 `LIMIT n OFFSET m`使用して`OFFSET m ROWS FETCH NEXT n ROWS ONLY`を置き換えることができます。例えば：

```sql
SELECT * FROM tables LIMIT 2000 OFFSET 0
```

### <code>NULL</code>値のソート順 {#sorting-order-on-code-null-code-values}

Oracle では、次の場合に`NULL`値が`ORDER BY`句でソートされます。

-   `ORDER BY column ASC`ステートメントでは、最後に`NULL`値が返されます。

-   `ORDER BY column DESC`ステートメントでは、最初に`NULL`値が返されます。

-   `ORDER BY column [ASC|DESC] NULLS FIRST`ステートメントでは、非 NULL 値の前に`NULL`値が返されます。非 NULL 値は、 `ASC|DESC`で指定された昇順または降順で返されます。

-   `ORDER BY column [ASC|DESC] NULLS LAST`ステートメントでは、非 NULL 値の後に`NULL`値が返されます。非 NULL 値は、 `ASC|DESC`で指定された昇順または降順で返されます。

TiDB では、次の場合に`NULL`値が`ORDER BY`句でソートされます。

-   `ORDER BY column ASC`ステートメントでは、最初に`NULL`値が返されます。

-   `ORDER BY column DESC`ステートメントでは、最後に`NULL`値が返されます。

次の表は、Oracle と TiDB における同等の`ORDER BY`ステートメントの例を示しています。

| オラクルで`ORDER BY`                                    | TiDB の同等のステートメント                                          |
| :------------------------------------------------- | :-------------------------------------------------------- |
| `SELECT * FROM t1 ORDER BY name NULLS FIRST;`      | `SELECT * FROM t1 ORDER BY name;`                         |
| `SELECT * FROM t1 ORDER BY name DESC NULLS LAST;`  | `SELECT * FROM t1 ORDER BY name DESC;`                    |
| `SELECT * FROM t1 ORDER BY name DESC NULLS FIRST;` | `SELECT * FROM t1 ORDER BY ISNULL(name) DESC, name DESC;` |
| `SELECT * FROM t1 ORDER BY name ASC NULLS LAST;`   | `SELECT * FROM t1 ORDER BY ISNULL(name), name;`           |
