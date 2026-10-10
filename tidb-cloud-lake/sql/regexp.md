---
title: REGEXP
summary: 文字列 `<expr>` が `<pattern>` で指定された正規表現に一致する場合は true を返し、それ以外の場合は false を返します。
---

# REGEXP

文字列 `<expr>` が `<pattern>` で指定された正規表現に一致する場合は `true` を返し、それ以外の場合は `false` を返します。

## 構文 {#syntax}

```sql
<expr> REGEXP <pattern>
```

## エイリアス {#aliases}

- [RLIKE](/tidb-cloud-lake/sql/rlike.md)

## 例 {#examples}

```sql
SELECT 'datalake' REGEXP 'd*', 'datalake' RLIKE 'd*';

┌────────────────────────────────────────────────────┐
│ ('datalake' regexp 'd*') │ ('datalake' rlike 'd*') │
├──────────────────────────┼─────────────────────────┤
│ true                     │ true                    │
└────────────────────────────────────────────────────┘
```