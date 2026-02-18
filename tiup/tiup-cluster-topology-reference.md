---
title: Topology Configuration File for TiDB Deployment Using TiUP
summary: TiUPは、トポロジファイルを使用してTiDBのクラスタートポロジをデプロイまたは変更します。また、Prometheus、Grafana、Alertmanagerなどの監視サーバーもデプロイします。トポロジファイルには、グローバル設定、監視サービス、コンポーネントバージョンなどのセクションが含まれています。各セクションでは、対応するサービスがデプロイされるマシンとその設定を指定します。
---

# TiUPを使用した TiDB デプロイメントのトポロジコンフィグレーションファイル {#topology-configuration-file-for-tidb-deployment-using-tiup}

TiUPを使用して TiDB をデプロイまたは拡張するには、クラスター トポロジを記述するトポロジ ファイル ( [サンプル](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml) ) を提供する必要があります。

同様に、クラスタートポロジを変更するには、トポロジファイルに変更を加える必要があります。違いは、クラスターのデプロイ後は、トポロジファイル内のフィールドの一部しか変更できないことです。このドキュメントでは、トポロジファイルの各セクションと各セクション内の各フィールドについて説明します。

TiUPを使用して TiDB クラスターをデプロイすると、Prometheus、Grafana、Alertmanager などの監視サーバーTiUPデプロイされます。また、このクラスターをスケールアウトすると、 TiUP は新しいノードを監視スコープに追加します。上記の監視サーバーの設定をカスタマイズするには、 [監視サーバーの構成をカスタマイズする](/tiup/customized-montior-in-tiup-environment.md)の手順に従ってください。

## ファイル構造 {#file-structure}

TiUPを使用した TiDB デプロイメントのトポロジ構成ファイルには、次のセクションが含まれる場合があります。

