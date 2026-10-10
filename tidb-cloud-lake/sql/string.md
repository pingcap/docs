---
title: String
summary: 基本的な String データ型。
---

# String

## String データ型 {#string-data-types}

{{{ .lake }}} では、文字列は `VARCHAR` フィールドに格納でき、ストレージサイズは可変です。

| 名前    | エイリアス | ストレージサイズ |
|---------|---------|--------------|
| VARCHAR | STRING  | 可変     |

## 関数 {#functions}

[文字列関数](/tidb-cloud-lake/sql/string-functions-overview.md) を参照してください。

## 例 {#example}

```sql
CREATE TABLE string_table(text VARCHAR);
```

```
DESC string_table;
```

結果:

```
┌──────────────────────────────────────────────┐
│  Field │   Type  │  Null  │ Default │  Extra │
├────────┼─────────┼────────┼─────────┼────────┤
│ text   │ VARCHAR │ YES    │ NULL    │        │
└──────────────────────────────────────────────┘
```

```sql
INSERT INTO string_table VALUES('tidbcloudlake');
```

```
SELECT * FROM string_table;
```

結果:

```
┌──────────────────┐
│       text       │
├──────────────────┤
│ tidbcloudlake    │
└──────────────────┘
```