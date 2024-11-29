---
title: Recovery Group Billing
summary: TiDB Cloudのリカバリ グループの課金について説明します。
---

# リカバリーグループ請求 {#recovery-group-billing}

TiDB Cloud は、リカバリ グループのプライマリ クラスターにデプロイされた TiKV ノードのサイズに基づいてリカバリ グループに対して課金します。クラスターを[回復グループを作成する](/tidb-cloud/recovery-group-get-started.md)にすると、リカバリ グループのプライマリ クラスターを選択できます。TiKV 構成が大きいほど、リカバリ グループの保護にかかるコストが高くなります。

TiDB Cloud、データ処理に対しても GiB 単位で課金されます。データ処理料金は、データが別のリージョンのセカンダリ クラスターに複製されるか、同じリージョン内で複製されるかによって異なります。

## 価格 {#pricing}

TiDB Cloudリカバリ グループでサポートされているリージョンと価格については、 [回復グループコスト](https://www.pingcap.com/tidb-cloud-pricing-details/#recovery-group-cost)参照してください。
