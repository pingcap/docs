---
title: Worker の例
summary: "{{{ .lake }}} で UDF 実行環境を管理するために WORKER コマンドを使用する包括的な例。"
---

# Worker の例

> **Note:**
>
> v1.3.0 で導入されました。

このページでは、{{{ .lake }}} で UDF 実行環境を管理するために WORKER コマンドを使用する包括的な例を紹介します。

## 基本的な Worker ライフサイクル {#basic-worker-lifecycle}

### 1. Worker を作成する {#1-create-a-worker}

`read_env` という名前の UDF 用の基本的な worker を作成します。

```sql
CREATE WORKER read_env;
```

エラーを回避するために、`IF NOT EXISTS` を付けて worker を作成します。

```sql
CREATE WORKER IF NOT EXISTS read_env;
```

カスタム設定を指定して worker を作成します。

```sql
CREATE WORKER read_env
    WITH size = 'small',
         auto_suspend = '300',
         auto_resume = 'true',
         max_cluster_count = '3',
         min_cluster_count = '1';
```

### 2. Worker を一覧表示する {#2-list-workers}

現在のテナント内のすべての worker を表示します。

```sql
SHOW WORKERS;
```

### 3. Worker 設定を変更する {#3-modify-worker-settings}

worker のサイズと自動サスペンド設定を変更します。

```sql
ALTER WORKER read_env SET size = 'medium', auto_suspend = '600';
```

特定のオプションをデフォルト値にリセットします。

```sql
ALTER WORKER read_env UNSET size, auto_suspend;
```

### 4. Worker タグを管理する {#4-manage-worker-tags}

worker を分類するためのタグを追加します。

```sql
ALTER WORKER read_env SET TAG purpose = 'sandbox', owner = 'ci';
```

不要になったタグを削除します。

```sql
ALTER WORKER read_env UNSET TAG purpose, owner;
```

### 5. Worker の状態を制御する {#5-control-worker-state}

worker をサスペンドします（実行環境を停止します）。

```sql
ALTER WORKER read_env SUSPEND;
```

サスペンドされた worker を再開します。

```sql
ALTER WORKER read_env RESUME;
```

### 6. Worker を削除する {#6-remove-a-worker}

不要になった worker を削除します。

```sql
DROP WORKER read_env;
```

安全に worker を削除します（存在しない場合でもエラーになりません）。

```sql
DROP WORKER IF EXISTS read_env;
```

## 高度な例 {#advanced-examples}

### 異なる環境向けの Worker {#worker-for-different-environments}

環境ごとに異なる設定で worker を作成し、それぞれにタグを付けます。

```sql
-- Development worker
CREATE WORKER dev_processor WITH
    size = 'small',
    auto_suspend = '60',
    auto_resume = 'true',
    max_cluster_count = '1',
    min_cluster_count = '1';

ALTER WORKER dev_processor SET TAG environment = 'development', purpose = 'testing';

-- Production worker
CREATE WORKER prod_processor WITH
    size = 'large',
    auto_suspend = '1800',
    auto_resume = 'true',
    max_cluster_count = '5',
    min_cluster_count = '2';

ALTER WORKER prod_processor SET TAG environment = 'production', team = 'data-engineering';
```

### 動的な Worker 管理 {#dynamic-worker-management}

特定の設定を持つ worker が存在することを保証するスクリプトです。

```sql
-- Create worker if it doesn't exist
CREATE WORKER IF NOT EXISTS my_worker WITH
    size = 'small',
    auto_suspend = '300';

-- Update tags
ALTER WORKER my_worker SET TAG
    environment = 'staging',
    owner = 'ci';

-- Tune options later
ALTER WORKER my_worker SET auto_resume = 'true', max_cluster_count = '2';

-- Show current configuration
SHOW WORKERS;
```

## ベストプラクティス {#best-practices}

### 1. 命名規則 {#1-naming-conventions}

