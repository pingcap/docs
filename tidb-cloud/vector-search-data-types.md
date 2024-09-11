---
title: Vector Data Types
summary: TiDB の Vector データ型について学習します。
---

# ベクトルデータ型 {#vector-data-types}

TiDB は、AI ベクトル埋め込みユースケース向けに特別に最適化されたベクトル データ型を提供します。ベクトル データ型を使用すると、 `[0.3, 0.5, -0.1, ...]`などの浮動小数点数のシーケンスを効率的に保存および照会できます。

現在、次のベクター データ型が利用可能です。

-   `VECTOR` : 単精度浮動小数点数のシーケンス。行ごとに次元が異なる場合があります。
-   `VECTOR(D)` : 固定次元`D`の単精度浮動小数点数のシーケンス。

Vector データ型は、 `JSON`列に格納する場合に比べて次の利点があります。

-   ベクトル インデックスのサポート。ベクトル検索を高速化するために[ベクター検索インデックス](/tidb-cloud/vector-search-index.md)構築できます。
-   次元の強制。異なる次元のベクトルの挿入を禁止するために次元を指定できます。
-   最適化されたstorage形式。ベクター データ型は、 `JSON`データ型よりもさらに効率的にスペースを節約して保存されます。

> **注記：**
>
> ベクトル データ型は[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターでのみ使用できます。

## 値の構文 {#value-syntax}

Vector 値には任意の数の浮動小数点数が含まれます。次の構文の文字列を使用して Vector 値を表すことができます。

```sql
'[<float>, <float>, ...]'
```

例：

```sql
CREATE TABLE vector_table (
    id INT PRIMARY KEY,
    embedding VECTOR(3)
);

INSERT INTO vector_table VALUES (1, '[0.3, 0.5, -0.1]');

INSERT INTO vector_table VALUES (2, NULL);
```

無効な構文でベクトル値を挿入すると、エラーが発生します。

```sql
[tidb]> INSERT INTO vector_table VALUES (3, '[5, ]');
ERROR 1105 (HY000): Invalid vector text: [5, ]
```

前の例では、 `embedding`列目に次元 3 が適用されているため、異なる次元のベクトルを挿入するとエラーが発生します。

```sql
[tidb]> INSERT INTO vector_table VALUES (4, '[0.3, 0.5]');
ERROR 1105 (HY000): vector has 2 dimensions, does not fit VECTOR(3)
```

Vector データ型で使用可能な関数と演算子については[ベクトル関数と演算子](/tidb-cloud/vector-search-functions-and-operators.md)参照してください。

ベクトル検索インデックスの構築と使用については、 [ベクター検索インデックス](/tidb-cloud/vector-search-index.md)参照してください。

## 異なる次元のベクトル {#vectors-with-different-dimensions}

`VECTOR`型の次元パラメータを省略すると、異なる次元のベクトルを同じ列に格納できます。

```sql
CREATE TABLE vector_table (
    id INT PRIMARY KEY,
    embedding VECTOR
);

INSERT INTO vector_table VALUES (1, '[0.3, 0.5, -0.1]'); -- 3 dimensions vector, OK
INSERT INTO vector_table VALUES (2, '[0.3, 0.5]');       -- 2 dimensions vector, OK
```

ただし、ベクトル距離は同じ次元のベクトル間でのみ計算できるため、この列に[ベクター検索インデックス](/tidb-cloud/vector-search-index.md)構築することはできません。

## 比較 {#comparison}

[比較演算子](/functions-and-operators/operators.md)を使用して、 `=` 、 `!=` 、 `<` 、 `>` 、 `<=` 、 `>=`などのベクトル データ型を比較できます。ベクトル データ型の比較演算子と関数の完全なリストについては、 [ベクトル関数と演算子](/tidb-cloud/vector-search-functions-and-operators.md)を参照してください。

ベクトル データ型は要素ごとに数値的に比較されます。例:

-   `[1] < [12]`
-   `[1,2,3] < [1,2,5]`
-   `[1,2,3] = [1,2,3]`
-   `[2,2,3] > [1,2,3]`

異なる次元を持つベクトルは、辞書式比較を使用して比較され、次の特性を持ちます。

-   2 つのベクトルは要素ごとに比較され、各要素は数値的に比較されます。
-   最初の不一致要素によって、どのベクトルが辞書式に他より*小さい*か*大きいかが*決まります。
-   あるベクトルが別のベクトルの接頭辞である場合、短いベクトルは辞書順では他のベクトルより*小さく*なります。
-   同じ長さで同一の要素を持つベクトルは辞書的に*等しい*。
-   空のベクトルは、辞書順では空でないベクトルよりも*小さく*なります。
-   2 つの空のベクトルは辞書的に*等しい*です。

例:

-   `[] < [1]`
-   `[1,2,3] < [1,2,3,0]`

ベクトル定数を比較する場合は、文字列値に基づく比較を避けるために、文字列からベクトルへの[明示的なキャスト](#cast)実行を検討してください。

```sql
-- Because string is given, TiDB is comparing strings:
[tidb]> SELECT '[12.0]' < '[4.0]';
+--------------------+
| '[12.0]' < '[4.0]' |
+--------------------+
|                  1 |
+--------------------+
1 row in set (0.01 sec)

-- Cast to vector explicitly to compare by vectors:
[tidb]> SELECT VEC_FROM_TEXT('[12.0]') < VEC_FROM_TEXT('[4.0]');
+--------------------------------------------------+
| VEC_FROM_TEXT('[12.0]') < VEC_FROM_TEXT('[4.0]') |
+--------------------------------------------------+
|                                                0 |
+--------------------------------------------------+
1 row in set (0.01 sec)
```

## 算術 {#arithmetic}

ベクトル データ型は、要素ごとの算術演算`+` (加算) と`-` (減算) をサポートします。ただし、異なる次元のベクトル間で算術演算を実行するとエラーが発生します。

例:

```sql
[tidb]> SELECT VEC_FROM_TEXT('[4]') + VEC_FROM_TEXT('[5]');
+---------------------------------------------+
| VEC_FROM_TEXT('[4]') + VEC_FROM_TEXT('[5]') |
+---------------------------------------------+
| [9]                                         |
+---------------------------------------------+
1 row in set (0.01 sec)

mysql> SELECT VEC_FROM_TEXT('[2,3,4]') - VEC_FROM_TEXT('[1,2,3]');
+-----------------------------------------------------+
| VEC_FROM_TEXT('[2,3,4]') - VEC_FROM_TEXT('[1,2,3]') |
+-----------------------------------------------------+
| [1,1,1]                                             |
+-----------------------------------------------------+
1 row in set (0.01 sec)

[tidb]> SELECT VEC_FROM_TEXT('[4]') + VEC_FROM_TEXT('[1,2,3]');
ERROR 1105 (HY000): vectors have different dimensions: 1 and 3
```

## キャスト {#cast}

### ベクトル ⇨ 文字列間のキャスト {#cast-between-vector-string}

Vector と String 間でキャストするには、次の関数を使用します。

-   `CAST(... AS VECTOR)` : 文字列 ⇒ ベクトル
-   `CAST(... AS CHAR)` : ベクトル ⇒ 文字列
-   `VEC_FROM_TEXT` : 文字列 ⇒ ベクトル
-   `VEC_AS_TEXT` : ベクトル ⇒ 文字列

ベクトル データ型を受け取る関数を呼び出すときに暗黙的なキャストが行われます。

```sql
-- There is an implicit cast here, since VEC_DIMS only accepts VECTOR arguments:
[tidb]> SELECT VEC_DIMS('[0.3, 0.5, -0.1]');
+------------------------------+
| VEC_DIMS('[0.3, 0.5, -0.1]') |
+------------------------------+
|                            3 |
+------------------------------+
1 row in set (0.01 sec)

-- Cast explicitly using VEC_FROM_TEXT:
[tidb]> SELECT VEC_DIMS(VEC_FROM_TEXT('[0.3, 0.5, -0.1]'));
+---------------------------------------------+
| VEC_DIMS(VEC_FROM_TEXT('[0.3, 0.5, -0.1]')) |
+---------------------------------------------+
|                                           3 |
+---------------------------------------------+
1 row in set (0.01 sec)

-- Cast explicitly using CAST(... AS VECTOR):
[tidb]> SELECT VEC_DIMS(CAST('[0.3, 0.5, -0.1]' AS VECTOR));
+----------------------------------------------+
| VEC_DIMS(CAST('[0.3, 0.5, -0.1]' AS VECTOR)) |
+----------------------------------------------+
|                                            3 |
+----------------------------------------------+
1 row in set (0.01 sec)
```

演算子または関数が複数のデータ型を受け入れる場合は、明示的なキャストを使用します。たとえば、比較では、明示的なキャストを使用して、文字列値ではなくベクトル数値を比較します。

```sql
-- Because string is given, TiDB is comparing strings:
[tidb]> SELECT '[12.0]' < '[4.0]';
+--------------------+
| '[12.0]' < '[4.0]' |
+--------------------+
|                  1 |
+--------------------+
1 row in set (0.01 sec)

-- Cast to vector explicitly to compare by vectors:
[tidb]> SELECT VEC_FROM_TEXT('[12.0]') < VEC_FROM_TEXT('[4.0]');
+--------------------------------------------------+
| VEC_FROM_TEXT('[12.0]') < VEC_FROM_TEXT('[4.0]') |
+--------------------------------------------------+
|                                                0 |
+--------------------------------------------------+
1 row in set (0.01 sec)
```

ベクトルを明示的に文字列表現にキャストするには、 `VEC_AS_TEXT()`関数を使用します。

```sql
-- String representation is normalized:
[tidb]> SELECT VEC_AS_TEXT('[0.3,     0.5,  -0.1]');
+--------------------------------------+
| VEC_AS_TEXT('[0.3,     0.5,  -0.1]') |
+--------------------------------------+
| [0.3,0.5,-0.1]                       |
+--------------------------------------+
1 row in set (0.01 sec)
```

追加のキャスト関数については、 [ベクトル関数と演算子](/tidb-cloud/vector-search-functions-and-operators.md)参照してください。

### ベクター と 他のデータ型間のキャスト {#cast-between-vector-other-data-types}

現在、 Vector と他のデータ型 ( `JSON`など) を直接キャストすることはできません。中間型として String を使用する必要があります。

## 制限 {#restrictions}

-   サポートされるベクターの最大次元は 16000 です。
-   ベクトル データ型には`NaN` 、 `Infinity` 、または`-Infinity`値を保存できません。
-   現在、ベクター データ型では倍精度浮動小数点数を格納できません。これは将来のリリースでサポートされる予定です。それまでの間、ベクター データ型に倍精度浮動小数点数をインポートすると、単精度数に変換されます。

その他の制限については[ベクトル検索の制限](/tidb-cloud/vector-search-limitations.md)参照してください。

## MySQL 互換性 {#mysql-compatibility}

ベクトル データ型は TiDB 固有であり、MySQL ではサポートされていません。

## 参照 {#see-also}

-   [ベクトル関数と演算子](/tidb-cloud/vector-search-functions-and-operators.md)
-   [ベクター検索インデックス](/tidb-cloud/vector-search-index.md)
-   [ベクトル検索のパフォーマンスを向上させる](/tidb-cloud/vector-search-improve-performance.md)
