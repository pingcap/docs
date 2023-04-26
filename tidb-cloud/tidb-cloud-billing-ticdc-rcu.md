---
title: Changefeed Billing
summary: Learn about billing for changefeeds in TiDB Cloud.
aliases: ['/tidbcloud/tidb-cloud-billing-tcu']
---

# チェンジフィード請求 {#changefeed-billing}

TiDB Cloud は、 TiCDC Replication Capacity Units (RCU) で[チェンジフィード](/tidb-cloud/changefeed-overview.md)の容量を測定します。クラスターの[チェンジフィードを作成する](/tidb-cloud/changefeed-overview.md#create-a-changefeed)は、適切な仕様を選択できます。 RCU が高いほど、レプリケーションのパフォーマンスが向上します。これらの TiCDC changefeed RCU に対して課金されます。

## TiCDC RCU の数 {#number-of-ticdc-rcus}

次の表に、changefeeds の仕様と対応するレプリケーション パフォーマンスを示します。

| 仕様      | 最大のレプリケーション パフォーマンス |
| ------- | ------------------- |
| 2つのRCU  | 5,000 行/秒           |
| 4つのRCU  | 10,000 行/秒          |
| 8つのRCU  | 20,000 行/秒          |
| 16個のRCU | 40,000 行/秒          |
| 24個のRCU | 60,000 行/秒          |
| RCU 32台 | 80,000 行/秒          |
| 40RCU   | 100,000 行/秒         |

> **ノート：**
>
> 上記のパフォーマンス データは参考用であり、シナリオによって異なる場合があります。

## 価格 {#price}

サポートされているリージョンと各 TiCDC RCU のTiDB Cloudの価格については、 [変更フィードのコスト](https://www.pingcap.com/tidb-cloud-pricing-details/#changefeed-cost)を参照してください。
