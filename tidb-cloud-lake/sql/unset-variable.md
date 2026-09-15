---
title: UNSET VARIABLE
summary: 从当前会话中移除一个或多个变量。
---

# UNSET VARIABLE

从当前会话中移除一个或多个变量。

## 语法 {#syntax}

```sql
-- Remove one variable
UNSET VARIABLE <variable_name>

-- Remove more than one variable
UNSET VARIABLE (<variable1>, <variable2>, ...)
```

## 示例 {#examples}

以下示例取消设置单个变量：

```sql
-- Remove the variable a from the session
UNSET VARIABLE a;
```

以下示例取消设置多个变量：

```sql
-- Remove variables x and y from the session
UNSET VARIABLE (x, y);
```