---
title: "CAST::"
---

Converts a value from one data type to another. `::` is an alias for CAST.

See also: [TRY_CAST](try-cast.md)

## Syntax

```sql
CAST( <expr> AS <data_type> )

<expr>::<data_type>
```

## Examples

```sql
SELECT CAST(1 AS VARCHAR), 1::VARCHAR;

┌───────────────────────────────┐
│ cast(1 as string) │ 1::string │
├───────────────────┼───────────┤
│ 1                 │ 1         │
└───────────────────────────────┘
```


Cast String to
Variant and Cast Variant to `Map<String, Variant>`
```sql
select '{"k1":"v1","k2":"v2"}'::Variant a, a::Map(String, String) b, b::Variant = a;
┌──────────────────────┬──────────────────────┬────────────────┐
│ a                    │ b                    │ b::VARIANT = a │
├──────────────────────┼──────────────────────┼────────────────┤
│ {"k1":"v1","k2":"v2"}│ {'k1':'v1','k2':'v2'}│ 1              │
└──────────────────────┴──────────────────────┴────────────────┘
```
