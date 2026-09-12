---
title: Decimal
summary: Decimal 类型是用于存储和处理的高精度数值。
---

# Decimal

## 概述 {#overview}

`DECIMAL(P, S)` 用于存储精确数值，其中精度 `P` 表示总位数（1–76），扩展 `S` 表示小数点右侧的位数（0–P）。取值必须位于 ±`(10^P - 1) / 10^S` 范围内。精度不超过 38 的值使用 `DECIMAL128`，更大的值使用 `DECIMAL256`。

## 示例 {#examples}

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

结果：

```
┌─────────────┬──────────┬──────────┬────────────┬────────────┐
│ description │ amount   │ tax_rate │ tax_value  │ total_due  │
├─────────────┼──────────┼──────────┼────────────┼────────────┤
│ Laptop      │ 1299.99  │ 0.1300   │ 168.998700 │ 1468.988700 │
│ Monitor     │  399.50  │ 0.0750   │  29.962500 │  429.462500 │
└─────────────┴──────────┴──────────┴────────────┴────────────┘
```

算术运算会自动保持精度：加法会保留最宽的整数部分和小数部分，乘法会累加精度，除法会保留左操作数的扩展。如果你需要特定的结果格式，请使用显式类型转换。

```sql
SELECT
  SUM(amount)                              AS sum_default,
  CAST(SUM(amount) AS DECIMAL(12, 2))      AS sum_cast,
  AVG(amount)                              AS avg_default,
  CAST(AVG(amount) AS DECIMAL(12, 4))      AS avg_cast
FROM invoices;
```

结果：

```
┌─────────────┬───────────┬────────────────┬──────────┐
│ sum_default │ sum_cast  │ avg_default    │ avg_cast │
├─────────────┼───────────┼────────────────┼──────────┤
│ 1699.49     │ 1699.49   │ 849.74500000   │ 849.7450 │
└─────────────┴───────────┴────────────────┴──────────┘
```

如果某个运算会导致整数部分溢出，{{{ .lake }}} 会报错；多余的小数位会被截断而不是四舍五入。你可以通过调整 `P`/`S` 或对结果进行类型转换来控制这两种行为。