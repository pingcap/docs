---
title: Quickly Deploy a Local TiDB Cluster
summary: Learn how to quickly deploy a local TiDB cluster using the playground component of TiUP.
---

# ローカル TiDBクラスタを迅速にデプロイ {#quickly-deploy-a-local-tidb-cluster}

TiDB クラスターは、複数のコンポーネントで構成される分散システムです。一般的な TiDB クラスターは、少なくとも 3 つの PD ノード、3 つの TiKV ノード、および 2 つの TiDB ノードで構成されます。 TiDB を簡単に体験したい場合、非常に多くのコンポーネントを手動でデプロイするのは時間がかかり、複雑だと感じるかもしれません。このドキュメントでは、TiUPのプレイグラウンドコンポーネントと、それを使用してローカル TiDB テスト環境を迅速に構築する方法を紹介します。

## TiUPプレイグラウンドの概要 {#tiup-playground-overview}

Playgroundコンポーネントの基本的な使用法は次のとおりです。

```bash
tiup playground ${version} [flags]
```

`tiup playground`コマンドを直接実行すると、 TiUP はローカルにインストールされた TiDB、TiKV、および PD コンポーネントを使用するか、これらのコンポーネントの安定バージョンをインストールして、1 つの TiKV インスタンス、1 つの TiDB インスタンス、1 つの PD インスタンス、および 1 つの PD インスタンスで構成される TiDB クラスターを開始します。 TiFlashインスタンス。

このコマンドは実際に次の操作を実行します。

-   このコマンドはプレイグラウンドコンポーネントのバージョンを指定しないため、 TiUP はまず、インストールされているプレイグラウンドコンポーネントの最新バージョンをチェックします。最新バージョンが v1.11.3 であると仮定すると、このコマンドは`tiup playground:v1.11.3`と同じように機能します。
-   TiUPプレイグラウンドを使用して TiDB、TiKV、および PD コンポーネントをインストールしていない場合、プレイグラウンドコンポーネントはこれらのコンポーネントの最新の安定したバージョンをインストールし、これらのインスタンスを起動します。
-   このコマンドは TiDB、PD、および TiKVコンポーネントのバージョンを指定しないため、 TiUPプレイグラウンドはデフォルトで各コンポーネントの最新バージョンを使用します。最新バージョンが v7.1.2 であると仮定すると、このコマンドは`tiup playground:v1.11.3 v7.1.2`と同じように機能します。
-   このコマンドでは各コンポーネントの数が指定されていないため、 TiUPプレイグラウンドはデフォルトで、1 つの TiDB インスタンス、1 つの TiKV インスタンス、1 つの PD インスタンス、および 1 つのTiFlashインスタンスで構成される最小のクラスターを開始します。
-   各 TiDBコンポーネントを開始すると、 TiUPプレイグラウンドはクラスターが正常に開始されたことを通知し、MySQL クライアントを介して TiDB クラスターに接続する方法や[TiDB ダッシュボード](/dashboard/dashboard-intro.md)にアクセスする方法などの役立つ情報を提供します。

プレイグラウンドコンポーネントのコマンドライン フラグは次のように説明されます。

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

### 利用可能な TiDB バージョンを確認する {#check-available-tidb-versions}

```shell
tiup list tidb
```

### 特定のバージョンの TiDB クラスターを開始する {#start-a-tidb-cluster-of-a-specific-version}

```shell
tiup playground ${version}
```

`${version}`ターゲットのバージョン番号に置き換えます。

### ナイトリーバージョンの TiDB クラスターを開始します。 {#start-a-tidb-cluster-of-the-nightly-version}

```shell
tiup playground nightly
```

上記のコマンドで、 `nightly` TiDB の最新開発バージョンを示します。

### PD のデフォルト設定を上書きする {#override-pd-s-default-configuration}

まず、 [PD構成テンプレート](https://github.com/pingcap/pd/blob/master/conf/config.toml)をコピーする必要があります。コピーしたファイルを`~/config/pd.toml`に配置し、必要に応じていくつかの変更を加えた場合、次のコマンドを実行して PD のデフォルト構成をオーバーライドできます。

```shell
tiup playground --pd.config ~/config/pd.toml
```

### デフォルトのバイナリファイルを置き換える {#replace-the-default-binary-files}

デフォルトでは、プレイグラウンドが開始されると、公式ミラーからのバイナリ ファイルを使用して各コンポーネントが開始されます。テストのために一時的にコンパイルされたローカル バイナリ ファイルをクラスターに配置する場合は、置換に`--{comp}.binpath`フラグを使用できます。たとえば、次のコマンドを実行して TiDB のバイナリ ファイルを置き換えます。

```shell
tiup playground --db.binpath /xx/tidb-server
```

### 複数のコンポーネントインスタンスを開始する {#start-multiple-component-instances}

デフォルトでは、TiDB、TiKV、PDコンポーネントごとにインスタンスが 1 つだけ起動されます。各コンポーネントに対して複数のインスタンスを開始するには、次のフラグを追加します。

```shell
tiup playground --db 3 --pd 3 --kv 3
```

### TiDB クラスターの起動時にタグを指定します {#specify-a-tag-when-starting-the-tidb-cluster}

TiUPプレイグラウンドを使用して開始された TiDB クラスターを停止すると、すべてのクラスター データもクリーンアップされます。 TiUPプレイグラウンドを使用して TiDB クラスターを開始し、クラスター データが自動的にクリーンアップされないようにするには、クラスターの開始時にタグを指定できます。タグを指定すると、 `~/.tiup/data`ディレクトリにクラスター データが見つかります。次のコマンドを実行してタグを指定します。

```shell
tiup playground --tag <tagname>
```

この方法で開始されたクラスターの場合、データ ファイルはクラスターの停止後も保持されます。このタグを使用して次回クラスターを開始すると、クラスターの停止後に保持されていたデータを使用できるようになります。

## プレイグラウンドによって開始された TiDB クラスターにすばやく接続します {#quickly-connect-to-the-tidb-cluster-started-by-playground}

TiUP は、プレイグラウンドによって開始されたローカル TiDB クラスターを自動的に検索して接続するために使用される`client`コンポーネントを提供します。使用方法は次のとおりです。

```shell
tiup client
```

このコマンドは、現在のマシン上のプレイグラウンドによって開始された TiDB クラスターのリストをコンソールに表示します。接続する TiDB クラスターを選択します。 <kbd>Enter</kbd>をクリックすると、TiDB に接続するための組み込み MySQL クライアントが開きます。

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

クラスターをスケールアウトするためのコマンドライン パラメーターは、クラスターを開始するためのコマンドライン パラメーターと似ています。次のコマンドを実行すると、2 つの TiDB インスタンスをスケールアウトできます。

```shell
tiup playground scale-out --db 2
```

## クラスタースケールイン {#scale-in-a-cluster}

`tiup playground scale-in`コマンドに`pid`指定して、対応するインスタンスをスケールインできます。 `pid`表示するには、 `tiup playground display`を実行します。

```shell
tiup playground scale-in --pid 86526
```
