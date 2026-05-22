---
title: TiDB Accelerated Table Creation
summary: TiDBでテーブルを作成する際のパフォーマンス最適化の概念、原則、および実装の詳細について学びます。
---

# TiDB高速テーブル作成 {#tidb-accelerated-table-creation}

TiDB v7.6.0 では、テーブル作成の高速化をサポートするシステム変数[`tidb_ddl_version`](https://docs-archive.pingcap.com/tidb/v7.6/system-variables/#tidb_ddl_version-new-in-v760)が導入され、一括テーブル作成の効率が向上しました。v8.0.0 以降、このシステム変数は[`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)に名称変更されました。

[`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)で高速テーブル作成を有効にすると、同じスキーマを持つテーブル作成ステートメントが同じ TiDB ノードに同時にコミットされた場合、テーブル作成パフォーマンスを向上させるために、バッチ テーブル作成ステートメントにマージされます。したがって、テーブル作成パフォーマンスを向上させるには、同じ TiDB ノードに接続し、同じスキーマを持つテーブルを並行して作成し、並行処理数を適切に増やすようにしてください。

マージされたバッチテーブル作成ステートメントは同じトランザクション内で実行されるため、いずれかのステートメントが失敗すると、すべてが失敗します。

## TiDBツールとの互換性 {#compatibility-with-tidb-tools}

-   TiDB v8.3.0より前のバージョンでは、 [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview) `tidb_enable_fast_create_table`によって作成されたテーブルのレプリケーションをサポートしていませんでした。v8.3.0以降では、TiCDCはこれらのテーブルを適切にレプリケーションできます。

## 制限 {#limitation}

テーブル作成時のパフォーマンス最適化は、 [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)文でのみ使用可能になりました。ただし、この文には外部キー制約を含めてはなりません。

## テーブル作成を高速化するには、 <code>tidb_enable_fast_create_table</code>使用してください。 {#use-code-tidb-enable-fast-create-table-code-to-accelerate-table-creation}

システム変数[`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)の値を指定することで、テーブル作成時のパフォーマンス最適化を有効または無効にすることができます。

TiDB v8.5.0以降、新しく作成されたクラスターでは、高速テーブル作成機能がデフォルトで有効になり、 `tidb_enable_fast_create_table`が`ON`に設定されます。v8.4.0以前のバージョンからアップグレードされたクラスターの場合、 `tidb_enable_fast_create_table`のデフォルト値は変更されません。

テーブル作成時のパフォーマンス最適化を有効にするには、この変数の値を`ON`に設定してください。

```sql
SET GLOBAL tidb_enable_fast_create_table = ON;
```

テーブル作成時のパフォーマンス最適化を無効にするには、この変数の値を`OFF`に設定してください。

```sql
SET GLOBAL tidb_enable_fast_create_table = OFF;
```
