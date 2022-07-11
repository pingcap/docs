---
title: Topology Configuration File for TiDB Deployment Using TiUP
---

# TiUPを使用したTiDB展開用のトポロジConfiguration / コンフィグレーションファイル {#topology-configuration-file-for-tidb-deployment-using-tiup}

TiUPを使用してTiDBを展開またはスケーリングするには、クラスタトポロジを記述するトポロジファイル（ [サンプル](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml) ）を提供する必要があります。

同様に、クラスタトポロジを変更するには、トポロジファイルを変更する必要があります。違いは、クラスタがデプロイされた後は、トポロジー・ファイルのフィールドの一部しか変更できないことです。このドキュメントでは、トポロジファイルの各セクションと各セクションの各フィールドを紹介します。

## ファイル構造 {#file-structure}

TiUPを使用したTiDB展開のトポロジ構成ファイルには、次のセクションが含まれる場合があります。

-   [グローバル](#global) ：クラスターのグローバル構成。一部の構成項目はデフォルト値を使用しており、インスタンスごとに個別に構成できます。
-   [監視](#monitored) ：監視サービスのConfiguration / コンフィグレーション、つまり、blackbox_exporterと`node_exporter` 。各マシンには、 `node_exporter`と`blackbox_exporter`が配備されています。
-   [server_configs](#server_configs) ：コンポーネントのグローバル構成。各コンポーネントを個別に構成できます。インスタンスに同じ名前の構成アイテムがある場合、インスタンスの構成アイテムが有効になります。
-   [pd_servers](#pd_servers) ：PDインスタンスの構成。この構成は、PDコンポーネントが展開されるマシンを指定します。
-   [tidb_servers](#tidb_servers) ：TiDBインスタンスの構成。この構成は、TiDBコンポーネントがデプロイされるマシンを指定します。
-   [tikv_servers](#tikv_servers) ：TiKVインスタンスの構成。この構成は、TiKVコンポーネントが展開されるマシンを指定します。
-   [tiflash_servers](#tiflash_servers) ：TiFlashインスタンスの構成。この構成は、TiFlashコンポーネントが展開されるマシンを指定します。
-   [pump_servers](#pump_servers) ： Pumpインスタンスの構成。この構成は、 Pumpコンポーネントがデプロイされるマシンを指定します。
-   [drainer_servers](#drainer_servers) ： Drainerインスタンスの構成。この構成は、 Drainerコンポーネントがデプロイされるマシンを指定します。
-   [cdc_servers](#cdc_servers) ：TiCDCインスタンスの構成。この構成は、TiCDCコンポーネントが展開されるマシンを指定します。
-   [tispark_masters](#tispark_masters) ：TiSparkマスターインスタンスの構成。この構成は、TiSparkマスターコンポーネントが展開されるマシンを指定します。 TiSparkマスターの1つのノードのみをデプロイできます。
-   [tispark_workers](#tispark_workers) ：TiSparkワーカーインスタンスの構成。この構成は、TiSparkワーカーコンポーネントが展開されるマシンを指定します。
-   [Monitoring_servers](#monitoring_servers) ：PrometheusとNGMonitoringがデプロイされるマシンを指定します。 TiUPは複数のPrometheusインスタンスのデプロイをサポートしていますが、最初のインスタンスのみが使用されます。
-   [grafana_servers](#grafana_servers) ：Grafanaインスタンスの構成。この構成は、Grafanaがデプロイされるマシンを指定します。
-   [alertmanager_servers](#alertmanager_servers) ：Alertmanagerインスタンスの構成。この構成は、Alertmanagerがデプロイされているマシンを指定します。

### <code>global</code> {#code-global-code}

`global`セクションはクラスターのグローバル構成に対応し、次のフィールドがあります。

-   `user` ：デプロイされたクラスタの開始に使用されたユーザー。デフォルト値は`"tidb"`です。 `<user>`フィールドで指定されたユーザーがターゲットマシンに存在しない場合、このユーザーは自動的に作成されます。

-   `group` ：ユーザーが属するユーザーグループ。ユーザーの作成時に指定します。値のデフォルトは`<user>`フィールドの値です。指定したグループが存在しない場合は、自動的に作成されます。

-   `ssh_port` ：操作のためにターゲットマシンに接続するSSHポートを指定します。デフォルト値は`22`です。

-   `enable_tls` ：クラスタのTLSを有効にするかどうかを指定します。 TLSを有効にした後、生成されたTLS証明書は、コンポーネント間またはクライアントとコンポーネント間の接続に使用する必要があります。**一度有効にすると、無効にすることはできません**。デフォルト値は`false`です。

-   `deploy_dir` ：各コンポーネントのデプロイメントディレクトリ。デフォルト値は`"deployed"`です。その適用規則は次のとおりです。

    -   絶対パス`deploy_dir`がインスタンスレベルで構成されている場合、実際のデプロイメントディレクトリはインスタンス用に構成されてい`deploy_dir` 。

    -   インスタンスごとに、 `deploy_dir`を構成しない場合、そのデフォルト値は相対パス`<component-name>-<component-port>`です。

    -   `global.deploy_dir`が絶対パスの場合、コンポーネントは`<global.deploy_dir>/<instance.deploy_dir>`ディレクトリにデプロイされます。

    -   `global.deploy_dir`が相対パスの場合、コンポーネントは`/home/<global.user>/<global.deploy_dir>/<instance.deploy_dir>`ディレクトリにデプロイされます。

-   `data_dir` ：データディレクトリ。デフォルト値： `"data"` 。その適用規則は次のとおりです。

    -   絶対パス`data_dir`がインスタンスレベルで構成されている場合、実際のデプロイメントディレクトリはインスタンス用に構成されてい`data_dir` 。

    -   インスタンスごとに、 `data_dir`を構成しない場合、デフォルト値は`<global.data_dir>`です。

    -   `data_dir`が相対パスの場合、コンポーネントデータは`<deploy_dir>/<data_dir>`に配置されます。 `<deploy_dir>`の計算規則については、 `deploy_dir`フィールドの適用規則を参照してください。

-   `log_dir` ：ログディレクトリ。デフォルト値： `"log"` 。その適用規則は次のとおりです。

    -   絶対パス`log_dir`がインスタンスレベルで構成されている場合、実際のログディレクトリはインスタンス用に構成された`log_dir`です。

    -   インスタンスごとに、 `log_dir`を構成しない場合、デフォルト値は`<global.log_dir>`です。

    -   `log_dir`が相対パスの場合、コンポーネントログは`<deploy_dir>/<log_dir>`に配置されます。 `<deploy_dir>`の計算規則については、 `deploy_dir`フィールドの適用規則を参照してください。

-   `os` ：ターゲットマシンのオペレーティングシステム。フィールドは、ターゲットマシンにプッシュされたコンポーネントに適応するオペレーティングシステムを制御します。デフォルト値は「linux」です。

-   `arch` ：ターゲットマシンのCPUアーキテクチャ。このフィールドは、ターゲットマシンにプッシュされるバイナリパッケージに適応するプラットフォームを制御します。サポートされている値は「amd64」と「arm64」です。デフォルト値は「amd64」です。

-   `resource_control` ：ランタイムリソース制御。このフィールドのすべての構成は、systemdのサービスファイルに書き込まれます。デフォルトでは制限はありません。制御できるリソースは次のとおりです。

    -   `memory_limit` ：最大実行時メモリを制限します。たとえば、「2G」は、最大2GBのメモリを使用できることを意味します。

    -   `cpu_quota` ：実行時の最大CPU使用率を制限します。たとえば、「200％」。

    -   `io_read_bandwidth_max` ：ディスク読み取りの最大I/O帯域幅を制限します。たとえば、 `"/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0 100M"` 。

    -   `io_write_bandwidth_max` ：ディスク書き込みの最大I/O帯域幅を制限します。たとえば、 `/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0 100M` 。

    -   `limit_core` ：コアダンプのサイズを制御します。

`global`の構成例は次のとおりです。

```yaml
global:
  user: "tidb"
  resource_control:
    memory_limit: "2G"
```

上記の構成では、 `tidb`ユーザーを使用してクラスタを開始します。同時に、各コンポーネントの実行時には、最大2GBのメモリに制限されます。

### <code>monitored</code> {#code-monitored-code}

`monitored`は、ターゲットマシンで監視サービスを構成するために使用されます： [`node_exporter`](https://github.com/prometheus/node_exporter)および[`blackbox_exporter`](https://github.com/prometheus/blackbox_exporter) 。次のフィールドが含まれています。

-   `node_exporter_port` ： `node_exporter`のサービスポート。デフォルト値は`9100`です。

-   `blackbox_exporter_port` ： `blackbox_exporter`のサービスポート。デフォルト値は`9115`です。

-   `deploy_dir` ：デプロイメントディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ディレクトリは`global`で構成された`deploy_dir`ディレクトリに従って生成されます。

-   `data_dir` ：データディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ディレクトリは`global`で構成された`data_dir`ディレクトリに従って生成されます。

-   `log_dir` ：ログディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ログは`global`で構成された`log_dir`ディレクトリに従って生成されます。

`monitored`の構成例は次のとおりです。

```yaml
monitored:
  node_exporter_port: 9100
  blackbox_exporter_port: 9115
```

上記の構成では、 `node_exporter`が`9100`ポートを使用し、 `blackbox_exporter`が`9115`ポートを使用することを指定しています。

### <code>server_configs</code> {#code-server-configs-code}

`server_configs`は、サービスを構成し、各コンポーネントの構成ファイルを生成するために使用されます。 `global`セクションと同様に、このセクションの構成は、インスタンス内の同じ名前の構成で上書きできます。 `server_configs`には、主に次のフィールドが含まれます。

-   `tidb` ：TiDBサービス関連の構成。完全な構成については、 [TiDB構成ファイル](/tidb-configuration-file.md)を参照してください。

-   `tikv` ：TiKVサービス関連の構成。完全な構成については、 [TiKV構成ファイル](/tikv-configuration-file.md)を参照してください。

-   `pd` ：PDサービス関連の構成。完全な構成については、 [PD構成ファイル](/pd-configuration-file.md)を参照してください。

-   `tiflash` ：TiFlashサービス関連の構成。完全な構成については、 [TiFlash構成ファイル](/tiflash/tiflash-configuration.md)を参照してください。

-   `tiflash_learner` ：各TiFlashノードには特別な組み込みTiKVがあります。この構成アイテムは、この特別なTiKVを構成するために使用されます。通常、この構成アイテムのコンテンツを変更することはお勧めしません。

-   `pump` ：Pumpサービス関連の構成。完全な構成については、 [Binlog構成ファイル](/tidb-binlog/tidb-binlog-configuration-file.md#pump)を参照してください。

-   `drainer` ：ドDrainerサービス関連の構成。完全な構成については、 [Binlog構成ファイル](/tidb-binlog/tidb-binlog-configuration-file.md#drainer)を参照してください。

-   `cdc` ：TiCDCサービス関連の構成。完全な構成については、 [TiCDCをデプロイ](/ticdc/deploy-ticdc.md)を参照してください。

`server_configs`の構成例は次のとおりです。

```yaml
server_configs:
  tidb:
    run-ddl: true
    lease: "45s"
    split-table: true
    token-limit: 1000
  tikv:
    log-level: "info"
    readpool.unified.min-thread-count: 1
```

上記の構成は、TiDBおよびTiKVのグローバル構成を指定します。

### <code>pd_servers</code> {#code-pd-servers-code}

`pd_servers`は、PDサービスが展開されるマシンを指定します。また、各マシンのサービス構成も指定します。 `pd_servers`は配列であり、配列の各要素には次のフィールドが含まれています。

-   `host` ：PDサービスが展開されるマシンを指定します。フィールド値はIPアドレスであり、必須です。

-   `listen_host` ：マシンに複数のIPアドレスがある場合、 `listen_host`はサービスのリスニングIPアドレスを指定します。デフォルト値は`0.0.0.0`です。

-   `ssh_port` ：操作のためにターゲットマシンに接続するSSHポートを指定します。指定されていない場合は、 `global`のセクションのうち`ssh_port`つが使用されます。

-   `name` ：PDインスタンスの名前を指定します。異なるインスタンスには一意の名前が必要です。そうしないと、インスタンスをデプロイできません。

-   `client_port` ：PDがクライアントへの接続に使用するポートを指定します。デフォルト値は`2379`です。

-   `peer_port` ：PD間の通信用ポートを指定します。デフォルト値は`2380`です。

-   `deploy_dir` ：デプロイメントディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ディレクトリは`global`で構成された`deploy_dir`ディレクトリに従って生成されます。

-   `data_dir` ：データディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ディレクトリは`global`で構成された`data_dir`ディレクトリに従って生成されます。

-   `log_dir` ：ログディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ログは`global`で構成された`log_dir`ディレクトリに従って生成されます。

-   `numa_node` ：NUMAポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲットマシンに[numactl](https://linux.die.net/man/8/numactl)がインストールされていることを確認する必要があります。このフィールドが指定されている場合、cpubindおよびmembindポリシーは[numactl](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などのNUMAノードのIDです。

-   `config` ：このフィールドの構成ルールは、 `server_configs`の`pd`構成ルールと同じです。このフィールドが構成されている場合、フィールドのコンテンツは`server_configs`の`pd`のコンテンツとマージされます（2つのフィールドが重複している場合、このフィールドのコンテンツが有効になります）。次に、構成ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `os` ： `host`で指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値です。

-   `arch` ： `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値です。

-   `resource_control` ：サービスのリソース制御。このフィールドが構成されている場合、フィールドのコンテンツは`global`の`resource_control`つのコンテンツとマージされます（2つのフィールドが重複している場合、このフィールドのコンテンツが有効になります）。次に、systemd構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の構成ルールは、 `global`の`resource_control`のコンテンツと同じです。

上記のフィールドの場合、展開後にこれらの構成済みフィールドを変更することはできません。

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

`pd_servers`の構成例は次のとおりです。

```yaml
pd_servers:
  - host: 10.0.1.11
    config:
      schedule.max-merge-region-size: 20
      schedule.max-merge-region-keys: 200000
  - host: 10.0.1.12
```

上記の構成は、PDが`10.0.1.11`と`10.0.1.12`に展開されることを指定し、 `10.0.1.11`のPDに対して特定の構成を作成します。

### <code>tidb_servers</code> {#code-tidb-servers-code}

`tidb_servers`は、TiDBサービスが展開されるマシンを指定します。また、各マシンのサービス構成も指定します。 `tidb_servers`は配列であり、配列の各要素には次のフィールドが含まれています。

-   `host` ：TiDBサービスが展開されるマシンを指定します。フィールド値はIPアドレスであり、必須です。

-   `listen_host` ：マシンに複数のIPアドレスがある場合、 `listen_host`はサービスのリスニングIPアドレスを指定します。デフォルト値は`0.0.0.0`です。

-   `ssh_port` ：操作のためにターゲットマシンに接続するSSHポートを指定します。指定されていない場合は、 `global`のセクションのうち`ssh_port`つが使用されます。

-   `port` ：MySQLクライアントへの接続を提供するために使用されるTiDBサービスのリスニングポート。デフォルト値は`4000`です。

-   `status_port` ：TiDBステータスサービスのリスニングポート。HTTPリクエストを介して外部からTiDBサービスのステータスを表示するために使用されます。デフォルト値は`10080`です。

-   `deploy_dir` ：デプロイメントディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ディレクトリは`global`で構成された`deploy_dir`ディレクトリに従って生成されます。

-   `log_dir` ：ログディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ログは`global`で構成された`log_dir`ディレクトリに従って生成されます。

-   `numa_node` ：NUMAポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲットマシンに[numactl](https://linux.die.net/man/8/numactl)がインストールされていることを確認する必要があります。このフィールドが指定されている場合、cpubindおよびmembindポリシーは[numactl](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などのNUMAノードのIDです。

-   `config` ：このフィールドの構成ルールは、 `server_configs`の`tidb`構成ルールと同じです。このフィールドが構成されている場合、フィールドのコンテンツは`server_configs`の`tidb`のコンテンツとマージされます（2つのフィールドが重複している場合、このフィールドのコンテンツが有効になります）。次に、構成ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `os` ： `host`で指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値です。

-   `arch` ： `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値です。

-   `resource_control` ：サービスのリソース制御。このフィールドが構成されている場合、フィールドのコンテンツは`global`の`resource_control`つのコンテンツとマージされます（2つのフィールドが重複している場合、このフィールドのコンテンツが有効になります）。次に、systemd構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の構成ルールは、 `global`の`resource_control`のコンテンツと同じです。

上記のフィールドの場合、展開後にこれらの構成済みフィールドを変更することはできません。

-   `host`
-   `listen_host`
-   `port`
-   `status_port`
-   `deploy_dir`
-   `log_dir`
-   `arch`
-   `os`

`tidb_servers`の構成例は次のとおりです。

```yaml
tidb_servers:
  - host: 10.0.1.14
    config:
      log.level: warn
      log.slow-query-file: tidb-slow-overwrited.log
  - host: 10.0.1.15
```

### <code>tikv_servers</code> {#code-tikv-servers-code}

`tikv_servers`は、TiKVサービスが展開されるマシンを指定します。また、各マシンのサービス構成も指定します。 `tikv_servers`は配列であり、配列の各要素には次のフィールドが含まれています。

-   `host` ：TiKVサービスが展開されるマシンを指定します。フィールド値はIPアドレスであり、必須です。

-   `listen_host` ：マシンに複数のIPアドレスがある場合、 `listen_host`はサービスのリスニングIPアドレスを指定します。デフォルト値は`0.0.0.0`です。

-   `ssh_port` ：操作のためにターゲットマシンに接続するSSHポートを指定します。指定されていない場合は、 `global`のセクションのうち`ssh_port`つが使用されます。

-   `port` ：TiKVサービスのリスニングポート。デフォルト値は`20160`です。

-   `status_port` ：TiKVステータスサービスのリスニングポート。デフォルト値は`20180`です。

-   `deploy_dir` ：デプロイメントディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ディレクトリは`global`で構成された`deploy_dir`ディレクトリに従って生成されます。

-   `data_dir` ：データディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ディレクトリは`global`で構成された`data_dir`ディレクトリに従って生成されます。

-   `log_dir` ：ログディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ログは`global`で構成された`log_dir`ディレクトリに従って生成されます。

-   `numa_node` ：NUMAポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲットマシンに[numactl](https://linux.die.net/man/8/numactl)がインストールされていることを確認する必要があります。このフィールドが指定されている場合、cpubindおよびmembindポリシーは[numactl](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などのNUMAノードのIDです。

-   `config` ：このフィールドの構成ルールは、 `server_configs`の`tikv`構成ルールと同じです。このフィールドが構成されている場合、フィールドのコンテンツは`server_configs`の`tikv`のコンテンツとマージされます（2つのフィールドが重複している場合、このフィールドのコンテンツが有効になります）。次に、構成ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `os` ： `host`で指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値です。

-   `arch` ： `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値です。

-   `resource_control` ：サービスのリソース制御。このフィールドが構成されている場合、フィールドのコンテンツは`global`の`resource_control`つのコンテンツとマージされます（2つのフィールドが重複している場合、このフィールドのコンテンツが有効になります）。次に、systemd構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の構成ルールは、 `global`の`resource_control`のコンテンツと同じです。

上記のフィールドの場合、展開後にこれらの構成済みフィールドを変更することはできません。

-   `host`
-   `listen_host`
-   `port`
-   `status_port`
-   `deploy_dir`
-   `data_dir`
-   `log_dir`
-   `arch`
-   `os`

`tikv_servers`の構成例は次のとおりです。

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

`tiflash_servers`は、TiFlashサービスが展開されるマシンを指定します。また、各マシンのサービス構成も指定します。このセクションは配列であり、配列の各要素には次のフィールドが含まれています。

-   `host` ：TiFlashサービスが展開されるマシンを指定します。フィールド値はIPアドレスであり、必須です。

-   `ssh_port` ：操作のためにターゲットマシンに接続するSSHポートを指定します。指定されていない場合は、 `global`のセクションのうち`ssh_port`つが使用されます。

-   `tcp_port` ：TiFlashTCPサービスのポート。デフォルト値は`9000`です。

-   `http_port` ：TiFlashHTTPサービスのポート。デフォルト値は`8123`です。

-   `flash_service_port` ：TiFlashがサービスを提供するためのポート。 TiDBは、このポートを介してTiFlashからデータを読み取ります。デフォルト値は`3930`です。

-   `metrics_port` ：メトリックデータを出力するために使用されるTiFlashのステータスポート。デフォルト値は`8234`です。

-   `flash_proxy_port` ：内蔵TiKVのポート。デフォルト値は`20170`です。

-   `flash_proxy_status_port` ：内蔵TiKVのステータスポート。デフォルト値は`20292`です。

-   `deploy_dir` ：デプロイメントディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ディレクトリは`global`で構成された`deploy_dir`ディレクトリに従って生成されます。

-   `data_dir` ：データディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ディレクトリは`global`で構成された`data_dir`ディレクトリに従って生成されます。 TiFlashは、コンマで区切られた複数の`data_dir`のディレクトリをサポートします。

-   `log_dir` ：ログディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ログは`global`で構成された`log_dir`ディレクトリに従って生成されます。

-   `tmp_path` ：TiFlash一時ファイルのストレージパス。デフォルト値は[ `path`または`storage.latest.dir`の最初のディレクトリ]+&quot;/tmp&quot;です。

-   `numa_node` ：NUMAポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲットマシンに[numactl](https://linux.die.net/man/8/numactl)がインストールされていることを確認する必要があります。このフィールドが指定されている場合、cpubindおよびmembindポリシーは[numactl](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などのNUMAノードのIDです。

-   `config` ：このフィールドの構成ルールは、 `server_configs`の`tiflash`構成ルールと同じです。このフィールドが構成されている場合、フィールドのコンテンツは`server_configs`の`tiflash`のコンテンツとマージされます（2つのフィールドが重複している場合、このフィールドのコンテンツが有効になります）。次に、構成ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `learner_config` ：各TiFlashノードには特別な組み込みTiKVがあります。この構成アイテムは、この特別なTiKVを構成するために使用されます。通常、この構成アイテムのコンテンツを変更することはお勧めしません。

-   `os` ： `host`で指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値です。

-   `arch` ： `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値です。

-   `resource_control` ：サービスのリソース制御。このフィールドが構成されている場合、フィールドのコンテンツは`global`の`resource_control`つのコンテンツとマージされます（2つのフィールドが重複している場合、このフィールドのコンテンツが有効になります）。次に、systemd構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の構成ルールは、 `global`の`resource_control`のコンテンツと同じです。

展開後、上記のフィールドでは、ディレクトリを`data_dir`にのみ追加できます。以下のフィールドについては、これらのフィールドを変更することはできません。

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

`tiflash_servers`の構成例は次のとおりです。

```yaml
tiflash_servers:
  - host: 10.0.1.21
  - host: 10.0.1.22
```

### <code>pump_servers</code> {#code-pump-servers-code}

`pump_servers`は、 BinlogのPumpサービスが展開されるマシンを指定します。また、各マシンのサービス構成も指定します。 `pump_servers`は配列であり、配列の各要素には次のフィールドが含まれています。

-   `host` ：Pumpサービスが展開されるマシンを指定します。フィールド値はIPアドレスであり、必須です。

-   `ssh_port` ：操作のためにターゲットマシンに接続するSSHポートを指定します。指定されていない場合は、 `global`のセクションのうち`ssh_port`つが使用されます。

-   `port` ：Pumpサービスのリスニングポート。デフォルト値は`8250`です。

-   `deploy_dir` ：デプロイメントディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ディレクトリは`global`で構成された`deploy_dir`ディレクトリに従って生成されます。

-   `data_dir` ：データディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ディレクトリは`global`で構成された`data_dir`ディレクトリに従って生成されます。

-   `log_dir` ：ログディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ログは`global`で構成された`log_dir`ディレクトリに従って生成されます。

-   `numa_node` ：NUMAポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲットマシンに[numactl](https://linux.die.net/man/8/numactl)がインストールされていることを確認する必要があります。このフィールドが指定されている場合、cpubindおよびmembindポリシーは[numactl](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などのNUMAノードのIDです。

-   `config` ：このフィールドの構成ルールは、 `server_configs`の`pump`構成ルールと同じです。このフィールドが構成されている場合、フィールドのコンテンツは`server_configs`の`pump`のコンテンツとマージされます（2つのフィールドが重複している場合、このフィールドのコンテンツが有効になります）。次に、構成ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `os` ： `host`で指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値です。

-   `arch` ： `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値です。

-   `resource_control` ：サービスのリソース制御。このフィールドが構成されている場合、フィールドのコンテンツは`global`の`resource_control`つのコンテンツとマージされます（2つのフィールドが重複している場合、このフィールドのコンテンツが有効になります）。次に、systemd構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の構成ルールは、 `global`の`resource_control`のコンテンツと同じです。

上記のフィールドの場合、展開後にこれらの構成済みフィールドを変更することはできません。

-   `host`
-   `port`
-   `deploy_dir`
-   `data_dir`
-   `log_dir`
-   `arch`
-   `os`

`pump_servers`の構成例は次のとおりです。

```yaml
pump_servers:
  - host: 10.0.1.21
    config:
      gc: 7
  - host: 10.0.1.22
```

### <code>drainer_servers</code> {#code-drainer-servers-code}

`drainer_servers`は、 BinlogDrainerが展開されるマシンを指定します。また、各マシンのサービス構成も指定します。 `drainer_servers`は配列です。各配列要素には、次のフィールドが含まれています。

-   `host` ： Drainerサービスがデプロイされるマシンを指定します。フィールド値はIPアドレスであり、必須です。

-   `ssh_port` ：操作のためにターゲットマシンに接続するSSHポートを指定します。指定されていない場合は、 `global`のセクションのうち`ssh_port`つが使用されます。

-   `port` ：Drainerサービスのリスニングポート。デフォルト値は`8249`です。

-   `deploy_dir` ：デプロイメントディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ディレクトリは`global`で構成された`deploy_dir`ディレクトリに従って生成されます。

-   `data_dir` ：データディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ディレクトリは`global`で構成された`data_dir`ディレクトリに従って生成されます。

-   `log_dir` ：ログディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ログは`global`で構成された`log_dir`ディレクトリに従って生成されます。

-   `commit_ts` （非推奨）： Drainerが起動すると、チェックポイントを読み取ります。 Drainerがチェックポイントを取得しない場合、Drainerはこのフィールドを最初の起動のレプリケーション時点として使用します。このフィールドのデフォルトは`-1`です（Drainerは常にPDからcommit_tsとして最新のタイムスタンプを取得します）。

-   `numa_node` ：NUMAポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲットマシンに[numactl](https://linux.die.net/man/8/numactl)がインストールされていることを確認する必要があります。このフィールドが指定されている場合、cpubindおよびmembindポリシーは[numactl](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などのNUMAノードのIDです。

-   `config` ：このフィールドの構成ルールは、 `server_configs`の`drainer`構成ルールと同じです。このフィールドが構成されている場合、フィールドのコンテンツは`server_configs`の`drainer`のコンテンツとマージされます（2つのフィールドが重複している場合、このフィールドのコンテンツが有効になります）。次に、構成ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `os` ： `host`で指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値です。

-   `arch` ： `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値です。

-   `resource_control` ：サービスのリソース制御。このフィールドが構成されている場合、フィールドのコンテンツは`global`の`resource_control`つのコンテンツとマージされます（2つのフィールドが重複している場合、このフィールドのコンテンツが有効になります）。次に、systemd構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の構成ルールは、 `global`の`resource_control`のコンテンツと同じです。

上記のフィールドの場合、展開後にこれらの構成済みフィールドを変更することはできません。

-   `host`
-   `port`
-   `deploy_dir`
-   `data_dir`
-   `log_dir`
-   `arch`
-   `os`

`commit_ts`フィールドは、TiUP v1.9.2以降非推奨になり、 Drainerの開始スクリプトには記録されません。それでもこのフィールドを使用する必要がある場合は、次の例を参照して`config`の`initial-commit-ts`フィールドを構成してください。

`drainer_servers`の構成例は次のとおりです。

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

`cdc_servers`は、TiCDCサービスが展開されるマシンを指定します。また、各マシンのサービス構成も指定します。 `cdc_servers`は配列です。各配列要素には、次のフィールドが含まれています。

-   `host` ：TiCDCサービスが展開されるマシンを指定します。フィールド値はIPアドレスであり、必須です。

-   `ssh_port` ：操作のためにターゲットマシンに接続するSSHポートを指定します。指定されていない場合は、 `global`のセクションのうち`ssh_port`つが使用されます。

-   `port` ：TiCDCサービスのリスニングポート。デフォルト値は`8300`です。

-   `deploy_dir` ：デプロイメントディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ディレクトリは`global`で構成された`deploy_dir`ディレクトリに従って生成されます。

-   `data_dir` ：データディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ディレクトリは`global`で構成された`data_dir`ディレクトリに従って生成されます。

-   `log_dir` ：ログディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ログは`global`で構成された`log_dir`ディレクトリに従って生成されます。

-   `gc-ttl` ：TiCDCによってPDで設定されたサービスレベルGCセーフポイントの存続時間（TTL）期間（秒単位）。デフォルト値は`86400` 、つまり24時間です。

-   `tz` ：TiCDCサービスが使用するタイムゾーン。 TiCDCは、タイムスタンプなどの時間データ型を内部で変換するとき、およびデータをダウンストリームに複製するときに、このタイムゾーンを使用します。デフォルト値は、プロセスが実行されるローカルタイムゾーンです。

-   `numa_node` ：NUMAポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲットマシンに[numactl](https://linux.die.net/man/8/numactl)がインストールされていることを確認する必要があります。このフィールドが指定されている場合、cpubindおよびmembindポリシーは[numactl](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などのNUMAノードのIDです。

-   `config` ：フィールドの内容は`server_configs`の`cdc`つの内容とマージされます（2つのフィールドが重なる場合、このフィールドの内容が有効になります）。次に、構成ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `os` ： `host`で指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値です。

-   `arch` ： `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値です。

-   `resource_control` ：サービスのリソース制御。このフィールドが構成されている場合、フィールドのコンテンツは`global`の`resource_control`つのコンテンツとマージされます（2つのフィールドが重複している場合、このフィールドのコンテンツが有効になります）。次に、systemd構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の構成ルールは、 `global`の`resource_control`のコンテンツと同じです。

上記のフィールドの場合、展開後にこれらの構成済みフィールドを変更することはできません。

-   `host`
-   `port`
-   `deploy_dir`
-   `data_dir`
-   `log_dir`
-   `arch`
-   `os`

`cdc_servers`の構成例は次のとおりです。

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

`tispark_masters`は、TiSparkのマスターノードが展開されるマシンを指定します。また、各マシンのサービス構成も指定します。 `tispark_masters`は配列です。各配列要素には、次のフィールドが含まれています。

-   `host` ：TiSparkマスターがデプロイされているマシンを指定します。フィールド値はIPアドレスであり、必須です。

-   `listen_host` ：マシンに複数のIPアドレスがある場合、 `listen_host`はサービスのリスニングIPアドレスを指定します。デフォルト値は`0.0.0.0`です。

-   `ssh_port` ：操作のためにターゲットマシンに接続するSSHポートを指定します。指定されていない場合は、 `global`のセクションのうち`ssh_port`つが使用されます。

-   `port` ：Sparkのリスニングポート。ノードの前の通信に使用されます。デフォルト値は`7077`です。

-   `web_port` ：Webサービスとタスクステータスを提供するSparkのWebポート。デフォルト値は`8080`です。

-   `deploy_dir` ：デプロイメントディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ディレクトリは`global`で構成された`deploy_dir`ディレクトリに従って生成されます。

-   `java_home` ：使用するJRE環境のパスを指定します。このパラメーターは、 `JAVA_HOME`のシステム環境変数に対応します。

-   `spark_config` ：TiSparkサービスを構成するように構成します。次に、構成ファイルが生成され、 `host`で指定されたマシンに送信されます。

-   `spark_env` ：Sparkの起動時に環境変数を設定します。

-   `os` ： `host`で指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値です。

-   `arch` ： `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値です。

上記のフィールドの場合、展開後にこれらの構成済みフィールドを変更することはできません。

-   `host`
-   `listen_host`
-   `port`
-   `web_port`
-   `deploy_dir`
-   `arch`
-   `os`

`tispark_masters`の構成例は次のとおりです。

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

`tispark_workers`は、TiSparkのワーカーノードが展開されるマシンを指定します。また、各マシンのサービス構成も指定します。 `tispark_workers`は配列です。各配列要素には、次のフィールドが含まれています。

-   `host` ：TiSparkワーカーがデプロイされるマシンを指定します。フィールド値はIPアドレスであり、必須です。

-   `listen_host` ：マシンに複数のIPアドレスがある場合、 `listen_host`はサービスのリスニングIPアドレスを指定します。デフォルト値は`0.0.0.0`です。

-   `ssh_port` ：操作のためにターゲットマシンに接続するSSHポートを指定します。指定されていない場合は、 `global`のセクションのうち`ssh_port`つが使用されます。

-   `port` ：Sparkのリスニングポート。ノードの前の通信に使用されます。デフォルト値は`7077`です。

-   `web_port` ：Webサービスとタスクステータスを提供するSparkのWebポート。デフォルト値は`8080`です。

-   `deploy_dir` ：デプロイメントディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ディレクトリは`global`で構成された`deploy_dir`ディレクトリに従って生成されます。

-   `java_home` ：使用するJRE環境が配置されているパスを指定します。このパラメーターは、 `JAVA_HOME`のシステム環境変数に対応します。

-   `os` ： `host`で指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値です。

-   `arch` ： `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値です。

上記のフィールドの場合、展開後にこれらの構成済みフィールドを変更することはできません。

-   `host`
-   `listen_host`
-   `port`
-   `web_port`
-   `deploy_dir`
-   `arch`
-   `os`

`tispark_workers`の構成例は次のとおりです。

```yaml
tispark_workers:
  - host: 10.0.1.22
  - host: 10.0.1.23
```

### <code>monitoring_servers</code> {#code-monitoring-servers-code}

`monitoring_servers`は、Prometheusサービスがデプロイされるマシンを指定します。また、各マシンのサービス構成も指定します。 `monitoring_servers`は配列です。各配列要素には、次のフィールドが含まれています。

-   `host` ：監視サービスが展開されているマシンを指定します。フィールド値はIPアドレスであり、必須です。

-   `ng_port` ：NGMonitoringに接続するSSHポートを指定します。 TiUP v1.7.0で導入されたこのフィールドは、TiDB5.3.0以降で[継続的なプロファイリング](/dashboard/dashboard-profiling.md)およびTop SQLをサポートします。

-   `ssh_port` ：操作のためにターゲットマシンに接続するSSHポートを指定します。指定されていない場合は、 `global`のセクションのうち`ssh_port`つが使用されます。

-   `port` ：Prometheusサービスのリスニングポート。デフォルト値は`9090`です。

-   `deploy_dir` ：デプロイメントディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ディレクトリは`global`で構成された`deploy_dir`ディレクトリに従って生成されます。

-   `data_dir` ：データディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ディレクトリは`global`で構成された`data_dir`ディレクトリに従って生成されます。

-   `log_dir` ：ログディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ログは`global`で構成された`log_dir`ディレクトリに従って生成されます。

-   `numa_node` ：NUMAポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲットマシンに[numactl](https://linux.die.net/man/8/numactl)がインストールされていることを確認する必要があります。このフィールドが指定されている場合、cpubindおよびmembindポリシーは[numactl](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などのNUMAノードのIDです。

-   `storage_retention` ：プロメテウスモニタリングデータの保持時間。デフォルト値は`"30d"`です。

-   `rule_dir` ：完全な`*.rules.yml`のファイルを含むローカルディレクトリを指定します。これらのファイルは、Prometheusのルールとして、クラスタ構成の初期化フェーズ中にターゲットマシンに転送されます。

-   `remote_config` ：リモートへのPrometheusデータの書き込み、またはリモートからのデータの読み取りをサポートします。このフィールドには2つの構成があります。
    -   `remote_write` ：Prometheusドキュメント[`&#x3C;remote_write>`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write)を参照してください。
    -   `remote_read` ：Prometheusドキュメント[`&#x3C;remote_read>`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_read)を参照してください。

-   `external_alertmanagers` ： `external_alertmanagers`フィールドが構成されている場合、Prometheusはクラスタの外部にあるAlertmanagerに構成動作を警告します。このフィールドは配列であり、各要素は外部Alertmanagerであり、 `host`つと`web_port`のフィールドで構成されています。

-   `os` ： `host`で指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値です。

-   `arch` ： `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値です。

-   `resource_control` ：サービスのリソース制御。このフィールドが構成されている場合、フィールドのコンテンツは`global`の`resource_control`つのコンテンツとマージされます（2つのフィールドが重複している場合、このフィールドのコンテンツが有効になります）。次に、systemd構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の構成ルールは、 `global`の`resource_control`のコンテンツと同じです。

上記のフィールドの場合、展開後にこれらの構成済みフィールドを変更することはできません。

-   `host`
-   `port`
-   `deploy_dir`
-   `data_dir`
-   `log_dir`
-   `arch`
-   `os`

`monitoring_servers`の構成例は次のとおりです。

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

`grafana_servers`は、Grafanaサービスがデプロイされるマシンを指定します。また、各マシンのサービス構成も指定します。 `grafana_servers`は配列です。各配列要素には、次のフィールドが含まれています。

-   `host` ：Grafanaサービスがデプロイされるマシンを指定します。フィールド値はIPアドレスであり、必須です。

-   `ssh_port` ：操作のためにターゲットマシンに接続するSSHポートを指定します。指定されていない場合は、 `global`のセクションのうち`ssh_port`つが使用されます。

-   `port` ：Grafanaサービスのリスニングポート。デフォルト値は`3000`です。

-   `deploy_dir` ：デプロイメントディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ディレクトリは`global`で構成された`deploy_dir`ディレクトリに従って生成されます。

-   `os` ： `host`で指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値です。

-   `arch` ： `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値です。

-   `username` ：Grafanaログインインターフェースのユーザー名。

-   `password` ：Grafanaに対応するパスワード。

-   `dashboard_dir` ：完全な`dashboard(*.json)`のファイルを含むローカルディレクトリを指定します。これらのファイルは、クラスタ構成の初期化フェーズ中に、Grafanaのダッシュボードとしてターゲットマシンに転送されます。

-   `resource_control` ：サービスのリソース制御。このフィールドが構成されている場合、フィールドのコンテンツは`global`の`resource_control`つのコンテンツとマージされます（2つのフィールドが重複している場合、このフィールドのコンテンツが有効になります）。次に、systemd構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の構成ルールは、 `global`の`resource_control`のコンテンツと同じです。

> **ノート：**
>
> `grafana_servers`の`dashboard_dir`フィールドが構成されている場合、 `tiup cluster rename`コマンドを実行してクラスタの名前を変更した後、次の操作を実行する必要があります。
>
> 1.  ローカルダッシュボードディレクトリ内の`*.json`ファイルについて、 `datasource`フィールドの値を新しいクラスタ名に更新します（ `datasource`はクラスタ名にちなんで名付けられているため）。
> 2.  `tiup cluster reload -R grafana`コマンドを実行します。

上記のフィールドの場合、展開後にこれらの構成済みフィールドを変更することはできません。

-   `host`
-   `port`
-   `deploy_dir`
-   `arch`
-   `os`

`grafana_servers`の構成例は次のとおりです。

```yaml
grafana_servers:
  - host: 10.0.1.11
    dashboard_dir: /local/dashboard/dir
```

### <code>alertmanager_servers</code> {#code-alertmanager-servers-code}

`alertmanager_servers`は、Alertmanagerサービスがデプロイされるマシンを指定します。また、各マシンのサービス構成も指定します。 `alertmanager_servers`は配列です。各配列要素には、次のフィールドが含まれています。

-   `host` ：Alertmanagerサービスがデプロイされるマシンを指定します。フィールド値はIPアドレスであり、必須です。

-   `ssh_port` ：操作のためにターゲットマシンに接続するSSHポートを指定します。指定されていない場合は、 `global`のセクションのうち`ssh_port`つが使用されます。

-   `web_port` ：AlertmanagerがWebサービスを提供するために使用するポートを指定します。デフォルト値は`9093`です。

-   `cluster_port` ：1つのAlertmangerと他のAlertmanager間の通信ポートを指定します。デフォルト値は`9094`です。

-   `deploy_dir` ：デプロイメントディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ディレクトリは`global`で構成された`deploy_dir`ディレクトリに従って生成されます。

-   `data_dir` ：データディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ディレクトリは`global`で構成された`data_dir`ディレクトリに従って生成されます。

-   `log_dir` ：ログディレクトリを指定します。相対ディレクトリとして指定または指定されていない場合、ログは`global`で構成された`log_dir`ディレクトリに従って生成されます。

-   `numa_node` ：NUMAポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲットマシンに[numactl](https://linux.die.net/man/8/numactl)がインストールされていることを確認する必要があります。このフィールドが指定されている場合、cpubindおよびmembindポリシーは[numactl](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などのNUMAノードのIDです。

-   `config_file` ：クラスタ構成の初期化段階でターゲットマシンに転送されるローカルファイルをAlertmanagerの構成として指定します。

-   `os` ： `host`で指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`の`os`値です。

-   `arch` ： `host`で指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`の`arch`値です。

-   `resource_control` ：サービスのリソース制御。このフィールドが構成されている場合、フィールドのコンテンツは`global`の`resource_control`つのコンテンツとマージされます（2つのフィールドが重複している場合、このフィールドのコンテンツが有効になります）。次に、systemd構成ファイルが生成され、 `host`で指定されたマシンに送信されます。 `resource_control`の構成ルールは、 `global`の`resource_control`のコンテンツと同じです。

上記のフィールドの場合、展開後にこれらの構成済みフィールドを変更することはできません。

-   `host`
-   `web_port`
-   `cluster_port`
-   `deploy_dir`
-   `data_dir`
-   `log_dir`
-   `arch`
-   `os`

`alertmanager_servers`の構成例は次のとおりです。

```yaml
alertmanager_servers:
  - host: 10.0.1.11
    config_file: /local/config/file
  - host: 10.0.1.12
    config_file: /local/config/file
```
