---
title: TiDB Cloud Lake PoC ガイド
summary: スキーママッピング、クラスターキー、reclustering、ブロックサイズ、マテリアライズドビューを使用して、代表的なワークロードで TiDB Cloud Lake を評価します。
---

# TiDB Cloud Lake PoC ガイド <!--Corresponding EN commit: 98a43e43b8d02b1c0a405d0332dadbd055612466-->

このガイドでは、TiDB Cloud Premium インスタンスから TiDB Cloud Lake へのデータレプリケーションを主な例として、TiDB Cloud Lake の再現可能な概念実証（PoC）について説明します。代表的なワークロードに最も大きな影響を与える判断事項、すなわちオブジェクトストレージと PrivateLink 接続、スキーマ互換性、データレイアウト、overlap のメンテナンス、ブロックサイズ、事前集計に焦点を当てています。

PoC は、代表的なデータサンプルと本番で使用するクエリパターンで実行してください。クエリレイテンシー、QPS、Warehouse サイズ、ストレージサイズを記録し、各最適化を同じベースラインと比較できるようにします。

## Step 1. S3 接続を設定する {#step-1-configure-an-s3-connection}

ソースパイプラインがすでに Parquet、CSV、または JSON オブジェクトをオブジェクトストレージに書き込んでいる場合は、S3 バケットを使用します。**Home > Connect** で TiDB Cloud Lake デプロイメント用の IAM role ARN を取得し、[AWS IAM Role による認証](/tidb-cloud-lake/guides/authenticate-with-aws-iam-role.md) に従って S3 接続、stage、およびデータロードを設定します。

## Step 2. PrivateLink を設定する {#step-2-configure-privatelink}

トラフィックをプライベートネットワーク経路内に留める必要がある場合は、PrivateLink を使用します。**Home > Connect** で PrivateLink service を取得し、[AWS PrivateLink で接続する](/tidb-cloud-lake/guides/connect-with-aws-privatelink.md) に従って接続を設定します。ロードを開始する前に、クライアントまたはソースクラスターから、エンドポイント、security-group ルール、DNS の動作、およびルートを確認してください。

## Step 3. Data Pipeline を使用して TiDB Cloud Premium インスタンスから TiDB Cloud Lake にデータをレプリケートする {#step-3-use-data-pipeline-to-replicate-data-from-a-tidb-cloud-premium-instance-to-tidb-cloud-lake}

TiDB Cloud Data Pipeline を使用すると、サードパーティの ETL ツールを導入せずに、TiDB Cloud Premium インスタンスから TiDB Cloud Lake にデータをレプリケートできます。Data Pipeline はまず選択したソースデータの完全なスナップショットをエクスポートし、その後、行レベルの変更を継続的にレプリケートすることで、TiDB Cloud Lake 内のデータを最新の状態に保ちます。

