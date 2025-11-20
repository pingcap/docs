---
title: Changefeed Billing for TiDB Cloud Premium
summary: TiDB Cloud Premium の変更フィードに対する課金について説明します。
---

# TiDB Cloud Premium の Changefeed 課金 {#changefeed-billing-for-tidb-cloud-premium}

このドキュメントでは、TiDB Cloud Premium の変更フィードの課金の詳細について説明します。

## CCUコスト {#ccu-cost}

TiDB Cloud Premiumは、 [チェンジフィード](/tidb-cloud/changefeed-overview.md)をTiCDC Changefeed Capacity Units（CCU）で測定します。インスタンスを[チェンジフィードを作成する](/tidb-cloud/changefeed-overview.md#create-a-changefeed)にすると、適切な仕様を選択できます。CCUが高いほど、レプリケーションのパフォーマンスが向上します。これらのTiCDC CCUに対して料金が発生します。

### TiCDC CCUの数 {#number-of-ticdc-ccus}

次の表は、変更フィードの仕様と対応するレプリケーション パフォーマンスを示しています。

| 仕様      | 最大のレプリケーションパフォーマンス |
| ------- | ------------------ |
| 2台のCCU  | 5,000行/秒           |
| 4つのCCU  | 10,000行/秒          |
| 8つのCCU  | 20,000行/秒          |
| 16台のCCU | 40,000行/秒          |
| 24台のCCU | 60,000行/秒          |
| 32台のCCU | 80,000行/秒          |
| 40 CCU  | 100,000行/秒         |
| 64 CCU  | 160,000行/秒         |
| 96 CCU  | 240,000行/秒         |
| 128 CCU | 320,000行/秒         |
| 192 CCU | 480,000行/秒         |
| 256 CCU | 640,000行/秒         |
| 320 CCU | 80万行/秒             |
| 384 CCU | 960,000行/秒         |

> **注記：**
>
> 上記のパフォーマンスデータは参考用であり、シナリオによって異なる場合があります。本番環境でChangeFeed機能を使用する前に、実際のワークロードテストを実施することを強くお勧めします。ご不明な点がございましたら、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

### 価格 {#price}

現在、 TiDB Cloud Premium はプライベートプレビュー段階です。価格の詳細については[営業担当にお問い合わせください](https://www.pingcap.com/contact-us/)ご覧ください。

## プライベートデータリンクのコスト {#private-data-link-cost}

**プライベートリンク**または**プライベートサービスコネクトの**ネットワーク接続方法を選択した場合、追加の**プライベートデータリンク**料金が発生します。これらの料金は[データ転送コスト](https://www.pingcap.com/tidb-dedicated-pricing-details/#data-transfer-cost)カテゴリに該当します。

**プライベート データ リンク**の料金は**$0.01/GiB**で、**データ処理量**[AWS インターフェースエンドポイントの料金](https://aws.amazon.com/privatelink/pricing/#Interface_Endpoint_pricing) 、**コンシューマー データ処理**量[Google Cloud プライベート サービス コネクトの料金](https://cloud.google.com/vpc/pricing#psc-forwarding-rules) 、**受信/送信データ処理量**[Azure Private Link の料金](https://azure.microsoft.com/en-us/pricing/details/private-link/)と同じです。
