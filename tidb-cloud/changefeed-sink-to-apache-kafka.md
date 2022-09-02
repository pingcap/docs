---
title: Sink to Apache Kafka
Summary: Learn how to create a changefeed to stream data from TiDB Cloud to Apache Kafka. 
---

# Apache Kafka にシンクする {#sink-to-apache-kafka}

> **警告：**
>
> 現在、 **Sink to Apache Kafka**は実験的機能です。実稼働環境で使用することはお勧めしません。

このドキュメントでは、 **Sink to Apache Kafka** changefeed を使用して、 TiDB Cloudから Apache Kafka にデータをストリーミングする方法について説明します。

## 前提条件 {#prerequisites}

### 通信網 {#network}

TiDBクラスタが Apache Kafka サービスに接続できることを確認してください。

インターネットにアクセスできない AWS VPC に Apache Kafka サービスがある場合は、次の手順を実行します。

1.  Apache Kafka サービスの VPC と TiDB クラスターの間の[VPC ピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md) 。

2.  Apache Kafka サービスが関連付けられているセキュリティ グループの受信規則を変更します。

    TiDB Cloudクラスターが配置されているリージョンの CIDR をインバウンド規則に追加する必要があります。 CIDR は VPC Peering ページにあります。そうすることで、トラフィックが TiDB クラスターから Kafka ブローカーに流れるようになります。

3.  Apache Kafka URL にホスト名が含まれている場合、 TiDB Cloudが Apache Kafka ブローカーの DNS ホスト名を解決できるようにする必要があります。

    1.  [VPC ピアリング接続の DNS 解決を有効にする](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns)の手順に従います。
    2.  **Accepter DNS 解決**オプションを有効にします。

インターネットにアクセスできない GCP VPC に Apache Kafka サービスがある場合は、次の手順を実行します。

1.  Apache Kafka サービスの VPC と TiDB クラスターの間の[VPC ピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md) 。
2.  Apache Kafka が配置されている VPC のイングレス ファイアウォール ルールを変更します。

    TiDB Cloudクラスターが配置されているリージョンの CIDR をイングレス ファイアウォール ルールに追加する必要があります。 CIDR は VPC Peering ページにあります。そうすることで、トラフィックが TiDB クラスターから Kafka ブローカーに流れるようになります。

### トピック {#topic}

Apache Kafka Sink を作成する前に、トピックを準備する必要があります。テーブルに基づいて、シンクはデータをトピックの異なるパーティションに分散します。

## シンクを作成する {#create-a-sink}

前提条件を完了すると、データを Apache Kafka にシンクできます。

1.  TiDB クラスターの**Changefeed**タブに移動します。
2.  [ **Sink to Apache Kafka] を**クリックします。
3.  Kafka URL と Kafka トピックを入力します。
4.  [**接続のテスト]**をクリックします。 TiDBクラスタが Apache Kafka サービスに接続できる場合は、[<strong>確認</strong>] ボタンが表示されます。
5.  [**確認**] をクリックすると、しばらくするとシンクが動作を開始し、シンクのステータスが [作成中] に<strong>変わり</strong>ます。

## シンクを削除する {#delete-a-sink}

1.  クラスターの**Changefeed**タブに移動します。
2.  **Sink to Apache Kafka**のゴミ箱ボタンをクリック

## 制限 {#restrictions}

TiDB Cloudは TiCDC を使用して変更フィードを確立するため、同じ[TiCDCとしての制限](https://docs.pingcap.com/tidb/stable/ticdc-overview#restrictions)を持ちます。
