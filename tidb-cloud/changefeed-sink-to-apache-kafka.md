---
title: Sink to Apache Kafka
Summary: Learn how to create a changefeed to stream data from TiDB Cloud to Apache Kafka. 
---

# ApacheKafkaにシンクします {#sink-to-apache-kafka}

> **警告：**
>
> 現在、 **Sink toApacheKafka**は実験的機能です。実稼働環境での使用はお勧めしません。

このドキュメントでは、 **Sink** toApacheKafkaチェンジフィードを使用してTiDBCloudからApacheKafkaにデータをストリーミングする方法について説明します。

## 前提条件 {#prerequisites}

### 通信網 {#network}

TiDBクラスターがApacheKafkaサービスに接続できることを確認してください。

ApacheKafkaサービスがインターネットにアクセスできないAWSVPCにある場合は、次の手順を実行します。

1.  ApacheKafkaサービスのVPCとTiDBクラスタの間の[VPCピアリング接続を設定します](/tidb-cloud/set-up-vpc-peering-connections.md) 。

2.  ApacheKafkaサービスが関連付けられているセキュリティグループのインバウンドルールを変更します。

    TiDBクラウドクラスタが配置されているリージョンのCIDRをインバウンドルールに追加する必要があります。 CIDRは、VPCピアリングページにあります。そうすることで、トラフィックがTiDBクラスタからKafkaブローカーに流れるようになります。

3.  Apache Kafka URLにホスト名が含まれている場合は、TiDBCloudがApacheKafkaブローカーのDNSホスト名を解決できるようにする必要があります。

    1.  [VPCピアリング接続のDNS解決を有効にする](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns)の手順に従います。
    2.  **AccepterDNS解決**オプションを有効にします。

ApacheKafkaサービスがインターネットにアクセスできないGCPVPCにある場合は、次の手順を実行します。

1.  ApacheKafkaサービスのVPCとTiDBクラスタの間の[VPCピアリング接続を設定します](/tidb-cloud/set-up-vpc-peering-connections.md) 。
2.  ApacheKafkaが配置されているVPCの入力ファイアウォールルールを変更します。

    TiDBクラウドクラスタが配置されているリージョンのCIDRを入力ファイアウォールルールに追加する必要があります。 CIDRは、VPCピアリングページにあります。そうすることで、トラフィックがTiDBクラスタからKafkaブローカーに流れるようになります。

### トピック {#topic}

Apache Kafka Sinkを作成する前に、トピックを準備する必要があります。テーブルに基づいて、シンクはトピックのさまざまなパーティションにデータを配布します。

## シンクを作成する {#create-a-sink}

前提条件を完了したら、データをApacheKafkaにシンクできます。

1.  **TiDB**クラスタの[チェンジフィード]タブに移動します。
2.  [ **Sink toApacheKafka]を**クリックします。
3.  KafkaURLとKafkaトピックを入力します。
4.  [**接続のテスト]**をクリックします。 TiDBクラスターがApacheKafkaサービスに接続できる場合は、[<strong>確認</strong>]ボタンが表示されます。
5.  [**確認**]をクリックすると、しばらくするとシンクが動作を開始し、シンクのステータスが[<strong>生産</strong>中]に変わります。

## シンクを削除する {#delete-a-sink}

1.  クラスタの[**チェンジフィード**]タブに移動します。
2.  **Sink toApacheKafka**のゴミ箱ボタンをクリックします

## 制限 {#restrictions}

TiDBクラウドはTiCDCを使用してチェンジフィードを確立するため、同じ[TiCDCとしての制限](https://docs.pingcap.com/tidb/stable/ticdc-overview#restrictions)があります。