-   [グローバル](#global) : クラスターのグローバル設定。一部の設定項目はデフォルト値を使用しますが、インスタンスごとに個別に設定できます。
-   [監視](#monitored) : 監視サービス（blackbox_exporterと`node_exporter`のコンフィグレーション。各マシンに`node_exporter`と`blackbox_exporter`デプロイされています。
-   [サーバー構成](#server_configs) : コンポーネントのグローバル設定。各コンポーネントを個別に設定できます。インスタンスに同じ名前の設定項目がある場合は、インスタンスの設定項目が有効になります。
-   [コンポーネントバージョン](#component_versions) : コンポーネントバージョン。コンポーネントがクラスタバージョンを使用しない場合に設定します。このセクションはtiup-cluster v1.14.0で導入されました。
-   [pd_servers](#pd_servers) : PDインスタンスの構成。この構成では、PDコンポーネントがデプロイされるマシンを指定します。
-   [tidb_servers](#tidb_servers) : TiDBインスタンスの構成。この構成では、TiDBコンポーネントがデプロイされるマシンを指定します。
-   [tikv_servers](#tikv_servers) : TiKVインスタンスの構成。この構成では、TiKVコンポーネントがデプロイされるマシンを指定します。
-   [tiflash_servers](#tiflash_servers) : TiFlashインスタンスの構成。この構成では、 TiFlashコンポーネントがデプロイされるマシンを指定します。
-   [tiproxy_servers](#tiproxy_servers) : TiProxyインスタンスの構成。この構成は、TiProxyコンポーネントがデプロイされるマシンを指定します。
-   [kvcdc_servers](#kvcdc_servers) : インスタンス[TiKV-CDC](https://tikv.org/docs/7.1/concepts/explore-tikv-features/cdc/cdc/)の構成。この構成では、TiKV-CDCコンポーネントがデプロイされるマシンを指定します。
-   [cdc_servers](#cdc_servers) : TiCDCインスタンスの構成。この構成では、TiCDCコンポーネントがデプロイされるマシンを指定します。
-   [tso_servers](/tiup/tiup-cluster-topology-reference.md#tso_servers) : TSOインスタンスの設定。この設定は、 `tso`マイクロサービスがデプロイされるマシンを指定します（ [PDマイクロサービス](/pd-microservices.md)番目のマイクロサービスを有効にするには、 [`global`](#global)のマイクロサービスで`pd_mode: "ms"`マイクロサービスを設定する必要があります）。
-   [スケジューリングサーバー](/tiup/tiup-cluster-topology-reference.md#scheduling_servers) : スケジューリングインスタンスの設定。この設定では、 `scheduling`マイクロサービスがデプロイされるマシンを指定します（ [PDマイクロサービス](/pd-microservices.md)有効にするには、 [`global`](#global)で`pd_mode: "ms"`設定する必要があります）。
-   [監視サーバー](#monitoring_servers) : PrometheusとNGMonitoringがデプロイされるマシンを指定します。TiUPは複数のPrometheusインスタンスのデプロイをサポートしていますが、最初のインスタンスのみが使用されます。
-   [grafana_servers](#grafana_servers) : Grafanaインスタンスの設定。この設定では、Grafanaがデプロイされるマシンを指定します。
-   [アラートマネージャーサーバー](#alertmanager_servers) : Alertmanagerインスタンスの設定。この設定では、Alertmanagerがデプロイされるマシンを指定します。

### <code>global</code> {#code-global-code}

`global`セクションはクラスターのグローバル構成に対応し、次のフィールドがあります。

-   `user` : デプロイされたクラスターを起動するために使用するユーザー。デフォルト値は`"tidb"`です。4 フィールドに指定されたユーザーが`<user>`マシン上に存在しない場合、このユーザーは自動的に作成されます。

-   `group` : ユーザーが所属するユーザーグループ。ユーザー作成時に指定されます。デフォルト値は`<user>`番目のフィールドの値です。指定されたグループが存在しない場合は、自動的に作成されます。

-   `systemd_mode` : クラスタのデプロイメント時にターゲットマシンで使用される`systemd`モードを指定します。デフォルト値は`system`です。 `user`に設定すると、ターゲットマシンでsudo権限は不要になり、 [TiUP no-sudo モード](/tiup/tiup-cluster-no-sudo-mode.md)使用されます。

-   `ssh_port` : 操作のためにターゲットマシンに接続するためのSSHポートを指定します。デフォルト値は`22`です。

-   `enable_tls` : クラスタでTLSを有効にするかどうかを指定します。TLSを有効にすると、生成されたTLS証明書はコンポーネント間またはクライアントとコンポーネント間の接続に使用する必要があります。デフォルト値は`false`です。

-   `listen_host` : デフォルトのリスニングIPアドレスを指定します。空の場合、各インスタンスは、 `host`フィールドに`:`含まれているかどうかに基づいて、自動的に`::`または`0.0.0.0`に設​​定します。このフィールドはtiup-cluster v1.14.0で導入されました。

-   `deploy_dir` : 各コンポーネントの配置ディレクトリ。デフォルト値は`"deployed"`です。適用ルールは以下のとおりです。

    -   インスタンス レベルで絶対パス`deploy_dir`が設定されている場合、実際のデプロイメント ディレクトリはインスタンスに対して`deploy_dir`設定されます。

    -   各インスタンスに対して`deploy_dir`設定しない場合、デフォルト値は相対パス`<component-name>-<component-port>`になります。

    -   `global.deploy_dir`が絶対パスの場合、コンポーネントは`<global.deploy_dir>/<instance.deploy_dir>`ディレクトリにデプロイされます。

    -   `global.deploy_dir`相対パスの場合、コンポーネントは`/home/<global.user>/<global.deploy_dir>/<instance.deploy_dir>`ディレクトリにデプロイされます。

-   `data_dir` : データディレクトリ。デフォルト値: `"data"` 。適用ルールは以下のとおりです。

    -   インスタンス レベルで絶対パス`data_dir`が設定されている場合、実際のデプロイメント ディレクトリはインスタンスに対して`data_dir`設定されます。

    -   各インスタンスに対して`data_dir`設定しない場合、デフォルト値は`<global.data_dir>`になります。

    -   `data_dir`相対パスの場合、コンポーネントデータは`<deploy_dir>/<data_dir>`に配置されます。 `<deploy_dir>`の計算規則については、 `deploy_dir`フィールドの適用規則を参照してください。

-   `log_dir` : ログディレクトリ。デフォルト値: `"log"` 。適用ルールは以下のとおりです。

    -   絶対パス`log_dir`インスタンス レベルで構成されている場合、実際のログ ディレクトリはインスタンスに構成されている`log_dir`になります。

    -   各インスタンスで`log_dir`設定しない場合、デフォルト値は`<global.log_dir>`になります。

    -   `log_dir`相対パスの場合、コンポーネントログは`<deploy_dir>/<log_dir>`に配置されます。 `<deploy_dir>`の計算規則については、 `deploy_dir`フィールドの適用規則を参照してください。

-   `os` : ターゲットマシンのオペレーティングシステム。このフィールドは、ターゲットマシンにプッシュされるコンポーネントをどのオペレーティングシステムに適応させるかを制御します。デフォルト値は「linux」です。

-   `arch` : ターゲットマシンのCPUアーキテクチャ。このフィールドは、ターゲットマシンにプッシュされるバイナリパッケージをどのプラットフォームに適合させるかを制御します。サポートされている値は「amd64」と「arm64」です。デフォルト値は「amd64」です。

-   `pd_mode` : PD動作モード。このフィールドは、 [PDマイクロサービス](/pd-microservices.md)マイクロサービスを有効にするかどうかを制御します。サポートされる値は「ms」です。このフィールドを指定すると、PDマイクロサービスが有効になります。

-   `resource_control` : ランタイムリソース制御。このフィールドのすべての設定は、systemd のサービスファイルに書き込まれます。デフォルトでは制限はありません。制御可能なリソースは以下のとおりです。

    -   `memory_limit` : 最大ランタイムメモリを制限します。たとえば、「2G」は最大2GBのメモリが使用できることを意味します。

    -   `cpu_quota` : 実行時のCPU使用率の上限を制限します。例：200%

    -   `io_read_bandwidth_max` : ディスク読み取りの最大I/O帯域幅を制限します。例： `"/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0 100M"` 。

    -   `io_write_bandwidth_max` : ディスク書き込みの最大I/O帯域幅を制限します。例： `/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0 100M` 。

    -   `limit_core` : コアダンプのサイズを制御します。

`global`構成の例は次のとおりです。

```yaml
global:
  user: "tidb"
  resource_control:
    memory_limit: "2G"
```

上記の構成では、 `tidb`ユーザーを使用してクラスターを起動します。同時に、各コンポーネントは最大2GBに制限されます。

### <code>monitored</code> {#code-monitored-code}

`monitored`はターゲットマシン上の監視サービスを設定するために使用されます: [`node_exporter`](https://github.com/prometheus/node_exporter)および[`blackbox_exporter`](https://github.com/prometheus/blackbox_exporter) 。以下のフィールドが含まれます:

-   `node_exporter_port` : サービスポート`node_exporter`デフォルト値は`9100`です。

-   `blackbox_exporter_port` : サービスポート`blackbox_exporter`デフォルト値は`9115`です。

-   `deploy_dir` : デプロイメントディレクトリを指定します。指定されていない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `data_dir` : データディレクトリを指定します。指定されない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`data_dir`ディレクトリに従ってディレクトリが生成されます。

-   `log_dir` : ログディレクトリを指定します。指定されていない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`log_dir`ディレクトリに従ってログが生成されます。

`monitored`構成の例は次のとおりです。

```yaml
monitored:
  node_exporter_port: 9100
  blackbox_exporter_port: 9115
```

上記の構成では、 `node_exporter` `9100`ポートを使用し、 `blackbox_exporter` `9115`ポートを使用するように指定しています。

### <code>server_configs</code> {#code-server-configs-code}

`server_configs` 、サービスの設定と各コンポーネントの設定ファイルの生成に使用されます。2 `global`と同様に、このセクションの設定は、インスタンス内の同名の設定によって上書きできます。4 `server_configs`は主に以下のフィールドが含まれます。

-   `tidb` : TiDBサービス関連の設定。詳細な設定については[TiDB構成ファイル](/tidb-configuration-file.md)参照してください。

-   `tikv` : TiKVサービス関連の設定。詳細な設定については[TiKV設定ファイル](/tikv-configuration-file.md)参照してください。

-   `pd` : PDサービス関連の設定。詳細な設定については[PD設定ファイル](/pd-configuration-file.md)参照してください。

-   `tiflash` : TiFlashサービス関連の設定。詳細な設定については[TiFlash設定ファイル](/tiflash/tiflash-configuration.md)参照してください。

-   `tiflash_learner` : 各TiFlashノードには特別な TiKV が組み込まれています。この設定項目は、この特別な TiKV を設定するために使用されます。通常、この設定項目の内容を変更することは推奨されません。

-   `tiproxy` : TiProxyサービス関連の設定。詳細な設定については[TiProxy設定ファイル](/tiproxy/tiproxy-configuration.md)参照してください。

-   `cdc` : TiCDCサービス関連の設定。詳細な設定については[TiCDCをデプロイ](/ticdc/deploy-ticdc.md)参照してください。

-   `tso` : `tso`マイクロサービス関連の設定。完全な設定については[TSO構成ファイル](/tso-configuration-file.md)参照してください。

-   `scheduling` : `scheduling`マイクロサービス関連の設定。完全な設定については[スケジュール設定ファイル](/scheduling-configuration-file.md)参照してください。

`server_configs`構成の例は次のとおりです。

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
> TiDB、TiKV、PD、TiCDC など、バージョン番号を共有するコンポーネントについては、混在バージョンのデプロイメントシナリオで正常に動作することを保証するための完全なテストは存在しません。このセクションは、テスト環境でのみ使用するか、 [テクニカルサポート](/support.md)の支援を受けて使用してください。

`component_versions`は、特定のコンポーネントのバージョン番号を指定するために使用されます。

-   `component_versions`が設定されていない場合、各コンポーネントはTiDB クラスターと同じバージョン番号 (PD や TiKV など) を使用するか、最新バージョン (Alertmanager など) を使用します。
-   `component_versions`設定されている場合、対応するコンポーネントは指定されたバージョンを使用し、このバージョンは後続のクラスターのスケーリングおよびアップグレード操作で使用されます。

特定のバージョンのコンポーネントを使用する必要がある場合にのみ構成するようにしてください。

`component_versions`は次のフィールドが含まれます。

-   `tikv` : TiKVコンポーネントのバージョン
-   `tiflash` : TiFlashコンポーネントのバージョン
-   `pd` : PDコンポーネントのバージョン
-   `tidb_dashboard` : スタンドアロンの TiDB ダッシュボードコンポーネントのバージョン
-   `cdc` : CDCコンポーネントのバージョン
-   `kvcdc` : TiKV-CDCコンポーネントのバージョン
-   `tiproxy` : TiProxyコンポーネントのバージョン
-   `prometheus` : Prometheusコンポーネントのバージョン
-   `grafana` : Grafanaコンポーネントのバージョン
-   `alertmanager` : Alertmanagerコンポーネントのバージョン
-   `tso` : TSOコンポーネントのバージョン
-   `scheduling` : スケジュールコンポーネントのバージョン

以下は`component_versions`の構成例です。

```yaml
component_versions:
  kvcdc: "v1.1.1"
```

上記の構成では、TiKV-CDC のバージョン番号を`v1.1.1`に指定しています。

### <code>pd_servers</code> {#code-pd-servers-code}

`pd_servers` 、PD サービスがデプロイされるマシンを指定します。また、各マシンのサービス構成も指定します`pd_servers`は配列であり、配列の各要素には以下のフィールドが含まれます。

-   `host` : PDサービスがデプロイされるマシンを指定します。このフィールド値はIPアドレスで、必須です。

-   `listen_host` : マシンに複数のIPアドレスがある場合、 `listen_host`サービスのリスニングIPアドレスを指定します。デフォルト値は`0.0.0.0`です。

-   `ssh_port` : 操作のために対象マシンに接続するためのSSHポートを指定します。指定されていない場合は、 `global`セクションのうち`ssh_port`のセクションが使用されます。

-   `name` : PDインスタンスの名前を指定します。異なるインスタンスにはそれぞれ一意の名前を付ける必要があります。そうでない場合、インスタンスをデプロイできません。

-   `client_port` : PDがクライアントへの接続に使用するポートを指定します。デフォルト値は`2379`です。

-   `peer_port` : PD間の通信ポートを指定します。デフォルト値は`2380`です。

-   `deploy_dir` : デプロイメントディレクトリを指定します。指定されていない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `data_dir` : データディレクトリを指定します。指定されない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`data_dir`ディレクトリに従ってディレクトリが生成されます。

-   `log_dir` : ログディレクトリを指定します。指定されていない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`log_dir`ディレクトリに従ってログが生成されます。

-   `numa_node` : インスタンスにNUMAポリシーを割り当てます。このフィールドを指定する前に、対象マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドを指定した場合、cpubindおよびmembindポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)使用して割り当てられます。このフィールドは文字列型です。フィールド値はNUMAノードのID（例：&quot;0,1&quot;）です。

-   `config` : このフィールドの設定ルールは、 `server_configs`の`pd`設定ルールと同じです。このフィールドが設定されている場合、フィールドの内容は`server_configs`の`pd`内容とマージされます（2 つのフィールドが重複している場合は、このフィールドの内容が有効になります）。その後、設定ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `os` : `host`で指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値になります。

-   `arch` : `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値になります。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます（2つのフィールドが重複している場合は、このフィールドの内容が有効になります）。その後、systemd設定ファイルが生成され、 `host`で指定されたマシンに送信されます`resource_control`の設定ルールは、 `global`の`resource_control`内容と同じです。

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

`pd_servers`構成の例は次のとおりです。

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

`tidb_servers` TiDB サービスがデプロイされるマシンを指定します。また、各マシンのサービス構成も指定します`tidb_servers`は配列であり、配列の各要素には以下のフィールドが含まれます。

-   `host` : TiDBサービスがデプロイされるマシンを指定します。このフィールド値はIPアドレスで、必須です。

-   `listen_host` : マシンに複数のIPアドレスがある場合、 `listen_host`サービスのリスニングIPアドレスを指定します。デフォルト値は`0.0.0.0`です。

-   `ssh_port` : 操作のために対象マシンに接続するためのSSHポートを指定します。指定されていない場合は、 `global`セクションのうち`ssh_port`のセクションが使用されます。

-   `port` : TiDBサービスのリスニングポート。MySQLクライアントへの接続に使用されます。デフォルト値は`4000`です。

-   `status_port` : TiDBステータスサービスのリスニングポート。HTTPリクエストを介して外部からTiDBサービスのステータスを確認するために使用されます。デフォルト値は`10080`です。

-   `deploy_dir` : デプロイメントディレクトリを指定します。指定されていない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `log_dir` : ログディレクトリを指定します。指定されていない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`log_dir`ディレクトリに従ってログが生成されます。

-   `numa_node` : インスタンスにNUMAポリシーを割り当てます。このフィールドを指定する前に、対象マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドを指定した場合、cpubindおよびmembindポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)使用して割り当てられます。このフィールドは文字列型です。フィールド値はNUMAノードのID（例：&quot;0,1&quot;）です。

-   `config` : このフィールドの設定ルールは、 `server_configs`の`tidb`設定ルールと同じです。このフィールドが設定されている場合、フィールドの内容は`server_configs`の`tidb`内容とマージされます（2 つのフィールドが重複している場合は、このフィールドの内容が有効になります）。その後、設定ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `os` : `host`で指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値になります。

-   `arch` : `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値になります。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます（2つのフィールドが重複している場合は、このフィールドの内容が有効になります）。その後、systemd設定ファイルが生成され、 `host`で指定されたマシンに送信されます`resource_control`の設定ルールは、 `global`の`resource_control`内容と同じです。

上記のフィールドについては、デプロイメント後にこれらの構成済みフィールドを変更することはできません。

-   `host`
-   `listen_host`
-   `port`
-   `status_port`
-   `deploy_dir`
-   `log_dir`
-   `arch`
-   `os`

`tidb_servers`構成の例は次のとおりです。

```yaml
tidb_servers:
  - host: 10.0.1.14
    config:
      log.level: warn
      log.slow-query-file: tidb-slow-overwrited.log
  - host: 10.0.1.15
```

### <code>tikv_servers</code> {#code-tikv-servers-code}

`tikv_servers` TiKV サービスがデプロイされるマシンを指定します。また、各マシンのサービス構成も指定します`tikv_servers`は配列であり、配列の各要素には以下のフィールドが含まれます。

-   `host` : TiKVサービスがデプロイされるマシンを指定します。このフィールド値はIPアドレスで、必須です。

-   `listen_host` : マシンに複数のIPアドレスがある場合、 `listen_host`サービスのリスニングIPアドレスを指定します。デフォルト値は`0.0.0.0`です。

-   `ssh_port` : 操作のために対象マシンに接続するためのSSHポートを指定します。指定されていない場合は、 `global`セクションのうち`ssh_port`のセクションが使用されます。

-   `port` : TiKVサービスのリスニングポート。デフォルト値は`20160`です。

-   `status_port` : TiKVステータスサービスのリスニングポート。デフォルト値は`20180`です。

-   `deploy_dir` : デプロイメントディレクトリを指定します。指定されていない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `data_dir` : データディレクトリを指定します。指定されない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`data_dir`ディレクトリに従ってディレクトリが生成されます。

-   `log_dir` : ログディレクトリを指定します。指定されていない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`log_dir`ディレクトリに従ってログが生成されます。

-   `numa_node` : インスタンスにNUMAポリシーを割り当てます。このフィールドを指定する前に、対象マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドを指定した場合、cpubindおよびmembindポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)使用して割り当てられます。このフィールドは文字列型です。フィールド値はNUMAノードのID（例：&quot;0,1&quot;）です。

-   `config` : このフィールドの設定ルールは、 `server_configs`の`tikv`設定ルールと同じです。このフィールドが設定されている場合、フィールドの内容は`server_configs`の`tikv`内容とマージされます（2 つのフィールドが重複している場合は、このフィールドの内容が有効になります）。その後、設定ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `os` : `host`で指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値になります。

-   `arch` : `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値になります。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます（2つのフィールドが重複している場合は、このフィールドの内容が有効になります）。その後、systemd設定ファイルが生成され、 `host`で指定されたマシンに送信されます`resource_control`の設定ルールは、 `global`の`resource_control`内容と同じです。

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

`tikv_servers`構成の例は次のとおりです。

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

`tiflash_servers` 、 TiFlashサービスが展開されるマシンを指定します。また、各マシンにおけるサービス構成も指定します。このセクションは配列であり、配列の各要素には以下のフィールドが含まれます。

-   `host` : TiFlashサービスが展開されるマシンを指定します。このフィールド値は IP アドレスで、必須です。

-   `ssh_port` : 操作のために対象マシンに接続するためのSSHポートを指定します。指定されていない場合は、 `global`セクションのうち`ssh_port`のセクションが使用されます。

-   `tcp_port` : 内部テスト用のTiFlash TCPサービスのポート。デフォルト値は`9000`です。TiUP TiUP以降、この設定項目はv7.1.0以降のクラスターでは有効になりません。

-   `flash_service_port` : TiFlashがサービスを提供するポート。TiDBはこのポートを介してTiFlashからデータを読み取ります。デフォルト値は`3930`です。

-   `metrics_port` : TiFlashのステータスポート。メトリックデータの出力に使用されます。デフォルト値は`8234`です。

-   `flash_proxy_port` : 内蔵TiKVのポート。デフォルト値は`20170`です。

-   `flash_proxy_status_port` : 内蔵TiKVのステータスポート。デフォルト値は`20292`です。

-   `deploy_dir` : デプロイメントディレクトリを指定します。指定されていない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `data_dir` : データディレクトリを指定します。指定されていない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`data_dir`ディレクトリに従ってディレクトリが生成されます。TiFlashは、カンマで区切られた複数の`data_dir`ディレクトリをサポートしています。

-   `log_dir` : ログディレクトリを指定します。指定されていない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`log_dir`ディレクトリに従ってログが生成されます。

-   `tmp_path` : TiFlash一時ファイルのstorageパス。デフォルト値は[ `path`または`storage.latest.dir`の最初のディレクトリ] + &quot;/tmp&quot;です。

-   `numa_node` : インスタンスにNUMAポリシーを割り当てます。このフィールドを指定する前に、対象マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドを指定した場合、cpubindおよびmembindポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)使用して割り当てられます。このフィールドは文字列型です。フィールド値はNUMAノードのID（例：&quot;0,1&quot;）です。

-   `config` : このフィールドの設定ルールは、 `server_configs`の`tiflash`設定ルールと同じです。このフィールドが設定されている場合、フィールドの内容は`server_configs`の`tiflash`内容とマージされます（2 つのフィールドが重複している場合は、このフィールドの内容が有効になります）。その後、設定ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `learner_config` : 各TiFlashノードには特別な TiKV が組み込まれています。この設定項目は、この特別な TiKV を設定するために使用されます。通常、この設定項目の内容を変更することは推奨されません。

-   `os` : `host`で指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値になります。

-   `arch` : `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値になります。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます（2つのフィールドが重複している場合は、このフィールドの内容が有効になります）。その後、systemd設定ファイルが生成され、 `host`で指定されたマシンに送信されます`resource_control`の設定ルールは、 `global`の`resource_control`内容と同じです。

デプロイメント後、上記のフィールドではディレクトリを`data_dir`にのみ追加できます。以下のフィールドでは、これらのフィールドを変更することはできません。

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

`tiflash_servers`構成の例は次のとおりです。

```yaml
tiflash_servers:
  - host: 10.0.1.21
  - host: 10.0.1.22
```

### <code>tiproxy_servers</code> {#code-tiproxy-servers-code}

`tiproxy_servers` 、TiProxy サービスが展開されるマシンと、各マシン上のサービスの構成を指定します。2 `tiproxy_servers`配列であり、配列の各要素には次のフィールドが含まれます。

-   `host` : TiProxyサービスがデプロイされているマシンのIPアドレスを指定します。このフィールドは必須です。

-   `ssh_port` : 操作のために対象マシンに接続するためのSSHポートを指定します。指定されていない場合は、 `global`セクションのうち`ssh_port`のセクションが使用されます。

-   `port` : TiProxy SQL サービスのリスニングポート。デフォルト値は`6000`です。

-   `status_port` : TiProxyステータスサービスのリスニングポート。HTTPリクエストを介して外部からTiProxyサービスのステータスを確認するために使用されます。デフォルト値は`3080`です。

-   `deploy_dir` : デプロイメントディレクトリを指定します。指定されていない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`deploy_dir`ディレクトリに基づいてディレクトリが生成されます。

-   `numa_node` : インスタンスにNUMAポリシーを割り当てます。このフィールドを指定する前に、対象マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドを指定した場合、 cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。値は NUMA ノードの ID（例： `"0,1"`です。

-   `config` : このフィールドの設定ルールは、 `server_configs`の`tiproxy`設定ルールと同じです。このフィールドが設定されている場合、フィールドの内容は`server_configs`の`tiproxy`内容とマージされます。これら 2 つのフィールドが重複している場合、このフィールドの内容が有効になります。その後、設定ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `os` : `host`で指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値になります。

-   `arch` : `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値になります。

上記のフィールドのうち、次の設定済みフィールドは、デプロイメント後に変更できません。

-   `host`
-   `port`
-   `deploy_dir`
-   `arch`
-   `os`

`tiproxy_servers`構成の例は次のとおりです。

```yaml
tiproxy_servers:
  - host: 10.0.1.21
    port: 6000
    status_port: 3080
    config:
      labels: { zone: "zone1" }
  - host: 10.0.1.22
    port: 6000
    status_port: 3080
    config:
      labels: { zone: "zone2" }
```

その他の構成例については、 [TiProxy 展開トポロジ](/tiproxy/tiproxy-deployment-topology.md)参照してください。

### <code>kvcdc_servers</code> {#code-kvcdc-servers-code}

`kvcdc_servers` 、 [TiKV-CDC](https://tikv.org/docs/7.1/concepts/explore-tikv-features/cdc/cdc/)サービスがデプロイされるマシンを指定します。また、各マシンにおけるサービス構成も指定します`kvcdc_servers`は配列です。各配列要素には、以下のフィールドが含まれます。

-   `host` : TiKV-CDC サービスがデプロイされるマシンを指定します。このフィールド値は IP アドレスで、必須です。

-   `ssh_port` : 操作のために対象マシンに接続するためのSSHポートを指定します。指定されていない場合は、 `global`セクションのうち`ssh_port`のセクションが使用されます。

-   `port` : TiKV-CDCサービスのリスニングポート。デフォルト値は`8600`です。

-   `deploy_dir` : デプロイメントディレクトリを指定します。指定されていない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `data-dir` : TiKV-CDC が主にソート用の一時ファイルを保存するディレクトリを指定します（オプション）。このディレクトリの空きディスク容量は500 GiB以上が推奨されます。

-   `log_dir` : ログディレクトリを指定します。指定されていない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`log_dir`ディレクトリに従ってログが生成されます。

-   `gc-ttl` : TiKV-CDC（オプション）によってPDに設定されるサービスレベルGCセーフポイントのTTL（Time to Live、秒単位）。これはレプリケーションタスクを一時停止できる期間で、デフォルトは`86400` （24時間）です。レプリケーションタスクの一時停止は、TiKVガベージコレクションセーフポイントの進行状況に影響することに注意してください。 `gc-ttl`長いほど、変更フィードを一時停止できる時間は長くなりますが、同時に、より多くの古いデータが保持され、より多くのスペースを占有することになります。逆もまた同様です。

-   `tz` : TiKV-CDCサービスが使用するタイムゾーン。TiKV-CDCは、タイムスタンプなどの時間データ型を内部的に変換する際、および下流にデータを複製する際にこのタイムゾーンを使用します。デフォルト値は、プロセスが実行されるローカルタイムゾーンです。

-   `numa_node` : インスタンスにNUMAポリシーを割り当てます。このフィールドを指定する前に、対象マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドを指定した場合、cpubindおよびmembindポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)使用して割り当てられます。このフィールドは文字列型です。フィールド値はNUMAノードのID（例：&quot;0,1&quot;）です。

-   `config` : TiKV-CDC が使用する構成ファイルのアドレス (オプション)。

-   `os` : `host`で指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値になります。

-   `arch` : `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値になります。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます（2つのフィールドが重複している場合は、このフィールドの内容が有効になります）。その後、systemd設定ファイルが生成され、 `host`で指定されたマシンに送信されます`resource_control`の設定ルールは、 `global`の`resource_control`内容と同じです。

上記のフィールドについては、デプロイメント後にこれらの構成済みフィールドを変更することはできません。

-   `host`
-   `port`
-   `deploy_dir`
-   `data_dir`
-   `log_dir`
-   `arch`
-   `os`

`kvcdc_servers`構成の例は次のとおりです。

```yaml
kvcdc_servers:
  - host: 10.0.1.21
  - host: 10.0.1.22
```

### <code>cdc_servers</code> {#code-cdc-servers-code}

`cdc_servers` TiCDCサービスがデプロイされるマシンを指定します。また、各マシンにおけるサービス構成も指定します`cdc_servers`は配列です。各配列要素には以下のフィールドが含まれます。

-   `host` : TiCDC サービスがデプロイされるマシンを指定します。このフィールド値は IP アドレスで、必須です。

-   `ssh_port` : 操作のために対象マシンに接続するためのSSHポートを指定します。指定されていない場合は、 `global`セクションのうち`ssh_port`のセクションが使用されます。

-   `port` : TiCDCサービスのリスニングポート。デフォルト値は`8300`です。

-   `deploy_dir` : デプロイメントディレクトリを指定します。指定されていない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `data_dir` : データディレクトリを指定します。指定されない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`data_dir`ディレクトリに従ってディレクトリが生成されます。

-   `log_dir` : ログディレクトリを指定します。指定されていない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`log_dir`ディレクトリに従ってログが生成されます。

-   `gc-ttl` : TiCDCによってPDに設定されるサービスレベルGCセーフポイントのTime To Live（TTL）期間（秒）。デフォルト値は`86400` （24時間）です。

-   `tz` : TiCDCサービスが使用するタイムゾーン。TiCDCは、タイムスタンプなどの時間データ型を内部的に変換する際、および下流にデータを複製する際にこのタイムゾーンを使用します。デフォルト値は、プロセスが実行されるローカルタイムゾーンです。

-   `numa_node` : インスタンスにNUMAポリシーを割り当てます。このフィールドを指定する前に、対象マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドを指定した場合、cpubindおよびmembindポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)使用して割り当てられます。このフィールドは文字列型です。フィールド値はNUMAノードのID（例：&quot;0,1&quot;）です。

-   `config` : フィールドの内容は`server_configs`の`cdc`内容とマージされます（2つのフィールドが重複している場合は、このフィールドの内容が有効になります）。その後、設定ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `os` : `host`で指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値になります。

-   `arch` : `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値になります。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます（2つのフィールドが重複している場合は、このフィールドの内容が有効になります）。その後、systemd設定ファイルが生成され、 `host`で指定されたマシンに送信されます`resource_control`の設定ルールは、 `global`の`resource_control`内容と同じです。

-   `ticdc_cluster_id` : サービスに対応するTiCDCクラスタIDを指定します。このフィールドが指定されていない場合、サービスはデフォルトのTiCDCクラスタに参加します。このフィールドはTiDB v6.3.0以降のバージョンでのみ有効です。

上記のフィールドについては、デプロイメント後にこれらの構成済みフィールドを変更することはできません。

-   `host`
-   `port`
-   `deploy_dir`
-   `data_dir`
-   `log_dir`
-   `arch`
-   `os`
-   `ticdc_cluster_id`

`cdc_servers`構成の例は次のとおりです。

```yaml
cdc_servers:
  - host: 10.0.1.20
    gc-ttl: 86400
    data_dir: "/cdc-data"
  - host: 10.0.1.21
    gc-ttl: 86400
    data_dir: "/cdc-data"
```

### <code>tso_servers</code> {#code-tso-servers-code}

`tso_servers` 、 `tso`マイクロサービスがデプロイされるマシンを指定します。また、各マシンのサービス構成も指定します。4 `tso_servers`配列であり、配列の各要素には以下のフィールドが含まれます。

-   `host` : `tso`マイクロサービスがデプロイされているマシンのIPアドレスを指定します。このフィールド値は必須です。
-   `ssh_port` : 操作のために対象マシンに接続するためのSSHポートを指定します。指定されていない場合は、 `global`セクションのうち`ssh_port`のセクションが使用されます。
-   `port` : `tso`マイクロサービスのリスニングポートを指定します。デフォルト値は`3379`です。
-   `deploy_dir` : デプロイメントディレクトリを指定します。指定されていない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`deploy_dir`ディレクトリに従ってディレクトリが生成されます。
-   `data_dir` : データディレクトリを指定します。指定されない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`data_dir`ディレクトリに従ってディレクトリが生成されます。
-   `config` : このフィールドの設定ルールは、 `server_configs`の`tso`設定ルールと同じです。このフィールドが設定されている場合、フィールドの内容は`server_configs`の`tso`内容とマージされます（2 つのフィールドが重複している場合は、このフィールドの内容が有効になります）。その後、設定ファイルが生成され、 `host`で指定されたマシンに送信されます。
-   `os` : `host`で指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値になります。
-   `arch` : `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値になります。

上記のフィールドのうち、デプロイメント後に次のフィールドを変更することはできません。

-   `host`
-   `port`
-   `deploy_dir`
-   `data_dir`
-   `arch`
-   `os`

`tso_servers`構成の例は次のとおりです。

```yaml
tso_servers:
  - host: 10.0.1.21
  - host: 10.0.1.22
```

### <code>scheduling_servers</code> {#code-scheduling-servers-code}

`scheduling_servers` 、 `scheduling`マイクロサービスがデプロイされるマシンを指定します。また、各マシンのサービス構成も指定します。4 `scheduling_servers`配列であり、配列の各要素には以下のフィールドが含まれます。

-   `host` : `scheduling`マイクロサービスがデプロイされているマシンのIPアドレスを指定します。このフィールドは必須です。
-   `ssh_port` : 操作のために対象マシンに接続するためのSSHポートを指定します。指定されていない場合は、 `global`セクションのうち`ssh_port`のセクションが使用されます。
-   `port` : `scheduling`マイクロサービスのリスニングポートを指定します。デフォルト値は`3379`です。
-   `deploy_dir` : デプロイメントディレクトリを指定します。指定されていない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`deploy_dir`ディレクトリに従ってディレクトリが生成されます。
-   `data_dir` : データディレクトリを指定します。指定されない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`data_dir`ディレクトリに従ってディレクトリが生成されます。
-   `config` : このフィールドの設定ルールは、 `server_configs`の`scheduling`設定ルールと同じです。このフィールドが設定されている場合、フィールドの内容は`server_configs`の`scheduling`内容とマージされます（2 つのフィールドが重複している場合は、このフィールドの内容が有効になります）。その後、設定ファイルが生成され、 `host`で指定されたマシンに送信されます。
-   `os` : `host`で指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値になります。
-   `arch` : `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値になります。

上記のフィールドのうち、デプロイメント後に次のフィールドを変更することはできません。

-   `host`
-   `port`
-   `deploy_dir`
-   `data_dir`
-   `arch`
-   `os`

`scheduling_servers`構成の例は次のとおりです。

```yaml
scheduling_servers:
  - host: 10.0.1.21
  - host: 10.0.1.22
```

### <code>monitoring_servers</code> {#code-monitoring-servers-code}

`monitoring_servers` 、Prometheus サービスがデプロイされるマシンを指定します。また、各マシンのサービス設定も指定します`monitoring_servers`は配列です。各配列要素には以下のフィールドが含まれます。

-   `host` : 監視サービスがデプロイされているマシンを指定します。このフィールド値はIPアドレスで、必須です。

-   `ng_port` : NgMonitoringがリッスンするポートを指定します。TiUP TiUPで導入されたこのフィールドは、 [継続的なプロファイリング](/dashboard/dashboard-profiling.md)と[Top SQL](/dashboard/top-sql.md)をサポートします。デフォルト値は`12020`です。

-   `ssh_port` : 操作のために対象マシンに接続するためのSSHポートを指定します。指定されていない場合は、 `global`セクションのうち`ssh_port`のセクションが使用されます。

-   `port` : Prometheusサービスのリスニングポート。デフォルト値は`9090`です。

-   `deploy_dir` : デプロイメントディレクトリを指定します。指定されていない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `data_dir` : データディレクトリを指定します。指定されない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`data_dir`ディレクトリに従ってディレクトリが生成されます。

-   `log_dir` : ログディレクトリを指定します。指定されていない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`log_dir`ディレクトリに従ってログが生成されます。

-   `numa_node` : インスタンスにNUMAポリシーを割り当てます。このフィールドを指定する前に、対象マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドを指定した場合、cpubindおよびmembindポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)使用して割り当てられます。このフィールドは文字列型です。フィールド値はNUMAノードのID（例：&quot;0,1&quot;）です。

-   `storage_retention` : Prometheus監視データの保持期間。デフォルト値は`"30d"`です。

-   `rule_dir` : `*.rules.yml`ファイルすべてを含むローカルディレクトリを指定します。これらのファイルは、Prometheusのルールとして、クラスター構成の初期化フェーズ中にターゲットマシンに転送されます。

-   `remote_config` : Prometheusデータのリモートへの書き込み、またはリモートからのデータの読み取りをサポートします。このフィールドには2つの設定があります。
    -   `remote_write` : Prometheus ドキュメント[`&#x3C;remote_write>`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write)を参照してください。
    -   `remote_read` : Prometheus ドキュメント[`&#x3C;remote_read>`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_read)を参照してください。

-   `external_alertmanagers` : `external_alertmanagers`番目のフィールドが設定されている場合、Prometheusはクラスター外のAlertmanagerに構成動作を通知します。このフィールドは配列であり、各要素は外部Alertmanagerであり、 `host`と`web_port`番目のフィールドで構成されます。

-   `os` : `host`で指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値になります。

-   `arch` : `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値になります。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます（2つのフィールドが重複している場合は、このフィールドの内容が有効になります）。その後、systemd設定ファイルが生成され、 `host`で指定されたマシンに送信されます`resource_control`の設定ルールは、 `global`の`resource_control`内容と同じです。

-   `additional_args` : TiUP v1.15.0で導入されたこのフィールドは、Prometheusの実行に必要な追加パラメータを設定します。このフィールドは配列であり、配列の各要素はPrometheusの実行パラメータです。例えば、Prometheusのホットリロード機能を有効にするには、このフィールドを`--web.enable-lifecycle`に設定します。

-   `additional_scrape_conf` : カスタマイズされたPrometheusスクレイプ設定。TiDBクラスターをデプロイ、スケールアウト、スケールイン、またはリロードすると、 TiUPは`additional_scrape_conf`フィールドの内容をPrometheus設定ファイルの対応するパラメータに追加します。詳細については、 [Prometheusのスクレイプ設定をカスタマイズする](/tiup/customized-montior-in-tiup-environment.md#customize-prometheus-scrape-configuration)参照してください。

上記のフィールドについては、デプロイメント後にこれらの構成済みフィールドを変更することはできません。

-   `host`
-   `port`
-   `deploy_dir`
-   `data_dir`
-   `log_dir`
-   `arch`
-   `os`

`monitoring_servers`構成の例は次のとおりです。

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

`grafana_servers` 、Grafana サービスがデプロイされるマシンを指定します。また、各マシンにおけるサービス設定も指定します`grafana_servers`は配列です。各配列要素には以下のフィールドが含まれます。

-   `host` : Grafanaサービスがデプロイされるマシンを指定します。このフィールド値はIPアドレスで、必須です。

-   `ssh_port` : 操作のために対象マシンに接続するためのSSHポートを指定します。指定されていない場合は、 `global`セクションのうち`ssh_port`のセクションが使用されます。

-   `port` : Grafanaサービスのリスニングポート。デフォルト値は`3000`です。

-   `deploy_dir` : デプロイメントディレクトリを指定します。指定されていない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `os` : `host`で指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値になります。

-   `arch` : `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値になります。

-   `username` : Grafana ログイン インターフェース上のユーザー名。

-   `password` : Grafanaに対応するパスワード。

-   `dashboard_dir` : `dashboard(*.json)`ファイルすべてを含むローカルディレクトリを指定します。これらのファイルは、クラスター構成の初期化フェーズ中に、Grafanaのダッシュボードとしてターゲットマシンに転送されます。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます（2つのフィールドが重複している場合は、このフィールドの内容が有効になります）。その後、systemd設定ファイルが生成され、 `host`で指定されたマシンに送信されます`resource_control`の設定ルールは、 `global`の`resource_control`内容と同じです。

-   `config` : このフィールドは、Grafanaにカスタム設定を追加するために使用されます。TiDBクラスターをデプロイ、スケールアウト、スケールイン、またはリロードすると、 TiUPは`config`フィールドの内容をGrafana設定ファイル`grafana.ini`に追加します。詳細については、 [その他のGrafana設定をカスタマイズする](/tiup/customized-montior-in-tiup-environment.md#customize-other-grafana-configurations)参照してください。

> **注記：**
>
> `dashboard_dir`フィールドが`grafana_servers`に設定されている場合、クラスターの名前を変更する`tiup cluster rename`コマンドを実行した後、次の操作を実行する必要があります。
>
> 1.  ローカル ダッシュボード ディレクトリ内の`*.json`ファイルについては、 `datasource`フィールドの値を新しいクラスター名に更新します ( `datasource`クラスター名に基づいて命名されているため)。
> 2.  `tiup cluster reload -R grafana`コマンドを実行します。

上記のフィールドについては、デプロイメント後にこれらの構成済みフィールドを変更することはできません。

-   `host`
-   `port`
-   `deploy_dir`
-   `arch`
-   `os`

`grafana_servers`構成の例は次のとおりです。

```yaml
grafana_servers:
  - host: 10.0.1.11
    dashboard_dir: /local/dashboard/dir
```

### <code>alertmanager_servers</code> {#code-alertmanager-servers-code}

`alertmanager_servers` 、Alertmanager サービスがデプロイされるマシンを指定します。また、各マシンのサービス構成も指定します`alertmanager_servers`は配列です。各配列要素には、以下のフィールドが含まれます。

-   `host` : Alertmanager サービスがデプロイされているマシンを指定します。このフィールド値は IP アドレスで、必須です。

-   `ssh_port` : 操作のために対象マシンに接続するためのSSHポートを指定します。指定されていない場合は、 `global`セクションのうち`ssh_port`のセクションが使用されます。

-   `web_port` : AlertmanagerがWebサービスを提供するために使用するポートを指定します。デフォルト値は`9093`です。

-   `cluster_port` : Alertmanager間の通信ポートを指定します。デフォルト値は`9094`です。

-   `deploy_dir` : デプロイメントディレクトリを指定します。指定されていない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`deploy_dir`ディレクトリに従ってディレクトリが生成されます。

-   `data_dir` : データディレクトリを指定します。指定されない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`data_dir`ディレクトリに従ってディレクトリが生成されます。

-   `log_dir` : ログディレクトリを指定します。指定されていない場合、または相対ディレクトリとして指定された場合は、 `global`で設定された`log_dir`ディレクトリに従ってログが生成されます。

-   `numa_node` : インスタンスにNUMAポリシーを割り当てます。このフィールドを指定する前に、対象マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドを指定した場合、cpubindおよびmembindポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)使用して割り当てられます。このフィールドは文字列型です。フィールド値はNUMAノードのID（例：&quot;0,1&quot;）です。

-   `config_file` : クラスター構成の初期化フェーズ中に、Alertmanager の構成としてターゲット マシンに転送されるローカル ファイルを指定します。

-   `os` : `host`で指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値になります。

-   `arch` : `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値になります。

-   `resource_control` : サービスのリソース制御。このフィールドが設定されている場合、フィールドの内容は`global`の`resource_control`内容とマージされます（2つのフィールドが重複している場合は、このフィールドの内容が有効になります）。その後、systemd設定ファイルが生成され、 `host`で指定されたマシンに送信されます`resource_control`の設定ルールは、 `global`の`resource_control`内容と同じです。

-   `listen_host` : Alertmanager にプロキシ経由でアクセスできるように、リスニングアドレスを指定します。 `0.0.0.0`に設定することをお勧めします。詳細については、 [Alertmanager 設定をカスタマイズする](/tiup/customized-montior-in-tiup-environment.md#customize-alertmanager-configurations)参照してください。

上記のフィールドについては、デプロイメント後にこれらの構成済みフィールドを変更することはできません。

-   `host`
-   `web_port`
-   `cluster_port`
-   `deploy_dir`
-   `data_dir`
-   `log_dir`
-   `arch`
-   `os`

`alertmanager_servers`構成の例は次のとおりです。

```yaml
alertmanager_servers:
  - host: 10.0.1.11
    config_file: /local/config/file
  - host: 10.0.1.12
    config_file: /local/config/file
```
