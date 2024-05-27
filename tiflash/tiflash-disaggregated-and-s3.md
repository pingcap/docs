---
title: TiFlash Disaggregated Storage and Compute Architecture and S3 Support
summary: TiFlash の分散storageとコンピューティングアーキテクチャ、および S3 サポートについて学習します。
---

# TiFlash分散ストレージおよびコンピューティングアーキテクチャと S3 サポート {#tiflash-disaggregated-storage-and-compute-architecture-and-s3-support}

デフォルトでは、 TiFlashは結合storageおよびコンピューティングアーキテクチャを使用して展開され、各TiFlashノードはstorageとコンピューティング ノードの両方として機能します。TiDB v7.0.0 以降、 TiFlash は分散storageおよびコンピューティングアーキテクチャをサポートし、Amazon S3 または S3 互換オブジェクトstorage(MinIO など) にデータを保存できます。

## アーキテクチャの概要 {#architecture-overview}

![TiFlash Write and Compute Separation Architecture](/media/tiflash/tiflash-s3.png)

分散storageおよびコンピューティングアーキテクチャでは、 TiFlashプロセスのさまざまな機能が分割され、書き込みノードとコンピューティング ノードの 2 種類のノードに割り当てられます。これら 2 種類のノードは個別に展開し、独立して拡張できるため、必要に応じて展開する書き込みノードとコンピューティング ノードの数を決定できます。

-   TiFlash書き込みノード

    書き込みノードは、TiKVからRaftログデータを受け取り、データを列指向形式に変換し、一定期間内に更新されたすべてのデータを定期的にパッケージ化してS3にアップロードします。また、書き込みノードは、クエリパフォーマンスを向上させるために継続的にデータを整理したり、無駄なデータを削除したりするなど、S3上のデータを管理します。

    書き込みノードは、メモリの過剰な使用を避けるために、ローカル ディスク (通常は NVMe SSD) を使用して最新の書き込みデータをキャッシュします。

-   TiFlashコンピューティングノード

    コンピューティング ノードは、TiDB ノードから送信されたクエリ要求を実行します。最初に書き込みノードにアクセスしてデータ スナップショットを取得し、次に書き込みノードから最新のデータ (つまり、まだ S3 にアップロードされていないデータ) を読み取り、残りのほとんどのデータを S3 から読み取ります。

    コンピューティング ノードは、ローカル ディスク (通常は NVMe SSD) をデータ ファイルのキャッシュとして使用し、リモートの場所 (書き込みノードまたは S3) から同じデータを繰り返し読み取ることを回避し、クエリ パフォーマンスを向上させます。

    コンピューティング ノードはステートレスであり、スケーリング速度は第 2 レベルです。この機能を使用すると、次のようにコストを削減できます。

    -   クエリのワークロードが低い場合は、コンピューティング ノードの数を減らしてコストを節約します。クエリがない場合は、すべてのコンピューティング ノードを停止することもできます。
    -   クエリのワークロードが増加した場合は、コンピューティング ノードの数を迅速に増やして、クエリのパフォーマンスを確保します。

## シナリオ {#scenarios}

TiFlashの分散storageおよびコンピューティングアーキテクチャは、コスト効率の高いデータ分析サービスに適しています。このアーキテクチャでは、storageリソースとコンピューティング リソースを必要に応じて個別に拡張できるため、次のシナリオで大きなメリットが得られます。

-   データ量は多いですが、頻繁にクエリされるデータはごくわずかです。データのほとんどはコールド データであり、めったにクエリされません。このとき、頻繁にクエリされるデータは通常、コンピューティング ノードのローカル SSD にキャッシュされ、高速なクエリ パフォーマンスを提供しますが、その他ほとんどのコールド データは、ストレージstorageを節約するために、低コストの S3 またはその他のオブジェクトstorageに保存されます。

-   コンピューティング リソースの需要には明らかなピークと谷があります。たとえば、集中的な調整クエリは通常夜間に実行され、大量のコンピューティング リソースを必要とします。この場合、夜間に一時的にコンピューティング ノードを追加することを検討できます。一方、他の時間帯には、通常のクエリ タスクを完了するために必要なコンピューティング ノードは少なくなります。

## 前提条件 {#prerequisites}

