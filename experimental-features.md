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
-   [コスト モデル バージョン 2](/cost-model.md#cost-model-version-2) . (v6.2.0 で導入)
-   [ファストスキャン](/develop/dev-guide-use-fastscan.md) . (v6.2.0 で導入)
-   [拡張統計](/extended-statistics.md) . (v5.0.0 で導入)
-   [統計をすばやく作成するために、約 10000 行のデータをランダムにサンプリングします](/system-variables.md#tidb_enable_fast_analyze) (v3.0 で導入)

## 安定性 {#stability}

-   オプティマイザーが選択するインデックスの安定性を向上させます。複数列の順序依存情報を収集して統計機能を拡張します (v5.0 で導入)。
-   [バックグラウンド クォータ リミッター](/tikv-configuration-file.md#background-quota-limiter) (v6.2.0 で導入): バックグラウンド クォータ関連の構成アイテムを使用して、バックグラウンドで使用される CPU リソースを制限できます。リクエストが Quota Limiter をトリガーすると、リクエストは TiKV が CPU リソースを解放するまでしばらく待機する必要があります。

## スケジューリング {#scheduling}

エラスティック スケジューリング機能。これにより、TiDB クラスターは、リアルタイムのワークロードに基づいて Kubernetes で動的にスケールアウトおよびスケールインできます。これにより、アプリケーションのピーク時のストレスが効果的に軽減され、オーバーヘッドが節約されます。詳細は[TidbCluster 自動スケーリングを有効にする](https://docs.pingcap.com/tidb-in-kubernetes/stable/enable-tidb-cluster-auto-scaling)を参照してください。 (v4.0 で導入)

## SQL {#sql}

-   表情インデックス機能。式インデックスは、関数ベースのインデックスとも呼ばれます。インデックスを作成する場合、インデックス フィールドは特定の列である必要はありませんが、1 つ以上の列から計算された式にすることができます。この機能は、計算ベースのテーブルにすばやくアクセスするのに役立ちます。詳細は[発現指数](/sql-statements/sql-statement-create-index.md)を参照してください。 (v4.0 で導入)
-   [生成された列](/generated-columns.md) (v2.1 で導入)
-   [ユーザー定義変数](/user-defined-variables.md) (v2.1 で導入)
-   [カスケード プランナー](/system-variables.md#tidb_enable_cascades_planner) : カスケード フレームワーク ベースのトップダウン クエリ オプティマイザー (v3.0 で導入)
-   [メタデータ ロック](/metadata-lock.md) (v6.3.0 で導入)
-   [範囲 INTERVAL パーティショニング](/partitioned-table.md#range-interval-partitioning) (v6.3.0 で導入)
-   [インデックス アクセラレーションを追加する](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) (v6.3.0 で導入)

## 保管所 {#storage}

-   [タイタン レベル マージ](/storage-engine/titan-configuration.md#level-merge-experimental) (v4.0 で導入)
-   分割 リージョンはバケットに分割されます。 [バケットは同時クエリの単位として使用されます](/tune-region-performance.md#use-bucket-to-increase-concurrency)スキャンの同時実行性を向上させます。 (v6.1.0 で導入)
-   TiKV は[API V2](/tikv-configuration-file.md#api-version-new-in-v610)を紹介します。 (v6.1.0 で導入)

## データ移行 {#data-migration}

-   DM で移行タスクを管理する場合は[WebUI を使用する](/dm/dm-webui-guide.md) 。 (v6.0 で導入)
-   TiDB Lightningの場合は[ディスク クォータの構成](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#configure-disk-quota-new-in-v620) 。 (v6.2.0 で導入)
-   [DM での継続的なデータ検証](/dm/dm-continuous-data-validation.md) (v6.2.0 で導入)

## データ共有サブスクリプション {#data-share-subscription}

-   [クラスタ間の RawKV レプリケーション](/tikv-configuration-file.md#api-version-new-in-v610) (v6.2.0 で導入)

## ガベージ コレクション {#garbage-collection}

-   [グリーンGC](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50) (v5.0 で導入)

## 診断 {#diagnostics}

-   [SQL 診断](/information-schema/information-schema-sql-diagnostics.md) (v4.0 で導入)
-   [クラスタ診断](/dashboard/dashboard-diagnostics-access.md) (v4.0 で導入)
-   [TiKV-FastTune ダッシュボード](/grafana-tikv-dashboard.md#tikv-fasttune-dashboard) (v4.0 で導入)
