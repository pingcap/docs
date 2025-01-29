---
title: Topology Configuration File for TiDB Deployment Using TiUP
summary: TiUP は、トポロジ ファイルを使用して、TiDB のクラスター トポロジを展開または変更します。また、Prometheus、Grafana、Alertmanager などの監視サーバーも展開します。トポロジ ファイルには、グローバル構成、監視サービス、コンポーネントバージョンなどのセクションが含まれています。各セクションでは、対応するサービスが展開されるマシンとその構成を指定します。
---

# TiUPを使用した TiDB デプロイメントのトポロジコンフィグレーションファイル {#topology-configuration-file-for-tidb-deployment-using-tiup}

TiUPを使用してTiDBをデプロイまたは拡張するには、クラスタートポロジを記述するトポロジファイル（ [サンプル](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml) ）を提供する必要があります。

同様に、クラスター トポロジを変更するには、トポロジ ファイルを変更する必要があります。違いは、クラスターがデプロイされた後は、トポロジ ファイル内のフィールドの一部しか変更できないことです。このドキュメントでは、トポロジ ファイルの各セクションと、各セクション内の各フィールドについて説明します。

TiUP を使用して TiDB クラスターをデプロイすると、 TiUP はPrometheus、Grafana、Alertmanager などの監視サーバーもデプロイします。その間に、このクラスターをスケールアウトすると、 TiUP は新しいノードを監視範囲に追加します。前述の監視サーバーの構成をカスタマイズするには、 [監視サーバーの構成をカスタマイズする](/tiup/customized-montior-in-tiup-environment.md)の手順に従ってください。

## ファイル構造 {#file-structure}

TiUPを使用した TiDB デプロイメントのトポロジ構成ファイルには、次のセクションが含まれる場合があります。

