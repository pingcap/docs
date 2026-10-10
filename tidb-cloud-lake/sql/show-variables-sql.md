---
title: SHOW_VARIABLES
summary: すべてのセッション変数と、その名前、値、型などの詳細を表示します。
---

# SHOW_VARIABLES

すべてのセッション変数と、その名前、値、型などの詳細を表示します。

関連情報: [SHOW VARIABLES](/tidb-cloud-lake/sql/show-variables.md)

## 構文 {#syntax}

```sql
SHOW_VARIABLES()
```

## 例 {#examples}

```sql
SELECT name, value, type FROM SHOW_VARIABLES();

┌──────────────────────────┐
│  name  │  value │  type  │
├────────┼────────┼────────┤
│ y      │ 'yy'   │ String │
│ b      │ 55     │ UInt8  │
│ x      │ 'xx'   │ String │
│ a      │ 3      │ UInt8  │
└──────────────────────────┘
```