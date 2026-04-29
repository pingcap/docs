---
title: TiDB Cloud API v1beta2 Overview
summary: TiDB Cloudのv1beta2 APIについて学びましょう。
---

# TiDB CloudAPI v1beta2 の概要 {#tidb-cloud-api-v1beta2-overview}

TiDB Cloud API v1beta2は、 [TiDB Cloudプレミアム](/tidb-cloud/select-cluster-tier.md#premium)インスタンスおよび関連リソースをプログラムから管理できるRESTful APIです。

現在、 TiDB Cloud Premium のリソースを管理するには、以下の v1beta2 API を使用できます。

-   [TiDB Cloud Premium API](https://docs.pingcap.com/tidbcloud/api/v1beta2/premium) ： TiDB Cloud Premiumインスタンス、バックアップ、リージョンを管理します。このAPIには以下のリソースが含まれています。

    -   **TiDB Cloud Premiumインスタンス**：パスワード、CA証明書、クラウドプロバイダー情報など、 TiDB Cloud Premiumインスタンスのライフサイクルと構成を管理します。
    -   **バックアップ**： TiDB Cloud Premiumインスタンスのバックアップを管理します。バックアップベースのリストア機能も含まれます。
    -   **リージョン**： TiDB Cloud Premiumインスタンスを作成するために利用可能なリージョンを取得します。
