---
title: Quickly Deploy a Local TiDB Cluster
summary: Learn how to quickly deploy a local TiDB cluster using the playground component of TiUP.
---

# ローカルTiDBクラスターを迅速にデプロイする {#quickly-deploy-a-local-tidb-cluster}

TiDBクラスタは、複数のコンポーネントで構成される分散システムです。一般的なTiDBクラスタは、少なくとも3つのPDノード、3つのTiKVノード、および2つのTiDBノードで構成されます。 TiDBをすばやく体験したい場合は、非常に多くのコンポーネントを手動でデプロイするのに時間がかかり、複雑になることがあります。このドキュメントでは、TiUPのプレイグラウンドコンポーネントと、それを使用してローカルTiDBテスト環境をすばやく構築する方法を紹介します。

## TiUPプレイグラウンドの概要 {#tiup-playground-overview}

遊び場コンポーネントの基本的な使用法を以下に示します。

```bash
tiup playground ${version} [flags]
```

`tiup playground`コマンドを直接実行する場合、TiUPはローカルにインストールされたTiDB、TiKV、およびPDコンポーネントを使用するか、これらのコンポーネントの安定バージョンをインストールして、1つのTiKVインスタンス、1つのTiDBインスタンス、1つのPDインスタンス、および1つのTiDBクラスタで構成されるTiDBクラスターを開始します。 TiFlashインスタンス。

このコマンドは、実際には次の操作を実行します。

-   このコマンドはプレイグラウンドコンポーネントのバージョンを指定しないため、TiUPは最初にインストールされているプレイグラウンドコンポーネントの最新バージョンをチェックします。最新バージョンがv1.10.0であるとすると、このコマンドは`tiup playground:v1.10.0`と同じように機能します。
-   TiUPプレイグラウンドを使用してTiDB、TiKV、およびPDコンポーネントをインストールしていない場合、プレイグラウンドコンポーネントは、これらのコンポーネントの最新の安定バージョンをインストールしてから、これらのインスタンスを起動します。
-   このコマンドはTiDB、PD、およびTiKVコンポーネントのバージョンを指定しないため、TiUPプレイグラウンドはデフォルトで各コンポーネントの最新バージョンを使用します。最新バージョンがv6.1.0であるとすると、このコマンドは`tiup playground:v1.10.0 v6.1.0`と同じように機能します。
-   このコマンドは各コンポーネントの数を指定しないため、TiUPプレイグラウンドは、デフォルトで、1つのTiDBインスタンス、1つのTiKVインスタンス、1つのPDインスタンス、および1つのTiFlashインスタンスで構成される最小のクラスタを開始します。
-   各TiDBコンポーネントを開始した後、TiUPプレイグラウンドは、クラスタが正常に開始されたことを通知し、MySQLクライアントを介してTiDBクラスタに接続する方法や[TiDBダッシュボード](/dashboard/dashboard-intro.md)にアクセスする方法などのいくつかの有用な情報を提供します。

プレイグラウンドコンポーネントのコマンドラインフラグは次のとおりです。

```bash
Flags:
      --db int                   Specify the number of TiDB instances (default: 1)
      --db.host host             Specify the listening address of TiDB
      --db.port int              Specify the port of TiDB
      --db.binpath string        Specify the TiDB instance binary path (optional, for debugging)
      --db.config string         Specify the TiDB instance configuration file (optional, for debugging)
      --db.timeout int           Specify TiDB maximum wait time in seconds for starting. 0 means no limit
      --drainer int              Specify Drainer data of the cluster
      --drainer.binpath string   Specify the location of the Drainer binary files (optional, for debugging)
      --drainer.config string    Specify the Drainer configuration file
  -h, --help                     help for tiup
      --host string              Specify the listening address of each component (default: `127.0.0.1`). Set it to `0.0.0.0` if provided for access of other machines
      --kv int                   Specify the number of TiKV instances (default: 1)
      --kv.binpath string        Specify the TiKV instance binary path (optional, for debugging)
      --kv.config string         Specify the TiKV instance configuration file (optional, for debugging)
      --mode string              Specify the playground mode: 'tidb' (default) and 'tikv-slim'
      --pd int                   Specify the number of PD instances (default: 1)
      --pd.host host             Specify the listening address of PD
      --pd.binpath string        Specify the PD instance binary path (optional, for debugging)
      --pd.config string         Specify the PD instance configuration file (optional, for debugging)
      --pump int                 Specify the number of Pump instances. If the value is not `0`, TiDB Binlog is enabled.
      --pump.binpath string      Specify the location of the Pump binary files (optional, for debugging)
      --pump.config string       Specify the Pump configuration file (optional, for debugging)
      -T, --tag string           Specify a tag for playground
      --ticdc int                Specify the number of TiCDC instances (default: 0)
      --ticdc.binpath string     Specify the TiCDC instance binary path (optional, for debugging)
      --ticdc.config string      Specify the TiCDC instance configuration file (optional, for debugging)
      --tiflash int              Specify the number of TiFlash instances (default: 1)
      --tiflash.binpath string   Specify the TiFlash instance binary path (optional, for debugging)
      --tiflash.config string    Specify the TiFlash instance configuration file (optional, for debugging)
      --tiflash.timeout int      Specify TiFlash maximum wait time in seconds for starting. 0 means no limit
      -v, --version              Specify the version of playground
      --without-monitor          Disable the monitoring function of Prometheus and Grafana. If you do not add this flag, the monitoring function is enabled by default.
```

