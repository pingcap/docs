---
title: TiDB Experimental Features
summary: Learn the experimental features of TiDB.
---

# TiDBの実験的特徴 {#tidb-experimental-features}

このドキュメントでは、さまざまなバージョンのTiDBの実験的機能を紹介します。これらの機能を実稼働環境で使用することはお勧めし**ません**。

## パフォーマンス {#performance}

-   [TiFlashスレッドプールを自動的にスケーリングする](/tiflash/tiflash-configuration.md) 。 （v5.4で導入）
-   [Raft Engine](/tikv-configuration-file.md#raft-engine) 。 （v5.4で導入）
-   [`PREDICATE COLUMNS`の統計収集をサポート](/statistics.md#collect-statistics-on-some-columns) （v5.4で導入）
-   [統計の同期ロードをサポート](/statistics.md#load-statistics) 。 （v5.4で導入）

## 安定 {#stability}

-   TiFlashは、データの圧縮または並べ替えによってI / Oリソースの使用を制限し、バックグラウンドタスクとフロントエンドデータの読み取りおよび書き込みの間のI / Oリソースの競合を軽減します（v5.0で導入）
-   オプティマイザーによるインデックスの選択の安定性を向上させます（v5.0で導入）
    -   複数列の順序依存関係情報を収集して、統計機能を拡張します。
    -   `CMSKetch`とヒストグラムから`TopN`の値を削除し、各テーブルインデックスのヒストグラムバケットのNDV情報を追加するなど、統計モジュールをリファクタリングします。

## スケジューリング {#scheduling}

-   カスケード配置ルール機能。これは、PDがさまざまなタイプのデータに対応するスケジュールを生成するようにガイドするレプリカルールシステムです。さまざまなスケジューリングルールを組み合わせることで、レプリカの数、保存場所、ホストタイプ、Raft選挙に参加するかどうか、Raftリーダーとして機能するかどうかなど、任意の連続データ範囲の属性を細かく制御できます。詳細については、 [カスケード配置ルール](/configure-placement-rules.md)を参照してください。 （v4.0で導入）
-   エラスティックスケジューリング機能。これにより、TiDBクラスタがリアルタイムワークロードに基づいてKubernetesで動的にスケールアウトおよびスケールインできるようになり、アプリケーションのピーク時のストレスが効果的に軽減され、オーバーヘッドが節約されます。詳細については、 [TidbCluster自動スケーリングを有効にする](https://docs.pingcap.com/tidb-in-kubernetes/stable/enable-tidb-cluster-auto-scaling)を参照してください。 （v4.0で導入）

## SQL {#sql}

-   [SQLインターフェイスを使用して、データの配置ルールを設定します](/placement-rules-in-sql.md) （v5.3で導入）
-   リストパーティション（v5.0で導入）
-   COLUMNSパーティションの一覧表示（v5.0で導入）
-   [パーティションテーブルの動的プルーニングモード](/partitioned-table.md#dynamic-pruning-mode) 。 （v5.1で導入）
-   式インデックス機能。式インデックスは、関数ベースのインデックスとも呼ばれます。インデックスを作成する場合、インデックスフィールドは特定の列である必要はありませんが、1つ以上の列から計算された式にすることができます。この機能は、計算ベースのテーブルにすばやくアクセスするのに役立ちます。詳細については、 [式インデックス](/sql-statements/sql-statement-create-index.md)を参照してください。 （v4.0で導入）
-   [生成された列](/generated-columns.md) （v2.1で導入）
-   [ユーザー定義変数](/user-defined-variables.md) （v2.1で導入）
-   [JSONデータ型](/data-type-json.md)および[JSON関数](/functions-and-operators/json-functions.md) （v2.1で導入）
-   [意見](/information-schema/information-schema-views.md) （v2.1で導入）

## Configuration / コンフィグレーション管理 {#configuration-management}

-   構成パラメーターをPDに永続的に保存し、構成アイテムの動的な変更をサポートします。 （v4.0で導入）
-   [設定を表示](/sql-statements/sql-statement-show-config.md) （v4.0で導入）

## データ共有とサブスクリプション {#data-sharing-and-subscription}

-   [TiCDCをKafkaConnect（Confluent Platform）と統合する](/ticdc/integrate-confluent-using-ticdc.md) （v5.0で導入）

## 保管所 {#storage}

-   [タイタンを無効にする](/storage-engine/titan-configuration.md#disable-titan-experimental) （v4.0で導入）
-   [タイタンレベルマージ](/storage-engine/titan-configuration.md#level-merge-experimental) （v4.0で導入）
-   TiFlashは、ストレージエンジンの新しいデータを複数のハードドライブに分散して、I/O圧力を共有することをサポートしています。 （v4.0で導入）

## バックアップと復元 {#backup-and-restoration}

-   [RawKVをバックアップする](/br/use-br-command-line-tool.md#back-up-raw-kv-experimental-feature) （v3.1で導入）

## ガベージコレクション {#garbage-collection}

-   [グリーンGC](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50) （v5.0で導入）

## 診断 {#diagnostics}

-   [SQL診断](/information-schema/information-schema-sql-diagnostics.md) （v4.0で導入）
-   [クラスター診断](/dashboard/dashboard-diagnostics-access.md) （v4.0で導入）
-   [継続的なプロファイリング](/dashboard/continuous-profiling.md) （v5.3で導入）
-   [オンラインの安全でない回復](/online-unsafe-recovery.md) （v5.3で導入）
-   [Top SQL](/dashboard/top-sql.md) （v5.4で導入）
