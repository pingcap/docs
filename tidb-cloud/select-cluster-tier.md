---
title: Select Your Cluster Tier
summary: Learn how to select your cluster tier on TiDB Cloud.
aliases: ['/tidbcloud/public-preview/developer-tier-cluster']
---

# クラスター層を選択する {#select-your-cluster-tier}

クラスタ層によって、クラスタのスループットとパフォーマンスが決まります。

TiDB Cloudは、クラスタ層の次の 2 つのオプションを提供します。クラスタを作成する前に、どのオプションがニーズにより適しているかを検討する必要があります。

-   [開発者層](#developer-tier)
-   [専用ティア](#dedicated-tier)

## 開発者層 {#developer-tier}

TiDB Cloud Developer Tier は、TiDB のフル マネージド サービスである 1 の[TiDB Cloud](https://pingcap.com/products/tidbcloud)年間の無料トライアルです。開発者層クラスターは、プロトタイプ アプリケーション、ハッカソン、アカデミック コースなどの非運用ワークロードに使用したり、非商用データセットに一時的なデータ サービスを提供したりするために使用できます。

各 Developer Tierクラスタはフル機能の TiDBクラスタであり、以下が付属しています。

-   1 つの TiDB 共有ノード
-   1 つの TiKV 共有ノード (1 GiB の OLTP ストレージを使用)
-   1 つの TiFlash 共有ノード (1 GiB の OLAP ストレージを使用)

開発者層クラスターは共有ノードで実行されます。各ノードは仮想マシン (VM) 上の独自のコンテナーで実行されますが、その VM は他の TiDB、TiKV、または TiFlash ノードも実行しています。その結果、共有ノードは、標準の専用TiDB Cloudノードと比較してパフォーマンスが低下します。ただし、すべてのノードが個別のコンテナーで実行され、専用のクラウド ディスクがあるため、Developer Tierクラスタに格納されたデータは分離され、他の TiDB クラスターに公開されることはありません。

TiDB Cloudアカウントごとに、無料の Developer Tierクラスタを 1 つ使用して 1 年間使用できます。一度に実行できる Developer Tierクラスタは 1 つだけですが、クラスタの削除と再作成は何度でも行うことができます。

1 年間の無料トライアルは、最初の Developer Tierクラスタが作成された日から始まります。

### ユーザー名のプレフィックス {#user-name-prefix}

<!--Important: Do not update the section name "User name prefix" because this section is referenced by TiDB backend error messages.-->

各 Developer Tierクラスタに対して、 TiDB Cloudは一意のプレフィックスを生成して、他のクラスターと区別します。

データベース ユーザー名を使用または設定するときは常に、ユーザー名にプレフィックスを含める必要があります。たとえば、クラスタのプレフィックスが`3pTAoNNegb47Uc8`であるとします。

-   クラスタに接続するには:

    ```shell
    mysql --connect-timeout 15 -u '3pTAoNNegb47Uc8.root' -h <host> -P 4000 -D test -p
    ```

-   データベース ユーザーを作成するには:

    ```sql
    CREATE USER '3pTAoNNegb47Uc8.jeffrey';
    ```

クラスタのプレフィックスを取得するには、次の手順を実行します。

1.  [**アクティブなクラスター]**ページに移動します。
2.  領域の右上隅にある [**接続]**をクリックします。接続ダイアログボックスが表示されます。

    > **ヒント：**
    >
    > または、[**アクティブなクラスター**] ページでクラスタの名前をクリックし、右上隅にある [<strong>接続</strong>] をクリックすることもできます。
3.  ダイアログで、[**ステップ 2: SQL クライアントに接続し**てプレフィックスを取得する] を見つけます。

### 自動ハイバネーションとレジューム {#automatic-hibernation-and-resuming}

Developer Tierクラスタが 24 時間アイドル状態になると、クラスタは自動的に休止状態になります。

休止状態は、クラスタに保存されているデータには影響しませんが、監視情報の収集とコンピューティング リソースの消費を停止するだけです。

ハイバネーション中、クラスタのステータスは引き続き**Normal**として表示され、 TiDB Cloudコンソールでハイバネーションに関するメッセージを確認できます。

Developer Tierクラスタを再び使用したいときはいつでも、通常どおり MySQL クライアントドライバーまたは ORM フレームワークを使用してクラスタに接続するだけです。クラスタは 50 秒以内に再開され、自動的にサービスに戻ります。

または、 TiDB Cloudコンソールにログインし、[**アクティブなクラスター**] ページでクラスタの [<strong>再開</strong>] をクリックすることもできます。

### 開発者層の特別利用規約 {#developer-tier-special-terms-and-conditions}

-   アップタイム SLA 保証なし。
-   高可用性や自動フェイルオーバーはありません。
-   クラスターへのアップグレードでは、大幅なダウンタイムが発生する可能性があります。
-   バックアップおよび復元機能は使用できません。 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)を使用して、データをバックアップとしてエクスポートできます。
-   Developer Tierクラスタへの接続の最大数は 50 です。
-   変更フィード (Apache Kafka Sink および MySQL Sink) を作成したり、 [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview)を使用して増分データを複製したりすることはできません。
-   VPC ピアリングを使用してクラスターに接続することはできません。
-   クラスターをより大きなストレージや標準ノードにスケーリングしたり、ノード数を増やしたりすることはできません。
-   [モニタリングページ](/tidb-cloud/built-in-monitoring.md)は表示できません。
-   サードパーティの監視サービスは使用できません。
-   TiDBクラスタのポート番号はカスタマイズできません。
-   データ転送は、1 週間あたり合計 20 GiB に制限されています。 20 GiB の制限に達すると、ネットワーク トラフィックは 10 KB/秒に調整されます。

## 専用ティア {#dedicated-tier}

TiDB Cloud Dedicated Tier は、クロスゾーンの高可用性、水平スケーリング、および[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)の利点を備えた、実動使用専用です。

Dedicated Tier クラスターの場合、ビジネス ニーズに応じて、TiDB、TiKV、および TiFlash のクラスタサイズを簡単にカスタマイズできます。 TiKV ノードと TiFlash ノードごとに、ノード上のデータが複製され、異なるアベイラビリティ ゾーンに分散され[高可用性](/tidb-cloud/high-availability-with-multi-az.md) 。

Dedicated Tierクラスタを作成するには、 [支払い方法を追加する](/tidb-cloud/tidb-cloud-billing.md#payment-method)または[概念実証 (PoC) トライアルに申し込む](/tidb-cloud/tidb-cloud-poc.md)が必要です。

> **ノート：**
>
> クラスタの作成後にクラスタのストレージ サイズを減らすことはできません。
