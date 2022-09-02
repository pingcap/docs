---
title: TiDB Lightning Deployment
summary: Deploy TiDB Lightning to quickly import large amounts of new data.
---

# TiDB Lightningの導入 {#tidb-lightning-deployment}

このドキュメントでは、ローカル バックエンドを使用するTiDB Lightningのハードウェア要件と、手動でデプロイする方法について説明します。

## ノート {#notes}

TiDB Lightningを開始する前に、次の点に注意してください。

-   `tidb-lightning`がクラッシュした場合、クラスターは「インポート モード」のままになります。 「通常モード」に戻すのを忘れると、TiKV クラスター上に圧縮されていない大量のデータが発生し、異常に高い CPU 使用率とストールが発生する可能性があります。 `tidb-lightning-ctl`ツールを使用して、クラスターを手動で「通常モード」に戻すことができます。

    ```sh
    bin/tidb-lightning-ctl --switch-mode=normal
    ```

## ハードウェア要件 {#hardware-requirements}

`tidb-lightning`は、リソースを大量に消費するプログラムです。以下のように展開することをお勧めします。

-   32 以上の論理コア CPU
-   20GB以上のメモリ
-   データ ソース全体を格納するのに十分な大きさの SSD、より高速な読み取り速度を優先する
-   10 ギガビット ネットワーク カード (1 GB/秒以上で転送可能)
-   `tidb-lightning`は、実行時にすべての CPU コアを完全に消費するため、専用のマシンにデプロイすることを強くお勧めします。不可能な場合は、 `tidb-lightning`を`tidb-server`などの他のコンポーネントと一緒にデプロイし、CPU 使用率を`region-concurrency`設定で制限することができます。

> **ノート：**
>
> -   `tidb-lightning`は CPU を集中的に使用するプログラムです。コンポーネントが混在する環境では、 `tidb-lightning`に割り当てるリソースを制限する必要があります。そうしないと、他のコンポーネントが実行できなくなる可能性があります。 CPU 論理コアの`region-concurrency` ～ 75% を設定することをお勧めします。たとえば、CPU に 32 個の論理コアがある場合、 `region-concurrency` ～ 24 を設定できます。

さらに、ターゲット TiKV クラスターには、新しいデータを吸収するのに十分なスペースが必要です。 [標準要件](/hardware-and-software-requirements.md)以外に、ターゲット TiKV クラスターの合計空き容量は、**データ ソースのサイズ × <a href="/faq/manage-cluster-faq.md#is-the-number-of-replicas-in-each-region-configurable-if-yes-how-to-configure-it">レプリカの数</a>× 2**より大きくなければなりません。

デフォルトのレプリカ カウントが 3 の場合、これは合計空き領域がデータ ソースのサイズの少なくとも 6 倍である必要があることを意味します。

## データのエクスポート {#export-data}

[`dumpling`ツール](/dumpling-overview.md)を使用して、次のコマンドを使用して MySQL からデータをエクスポートします。

```sh
./dumpling -h 127.0.0.1 -P 3306 -u root -t 16 -F 256MB -B test -f 'test.t[12]' -o /data/my_database/
```

このコマンドでは、

-   `-B test` : データが`test`データベースからエクスポートされることを意味します。
-   `-f test.t[12]` : `test.t1`と`test.t2`のテーブルのみがエクスポートされることを意味します。
-   `-t 16` : データのエクスポートに 16 個のスレッドが使用されることを意味します。
-   `-F 256MB` : テーブルがチャンクに分割され、1 つのチャンクが 256 MB であることを意味します。

データ ソースが CSV ファイルで構成されている場合、構成については[CSV サポート](/tidb-lightning/migrate-from-csv-using-tidb-lightning.md)を参照してください。

## TiDB Lightningをデプロイ {#deploy-tidb-lightning}

このセクションでは、方法について説明し[TiDB Lightningを手動でデプロイする](#deploy-tidb-lightning-manually) 。

### TiDB Lightningを手動でデプロイ {#deploy-tidb-lightning-manually}

#### ステップ 1: TiDB クラスターをデプロイする {#step-1-deploy-a-tidb-cluster}

データをインポートする前に、TiDB クラスターをデプロイする必要があります。最新の安定版を使用することを強くお勧めします。

導入手順は[TiDB クイック スタート ガイド](/quick-start-with-tidb.md)にあります。

#### ステップ 2: TiDB Lightningインストール パッケージをダウンロードする {#step-2-download-the-tidb-lightning-installation-package}

[TiDB ツールをダウンロード](/download-ecosystem-tools.md)ドキュメントを参照して、 TiDB Lightningパッケージをダウンロードしてください。

> **ノート：**
>
> TiDB Lightningは、以前のバージョンの TiDB クラスターと互換性があります。 TiDB Lightningインストール パッケージの最新の安定バージョンをダウンロードすることをお勧めします。

#### ステップ 3: <code>tidb-lightning</code>を開始する {#step-3-start-code-tidb-lightning-code}

1.  ツール セットから`bin/tidb-lightning`と`bin/tidb-lightning-ctl`をアップロードします。

2.  データ ソースを同じマシンにマウントします。

3.  構成する`tidb-lightning.toml` .以下のテンプレートに表示されない構成の場合、 TiDB Lightningは構成エラーをログ ファイルに書き込み、終了します。

    `sorted-kv-dir`は、ソートされた Key-Value ファイルの一時ストレージ ディレクトリを設定します。ディレクトリは空である必要があり、ストレージ スペース**はインポートするデータセットのサイズより大きくなければなりません**。詳細は[ダウンストリームのストレージ容量要件](/tidb-lightning/tidb-lightning-requirements.md#resource-requirements)を参照してください。

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

    上記は重要な設定のみを示しています。設定の完全なリストについては、セクション[Configuration / コンフィグレーション](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-global)を参照してください。

4.  `tidb-lightning`を実行します。

    ```sh
    nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```

## TiDB Lightningのアップグレード {#upgrading-tidb-lightning}

バイナリのみを置き換えるだけで、 TiDB Lightningをアップグレードできます。これ以上の構成は必要ありません。 TiDB Lightningを再起動する詳細な手順については、 [FAQ](/tidb-lightning/tidb-lightning-faq.md#how-to-properly-restart-tidb-lightning)を参照してください。

インポート タスクが実行中の場合は、完了するまで待ってからTiDB Lightningをアップグレードすることをお勧めします。そうしないと、チェックポイントがバージョン間で機能するという保証がないため、最初から再インポートする必要が生じる可能性があります。
