---
title: bool_or
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.756"/>

Returns true if at least one input value is true, otherwise false

- NULL values are ignored.
- If all input values are null, the result is null.
- Supports for boolean types

## Syntax

```sql
bool_or(<expr>)
```

## Return Type

Same as the input type.

## Examples

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