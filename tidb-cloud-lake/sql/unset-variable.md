---
title: UNSET VARIABLE
summary: 現在のセッションから 1 つ以上の変数を削除します。
---

# UNSET VARIABLE

現在のセッションから 1 つ以上の変数を削除します。

## 構文 {#syntax}

```sql
-- Remove one variable
UNSET VARIABLE <variable_name>

-- Remove more than one variable
UNSET VARIABLE (<variable1>, <variable2>, ...)
```

## 例 {#examples}

次の例では、単一の変数を unset します。

```sql
-- Remove the variable a from the session
UNSET VARIABLE a;
```

次の例では、複数の変数を unset します。

```sql
-- Remove variables x and y from the session
UNSET VARIABLE (x, y);
```