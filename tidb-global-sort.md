---
title: TiDB Global Sort
summary: TiDB グローバル ソートの使用例、制限、使用方法、実装の原則について学習します。
---

<!-- markdownlint-disable MD029 -->

<!-- markdownlint-disable MD046 -->

# TiDB グローバルソート {#tidb-global-sort}

> **注記：**
>
> -   現在、グローバル ソート プロセスは、TiDB ノードのコンピューティング リソースとメモリリソースを大量に消費します。ユーザー ビジネス アプリケーションの実行中にオンラインでインデックスを追加するなどのシナリオでは、クラスターに新しい TiDB ノードを追加し、これらのノードの[`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740)変数を構成し、これらのノードに接続してタスクを作成することをお勧めします。このようにして、分散フレームワークはこれらのノードにタスクをスケジュールし、他の TiDB ノードからワークロードを分離して、 `ADD INDEX`や`IMPORT INTO`などのバックエンド タスクの実行がユーザー ビジネス アプリケーションに与える影響を軽減します。
> -   グローバル ソート機能を使用する場合は、OOM を回避するために、少なくとも 16 コアの CPU と 32 GiB のメモリを備えた TiDB ノードを使用することをお勧めします。

> **注記：**
>
> この機能は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

## 概要 {#overview}

TiDB グローバル ソート機能は、データ インポートおよび DDL (データ定義言語) 操作の安定性と効率性を高めます。1 [TiDB 分散実行フレームワーク (DXF)](/tidb-distributed-execution-framework.md)汎用演算子として機能し、クラウド上でグローバル ソート サービスを提供します。

現在、グローバルソート機能は、クラウドstorageとして Amazon S3 の使用をサポートしています。

## ユースケース {#use-cases}

グローバルソート機能は、 `IMPORT INTO`と`CREATE INDEX`の安定性と効率性を高めます。タスクによって処理されるデータをグローバルにソートすることで、TiKV へのデータ書き込みの安定性、制御性、スケーラビリティが向上します。これにより、データインポートおよび DDL タスクのユーザーエクスペリエンスが向上し、サービスの品質が向上します。

グローバル ソート機能は、統合された DXF 内でタスクを実行し、グローバル規模でデータの効率的かつ並列的なソートを保証します。

## 制限事項 {#limitations}

現在、グローバル ソート機能は、クエリ結果のソートを担当するクエリ実行プロセスのコンポーネントとして使用されていません。

## 使用法 {#usage}

グローバルソートを有効にするには、次の手順に従います。

1.  [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)の値を`ON`に設定して DXF を有効にします。v8.1.0 以降では、この変数はデフォルトで有効になっています。v8.1.0 以降のバージョンで新しく作成されたクラスターの場合は、この手順をスキップできます。

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
