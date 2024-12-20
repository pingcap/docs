---
title: Comparisons between Functions and Syntax of Oracle and TiDB
summary: Oracle と TiDB の関数と構文の比較を学習します。
---

# Oracle と TiDB の機能と構文の比較 {#comparisons-between-functions-and-syntax-of-oracle-and-tidb}

このドキュメントでは、Oracle と TiDB の関数と構文の比較について説明します。Oracle関数に基づいて対応する TiDB関数を見つけ、Oracle と TiDB の構文の違いを理解するのに役立ちます。

> **注記：**
>
> このドキュメントの関数と構文は、Oracle 12.2.0.1.0 および TiDB v5.4.0 に基づいています。他のバージョンでは異なる場合があります。

## 関数の比較 {#comparisons-of-functions}

次の表は、いくつかの Oracle 関数と TiDB関数の比較を示しています。

| 関数                     | Oracle構文                                                                                                                   | TiDB構文                                                                                                                                        | 注記                                                                                                                                                                  |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 値を特定の型にキャストする          | <li>`TO_NUMBER(key)`</li><li> `TO_CHAR(key)`</li>                                                                          | `CONVERT(key,dataType)`                                                                                                                       | TiDB は、値を`BINARY` 、 `CHAR` 、 `DATE` 、 `DATETIME` 、 `TIME` 、 `SIGNED INTEGER` 、 `UNSIGNED INTEGER` 、 `DECIMAL`のいずれかの型にキャストすることをサポートしています。                            |
| 日付を文字列に変換する            | <li>`TO_CHAR(SYSDATE,'yyyy-MM-dd hh24:mi:ss')`</li><li> `TO_CHAR(SYSDATE,'yyyy-MM-dd')`</li>                               | <li>`DATE_FORMAT(NOW(),'%Y-%m-%d %H:%i:%s')`</li><li> `DATE_FORMAT(NOW(),'%Y-%m-%d')`</li>                                                    | TiDB のフォーマット文字列では大文字と小文字が区別されます。                                                                                                                                    |
| 文字列を日付に変換する            | <li>`TO_DATE('2021-05-28 17:31:37','yyyy-MM-dd hh24:mi:ss')`</li><li> `TO_DATE('2021-05-28','yyyy-MM-dd hh24:mi:ss')`</li> | <li>`STR_TO_DATE('2021-05-28 17:31:37','%Y-%m-%d %H:%i:%s')`</li><li> `STR_TO_DATE('2021-05-28','%Y-%m-%d%T')`</li>                           | TiDB のフォーマット文字列では大文字と小文字が区別されます。                                                                                                                                    |
| 現在のシステム時間を秒単位で取得します    | `SYSDATE`                                                                                                                  | `NOW()`                                                                                                                                       |                                                                                                                                                                     |
| 現在のシステム時間をマイクロ秒精度で取得する | `SYSTIMESTAMP`                                                                                                             | `CURRENT_TIMESTAMP(6)`                                                                                                                        |                                                                                                                                                                     |
| 2つの日付間の日数を取得する         | `date1 - date2`                                                                                                            | `DATEDIFF(date1, date2)`                                                                                                                      |                                                                                                                                                                     |
| 2つの日付間の月数を取得する         | `MONTHS_BETWEEN(ENDDATE,SYSDATE)`                                                                                          | `TIMESTAMPDIFF(MONTH,SYSDATE,ENDDATE)`                                                                                                        | Oracle の`MONTHS_BETWEEN()`と TiDB の`TIMESTAMPDIFF()`の結果は異なります。5 `TIMESTAMPDIFF()`整数を返します。2 つの関数のパラメータが入れ替わっていることに注意してください。                                           |
| 日付に`n`日追加する            | `DATEVAL + n`                                                                                                              | `DATE_ADD(dateVal,INTERVAL n DAY)`                                                                                                            | `n`負の値になる場合があります。                                                                                                                                                   |
| 日付に`n`月を追加する           | `ADD_MONTHS(dateVal,n)`                                                                                                    | `DATE_ADD(dateVal,INTERVAL n MONTH)`                                                                                                          | `n`負の値になる場合があります。                                                                                                                                                   |
| デートの日をゲット              | `TRUNC(SYSDATE)`                                                                                                           | <li>`CAST(NOW() AS DATE)`</li><li> `DATE_FORMAT(NOW(),'%Y-%m-%d')`</li>                                                                       | TiDB では、 `CAST`と`DATE_FORMAT`同じ結果を返します。                                                                                                                             |
| 日付の月を取得する              | `TRUNC(SYSDATE,'mm')`                                                                                                      | `DATE_ADD(CURDATE(),interval - day(CURDATE()) + 1 day)`                                                                                       |                                                                                                                                                                     |
| 値を切り捨てる                | `TRUNC(2.136) = 2`<br/> `TRUNC(2.136,2) = 2.13`                                                                            | `TRUNCATE(2.136,0) = 2`<br/> `TRUNCATE(2.136,2) = 2.13`                                                                                       | データの精度は保持されます。対応する小数点以下の桁は四捨五入せずに切り捨てます。                                                                                                                            |
| シーケンス内の次の値を取得する        | `sequence_name.NEXTVAL`                                                                                                    | `NEXTVAL(sequence_name)`                                                                                                                      |                                                                                                                                                                     |
| ランダムなシーケンス値を取得する       | `SYS_GUID()`                                                                                                               | `UUID()`                                                                                                                                      | TiDB はユニバーサル ユニーク識別子 (UUID) を返します。                                                                                                                                  |
| 左結合または右結合              | `SELECT * FROM a, b WHERE a.id = b.id(+);`<br/>`SELECT * FROM a, b WHERE a.id(+) = b.id;`                                  | `SELECT * FROM a LEFT JOIN b ON a.id = b.id;`<br/>`SELECT * FROM a RIGHT JOIN b ON a.id = b.id;`                                              | 相関クエリでは、TiDB は (+) を使用した左結合または右結合をサポートしていません。代わりに`LEFT JOIN`または`RIGHT JOIN`使用できます。                                                                                  |
| `NVL()`                | `NVL(key,val)`                                                                                                             | `IFNULL(key,val)`                                                                                                                             | フィールドの値が`NULL`の場合は`val`を返し、それ以外の場合はフィールドの値を返します。                                                                                                                    |
| `NVL2()`               | `NVL2(key, val1, val2)`                                                                                                    | `IF(key is NOT NULL, val1, val2)`                                                                                                             | フィールドの値が`NULL`でない場合は`val1`返し、それ以外の場合は`val2`返します。                                                                                                                    |
| `DECODE()`             | <li>`DECODE(key,val1,val2,val3)`</li><li> `DECODE(value,if1,val1,if2,val2,...,ifn,valn,val)`</li>                          | <li>`IF(key=val1,val2,val3)`</li><li> `CASE WHEN value=if1 THEN val1 WHEN value=if2 THEN val2,...,WHEN value=ifn THEN valn ELSE val END`</li> | <li>フィールドの値が`val1`場合は`val2`返し、それ以外の場合は`val3`返します。</li><li>フィールドの値が条件1（ `if1` ）を満たす場合は`val1`返します。条件2（ `if2` ）を満たす場合は`val2`を返します。条件3（ `if3` ）を満たす場合は`val3`を返します。</li> |
| 文字列`a`と`b`を連結する        | `'a' || 'b'`                                                                                                               | `CONCAT('a','b')`                                                                                                                             |                                                                                                                                                                     |
| 文字列の長さを取得する            | `LENGTH(str)`                                                                                                              | `CHAR_LENGTH(str)`                                                                                                                            |                                                                                                                                                                     |
| 指定された部分文字列を取得する        | `SUBSTR('abcdefg',0,2) = 'ab'`<br/> `SUBSTR('abcdefg',1,2) = 'ab'`                                                         | `SUBSTRING('abcdefg',0,2) = ''`<br/>`SUBSTRING('abcdefg',1,2) = 'ab'`                                                                         | <li>Oracle では、開始位置 0 は 1 と同じ効果を持ちます。</li><li> TiDB では、開始位置 0 は空の文字列を返します。先頭から部分文字列を取得する場合は、開始位置を 1 にする必要があります。</li>                                                 |
| 部分文字列の位置を取得する          | `INSTR('abcdefg','b',1,1)`                                                                                                 | `INSTR('abcdefg','b')`                                                                                                                        | `'abcdefg'`の最初の文字から検索し、 `'b'`が最初に出現する位置を返します。                                                                                                                       |
| 部分文字列の位置を取得する          | `INSTR('stst','s',1,2)`                                                                                                    | `LENGTH(SUBSTRING_INDEX('stst','s',2)) + 1`                                                                                                   | `'stst'`の最初の文字から検索し、 `'s'`の 2 番目の出現位置を返します。                                                                                                                         |
| 部分文字列の位置を取得する          | `INSTR('abcabc','b',2,1)`                                                                                                  | `LOCATE('b','abcabc',2)`                                                                                                                      | `abcabc`の 2 番目の文字から検索し、 `b`が最初に出現する位置を返します。                                                                                                                         |
| 列の値を連結する               | `LISTAGG(CONCAT(E.dimensionid,'---',E.DIMENSIONNAME),'***') within GROUP(ORDER BY DIMENSIONNAME)`                          | `GROUP_CONCAT(CONCAT(E.dimensionid,'---',E.DIMENSIONNAME) ORDER BY DIMENSIONNAME SEPARATOR '***')`                                            | 指定された列の値を`***`区切り文字で 1 行に連結します。                                                                                                                                     |
| ASCIIコードを文字に変換する       | `CHR(n)`                                                                                                                   | `CHAR(n)`                                                                                                                                     | Oracleのタブ（ `CHR(9)` ）、 `CHAR(13)` （ `CHR(10)` ）、CR（ `CHR(13)` ）文字は`CHAR(10)` TiDBの`CHAR(9)`に対応します。                                                                  |

