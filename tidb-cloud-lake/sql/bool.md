---
title: bool_and
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.756"/>

Returns true if all input values are true, otherwise false.

- NULL values are ignored.
- If all input values are null, the result is null.
- Supports for boolean types

## Syntax

```sql
bool_and(<expr>)
```

## Return Type

Same as the input type.

## Examples

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