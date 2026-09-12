---
title: CAST
summary: 将一个值从一种数据类型转换为另一种。`::` 是 CAST 的别名。
---

# CAST

将一个值从一种数据类型转换为另一种。`::` 是 CAST 的别名。

另请参阅：[TRY_CAST](/tidb-cloud-lake/sql/try-cast.md)

## 语法 {#syntax}

```sql
CAST( <expr> AS <data_type> )

<expr>::<data_type>
```

## 示例 {#examples}

```sql
SELECT CAST(1 AS VARCHAR), 1::VARCHAR;

┌───────────────────────────────┐
│ cast(1 as string) │ 1::string │
├───────────────────┼───────────┤
│ 1                 │ 1         │
└───────────────────────────────┘
```

将字符串转换为 Variant，并将 Variant 转换为 `Map<String, Variant>`

```sql
select '{"k1":"v1","k2":"v2"}'::Variant a, a::Map(String, String) b, b::Variant = a;
┌──────────────────────┬──────────────────────┬────────────────┐
│ a                    │ b                    │ b::VARIANT = a │
├──────────────────────┼──────────────────────┼────────────────┤
│ {"k1":"v1","k2":"v2"}│ {'k1':'v1','k2':'v2'}│ 1              │
└──────────────────────┴──────────────────────┴────────────────┘
```