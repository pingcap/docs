---
title: Data Migration Billing
summary: Learn about billing for Data Migration in TiDB Cloud.
---

# データ移行の請求 {#data-migration-billing}

このドキュメントでは、 TiDB Cloudでのデータ移行の課金について説明します。

## データ移行の仕様 {#specifications-for-data-migration}

TiDB Cloud は、レプリケーション キャパシティ ユニット (RCU) でデータ移行のキャパシティを測定します。データ移行ジョブを作成するときに、適切な仕様を選択できます。 RCU が高いほど、移行のパフォーマンスが向上します。これらのデータ移行 RCU に対して課金されます。

データ移行の仕様と対応する性能を次の表に示します。

| 仕様      | 完全なデータ移行 | 増分データ移行    |
| ------- | -------- | ---------- |
| 2つのRCU  | 25 MiB/秒 | 10,000 行/秒 |
| 4つのRCU  | 35 MiB/秒 | 20,000 行/秒 |
| 8つのRCU  | 40 MiB/秒 | 40,000 行/秒 |
| 16個のRCU | 45 MiB/秒 | 80,000 行/秒 |

この表のすべてのパフォーマンス値は最大パフォーマンスであることに注意してください。アップストリーム データベースとダウンストリーム データベースにパフォーマンス、ネットワーク帯域幅、またはその他のボトルネックがないことを前提としています。パフォーマンス値は参照用であり、シナリオによって異なる場合があります。

データ移行ジョブは、完全なデータ移行パフォーマンスを MiB/秒で測定します。この単位は、データ移行ジョブによって 1 秒あたりに移行されるデータの量 (MiB 単位) を示します。

データ移行ジョブは、増分データ移行のパフォーマンスを行/秒で測定します。この単位は、1 秒あたりにターゲット データベースに移行される行数を示します。たとえば、上流のデータベースが約 1 秒で 10,000 行の`INSERT` `UPDATE`または`DELETE`のステートメントを実行する場合、対応する仕様の Data Migration ジョブは、約 1 秒で 10,000 行を下流に複製できます。

## 価格 {#price}

データ移行 RCU ごとにサポートされているリージョンとTiDB Cloudの価格については、 [データ移行コスト](https://www.pingcap.com/tidb-cloud-pricing-details/#dm-cost)を参照してください。

データ移行ジョブは、ターゲットの TiDB クラスターと同じリージョンにあります。

AWS PrivateLink または VPC ピアリング接続を使用していて、ソース データベースと TiDB クラスターが同じリージョンまたは同じアベイラビリティ ゾーン (AZ) にない場合は、2 つの追加トラフィック料金が発生することに注意してください: クロスリージョンクロス AZ トラフィック料金。

-   ソース データベースと TiDB クラスターが同じリージョンにない場合、データ移行ジョブがソース データベースからデータを収集するときに、リージョン間のトラフィック料金が発生します。

    ![Cross-region traffic charges](/media/tidb-cloud/dm-billing-cross-region-fees.png)

-   ソース データベースと TiDB クラスターが同じリージョンにあるが異なる AZ にある場合、データ移行ジョブがソース データベースからデータを収集するときにクロス AZ トラフィック料金が発生します。

    ![Cross-AZ traffic charges](/media/tidb-cloud/dm-billing-cross-az-fees.png)

-   データ移行ジョブと TiDB クラスターが同じ AZ にない場合、データ移行ジョブがターゲット TiDB クラスターにデータを書き込むときにクロス AZ トラフィック料金が発生します。さらに、データ移行ジョブと TiDB クラスターがソース データベースと同じ AZ (またはリージョン) にない場合、データ移行ジョブがソースからデータを収集するときにクロス AZ (またはクロスリージョン) トラフィック料金が発生します。データベース。

    ![Cross-region and cross-AZ traffic charges](/media/tidb-cloud/dm-billing-cross-region-and-az-fees.png)

クロスリージョンおよびクロス AZ トラフィックの料金は、 TiDB Cloudの料金と同じです。詳細については、 [TiDB Cloudの価格詳細](https://en.pingcap.com/tidb-cloud-pricing-details/)を参照してください。

## こちらもご覧ください {#see-also}

-   [データ移行を使用して MySQL 互換データベースから移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)
