---
title: マテリアライズドビュー
summary: マテリアライズドビューは、クエリ結果を物理的に保存するビューです。TiDB Cloud Lake は、マテリアライズドビューの作成時にソーステーブルの変更追跡を有効にします。
---

# マテリアライズドビュー

マテリアライズドビューは、クエリ結果を物理的に保存するビューです。これは、`default` catalog 内の 1 つの永続的な FUSE テーブル上に定義されます。{{{ .lake }}} は、マテリアライズドビューの作成時にソーステーブルの変更追跡を有効にします。

論理ビューとは異なり、マテリアライズドビューは明示的に refresh して、ソーステーブルからの変更を永続化できます。物理ストレージがソーステーブルに遅れている場合でも、読み取りの一貫性は保たれます。最初の refresh の前に、{{{ .lake }}} はソースに対して定義を評価します。未 refresh のソース変更がある場合、{{{ .lake }}} は **read fix** を使用します。つまり、読み取り時に永続化されたマテリアライズドビューのデータと必要な増分ソースデータを union し（その増分にもビュー定義を適用し）、結果を返します。そのため、クエリは古いマテリアライズドデータではなく、最新の結果を返します。

## 制限事項 {#limitations}

- 定義は、厳密に 1 つのベーステーブルに対する単純な `SELECT ... FROM ... [WHERE ...] [GROUP BY ...]` クエリである必要があります。テーブル結合、サブクエリ、集合演算、および非決定的 関数 はサポートされていません。
- 集計 は `sum`、`min`、`max`、`avg`、`count`、`approx_count_distinct` のみサポートされます。`DISTINCT`、`FILTER`、window、および ordered aggregate 形式はサポートされていません。
- ソースは、`default` catalog 内の永続的な FUSE ベーステーブルである必要があります。マテリアライズドビューは、別のビューや異なるテーブルエンジンをソースとして使用できません。
- マテリアライズドビューは読み取り専用です。内容を 管理 するには `REFRESH MATERIALIZED VIEW` を使用します。`INSERT`、`UPDATE`、`DELETE`、`TRUNCATE`、および通常の `ALTER TABLE` 操作はサポートされていません。

## マテリアライズドビューを作成する {#create-a-materialized-view}

```sql
CREATE [ OR REPLACE ] MATERIALIZED VIEW [ IF NOT EXISTS ]
  [ <catalog_name>. ][ <database_name>. ]<view_name>
  [ ( <column_name>, ... ) ]
  [ CLUSTER BY ( <expr>, ... ) ]
  [ COMMENT = '<comment>' ]
  [ <fuse_table_option> = <value> ... ]
AS <query>
```

`CLUSTER BY` では明示的なカラムリストが必要で、非集計の出力カラムまたは `GROUP BY` キーを参照できます。オプションの Fuse テーブルオプションは物理ストレージレイアウトを制御します。サポートされるオプションについては、[CREATE TABLE](/tidb-cloud-lake/sql/create-table.md) を参照してください。

作成時には定義が記録されますが、物理ストレージは同期的には投入されません。初期データをマテリアライズするには、`REFRESH MATERIALIZED VIEW` を実行してください。

```sql
CREATE TABLE orders (
  order_id INT,
  customer_id INT,
  amount DECIMAL(10, 2),
  paid BOOLEAN
);

CREATE MATERIALIZED VIEW paid_orders_by_customer
  (customer_id, total_amount, order_count)
  CLUSTER BY (customer_id)
  COMMENT = 'Paid-order totals by customer'
AS
SELECT customer_id, sum(amount), count(*)
FROM orders
WHERE paid
GROUP BY customer_id;

REFRESH MATERIALIZED VIEW paid_orders_by_customer;
```

`CREATE OR REPLACE` は既存のマテリアライズドビューを置き換えます。`IF NOT EXISTS` は、名前がすでに存在する場合は何も行いません。

## マテリアライズドビューを refresh する {#refresh-a-materialized-view}

```sql
REFRESH MATERIALIZED VIEW [ <catalog_name>. ][ <database_name>. ]<view_name>
```

最初の refresh ではソースデータがマテリアライズされます。以降の refresh では、append-only の変更が増分的に処理されます。ソースに `UPDATE`、`DELETE`、または `TRUNCATE` の変更がある場合、{{{ .lake }}} は現在のソース状態からマテリアライズドビューを再構築し、結果の正しさを保ちます。

## 物理レイアウトを変更する {#change-physical-layout}

サポートされる 管理 操作には、専用の `ALTER MATERIALIZED VIEW` 構文を使用します。

```sql
ALTER MATERIALIZED VIEW <view_name> CLUSTER BY ( <expr>, ... );
ALTER MATERIALIZED VIEW <view_name> DROP CLUSTER KEY;
ALTER MATERIALIZED VIEW <view_name> RECLUSTER [ FINAL ] [ LIMIT <n> ];
ALTER MATERIALIZED VIEW <view_name> SET OPTIONS ( <option> = <value>, ... );
ALTER MATERIALIZED VIEW <view_name> UNSET OPTIONS ( <option>, ... );
ALTER MATERIALIZED VIEW <view_name> COMMENT = '<comment>';
```

たとえば、refresh の前にレイアウトオプションを設定できます。

```sql
ALTER MATERIALIZED VIEW paid_orders_by_customer SET OPTIONS (row_per_block = 2);
REFRESH MATERIALIZED VIEW paid_orders_by_customer;
```

マテリアライズドビューでは `RECLUSTER WHERE` はサポートされていません。定義を変更するには `CREATE OR REPLACE MATERIALIZED VIEW` を使用してください。`ALTER VIEW` は適用されません。

## 定義を表示および削除する {#view-and-remove-definitions}

```sql
SHOW MATERIALIZED VIEWS
  [ { FROM | IN } <database_name> ]
  [ LIKE '<pattern>' | WHERE <expr> ];

SHOW CREATE MATERIALIZED VIEW
  [ <catalog_name>. ][ <database_name>. ]<view_name>;

DROP MATERIALIZED VIEW [ IF EXISTS ]
  [ <catalog_name>. ][ <database_name>. ]<view_name>;
```

```sql
SHOW MATERIALIZED VIEWS LIKE 'paid_orders%';
SHOW CREATE MATERIALIZED VIEW paid_orders_by_customer;
DROP MATERIALIZED VIEW IF EXISTS paid_orders_by_customer;
```

## アクセス制御要件 {#access-control-requirements}

マテリアライズドビューに対して query、refresh、alter、show、または drop を行うには、ユーザーはそのソーステーブルに対する `SELECT` 権限（または同等のアクセスを提供する所有権）を持っている必要があります。権限は現在のソーステーブル ID に対してチェックされるため、ソーステーブルの rename を行ってもこの要件は変わりません。