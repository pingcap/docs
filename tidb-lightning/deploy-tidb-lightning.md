---
title: Deploy TiDB Lightning
summary: Deploy TiDB Lightning to quickly import large amounts of new data.
---

# TiDB Lightningをデプロイ {#deploy-tidb-lightning}

このドキュメントでは、 TiDB Lightningを使用してデータをインポートするためのハードウェア要件と、手動でデプロイする方法について説明します。ハードウェア リソースの要件は、インポート モードによって異なります。詳細については、次のドキュメントを参照してください。

-   [物理インポート モードの要件と制限](/tidb-lightning/tidb-lightning-physical-import-mode.md#requirements-and-restrictions)
-   [論理インポート モードの要件と制限](/tidb-lightning/tidb-lightning-logical-import-mode.md)

## TiUPを使用したオンライン展開 (推奨) {#online-deployment-using-tiup-recommended}

1.  次のコマンドを使用してTiUPをインストールします。

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

    このコマンドは、 TiUP を`PATH`環境変数に自動的に追加します。 TiUPを使用する前に、新しいターミナル セッションを開始するか、 `source ~/.bashrc`を実行する必要があります。 (環境によっては、 `source ~/.profile`実行する必要がある場合があります。具体的なコマンドについては、 TiUPの出力を確認してください。)

2.  TiUPを使用してTiDB Lightningをインストールします。

    ```shell
    tiup install tidb-lightning
    ```

## 手動展開 {#manual-deployment}

### TiDB Lightningバイナリをダウンロード {#download-tidb-lightning-binaries}

[TiDB ツールをダウンロード](/download-ecosystem-tools.md)を参照して、 TiDB Lightningバイナリをダウンロードします。 TiDB Lightning は、 TiDB の初期バージョンと完全に互換性があります。最新バージョンのTiDB Lightningを使用することをお勧めします。

TiDB Lightningバイナリ パッケージを解凍して、 `tidb-lightning`実行可能ファイルを取得します。

```bash
tar -zxvf tidb-lightning-${version}-linux-amd64.tar.gz
chmod +x tidb-lightning
```

このコマンドでは、

-   `-B test` : データが`test`データベースからエクスポートされることを意味します。
-   `-f test.t[12]` : `test.t1`と`test.t2`テーブルのみがエクスポートされることを意味します。
-   `-t 16` : データのエクスポートに 16 個のスレッドが使用されることを意味します。
-   `-F 256MB` : テーブルがチャンクに分割され、1 つのチャンクが 256 MB であることを意味します。

データ ソースが CSV ファイルで構成されている場合、構成については[CSV サポート](/tidb-lightning/migrate-from-csv-using-tidb-lightning.md)を参照してください。

## TiDB Lightningをデプロイ {#deploy-tidb-lightning}

このセクションでは、 [TiDB Lightning を手動でデプロイする](#deploy-tidb-lightning-manually)について説明します。

### TiDB Lightning を手動でデプロイ {#deploy-tidb-lightning-manually}

#### ステップ 1: TiDB クラスターをデプロイ {#step-1-deploy-a-tidb-cluster}

データをインポートする前に、TiDB クラスターをデプロイする必要があります。最新の安定版を使用することを強くお勧めします。

導入手順は[TiDB クイック スタート ガイド](/quick-start-with-tidb.md)にあります。

#### ステップ 2: TiDB Lightningインストール パッケージをダウンロードする {#step-2-download-the-tidb-lightning-installation-package}

[TiDB ツールをダウンロード](/download-ecosystem-tools.md)ドキュメントを参照して、 TiDB Lightningパッケージをダウンロードしてください。

> **ノート：**
>
> TiDB Lightning は、以前のバージョンの TiDB クラスターと互換性があります。 TiDB Lightningインストール パッケージの最新の安定バージョンをダウンロードすることをお勧めします。

#### ステップ 3: <code>tidb-lightning</code>を開始する {#step-3-start-code-tidb-lightning-code}

1.  ツール セットから`bin/tidb-lightning`と`bin/tidb-lightning-ctl`をアップロードします。

2.  データ ソースを同じマシンにマウントします。

3.  構成する`tidb-lightning.toml` .以下のテンプレートに表示されない構成の場合、 TiDB Lightning は構成エラーをログ ファイルに書き込み、終了します。

    `sorted-kv-dir`ソートされた Key-Value ファイルの一時storageディレクトリを設定します。ディレクトリは空である必要があり、storageスペース**はインポートするデータセットのサイズより大きくなければなりません**。詳細は[ダウンストリームのstorage容量要件](/tidb-lightning/tidb-lightning-requirements.md#storage-space-of-the-target-database)を参照してください。

    ```toml
    [lightning]
    # The concurrency number of data. It is set to the number of logical CPU
    # cores by default. When deploying together with other components, you can
    # set it to 75% of the size of logical CPU cores to limit the CPU usage.
    # region-concurrency =

    # Logging
    level = "info"
    file = "tidb-lightning.log"

    [tikv-importer]
    # Sets the backend to the "local" mode.
    backend = "local"
    # Sets the directory of temporary local storage.
    sorted-kv-dir = "/mnt/ssd/sorted-kv-dir"

    [mydumper]
    # Local source data directory
    data-source-dir = "/data/my_database"

    [tidb]
    # Configuration of any TiDB server from the cluster
    host = "172.16.31.1"
    port = 4000
    user = "root"
    password = ""
    # Table schema information is fetched from TiDB via this status-port.
    status-port = 10080
    # An address of pd-server.
    pd-addr = "172.16.31.4:2379"
    ```

    上記は重要な設定のみを示しています。設定の完全なリストについては、セクション[コンフィグレーション](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-global)を参照してください。

4.  `tidb-lightning`を実行します。

    ```sh
    nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```

## TiDB Lightningのアップグレード {#upgrade-tidb-lightning}

バイナリを置き換えるだけで、それ以上の構成を行わなくてもTiDB Lightningをアップグレードできます。アップグレード後、 TiDB Lightningを再起動する必要があります。詳細については、 [TiDB Lightning を適切に再起動する方法](/tidb-lightning/tidb-lightning-faq.md#how-to-properly-restart-tidb-lightning)を参照してください。

インポート タスクが実行中の場合は、完了するまで待ってからTiDB Lightningをアップグレードすることをお勧めします。そうしないと、チェックポイントがバージョン間で機能するという保証がないため、最初から再インポートする必要が生じる可能性があります。
