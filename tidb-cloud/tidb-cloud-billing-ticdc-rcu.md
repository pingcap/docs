---
title: Changefeed Billing
summary: Learn about billing for changefeeds in TiDB Cloud.
aliases: ['/tidbcloud/tidb-cloud-billing-tcu']
---

# チェンジフィード請求 {#changefeed-billing}

TiDB Cloudは、TiCDC Replication Capacity Units (RCU) で変更フィードの容量を測定します。クラスターの最初の変更フィードを作成すると、 TiDB Cloudが TiCDC RCU を自動的にセットアップし、これらの TiCDC RCU に対して課金されます。 1 つのクラスターで作成されたすべての変更フィードは、同じ TiCDC RCU を共有します。

## TiCDC RCU の数 {#number-of-ticdc-rcus}

TiDB クラスターごとに、クラスター内のすべての TiKV ノードの合計 vCPU 数に従って、TiCDC RCU の数がTiDB Cloudによって次のように設定されます。

| すべての TiKV ノードの合計 vCPU | RCUの数 |
| --------------------- | ----- |
| &lt; 48               | 16    |
| = 48、および &lt; 120     | 24    |
| = 120、および &lt;= 168   | 32    |
| 168                   | 40    |

## 価格 {#price}

サポートされているリージョンと各 TiCDC RCU のTiDB Cloudの価格については、 [変更フィードのコスト](https://www.pingcap.com/tidb-cloud-pricing-details/#changefeed-cost)を参照してください。
