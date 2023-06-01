---
title: Changefeed Billing
summary: Learn about billing for changefeeds in TiDB Cloud.
---

# 変更フィード請求 {#changefeed-billing}

TiDB Cloud は、変更フィードの容量を TiCDC レプリケーション キャパシティ ユニット (RCU) で測定します。クラスターの最初の変更フィードを作成すると、 TiDB Cloudによって自動的に TiCDC RCU がセットアップされ、これらの TiCDC RCU に対して料金が発生します。単一クラスター内に作成されたすべての変更フィードは、同じ TiCDC RCU を共有します。

## TiCDC RCU の数 {#number-of-ticdc-rcus}

TiDB クラスターごとに、TiCDC RCU の数は、クラスター内のすべての TiKV ノードの合計 vCPU 数に応じてTiDB Cloudによって次のように設定されます。

| すべての TiKV ノードの vCPU の合計                     | RCUの数 |
| ------------------------------------------- | ----- |
| &lt; 48                                     | 16    |
| <blockquote>= 48、かつ &lt; 120</blockquote>   | 24    |
| <blockquote>= 120、かつ &lt;= 168</blockquote> | 32    |
| <blockquote>168</blockquote>                | 40    |

## 価格 {#price}

次の表に、各 TiCDC RCU のTiDB Cloudの価格を示します。

| クラウドプロバイダー | リージョン                   | RCU 価格 ($/時間) |
| ---------- | ----------------------- | ------------- |
| AWS        | オレゴン州 (us-west-2)       | $0.1307       |
| AWS        | バージニア北部 (us-east-1)     | $0.1307       |
| AWS        | ムンバイ (ap-south-1)       | $0.1393       |
| AWS        | シンガポール (ap-southeast-1) | $0.1623       |
| AWS        | 東京 (ap-northeast-1)     | $0.1669       |
| AWS        | フランクフルト (EU-central-1)  | $0.1564       |
| GCP        | オレゴン州 (us-west1)        | $0.1452       |
| GCP        | バージニア北部 (us-east4)      | $0.1626       |
| GCP        | アイオワ州 (us-central1)     | $0.1452       |
| GCP        | シンガポール (アジア南東1)         | $0.1746       |
| GCP        | 台湾 (アジア東1)              | $0.1628       |
| GCP        | 東京 (アジア北東1)             | $0.1868       |
| GCP        | 大阪（アジア東北2）              | $0.1868       |
