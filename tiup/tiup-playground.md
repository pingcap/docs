---
title: Quickly Deploy a Local TiDB Cluster
summary: TiUPのプレイグラウンドコンポーネントを使用して、ローカル TiDB クラスターをすばやくデプロイする方法を学習します。
---

# ローカル TiDBクラスタを迅速にデプロイ {#quickly-deploy-a-local-tidb-cluster}

TiDBクラスタは、複数のコンポーネントで構成される分散システムです。典型的なTiDBクラスタは、少なくとも3つのPDノード、3つのTiKVノード、そして2つのTiDBノードで構成されます。TiDBをすぐに試してみたい場合、多数のコンポーネントを手動でデプロイするのは時間がかかり、複雑だと感じるかもしれません。このドキュメントでは、 TiUPのプレイグラウンドコンポーネントと、それを使用してローカルのTiDBテスト環境を迅速に構築する方法を紹介します。

## TiUPプレイグラウンドの概要 {#tiup-playground-overview}

プレイグラウンドコンポーネントの基本的な使用方法は次のとおりです。

```bash
tiup playground ${version} [flags]
```

`tiup playground`コマンドを直接実行すると、 TiUP はローカルにインストールされた TiDB、TiKV、および PD コンポーネントを使用するか、これらのコンポーネントの安定バージョンをインストールして、1 つの TiKV インスタンス、1 つの TiDB インスタンス、1 つの PD インスタンス、および 1 つのTiFlashインスタンスで構成される TiDB クラスターを起動します。

このコマンドは実際には次の操作を実行します。

-   このコマンドはプレイグラウンドコンポーネントのバージョンを指定しないため、 TiUPはまずインストールされているプレイグラウンドコンポーネントの最新バージョンを確認します。最新バージョンがv1.12.3であると仮定すると、このコマンドは`tiup playground:v1.12.3`と同じように動作します。
-   TiUPプレイグラウンドを使用して TiDB、TiKV、および PD コンポーネントをインストールしていない場合、プレイグラウンドコンポーネントはこれらのコンポーネントの最新の安定バージョンをインストールしてから、これらのインスタンスを起動します。
-   このコマンドはTiDB、PD、およびTiKVコンポーネントのバージョンを指定しないため、 TiUPプレイグラウンドはデフォルトで各コンポーネントの最新バージョンを使用します。最新バージョンがv8.5.3であると仮定すると、このコマンドは`tiup playground:v1.12.3 v8.5.3`と同じように動作します。
-   このコマンドは各コンポーネントの数を指定しないため、デフォルトでは、 TiUPプレイグラウンドは 1 つの TiDB インスタンス、1 つの TiKV インスタンス、1 つの PD インスタンス、および 1 つのTiFlashインスタンスで構成される最小のクラスターを起動します。
-   各 TiDBコンポーネントを起動すると、 TiUPプレイグラウンドによってクラスターが正常に起動されたことが通知され、MySQL クライアント経由で TiDB クラスターに接続する方法や[TiDBダッシュボード](/dashboard/dashboard-intro.md)アクセスする方法などの役立つ情報が提供されます。

次のコマンドを使用して、プレイグラウンドコンポーネントのコマンドライン フラグを表示できます。

```shell
tiup playground --help
```

## 例 {#examples}

### 利用可能なTiDBのバージョンを確認する {#check-available-tidb-versions}

```shell
tiup list tidb
```

### 特定のバージョンの TiDB クラスターを起動する {#start-a-tidb-cluster-of-a-specific-version}

```shell
tiup playground ${version}
```

`${version}`ターゲットのバージョン番号に置き換えます。

### ナイトリーバージョンのTiDBクラスタを起動する {#start-a-tidb-cluster-of-the-nightly-version}

```shell
tiup playground nightly
```

上記のコマンドでは、 `nightly` TiDB の最新の開発バージョンを示します。

### PDのデフォルト設定を上書きする {#override-pd-s-default-configuration}

