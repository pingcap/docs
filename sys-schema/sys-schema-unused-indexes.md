---
title: schema_unused_indexes
summary: sys スキーマの `schema_unused_indexes` テーブルについて学習します。
---

# <code>schema_unused_indexes</code> {#code-schema-unused-indexes-code}

`schema_unused_indexes` 、TiDB の最後の起動以降に使用されていないインデックスを記録します。次の列が含まれます。

-   `OBJECT_SCHEMA` : インデックスを含むテーブルが属するデータベースの名前。
-   `OBJECT_NAME` : インデックスを含むテーブルの名前。
-   `INDEX_NAME` : インデックスの名前。

```sql
USE SYS;
DESC SCHEMA_UNUSED_INDEXES;
```

出力は次のようになります。

```sql
+---------------+-------------+------+------+---------+-------+
| Field         | Type        | Null | Key  | Default | Extra |
+---------------+-------------+------+------+---------+-------+
| object_schema | varchar(64) | YES  |      | NULL    |       |
| object_name   | varchar(64) | YES  |      | NULL    |       |
| index_name    | varchar(64) | YES  |      | NULL    |       |
+---------------+-------------+------+------+---------+-------+
3 rows in set (0.00 sec)
```

## <code>schema_unused_indexes</code>ビューを手動で作成する {#manually-create-the-code-schema-unused-indexes-code-view}

v8.0.0 より前のバージョンからアップグレードされたクラスターの場合、 `sys`スキーマとその中のビューは自動的に作成されません。次の SQL ステートメントを使用して手動で作成できます。

```sql
CREATE DATABASE IF NOT EXISTS sys;
CREATE OR REPLACE VIEW sys.schema_unused_indexes AS
  SELECT
    table_schema as object_schema,
    table_name as object_name,
    index_name
  FROM information_schema.cluster_tidb_index_usage
  WHERE
    table_schema not in ('sys', 'mysql', 'INFORMATION_SCHEMA', 'PERFORMANCE_SCHEMA') and
    index_name != 'PRIMARY'
  GROUP BY table_schema, table_name, index_name
  HAVING
    sum(last_access_time) is null;
```

## 続きを読む {#read-more}

-   [`INFORMATION_SCHEMA.TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md)
