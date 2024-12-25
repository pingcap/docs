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

次のコマンドを使用して、プレイグラウンドコンポーネントのコマンドライン フラグを表示できます。

```shell
tiup playground --help
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

### TiDBクラスタを起動するときにデータを保存するタグを指定します {#specify-a-tag-when-starting-the-tidb-cluster-to-store-the-data}

TiUPプレイグラウンドを使用して起動した TiDB クラスターを停止すると、すべてのクラスター データもクリーンアップされます。TiUP プレイグラウンドを使用してTiUPクラスターを起動し、クラスター データが自動的にクリーンアップされないようにするには、クラスターの起動時にタグを指定します。タグを指定すると、クラスター データは`~/.tiup/data`ディレクトリにあります。タグを指定するには、次のコマンドを実行します。

```shell
tiup playground --tag ${tag_name}
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

## TiProxy をデプロイ {#deploy-tiproxy}

[Tiプロキシ](/tiproxy/tiproxy-overview.md)は PingCAP の公式プロキシコンポーネントであり、クライアントと TiDBサーバーの間に配置され、負荷分散、接続の永続性、サービス検出、および TiDB のその他の機能を提供します。

TiUP v1.15.0 以降では、 TiUP Playground を使用してクラスターに TiProxy をデプロイできます。

1.  `tidb.toml`ファイルを作成し、次の構成を追加します。

        graceful-wait-before-shutdown=15

    この構成項目は、TiDB がサーバーをシャットダウンする前に待機する期間 (秒単位) を制御し、クラスターのスケールイン操作中にクライアントが切断されるのを回避します。

2.  TiDB クラスターを起動します。

    ```shell
    tiup playground v8.1.1 --tiproxy 1 --db.config tidb.toml
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
