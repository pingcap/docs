---
title: Numeric Types
summary: Learn about numeric data types supported in TiDB.
---

# 数値型 {#numeric-types}

TiDB は、以下を含むすべての MySQL 数値型をサポートしています。

-   [整数型](#integer-types) (正確な値)
-   [浮動小数点型](#floating-point-types) (近似値)
-   [固定小数点型](#fixed-point-types) (正確な値)

## 整数型 {#integer-types}

TiDB は、 `INTEGER` / `INT` 、 `TINYINT` 、 `SMALLINT` 、 `MEDIUMINT` 、および`BIGINT`を含むすべての MySQL 整数型をサポートしています。詳細については、 [MySQL の整数データ型の構文](https://dev.mysql.com/doc/refman/5.7/en/integer-types.html)参照してください。

次の表は、フィールドの説明をまとめたものです。

| 構文要素  | 説明                                                   |
| ----- | ---------------------------------------------------- |
| M     | タイプの表示幅。オプション。                                       |
| 未署名   | 未署名。省略した場合は SIGNED です。                               |
| ゼロフィル | 数値列に ZEROFILL を指定すると、TiDB は UNSIGNED 属性を列に自動的に追加します。 |

次の表は、TiDB でサポートされている整数型に必要なstorageと範囲をまとめたものです。

| データ・タイプ     | 必要なストレージ (バイト) | 最小値 (符号付き/符号なし)          | 最大値 (符号あり/符号なし)                            |
| ----------- | -------------- | ------------------------ | ------------------------------------------ |
| `TINYINT`   | 1              | -128 / 0                 | 127 / 255                                  |
| `SMALLINT`  | 2              | -32768 / 0               | 32767 / 65535                              |
| `MEDIUMINT` | 3              | -8388608 / 0             | 8388607 / 16777215                         |
| `INT`       | 4              | -2147483648 / 0          | 2147483647 / 4294967295                    |
| `BIGINT`    | 8              | -9223372036854775808 / 0 | 9223372036854775807 / 18446744073709551615 |

### <code>BIT</code>タイプ {#code-bit-code-type}

BIT データ型。 BIT(M) の型は、M ビット値のstorageを有効にします。 M は 1 ～ 64 の範囲で指定でき、デフォルト値は 1 です。

```sql
BIT[(M)]
```

### <code>BOOLEAN</code>型 {#code-boolean-code-type}

`BOOLEAN`型とそのエイリアス`BOOL` `TINYINT(1)`と同等です。値が`0`の場合、 `False`と見なされます。それ以外の場合は、 `True`と見なされます。 MySQL と同様に、 `True` `1`で、 `False`は`0`です。

```sql
BOOLEAN
```

### <code>TINYINT</code>型 {#code-tinyint-code-type}

`TINYINT`データ型は、範囲 [-128, 127] の符号付き値と範囲 [0, 255] の符号なし値を格納します。

```sql
TINYINT[(M)] [UNSIGNED] [ZEROFILL]
```

### <code>SMALLINT</code>型 {#code-smallint-code-type}

`SMALLINT`データ型は、範囲 [-32768, 32767] の符号付きの値と、範囲 [0, 65535] の符号なしの値を格納します。

```sql
SMALLINT[(M)] [UNSIGNED] [ZEROFILL]
```

### <code>MEDIUMINT</code>タイプ {#code-mediumint-code-type}

`MEDIUMINT`データ型は、範囲 [-8388608, 8388607] の符号付きの値と、範囲 [0, 16777215] の符号なしの値を格納します。

```sql
MEDIUMINT[(M)] [UNSIGNED] [ZEROFILL]
```

### <code>INTEGER</code>型 {#code-integer-code-type}

`INTEGER`型とそのエイリアス`INT` 、範囲 [-2147483648, 2147483647] の符号付きの値と、範囲 [0, 4294967295] の符号なしの値を格納します。

```sql
INT[(M)] [UNSIGNED] [ZEROFILL]
```

別のフォームを使用することもできます。

```sql
INTEGER[(M)] [UNSIGNED] [ZEROFILL]
```

### <code>BIGINT</code>型 {#code-bigint-code-type}

`BIGINT`データ型には、範囲 [-9223372036854775808, 9223372036854775807] の符号付きの値と、範囲 [0, 18446744073709551615] の符号なしの値が格納されます。

```sql
BIGINT[(M)] [UNSIGNED] [ZEROFILL]
```

## 浮動小数点型 {#floating-point-types}

TiDB は、 `FLOAT`および`DOUBLE`を含むすべての MySQL 浮動小数点型をサポートします。詳細については、 [浮動小数点型 (近似値) - MySQL の FLOAT、DOUBLE](https://dev.mysql.com/doc/refman/5.7/en/floating-point-types.html)を参照してください。

次の表は、フィールドの説明をまとめたものです。

| 構文要素  | 説明                                                   |
| ----- | ---------------------------------------------------- |
| M     | 総桁数                                                  |
| D     | 小数点以下の桁数                                             |
| 未署名   | 未署名。省略した場合は SIGNED です。                               |
| ゼロフィル | 数値列に ZEROFILL を指定すると、TiDB は UNSIGNED 属性を列に自動的に追加します。 |

次の表は、TiDB でサポートされる浮動小数点型に必要なstorageをまとめたものです。

| データ・タイプ    | 必要なストレージ (バイト)                                              |
| ---------- | ----------------------------------------------------------- |
| `FLOAT`    | 4                                                           |
| `FLOAT(p)` | 0 &lt;= p &lt;= 24 の場合は 4 です。 25 &lt;= p &lt;= 53 の場合、8 です。 |
| `DOUBLE`   | 8                                                           |

### <code>FLOAT</code>型 {#code-float-code-type}

`FLOAT`型は単精度浮動小数点数を格納します。許容値は -3.402823466E+38 ～ -1.175494351E-38、0、および 1.175494351E-38 ～ 3.402823466E+38 です。これらは、IEEE 規格に基づく理論上の制限です。ハードウェアまたはオペレーティング システムによっては、実際の範囲がわずかに小さくなる場合があります。

`FLOAT(p)`を使用して、必要な精度をビット単位で表すことができます。 TiDB は、この値を使用して、結果のデータ型に`FLOAT`または`DOUBLE`のどちらを使用するかを決定します。 p が 0 から 24 の場合、データ型は M または D 値のない FLOAT になります。 p が 25 から 53 の場合、データ型は`DOUBLE`になり、M または D の値はありません。結果の列の範囲は、単精度`FLOAT`または倍精度`DOUBLE`データ型の場合と同じです。

```sql
FLOAT[(M,D)] [UNSIGNED] [ZEROFILL]
FLOAT(p) [UNSIGNED] [ZEROFILL]
```

> **ノート：**
>
> MySQL と同様に、 `FLOAT`データ型には近似値が格納されます。通貨などの値については、代わりに`DECIMAL`型を使用することをお勧めします。
>
> TiDB では`FLOAT`データ型のデフォルトの精度は 8 桁ですが、MySQL ではデフォルトの精度は 6 桁です。たとえば、TiDB と MySQL の両方で`FLOAT`型の列に`123456789`と`1.23456789`を挿入すると仮定すると、MySQL で対応する値をクエリすると`123457000`と`1.23457`が得られますが、TiDB では`123456790`と`1.2345679`が得られます。

### <code>DOUBLE</code>タイプ {#code-double-code-type}

`DOUBLE`型とそのエイリアス`DOUBLE PRECISION`は、倍精度浮動小数点数を格納します。許容値は -1.7976931348623157E+308 ～ -2.2250738585072014E-308、0、および 2.2250738585072014E-308 ～ 1.7976931348623157E+308 です。これらは、IEEE 規格に基づく理論上の制限です。ハードウェアまたはオペレーティング システムによっては、実際の範囲がわずかに小さくなる場合があります。

```sql
DOUBLE[(M,D)] [UNSIGNED] [ZEROFILL]
DOUBLE PRECISION [(M,D)] [UNSIGNED] [ZEROFILL], REAL[(M,D)] [UNSIGNED] [ZEROFILL]
```

> **警告：**
>
> MySQL と同様に、 `DOUBLE`データ型には近似値が格納されます。通貨などの値については、代わりに`DECIMAL`型を使用することをお勧めします。

## 固定小数点型 {#fixed-point-types}

TiDB は、DECIMAL や NUMERIC を含むすべての MySQL 浮動小数点型をサポートしています。詳細については、 [固定小数点型 (正確な値) - MySQL の DECIMAL、NUMERIC](https://dev.mysql.com/doc/refman/5.7/en/fixed-point-types.html) .

フィールドの意味:

| 構文要素  | 説明                                                   |
| ----- | ---------------------------------------------------- |
| M     | 10 進数の合計桁数                                           |
| D     | 小数点以下の桁数                                             |
| 未署名   | 未署名。省略した場合は SIGNED です。                               |
| ゼロフィル | 数値列に ZEROFILL を指定すると、TiDB は UNSIGNED 属性を列に自動的に追加します。 |

### <code>DECIMAL</code>型 {#code-decimal-code-type}

`DECIMAL`とそのエイリアス`NUMERIC` 、パックされた「正確な」固定小数点数を格納します。 M は 10 進数の合計桁数 (精度)、D は小数点以下の桁数 (位取り) です。小数点と (負の数の場合) - 記号は M ではカウントされません。D が 0 の場合、値には小数点または小数部分がありません。 DECIMAL の最大桁数 (M) は 65 です。サポートされている小数 (D) の最大数は 30 です。D が省略された場合、デフォルトは 0 です。M が省略された場合、デフォルトは 10 です。

```sql
DECIMAL[(M[,D])] [UNSIGNED] [ZEROFILL]
NUMERIC[(M[,D])] [UNSIGNED] [ZEROFILL]
```
