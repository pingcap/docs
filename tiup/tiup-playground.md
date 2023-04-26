---
title: Quickly Deploy a Local TiDB Cluster
summary: Learn how to quickly deploy a local TiDB cluster using the playground component of TiUP.
---

# ローカル TiDBクラスタをすばやくデプロイ {#quickly-deploy-a-local-tidb-cluster}

TiDB クラスターは、複数のコンポーネントで構成される分散システムです。一般的な TiDB クラスターは、少なくとも 3 つの PD ノード、3 つの TiKV ノード、および 2 つの TiDB ノードで構成されます。 TiDB を手早く体験したい場合、非常に多くのコンポーネントを手動で展開するのは時間がかかり、複雑であることに気付くかもしれません。このドキュメントでは、TiUPのプレイグラウンドコンポーネントと、それを使用してローカルの TiDB テスト環境をすばやく構築する方法を紹介します。

## TiUPプレイグラウンド概要 {#tiup-playground-overview}

プレイグラウンドコンポーネントの基本的な使用方法は次のとおりです。

```bash
tiup playground ${version} [flags]
```

`tiup playground`コマンドを直接実行すると、 TiUP はローカルにインストールされた TiDB、TiKV、および PD コンポーネントを使用するか、これらのコンポーネントの安定バージョンをインストールして、1 つの TiKV インスタンス、1 つの TiDB インスタンス、1 つの PD インスタンス、および 1 つの TiDB クラスターで構成される TiDB クラスターを開始します。 TiFlashインスタンス。

このコマンドは、実際には次の操作を実行します。

-   このコマンドはプレイグラウンドコンポーネントのバージョンを指定しないため、 TiUP はインストールされているプレイグラウンドコンポーネントの最新バージョンを最初にチェックします。最新バージョンが v1.11.3 であると仮定すると、このコマンドは`tiup playground:v1.11.3`と同じように機能します。
-   TiUPプレイグラウンドを使用して TiDB、TiKV、および PD コンポーネントをインストールしていない場合、プレイグラウンドコンポーネントはこれらのコンポーネントの最新の安定したバージョンをインストールしてから、これらのインスタンスを起動します。
-   このコマンドは TiDB、PD、および TiKVコンポーネントのバージョンを指定しないため、 TiUPプレイグラウンドはデフォルトで各コンポーネントの最新バージョンを使用します。最新バージョンが v6.5.2 であると仮定すると、このコマンドは`tiup playground:v1.11.3 v6.5.2`と同じように機能します。
-   このコマンドは各コンポーネントの数を指定しないため、 TiUPプレイグラウンドはデフォルトで、1 つの TiDB インスタンス、1 つの TiKV インスタンス、1 つの PD インスタンス、および 1 つのTiFlashインスタンスで構成される最小のクラスターを開始します。
-   各 TiDBコンポーネントを開始した後、 TiUPプレイグラウンドは、クラスターが正常に開始されたことを通知し、MySQL クライアントを介して TiDB クラスターに接続する方法や[TiDB ダッシュボード](/dashboard/dashboard-intro.md)にアクセスする方法など、いくつかの有用な情報を提供します。

プレイグラウンドコンポーネントのコマンドライン フラグは、次のように記述されています。

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

### 利用可能な TiDB のバージョンを確認する {#check-available-tidb-versions}

```shell
tiup list tidb
```

### 特定のバージョンの TiDB クラスターを開始する {#start-a-tidb-cluster-of-a-specific-version}

```shell
tiup playground ${version}
```

`${version}`ターゲットのバージョン番号に置き換えます。

### ナイトリー版の TiDB クラスターを起動する {#start-a-tidb-cluster-of-the-nightly-version}

```shell
tiup playground nightly
```

上記のコマンドで、 `nightly` TiDB の最新の開発バージョンを示します。

### PD のデフォルト設定をオーバーライドする {#override-pd-s-default-configuration}

まず、 [PD 構成テンプレート](https://github.com/pingcap/pd/blob/master/conf/config.toml)をコピーする必要があります。コピーしたファイルを`~/config/pd.toml`に配置し、必要に応じて変更を加えると仮定すると、次のコマンドを実行して PD のデフォルト構成をオーバーライドできます。

```shell
tiup playground --pd.config ~/config/pd.toml
```

### デフォルトのバイナリ ファイルを置き換える {#replace-the-default-binary-files}

デフォルトでは、プレイグラウンドが開始されると、公式ミラーのバイナリ ファイルを使用して各コンポーネントが開始されます。一時的にコンパイルされたローカル バイナリ ファイルをテスト用にクラスターに配置する場合は、 `--{comp}.binpath`フラグを使用して置き換えることができます。たとえば、次のコマンドを実行して、TiDB のバイナリ ファイルを置き換えます。

```shell
tiup playground --db.binpath /xx/tidb-server
```

### 複数のコンポーネントインスタンスを開始する {#start-multiple-component-instances}

デフォルトでは、TiDB、TiKV、および PDコンポーネントごとに 1 つのインスタンスのみが開始されます。コンポーネントごとに複数のインスタンスを開始するには、次のフラグを追加します。

```shell
tiup playground --db 3 --pd 3 --kv 3
```

### TiDBクラスター起動時にタグを指定する {#specify-a-tag-when-starting-the-tidb-cluster}

TiUPプレイグラウンドを使用して開始された TiDB クラスターを停止すると、すべてのクラスター データもクリーンアップされます。 TiUPプレイグラウンドを使用して TiDB クラスターを開始し、クラスター データが自動的にクリーンアップされないようにするには、クラスターの開始時にタグを指定します。タグを指定すると、 `~/.tiup/data`ディレクトリにクラスター データが表示されます。次のコマンドを実行して、タグを指定します。

```shell
tiup playground --tag <tagname>
```

この方法で開始されたクラスターの場合、データ ファイルはクラスターの停止後も保持されます。このタグを使用して次回クラスターを開始すると、クラスターの停止以降に保持されたデータを使用できます。

## プレイグラウンドで開始された TiDB クラスターにすばやく接続する {#quickly-connect-to-the-tidb-cluster-started-by-playground}

TiUP は`client`コンポーネントを提供します。これは、playground によって開始されたローカル TiDB クラスターを自動的に見つけて接続するために使用されます。使用方法は次のとおりです。

```shell
tiup client
```

このコマンドは、コンソールの現在のマシンでプレイグラウンドによって開始された TiDB クラスターのリストを提供します。接続する TiDB クラスターを選択します。 <kbd>Enter</kbd>をクリックすると、組み込みの MySQL クライアントが開き、TiDB に接続されます。

## 起動したクラスタの情報をビュー {#view-information-of-the-started-cluster}

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

## クラスターをスケールアウトする {#scale-out-a-cluster}

クラスターをスケールアウトするためのコマンドライン パラメーターは、クラスターを開始するためのパラメーターと似ています。次のコマンドを実行して、2 つの TiDB インスタンスをスケールアウトできます。

```shell
tiup playground scale-out --db 2
```

## クラスターでのスケールイン {#scale-in-a-cluster}

`tiup playground scale-in`コマンドで`pid`指定して、対応するインスタンスにスケーリングできます。 `pid`表示するには、 `tiup playground display`を実行します。

```shell
tiup playground scale-in --pid 86526
```
