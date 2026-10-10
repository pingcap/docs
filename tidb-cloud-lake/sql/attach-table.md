---
title: ATTACH TABLE
summary: ATTACH TABLE は、既存のテーブルデータをコピーせずに読み取り専用リンクを作成します。
---

# ATTACH TABLE

ATTACH TABLE は、既存のテーブルデータをコピーせずに読み取り専用リンクを作成します。

## 主な機能 {#key-features}

- **ゼロコピーのデータアクセス**: 物理的なデータ移動なしでソースデータにリンクします
- **リアルタイム更新**: ソーステーブルの変更は、アタッチされたテーブルに即座に反映されます
- **読み取り専用モード**: SELECT クエリのみをサポートします（INSERT、UPDATE、DELETE 操作は不可）
- **カラムレベルアクセス**: セキュリティとパフォーマンスのために、特定のカラムのみを任意で含められます

## 構文 {#syntax}

```sql
ATTACH TABLE <target_table_name> [ ( <column_list> ) ] '<source_table_data_URI>'
CONNECTION = ( CONNECTION_NAME = '<connection_name>' )
```

### パラメータ {#parameters}

- **`<target_table_name>`**: 作成する新しいアタッチ済みテーブルの名前

- **`<column_list>`**: ソーステーブルから含めるカラムの任意のリスト
    - 省略した場合、すべてのカラムが含まれます
    - カラムレベルのセキュリティとアクセス制御を提供します
    - 例: `(customer_id, product, amount)`

- **`<source_table_data_URI>`**: オブジェクトストレージ内のソーステーブルデータへのパス
    - 形式: `s3://<bucket-name>/<database_ID>/<table_ID>/`
    - 例: `s3://lake-toronto/1/23351/`

- **`CONNECTION_NAME`**: [CREATE CONNECTION](/tidb-cloud-lake/sql/create-connection.md) で作成した接続を参照します

### ソーステーブルパスの見つけ方 {#finding-the-source-table-path}

データベース ID とテーブル ID を取得するには、[FUSE_SNAPSHOT](/tidb-cloud-lake/sql/fuse-snapshot.md) 関数を使用します。

```sql
SELECT snapshot_location FROM FUSE_SNAPSHOT('default', 'employees');
-- Result contains: 1/23351/_ss/... → Path is s3://your-bucket/1/23351/
```

## データ共有の利点 {#data-sharing-benefits}

### 仕組み {#how-it-works}

```
                Object Storage (S3, MinIO, Azure, etc.)
                         ┌─────────────┐
                         │ Source Data │
                         └──────┬──────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│ Marketing   │         │  Finance    │         │   Sales     │
│ Team View   │         │ Team View   │         │ Team View   │
└─────────────┘         └─────────────┘         └─────────────┘
```

### 主な利点 {#key-advantages}

| 従来のアプローチ | {{{ .lake }}} ATTACH TABLE |
|---------------------|----------------------|
| 複数のデータコピー | すべてで共有される単一コピー |
| ETL の遅延、同期の問題 | リアルタイムで常に最新 |
| 複雑なメンテナンス | メンテナンス不要 |
| コピーが増えるほどセキュリティリスクが増加 | きめ細かなカラムアクセス |
| データ移動により低速 | 元データに対する完全な最適化 |

### セキュリティとパフォーマンス {#security-and-performance}

- **カラムレベルのセキュリティ**: 各チームは必要なカラムのみを参照できます
- **リアルタイム更新**: ソースの変更は、すべてのアタッチ済みテーブルに即座に反映されます
- **強整合性**: 部分更新ではなく、常に完全なデータスナップショットを参照できます
- **フルパフォーマンス**: ソーステーブルのすべてのインデックスと最適化を継承します

## 例 {#examples}

### 基本的な使い方 {#basic-usage}

```sql
-- Step 1: Create a connection to your storage
CREATE CONNECTION my_s3_connection
    STORAGE_TYPE = 's3'
    ACCESS_KEY_ID = '<your_aws_key_id>'
    SECRET_ACCESS_KEY = '<your_aws_secret_key>';

-- Step 2: Attach a table with all columns
ATTACH TABLE population_all_columns 's3://lake-doc/1/16/'
    CONNECTION = (CONNECTION_NAME = 'my_s3_connection');
```

### セキュリティのためのカラム選択 {#column-selection-for-security}

```sql
-- Attach only specific columns for data security
ATTACH TABLE population_selected (city, population) 's3://lake-doc/1/16/'
    CONNECTION = (CONNECTION_NAME = 'my_s3_connection');
```

### IAM ロール認証の使用 {#using-iam-role-authentication}

```sql
-- Create a connection using IAM role (more secure than access keys)
CREATE CONNECTION s3_role_connection
    STORAGE_TYPE = 's3'
    ROLE_ARN = 'arn:aws:iam::123456789012:role/lake-role';

-- Attach table using the IAM role connection
ATTACH TABLE population_all_columns 's3://lake-doc/1/16/'
    CONNECTION = (CONNECTION_NAME = 's3_role_connection');
```

### チーム別ビュー {#team-specific-views}

```sql
-- Marketing: Customer behavior analysis
ATTACH TABLE marketing_view (customer_id, product, amount, order_date)
's3://your-bucket/1/23351/'
CONNECTION = (CONNECTION_NAME = 'my_s3_connection');

-- Finance: Revenue tracking (different columns)
ATTACH TABLE finance_view (order_id, amount, profit, order_date)
's3://your-bucket/1/23351/'
CONNECTION = (CONNECTION_NAME = 'my_s3_connection');
```