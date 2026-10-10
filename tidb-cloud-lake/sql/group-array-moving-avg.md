---
title: GROUP_ARRAY_MOVING_AVG
summary: GROUP_ARRAY_MOVING_AVG 関数は、入力値の移動平均を計算します。この関数は、ウィンドウサイズをパラメータとして受け取ることができます。指定しない場合、ウィンドウサイズは入力値の数と同じになります。
---

# GROUP_ARRAY_MOVING_AVG

GROUP_ARRAY_MOVING_AVG 関数は、入力値の移動平均を計算します。この関数は、ウィンドウサイズをパラメータとして受け取ることができます。指定しない場合、ウィンドウサイズは入力値の数と同じになります。

## 構文 {#syntax}

```sql
GROUP_ARRAY_MOVING_AVG(<expr>)

GROUP_ARRAY_MOVING_AVG(<window_size>)(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|------------------| ------------------------ |
| `<window_size>`  | 任意の数値式 |
| `<expr>`         | 任意の数値式 |

## 戻り値の型 {#return-type}

ソースデータ型に応じて、double または decimal の要素を持つ [配列](/tidb-cloud-lake/sql/array.md) を返します。

## 例 {#examples}

```sql
-- Create a table and insert sample data
CREATE TABLE hits (
  user_id INT,
  request_num INT
);

INSERT INTO hits (user_id, request_num)
VALUES (1, 10),
       (2, 15),
       (3, 20),
       (1, 13),
       (2, 21),
       (3, 25),
       (1, 30),
       (2, 41),
       (3, 45);

SELECT user_id, GROUP_ARRAY_MOVING_AVG(2)(request_num) AS avg_request_num
FROM hits
GROUP BY user_id;

| user_id | avg_request_num  |
|---------|------------------|
|       1 | [5.0,11.5,21.5]  |
|       3 | [10.0,22.5,35.0] |
|       2 | [7.5,18.0,31.0]  |
```