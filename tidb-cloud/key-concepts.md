---
title: Overview of Key Concepts
summary: TiDB Cloudの主要な概念について学習します。
---

# 主要概念の概要 {#overview-of-key-concepts}

このドキュメントでは、 [TiDB Cloud](https://www.pingcap.com/tidb-cloud/)の主要な概念の概要を説明します。これらの概念を理解することで、 TiDB Cloud の機能をより効果的に活用できるようになります。

## アーキテクチャ {#architecture}

TiDB Cloud は、コンピューティングとstorageを分離し、弾力的なスケーリングと高可用性を実現するクラウドネイティブの分散アーキテクチャ上に構築されています[TiDB Cloudアーキテクチャの詳細](/tidb-cloud/architecture-concepts.md) 。

## データベーススキーマ {#database-schema}

TiDB Cloud を使用すると、データベース、テーブル、列、インデックス、制約などのオブジェクトを使用してデータを整理および構造化できます。また、一時テーブル、ベクターインデックス、キャッシュテーブルなどの高度な機能もサポートしています[データベーススキーマの詳細](/tidb-cloud/database-schema-concepts.md) 。

## 取引 {#transactions}

TiDB は完全な分散トランザクションを提供し、モデル[取引について詳しくはこちら](/tidb-cloud/transaction-concepts.md) [Google パーコレーター](https://research.google.com/pubs/pub36726.html)基づいたいくつかの最適化が施されています。

## SQL {#sql}

TiDB は、MySQL プロトコルおよびMySQL 5.7と MySQL 8.0.1 の共通機能と構文と高い互換性があります[TiDB Cloudの SQL について詳しく見る](/tidb-cloud/sql-concepts.md)

## AI機能 {#ai-features}

TiDB Cloudの AI 機能を使用すると、データの探索、検索、統合のための高度なテクノロジーを最大限に活用できます[AI機能について詳しくはこちら](/tidb-cloud/ai-feature-concepts.md) 。

## データサービス（ベータ版） {#data-service-beta}

データ サービスを使用すると、カスタム API エンドポイントを使用して HTTPS リクエスト経由でTiDB Cloudデータにアクセスできます[データサービスの詳細](/tidb-cloud/data-service-concepts.md) 。

## スケーラビリティ {#scalability}

TiDB Cloud Dedicated を使用すると、データ量やワークロードの変化に合わせてコンピューティング リソースとstorageリソースを個別に調整できます[スケーラビリティについて詳しく見る](/tidb-cloud/scalability-concepts.md) 。

## 高可用性 {#high-availability}

TiDB Cloud は、 TiDB Cloud Serverless クラスターとTiDB Cloud Dedicated クラスターの両方で高可用性を保証します。

-   [TiDB Cloud Serverless の高可用性](/tidb-cloud/serverless-high-availability.md)
-   [TiDB Cloud専用における高可用性](/tidb-cloud/high-availability-with-multi-az.md)

## 監視 {#monitoring}

TiDB Cloud は、クラスターのパフォーマンスと健全性を包括的に監視する機能を提供します[監視について詳しくはこちら](/tidb-cloud/monitoring-concepts.md) 。

## データストリーミング {#data-streaming}

TiDB Cloud を使用すると、TiDB クラスタからのデータ変更を Kafka、MySQL、オブジェクトstorageなどの他のシステムにストリーミングできます[データストリーミングの詳細](/tidb-cloud/data-streaming-concepts.md) 。

## バックアップと復元 {#backup-x26-restore}

TiDB Cloud は、自動バックアップ ソリューションとポイントインタイム リカバリ (PITR) 機能を提供します[バックアップと復元の詳細](/tidb-cloud/backup-and-restore-concepts.md) 。

## Security {#security}

TiDB Cloud は、データを保護し、アクセス制御を強化し、最新のコンプライアンス標準を満たすように設計された、堅牢で柔軟なセキュリティ フレームワークを提供します[セキュリティについて詳しくはこちら](/tidb-cloud/security-concepts.md) 。