## 構文の比較 {#comparisons-of-syntax}

このセクションでは、Oracle と TiDB の構文の違いについて説明します。

### 文字列構文 {#string-syntax}

Oracle では、文字列は一重引用符 (&#39;&#39;) でのみ囲むことができます。たとえば、 `'a'`です。

TiDB では、文字列を一重引用符 (&#39;&#39;) または二重引用符 (&quot;&quot;) で囲むことができます。たとえば、 `'a'`と`"a"` 。

### <code>NULL</code>と空の文字列の違い {#difference-between-code-null-code-and-an-empty-string}

Oracle は`NULL`と空の文字列`''`を区別しません。つまり、 `NULL` `''`と同等です。

TiDB は`NULL`と空の文字列`''`を区別します。

### <code>INSERT</code>ステートメントで同じテーブルを読み書きする {#read-and-write-to-the-same-table-in-an-code-insert-code-statement}

Oracle は、 `INSERT`ステートメントで同じテーブルへの読み取りと書き込みをサポートしています。例:

```sql
INSERT INTO table1 VALUES (field1,(SELECT field2 FROM table1 WHERE...))
```

TiDB は、 `INSERT`ステートメントで同じテーブルへの読み取りと書き込みをサポートしていません。例:

```sql
INSERT INTO table1 VALUES (field1,(SELECT T.fields2 FROM table1 T WHERE...))
```

### クエリから最初のn行を取得する {#get-the-first-n-rows-from-a-query}

Oracle では、クエリから最初の n 行を取得するには、 `ROWNUM <= n`句を使用できます。たとえば、 `ROWNUM <= 10`です。

TiDB では、クエリから最初の n 行を取得するために、 `LIMIT n`句を使用できます。たとえば、 `LIMIT 10`です。Hibernate クエリ言語 (HQL) で`LIMIT`を含む SQL ステートメントを実行すると、エラーが発生します。Hibernate ステートメントを SQL ステートメントに変更する必要があります。

### <code>UPDATE</code>ステートメントで複数のテーブルを更新する {#update-multiple-tables-in-an-code-update-code-statement}

Oracle では、複数のテーブルを更新するときに、特定のフィールド更新関係をリストする必要はありません。例:

```sql
UPDATE test1 SET(test1.name,test1.age) = (SELECT test2.name,test2.age FROM test2 WHERE test2.id=test1.id)
```

TiDB では、複数のテーブルを更新する場合、特定のフィールドの更新関係をすべて`SET`にリストする必要があります。例:

```sql
UPDATE test1,test2 SET test1.name=test2.name,test1.age=test2.age WHERE test1.id=test2.id
```

### 派生テーブル別名 {#derived-table-alias}

Oracle では、複数のテーブルをクエリする場合、派生テーブルに別名を追加する必要はありません。例:

```sql
SELECT * FROM (SELECT * FROM test)
```

TiDB では、複数のテーブルをクエリする場合、派生テーブルごとに独自のエイリアスが必要です。例:

```sql
SELECT * FROM (SELECT * FROM test) t
```

### 集合演算 {#set-operations}

Oracle では、最初のクエリ結果にはあるが 2 番目のクエリ結果にはない行を取得するには、 `MINUS`セット操作を使用できます。例:

```sql
SELECT * FROM t1 MINUS SELECT * FROM t2
```

TiDB は`MINUS`操作をサポートしていません。3 `EXCEPT`操作を使用できます。例:

```sql
SELECT * FROM t1 EXCEPT SELECT * FROM t2
```

### コメント構文 {#comment-syntax}

Oracle では、コメント構文は`--Comment`です。

TiDB では、コメント構文は`-- Comment`です。TiDB では`--`後に空白があることに注意してください。

### ページネーション {#pagination}

Oracle では、 `OFFSET m ROWS`使用して`m`行をスキップし、 `FETCH NEXT n ROWS ONLY`を使用して`n`行をフェッチできます。例:

```sql
SELECT * FROM tables OFFSET 0 ROWS FETCH NEXT 2000 ROWS ONLY
```

TiDB では、 `OFFSET m ROWS FETCH NEXT n ROWS ONLY`代わりに`LIMIT n OFFSET m`使用できます。例:

```sql
SELECT * FROM tables LIMIT 2000 OFFSET 0
```

### <code>NULL</code>値のソート順 {#sorting-order-on-code-null-code-values}

Oracle では、次の場合に`NULL`値が`ORDER BY`句によってソートされます。

-   `ORDER BY column ASC`ステートメントでは、最後に`NULL`値が返されます。

-   `ORDER BY column DESC`ステートメントでは、最初に`NULL`値が返されます。

-   `ORDER BY column [ASC|DESC] NULLS FIRST`文では、 `NULL`の値が NULL 以外の値の前に返されます。 NULL 以外の値は、 `ASC|DESC`で指定された昇順または降順で返されます。

-   `ORDER BY column [ASC|DESC] NULLS LAST`文では、非 NULL 値の後に`NULL`値が返されます。非 NULL 値は、 `ASC|DESC`で指定された昇順または降順で返されます。

TiDB では、次の場合に`NULL`値が`ORDER BY`句によってソートされます。

-   `ORDER BY column ASC`ステートメントでは、最初に`NULL`値が返されます。

-   `ORDER BY column DESC`ステートメントでは、最後に`NULL`値が返されます。

次の表は、Oracle と TiDB の同等の`ORDER BY`ステートメントの例を示しています。

| Oracle の`ORDER BY`                                 | TiDB の同等のステートメント                                          |
| :------------------------------------------------- | :-------------------------------------------------------- |
| `SELECT * FROM t1 ORDER BY name NULLS FIRST;`      | `SELECT * FROM t1 ORDER BY name;`                         |
| `SELECT * FROM t1 ORDER BY name DESC NULLS LAST;`  | `SELECT * FROM t1 ORDER BY name DESC;`                    |
| `SELECT * FROM t1 ORDER BY name DESC NULLS FIRST;` | `SELECT * FROM t1 ORDER BY ISNULL(name) DESC, name DESC;` |
| `SELECT * FROM t1 ORDER BY name ASC NULLS LAST;`   | `SELECT * FROM t1 ORDER BY ISNULL(name), name;`           |
