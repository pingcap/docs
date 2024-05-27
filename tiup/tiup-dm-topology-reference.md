---
title: Topology Configuration File for DM Cluster Deployment Using TiUP
summary: TiUPを使用して TiDB データ移行 (DM) クラスターをデプロイまたは拡張するには、クラスターのグローバル構成、サーバー構成、マスター サーバー、ワーカー サーバー、監視サーバー、Grafana サーバー、および Alertmanager サーバーを記述するトポロジ ファイルが必要です。各セクションには、構成用の特定のフィールドが含まれています。トポロジ ファイルの構造には、global、server_configs、master_servers、worker_servers、monitoring_servers、grafana_servers、および alertmanager_servers が含まれます。各セクションには、デプロイと構成用に独自の構成可能なフィールド セットがあります。
---

# TiUPを使用した DMクラスタ展開のトポロジコンフィグレーションファイル {#topology-configuration-file-for-dm-cluster-deployment-using-tiup}

TiDBデータ移行（DM）クラスターをデプロイまたは拡張するには、クラスタートポロジを記述するトポロジファイル（ [サンプル](https://github.com/pingcap/tiup/blob/master/embed/examples/dm/topology.example.yaml) ）を提供する必要があります。

同様に、クラスター トポロジを変更するには、トポロジ ファイルを変更する必要があります。違いは、クラスターがデプロイされた後は、トポロジ ファイル内のフィールドの一部しか変更できないことです。このドキュメントでは、トポロジ ファイルの各セクションと、各セクション内の各フィールドについて説明します。

## ファイル構造 {#file-structure}

TiUPを使用した DM クラスターの展開用のトポロジ構成ファイルには、次のセクションが含まれる場合があります。

-   [グローバル](#global) : クラスターのグローバル構成。構成項目の一部はクラスターのデフォルト値を使用し、各インスタンスで個別に構成できます。
-   [サーバー構成](#server_configs) : コンポーネントのグローバル構成。各コンポーネントを個別に構成できます。インスタンスに同じキーの構成項目がある場合は、インスタンスの構成項目が有効になります。
-   [マスターサーバー](#master_servers) : DM マスター インスタンスの構成。この構成では、DMコンポーネントのマスター サービスがデプロイされるマシンを指定します。
-   [ワーカーサーバー](#worker_servers) : DM ワーカー インスタンスの構成。この構成では、DMコンポーネントのワーカー サービスがデプロイされるマシンを指定します。
-   [監視サーバー](#monitoring_servers) : Prometheus インスタンスがデプロイされるマシンを指定します。TiUPは複数の Prometheus インスタンスのデプロイをサポートしていますが、最初のインスタンスのみが使用されます。
-   [grafana_サーバー](#grafana_servers) : Grafana インスタンスの構成。構成では、Grafana インスタンスがデプロイされるマシンを指定します。
-   [アラートマネージャサーバー](#alertmanager_servers) : Alertemanager インスタンスの構成。構成では、Alertmanager インスタンスがデプロイされるマシンを指定します。

### <code>global</code> {#code-global-code}

`global`セクションはクラスターのグローバル構成に対応し、次のフィールドがあります。

-   `user` : デプロイされたクラスターを起動するユーザー。デフォルト値は「tidb」です。2 フィールドに指定され`<user>`ユーザーがターゲット マシンに存在しない場合、 TiUP は自動的にユーザーの作成を試みます。
-   `group` : ユーザーが自動的に作成されるときにユーザーが属するユーザー グループ。デフォルト値は`<user>`フィールドと同じです。指定されたグループが存在しない場合は、自動的に作成されます。
-   `ssh_port` : 操作のためにターゲットマシンに接続するための SSH ポート。デフォルト値は「22」です。
-   `deploy_dir` : 各コンポーネントのデプロイメント ディレクトリ。デフォルト値は「deploy」です。構築ルールは次のとおりです。
    -   絶対パス`deploy_dir`がインスタンス レベルで構成されている場合、実際のデプロイメント ディレクトリはインスタンスに構成されている`deploy_dir`になります。
    -   各インスタンスに対して`deploy_dir`設定しない場合、デフォルト値は相対パス`<component-name>-<component-port>`になります。
    -   `global.deploy_dir`絶対パスに設定されている場合、コンポーネントは`<global.deploy_dir>/<instance.deploy_dir>`ディレクトリにデプロイされます。
    -   `global.deploy_dir`相対パスに設定されている場合、コンポーネントは`/home/<global.user>/<global.deploy_dir>/<instance.deploy_dir>`ディレクトリにデプロイされます。
-   `data_dir` : データディレクトリ。デフォルト値は「data」です。構築ルールは次のとおりです。
    -   絶対パス`data_dir`がインスタンス レベルで構成されている場合、実際のデータ ディレクトリはインスタンスに構成されている`data_dir`になります。
    -   各インスタンスで`data_dir`設定されていない場合、デフォルト値は`<global.data_dir>`になります。
    -   `data_dir`相対パスに設定されている場合、コンポーネントデータは`<deploy_dir>/<data_dir>`に保存されます。 `<deploy_dir>`の構築ルールについては、 `deploy_dir`フィールドの構築ルールを参照してください。
-   `log_dir` : データディレクトリ。デフォルト値は「log」です。構築ルールは次のとおりです。
    -   インスタンス レベルで絶対パス`log_dir`が設定されている場合、実際のログ ディレクトリはインスタンスに設定されている`log_dir`になります。
    -   各インスタンスについて、ユーザーが`log_dir`を設定しない場合、デフォルト値は`<global.log_dir>`なります。
    -   `log_dir`相対パスの場合、コンポーネントログは`<deploy_dir>/<log_dir>`に保存されます。 `<deploy_dir>`の構築ルールについては、 `deploy_dir`フィールドの構築ルールを参照してください。
-   `os` : ターゲット マシンのオペレーティング システム。このフィールドは、ターゲット マシンにプッシュされるコンポーネントをどのオペレーティング システムに適合させるかを制御します。デフォルト値は「linux」です。
-   `arch` : ターゲット マシンの CPUアーキテクチャ。このフィールドは、ターゲット マシンにプッシュされるバイナリ パッケージをどのプラットフォームに適合させるかを制御します。サポートされている値は「amd64」と「arm64」です。デフォルト値は「amd64」です。
-   `resource_control` : ランタイム リソース制御。このフィールドのすべての設定は、systemd のサービス ファイルに書き込まれます。デフォルトでは制限はありません。制御できるリソースは次のとおりです。
    -   `memory_limit` : 実行時に最大メモリを制限します。たとえば、「2G」は最大 2 GB のメモリが使用できることを意味します。
    -   `cpu_quota` : 実行時の最大 CPU 使用率を制限します。たとえば、「200%」などです。
    -   `io_read_bandwidth_max` : ディスク読み取りの最大 I/O 帯域幅を制限します。たとえば、 `"/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0:0 100M"` 。
    -   `io_write_bandwidth_max` : ディスク書き込みの最大 I/O 帯域幅を制限します。たとえば、 `"/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0:0 100M"` 。
    -   `limit_core` : コアダンプのサイズを制御します。

`global`構成例:

```yaml
global:
  user: "tidb"
  resource_control:
    memory_limit: "2G"
```

この例では、構成では、クラスターを起動するために`tidb`ユーザーが使用され、各コンポーネントの実行時に最大 2 GB のメモリに制限されることが指定されています。

### <code>server_configs</code> {#code-server-configs-code}

`server_configs`は、サービスを設定し、各コンポーネントの設定ファイルを生成するために使用されます。 `global`セクションと同様に、 `server_configs`セクションの設定は、インスタンス内の同じキーを持つ設定によって上書きできます。 `server_configs`には主に次のフィールドが含まれます。

-   `master` : DM マスター サービスに関連する構成。サポートされているすべての構成項目については、 [DMマスターコンフィグレーションファイル](/dm/dm-master-configuration-file.md)を参照してください。
-   `worker` : DM ワーカー サービスに関連する構成。サポートされているすべての構成項目については、 [DM-workerコンフィグレーションファイル](/dm/dm-worker-configuration-file.md)を参照してください。

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

`master_servers`は、DMコンポーネントのマスター ノードがデプロイされるマシンを指定します。各マシンのサービス構成を指定することもできます。2 `master_servers`配列です。各配列要素には、次のフィールドが含まれます。

-   `host` : デプロイ先のマシンを指定します。フィールド値は IP アドレスであり、必須です。
-   `ssh_port` : 操作のためにターゲット マシンに接続するための SSH ポートを指定します。フィールドが指定されていない場合は、セクション`global`の`ssh_port`が使用されます。
-   `name` : DM マスター インスタンスの名前を指定します。名前はインスタンスごとに一意である必要があります。そうでない場合、クラスターをデプロイできません。
-   `port` : DM マスターがサービスを提供するポートを指定します。デフォルト値は「8261」です。
-   `peer_port` : DM マスター間の通信用のポートを指定します。デフォルト値は「8291」です。
-   `deploy_dir` : デプロイメント ディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、デプロイメント ディレクトリは`global`セクションの`deploy_dir`構成に従って生成されます。
-   `data_dir` : データ ディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、データ ディレクトリは`global`セクションの`data_dir`構成に従って生成されます。
-   `log_dir` : ログ ディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、ログ ディレクトリは`global`セクションの`log_dir`構成に従って生成されます。
-   `numa_node` : インスタンスに NUMA ポリシーを割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドを指定すると、cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、&quot;0,1&quot; などの NUMA ノードの ID です。
-   `config` : このフィールドの設定ルールは、セクション`server_configs`の`master`と同じです。6 `config`指定された場合、セクション`server_configs`の`config`の設定がセクション`master`の設定とマージされ (2 つのフィールドが重複している場合は、このフィールドの設定が有効になります)、設定ファイルが生成され、セクション`host`で指定されたマシンに配布されます。
-   `os` : `host`フィールドで指定されたマシンのオペレーティング システム。フィールドが指定されていない場合、デフォルト値は`global`セクションで構成された`os`値になります。
-   `arch` : `host`フィールドで指定されたマシンのアーキテクチャ。フィールドが指定されていない場合、デフォルト値は`global`セクションで構成された`arch`値になります。
-   `resource_control` : このサービスに対するリソース制御。このフィールドが指定された場合、このフィールドの設定はセクション`global`の`resource_control`の設定とマージされ (2 つのフィールドが重複している場合は、このフィールドの設定が有効になります)、systemd の設定ファイルが生成され、セクション`host`で指定されたマシンに配布されます。このフィールドの設定ルールは、セクション`global`の`resource_control`と同じです。
-   `v1_source_path` : v1.0.x からアップグレードする場合、このフィールドに V1 ソースの構成ファイルが配置されているディレクトリを指定できます。

`master_servers`セクションでは、デプロイメントが完了した後は、次のフィールドを変更することはできません。

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

`worker_servers`は、DMコンポーネントのマスター ノードがデプロイされるマシンを指定します。各マシンのサービス構成を指定することもできます。2 `worker_servers`配列です。各配列要素には、次のフィールドが含まれます。

-   `host` : デプロイ先のマシンを指定します。フィールド値は IP アドレスであり、必須です。
-   `ssh_port` : 操作のためにターゲット マシンに接続するための SSH ポートを指定します。フィールドが指定されていない場合は、セクション`global`の`ssh_port`が使用されます。
-   `name` : DM ワーカー インスタンスの名前を指定します。名前はインスタンスごとに一意である必要があります。そうでない場合、クラスターをデプロイできません。
-   `port` : DM ワーカーがサービスを提供するポートを指定します。デフォルト値は「8262」です。
-   `deploy_dir` : デプロイメント ディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、デプロイメント ディレクトリは`global`セクションの`deploy_dir`構成に従って生成されます。
-   `data_dir` : データ ディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、データ ディレクトリは`global`セクションの`data_dir`構成に従って生成されます。
-   `log_dir` : ログ ディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、ログ ディレクトリは`global`セクションの`log_dir`構成に従って生成されます。
-   `numa_node` : インスタンスに NUMA ポリシーを割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドを指定すると、cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、&quot;0,1&quot; などの NUMA ノードの ID です。
-   `config` : このフィールドの設定ルールは、セクション`server_configs`の`worker`と同じです。6 `config`指定された場合、セクション`server_configs`の`config`の設定がセクション`worker`の設定とマージされ (2 つのフィールドが重複している場合は、このフィールドの設定が有効になります)、設定ファイルが生成され、セクション`host`で指定されたマシンに配布されます。
-   `os` : `host`フィールドで指定されたマシンのオペレーティング システム。フィールドが指定されていない場合、デフォルト値は`global`セクションで構成された`os`値になります。
-   `arch` : `host`フィールドで指定されたマシンのアーキテクチャ。フィールドが指定されていない場合、デフォルト値は`global`セクションで構成された`arch`値になります。
-   `resource_control` : このサービスに対するリソース制御。このフィールドが指定された場合、このフィールドの設定はセクション`global`の`resource_control`の設定とマージされ (2 つのフィールドが重複している場合は、このフィールドの設定が有効になります)、systemd の設定ファイルが生成され、セクション`host`で指定されたマシンに配布されます。このフィールドの設定ルールは、セクション`global`の`resource_control`と同じです。

`worker_servers`セクションでは、デプロイメントが完了した後は、次のフィールドを変更することはできません。

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

`monitoring_servers` 、Prometheus サービスがデプロイされるマシンを指定します。マシン上のサービス構成を指定することもできます`monitoring_servers`は配列です。各配列要素には、次のフィールドが含まれます。

-   `host` : デプロイ先のマシンを指定します。フィールド値は IP アドレスであり、必須です。
-   `ssh_port` : 操作のためにターゲット マシンに接続するための SSH ポートを指定します。フィールドが指定されていない場合は、セクション`global`の`ssh_port`が使用されます。
-   `port` : Prometheus がサービスを提供するポートを指定します。デフォルト値は「9090」です。
-   `deploy_dir` : デプロイメント ディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、デプロイメント ディレクトリは`global`セクションの`deploy_dir`構成に従って生成されます。
-   `data_dir` : データ ディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、データ ディレクトリは`global`セクションの`data_dir`構成に従って生成されます。
-   `log_dir` : ログ ディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、ログ ディレクトリは`global`セクションの`log_dir`構成に従って生成されます。
-   `numa_node` : インスタンスに NUMA ポリシーを割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドが指定されている場合、cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、&quot;0,1&quot; などの NUMA ノードの ID です。
-   `storage_retention` : Prometheus 監視データの保持時間を指定します。デフォルト値は「15d」です。
-   `rule_dir` : 完全な`*.rules.yml`ファイルが配置されているローカル ディレクトリを指定します。指定されたディレクトリ内のファイルは、クラスター構成の初期化フェーズ中に Prometheus ルールとしてターゲット マシンに送信されます。
-   `remote_config` : Prometheus データをリモートに書き込むか、リモートからデータを読み取ることをサポートします。このフィールドには 2 つの構成があります。
    -   `remote_write` : Prometheusドキュメント[`&#x3C;remote_write>`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write)を参照してください。
    -   `remote_read` : Prometheusドキュメント[`&#x3C;remote_read>`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_read)を参照してください。
-   `external_alertmanagers` : `external_alertmanagers`フィールドが設定されている場合、Prometheus はクラスター外の Alertmanager に設定動作を通知します。このフィールドは配列であり、各要素は外部 Alertmanager であり、 `host`フィールドと`web_port`フィールドで構成されます。
-   `os` : `host`フィールドで指定されたマシンのオペレーティング システム。フィールドが指定されていない場合、デフォルト値は`global`セクションで構成された`os`値になります。
-   `arch` : `host`フィールドで指定されたマシンのアーキテクチャ。フィールドが指定されていない場合、デフォルト値は`global`セクションで構成された`arch`値になります。
-   `resource_control` : このサービスに対するリソース制御。このフィールドが指定された場合、このフィールドの設定はセクション`global`の`resource_control`の設定とマージされ (2 つのフィールドが重複している場合は、このフィールドの設定が有効になります)、systemd の設定ファイルが生成され、セクション`host`で指定されたマシンに配布されます。このフィールドの設定ルールは、セクション`global`の`resource_control`と同じです。

`monitoring_servers`セクションでは、デプロイメントが完了した後は、次のフィールドを変更することはできません。

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

`grafana_servers` 、Grafana サービスがデプロイされるマシンを指定します。マシン上のサービス構成を指定することもできます`grafana_servers`は配列です。各配列要素には、次のフィールドが含まれます。

-   `host` : デプロイ先のマシンを指定します。フィールド値は IP アドレスであり、必須です。
-   `ssh_port` : 操作のためにターゲット マシンに接続するための SSH ポートを指定します。フィールドが指定されていない場合は、セクション`global`の`ssh_port`が使用されます。
-   `port` : Grafana がサービスを提供するポートを指定します。デフォルト値は「3000」です。
-   `deploy_dir` : デプロイメント ディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、デプロイメント ディレクトリは`global`セクションの`deploy_dir`構成に従って生成されます。
-   `os` : `host`フィールドで指定されたマシンのオペレーティング システム。フィールドが指定されていない場合、デフォルト値は`global`セクションで構成された`os`値になります。
-   `arch` : `host`フィールドで指定されたマシンのアーキテクチャ。フィールドが指定されていない場合、デフォルト値は`global`セクションで構成された`arch`値になります。
-   `username` : Grafana ログイン画面のユーザー名を指定します。
-   `password` : Grafana の対応するパスワードを指定します。
-   `dashboard_dir` : 完全な`dashboard(*.json)`ファイルが配置されているローカル ディレクトリを指定します。指定されたディレクトリ内のファイルは、クラスター構成の初期化フェーズ中に Grafana ダッシュボードとしてターゲット マシンに送信されます。
-   `resource_control` : このサービスに対するリソース制御。このフィールドが指定された場合、このフィールドの設定はセクション`global`の`resource_control`の設定とマージされ (2 つのフィールドが重複している場合は、このフィールドの設定が有効になります)、systemd の設定ファイルが生成され、セクション`host`で指定されたマシンに配布されます。このフィールドの設定ルールは、セクション`global`の`resource_control`と同じです。

> **注記：**
>
> `dashboard_dir`フィールドが`grafana_servers`に設定されている場合、クラスターの名前を変更する`tiup cluster rename`コマンドを実行した後、次の操作を実行する必要があります。
>
> 1.  ローカルの`dashboards`ディレクトリで、 `datasource`フィールドの値を新しいクラスター名に更新します ( `datasource`はクラスター名に基づいて名前が付けられます)。
> 2.  `tiup cluster reload -R grafana`コマンドを実行します。

`grafana_servers`では、デプロイメントが完了した後は、次のフィールドを変更できません。

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

`alertmanager_servers` 、Alertmanager サービスが展開されるマシンを指定します。各マシンのサービス構成を指定することもできます`alertmanager_servers`は配列です。各配列要素には、次のフィールドが含まれます。

-   `host` : デプロイ先のマシンを指定します。フィールド値は IP アドレスであり、必須です。
-   `ssh_port` : 操作のためにターゲット マシンに接続するための SSH ポートを指定します。フィールドが指定されていない場合は、セクション`global`の`ssh_port`が使用されます。
-   `web_port` : Alertmanager が Web サービスを提供するポートを指定します。デフォルト値は「9093」です。
-   `cluster_port` : 1 つの Alertmanager と他の Alertmanager 間の通信ポートを指定します。デフォルト値は「9094」です。
-   `deploy_dir` : デプロイメント ディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、デプロイメント ディレクトリは`global`セクションの`deploy_dir`構成に従って生成されます。
-   `data_dir` : データ ディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、データ ディレクトリは`global`セクションの`data_dir`構成に従って生成されます。
-   `log_dir` : ログ ディレクトリを指定します。フィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、ログ ディレクトリは`global`セクションの`log_dir`構成に従って生成されます。
-   `numa_node` : インスタンスに NUMA ポリシーを割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドが指定されている場合、cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、&quot;0,1&quot; などの NUMA ノードの ID です。
-   `config_file` : ローカル ファイルを指定します。指定されたファイルは、クラスター構成の初期化フェーズ中に、Alertmanager の構成としてターゲット マシンに送信されます。
-   `os` : `host`フィールドで指定されたマシンのオペレーティング システム。フィールドが指定されていない場合、デフォルト値は`global`セクションで構成された`os`値になります。
-   `arch` : `host`フィールドで指定されたマシンのアーキテクチャ。フィールドが指定されていない場合、デフォルト値は`global`セクションで構成された`arch`値になります。
-   `resource_control` : このサービスに対するリソース制御。このフィールドが指定された場合、このフィールドの設定はセクション`global`の`resource_control`の設定とマージされ (2 つのフィールドが重複している場合は、このフィールドの設定が有効になります)、systemd の設定ファイルが生成され、セクション`host`で指定されたマシンに配布されます。このフィールドの設定ルールは、セクション`global`の`resource_control`と同じです。

`alertmanager_servers`では、デプロイメントが完了した後は、次のフィールドを変更できません。

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
