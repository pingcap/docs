---
title: bool_and
summary: すべての入力値が true の場合に true を返し、それ以外の場合は false を返します。
---

# bool_and

すべての入力値が true の場合に true を返し、それ以外の場合は false を返します。

- NULL 値は無視されます。
- すべての入力値が null の場合、結果は null になります。
- boolean 型をサポートします

## 構文 {#syntax}

```sql
bool_and(<expr>)
```

## 戻り値の型 {#return-type}

入力型と同じです。

## 例 {#examples}

```sql
select bool_and(t) from (values (true), (true), (null)) a(t);
╭───────────────────╮
│    bool_and(t)    │
│ Nullable(Boolean) │
├───────────────────┤
│ true              │
╰───────────────────╯

select bool_and(t) from (values (true), (true), (true)) a(t);

╭───────────────────╮
│    bool_and(t)    │
│ Nullable(Boolean) │
├───────────────────┤
│ true              │
╰───────────────────╯

select bool_and(t) from (values (true), (true), (false)) a(t);
╭───────────────────╮
│    bool_and(t)    │
│ Nullable(Boolean) │
├───────────────────┤
│ false             │
╰───────────────────╯
```