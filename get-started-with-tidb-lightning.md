---
title: Quick Start for TiDB Lightning
summary: TiDB Lightningは、MySQLデータをTiDBクラスタにインポートするためのツールです。本番や開発環境ではなく、テストおよび試用目的でのみ使用することをお勧めします。このプロセスには、フルバックアップデータの準備、TiDBクラスタのデプロイ、 TiDB Lightningのインストール、 TiDB Lightningの起動、およびデータ整合性のチェックが含まれます。詳細な機能と使用方法については、 TiDB Lightningの概要を参照してください。
---

# TiDB Lightningクイックスタート {#quick-start-for-tidb-lightning}

このドキュメントでは、MySQLデータをTiDBクラスタにインポートすることでTiDB Lightningを使い始めるための簡単なガイドを提供します。

> **警告：**
>
> このチュートリアルで紹介するデプロイ方法は、テストおよび試用のみを推奨します。**本番や開発環境では適用しないでください。**

## ステップ1：フルバックアップデータを準備する {#step-1-prepare-full-backup-data}

まず、[Dumpling](/dumpling-overview.md)を使用してMySQLからデータをエクスポートします。

1.  TiUPが既にインストールされているかどうかを確認するには、 `tiup --version`を実行してください。TiUPがインストールされている場合は、この手順をスキップしてください。TiUPがインストールされていない場合は、次のコマンドを実行してください。

        curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh

2.  TiUPを使用してDumplingをインストールする方法：

    ```shell
    tiup install dumpling
    ```

3.  MySQL からデータをエクスポートするには、 [Dumplingを使用してデータをエクスポートする](/dumpling-overview.md#export-to-sql-files)に記載されている詳細な手順を参照してください。

    ```sh
    tiup dumpling -h 127.0.0.1 -P 3306 -u root -t 16 -F 256MB -B test -f 'test.t[12]' -o /data/my_database/
    ```

    上記のコマンドでは：

    -   `-t 16` : 16 スレッドを使用してデータをエクスポートします。
    -   `-F 256MB` : 各テーブルを複数のファイルに分割し、各ファイルのサイズは約 256 MB にします。
    -   `-B test` : `test`データベースからエクスポートします。
    -   `-f 'test.t[12]'` : 2 つのテーブル`test.t1`と`test.t2`のみをエクスポートします。

    エクスポートされた完全なバックアップデータは、 `/data/my_database`ディレクトリに保存されます。

## ステップ2：TiDBクラスタをデプロイ {#step-2-deploy-the-tidb-cluster}

データインポートを開始する前に、インポート用のTiDBクラスタをデプロイする必要があります。既にTiDBクラスタをお持ちの場合は、この手順をスキップできます。

TiDB クラスターのデプロイ手順については、 [TiDB Self-Managedのクイックスタート](/quick-start-with-tidb.md)を参照してください。

## ステップ3： TiDB Lightningをインストールする {#step-3-install-tidb-lightning}

最新バージョンのTiDB Lightningをインストールするには、以下のコマンドを実行してください。

```shell
tiup install tidb-lightning
```

## ステップ4： TiDB Lightningを起動する {#step-4-start-tidb-lightning}

> **注記：**
>
> このセクションのインポート方法は、テストと機能体験にのみ適しています。本番環境については、 [MySQLからTiDBへの大規模データセットの移行](/migrate-large-mysql-to-tidb.md)を参照してください。

1.  構成ファイル`tidb-lightning.toml`を作成し、クラスタ情報に基づいて以下の設定を入力してください。

    ```toml
    [lightning]
    # Logging
    level = "info"
    file = "tidb-lightning.log"

    [tikv-importer]
    # Configure the import mode
    backend = "local"
    # Sets the directory for temporarily storing the sorted key-value pairs. The target directory must be empty.
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
    # The PD address of the cluster. Starting from v7.6.0, TiDB supports setting multiple PD addresses.
    pd-addr = "172.16.31.3:2379,56.78.90.12:3456"
    ```

2.  `tidb-lightning`を実行します。 `SIGHUP`を使用してコマンドラインから直接プログラムを起動したときに、 `nohup`シグナルによってプログラムが終了するのを避けるため、 `nohup`コマンドをスクリプトに記述することをお勧めします。例:

    ```shell
    #!/bin/bash
    nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```

## ステップ5：データの整合性を確認する {#step-5-check-data-integrity}

インポートが完了すると、 TiDB Lightning は自動的に終了します。インポートが成功した場合、ログファイルの最終行に`tidb lightning exit`が表示されます。

エラーが発生した場合は、 [TiDB Lightningよくある質問](/tidb-lightning/tidb-lightning-faq.md)を参照してください。

## まとめ {#summary}

このチュートリアルでは、TiDB Lightningとは何か、そしてTiDB Lightningクラスタを迅速にデプロイして完全なバックアップデータをTiDBクラスタにインポートする方法について簡単に説明します。

TiDB Lightning の詳しい機能や使い方については、 [TiDB Lightningの概要](/tidb-lightning/tidb-lightning-overview.md)をご覧ください。

## 関連リソース {#related-resources}

<RelatedResources>
  <ResourceCard title="TiDB Admin Lab 6: Importing Data into TiDB Using TiDB Lightning" type="lab" link="https://labs.tidb.io/labs/dba_303_lab_ff5" imgSrc="https://lab-static.pingcap.com/quick-demo/dba_303_ch07_en.png" duration="60 mins" />
</RelatedResources>
