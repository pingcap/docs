---
title: Changefeed Billing
summary: Learn about billing for changefeeds in TiDB Cloud.
aliases: ['/tidbcloud/tidb-cloud-billing-tcu']
---

# チェンジフィード請求 {#changefeed-billing}

TiDB Cloud は、 TiCDC Replication Capacity Units (RCU) で変更フィードの容量を測定します。クラスターの最初の変更フィードを作成すると、 TiDB Cloud が自動的に TiCDC RCU をセットアップし、これらの TiCDC RCU に対して課金されます。 1 つのクラスターで作成されたすべての変更フィードは、同じ TiCDC RCU を共有します。

## TiCDC RCU の数 {#number-of-ticdc-rcus}

TiDB クラスターごとに、クラスター内のすべての TiKV ノードの合計 vCPU 数に応じて、TiCDC RCU の数がTiDB Cloudによって次のように設定されます。

| すべての TiKV ノードの合計 vCPU | RCUの数 |
| --------------------- | ----- |
| &lt; 48               | 16    |
| = 48、および &lt; 120     | 24    |
| = 120、および &lt;= 168   | 32    |
| 168                   | 40    |

## 価格 {#price}

次の表に、TiCDC RCU ごとのTiDB Cloudの価格を示します。

| クラウド プロバイダー | リージョン                    | RCU 料金 ($/時間) |
| ----------- | ------------------------ | ------------- |
| AWS         | オレゴン (us-west-2)         | $0.1307       |
| AWS         | 北バージニア (us-east-1)       | $0.1307       |
| AWS         | ムンバイ (ap-south-1)        | $0.1393       |
| AWS         | シンガポール (ap-southeast-1)  | $0.1623       |
| AWS         | 東京 (ap-northeast-1)      | $0.1669       |
| AWS         | フランクフルト (eu-central-1)   | $0.1564       |
| GCP         | オレゴン (us-west1)          | $0.1452       |
| GCP         | 北バージニア (us-east4)        | $0.1626       |
| GCP         | アイオワ (us-central1)       | $0.1452       |
| GCP         | シンガポール (asia-southeast1) | $0.1746       |
| GCP         | 台湾 (asia-east1)          | $0.1628       |
| GCP         | 東京 (asia-northeast1)     | $0.1868       |
| GCP         | 大阪 (asia-northeast2)     | $0.1868       |
