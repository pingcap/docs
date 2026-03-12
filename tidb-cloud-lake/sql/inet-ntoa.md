---
title: INET_NTOA
---

Converts a 32-bit integer to an IPv4 address.

## Syntax

```sql
INET_NOTA( <int32> )
```

## Aliases

- [IPV4_NUM_TO_STRING](ipv4-num-to-string.md)

## Return Type

String.

## Examples

```sql
SELECT IPV4_NUM_TO_STRING(16909060), INET_NTOA(16909060);

┌────────────────────────────────────────────────────┐
│ ipv4_num_to_string(16909060) │ inet_ntoa(16909060) │
├──────────────────────────────┼─────────────────────┤
│ 1.2.3.4                      │ 1.2.3.4             │
└────────────────────────────────────────────────────┘
```