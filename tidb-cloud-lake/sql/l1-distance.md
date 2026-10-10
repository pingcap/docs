---
title: L1_DISTANCE
summary: 2 つのベクトル間のマンハッタン（L1）距離を計算し、対応する要素間の絶対差の総和を測定します。
---

# L1_DISTANCE

2 つのベクトル間のマンハッタン（L1）距離を計算し、対応する要素間の絶対差の総和を測定します。

## 構文 {#syntax}

```sql
L1_DISTANCE(vector1, vector2)
```

## 引数 {#arguments}

- `vector1`: 1 つ目のベクトル（VECTOR データ型）
- `vector2`: 2 つ目のベクトル（VECTOR データ型）

## 戻り値 {#returns}

2 つのベクトル間のマンハッタン（L1）距離を表す FLOAT 値を返します。値は常に 0 以上です。

- 0: 同一のベクトル
- より大きい値: より離れているベクトル

## 説明 {#description}

L1 距離は、マンハッタン距離または taxicab distance とも呼ばれ、2 つのベクトルの対応する要素間の絶対差の総和を計算します。特徴量の比較やスパースデータの分析に役立ちます。

式: `L1_DISTANCE(a, b) = |a1 - b1| + |a2 - b2| + ... + |an - bn|`

## 例 {#examples}

### 基本的な使用方法 {#basic-usage}

```sql
-- Calculate L1 distance between two vectors
SELECT L1_DISTANCE([1.0, 2.0, 3.0]::vector(3), [4.0, 5.0, 6.0]::vector(3)) AS distance;
```

結果:

```
╭──────────╮
│ distance │
├──────────┤
│        9 │
╰──────────╯
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

L1 距離を使用して [1, 2, 3] に最も近いベクトルを見つけます。

```sql
SELECT
    id,
    vec,
    L1_DISTANCE(vec, [1.0000, 2.0000, 3.0000]::VECTOR(3)) AS distance
FROM
    vectors
ORDER BY
    distance ASC;
```

```
╭─────────────────────────────╮
│ id │    vec    │  distance  │
├────┼───────────┼────────────┤
│  1 │ [1,2,3]   │          0 │
│  2 │ [1,2.2,3] │ 0.20000005 │
│  3 │ [4,5,6]   │          9 │
╰─────────────────────────────╯
```