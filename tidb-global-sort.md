---
title: TiDB Global Sort
summary: TiDB グローバル ソートの使用例、制限、使用方法、実装の原則について学習します。
---

<!-- markdownlint-disable MD029 -->

<!-- markdownlint-disable MD046 -->

# TiDB グローバルソート {#tidb-global-sort}

> **警告：**
>
> この機能は実験的ものです。本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告できます。

> **注記：**
>
> この機能は[TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)クラスターでは使用できません。

## 概要 {#overview}

TiDB グローバル ソート機能は、データ インポートおよび DDL (データ定義言語) 操作の安定性と効率性を高めます。1 [TiDB 分散実行フレームワーク (DXF)](/tidb-distributed-execution-framework.md)汎用演算子として機能し、クラウド上でグローバル ソート サービスを提供します。

グローバルソート機能は現在、クラウドstorageとして Amazon S3 の使用のみをサポートしています。将来のリリースでは、POSIX などの複数の共有storageインターフェースをサポートするように拡張され、さまざまなstorageシステムとのシームレスな統合が可能になります。この柔軟性により、さまざまなユースケースで効率的かつ適応性の高いデータソートが可能になります。

## ユースケース {#use-cases}

グローバルソート機能は、 `IMPORT INTO`と`CREATE INDEX`の安定性と効率性を高めます。タスクによって処理されるデータをグローバルにソートすることで、TiKV へのデータ書き込みの安定性、制御性、スケーラビリティが向上します。これにより、データインポートおよび DDL タスクのユーザーエクスペリエンスが向上し、サービスの品質が向上します。

グローバル ソート機能は、統合された DXF 内でタスクを実行し、グローバル規模でデータの効率的かつ並列的なソートを保証します。

## 制限事項 {#limitations}

現在、グローバル ソート機能は、クエリ結果のソートを担当するクエリ実行プロセスのコンポーネントとして使用されていません。

## 使用法 {#usage}

グローバルソートを有効にするには、次の手順に従います。

1.  値を[`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)から`ON`に設定して DXF を有効にします。

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

<CustomContent platform="tidb">

2.  [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740)正しいクラウドstorageパスに設定します。3 [例](/br/backup-and-restore-storages.md)参照してください。

    ```sql
    SET GLOBAL tidb_cloud_storage_uri = 's3://my-bucket/test-data?role-arn=arn:aws:iam::888888888888:role/my-role'
    ```

</CustomContent>
<CustomContent platform="tidb-cloud">

2.  [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740)正しいクラウドstorageパスに設定します。3 [例](https://docs.pingcap.com/tidb/stable/backup-and-restore-storages)参照してください。

    ```sql
    SET GLOBAL tidb_cloud_storage_uri = 's3://my-bucket/test-data?role-arn=arn:aws:iam::888888888888:role/my-role'
    ```

</CustomContent>

> **注記：**
>
> [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)の場合、 [`CLOUD_STORAGE_URI`](/sql-statements/sql-statement-import-into.md#withoptions)オプションを使用してクラウドstorageパスを指定することもできます。 [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740)と`CLOUD_STORAGE_URI`両方に有効なクラウドstorageパスが設定されている場合、 `CLOUD_STORAGE_URI`の設定が[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)に有効になります。

## 実施原則 {#implementation-principles}

グローバル ソート機能のアルゴリズムは次のとおりです。

![Algorithm of Global Sort](/media/dist-task/global-sort.jpeg)

詳細な実装原則は次のとおりです。

### ステップ1: データをスキャンして準備する {#step-1-scan-and-prepare-data}

1.  TiDB ノードが特定の範囲のデータをスキャンした後 (データ ソースは CSV データまたは TiKV のテーブル データのいずれかになります)、次のようになります。

    1.  TiDB ノードはそれらをキーと値のペアにエンコードします。
    2.  TiDB ノードは、キーと値のペアを複数のブロック データ セグメントに分類します (データ セグメントはローカルに分類されます)。各セグメントは 1 つのファイルであり、クラウドstorageにアップロードされます。

2.  TiDB ノードは、各セグメントの実際のキーと値の範囲 (統計ファイルと呼ばれる) も連続して記録します。これは、スケーラブルなソートの実装に不可欠な準備です。これらのファイルは、実際のデータとともにクラウドstorageにアップロードされます。

### ステップ2: データを分類して分配する {#step-2-sort-and-distribute-data}

ステップ 1 から、グローバル ソート プログラムは、ソートされたブロックのリストとそれに対応する統計ファイルを取得します。これにより、ローカルにソートされたブロックの数が得られます。プログラムには、PD が分割および分散に使用できる実際のデータ スコープもあります。次の手順が実行されます。

1.  統計ファイル内のレコードを並べ替えて、ほぼ等しいサイズの範囲に分割します。これは、並列で実行されるサブタスクです。
2.  サブタスクを TiDB ノードに分散して実行します。
3.  各 TiDB ノードは、サブタスクのデータを範囲ごとに独立して分類し、重複することなく TiKV に取り込みます。
