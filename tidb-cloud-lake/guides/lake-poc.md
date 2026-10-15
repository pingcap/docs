---
title: TiDB Cloud Lake 概念验证（PoC）指南
summary: 使用 schema 映射、cluster key、reclustering、块大小和物化视图，通过具有代表性的工作负载评估 TiDB Cloud Lake。
---

# TiDB Cloud Lake 概念验证（PoC）指南

本文档介绍了一个可重复执行的 TiDB Cloud Lake 概念验证（PoC）流程，并以将数据从 TiDB Cloud Premium 实例复制到 TiDB Cloud Lake 为主要示例。本文重点关注对代表性工作负载影响最大的决策：对象存储和 PrivateLink 连接、schema 兼容性、数据布局、重叠维护、块大小以及预聚合。

请使用具有代表性的数据样本以及生产环境中使用的查询模式来执行 PoC。记录查询延时、QPS、计算集群大小和存储大小，以便你能够基于相同的基线比较每项优化的效果。

## Step 1. 配置 S3 连接 {#step-1-configure-an-s3-connection}

当源端管道已经将 Parquet、CSV 或 JSON 对象写入对象存储时，请使用 S3 存储桶。在 **Home > Connect** 中，获取你的 TiDB Cloud Lake 部署的 IAM role ARN，并按照 [使用 AWS IAM Role 进行认证](/tidb-cloud-lake/guides/authenticate-with-aws-iam-role.md) 配置 S3 连接、stage 和数据加载。

## Step 2. 配置 PrivateLink {#step-2-configure-privatelink}

当流量必须保持在私有网络路径中时，请使用 PrivateLink。在 **Home > Connect** 中，获取 PrivateLink 服务，并按照 [通过 AWS PrivateLink 连接](/tidb-cloud-lake/guides/connect-with-aws-privatelink.md) 配置连接。在开始加载之前，请先从客户端或源集群验证 endpoint、安全组规则、DNS 行为以及路由。

## Step 3. 使用 Data Pipeline 将数据从 TiDB Cloud Premium 实例复制到 TiDB Cloud Lake {#step-3-use-data-pipeline-to-replicate-data-from-a-tidb-cloud-premium-instance-to-tidb-cloud-lake}

使用 TiDB Cloud Data Pipeline 可以将数据从 TiDB Cloud Premium 实例复制到 TiDB Cloud Lake，而无需引入第三方 ETL 工具。Data Pipeline 会先导出所选源数据的完整快照，然后持续复制行级变更，从而使 TiDB Cloud Lake 中的数据保持最新。