- UDF の用途が分かる説明的な名前を使用する
- 環境を表すサフィックスを含める（例: `_dev`、`_prod`、`_staging`）
- 複数チームの環境では、チーム名やプロジェクト名のプレフィックスを検討する

### 2. リソースサイズ設定 {#2-resource-sizing}

- 開発およびテストでは `size='small'` から始める
- 使用頻度の低い worker のコストを節約するために `auto_suspend` を使用する
- 想定されるロード (load) に基づいて適切な `min_cluster_count` を設定する

### 3. タグ戦略 {#3-tag-strategy}

- コスト配分とリソース追跡のためにタグを使用する
- 環境、チーム、プロジェクトの情報を含める
- 監査目的で作成日と所有者を追加する

### 4. ライフサイクル管理 {#4-lifecycle-management}

- 冪等なスクリプトのために `IF NOT EXISTS` と `IF EXISTS` を使用する
- `SHOW WORKERS` で worker の使用状況を監視する
- コスト削減のために未使用の worker をクリーンアップする

## 一般的なユースケース {#common-use-cases}

### 1. UDF 開発 {#1-udf-development}

```sql
-- Create a worker for UDF development
CREATE WORKER dev_transform WITH
    size = 'small',
    auto_suspend = '60';

ALTER WORKER dev_transform SET TAG environment = 'development', purpose = 'testing';

-- After UDF is developed and tested
ALTER WORKER dev_transform SET
    size = 'medium',
    auto_suspend = '300';

ALTER WORKER dev_transform SET TAG purpose = 'production-ready';
```

### 2. バッチ処理 {#2-batch-processing}

```sql
-- Worker for nightly batch jobs
CREATE WORKER nightly_etl WITH
    size = 'large',
    auto_suspend = '3600',  -- Suspend after 1 hour of inactivity
    auto_resume = 'false';  -- Don't auto-resume (manual control)

ALTER WORKER nightly_etl SET TAG
    schedule = 'nightly',
    job_type = 'etl',
    criticality = 'high';
```

### 3. マルチテナント環境 {#3-multi-tenant-environments}

```sql
-- Workers for different teams
CREATE WORKER team_a_processor WITH
    size = 'medium';

ALTER WORKER team_a_processor SET TAG team = 'team-a', billing_code = 'TA-2024';

CREATE WORKER team_b_processor WITH
    size = 'small';

ALTER WORKER team_b_processor SET TAG team = 'team-b', billing_code = 'TB-2024';
```

## トラブルシューティング {#troubleshooting}

### Worker が起動しない {#worker-not-starting}

Worker が想定どおりに起動しない場合は、次の点を確認してください。

1. UDF が存在し、適切に設定されているか確認する
2. 環境変数がクラウドコンソールで設定されていることを確認する
3. 現在の Worker メタデータを確認し、必要に応じて再開する

```sql
-- Inspect current worker metadata
SHOW WORKERS;

-- Resume the worker
ALTER WORKER my_worker RESUME;
```

### 権限の問題 {#permission-issues}

必要な権限があることを確認してください。

```sql
-- Check your privileges
SHOW GRANTS;
```

### リソース制約 {#resource-constraints}

パフォーマンスの問題が発生している場合は、次を試してください。

```sql
-- Increase worker size
ALTER WORKER my_worker SET size = 'large';

-- Adjust cluster counts
ALTER WORKER my_worker SET
    max_cluster_count = '5',
    min_cluster_count = '2';
```

## 関連トピック {#related-topics}

- [ユーザー定義関数 (UDF)](/tidb-cloud-lake/sql/user-defined-function.md) - UDF の作成方法と使用方法について説明します
- [Warehouse 管理](/tidb-cloud-lake/sql/warehouse-overview.md) - クエリ実行用のコンピュートリソースを管理します
- [Workload Groups](/tidb-cloud-lake/sql/workload-group.md) - リソース割り当てと優先度を制御します