---
title: TiDB Accelerated Table Creation
summary: TiDB でテーブルを作成する場合のパフォーマンス最適化の概念、原則、実装の詳細を学習します。
---

# TiDB 高速テーブル作成 {#tidb-accelerated-table-creation}

TiDB v7.6.0では、テーブル作成の高速化をサポートするシステム変数[`tidb_ddl_version`](https://docs.pingcap.com/tidb/v7.6/system-variables#tidb_enable_fast_create_table-new-in-v800)が導入され、バルクテーブル作成の効率が向上しました。v8.0.0以降、このシステム変数の名前は[`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)に変更されます。

[`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)で高速テーブル作成を有効にすると、同じTiDBノードに同時にコミットされた同一スキーマのテーブル作成文がバッチテーブル作成文にマージされ、テーブル作成パフォーマンスが向上します。したがって、テーブル作成パフォーマンスを向上させるには、同じTiDBノードに接続し、同一スキーマのテーブルを同時に作成し、同時実行性を適切に高めるようにしてください。

マージされたバッチ テーブル作成ステートメントは同じトランザクション内で実行されるため、そのうちの 1 つのステートメントが失敗すると、すべてが失敗します。

## TiDBツールとの互換性 {#compatibility-with-tidb-tools}

-   TiDB v8.3.0より前のバージョンでは、 [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview) `tidb_enable_fast_create_table`で作成されたテーブルのレプリケーションをサポートしていません。v8.3.0以降、TiCDCはこれらのテーブルを適切にレプリケーションできます。

## 制限 {#limitation}

[`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)のステートメントでのみテーブル作成のパフォーマンス最適化を使用できるようになりました。このステートメントには外部キー制約を含めることはできません。

## <code>tidb_enable_fast_create_table</code>を使用してテーブル作成を高速化します {#use-code-tidb-enable-fast-create-table-code-to-accelerate-table-creation}

システム変数[`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)の値を指定することにより、テーブル作成のパフォーマンス最適化を有効または無効にすることができます。

TiDB v8.5.0以降、新規作成されたクラスターでは高速テーブル作成機能がデフォルトで有効になり、 `tidb_enable_fast_create_table`が`ON`に設定されます。v8.4.0以前のバージョンからアップグレードされたクラスターでは、デフォルト値の`tidb_enable_fast_create_table`は変更されません。

テーブル作成のパフォーマンス最適化を有効にするには、この変数の値を`ON`に設定します。

```sql
SET GLOBAL tidb_enable_fast_create_table = ON;
```

テーブル作成のパフォーマンス最適化を無効にするには、この変数の値を`OFF`に設定します。

```sql
SET GLOBAL tidb_enable_fast_create_table = OFF;
```
