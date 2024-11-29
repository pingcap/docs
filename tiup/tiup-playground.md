---
title: Quickly Deploy a Local TiDB Cluster
summary: TiUPのプレイグラウンドコンポーネントを使用して、ローカル TiDB クラスターをすばやくデプロイする方法を学習します。
---

# ローカル TiDBクラスタを迅速にデプロイ {#quickly-deploy-a-local-tidb-cluster}

TiDB クラスターは、複数のコンポーネントで構成される分散システムです。一般的な TiDB クラスターは、少なくとも 3 つの PD ノード、3 つの TiKV ノード、および 2 つの TiDB ノードで構成されます。TiDB をすぐに試してみたい場合、多数のコンポーネントを手動でデプロイするのは時間がかかり、複雑であると感じるかもしれません。このドキュメントでは、 TiUPのプレイグラウンドコンポーネントと、それを使用してローカル TiDB テスト環境をすばやく構築する方法を紹介します。

## TiUP遊び場の概要 {#tiup-playground-overview}

プレイグラウンドコンポーネントの基本的な使用方法は次のとおりです。

```bash
tiup playground ${version} [flags]
```

`tiup playground`コマンドを直接実行すると、 TiUP はローカルにインストールされた TiDB、TiKV、および PD コンポーネントを使用するか、これらのコンポーネントの安定バージョンをインストールして、1 つの TiKV インスタンス、1 つの TiDB インスタンス、1 つの PD インスタンス、および 1 つのTiFlashインスタンスで構成される TiDB クラスターを起動します。

このコマンドは実際には次の操作を実行します。

-   このコマンドはプレイグラウンドコンポーネントのバージョンを指定しないため、 TiUP は最初にインストールされているプレイグラウンドコンポーネントの最新バージョンをチェックします。最新バージョンが v1.12.3 であると仮定すると、このコマンドは`tiup playground:v1.12.3`と同じように動作します。
-   TiUPプレイグラウンドを使用して TiDB、TiKV、および PD コンポーネントをインストールしていない場合、プレイグラウンドコンポーネントはこれらのコンポーネントの最新の安定バージョンをインストールしてから、これらのインスタンスを起動します。
-   このコマンドは TiDB、PD、および TiKVコンポーネントのバージョンを指定しないため、 TiUPプレイグラウンドはデフォルトで各コンポーネントの最新バージョンを使用します。最新バージョンが v8.1.1 であると仮定すると、このコマンドは`tiup playground:v1.12.3 v8.1.1`と同じように動作します。
-   このコマンドは各コンポーネントの数を指定しないため、 TiUPプレイグラウンドはデフォルトで、1 つの TiDB インスタンス、1 つの TiKV インスタンス、1 つの PD インスタンス、および 1 つのTiFlashインスタンスで構成される最小のクラスターを起動します。
-   各 TiDBコンポーネントを起動すると、 TiUPプレイグラウンドはクラスターが正常に起動したことを通知し、MySQL クライアント経由で TiDB クラスターに接続する方法や[TiDBダッシュボード](/dashboard/dashboard-intro.md)にアクセスする方法などの役立つ情報を提供します。

プレイグラウンドコンポーネントのコマンドライン フラグは次のように記述されます。

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
      --tiproxy int              TiProxy instance number
      --tiproxy.binpath string   TiProxy instance binary path
      --tiproxy.config string    TiProxy instance configuration file
      --tiproxy.host host        Playground TiProxy host. If not provided, TiProxy will still use host flag as its host
      --tiproxy.port int         Playground TiProxy port. If not provided, TiProxy will use 6000 as its port
      --tiproxy.timeout int      TiProxy max wait time in seconds for starting. 0 means no limit (default 60)
      -v, --version              Specify the version of playground
      --without-monitor          Disable the monitoring function of Prometheus and Grafana. If you do not add this flag, the monitoring function is enabled by default.
