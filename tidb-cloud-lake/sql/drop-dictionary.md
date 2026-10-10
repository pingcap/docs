---
title: DROP DICTIONARY
summary: 辞書を削除します。
---

# DROP DICTIONARY

辞書を削除します。

## 構文 {#syntax}

```sql
DROP DICTIONARY [ IF EXISTS ] [ <catalog_name>. ][ <database_name>. ]<dictionary_name>
```

## パラメータ {#parameters}

| パラメータ | 説明 |
|-----------|-------------|
| `IF EXISTS` | 任意。辞書が存在しない場合のエラーを抑制します。 |
| `<dictionary_name>` | 辞書名です。catalog 名および database 名で修飾できます。 |

## 例 {#examples}

```sql
DROP DICTIONARY user_info;
```

```sql
DROP DICTIONARY IF EXISTS default.user_info;
```