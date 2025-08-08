---
title: Numeric Types
summary: TiDB でサポートされている数値データ型について学習します。
---

# 数値型 {#numeric-types}

TiDB は、以下を含むすべての MySQL 数値型をサポートしています。

-   [整数型](#integer-types) (正確な値)
-   [浮動小数点型](#floating-point-types) (近似値)
-   [固定小数点型](#fixed-point-types) (正確な値)

## 整数型 {#integer-types}

TiDBは、 `INTEGER` / `INT` 、 `TINYINT` 、 `SMALLINT` 、 `MEDIUMINT` 、 `BIGINT`を含むすべてのMySQL整数型をサポートしています。詳細については、 [MySQLの整数データ型の構文](https://dev.mysql.com/doc/refman/8.0/en/integer-types.html)参照してください。

次の表はフィールドの説明をまとめたものです。

<CustomContent platform="tidb">

> **警告：**
>
> バージョン8.5.0以降、整数の表示幅は非推奨となりました（デフォルトでは[`deprecate-integer-display-length`](/tidb-configuration-file.md#deprecate-integer-display-length)が`true`なります）。整数型の表示幅の指定は推奨されません。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **警告：**
>
> バージョン8.5.0以降、整数の表示幅は非推奨となりました。整数型の表示幅の指定は推奨されません。

</CustomContent>

| 構文要素  | 説明                                                   |
| ----- | ---------------------------------------------------- |
| M     | タイプの表示幅。オプション。                                       |
| 署名なし  | UNSIGNED。省略した場合はSIGNEDになります。                         |
| ゼロフィル | 数値列に ZEROFILL を指定すると、TiDB は列に UNSIGNED 属性を自動的に追加します。 |

次の表は、TiDB でサポートされる整数型に必要なstorageと範囲をまとめたものです。

| データ型        | 必要なストレージ容量（バイト） | 最小値（符号付き/符号なし）           | 最大値（符号付き/符号なし）                             |
| ----------- | --------------- | ------------------------ | ------------------------------------------ |
| `TINYINT`   | 1               | -128 / 0                 | 127 / 255                                  |
| `SMALLINT`  | 2               | -32768 / 0               | 32767 / 65535                              |
| `MEDIUMINT` | 3               | -8388608 / 0             | 8388607 / 16777215                         |
| `INT`       | 4               | -2147483648 / 0          | 2147483647 / 4294967295                    |
| `BIGINT`    | 8               | -9223372036854775808 / 0 | 9223372036854775807 / 18446744073709551615 |

### <code>BIT</code>タイプ {#code-bit-code-type}

BITデータ型。BIT(M)型はMビット値をstorageします。Mは1から64までの範囲で指定でき、デフォルト値は1です。

```sql
BIT[(M)]
```

### <code>BOOLEAN</code>型 {#code-boolean-code-type}

`BOOLEAN`型とそのエイリアス`BOOL` `TINYINT(1)`と同等です。値が`0`場合は`False` 、それ以外の場合は`True`とみなされます。MySQLと同様に、 `True`は`1` 、 `False`は`0`です。

```sql
BOOLEAN
```

### <code>TINYINT</code>型 {#code-tinyint-code-type}

`TINYINT`データ型は、[-128, 127] の範囲の符号付き値と [0, 255] の範囲の符号なし値を格納します。

```sql
TINYINT[(M)] [UNSIGNED] [ZEROFILL]
```

### <code>SMALLINT</code>型 {#code-smallint-code-type}

`SMALLINT`データ型は、[-32768、32767]の範囲の符号付き値と、[0、65535]の範囲の符号なし値を格納します。

```sql
SMALLINT[(M)] [UNSIGNED] [ZEROFILL]
```

### <code>MEDIUMINT</code>タイプ {#code-mediumint-code-type}

`MEDIUMINT`データ型は、[-8388608、8388607]の範囲の符号付き値と、[0、16777215]の範囲の符号なし値を格納します。

```sql
MEDIUMINT[(M)] [UNSIGNED] [ZEROFILL]
```

### <code>INTEGER</code>型 {#code-integer-code-type}

`INTEGER`型とそのエイリアス`INT`は、[-2147483648、2147483647] の範囲の符号付き値と、[0、4294967295] の範囲の符号なし値を格納します。

```sql
INT[(M)] [UNSIGNED] [ZEROFILL]
```

別の形式を使用することもできます:

```sql
INTEGER[(M)] [UNSIGNED] [ZEROFILL]
```

### <code>BIGINT</code>型 {#code-bigint-code-type}

`BIGINT`データ型は、[-9223372036854775808、9223372036854775807]の範囲の符号付き値と、[0、18446744073709551615]の範囲の符号なし値を格納します。

```sql
BIGINT[(M)] [UNSIGNED] [ZEROFILL]
```

## 浮動小数点型 {#floating-point-types}

TiDBは、 `FLOAT` 、 `DOUBLE`含むすべてのMySQL浮動小数点型をサポートしています。詳細については、 [浮動小数点型（近似値） - MySQL の FLOAT、DOUBLE](https://dev.mysql.com/doc/refman/8.0/en/floating-point-types.html)参照してください。

次の表はフィールドの説明をまとめたものです。

| 構文要素  | 説明                                                   |
| ----- | ---------------------------------------------------- |
| M     | 桁の総数                                                 |
| D     | 小数点以下の桁数                                             |
| 署名なし  | UNSIGNED。省略した場合はSIGNEDになります。                         |
| ゼロフィル | 数値列に ZEROFILL を指定すると、TiDB は列に UNSIGNED 属性を自動的に追加します。 |

次の表は、TiDB でサポートされる浮動小数点型に必要なstorageをまとめたものです。

| データ型       | 必要なストレージ容量（バイト）                                  |
| ---------- | ------------------------------------------------ |
| `FLOAT`    | 4                                                |
| `FLOAT(p)` | 0 &lt;= p &lt;= 24の場合は4、25 &lt;= p &lt;= 53の場合は8 |
| `DOUBLE`   | 8                                                |

### <code>FLOAT</code>型 {#code-float-code-type}

`FLOAT`型は単精度浮動小数点数を保存します。許容値は-3.402823466E+38～-1.175494351E-38、0、1.175494351E-38～3.402823466E+38です。これらはIEEE標準に基づく理論上の制限です。実際の範囲は、ハードウェアやオペレーティングシステムによって若干狭くなる場合があります。

`FLOAT(p)`必要なビット精度を表すために使用できます。TiDB はこの値を使用して、結果のデータ型に`FLOAT`使用するか`DOUBLE`使用するかを決定します。p が 0 から 24 の場合、データ型は M 値または D 値を持たない FLOAT になります。p が 25 から 53 の場合、データ型は M 値または D 値を持たない`DOUBLE`になります。結果の列の範囲は、単精度`FLOAT`または倍精度`DOUBLE`データ型と同じです。

```sql
FLOAT[(M,D)] [UNSIGNED] [ZEROFILL]
FLOAT(p) [UNSIGNED] [ZEROFILL]
```

> **注記：**
>
> MySQLと同様に、 `FLOAT`データ型は近似値を保存します。通貨などの値の場合は、代わりに`DECIMAL`データ型を使用することをお勧めします。
>
> TiDBでは、 `FLOAT`データ型のデフォルトの精度は8桁ですが、MySQLでは6桁です。例えば、TiDBとMySQLの両方で`FLOAT`型の列に`123456789`と`1.23456789`挿入した場合、MySQLで対応する値をクエリすると、 `123457000`と`1.23457`返されますが、TiDBでは`123456790`と`1.2345679`返されます。

### <code>DOUBLE</code>型 {#code-double-code-type}

`DOUBLE`型とそのエイリアス`DOUBLE PRECISION`は、倍精度浮動小数点数を格納します。許容値は -1.7976931348623157E+308 ～ -2.2250738585072014E-308、0、および 2.2250738585072014E-308 ～ 1.7976931348623157E+308 です。これらは IEEE 標準に基づく理論上の制限です。実際の範囲は、ハードウェアやオペレーティングシステムによって若干狭くなる場合があります。

```sql
DOUBLE[(M,D)] [UNSIGNED] [ZEROFILL]
DOUBLE PRECISION [(M,D)] [UNSIGNED] [ZEROFILL], REAL[(M,D)] [UNSIGNED] [ZEROFILL]
```

> **警告：**
>
> MySQLと同様に、 `DOUBLE`データ型は近似値を保存します。通貨などの値の場合は、代わりに`DECIMAL`データ型を使用することをお勧めします。

> **注記：**
>
> TiDBが科学表記法で表現された倍精度浮動小数点数を`CHAR`型に変換すると、MySQLでの表示と矛盾する結果が表示されます。詳細は[キャスト関数と演算子](/functions-and-operators/cast-functions-and-operators.md)参照してください。

## 固定小数点型 {#fixed-point-types}

TiDBは、DECIMALやNUMERICを含むすべてのMySQL浮動小数点型をサポートしています。詳細については、 [固定小数点型（正確な値） - MySQL の DECIMAL、NUMERIC](https://dev.mysql.com/doc/refman/8.0/en/fixed-point-types.html) 。

フィールドの意味:

| 構文要素  | 説明                                                   |
| ----- | ---------------------------------------------------- |
| M     | 小数点以下の桁数                                             |
| D     | 小数点以下の桁数                                             |
| 署名なし  | UNSIGNED。省略した場合はSIGNEDになります。                         |
| ゼロフィル | 数値列に ZEROFILL を指定すると、TiDB は列に UNSIGNED 属性を自動的に追加します。 |

### <code>DECIMAL</code>型 {#code-decimal-code-type}

`DECIMAL`とそのエイリアス`NUMERIC`は、パックされた「正確な」固定小数点数を格納します。M は小数点以下の桁数（精度）、D は小数点以下の桁数（スケール）です。小数点と（負数の場合は）- 記号は M には含まれません。D が 0 の場合、値には小数点も小数部もありません。DECIMAL の最大桁数（M）は 65 です。サポートされる小数点の最大桁数（D）は 30 です。D が省略された場合、デフォルトは 0 です。M が省略された場合、デフォルトは 10 です。

```sql
DECIMAL[(M[,D])] [UNSIGNED] [ZEROFILL]
NUMERIC[(M[,D])] [UNSIGNED] [ZEROFILL]
```