```

## 例 {#examples}

### 利用可能なTiDBバージョンを確認する {#check-available-tidb-versions}

```shell
tiup list tidb
```

### 特定のバージョンのTiDBクラスタを起動する {#start-a-tidb-cluster-of-a-specific-version}

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

まず、 [PD 構成テンプレート](https://github.com/pingcap/pd/blob/release-8.1/conf/config.toml)をコピーする必要があります。コピーしたファイルを`~/config/pd.toml`に配置し、必要に応じて変更を加えたら、次のコマンドを実行して PD のデフォルト設定を上書きできます。

```shell
tiup playground --pd.config ~/config/pd.toml
```

### デフォルトのバイナリファイルを置き換える {#replace-the-default-binary-files}

デフォルトでは、プレイグラウンドを起動すると、各コンポーネントは公式ミラーからのバイナリ ファイルを使用して起動されます。テスト用に一時的にコンパイルされたローカル バイナリ ファイルをクラスターに配置する場合は、置き換えに`--{comp}.binpath`フラグを使用できます。たとえば、TiDB のバイナリ ファイルを置き換えるには、次のコマンドを実行します。

```shell
tiup playground --db.binpath /xx/tidb-server
```

### 複数のコンポーネントインスタンスを起動する {#start-multiple-component-instances}

デフォルトでは、TiDB、TiKV、PDコンポーネントごとに 1 つのインスタンスのみが起動されます。各コンポーネントに対して複数のインスタンスを起動するには、次のフラグを追加します。

```shell
tiup playground --db 3 --pd 3 --kv 3
```

### TiDBクラスタを起動するときにタグを指定する {#specify-a-tag-when-starting-the-tidb-cluster}

TiUPプレイグラウンドを使用して起動した TiDB クラスターを停止すると、すべてのクラスター データもクリーンアップされます。TiUP プレイグラウンドを使用してTiUPクラスターを起動し、クラスター データが自動的にクリーンアップされないようにするには、クラスターの起動時にタグを指定します。タグを指定すると、クラスター データは`~/.tiup/data`ディレクトリにあります。タグを指定するには、次のコマンドを実行します。

```shell
tiup playground --tag <tagname>
```

この方法で起動したクラスターの場合、クラスターが停止した後もデータ ファイルは保持されます。次回クラスターを起動するときにこのタグを使用すると、クラスターが停止してから保持されているデータを使用できます。

## プレイグラウンドによって開始された TiDB クラスターにすばやく接続します {#quickly-connect-to-the-tidb-cluster-started-by-playground}

TiUP は、プレイグラウンドによって起動されたローカル TiDB クラスターを自動的に検出して接続するために使用される`client`コンポーネントを提供します。使用方法は次のとおりです。

```shell
tiup client
```

このコマンドは、コンソール上の現在のマシンでプレイグラウンドによって起動された TiDB クラスターのリストを表示します。接続する TiDB クラスターを選択します。Enter<kbd>を</kbd>クリックすると、組み込みの MySQL クライアントが開き、TiDB に接続します。

## 起動したクラスターの情報をビュー {#view-information-of-the-started-cluster}

```shell
tiup playground display
```

上記のコマンドは次の結果を返します。

    Pid    Role     Uptime
    ---    ----     ------
    84518  pd       35m22.929404512s
    84519  tikv     35m22.927757153s
    84520  pump     35m22.92618275s
    86189  tidb     exited
    86526  tidb     34m28.293148663s
    86190  drainer  35m19.91349249s

## クラスターをスケールアウトする {#scale-out-a-cluster}

クラスターをスケールアウトするためのコマンドライン パラメータは、クラスターを起動するためのものと似ています。次のコマンドを実行すると、2 つの TiDB インスタンスをスケールアウトできます。

```shell
tiup playground scale-out --db 2
```

## クラスターのスケールイン {#scale-in-a-cluster}

`tiup playground scale-in`コマンドで`pid`指定すると、対応するインスタンスをスケールできます。 `pid`を表示するには、 `tiup playground display`を実行します。

```shell
tiup playground scale-in --pid 86526
```
