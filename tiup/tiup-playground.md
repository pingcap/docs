---
title: Quickly Deploy a Local TiDB Cluster
summary: TiUPのプレイグラウンドコンポーネントを使用して、ローカルTiDBクラスタを迅速にデプロイする方法を学びましょう。
---

# ローカルTiDBクラスタを迅速にデプロイ {#quickly-deploy-a-local-tidb-cluster}

TiDBクラスタは、複数のコンポーネントで構成される分散システムです。一般的なTiDBクラスタは、少なくとも3つのPDノード、3つのTiKVノード、および2つのTiDBノードで構成されます。TiDBをすぐに試してみたい場合、これほど多くのコンポーネントを手動でデプロイするのは時間と手間がかかるかもしれません。このドキュメントでは、 TiUPのプレイグラウンドコンポーネントと、それを使用してローカルのTiDBテスト環境を迅速に構築する方法について説明します。

## TiUP遊具施設の概要 {#tiup-playground-overview}

プレイグラウンドコンポーネントの基本的な使用方法を以下に示します。

```bash
tiup playground ${version} [flags]
```

`tiup playground`コマンドを直接実行すると、 TiUP はローカルにインストールされている TiDB、TiKV、および PD コンポーネントを使用するか、これらのコンポーネントの安定版をインストールして、1 つの TiKV インスタンス、1 つの TiDB インスタンス、1 つの PD インスタンス、および 1 つのTiFlashインスタンスで構成される TiDB クラスタを起動します。

このコマンドは実際には以下の操作を実行します。

-   このコマンドではプレイグラウンドコンポーネントのバージョンが指定されていないため、 TiUP はまずインストールされているプレイグラウンドコンポーネントの最新バージョンを確認します。最新バージョンが v1.12.3 であると仮定すると、このコマンドは`tiup playground:v1.12.3`と同じように動作します。
-   TiUP playgroundを使用してTiDB、TiKV、およびPDコンポーネントをインストールしていない場合、playgroundコンポーネントはこれらのコンポーネントの最新の安定版をインストールし、その後これらのインスタンスを起動します。
-   このコマンドでは TiDB、PD、TiKVコンポーネントのバージョンが指定されていないため、 TiUP playground はデフォルトで各コンポーネントの最新バージョンを使用します。最新バージョンが v8.5.4 であると仮定すると、このコマンドは`tiup playground:v1.12.3 v8.5.4`と同じように動作します。
-   このコマンドでは各コンポーネントの数を指定しないため、 TiUP playground はデフォルトで、TiDB インスタンス、TiKV インスタンス、PD インスタンス、 TiFlashインスタンスがそれぞれ 1 つずつで構成される最小のクラスタを起動します。
-   TiDB の各コンポーネントを起動した後、 TiUPプレイグラウンドはクラスターが正常に起動したことを通知し、MySQL クライアントを介して TiDB クラスターに接続する方法や、 [TiDBダッシュボード](/dashboard/dashboard-intro.md)にアクセスする方法など、いくつかの有用な情報を提供します。

プレイグラウンドコンポーネントのコマンドラインフラグを表示するには、次のコマンドを使用できます。

```shell
tiup playground --help
```

## 例 {#examples}

### 利用可能なTiDBバージョンを確認してください {#check-available-tidb-versions}

```shell
tiup list tidb
```

### 特定のバージョンのTiDBクラスタを起動する {#start-a-tidb-cluster-of-a-specific-version}

```shell
tiup playground ${version}
```

`${version}`対象のバージョン番号に置き換えてください。

### ナイトリーバージョンのTiDBクラスタを起動します {#start-a-tidb-cluster-of-the-nightly-version}

```shell
tiup playground nightly
```

上記のコマンドにおいて、 `nightly` TiDBの最新開発バージョンを示します。

### PDのデフォルト設定を上書きする {#override-pd-s-default-configuration}