1.  TiFlashデータを保存するための Amazon S3 バケットを準備します。

    既存のバケットを使用することもできますが、各 TiDB クラスターに専用のキープレフィックスを予約する必要があります。S3 バケットの詳細については、 [AWS ドキュメント](https://docs.aws.amazon.com/en_us/AmazonS3/latest/userguide/creating-buckets-s3.html)参照してください。

    [ミニオ](https://min.io/)などの他の S3 互換オブジェクトstorageを使用することもできます。

    TiFlash は、データにアクセスするために次の S3 API を使用する必要があります。TiDB クラスター内のTiFlashノードにこれらの API に対する必要な権限があることを確認してください。

    -   オブジェクトを置く
    -   オブジェクトの取得
    -   オブジェクトのコピー
    -   オブジェクトの削除
    -   リストオブジェクトV2
    -   オブジェクトタグ付けを取得
    -   PutBucketライフサイクル

2.  TiDB クラスターに、結合storageおよびコンピューティングアーキテクチャを使用してデプロイされたTiFlashノードがないことを確認します。ある場合は、すべてのテーブルのTiFlashレプリカ数を`0`に設定してから、すべてのTiFlashノードを削除します。例:

    ```sql
    SELECT * FROM INFORMATION_SCHEMA.TIFLASH_REPLICA; # Query all tables with TiFlash replicas
    ALTER TABLE table_name SET TIFLASH REPLICA 0;     # Set the TiFlash replica count of all tables to `0`
    ```

    ```shell
    tiup cluster scale-in mycluster -N 'node0,node1...' # Remove all TiFlash nodes
    tiup cluster display mycluster                     # Wait for all TiFlash nodes to enter the Tombstone state
    tiup cluster prune mycluster                       # Remove all TiFlash nodes in the Tombstone state
    ```

## 使用法 {#usage}

デフォルトでは、 TiUP は結合storageおよびコンピューティングアーキテクチャにTiFlashを展開します。分散storageおよびコンピューティングアーキテクチャにTiFlashを展開する必要がある場合は、手動で構成するために次の手順に従います。

1.  次の構成で、 `scale-out.topo.yaml`などのTiFlashトポロジ構成ファイルを準備します。

    ```yaml
    tiflash_servers:
      # In the TiFlash topology configuration file, the `storage.s3` configuration indicates that the disaggregated storage and compute architecture is used for deployment.
      # If `flash.disaggregated_mode: tiflash_compute` is configured for a node, it is a Compute Node.
      # If `flash.disaggregated_mode: tiflash_write` is configured for a node, it is a Write Node.

      # 172.31.8.1~2 are TiFlash Write Nodes
      - host: 172.31.8.1
        config:
          flash.disaggregated_mode: tiflash_write               # This is a Write Node
          storage.s3.endpoint: http://s3.{region}.amazonaws.com # S3 endpoint address
          storage.s3.bucket: mybucket                           # TiFlash stores all data in this bucket
          storage.s3.root: /cluster1_data                       # Root directory where data is stored in the S3 bucket
          storage.s3.access_key_id: {ACCESS_KEY_ID}             # Access S3 with ACCESS_KEY_ID
          storage.s3.secret_access_key: {SECRET_ACCESS_KEY}     # Access S3 with SECRET_ACCESS_KEY
          storage.main.dir: ["/data1/tiflash/data"]             # Local data directory of the Write Node. Configure it in the same way as the directory configuration of the coupled storage and compute architecture
      - host: 172.31.8.2
        config:
          flash.disaggregated_mode: tiflash_write               # This is a Write Node
          storage.s3.endpoint: http://s3.{region}.amazonaws.com # S3 endpoint address
          storage.s3.bucket: mybucket                           # TiFlash stores all data in this bucket
          storage.s3.root: /cluster1_data                       # Root directory where data is stored in the S3 bucket
          storage.s3.access_key_id: {ACCESS_KEY_ID}             # Access S3 with ACCESS_KEY_ID
          storage.s3.secret_access_key: {SECRET_ACCESS_KEY}     # Access S3 with SECRET_ACCESS_KEY
          storage.main.dir: ["/data1/tiflash/data"]             # Local data directory of the Write Node. Configure it in the same way as the directory configuration of the coupled storage and compute architecture

      # 172.31.9.1~2 are TiFlash Compute Nodes
      - host: 172.31.9.1
        config:
          flash.disaggregated_mode: tiflash_compute             # This is a Compute Node
          storage.s3.endpoint: http://s3.{region}.amazonaws.com # S3 endpoint address
          storage.s3.bucket: mybucket                           # TiFlash stores all data in this bucket
          storage.s3.root: /cluster1_data                       # Root directory where data is stored in the S3 bucket
          storage.s3.access_key_id: {ACCESS_KEY_ID}             # Access S3 with ACCESS_KEY_ID
          storage.s3.secret_access_key: {SECRET_ACCESS_KEY}     # Access S3 with SECRET_ACCESS_KEY
          storage.main.dir: ["/data1/tiflash/data"]             # Local data directory of the Compute Node. Configure it in the same way as the directory configuration of the coupled storage and compute architecture
          storage.remote.cache.dir: /data1/tiflash/cache        # Local data cache directory of the Compute Node
          storage.remote.cache.capacity: 858993459200           # 800 GiB
      - host: 172.31.9.2
        config:
          flash.disaggregated_mode: tiflash_compute             # This is a Compute Node
          storage.s3.endpoint: http://s3.{region}.amazonaws.com # S3 endpoint address
          storage.s3.bucket: mybucket                           # TiFlash stores all data in this bucket
          storage.s3.root: /cluster1_data                       # Root directory where data is stored in the S3 bucket
          storage.s3.access_key_id: {ACCESS_KEY_ID}             # Access S3 with ACCESS_KEY_ID
          storage.s3.secret_access_key: {SECRET_ACCESS_KEY}     # Access S3 with SECRET_ACCESS_KEY
          storage.main.dir: ["/data1/tiflash/data"]             # Local data directory of the Compute Node. Configure it in the same way as the directory configuration of the coupled storage and compute architecture
          storage.remote.cache.dir: /data1/tiflash/cache        # Local data cache directory of the Compute Node
          storage.remote.cache.capacity: 858993459200           # 800 GiB
    ```

    -   なお、上記`ACCESS_KEY_ID`と`SECRET_ACCESS_KEY`は設定ファイルに直接記述されています。環境変数を使用して個別に設定することもできます。両方の方法で設定した場合、環境変数が優先されます。

        環境変数を使用して`ACCESS_KEY_ID`と`SECRET_ACCESS_KEY`を構成するには、 TiFlashプロセスが展開されているすべてのマシンでTiFlashプロセスを開始するユーザー環境 (通常は`tidb` ) に切り替え、 `~/.bash_profile`を変更して次の構成を追加します。

        ```shell
        export S3_ACCESS_KEY_ID={ACCESS_KEY_ID}
        export S3_SECRET_ACCESS_KEY={SECRET_ACCESS_KEY}
        ```

    -   `storage.s3.endpoint` `http`または`https`モードを使用して S3 に接続することをサポートしており、URL を直接変更することでモードを設定できます。たとえば、 `https://s3.{region}.amazonaws.com` 。

2.  TiFlashノードを追加し、 TiFlashレプリカの数をリセットします。

    ```shell
    tiup cluster scale-out mycluster ./scale-out.topo.yaml
    ```

    ```sql
    ALTER TABLE table_name SET TIFLASH REPLICA 1;
    ```

3.  分散storageおよびコンピューティングアーキテクチャを使用してTiFlash をクエリするように TiDB 構成を変更します。

    1.  TiDB 構成ファイルを編集モードで開きます。

        ```shell
        tiup cluster edit-config mycluster
        ```

    2.  TiDB 構成ファイルに次の構成項目を追加します。

        ```shell
        server_configs:
        tidb:
        disaggregated-tiflash: true   # Query TiFlash using the disaggregated storage and compute architecture
        ```

    3.  TiDBを再起動します。

        ```shell
        tiup cluster reload mycluster -R tidb
        ```

## 制限 {#restrictions}

-   TiFlash は**、分散型storageおよびコンピューティングアーキテクチャ**と結合**型storageおよびコンピューティングアーキテクチャ**間のインプレース切り替えをサポートしていません。分散型アーキテクチャに切り替える前に、結合型アーキテクチャを使用して展開されている既存のTiFlashノードをすべて削除する必要があります。
-   あるアーキテクチャから別のアーキテクチャに移行した後、すべてのTiFlashデータを再度複製する必要があります。
-   同じ TiDB クラスターでは、同じアーキテクチャのTiFlashノードのみが許可されます。 1 つのクラスターに 2 つのアーキテクチャを共存させることはできません。
-   分散型storageおよびコンピューティングアーキテクチャはS3 API を使用したオブジェクトstorageのみをサポートしますが、結合型storageおよびコンピューティングアーキテクチャはローカルstorageのみをサポートします。
-   S3storageを使用する場合、 TiFlashノードは自身のノード上にないファイルのキーを取得できないため、 [保存時の暗号化](/encryption-at-rest.md)機能は使用できません。
