---
title: TiDB Experimental Features
summary: Learn the experimental features of TiDB.
---

# TiDB の実験的機能 {#tidb-experimental-features}

このドキュメントでは、さまざまなバージョンの TiDB の実験的機能を紹介します。これらの機能を本番環境で使用することはお勧めし**ません**。

## パフォーマンス {#performance}

-   [TiFlash スレッド プールを自動的にスケーリングする](/tiflash/tiflash-configuration.md) . (v5.4 で導入)
-   [Raft Engine](/tikv-configuration-file.md#raft-engine) . (v5.4 で導入)
-   [`PREDICATE COLUMNS`の統計収集のサポート](/statistics.md#collect-statistics-on-some-columns) (v5.4 で導入)
-   [統計の同期ロードをサポート](/statistics.md#load-statistics) . (v5.4 で導入)
-   [統計をすばやく作成するために、約 10000 行のデータをランダムにサンプリングします](/system-variables.md#tidb_enable_fast_analyze) (v3.0 で導入)

## 安定性 {#stability}

-   オプティマイザーが選択するインデックスの安定性を向上させます。複数列の順序依存情報を収集して統計機能を拡張します (v5.0 で導入)。

## スケジューリング {#scheduling}

エラスティック スケジューリング機能。これにより、TiDB クラスターは、リアルタイムのワークロードに基づいて Kubernetes で動的にスケールアウトおよびスケールインできます。これにより、アプリケーションのピーク時のストレスが効果的に軽減され、オーバーヘッドが節約されます。詳細は[TidbCluster 自動スケーリングを有効にする](https://docs.pingcap.com/tidb-in-kubernetes/stable/enable-tidb-cluster-auto-scaling)を参照してください。 (v4.0 で導入)

## SQL {#sql}

-   [SQL インターフェイスを使用してデータの配置ルールを設定する](/placement-rules-in-sql.md) (v5.3 で導入)
-   リスト パーティション (v5.0 で導入)
-   COLUMNS パーティションの一覧表示 (v5.0 で導入)
-   [分割されたテーブルの動的プルーニング モード](/partitioned-table.md#dynamic-pruning-mode) . (v5.1 で導入)
-   表情インデックス機能。式インデックスは、関数ベースのインデックスとも呼ばれます。インデックスを作成する場合、インデックス フィールドは特定の列である必要はありませんが、1 つ以上の列から計算された式にすることができます。この機能は、計算ベースのテーブルにすばやくアクセスするのに役立ちます。詳細は[発現指数](/sql-statements/sql-statement-create-index.md)を参照してください。 (v4.0 で導入)
-   [生成された列](/generated-columns.md) (v2.1 で導入)
-   [ユーザー定義変数](/user-defined-variables.md) (v2.1 で導入)
-   [JSON データ型](/data-type-json.md)と[JSON関数](/functions-and-operators/json-functions.md) (v2.1 で導入)
-   [`ALTER TABLE`を使用して複数の列またはインデックスを変更する](/system-variables.md#tidb_enable_change_multi_schema) (v5.0.0 で導入)
-   [カスケード プランナー](/system-variables.md#tidb_enable_cascades_planner) : カスケード フレームワーク ベースのトップダウン クエリ オプティマイザー (v3.0 で導入)
-   [テーブルロック](/tidb-configuration-file.md#enable-table-lock-new-in-v400) (v4.0.0 で導入)

## Configuration / コンフィグレーション管理 {#configuration-management}

-   構成パラメーターを PD に永続的に保存し、構成アイテムの動的な変更をサポートします。 (v4.0 で導入)

## データの共有と購読 {#data-sharing-and-subscription}

-   [TiCDC を Kafka Connect (コンフルエント プラットフォーム) と統合する](/ticdc/integrate-confluent-using-ticdc.md) (v5.0 で導入)

## 保管所 {#storage}

-   [タイタンを無効にする](/storage-engine/titan-configuration.md#disable-titan-experimental) (v4.0 で導入)
-   [タイタン レベル マージ](/storage-engine/titan-configuration.md#level-merge-experimental) (v4.0 で導入)

## バックアップと復元 {#backup-and-restoration}

-   [Raw KV のバックアップ](/br/use-br-command-line-tool.md#back-up-raw-kv-experimental-feature) (v3.1 で導入)

## ガベージ コレクション {#garbage-collection}

-   [グリーンGC](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50) (v5.0 で導入)

## 診断 {#diagnostics}

-   [SQL 診断](/information-schema/information-schema-sql-diagnostics.md) (v4.0 で導入)
-   [クラスタ診断](/dashboard/dashboard-diagnostics-access.md) (v4.0 で導入)
-   [継続的なプロファイリング](/dashboard/continuous-profiling.md) (v5.3 で導入)
-   [オンラインの安全でない回復](/online-unsafe-recovery.md) (v5.3 で導入)
-   [Top SQL](/dashboard/top-sql.md) (v5.4 で導入)
