---
title: SHOW DATABASES
summary: インスタンス上に存在するデータベースの一覧を表示します。
---

# SHOW DATABASES

インスタンス上に存在するデータベースの一覧を表示します。

関連情報: [system.databases](/tidb-cloud-lake/sql/system-databases.md)

## 構文 {#syntax}

```sql
SHOW [ FULL ] DATABASES
    [ LIKE '<pattern>' | WHERE <expr> ]
```

| パラメータ | 説明                                                                                                                 |
|-----------|-----------------------------------------------------------------------------------------------------------------------------|
| FULL      | 追加情報を含めて結果を一覧表示します。詳細は [例](#examples) を参照してください。                                  |
| LIKE      | 大文字と小文字を区別するパターンマッチングを使用して、名前で結果を絞り込みます。                                                   |
| WHERE     | WHERE 句の式を使用して結果を絞り込みます。                                                                |

## 例 {#examples}

```sql
SHOW DATABASES;

┌──────────────────────┐
│ databases_in_default │
├──────────────────────┤
│ canada               │
│ china                │
│ default              │
│ information_schema   │
│ system               │
│ test                 │
└──────────────────────┘

SHOW FULL DATABASES;

┌───────────────────────────────────────────────────┐
│ catalog │       owner      │ databases_in_default │
├─────────┼──────────────────┼──────────────────────┤
│ default │ account_admin    │ canada               │
│ default │ account_admin    │ china                │
│ default │ NULL             │ default              │
│ default │ NULL             │ information_schema   │
│ default │ NULL             │ system               │
│ default │ account_admin    │ test                 │
└───────────────────────────────────────────────────┘
```