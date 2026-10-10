---
title: WITH CONSUME
summary: SELECT クエリ内でストリームからデータを消費します。
---

# WITH CONSUME

SELECT クエリ内でストリームからデータを消費します。

関連情報: [WITH Stream Hints](/tidb-cloud-lake/sql/stream-hints.md)

## 構文 {#syntax}

```sql
SELECT ...
FROM <stream_name> WITH CONSUME [ AS <alias> ]
[ WHERE <conditions> ]
```

> **Note:**
>
> クエリが正常に実行される限り、WITH CONSUME 句は、WHERE 条件を使用してその一部だけをクエリした場合でも、ストリームによってキャプチャされたすべてのデータを消費します。

## 例 {#examples}

`s` という名前のストリームがあり、次のデータをキャプチャしているとします。

```sql
SELECT * FROM s;

┌────────────────────────────────────────────────────────────────────────────────────────────────┐
│        a        │   change$action  │              change$row_id             │ change$is_update │
├─────────────────┼──────────────────┼────────────────────────────────────────┼──────────────────┤
│               3 │ INSERT           │ 4942372d864147e98188f3b486ec18d2000000 │ false            │
│               1 │ DELETE           │ 3df95ad8552e4967a704e1c7209d3dff000000 │ false            │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
```

ここで `WITH CONSUME` を使用してストリームをクエリすると、次の結果が返されます。

```sql
SELECT
  a
FROM
  s WITH CONSUME AS ss
WHERE
  ss.change$action = 'INSERT';

┌─────────────────┐
│        a        │
├─────────────────┤
│               3 │
└─────────────────┘
```

上記のクエリによってストリーム内に存在していたすべてのデータが消費されたため、ストリームは現在空です。

```sql
-- empty results
SELECT * FROM s;
```