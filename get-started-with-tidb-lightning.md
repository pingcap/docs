---
title: Quick Start for TiDB Lightning
summary: TiDB Lightning は、MySQL データを TiDB クラスターにインポートするためのツールです。本番や開発環境ではなく、テストおよび試用目的のみに推奨されます。プロセスには、完全バックアップ データの準備、TiDB クラスターのデプロイ、 TiDB Lightningのインストール、 TiDB Lightningの起動、およびデータ整合性のチェックが含まれます。詳細な機能と使用方法については、 TiDB Lightning の概要を参照してください。
---

# TiDB Lightningのクイック スタート {#quick-start-for-tidb-lightning}

このドキュメントでは、MySQL データを TiDB クラスターにインポートしてTiDB Lightningを使い始めるためのクイック ガイドを提供します。

> **警告：**
>
> このチュートリアルのデプロイメント方法は、テストとトライアルにのみ推奨されます。**本番や開発環境には適用しないでください。**

## ステップ1: 完全バックアップデータを準備する {#step-1-prepare-full-backup-data}

まず、 [団子](/dumpling-overview.md)使用して MySQL からデータをエクスポートできます。

1.  `tiup --version`実行して、 TiUPがすでにインストールされているかどうかを確認します。TiUPがインストールされている場合は、この手順をスキップします。TiUPがインストールされていない場合は、次のコマンドを実行します。

        curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh

2.  TiUP を使用してDumplingをインストールする:

    ```shell
    tiup install dumpling
    ```

3.  MySQL からデータをエクスポートするには、 [Dumpling を使用してデータをエクスポートする](/dumpling-overview.md#export-to-sql-files)に記載されている詳細な手順を参照してください。

    ```sh
    tiup dumpling -h 127.0.0.1 -P 3306 -u root -t 16 -F 256MB -B test -f 'test.t[12]' -o /data/my_database/
    ```

    上記のコマンドでは:

    -   `-t 16` : 16 スレッドを使用してデータをエクスポートします。
    -   `-F 256MB` : 各テーブルを複数のファイルに分割し、各ファイルのサイズは約 256 MB になります。
    -   `-B test` : `test`データベースからエクスポートします。
    -   `-f 'test.t[12]'` : テーブル`test.t1`と`test.t2` 2 つのみをエクスポートします。

    エクスポートされた完全バックアップ データは`/data/my_database`ディレクトリに保存されます。

## ステップ2: TiDBクラスターをデプロイ {#step-2-deploy-the-tidb-cluster}

データのインポートを開始する前に、インポート用の TiDB クラスターをデプロイする必要があります。すでに TiDB クラスターがある場合は、この手順をスキップできます。

TiDB クラスターをデプロイする手順については、 [TiDB データベース プラットフォームのクイック スタート ガイド](/quick-start-with-tidb.md)を参照してください。

## ステップ3: TiDB Lightningをインストールする {#step-3-install-tidb-lightning}

次のコマンドを実行して、 TiDB Lightningの最新バージョンをインストールします。

```shell
tiup install tidb-lightning
```

## ステップ4: TiDB Lightningを起動する {#step-4-start-tidb-lightning}

> **注記：**
>
> このセクションのインポート方法は、テストと機能体験にのみ適しています。本番環境では、 [大規模なデータセットをMySQLからTiDBに移行する](/migrate-large-mysql-to-tidb.md)を参照してください。

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

2.  `tidb-lightning`を実行します。 `nohup`使用してコマンドラインで直接プログラムを起動するときに`SIGHUP`シグナルによってプログラムが終了するのを回避するには、 `nohup`コマンドをスクリプトに配置することをお勧めします。 例:

    ```shell
    #!/bin/bash
    nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```

## ステップ5: データの整合性を確認する {#step-5-check-data-integrity}

インポートが完了すると、 TiDB Lightning は自動的に終了します。インポートが成功した場合は、ログ ファイルの最後の行に`tidb lightning exit`表示されます。

エラーが発生した場合は、 [TiDB Lightningよくある質問](/tidb-lightning/tidb-lightning-faq.md)を参照してください。

## まとめ {#summary}

このチュートリアルでは、 TiDB Lightningとは何か、またTiDB Lightningクラスターをすばやく展開して完全バックアップ データを TiDB クラスターにインポートする方法について簡単に説明します。

TiDB Lightningの詳細な機能と使用方法については、 [TiDB Lightning の概要](/tidb-lightning/tidb-lightning-overview.md)を参照してください。
