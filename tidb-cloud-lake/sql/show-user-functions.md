---
title: SHOW USER FUNCTIONS
summary: スカラー関数、テーブル関数、埋め込み関数、外部関数を含む、すべてのユーザー定義関数を一覧表示します。
---

# SHOW USER FUNCTIONS

スカラー関数、テーブル関数、埋め込み関数、外部関数を含む、すべてのユーザー定義関数を一覧表示します。

## 構文 {#syntax}

```sql
SHOW USER FUNCTIONS
```

## 出力カラム {#output-columns}

| カラム | 説明 |
|--------|-------------|
| `name` | 関数名 |
| `is_aggregate` | 集約関数かどうか（UDF の場合は NULL） |
| `description` | 指定されている場合の関数の説明 |
| `arguments` | JSON 形式の関数パラメータ |
| `language` | プログラミング言語: SQL、python、javascript、wasm、または external |
| `created_on` | 関数の作成タイムスタンプ |

## 例 {#examples}

```sql
SHOW USER FUNCTIONS;

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  name  │    is_aggregate   │ description │           arguments           │ language │         created_on         │
│ String │ Nullable(Boolean) │    String   │            Variant            │  String  │          Timestamp         │
├────────┼───────────────────┼─────────────┼───────────────────────────────┼──────────┼────────────────────────────┤
│ get_v1 │ NULL              │             │ {"parameters":["input_json"]} │ SQL      │ 2024-11-18 23:20:28.432842 │
│ get_v2 │ NULL              │             │ {"parameters":["input_json"]} │ SQL      │ 2024-11-18 23:21:46.838744 │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```