-   [グローバル](#global) : クラスターのグローバル構成。一部の構成項目ではデフォルト値が使用され、各インスタンスで個別に構成できます。
-   [監視された](#monitored) : 監視サービス、つまり blackbox_exporter と`node_exporter`コンフィグレーション。各マシンには、 `node_exporter`と`blackbox_exporter`デプロイされています。
-   [サーバー構成](#server_configs) : コンポーネントのグローバル構成。各コンポーネントを個別に構成できます。インスタンスに同じ名前の構成項目がある場合は、インスタンスの構成項目が有効になります。
-   [コンポーネントバージョン](#component_versions) : コンポーネントのバージョン。コンポーネントがクラスター バージョンを使用しない場合に設定できます。このセクションは、 tiup-cluster v1.14.0 で導入されました。
-   [pd_servers](#pd_servers) : PD インスタンスの構成。この構成は、PDコンポーネントがデプロイされるマシンを指定します。
-   [tidb_servers](#tidb_servers) : TiDB インスタンスの構成。この構成は、TiDBコンポーネントがデプロイされるマシンを指定します。
-   [tikv_サーバー](#tikv_servers) : TiKV インスタンスの構成。この構成は、TiKVコンポーネントがデプロイされるマシンを指定します。
-   [tiflash_servers](#tiflash_servers) : TiFlashインスタンスの構成。この構成は、 TiFlashコンポーネントがデプロイされるマシンを指定します。
-   [プロキシサーバー](#tiproxy_servers) : TiProxy インスタンスの構成。この構成は、TiProxyコンポーネントが展開されるマシンを指定します。
-   [ポンプサーバー](#pump_servers) : Pumpインスタンスの構成。この構成は、 Pumpコンポーネントがデプロイされるマシンを指定します。
-   [ドレイナーサーバー](#drainer_servers) : Drainerインスタンスの構成。この構成は、 Drainerコンポーネントがデプロイされるマシンを指定します。
-   [kvcdc_servers](#kvcdc_servers) : [ティKV-CDC](https://tikv.org/docs/7.1/concepts/explore-tikv-features/cdc/cdc/)番目のインスタンスの構成。この構成は、TiKV-CDCコンポーネントがデプロイされるマシンを指定します。
-   [cdc_servers](#cdc_servers) : TiCDC インスタンスの構成。この構成は、TiCDCコンポーネントがデプロイされるマシンを指定します。
-   [tispark_masters](#tispark_masters) : TiSpark マスター インスタンスの構成。この構成は、TiSpark マスターコンポーネントがデプロイされるマシンを指定します。デプロイできる TiSpark マスターのノードは 1 つだけです。
-   [tispark_workers](#tispark_workers) : TiSpark ワーカー インスタンスの構成。この構成は、TiSpark ワーカーコンポーネントがデプロイされるマシンを指定します。
-   [監視サーバー](#monitoring_servers) : Prometheus と NGMonitoring がデプロイされるマシンを指定します。TiUPは複数の Prometheus インスタンスのデプロイをサポートしていますが、最初のインスタンスのみが使用されます。
-   [グラファナサーバー](#grafana_servers) : Grafana インスタンスの構成。この構成は、Grafana がデプロイされるマシンを指定します。
-   [アラートマネージャサーバー](#alertmanager_servers) : Alertmanager インスタンスの構成。この構成は、Alertmanager がデプロイされるマシンを指定します。

### <code>global</code> {#code-global-code}

`global`セクションはクラスターのグローバル構成に対応し、次のフィールドがあります。

-   `user` : デプロイされたクラスターを起動するために使用されるユーザー。デフォルト値は`"tidb"`です。4 `<user>`に指定されたユーザーがターゲット マシンに存在しない場合は、このユーザーは自動的に作成されます。

-   `group` : ユーザーが属するユーザー グループ。ユーザーの作成時に指定されます。デフォルト値は`<user>`フィールドの値になります。指定されたグループが存在しない場合は、自動的に作成されます。

-   `ssh_port` : 操作のためにターゲットマシンに接続するための SSH ポートを指定します。デフォルト値は`22`です。

-   `enable_tls` : クラスターに対して TLS を有効にするかどうかを指定します。TLS を有効にすると、生成された TLS 証明書は、コンポーネント間またはクライアントとコンポーネント間の接続に使用する必要があります。デフォルト値は`false`です。

-   `listen_host` : デフォルトのリスニング IP アドレスを指定します。空の場合、各インスタンスは、 `host`フィールドに`:`含まれているかどうかに基づいて、自動的に`::`または`0.0.0.0`に設定します。このフィールドは、tiup-cluster v1.14.0 で導入されました。

-   `deploy_dir` : 各コンポーネントのデプロイメントディレクトリ。デフォルト値は`"deployed"`です。その適用ルールは次のとおりです。

    -   インスタンス レベルで絶対パス`deploy_dir`が設定されている場合、実際のデプロイメント ディレクトリはインスタンスに対して`deploy_dir`に設定されます。

    -   各インスタンスに対して`deploy_dir`設定しない場合、デフォルト値は相対パス`<component-name>-<component-port>`になります。

    -   `global.deploy_dir`絶対パスの場合、コンポーネントは`<global.deploy_dir>/<instance.deploy_dir>`ディレクトリにデプロイされます。

    -   `global.deploy_dir`が相対パスの場合、コンポーネントは`/home/<global.user>/<global.deploy_dir>/<instance.deploy_dir>`ディレクトリにデプロイされます。

-   `data_dir` : データディレクトリ。デフォルト値: `"data"`適用ルールは次のとおりです。

    -   インスタンス レベルで絶対パス`data_dir`が設定されている場合、実際のデプロイメント ディレクトリはインスタンスに対して`data_dir`に設定されます。

    -   各インスタンスに対して`data_dir`設定しない場合、デフォルト値は`<global.data_dir>`になります。

    -   `data_dir`相対パスの場合、コンポーネントデータは`<deploy_dir>/<data_dir>`に配置されます。 `<deploy_dir>`の計算規則については、 `deploy_dir`フィールドの適用規則を参照してください。

-   `log_dir` : ログディレクトリ。デフォルト値: `"log"`適用ルールは次のとおりです。

    -   絶対パス`log_dir`がインスタンス レベルで構成されている場合、実際のログ ディレクトリはインスタンスに構成されている`log_dir`になります。

    -   各インスタンスに対して`log_dir`設定しない場合、デフォルト値は`<global.log_dir>`なります。

    -   `log_dir`相対パスの場合、コンポーネントログは`<deploy_dir>/<log_dir>`に配置されます。 `<deploy_dir>`の計算規則については、 `deploy_dir`フィールドの適用規則を参照してください。

-   `os` : ターゲット マシンのオペレーティング システム。このフィールドは、ターゲット マシンにプッシュされるコンポーネントをどのオペレーティング システムに適合させるかを制御します。デフォルト値は「linux」です。

-   `arch` : ターゲット マシンの CPUアーキテクチャ。このフィールドは、ターゲット マシンにプッシュされるバイナリ パッケージをどのプラットフォームに適合させるかを制御します。サポートされている値は「amd64」と「arm64」です。デフォルト値は「amd64」です。

-   `resource_control` : ランタイム リソース制御。このフィールドのすべての設定は、systemd のサービス ファイルに書き込まれます。デフォルトでは制限はありません。制御できるリソースは次のとおりです。

    -   `memory_limit` : 最大ランタイムメモリを制限します。たとえば、「2G」は最大 2 GB のメモリが使用できることを意味します。

    -   `cpu_quota` : 実行時の最大 CPU 使用率を制限します。たとえば、「200%」などです。

    -   `io_read_bandwidth_max` : ディスク読み取りの最大 I/O 帯域幅を制限します。たとえば、 `"/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0 100M"`です。

    -   `io_write_bandwidth_max` : ディスク書き込みの最大 I/O 帯域幅を制限します。たとえば、 `/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0 100M`です。

    -   `limit_core` : コアダンプのサイズを制御します。

`global`構成例は次のとおりです。

```yaml
global:
  user: "tidb"
  resource_control:
    memory_limit: "2G"
```

上記の構成では、 `tidb`ユーザーを使用してクラスターを起動します。同時に、各コンポーネントは実行時に最大 2 GB のメモリに制限されます。

### <code>monitored</code> {#code-monitored-code}

`monitored` 、ターゲット マシンの監視サービスを構成するために使用されます: [`node_exporter`](https://github.com/prometheus/node_exporter)および[`blackbox_exporter`](https://github.com/prometheus/blackbox_exporter) 。次のフィールドが含まれます。

-   `node_exporter_port` : サービスポート`node_exporter` 。デフォルト値は`9100`です。

-   `blackbox_exporter_port` : サービスポート`blackbox_exporter` 。デフォルト値は`9115`です。

-   `deploy_dir` : 展開ディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `data_dir` : データディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`data_dir`ディレクトリに従ってディレクトリが生成されます。

-   `log_dir` : ログディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`log_dir`ディレクトリに従ってログが生成されます。

`monitored`構成例は次のとおりです。

```yaml
monitored:
  node_exporter_port: 9100
  blackbox_exporter_port: 9115
```

上記の構成では、 `node_exporter` `9100`ポートを使用し、 `blackbox_exporter` `9115`ポートを使用するように指定しています。

### <code>server_configs</code> {#code-server-configs-code}

`server_configs` 、サービスを設定し、各コンポーネントの設定ファイルを生成するために使用されます。 `global`セクションと同様に、このセクションの設定は、インスタンス内の同じ名前の設定によって上書きできます。 `server_configs`には主に次のフィールドが含まれます。

-   `tidb` : TiDB サービス関連の構成。完全な構成については、 [TiDB 構成ファイル](/tidb-configuration-file.md)参照してください。

-   `tikv` : TiKV サービス関連の構成。完全な構成については、 [TiKV 設定ファイル](/tikv-configuration-file.md)参照してください。

-   `pd` : PD サービス関連の設定。完全な設定については、 [PD 設定ファイル](/pd-configuration-file.md)参照してください。

-   `tiflash` : TiFlashサービス関連の構成。完全な構成については、 [TiFlash構成ファイル](/tiflash/tiflash-configuration.md)参照してください。

-   `tiflash_learner` : 各TiFlashノードには特別な組み込み TiKV があります。この構成項目は、この特別な TiKV を構成するために使用されます。通常、この構成項目の下のコンテンツを変更することは推奨されません。

-   `tiproxy` : TiProxy サービス関連の構成。完全な構成については、 [TiProxy 構成ファイル](/tiproxy/tiproxy-configuration.md)参照してください。

-   `pump` :Pumpサービス関連の構成。完全な構成については、 [TiDBBinlog構成ファイル](/tidb-binlog/tidb-binlog-configuration-file.md#pump)参照してください。

-   `drainer` :Drainerサービス関連の構成。完全な構成については、 [TiDBBinlog構成ファイル](/tidb-binlog/tidb-binlog-configuration-file.md#drainer)参照してください。

-   `cdc` : TiCDC サービス関連の構成。完全な構成については、 [TiCDC をデプロイ](/ticdc/deploy-ticdc.md)参照してください。

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
> TiDB、TiKV、PD、TiCDC など、バージョン番号を共有するコンポーネントについては、混合バージョンの展開シナリオで正しく動作することを確認するための完全なテストはありません。このセクションは、テスト環境でのみ使用するか、 [テクニカルサポート](/support.md)の助けを借りて使用してください。

`component_versions`特定のコンポーネントのバージョン番号を指定するために使用されます。

-   `component_versions`が設定されていない場合、各コンポーネントはTiDB クラスターと同じバージョン番号 (PD や TiKV など) を使用するか、最新バージョン (Alertmanager など) を使用します。
-   `component_versions`が設定されている場合、対応するコンポーネントは指定されたバージョンを使用し、このバージョンは後続のクラスターのスケーリングおよびアップグレード操作で使用されます。

特定のバージョンのコンポーネントを使用する必要がある場合にのみ構成するようにしてください。

`component_versions`には次のフィールドが含まれます。

-   `tikv` : TiKVコンポーネントのバージョン
-   `tiflash` : TiFlashコンポーネントのバージョン
-   `pd` : PDコンポーネントのバージョン
-   `tidb_dashboard` : スタンドアロンの TiDB ダッシュボードコンポーネントのバージョン
-   `pump` :Pumpコンポーネントのバージョン
-   `drainer` :Drainerコンポーネントのバージョン
-   `cdc` : CDCコンポーネントのバージョン
-   `kvcdc` : TiKV-CDCコンポーネントのバージョン
-   `tiproxy` : TiProxyコンポーネントのバージョン
-   `prometheus` : Prometheusコンポーネントのバージョン
-   `grafana` : Grafanaコンポーネントのバージョン
-   `alertmanager` : Alertmanagerコンポーネントのバージョン

以下は`component_versions`の構成例です。

```yaml
component_versions:
  kvcdc: "v1.1.1"
```

上記の構成では、TiKV-CDC のバージョン番号を`v1.1.1`に指定しています。

### <code>pd_servers</code> {#code-pd-servers-code}

`pd_servers` PD サービスが展開されるマシンを指定します。また、各マシンのサービス構成も指定します`pd_servers`は配列であり、配列の各要素には次のフィールドが含まれます。

-   `host` : PD サービスが展開されるマシンを指定します。フィールド値は IP アドレスであり、必須です。

-   `listen_host` : マシンに複数の IP アドレスがある場合、 `listen_host`サービスのリッスン IP アドレスを指定します。デフォルト値は`0.0.0.0`です。

-   `ssh_port` : 操作のためにターゲットマシンに接続するための SSH ポートを指定します。指定されていない場合は、 `global`のセクションのうち`ssh_port`番目が使用されます。

-   `name` : PD インスタンスの名前を指定します。異なるインスタンスには一意の名前を付ける必要があります。そうでない場合、インスタンスをデプロイできません。

-   `client_port` : PD がクライアントに接続するために使用するポートを指定します。デフォルト値は`2379`です。

-   `peer_port` : PD間の通信用のポートを指定します。デフォルト値は`2380`です。

-   `deploy_dir` : 展開ディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `data_dir` : データディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`data_dir`ディレクトリに従ってディレクトリが生成されます。

-   `log_dir` : ログディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`log_dir`ディレクトリに従ってログが生成されます。

-   `numa_node` : インスタンスに NUMA ポリシーを割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドを指定すると、cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)使用して割り当てられます。このフィールドは文字列型です。フィールド値は、&quot;0,1&quot; などの NUMA ノードの ID です。

-   `config` : このフィールドの設定ルールは、 `server_configs`の`pd`設定ルールと同じです。このフィールドが設定されている場合、フィールドの内容は`server_configs`の`pd`内容と結合されます (2 つのフィールドが重複している場合は、このフィールドの内容が有効になります)。その後、設定ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `os` : `host`で指定されたマシンのオペレーティング システム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値になります。

-   `arch` : `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値になります。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます (2 つのフィールドが重複している場合は、このフィールドの内容が有効になります)。次に、systemd 構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の構成ルールは、 `global`の`resource_control`内容と同じです。

上記のフィールドについては、デプロイメント後にこれらの構成済みフィールドを変更することはできません。

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

上記の構成では、 PD が`10.0.1.11`と`10.0.1.12`に展開されることを指定し、 `10.0.1.11`の PD に対して特定の構成を作成します。

### <code>tidb_servers</code> {#code-tidb-servers-code}

`tidb_servers` TiDB サービスがデプロイされるマシンを指定します。また、各マシンのサービス構成も指定します`tidb_servers`は配列であり、配列の各要素には次のフィールドが含まれます。

-   `host` : TiDB サービスがデプロイされるマシンを指定します。フィールド値は IP アドレスであり、必須です。

-   `listen_host` : マシンに複数の IP アドレスがある場合、 `listen_host`サービスのリッスン IP アドレスを指定します。デフォルト値は`0.0.0.0`です。

-   `ssh_port` : 操作のためにターゲットマシンに接続するための SSH ポートを指定します。指定されていない場合は、 `global`のセクションのうち`ssh_port`番目が使用されます。

-   `port` : MySQL クライアントへの接続を提供するために使用される TiDB サービスのリスニング ポート。デフォルト値は`4000`です。

-   `status_port` : TiDB ステータス サービスのリスニング ポート。HTTP 要求を介して外部から TiDB サービスのステータスを表示するために使用されます。デフォルト値は`10080`です。

-   `deploy_dir` : 展開ディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `log_dir` : ログディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`log_dir`ディレクトリに従ってログが生成されます。

-   `numa_node` : インスタンスに NUMA ポリシーを割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドを指定すると、cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)使用して割り当てられます。このフィールドは文字列型です。フィールド値は、&quot;0,1&quot; などの NUMA ノードの ID です。

-   `config` : このフィールドの設定ルールは、 `server_configs`の`tidb`設定ルールと同じです。このフィールドが設定されている場合、フィールドの内容は`server_configs`の`tidb`内容と結合されます (2 つのフィールドが重複している場合は、このフィールドの内容が有効になります)。その後、設定ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `os` : `host`で指定されたマシンのオペレーティング システム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値になります。

-   `arch` : `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値になります。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます (2 つのフィールドが重複している場合は、このフィールドの内容が有効になります)。次に、systemd 構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の構成ルールは、 `global`の`resource_control`内容と同じです。

上記のフィールドについては、デプロイメント後にこれらの構成済みフィールドを変更することはできません。

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

`tikv_servers` 、TiKV サービスが展開されるマシンを指定します。また、各マシンのサービス構成も指定します`tikv_servers`は配列であり、配列の各要素には次のフィールドが含まれます。

-   `host` : TiKV サービスが展開されるマシンを指定します。フィールド値は IP アドレスであり、必須です。

-   `listen_host` : マシンに複数の IP アドレスがある場合、 `listen_host`サービスのリッスン IP アドレスを指定します。デフォルト値は`0.0.0.0`です。

-   `ssh_port` : 操作のためにターゲットマシンに接続するための SSH ポートを指定します。指定されていない場合は、 `global`のセクションのうち`ssh_port`番目が使用されます。

-   `port` : TiKV サービスのリスニング ポート。デフォルト値は`20160`です。

-   `status_port` : TiKV ステータス サービスのリスニング ポート。デフォルト値は`20180`です。

-   `deploy_dir` : 展開ディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `data_dir` : データディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`data_dir`ディレクトリに従ってディレクトリが生成されます。

-   `log_dir` : ログディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`log_dir`ディレクトリに従ってログが生成されます。

-   `numa_node` : インスタンスに NUMA ポリシーを割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドを指定すると、cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)使用して割り当てられます。このフィールドは文字列型です。フィールド値は、&quot;0,1&quot; などの NUMA ノードの ID です。

-   `config` : このフィールドの設定ルールは、 `server_configs`の`tikv`設定ルールと同じです。このフィールドが設定されている場合、フィールドの内容は`server_configs`の`tikv`内容と結合されます (2 つのフィールドが重複している場合は、このフィールドの内容が有効になります)。その後、設定ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `os` : `host`で指定されたマシンのオペレーティング システム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値になります。

-   `arch` : `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値になります。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます (2 つのフィールドが重複している場合は、このフィールドの内容が有効になります)。次に、systemd 構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の構成ルールは、 `global`の`resource_control`内容と同じです。

上記のフィールドについては、デプロイメント後にこれらの構成済みフィールドを変更することはできません。

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

-   `ssh_port` : 操作のためにターゲットマシンに接続するための SSH ポートを指定します。指定されていない場合は、 `global`のセクションのうち`ssh_port`番目が使用されます。

-   `tcp_port` : 内部テスト用のTiFlash TCP サービスのポート。デフォルト値は`9000`です。TiUP v1.12.5 以降では、この構成項目はv7.1.0 以降のクラスターでは有効になりません。

-   `flash_service_port` : TiFlashがサービスを提供するポート。TiDB はこのポートを介してTiFlashからデータを読み取ります。デフォルト値は`3930`です。

-   `metrics_port` : メトリックデータを出力するために使用される TiFlash のステータス ポート。デフォルト値は`8234`です。

-   `flash_proxy_port` : 組み込み TiKV のポート。デフォルト値は`20170`です。

-   `flash_proxy_status_port` : 組み込み TiKV のステータス ポート。デフォルト値は`20292`です。

-   `deploy_dir` : 展開ディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `data_dir` : データディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`data_dir`ディレクトリに従ってディレクトリが生成されます。TiFlashは、カンマで区切られた複数の`data_dir`ディレクトリをサポートしています。

-   `log_dir` : ログディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`log_dir`ディレクトリに従ってログが生成されます。

-   `tmp_path` : TiFlash一時ファイルのstorageパス。デフォルト値は[ `path`または`storage.latest.dir`の最初のディレクトリ] + &quot;/tmp&quot;です。

-   `numa_node` : インスタンスに NUMA ポリシーを割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドを指定すると、cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)使用して割り当てられます。このフィールドは文字列型です。フィールド値は、&quot;0,1&quot; などの NUMA ノードの ID です。

-   `config` : このフィールドの設定ルールは、 `server_configs`の`tiflash`設定ルールと同じです。このフィールドが設定されている場合、フィールドの内容は`server_configs`の`tiflash`内容と結合されます (2 つのフィールドが重複している場合は、このフィールドの内容が有効になります)。その後、設定ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `learner_config` : 各TiFlashノードには特別な組み込み TiKV があります。この構成項目は、この特別な TiKV を構成するために使用されます。通常、この構成項目の下のコンテンツを変更することは推奨されません。

-   `os` : `host`で指定されたマシンのオペレーティング システム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値になります。

-   `arch` : `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値になります。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます (2 つのフィールドが重複している場合は、このフィールドの内容が有効になります)。次に、systemd 構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の構成ルールは、 `global`の`resource_control`内容と同じです。

デプロイ後、上記のフィールドではディレクトリを`data_dir`のみ追加できます。以下のフィールドでは、これらのフィールドを変更することはできません。

-   `host`
-   `tcp_port`
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

### <code>tiproxy_servers</code> {#code-tiproxy-servers-code}

`tiproxy_servers` TiProxy サービスが展開されるマシンと、各マシン上のサービス構成を指定します。2 `tiproxy_servers`配列であり、配列の各要素には次のフィールドが含まれます。

-   `host` : TiProxy サービスが展開されるマシンの IP アドレスを指定します。このフィールドは必須です。

-   `ssh_port` : 操作のためにターゲットマシンに接続するための SSH ポートを指定します。指定されていない場合は、 `global`のセクションのうち`ssh_port`番目が使用されます。

-   `port` : TiProxy SQL サービスのリスニング ポート。デフォルト値は`6000`です。

-   `deploy_dir` : デプロイメントディレクトリを指定します。指定されていない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`deploy_dir`ディレクトリに基づいてディレクトリが生成されます。

-   `data_dir` : データディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`data_dir`ディレクトリに基づいてディレクトリが生成されます。

-   `numa_node` : インスタンスに NUMA ポリシーを割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドが指定されている場合、 cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)使用して割り当てられます。このフィールドは文字列型です。値は NUMA ノードの ID (例: `"0,1"`です。

-   `config` : このフィールドの設定ルールは、 `server_configs`の`tiproxy`設定ルールと同じです。このフィールドが設定されている場合、フィールドの内容は`server_configs`の`tiproxy`内容と結合されます。これら 2 つのフィールドが重複している場合、このフィールドの内容が有効になります。その後、設定ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `os` : `host`で指定されたマシンのオペレーティング システム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値になります。

-   `arch` : `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値になります。

上記のフィールドのうち、次の構成済みフィールドは、デプロイメント後に変更できません。

-   `host`
-   `port`
-   `deploy_dir`
-   `data_dir`
-   `arch`
-   `os`

`tiproxy_servers`構成例は次のとおりです。

```yaml
tiproxy_servers:
  - host: 10.0.1.21
  - host: 10.0.1.22
```

### <code>pump_servers</code> {#code-pump-servers-code}

`pump_servers` TiDB BinlogのPumpサービスがデプロイされるマシンを指定します。また、各マシンのサービス構成も指定します`pump_servers`は配列であり、配列の各要素には次のフィールドが含まれます。

-   `host` : Pumpサービスが展開されるマシンを指定します。フィールド値は IP アドレスであり、必須です。

-   `ssh_port` : 操作のためにターゲットマシンに接続するための SSH ポートを指定します。指定されていない場合は、 `global`のセクションのうち`ssh_port`番目が使用されます。

-   `port` :Pumpサービスのリスニング ポート。デフォルト値は`8250`です。

-   `deploy_dir` : 展開ディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `data_dir` : データディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`data_dir`ディレクトリに従ってディレクトリが生成されます。

-   `log_dir` : ログディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`log_dir`ディレクトリに従ってログが生成されます。

-   `numa_node` : インスタンスに NUMA ポリシーを割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドを指定すると、cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)使用して割り当てられます。このフィールドは文字列型です。フィールド値は、&quot;0,1&quot; などの NUMA ノードの ID です。

-   `config` : このフィールドの設定ルールは、 `server_configs`の`pump`設定ルールと同じです。このフィールドが設定されている場合、フィールドの内容は`server_configs`の`pump`内容と結合されます (2 つのフィールドが重複している場合は、このフィールドの内容が有効になります)。その後、設定ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `os` : `host`で指定されたマシンのオペレーティング システム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値になります。

-   `arch` : `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値になります。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます (2 つのフィールドが重複している場合は、このフィールドの内容が有効になります)。次に、systemd 構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の構成ルールは、 `global`の`resource_control`内容と同じです。

上記のフィールドについては、デプロイメント後にこれらの構成済みフィールドを変更することはできません。

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

`drainer_servers` TiDB BinlogのDrainerサービスがデプロイされるマシンを指定します。また、各マシンのサービス構成も指定します`drainer_servers`は配列です。各配列要素には、次のフィールドが含まれます。

-   `host` : Drainerサービスが展開されるマシンを指定します。フィールド値は IP アドレスであり、必須です。

-   `ssh_port` : 操作のためにターゲットマシンに接続するための SSH ポートを指定します。指定されていない場合は、 `global`のセクションのうち`ssh_port`番目が使用されます。

-   `port` : Drainerサービスのリスニング ポート。デフォルト値は`8249`です。

-   `deploy_dir` : 展開ディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `data_dir` : データディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`data_dir`ディレクトリに従ってディレクトリが生成されます。

-   `log_dir` : ログディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`log_dir`ディレクトリに従ってログが生成されます。

-   `commit_ts` (非推奨): Drainer が起動すると、チェックポイントを読み取ります。Drainerがチェックポイントを取得しない場合は、このフィールドを初期起動のレプリケーション タイム ポイントとして使用します。このフィールドのデフォルトは`-1`です (Drainer は常に最新のタイムスタンプを PD から commit_ts として取得します)。

-   `numa_node` : インスタンスに NUMA ポリシーを割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドを指定すると、cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)使用して割り当てられます。このフィールドは文字列型です。フィールド値は、&quot;0,1&quot; などの NUMA ノードの ID です。

-   `config` : このフィールドの設定ルールは、 `server_configs`の`drainer`設定ルールと同じです。このフィールドが設定されている場合、フィールドの内容は`server_configs`の`drainer`内容と結合されます (2 つのフィールドが重複している場合は、このフィールドの内容が有効になります)。その後、設定ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `os` : `host`で指定されたマシンのオペレーティング システム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値になります。

-   `arch` : `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値になります。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます (2 つのフィールドが重複している場合は、このフィールドの内容が有効になります)。次に、systemd 構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の構成ルールは、 `global`の`resource_control`内容と同じです。

上記のフィールドについては、デプロイメント後にこれらの構成済みフィールドを変更することはできません。

-   `host`
-   `port`
-   `deploy_dir`
-   `data_dir`
-   `log_dir`
-   `arch`
-   `os`

`commit_ts`フィールドはTiUP v1.9.2 以降では非推奨となり、 Drainerの起動スクリプトには記録されません。このフィールドを引き続き使用する必要がある場合は、次の例を参照して`config`の`initial-commit-ts`フィールドを構成してください。

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

### <code>kvcdc_servers</code> {#code-kvcdc-servers-code}

`kvcdc_servers` [ティKV-CDC](https://tikv.org/docs/7.1/concepts/explore-tikv-features/cdc/cdc/)のサービスがデプロイされるマシンを指定します。また、各マシンのサービス構成も指定します`kvcdc_servers`は配列です。各配列要素には、次のフィールドが含まれます。

-   `host` : TiKV-CDC サービスがデプロイされるマシンを指定します。フィールド値は IP アドレスであり、必須です。

-   `ssh_port` : 操作のためにターゲットマシンに接続するための SSH ポートを指定します。指定されていない場合は、 `global`のセクションのうち`ssh_port`番目が使用されます。

-   `port` : TiKV-CDC サービスのリスニング ポート。デフォルト値は`8600`です。

-   `deploy_dir` : 展開ディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `data-dir` : TiKV-CDC が主にソート用の一時ファイルを格納するために使用するディレクトリを指定します (オプション)。このディレクトリの空きディスク領域は 500 GiB 以上が推奨されます。

-   `log_dir` : ログディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`log_dir`ディレクトリに従ってログが生成されます。

-   `gc-ttl` : TiKV-CDC によって設定された PD のサービス レベル GC セーフポイントの TTL (Time to Live、秒単位) (オプション)。これは、レプリケーション タスクを一時停止できる期間で、デフォルトは`86400` (24 時間) です。レプリケーション タスクを一時停止すると、TiKVガベージコレクションセーフポイントの進行に影響することに注意してください。 `gc-ttl`が長いほど、変更フィードを一時停止できる時間が長くなりますが、同時に、より多くの古いデータが保持され、より多くのスペースを占有します。その逆も同様です。

-   `tz` : TiKV-CDC サービスが使用するタイムゾーン。TiKV-CDC は、タイムスタンプなどの時間データ型を内部的に変換するとき、およびデータをダウンストリームに複製するときにこのタイムゾーンを使用します。デフォルト値は、プロセスが実行されるローカル タイムゾーンです。

-   `numa_node` : インスタンスに NUMA ポリシーを割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドを指定すると、cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)使用して割り当てられます。このフィールドは文字列型です。フィールド値は、&quot;0,1&quot; などの NUMA ノードの ID です。

-   `config` : TiKV-CDC が使用する構成ファイルのアドレス (オプション)。

-   `os` : `host`で指定されたマシンのオペレーティング システム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値になります。

-   `arch` : `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値になります。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます (2 つのフィールドが重複している場合は、このフィールドの内容が有効になります)。次に、systemd 構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の構成ルールは、 `global`の`resource_control`内容と同じです。

上記のフィールドについては、デプロイメント後にこれらの構成済みフィールドを変更することはできません。

-   `host`
-   `port`
-   `deploy_dir`
-   `data_dir`
-   `log_dir`
-   `arch`
-   `os`

`kvcdc_servers`構成例は次のとおりです。

```yaml
kvcdc_servers:
  - host: 10.0.1.21
  - host: 10.0.1.22
```

### <code>cdc_servers</code> {#code-cdc-servers-code}

`cdc_servers` TiCDC サービスが展開されるマシンを指定します。また、各マシンのサービス構成も指定します`cdc_servers`は配列です。各配列要素には、次のフィールドが含まれます。

-   `host` : TiCDC サービスが展開されるマシンを指定します。フィールド値は IP アドレスであり、必須です。

-   `ssh_port` : 操作のためにターゲットマシンに接続するための SSH ポートを指定します。指定されていない場合は、 `global`のセクションのうち`ssh_port`番目が使用されます。

-   `port` : TiCDC サービスのリスニング ポート。デフォルト値は`8300`です。

-   `deploy_dir` : 展開ディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `data_dir` : データディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`data_dir`ディレクトリに従ってディレクトリが生成されます。

-   `log_dir` : ログディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`log_dir`ディレクトリに従ってログが生成されます。

-   `gc-ttl` : PD で TiCDC によって設定されたサービス レベル GC セーフポイントの有効期間 (TTL) (秒単位)。デフォルト値は`86400` (24 時間) です。

-   `tz` : TiCDC サービスが使用するタイム ゾーン。TiCDC は、タイムスタンプなどの時間データ型を内部的に変換するとき、およびデータをダウンストリームに複製するときにこのタイム ゾーンを使用します。デフォルト値は、プロセスが実行されるローカル タイム ゾーンです。

-   `numa_node` : インスタンスに NUMA ポリシーを割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドを指定すると、cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)使用して割り当てられます。このフィールドは文字列型です。フィールド値は、&quot;0,1&quot; などの NUMA ノードの ID です。

-   `config` : フィールドの内容は`server_configs`の`cdc`内容と結合されます (2 つのフィールドが重複している場合は、このフィールドの内容が有効になります)。その後、構成ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `os` : `host`で指定されたマシンのオペレーティング システム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値になります。

-   `arch` : `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値になります。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます (2 つのフィールドが重複している場合は、このフィールドの内容が有効になります)。次に、systemd 構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の構成ルールは、 `global`の`resource_control`内容と同じです。

-   `ticdc_cluster_id` : サービスに対応する TiCDC クラスター ID を指定します。このフィールドが指定されていない場合、サービスはデフォルトの TiCDC クラスターに参加します。このフィールドは、TiDB v6.3.0 以降のバージョンでのみ有効です。

上記のフィールドについては、デプロイメント後にこれらの構成済みフィールドを変更することはできません。

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

`tispark_masters` TiSpark のマスター ノードがデプロイされるマシンを指定します。また、各マシンのサービス構成も指定します`tispark_masters`は配列です。各配列要素には、次のフィールドが含まれます。

-   `host` : TiSpark マスターがデプロイされるマシンを指定します。フィールド値は IP アドレスであり、必須です。

-   `listen_host` : マシンに複数の IP アドレスがある場合、 `listen_host`サービスのリッスン IP アドレスを指定します。デフォルト値は`0.0.0.0`です。

-   `ssh_port` : 操作のためにターゲットマシンに接続するための SSH ポートを指定します。指定されていない場合は、 `global`のセクションのうち`ssh_port`番目が使用されます。

-   `port` : ノード前の通信に使用される Spark のリスニング ポート。デフォルト値は`7077`です。

-   `web_port` : Web サービスとタスク ステータスを提供する Spark の Web ポート。デフォルト値は`8080`です。

-   `deploy_dir` : 展開ディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `java_home` : 使用する JRE 環境のパスを指定します。このパラメータは、 `JAVA_HOME`システム環境変数に対応します。

-   `spark_config` : TiSpark サービスを構成するように構成します。次に、構成ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `spark_env` : Spark の起動時に環境変数を設定します。

-   `os` : `host`で指定されたマシンのオペレーティング システム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値になります。

-   `arch` : `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値になります。

上記のフィールドについては、デプロイメント後にこれらの構成済みフィールドを変更することはできません。

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

`tispark_workers` TiSpark のワーカー ノードがデプロイされるマシンを指定します。また、各マシンのサービス構成も指定します`tispark_workers`は配列です。各配列要素には、次のフィールドが含まれます。

-   `host` : TiSpark ワーカーがデプロイされるマシンを指定します。フィールド値は IP アドレスであり、必須です。

-   `listen_host` : マシンに複数の IP アドレスがある場合、 `listen_host`サービスのリッスン IP アドレスを指定します。デフォルト値は`0.0.0.0`です。

-   `ssh_port` : 操作のためにターゲットマシンに接続するための SSH ポートを指定します。指定されていない場合は、 `global`のセクションのうち`ssh_port`番目が使用されます。

-   `port` : ノード前の通信に使用される Spark のリスニング ポート。デフォルト値は`7077`です。

-   `web_port` : Web サービスとタスク ステータスを提供する Spark の Web ポート。デフォルト値は`8080`です。

-   `deploy_dir` : 展開ディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `java_home` : 使用する JRE 環境が配置されているパスを指定します。このパラメータは、 `JAVA_HOME`システム環境変数に対応します。

-   `os` : `host`で指定されたマシンのオペレーティング システム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値になります。

-   `arch` : `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値になります。

上記のフィールドについては、デプロイメント後にこれらの構成済みフィールドを変更することはできません。

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

`monitoring_servers` Prometheus サービスがデプロイされるマシンを指定します。また、各マシンのサービス構成も指定します`monitoring_servers`は配列です。各配列要素には、次のフィールドが含まれます。

-   `host` : 監視サービスが展開されるマシンを指定します。フィールド値は IP アドレスであり、必須です。

-   `ng_port` : NgMonitoring がリッスンするポートを指定します。TiUP TiUPで導入されたこのフィールドは、 [継続的なプロファイリング](/dashboard/dashboard-profiling.md)と[Top SQL](/dashboard/top-sql.md)サポートします。デフォルト値は`12020`です。

-   `ssh_port` : 操作のためにターゲットマシンに接続するための SSH ポートを指定します。指定されていない場合は、 `global`のセクションのうち`ssh_port`番目が使用されます。

-   `port` : Prometheus サービスのリスニング ポート。デフォルト値は`9090`です。

-   `deploy_dir` : 展開ディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `data_dir` : データディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`data_dir`ディレクトリに従ってディレクトリが生成されます。

-   `log_dir` : ログディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`log_dir`ディレクトリに従ってログが生成されます。

-   `numa_node` : インスタンスに NUMA ポリシーを割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドを指定すると、cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)使用して割り当てられます。このフィールドは文字列型です。フィールド値は、&quot;0,1&quot; などの NUMA ノードの ID です。

-   `storage_retention` : Prometheus 監視データの保持時間。デフォルト値は`"30d"`です。

-   `rule_dir` : 完全な`*.rules.yml`のファイルを格納するローカル ディレクトリを指定します。これらのファイルは、Prometheus のルールとして、クラスター構成の初期化フェーズ中にターゲット マシンに転送されます。

-   `remote_config` : Prometheus データをリモートに書き込むか、リモートからデータを読み取ることをサポートします。このフィールドには 2 つの構成があります。
    -   `remote_write` : Prometheusドキュメント[`&#x3C;remote_write>`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write)を参照してください。
    -   `remote_read` : Prometheusドキュメント[`&#x3C;remote_read>`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_read)を参照してください。

-   `external_alertmanagers` : `external_alertmanagers`フィールドが設定されている場合、Prometheus はクラスター外の Alertmanager に設定動作を通知します。このフィールドは配列であり、各要素は外部 Alertmanager であり、 `host`フィールドと`web_port`フィールドで構成されます。

-   `os` : `host`で指定されたマシンのオペレーティング システム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値になります。

-   `arch` : `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値になります。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます (2 つのフィールドが重複している場合は、このフィールドの内容が有効になります)。次に、systemd 構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の構成ルールは、 `global`の`resource_control`内容と同じです。

-   `additional_args` : TiUP v1.15.0 で導入されたこのフィールドは、Prometheus を実行するための追加パラメータを構成します。このフィールドは配列であり、配列の各要素は Prometheus 実行パラメータです。たとえば、Prometheus ホット リロード機能を有効にするには、このフィールドを`--web.enable-lifecycle`に設定します。

-   `additional_scrape_conf` : カスタマイズされた Prometheus スクレイプ構成。TiDB クラスターをデプロイ、スケールアウト、スケールイン、またはリロードすると、 TiUP は`additional_scrape_conf`フィールドの内容を Prometheus 構成ファイルの対応するパラメーターに追加します。詳細については、 [Prometheus スクレイプ設定をカスタマイズする](/tiup/customized-montior-in-tiup-environment.md#customize-prometheus-scrape-configuration)参照してください。

上記のフィールドについては、デプロイメント後にこれらの構成済みフィールドを変更することはできません。

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
    additional_args:
    - --web.enable-lifecycle
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

`grafana_servers` Grafana サービスがデプロイされるマシンを指定します。また、各マシンのサービス構成も指定します`grafana_servers`は配列です。各配列要素には、次のフィールドが含まれます。

-   `host` : Grafana サービスがデプロイされるマシンを指定します。フィールド値は IP アドレスであり、必須です。

-   `ssh_port` : 操作のためにターゲットマシンに接続するための SSH ポートを指定します。指定されていない場合は、 `global`のセクションのうち`ssh_port`番目が使用されます。

-   `port` : Grafana サービスのリスニング ポート。デフォルト値は`3000`です。

-   `deploy_dir` : 展開ディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `os` : `host`で指定されたマシンのオペレーティング システム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値になります。

-   `arch` : `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値になります。

-   `username` : Grafana ログイン インターフェース上のユーザー名。

-   `password` : Grafanaに対応するパスワード。

-   `dashboard_dir` : 完全な`dashboard(*.json)`のファイルを格納するローカル ディレクトリを指定します。これらのファイルは、Grafana のダッシュボードとして、クラスター構成の初期化フェーズ中にターゲット マシンに転送されます。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます (2 つのフィールドが重複している場合は、このフィールドの内容が有効になります)。次に、systemd 構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の構成ルールは、 `global`の`resource_control`内容と同じです。

-   `config` : このフィールドは、Grafana にカスタム構成を追加するために使用されます。TiDB クラスターをデプロイ、スケールアウト、スケールイン、またはリロードすると、 TiUP は`config`フィールドの内容を Grafana 構成ファイル`grafana.ini`に追加します。詳細については、 [その他のGrafana設定をカスタマイズする](/tiup/customized-montior-in-tiup-environment.md#customize-other-grafana-configurations)参照してください。

> **注記：**
>
> `dashboard_dir`フィールドが`grafana_servers`に設定されている場合、クラスターの名前を変更する`tiup cluster rename`コマンドを実行した後、次の操作を実行する必要があります。
>
> 1.  ローカル ダッシュボード ディレクトリ内の`*.json`ファイルについては、 `datasource`フィールドの値を新しいクラスター名に更新します ( `datasource`クラスター名に基づいて名前が付けられているため)。
> 2.  `tiup cluster reload -R grafana`コマンドを実行します。

上記のフィールドについては、デプロイメント後にこれらの構成済みフィールドを変更することはできません。

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

`alertmanager_servers` Alertmanager サービスが展開されるマシンを指定します。また、各マシンのサービス構成も指定します`alertmanager_servers`は配列です。各配列要素には、次のフィールドが含まれます。

-   `host` : Alertmanager サービスが展開されるマシンを指定します。フィールド値は IP アドレスであり、必須です。

-   `ssh_port` : 操作のためにターゲットマシンに接続するための SSH ポートを指定します。指定されていない場合は、 `global`のセクションのうち`ssh_port`番目が使用されます。

-   `web_port` : Alertmanager が Web サービスを提供するために使用するポートを指定します。デフォルト値は`9093`です。

-   `cluster_port` : 1 つの Alertmanager と他の Alertmanager 間の通信ポートを指定します。デフォルト値は`9094`です。

-   `deploy_dir` : 展開ディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `data_dir` : データディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`data_dir`ディレクトリに従ってディレクトリが生成されます。

-   `log_dir` : ログディレクトリを指定します。指定しない場合、または相対ディレクトリとして指定した場合は、 `global`で設定した`log_dir`ディレクトリに従ってログが生成されます。

-   `numa_node` : インスタンスに NUMA ポリシーを割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドを指定すると、cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)使用して割り当てられます。このフィールドは文字列型です。フィールド値は、&quot;0,1&quot; などの NUMA ノードの ID です。

-   `config_file` : クラスター構成の初期化フェーズ中に Alertmanager の構成としてターゲット マシンに転送されるローカル ファイルを指定します。

-   `os` : `host`で指定されたマシンのオペレーティング システム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値になります。

-   `arch` : `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値になります。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます (2 つのフィールドが重複している場合は、このフィールドの内容が有効になります)。次に、systemd 構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の構成ルールは、 `global`の`resource_control`内容と同じです。

-   `listen_host` : Alertmanager にプロキシ経由でアクセスできるように、リスニング アドレスを指定します。 `0.0.0.0`に設定することをお勧めします。詳細については、 [Alertmanager 設定をカスタマイズする](/tiup/customized-montior-in-tiup-environment.md#customize-alertmanager-configurations)参照してください。

上記のフィールドについては、デプロイメント後にこれらの構成済みフィールドを変更することはできません。

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
