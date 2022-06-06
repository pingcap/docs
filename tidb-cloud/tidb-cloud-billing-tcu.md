---
title: Changefeed Billing
summary: Learn about billing for changefeeds in TiDB Cloud.
---

# チェンジフィード請求 {#changefeed-billing}

TiDB Cloudは、TiCDCキャパシティユニット（TCU）でチェンジフィードのキャパシティを測定します。クラスタの最初のチェンジフィードを作成すると、TiDBクラウドは自動的にTiCDCキャパシティーユニット（TCU）をセットアップし、これらのTiCDCキャパシティーユニットの料金が請求されます。単一のクラスタで作成されたすべてのチェンジフィードは、同じTiCDCキャパシティーユニットを共有します。

## TiCDC容量ユニットの数 {#number-of-ticdc-capacity-units}

TiDBクラスタごとに、TiCDCキャパシティーユニットの数は、クラスタのすべてのTiKVノードの合計vCPU数に応じて、次のようにTiDBクラウドによって設定されます。

| すべてのTiKVノードの合計vCPU | TCUの数 |
| ------------------ | ----- |
| &lt;48             | 16    |
| = 48、および&lt;120    | 24    |
| = 120、および&lt;= 168 | 32    |
| 168                | 40    |

## 価格 {#price}

次の表に、各TiCDCキャパシティユニット（TCU）のTiDBクラウドの価格を示します。

| 領域                    | TCU価格（$ / hr） |
| --------------------- | ------------- |
| aws / us-west-2       | 0.1307ドル      |
| aws / us-east-1       | 0.1307ドル      |
| aws / ap-northeast-1  | 0.1669ドル      |
| aws / ap-southeast-1  | 0.1623ドル      |
| aws / eu-central-1    | 0.1564ドル      |
| aws / ap-south-1      | 0.1393ドル      |
| gcp / us-west1        | 0.1452ドル      |
| gcp / us-central1     | 0.1452ドル      |
| gcp / asia-northeast1 | 0.1868ドル      |
| gcp / asia-southeast1 | 0.1746ドル      |
