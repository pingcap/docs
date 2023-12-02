---
title: Upgrade TiDB Binlog
summary: Learn how to upgrade TiDB Binlog to the latest cluster version.
---

# TiDBBinlogをアップグレードする {#upgrade-tidb-binlog}

このドキュメントでは、手動でデプロイされた TiDB Binlogを最新の[集まる](/tidb-binlog/tidb-binlog-overview.md)バージョンにアップグレードする方法を紹介します。 TiDB Binlog を以前の互換性のないバージョン (Kafka/ローカル バージョン) から最新バージョンにアップグレードする方法に関するセクションもあります。

> **注記：**
>
> -   TiDB Binlog は、 TiDB v5.0 で導入された一部の機能と互換性がなく、一緒に使用することはできません。詳細は[ノート](/tidb-binlog/tidb-binlog-overview.md#notes)を参照してください。
> -   TiDB v7.5.0 以降、TiDB Binlogのデータ レプリケーション機能のテクニカル サポートは提供されなくなりました。データ レプリケーションの代替ソリューションとして[TiCDC](/ticdc/ticdc-overview.md)を使用することを強くお勧めします。
> -   TiDB v7.5.0 は TiDB Binlogのリアルタイム バックアップおよび復元機能を引き続きサポートしていますが、このコンポーネントは将来のバージョンでは完全に非推奨になります。データ回復の代替ソリューションとして[PITR](/br/br-pitr-guide.md)を使用することをお勧めします。

## 手動でデプロイされた TiDB Binlogをアップグレードする {#upgrade-tidb-binlog-deployed-manually}

TiDB Binlog を手動で展開する場合は、このセクションの手順に従ってください。

### Pumpのアップグレード {#upgrade-pump}

まず、クラスター内の各Pumpインスタンスを 1 つずつアップグレードします。これにより、TiDB からバイナリログを受信できるPumpインスタンスがクラスター内に常に存在することが保証されます。手順は以下のとおりです。

1.  元のファイルを新しいバージョンの`pump`に置き換えます。
2.  Pumpプロセスを再起動します。

### アップグレードDrainer {#upgrade-drainer}

次に、 Drainerコンポーネントをアップグレードします。

1.  元のファイルを新しいバージョンの`drainer`に置き換えます。
2.  Drainerプロセスを再起動します。

## TiDB Binlog をKafka/ローカル バージョンからクラスター バージョンにアップグレードします。 {#upgrade-tidb-binlog-from-kafka-local-version-to-the-cluster-version}

新しい TiDB バージョン (v2.0.8- binlog、 v2.1.0-rc.5 以降) は、TiDB Binlogの Kafka バージョンまたはローカル バージョンと互換性がありません。 TiDB が新しいバージョンのいずれかにアップグレードされる場合は、TiDB Binlogのクラスター バージョンを使用する必要があります。アップグレード前に Kafka または TiDB Binlogのローカル バージョンを使用している場合は、TiDB Binlogをクラスター バージョンにアップグレードする必要があります。

TiDB Binlogバージョンと TiDB バージョンの対応関係を次の表に示します。

| TiDBBinlogのバージョン | TiDBのバージョン                          | 注記                                                                    |
| ---------------- | ----------------------------------- | --------------------------------------------------------------------- |
| 地元               | TiDB 1.0 以前                         |                                                                       |
| カフカ              | TiDB 1.0 ～ TiDB 2.1 RC5             | TiDB 1.0 は、TiDB Binlogのローカル バージョンと Kafka バージョンの両方をサポートします。            |
| クラスタ             | TiDB v2.0.8- binlog、TiDB 2.1 RC5 以降 | TiDB v2.0.8- binlog は、 TiDB Binlogのクラスター バージョンをサポートする特別な 2.0 バージョンです。 |

### アップグレードプロセス {#upgrade-process}

> **注記：**
>
> 完全なデータのインポートが許容される場合は、古いバージョンを放棄して、 [TiDBBinlogクラスタの展開](/tidb-binlog/deploy-tidb-binlog.md)の TiDB Binlogをデプロイできます。

元のチェックポイントからレプリケーションを再開する場合は、次の手順を実行して TiDB Binlogをアップグレードします。

1.  新しいバージョンのPumpをデプロイ。

2.  TiDB クラスター サービスを停止します。

3.  TiDB と構成をアップグレードし、binlogデータを新しいPumpクラスターに書き込みます。

4.  TiDB クラスターをサービスに再接続します。

5.  古いバージョンのDrainer が古いバージョンのPumpのデータをダウンストリームに完全に複製していることを確認してください。

    Drainerの`status`インターフェイスをクエリし、次のようにコマンドを実行します。

    ```bash
    curl 'http://172.16.10.49:8249/status'
    ```

        {"PumpPos":{"172.16.10.49:8250":{"offset":32686}},"Synced": true ,"DepositWindow":{"Upper":398907800202772481,"Lower":398907799455662081}}

    戻り値`Synced`が True の場合、 Drainer が古いバージョンのPumpのデータをダウンストリームに完全に複製したことを意味します。

6.  新しいバージョンのDrainerを起動します。

7.  古いバージョンのPumpとDrainer 、および依存する Kafka と ZooKeeper を閉じます。
