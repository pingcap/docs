---
title: INNER_PRODUCT
summary: 2 つのベクトルの内積（ドット積）を計算します。これは、ベクトル間の類似性と射影を測定します。
---

# INNER_PRODUCT

2 つのベクトルの内積（ドット積）を計算します。これは、ベクトル間の類似性と射影を測定します。

## 構文 {#syntax}

```sql
INNER_PRODUCT(vector1, vector2)
```

## 引数 {#arguments}

- `vector1`: 1 つ目のベクトル（VECTOR Data Type）
- `vector2`: 2 つ目のベクトル（VECTOR Data Type）

## 戻り値 {#returns}

2 つのベクトルの内積を表す FLOAT 値を返します。

## 説明 {#description}

内積（ドット積とも呼ばれます）は、2 つのベクトルにおける対応する要素同士の積の総和を計算します。この関数は次の処理を行います。

1. 2 つの入力ベクトルの長さが同じであることを検証する
2. 各ベクトルの対応する要素同士を乗算する
3. すべての積を合計して、単一のスカラー値を生成する

実装されている数式は次のとおりです。

```
inner_product(v1, v2) = Σ(v1ᵢ * v2ᵢ)
```

ここで、v1ᵢ と v2ᵢ は入力ベクトルの要素です。

内積は、次のような場面で基本となる概念です。

- ベクトルの類似性の測定（値が大きいほど方向がより類似していることを示します）
- あるベクトルを別のベクトルへ射影する計算
- 機械学習アルゴリズム（ニューラルネットワーク、SVM など）
- 仕事やエネルギーに関する物理計算

> **Note:**
>
> この関数は {{{ .lake }}} 内でベクトル計算を実行し、外部 API には依存しません。

## 例 {#examples}

### 基本的な使用方法 {#basic-usage}

```sql
SELECT INNER_PRODUCT([1,2,3]::VECTOR(3), [4,5,6]::VECTOR(3)) AS inner_product;
```

結果:

```
┌───────────────┐
│ inner_product │
├───────────────┤
│          32.0 │
└───────────────┘
```

### テーブルデータを使用する {#working-with-table-data}

ベクトルデータを含むテーブルを作成します。

```sql
CREATE TABLE vector_examples (
    id INT,
    vector_a VECTOR(3),
    vector_b VECTOR(3)
);

INSERT INTO vector_examples VALUES
    (1, [1.0, 2.0, 3.0], [4.0, 5.0, 6.0]),
    (2, [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]),
    (3, [2.0, 3.0, 1.0], [1.0, 2.0, 3.0]);
```

内積を計算します。

```sql
SELECT
    id,
    vector_a,
    vector_b,
    INNER_PRODUCT(vector_a, vector_b) AS inner_product
FROM vector_examples;
```

結果:

```
┌────┬───────────────┬───────────────┬───────────────┐
│ id │   vector_a    │   vector_b    │ inner_product │
├────┼───────────────┼───────────────┼───────────────┤
│  1 │ [1.0,2.0,3.0] │ [4.0,5.0,6.0] │          32.0 │
│  2 │ [1.0,0.0,0.0] │ [0.0,1.0,0.0] │           0.0 │
│  3 │ [2.0,3.0,1.0] │ [1.0,2.0,3.0] │          11.0 │
└────┴───────────────┴───────────────┴───────────────┘
```

### ベクトル類似性の分析 {#vector-similarity-analysis}

```sql
-- Calculate inner products to measure vector similarity
SELECT
    INNER_PRODUCT([1,0,0]::VECTOR(3), [1,0,0]::VECTOR(3)) AS same_direction,
    INNER_PRODUCT([1,0,0]::VECTOR(3), [0,1,0]::VECTOR(3)) AS orthogonal,
    INNER_PRODUCT([1,0,0]::VECTOR(3), [-1,0,0]::VECTOR(3)) AS opposite;
```

結果:

```
┌────────────────┬─────────────┬──────────┐
│ same_direction │ orthogonal  │ opposite │
├────────────────┼─────────────┼──────────┤
│           1.0  │         0.0 │     -1.0 │
└────────────────┴─────────────┴──────────┘
```