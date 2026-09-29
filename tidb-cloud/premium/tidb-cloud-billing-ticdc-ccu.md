---
title: Changefeed Billing for {{{ .essential }}} and Premium
summary: "{{{ .essential }}} と Premium における変更フィードの課金について学びましょう。"
---

# {{{ .essential }}} と Premium の変更フィードの課金 {#changefeed-billing-for-tidb-cloud-premium}

このドキュメントでは、{{{ .essential }}} と Premium における変更フィードの請求詳細について説明します。

## CCUコスト {#ccu-cost}

{{{ .essential }}} と Premium は、[変更フィード](/tidb-cloud/changefeed-overview.md)のキャパシティを TiCDC Changefeed Capacity Unit (CCU) 単位で測定します。インスタンスの[変更フィードを作成する](/tidb-cloud/changefeed-overview.md#create-a-changefeed)ときに、適切な仕様を選択できます。 CCU が高いほど、レプリケーションのパフォーマンスが向上します。これらの TiCDC CCU に対して料金が発生します。

### TiCDC CCUの数 {#number-of-ticdc-ccus}

以下の表は、変更フィードの仕様とそれに対応するレプリケーション性能を示しています。

| 仕様            | 最大レプリケーション性能 |
| ------------- | -------------- |
| 2 CCU         | 5,000行/秒       |
| 4 CCU         | 10,000行/秒      |
| 8 CCU         | 20,000行/秒      |
| 16 CCU        | 40,000行/秒      |
| 24 CCU        | 60,000行/秒      |
| 32 CCU        | 80,000行/秒      |
| 40 CCU        | 10万行/秒         |
| 64 CCU        | 16万行/秒         |
| 96 CCU        | 24万行/秒         |
| 128 CCU       | 32万行/秒         |
| 192 CCU       | 48万行/秒         |
| 256 CCU       | 64万行/秒         |
| 320 CCU       | 80万行/秒         |
| 384 CCU       | 96万行/秒         |

> **Note:**
>
> 上記のパフォーマンスデータは参考値であり、状況によって異なる場合があります。本番環境でchangefeed機能を使用する前に、実際のワークロードテストを実施することを強くお勧めします。さらにサポートが必要な場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

### 価格 {#price}

現在、 {{{ .essential }}} と Premium はパブリックプレビュー段階にあります。価格の詳細については、以下のページを参照してください:

- [{{{ .essential }}} の料金詳細](https://www.pingcap.com/tidb-cloud-essential-pricing-details/)
- [{{{ .premium }}} の料金詳細](https://www.pingcap.com/tidb-cloud-premium-pricing-details/)

## プライベートデータリンクの費用 {#private-data-link-cost}

**Private Link**または**Private Service Connect**ネットワーク接続方法を選択した場合、追加の**Private Data Link**料金が発生します。これらの料金は[データ転送コスト](https://www.pingcap.com/tidb-dedicated-pricing-details/#data-transfer-cost)カテゴリに分類されます。

**Private Data Link**の価格は**$0.01/GiB**で、AWS Interface Endpoint の**Data Processed**の[AWS Interface Endpoint の料金](https://aws.amazon.com/privatelink/pricing/#Interface_Endpoint_pricing)、Google Cloud Private Service Connect の**Consumer data processing**の[Google Cloud Private Service Connect の料金](https://cloud.google.com/vpc/pricing#psc-forwarding-rules)、Azure Private Link の**Inbound/Outbound Data Processed**の[Azure Private Link の価格](https://azure.microsoft.com/en-us/pricing/details/private-link/)と同じです。
