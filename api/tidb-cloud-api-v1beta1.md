---
title: TiDB Cloud API v1beta1 Overview
summary: TiDB Cloudの v1beta1 API について学習します。
---

# TiDB CloudAPI v1beta1 の概要 {#tidb-cloud-api-v1beta1-overview}

TiDB Cloud API v1beta1 は、 TiDB Cloud内の管理オブジェクトをプログラム的に管理するためのアクセスを提供する RESTful API です。この API を使用すると、クラスタレベルのリソース（クラスタやブランチなど）や組織レベルまたはプロジェクトレベルのリソース（課金、データサービス、 IAMなど）を自動的かつ効率的に管理できます。

現在、次の v1beta1 API を使用してTiDB Cloud内のリソースを管理できます。

-   クラスターレベルのリソース:
    -   [TiDB Cloud Starter または Essential クラスタ](https://docs.pingcap.com/tidbcloud/api/v1beta1/serverless) : TiDB Cloud Starter または Essential クラスターのクラスター、ブランチ、データ エクスポート タスク、およびデータ インポート タスクを管理します。
    -   [TiDB Cloud専用クラスタ](https://docs.pingcap.com/tidbcloud/api/v1beta1/dedicated) : TiDB Cloud Dedicated クラスターのクラスター、リージョン、プライベート エンドポイント接続、およびデータ インポート タスクを管理します。
-   組織またはプロジェクトレベルのリソース:
    -   [請求する](https://docs.pingcap.com/tidbcloud/api/v1beta1/billing) : TiDB Cloudクラスターの課金を管理します。
    -   [データサービス](https://docs.pingcap.com/tidbcloud/api/v1beta1/dataservice) : TiDB Cloudクラスターのデータ サービス内のリソースを管理します。
    -   [IAMは](https://docs.pingcap.com/tidbcloud/api/v1beta1/iam) : TiDB Cloudクラスターの API キーを管理します。
    -   [MSP（非推奨）](https://docs.pingcap.com/tidbcloud/api/v1beta1/msp)
