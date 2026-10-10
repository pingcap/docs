---
title: TiDB Cloud Lake のデータ共有の仕組み
summary: 異なるチームは、同じデータの異なる部分を必要とします。従来のソリューションではデータを何度もコピーする必要があり、コストが高く、管理も困難です。
---

# TiDB Cloud Lake のデータ共有の仕組み

## Data Sharing とは何ですか？ {#what-is-data-sharing}

異なるチームは、同じデータの異なる部分を必要とします。従来のソリューションではデータを何度もコピーする必要があり、コストが高く、管理も困難です。

{{{ .lake }}} の **[ATTACH TABLE](/tidb-cloud-lake/sql/attach-table.md)** は、この課題をスマートに解決します。データをコピーすることなく、同じデータに対して複数の「ビュー」を作成できます。これは {{{ .lake }}} の **真のコンピュートとストレージの分離** を活用したものです。クラウドストレージでもオンプレミスのオブジェクトストレージでも、**1 回保存すれば、どこからでもアクセス**できます。

ATTACH TABLE は、コンピューターのショートカットのようなものだと考えてください。元のファイルを複製せずに、そのファイルを参照します。

```
                Object Storage (S3, MinIO, Azure, etc.)
                         ┌─────────────┐
                         │ Your Data   │
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

## ATTACH TABLE の使い方 {#how-to-use-attach-table}

**Step 1: データの場所を確認する**

```sql
SELECT snapshot_location FROM FUSE_SNAPSHOT('default', 'company_sales');
-- Result: 1/23351/_ss/... → Data at s3://your-bucket/1/23351/
```

**Step 2: チームごとのビューを作成する**

```sql
-- Marketing: Customer behavior analysis
ATTACH TABLE marketing_view (customer_id, product, amount, order_date)
's3://your-bucket/1/23351/' CONNECTION = (ACCESS_KEY_ID = 'xxx', SECRET_ACCESS_KEY = 'yyy');

-- Finance: Revenue tracking
ATTACH TABLE finance_view (order_id, amount, profit, order_date)
's3://your-bucket/1/23351/' CONNECTION = (ACCESS_KEY_ID = 'xxx', SECRET_ACCESS_KEY = 'yyy');

-- HR: Employee info without salaries
ATTACH TABLE hr_employees (employee_id, name, department)
's3://data/1/23351/' CONNECTION = (...);

-- Development: Production structure without sensitive data
ATTACH TABLE dev_customers (customer_id, country, created_date)
's3://data/1/23351/' CONNECTION = (...);
```

**Step 3: それぞれ独立してクエリを実行する**

```sql
-- Marketing analyzes trends
SELECT product, COUNT(*) FROM marketing_view GROUP BY product;

-- Finance tracks profit
SELECT order_date, SUM(profit) FROM finance_view GROUP BY order_date;
```

## 主なメリット {#key-benefits}

**リアルタイム更新**: ソースデータが変更されると、接続されたすべてのテーブルに即座に反映されます

```sql
INSERT INTO company_sales VALUES (1001, 501, 'Laptop', 1299.99, 299.99, 'user@email.com', '2025-01-20');
SELECT COUNT(*) FROM marketing_view WHERE order_date = '2024-01-20'; -- Returns: 1
```

**カラムレベルのセキュリティ**: 各チームは必要な情報だけを参照できます。たとえば、Marketing は profit を参照できず、Finance は顧客のメールアドレスを参照できません

**強い整合性**: 部分的に更新されたデータを読むことはなく、常に完全なスナップショットを参照できます。財務レポートやコンプライアンスに最適です

**高いパフォーマンス**: すべてのインデックスが自動的に利用され、通常のテーブルと同じ速度で動作します

## これが重要な理由 {#why-this-matters}

| 従来のアプローチ | {{{ .lake }}} ATTACH TABLE |
|---------------------|----------------------|
| 複数のデータコピー | すべてで共有される単一コピー |
| ETL の遅延、同期の問題 | リアルタイムで常に最新 |
| 複雑な管理 | 管理不要 |
| コピーが増えるほどセキュリティリスクも増加 | きめ細かなカラムアクセス |
| データ移動により低速 | 元データに対する完全な最適化 |

## 内部での動作の仕組み {#how-it-works-under-the-hood}

```
Query: SELECT product, SUM(amount) FROM marketing_view GROUP BY product

┌─────────────────────────────────────────────────────────────────┐
│                    Query Execution Flow                         │
└─────────────────────────────────────────────────────────────────┘

    User Query
        │
        ▼
┌───────────────────┐    ┌─────────────────────────────────────┐
│ 1. Read Snapshot  │───►│ s3://bucket/1/23351/_ss/            │
│    Metadata       │    │ Get current table state             │
└───────────────────┘    └─────────────────────────────────────┘
        │
        ▼
┌───────────────────┐    ┌─────────────────────────────────────┐
│ 2. Apply Column   │───►│ Filter: customer_id, product,       │
│    Filter         │    │         amount, order_date          │
└───────────────────┘    └─────────────────────────────────────┘
        │
        ▼
┌───────────────────┐    ┌─────────────────────────────────────┐
│ 3. Check Stats &  │───►│ • Segment min/max values            │
│    Indexes        │    │ • Bloom filters                     │
└───────────────────┘    │ • Aggregate indexes                 │
        │                └─────────────────────────────────────┘
        ▼
┌───────────────────┐    ┌─────────────────────────────────────┐
│ 4. Smart Data     │───►│ Skip irrelevant blocks              │
│    Fetching       │    │ Download only needed data from _b/  │
└───────────────────┘    └─────────────────────────────────────┘
        │
        ▼
┌───────────────────┐    ┌─────────────────────────────────────┐
│ 5. Local          │───►│ Full optimization & parallelism     │
│    Execution      │    │ Process with all available indexes  │
└───────────────────┘    └─────────────────────────────────────┘
        │
        ▼
    Results: Product sales summary
```

複数の {{{ .lake }}} クラスターは、相互に調整することなくこのフローを同時に実行できます。これは、真のコンピュートとストレージの分離が実際に機能していることを示しています。

ATTACH TABLE は、根本的な発想の転換を表しています。つまり、**ユースケースごとにデータをコピーする方式から、1 つのコピーに対して多数のビューを持つ方式への転換**です。クラウド環境でもオンプレミス環境でも、{{{ .lake }}} のアーキテクチャにより、エンタープライズグレードの整合性とセキュリティを維持しながら、強力で効率的なデータ共有を実現できます。