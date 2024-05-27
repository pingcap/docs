---
title: TiDB Accelerated Table Creation
aliases: ['/tidb/stable/ddl-v2/']
summary: TiDB でテーブルを作成する場合のパフォーマンス最適化の概念、原則、実装の詳細を学習します。
---

# TiDB 高速テーブル作成 {#tidb-accelerated-table-creation}

TiDB v7.6.0 では、テーブル作成の高速化をサポートするシステム変数[`tidb_ddl_version`](https://docs.pingcap.com/tidb/v7.6/system-variables#tidb_enable_fast_create_table-new-in-v800)が導入され、バルク テーブル作成の効率が向上しました。v8.0.0 以降では、このシステム変数の名前は[`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)に変更されています。

TiDB は、オンライン非同期スキーマ変更アルゴリズムを使用してメタデータを変更します。すべての DDL ジョブは`mysql.tidb_ddl_job`テーブルに送信され、所有者ノードが DDL ジョブをプルして実行します。オンライン DDL アルゴリズムの各フェーズを実行した後、DDL ジョブは完了としてマークされ、 `mysql.tidb_ddl_history`テーブルに移動されます。したがって、DDL ステートメントは所有者ノードでのみ実行でき、線形に拡張することはできません。

ただし、一部の DDL ステートメントでは、オンライン DDL アルゴリズムに厳密に従う必要はありません。たとえば、 `CREATE TABLE`ステートメントでは、ジョブの状態は`none`と`public` 2 つだけです。そのため、TiDB は DDL の実行プロセスを簡素化し、テーブル作成を高速化するために、所有者以外のノードで`CREATE TABLE`ステートメントを実行します。

> **警告：**
>
> この機能は現在実験的機能であり、本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を上げてフィードバックをお寄せください。

## TiDBツールとの互換性 {#compatibility-with-tidb-tools}

-   [ティCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview) `tidb_enable_fast_create_table`によって作成されたテーブルの複製をサポートしていません。

## 制限 {#limitation}

パフォーマンスの最適化は、 [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)ステートメントでのみテーブル作成に使用できるようになりました。このステートメントには、外部キー制約を含めることはできません。

## テーブル作成を高速化するには、 <code>tidb_enable_fast_create_table</code>を使用します。 {#use-code-tidb-enable-fast-create-table-code-to-accelerate-table-creation}

システム変数[`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)の値を指定することにより、テーブル作成のパフォーマンス最適化を有効または無効にすることができます。

テーブル作成のパフォーマンス最適化を有効にするには、この変数の値を`ON`に設定します。

```sql
SET GLOBAL tidb_enable_fast_create_table = ON;
```

テーブル作成のパフォーマンス最適化を無効にするには、この変数の値を`OFF`に設定します。

```sql
SET GLOBAL tidb_enable_fast_create_table = OFF;
```

## 実施原則 {#implementation-principle}

テーブル作成のパフォーマンス最適化の詳細な実装原則は次のとおりです。

1.  `CREATE TABLE`ジョブを作成します。

    `CREATE TABLE`ステートメントを解析することによって、対応する DDL ジョブが生成されます。

2.  `CREATE TABLE`ジョブを実行します。

    `CREATE TABLE`ステートメントを受信した TiDB ノードはそれを直接実行し、テーブル構造を TiKV に永続化します。同時に、 `CREATE TABLE`ジョブは完了としてマークされ、 `mysql.tidb_ddl_history`テーブルに挿入されます。

3.  テーブル情報を同期します。

    TiDB は、新しく作成されたテーブル構造を同期するように他のノードに通知します。
