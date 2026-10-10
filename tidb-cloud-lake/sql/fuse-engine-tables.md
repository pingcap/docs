---
title: Fuse Engine Tables
summary: "{{{ .lake }}} はデフォルトのストレージエンジンとして Fuse Engine を使用し、Git のようなデータ管理システムを提供します。"
---

# Fuse Engine Tables

## 概要 {#overview}

{{{ .lake }}} はデフォルトのストレージエンジンとして Fuse Engine を使用し、以下の機能を備えた Git のようなデータ管理システムを提供します。

- **スナップショットベースのアーキテクチャ**: 任意の時点のデータをクエリおよび復元でき、リカバリのためにデータ変更履歴を保持します
- **高パフォーマンス**: 自動インデックス作成とブルームフィルターにより分析ワークロード向けに最適化されています
- **効率的なストレージ**: 高圧縮の Parquet 形式を使用し、最適なストレージ効率を実現します
- **柔軟な設定**: 圧縮、インデックス作成、ストレージオプションをカスタマイズできます
- **データメンテナンス**: 自動データ保持、スナップショット管理、変更追跡機能を備えています

## Fuse Engine を使用する場合 {#when-to-use-fuse-engine}

以下の用途に適しています。

- **分析**: カラムナストレージによる OLAP クエリ
- **データウェアハウジング**: 大量の履歴データ
- **タイムトラベル**: 過去のデータバージョンへのアクセス
- **クラウドストレージ**: オブジェクトストレージ向けに最適化

## 構文 {#syntax}

```sql
CREATE TABLE <table_name> (
  <column_definitions>
) [ENGINE = FUSE]
[CLUSTER BY (<expr> [, <expr>, ...] )]
[<Options>];
```

`CREATE TABLE` 構文の詳細については、[CREATE TABLE](/tidb-cloud-lake/sql/create-table.md) を参照してください。

## パラメータ {#parameters}

以下は、Fuse Engine テーブルを作成する際の主なパラメータです。

### `ENGINE` {#engine}

**説明:** エンジンを明示的に指定しない場合、{{{ .lake }}} は自動的に Fuse Engine を使用してテーブルを作成します。これは `ENGINE = FUSE` と同等です。

### `CLUSTER BY` {#cluster-by}

**説明:** 複数の式で構成されるデータのソート方法を指定します。詳細については、[クラスターキー](/tidb-cloud-lake/sql/cluster-key.md) を参照してください。

### `<Options>`

**説明:** Fuse Engine は、テーブルのプロパティをカスタマイズできるさまざまなオプション（大文字小文字を区別しない）を提供します。

