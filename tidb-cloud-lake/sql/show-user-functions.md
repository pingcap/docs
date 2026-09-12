---
title: SHOW USER FUNCTIONS
summary: 列出所有用户定义函数，包括标量函数、表函数、嵌入式函数和外部函数。
---

# SHOW USER FUNCTIONS

列出所有用户定义函数，包括标量函数、表函数、嵌入式函数和外部函数。

## 语法 {#syntax}

```sql
SHOW USER FUNCTIONS
```

## 输出列 {#output-columns}

| 列 | 描述 |
|--------|-------------|
| `name` | 函数名称 |
| `is_aggregate` | 是否为聚合函数（对于 UDF 为 NULL） |
| `description` | 如果提供，则为函数描述 |
| `arguments` | JSON 格式的函数参数 |
| `language` | 编程语言：SQL、python、javascript、wasm 或 external |
| `created_on` | 函数创建时间戳 |

## 示例 {#examples}

```sql
SHOW USER FUNCTIONS;

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  name  │    is_aggregate   │ description │           arguments           │ language │         created_on         │
│ String │ Nullable(Boolean) │    String   │            Variant            │  String  │          Timestamp         │
├────────┼───────────────────┼─────────────┼───────────────────────────────┼──────────┼────────────────────────────┤
│ get_v1 │ NULL              │             │ {"parameters":["input_json"]} │ SQL      │ 2024-11-18 23:20:28.432842 │
│ get_v2 │ NULL              │             │ {"parameters":["input_json"]} │ SQL      │ 2024-11-18 23:21:46.838744 │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```