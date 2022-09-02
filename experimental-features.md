---
title: TiDB Experimental Features
summary: Learn the experimental features of TiDB.
---

# TiDB の実験的機能 {#tidb-experimental-features}

このドキュメントでは、さまざまなバージョンの TiDB の実験的機能を紹介します。これらの機能を本番環境で使用することはお勧めし**ません**。

## パフォーマンス {#performance}

-   [`PREDICATE COLUMNS`の統計収集のサポート](/statistics.md#collect-statistics-on-some-columns) (v5.4 で導入)
-   [統計の同期ロードをサポート](/statistics.md#load-statistics) . (v5.4 で導入)
-   [統計を収集するためのメモリ クォータを制御する](/statistics.md#the-memory-quota-for-collecting-statistics) . (v6.1.0 で導入)
-   [統計をすばやく作成するために、約 10000 行のデータをランダムにサンプリングします](/system-variables.md#tidb_enable_fast_analyze) (v3.0 で導入)

## 安定性 {#stability}

-   オプティマイザーが選択するインデックスの安定性を向上させます。複数列の順序依存情報を収集して統計機能を拡張します (v5.0 で導入)。
-   TiKV が限られたリソースで展開されている場合、TiKV のフォアグラウンドが処理する読み取りおよび書き込み要求が多すぎると、そのような要求の処理を支援するためにバックグラウンドで使用される CPU リソースが占有され、TiKV のパフォーマンスの安定性に影響します。この状況を回避するには、 [クォータリミッター](/tikv-configuration-file.md#quota)を使用して、フォアグラウンドで使用される CPU リソースを制限します。 (v6.0 で導入)

## スケジューリング {#scheduling}

エラスティック スケジューリング機能。これにより、TiDB クラスターは、リアルタイムのワークロードに基づいて Kubernetes で動的にスケールアウトおよびスケールインできます。これにより、アプリケーションのピーク時のストレスが効果的に軽減され、オーバーヘッドが節約されます。詳細は[TidbCluster 自動スケーリングを有効にする](https://docs.pingcap.com/tidb-in-kubernetes/stable/enable-tidb-cluster-auto-scaling)を参照してください。 (v4.0 で導入)

## SQL {#sql}

-   表情インデックス機能。式インデックスは、関数ベースのインデックスとも呼ばれます。インデックスを作成する場合、インデックス フィールドは特定の列である必要はありませんが、1 つ以上の列から計算された式にすることができます。この機能は、計算ベースのテーブルにすばやくアクセスするのに役立ちます。詳細は[発現指数](/sql-statements/sql-statement-create-index.md)を参照してください。 (v4.0 で導入)
-   [生成された列](/generated-columns.md) (v2.1 で導入)
-   [ユーザー定義変数](/user-defined-variables.md) (v2.1 で導入)
-   [JSON データ型](/data-type-json.md)と[JSON関数](/functions-and-operators/json-functions.md) (v2.1 で導入)
-   [カスケード プランナー](/system-variables.md#tidb_enable_cascades_planner) : カスケード フレームワーク ベースのトップダウン クエリ オプティマイザー (v3.0 で導入)
-   [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md) (v6.1.0 で導入)
-   [`ALTER TABLE`を使用して複数の列またはインデックスを変更する](/system-variables.md#tidb_enable_change_multi_schema) (v5.0.0 で導入)

## 保管所 {#storage}

-   [タイタンを無効にする](/storage-engine/titan-configuration.md#disable-titan-experimental) (v4.0 で導入)
-   [タイタン レベル マージ](/storage-engine/titan-configuration.md#level-merge-experimental) (v4.0 で導入)
-   分割 リージョンはバケットに分割されます。 [バケットは同時クエリの単位として使用されます](/tune-region-performance.md#use-bucket-to-increase-concurrency)スキャンの同時実行性を向上させます。 (v6.1.0 で導入)
-   TiKV は[API V2](/tikv-configuration-file.md#api-version-new-in-v610)を紹介します。 (v6.1.0 で導入)

## バックアップと復元 {#backup-and-restoration}

-   [RawKV のバックアップと復元](/br/rawkv-backup-and-restore.md) (v3.1 で導入)

## データ移行 {#data-migration}

-   DM で移行タスクを管理する場合は[WebUI を使用する](/dm/dm-webui-guide.md) 。 (v6.0 で導入)

## ガベージ コレクション {#garbage-collection}

-   [グリーンGC](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50) (v5.0 で導入)

## 診断 {#diagnostics}

-   [SQL 診断](/information-schema/information-schema-sql-diagnostics.md) (v4.0 で導入)
-   [クラスタ診断](/dashboard/dashboard-diagnostics-access.md) (v4.0 で導入)