まず、 [PD構成テンプレート](https://github.com/pingcap/pd/blob/master/conf/config.toml)コピーする必要があります。コピーしたファイルを`~/config/pd.toml`に配置し、必要に応じて変更を加えた後、以下のコマンドを実行して PD のデフォルト設定を上書きできます。

```shell
tiup playground --pd.config ~/config/pd.toml
```

### デフォルトのバイナリファイルを置き換える {#replace-the-default-binary-files}

デフォルトでは、プレイグラウンドを起動すると、各コンポーネントは公式ミラーから取得したバイナリファイルを使用して起動されます。テストのために一時的にコンパイルされたローカルバイナリファイルをクラスタに配置する場合は、置換フラグ`--{comp}.binpath`使用できます。例えば、TiDBのバイナリファイルを置換するには、以下のコマンドを実行します。

```shell
tiup playground --db.binpath /xx/tidb-server
```

### 複数のコンポーネントインスタンスを起動する {#start-multiple-component-instances}

デフォルトでは、TiDB、TiKV、PDの各コンポーネントごとに1つのインスタンスのみが起動されます。各コンポーネントごとに複数のインスタンスを起動するには、次のフラグを追加します。

```shell
tiup playground --db 3 --pd 3 --kv 3
```

### TiDBクラスタを起動するときにデータを保存するタグを指定します {#specify-a-tag-when-starting-the-tidb-cluster-to-store-the-data}

TiUPプレイグラウンドを使用して起動したTiDBクラスタを停止すると、クラスタデータもすべてクリーンアップされます。TiUPTiUPグラウンドを使用してTiDBクラスタを起動し、クラスタデータが自動的にクリーンアップされないようにするには、クラスタの起動時にタグを指定します。タグを指定すると、クラスタデータは`~/.tiup/data`ディレクトリに保存されます。タグを指定するには、以下のコマンドを実行します。

```shell
tiup playground --tag ${tag_name}
```

この方法で起動したクラスタでは、クラスタの停止後もデータファイルが保持されます。このタグを使用して次回クラスタを起動すると、クラスタ停止後に保持されたデータを使用できます。

## プレイグラウンドによって開始された TiDB クラスターにすばやく接続します {#quickly-connect-to-the-tidb-cluster-started-by-playground}

TiUPは、プレイグラウンドによって起動されたローカルTiDBクラスタを自動的に検出して接続するために使用される`client`コンポーネントを提供します。使用方法は次のとおりです。

```shell
tiup client
```

このコマンドは、現在のマシン上でプレイグラウンドによって起動されたTiDBクラスタのリストをコンソールに表示します。接続するTiDBクラスタを選択してください。Enter<kbd>キー</kbd>を押すと、TiDBに接続するための組み込みMySQLクライアントが開きます。

## 起動したクラスターの情報をビュー {#view-information-of-the-started-cluster}

```shell
tiup playground display
```

上記のコマンドは次の結果を返します。

    Pid    Role     Uptime
    ---    ----     ------
    84518  pd       35m22.929404512s
    84519  tikv     35m22.927757153s
    86189  tidb     exited
    86526  tidb     34m28.293148663s

## クラスターをスケールアウトする {#scale-out-a-cluster}

クラスターをスケールアウトするためのコマンドラインパラメータは、クラスターを起動するためのものと似ています。以下のコマンドを実行することで、2つのTiDBインスタンスをスケールアウトできます。

```shell
tiup playground scale-out --db 2
```

## クラスターのスケールイン {#scale-in-a-cluster}

`tiup playground scale-in`コマンドに`pid`指定すると、対応するインスタンスをスケールインできます。 `pid`を表示するには、 `tiup playground display`実行してください。

```shell
tiup playground scale-in --pid 86526
```

## TiProxyをデプロイ {#deploy-tiproxy}

[TiProxy](/tiproxy/tiproxy-overview.md)は PingCAP の公式プロキシコンポーネントであり、クライアントと TiDBサーバーの間に配置され、負荷分散、接続の永続性、サービス検出、および TiDB のその他の機能を提供します。

TiUP v1.15.0 以降では、 TiUP Playground を使用してクラスターに TiProxy をデプロイできます。

1.  `tidb.toml`ファイルを作成し、次の構成を追加します。

        graceful-wait-before-shutdown=15

    この構成項目は、TiDB がサーバーをシャットダウンする前に待機する期間 (秒単位) を制御し、クラスターのスケールイン操作中にクライアントが切断されるのを回避します。

2.  TiDB クラスターを起動します。

    ```shell
    tiup playground v8.5.3 --tiproxy 1 --db.config tidb.toml
    ```

    プレイグラウンドコンポーネントでは、TiProxy 関連のコマンドライン フラグは次のとおりです。

    ```bash
    Flags:
          --tiproxy int                  The number of TiProxy nodes in the cluster. If not specified, TiProxy is not deployed.
          --tiproxy.binpath string       TiProxy instance binary path.
          --tiproxy.config string        TiProxy instance configuration file.
          --tiproxy.host host            Playground TiProxy host. If not provided, TiProxy will still use host flag as its host.
          --tiproxy.port int             Playground TiProxy port. If not provided, TiProxy will use 6000 as its port.
          --tiproxy.timeout int          TiProxy maximum wait time in seconds for starting. 0 means no limit (default 60).
          --tiproxy.version string       The version of TiProxy. If not specified, the latest version of TiProxy is deployed.
    ```

TiProxy の導入と使用の詳細については、 [TiProxyのインストールと使用方法](/tiproxy/tiproxy-overview.md#installation-and-usage)参照してください。

TiProxy クライアント プログラム`tiproxyctl`を使用するには、 [TiProxyコントロールをインストールする](/tiproxy/tiproxy-command-line-flags.md#install-tiproxy-control)参照してください。

## PDマイクロサービスのデプロイ {#deploy-pd-microservices}

v8.2.0以降、 TiUPを使用して[PDマイクロサービスモード](/pd-microservices.md) （実験的）のマイクロサービスをデプロイできます。TiUP Playgroundを使用して、以下の手順で`tso`と`scheduling`マイクロサービスをクラスターにデプロイできます。

```shell
tiup playground v8.5.3 --pd.mode ms --pd 3 --tso 2 --scheduling 2
```

-   `--pd.mode` : これを`ms`に設定すると、PD のマイクロサービス モードが有効になります。
-   `--pd <num>` : PDマイクロサービスのAPIの数を指定します。少なくとも`1`である必要があります。
-   `--tso <num>` : `tso`マイクロサービスにデプロイされるインスタンスの数を指定します。
-   `--scheduling <num>` : `scheduling`マイクロサービスにデプロイされるインスタンスの数を指定します。
