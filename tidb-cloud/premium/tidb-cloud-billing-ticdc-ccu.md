---
title: Changefeed Billing for TiDB Cloud Premium
summary: TiDB Cloud Premiumにおける変更フィードの課金について学びましょう。
---

# TiDB Cloud Premium の課金に関する変更履歴 {#changefeed-billing-for-tidb-cloud-premium}

このドキュメントでは、TiDB Cloud Premiumにおける変更フィードの請求詳細について説明します。

## CCUコスト {#ccu-cost}

TiDB Cloud Premium は、TiCDC Changefeed Capacity Unit (CCU) の[変更フィード](/tidb-cloud/changefeed-overview.md)の容量を測定します。インスタンスの[変更フィードを作成する](/tidb-cloud/changefeed-overview.md#create-a-changefeed)ときに、適切な仕様を選択できます。 CCU が高いほど、レプリケーションのパフォーマンスが向上します。これらの TiCDC CCU に対して料金が発生します。

### TiCDC CCUの数 {#number-of-ticdc-ccus}

以下の表は、変更フィードの仕様とそれに対応するレプリケーション性能を示しています。

| 仕様            | 最大レプリケ​​ーション性能 |
| ------------- | -------------- |
| CCU 2室        | 5,000行/秒       |
| CCU 4室        | 10,000行/秒      |
| CCU 8室        | 20,000行/秒      |
| 16のCCU        | 40,000行/秒      |
| 24のCCU        | 60,000行/秒      |
| 32のCCU        | 80,000行/秒      |
| CCU（集中治療室）40室 | 10万行/秒         |
| 64のCCU        | 16万行/秒         |
| 96のCCU        | 24万行/秒         |
| 128のCCU       | 32万行/秒         |
| 192のCCU       | 48万行/秒         |
| 256のCCU       | 64万行/秒         |
| 320のCCU       | 80万行/秒         |
| 384のCCU       | 96万行/秒         |

> **注記：**
>
> 上記のパフォーマンスデータは参考値であり、状況によって異なる場合があります。本番環境でchangefeed機能を使用する前に、実際のワークロードテストを実施することを強くお勧めします。さらにサポートが必要な場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

### 価格 {#price}

現在、 TiDB Cloud Premium はパブリック プレビュー段階にあります。詳細については、 [TiDB Cloud Premiumの料金詳細](https://www.pingcap.com/tidb-cloud-premium-pricing-details/)を参照してください。

## プライベートデータリンクの費用 {#private-data-link-cost}

**プライベートリンク**または**プライベートサービスコネクトの**ネットワーク接続方法を選択した場合、追加の**プライベートデータリンク**料金が発生します。これらの料金は[データ転送コスト](https://www.pingcap.com/tidb-dedicated-pricing-details/#data-transfer-cost)カテゴリに分類されます。

**Private Data Link**の価格は**$0.01/GiB**で、 [AWS Interface Endpoint の料金](https://aws.amazon.com/privatelink/pricing/#Interface_Endpoint_pricing)の**データ処理の**料金、Google Cloud Private Service Connect の**コンシューマ データ処理の**[Google Cloud Private Service Connect の料金](https://cloud.google.com/vpc/pricing#psc-forwarding-rules)、Azure Private Link の**インバウンド/アウトバウンド データ処理**[Azure Private Link の価格](https://azure.microsoft.com/en-us/pricing/details/private-link/)と同じです。
