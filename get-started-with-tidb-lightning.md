---
title: Quick Start for TiDB Lightning
summary: TiDB Lightningは、MySQLデータをTiDBクラスタにインポートするためのツールです。本番や開発環境ではなく、テストおよびトライアル用途にのみ推奨されます。このプロセスには、フルバックアップデータの準備、TiDBクラスタのデプロイ、 TiDB Lightningのインストール、 TiDB Lightningの起動、そしてデータ整合性のチェックが含まれます。詳細な機能と使用方法については、 TiDB Lightningの概要をご覧ください。
---

# TiDB Lightningのクイックスタート {#quick-start-for-tidb-lightning}

このドキュメントでは、MySQL データを TiDB クラスターにインポートしてTiDB Lightningを使い始めるためのクイック ガイドを提供します。

> **警告：**
>
> このチュートリアルで紹介するデプロイ方法は、テストおよび試行目的のみに推奨されます。**本番や開発環境には適用しないでください。**

## ステップ1: 完全バックアップデータを準備する {#step-1-prepare-full-backup-data}

まず、 [団子](/dumpling-overview.md)使用して MySQL からデータをエクスポートできます。

1.  `tiup --version`実行して、 TiUPが既にインストールされているかどうかを確認します。TiUPがインストールされている場合は、この手順をスキップしてください。TiUPがインストールされていない場合は、以下のコマンドを実行してください。

        curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh

2.  TiUPを使用してDumplingをインストールする:

    ```shell
    tiup install dumpling
    ```

3.  MySQL からデータをエクスポートするには、 [Dumplingを使用してデータをエクスポートする](/dumpling-overview.md#export-to-sql-files)に記載されている詳細な手順を参照してください。

    ```sh
    tiup dumpling -h 127.0.0.1 -P 3306 -u root -t 16 -F 256MB -B test -f 'test.t[12]' -o /data/my_database/
    ```

    上記のコマンドでは、

    -   `-t 16` : 16 スレッドを使用してデータをエクスポートします。
    -   `-F 256MB` : 各テーブルを複数のファイルに分割します。各ファイルのサイズは約 256 MB になります。
    -   `-B test` : `test`データベースからエクスポートします。
    -   `-f 'test.t[12]'` : テーブル`test.t1`と`test.t2` 2 つのテーブルのみをエクスポートします。

    エクスポートされた完全バックアップ データは`/data/my_database`ディレクトリに保存されます。

## ステップ2: TiDBクラスターをデプロイ {#step-2-deploy-the-tidb-cluster}

データのインポートを開始する前に、インポート用のTiDBクラスターをデプロイする必要があります。既にTiDBクラスターをお持ちの場合は、この手順をスキップできます。

TiDB クラスターをデプロイする手順については、 [TiDBセルフマネージドのクイックスタート](/quick-start-with-tidb.md)を参照してください。

## ステップ3: TiDB Lightningをインストールする {#step-3-install-tidb-lightning}

次のコマンドを実行して、 TiDB Lightningの最新バージョンをインストールします。

```shell
tiup install tidb-lightning
```

## ステップ4: TiDB Lightningを起動する {#step-4-start-tidb-lightning}

> **注記：**
>
> このセクションのインポート方法は、テストおよび機能確認にのみ適しています。本番環境では、 [大規模データセットをMySQLからTiDBに移行する](/migrate-large-mysql-to-tidb.md)を参照してください。

1.  構成ファイル`tidb-lightning.toml`を作成し、クラスター情報に基づいて次の設定を入力します。

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

2.  `tidb-lightning`実行します。コマンドラインで`nohup`使用して直接プログラムを起動した際に`SIGHUP`シグナルによってプログラムが終了してしまうのを防ぐため、 `nohup`コマンドをスクリプトに含めることをお勧めします。例:

    ```shell
    #!/bin/bash
    nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```

## ステップ5: データの整合性を確認する {#step-5-check-data-integrity}

インポートが完了すると、 TiDB Lightning は自動的に終了します。インポートが成功した場合、ログファイルの最終行に`tidb lightning exit`表示されます。

エラーが発生した場合は、 [TiDB Lightningに関するよくある質問](/tidb-lightning/tidb-lightning-faq.md)を参照してください。

## まとめ {#summary}

このチュートリアルでは、TiDB Lightningとは何か、またTiDB Lightningクラスターを迅速に展開して完全バックアップ データを TiDB クラスターにインポートする方法について簡単に説明します。

TiDB Lightning の詳細な機能と使用方法については、 [TiDB Lightning の概要](/tidb-lightning/tidb-lightning-overview.md)を参照してください。
