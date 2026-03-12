---
title: TRY_TO_BINARY
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.673"/>

An enhanced version of [TO_BINARY](to-binary.md) that converts an input expression to a binary value, returning `NULL` if the conversion fails instead of raising an error.

See also: [TO_BINARY](to-binary.md)

## Syntax

```sql
TRY_TO_BINARY( <expr> )
```

## Examples

This example successfully converts the JSON data to binary:

```sql
SELECT TRY_TO_BINARY(PARSE_JSON('{"key":"value", "number":123}')) AS binary_variant_success;

┌──────────────────────────────────────────────────────────────────────────┐
│                              binary_variant                              │
├──────────────────────────────────────────────────────────────────────────┤
│ 40000002100000031000000610000005200000026B65796E756D62657276616C7565507B │
└──────────────────────────────────────────────────────────────────────────┘
```

This example demonstrates that the function fails to convert when the input is `NULL`:

```sql
SELECT TRY_TO_BINARY(PARSE_JSON(NULL)) AS binary_variant_invalid_json;

┌─────────────────────────────┐
│ binary_variant_invalid_json │
├─────────────────────────────┤
│ NULL                        │
└─────────────────────────────┘
```