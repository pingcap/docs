---
title: REFRESH VIRTUAL COLUMN
summary: {{{ .lake }}} 中的 `REFRESH VIRTUAL COLUMN` 命令用于显式触发为现有表创建虚拟列。虽然 {{{ .lake }}} 会自动管理新数据的虚拟列，但在某些特定场景下，仍需要手动刷新才能充分利用此功能。
---

# REFRESH VIRTUAL COLUMN

{{{ .lake }}} 中的 `REFRESH VIRTUAL COLUMN` 命令用于显式触发为现有表创建虚拟列。虽然 {{{ .lake }}} 会自动管理新数据的虚拟列，但在某些特定场景下，仍需要手动刷新才能充分利用此功能。

从 v1.2.832 开始，虚拟列默认启用。

## 何时使用 `REFRESH VIRTUAL COLUMN` {#when-to-use-refresh-virtual-column}

- **功能启用前已存在的表：** 如果你的表中包含 `VARIANT` 数据，并且这些表是在虚拟列功能启用之前创建的（或者是在升级到支持自动创建虚拟列的版本之前创建的），则需要刷新虚拟列以启用查询加速。对于这些表中已经存在的数据，{{{ .lake }}} 不会自动创建虚拟列。

## 语法 {#syntax}

```sql
REFRESH VIRTUAL COLUMN FOR <table>
```

## 示例 {#examples}

以下示例为名为 `test` 的表刷新虚拟列：

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