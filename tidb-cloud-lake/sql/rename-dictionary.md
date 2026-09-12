---
title: RENAME DICTIONARY
summary: 重命名字典。
---

# RENAME DICTIONARY

重命名字典。

## 语法 {#syntax}

```sql
RENAME DICTIONARY [ IF EXISTS ]
    [ <catalog_name>. ][ <database_name>. ]<dictionary_name>
    TO [ <new_catalog_name>. ][ <new_database_name>. ]<new_dictionary_name>
```

## 参数 {#parameters}

| 参数 | 描述 |
|-----------|-------------|
| `IF EXISTS` | 可选。如果源字典不存在，则抑制报错。 |
| `<dictionary_name>` | 当前字典名称。 |
| `<new_dictionary_name>` | 新的字典名称。 |

## 示例 {#examples}

```sql
RENAME DICTIONARY user_info TO user_profile;
```

```sql
RENAME DICTIONARY IF EXISTS default.user_info TO analytics.user_profile;
```