- 詳細は [Fuse Engine オプション](#fuse-engine-options) を参照してください。
- 複数のオプションはスペースで区切ります。
- テーブルのオプションを変更するには [ALTER TABLE](/tidb-cloud-lake/sql/alter-table.md#fuse-engine-options) を使用します。
- テーブルのオプションを表示するには [SHOW CREATE TABLE](/tidb-cloud-lake/sql/show-create-table.md) を使用します。

## Fuse Engine オプション {#fuse-engine-options}

以下は、用途別に分類した利用可能な Fuse Engine オプションです。

### `compression` {#compression}

- **構文:** `compression = '<compression>'`
- **説明:** エンジンの圧縮方式を指定します。圧縮オプションには lz4、zstd、snappy、none があります。圧縮方式のデフォルトは、オブジェクトストレージでは zstd、ファイルシステム (fs) ストレージでは lz4 です。

### `snapshot_loc` {#snapshot-loc}

- **構文:** `snapshot_loc = '<snapshot_loc>'`
- **説明:** 文字列形式の location パラメータを指定し、データをコピーせずにテーブルを簡単に共有できるようにします。

### `block_size_threshold` {#block-size-threshold}

- **構文:** `block_size_threshold = <n>`
- **説明:** 最大ブロックサイズをバイト単位で指定します。デフォルトは 104,857,600 バイトです。

### `block_per_segment` {#block-per-segment}

- **構文:** `block_per_segment = <n>`
- **説明:** セグメント内の最大ブロック数を指定します。デフォルトは 1,000 です。

### `row_per_block` {#row-per-block}

- **構文:** `row_per_block = <n>`
- **説明:** ファイル内の最大行数を指定します。デフォルトは 1,000,000 です。

### `bloom_index_columns` {#bloom-index-columns}

- **構文:** `bloom_index_columns = '<column> [, <column> ...]'`
- **説明:** ブルームインデックスに使用するカラムを指定します。これらのカラムのデータ型には、Map、Number、String、Date、Timestamp を使用できます。特定のカラムを指定しない場合、ブルームインデックスはデフォルトですべてのサポート対象カラムに作成されます。`bloom_index_columns=''` を指定すると、ブルームインデックス作成は無効になります。

### `bloom_index_type` {#bloom-index-type}

- **構文:** `bloom_index_type = 'xor8' | 'binary_fuse32'`
- **説明:** ブルームインデックスに使用するフィルターアルゴリズムを指定します。デフォルトは `xor8` です。ポイントルックアップの負荷が高いテーブルでは `binary_fuse32` を使用してください。インデックスサイズが大きくなる（`xor8` の約 4 倍）代わりに、偽陽性率が低くなります。

    `ALTER TABLE ... SET OPTIONS(bloom_index_type = ...)` は、新しい書き込みと再構築されたブルームインデックスにのみ影響する点に注意してください。既存の `xor8` インデックスファイルと新しい `binary_fuse32` インデックスファイルは、同じテーブル内に共存できます。

    **例:**

    ```sql
    -- Set bloom_index_type at table creation
    CREATE TABLE t (a INT) bloom_index_type = 'binary_fuse32';

    -- Change bloom_index_type for an existing table (affects new writes only)
    ALTER TABLE t SET OPTIONS(bloom_index_type = 'binary_fuse32');

    -- Revert to xor8
    ALTER TABLE t SET OPTIONS(bloom_index_type = 'xor8');
    ```

### `change_tracking` {#change-tracking}

- **構文:** `change_tracking = True / False`
- **説明:** Fuse Engine でこのオプションを `True` に設定すると、テーブルの変更を追跡できます。テーブルに対して stream を作成すると、自動的に `change_tracking` が `True` に設定され、変更追跡メタデータとして追加の隠しカラムがテーブルに導入されます。詳細については、[How Stream Works](/tidb-cloud-lake/guides/track-and-transform-data-via-streams.md) を参照してください。

### `data_retention_period_in_hours` {#data-retention-period-in-hours}

- **構文:** `data_retention_period_in_hours = <n>`
- **説明:** テーブルデータを保持する時間数を指定します。最小値は 1 時間です。最大値は {{{ .lake }}} のサービス設定によって決まり、指定されていない場合のデフォルトは 2,160 時間（90 日 x 24 時間）です。

### `enable_auto_vacuum` {#enable-auto-vacuum}

- **構文:** `enable_auto_vacuum = 0 / 1`
- **説明:** 変更操作中にテーブルが自動的に vacuum 操作をトリガーするかどうかを制御します。これは、すべてのテーブルに対する設定としてグローバルに設定することも、テーブルレベルで設定することもできます。テーブルレベルのオプションは、同名の session/global 設定よりも優先されます。有効化されている場合（1 に設定）、INSERT や ALTER TABLE などの変更操作の後に vacuum 操作が自動的にトリガーされ、設定された保持ポリシーに従ってテーブルデータがクリーンアップされます。

**例:**

```sql
-- Set enable_auto_vacuum globally for all tables across all sessions
SET GLOBAL enable_auto_vacuum = 1;

-- Create a table with auto vacuum disabled (overrides global setting)
CREATE OR REPLACE TABLE t1 (id INT) ENABLE_AUTO_VACUUM = 0;
INSERT INTO t1 VALUES(1); -- Won't trigger vacuum despite global setting

-- Create another table that inherits the global setting
CREATE OR REPLACE TABLE t2 (id INT);
INSERT INTO t2 VALUES(1); -- Will trigger vacuum due to global setting

-- Enable auto vacuum for an existing table
ALTER TABLE t1 SET OPTIONS(ENABLE_AUTO_VACUUM = 1);
INSERT INTO t1 VALUES(2); -- Now will trigger vacuum

-- Table option takes precedence over global settings
SET GLOBAL enable_auto_vacuum = 0; -- Turn off globally
-- t1 will still vacuum because table setting overrides global
INSERT INTO t1 VALUES(3); -- Will still trigger vacuum
INSERT INTO t2 VALUES(2); -- Won't trigger vacuum anymore
```

### `data_retention_num_snapshots_to_keep` {#data-retention-num-snapshots-to-keep}

- **構文:** `data_retention_num_snapshots_to_keep = <n>`
- **説明:** vacuum 操作中に保持するスナップショット数を指定します。これは、すべてのテーブルに対する設定としてグローバルに設定することも、テーブルレベルで設定することもできます。テーブルレベルのオプションは、同名の session/global 設定よりも優先されます。設定すると、vacuum 操作後は指定した数の最新スナップショットのみが保持されます。`data_retention_time_in_days` 設定を上書きします。0 に設定した場合、この設定は無視されます。このオプションは `enable_auto_vacuum` 設定と組み合わせて機能し、スナップショット保持ポリシーをきめ細かく制御できます。

**例:**

```sql
-- Set global retention to 10 snapshots for all tables across all sessions
SET GLOBAL data_retention_num_snapshots_to_keep = 10;

-- Create a table with custom snapshot retention (overrides global setting)
CREATE OR REPLACE TABLE t1 (id INT)
  enable_auto_vacuum = 1
  data_retention_num_snapshots_to_keep = 5;

-- Create another table that inherits the global setting
CREATE OR REPLACE TABLE t2 (id INT) enable_auto_vacuum = 1;

-- When vacuum is triggered:
-- t1 will keep 5 snapshots (table setting)
-- t2 will keep 10 snapshots (global setting)

-- Change global setting
SET GLOBAL data_retention_num_snapshots_to_keep = 20;

-- Table options still take precedence:
-- t1 will still keep only 5 snapshots
-- t2 will now keep 20 snapshots

-- Modify snapshot retention for an existing table
ALTER TABLE t1 SET OPTIONS(data_retention_num_snapshots_to_keep = 3);
-- Now t1 will keep 3 snapshots when vacuum is triggered
```

### `enable_schema_evolution` {#enable-schema-evolution}

- **構文:**

    `enable_schema_evolution = True / False`

- **説明:**

    `COPY INTO` 操作中にテーブルスキーマを自動的に Schema Evolution できるかどうかを制御します。有効化すると（`True` に設定）、{{{ .lake }}} は、スキーマに宛先テーブルに存在しないカラムを含む Parquet ファイルをロード (load) する際に、不足しているカラムをテーブルに自動的に追加します。既存の行に対する不足値は `NULL` で埋められます。詳細は、[Schema Evolution](/tidb-cloud-lake/guides/schema-evolution.md) を参照してください。

**例:**

```sql
-- Enable schema evolution for an existing table
ALTER TABLE invoices SET OPTIONS(ENABLE_SCHEMA_EVOLUTION = true);

-- Create a new table with schema evolution enabled
CREATE OR REPLACE TABLE invoices (order_id INT) ENABLE_SCHEMA_EVOLUTION = true;
```