---
title: Vector Data Types
summary: TiDB の Vector データ型について学習します。
---

# ベクトルデータ型 {#vector-data-types}

ベクトルは、 `[0.3, 0.5, -0.1, ...]`などの浮動小数点数のシーケンスです。TiDB は、AI アプリケーションで広く使用されているベクトル埋め込みを効率的に保存およびクエリするために特別に最適化されたベクトル データ型を提供します。

<CustomContent platform="tidb">

> **警告：**
>
> この機能は実験的です。本番環境での使用は推奨されません。この機能は予告なく変更される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この機能はベータ版です。予告なく変更される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

</CustomContent>

> **注記：**
>
> ベクトルデータ型は、TiDB Self-Managed、 [TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) [TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)使用できます[TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) Self-Managed およびTiDB Cloud Dedicated の場合、TiDB バージョンは v8.4.0 以降である必要があります (v8.5.0 以降を推奨)。

現在、次のベクター データ型が利用可能です。

-   `VECTOR` : 任意の次元の単精度浮動小数点数のシーケンス。
-   `VECTOR(D)` : 固定次元`D`を持つ単精度浮動小数点数のシーケンス。

ベクトル データ型を使用すると、 [`JSON`](/data-type-json.md)型を使用する場合に比べて次の利点があります。

-   ベクトル インデックスのサポート: ベクトルの検索を高速化するために[ベクター検索インデックス](/vector-search/vector-search-index.md)構築できます。
-   次元の強制: 異なる次元のベクトルの挿入を禁止する次元を指定できます。
-   最適化されたstorage形式: ベクター データ型はベクター データの処理に最適化されており、 `JSON`型に比べて優れたスペース効率とパフォーマンスを提供します。

## 構文 {#syntax}

次の構文の文字列を使用して Vector 値を表すことができます。

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

次の例では、テーブルの作成時に`embedding`列に次元`3`が強制されるため、異なる次元のベクトルを挿入するとエラーが発生します。

```sql
[tidb]> INSERT INTO vector_table VALUES (4, '[0.3, 0.5]');
ERROR 1105 (HY000): vector has 2 dimensions, does not fit VECTOR(3)
```

ベクトル データ型で使用できる関数と演算子については、 [ベクトル関数と演算子](/vector-search/vector-search-functions-and-operators.md)参照してください。

ベクター検索インデックスの構築と使用の詳細については、 [ベクター検索インデックス](/vector-search/vector-search-index.md)参照してください。

## 異なる次元のベクトルを保存する {#store-vectors-with-different-dimensions}

`VECTOR`型の次元パラメータを省略することで、同じ列に異なる次元のベクトルを保存できます。

```sql
CREATE TABLE vector_table (
    id INT PRIMARY KEY,
    embedding VECTOR
);

INSERT INTO vector_table VALUES (1, '[0.3, 0.5, -0.1]'); -- 3 dimensions vector, OK
INSERT INTO vector_table VALUES (2, '[0.3, 0.5]');       -- 2 dimensions vector, OK
```

ただし、ベクトル距離は同じ次元のベクトル間でのみ計算できるため、この列に[ベクター検索インデックス](/vector-search/vector-search-index.md)構築できないことに注意してください。

## 比較 {#comparison}

[比較演算子](/functions-and-operators/operators.md)を使用して、 `=` 、 `!=` 、 `<` 、 `>` 、 `<=` 、 `>=`などのベクトルデータ型を比較できます。ベクトルデータ型の比較演算子と関数の完全なリストについては、 [ベクトル関数と演算子](/vector-search/vector-search-functions-and-operators.md)参照してください。

ベクトルデータ型は要素ごとに数値的に比較されます。例:

-   `[1] < [12]`
-   `[1,2,3] < [1,2,5]`
-   `[1,2,3] = [1,2,3]`
-   `[2,2,3] > [1,2,3]`

異なる次元を持つ 2 つのベクトルは、次の規則に従って辞書式比較を使用して比較されます。

-   2 つのベクトルは最初から要素ごとに比較され、各要素は数値的に比較されます。
-   最初の不一致要素によって、どのベクトルが辞書式に他より*小さい*か*大きいかが*決まります。
-   あるベクトルが別のベクトルの接頭辞である場合、短いベクトルは辞書順でもう一方より*小さくなります*。例えば、 `[1,2,3] < [1,2,3,0]` 。
-   同じ長さで同一の要素を持つベクトルは辞書的に*等しい*です。
-   空ベクトルは、辞書順で空でないベクトルよりも*小さい*。例えば、 `[] < [1]` 。
-   2 つの空のベクトルは辞書的に*等しい*です。

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

ベクトルデータ型は、算術演算`+` （加算）と`-` （減算）をサポートします。ただし、異なる次元のベクトル間の算術演算はサポートされておらず、エラーが発生します。

例:

