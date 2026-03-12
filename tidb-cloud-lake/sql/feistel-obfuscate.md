---
title: FEISTEL_OBFUSCATE
---

Deterministically obfuscate integers (e.g. IDs or phone numbers) while preserving bit length and value cardinality so joins still work.

## Syntax

```sql
FEISTEL_OBFUSCATE( <number>, <seed> )
```

## Arguments

| Arguments | Description |
| ----------- | ----------- |
| `number` | Input |
| `seed` | The data for corresponding non-text columns for different tables will be transformed in the same way, so the data for different tables can be JOINed after obfuscation |

## Return Type

Same as input

## Examples

```sql
SELECT feistel_obfuscate(10000,1561819567875);
+------------------------------------------+
| feistel_obfuscate(10000, 1561819567875)  |
+------------------------------------------+
| 15669                                    |
+------------------------------------------+
```

feistel_obfuscate preserves the number of bits in the original input. If mapping to a larger range is required, an offset can be added to the original input, e.g. feistel_obfuscate(n+10000,50)
```sql
SELECT feistel_obfuscate(10,1561819567875);
+------------------------------------------+
| feistel_obfuscate(10, 1561819567875)     |
+------------------------------------------+
| 13                                       |
+------------------------------------------+
```

Phone-number style example (seed = 4242):

```sql
SELECT 13000000000 + number AS phone,
       feistel_obfuscate(13000000000 + number, 4242) AS masked_phone
FROM numbers(5);

-- Sample output
+-------------+--------------+
|    phone    | masked_phone |
+-------------+--------------+
| 13000000000 | 12221668677  |
| 13000000001 | 10245458699  |
| 13000000002 | 15398657780  |
| 13000000003 | 9910824758   |
| 13000000004 | 13299971128  |
+-------------+--------------+
```
