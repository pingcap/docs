---
title: ARG_MAX
summary: 最大の val 値に対応する arg 値を計算します。val の最大値に対して arg の値が複数ある場合は、最初に見つかった値を返します。
---

# ARG_MAX

最大の `val` 値に対応する `arg` 値を計算します。`val` の最大値に対して `arg` の値が複数ある場合は、最初に見つかった値を返します。

## 構文 {#syntax}

```sql
ARG_MAX(<arg>, <val>)
```

## 引数 {#arguments}

| 引数 | 説明                                                                                       |
|-----------|---------------------------------------------------------------------------------------------------|
| `<arg>`   | [{{{ .lake }}} がサポートする任意のデータ型](/tidb-cloud-lake/sql/data-types.md) の引数 |
| `<val>`   | [{{{ .lake }}} がサポートする任意のデータ型](/tidb-cloud-lake/sql/data-types.md) の値    |

## 戻り値の型 {#return-type}

最大の `val` 値に対応する `arg` 値を返します。

戻り値の型は `arg` の型と一致します。

## 例 {#example}

**テーブルの作成とサンプルデータの挿入**

`sales` という名前のテーブルを作成し、サンプルデータをいくつか挿入します。

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

**クエリ: ARG_MAX() 関数の使用**

次に、ARG_MAX() 関数を使用して、最大価格の製品を見つけます。

```sql
SELECT ARG_MAX(product, price) AS max_price_product
FROM sales;
```

結果は次のようになります。

```sql
| max_price_product |
| ----------------- |
| Product C         |
```