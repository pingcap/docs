---
title: COSINE_DISTANCE
summary: {{{ .lake }}} における cosine_distance 関数を使用した類似度の測定。
---

# COSINE_DISTANCE

2 つのベクトル間のコサイン距離を計算し、それらがどの程度異なるかを測定します。

## 構文 {#syntax}

```sql
COSINE_DISTANCE(vector1, vector2)
```

## 引数 {#arguments}

- `vector1`: 1 つ目のベクトル（VECTOR Data Type）
- `vector2`: 2 つ目のベクトル（VECTOR Data Type）

## 戻り値 {#returns}

0 から 1 の間の FLOAT 値を返します。

- 0: 同一のベクトル（完全に類似）
- 1: 直交するベクトル（完全に非類似）

## 説明 {#description}

コサイン距離は、ベクトルの大きさに関係なく、2 つのベクトル間の角度に基づいてそれらの非類似度を測定します。この関数は次の処理を行います。

1. 2 つの入力ベクトルの長さが同じであることを検証する
2. 2 つのベクトルの要素ごとの積の合計（内積）を計算する
3. 各ベクトルについて、各要素の二乗和の平方根（ベクトルの大きさ）を計算する
4. `1 - (dot_product / (magnitude1 * magnitude2))` を返す

実装されている数式は次のとおりです。

```
cosine_distance(v1, v2) = 1 - (Σ(v1ᵢ * v2ᵢ) / (√Σ(v1ᵢ²) * √Σ(v2ᵢ²)))
```

ここで、v1ᵢ と v2ᵢ は入力ベクトルの要素です。

> **Note:**
>
> この関数は {{{ .lake }}} 内でベクトル計算を実行し、外部 API には依存しません。

## 例 {#examples}

### 基本的な使用方法 {#basic-usage}

```sql
-- Calculate cosine distance between two vectors
SELECT COSINE_DISTANCE([1.0, 2.0, 3.0]::vector(3), [4.0, 5.0, 6.0]::vector(3)) AS distance;
```

結果:

```
╭─────────────╮
│   distance  │
├─────────────┤
│ 0.025368214 │
╰─────────────╯
```

ベクトルデータを含むテーブルを作成します。

```sql
CREATE OR REPLACE TABLE vectors (
    id INT,
    vec VECTOR(3)
);

INSERT INTO vectors VALUES
    (1, [1.0000, 2.0000, 3.0000]),
    (2, [1.0000, 2.2000, 3.0000]),
    (3, [4.0000, 5.0000, 6.0000]);
```

[1, 2, 3] に最も類似するベクトルを検索します。

```sql
SELECT
    id,
    vec,
    COSINE_DISTANCE(vec, [1.0000, 2.0000, 3.0000]::VECTOR(3)) AS distance
FROM
    vectors
ORDER BY
    distance ASC;
```

```
╭────────────────────────────────────╮
│ id │    vec    │      distance     │
├────┼───────────┼───────────────────┤
│  1 │ [1,2,3]   │ 0.000000059604645 │
│  2 │ [1,2.2,3] │     0.00096315145 │
│  3 │ [4,5,6]   │       0.025368214 │
╰────────────────────────────────────╯
```