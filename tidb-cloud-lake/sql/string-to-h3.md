---
title: STRING_TO_H3
summary: 文字列表現を H3 (uint64) 表現に変換します。
---

# STRING_TO_H3

文字列表現を [H3](https://eng.uber.com/h3/) の表現 (uint64) に変換します。

## 構文 {#syntax}

```sql
STRING_TO_H3(h3)
```

## 例 {#examples}

```sql
SELECT STRING_TO_H3('8d11aa6a38826ff');

┌─────────────────────────────────┐
│ string_to_h3('8d11aa6a38826ff') │
├─────────────────────────────────┤
│              635318325446452991 │
└─────────────────────────────────┘
```