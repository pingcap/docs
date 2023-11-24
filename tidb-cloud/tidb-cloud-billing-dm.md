---
title: Data Migration Billing
summary: Learn about billing for Data Migration in TiDB Cloud.
---

# データ移行の請求 {#data-migration-billing}

このドキュメントでは、 TiDB Cloudでのデータ移行の請求について説明します。

## データ移行の仕様 {#specifications-for-data-migration}

TiDB Cloudは、データ移行の容量をレプリケーション キャパシティ ユニット (RCU) で測定します。データ移行ジョブを作成するときに、適切な仕様を選択できます。 RCU が高いほど、移行パフォーマンスが向上します。これらのデータ移行 RCU に対して料金が発生します。

次の表に、データ移行の仕様と対応するパフォーマンスを示します。

| 仕様     | 完全なデータ移行 | 増分データ移行   |
| ------ | -------- | --------- |
| 2 RCU  | 25 MiB/秒 | 10,000行/秒 |
| 4 RCU  | 35 MiB/秒 | 20,000行/秒 |
| 8 RCU  | 40MiB/秒  | 40,000行/秒 |
| 16 RCU | 45MiB/秒  | 80,000行/秒 |

この表の性能値はすべて最大性能であることに注意してください。アップストリームおよびダウンストリームのデータベースにはパフォーマンス、ネットワーク帯域幅、またはその他のボトルネックがないことが前提となります。パフォーマンス値は参考用のみであり、シナリオによって異なる場合があります。

データ移行ジョブは、完全なデータ移行パフォーマンスを MiB/秒で測定します。この単位は、データ移行ジョブによって 1 秒あたりに移行されるデータの量 (MiB 単位) を示します。

データ移行ジョブは、増分データ移行パフォーマンスを行/秒単位で測定します。この単位は、1 秒あたりにターゲット データベースに移行される行数を示します。たとえば、アップストリーム データベースが 10,000 行の`INSERT` 、 `UPDATE` 、または`DELETE`のステートメントを約 1 秒で実行する場合、対応する仕様のデータ移行ジョブは、その 10,000 行を約 1 秒でダウンストリームにレプリケートできます。

## 価格 {#price}

各データ移行 RCU のサポートされるリージョンとTiDB Cloudの価格については、 [データ移行コスト](https://www.pingcap.com/tidb-cloud-pricing-details/#dm-cost)を参照してください。

データ移行ジョブは、ターゲット TiDB ノードと同じリージョンにあります。

AWS PrivateLink または VPC ピアリング接続を使用しており、ソース データベースと TiDB ノードが同じリージョンまたは同じアベイラビリティ ゾーン (AZ) にない場合、次の 2 つの追加トラフィック料金が発生することに注意してください。そしてクロスアリゾナ州のトラフィック料金。

-   ソース データベースと TiDB ノードが同じリージョンにない場合、データ移行ジョブがソース データベースからデータを収集するときにリージョン間トラフィック料金が発生します。

    ![Cross-region traffic charges](/media/tidb-cloud/dm-billing-cross-region-fees.png)

-   ソース データベースと TiDB ノードが同じリージョンにあるものの、異なる AZ にある場合、データ移行ジョブがソース データベースからデータを収集するときに、クロス AZ トラフィック料金が発生します。

    ![Cross-AZ traffic charges](/media/tidb-cloud/dm-billing-cross-az-fees.png)

-   データ移行ジョブと TiDB ノードが同じ AZ にない場合、データ移行ジョブがターゲット TiDB ノードにデータを書き込むときにクロス AZ トラフィック料金が発生します。さらに、データ移行ジョブと TiDB ノードがソース データベースと同じ AZ (またはリージョン) にない場合、データ移行ジョブがソース データベースからデータを収集するときにクロス AZ (またはクロスリージョン) トラフィック料金が発生します。データベース。

    ![Cross-region and cross-AZ traffic charges](/media/tidb-cloud/dm-billing-cross-region-and-az-fees.png)

クロスリージョンおよびクロス AZ トラフィックの料金は、 TiDB Cloudの料金と同じです。詳細については、 [TiDB Cloudの料金詳細](https://en.pingcap.com/tidb-cloud-pricing-details/)を参照してください。

## こちらも参照 {#see-also}

-   [データ移行を使用した MySQL 互換データベースからの移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md)
