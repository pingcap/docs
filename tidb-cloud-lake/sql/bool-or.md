---
title: bool_or
summary: 如果至少有一个输入值为 true，则返回 true；否则返回 false。
---

# bool_or

如果至少有一个输入值为 true，则返回 true；否则返回 false

- 会忽略 NULL 值。
- 如果所有输入值都是 null，结果为 null。
- 支持布尔类型

## 语法 {#syntax}

```sql
bool_or(<expr>)
```

## 返回类型 {#return-type}

与输入类型相同。

## 示例 {#examples}

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