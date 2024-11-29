---
title: Upgrade TiDB Binlog
summary: TiDB Binlog を最新のクラスター バージョンにアップグレードする方法を学びます。
---

# TiDBBinlogのアップグレード {#upgrade-tidb-binlog}

このドキュメントでは、手動でデプロイされた TiDB Binlog を最新バージョン[クラスタ](/tidb-binlog/tidb-binlog-overview.md)にアップグレードする方法を紹介します。また、以前の互換性のないバージョン (Kafka/Local バージョン) から最新バージョンに TiDB Binlog をアップグレードする方法についてのセクションもあります。

> **注記：**
>
> -   TiDB Binlog はTiDB v5.0 で導入された一部の機能と互換性がなく、併用できません。詳細については[注記](/tidb-binlog/tidb-binlog-overview.md#notes)参照してください。
> -   TiDB v7.5.0 以降、TiDB Binlogのデータ レプリケーション機能のテクニカル サポートは提供されなくなりました。データ レプリケーションの代替ソリューションとして[ティCDC](/ticdc/ticdc-overview.md)使用することを強くお勧めします。
> -   TiDB v7.5.0 では、TiDB Binlogのリアルタイム バックアップと復元機能が引き続きサポートされていますが、このコンポーネントは将来のバージョンでは完全に廃止される予定です。データ復旧の代替ソリューションとして[ピトル](/br/br-pitr-guide.md)使用することをお勧めします。

## 手動でデプロイされた TiDB Binlogをアップグレードする {#upgrade-tidb-binlog-deployed-manually}

TiDB Binlog を手動でデプロイする場合は、このセクションの手順に従ってください。

### Pumpのアップグレード {#upgrade-pump}

まず、クラスター内の各Pumpインスタンスを 1 つずつアップグレードします。これにより、TiDB からバイナリログを受信できるPumpインスタンスがクラスター内に常に存在するようになります。手順は次のとおりです。

1.  元のファイルを`pump`の新しいバージョンに置き換えます。
2.  Pumpプロセスを再起動します。

### アップグレードDrainer {#upgrade-drainer}

次に、 Drainerコンポーネントをアップグレードします。

1.  元のファイルを`drainer`の新しいバージョンに置き換えます。
2.  Drainerプロセスを再起動します。

## TiDB Binlog をKafka/Local バージョンからクラスター バージョンにアップグレードする {#upgrade-tidb-binlog-from-kafka-local-version-to-the-cluster-version}

新しい TiDB バージョン (v2.0.8- binlog、v2.1.0-rc.5 以降) は、 TiDB Binlogの Kafka バージョンまたはローカル バージョンと互換性がありません。 TiDB を新しいバージョンのいずれかにアップグレードする場合は、 TiDB Binlogのクラスター バージョンを使用する必要があります。 アップグレード前に TiDB Binlogの Kafka バージョンまたはローカル バージョンを使用している場合は、 TiDB Binlog をクラスター バージョンにアップグレードする必要があります。

TiDB Binlogバージョンと TiDB バージョンの対応関係を次の表に示します。

| TiDBBinlogバージョン | TiDB バージョン                          | 注記                                                                    |
| --------------- | ----------------------------------- | --------------------------------------------------------------------- |
| 地元              | TiDB 1.0 以前                         |                                                                       |
| カフカ             | TiDB 1.0 ~ TiDB 2.1 RC5             | TiDB 1.0 は、TiDB Binlogのローカル バージョンと Kafka バージョンの両方をサポートします。            |
| クラスタ            | TiDB v2.0.8- binlog、TiDB 2.1 RC5 以降 | TiDB v2.0.8- binlog は、 TiDB Binlogのクラスター バージョンをサポートする特別な 2.0 バージョンです。 |

### アップグレードプロセス {#upgrade-process}

> **注記：**
>
> 全データのインポートが許容される場合は、古いバージョンを破棄し、 [TiDBBinlogクラスタの展開](/tidb-binlog/deploy-tidb-binlog.md)に従って TiDB Binlog をデプロイできます。

元のチェックポイントからレプリケーションを再開する場合は、次の手順を実行して TiDB Binlog をアップグレードします。

1.  Pumpの新しいバージョンをデプロイ。

2.  TiDB クラスター サービスを停止します。

3.  TiDB と構成をアップグレードし、 binlogデータを新しいPumpクラスターに書き込みます。

4.  TiDB クラスターをサービスに再接続します。

5.  古いバージョンのDrainerが、古いバージョンのPumpのデータを下流に完全に複製していることを確認します。

    Drainerの`status`インターフェースを照会するには、次のコマンドを実行します。

    ```bash
    curl 'http://172.16.10.49:8249/status'
    ```

        {"PumpPos":{"172.16.10.49:8250":{"offset":32686}},"Synced": true ,"DepositWindow":{"Upper":398907800202772481,"Lower":398907799455662081}}

    戻り値`Synced`が True の場合、 Drainer が古いバージョンのPumpのデータを下流に完全に複製したことを意味します。

6.  Drainerの新しいバージョンを起動します。

7.  古いバージョンのPumpとDrainerおよび依存する Kafka と ZooKeeper を閉じます。
