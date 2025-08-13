---
title: Data Migration Billing
summary: TiDB Cloudでのデータ移行の課金について説明します。
---

# データ移行の請求 {#data-migration-billing}

このドキュメントでは、 TiDB Cloudでのデータ移行の課金について説明します。

## データ移行の仕様 {#specifications-for-data-migration}

TiDB Cloudは、データ移行のキャパシティをレプリケーション容量単位（RCU）で測定します。データ移行ジョブを作成する際に、適切な仕様を選択できます。RCUが高いほど、移行パフォーマンスが向上します。これらのデータ移行RCUに対して料金が発生します。

次の表は、各データ移行仕様に対応するパフォーマンスと移行できるテーブルの最大数を示しています。

| 仕様     | 完全なデータ移行 | 増分データ移行   | テーブルの最大数 |
| ------ | -------- | --------- | -------- |
| 2台のRCU | 25 MiB/秒 | 10,000行/秒 | 500      |
| 4台のRCU | 35 MiB/秒 | 20,000行/秒 | 10000    |
| 8台のRCU | 40 MiB/秒 | 40,000行/秒 | 30000    |
| 16 RCU | 45 MiB/秒 | 80,000行/秒 | 60000    |

データ移行 RCU の価格の詳細については、 [データ移行コスト](https://www.pingcap.com/tidb-dedicated-pricing-details/#dm-cost)参照してください。

> **注記：**
>
> -   移行するテーブルの数がテーブルの最大数を超えると、データ移行ジョブは引き続き実行される可能性がありますが、ジョブが不安定になったり、失敗したりする可能性があります。
> -   この表のパフォーマンス値はすべて最大値かつ最適な値です。上流および下流のデータベースにパフォーマンス、ネットワーク帯域幅、その他のボトルネックがないことを前提としています。パフォーマンス値は参考値であり、シナリオによって異なる場合があります。

データ移行ジョブは、完全なデータ移行パフォーマンスをMiB/秒単位で測定します。この単位は、データ移行ジョブによって1秒あたりに移行されるデータ量（MiB単位）を示します。

データ移行ジョブは、増分データ移行のパフォーマンスを行数/秒で測定します。この単位は、 `INSERT` `UPDATE`または`DELETE`回、約1秒で実行する場合、対応する仕様のデータ移行ジョブは、10,000行を下流データベースに約1秒で複製できます。

## 価格 {#price}

各 Data Migration RCU でサポートされているリージョンとTiDB Cloudの価格については、 [データ移行コスト](https://www.pingcap.com/tidb-cloud-pricing-details/#dm-cost)参照してください。

データ移行ジョブは、ターゲット TiDB ノードと同じリージョンにあります。

AWS PrivateLink または VPC ピアリング接続を使用しており、ソースデータベースと TiDB ノードが同じリージョンまたは同じアベイラビリティーゾーン (AZ) にない場合は、クロスリージョントラフィック料金とクロス AZ トラフィック料金の 2 つの追加トラフィック料金が発生することに注意してください。

-   ソース データベースと TiDB ノードが同じリージョンにない場合、データ移行ジョブがソース データベースからデータを収集するときに、リージョン間のトラフィック料金が発生します。

    ![Cross-region traffic charges](/media/tidb-cloud/dm-billing-cross-region-fees.png)

-   ソース データベースと TiDB ノードが同じリージョン内であっても異なる AZ にある場合、データ移行ジョブがソース データベースからデータを収集するときに、AZ 間のトラフィック料金が発生します。

    ![Cross-AZ traffic charges](/media/tidb-cloud/dm-billing-cross-az-fees.png)

-   データ移行ジョブとTiDBノードが同じAZにない場合、データ移行ジョブがターゲットTiDBノードにデータを書き込む際に、AZ間トラフィック料金が発生します。さらに、データ移行ジョブとTiDBノードがソースデータベースと同じAZ（またはリージョン）にない場合、データ移行ジョブがソースデータベースからデータを収集する際に、AZ間（またはリージョン間）トラフィック料金が発生します。

    ![Cross-region and cross-AZ traffic charges](/media/tidb-cloud/dm-billing-cross-region-and-az-fees.png)

クロスリージョンおよびクロスAZトラフィックの料金はTiDB Cloudと同じです。詳細については[TiDB Cloud専用料金の詳細](https://www.pingcap.com/tidb-dedicated-pricing-details/)ご覧ください。

## 参照 {#see-also}

-   [データ移行を使用してMySQL互換データベースから移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)
