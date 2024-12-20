---
title: TiDB Accelerated Table Creation
summary: TiDB でテーブルを作成する場合のパフォーマンス最適化の概念、原則、実装の詳細を学習します。
---

# TiDB 高速テーブル作成 {#tidb-accelerated-table-creation}

TiDB v7.6.0 では、テーブル作成の高速化をサポートするシステム変数[`tidb_ddl_version`](https://docs.pingcap.com/tidb/v7.6/system-variables#tidb_enable_fast_create_table-new-in-v800)が導入され、バルク テーブル作成の効率が向上しました。v8.0.0 以降では、このシステム変数の名前が[`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)に変更されています。

[`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)で高速テーブル作成を有効にすると、同じ TiDB ノードに同時にコミットされた同じスキーマのテーブル作成ステートメントがバッチ テーブル作成ステートメントにマージされ、テーブル作成のパフォーマンスが向上します。したがって、テーブル作成のパフォーマンスを向上させるには、同じ TiDB ノードに接続し、同じスキーマのテーブルを同時に作成し、同時実行性を適切に高めるようにしてください。

マージされたバッチ テーブル作成ステートメントは同じトランザクション内で実行されるため、そのうちの 1 つのステートメントが失敗すると、すべてが失敗します。

## TiDBツールとの互換性 {#compatibility-with-tidb-tools}

-   TiDB v8.3.0 より前では、 [ティCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview) `tidb_enable_fast_create_table`によって作成されたテーブルの複製をサポートしていません。v8.3.0 以降では、 TiCDC はこれらのテーブルを適切に複製できます。

## 制限 {#limitation}

パフォーマンス最適化は、 [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)ステートメントでのみテーブル作成に使用できるようになり、このステートメントには外部キー制約を含めることはできません。

## テーブル作成を高速化するには、 <code>tidb_enable_fast_create_table</code>を使用します。 {#use-code-tidb-enable-fast-create-table-code-to-accelerate-table-creation}

システム変数[`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)の値を指定することにより、テーブル作成のパフォーマンス最適化を有効または無効にすることができます。

TiDB v8.5.0 以降では、新しく作成されたクラスターに対して高速テーブル作成機能がデフォルトで有効になっており、 `tidb_enable_fast_create_table`が`ON`に設定されています。v8.4.0 以前のバージョンからアップグレードされたクラスターの場合、デフォルト値の`tidb_enable_fast_create_table`は変更されません。

テーブル作成のパフォーマンス最適化を有効にするには、この変数の値を`ON`に設定します。

```sql
SET GLOBAL tidb_enable_fast_create_table = ON;
```

テーブル作成のパフォーマンス最適化を無効にするには、この変数の値を`OFF`に設定します。

```sql
SET GLOBAL tidb_enable_fast_create_table = OFF;
```
