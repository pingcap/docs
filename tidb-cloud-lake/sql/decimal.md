---
title: Decimal
summary: Decimal 型は、高精度の数値を保存および操作するための型です。
---

# Decimal

## 概要 {#overview}

`DECIMAL(P, S)` は、精度 `P`（全桁数、1–76）とスケール `S`（小数点以下の桁数、0–P）を持つ正確な数値を格納します。値は ±`(10^P - 1) / 10^S` の範囲内である必要があります。精度が 38 までの値には `DECIMAL128` が使用され、それより大きい値には `DECIMAL256` が使用されます。

## 例 {#examples}

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

結果:

```
┌─────────────┬──────────┬──────────┬────────────┬────────────┐
│ description │ amount   │ tax_rate │ tax_value  │ total_due  │
├─────────────┼──────────┼──────────┼────────────┼────────────┤
│ Laptop      │ 1299.99  │ 0.1300   │ 168.998700 │ 1468.988700 │
│ Monitor     │  399.50  │ 0.0750   │  29.962500 │  429.462500 │
└─────────────┴──────────┴──────────┴────────────┴────────────┘
```

算術演算では精度が自動的に保持されます。加算では整数部と小数部のうち広い方が維持され、乗算では精度が加算され、除算では左オペランドのスケールが維持されます。必要な結果の形式がある場合は、明示的なキャストを使用してください。

```sql
SELECT
  SUM(amount)                              AS sum_default,
  CAST(SUM(amount) AS DECIMAL(12, 2))      AS sum_cast,
  AVG(amount)                              AS avg_default,
  CAST(AVG(amount) AS DECIMAL(12, 4))      AS avg_cast
FROM invoices;
```

結果:

```
┌─────────────┬───────────┬────────────────┬──────────┐
│ sum_default │ sum_cast  │ avg_default    │ avg_cast │
├─────────────┼───────────┼────────────────┼──────────┤
│ 1699.49     │ 1699.49   │ 849.74500000   │ 849.7450 │
└─────────────┴───────────┴────────────────┴──────────┘
```

演算によって整数部がオーバーフローする場合、{{{ .lake }}} はエラーを返します。余分な小数桁は丸められずに切り捨てられます。これら 2 つの動作を制御するには、`P`/`S` を調整するか、結果をキャストしてください。