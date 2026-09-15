---
title: bool_and
summary: 如果所有输入值都为 true，则返回 true；否则返回 false。
---

# bool_and

如果所有输入值都为 true，则返回 true；否则返回 false。

- 会忽略 NULL 值。
- 如果所有输入值都为 null，结果为 null。
- 支持布尔类型

## 语法 {#syntax}

```sql
bool_and(<expr>)
```

## 返回类型 {#return-type}

与输入类型相同。

## 示例 {#examples}

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