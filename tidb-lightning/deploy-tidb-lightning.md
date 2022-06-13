---
title: TiDB Lightning Deployment
summary: Deploy TiDB Lightning to quickly import large amounts of new data.
---

# TiDBLightningの導入 {#tidb-lightning-deployment}

このドキュメントでは、ローカルバックエンドを使用したTiDB Lightningのハードウェア要件と、それを手動で展開する方法について説明します。

## ノート {#notes}

TiDB Lightningを開始する前に、次の点に注意してください。

-   `tidb-lightning`がクラッシュした場合、クラスタは「インポートモード」のままになります。 「通常モード」に戻すのを忘れると、TiKVクラスタ上に大量の圧縮されていないデータが発生し、異常に高いCPU使用率とストールが発生する可能性があります。 `tidb-lightning-ctl`のツールを使用して、クラスタを手動で「通常モード」に戻すことができます。

    ```sh
    bin/tidb-lightning-ctl --switch-mode=normal
    ```

## ハードウェア要件 {#hardware-requirements}

`tidb-lightning`はリソースを大量に消費するプログラムです。次のように展開することをお勧めします。

-   32以上の論理コアCPU
-   20GB以上のメモリ
-   データソース全体を保存するのに十分な大きさのSSDで、より高速な読み取り速度を優先します
-   10ギガビットネットワークカード（1GB /秒以上で転送可能）
-   `tidb-lightning`は、実行時にすべてのCPUコアを完全に消費するため、専用マシンにデプロイすることを強くお勧めします。不可能な場合は、 `tidb-lightning`を`tidb-server`などの他のコンポーネントと一緒にデプロイし、CPU使用率を`region-concurrency`設定で制限することができます。

> **ノート：**
>
> -   `tidb-lightning`はCPUを集中的に使用するプログラムです。コンポーネントが混在する環境では、 `tidb-lightning`に割り当てられるリソースを制限する必要があります。そうしないと、他のコンポーネントを実行できない可能性があります。 CPU論理コアの`region-concurrency` ％を設定することをお勧めします。たとえば、CPUに32個の論理コアがある場合、 `region-concurrency`を24に設定できます。

さらに、ターゲットTiKVクラスタには、新しいデータを吸収するのに十分なスペースが必要です。 [標準要件](/hardware-and-software-requirements.md)に加えて、ターゲットTiKVクラスタの合計空き領域は、**データソースのサイズ× <a href="/faq/manage-cluster-faq.md#is-the-number-of-replicas-in-each-region-configurable-if-yes-how-to-configure-it">レプリカの数</a>×2**よりも大きくする必要があります。

デフォルトのレプリカ数が3の場合、これは、合計空き領域がデータソースのサイズの少なくとも6倍であることを意味します。

## データのエクスポート {#export-data}

次のコマンドを使用してMySQLからデータをエクスポートするには、 [`dumpling`ツール](/dumpling-overview.md)を使用します。

```sh
./dumpling -h 127.0.0.1 -P 3306 -u root -t 16 -F 256MB -B test -f 'test.t[12]' -o /data/my_database/
```

このコマンドでは、

-   `-B test` ：データが`test`データベースからエクスポートされることを意味します。
-   `-f test.t[12]` ： `test.t1`つと`test.t2`のテーブルのみがエクスポートされることを意味します。
-   `-t 16` ：データのエクスポートに16スレッドが使用されることを意味します。
-   `-F 256MB` ：テーブルがチャンクに分割され、1つのチャンクが256MBであることを意味します。

データソースがCSVファイルで構成されている場合、構成については[CSVサポート](/tidb-lightning/migrate-from-csv-using-tidb-lightning.md)を参照してください。

## TiDBLightningをデプロイ {#deploy-tidb-lightning}

このセクションでは、 [TiDBLightningを手動でデプロイする](#deploy-tidb-lightning-manually)の方法について説明します。

### TiDBLightningを手動でデプロイ {#deploy-tidb-lightning-manually}

#### ステップ1：TiDBクラスタをデプロイする {#step-1-deploy-a-tidb-cluster}

データをインポートする前に、TiDBクラスタをデプロイする必要があります。最新の安定バージョンを使用することを強くお勧めします。

展開手順は[TiDBクイックスタートガイド](/quick-start-with-tidb.md)にあります。

#### 手順2：TiDBLightningインストールパッケージをダウンロードする {#step-2-download-the-tidb-lightning-installation-package}

TiDB Lightningパッケージをダウンロードするには、 [TiDBツールをダウンロードする](/download-ecosystem-tools.md)のドキュメントを参照してください。

> **ノート：**
>
> TiDB Lightningは、以前のバージョンのTiDBクラスターと互換性があります。 TiDBLightningインストールパッケージの最新の安定バージョンをダウンロードすることをお勧めします。

#### ステップ3： <code>tidb-lightning</code>を開始します {#step-3-start-code-tidb-lightning-code}

1.  ツールセットから`bin/tidb-lightning`と`bin/tidb-lightning-ctl`をアップロードします。

2.  データソースを同じマシンにマウントします。

3.  `tidb-lightning.toml`を構成します。以下のテンプレートに表示されない構成の場合、TiDBLightningは構成エラーをログファイルに書き込んで終了します。

    `sorted-kv-dir`は、ソートされたKey-Valueファイルの一時ストレージディレクトリを設定します。ディレクトリは空である必要があり、ストレージスペース**はインポートするデータセットのサイズよりも大きい必要があります**。詳細については、 [ダウンストリームストレージスペースの要件](/tidb-lightning/tidb-lightning-requirements.md#resource-requirements)を参照してください。

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

    上記は基本的な設定のみを示しています。設定の完全なリストについては、 [Configuration / コンフィグレーション](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-global)セクションを参照してください。

4.  `tidb-lightning`を実行します。

    ```sh
    nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```

## TiDBLightningのアップグレード {#upgrading-tidb-lightning}

バイナリのみを置き換えることで、TiDBLightningをアップグレードできます。これ以上の構成は必要ありません。 TiDB Lightningを再起動する詳細な手順については、 [FAQ](/tidb-lightning/tidb-lightning-faq.md#how-to-properly-restart-tidb-lightning)を参照してください。

インポートタスクが実行されている場合は、TiDBLightningをアップグレードする前にタスクが完了するまで待つことをお勧めします。そうしないと、チェックポイントがバージョン間で機能する保証がないため、最初から再インポートする必要がある可能性があります。
