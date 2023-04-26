---
title: Get Started with TiDB Lightning
summary: Learn how to deploy TiDB Lightning and import full backup data to TiDB.
---

# TiDB Lightningを始めよう {#get-started-with-tidb-lightning}

このチュートリアルでは、いくつかの新しいクリーンな CentOS 7 インスタンスを使用することを前提としています。 VMware、VirtualBox、またはその他のツールを使用して、仮想マシンをローカルに展開するか、ベンダー提供のプラットフォームに小規模なクラウド仮想マシンを展開できます。 TiDB Lightning は大量のコンピューター リソースを消費するため、最高のパフォーマンスで実行するには、少なくとも 16 GB のメモリと 32 コアの CPU を割り当てることをお勧めします。

> **警告：**
>
> このチュートリアルのデプロイ方法は、テストと試用のみに推奨されます。**本番環境または開発環境では適用しないでください。**

## フルバックアップデータを準備する {#prepare-full-backup-data}

まず、 [`dumpling`](/dumpling-overview.md)使用して MySQL からデータをエクスポートします。

{{< copyable "" >}}

```sh
tiup dumpling -h 127.0.0.1 -P 3306 -u root -t 16 -F 256MB -B test -f 'test.t[12]' -o /data/my_database/
```

上記のコマンドで:

-   `-B test` : データが`test`データベースからエクスポートされることを意味します。
-   `-f test.t[12]` : `test.t1`と`test.t2`テーブルのみがエクスポートされることを意味します。
-   `-t 16` : データのエクスポートに 16 個のスレッドが使用されることを意味します。
-   `-F 256MB` : テーブルがチャンクに分割され、1 つのチャンクが 256 MB であることを意味します。

このコマンドを実行すると、フル バックアップ データが`/data/my_database`ディレクトリにエクスポートされます。

## TiDB Lightningをデプロイ {#deploy-tidb-lightning}

### ステップ 1: TiDB クラスターをデプロイ {#step-1-deploy-a-tidb-cluster}

データをインポートする前に、TiDB クラスターをデプロイする必要があります。このチュートリアルでは、TiDB v5.4.0 を例として使用します。配備方法については、 [TiUPを使用して TiDBクラスタをデプロイ](/production-deployment-using-tiup.md)を参照してください。

### ステップ 2: TiDB Lightningインストール パッケージをダウンロードする {#step-2-download-tidb-lightning-installation-package}

TiDB Lightningインストール パッケージはTiDB Toolkitに含まれています。 TiDB Toolkitをダウンロードするには、 [TiDB ツールをダウンロード](/download-ecosystem-tools.md)を参照してください。

> **ノート：**
>
> TiDB Lightning は、以前のバージョンの TiDB クラスターと互換性があります。 TiDB Lightningインストール パッケージの最新の安定バージョンをダウンロードすることをお勧めします。

### ステップ 3: <code>tidb-lightning</code>を開始する {#step-3-start-code-tidb-lightning-code}

1.  パッケージ内の`bin/tidb-lightning`と`bin/tidb-lightning-ctl` TiDB Lightningがデプロイされているサーバーにアップロードします。

2.  [準備されたデータソース](#prepare-full-backup-data)をサーバーにアップロードします。

3.  `tidb-lightning.toml`を次のように構成します。

    ```toml
    [lightning]
    # Logging
    level = "info"
    file = "tidb-lightning.log"

    [tikv-importer]
    # Configure the import mode
    backend = "local"
    # Sets the directory for temporarily storing the sorted key-value pairs.
    # The target directory must be empty.
    sorted-kv-dir = "/mnt/ssd/sorted-kv-dir"

    [mydumper]
    # Local source data directory
    data-source-dir = "/data/my_datasource/"

    # Configures the wildcard rule. By default, all tables in the mysql, sys, INFORMATION_SCHEMA, PERFORMANCE_SCHEMA, METRICS_SCHEMA, and INSPECTION_SCHEMA system databases are filtered.
    # If this item is not configured, the "cannot find schema" error occurs when system tables are imported.
    filter = ['*.*', '!mysql.*', '!sys.*', '!INFORMATION_SCHEMA.*', '!PERFORMANCE_SCHEMA.*', '!METRICS_SCHEMA.*', '!INSPECTION_SCHEMA.*']
    [tidb]
    # Information of the target cluster
    host = "172.16.31.2"
    port = 4000
    user = "root"
    password = "rootroot"
    # Table schema information is fetched from TiDB via this status-port.
    status-port = 10080
    # The PD address of the cluster
    pd-addr = "172.16.31.3:2379"
    ```

4.  パラメータを適切に設定したら、 `nohup`コマンドを使用して`tidb-lightning`プロセスを開始します。コマンドラインでコマンドを直接実行すると、SIGHUP シグナルを受信したためにプロセスが終了する場合があります。代わりに、 `nohup`コマンドを含む bash スクリプトを実行することをお勧めします。

    {{< copyable "" >}}

    ```sh
    #!/bin/bash
    nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```

### ステップ 4: データの整合性を確認する {#step-4-check-data-integrity}

インポートが完了すると、 TiDB Lightning は自動的に終了します。インポートが成功すると、ログ ファイルの最後の行に`tidb lightning exit`が表示されます。

エラーが発生した場合は、 [TiDB LightningFAQ](/tidb-lightning/tidb-lightning-faq.md)を参照してください。

## まとめ {#summary}

このチュートリアルでは、 TiDB Lightning とは何か、およびTiDB Lightningクラスターを迅速に展開してフル バックアップ データを TiDB クラスターにインポートする方法を簡単に紹介します。

TiDB Lightningの詳細な機能と使用方法については、 [TiDB Lightningの概要](/tidb-lightning/tidb-lightning-overview.md)を参照してください。
