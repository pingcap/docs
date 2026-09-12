---
title: SHOW VARIABLES
summary: 显示所有会话变量及其详细信息，例如名称、值和类型。
---

# SHOW VARIABLES

显示所有会话变量及其详细信息，例如名称、值和类型。

另请参阅：[SHOW_VARIABLES](/tidb-cloud-lake/sql/show-variables.md)

## 语法 {#syntax}

```sql
SHOW VARIABLES [ LIKE '<pattern>' | WHERE <expr> ]
```

## 示例 {#examples}

以下示例列出了所有会话变量及其值和类型：

```sql
SHOW VARIABLES;

┌──────────────────────────┐
│  name  │  value │  type  │
├────────┼────────┼────────┤
│ a      │ 3      │ UInt8  │
│ b      │ 55     │ UInt8  │
│ x      │ 'xx'   │ String │
│ y      │ 'yy'   │ String │
└──────────────────────────┘
```

要筛选并仅返回名为 `a` 的变量，请使用以下任一查询：

```sql
SHOW VARIABLES LIKE 'a';

SHOW VARIABLES WHERE name = 'a';
```