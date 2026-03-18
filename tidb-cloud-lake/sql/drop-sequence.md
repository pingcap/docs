---
title: DROP SEQUENCE
summary: Deletes an existing sequence from Databend.
---

> **Note:**
>
> Introduced or updated in v1.2.426.

Deletes an existing sequence from Databend.

## Syntax

```sql
DROP SEQUENCE [IF EXISTS] <sequence>
```

| Parameter    | Description                             |
|--------------|-----------------------------------------|
| `<sequence>` | The name of the sequence to be deleted. |

## Examples

```sql
-- Delete a sequence named staff_id_seq
DROP SEQUENCE staff_id_seq;
```