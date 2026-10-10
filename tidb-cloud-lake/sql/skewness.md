---
title: SKEWNESS
summary: 集約関数。
---

# SKEWNESS

集約関数。

`SKEWNESS()` 関数は、すべての入力値の歪度を返します。

## 構文 {#syntax}

```sql
SKEWNESS(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------| -----------|
| `<expr>`  | 任意の数値式 |

## 戻り値の型 {#return-type}

NULL 可能な Float64。

## 例 {#example}

**テーブルを作成してサンプルデータを挿入する**

```sql
CREATE TABLE temperature_data (
                                  id INT,
                                  city_id INT,
                                  temperature FLOAT
);

INSERT INTO temperature_data (id, city_id, temperature)
VALUES (1, 1, 60),
       (2, 1, 65),
       (3, 1, 62),
       (4, 2, 70),
       (5, 2, 75);
```

**クエリ例: 温度データの歪度を計算する**

```sql
SELECT SKEWNESS(temperature) AS temperature_skewness
FROM temperature_data;
```

**結果**

```sql
| temperature_skewness |
|----------------------|
|      0.68            |
```