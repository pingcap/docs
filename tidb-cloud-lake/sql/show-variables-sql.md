---
title: SHOW_VARIABLES
summary: 显示所有会话变量及其详细信息，例如名称、值和类型。
---

# SHOW_VARIABLES

显示所有会话变量及其详细信息，例如名称、值和类型。

另请参阅：[SHOW VARIABLES](/tidb-cloud-lake/sql/show-variables.md)

## 语法 {#syntax}

```sql
SHOW_VARIABLES()
```

## 示例 {#examples}

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