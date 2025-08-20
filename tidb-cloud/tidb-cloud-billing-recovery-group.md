---
title: Recovery Group Billing
summary: TiDB Cloudのリカバリ グループの課金について説明します。
---

# リカバリグループ請求 {#recovery-group-billing}

TiDB Cloudは、リカバリグループのプライマリクラスターにデプロイされたTiKVノードのサイズに基づいて、リカバリグループの料金を請求します。クラスターを[回復グループを作成する](/tidb-cloud/recovery-group-get-started.md)アップグレードする際に、リカバリグループのプライマリクラスターを選択できます。TiKV構成が大きいほど、リカバリグループの保護コストが高くなります。

TiDB Cloud、データ処理もGiB単位で課金されます。データ処理料金は、データが別のリージョンのセカンダリクラスターに複製されるか、同じリージョン内で複製されるかによって異なります。

## 価格 {#pricing}

TiDB Cloudリカバリ グループがサポートされているリージョンと価格については、 [回復グループコスト](https://www.pingcap.com/tidb-dedicated-pricing-details/#recovery-group-cost)参照してください。
