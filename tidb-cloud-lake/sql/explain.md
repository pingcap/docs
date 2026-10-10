---
title: EXPLAIN
summary: SQL ステートメントの実行計画を表示します。実行計画は異なる演算子で構成されるツリーとして表示され、{{{ .lake }}} が SQL ステートメントをどのように実行するかを確認できます。演算子には通常、{{{ .lake }}} が実行するアクションや、クエリに関連するオブジェクトを説明する 1 つ以上のフィールドが含まれます。
---

# EXPLAIN

SQL ステートメントの実行計画を表示します。実行計画は異なる演算子で構成されるツリーとして表示され、{{{ .lake }}} が SQL ステートメントをどのように実行するかを確認できます。演算子には通常、{{{ .lake }}} が実行するアクションや、クエリに関連するオブジェクトを説明する 1 つ以上のフィールドが含まれます。

たとえば、次の EXPLAIN コマンドが返す実行計画には、複数のフィールドを持つ *TableScan* という名前の演算子が含まれています。

```sql
EXPLAIN SELECT * FROM allemployees;

---
TableScan
├── table: default.default.allemployees
├── read rows: 5
├── read bytes: 592
├── partitions total: 5
├── partitions scanned: 5
└── push downs: [filters: [], limit: NONE]
```

{{{ .lake }}} を使用している場合は、Query Profile 機能を利用して SQL ステートメントの実行計画を可視化できます。

## Syntax {#syntax}

```sql
EXPLAIN <statement>
```

## Examples {#examples}

```sql
EXPLAIN select t.number from numbers(1) as t, numbers(1) as t1 where t.number = t1.number;
----
Project
├── columns: [number (#0)]
└── HashJoin
    ├── join type: INNER
    ├── build keys: [numbers.number (#1)]
    ├── probe keys: [numbers.number (#0)]
    ├── filters: []
    ├── TableScan(Build)
    │   ├── table: default.system.numbers
    │   ├── read rows: 1
    │   ├── read bytes: 8
    │   ├── partitions total: 1
    │   ├── partitions scanned: 1
    │   └── push downs: [filters: [], limit: NONE]
    └── TableScan(Probe)
        ├── table: default.system.numbers
        ├── read rows: 1
        ├── read bytes: 8
        ├── partitions total: 1
        ├── partitions scanned: 1
        └── push downs: [filters: [], limit: NONE]
```