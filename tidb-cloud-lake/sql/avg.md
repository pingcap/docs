---
title: AVG
summary: 集約関数。
---

# AVG

集約関数。

AVG() 関数は、式の平均値を返します。

**Note:** NULL 値はカウントされません。

## 構文 {#syntax}

```sql
AVG(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|--------------------------|
| `<expr>`  | 任意の数値式 |

## 戻り値の型 {#return-type}

double

## 例 {#examples}

**テーブルの作成とサンプルデータの挿入**

`sales` という名前のテーブルを作成し、いくつかのサンプルデータを挿入します。

```sql
CREATE TABLE sales (
  id INTEGER,
  product VARCHAR(50),
  price FLOAT
);

INSERT INTO sales (id, product, price)
VALUES (1, 'Product A', 10.5),
       (2, 'Product B', 20.75),
       (3, 'Product C', 30.0),
       (4, 'Product D', 15.25),
       (5, 'Product E', 25.5);
```

**クエリ: AVG() 関数の使用**

次に、AVG() 関数を使用して、`sales` テーブル内のすべての商品の平均価格を求めます。

```sql
SELECT AVG(price) AS avg_price
FROM sales;
```

結果は次のようになります。

```sql
| avg_price |
| --------- |
| 20.4      |
```