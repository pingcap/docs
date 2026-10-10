---
title: BETWEEN
summary: 指定された数値または文字列 `<expr>` が、定義された下限値と上限値の範囲内にある場合に true を返します。
---

# BETWEEN

指定された数値または文字列 `<expr>` が、定義された下限値と上限値の範囲内にある場合に `true` を返します。

## 構文 {#syntax}

```sql
<expr> [ NOT ] BETWEEN <lower_limit> AND <upper_limit>
```

## 例 {#examples}

```sql
SELECT 'true' WHERE 5 BETWEEN 0 AND 5;

┌────────┐
│ 'true' │
├────────┤
│ true   │
└────────┘

SELECT 'true' WHERE 'data' BETWEEN 'data' AND 'datalakecloud';

┌────────┐
│ 'true' │
├────────┤
│ true   │
└────────┘
```