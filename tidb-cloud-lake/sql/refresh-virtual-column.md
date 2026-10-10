---
title: REFRESH VIRTUAL COLUMN
summary: {{{ .lake }}} の `REFRESH VIRTUAL COLUMN` コマンドは、既存のテーブルに対する仮想カラムの作成を明示的にトリガーするために使用されます。{{{ .lake }}} は新しいデータに対して仮想カラムを自動的に管理しますが、この機能を最大限に活用するために手動でのリフレッシュが必要となる特定のシナリオがあります。
---

# REFRESH VIRTUAL COLUMN

{{{ .lake }}} の `REFRESH VIRTUAL COLUMN` コマンドは、既存のテーブルに対する仮想カラムの作成を明示的にトリガーするために使用されます。{{{ .lake }}} は新しいデータに対して仮想カラムを自動的に管理しますが、この機能を最大限に活用するために手動でのリフレッシュが必要となる特定のシナリオがあります。

仮想カラムは v1.2.832 以降、デフォルトで有効になっています。

## `REFRESH VIRTUAL COLUMN` を使用するタイミング {#when-to-use-refresh-virtual-column}

- **機能有効化前の既存テーブル:** 仮想カラム機能が有効になる *前* に作成された `VARIANT` データを含むテーブルがある場合（または仮想カラムの自動作成に対応したバージョンへアップグレードする前に作成された場合）、クエリ高速化を有効にするには仮想カラムをリフレッシュする必要があります。{{{ .lake }}} は、これらのテーブルにすでに存在しているデータに対しては仮想カラムを自動作成しません。

## 構文 {#syntax}

```sql
REFRESH VIRTUAL COLUMN FOR <table>
```

## 例 {#examples}

次の例では、`test` という名前のテーブルに対して仮想カラムをリフレッシュします。

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

REFRESH VIRTUAL COLUMN FOR test;

SHOW VIRTUAL COLUMNS WHERE table = 'test' AND database = 'default';
╭───────────────────────────────────────────────────────────────────────────────────────────────────╮
│ database │  table │ source_column │ virtual_column_id │ virtual_column_name │ virtual_column_type │
│  String  │ String │     String    │       UInt32      │        String       │        String       │
├──────────┼────────┼───────────────┼───────────────────┼─────────────────────┼─────────────────────┤
│ default  │ test   │ val           │        3000000000 │ ['id']              │ UInt64              │
│ default  │ test   │ val           │        3000000001 │ ['name']            │ String              │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯
```