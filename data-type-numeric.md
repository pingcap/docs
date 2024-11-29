---
title: Numeric Types
summary: TiDB でサポートされている数値データ型について学習します。
---

# 数値型 {#numeric-types}

TiDB は、以下を含むすべての MySQL 数値型をサポートしています。

-   [整数型](#integer-types) (正確な値)
-   [浮動小数点型](#floating-point-types) (おおよその値)
-   [固定小数点型](#fixed-point-types) (正確な値)

## 整数型 {#integer-types}

TiDB は、 `INTEGER` / `INT` 、 `TINYINT` 、 `SMALLINT` 、 `MEDIUMINT` 、 `BIGINT`を含むすべての MySQL 整数型をサポートしています。詳細については、 [MySQL の整数データ型構文](https://dev.mysql.com/doc/refman/8.0/en/integer-types.html)参照してください。

次の表はフィールドの説明をまとめたものです。

| 構文要素  | 説明                                                   |
| ----- | ---------------------------------------------------- |
| ま     | タイプの表示幅。オプション。                                       |
| 未署名   | UNSIGNED。省略した場合はSIGNEDになります。                         |
| ゼロフィル | 数値列に ZEROFILL を指定すると、TiDB は列に UNSIGNED 属性を自動的に追加します。 |

次の表は、TiDB でサポートされる整数型に必要なstorageと範囲をまとめたものです。

| データタイプ      | 必要なストレージ容量 (バイト) | 最小値（符号付き/符号なし）           | 最大値（符号付き/符号なし）                             |
| ----------- | ---------------- | ------------------------ | ------------------------------------------ |
| `TINYINT`   | 1                | -128 / 0                 | 127 / 255                                  |
| `SMALLINT`  | 2                | -32768 / 0               | 32767 / 65535                              |
| `MEDIUMINT` | 3                | -8388608 / 0             | 8388607 / 16777215                         |
| `INT`       | 4                | -2147483648 / 0          | 2147483647 / 4294967295                    |
| `BIGINT`    | 8                | -9223372036854775808 / 0 | 9223372036854775807 / 18446744073709551615 |

### <code>BIT</code>タイプ {#code-bit-code-type}

BIT データ型。BIT(M) 型では、M ビット値のstorageが可能になります。M の範囲は 1 から 64 で、デフォルト値は 1 です。

```sql
BIT[(M)]
```

### <code>BOOLEAN</code>型 {#code-boolean-code-type}

`BOOLEAN`型とその別名`BOOL` `TINYINT(1)`と同等です。値が`0`の場合は`False`とみなされ、それ以外の場合は`True`とみなされます。MySQL と同様に、 `True`は`1` 、 `False`は`0`です。

```sql
BOOLEAN
```

### <code>TINYINT</code>型 {#code-tinyint-code-type}

`TINYINT`データ型は、範囲 [-128, 127] の符号付き値と範囲 [0, 255] の符号なし値を格納します。

```sql
TINYINT[(M)] [UNSIGNED] [ZEROFILL]
```

### <code>SMALLINT</code>型 {#code-smallint-code-type}

`SMALLINT`データ型は、[-32768、32767] の範囲の符号付き値と、[0、65535] の範囲の符号なし値を格納します。

```sql
SMALLINT[(M)] [UNSIGNED] [ZEROFILL]
```

### <code>MEDIUMINT</code>タイプ {#code-mediumint-code-type}

`MEDIUMINT`データ型は、[-8388608、8388607] の範囲の符号付き値と、[0、16777215] の範囲の符号なし値を格納します。

```sql
MEDIUMINT[(M)] [UNSIGNED] [ZEROFILL]
```

### <code>INTEGER</code>型 {#code-integer-code-type}

`INTEGER`型とそのエイリアス`INT`は、範囲 [-2147483648、2147483647] の符号付き値と範囲 [0、4294967295] の符号なし値を格納します。

```sql
INT[(M)] [UNSIGNED] [ZEROFILL]
```

別の形式を使用することもできます:

```sql
INTEGER[(M)] [UNSIGNED] [ZEROFILL]
```

### <code>BIGINT</code>型 {#code-bigint-code-type}

`BIGINT`データ型は、[-9223372036854775808、9223372036854775807] の範囲の符号付き値と、[0、18446744073709551615] の範囲の符号なし値を格納します。

```sql
BIGINT[(M)] [UNSIGNED] [ZEROFILL]
```

## 浮動小数点型 {#floating-point-types}

TiDB は、 `FLOAT` 、 `DOUBLE`を含むすべての MySQL 浮動小数点型をサポートしています。詳細については、 [浮動小数点型 (近似値) - MySQL の FLOAT、DOUBLE](https://dev.mysql.com/doc/refman/8.0/en/floating-point-types.html)参照してください。

次の表はフィールドの説明をまとめたものです。

| 構文要素  | 説明                                                   |
| ----- | ---------------------------------------------------- |
| ま     | 桁の総数                                                 |
| だ     | 小数点以下の桁数                                             |
| 未署名   | UNSIGNED。省略した場合はSIGNEDになります。                         |
| ゼロフィル | 数値列に ZEROFILL を指定すると、TiDB は列に UNSIGNED 属性を自動的に追加します。 |

次の表は、TiDB でサポートされる浮動小数点型に必要なstorageをまとめたものです。

| データタイプ     | 必要なストレージ容量 (バイト)                                 |
| ---------- | ------------------------------------------------ |
| `FLOAT`    | 4                                                |
| `FLOAT(p)` | 0 &lt;= p &lt;= 24の場合は4、25 &lt;= p &lt;= 53の場合は8 |
| `DOUBLE`   | 8                                                |

### <code>FLOAT</code>型 {#code-float-code-type}

`FLOAT`型は単精度浮動小数点数を格納します。許容値は -3.402823466E+38 ～ -1.175494351E-38、0、および 1.175494351E-38 ～ 3.402823466E+38 です。これらは IEEE 標準に基づく理論上の制限です。実際の範囲は、ハードウェアまたはオペレーティング システムによっては若干小さくなる場合があります。

`FLOAT(p)` 、必要な精度をビット単位で表すために使用できます。TiDB はこの値を使用して、結果のデータ型に`FLOAT`使用するか`DOUBLE`使用するかを決定します。p が 0 から 24 の場合、データ型は M 値または D 値のない FLOAT になります。p が 25 から 53 の場合、データ型は M 値または D 値のない`DOUBLE`なります。結果の列の範囲は、単精度`FLOAT`または倍精度`DOUBLE`データ型の場合と同じです。

```sql
FLOAT[(M,D)] [UNSIGNED] [ZEROFILL]
FLOAT(p) [UNSIGNED] [ZEROFILL]
```

> **注記：**
>
> MySQL と同様に、 `FLOAT`データ型には近似値が格納されます。通貨などの値の場合は、代わりに`DECIMAL`型を使用することをお勧めします。
>
> TiDB では、 `FLOAT`データ型のデフォルトの精度は 8 桁ですが、MySQL では、デフォルトの精度は 6 桁です。たとえば、TiDB と MySQL の両方で`FLOAT`型の列に`123456789`と`1.23456789`挿入すると、MySQL で対応する値をクエリすると`123457000`と`1.23457`返されますが、TiDB では`123456790`と`1.2345679`返されます。

### <code>DOUBLE</code>型 {#code-double-code-type}

`DOUBLE`型とそのエイリアス`DOUBLE PRECISION` 、倍精度浮動小数点数を格納します。許容される値は、-1.7976931348623157E+308 ～ -2.2250738585072014E-308、0、および 2.2250738585072014E-308 ～ 1.7976931348623157E+308 です。これらは、IEEE 標準に基づく理論上の制限です。実際の範囲は、ハードウェアまたはオペレーティング システムによっては若干小さくなる場合があります。

```sql
DOUBLE[(M,D)] [UNSIGNED] [ZEROFILL]
DOUBLE PRECISION [(M,D)] [UNSIGNED] [ZEROFILL], REAL[(M,D)] [UNSIGNED] [ZEROFILL]
```

> **警告：**
>
> MySQL と同様に、 `DOUBLE`データ型には近似値が格納されます。通貨などの値の場合は、代わりに`DECIMAL`型を使用することをお勧めします。

> **注記：**
>
> TiDB が科学的記数法で表現された倍精度浮動小数点数を`CHAR`型に変換すると、MySQL と結果が一致せずに表示されます。詳細は[キャスト関数と演算子](/functions-and-operators/cast-functions-and-operators.md)参照してください。

## 固定小数点型 {#fixed-point-types}

TiDB は、DECIMAL や NUMERIC を含むすべての MySQL 浮動小数点型をサポートしています。詳細については、 [固定小数点型 (正確な値) - MySQL の DECIMAL、NUMERIC](https://dev.mysql.com/doc/refman/8.0/en/fixed-point-types.html)参照してください。

フィールドの意味:

| 構文要素  | 説明                                                   |
| ----- | ---------------------------------------------------- |
| ま     | 小数点以下の桁数                                             |
| だ     | 小数点以下の桁数                                             |
| 未署名   | UNSIGNED。省略した場合はSIGNEDになります。                         |
| ゼロフィル | 数値列に ZEROFILL を指定すると、TiDB は列に UNSIGNED 属性を自動的に追加します。 |

### <code>DECIMAL</code>型 {#code-decimal-code-type}

`DECIMAL`とそのエイリアス`NUMERIC`パックされた「正確な」固定小数点数を格納します。M は小数点以下の桁数 (精度) で、D は小数点以下の桁数 (スケール) です。小数点と (負の数の場合) - 記号は M には含まれません。D が 0 の場合、値には小数点も小数部もありません。DECIMAL の最大桁数 (M) は 65 です。サポートされる小数点の最大数 (D) は 30 です。D を省略した場合、デフォルトは 0 です。M を省略した場合、デフォルトは 10 です。

```sql
DECIMAL[(M[,D])] [UNSIGNED] [ZEROFILL]
NUMERIC[(M[,D])] [UNSIGNED] [ZEROFILL]
```
