---
title: TiDB Lightning Tutorial
summary: Learn how to deploy TiDB Lightning and import full backup data to TiDB.
---

# TiDBLightningチュートリアル {#tidb-lightning-tutorial}

[TiDB Lightning](https://github.com/pingcap/tidb-lightning)は、大量のデータをTiDBクラスタに高速に完全にインポートするために使用されるツールです。現在、TiDB Lightningは、SQLまたはCSVデータソースを介してエクスポートされたSQLダンプの読み取りをサポートしています。次の2つのシナリオで使用できます。

-   **大量**の<strong>新しい</strong>データ<strong>をすばやく</strong>インポートする
-   すべてのデータをバックアップおよび復元する

![Architecture of TiDB Lightning tool set](/media/tidb-lightning-architecture.png)

## 前提条件 {#prerequisites}

このチュートリアルでは、いくつかの新しくクリーンなCentOS7インスタンスを使用することを前提としています。 VMware、VirtualBox、またはその他のツールを使用して、仮想マシンをローカルに展開したり、ベンダー提供のプラットフォームに小さなクラウド仮想マシンを展開したりできます。 TiDB Lightningは大量のコンピュータリソースを消費するため、最高のパフォーマンスで実行するには、少なくとも16GBのメモリと32コアのCPUを割り当てることをお勧めします。

> **警告：**
>
> このチュートリアルの展開方法は、テストと試行にのみ推奨されます。**本番環境または開発環境には適用しないでください。**

## 完全バックアップデータを準備する {#prepare-full-backup-data}

まず、 [`dumpling`](/dumpling-overview.md)を使用してMySQLからデータをエクスポートします。

{{< copyable "" >}}

```sh
./dumpling -h 127.0.0.1 -P 3306 -u root -t 16 -F 256MB -B test -f 'test.t[12]' -o /data/my_database/
```

上記のコマンドでは：

-   `-B test` ：データが`test`データベースからエクスポートされることを意味します。
-   `-f test.t[12]` ： `test.t1`つと`test.t2`のテーブルのみがエクスポートされることを意味します。
-   `-t 16` ：データのエクスポートに16スレッドが使用されることを意味します。
-   `-F 256MB` ：テーブルがチャンクに分割され、1つのチャンクが256MBであることを意味します。

このコマンドを実行すると、完全バックアップデータが`/data/my_database`ディレクトリにエクスポートされます。

## TiDBLightningをデプロイ {#deploy-tidb-lightning}

### ステップ1：TiDBクラスタをデプロイ {#step-1-deploy-tidb-cluster}

データをインポートする前に、TiDBクラスタをデプロイする必要があります。このチュートリアルでは、例としてTiDBv5.4.0を使用します。展開方法については、 [TiUPを使用してTiDBクラスターをデプロイする](/production-deployment-using-tiup.md)を参照してください。

### ステップ2：TiDBLightningインストールパッケージをダウンロードする {#step-2-download-tidb-lightning-installation-package}

TiDB Lightningインストールパッケージは、TiDBツールキットに含まれています。 TiDB Toolkitをダウンロードするには、 [TiDBツールをダウンロードする](/download-ecosystem-tools.md)を参照してください。

> **ノート：**
>
> TiDB Lightningは、以前のバージョンのTiDBクラスターと互換性があります。 TiDBLightningインストールパッケージの最新の安定バージョンをダウンロードすることをお勧めします。

### ステップ3： <code>tidb-lightning</code>を開始します {#step-3-start-code-tidb-lightning-code}

1.  パッケージ内の`bin/tidb-lightning`と`bin/tidb-lightning-ctl`を、TiDBLightningがデプロイされているサーバーにアップロードします。

2.  [準備されたデータソース](#prepare-full-backup-data)をサーバーにアップロードします。

3.  `tidb-lightning.toml`を次のように構成します。

    ```toml
    [lightning]
    # Logging
    level = "info"
    file = "tidb-lightning.log"

    [tikv-importer]
    # Uses the Local-backend
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

4.  パラメータを適切に設定した後、 `nohup`コマンドを使用して`tidb-lightning`プロセスを開始します。コマンドラインでコマンドを直接実行すると、SIGHUP信号を受信したためにプロセスが終了する場合があります。代わりに、 `nohup`コマンドを含むbashスクリプトを実行することをお勧めします。

    {{< copyable "" >}}

    ```sh
    #!/bin/bash
    nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```

### ステップ4：データの整合性を確認する {#step-4-check-data-integrity}

インポートが完了すると、TiDBLightningは自動的に終了します。インポートが成功すると、ログファイルの最後の行に`tidb lightning exit`が表示されます。

エラーが発生した場合は、 [TiDB LightningFAQ](/tidb-lightning/tidb-lightning-faq.md)を参照してください。

## 概要 {#summary}

このチュートリアルでは、TiDB Lightningとは何か、およびTiDBLightningクラスターをすばやく展開して完全バックアップデータをTiDBクラスタにインポートする方法を簡単に紹介しクラスタ。

TiDB Lightningの詳細な機能と使用法については、 [TiDBLightningの概要](/tidb-lightning/tidb-lightning-overview.md)を参照してください。