Data Pipeline は増分レプリケーションに TiCDC を使用し、TiDB Cloud と TiDB Cloud Lake 間でデータを転送するために外部 stage を使用します。PoC を開始する前に、必要な機能がご利用の TiDB Cloud プランで使用可能であること、および外部 stage とアクセスポリシーが設定されていることを確認してください。現在の提供状況と設定要件については、[Data Pipeline to TiDB Cloud Lake](https://docs.pingcap.com/tidbcloud/data-pipeline-sink-to-lake/) を参照してください。

PoC では、代表的なテーブルを選択し、それらのスキーマ、想定行数、および鮮度目標を記録してください。初期スナップショットの完了後、行数、null 数、サンプル集計、最小値と最大値をソースと比較します。次に、ソースで代表的な insert、update、delete を生成し、TiDB Cloud Lake が想定されるレプリケーションレイテンシー内でそれらを反映することを確認します。レプリケートされたテーブルをクエリ性能テストに使用する前に、スナップショット所要時間、レプリケーション遅延、拒否されたレコード、およびスキーママッピングエラーを記録してください。

### ソーススキーマをマッピングして検証する {#map-and-validate-the-source-schema}

ファイルをロードしたりレプリケーションを開始したりする前に、各ソースカラムと対応する Lake のターゲットカラム、データ型、null 許容性、デフォルト値、および必要な変換を記録してください。decimal の精度とスケール、signed および unsigned 整数の範囲、timestamp の精度とタイムゾーン、文字列エンコーディングを確認します。ターゲット型の選択には [Lake データ型リファレンス](/tidb-cloud-lake/sql/data-types.md) を使用してください。型名が一致していても意味論が同一であるとは限りません。

null と境界値を含む小さなサンプルをロードします。同じスナップショットまたはレプリケーションチェックポイント時点で、行数と null 数、最小値と最大値、集計結果をソースと比較してください。変換によって精度と timestamp の意味が保持されていることを確認し、完全ロードを開始する前に、拒否または切り捨てられた値を調査してください。

## Step 4. 性能ベースラインを確立する {#step-4-establish-the-performance-baseline}

Lake のクエリ性能に影響する主な要因は次のとおりです。

1. **Warehouse リソース。** CPU、メモリ、Warehouse サイズ、および同時実行制限によって、一度に実行できる作業量が決まります。
2. **データレイアウト。** クラスターキーの順序、ブロック overlap、ブロックサイズによって、どれだけデータを pruning できるかが決まります。
3. **クエリパターン。** 必要なカラムだけを投影し、可能であれば選択性の高い述語に先頭のクラスターキーカラムを含めてください。

各ベースラインクエリについて `EXPLAIN` の出力を取得してください。`TableScan` が支配的な場合は、同時実行数を増やす前に、クラスターキー pruning、overlap メトリクス、ブロックサイズ、キャッシュヒット率、および Warehouse 容量を確認します。

## Step 5. ワークロードに効果がある場合はクラスターキーを選択する {#step-5-choose-a-cluster-key-when-the-workload-benefits}

予測可能なフィルターや範囲スキャンを持つ大きなテーブルを作成する場合は、クラスターキーを評価してください。小さなテーブル、ランダムアクセスパターン、頻繁な変更では、メンテナンスコストを正当化できるほどの効果が得られない場合があります。フィルター、テーブル結合、または範囲スキャンで頻繁に使用されるカラムを使い、最もよくフィルターされるカラムを先頭に配置します。キー式はできるだけ狭く保ってください。長い文字列には、長さを制限した prefix 式を使用します。

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

クラスターキーのない大きなテーブルで、範囲述語が多数のブロックをスキャンしている場合は、クエリ性能を比較する前に、キーの追加と reclustering を評価してください。

```sql
ALTER TABLE lineitem CLUSTER BY (DATE_TRUNC(MONTH, l_shipdate), l_orderkey);
ALTER TABLE lineitem RECLUSTER FINAL;
```

キー設計の詳細については、[クラスターキーガイド](/tidb-cloud-lake/guides/cluster-key-performance.md) を参照してください。

## Step 6. overlap を監視し、`RECLUSTER FINAL` を実行する {#step-6-monitor-overlap-and-run-recluster-final}

クラスターキーは、グローバルに 1 つのソート済みファイルを強制するものではありません。バルクロードや大規模な変更によって、多数のブロックが overlap した状態になり、取り込み速度を維持しつつ pruning 効率が低下することがあります。初期ロード後、および大きなデータ変更後に、overlap メトリクスが必要性を示している場合は、次の操作を実行してください。操作中は、テーブルへのレプリケーションを含む書き込みを停止します。`RECLUSTER` の実行中は DML を実行しないでください。詳細については、[RECLUSTER TABLE](/tidb-cloud-lake/sql/recluster-table.md) を参照してください。

```sql
ALTER TABLE lineitem RECLUSTER FINAL;
```

reclustering の前後で [CLUSTERING_INFORMATION](/tidb-cloud-lake/sql/clustering-information.md) を確認してください。`average_overlaps`、`average_depth`、`block_depth_histogram` を、スキャンされたバイト数およびクエリレイテンシーとあわせて追跡します。一般に、depth と overlap が低いほど、より良い clustering を示します。データ分布に対して有用なメンテナンス閾値を確立するために、reclustering の前後で同じワークロードを比較してください。

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

次のメトリクス要約は、比較的中程度の overlap を示しています。これらの値は普遍的な健全性しきい値でも、この関数の完全な出力でもありません。

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

次のメトリクス要約は、深刻な overlap を示しています。`average_depth` が総ブロック数に近くなっています。クエリスキャンとレイテンシーを確認し、reclustering をスケジュールし、このパターンが続く場合はクラスターキー設計を見直してください。

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

継続的に変化するテーブルについては、DML とレプリケーション書き込みを停止したメンテナンスウィンドウ中に reclustering をスケジュールしてください。スケジュールは観測された overlap の傾向に基づいて選択し、その計算コストを測定します。次の hourly task は一例です。これは writer を停止しないため、再開前にメンテナンスウィンドウを調整してください。

```sql
CREATE OR REPLACE TASK lineitem_hourly
  WAREHOUSE = 'default'
  SCHEDULE = 60 MINUTE
  COMMENT = 'Hourly FINAL recluster for lineitem'
AS
  ALTER TABLE lineitem RECLUSTER FINAL;

ALTER TASK lineitem_hourly RESUME;
```

## Step 7. 適切なブロックサイズを選択する {#step-7-choose-an-appropriate-block-size}

書き込みパターンに合ったブロックサイズから開始してください。

- 大規模な append と分析読み取りでは、536870912 bytes (512 MiB) のしきい値を評価します。
- 頻繁な小規模 insert、update、delete では、書き換えコストと write amplification を減らすために、より小さいブロックを評価します。

PoC データをロードする前に、このオプションを適用してください。

```sql
ALTER TABLE lineitem SET OPTIONS (BLOCK_SIZE_THRESHOLD = 536870912);
```

これは評価の出発点であり、普遍的なデフォルト値ではありません。同じデータとクエリで、ロード時間、書き込みコスト、スキャンされたバイト数、およびクエリレイテンシーを比較してください。

## Step 8. 繰り返し行う集計にはマテリアライズドビューを使用する {#step-8-use-materialized-views-for-repeated-aggregation}

ワークロードが同じ粒度で 1 つのテーブルを繰り返し集計する場合は、マテリアライズドビューを使用して、頻繁にクエリされるディメンションを事前集計してください。ベーステーブルとビューのクラスターキーをダッシュボードの述語に合わせ、そのクエリを同じ Warehouse とキャッシュ条件下のベースラインと比較する前に、ビューを refresh します。作成時には定義が記録され、最初の refresh で物理ストレージが作成されます。

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

マテリアライズドビューは、単一テーブルの集計に最も適しています。詳細は、[TiDB Cloud Lake のマテリアライズドビューのドキュメント](/tidb-cloud-lake/sql/materialized-view.md) を参照してください。