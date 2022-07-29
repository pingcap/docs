---
title: Select Your Cluster Tier
summary: Learn how to select your cluster tier on TiDB Cloud.
aliases: ['/tidbcloud/public-preview/developer-tier-cluster']
---

# クラスター層を選択する {#select-your-cluster-tier}

クラスタ層は、クラスタのスループットとパフォーマンスを決定します。

TiDB Cloudは、クラスタ層の次の2つのオプションを提供します。クラスタを作成する前に、どのオプションがニーズに適しているかを検討する必要があります。

-   [開発者層](#developer-tier)
-   [専用層](#dedicated-tier)

## 開発者層 {#developer-tier}

TiDB Cloud開発者層は、TiDBのフルマネージドサービスである1の[TiDB Cloud](https://pingcap.com/products/tidbcloud)年間の無料トライアルです。開発者層クラスターは、プロトタイプアプリケーション、ハッカソン、アカデミックコースなどの非本番ワークロードに使用したり、非商用データセットに一時的なデータサービスを提供したりするために使用できます。

各開発者層クラスタはフル機能のTiDBクラスタであり、次のものが付属しています。

-   1TiDB共有ノード
-   1つのTiKV共有ノード（1 GiBのOLTPストレージを使用）
-   1つのTiFlash共有ノード（1 GiBのOLAPストレージを使用）

開発者層クラスターは共有ノードで実行されます。各ノードは仮想マシン（VM）上の独自のコンテナーで実行されますが、そのVMは他のTiDB、TiKV、またはTiFlashノードも実行しています。その結果、共有ノードは、標準の専用TiDB Cloudノードと比較してパフォーマンスが低下します。ただし、すべてのノードが別々のコンテナーで実行され、専用のクラウドディスクがあるため、開発者層クラスタに格納されたデータは分離され、他のTiDBクラスターに公開されることはありません。

TiDB Cloudアカウントごとに、1つの無料の開発者層クラスタを使用して1年間使用できます。一度に実行できる開発者層クラスタは1つだけですが、クラスタの削除と再作成は何度でも行うことができます。

1年間の無料トライアルは、最初の開発者層クラスタが作成された日から始まります。

### ユーザー名のプレフィックス {#user-name-prefix}

<!--Important: Do not update the section name "User name prefix" because this section is referenced by TiDB backend error messages.-->

開発者層クラスタごとに、 TiDB Cloudは他のクラスターと区別するために一意のプレフィックスを生成します。

データベースのユーザー名を使用または設定するときは常に、ユーザー名にプレフィックスを含める必要があります。たとえば、クラスタのプレフィックスが`3pTAoNNegb47Uc8`であると想定します。

-   クラスタに接続するには：

    ```shell
    mysql --connect-timeout 15 -u '3pTAoNNegb47Uc8.root' -h <host> -P 4000 -D test -p
    ```

-   データベースユーザーを作成するには：

    ```sql
    CREATE USER '3pTAoNNegb47Uc8.jeffrey';
    ```

クラスタのプレフィックスを取得するには、次の手順を実行します。

1.  TiDB Cloudコンソールで、プロジェクトの[**アクティブクラスター**]ページに移動し、クラスタの名前をクリックします。
2.  左側のクラスタ情報ペインで、[**接続**]をクリックします。 [ <strong>TiDBに接続</strong>]ダイアログが表示されます。
3.  ダイアログで、[**ステップ2：SQLクライアントに接続し**てプレフィックスを取得する]を見つけます。

### 自動休止状態と再開 {#automatic-hibernation-and-resuming}

開発者層クラスタが24時間アイドル状態のままになると、クラスタは自動的に休止状態になります。

休止状態は、クラスタに格納されているデータには影響しませんが、監視情報の収集とコンピューティングリソースの消費を停止するだけです。

休止状態の間、クラスタのステータスは引き続き**正常**として表示され、休止状態に関するメッセージがTiDB Cloudコンソールに表示されます。

開発者層クラスタを再度使用する場合は、通常どおり、MySQLクライアントドライバーまたはORMフレームワークを使用してクラスタに接続するだけです。クラスタは50秒以内に再開され、自動的にサービスに戻ります。

または、 TiDB Cloudコンソールにログインし、[**アクティブなクラスター**]ページでクラスタの[<strong>再開</strong>]をクリックすることもできます。

### 開発者層の特別な利用規約 {#developer-tier-special-terms-and-conditions}

-   稼働時間のSLA保証はありません。
-   高可用性や自動フェイルオーバーはありません。
-   クラスターへのアップグレードでは、重大なダウンタイムが発生する可能性があります。
-   バックアップと復元機能は使用できません。 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)を使用して、データをバックアップとしてエクスポートできます。
-   開発者層クラスタへの接続の最大数は50です。
-   チェンジフィード（Apache KafkaSinkおよびMySQLSink）を作成したり、 [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview)を使用して増分データを複製したりすることはできません。
-   VPCピアリングを使用してクラスターに接続することはできません。
-   クラスターをより大きなストレージや標準ノードに拡張したり、ノードの数を増やしたりすることはできません。
-   サードパーティの監視サービスを使用することはできません。
-   TiDBクラスタのポート番号をカスタマイズすることはできません。
-   データ転送は、週に合計20GiBの入出力に制限されています。 20 GiBの制限に達すると、ネットワークトラフィックは10 KB/sに抑制されます。

## 専用層 {#dedicated-tier}

TiDB Cloud Dedicated Tierは、クロスゾーンの高可用性、水平スケーリング、および[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)の利点を備えた、本番環境での使用専用です。

専用層クラスターの場合、ビジネスニーズに応じて、TiDB、TiKV、およびTiFlashのクラスタサイズを簡単にカスタマイズできます。 TiKVノードとTiFlashノードごとに、ノード上のデータが複製され、 [高可用性](/tidb-cloud/high-availability-with-multi-az.md)つの異なるアベイラビリティーゾーンに分散されます。

専用層クラスタを作成するには、 [お支払い方法を追加する](/tidb-cloud/tidb-cloud-billing.md#payment-method)または[概念実証（PoC）トライアルを申請する](/tidb-cloud/tidb-cloud-poc.md)にする必要があります。

> **ノート：**
>
> クラスタの作成後にクラスタストレージサイズを減らすことはできません。
