---
title: Select Your Cluster Tier
summary: Learn how to select your cluster tier on TiDB Cloud.
aliases: ['/tidbcloud/public-preview/developer-tier-cluster']
---

# Cluster Tierを選択する {#select-your-cluster-tier}

クラスター層によって、クラスターのスループットとパフォーマンスが決まります。

TiDB Cloudは、クラスター層の次の 2 つのオプションを提供します。クラスターを作成する前に、どのオプションがニーズに適しているかを検討する必要があります。

-   [サーバーレス層](#serverless-tier)
-   [Dedicated Tier](#dedicated-tier)

## サーバーレス層 {#serverless-tier}

TiDB Cloud Tier (以前はDeveloper Tierと呼ばれていた) は、TiDB のフル マネージド サービスです。これはまだベータ版であり、本番環境では使用しないでください。ただし、サーバーレス層クラスターは、プロトタイプ アプリケーション、ハッカソン、アカデミック コースなどの非運用ワークロードに使用したり、データセットに一時的なデータ サービスを提供したりするために使用できます。

TiDB Cloudアカウントごとに、無料の Serverless Tier クラスターを作成して、ベータ フェーズで使用できます。一度に実行できる Serverless Tier クラスターは 1 つだけですが、クラスターの削除と再作成は何度でも実行できます。

### ユーザー名のプレフィックス {#user-name-prefix}

<!--Important: Do not update the section name "User name prefix" because this section is referenced by TiDB backend error messages.-->

サーバーレス層クラスターごとに、 TiDB Cloudは一意のプレフィックスを生成して、他のクラスターと区別します。

データベース ユーザー名を使用または設定するときは常に、ユーザー名にプレフィックスを含める必要があります。たとえば、クラスターのプレフィックスが`3pTAoNNegb47Uc8`であるとします。

-   クラスターに接続するには:

    ```shell
    mysql --connect-timeout 15 -u '3pTAoNNegb47Uc8.root' -h <host> -P 4000 -D test -p
    ```

-   データベース ユーザーを作成するには:

    ```sql
    CREATE USER '3pTAoNNegb47Uc8.jeffrey';
    ```

クラスターのプレフィックスを取得するには、次の手順を実行します。

1.  [**クラスター]**ページに移動します。
2.  クラスター領域の右上隅にある [**接続]**をクリックします。接続ダイアログボックスが表示されます。
3.  ダイアログで、[**ステップ 2: SQL クライアント**に接続し、接続文字列のプレフィックスを取得する] を見つけます。

### サーバーレス ティアの特別利用規約 {#serverless-tier-special-terms-and-conditions}

-   Serverless Tier には、ベータ フェーズ中のアップタイム SLA 保証はありません。 Serverless Tier ベータ版を使用して商用または実稼働データセットを保存する場合、使用に伴う潜在的なリスクはご自身で負う必要があり、PingCAP はいかなる損害についても責任を負わないものとします。
-   バックアップおよび復元機能は使用できません。 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)を使用して、データをバックアップとしてエクスポートできます。
-   変更フィード (Apache Kafka Sink および MySQL Sink) を作成したり、 [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview)を使用して増分データを複製したりすることはできません。
-   VPC ピアリングまたはプライベート エンドポイントを使用して Serverless Tier クラスターに接続することはできません。
-   クラスターをより大きなストレージや標準ノードにスケーリングしたり、ノード数を増やしたりすることはできません。
-   Serverless Tier クラスターを[一時停止または再開](/tidb-cloud/pause-or-resume-tidb-cluster.md)にすることはできません。
-   [モニタリングページ](/tidb-cloud/built-in-monitoring.md)は表示できません。
-   サードパーティの監視サービスは使用できません。
-   TiDB クラスターのポート番号をカスタマイズすることはできません。
-   データ転送は、1 週間あたり合計 20 GiB に制限されています。 20 GiB の制限に達すると、ネットワーク トラフィックは 10 KB/秒に調整されます。

## Dedicated Tier {#dedicated-tier}

TiDB Cloud Dedicated Tierは、クロスゾーンの高可用性、水平スケーリング、および[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)の利点を備えた、実動使用専用です。

Dedicated Tierクラスターの場合、ビジネス ニーズに応じて、TiDB、TiKV、およびTiFlashのクラスター サイズを簡単にカスタマイズできます。 TiKV ノードとTiFlashノードごとに、ノード上のデータが複製され、異なるアベイラビリティ ゾーンに分散され[高可用性](/tidb-cloud/high-availability-with-multi-az.md) 。

Dedicated Tierクラスターを作成するには、 [支払い方法を追加する](/tidb-cloud/tidb-cloud-billing.md#payment-method)または[概念実証 (PoC) トライアルに申し込む](/tidb-cloud/tidb-cloud-poc.md)が必要です。

> **ノート：**
>
> クラスターの作成後にノード ストレージを減らすことはできません。
