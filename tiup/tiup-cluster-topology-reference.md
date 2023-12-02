---
title: Topology Configuration File for TiDB Deployment Using TiUP
---

# TiUPを使用した TiDB デプロイメント用のトポロジーコンフィグレーションファイル {#topology-configuration-file-for-tidb-deployment-using-tiup}

TiUPを使用して TiDB をデプロイまたはスケーリングするには、クラスター トポロジを記述するトポロジ ファイル ( [サンプル](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml) ) を提供する必要があります。

同様に、クラスター トポロジを変更するには、トポロジ ファイルを変更する必要があります。違いは、クラスターのデプロイ後は、トポロジー ファイル内のフィールドの一部のみを変更できることです。このドキュメントでは、トポロジ ファイルの各セクションと各セクションの各フィールドを紹介します。

## ファイル構造 {#file-structure}

TiUPを使用した TiDB 導入用のトポロジ構成ファイルには、次のセクションが含まれる場合があります。

-   [グローバル](#global) : クラスターのグローバル構成。一部の構成項目はデフォルト値を使用しており、インスタンスごとに個別に構成できます。
-   [監視されている](#monitored) : 監視サービス、つまり blackbox_exporter と`node_exporter`のコンフィグレーション。各マシンには`node_exporter`と`blackbox_exporter`がデプロイされます。
-   [サーバー構成](#server_configs) : コンポーネントのグローバル構成。各コンポーネントを個別に構成できます。インスタンスに同じ名前の構成アイテムがある場合、インスタンスの構成アイテムが有効になります。
-   [コンポーネントのバージョン](#component_versions) : コンポーネントのバージョン。コンポーネントがクラスター バージョンを使用しない場合に構成できます。このセクションは、 tiup-cluster v1.14.0 で導入されました。
-   [pd_servers](#pd_servers) : PD インスタンスの構成。この構成では、PDコンポーネントがデプロイされるマシンを指定します。
-   [tidb_servers](#tidb_servers) : TiDB インスタンスの構成。この構成では、TiDBコンポーネントがデプロイされるマシンを指定します。
-   [tikv_servers](#tikv_servers) : TiKV インスタンスの構成。この構成では、TiKVコンポーネントがデプロイされるマシンを指定します。
-   [tflash_servers](#tiflash_servers) : TiFlashインスタンスの構成。この構成では、 TiFlashコンポーネントが展開されるマシンを指定します。
-   [ポンプサーバー](#pump_servers) :Pumpインスタンスの構成。この構成では、Pumpコンポーネントがデプロイされるマシンを指定します。
-   [ドレイナーサーバー](#drainer_servers) : Drainerインスタンスの構成。この構成では、 Drainerコンポーネントがデプロイされるマシンを指定します。
-   [cdc_servers](#cdc_servers) : TiCDC インスタンスの構成。この構成では、TiCDCコンポーネントがデプロイされるマシンを指定します。
-   [tispark_masters](#tispark_masters) : TiSpark マスター インスタンスの構成。この構成では、TiSpark マスターコンポーネントがデプロイされるマシンを指定します。 TiSpark マスターのノードは 1 つだけデプロイできます。
-   [tispark_workers](#tispark_workers) : TiSpark ワーカー インスタンスの構成。この構成では、TiSpark ワーカーコンポーネントがデプロイされるマシンを指定します。
-   [監視サーバー](#monitoring_servers) : Prometheus と NGMonitoring がデプロイされるマシンを指定します。 TiUP は複数の Prometheus インスタンスのデプロイをサポートしていますが、最初のインスタンスのみが使用されます。
-   [グラファナサーバー](#grafana_servers) : Grafana インスタンスの構成。この構成では、Grafana がデプロイされるマシンを指定します。
-   [アラートマネージャー_サーバー](#alertmanager_servers) : Alertmanager インスタンスの構成。この構成では、Alertmanager が展開されるマシンを指定します。

### <code>global</code> {#code-global-code}

`global`セクションはクラスターのグローバル構成に対応し、次のフィールドがあります。

-   `user` : デプロイされたクラスターの起動に使用されたユーザー。デフォルト値は`"tidb"`です。 `<user>`フィールドで指定したユーザーがターゲット マシンに存在しない場合、このユーザーは自動的に作成されます。

-   `group` : ユーザーが所属するユーザーグループ。ユーザー作成時に指定します。値のデフォルトは`<user>`フィールドの値です。指定したグループが存在しない場合は、自動的に作成されます。

-   `ssh_port` : 操作のためにターゲット マシンに接続する SSH ポートを指定します。デフォルト値は`22`です。

-   `enable_tls` : クラスターに対して TLS を有効にするかどうかを指定します。 TLS を有効にした後、生成された TLS 証明書をコンポーネント間またはクライアントとコンポーネント間の接続に使用する必要があります。デフォルト値は`false`です。

-   `listen_host` : デフォルトのリスニング IP アドレスを指定します。空の場合、各インスタンスは、その`host`フィールドに`:`含まれているかどうかに基づいて、自動的に`::`または`0.0.0.0`に設定します。このフィールドは、 tiup-cluster v1.14.0 で導入されました。

-   `deploy_dir` : 各コンポーネントのデプロイメント ディレクトリ。デフォルト値は`"deployed"`です。その適用ルールは次のとおりです。

    -   絶対パス`deploy_dir`がインスタンス レベルで構成されている場合、実際のデプロイメント ディレクトリは`deploy_dir`に対して構成されます。

    -   各インスタンスについて、 `deploy_dir`を構成しない場合、そのデフォルト値は相対パス`<component-name>-<component-port>`です。

    -   `global.deploy_dir`が絶対パスの場合、コンポーネントは`<global.deploy_dir>/<instance.deploy_dir>`ディレクトリにデプロイされます。

    -   `global.deploy_dir`が相対パスの場合、コンポーネントは`/home/<global.user>/<global.deploy_dir>/<instance.deploy_dir>`ディレクトリにデプロイされます。

-   `data_dir` : データディレクトリ。デフォルト値: `"data"` 。その適用ルールは次のとおりです。

    -   絶対パス`data_dir`がインスタンス レベルで構成されている場合、実際のデプロイメント ディレクトリは`data_dir`に対して構成されます。

    -   各インスタンスについて、 `data_dir`構成しない場合、デフォルト値は`<global.data_dir>`です。

    -   `data_dir`が相対パスの場合、コンポーネントデータは`<deploy_dir>/<data_dir>`に配置されます。 `<deploy_dir>`の計算規則については、 `deploy_dir`フィールドの適用規則を参照してください。

-   `log_dir` : ログディレクトリ。デフォルト値: `"log"` 。その適用ルールは次のとおりです。

    -   絶対パス`log_dir`がインスタンス レベルで設定されている場合、実際のログ ディレクトリはインスタンスに設定されている`log_dir`なります。

    -   各インスタンスについて、 `log_dir`を構成しない場合、デフォルト値は`<global.log_dir>`です。

    -   `log_dir`が相対パスの場合、コンポーネントログは`<deploy_dir>/<log_dir>`に配置されます。 `<deploy_dir>`の計算規則については、 `deploy_dir`フィールドの適用規則を参照してください。

-   `os` : ターゲット マシンのオペレーティング システム。このフィールドは、ターゲット マシンにプッシュされるコンポーネントにどのオペレーティング システムを適応させるかを制御します。デフォルト値は「linux」です。

-   `arch` : ターゲット マシンの CPUアーキテクチャ。このフィールドは、ターゲット マシンにプッシュされるバイナリ パッケージをどのプラットフォームに適応させるかを制御します。サポートされている値は「amd64」と「arm64」です。デフォルト値は「amd64」です。

-   `resource_control` : ランタイムリソース制御。このフィールドのすべての設定は、systemd のサービス ファイルに書き込まれます。デフォルトでは制限はありません。制御できるリソースは以下のとおりです。

    -   `memory_limit` : 最大実行時メモリを制限します。例えば「2G」は、最大2GBのメモリを使用できることを意味します。

    -   `cpu_quota` : 実行時の最大 CPU 使用率を制限します。たとえば、「200%」です。

    -   `io_read_bandwidth_max` : ディスク読み取りの最大 I/O 帯域幅を制限します。たとえば、 `"/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0 100M"` 。

    -   `io_write_bandwidth_max` : ディスク書き込みの最大 I/O 帯域幅を制限します。たとえば、 `/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0 100M` 。

    -   `limit_core` : コア ダンプのサイズを制御します。

`global`構成例は次のとおりです。

```yaml
global:
  user: "tidb"
  resource_control:
    memory_limit: "2G"
```

上記の構成では、 `tidb`ユーザーを使用してクラスターを起動します。同時に、各コンポーネントの実行時のメモリは最大 2 GB に制限されます。

### <code>monitored</code> {#code-monitored-code}

`monitored`は、ターゲット マシン ( [`node_exporter`](https://github.com/prometheus/node_exporter)および[`blackbox_exporter`](https://github.com/prometheus/blackbox_exporter)で監視サービスを構成するために使用されます。次のフィールドが含まれます。

-   `node_exporter_port` : `node_exporter`のサービスポート。デフォルト値は`9100`です。

-   `blackbox_exporter_port` : `blackbox_exporter`のサービスポート。デフォルト値は`9115`です。

-   `deploy_dir` : デプロイメントディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `data_dir` : データディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`data_dir`ディレクトリに従ってディレクトリが生成されます。

-   `log_dir` : ログディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`log_dir`ディレクトリに従ってログが生成されます。

`monitored`構成例は次のとおりです。

```yaml
monitored:
  node_exporter_port: 9100
  blackbox_exporter_port: 9115
```

上記の設定では、 `node_exporter` `9100`ポートを使用し、 `blackbox_exporter` `9115`ポートを使用することを指定しています。

### <code>server_configs</code> {#code-server-configs-code}

`server_configs`は、サービスを構成し、各コンポーネントの構成ファイルを生成するために使用されます。 `global`セクションと同様に、このセクションの構成は、インスタンス内の同じ名前の構成によって上書きできます。 `server_configs`は主に次のフィールドが含まれます。

-   `tidb` : TiDB サービス関連の構成。完全な構成については、 [TiDB 設定ファイル](/tidb-configuration-file.md)を参照してください。

-   `tikv` : TiKV サービス関連の構成。完全な構成については、 [TiKV設定ファイル](/tikv-configuration-file.md)を参照してください。

-   `pd` : PD サービス関連の設定。完全な構成については、 [PD設定ファイル](/pd-configuration-file.md)を参照してください。

-   `tiflash` : TiFlashサービス関連の設定。完全な構成については、 [TiFlash設定ファイル](/tiflash/tiflash-configuration.md)を参照してください。

-   `tiflash_learner` : 各TiFlashノードには特別な組み込み TiKV があります。この構成アイテムは、この特別な TiKV を構成するために使用されます。通常、この構成項目の内容を変更することはお勧めできません。

-   `pump` :Pumpサービス関連の構成。完全な構成については、 [TiDBBinlog構成ファイル](/tidb-binlog/tidb-binlog-configuration-file.md#pump)を参照してください。

-   `drainer` :Drainerサービス関連の設定。完全な構成については、 [TiDBBinlog構成ファイル](/tidb-binlog/tidb-binlog-configuration-file.md#drainer)を参照してください。

-   `cdc` : TiCDC サービス関連の構成。完全な構成については、 [TiCDCのデプロイ](/ticdc/deploy-ticdc.md)を参照してください。

`server_configs`構成例は次のとおりです。

```yaml
server_configs:
  tidb:
    lease: "45s"
    split-table: true
    token-limit: 1000
    instance.tidb_enable_ddl: true
  tikv:
    log-level: "info"
    readpool.unified.min-thread-count: 1
```

上記の構成は、TiDB と TiKV のグローバル構成を指定します。

### <code>component_versions</code> {#code-component-versions-code}

> **注記：**
>
> TiDB、TiKV、PD、TiCDC など、バージョン番号を共有するコンポーネントについては、バージョンが混在した展開シナリオで適切に動作することを確認するための完全なテストはありません。このセクションは、テスト環境でのみ使用するか、 [テクニカルサポート](/support.md)の助けを借りて使用するようにしてください。

`component_versions`は、特定のコンポーネントのバージョン番号を指定するために使用されます。

-   `component_versions`が構成されていない場合、各コンポーネントはTiDB クラスターと同じバージョン番号 (PD や TiKV など) を使用するか、最新バージョン (Alertmanager など) を使用します。
-   `component_versions`が構成されている場合、対応するコンポーネントは指定されたバージョンを使用し、このバージョンは後続のクラスターのスケーリングおよびアップグレード操作で使用されます。

コンポーネントの特定のバージョンを使用する必要がある場合にのみ設定してください。

`component_versions`には次のフィールドが含まれます。

-   `tikv` : TiKVコンポーネントのバージョン
-   `tiflash` : TiFlashコンポーネントのバージョン
-   `pd` : PDコンポーネントのバージョン
-   `tidb_dashboard` : スタンドアロン TiDB ダッシュボードコンポーネントのバージョン
-   `pump` :Pumpコンポーネントのバージョン
-   `drainer` :Drainerコンポーネントのバージョン
-   `cdc` : CDCコンポーネントのバージョン
-   `kvcdc` : TiKV-CDCコンポーネントのバージョン
-   `tiproxy` : TiProxyコンポーネントのバージョン
-   `prometheus` : Prometheusコンポーネントのバージョン
-   `grafana` : Grafanaコンポーネントのバージョン
-   `alertmanager` : Alertmanagerコンポーネントのバージョン

以下は`component_versions`の設定例です。

```yaml
component_versions:
  kvcdc: "v1.1.1"
```

前述の構成では、TiKV-CDC のバージョン番号が`v1.1.1`に指定されています。

### <code>pd_servers</code> {#code-pd-servers-code}

`pd_servers` PD サービスが展開されるマシンを指定します。また、各マシンのサービス構成も指定します。 `pd_servers`は配列であり、配列の各要素には次のフィールドが含まれます。

-   `host` : PD サービスが展開されるマシンを指定します。フィールド値は IP アドレスであり、必須です。

-   `listen_host` : マシンに複数の IP アドレスがある場合、 `listen_host`サービスのリスニング IP アドレスを指定します。デフォルト値は`0.0.0.0`です。

-   `ssh_port` : 操作のためにターゲット マシンに接続する SSH ポートを指定します。指定しない場合は、 `global`セクションのうち`ssh_port`使用されます。

-   `name` : PD インスタンスの名前を指定します。異なるインスタンスには一意の名前が必要です。そうしないと、インスタンスをデプロイできません。

-   `client_port` : PD がクライアントへの接続に使用するポートを指定します。デフォルト値は`2379`です。

-   `peer_port` : PD間通信用のポートを指定します。デフォルト値は`2380`です。

-   `deploy_dir` : デプロイメントディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `data_dir` : データディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`data_dir`ディレクトリに従ってディレクトリが生成されます。

-   `log_dir` : ログディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`log_dir`ディレクトリに従ってログが生成されます。

-   `numa_node` : NUMA ポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドが指定されている場合、 cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などの NUMA ノードの ID です。

-   `config` : このフィールドの設定ルールは、 `server_configs`の`pd`の設定ルールと同じです。このフィールドが設定されている場合、フィールドの内容は`server_configs`の`pd`内容とマージされます (2 つのフィールドが重複する場合、このフィールドの内容が有効になります)。次に、構成ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `os` : `host`で指定したマシンのOS。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値です。

-   `arch` : `host`で指定したマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値です。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます (2 つのフィールドが重複している場合、このフィールドの内容が有効になります)。次に、systemd 構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の設定ルールは、 `global`の`resource_control`内容と同じです。

上記のフィールドについては、展開後に構成されたフィールドを変更することはできません。

-   `host`
-   `listen_host`
-   `name`
-   `client_port`
-   `peer_port`
-   `deploy_dir`
-   `data_dir`
-   `log_dir`
-   `arch`
-   `os`

`pd_servers`構成例は次のとおりです。

```yaml
pd_servers:
  - host: 10.0.1.11
    config:
      schedule.max-merge-region-size: 20
      schedule.max-merge-region-keys: 200000
  - host: 10.0.1.12
```

上記の設定では、PD が`10.0.1.11`と`10.0.1.12`に展開されることを指定し、PD `10.0.1.11`に対して特定の設定を行っています。

### <code>tidb_servers</code> {#code-tidb-servers-code}

`tidb_servers` 、TiDB サービスがデプロイされるマシンを指定します。また、各マシンのサービス構成も指定します。 `tidb_servers`は配列であり、配列の各要素には次のフィールドが含まれます。

-   `host` : TiDB サービスがデプロイされるマシンを指定します。フィールド値は IP アドレスであり、必須です。

-   `listen_host` : マシンに複数の IP アドレスがある場合、 `listen_host`サービスのリスニング IP アドレスを指定します。デフォルト値は`0.0.0.0`です。

-   `ssh_port` : 操作のためにターゲット マシンに接続する SSH ポートを指定します。指定しない場合は、 `global`セクションのうち`ssh_port`使用されます。

-   `port` : TiDB サービスのリスニング ポート。MySQL クライアントへの接続を提供するために使用されます。デフォルト値は`4000`です。

-   `status_port` : TiDB ステータス サービスのリスニング ポート。HTTP リクエストを介して外部から TiDB サービスのステータスを表示するために使用されます。デフォルト値は`10080`です。

-   `deploy_dir` : デプロイメントディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `log_dir` : ログディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`log_dir`ディレクトリに従ってログが生成されます。

-   `numa_node` : NUMA ポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドが指定されている場合、 cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などの NUMA ノードの ID です。

-   `config` : このフィールドの設定ルールは、 `server_configs`の`tidb`の設定ルールと同じです。このフィールドが設定されている場合、フィールドの内容は`server_configs`の`tidb`内容とマージされます (2 つのフィールドが重複する場合、このフィールドの内容が有効になります)。次に、構成ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `os` : `host`で指定したマシンのOS。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値です。

-   `arch` : `host`で指定したマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値です。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます (2 つのフィールドが重複している場合、このフィールドの内容が有効になります)。次に、systemd 構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の設定ルールは、 `global`の`resource_control`内容と同じです。

上記のフィールドについては、展開後に構成されたフィールドを変更することはできません。

-   `host`
-   `listen_host`
-   `port`
-   `status_port`
-   `deploy_dir`
-   `log_dir`
-   `arch`
-   `os`

`tidb_servers`構成例は次のとおりです。

```yaml
tidb_servers:
  - host: 10.0.1.14
    config:
      log.level: warn
      log.slow-query-file: tidb-slow-overwrited.log
  - host: 10.0.1.15
```

### <code>tikv_servers</code> {#code-tikv-servers-code}

`tikv_servers` 、TiKV サービスがデプロイされるマシンを指定します。また、各マシンのサービス構成も指定します。 `tikv_servers`は配列であり、配列の各要素には次のフィールドが含まれます。

-   `host` : TiKV サービスが展開されるマシンを指定します。フィールド値は IP アドレスであり、必須です。

-   `listen_host` : マシンに複数の IP アドレスがある場合、 `listen_host`サービスのリスニング IP アドレスを指定します。デフォルト値は`0.0.0.0`です。

-   `ssh_port` : 操作のためにターゲット マシンに接続する SSH ポートを指定します。指定しない場合は、 `global`セクションのうち`ssh_port`が使用されます。

-   `port` : TiKV サービスのリスニング ポート。デフォルト値は`20160`です。

-   `status_port` : TiKV ステータス サービスのリスニング ポート。デフォルト値は`20180`です。

-   `deploy_dir` : デプロイメントディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `data_dir` : データディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`data_dir`ディレクトリに従ってディレクトリが生成されます。

-   `log_dir` : ログディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`log_dir`ディレクトリに従ってログが生成されます。

-   `numa_node` : NUMA ポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドが指定されている場合、 cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などの NUMA ノードの ID です。

-   `config` : このフィールドの設定ルールは、 `server_configs`の`tikv`の設定ルールと同じです。このフィールドが設定されている場合、フィールドの内容は`server_configs`の`tikv`内容とマージされます (2 つのフィールドが重複する場合、このフィールドの内容が有効になります)。次に、構成ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `os` : `host`で指定したマシンのOS。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値です。

-   `arch` : `host`で指定したマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値です。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます (2 つのフィールドが重複している場合、このフィールドの内容が有効になります)。次に、systemd 構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の設定ルールは、 `global`の`resource_control`内容と同じです。

上記のフィールドについては、展開後に構成されたフィールドを変更することはできません。

-   `host`
-   `listen_host`
-   `port`
-   `status_port`
-   `deploy_dir`
-   `data_dir`
-   `log_dir`
-   `arch`
-   `os`

`tikv_servers`構成例は次のとおりです。

```yaml
tikv_servers:
  - host: 10.0.1.14
    config:
      server.labels: { zone: "zone1", host: "host1" }
  - host: 10.0.1.15
    config:
      server.labels: { zone: "zone1", host: "host2" }
```

### <code>tiflash_servers</code> {#code-tiflash-servers-code}

`tiflash_servers` TiFlashサービスが展開されるマシンを指定します。また、各マシンのサービス構成も指定します。このセクションは配列であり、配列の各要素には次のフィールドが含まれます。

-   `host` : TiFlashサービスが展開されるマシンを指定します。フィールド値は IP アドレスであり、必須です。

-   `ssh_port` : 操作のためにターゲット マシンに接続する SSH ポートを指定します。指定しない場合は、 `global`セクションのうち`ssh_port`使用されます。

-   `tcp_port` : TiFlash TCP サービスのポート。デフォルト値は`9000`です。

-   `flash_service_port` : TiFlashがサービスを提供するポート。 TiDB は、このポートを介してTiFlashからデータを読み取ります。デフォルト値は`3930`です。

-   `metrics_port` : TiFlash のステータス ポート。メトリック データの出力に使用されます。デフォルト値は`8234`です。

-   `flash_proxy_port` : 内蔵 TiKV のポート。デフォルト値は`20170`です。

-   `flash_proxy_status_port` : 内蔵 TiKV のステータス ポート。デフォルト値は`20292`です。

-   `deploy_dir` : デプロイメントディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `data_dir` : データディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`data_dir`ディレクトリに従ってディレクトリが生成されます。 TiFlash は、カンマで区切られた複数の`data_dir`のディレクトリをサポートします。

-   `log_dir` : ログディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`log_dir`ディレクトリに従ってログが生成されます。

-   `tmp_path` : TiFlash一時ファイルのstorageパス。デフォルト値は [ `path`または`storage.latest.dir`の最初のディレクトリ] + &quot;/tmp&quot; です。

-   `numa_node` : NUMA ポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドが指定されている場合、 cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などの NUMA ノードの ID です。

-   `config` : このフィールドの設定ルールは、 `server_configs`の`tiflash`の設定ルールと同じです。このフィールドが設定されている場合、フィールドの内容は`server_configs`の`tiflash`内容とマージされます (2 つのフィールドが重複する場合、このフィールドの内容が有効になります)。次に、構成ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `learner_config` : 各TiFlashノードには特別な組み込み TiKV があります。この構成アイテムは、この特別な TiKV を構成するために使用されます。通常、この構成項目の内容を変更することはお勧めできません。

-   `os` : `host`で指定したマシンのOS。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値です。

-   `arch` : `host`で指定したマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値です。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます (2 つのフィールドが重複している場合、このフィールドの内容が有効になります)。次に、systemd 構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の設定ルールは、 `global`の`resource_control`内容と同じです。

デプロイメント後、上記のフィールドについては、 `data_dir`にのみディレクトリを追加できます。以下のフィールドについては、これらのフィールドを変更することはできません。

-   `host`
-   `tcp_port`
-   `http_port`
-   `flash_service_port`
-   `flash_proxy_port`
-   `flash_proxy_status_port`
-   `metrics_port`
-   `deploy_dir`
-   `log_dir`
-   `tmp_path`
-   `arch`
-   `os`

`tiflash_servers`構成例は次のとおりです。

```yaml
tiflash_servers:
  - host: 10.0.1.21
  - host: 10.0.1.22
```

### <code>pump_servers</code> {#code-pump-servers-code}

`pump_servers` 、TiDB BinlogのPumpサービスがデプロイされるマシンを指定します。また、各マシンのサービス構成も指定します。 `pump_servers`は配列であり、配列の各要素には次のフィールドが含まれます。

-   `host` :Pumpサービスがデプロイされるマシンを指定します。フィールド値は IP アドレスであり、必須です。

-   `ssh_port` : 操作のためにターゲット マシンに接続する SSH ポートを指定します。指定しない場合は、 `global`セクションのうち`ssh_port`が使用されます。

-   `port` :Pumpサービスのリスニング ポート。デフォルト値は`8250`です。

-   `deploy_dir` : デプロイメントディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `data_dir` : データディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`data_dir`ディレクトリに従ってディレクトリが生成されます。

-   `log_dir` : ログディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`log_dir`ディレクトリに従ってログが生成されます。

-   `numa_node` : NUMA ポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドが指定されている場合、 cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などの NUMA ノードの ID です。

-   `config` : このフィールドの設定ルールは、 `server_configs`の`pump`の設定ルールと同じです。このフィールドが設定されている場合、フィールドの内容は`server_configs`の`pump`内容とマージされます (2 つのフィールドが重複する場合、このフィールドの内容が有効になります)。次に、構成ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `os` : `host`で指定したマシンのOS。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値です。

-   `arch` : `host`で指定したマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値です。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます (2 つのフィールドが重複している場合、このフィールドの内容が有効になります)。次に、systemd 構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の設定ルールは、 `global`の`resource_control`内容と同じです。

上記のフィールドについては、展開後に構成されたフィールドを変更することはできません。

-   `host`
-   `port`
-   `deploy_dir`
-   `data_dir`
-   `log_dir`
-   `arch`
-   `os`

`pump_servers`構成例は次のとおりです。

```yaml
pump_servers:
  - host: 10.0.1.21
    config:
      gc: 7
  - host: 10.0.1.22
```

### <code>drainer_servers</code> {#code-drainer-servers-code}

`drainer_servers` 、TiDB BinlogのDrainerサービスがデプロイされるマシンを指定します。また、各マシンのサービス構成も指定します。 `drainer_servers`は配列です。各配列要素には次のフィールドが含まれます。

-   `host` : Drainerサービスがデプロイされるマシンを指定します。フィールド値は IP アドレスであり、必須です。

-   `ssh_port` : 操作のためにターゲット マシンに接続する SSH ポートを指定します。指定しない場合は、 `global`セクションのうち`ssh_port`が使用されます。

-   `port` : Drainerサービスのリスニング ポート。デフォルト値は`8249`です。

-   `deploy_dir` : デプロイメントディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `data_dir` : データディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`data_dir`ディレクトリに従ってディレクトリが生成されます。

-   `log_dir` : ログディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`log_dir`ディレクトリに従ってログが生成されます。

-   `commit_ts` (非推奨): Drainer が起動すると、チェックポイントが読み取られます。 Drainer がチェックポイントを取得しない場合、Drainer はこのフィールドを最初の起動時のレプリケーション時点として使用します。このフィールドのデフォルトは`-1`です (Drainer は常に PD から最新のタイムスタンプを commit_ts として取得します)。

-   `numa_node` : NUMA ポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドが指定されている場合、 cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などの NUMA ノードの ID です。

-   `config` : このフィールドの設定ルールは、 `server_configs`の`drainer`の設定ルールと同じです。このフィールドが設定されている場合、フィールドの内容は`server_configs`の`drainer`内容とマージされます (2 つのフィールドが重複する場合、このフィールドの内容が有効になります)。次に、構成ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `os` : `host`で指定したマシンのOS。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値です。

-   `arch` : `host`で指定したマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値です。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます (2 つのフィールドが重複している場合、このフィールドの内容が有効になります)。次に、systemd 構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の設定ルールは、 `global`の`resource_control`内容と同じです。

上記のフィールドについては、展開後に構成されたフィールドを変更することはできません。

-   `host`
-   `port`
-   `deploy_dir`
-   `data_dir`
-   `log_dir`
-   `arch`
-   `os`

`commit_ts`フィールドはTiUP v1.9.2 以降非推奨となり、 Drainerの起動スクリプトには記録されません。このフィールドを引き続き使用する必要がある場合は、次の例を参照して、 `config`の`initial-commit-ts`フィールドを構成します。

`drainer_servers`構成例は次のとおりです。

```yaml
drainer_servers:
  - host: 10.0.1.21
    config:
      initial-commit-ts: -1
      syncer.db-type: "mysql"
      syncer.to.host: "127.0.0.1"
      syncer.to.user: "root"
      syncer.to.password: ""
      syncer.to.port: 3306
      syncer.ignore-table:
        - db-name: test
          tbl-name: log
        - db-name: test
          tbl-name: audit
```

### <code>cdc_servers</code> {#code-cdc-servers-code}

`cdc_servers` 、TiCDC サービスがデプロイされるマシンを指定します。また、各マシンのサービス構成も指定します。 `cdc_servers`は配列です。各配列要素には次のフィールドが含まれます。

-   `host` : TiCDC サービスがデプロイされるマシンを指定します。フィールド値は IP アドレスであり、必須です。

-   `ssh_port` : 操作のためにターゲット マシンに接続する SSH ポートを指定します。指定しない場合は、 `global`セクションのうち`ssh_port`が使用されます。

-   `port` : TiCDC サービスのリスニング ポート。デフォルト値は`8300`です。

-   `deploy_dir` : デプロイメントディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `data_dir` : データディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`data_dir`ディレクトリに従ってディレクトリが生成されます。

-   `log_dir` : ログディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`log_dir`ディレクトリに従ってログが生成されます。

-   `gc-ttl` : PD の TiCDC によって設定されたサービス レベル GC セーフポイントの存続時間 (TTL) の期間 (秒単位)。デフォルト値は`86400` 、つまり 24 時間です。

-   `tz` : TiCDC サービスが使用するタイムゾーン。 TiCDC は、タイムスタンプなどの時間データ型を内部で変換するとき、およびデータをダウンストリームにレプリケートするときに、このタイム ゾーンを使用します。デフォルト値は、プロセスが実行されるローカル タイム ゾーンです。

-   `numa_node` : NUMA ポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドが指定されている場合、 cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などの NUMA ノードの ID です。

-   `config` : フィールドの内容は`server_configs`の`cdc`内容とマージされます (2 つのフィールドが重複する場合、このフィールドの内容が有効になります)。次に、構成ファイルが生成され、 `host`で指定したマシンに送信されます。

-   `os` : `host`で指定したマシンのOS。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値です。

-   `arch` : `host`で指定したマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値です。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます (2 つのフィールドが重複している場合、このフィールドの内容が有効になります)。次に、systemd 構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の設定ルールは、 `global`の`resource_control`内容と同じです。

-   `ticdc_cluster_id` : サービスに対応する TiCDC クラスター ID を指定します。このフィールドが指定されていない場合、サービスはデフォルトの TiCDC クラスターに参加します。このフィールドは、TiDB v6.3.0 以降のバージョンでのみ有効です。

上記のフィールドについては、展開後に構成されたフィールドを変更することはできません。

-   `host`
-   `port`
-   `deploy_dir`
-   `data_dir`
-   `log_dir`
-   `arch`
-   `os`
-   `ticdc_cluster_id`

`cdc_servers`構成例は次のとおりです。

```yaml
cdc_servers:
  - host: 10.0.1.20
    gc-ttl: 86400
    data_dir: "/cdc-data"
  - host: 10.0.1.21
    gc-ttl: 86400
    data_dir: "/cdc-data"
```

### <code>tispark_masters</code> {#code-tispark-masters-code}

`tispark_masters` 、TiSpark のマスター ノードがデプロイされるマシンを指定します。また、各マシンのサービス構成も指定します。 `tispark_masters`は配列です。各配列要素には次のフィールドが含まれます。

-   `host` : TiSpark マスターがデプロイされるマシンを指定します。フィールド値は IP アドレスであり、必須です。

-   `listen_host` : マシンに複数の IP アドレスがある場合、 `listen_host`サービスのリスニング IP アドレスを指定します。デフォルト値は`0.0.0.0`です。

-   `ssh_port` : 操作のためにターゲット マシンに接続する SSH ポートを指定します。指定しない場合は、 `global`セクションのうち`ssh_port`使用されます。

-   `port` : Spark のリスニング ポート。ノードの前の通信に使用されます。デフォルト値は`7077`です。

-   `web_port` : Spark の Web ポート。Web サービスとタスクのステータスを提供します。デフォルト値は`8080`です。

-   `deploy_dir` : デプロイメントディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `java_home` : 使用するJRE環境のパスを指定します。このパラメータは`JAVA_HOME`システム環境変数に対応します。

-   `spark_config` : TiSpark サービスを構成するように構成します。次に、構成ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `spark_env` : Spark の起動時に環境変数を構成します。

-   `os` : `host`で指定したマシンのOS。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値です。

-   `arch` : `host`で指定したマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値です。

上記のフィールドについては、展開後に構成されたフィールドを変更することはできません。

-   `host`
-   `listen_host`
-   `port`
-   `web_port`
-   `deploy_dir`
-   `arch`
-   `os`

`tispark_masters`構成例は次のとおりです。

```yaml
tispark_masters:
  - host: 10.0.1.21
    spark_config:
      spark.driver.memory: "2g"
      spark.eventLog.enabled: "False"
      spark.tispark.grpc.framesize: 2147483647
      spark.tispark.grpc.timeout_in_sec: 100
      spark.tispark.meta.reload_period_in_sec: 60
      spark.tispark.request.command.priority: "Low"
      spark.tispark.table.scan_concurrency: 256
    spark_env:
      SPARK_EXECUTOR_CORES: 5
      SPARK_EXECUTOR_MEMORY: "10g"
      SPARK_WORKER_CORES: 5
      SPARK_WORKER_MEMORY: "10g"
  - host: 10.0.1.22
```

### <code>tispark_workers</code> {#code-tispark-workers-code}

`tispark_workers` 、TiSpark のワーカー ノードがデプロイされるマシンを指定します。また、各マシンのサービス構成も指定します。 `tispark_workers`は配列です。各配列要素には次のフィールドが含まれます。

-   `host` : TiSpark ワーカーがデプロイされるマシンを指定します。フィールド値は IP アドレスであり、必須です。

-   `listen_host` : マシンに複数の IP アドレスがある場合、 `listen_host`サービスのリスニング IP アドレスを指定します。デフォルト値は`0.0.0.0`です。

-   `ssh_port` : 操作のためにターゲット マシンに接続する SSH ポートを指定します。指定しない場合は、 `global`セクションのうち`ssh_port`使用されます。

-   `port` : Spark のリスニング ポート。ノードの前の通信に使用されます。デフォルト値は`7077`です。

-   `web_port` : Spark の Web ポート。Web サービスとタスクのステータスを提供します。デフォルト値は`8080`です。

-   `deploy_dir` : デプロイメントディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `java_home` : 使用するJRE環境が配置されているパスを指定します。このパラメータは`JAVA_HOME`システム環境変数に対応します。

-   `os` : `host`で指定したマシンのOS。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値です。

-   `arch` : `host`で指定したマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値です。

上記のフィールドについては、展開後に構成されたフィールドを変更することはできません。

-   `host`
-   `listen_host`
-   `port`
-   `web_port`
-   `deploy_dir`
-   `arch`
-   `os`

`tispark_workers`構成例は次のとおりです。

```yaml
tispark_workers:
  - host: 10.0.1.22
  - host: 10.0.1.23
```

### <code>monitoring_servers</code> {#code-monitoring-servers-code}

`monitoring_servers` Prometheus サービスがデプロイされるマシンを指定します。また、各マシンのサービス構成も指定します。 `monitoring_servers`は配列です。各配列要素には次のフィールドが含まれます。

-   `host` : 監視サービスが展開されるマシンを指定します。フィールド値は IP アドレスであり、必須です。

-   `ng_port` : NgMonitoring がリッスンするポートを指定します。 TiUP v1.7.0 で導入されたこのフィールドは[継続的なプロファイリング](/dashboard/dashboard-profiling.md)と[Top SQL](/dashboard/top-sql.md)をサポートします。デフォルト値は`12020`です。

-   `ssh_port` : 操作のためにターゲット マシンに接続する SSH ポートを指定します。指定しない場合は、 `global`セクションのうち`ssh_port`が使用されます。

-   `port` : Prometheus サービスのリスニング ポート。デフォルト値は`9090`です。

-   `deploy_dir` : デプロイメントディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `data_dir` : データディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`data_dir`ディレクトリに従ってディレクトリが生成されます。

-   `log_dir` : ログディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`log_dir`ディレクトリに従ってログが生成されます。

-   `numa_node` : NUMA ポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドが指定されている場合、 cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などの NUMA ノードの ID です。

-   `storage_retention` : Prometheus 監視データの保持期間。デフォルト値は`"30d"`です。

-   `rule_dir` : 完全な`*.rules.yml`のファイルを含むローカル ディレクトリを指定します。これらのファイルは、Prometheus のルールとして、クラスター構成の初期化フェーズ中にターゲット マシンに転送されます。

-   `remote_config` : Prometheus データのリモートへの書き込み、またはリモートからのデータの読み取りをサポートします。このフィールドには 2 つの構成があります。
    -   `remote_write` : Prometheus のドキュメント[`&#x3C;remote_write>`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write)を参照してください。
    -   `remote_read` : Prometheus のドキュメント[`&#x3C;remote_read>`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_read)を参照してください。

-   `external_alertmanagers` : `external_alertmanagers`フィールドが設定されている場合、Prometheus はクラスターの外部にある Alertmanager に設定動作を警告します。このフィールドは配列であり、その各要素は外部 Alertmanager であり、 `host`フィールドと`web_port`フィールドで構成されます。

-   `os` : `host`で指定したマシンのOS。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値です。

-   `arch` : `host`で指定したマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値です。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます (2 つのフィールドが重複している場合、このフィールドの内容が有効になります)。次に、systemd 構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の設定ルールは、 `global`の`resource_control`内容と同じです。

上記のフィールドについては、展開後に構成されたフィールドを変更することはできません。

-   `host`
-   `port`
-   `deploy_dir`
-   `data_dir`
-   `log_dir`
-   `arch`
-   `os`

`monitoring_servers`構成例は次のとおりです。

```yaml
monitoring_servers:
  - host: 10.0.1.11
    rule_dir: /local/rule/dir
    remote_config:
      remote_write:
      - queue_config:
          batch_send_deadline: 5m
          capacity: 100000
          max_samples_per_send: 10000
          max_shards: 300
        url: http://127.0.0.1:8003/write
      remote_read:
      - url: http://127.0.0.1:8003/read
      external_alertmanagers:
      - host: 10.1.1.1
        web_port: 9093
      - host: 10.1.1.2
        web_port: 9094
```

### <code>grafana_servers</code> {#code-grafana-servers-code}

`grafana_servers` 、Grafana サービスがデプロイされるマシンを指定します。また、各マシンのサービス構成も指定します。 `grafana_servers`は配列です。各配列要素には次のフィールドが含まれます。

-   `host` : Grafana サービスがデプロイされるマシンを指定します。フィールド値は IP アドレスであり、必須です。

-   `ssh_port` : 操作のためにターゲット マシンに接続する SSH ポートを指定します。指定しない場合は、 `global`セクションのうち`ssh_port`が使用されます。

-   `port` : Grafana サービスのリスニング ポート。デフォルト値は`3000`です。

-   `deploy_dir` : デプロイメントディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `os` : `host`で指定したマシンのOS。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値です。

-   `arch` : `host`で指定したマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値です。

-   `username` : Grafana ログイン インターフェイスのユーザー名。

-   `password` : Grafana に対応するパスワード。

-   `dashboard_dir` : 完全な`dashboard(*.json)`のファイルを含むローカル ディレクトリを指定します。これらのファイルは、クラスター構成の初期化フェーズ中に、Grafana のダッシュボードとしてターゲット マシンに転送されます。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます (2 つのフィールドが重複している場合、このフィールドの内容が有効になります)。次に、systemd 構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の設定ルールは、 `global`の`resource_control`内容と同じです。

> **注記：**
>
> `grafana_servers`の`dashboard_dir`フィールドが構成されている場合は、 `tiup cluster rename`コマンドを実行してクラスターの名前を変更した後、次の操作を実行する必要があります。
>
> 1.  ローカル ダッシュボード ディレクトリ内の`*.json`ファイルについて、 `datasource`フィールドの値を新しいクラスター名に更新します ( `datasource`はクラスター名にちなんで命名されているため)。
> 2.  `tiup cluster reload -R grafana`コマンドを実行します。

上記のフィールドについては、展開後に構成されたフィールドを変更することはできません。

-   `host`
-   `port`
-   `deploy_dir`
-   `arch`
-   `os`

`grafana_servers`構成例は次のとおりです。

```yaml
grafana_servers:
  - host: 10.0.1.11
    dashboard_dir: /local/dashboard/dir
```

### <code>alertmanager_servers</code> {#code-alertmanager-servers-code}

`alertmanager_servers` Alertmanager サービスが展開されるマシンを指定します。また、各マシンのサービス構成も指定します。 `alertmanager_servers`は配列です。各配列要素には次のフィールドが含まれます。

-   `host` : Alertmanager サービスが展開されるマシンを指定します。フィールド値は IP アドレスであり、必須です。

-   `ssh_port` : 操作のためにターゲット マシンに接続する SSH ポートを指定します。指定しない場合は、 `global`セクションのうち`ssh_port`使用されます。

-   `web_port` : Alertmanager が Web サービスを提供するために使用するポートを指定します。デフォルト値は`9093`です。

-   `cluster_port` : 1 つのアラートマネージャーと他のアラートマネージャー間の通信ポートを指定します。デフォルト値は`9094`です。

-   `deploy_dir` : デプロイメントディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `data_dir` : データディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`data_dir`ディレクトリに従ってディレクトリが生成されます。

-   `log_dir` : ログディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`log_dir`ディレクトリに従ってログが生成されます。

-   `numa_node` : NUMA ポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドが指定されている場合、 cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などの NUMA ノードの ID です。

-   `config_file` : クラスタ構成の初期化フェーズ中にターゲット マシンに転送されるローカル ファイルを Alertmanager の構成として指定します。

-   `os` : `host`で指定したマシンのOS。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値です。

-   `arch` : `host`で指定したマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値です。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます (2 つのフィールドが重複している場合、このフィールドの内容が有効になります)。次に、systemd 構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の設定ルールは、 `global`の`resource_control`内容と同じです。

上記のフィールドについては、展開後に構成されたフィールドを変更することはできません。

-   `host`
-   `web_port`
-   `cluster_port`
-   `deploy_dir`
-   `data_dir`
-   `log_dir`
-   `arch`
-   `os`

`alertmanager_servers`構成例は次のとおりです。

```yaml
alertmanager_servers:
  - host: 10.0.1.11
    config_file: /local/config/file
  - host: 10.0.1.12
    config_file: /local/config/file
```
