---
title: bool_or
summary: 少なくとも 1 つの入力値が true の場合に true を返し、それ以外の場合は false を返します。
---

# bool_or

少なくとも 1 つの入力値が true の場合に true を返し、それ以外の場合は false を返します。

- NULL 値は無視されます。
- すべての入力値が null の場合、結果は null になります。
- boolean 型をサポートします。

## 構文 {#syntax}

```sql
bool_or(<expr>)
```

## 戻り値の型 {#return-type}

入力型と同じです。

## 例 {#examples}

```sql
select bool_or(t) from (values (true), (true), (null)) a(t);
╭───────────────────╮
│    bool_or(t)     │
│ Nullable(Boolean) │
├───────────────────┤
│ true              │
╰───────────────────╯

select bool_or(t) from (values (true), (true), (false)) a(t);
╭───────────────────╮
│    bool_or(t)     │
│ Nullable(Boolean) │
├───────────────────┤
│ true              │
╰───────────────────╯

select bool_or(t) from (values (false), (false), (false)) a(t);
╭───────────────────╮
│    bool_or(t)    │
│ Nullable(Boolean) │
├───────────────────┤
│ false             │
╰───────────────────╯
```