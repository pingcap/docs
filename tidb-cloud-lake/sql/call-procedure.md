---
title: CALL PROCEDURE
summary: ストアドプロシージャ名を指定して実行し、必要に応じて引数を渡します。
---

# CALL PROCEDURE

ストアドプロシージャ名を指定して実行し、プロシージャが必要とする場合は引数を渡します。

## 構文 {#syntax}

```sql
CALL PROCEDURE <procedure_name>([<argument1>, <argument2>, ...])
```

## 例 {#examples}

次の例は、重量をキログラム (kg) からポンド (lb) に変換するストアドプロシージャを作成して呼び出す方法を示しています。

```sql
CREATE PROCEDURE convert_kg_to_lb(kg DECIMAL(4, 2))
RETURNS DECIMAL(10, 2)
LANGUAGE SQL
COMMENT = 'Converts kilograms to pounds'
AS $$
BEGIN
    RETURN kg * 2.20462;
END;
$$;

CALL PROCEDURE convert_kg_to_lb(10.00);

┌────────────┐
│   Result   │
├────────────┤
│ 22.0462000 │
└────────────┘
```