---
title: OBFUSCATE
---

Dataset anonymization. This is a quick tool, and for more complex scenarios, it is recommended to directly use the underlying function [MARKOV_TRAIN](../07-aggregate-functions/aggregate-markov-train.md), [MARKOV_GENERATE](../19-data-anonymization-functions/markov_generate.md), [FEISTEL_OBFUSCATE](../19-data-anonymization-functions/feistel_obfuscate.md).

## Syntax

```sql
OBFUSCATE('<table>'[, seed => <seed>])
```

## Examples

```sql
CREATE OR REPLACE TABLE demo_customers AS
SELECT *
FROM (
  VALUES
    (1,'Alice Johnson','alice.johnson@gmail.com','555-123-0001','123 Maple St, Springfield, IL'),
    (2,'Bob Smith','bob.smith@yahoo.com','555-123-0002','456 Oak Ave, Dayton, OH'),
    (3,'Carol Davis','carol.davis@outlook.com','555-123-0003','789 Pine Rd, Austin, TX'),
    (4,'David Miller','david.miller@example.com','555-123-0004','321 Birch Blvd, Denver, CO'),
    (5,'Emma Wilson','emma.wilson@example.com','555-123-0005','654 Cedar Ln, Seattle, WA'),
    (6,'Frank Brown','frank.brown@gmail.com','555-123-0006','987 Walnut Dr, Portland, OR'),
    (7,'Grace Lee','grace.lee@example.com','555-123-0007','159 Ash Ct, Boston, MA'),
    (8,'Henry Clark','henry.clark@example.com','555-123-0008','753 Elm St, Phoenix, AZ')
) AS t(id, full_name, email, phone, address);

-- One-call table masking; seed keeps it reproducible
SELECT * FROM obfuscate(demo_customers, seed=>2025)
ORDER BY id;

-- Sample output
┌────id┬───────────────┬────────────────────────────────┬──────────────┬────────────────────────────────────┐
│  1  │ Alice Johnson  │ emma.wilson@example.com        │ 555-123-0002 │ 123 Maple St, Phoenix, AZ         │
│  2  │ Alice Johnson  │ grace.lee@example.com          │ 555-123-0007 │ 753 Elm St, Phoenix, AZ           │
│  3  │ David Miller   │ frank.brown@gmail.com          │ 555-123-0001 │ 321 Birch Blvd, Denver,           │
│  4  │ Alice Johnson  │ emma.wilson@example.com        │ 555-123-0001 │ 654 Cedar Ln, Seattle, WA         │
│  5  │ Grace Lee      │ carol.david.miller@example     │ 555-123-0003 │ 123 Maple St, Phoenix, AZ         │
│  6  │ Carol David    │ emma.wilson@example.com        │ 555-123-0003 │ 654 Cedar Ln, Seattle,            │
│  7  │ Emma Wilson    │ bob.smith@yahoo.com            │ 555-123-0004 │ 456 Oak Ave, Dayton, MA           │
│  9  │ Carol David    │ frank.brown@gmail.com          │ 555-123-0006 │ 456 Oak Ave, Dayton, MA           │
└──────┴───────────────┴────────────────────────────────┴──────────────┴────────────────────────────────────┘
```
