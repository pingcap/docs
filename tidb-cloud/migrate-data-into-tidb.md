---
title: Migrate from MySQL-Compatible Databases
summary: Learn how to migrate data from MySQL-compatible databases to TiDB Cloud using the Dumpling and TiDB Lightning tools.
---

# MySQL互換データベースからデータを移行する {#migrate-data-from-mysql-compatible-databases}

TiDBはMySQLと高い互換性があります。データがセルフホストのMySQLインスタンスからのものであるか、パブリッククラウドによって提供されるRDSサービスからのものであるかに関係なく、MySQL互換データベースからTiDBにデータをスムーズに移行できます。

このドキュメントでは、 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)を使用してMySQL互換データベースからデータをエクスポートし、 [TiDB Lightning](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview)バックエンドを使用してデータをTiDB Cloudにインポートする方法について説明します。

> **ノート：**
>
> アップストリームデータベースがAuroraの場合は、このドキュメントを参照する代わりに、 [AuroraからTiDB Cloudに一括で移行する](/tidb-cloud/migrate-from-aurora-bulk-import.md)の手順に従ってください。

## 前提条件 {#prerequisites}

MySQL互換データベースからTiDBにデータを移行する前に、サポートされているTiDB Cloudの照合が要件を満たしていることを確認してください。

デフォルトでは、 TiDB Cloudは次のCI照合をサポートします。

-   ascii_bin
-   バイナリ
-   latin1_bin
-   utf8_bin
-   utf8_general_ci
-   utf8_unicode_ci
-   utf8mb4_bin
-   utf8mb4_general_ci
-   utf8mb4_unicode_ci

## 手順1.TiUPをインストールします {#step-1-install-tiup}

TiUPは、TiDBエコシステムのパッケージマネージャーであり、1行のコマンドで任意のTiDBクラスタコンポーネントを実行するのに役立ちます。このドキュメントでは、TiUPを使用してDumplingとTiDB Lightningをインストールして実行します。

1.  TiUPをダウンロードしてインストールします。

    {{< copyable "" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2.  グローバル環境変数を宣言します。

    > **ノート：**
    >
    > インストール後、TiUPは対応する`profile`のファイルの絶対パスを表示します。次のコマンドでは、 `.bash_profile`を`profile`ファイルのパスに変更する必要があります。

    {{< copyable "" >}}

    ```shell
    source .bash_profile
    ```

## ステップ2.MySQL互換データベースからデータをエクスポートする {#step-2-export-data-from-mysql-compatible-databases}

`mysqldump`または`mydumper`を使用するなど、MySQLからデータをダンプする方法はいくつかあります。パフォーマンスとTiDBとの互換性を高めるために、 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)を使用することをお勧めします。TiDBは、PingCAPによって作成されたオープンソースツールの1つでもあります。

1.  Dumplingをインストールします：

    {{< copyable "" >}}

    ```shell
    tiup install dumpling
    ```

2.  Dumplingを使用してMySQLデータベースをエクスポートします。

    -   データをAmazonS3クラウドストレージにエクスポートするには、 [AmazonS3クラウドストレージにデータをエクスポートする](https://docs.pingcap.com/tidb/stable/dumpling-overview#export-data-to-amazon-s3-cloud-storage)を参照してください。
    -   データをローカルデータファイルにエクスポートするには、次のコマンドを使用します。

        {{< copyable "" >}}

        ```shell
        tiup dumpling -h <mysql-host> -P 3306 -u <user> -F 64MiB -t 8 -o /path/to/export/dir
        ```

        指定した一部のデータベースのみをエクスポートする場合は、 `-B`を使用してデータベース名のコンマ区切りリストを指定します。

        必要な最小権限は次のとおりです。

        -   `SELECT`
        -   `RELOAD`
        -   `LOCK TABLES`
        -   `REPLICATION CLIENT`

## ステップTiDB Cloudにデータをインポートする {#step-3-import-data-to-tidb-cloud}

ソースデータの場所とサイズに応じて、インポート方法は異なります。

-   ソースデータがAmazonS3クラウドストレージにある場合は、次の手順を実行します。

    1.  TiDBクラウドがAmazonS3バケット内のソースデータにアクセスできるようにAmazonS3アクセスを設定します。詳細については、 [AmazonS3アクセスを設定する](/tidb-cloud/migrate-from-amazon-s3-or-gcs.md#step-2-configure-amazon-s3-access)を参照してください。
    2.  TiDB Cloudコンソールから、[TiDBクラスター]ページに移動し、ターゲットクラスタの名前をクリックして、独自の概要ページに移動します。左側のクラスタ情報ペインで、[**インポート**]をクリックし、[<strong>データインポートタスク</strong>]ページでインポート関連情報を入力します。

-   ソースデータがローカルファイルにある場合は、次のいずれかを実行します。

    -   データが1TBを超える場合は、データをTiDB Cloudにインポートまたは移行するためのステージング領域としてAmazonS3またはGCSを使用することをお勧めします。詳細については、 [AmazonS3またはGCSからTiDB Cloudにインポートまたは移行します](/tidb-cloud/migrate-from-amazon-s3-or-gcs.md)を参照してください。
    -   データが1TB未満の場合は、このドキュメントの次の手順に従ってTiDB Lightningバックエンドを使用できます。

次の手順は、 TiDB Lightningバックエンドを使用してデータをTiDB Cloudにインポートする方法を示しています。

1.  TiDB Lightningをインストールします：

    {{< copyable "" >}}

    ```shell
    tiup install tidb-lightning
    ```

2.  TiDB Lightning構成ファイルを作成し、インポート情報を構成します。

    1.  TiDB Lightning構成ファイルを作成します。

        {{< copyable "" >}}

        ```shell
        vim tidb-lighting.toml
        ```

    2.  インポート情報を構成します。

        {{< copyable "" >}}

        ```toml
        [lightning] 
        # The address and port to check TiDB Lightning metrics.
        status-addr = '127.0.0.1:8289'

        [tidb]
        # The target cluster information. Fill in one address of tidb-server. 
        # For example: 172.16.128.1
        host = "${host}" 
        # The port number of the target cluster. For example: 4000
        port = ${port number}
        # The target database username. For example: root
        user = "${user_name}" 
        # The target database password. 
        password = "${password}" 

        [tikv-importer]
        # The TiDB backend to be used for data importing. 
        backend = "tidb"

        [mydumper]
        # The data source directory, supporting local path and s3.
        # For example: `/data` for local path or `s3://bucket-name/data-path` for s3
        data-source-dir = "${data_path}"  

        # When Dumpling is used to export data, the corresponding table schemas are exported too by default. 
        # If you want TiDB Lightning to automatically create table schemas in TiDB Cloud according to the exported schemas, set no-schema to false. 
        no-schema = false
        ```

        ターゲットTiDBクラスタでTLSを構成する場合、またはさらに構成を行う場合は、 [TiDB LightningConfiguration / コンフィグレーション](https://docs.pingcap.com/tidb/stable/tidb-lightning-configuration)を参照してください。

3.  TiDB Lightningを使用してデータをTiDBにインポートします：

    {{< copyable "" >}}

    ```shell
    nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```

    インポートタスクが開始された後、次のいずれかの方法でインポートの進行状況を表示できます。

    -   コマンドラインを使用して進行状況を取得するには、ログのキーワード`progress`を`grep`にします。これは、デフォルトで5分ごとに更新されます。
    -   TiDB監視フレームワークを使用してより多くの監視メトリックを取得するには、 [TiDB Lightning Monitoring](https://docs.pingcap.com/tidb/stable/monitor-tidb-lightning)を参照してください。