```sql
[tidb]> SELECT VEC_FROM_TEXT('[4]') + VEC_FROM_TEXT('[5]');
+---------------------------------------------+
| VEC_FROM_TEXT('[4]') + VEC_FROM_TEXT('[5]') |
+---------------------------------------------+
| [9]                                         |
+---------------------------------------------+
1 row in set (0.01 sec)

[tidb]> SELECT VEC_FROM_TEXT('[2,3,4]') - VEC_FROM_TEXT('[1,2,3]');
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

### ベクター⇔文字列間のキャスト {#cast-between-vector-string}

Vector と String 間のキャストを行うには、次の関数を使用します。

-   `CAST(... AS VECTOR)` : 文字列 ⇒ ベクトル
-   `CAST(... AS CHAR)` : ベクトル ⇒ 文字列
-   `VEC_FROM_TEXT` : 文字列 ⇒ ベクトル
-   `VEC_AS_TEXT` : ベクトル ⇒ 文字列

ユーザビリティを向上させるため、ベクトル相関距離関数など、ベクトルデータ型のみをサポートする関数を呼び出す場合は、形式に準拠した文字列を渡すだけで済みます。この場合、TiDB は自動的に暗黙的なキャストを実行します。

```sql
-- The VEC_DIMS function only accepts VECTOR arguments, so you can directly pass in a string for an implicit cast.
[tidb]> SELECT VEC_DIMS('[0.3, 0.5, -0.1]');
+------------------------------+
| VEC_DIMS('[0.3, 0.5, -0.1]') |
+------------------------------+
|                            3 |
+------------------------------+
1 row in set (0.01 sec)

-- You can also explicitly cast a string to a vector using VEC_FROM_TEXT and then pass the vector to the VEC_DIMS function.
[tidb]> SELECT VEC_DIMS(VEC_FROM_TEXT('[0.3, 0.5, -0.1]'));
+---------------------------------------------+
| VEC_DIMS(VEC_FROM_TEXT('[0.3, 0.5, -0.1]')) |
+---------------------------------------------+
|                                           3 |
+---------------------------------------------+
1 row in set (0.01 sec)

-- You can also cast explicitly using CAST(... AS VECTOR):
[tidb]> SELECT VEC_DIMS(CAST('[0.3, 0.5, -0.1]' AS VECTOR));
+----------------------------------------------+
| VEC_DIMS(CAST('[0.3, 0.5, -0.1]' AS VECTOR)) |
+----------------------------------------------+
|                                            3 |
+----------------------------------------------+
1 row in set (0.01 sec)
```

複数のデータ型を受け入れる演算子または関数を使用する場合、文字列をその演算子または関数に渡す前に、文字列型を明示的にベクター型にキャストする必要があります。これは、TiDB がこのような場合、暗黙的なキャストを行わないためです。例えば、比較演算を実行する前に、文字列を明示的にベクター型にキャストする必要があります。そうしないと、TiDB は文字列をベクター数値ではなく文字列値として比較します。

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

ベクトルを明示的に文字列表現にキャストすることもできます。1 `VEC_AS_TEXT()`を例に挙げましょう。

```sql
-- The string is first implicitly cast to a vector, and then the vector is explicitly cast to a string, thus returning a string in the normalized format:
[tidb]> SELECT VEC_AS_TEXT('[0.3,     0.5,  -0.1]');
+--------------------------------------+
| VEC_AS_TEXT('[0.3,     0.5,  -0.1]') |
+--------------------------------------+
| [0.3,0.5,-0.1]                       |
+--------------------------------------+
1 row in set (0.01 sec)
```

追加のキャスト関数については、 [ベクトル関数と演算子](/vector-search/vector-search-functions-and-operators.md)参照してください。

### ベクター⇔他のデータ型間のキャスト {#cast-between-vector-other-data-types}

現在、 Vector と他のデータ型（ `JSON`など）間の直接キャストはサポートされていません。この制限を回避するには、SQL文でキャストする際の中間データ型として String を使用してください。

テーブルに格納されているベクトル データ型の列は、 `ALTER TABLE ... MODIFY COLUMN ...`使用して他のデータ型に変換できないことに注意してください。

## 制限 {#restrictions}

ベクトル データ型の制限については、 [ベクトル検索の制限](/vector-search/vector-search-limitations.md)および[ベクトルインデックスの制限](/vector-search/vector-search-index.md#restrictions)参照してください。

## MySQLの互換性 {#mysql-compatibility}

ベクトル データ型は TiDB 固有であり、MySQL ではサポートされていません。

## 参照 {#see-also}

-   [ベクトル関数と演算子](/vector-search/vector-search-functions-and-operators.md)
-   [ベクター検索インデックス](/vector-search/vector-search-index.md)
-   [ベクトル検索のパフォーマンスを向上させる](/vector-search/vector-search-improve-performance.md)
