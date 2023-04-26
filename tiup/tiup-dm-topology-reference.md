---
title: Topology Configuration File for DM Cluster Deployment Using TiUP
---

# TiUPを使用した DMクラスタ展開用のトポロジコンフィグレーションファイル {#topology-configuration-file-for-dm-cluster-deployment-using-tiup}

TiDB Data Migration (DM) クラスターをデプロイまたはスケーリングするには、クラスター トポロジーを記述するトポロジー ファイル ( [サンプル](https://github.com/pingcap/tiup/blob/master/embed/examples/dm/topology.example.yaml) ) を提供する必要があります。

同様に、クラスタ トポロジを変更するには、トポロジ ファイルを変更する必要があります。違いは、クラスターがデプロイされた後は、トポロジー ファイル内のフィールドの一部しか変更できないことです。このドキュメントでは、トポロジ ファイルの各セクションと、各セクションの各フィールドについて説明します。

## ファイル構造 {#file-structure}

TiUPを使用した DM クラスター展開のトポロジ構成ファイルには、次のセクションが含まれる場合があります。

-   [グローバル](#global) : クラスターのグローバル構成。一部の構成項目はクラスターのデフォルト値を使用し、インスタンスごとに個別に構成できます。
-   [サーバー構成](#server_configs) : コンポーネントのグローバル構成。各コンポーネントを個別に構成できます。インスタンスに同じキーを持つ構成アイテムがある場合、インスタンスの構成アイテムが有効になります。
-   [master_servers](#master_servers) : DM-master インスタンスの構成。構成は、DMコンポーネントのマスター サービスがデプロイされるマシンを指定します。
-   [worker_servers](#worker_servers) : DM-worker インスタンスの構成。構成は、DMコンポーネントのワーカー サービスがデプロイされるマシンを指定します。
-   [監視サーバー](#monitoring_servers) : Prometheus インスタンスがデプロイされるマシンを指定します。 TiUP は複数の Prometheus インスタンスのデプロイをサポートしていますが、最初のインスタンスのみが使用されます。
-   [grafana_servers](#grafana_servers) : Grafana インスタンスの構成。構成は、Grafana インスタンスがデプロイされるマシンを指定します。
-   [alertmanager_servers](#alertmanager_servers) : Alertemanager インスタンスの構成。構成は、Alertmanager インスタンスがデプロイされるマシンを指定します。

### <code>global</code> {#code-global-code}

`global`セクションはクラスターのグローバル構成に対応し、次のフィールドがあります。

-   `user` : デプロイされたクラスターを開始するユーザー。デフォルト値は「tidb」です。 `<user>`フィールドで指定されたユーザーがターゲット マシンに存在しない場合、 TiUP は自動的にユーザーの作成を試みます。
-   `group` : ユーザーが自動作成されたときにユーザーが属するユーザーグループ。デフォルト値は`<user>`フィールドと同じです。指定したグループが存在しない場合は、自動的に作成されます。
-   `ssh_port` : 操作のためにターゲット マシンに接続するための SSH ポート。デフォルト値は「22」です。
-   `deploy_dir` : 各コンポーネントのデプロイメント ディレクトリ。デフォルト値は「デプロイ」です。構築規則は次のとおりです。
    -   絶対パス`deploy_dir`がインスタンス レベルで設定されている場合、実際のデプロイ ディレクトリはインスタンス用に設定された`deploy_dir`なります。
    -   インスタンスごとに、構成しない場合`deploy_dir` 、デフォルト値は相対パス`<component-name>-<component-port>`です。
    -   `global.deploy_dir`を絶対パスに設定すると、コンポーネントは`<global.deploy_dir>/<instance.deploy_dir>`ディレクトリにデプロイされます。
    -   `global.deploy_dir`が相対パスに設定されている場合、コンポーネントは`/home/<global.user>/<global.deploy_dir>/<instance.deploy_dir>`ディレクトリにデプロイされます。
-   `data_dir` : データ ディレクトリ。デフォルト値は「データ」です。構築ルールは以下の通りです。
    -   絶対パス`data_dir`がインスタンス レベルで設定されている場合、実際のデータ ディレクトリはインスタンス用に設定された`data_dir`なります。
    -   インスタンスごとに、 `data_dir`が構成されていない場合、デフォルト値は`<global.data_dir>`です。
    -   `data_dir`が相対パスに設定されている場合、コンポーネントデータは`<deploy_dir>/<data_dir>`に格納されます。 `<deploy_dir>`の構成規則については、 `deploy_dir`フィールドの構成規則を参照してください。
-   `log_dir` : データ ディレクトリ。デフォルト値は「ログ」です。構築ルールは以下の通りです。
    -   `log_dir`の絶対パスがインスタンス レベルで構成されている場合、実際のログ ディレクトリはインスタンス用に構成された`log_dir`なります。
    -   インスタンスごとに、ユーザーが`log_dir`構成していない場合、デフォルト値は`<global.log_dir>`です。
    -   `log_dir`が相対パスの場合、コンポーネントログは`<deploy_dir>/<log_dir>`に格納されます。 `<deploy_dir>`の構成規則については、 `deploy_dir`フィールドの構成規則を参照してください。
-   `os` : ターゲット マシンのオペレーティング システム。このフィールドは、ターゲット マシンにプッシュされたコンポーネントをどのオペレーティング システムに適応させるかを制御します。デフォルト値は「linux」です。
-   `arch` : ターゲット マシンの CPUアーキテクチャ。このフィールドは、ターゲット マシンにプッシュされるバイナリ パッケージに適応するプラットフォームを制御します。サポートされている値は「amd64」と「arm64」です。デフォルト値は「amd64」です。
-   `resource_control` : ランタイム リソース制御。このフィールドのすべての構成は、systemd のサービス ファイルに書き込まれます。デフォルトでは制限はありません。制御できるリソースは次のとおりです。
    -   `memory_limit` : 実行時の最大メモリを制限します。たとえば、「2G」は、最大 2 GB のメモリを使用できることを意味します。
    -   `cpu_quota` : 実行時の最大 CPU 使用率を制限します。たとえば、「200%」です。
    -   `io_read_bandwidth_max` : ディスク読み取りの最大 I/O 帯域幅を制限します。たとえば、 `"/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0:0 100M"`です。
    -   `io_write_bandwidth_max` : ディスク書き込みの最大 I/O 帯域幅を制限します。たとえば、 `"/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0:0 100M"`です。
    -   `limit_core` : コア ダンプのサイズを制御します。

`global`構成例:

```yaml
global:
  user: "tidb"
  resource_control:
    memory_limit: "2G"
```

この例の構成では、クラスターの開始に`tidb`人のユーザーが使用されること、および各コンポーネントの実行時のメモリが最大 2 GB に制限されることが指定されています。

### <code>server_configs</code> {#code-server-configs-code}

`server_configs`は、サービスを構成し、各コンポーネントの構成ファイルを生成するために使用されます。 `global`セクションと同様に、 `server_configs`セクションの構成は、インスタンス内の同じキーを持つ構成によって上書きできます。 `server_configs`は、主に次のフィールドが含まれます。

-   `master` : DM-master サービスに関連する構成。サポートされているすべての構成アイテムについては、 [DMマスターコンフィグレーションファイル](/dm/dm-master-configuration-file.md)を参照してください。
-   `worker` : DM-worker サービスに関連する構成。サポートされているすべての構成項目については、 [DM-workerコンフィグレーションファイル](/dm/dm-worker-configuration-file.md)を参照してください。

`server_configs`構成例は次のとおりです。

```yaml
server_configs:
  master:
    log-level: info
    rpc-timeout: "30s"
    rpc-rate-limit: 10.0
    rpc-rate-burst: 40
  worker:
    log-level: info
```

## <code>master_servers</code> {#code-master-servers-code}

`master_servers` 、DMコンポーネントのマスター ノードがデプロイされるマシンを指定します。各マシンでサービス構成を指定することもできます。 `master_servers`は配列です。各配列要素には、次のフィールドが含まれます。

-   `host` : デプロイ先のマシンを指定します。フィールド値は IP アドレスで、必須です。
-   `ssh_port` : 操作のためにターゲット マシンに接続するための SSH ポートを指定します。フィールドが指定されていない場合は、 `global`セクションの`ssh_port`が使用されます。
-   `name` : DM マスター インスタンスの名前を指定します。名前はインスタンスごとに一意である必要があります。そうしないと、クラスターをデプロイできません。
-   `port` : DM-master がサービスを提供するポートを指定します。デフォルト値は「8261」です。
-   `peer_port` : DM マスター間の通信用のポートを指定します。デフォルト値は「8291」です。
-   `deploy_dir` : デプロイメント ディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、展開ディレクトリは`global`セクションの`deploy_dir`構成に従って生成されます。
-   `data_dir` : データ ディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、データ ディレクトリは`global`セクションの`data_dir`構成に従って生成されます。
-   `log_dir` : ログ ディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、ログ ディレクトリは`global`セクションの`log_dir`構成に従って生成されます。
-   `numa_node` : NUMA ポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲット マシンに[numactl](https://linux.die.net/man/8/numactl)がインストールされていることを確認する必要があります。このフィールドが指定されている場合、 cpubind および membind ポリシーは[numactl](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などの NUMA ノードの ID です。
-   `config` : このフィールドの構成規則は、 `server_configs`セクションの`master`と同じです。 `config`を指定すると、 `config`の構成が`server_configs`の`master`の構成とマージされ (2 つのフィールドが重複する場合は、このフィールドの構成が有効になります)、構成ファイルが生成され、指定されたマシンに配布されます。 `host`フィールド。
-   `os` : `host`フィールドで指定されたマシンのオペレーティング システム。フィールドが指定されていない場合、デフォルト値は`global`セクションで設定された`os`値です。
-   `arch` : `host`フィールドで指定されたマシンのアーキテクチャ。フィールドが指定されていない場合、デフォルト値は`global`セクションで設定された`arch`値です。
-   `resource_control` : このサービスのリソース制御。このフィールドを指定すると、このフィールドの設定が`global`セクションの`resource_control`の設定とマージされ (2 つのフィールドが重複する場合は、このフィールドの設定が有効になります)、systemd の設定ファイルが生成され、配布されます。 `host`フィールドで指定されたマシンに。このフィールドの構成ルールは、 `global`セクションの`resource_control`と同じです。
-   `v1_source_path` : v1.0.x からアップグレードする場合、V1 ソースの構成ファイルが置かれているディレクトリをこのフィールドに指定できます。

`master_servers`セクションでは、デプロイの完了後に次のフィールドを変更できません。

-   `host`
-   `name`
-   `port`
-   `peer_port`
-   `deploy_dir`
-   `data_dir`
-   `log_dir`
-   `arch`
-   `os`
-   `v1_source_path`

`master_servers`構成例は次のとおりです。

```yaml
master_servers:
  - host: 10.0.1.11
    name: master1
    ssh_port: 22
    port: 8261
    peer_port: 8291
    deploy_dir: "/dm-deploy/dm-master-8261"
    data_dir: "/dm-data/dm-master-8261"
    log_dir: "/dm-deploy/dm-master-8261/log"
    numa_node: "0,1"
    # The following configs are used to overwrite the `server_configs.master` values.
    config:
      log-level: info
      rpc-timeout: "30s"
      rpc-rate-limit: 10.0
      rpc-rate-burst: 40
  - host: 10.0.1.18
    name: master2
  - host: 10.0.1.19
    name: master3
```

## <code>worker_servers</code> {#code-worker-servers-code}

`worker_servers` 、DMコンポーネントのマスター ノードがデプロイされるマシンを指定します。各マシンでサービス構成を指定することもできます。 `worker_servers`は配列です。各配列要素には、次のフィールドが含まれます。

-   `host` : デプロイ先のマシンを指定します。フィールド値は IP アドレスで、必須です。
-   `ssh_port` : 操作のためにターゲット マシンに接続するための SSH ポートを指定します。フィールドが指定されていない場合は、 `global`セクションの`ssh_port`が使用されます。
-   `name` : DM-worker インスタンスの名前を指定します。名前はインスタンスごとに一意である必要があります。そうしないと、クラスターをデプロイできません。
-   `port` : DM-worker がサービスを提供するポートを指定します。デフォルト値は「8262」です。
-   `deploy_dir` : デプロイメント ディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、展開ディレクトリは`global`セクションの`deploy_dir`構成に従って生成されます。
-   `data_dir` : データ ディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、データ ディレクトリは`global`セクションの`data_dir`構成に従って生成されます。
-   `log_dir` : ログ ディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、ログ ディレクトリは`global`セクションの`log_dir`構成に従って生成されます。
-   `numa_node` : NUMA ポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲット マシンに[numactl](https://linux.die.net/man/8/numactl)がインストールされていることを確認する必要があります。このフィールドが指定されている場合、 cpubind および membind ポリシーは[numactl](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などの NUMA ノードの ID です。
-   `config` : このフィールドの構成規則は、 `server_configs`セクションの`worker`と同じです。 `config`を指定すると、 `config`の構成が`server_configs`の`worker`の構成とマージされ (2 つのフィールドが重複する場合は、このフィールドの構成が有効になります)、構成ファイルが生成され、指定されたマシンに配布されます。 `host`フィールド。
-   `os` : `host`フィールドで指定されたマシンのオペレーティング システム。フィールドが指定されていない場合、デフォルト値は`global`セクションで設定された`os`値です。
-   `arch` : `host`フィールドで指定されたマシンのアーキテクチャ。フィールドが指定されていない場合、デフォルト値は`global`セクションで設定された`arch`値です。
-   `resource_control` : このサービスのリソース制御。このフィールドを指定すると、このフィールドの設定が`global`セクションの`resource_control`の設定とマージされ (2 つのフィールドが重複する場合は、このフィールドの設定が有効になります)、systemd の設定ファイルが生成され、配布されます。 `host`フィールドで指定されたマシンに。このフィールドの構成ルールは、 `global`セクションの`resource_control`と同じです。

`worker_servers`セクションでは、デプロイの完了後に次のフィールドを変更できません。

-   `host`
-   `name`
-   `port`
-   `deploy_dir`
-   `data_dir`
-   `log_dir`
-   `arch`
-   `os`

`worker_servers`構成例は次のとおりです。

```yaml
worker_servers:
  - host: 10.0.1.12
    ssh_port: 22
    port: 8262
    deploy_dir: "/dm-deploy/dm-worker-8262"
    log_dir: "/dm-deploy/dm-worker-8262/log"
    numa_node: "0,1"
    # config is used to overwrite the `server_configs.worker` values
    config:
      log-level: info
  - host: 10.0.1.19
```

### <code>monitoring_servers</code> {#code-monitoring-servers-code}

`monitoring_servers` Prometheus サービスがデプロイされるマシンを指定します。マシンでサービス構成を指定することもできます。 `monitoring_servers`は配列です。各配列要素には、次のフィールドが含まれます。

-   `host` : デプロイ先のマシンを指定します。フィールド値は IP アドレスで、必須です。
-   `ssh_port` : 操作のためにターゲット マシンに接続するための SSH ポートを指定します。フィールドが指定されていない場合は、 `global`セクションの`ssh_port`が使用されます。
-   `port` : Prometheus がサービスを提供するポートを指定します。デフォルト値は「9090」です。
-   `deploy_dir` : デプロイメント ディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、展開ディレクトリは`global`セクションの`deploy_dir`構成に従って生成されます。
-   `data_dir` : データ ディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、データ ディレクトリは`global`セクションの`data_dir`構成に従って生成されます。
-   `log_dir` : ログ ディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、ログ ディレクトリは`global`セクションの`log_dir`構成に従って生成されます。
-   `numa_node` : NUMA ポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲット マシンに[numactl](https://linux.die.net/man/8/numactl)がインストールされていることを確認する必要があります。このフィールドが指定されている場合、 cpubind および membind ポリシーは[numactl](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などの NUMA ノードの ID です。
-   `storage_retention` : Prometheus モニタリング データの保存期間を指定します。デフォルト値は「15d」です。
-   `rule_dir` : 完全な`*.rules.yml`のファイルが配置されているローカル ディレクトリを指定します。指定されたディレクトリ内のファイルは、クラスター構成の初期化フェーズ中に Prometheus ルールとしてターゲット マシンに送信されます。
-   `remote_config` : リモートへの Prometheus データの書き込み、またはリモートからのデータの読み取りをサポートします。このフィールドには 2 つの構成があります。
    -   `remote_write` : Prometheus ドキュメント[`&#x3C;remote_write>`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write)を参照してください。
    -   `remote_read` : Prometheus ドキュメント[`&#x3C;remote_read>`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_read)を参照してください。
-   `external_alertmanagers` : `external_alertmanagers`フィールドが構成されている場合、Prometheus は構成動作をクラスター外の Alertmanager にアラートします。このフィールドは配列であり、その各要素は外部 Alertmanager であり、 `host`および`web_port`フィールドで構成されています。
-   `os` : `host`フィールドで指定されたマシンのオペレーティング システム。フィールドが指定されていない場合、デフォルト値は`global`セクションで設定された`os`値です。
-   `arch` : `host`フィールドで指定されたマシンのアーキテクチャ。フィールドが指定されていない場合、デフォルト値は`global`セクションで設定された`arch`値です。
-   `resource_control` : このサービスのリソース制御。このフィールドを指定すると、このフィールドの設定が`global`セクションの`resource_control`の設定とマージされ (2 つのフィールドが重複する場合は、このフィールドの設定が有効になります)、systemd の設定ファイルが生成され、配布されます。 `host`フィールドで指定されたマシンに。このフィールドの構成ルールは、 `global`セクションの`resource_control`と同じです。

`monitoring_servers`セクションでは、デプロイの完了後に次のフィールドを変更できません。

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
      - url: http://127.0.0.1:8003/read\
      external_alertmanagers:
      - host: 10.1.1.1
      web_port: 9093
      - host: 10.1.1.2
      web_port: 9094
```

### <code>grafana_servers</code> {#code-grafana-servers-code}

`grafana_servers` 、Grafana サービスがデプロイされるマシンを指定します。マシンでサービス構成を指定することもできます。 `grafana_servers`は配列です。各配列要素には、次のフィールドが含まれます。

-   `host` : デプロイ先のマシンを指定します。フィールド値は IP アドレスで、必須です。
-   `ssh_port` : 操作のためにターゲット マシンに接続するための SSH ポートを指定します。フィールドが指定されていない場合は、 `global`セクションの`ssh_port`が使用されます。
-   `port` : Grafana がサービスを提供するポートを指定します。デフォルト値は「3000」です。
-   `deploy_dir` : デプロイメント ディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、展開ディレクトリは`global`セクションの`deploy_dir`構成に従って生成されます。
-   `os` : `host`フィールドで指定されたマシンのオペレーティング システム。フィールドが指定されていない場合、デフォルト値は`global`セクションで設定された`os`値です。
-   `arch` : `host`フィールドで指定されたマシンのアーキテクチャ。フィールドが指定されていない場合、デフォルト値は`global`セクションで設定された`arch`値です。
-   `username` : Grafana ログイン画面のユーザー名を指定します。
-   `password` : Grafana の対応するパスワードを指定します。
-   `dashboard_dir` : 完全な`dashboard(*.json)`のファイルが配置されているローカル ディレクトリを指定します。指定したディレクトリ内のファイルは、クラスター構成の初期化フェーズ中に Grafana ダッシュボードとしてターゲット マシンに送信されます。
-   `resource_control` : このサービスのリソース制御。このフィールドを指定すると、このフィールドの設定が`global`セクションの`resource_control`の設定とマージされ (2 つのフィールドが重複する場合は、このフィールドの設定が有効になります)、systemd の設定ファイルが生成され、配布されます。 `host`フィールドで指定されたマシンに。このフィールドの構成ルールは、 `global`セクションの`resource_control`と同じです。

> **ノート：**
>
> `grafana_servers`の`dashboard_dir`フィールドが構成されている場合、 `tiup cluster rename`コマンドを実行してクラスターの名前を変更した後、次の操作を実行する必要があります。
>
> 1.  ローカル`dashboards`ディレクトリで、 `datasource`フィールドの値を新しいクラスター名に更新します ( `datasource`はクラスター名にちなんで命名されます)。
> 2.  `tiup cluster reload -R grafana`コマンドを実行します。

`grafana_servers`では、デプロイの完了後に次のフィールドを変更できません。

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

`alertmanager_servers` Alertmanager サービスがデプロイされるマシンを指定します。各マシンでサービス構成を指定することもできます。 `alertmanager_servers`は配列です。各配列要素には、次のフィールドが含まれます。

-   `host` : デプロイ先のマシンを指定します。フィールド値は IP アドレスで、必須です。
-   `ssh_port` : 操作のためにターゲット マシンに接続するための SSH ポートを指定します。フィールドが指定されていない場合は、 `global`セクションの`ssh_port`が使用されます。
-   `web_port` : Alertmanager が Web サービスを提供するポートを指定します。デフォルト値は「9093」です。
-   `cluster_port` : Alertmanager と他の Alertmanager 間の通信ポートを指定します。デフォルト値は「9094」です。
-   `deploy_dir` : デプロイメント ディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、展開ディレクトリは`global`セクションの`deploy_dir`構成に従って生成されます。
-   `data_dir` : データ ディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、データ ディレクトリは`global`セクションの`data_dir`構成に従って生成されます。
-   `log_dir` : ログ ディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、ログ ディレクトリは`global`セクションの`log_dir`構成に従って生成されます。
-   `numa_node` : NUMA ポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲット マシンに[numactl](https://linux.die.net/man/8/numactl)がインストールされていることを確認する必要があります。このフィールドが指定されている場合、 cpubind および membind ポリシーは[numactl](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などの NUMA ノードの ID です。
-   `config_file` : ローカル ファイルを指定します。指定したファイルは、クラスター構成の初期化フェーズ中に、Alertmanager の構成としてターゲット マシンに送信されます。
-   `os` : `host`フィールドで指定されたマシンのオペレーティング システム。フィールドが指定されていない場合、デフォルト値は`global`セクションで設定された`os`値です。
-   `arch` : `host`フィールドで指定されたマシンのアーキテクチャ。フィールドが指定されていない場合、デフォルト値は`global`セクションで設定された`arch`値です。
-   `resource_control` : このサービスのリソース制御。このフィールドを指定すると、このフィールドの設定が`global`セクションの`resource_control`の設定とマージされ (2 つのフィールドが重複する場合は、このフィールドの設定が有効になります)、systemd の設定ファイルが生成され、配布されます。 `host`フィールドで指定されたマシンに。このフィールドの構成ルールは、 `global`セクションの`resource_control`と同じです。

`alertmanager_servers`では、デプロイの完了後に次のフィールドを変更できません。

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
