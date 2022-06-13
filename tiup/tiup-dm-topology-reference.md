---
title: Topology Configuration File for DM Cluster Deployment Using TiUP
---

# TiUPを使用したDMクラスター展開用のトポロジーConfiguration / コンフィグレーションファイル {#topology-configuration-file-for-dm-cluster-deployment-using-tiup}

TiDBデータ移行（DM）クラスタを展開またはスケーリングするには、クラスタトポロジを記述するトポロジファイル（ [サンプル](https://github.com/pingcap/tiup/blob/master/embed/examples/dm/topology.example.yaml) ）を提供する必要があります。

同様に、クラスタトポロジを変更するには、トポロジファイルを変更する必要があります。違いは、クラスタがデプロイされた後は、トポロジー・ファイルのフィールドの一部しか変更できないことです。このドキュメントでは、トポロジファイルの各セクションと各セクションの各フィールドを紹介します。

## ファイル構造 {#file-structure}

TiUPを使用したDMクラスタ展開のトポロジ構成ファイルには、次のセクションが含まれる場合があります。

-   [グローバル](#global) ：クラスターのグローバル構成。一部の構成アイテムはクラスタのデフォルト値を使用し、インスタンスごとに個別に構成できます。
-   [server_configs](#server_configs) ：コンポーネントのグローバル構成。各コンポーネントを個別に構成できます。インスタンスに同じキーの構成アイテムがある場合、インスタンスの構成アイテムが有効になります。
-   [master_servers](#master_servers) ：DMマスターインスタンスの構成。構成は、DMコンポーネントのマスターサービスが展開されるマシンを指定します。
-   [worker_servers](#worker_servers) ：DM-workerインスタンスの構成。構成は、DMコンポーネントのワーカーサービスがデプロイされるマシンを指定します。
-   [Monitoring_servers](#monitoring_servers) ：Prometheusインスタンスがデプロイされるマシンを指定します。 TiUPは複数のPrometheusインスタンスのデプロイをサポートしていますが、最初のインスタンスのみが使用されます。
-   [grafana_servers](#grafana_servers) ：Grafanaインスタンスの構成。構成は、Grafanaインスタンスがデプロイされるマシンを指定します。
-   [alertmanager_servers](#alertmanager_servers) ：Alertemanagerインスタンスの構成。構成は、Alertmanagerインスタンスがデプロイされるマシンを指定します。

### <code>global</code> {#code-global-code}

`global`セクションは、クラスターのグローバル構成に対応し、次のフィールドがあります。

-   `user` ：デプロイされたクラスタを開始するユーザー。デフォルト値は「tidb」です。 `<user>`フィールドで指定されたユーザーがターゲットマシンに存在しない場合、TiUPは自動的にユーザーの作成を試みます。
-   `group` ：ユーザーが自動的に作成されるときにユーザーが属するユーザーグループ。デフォルト値は`<user>`フィールドと同じです。指定したグループが存在しない場合は、自動的に作成されます。
-   `ssh_port` ：操作のためにターゲットマシンに接続するためのSSHポート。デフォルト値は「22」です。
-   `deploy_dir` ：各コンポーネントのデプロイメントディレクトリ。デフォルト値は「deploy」です。構築ルールは次のとおりです。
    -   絶対パス`deploy_dir`がインスタンスレベルで構成されている場合、実際のデプロイメントディレクトリはインスタンス用に構成された`deploy_dir`です。
    -   インスタンスごとに、 `deploy_dir`を構成しない場合、デフォルト値は相対パス`<component-name>-<component-port>`です。
    -   `global.deploy_dir`が絶対パスに設定されている場合、コンポーネントは`<global.deploy_dir>/<instance.deploy_dir>`ディレクトリにデプロイされます。
    -   `global.deploy_dir`が相対パスに設定されている場合、コンポーネントは`/home/<global.user>/<global.deploy_dir>/<instance.deploy_dir>`ディレクトリにデプロイされます。
-   `data_dir` ：データディレクトリ。デフォルト値は「data」です。構成規則は次のとおりです。
    -   絶対パス`data_dir`がインスタンスレベルで構成されている場合、実際のデータディレクトリはインスタンス用に構成された`data_dir`です。
    -   インスタンスごとに、 `data_dir`が構成されていない場合、デフォルト値は`<global.data_dir>`です。
    -   `data_dir`が相対パスに設定されている場合、コンポーネントデータは`<deploy_dir>/<data_dir>`に格納されます。 `<deploy_dir>`の構築規則については、 `deploy_dir`フィールドの構築規則を参照してください。
-   `log_dir` ：データディレクトリ。デフォルト値は「log」です。構成規則は次のとおりです。
    -   絶対パス`log_dir`がインスタンスレベルで構成されている場合、実際のログディレクトリはインスタンス用に構成された`log_dir`です。
    -   インスタンスごとに、ユーザーが`log_dir`を構成していない場合、デフォルト値は`<global.log_dir>`です。
    -   `log_dir`が相対パスの場合、コンポーネントログは`<deploy_dir>/<log_dir>`に保存されます。 `<deploy_dir>`の構築規則については、 `deploy_dir`フィールドの構築規則を参照してください。
-   `os` ：ターゲットマシンのオペレーティングシステム。フィールドは、ターゲットマシンにプッシュされたコンポーネントに適応するオペレーティングシステムを制御します。デフォルト値は「linux」です。
-   `arch` ：ターゲットマシンのCPUアーキテクチャ。このフィールドは、ターゲットマシンにプッシュされるバイナリパッケージに適応するプラットフォームを制御します。サポートされている値は「amd64」と「arm64」です。デフォルト値は「amd64」です。
-   `resource_control` ：ランタイムリソース制御。このフィールドのすべての構成は、systemdのサービスファイルに書き込まれます。デフォルトでは制限はありません。制御できるリソースは次のとおりです。
    -   `memory_limit` ：実行時の最大メモリを制限します。たとえば、「2G」は、最大2GBのメモリを使用できることを意味します。
    -   `cpu_quota` ：実行時の最大CPU使用率を制限します。たとえば、「200％」。
    -   `io_read_bandwidth_max` ：ディスク読み取りの最大I/O帯域幅を制限します。たとえば、 `"/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0:0 100M"` 。
    -   `io_write_bandwidth_max` ：ディスク書き込みの最大I/O帯域幅を制限します。たとえば、 `"/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0:0 100M"` 。
    -   `limit_core` ：コアダンプのサイズを制御します。

`global`の構成例：

```yaml
global:
  user: "tidb"
  resource_control:
    memory_limit: "2G"
```

この例では、構成では、 `tidb`人のユーザーを使用してクラスタを開始し、各コンポーネントの実行時に最大2GBのメモリーに制限するように指定しています。

### <code>server_configs</code> {#code-server-configs-code}

`server_configs`は、サービスを構成し、各コンポーネントの構成ファイルを生成するために使用されます。 `global`セクションと同様に、 `server_configs`セクションの構成は、インスタンス内の同じキーを持つ構成で上書きできます。 `server_configs`には、主に次のフィールドが含まれています。

-   `master` ：DMマスターサービスに関連する構成。サポートされているすべての構成項目については、 [DMマスターConfiguration / コンフィグレーションファイル](/dm/dm-master-configuration-file.md)を参照してください。
-   `worker` ：DM-workerサービスに関連する構成。サポートされているすべての構成項目については、 [DM-workerConfiguration / コンフィグレーションファイル](/dm/dm-worker-configuration-file.md)を参照してください。

`server_configs`の構成例は次のとおりです。

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

`master_servers`は、DMコンポーネントのマスターノードが展開されるマシンを指定します。各マシンのサービス構成を指定することもできます。 `master_servers`は配列です。各配列要素には、次のフィールドが含まれています。

-   `host` ：デプロイ先のマシンを指定します。フィールド値はIPアドレスであり、必須です。
-   `ssh_port` ：操作のためにターゲットマシンに接続するSSHポートを指定します。フィールドが指定されていない場合、 `global`セクションの`ssh_port`が使用されます。
-   `name` ：DMマスターインスタンスの名前を指定します。名前は、インスタンスごとに一意である必要があります。そうしないと、クラスタをデプロイできません。
-   `port` ：DMマスターがサービスを提供するポートを指定します。デフォルト値は「8261」です。
-   `peer_port` ：DMマスター間の通信用のポートを指定します。デフォルト値は「8291」です。
-   `deploy_dir` ：デプロイメントディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、デプロイメントディレクトリは`global`セクションの`deploy_dir`構成に従って生成されます。
-   `data_dir` ：データディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、データディレクトリは`global`セクションの`data_dir`構成に従って生成されます。
-   `log_dir` ：ログディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、ログディレクトリは`global`セクションの`log_dir`構成に従って生成されます。
-   `numa_node` ：NUMAポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲットマシンに[numactl](https://linux.die.net/man/8/numactl)がインストールされていることを確認する必要があります。このフィールドが指定されている場合、cpubindおよびmembindポリシーは[numactl](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などのNUMAノードのIDです。
-   `config` ：このフィールドの構成規則は、 `server_configs`セクションの`master`の構成規則と同じです。 `config`が指定されている場合、 `config`の構成は`server_configs`の`master`の構成とマージされ（2つのフィールドが重複している場合、このフィールドの構成が有効になります）、構成ファイルが生成され、で指定されたマシンに配布されます。 `host`フィールド。
-   `os` ： `host`フィールドで指定されたマシンのオペレーティングシステム。フィールドが指定されていない場合、デフォルト値は`global`セクションで構成された`os`値です。
-   `arch` ： `host`フィールドで指定されたマシンのアーキテクチャ。フィールドが指定されていない場合、デフォルト値は`global`セクションで構成された`arch`値です。
-   `resource_control` ：このサービスのリソース制御。このフィールドが指定されている場合、このフィールドの構成は`global`セクションの`resource_control`の構成とマージされ（2つのフィールドが重複している場合、このフィールドの構成が有効になります）、systemdの構成ファイルが生成および配布されます。 `host`フィールドで指定されたマシンに。このフィールドの構成ルールは、 `global`セクションの`resource_control`の構成ルールと同じです。
-   `v1_source_path` ：v1.0.xからアップグレードする場合、このフィールドでV1ソースの構成ファイルが配置されているディレクトリを指定できます。

`master_servers`セクションでは、展開の完了後に次のフィールドを変更することはできません。

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

`master_servers`の構成例は次のとおりです。

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

`worker_servers`は、DMコンポーネントのマスターノードが展開されるマシンを指定します。各マシンのサービス構成を指定することもできます。 `worker_servers`は配列です。各配列要素には、次のフィールドが含まれています。

-   `host` ：デプロイ先のマシンを指定します。フィールド値はIPアドレスであり、必須です。
-   `ssh_port` ：操作のためにターゲットマシンに接続するSSHポートを指定します。フィールドが指定されていない場合、 `global`セクションの`ssh_port`が使用されます。
-   `name` ：DM-workerインスタンスの名前を指定します。名前は、インスタンスごとに一意である必要があります。そうしないと、クラスタをデプロイできません。
-   `port` ：DM-workerがサービスを提供するポートを指定します。デフォルト値は「8262」です。
-   `deploy_dir` ：デプロイメントディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、デプロイメントディレクトリは`global`セクションの`deploy_dir`構成に従って生成されます。
-   `data_dir` ：データディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、データディレクトリは`global`セクションの`data_dir`構成に従って生成されます。
-   `log_dir` ：ログディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、ログディレクトリは`global`セクションの`log_dir`構成に従って生成されます。
-   `numa_node` ：NUMAポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲットマシンに[numactl](https://linux.die.net/man/8/numactl)がインストールされていることを確認する必要があります。このフィールドが指定されている場合、cpubindおよびmembindポリシーは[numactl](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などのNUMAノードのIDです。
-   `config` ：このフィールドの構成規則は、 `server_configs`セクションの`worker`の構成規則と同じです。 `config`が指定されている場合、 `config`の構成は`server_configs`の`worker`の構成とマージされ（2つのフィールドが重複している場合、このフィールドの構成が有効になります）、構成ファイルが生成され、で指定されたマシンに配布されます。 `host`フィールド。
-   `os` ： `host`フィールドで指定されたマシンのオペレーティングシステム。フィールドが指定されていない場合、デフォルト値は`global`セクションで構成された`os`値です。
-   `arch` ： `host`フィールドで指定されたマシンのアーキテクチャ。フィールドが指定されていない場合、デフォルト値は`global`セクションで構成された`arch`値です。
-   `resource_control` ：このサービスのリソース制御。このフィールドが指定されている場合、このフィールドの構成は`global`セクションの`resource_control`の構成とマージされ（2つのフィールドが重複している場合、このフィールドの構成が有効になります）、systemdの構成ファイルが生成および配布されます。 `host`フィールドで指定されたマシンに。このフィールドの構成ルールは、 `global`セクションの`resource_control`の構成ルールと同じです。

`worker_servers`セクションでは、展開の完了後に次のフィールドを変更することはできません。

-   `host`
-   `name`
-   `port`
-   `deploy_dir`
-   `data_dir`
-   `log_dir`
-   `arch`
-   `os`

`worker_servers`の構成例は次のとおりです。

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

`monitoring_servers`は、Prometheusサービスがデプロイされるマシンを指定します。マシンのサービス構成を指定することもできます。 `monitoring_servers`は配列です。各配列要素には、次のフィールドが含まれています。

-   `host` ：デプロイ先のマシンを指定します。フィールド値はIPアドレスであり、必須です。
-   `ssh_port` ：操作のためにターゲットマシンに接続するSSHポートを指定します。フィールドが指定されていない場合、 `global`セクションの`ssh_port`が使用されます。
-   `port` ：Prometheusがサービスを提供するポートを指定します。デフォルト値は「9090」です。
-   `deploy_dir` ：デプロイメントディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、デプロイメントディレクトリは`global`セクションの`deploy_dir`構成に従って生成されます。
-   `data_dir` ：データディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、データディレクトリは`global`セクションの`data_dir`構成に従って生成されます。
-   `log_dir` ：ログディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、ログディレクトリは`global`セクションの`log_dir`構成に従って生成されます。
-   `numa_node` ：NUMAポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲットマシンに[numactl](https://linux.die.net/man/8/numactl)がインストールされていることを確認する必要があります。このフィールドが指定されている場合、cpubindおよびmembindポリシーは[numactl](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などのNUMAノードのIDです。
-   `storage_retention` ：Prometheusモニタリングデータの保持時間を指定します。デフォルト値は「15d」です。
-   `rule_dir` ：完全な`*.rules.yml`のファイルが配置されているローカルディレクトリを指定します。指定されたディレクトリ内のファイルは、クラスタ構成の初期化フェーズ中にPrometheusルールとしてターゲットマシンに送信されます。
-   `remote_config` ：リモートへのPrometheusデータの書き込み、またはリモートからのデータの読み取りをサポートします。このフィールドには2つの構成があります。
    -   `remote_write` ：Prometheusドキュメント[`&#x3C;remote_write>`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write)を参照してください。
    -   `remote_read` ：Prometheusドキュメント[`&#x3C;remote_read>`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_read)を参照してください。
-   `external_alertmanagers` ： `external_alertmanagers`フィールドが構成されている場合、Prometheusはクラスタの外部にあるAlertmanagerに構成動作を警告します。このフィールドは配列であり、各要素は外部Alertmanagerであり、 `host`つと`web_port`のフィールドで構成されています。
-   `os` ： `host`フィールドで指定されたマシンのオペレーティングシステム。フィールドが指定されていない場合、デフォルト値は`global`セクションで構成された`os`値です。
-   `arch` ： `host`フィールドで指定されたマシンのアーキテクチャ。フィールドが指定されていない場合、デフォルト値は`global`セクションで構成された`arch`値です。
-   `resource_control` ：このサービスのリソース制御。このフィールドが指定されている場合、このフィールドの構成は`global`セクションの`resource_control`の構成とマージされ（2つのフィールドが重複している場合、このフィールドの構成が有効になります）、systemdの構成ファイルが生成および配布されます。 `host`フィールドで指定されたマシンに。このフィールドの構成ルールは、 `global`セクションの`resource_control`の構成ルールと同じです。

`monitoring_servers`セクションでは、展開の完了後に次のフィールドを変更することはできません。

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
      - url: http://127.0.0.1:8003/read\
      external_alertmanagers:
      - host: 10.1.1.1
      web_port: 9093
      - host: 10.1.1.2
      web_port: 9094
```

### <code>grafana_servers</code> {#code-grafana-servers-code}

`grafana_servers`は、Grafanaサービスがデプロイされるマシンを指定します。マシンのサービス構成を指定することもできます。 `grafana_servers`は配列です。各配列要素には、次のフィールドが含まれています。

-   `host` ：デプロイ先のマシンを指定します。フィールド値はIPアドレスであり、必須です。
-   `ssh_port` ：操作のためにターゲットマシンに接続するSSHポートを指定します。フィールドが指定されていない場合、 `global`セクションの`ssh_port`が使用されます。
-   `port` ：Grafanaがサービスを提供するポートを指定します。デフォルト値は「3000」です。
-   `deploy_dir` ：デプロイメントディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、デプロイメントディレクトリは`global`セクションの`deploy_dir`構成に従って生成されます。
-   `os` ： `host`フィールドで指定されたマシンのオペレーティングシステム。フィールドが指定されていない場合、デフォルト値は`global`セクションで構成された`os`値です。
-   `arch` ： `host`フィールドで指定されたマシンのアーキテクチャ。フィールドが指定されていない場合、デフォルト値は`global`セクションで構成された`arch`値です。
-   `username` ：Grafanaログイン画面のユーザー名を指定します。
-   `password` ：Grafanaの対応するパスワードを指定します。
-   `dashboard_dir` ：完全な`dashboard(*.json)`のファイルが配置されているローカルディレクトリを指定します。指定されたディレクトリ内のファイルは、クラスタ構成の初期化フェーズ中にGrafanaダッシュボードとしてターゲットマシンに送信されます。
-   `resource_control` ：このサービスのリソース制御。このフィールドが指定されている場合、このフィールドの構成は`global`セクションの`resource_control`の構成とマージされ（2つのフィールドが重複している場合、このフィールドの構成が有効になります）、systemdの構成ファイルが生成および配布されます。 `host`フィールドで指定されたマシンに。このフィールドの構成ルールは、 `global`セクションの`resource_control`の構成ルールと同じです。

> **ノート：**
>
> `grafana_servers`の`dashboard_dir`フィールドが構成されている場合、 `tiup cluster rename`コマンドを実行してクラスタの名前を変更した後、次の操作を実行する必要があります。
>
> 1.  ローカル`dashboards`ディレクトリで、 `datasource`フィールドの値を新しいクラスタ名に更新します（ `datasource`はクラスタ名にちなんで名付けられています）。
> 2.  `tiup cluster reload -R grafana`コマンドを実行します。

`grafana_servers`では、展開の完了後に次のフィールドを変更することはできません。

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

`alertmanager_servers`は、Alertmanagerサービスがデプロイされるマシンを指定します。各マシンのサービス構成を指定することもできます。 `alertmanager_servers`は配列です。各配列要素には、次のフィールドが含まれています。

-   `host` ：デプロイ先のマシンを指定します。フィールド値はIPアドレスであり、必須です。
-   `ssh_port` ：操作のためにターゲットマシンに接続するSSHポートを指定します。フィールドが指定されていない場合、 `global`セクションの`ssh_port`が使用されます。
-   `web_port` ：AlertmanagerがWebサービスを提供するポートを指定します。デフォルト値は「9093」です。
-   `cluster_port` ：1つのAlertmangerと他のAlertmanager間の通信ポートを指定します。デフォルト値は「9094」です。
-   `deploy_dir` ：デプロイメントディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、デプロイメントディレクトリは`global`セクションの`deploy_dir`構成に従って生成されます。
-   `data_dir` ：データディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、データディレクトリは`global`セクションの`data_dir`構成に従って生成されます。
-   `log_dir` ：ログディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、ログディレクトリは`global`セクションの`log_dir`構成に従って生成されます。
-   `numa_node` ：NUMAポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲットマシンに[numactl](https://linux.die.net/man/8/numactl)がインストールされていることを確認する必要があります。このフィールドが指定されている場合、cpubindおよびmembindポリシーは[numactl](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などのNUMAノードのIDです。
-   `config_file` ：ローカルファイルを指定します。指定されたファイルは、クラスタ構成の初期化フェーズ中にAlertmanagerの構成としてターゲットマシンに送信されます。
-   `os` ： `host`フィールドで指定されたマシンのオペレーティングシステム。フィールドが指定されていない場合、デフォルト値は`global`セクションで構成された`os`値です。
-   `arch` ： `host`フィールドで指定されたマシンのアーキテクチャ。フィールドが指定されていない場合、デフォルト値は`global`セクションで構成された`arch`値です。
-   `resource_control` ：このサービスのリソース制御。このフィールドが指定されている場合、このフィールドの構成は`global`セクションの`resource_control`の構成とマージされ（2つのフィールドが重複している場合、このフィールドの構成が有効になります）、systemdの構成ファイルが生成および配布されます。 `host`フィールドで指定されたマシンに。このフィールドの構成ルールは、 `global`セクションの`resource_control`の構成ルールと同じです。

`alertmanager_servers`では、展開の完了後に次のフィールドを変更することはできません。

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
