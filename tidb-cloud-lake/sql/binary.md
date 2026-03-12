---
title: Binary
description: Variable-length sequences of raw bytes.
sidebar_position: 2
---

## Overview

`BINARY` (alias `VARBINARY`) stores variable-length byte sequences. Unlike `STRING`, the value is not interpreted as UTF-8 text, making it suitable for payloads such as digests, compressed data, or serialized objects. Use conversion functions like [UNHEX](../../20-sql-functions/06-string-functions/unhex.md), [FROM_BASE64](../../20-sql-functions/06-string-functions/from-base64.md), and [TO_HEX](../../20-sql-functions/02-conversion-functions/to-hex.md) to encode or decode values when reading or writing the data.

## Examples

### Insert Raw Bytes

```sql
CREATE TABLE binary_samples (
  id INT,
  raw BINARY
);

INSERT INTO binary_samples VALUES
  (1, UNHEX('68656c6c6f')),             -- "hello"
  (2, FROM_BASE64('ZGF0YWJlbmQ='));     -- "databend"
```

```sql
SELECT
  id,
  HEX(raw)     AS hex_value,
  LENGTH(raw)  AS byte_len
FROM binary_samples
ORDER BY id;
```

Result:
```
┌────┬──────────────┬──────────┐
│ id │ hex_value    │ byte_len │
├────┼──────────────┼──────────┤
│  1 │ 68656c6c6f   │        5 │
│  2 │ 6461746162656e64 │     8 │
└────┴──────────────┴──────────┘
```

### Convert Back to Text

Binary values can be converted to strings when needed:

```sql
SELECT
  id,
  TO_VARCHAR(raw) AS text_value
FROM binary_samples
ORDER BY id;
```

Result:
```
┌────┬─────────────┐
│ id │ text_value  │
├────┼─────────────┤
│  1 │ hello       │
│  2 │ databend    │
└────┴─────────────┘
```

Binary columns accept NULL values and can also be nested inside ARRAY, MAP, or TUPLE structures when you need to store byte payloads alongside other data.
