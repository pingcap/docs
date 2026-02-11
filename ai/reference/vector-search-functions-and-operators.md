---
title: Vector Functions and Operators
summary: Vector データ型で使用できる関数と演算子について学習します。
aliases: ['/tidb/stable/vector-search-functions-and-operators/','/tidb/dev/vector-search-functions-and-operators/','/tidbcloud/vector-search-functions-and-operators/']
---

# ベクトル関数と演算子 {#vector-functions-and-operators}

このドキュメントでは、ベクター データ型で使用できる関数と演算子の一覧を示します。

> **注記：**
>
> -   ベクトル関数と演算子はベータ版であり、予告なく変更される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。
> -   ベクトルデータ型とこれらのベクトル関数は、 [TiDBセルフマネージド](/overview.md) 、 [TiDB Cloudスターター](/tidb-cloud/select-cluster-tier.md#starter) 、 [TiDB Cloudエッセンシャル](/tidb-cloud/select-cluster-tier.md#essential) 、および[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)で使用できます。TiDB Self-ManagedおよびTiDB Cloud Dedicatedの場合、TiDBバージョンはv8.4.0以降である必要があります（v8.5.0以降を推奨）。

## ベクトル関数 {#vector-functions}

以下の関数は[ベクトルデータ型](/ai/reference/vector-search-data-types.md)専用に設計されています。

**ベクトル距離関数:**

| 関数名                                                         | 説明                            | [ベクトルインデックス](/ai/reference/vector-search-index.md)がサポート |
| ----------------------------------------------------------- | ----------------------------- | ------------------------------------------------------- |
| [`VEC_L2_DISTANCE`](#vec_l2_distance)                       | 2つのベクトル間のL2距離（ユークリッド距離）を計算します | はい                                                      |
| [`VEC_COSINE_DISTANCE`](#vec_cosine_distance)               | 2つのベクトル間のコサイン距離を計算します         | はい                                                      |
| [`VEC_NEGATIVE_INNER_PRODUCT`](#vec_negative_inner_product) | 2つのベクトルの内積の負数を計算します           | いいえ                                                     |
| [`VEC_L1_DISTANCE`](#vec_l1_distance)                       | 2つのベクトル間のL1距離（マンハッタン距離）を計算します | いいえ                                                     |

**その他のベクトル関数:**

| 関数名                               | 説明                          |
| --------------------------------- | --------------------------- |
| [`VEC_DIMS`](#vec_dims)           | ベクトルの次元を返す                  |
| [`VEC_L2_NORM`](#vec_l2_norm)     | ベクトルのL2ノルム（ユークリッドノルム）を計算します |
| [`VEC_FROM_TEXT`](#vec_from_text) | 文字列をベクトルに変換する               |
| [`VEC_AS_TEXT`](#vec_as_text)     | ベクトルを文字列に変換する               |

## 拡張された組み込み関数と演算子 {#extended-built-in-functions-and-operators}

次の組み込み関数と演算子は、 [ベクトルデータ型](/ai/reference/vector-search-data-types.md)演算をサポートするために拡張されています。

**算術演算子:**

| 名前                                                                                      | 説明             |
| :-------------------------------------------------------------------------------------- | :------------- |
| [`+`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_plus)  | ベクトル要素ごとの加算演算子 |
| [`-`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_minus) | ベクトル要素ごとの減算演算子 |

ベクトル演算の仕組みの詳細については、 [ベクトルデータ型 | 算術](/ai/reference/vector-search-data-types.md#arithmetic)参照してください。

**集計（GROUP BY）関数：**

| 名前                                                                                                            | 説明         |
| :------------------------------------------------------------------------------------------------------------ | :--------- |
| [`COUNT()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_count)                  | 返された行の数を返す |
| [`COUNT(DISTINCT)`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_count-distinct) | 異なる値の数を返す  |
| [`MAX()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_max)                      | 最大値を返す     |
| [`MIN()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_min)                      | 最小値を返す     |

**比較関数と演算子:**

| 名前                                                                                                                  | 説明                   |
| ------------------------------------------------------------------------------------------------------------------- | -------------------- |
| [`BETWEEN ... AND ...`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_between)         | 値が範囲内にあるかどうかを確認します   |
| [`COALESCE()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_coalesce)                 | 最初のNULL以外の引数を返す      |
| [`=`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal)                             | 等号演算子                |
| [`&#x3C;=>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal-to)                   | NULL安全等号演算子          |
| [`>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than)                      | より大きい演算子             |
| [`>=`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than-or-equal)            | より大きいか等しい演算子         |
| [`GREATEST()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_greatest)                 | 最大の引数を返す             |
| [`IN()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_in)                             | 値が値セット内であるかどうかを確認する  |
| [`IS NULL`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-null)                     | 値が`NULL`かどうかをテストする   |
| [`ISNULL()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_isnull)                     | 引数が`NULL`かどうかをテストする  |
| [`LEAST()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_least)                       | 最小の引数を返す             |
| [`&#x3C;`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than)                    | 小なり演算子               |
| [`&#x3C;=`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than-or-equal)          | 以下演算子                |
| [`NOT BETWEEN ... AND ...`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-between) | 値が範囲内にないか確認する        |
| [`!=` 、 `&lt;&gt;`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-equal)           | 等しくない演算子             |
| [`NOT IN()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-in)                     | 値が値のセット内にないかどうかを確認する |

ベクトルの比較方法の詳細については、 [ベクトルデータ型 | 比較](/ai/reference/vector-search-data-types.md#comparison)参照してください。

**制御フロー関数:**

| 名前                                                                                                | 説明                        |
| :------------------------------------------------------------------------------------------------ | :------------------------ |
| [`CASE`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#operator_case)       | ケース演算子                    |
| [`IF()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_if)         | if/else構文                 |
| [`IFNULL()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_ifnull) | null if/else 構文           |
| [`NULLIF()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_nullif) | expr1 = expr2の場合は`NULL`返す |

**キャスト関数:**

| 名前                                                                                          | 説明                    |
| :------------------------------------------------------------------------------------------ | :-------------------- |
| [`CAST()`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#function_cast)       | 値を文字列またはベクトルとしてキャストする |
| [`CONVERT()`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#function_convert) | 値を文字列としてキャストする        |

`CAST()`使用方法の詳細については、 [ベクトルデータ型 | キャスト](/ai/reference/vector-search-data-types.md#cast)参照してください。

## 完全な参考文献 {#full-references}

### VEC_L2_距離 {#vec-l2-distance}

```sql
VEC_L2_DISTANCE(vector1, vector2)
```

次の式を使用して、2 つのベクトル間の[L2距離](https://en.wikipedia.org/wiki/Euclidean_distance) (ユークリッド距離) を計算します。

$距離(p,q)=\sqrt {\sum \limits *{i=1}^{n}{(p* {i}-q_{i})^{2}}}$

2つのベクトルの次元数は同じである必要があります。そうでない場合はエラーが返されます。

例：

```sql
SELECT VEC_L2_DISTANCE('[0, 3]', '[4, 0]');
```

    +-------------------------------------+
    | VEC_L2_DISTANCE('[0, 3]', '[4, 0]') |
    +-------------------------------------+
    |                                   5 |
    +-------------------------------------+

### VEC_COSINE_DISTANCE {#vec-cosine-distance}

```sql
VEC_COSINE_DISTANCE(vector1, vector2)
```

次の式を使用して 2 つのベクトル間の[コサイン距離](https://en.wikipedia.org/wiki/Cosine_similarity)計算します。

$距離(p,q)=1.0 - {\frac {\sum \limits *{i=1}^{n}{p* {i}q_{i}}}{{\sqrt {\sum \limits *{i=1}^{n}{p* {i}^{2}}}}\cdot {\sqrt {\sum \limits *{i=1}^{n}{q* {i}^{2}}}}}}$

2つのベクトルの次元数は同じである必要があります。そうでない場合はエラーが返されます。

OpenAI からの埋め込みの場合、この関数を使用するのは[推奨](https://help.openai.com/en/articles/6824809-embeddings-faq)です。

例：

```sql
SELECT VEC_COSINE_DISTANCE('[1, 1]', '[-1, -1]');
```

    +-------------------------------------------+
    | VEC_COSINE_DISTANCE('[1, 1]', '[-1, -1]') |
    +-------------------------------------------+
    |                                         2 |
    +-------------------------------------------+

### VEC_負の内部積 {#vec-negative-inner-product}

```sql
VEC_NEGATIVE_INNER_PRODUCT(vector1, vector2)
```

次の数式を使用して、2 つのベクトル間の[内積](https://en.wikipedia.org/wiki/Dot_product)の負の値を使用して距離を計算します。

$DISTANCE(p,q)=- INNER_PROD(p,q)=-\sum \limits *{i=1}^{n}{p* {i}q_{i}}$

2つのベクトルの次元数は同じである必要があります。そうでない場合はエラーが返されます。

例：

```sql
SELECT VEC_NEGATIVE_INNER_PRODUCT('[1, 2]', '[3, 4]');
```

    +------------------------------------------------+
    | VEC_NEGATIVE_INNER_PRODUCT('[1, 2]', '[3, 4]') |
    +------------------------------------------------+
    |                                            -11 |
    +------------------------------------------------+

### VEC_L1_距離 {#vec-l1-distance}

```sql
VEC_L1_DISTANCE(vector1, vector2)
```

次の式を使用して、2 つのベクトル間の[L1距離](https://en.wikipedia.org/wiki/Taxicab_geometry) (マンハッタン距離) を計算します。

$距離(p,q)=\sum \limits *{i=1}^{n}{|p* {i}-q_{i}|}$

2つのベクトルの次元数は同じである必要があります。そうでない場合はエラーが返されます。

例：

```sql
SELECT VEC_L1_DISTANCE('[0, 0]', '[3, 4]');
```

    +-------------------------------------+
    | VEC_L1_DISTANCE('[0, 0]', '[3, 4]') |
    +-------------------------------------+
    |                                   7 |
    +-------------------------------------+

### VEC_DIMS {#vec-dims}

```sql
VEC_DIMS(vector)
```

ベクトルの次元を返します。

例:

```sql
SELECT VEC_DIMS('[1, 2, 3]');
```

    +-----------------------+
    | VEC_DIMS('[1, 2, 3]') |
    +-----------------------+
    |                     3 |
    +-----------------------+

```sql
SELECT VEC_DIMS('[]');
```

    +----------------+
    | VEC_DIMS('[]') |
    +----------------+
    |              0 |
    +----------------+

### VEC_L2_NORM {#vec-l2-norm}

```sql
VEC_L2_NORM(vector)
```

次の式を使用してベクトルの[L2ノルム](https://en.wikipedia.org/wiki/Norm_(mathematics)) (ユークリッド ノルム) を計算します。

$NORM(p)=\sqrt {\sum \limits *{i=1}^{n}{p* {i}^{2}}}$

例：

```sql
SELECT VEC_L2_NORM('[3, 4]');
```

    +-----------------------+
    | VEC_L2_NORM('[3, 4]') |
    +-----------------------+
    |                     5 |
    +-----------------------+

### VEC_FROM_TEXT {#vec-from-text}

```sql
VEC_FROM_TEXT(string)
```

文字列をベクトルに変換します。多くの場合、この変換は暗黙的に行われます。例えば、 `VECTOR`データ型の列にデータを挿入する場合などです。ただし、暗黙的な変換がサポートされていない式（ベクトルに対する算術演算など）では、この関数を明示的に呼び出す必要があります。

例：

```sql
SELECT VEC_FROM_TEXT('[1, 2]') + VEC_FROM_TEXT('[3, 4]');
```

    +-------------------------------------------------+
    | VEC_FROM_TEXT('[1,2]') + VEC_FROM_TEXT('[3,4]') |
    +-------------------------------------------------+
    | [4,6]                                           |
    +-------------------------------------------------+

### VEC_AS_TEXT {#vec-as-text}

```sql
VEC_AS_TEXT(vector)
```

ベクトルを文字列に変換します。

例：

```sql
SELECT VEC_AS_TEXT('[1.000, 2.5]');
```

    +-----------------------------+
    | VEC_AS_TEXT('[1.000, 2.5]') |
    +-----------------------------+
    | [1,2.5]                     |
    +-----------------------------+

## MySQLの互換性 {#mysql-compatibility}

ベクトル関数と、ベクトル データ型に対する組み込み関数および演算子の拡張使用は TiDB 固有のものであり、MySQL ではサポートされていません。

## 参照 {#see-also}

-   [ベクトルデータ型](/ai/reference/vector-search-data-types.md)
