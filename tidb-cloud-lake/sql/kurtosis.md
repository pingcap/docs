---
title: KURTOSIS
summary: 集約関数。
---

# KURTOSIS

集約関数。

`KURTOSIS()` 関数は、すべての入力値の過剰尖度を返します。

## 構文 {#syntax}

```sql
KURTOSIS(<expr>)
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
CREATE TABLE stock_prices (
  id INT,
  stock_symbol VARCHAR,
  price FLOAT
);

INSERT INTO stock_prices (id, stock_symbol, price)
VALUES (1, 'AAPL', 150),
       (2, 'AAPL', 152),
       (3, 'AAPL', 148),
       (4, 'AAPL', 160),
       (5, 'AAPL', 155);
```

**クエリのデモ: Apple 株価の過剰尖度を計算する**

```sql
SELECT KURTOSIS(price) AS excess_kurtosis
FROM stock_prices
WHERE stock_symbol = 'AAPL';
```

**結果**

```sql
|     excess_kurtosis     |
|-------------------------|
| 0.06818181325581445     |
```