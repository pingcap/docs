---
title: DROP PROCEDURE
summary: 既存のストアドプロシージャを削除します。
---

# DROP PROCEDURE

既存のストアドプロシージャを削除します。

## 構文 {#syntax}

```sql
DROP PROCEDURE <procedure_name>([<parameter_type1>, <parameter_type2>, ...])
```

- プロシージャにパラメータがない場合は、空の括弧を使用します: `DROP PROCEDURE <procedure_name>()`;
- パラメータがあるプロシージャでは、エラーを避けるために正確な型を指定してください。

## 例 {#examples}

この例では、ストアドプロシージャを作成してから削除します。

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

DROP PROCEDURE convert_kg_to_lb(Decimal(4, 2));
```