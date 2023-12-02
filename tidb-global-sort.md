---
title: TiDB Global Sort
summary: Learn the use cases, limitations, usage, and implementation principles of the TiDB Global Sort.
---

<!-- markdownlint-disable MD029 -->

<!-- markdownlint-disable MD046 -->

# TiDB グローバル ソート {#tidb-global-sort}

> **警告：**
>
> この機能は実験的です。本番環境で使用することはお勧めできません。この機能は予告なく変更または削除される場合があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。

<CustomContent platform="tidb-cloud">

> **注記：**
>
> 現在、この機能は TiDB 専用クラスターにのみ適用されます。 TiDB サーバーレス クラスターでは使用できません。

</CustomContent>

## 概要 {#overview}

TiDB グローバル ソート機能は、データ インポートと DDL (データ定義言語) 操作の安定性と効率を強化します。 [分散実行フレームワーク](/tidb-distributed-execution-framework.md)の総合事業者としてクラウド上でグローバルソートサービスを提供しています。

グローバル ソート機能は現在、クラウドstorageとして Amazon S3 の使用のみをサポートしています。将来のリリースでは、POSIX などの複数の共有storageインターフェイスをサポートするように拡張され、さまざまなstorageシステムとのシームレスな統合が可能になります。この柔軟性により、さまざまなユースケースに合わせて効率的かつ適応性のあるデータの並べ替えが可能になります。

## ユースケース {#use-cases}

グローバル ソート機能により、 `IMPORT INTO`と`CREATE INDEX`の安定性と効率が向上します。タスクによって処理されるデータをグローバルに並べ替えることにより、TiKV へのデータ書き込みの安定性、制御性、拡張性が向上します。これにより、データ インポートおよび DDL タスクのユーザー エクスペリエンスが向上し、さらに高品質のサービスが提供されます。

グローバル ソート機能は、統合された分散並列実行フレームワーク内でタスクを実行し、グローバル スケールでのデータの効率的かつ並列ソートを保証します。

## 制限事項 {#limitations}

現在、グローバル ソート機能は、クエリ結果の並べ替えを担当するクエリ実行プロセスのコンポーネントとしては使用されていません。

## 使用法 {#usage}

グローバル ソートを有効にするには、次の手順に従います。

1.  値[`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) ～ `ON`を設定して、分散実行フレームワークを有効にします。

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

<CustomContent platform="tidb">

2.  [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740)を正しいクラウドstorageパスに設定します。 [例](/br/backup-and-restore-storages.md)を参照してください。

> **注記：**
>
> [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)の場合、 [`CLOUD_STORAGE_URI`](/sql-statements/sql-statement-import-into.md#withoptions)オプションを使用してクラウドstorageパスを指定することもできます。 [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740)と`CLOUD_STORAGE_URI`の両方が有効なクラウドstorageパスで構成されている場合、 `CLOUD_STORAGE_URI`の構成は[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)にも有効になります。

</CustomContent>
<CustomContent platform="tidb-cloud">

2.  [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740)を正しいクラウドstorageパスに設定します。 [例](https://docs.pingcap.com/tidb/stable/backup-and-restore-storages)を参照してください。

</CustomContent>

    ```sql
    SET GLOBAL tidb_cloud_storage_uri = 's3://my-bucket/test-data?role-arn=arn:aws:iam::888888888888:role/my-role'
    ```

## 実装原則 {#implementation-principles}

グローバル ソート機能のアルゴリズムは次のとおりです。

![Algorithm of Global Sort](/media/dist-task/global-sort.jpeg)

詳細な実装原則は次のとおりです。

### ステップ 1: データをスキャンして準備する {#step-1-scan-and-prepare-data}

1.  TiDB ノードが特定範囲のデータをスキャンした後 (データ ソースは CSV データまたは TiKV のテーブル データのいずれかです):

    1.  TiDB ノードは、それらをキーと値のペアにエンコードします。
    2.  TiDB ノードは、Key-Value ペアをいくつかのブロック データ セグメントに分類します (データ セグメントはローカルに分類されます)。各セグメントは 1 つのファイルであり、クラウドstorageにアップロードされます。

2.  TiDB ノードは、各セグメント (統計ファイルと呼ばれる) のシリアルの実際の Key-Value 範囲も記録します。これは、スケーラブルな並べ替え実装の重要な準備となります。これらのファイルは、実際のデータとともにクラウドstorageにアップロードされます。

### ステップ 2: データの分類と配布 {#step-2-sort-and-distribute-data}

ステップ 1 から、グローバル ソート プログラムは、ソートされたブロックのリストと、ローカルでソートされたブロックの数を提供するそれに対応する統計ファイルを取得します。このプログラムには、PD が分割および分散するために使用できる実際のデータ スコープもあります。次の手順が実行されます。

1.  統計ファイル内のレコードを並べ替えて、ほぼ同じサイズの範囲に分割します。これらの範囲は、並行して実行されるサブタスクです。
2.  サブタスクを TiDB ノードに分散して実行します。
3.  各 TiDB ノードは、サブタスクのデータを個別に範囲にソートし、重複することなく TiKV に取り込みます。
