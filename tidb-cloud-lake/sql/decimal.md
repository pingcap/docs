---
title: Decimal
description: Decimal types are high-precision numeric values to be stored and manipulated.
sidebar_position: 5
---

## Overview

`DECIMAL(P, S)` stores exact numeric values with precision `P` (total digits, 1–76) and scale `S` (digits to the right of the decimal point, 0–P). Values must sit within ±`(10^P - 1) / 10^S`. Precisions up to 38 use `DECIMAL128`, and larger values use `DECIMAL256`.

## Examples

```sql
CREATE TABLE invoices (
  description STRING,
  amount DECIMAL(10, 2),
  tax_rate DECIMAL(5, 4)
);

INSERT INTO invoices VALUES
  ('Laptop', 1299.99, 0.1300),
  ('Monitor', 399.50, 0.0750);

SELECT
  description,
  amount,
  tax_rate,
  amount * tax_rate          AS tax_value,
  amount + amount * tax_rate AS total_due
FROM invoices;
```

Result:
```
┌─────────────┬──────────┬──────────┬────────────┬────────────┐
│ description │ amount   │ tax_rate │ tax_value  │ total_due  │
├─────────────┼──────────┼──────────┼────────────┼────────────┤
│ Laptop      │ 1299.99  │ 0.1300   │ 168.998700 │ 1468.988700 │
│ Monitor     │  399.50  │ 0.0750   │  29.962500 │  429.462500 │
└─────────────┴──────────┴──────────┴────────────┴────────────┘
```

Arithmetic preserves precision automatically: additions keep the widest integer and fractional parts, multiplication adds precisions, and division keeps the left operand's scale. Use explicit casts if you need a specific result shape.

```sql
SELECT
  SUM(amount)                              AS sum_default,
  CAST(SUM(amount) AS DECIMAL(12, 2))      AS sum_cast,
  AVG(amount)                              AS avg_default,
  CAST(AVG(amount) AS DECIMAL(12, 4))      AS avg_cast
FROM invoices;
```

Result:
```
┌─────────────┬───────────┬────────────────┬──────────┐
│ sum_default │ sum_cast  │ avg_default    │ avg_cast │
├─────────────┼───────────┼────────────────┼──────────┤
│ 1699.49     │ 1699.49   │ 849.74500000   │ 849.7450 │
└─────────────┴───────────┴────────────────┴──────────┘
```

If an operation would overflow the integer part, Databend raises an error; extra fractional digits are truncated rather than rounded. Adjust `P`/`S` or cast the result to control both behaviors.
