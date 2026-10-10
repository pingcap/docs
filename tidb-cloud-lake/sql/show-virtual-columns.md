---
title: SHOW VIRTUAL COLUMNS
summary: システム内で作成された仮想カラムを表示します。`SELECT * FROM system.virtual_columns` と同等です。
---

# SHOW VIRTUAL COLUMNS

システム内で作成された仮想カラムを表示します。`SELECT * FROM system.virtual_columns` と同等です。

仮想カラムは v1.2.832 以降、デフォルトで有効になっています。

関連情報: [system.virtual_columns](/tidb-cloud-lake/sql/system-virtual-columns.md)

## 推奨構文 {#preferred-syntax}

特定のテーブルを確認する、またはすべての仮想カラムを一覧表示するには、最もシンプルで実用的な形式でコマンドを使用します。

```sql
SHOW VIRTUAL COLUMNS [WHERE table = '<table_name>' AND database = '<database_name>']
```

## 例 {#example}

```sql
CREATE TABLE test(id int, val variant);

INSERT INTO
  test
VALUES
  (
    1,
    '{"id":1,"name":"datalake"}'
  ),
  (
    2,
    '{"id":2,"name":"databricks"}'
  );

SHOW VIRTUAL COLUMNS WHERE table = 'test' AND database = 'default';
╭───────────────────────────────────────────────────────────────────────────────────────────────────╮
│ database │  table │ source_column │ virtual_column_id │ virtual_column_name │ virtual_column_type │
│  String  │ String │     String    │       UInt32      │        String       │        String       │
├──────────┼────────┼───────────────┼───────────────────┼─────────────────────┼─────────────────────┤
│ default  │ test   │ val           │        3000000000 │ ['id']              │ UInt64              │
│ default  │ test   │ val           │        3000000001 │ ['name']            │ String              │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯
```