## 例 {#examples}

### 利用可能なTiDBバージョンを確認する {#check-available-tidb-versions}

{{< copyable "" >}}

```shell
tiup list tidb
```

### 特定のバージョンのTiDBクラスタを開始します {#start-a-tidb-cluster-of-a-specific-version}

{{< copyable "" >}}

```shell
tiup playground ${version}
```

`${version}`をターゲットバージョン番号に置き換えます。

### ナイトリーバージョンのTiDBクラスタを開始します {#start-a-tidb-cluster-of-the-nightly-version}

{{< copyable "" >}}

```shell
tiup playground nightly
```

上記のコマンドで、 `nightly`はTiDBの最新の開発バージョンを示します。

### PDのデフォルト設定を上書きする {#override-pd-s-default-configuration}

まず、 [PD構成テンプレート](https://github.com/pingcap/pd/blob/master/conf/config.toml)をコピーする必要があります。コピーしたファイルを`~/config/pd.toml`に配置し、必要に応じていくつかの変更を加えたとすると、次のコマンドを実行して、PDのデフォルト構成を上書きできます。

{{< copyable "" >}}

```shell
tiup playground --pd.config ~/config/pd.toml
```

### デフォルトのバイナリファイルを置き換えます {#replace-the-default-binary-files}

デフォルトでは、プレイグラウンドが開始されると、各コンポーネントは公式ミラーのバイナリファイルを使用して開始されます。一時的にコンパイルされたローカルバイナリファイルをテストのためにクラスタに配置する場合は、 `--{comp}.binpath`フラグを使用して置き換えることができます。たとえば、次のコマンドを実行して、TiDBのバイナリファイルを置き換えます。

{{< copyable "" >}}

```shell
tiup playground --db.binpath /xx/tidb-server
```

### 複数のコンポーネントインスタンスを開始します {#start-multiple-component-instances}

デフォルトでは、TiDB、TiKV、およびPDコンポーネントごとに1つのインスタンスのみが開始されます。コンポーネントごとに複数のインスタンスを開始するには、次のフラグを追加します。

{{< copyable "" >}}

```shell
tiup playground --db 3 --pd 3 --kv 3
```

## 遊び場によって開始されたTiDBクラスタにすばやく接続する {#quickly-connect-to-the-tidb-cluster-started-by-playground}

TiUPは、プレイグラウンドによって開始されたローカルTiDBクラスタを自動的に検索して接続するために使用される`client`つのコンポーネントを提供します。使用法は次のとおりです。

{{< copyable "" >}}

```shell
tiup client
```

このコマンドは、コンソール上の現在のマシンのプレイグラウンドによって開始されたTiDBクラスターのリストを提供します。接続するTiDBクラスタを選択します。 [ <kbd>Enter</kbd> ]をクリックすると、組み込みのMySQLクライアントが開いてTiDBに接続します。

## 開始されたクラスタの情報をビューする {#view-information-of-the-started-cluster}

{{< copyable "" >}}

```shell
tiup playground display
```

上記のコマンドは、次の結果を返します。

```
Pid    Role     Uptime
---    ----     ------
84518  pd       35m22.929404512s
84519  tikv     35m22.927757153s
84520  pump     35m22.92618275s
86189  tidb     exited
86526  tidb     34m28.293148663s
86190  drainer  35m19.91349249s
```

## クラスタをスケールアウトする {#scale-out-a-cluster}

クラスタを開始するためのパラメーターと似ています。次のコマンドを実行すると、2つのTiDBインスタンスをスケールアウトできます。

{{< copyable "" >}}

```shell
tiup playground scale-out --db 2
```

## クラスタでのスケーリング {#scale-in-a-cluster}

`tiup playground scale-in`コマンドに`pid`を指定して、対応するインスタンスでスケーリングできます。 `pid`を表示するには、 `tiup playground display`を実行します。

{{< copyable "" >}}

```shell
tiup playground scale-in --pid 86526
```
