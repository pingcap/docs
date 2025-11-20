---
title: Changefeed Billing for TiDB Cloud Dedicated
summary: TiDB Cloudの変更フィードに対する課金について説明します。
aliases: ['/tidbcloud/tidb-cloud-billing-tcu']
---

# TiDB Cloud DedicatedのChangefeed課金 {#changefeed-billing-for-tidb-cloud-dedicated}

このドキュメントでは、TiDB Cloud Dedicated の変更フィードの課金の詳細について説明します。

## RCUコスト {#rcu-cost}

TiDB Cloud Dedicatedは、TiCDCレプリケーション容量ユニット（RCU）を[チェンジフィード](/tidb-cloud/changefeed-overview.md)として容量を測定します。クラスターに[チェンジフィードを作成する](/tidb-cloud/changefeed-overview.md#create-a-changefeed)設定すると、適切な仕様を選択できます。RCUが大きいほど、レプリケーションパフォーマンスが向上します。これらのTiCDC変更フィードRCUに対して料金が発生します。

### TiCDC RCUの数 {#number-of-ticdc-rcus}

次の表は、変更フィードの仕様と対応するレプリケーション パフォーマンスを示しています。

| 仕様      | 最大のレプリケーションパフォーマンス |
| ------- | ------------------ |
| 2台のRCU  | 5,000行/秒           |
| 4つのRCU  | 10,000行/秒          |
| 8 RCU   | 20,000行/秒          |
| 16 RCU  | 40,000行/秒          |
| 24 RCU  | 60,000行/秒          |
| 32 RCU  | 80,000行/秒          |
| 40 RCU  | 100,000行/秒         |
| 64 RCU  | 160,000行/秒         |
| 96 RCU  | 240,000行/秒         |
| 128 RCU | 320,000行/秒         |
| 192 RCU | 480,000行/秒         |
| 256 RCU | 640,000行/秒         |
| 320 RCU | 80万行/秒             |
| 384 RCU | 960,000行/秒         |

> **注記：**
>
> 上記のパフォーマンスデータは参考用であり、シナリオによって異なる場合があります。本番環境でChangeFeed機能を使用する前に、実際のワークロードテストを実施することを強くお勧めします。ご不明な点がございましたら、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

### 価格 {#price}

各 TiCDC RCU でサポートされているリージョンとTiDB Cloudの価格については、 [チェンジフィードコスト](https://www.pingcap.com/tidb-dedicated-pricing-details/#changefeed-cost)参照してください。

## プライベートデータリンクのコスト {#private-data-link-cost}

**プライベートリンク**または**プライベートサービスコネクトの**ネットワーク接続方法を選択した場合、追加の**プライベートデータリンク**料金が発生します。これらの料金は[データ転送コスト](https://www.pingcap.com/tidb-dedicated-pricing-details/#data-transfer-cost)カテゴリに該当します。

**プライベート データ リンク**の料金は**$0.01/GiB**で、**データ処理量**[AWS インターフェースエンドポイントの料金](https://aws.amazon.com/privatelink/pricing/#Interface_Endpoint_pricing) 、**コンシューマー データ処理**量[Google Cloud プライベート サービス コネクトの料金](https://cloud.google.com/vpc/pricing#psc-forwarding-rules) 、**受信/送信データ処理量**[Azure Private Link の料金](https://azure.microsoft.com/en-us/pricing/details/private-link/)と同じです。
