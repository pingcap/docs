---
title: Changefeed Billing
summary: Learn about billing for changefeeds in TiDB Cloud.
---

# 変更フィード請求 {#changefeed-billing}

TiDB Cloudは、 TiCDC レプリケーション キャパシティ ユニット (RCU) で[変更フィード](/tidb-cloud/changefeed-overview.md)のキャパシティを測定します。クラスタの[変更フィードを作成する](/tidb-cloud/changefeed-overview.md#create-a-changefeed)は、適切な仕様を選択できます。 RCU が高いほど、レプリケーションのパフォーマンスが向上します。これらの TiCDC 変更フィード RCU に対して料金が発生します。

## TiCDC RCU の数 {#number-of-ticdc-rcus}

次の表に、変更フィードの仕様と対応するレプリケーション パフォーマンスを示します。

| 仕様     | 最大のレプリケーションパフォーマンス |
| ------ | ------------------ |
| 2 RCU  | 5,000行/秒           |
| 4 RCU  | 10,000行/秒          |
| 8 RCU  | 20,000行/秒          |
| 16 RCU | 40,000行/秒          |
| 24 RCU | 60,000行/秒          |
| 32 RCU | 80,000行/秒          |
| 40 RCU | 100,000行/秒         |

> **注記：**
>
> 上記のパフォーマンス データは参照のみを目的としており、シナリオによって異なる場合があります。

## 価格 {#price}

各 TiCDC RCU のサポートされるリージョンとTiDB Cloudの価格については、 [変更フィードのコスト](https://www.pingcap.com/tidb-cloud-pricing-details/#changefeed-cost)を参照してください。
