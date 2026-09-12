---
title: DROP DICTIONARY
summary: 删除一个字典。
---

# DROP DICTIONARY

删除一个字典。

## 语法 {#syntax}

```sql
DROP DICTIONARY [ IF EXISTS ] [ <catalog_name>. ][ <database_name>. ]<dictionary_name>
```

## 参数 {#parameters}

| 参数 | 描述 |
|-----------|-------------|
| `IF EXISTS` | 可选。如果字典不存在，则抑制报错。 |
| `<dictionary_name>` | 字典名称。你可以使用 catalog 和 database 名称对其进行限定。 |

## 示例 {#examples}

```sql
DROP DICTIONARY user_info;
```

```sql
DROP DICTIONARY IF EXISTS default.user_info;
```