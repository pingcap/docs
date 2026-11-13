---
title: TiDB Cloud API v1beta2 Overview
summary: TiDB Cloudのv1beta2 APIについて学びましょう。
---

# TiDB Cloud API v1beta2 の概要 {#tidb-cloud-api-v1beta2-overview}

TiDB Cloud API v1beta2は、 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential)インスタンス（TiDB バージョン `CLOUD.202603.x` 以降を実行しているもの）、 [TiDB Cloud Premium](/tidb-cloud/select-cluster-tier.md#premium)インスタンス、および関連リソースをプログラムから管理できるRESTful APIです。

> **Note:**
>
> TiDB v8.5.3 以前を実行している TiDB Cloud Essential インスタンスについては、代わりに [v1beta1 API](/api/tidb-cloud-api-v1beta1.md) を使用してください。

特に指定がない限り、このページでの「TiDB Cloud インスタンス」は、TiDB Cloud Premium インスタンスまたはサポートされている TiDB Cloud Essential インスタンスのいずれかを指します。

[TiDB Cloud API v1beta2 リファレンス](https://docs.pingcap.com/tidbcloud/api/v1beta2/) には、以下のリソースを管理するためのエンドポイントが用意されています。

- **TiDB Cloud インスタンス**：パスワード、CA証明書、クラウドプロバイダー情報など、TiDB Cloud インスタンスのライフサイクルと設定を管理します。
- **バックアップ**：TiDB Cloud インスタンスのバックアップを管理します。バックアップベースのリストア機能も含まれます。
- **Changefeed**：TiDB Cloud changefeed のライフサイクルと設定を管理します。
- **リージョン**：TiDB Cloud インスタンスを作成するために利用可能なリージョンを取得します。
