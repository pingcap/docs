---
title: RETENTION
summary: 集約関数。
---

# RETENTION

集約関数

`RETENTION()` 関数は、イベントに対して特定の条件が満たされたかどうかを示す `UInt8` 型の条件を、1 個から 32 個まで引数として受け取ります。

任意の条件を引数として指定できます（`WHERE` と同様）。

最初の条件を除き、各条件はペアとして適用されます。2 番目の結果は 1 番目と 2 番目の条件がともに真の場合に真となり、3 番目の結果は 1 番目と 3 番目の条件がともに真の場合に真となります。以下同様です。

## 構文 {#syntax}

```sql
RETENTION( <cond1> , <cond2> , ..., <cond32> );
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|---------------------------------------------|
| `<cond>`  | Boolean の結果を返す式 |

## 戻り値の型 {#return-type}

`1` または `0` の配列です。

## 例 {#example}

**テーブルを作成してサンプルデータを挿入します**

```sql
CREATE TABLE user_events (
  id INT,
  user_id INT,
  event_date DATE,
  event_type VARCHAR
);

INSERT INTO user_events (id, user_id, event_date, event_type)
VALUES (1, 1, '2022-01-01', 'signup'),
       (2, 1, '2022-01-02', 'login'),
       (3, 2, '2022-01-01', 'signup'),
       (4, 2, '2022-01-03', 'purchase'),
       (5, 3, '2022-01-01', 'signup'),
       (6, 3, '2022-01-02', 'login');
```

**クエリデモ: サインアップ、ログイン、購入イベントに基づくユーザー維持率の計算**

```sql
SELECT
  user_id,
  RETENTION(event_type = 'signup', event_type = 'login', event_type = 'purchase') AS retention
FROM user_events
GROUP BY user_id;
```

**結果**

```sql
| user_id | retention |
|---------|-----------|
|   1     | [1, 1, 0] |
|   2     | [1, 0, 1] |
|   3     | [1, 1, 0] |
```
