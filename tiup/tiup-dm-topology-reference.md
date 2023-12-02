---
title: Topology Configuration File for DM Cluster Deployment Using TiUP
---

# TiUPを使用した DMクラスタ展開用のトポロジコンフィグレーションファイル {#topology-configuration-file-for-dm-cluster-deployment-using-tiup}

TiDB データ マイグレーション (DM) クラスターをデプロイまたはスケーリングするには、クラスター トポロジーを記述するトポロジー ファイル ( [サンプル](https://github.com/pingcap/tiup/blob/master/embed/examples/dm/topology.example.yaml) ) を提供する必要があります。

同様に、クラスター トポロジを変更するには、トポロジ ファイルを変更する必要があります。違いは、クラスターのデプロイ後は、トポロジー ファイル内のフィールドの一部のみを変更できることです。このドキュメントでは、トポロジ ファイルの各セクションと各セクションの各フィールドを紹介します。

## ファイル構造 {#file-structure}

TiUPを使用した DM クラスター展開のトポロジ構成ファイルには、次のセクションが含まれる場合があります。

-   [グローバル](#global) : クラスターのグローバル構成。一部の構成項目はクラスターのデフォルト値を使用し、インスタンスごとに個別に構成できます。
-   [サーバー構成](#server_configs) : コンポーネントのグローバル構成。各コンポーネントを個別に構成できます。インスタンスに同じキーを持つ構成アイテムがある場合、インスタンスの構成アイテムが有効になります。
-   [マスターサーバー](#master_servers) : DM マスター インスタンスの構成。この構成では、DMコンポーネントのマスター サービスがデプロイされるマシンを指定します。
-   [ワーカーサーバー](#worker_servers) : DM ワーカー インスタンスの構成。この構成では、DMコンポーネントのワーカー サービスがデプロイされるマシンを指定します。
-   [監視サーバー](#monitoring_servers) : Prometheus インスタンスがデプロイされるマシンを指定します。 TiUP は複数の Prometheus インスタンスのデプロイをサポートしていますが、最初のインスタンスのみが使用されます。
-   [グラファナサーバー](#grafana_servers) : Grafana インスタンスの構成。構成では、Grafana インスタンスがデプロイされるマシンを指定します。
-   [アラートマネージャー_サーバー](#alertmanager_servers) : Alertemanager インスタンスの構成。この構成では、Alertmanager インスタンスがデプロイされるマシンを指定します。

### <code>global</code> {#code-global-code}

`global`セクションはクラスターのグローバル構成に対応し、次のフィールドがあります。

-   `user` : デプロイされたクラスターを開始するユーザー。デフォルト値は「tidb」です。 `<user>`フィールドで指定されたユーザーがターゲット マシンに存在しない場合、 TiUP は自動的にユーザーの作成を試みます。
-   `group` : ユーザーが自動作成されたときにユーザーが所属するユーザーグループ。デフォルト値は`<user>`フィールドと同じです。指定したグループが存在しない場合は、自動的に作成されます。
-   `ssh_port` : 操作のためにターゲット マシンに接続するための SSH ポート。デフォルト値は「22」です。
-   `deploy_dir` : 各コンポーネントのデプロイメント ディレクトリ。デフォルト値は「デプロイ」です。施工ルールは以下の通りです。
    -   絶対パス`deploy_dir`がインスタンス レベルで設定されている場合、実際のデプロイメント ディレクトリはインスタンスに設定されている`deploy_dir`なります。
    -   各インスタンスについて、 `deploy_dir`を構成しない場合、デフォルト値は相対パス`<component-name>-<component-port>`です。
    -   `global.deploy_dir`が絶対パスに設定されている場合、コンポーネントは`<global.deploy_dir>/<instance.deploy_dir>`ディレクトリにデプロイされます。
    -   `global.deploy_dir`が相対パスに設定されている場合、コンポーネントは`/home/<global.user>/<global.deploy_dir>/<instance.deploy_dir>`ディレクトリにデプロイされます。
-   `data_dir` : データディレクトリ。デフォルト値は「データ」です。施工ルールは以下の通りです。
    -   絶対パス`data_dir`がインスタンス レベルで設定されている場合、実際のデータ ディレクトリはインスタンスに設定されている`data_dir`です。
    -   各インスタンスで`data_dir`が構成されていない場合、デフォルト値は`<global.data_dir>`です。
    -   相対パスに`data_dir`を設定した場合、コンポーネントデータは`<deploy_dir>/<data_dir>`に格納されます。 `<deploy_dir>`の構築ルールについては、 `deploy_dir`フィールドの構築ルールを参照してください。
-   `log_dir` : データディレクトリ。デフォルト値は「ログ」です。施工ルールは以下の通りです。
    -   絶対パス`log_dir`がインスタンス レベルで設定されている場合、実際のログ ディレクトリはインスタンスに設定されている`log_dir`なります。
    -   各インスタンスについて、ユーザーが`log_dir`構成しない場合、デフォルト値は`<global.log_dir>`です。
    -   `log_dir`が相対パスの場合、コンポーネントログは`<deploy_dir>/<log_dir>`に保存されます。 `<deploy_dir>`の構築ルールについては、 `deploy_dir`フィールドの構築ルールを参照してください。
-   `os` : ターゲット マシンのオペレーティング システム。このフィールドは、ターゲット マシンにプッシュされるコンポーネントにどのオペレーティング システムを適応させるかを制御します。デフォルト値は「linux」です。
-   `arch` : ターゲット マシンの CPUアーキテクチャ。このフィールドは、ターゲット マシンにプッシュされるバイナリ パッケージをどのプラットフォームに適応させるかを制御します。サポートされている値は「amd64」と「arm64」です。デフォルト値は「amd64」です。
-   `resource_control` : ランタイムリソース制御。このフィールドのすべての設定は、systemd のサービス ファイルに書き込まれます。デフォルトでは制限はありません。制御できるリソースは以下のとおりです。
    -   `memory_limit` : 実行時の最大メモリを制限します。例えば「2G」は、最大2GBのメモリを使用できることを意味します。
    -   `cpu_quota` : 実行時の最大 CPU 使用率を制限します。たとえば、「200%」です。
    -   `io_read_bandwidth_max` : ディスク読み取りの最大 I/O 帯域幅を制限します。たとえば、 `"/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0:0 100M"` 。
    -   `io_write_bandwidth_max` : ディスク書き込みの最大 I/O 帯域幅を制限します。たとえば、 `"/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0:0 100M"` 。
    -   `limit_core` : コア ダンプのサイズを制御します。

`global`構成例:

```yaml
global:
  user: "tidb"
  resource_control:
    memory_limit: "2G"
```

この例では、クラスターの起動に`tidb`ユーザーが使用され、実行中の各コンポーネントのメモリが最大 2 GB に制限されることが構成で指定されています。

### <code>server_configs</code> {#code-server-configs-code}

`server_configs`は、サービスを構成し、各コンポーネントの構成ファイルを生成するために使用されます。 `global`セクションと同様に、 `server_configs`セクションの設定は、インスタンス内の同じキーを持つ設定によって上書きできます。 `server_configs`は主に次のフィールドが含まれます。

-   `master` : DMマスターサービスに関連する設定。サポートされているすべての構成項目については、 [DMマスターコンフィグレーションファイル](/dm/dm-master-configuration-file.md)を参照してください。
-   `worker` : DM-worker サービスに関連する構成。サポートされているすべての構成項目については、 [DM ワーカーコンフィグレーションファイル](/dm/dm-worker-configuration-file.md)を参照してください。

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

`master_servers` 、DMコンポーネントのマスター ノードがデプロイされるマシンを指定します。各マシンのサービス構成を指定することもできます。 `master_servers`は配列です。各配列要素には次のフィールドが含まれます。

-   `host` : デプロイ先のマシンを指定します。フィールド値は IP アドレスであり、必須です。
-   `ssh_port` : 操作のためにターゲット マシンに接続する SSH ポートを指定します。フィールドが指定されていない場合は、 `global`セクションの`ssh_port`が使用されます。
-   `name` : DM マスター インスタンスの名前を指定します。名前は異なるインスタンスに対して一意である必要があります。そうしないと、クラスターをデプロイできません。
-   `port` : DM マスターがサービスを提供するポートを指定します。デフォルト値は「8261」です。
-   `peer_port` : DM マスター間の通信用のポートを指定します。デフォルト値は「8291」です。
-   `deploy_dir` : デプロイメントディレクトリを指定します。フィールドが指定されていないか、相対ディレクトリとして指定されている場合、デプロイメント ディレクトリは`global`セクションの`deploy_dir`設定に従って生成されます。
-   `data_dir` : データディレクトリを指定します。フィールドが指定されていないか、相対ディレクトリとして指定されている場合、データ ディレクトリはセクション`global`の`data_dir`設定に従って生成されます。
-   `log_dir` : ログディレクトリを指定します。フィールドが指定されていないか、相対ディレクトリとして指定されている場合、ログ ディレクトリはセクション`global`の`log_dir`設定に従って生成されます。
-   `numa_node` : NUMA ポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドが指定されている場合、 cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などの NUMA ノードの ID です。
-   `config` : このフィールドの設定ルールは、セクション`server_configs`の`master`と同じです。 `config`を指定した場合、 `config`の設定は`server_configs`の`master`の設定とマージされ (2 つのフィールドが重複する場合、このフィールドの設定が有効になります)、設定ファイルが生成され、設定ファイルで指定されたマシンに配布されます。 `host`フィールド。
-   `os` : `host`フィールドで指定されたマシンのオペレーティング システム。フィールドが指定されていない場合、デフォルト値は`global`セクションで設定された`os`値です。
-   `arch` : `host`フィールドで指定されたマシンのアーキテクチャ。フィールドが指定されていない場合、デフォルト値は`global`セクションで設定された`arch`値です。
-   `resource_control` : このサービスのリソース制御。このフィールドを指定した場合、このフィールドの設定は`global`セクションの`resource_control`の設定とマージされ(2つのフィールドが重複している場合は、このフィールドの設定が有効になります)、systemdの設定ファイルが生成および配布されます。 `host`フィールドで指定されたマシンに送信します。このフィールドの設定ルールは、セクション`global`の`resource_control`と同じです。
-   `v1_source_path` : v1.0.x からアップグレードする場合、このフィールドで V1 ソースの構成ファイルが配置されているディレクトリを指定できます。

`master_servers`セクションでは、展開の完了後に次のフィールドを変更できません。

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

`worker_servers` 、DMコンポーネントのマスター ノードがデプロイされるマシンを指定します。各マシンのサービス構成を指定することもできます。 `worker_servers`は配列です。各配列要素には次のフィールドが含まれます。

-   `host` : デプロイ先のマシンを指定します。フィールド値は IP アドレスであり、必須です。
-   `ssh_port` : 操作のためにターゲット マシンに接続する SSH ポートを指定します。フィールドが指定されていない場合は、 `global`セクションの`ssh_port`が使用されます。
-   `name` : DM ワーカー インスタンスの名前を指定します。名前は異なるインスタンスに対して一意である必要があります。そうしないと、クラスターをデプロイできません。
-   `port` : DM ワーカーがサービスを提供するポートを指定します。デフォルト値は「8262」です。
-   `deploy_dir` : デプロイメントディレクトリを指定します。フィールドが指定されていないか、相対ディレクトリとして指定されている場合、デプロイメント ディレクトリは`global`セクションの`deploy_dir`設定に従って生成されます。
-   `data_dir` : データディレクトリを指定します。フィールドが指定されていないか、相対ディレクトリとして指定されている場合、データ ディレクトリはセクション`global`の`data_dir`設定に従って生成されます。
-   `log_dir` : ログディレクトリを指定します。フィールドが指定されていないか、相対ディレクトリとして指定されている場合、ログ ディレクトリはセクション`global`の`log_dir`設定に従って生成されます。
-   `numa_node` : NUMA ポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドが指定されている場合、 cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などの NUMA ノードの ID です。
-   `config` : このフィールドの設定ルールは、セクション`server_configs`の`worker`と同じです。 `config`を指定した場合、 `config`の設定は`server_configs`の`worker`の設定とマージされ (2 つのフィールドが重複する場合、このフィールドの設定が有効になります)、設定ファイルが生成され、設定ファイルで指定されたマシンに配布されます。 `host`フィールド。
-   `os` : `host`フィールドで指定されたマシンのオペレーティング システム。フィールドが指定されていない場合、デフォルト値は`global`セクションで設定された`os`値です。
-   `arch` : `host`フィールドで指定されたマシンのアーキテクチャ。フィールドが指定されていない場合、デフォルト値は`global`セクションで設定された`arch`値です。
-   `resource_control` : このサービスのリソース制御。このフィールドを指定した場合、このフィールドの設定は`global`セクションの`resource_control`の設定とマージされ(2つのフィールドが重複している場合は、このフィールドの設定が有効になります)、systemdの設定ファイルが生成および配布されます。 `host`フィールドで指定されたマシンに送信します。このフィールドの設定ルールは、セクション`global`の`resource_control`と同じです。

`worker_servers`セクションでは、展開の完了後に次のフィールドを変更できません。

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

`monitoring_servers` 、Prometheus サービスがデプロイされるマシンを指定します。マシン上のサービス構成を指定することもできます。 `monitoring_servers`は配列です。各配列要素には次のフィールドが含まれます。

-   `host` : デプロイ先のマシンを指定します。フィールド値は IP アドレスであり、必須です。
-   `ssh_port` : 操作のためにターゲット マシンに接続する SSH ポートを指定します。フィールドが指定されていない場合は、 `global`セクションの`ssh_port`が使用されます。
-   `port` : Prometheus がサービスを提供するポートを指定します。デフォルト値は「9090」です。
-   `deploy_dir` : デプロイメントディレクトリを指定します。フィールドが指定されていないか、相対ディレクトリとして指定されている場合、デプロイメント ディレクトリは`global`セクションの`deploy_dir`設定に従って生成されます。
-   `data_dir` : データディレクトリを指定します。フィールドが指定されていないか、相対ディレクトリとして指定されている場合、データ ディレクトリはセクション`global`の`data_dir`設定に従って生成されます。
-   `log_dir` : ログディレクトリを指定します。フィールドが指定されていないか、相対ディレクトリとして指定されている場合、ログ ディレクトリはセクション`global`の`log_dir`設定に従って生成されます。
-   `numa_node` : NUMA ポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドが指定されている場合、 cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などの NUMA ノードの ID です。
-   `storage_retention` : Prometheus 監視データの保持時間を指定します。デフォルト値は「15d」です。
-   `rule_dir` : `*.rules.yml`つのファイル全体が配置されているローカル ディレクトリを指定します。指定されたディレクトリ内のファイルは、クラスター構成の初期化フェーズ中に Prometheus ルールとしてターゲット マシンに送信されます。
-   `remote_config` : Prometheus データのリモートへの書き込み、またはリモートからのデータの読み取りをサポートします。このフィールドには 2 つの構成があります。
    -   `remote_write` : Prometheus のドキュメント[`&#x3C;remote_write>`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write)を参照してください。
    -   `remote_read` : Prometheus のドキュメント[`&#x3C;remote_read>`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_read)を参照してください。
-   `external_alertmanagers` : `external_alertmanagers`フィールドが設定されている場合、Prometheus はクラスターの外部にある Alertmanager に設定動作を警告します。このフィールドは配列であり、その各要素は外部 Alertmanager であり、 `host`フィールドと`web_port`フィールドで構成されます。
-   `os` : `host`フィールドで指定されたマシンのオペレーティング システム。フィールドが指定されていない場合、デフォルト値は`global`セクションで設定された`os`値です。
-   `arch` : `host`フィールドで指定されたマシンのアーキテクチャ。フィールドが指定されていない場合、デフォルト値は`global`セクションで設定された`arch`値です。
-   `resource_control` : このサービスのリソース制御。このフィールドを指定した場合、このフィールドの設定は`global`セクションの`resource_control`の設定とマージされ(2つのフィールドが重複している場合は、このフィールドの設定が有効になります)、systemdの設定ファイルが生成および配布されます。 `host`フィールドで指定されたマシンに送信します。このフィールドの設定ルールは、セクション`global`の`resource_control`と同じです。

`monitoring_servers`セクションでは、展開の完了後に次のフィールドを変更できません。

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

`grafana_servers` 、Grafana サービスがデプロイされるマシンを指定します。マシン上のサービス構成を指定することもできます。 `grafana_servers`は配列です。各配列要素には次のフィールドが含まれます。

-   `host` : デプロイ先のマシンを指定します。フィールド値は IP アドレスであり、必須です。
-   `ssh_port` : 操作のためにターゲット マシンに接続する SSH ポートを指定します。フィールドが指定されていない場合は、 `global`セクションの`ssh_port`が使用されます。
-   `port` : Grafana がサービスを提供するポートを指定します。デフォルト値は「3000」です。
-   `deploy_dir` : デプロイメントディレクトリを指定します。フィールドが指定されていないか、相対ディレクトリとして指定されている場合、デプロイメント ディレクトリはセクション`global`の`deploy_dir`設定に従って生成されます。
-   `os` : `host`フィールドで指定されたマシンのオペレーティング システム。フィールドが指定されていない場合、デフォルト値は`global`セクションで設定された`os`値です。
-   `arch` : `host`フィールドで指定されたマシンのアーキテクチャ。フィールドが指定されていない場合、デフォルト値は`global`セクションで設定された`arch`値です。
-   `username` : Grafana ログイン画面のユーザー名を指定します。
-   `password` : Grafana の対応するパスワードを指定します。
-   `dashboard_dir` : `dashboard(*.json)`つのファイル全体が配置されているローカル ディレクトリを指定します。指定されたディレクトリ内のファイルは、クラスター構成の初期化フェーズ中に Grafana ダッシュボードとしてターゲット マシンに送信されます。
-   `resource_control` : このサービスのリソース制御。このフィールドを指定した場合、このフィールドの設定は`global`セクションの`resource_control`の設定とマージされ(2つのフィールドが重複している場合は、このフィールドの設定が有効になります)、systemdの設定ファイルが生成および配布されます。 `host`フィールドで指定されたマシンに送信します。このフィールドの設定ルールは、セクション`global`の`resource_control`と同じです。

> **注記：**
>
> `grafana_servers`の`dashboard_dir`フィールドが構成されている場合は、 `tiup cluster rename`コマンドを実行してクラスターの名前を変更した後、次の操作を実行する必要があります。
>
> 1.  ローカル`dashboards`ディレクトリで、 `datasource`フィールドの値を新しいクラスター名に更新します ( `datasource`はクラスター名にちなんで命名されます)。
> 2.  `tiup cluster reload -R grafana`コマンドを実行します。

`grafana_servers`では、デプロイメントの完了後に次のフィールドを変更することはできません。

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

`alertmanager_servers` Alertmanager サービスが展開されるマシンを指定します。各マシンのサービス構成を指定することもできます。 `alertmanager_servers`は配列です。各配列要素には次のフィールドが含まれます。

-   `host` : デプロイ先のマシンを指定します。フィールド値は IP アドレスであり、必須です。
-   `ssh_port` : 操作のためにターゲット マシンに接続する SSH ポートを指定します。フィールドが指定されていない場合は、 `global`セクションの`ssh_port`が使用されます。
-   `web_port` : Alertmanager が Web サービスを提供するポートを指定します。デフォルト値は「9093」です。
-   `cluster_port` : 1 つのアラートマネージャーと他のアラートマネージャー間の通信ポートを指定します。デフォルト値は「9094」です。
-   `deploy_dir` : デプロイメントディレクトリを指定します。フィールドが指定されていないか、相対ディレクトリとして指定されている場合、デプロイメント ディレクトリはセクション`global`の`deploy_dir`設定に従って生成されます。
-   `data_dir` : データディレクトリを指定します。フィールドが指定されていないか、相対ディレクトリとして指定されている場合、データ ディレクトリはセクション`global`の`data_dir`設定に従って生成されます。
-   `log_dir` : ログディレクトリを指定します。フィールドが指定されていないか、相対ディレクトリとして指定されている場合、ログ ディレクトリはセクション`global`の`log_dir`設定に従って生成されます。
-   `numa_node` : NUMA ポリシーをインスタンスに割り当てます。このフィールドを指定する前に、ターゲット マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドが指定されている場合、 cpubind および membind ポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)を使用して割り当てられます。このフィールドは文字列型です。フィールド値は、「0,1」などの NUMA ノードの ID です。
-   `config_file` : ローカルファイルを指定します。指定されたファイルは、クラスター構成の初期化フェーズ中に、Alertmanager の構成としてターゲット マシンに送信されます。
-   `os` : `host`フィールドで指定されたマシンのオペレーティング システム。フィールドが指定されていない場合、デフォルト値は`global`セクションで設定された`os`値です。
-   `arch` : `host`フィールドで指定されたマシンのアーキテクチャ。フィールドが指定されていない場合、デフォルト値は`global`セクションで設定された`arch`値です。
-   `resource_control` : このサービスのリソース制御。このフィールドを指定した場合、このフィールドの設定は`global`セクションの`resource_control`の設定とマージされ(2つのフィールドが重複している場合は、このフィールドの設定が有効になります)、systemdの設定ファイルが生成および配布されます。 `host`フィールドで指定されたマシンに送信します。このフィールドの設定ルールは、セクション`global`の`resource_control`と同じです。

`alertmanager_servers`では、デプロイメントの完了後に次のフィールドを変更することはできません。

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
