---
title: RENAME DICTIONARY
summary: 辞書の名前を変更します。
---

# RENAME DICTIONARY

辞書の名前を変更します。

## 構文 {#syntax}

```sql
RENAME DICTIONARY [ IF EXISTS ]
    [ <catalog_name>. ][ <database_name>. ]<dictionary_name>
    TO [ <new_catalog_name>. ][ <new_database_name>. ]<new_dictionary_name>
```

## パラメータ {#parameters}

| パラメータ | 説明 |
|-----------|-------------|
| `IF EXISTS` | 任意。ソース辞書が存在しない場合のエラーを抑制します。 |
| `<dictionary_name>` | 現在の辞書名です。 |
| `<new_dictionary_name>` | 新しい辞書名です。 |

## 例 {#examples}

```sql
RENAME DICTIONARY user_info TO user_profile;
```

```sql
RENAME DICTIONARY IF EXISTS default.user_info TO analytics.user_profile;
```