まず、 [PD構成テンプレート](https://github.com/pingcap/pd/blob/master/conf/config.toml)をコピーする必要があります。コピーしたファイルを`~/config/pd.toml`に配置し、必要に応じて変更を加えたと仮定すると、次のコマンドを実行して PD のデフォルト設定を上書きできます。

```shell
tiup playground --pd.config ~/config/pd.toml
```

### デフォルトのバイナリファイルを置き換える {#replace-the-default-binary-files}

デフォルトでは、プレイグラウンドが起動されると、各コンポーネントは公式ミラーのバイナリファイルを使用して起動されます。テストのために一時的にコンパイルされたローカルバイナリファイルをクラスタに配置したい場合は、置換フラグ`--{comp}.binpath`を使用できます。たとえば、TiDB のバイナリファイルを置き換えるには、次のコマンドを実行します。

```shell
tiup playground --db.binpath /xx/tidb-server
```

### 複数のコンポーネントインスタンスを起動する {#start-multiple-component-instances}

デフォルトでは、TiDB、TiKV、PDの各コンポーネントに対して1つのインスタンスのみが起動されます。各コンポーネントに対して複数のインスタンスを起動するには、次のフラグを追加してください。

```shell
tiup playground --db 3 --pd 3 --kv 3
```

### TiDBクラスタの起動時に、データを保存するタグを指定します。 {#specify-a-tag-when-starting-the-tidb-cluster-to-store-the-data}

TiUP playground を使用して起動した TiDB クラスタを停止すると、クラスタデータもすべてクリーンアップされます。TiUP playground を使用してTiUPクラスタを起動し、クラスタデータが自動的にクリーンアップされないようにするには、クラスタ起動時にタグを指定できます。タグを指定すると、クラスタデータは`~/.tiup/data`ディレクトリに保存されます。タグを指定するには、次のコマンドを実行します。

```shell
tiup playground --tag ${tag_name}
```

このように起動したクラスターの場合、クラスター停止後もデータファイルは保持されます。次回クラスターを起動する際にこのタグを使用することで、クラスター停止以降に保持されたデータを利用することができます。

## TiDBダッシュボードとGrafanaにアクセスする {#access-tidb-dashboard-and-grafana}

TiUP playgroundを使用してTiDBクラスタを起動すると、ブラウザで次のアドレスにアクセスすることで、 [TiDBダッシュボード](/dashboard/dashboard-intro.md)とGrafanaにアクセスできます。

-   TiDBダッシュボード： `http://127.0.0.1:2379/dashboard`

    -   デフォルトのユーザー名: `root`
    -   デフォルトパスワード: `` (空欄の場合は、直接`Enter`を押してください)

-   グラファナ： `http://127.0.0.1:3000`

    -   デフォルトのユーザー名: `admin`
    -   デフォルトパスワード: `admin`

> **注記：**
>
> TiDB `root`ユーザーのパスワードを変更した場合は、新しいパスワードを使用してTiDBダッシュボードにログインしてください。

## playground で起動した TiDB クラスターにすばやく接続します {#quickly-connect-to-the-tidb-cluster-started-by-playground}

TiUPは、playgroundによって起動されたローカルTiDBクラスタを自動的に検出して接続するために使用される`client`コンポーネントを提供します。使用方法は以下のとおりです。

```shell
tiup client
```

このコマンドを実行すると、コンソールに、現在のマシン上でplaygroundによって起動されたTiDBクラスタの一覧が表示されます。接続するTiDBクラスタを選択してください。Enter<kbd>キー</kbd>を押すと、TiDBに接続するための組み込みのMySQLクライアントが開きます。

## 起動したクラスターの情報をビュー {#view-information-of-the-started-cluster}

```shell
tiup playground display
```

上記のコマンドを実行すると、以下の結果が返されます。

    Pid    Role     Uptime
    ---    ----     ------
    84518  pd       35m22.929404512s
    84519  tikv     35m22.927757153s
    86189  tidb     exited
    86526  tidb     34m28.293148663s

## クラスターをスケールアウトする {#scale-out-a-cluster}

クラスタをスケールアウトするためのコマンドラインパラメータは、クラスタを起動するためのパラメータと似ています。以下のコマンドを実行することで、2つのTiDBインスタンスをスケールアウトできます。

```shell
tiup playground scale-out --db 2
```

## クラスタースケールイン {#scale-in-a-cluster}

対応するインスタンスでスケールするには、 `tiup playground scale-in`コマンドで`pid`を指定できます。5 `pid`表示するには、 `tiup playground display`実行します。

```shell
tiup playground scale-in --pid 86526
```

## TiProxyをデプロイ {#deploy-tiproxy}

[TiProxy](/tiproxy/tiproxy-overview.md)はPingCAPの公式プロキシコンポーネントであり、クライアントとTiDBサーバーの間に配置され、TiDBの負荷分散、接続の永続性、サービス検出、およびその他の機能を提供します。

TiUP v1.15.0以降では、 TiUP Playgroundを使用してクラスターにTiProxyをデプロイできます。

1.  ファイル`tidb.toml`を作成し、以下の設定を追加してください。

        graceful-wait-before-shutdown=15

    この設定項目は、TiDBがサーバーをシャットダウンするまでの待機時間（秒単位）を制御し、クラスタのスケールイン操作中にクライアントが切断されるのを防ぎます。

2.  TiDBクラスタを起動します。

    ```shell
    tiup playground v8.5.4 --tiproxy 1 --db.config tidb.toml
    ```

    プレイグラウンドコンポーネントにおけるTiProxy関連のコマンドラインフラグは以下のとおりです。

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

TiProxyのデプロイと使用方法の詳細については、 [TiProxyのインストールと使用方法](/tiproxy/tiproxy-overview.md#installation-and-usage)参照してください。

TiProxyクライアントプログラム`tiproxyctl`を使用するには、 [TiProxy Controlをインストールする](/tiproxy/tiproxy-command-line-flags.md#install-tiproxy-control)参照してください。

## PDマイクロサービスをデプロイ {#deploy-pd-microservices}

バージョン8.2.0以降、 [PDマイクロサービスモード](/pd-microservices.md) （実験的）はTiUPを使用してデプロイできます。TiUP Playgroundを使用して、クラスター用に`tso`マイクロサービスと`scheduling`マイクロサービスを次のようにデプロイできます。

```shell
tiup playground v8.5.4 --pd.mode ms --pd 3 --tso 2 --scheduling 2
```

-   `--pd.mode` ：これを`ms`に設定すると、PDのマイクロサービスモードが有効になります。
-   `--pd <num>` : PDマイクロサービスのAPIの数を指定します。少なくとも`1`ある必要があります。
-   `--tso <num>` ： `tso`マイクロサービスにデプロイするインスタンスの数を指定します。
-   `--scheduling <num>` ： `scheduling`マイクロサービスにデプロイするインスタンスの数を指定します。
