---
title: Numeric Types
summary: Learn about numeric data types supported in TiDB.
---

# 数値タイプ {#numeric-types}

TiDBは、以下を含むすべてのMySQL数値タイプをサポートします。

-   [整数型](#integer-types) （正確な値）
-   [浮動小数点型](#floating-point-types) （概算値）
-   [固定小数点タイプ](#fixed-point-types) （正確な値）

## 整数型 {#integer-types}

`TINYINT`は、 `INTEGER` / `INT` 、および`SMALLINT`を含むすべてのMySQL整数型を`BIGINT`し`MEDIUMINT` 。詳細については、 [MySQLの整数データ型構文](https://dev.mysql.com/doc/refman/5.7/en/integer-types.html)を参照してください。

次の表は、フィールドの説明をまとめたものです。

| 構文要素  | 説明                                              |
| ----- | ----------------------------------------------- |
| M     | タイプの表示幅。オプション。                                  |
| 未署名   | 署名なし。省略した場合はSIGNEDです。                           |
| ゼロフィル | 数値列にZEROFILLを指定すると、TiDBは自動的にUNSIGNED属性を列に追加します。 |

次の表は、TiDBでサポートされている整数型に必要なストレージと範囲をまとめたものです。

| データ・タイプ     | 必要なストレージ（バイト） | 最小値（符号付き/符号なし）           | 最大値（符号付き/符号なし）                           |
| ----------- | ------------- | ------------------------ | ---------------------------------------- |
| `TINYINT`   | 1             | -128/0                   | 127/255                                  |
| `SMALLINT`  | 2             | -32768/0                 | 32767/65535                              |
| `MEDIUMINT` | 3             | -8388608 / 0             | 8388607/16777215                         |
| `INT`       | 4             | -2147483648/0            | 2147483647/4294967295                    |
| `BIGINT`    | 8             | -9223372036854775808 / 0 | 9223372036854775807/18446744073709551615 |

### <code>BIT</code>タイプ {#code-bit-code-type}

BITデータ型。 BIT（M）のタイプは、Mビット値の格納を可能にします。 Mの範囲は1〜64で、デフォルト値は1です。

```sql
BIT[(M)]
```

### <code>BOOLEAN</code>型 {#code-boolean-code-type}

`BOOLEAN`タイプとそのエイリアス`BOOL`は`TINYINT(1)`と同等です。値が`0`の場合、 `False`と見なされます。それ以外の場合は、 `True`と見なされます。 MySQLと同様に、 `True`は`1`は`False` `0` 。

```sql
BOOLEAN
```

### <code>TINYINT</code>タイプ {#code-tinyint-code-type}

`TINYINT`データ型は、範囲[-128、127]の符号付き値と範囲[0、255]の符号なし値を格納します。

```sql
TINYINT[(M)] [UNSIGNED] [ZEROFILL]
```

### <code>SMALLINT</code>タイプ {#code-smallint-code-type}

`SMALLINT`データ型は、範囲[-32768、32767]の符号付きの値と、範囲[0、65535]の符号なしの値を格納します。

```sql
SMALLINT[(M)] [UNSIGNED] [ZEROFILL]
```

### <code>MEDIUMINT</code>タイプ {#code-mediumint-code-type}

`MEDIUMINT`データ型は、範囲[-8388608、8388607]の符号付きの値と、範囲[0、16777215]の符号なしの値を格納します。

```sql
MEDIUMINT[(M)] [UNSIGNED] [ZEROFILL]
```

### <code>INTEGER</code>タイプ {#code-integer-code-type}

`INTEGER`タイプとそのエイリアス`INT`は、範囲[-2147483648、2147483647]の符号付き値と、範囲[0、4294967295]の符号なし値を格納します。

```sql
INT[(M)] [UNSIGNED] [ZEROFILL]
```

別のフォームを使用することもできます。

```sql
INTEGER[(M)] [UNSIGNED] [ZEROFILL]
```

### <code>BIGINT</code>タイプ {#code-bigint-code-type}

`BIGINT`データ型は、範囲[-9223372036854775808、9223372036854775807]の符号付き値と範囲[0、18446744073709551615]の符号なし値を格納します。

```sql
BIGINT[(M)] [UNSIGNED] [ZEROFILL]
```

## 浮動小数点型 {#floating-point-types}

TiDBは、 `FLOAT` 、および`DOUBLE`を含むすべてのMySQL浮動小数点型をサポートします。詳細については、 [浮動小数点型（概算値）-MySQLのFLOAT、DOUBLE](https://dev.mysql.com/doc/refman/5.7/en/floating-point-types.html)を参照してください。

次の表は、フィールドの説明をまとめたものです。

| 構文要素  | 説明                                              |
| ----- | ----------------------------------------------- |
| M     | 総桁数                                             |
| D     | 小数点以下の桁数                                        |
| 未署名   | 署名なし。省略した場合はSIGNEDです。                           |
| ゼロフィル | 数値列にZEROFILLを指定すると、TiDBは自動的にUNSIGNED属性を列に追加します。 |

次の表は、TiDBでサポートされている浮動小数点型に必要なストレージをまとめたものです。

| データ・タイプ    | 必要なストレージ（バイト）                                          |
| ---------- | ------------------------------------------------------ |
| `FLOAT`    | 4                                                      |
| `FLOAT(p)` | 0 &lt;= p &lt;= 24の場合、4です。 25 &lt;= p &lt;= 53の場合、8です。 |
| `DOUBLE`   | 8                                                      |

### <code>FLOAT</code>タイプ {#code-float-code-type}

`FLOAT`タイプは、単精度浮動小数点数を格納します。許容値は、-3.402823466E + 38〜-1.175494351E-38、0、および1.175494351E-38〜3.402823466E+38です。これらは、IEEE標準に基づく理論上の制限です。ハードウェアまたはオペレーティングシステムによっては、実際の範囲がわずかに小さくなる場合があります。

`FLOAT(p)`は、必要な精度をビットで表すために使用できます。 TiDBはこの値を使用して、結果のデータ型に`FLOAT`と`DOUBLE`のどちらを使用するかを決定します。 pが0〜24の場合、データ型はMまたはD値のないFLOATになります。 pが25〜53の場合、データ型は`DOUBLE`になり、M値またはD値はありません。結果の列の範囲は、単精度`FLOAT`または倍精度`DOUBLE`のデータ型の場合と同じです。

```sql
FLOAT[(M,D)] [UNSIGNED] [ZEROFILL]
FLOAT(p) [UNSIGNED] [ZEROFILL]
```

> **ノート：**
>
> MySQLと同様に、 `FLOAT`データ型は概算値を格納します。通貨などの値については、代わりに`DECIMAL`タイプを使用することをお勧めします。 TiDBでは、 `FLOAT`データ型のデフォルトの精度は8ビットですが、MySQLでは、デフォルトの精度は6ビットです。たとえば、TiDBとMySQLの両方で`FLOAT`タイプの列に`123456789`と`1.23456789`を挿入すると、MySQLで対応する値をクエリすると、 `123457000`と`1.23457`が得られますが、TiDBでは`123456790`と`1.2345679`が得られます。

### <code>DOUBLE</code>タイプ {#code-double-code-type}

`DOUBLE`型とそのエイリアス`DOUBLE PRECISION`は、倍精度浮動小数点数を格納します。許容値は、-1.7976931348623157E + 308〜-2.2250738585072014E-308、0、および2.2250738585072014E-308〜1.7976931348623157E+308です。これらは、IEEE標準に基づく理論上の制限です。ハードウェアまたはオペレーティングシステムによっては、実際の範囲がわずかに小さくなる場合があります。

```sql
DOUBLE[(M,D)] [UNSIGNED] [ZEROFILL]
DOUBLE PRECISION [(M,D)] [UNSIGNED] [ZEROFILL], REAL[(M,D)] [UNSIGNED] [ZEROFILL]
```

> **警告：**
>
> MySQLと同様に、 `DOUBLE`データ型は概算値を格納します。通貨などの値については、代わりに`DECIMAL`タイプを使用することをお勧めします。

## 固定小数点タイプ {#fixed-point-types}

TiDBは、DECIMALやNUMERICを含むすべてのMySQL浮動小数点型をサポートしています。詳細については、 [固定小数点タイプ（正確な値）-MySQLのDECIMAL、NUMERIC](https://dev.mysql.com/doc/refman/5.7/en/fixed-point-types.html) 。

フィールドの意味：

| 構文要素  | 説明                                              |
| ----- | ----------------------------------------------- |
| M     | 小数点以下の桁数の合計                                     |
| D     | 小数点以下の桁数                                        |
| 未署名   | 署名なし。省略した場合はSIGNEDです。                           |
| ゼロフィル | 数値列にZEROFILLを指定すると、TiDBは自動的にUNSIGNED属性を列に追加します。 |

### <code>DECIMAL</code>タイプ {#code-decimal-code-type}

`DECIMAL`とそのエイリアス`NUMERIC`は、パックされた「正確な」固定小数点数を格納します。 Mは小数点以下の合計桁数（精度）、Dは小数点以下の桁数（目盛り）です。小数点と（負の数の場合）-記号はMではカウントされません。Dが0の場合、値には小数点または小数部がありません。 DECIMALの最大桁数（M）は65です。サポートされる小数点以下の最大数（D）は30です。Dを省略した場合のデフォルトは0です。Mを省略した場合のデフォルトは10です。

```sql
DECIMAL[(M[,D])] [UNSIGNED] [ZEROFILL]
NUMERIC[(M[,D])] [UNSIGNED] [ZEROFILL]
```
