---
title: TiDB Experimental Features
summary: Learn the experimental features of TiDB.
---

# TiDB のExperimental機能 {#tidb-experimental-features}

このドキュメントでは、さまざまなバージョンの TiDB の実験的機能を紹介します。これらの機能を本番環境で使用することはお勧めし**ません**。

## パフォーマンス {#performance}

-   [`PREDICATE COLUMNS`の統計収集のサポート](/statistics.md#collect-statistics-on-some-columns) (v5.4 で導入)
-   [統計を収集するためのメモリ クォータを制御する](/statistics.md#the-memory-quota-for-collecting-statistics) . (v6.1.0 で導入)
-   [ファストスキャン](/develop/dev-guide-use-fastscan.md) . (v6.2.0 で導入)
-   [拡張統計](/extended-statistics.md) . (v5.0.0 で導入)
-   [統計をすばやく作成するために、約 10000 行のデータをランダムにサンプリングします](/system-variables.md#tidb_enable_fast_analyze) (v3.0 で導入)
-   [ロック統計のサポート](/statistics.md#lock-statistics) (v6.5.0 で導入)

## 安定性 {#stability}

-   オプティマイザーが選択するインデックスの安定性を向上させます。複数列の順序依存情報を収集して統計機能を拡張します (v5.0 で導入)。
-   [バックグラウンド クォータ リミッター](/tikv-configuration-file.md#background-quota-limiter) (v6.2.0 で導入): バックグラウンド クォータ関連の構成アイテムを使用して、バックグラウンドで使用される CPU リソースを制限できます。リクエストが Quota Limiter をトリガーすると、リクエストは TiKV が CPU リソースを解放するまでしばらく待機する必要があります。

## スケジューリング {#scheduling}

エラスティック スケジューリング機能。これにより、TiDB クラスターは、リアルタイムのワークロードに基づいて Kubernetes で動的にスケールアウトおよびスケールインできます。これにより、アプリケーションのピーク時のストレスが効果的に軽減され、オーバーヘッドが節約されます。詳細は[TidbCluster 自動スケーリングを有効にする](https://docs.pingcap.com/tidb-in-kubernetes/stable/enable-tidb-cluster-auto-scaling)を参照してください。 (v4.0 で導入)

## SQL {#sql}

-   [生成された列](/generated-columns.md) (v2.1 で導入)
-   [ユーザー定義変数](/user-defined-variables.md) (v2.1 で導入)
-   [カスケード プランナー](/system-variables.md#tidb_enable_cascades_planner) : カスケード フレームワーク ベースのトップダウン クエリ オプティマイザー (v3.0 で導入)
-   [テーブルロック](/tidb-configuration-file.md#enable-table-lock-new-in-v400) (v4.0.0 で導入)
-   [範囲 INTERVAL パーティショニング](/partitioned-table.md#range-interval-partitioning) (v6.3.0 で導入)
-   [有効期間](/time-to-live.md) (v6.5.0 で導入)
-   [TiFlashクエリ結果の実体化](/tiflash/tiflash-results-materialization.md) (v6.5.0 で導入)
-   [過去の実行計画に従ってバインディングを作成する](/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan) (v6.5.0 で導入)

## 保管所 {#storage}

-   [タイタン レベル マージ](/storage-engine/titan-configuration.md#level-merge-experimental) (v4.0 で導入)
-   分割 リージョンはバケットに分割されます。 [バケットは同時クエリの単位として使用されます](/tune-region-performance.md#use-bucket-to-increase-concurrency)スキャンの同時実行性を向上させます。 (v6.1.0 で導入)

## データ移行 {#data-migration}

-   DM で移行タスクを管理する場合は[WebUI を使用する](/dm/dm-webui-guide.md) 。 (v6.0 で導入)

## データ共有サブスクリプション {#data-share-subscription}

-   [クラスタ間の RawKV レプリケーション](/tikv-configuration-file.md#api-version-new-in-v610) (v6.2.0 で導入)
-   [TiCDC を介して Amazon S3、Azure Blob Storage、NFS にデータをストリーミングする](/ticdc/ticdc-sink-to-cloud-storage.md) (v6.5.0 で導入)

## ガベージ コレクション {#garbage-collection}

-   [グリーンGC](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50) (v5.0 で導入)

## 診断 {#diagnostics}

-   [TiKV-FastTune ダッシュボード](/grafana-tikv-dashboard.md#tikv-fasttune-dashboard) (v4.0 で導入)
