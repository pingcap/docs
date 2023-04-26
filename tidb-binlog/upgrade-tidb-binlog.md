---
title: Upgrade TiDB Binlog
summary: Learn how to upgrade TiDB Binlog to the latest cluster version.
---

# TiDBBinlogのアップグレード {#upgrade-tidb-binlog}

このドキュメントでは、手動でデプロイされた TiDB Binlogを最新の[集まる](/tidb-binlog/tidb-binlog-overview.md)バージョンにアップグレードする方法を紹介します。 TiDB Binlog を互換性のない以前のバージョン (Kafka/ローカル バージョン) から最新バージョンにアップグレードする方法に関するセクションもあります。

## 手動でデプロイされた TiDB Binlog のアップグレード {#upgrade-tidb-binlog-deployed-manually}

TiDB Binlog を手動でデプロイする場合は、このセクションの手順に従ってください。

### Pumpのアップグレード {#upgrade-pump}

まず、クラスター内の各Pumpインスタンスを 1 つずつアップグレードします。これにより、TiDB からバイナリログを受信できるPumpインスタンスがクラスター内に常に存在することが保証されます。手順は次のとおりです。

1.  元のファイルを新しいバージョンの`pump`に置き換えます。
2.  Pumpプロセスを再起動します。

### Drainerのアップグレード {#upgrade-drainer}

次に、 Drainerコンポーネントをアップグレードします。

1.  元のファイルを新しいバージョンの`drainer`に置き換えます。
2.  Drainerプロセスを再起動します。

## TiDB Binlog をKafka/Local バージョンからクラスター バージョンにアップグレードする {#upgrade-tidb-binlog-from-kafka-local-version-to-the-cluster-version}

新しい TiDB バージョン (v2.0.8- binlog、v2.1.0-rc.5 以降) は、Kafka バージョンまたはローカル バージョンの TiDB Binlogと互換性がありません。 TiDB を新しいバージョンのいずれかにアップグレードする場合は、TiDB Binlogのクラスター バージョンを使用する必要があります。アップグレード前に Kafka またはローカル バージョンの TiDB Binlog を使用している場合は、TiDB Binlogをクラスター バージョンにアップグレードする必要があります。

TiDB Binlog のバージョンと TiDB のバージョンの対応関係を次の表に示します。

| TiDB Binlogバージョン | TiDB バージョン                          | ノート                                                                   |
| ---------------- | ----------------------------------- | --------------------------------------------------------------------- |
| 地元               | TiDB 1.0 以前                         |                                                                       |
| カフカ              | TiDB 1.0 ~ TiDB 2.1 RC5             | TiDB 1.0 は、TiDB Binlogのローカル バージョンと Kafka バージョンの両方をサポートします。            |
| クラスタ             | TiDB v2.0.8- binlog、TiDB 2.1 RC5 以降 | TiDB v2.0.8- binlog は、 TiDB Binlogのクラスター バージョンをサポートする特別な 2.0 バージョンです。 |

### アップグレード プロセス {#upgrade-process}

> **ノート：**
>
> 完全なデータをインポートしても問題ない場合は、古いバージョンを破棄して、次の[TiDBBinlogクラスタの展開](/tidb-binlog/deploy-tidb-binlog.md)に従って TiDB Binlogをデプロイできます。

元のチェックポイントからレプリケーションを再開する場合は、次の手順を実行して TiDB Binlogをアップグレードします。

1.  新しいバージョンのPumpをデプロイ。

2.  TiDB クラスター サービスを停止します。

3.  TiDB と構成をアップグレードし、 binlogデータを新しいPumpクラスターに書き込みます。

4.  TiDB クラスターをサービスに再接続します。

5.  古いバージョンのDrainer が、古いバージョンのPumpのデータをダウンストリームに完全に複製したことを確認してください。

    以下のように、 Drainerの`status`インターフェースを照会します。コマンドは次のとおりです。

    {{< copyable "" >}}

    ```bash
    curl 'http://172.16.10.49:8249/status'
    ```

    ```
    {"PumpPos":{"172.16.10.49:8250":{"offset":32686}},"Synced": true ,"DepositWindow":{"Upper":398907800202772481,"Lower":398907799455662081}}
    ```

    戻り値`Synced`が True の場合、 Drainer が古いバージョンのPumpのデータを下流に完全に複製したことを意味します。

6.  新しいバージョンのDrainerを起動します。

7.  古いバージョンのPumpとDrainerおよび依存する Kafka と ZooKeeper を閉じます。