Data Pipeline 使用 TiCDC 进行增量复制，并通过外部 stage 在 TiDB Cloud 与 TiDB Cloud Lake 之间传输数据。在开始 PoC 之前，请验证你的 TiDB Cloud 套餐是否提供所需功能，并确认外部 stage 和访问策略已完成配置。有关当前可用性和配置要求，请参见 [Data Pipeline to TiDB Cloud Lake](https://docs.pingcap.com/tidbcloud/data-pipeline-sink-to-lake/)。

对于 PoC，请选择具有代表性的表，并记录其 schema、预期行数以及数据新鲜度目标。初始快照完成后，将行数、空值计数、样本聚合结果以及最小值和最大值与源端进行比较。然后，在源端生成具有代表性的插入、修改和删除操作，并验证 TiDB Cloud Lake 是否能在预期的复制延时内反映这些变更。在使用复制后的表进行查询性能测试之前，请记录快照持续时间、复制延迟、被拒绝的记录以及 schema 映射错误。

### 映射并验证源 schema {#map-and-validate-the-source-schema}

在加载文件或启动复制之前，请记录每个源列及其对应的目标 Lake 列、数据类型、可空性、默认值以及所需的任何转换。检查 decimal 精度和 scale、有符号与无符号整数范围、时间戳精度和时区，以及字符串编码。使用 [Lake 数据类型参考](/tidb-cloud-lake/sql/data-types.md) 选择目标类型；不要假设名称相同的类型具有完全相同的语义。

加载一个包含空值和边界值的小样本。将行数、空值计数、最小值和最大值以及聚合结果，与源端在相同快照或复制 checkpoint 下的数据进行比较。验证转换是否保留了精度和时间戳语义，并在开始完整加载之前调查被拒绝或被截断的值。

## Step 4. 建立性能基线 {#step-4-establish-the-performance-baseline}

影响 Lake 查询性能的主要因素包括：

1. **计算集群资源。** CPU、内存、计算集群大小和并发限制决定了同时可以运行多少工作。
2. **数据布局。** cluster key 顺序、块重叠和块大小决定了可以裁剪掉多少数据。
3. **查询模式。** 仅投影所需列，并尽可能让选择性谓词包含 cluster key 的前导列。

为每个基线查询捕获 `EXPLAIN` 输出。如果 `TableScan` 占主导，请在提高并发之前先检查 cluster key 裁剪、重叠指标、块大小、缓存命中率和计算集群容量。

## Step 5. 当工作负载能从中受益时选择 cluster key {#step-5-choose-a-cluster-key-when-the-workload-benefits}

在创建具有可预测过滤条件或范围扫描的大表时，请评估是否使用 cluster key。对于小表、随机访问模式以及频繁变更的场景，其收益可能不足以抵消维护成本。请选择经常出现在过滤、连接或范围扫描中的列，并将最常用于过滤的列放在前面。保持 key 表达式尽量简洁；对于较长的字符串，请使用有界前缀表达式。

```sql
CREATE TABLE lineitem (
  l_orderkey BIGINT NOT NULL,
  l_partkey INT NOT NULL,
  l_shipdate DATE NOT NULL,
  l_quantity DECIMAL(15, 2) NOT NULL,
  l_extendedprice DECIMAL(15, 2) NOT NULL
)
ENGINE = FUSE
CLUSTER BY (DATE_TRUNC(MONTH, l_shipdate), l_orderkey)
COMPRESSION = 'zstd'
STORAGE_FORMAT = 'parquet';
```

如果在没有 cluster key 的情况下，大表上的范围谓词会扫描大量块，请在比较查询性能之前评估添加 key 并执行 reclustering。

```sql
ALTER TABLE lineitem CLUSTER BY (DATE_TRUNC(MONTH, l_shipdate), l_orderkey);
ALTER TABLE lineitem RECLUSTER FINAL;
```

有关 key 设计的详细信息，请参见 [cluster key 指南](/tidb-cloud-lake/guides/cluster-key-performance.md)。

## Step 6. 监控重叠并运行 `RECLUSTER FINAL` {#step-6-monitor-overlap-and-run-recluster-final}

cluster key 并不会强制生成一个全局有序的文件。批量加载和大规模变异可能会导致许多块发生重叠，从而降低裁剪效果，但同时保持较快的写入速度。当重叠指标表明有必要时，请在初始加载之后以及重大数据变更之后运行以下操作。在执行期间，请暂停写入，包括复制到该表中的写入。`RECLUSTER` 运行期间不要执行 DML。详情请参见 [RECLUSTER TABLE](/tidb-cloud-lake/sql/recluster-table.md)。

```sql
ALTER TABLE lineitem RECLUSTER FINAL;
```

在 reclustering 前后检查 [CLUSTERING_INFORMATION](/tidb-cloud-lake/sql/clustering-information.md)。结合扫描字节数和查询延时，跟踪 `average_overlaps`、`average_depth` 和 `block_depth_histogram`。较低的 depth 和 overlap 通常表示更好的聚簇效果。对比 reclustering 前后相同工作负载的表现，以便为你的数据分布建立一个有用的维护阈值。

```sql
CREATE TABLE mytable(a INT, b INT) CLUSTER BY (a + 1);

INSERT INTO mytable VALUES (1, 1), (3, 3);
INSERT INTO mytable VALUES (2, 2), (5, 5);
INSERT INTO mytable VALUES (4, 4);

SELECT * FROM CLUSTERING_INFORMATION('default', 'mytable')\G
*************************** 1. row ***************************
            cluster_key: ((a + 1))
      total_block_count: 3
   constant_block_count: 1
 unclustered_block_count: 0
       average_overlaps: 1.3333
          average_depth: 2.0
   block_depth_histogram: {"00002":3}
```

以下指标摘要展示了相对中等程度的重叠。这些值并不是通用的健康阈值，也不是该函数的完整输出：

```json
{
  "cluster_key": "(yyyymm)",
  "info": {
    "average_depth": 40.6131,
    "average_overlaps": 40.7653,
    "total_block_count": 473
  },
  "type": "linear"
}
```

以下指标摘要显示了严重重叠：`average_depth` 已接近总块数。请检查查询扫描和延时，安排 reclustering，并在这种模式持续存在时重新评估 cluster key 设计：

```json
{
  "cluster_key": "(DATE_TRUNC(MONTH, l_shipdate), l_orderkey)",
  "info": {
    "average_depth": 10181.3357,
    "average_overlaps": 10211.5616,
    "total_block_count": 10214
  },
  "type": "linear"
}
```

对于持续发生变更的表，请在暂停 DML 和复制写入的维护窗口期间调度 reclustering。根据观察到的重叠趋势选择调度频率，并衡量其计算成本。以下每小时任务是一个示例；它不会暂停写入端，因此在恢复该任务之前，请先协调好维护窗口：

```sql
CREATE OR REPLACE TASK lineitem_hourly
  WAREHOUSE = 'default'
  SCHEDULE = 60 MINUTE
  COMMENT = 'Hourly FINAL recluster for lineitem'
AS
  ALTER TABLE lineitem RECLUSTER FINAL;

ALTER TASK lineitem_hourly RESUME;
```

## Step 7. 选择合适的块大小 {#step-7-choose-an-appropriate-block-size}

从与写入模式匹配的块大小开始：

- 对于大规模追加写入和分析型读取，请评估 536870912 字节（512 MiB）的阈值。
- 对于频繁的小批量插入、修改或删除，请评估更小的块，以降低重写成本和写放大。

在加载 PoC 数据之前应用该选项：

```sql
ALTER TABLE lineitem SET OPTIONS (BLOCK_SIZE_THRESHOLD = 536870912);
```

这只是评估的起点，而不是通用默认值。请在相同数据和查询条件下比较加载时间、写入成本、扫描字节数和查询延时。

## Step 8. 对重复聚合使用物化视图 {#step-8-use-materialized-views-for-repeated-aggregation}

当工作负载以相同粒度反复对单表进行聚合时，请使用物化视图对经常查询的维度进行预聚合。使基表和视图的 cluster key 与仪表盘谓词保持一致，然后在相同的计算集群和缓存条件下，将其查询与基线比较之前先刷新视图。创建操作只会记录定义；第一次刷新才会填充物理存储。

```sql
CREATE TABLE fact_table (
  tenant_id INT,
  account BIGINT,
  category_id INT,
  amount DECIMAL(19, 6)
);

-- Load representative data into fact_table before benchmarking.
CREATE MATERIALIZED VIEW mv_account_totals
  (tenant_id, account, category_id, total_amount)
CLUSTER BY (tenant_id, account)
AS
SELECT
  tenant_id,
  account,
  category_id,
  SUM(amount) AS total_amount
FROM fact_table
GROUP BY tenant_id, account, category_id;

REFRESH MATERIALIZED VIEW mv_account_totals;
```

物化视图最适合单表聚合。请参见 [TiDB Cloud Lake 物化视图文档](/tidb-cloud-lake/sql/materialized-view.md)。