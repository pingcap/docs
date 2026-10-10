---
title: OBFUSCATE
summary: データセットの匿名化。これは簡易ツールであり、より複雑なシナリオでは、基盤となる関数 MARKOV_TRAIN、MARKOV_GENERATE、FEISTEL_OBFUSCATE を直接使用することを推奨します。
---

# OBFUSCATE

データセットの匿名化。これは簡易ツールであり、より複雑なシナリオでは、基盤となる関数 [MARKOV_TRAIN](/tidb-cloud-lake/sql/markov-train.md)、[MARKOV_GENERATE](/tidb-cloud-lake/sql/markov-generate.md)、[FEISTEL_OBFUSCATE](/tidb-cloud-lake/sql/feistel-obfuscate.md) を直接使用することを推奨します。

## 構文 {#syntax}

```sql
OBFUSCATE('<table>'[, seed => <seed>])
```

## 例 {#examples}

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

-- 1 回の呼び出しでテーブルをマスキング。seed により再現可能性を維持
SELECT * FROM obfuscate(demo_customers, seed=>2025)
ORDER BY id;

-- 出力例
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