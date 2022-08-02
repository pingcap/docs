---
title: Changefeed Billing
summary: Learn about billing for changefeeds in TiDB Cloud.
---

# チェンジフィード請求 {#changefeed-billing}

TiDB Cloudは、変更フィードの容量を TiCDC 容量単位 (TCU) で測定します。クラスタの最初の変更フィードを作成すると、 TiDB Cloudは TiCDC キャパシティー ユニット (TCU) を自動的にセットアップし、これらの TiCDC キャパシティー ユニットに対して課金されます。 1 つのクラスタで作成されたすべての変更フィードは、同じ TiCDC キャパシティー ユニットを共有します。

## TiCDC キャパシティーユニットの数 {#number-of-ticdc-capacity-units}

TiDBクラスタごとに、クラスタ内のすべての TiKV ノードの合計 vCPU 数に従って、TiCDC キャパシティー ユニットの数がTiDB Cloudによって次のように設定されます。

| すべての TiKV ノードの合計 vCPU | TCUの数 |
| --------------------- | ----- |
| &lt; 48               | 16    |
| = 48、および &lt; 120     | 24    |
| = 120、および &lt;= 168   | 32    |
| 168                   | 40    |

## 価格 {#price}

次の表に、各 TiCDC キャパシティ ユニット (TCU) のTiDB Cloudの価格を示します。

| クラウド プロバイダー | リージョン                    | TCU 料金 ($/時) |
| ----------- | ------------------------ | ------------ |
| AWS         | オレゴン (us-west-2)         | $0.1307      |
| AWS         | 北バージニア (us-east-1)       | $0.1307      |
| AWS         | ムンバイ (ap-south-1)        | $0.1393      |
| AWS         | シンガポール (ap-southeast-1)  | $0.1623      |
| AWS         | 東京 (ap-northeast-1)      | $0.1669      |
| AWS         | フランクフルト (eu-central-1)   | $0.1564      |
| GCP         | オレゴン (us-west1)          | $0.1452      |
| GCP         | アイオワ (us-central1)       | $0.1452      |
| GCP         | シンガポール (asia-southeast1) | $0.1746      |
| GCP         | 台湾 (asia-east1)          | $0.1628      |
| GCP         | 東京 (asia-northeast1)     | $0.1868      |
