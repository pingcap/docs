---
title: Cast Functions and Operators
summary: キャスト関数と演算子について学習します。
---

# キャスト関数と演算子 {#cast-functions-and-operators}

キャスト関数と演算子を使用すると、あるデータ型から別のデータ型への値の変換が可能です。TiDBはMySQL 8.0で利用可能なすべての[キャスト関数と演算子](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html)をサポートしています。

| 名前                      | 説明               |
| ----------------------- | ---------------- |
| [`BINARY`](#binary)     | 文字列をバイナリ文字列に変換する |
| [`CAST()`](#cast)       | 値を特定の型にキャストする    |
| [`CONVERT()`](#convert) | 値を特定の型にキャストする    |

> **注記：**
>
> TiDBとMySQLは、 `SELECT CAST(MeN AS CHAR)` （またはそれに相当する`SELECT CONVERT(MeM, CHAR)` ）の結果に一貫性がありません。5 `MeN`倍精度浮動小数点数（科学的記数法）を表します。MySQLは`-15 <= N <= 14`場合は完全な数値を表示し、 `N < -15`または`N > 14`場合は科学的記数法を表示します。しかし、TiDBは常に完全な数値を表示します。例えば、MySQLでは`SELECT CAST(3.1415e15 AS CHAR)`の結果を`3.1415e15`と表示しますが、TiDBでは`3141500000000000`と表示します。

## バイナリ {#binary}

MySQL 8.0.27以降、 [`BINARY`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#operator_binary)演算子は非推奨となりました。TiDBとMySQLの両方で、代わりに`CAST(... AS BINARY)`を使用することをお勧めします。

## キャスト {#cast}

[`CAST(&#x3C;expression> AS &#x3C;type> [ARRAY])`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#function_cast)関数は、式を特定の型にキャストするために使用されます。

この関数は[多値インデックス](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)作成する場合にも使用されます。

次のタイプがサポートされています:

| タイプ                  | 説明                                        | 多値インデックスで使用できるかどうか   |
| -------------------- | ----------------------------------------- | -------------------- |
| `BINARY(n)`          | バイナリ文字列                                   | いいえ                  |
| `CHAR(n)`            | 文字列                                       | はい、ただし長さが指定されている場合のみ |
| `DATE`               | 日付                                        | はい                   |
| `DATETIME(fsp)`      | 日付/時刻（ `fsp`はオプション）                       | はい                   |
| `DECIMAL(n, m)`      | `n`進数。1 と`m`オプションで、指定しない場合は`10`と`0`になります。 | いいえ                  |
| `DOUBLE`             | 倍精度浮動小数点数                                 | いいえ                  |
| `FLOAT(n)`           | 浮動小数点数`n`オプションで、 `0`から`53`の範囲で指定します。      | いいえ                  |
| `JSON`               | JSON                                      | いいえ                  |
| `REAL`               | 浮動小数点数                                    | はい                   |
| `SIGNED [INTEGER]`   | 符号付き整数                                    | はい                   |
| `TIME(fsp)`          | 時間                                        | はい                   |
| `UNSIGNED [INTEGER]` | 符号なし整数                                    | はい                   |
| `VECTOR`             | ベクター                                      | いいえ                  |
| `YEAR`               | 年                                         | いいえ                  |

例:

次のステートメントは、バイナリ文字列を HEX リテラルから`CHAR`に変換します。

```sql
SELECT CAST(0x54694442 AS CHAR);
```

```sql
+--------------------------+
| CAST(0x54694442 AS CHAR) |
+--------------------------+
| TiDB                     |
+--------------------------+
1 row in set (0.0002 sec)
```

次の文は、JSON列から抽出された`a`の属性の値を符号なし配列にキャストします。配列へのキャストは、複数値インデックスのインデックス定義の一部としてのみサポートされることに注意してください。

```sql
CREATE TABLE t (
    id INT PRIMARY KEY,
    j JSON,
    INDEX idx_a ((CAST(j->'$.a' AS UNSIGNED ARRAY)))
);
INSERT INTO t VALUES (1, JSON_OBJECT('a',JSON_ARRAY(1,2,3)));
INSERT INTO t VALUES (2, JSON_OBJECT('a',JSON_ARRAY(4,5,6)));
INSERT INTO t VALUES (3, JSON_OBJECT('a',JSON_ARRAY(7,8,9)));
ANALYZE TABLE t;
```

```sql
 EXPLAIN SELECT * FROM t WHERE 1 MEMBER OF(j->'$.a')\G
*************************** 1. row ***************************
           id: IndexMerge_10
      estRows: 2.00
         task: root
access object: 
operator info: type: union
*************************** 2. row ***************************
           id: ├─IndexRangeScan_8(Build)
      estRows: 2.00
         task: cop[tikv]
access object: table:t, index:idx_a(cast(json_extract(`j`, _utf8mb4'$.a') as unsigned array))
operator info: range:[1,1], keep order:false, stats:partial[j:unInitialized]
*************************** 3. row ***************************
           id: └─TableRowIDScan_9(Probe)
      estRows: 2.00
         task: cop[tikv]
access object: table:t
operator info: keep order:false, stats:partial[j:unInitialized]
3 rows in set (0.00 sec)
```

## 変換する {#convert}

[`CONVERT()`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#function_convert)関数は[文字セット](/character-set-and-collation.md)間の変換に使用されます。

例：

```sql
SELECT CONVERT(0x616263 USING utf8mb4);
```

```sql
+---------------------------------+
| CONVERT(0x616263 USING utf8mb4) |
+---------------------------------+
| abc                             |
+---------------------------------+
1 row in set (0.0004 sec)
```

## MySQLの互換性 {#mysql-compatibility}

-   TiDBは`SPATIAL`型に対するキャスト演算をサポートしていません。詳細については[＃6347](https://github.com/pingcap/tidb/issues/6347)参照してください。
-   TiDBは`AT TIME ZONE` for `CAST()`をサポートしていません。詳細については[＃51742](https://github.com/pingcap/tidb/issues/51742)参照してください。
-   `CAST(24 AS YEAR)` TiDBでは2桁、MySQLでは4桁を返します。詳細については、 [＃29629](https://github.com/pingcap/tidb/issues/29629)参照してください。
