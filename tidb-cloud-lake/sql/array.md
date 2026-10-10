---
title: 配列
summary: 定義されたデータ型の配列。
---

# 配列

## 概要 {#overview}

`ARRAY(T)` は、すべての要素が型 `T` を共有する可変長コレクションを格納します。テーブル作成時に要素型を定義し、配列関数を使用して値を読み取ったり変換したりします。

> **Note:**
>
> {{{ .lake }}} の配列は 1 始まりです。`arr[1]` は最初の要素を返し、`arr[n]` は最後の要素を返します。

## 例 {#examples}

```sql
CREATE TABLE array_samples (arr ARRAY(INT64));

INSERT INTO array_samples VALUES ([1, 2, 3]), ([10, 20]);

SELECT
  arr,
  arr[1]   AS first_elem,
  arr[2]   AS second_elem
FROM array_samples;
```

結果:

```
┌────────────┬────────────┬──────────────┐
│ arr        │ first_elem │ second_elem │
├────────────┼────────────┼──────────────┤
│ [1,2,3]    │          1 │            2 │
│ [10,20]    │         10 │           20 │
└────────────┴────────────┴──────────────┘
```

```sql
-- Index 0 always returns NULL because arrays are 1-based.
SELECT arr[0] AS zeroth_elem FROM array_samples;
```

結果:

```
┌─────────────┐
│ zeroth_elem │
├─────────────┤
│ NULL        │
│ NULL        │
└─────────────┘
```