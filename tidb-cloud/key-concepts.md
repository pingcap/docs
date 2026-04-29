---
title: Overview of Key Concepts
summary: TiDB Cloudの主要な概念について学びましょう。
---

# 主要概念の概要 {#overview-of-key-concepts}

このドキュメントでは[TiDB Cloud](https://www.pingcap.com/tidb-cloud/)の主要な概念の概要を説明します。これらの概念を理解することで、 TiDB Cloud の機能をより効果的に活用できるようになります。

## アーキテクチャ {#architecture}

TiDB Cloudは、コンピューティングをstorageから分離するクラウドネイティブの分散アーキテクチャ上に構築されており、柔軟なスケーリングと高可用性を実現します。 [TiDB Cloudアーキテクチャの詳細についてはこちらをご覧ください。](/tidb-cloud/architecture-concepts.md)

## データベーススキーマ {#database-schema}

TiDB Cloudを使用すると、データベース、テーブル、列、インデックス、制約などのオブジェクトを使用してデータを整理および構造化できます。また、一時テーブル、ベクター インデックス、キャッシュされたテーブルなどの高度な機能もサポートしています。[データベーススキーマについて詳しくはこちらをご覧ください](/tidb-cloud/database-schema-concepts.md)。

## 取引 {#transactions}

TiDB は完全な分散トランザクションを提供し、モデルには[Googleパーコレーター](https://research.google.com/pubs/pub36726.html)に基づいていくつかの最適化が施さ[取引について詳しくはこちらをご覧ください](/tidb-cloud/transaction-concepts.md)ています。

## SQL {#sql}

TiDB は、MySQL プロトコル、およびMySQL 5.7および MySQL 8.0 の共通機能および構文と高い互換性があります。 [TiDB Cloudの SQL について詳しくはこちらをご覧ください。](/tidb-cloud/sql-concepts.md)

## AI機能 {#ai-features}

TiDB Cloudの AI 機能を使用すると、データの探索、検索、統合に高度なテクノロジーを最大限に活用できます。 [AI機能について詳しくはこちらをご覧ください](/tidb-cloud/ai-feature-concepts.md)。

## データサービス（ベータ版） {#data-service-beta}

データ サービスを使用すると、カスタム API エンドポイントを使用して HTTPS リクエスト経由でTiDB Cloudデータにアクセスできます。データ サービス[データサービスについて詳しくはこちらをご覧ください](/tidb-cloud/data-service-concepts.md)。

## 拡張性 {#scalability}

TiDB Cloud Dedicated を使用すると、データ量やワークロードの変化に合わせてコンピューティング リソースとstorageリソースを個別に調整できます。[拡張性について詳しくはこちらをご覧ください](/tidb-cloud/scalability-concepts.md)。

## 高可用性 {#high-availability}

TiDB Cloudは、サポートされているすべてのプランで高い可用性を保証します。

-   TiDB Cloud Starter、 TiDB Cloud Essential、およびTiDB Cloud Premium については、[TiDB Cloudにおける高可用性](/tidb-cloud/serverless-high-availability.md)を参照してください。
-   TiDB Cloud Dedicatedについては、 [TiDB Cloud Dedicatedにおける高可用性](/tidb-cloud/high-availability-with-multi-az.md)を参照してください。

## 監視 {#monitoring}

TiDB Cloudは、TiDB のパフォーマンスと健全性の包括的なモニタリング機能を提供します。モニタリング[モニタリングについて詳しくはこちらをご覧ください](/tidb-cloud/monitoring-concepts.md)。

## データストリーミング {#data-streaming}

TiDB Cloud を使用すると、データ変更を Kafka、MySQL、オブジェクトstorageなどの他のシステムにストリーミングできます。データ ストリーミング[データストリーミングについて詳しくはこちらをご覧ください](/tidb-cloud/data-streaming-concepts.md)。

## バックアップと復元 {#backup-x26-restore}

TiDB Cloudは [バックアップと復元について詳しくはこちらをご覧ください](/tidb-cloud/backup-and-restore-concepts.md)自動バックアップ ソリューションとポイントインタイムリカバリ(PITR) 機能を提供します。

## Security {#security}

TiDB Cloudは、データを保護し、アクセス制御を実施し、最新のコンプライアンス基準を満たすように設計された、堅牢かつ柔軟なセキュリティ フレームワークを提供します。セキュリティ[セキュリティについて詳しくはこちらをご覧ください](/tidb-cloud/security-concepts.md)。
