---
title: CONNECTION_ID
summary: 現在の接続の接続 ID を返します。
---

# CONNECTION_ID

現在の接続の接続 ID を返します。

## 構文 {#syntax}

```sql
CONNECTION_ID()
```

## 例 {#examples}

```sql
SELECT CONNECTION_ID();

┌──────────────────────────────────────┐
│            connection_id()           │
├──────────────────────────────────────┤
│ 23cb06ec-583e-4eba-b790-7c8cf72a53f8 │
└──────────────────────────────────────┘
```