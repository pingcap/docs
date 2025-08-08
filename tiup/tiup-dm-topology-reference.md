---
title: Topology Configuration File for DM Cluster Deployment Using TiUP
summary: TiUPを使用して TiDB データ移行 (DM) クラスターをデプロイまたは拡張するには、クラスターのグローバル設定、サーバー設定、マスターサーバー、ワーカーサーバー、モニタリングサーバー、Grafana サーバー、および Alertmanager サーバーを記述するトポロジファイルが必要です。各セクションには、設定用の特定のフィールドが含まれています。トポロジファイルの構造は、global、server_configs、master_servers、worker_servers、monitoring_servers、grafana_servers、およびalertmanager_servers で構成されます。各セクションには、デプロイと設定のための独自の設定可能なフィールドセットがあります。
---

# TiUPを使用した DMクラスタ展開のトポロジコンフィグレーションファイル {#topology-configuration-file-for-dm-cluster-deployment-using-tiup}

TiDBデータ移行（DM）クラスターをデプロイまたは拡張するには、クラスタートポロジを記述するトポロジファイル（ [サンプル](https://github.com/pingcap/tiup/blob/master/embed/examples/dm/topology.example.yaml) ）を提供する必要があります。

同様に、クラスタトポロジを変更するには、トポロジファイルに変更を加える必要があります。違いは、クラスタのデプロイ後は、トポロジファイル内のフィールドの一部しか変更できないことです。このドキュメントでは、トポロジファイルの各セクションと、各セクション内の各フィールドについて説明します。

## ファイル構造 {#file-structure}

TiUPを使用した DM クラスターのデプロイメントのトポロジ構成ファイルには、次のセクションが含まれる場合があります。

-   [グローバル](#global) : クラスターのグローバル設定。一部の設定項目はクラスターのデフォルト値を使用しますが、インスタンスごとに個別に設定できます。
-   [サーバー構成](#server_configs) : コンポーネントのグローバル設定。各コンポーネントを個別に設定できます。インスタンスに同じキーの設定項目がある場合、そのインスタンスの設定項目が有効になります。
-   [マスターサーバー](#master_servers) : DMマスターインスタンスの構成。この構成では、DMコンポーネントのマスターサービスがデプロイされるマシンを指定します。
-   [ワーカーサーバー](#worker_servers) : DMワーカーインスタンスの設定。この設定では、DMコンポーネントのワーカーサービスがデプロイされるマシンを指定します。
-   [監視サーバー](#monitoring_servers) : Prometheusインスタンスがデプロイされるマシンを指定します。TiUPは複数のPrometheusインスタンスのデプロイをサポートしていますが、最初のインスタンスのみが使用されます。
-   [grafana_servers](#grafana_servers) : Grafanaインスタンスの設定。この設定では、Grafanaインスタンスがデプロイされるマシンを指定します。
-   [アラートマネージャーサーバー](#alertmanager_servers) : Alertmanagerインスタンスの設定。この設定では、Alertmanagerインスタンスがデプロイされるマシンを指定します。

### <code>global</code> {#code-global-code}

`global`セクションはクラスターのグローバル構成に対応し、次のフィールドがあります。

-   `user` : デプロイされたクラスタを起動するユーザー。デフォルト値は「tidb」です。2 `<user>`に指定されたユーザーがターゲットマシン上に存在しない場合、 TiUP は自動的にユーザーの作成を試みます。
-   `group` : ユーザーが自動作成された際に所属するユーザーグループ。デフォルト値は`<user>`フィールドと同じです。指定されたグループが存在しない場合は、自動的に作成されます。
-   `ssh_port` : 操作のためにターゲットマシンに接続するためのSSHポート。デフォルト値は「22」です。
-   `deploy_dir` : 各コンポーネントのデプロイメントディレクトリ。デフォルト値は「deploy」です。構築ルールは以下のとおりです。
    -   絶対パス`deploy_dir`インスタンス レベルで構成されている場合、実際のデプロイメント ディレクトリはインスタンスに対して構成されている`deploy_dir`なります。
    -   各インスタンスに対して`deploy_dir`設定しない場合、デフォルト値は相対パス`<component-name>-<component-port>`なります。
    -   `global.deploy_dir`絶対パスに設定すると、コンポーネントは`<global.deploy_dir>/<instance.deploy_dir>`ディレクトリにデプロイされます。
    -   `global.deploy_dir`相対パスに設定すると、コンポーネントは`/home/<global.user>/<global.deploy_dir>/<instance.deploy_dir>`ディレクトリにデプロイされます。
-   `data_dir` : データディレクトリ。デフォルト値は「data」です。構築ルールは以下のとおりです。
    -   絶対パス`data_dir`インスタンス レベルで構成されている場合、実際のデータ ディレクトリはインスタンスに構成されている`data_dir`なります。
    -   各インスタンスに対して`data_dir`が設定されていない場合、デフォルト値は`<global.data_dir>`なります。
    -   `data_dir`相対パスに設定されている場合、コンポーネントデータは`<deploy_dir>/<data_dir>`に保存されます。 `<deploy_dir>`の構築規則については、 `deploy_dir`フィールドの構築規則を参照してください。
-   `log_dir` : データディレクトリ。デフォルト値は「log」です。構築ルールは以下のとおりです。
    -   インスタンス レベルで絶対パス`log_dir`が設定されている場合、実際のログ ディレクトリはインスタンスに設定されている`log_dir`なります。
    -   各インスタンスについて、ユーザーが`log_dir`設定しない場合、デフォルト値は`<global.log_dir>`なります。
    -   `log_dir`が相対パスの場合、コンポーネントログは`<deploy_dir>/<log_dir>`に保存されます。 `<deploy_dir>`の構築ルールについては、 `deploy_dir`フィールドの構築ルールを参照してください。
-   `os` : ターゲットマシンのオペレーティングシステム。このフィールドは、ターゲットマシンにプッシュされるコンポーネントをどのオペレーティングシステムに適応させるかを制御します。デフォルト値は「linux」です。
-   `arch` : ターゲットマシンのCPUアーキテクチャ。このフィールドは、ターゲットマシンにプッシュされるバイナリパッケージをどのプラットフォームに適合させるかを制御します。サポートされている値は「amd64」と「arm64」です。デフォルト値は「amd64」です。
-   `resource_control` : ランタイムリソース制御。このフィールドのすべての設定は、systemd のサービスファイルに書き込まれます。デフォルトでは制限はありません。制御可能なリソースは以下のとおりです。
    -   `memory_limit` : 実行時の最大メモリを制限します。例えば、「2G」は最大2GBのメモリが使用できることを意味します。
    -   `cpu_quota` : 実行時のCPU使用率の上限を制限します。例: 「200%」
    -   `io_read_bandwidth_max` : ディスク読み取りの最大I/O帯域幅を制限します。例： `"/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0:0 100M"` 。
    -   `io_write_bandwidth_max` : ディスク書き込みの最大I/O帯域幅を制限します。例： `"/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0:0 100M"` 。
    -   `limit_core` : コアダンプのサイズを制御します。

`global`構成例:

```yaml
global:
  user: "tidb"
  resource_control:
    memory_limit: "2G"
```

この例では、構成により、クラスターを起動するために`tidb`ユーザーが使用され、各コンポーネントの実行時に最大 2 GB のメモリに制限されることが指定されています。

### <code>server_configs</code> {#code-server-configs-code}

`server_configs` `server_configs`サービスの設定と各コンポーネントの設定ファイルの生成に使用されます。2 セクションと同様に、 `global`セクションの設定は、インスタンス内の同じキーを持つ設定によって上書きできます。6 `server_configs`は主に以下のフィールドが含まれます。

-   `master` : DMマスターサービスに関連する設定。サポートされているすべての設定項目については、 [DMマスターコンフィグレーションファイル](/dm/dm-master-configuration-file.md)参照してください。
-   `worker` : DM ワーカー サービスに関連する構成。サポートされているすべての構成項目については、 [DMワーカーコンフィグレーションファイル](/dm/dm-worker-configuration-file.md)参照してください。

`server_configs`構成の例は次のとおりです。

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

`master_servers` 、DMコンポーネントのマスターノードがデプロイされるマシンを指定します。また、各マシンのサービス構成を指定することもできます`master_servers`配列です。各配列要素には以下のフィールドが含まれます。

-   `host` : デプロイ先のマシンを指定します。このフィールド値はIPアドレスで、必須です。
-   `ssh_port` : 操作のためにターゲットマシンに接続するためのSSHポートを指定します。このフィールドが指定されていない場合は、セクション`global`の`ssh_port`使用されます。
-   `name` : DMマスターインスタンスの名前を指定します。名前はインスタンスごとに一意である必要があります。一意でない場合、クラスターをデプロイできません。
-   `port` : DMマスターがサービスを提供するポートを指定します。デフォルト値は「8261」です。
-   `peer_port` : DMマスター間の通信ポートを指定します。デフォルト値は「8291」です。
-   `deploy_dir` : デプロイメントディレクトリを指定します。このフィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、デプロイメントディレクトリは`global`セクションの`deploy_dir`設定に従って生成されます。
-   `data_dir` : データディレクトリを指定します。このフィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、データディレクトリはセクション`global`の`data_dir`設定に従って生成されます。
-   `log_dir` : ログディレクトリを指定します。このフィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、ログディレクトリはセクション`global`の`log_dir`設定に従って生成されます。
-   `numa_node` : インスタンスにNUMAポリシーを割り当てます。このフィールドを指定する前に、ターゲットマシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドを指定した場合、cpubindおよびmembindポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)使用して割り当てられます。このフィールドは文字列型です。フィールド値はNUMAノードのID（例：&quot;0,1&quot;）です。
-   `config` ：このフィールドの設定ルールは、セクション`server_configs`の`master`と同じです。6を指定した場合、セクション`config` `config`設定が`server_configs` `master`の設定とマージされ（2つのフィールドが重複している場合は、このフィールドの設定が有効になります）、設定ファイルが生成され、セクション`host`で指定されたマシンに配布されます。
-   `os` : `host`のフィールドで指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`番目のセクションで設定された`os`値です。
-   `arch` : `host`のフィールドで指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`番目のセクションで設定された`arch`値になります。
-   `resource_control` : このサービスにおけるリソース制御。このフィールドが指定された場合、このフィールドの設定はセクション`global`の`resource_control`の設定とマージされ（2つのフィールドが重複している場合は、このフィールドの設定が有効になります）、systemdの設定ファイルが生成され、セクション`host`で指定されたマシンに配布されます。このフィールドの設定ルールは、セクション`global`の`resource_control`の設定ルールと同じです。
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

`master_servers`構成の例は次のとおりです。

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

`worker_servers` 、DMコンポーネントのマスターノードがデプロイされるマシンを指定します。また、各マシンのサービス構成を指定することもできます`worker_servers`配列です。各配列要素には以下のフィールドが含まれます。

-   `host` : デプロイ先のマシンを指定します。このフィールド値はIPアドレスで、必須です。
-   `ssh_port` : 操作のためにターゲットマシンに接続するためのSSHポートを指定します。このフィールドが指定されていない場合は、セクション`global`の`ssh_port`使用されます。
-   `name` : DMワーカーインスタンスの名前を指定します。名前はインスタンスごとに一意である必要があります。一意でない場合、クラスターをデプロイできません。
-   `port` : DMワーカーがサービスを提供するポートを指定します。デフォルト値は「8262」です。
-   `deploy_dir` : デプロイメントディレクトリを指定します。このフィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、デプロイメントディレクトリは`global`セクションの`deploy_dir`設定に従って生成されます。
-   `data_dir` : データディレクトリを指定します。このフィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、データディレクトリはセクション`global`の`data_dir`設定に従って生成されます。
-   `log_dir` : ログディレクトリを指定します。このフィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、ログディレクトリはセクション`global`の`log_dir`設定に従って生成されます。
-   `numa_node` : インスタンスにNUMAポリシーを割り当てます。このフィールドを指定する前に、ターゲットマシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドを指定した場合、cpubindおよびmembindポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)使用して割り当てられます。このフィールドは文字列型です。フィールド値はNUMAノードのID（例：&quot;0,1&quot;）です。
-   `config` ：このフィールドの設定ルールは、セクション`server_configs`の`worker`と同じです。6を指定した場合、セクション`config` `config`設定が`server_configs` `worker`の設定とマージされ（2つのフィールドが重複している場合は、このフィールドの設定が有効になります）、設定ファイルが生成され、セクション`host`で指定されたマシンに配布されます。
-   `os` : `host`のフィールドで指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`番目のセクションで設定された`os`値です。
-   `arch` : `host`のフィールドで指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`番目のセクションで設定された`arch`値になります。
-   `resource_control` : このサービスにおけるリソース制御。このフィールドが指定された場合、このフィールドの設定はセクション`global`の`resource_control`の設定とマージされ（2つのフィールドが重複している場合は、このフィールドの設定が有効になります）、systemdの設定ファイルが生成され、セクション`host`で指定されたマシンに配布されます。このフィールドの設定ルールは、セクション`global`の`resource_control`の設定ルールと同じです。

`worker_servers`セクションでは、デプロイメントが完了した後は、次のフィールドを変更することはできません。

-   `host`
-   `name`
-   `port`
-   `deploy_dir`
-   `data_dir`
-   `log_dir`
-   `arch`
-   `os`

`worker_servers`構成の例は次のとおりです。

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

`monitoring_servers` 、Prometheus サービスがデプロイされるマシンを指定します。また、マシン上のサービス設定も指定できます`monitoring_servers`配列です。各配列要素には以下のフィールドが含まれます。

-   `host` : デプロイ先のマシンを指定します。このフィールド値はIPアドレスで、必須です。
-   `ssh_port` : 操作のためにターゲットマシンに接続するためのSSHポートを指定します。このフィールドが指定されていない場合は、セクション`global`の`ssh_port`使用されます。
-   `port` : Prometheusがサービスを提供するポートを指定します。デフォルト値は「9090」です。
-   `deploy_dir` : デプロイメントディレクトリを指定します。このフィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、デプロイメントディレクトリは`global`セクションの`deploy_dir`設定に従って生成されます。
-   `data_dir` : データディレクトリを指定します。このフィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、データディレクトリはセクション`global`の`data_dir`設定に従って生成されます。
-   `log_dir` : ログディレクトリを指定します。このフィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、ログディレクトリはセクション`global`の`log_dir`設定に従って生成されます。
-   `numa_node` : インスタンスにNUMAポリシーを割り当てます。このフィールドを指定する前に、対象マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドを指定した場合、cpubindおよびmembindポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)使用して割り当てられます。このフィールドは文字列型です。フィールド値はNUMAノードのID（例：&quot;0,1&quot;）です。
-   `storage_retention` : Prometheus監視データの保持期間を指定します。デフォルト値は「15日」です。
-   `rule_dir` : `*.rules.yml`のファイルすべてが保存されているローカルディレクトリを指定します。指定されたディレクトリ内のファイルは、クラスター構成の初期化フェーズでPrometheusルールとしてターゲットマシンに送信されます。
-   `remote_config` : Prometheusデータのリモートへの書き込み、またはリモートからのデータの読み取りをサポートします。このフィールドには2つの設定があります。
    -   `remote_write` : Prometheus ドキュメント[`&#x3C;remote_write>`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write)を参照してください。
    -   `remote_read` : Prometheus ドキュメント[`&#x3C;remote_read>`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_read)を参照してください。
-   `external_alertmanagers` : フィールド`external_alertmanagers`が設定されている場合、Prometheusはクラスター外のAlertmanagerに構成動作を通知します。このフィールドは配列であり、各要素は外部Alertmanagerであり、フィールド`host`とフィールド`web_port`で構成されます。
-   `os` : `host`のフィールドで指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`番目のセクションで設定された`os`値です。
-   `arch` : `host`のフィールドで指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`番目のセクションで設定された`arch`値になります。
-   `resource_control` : このサービスにおけるリソース制御。このフィールドが指定された場合、このフィールドの設定はセクション`global`の`resource_control`の設定とマージされ（2つのフィールドが重複している場合は、このフィールドの設定が有効になります）、systemdの設定ファイルが生成され、セクション`host`で指定されたマシンに配布されます。このフィールドの設定ルールは、セクション`global`の`resource_control`の設定ルールと同じです。

`monitoring_servers`セクションでは、デプロイメントが完了した後は、次のフィールドを変更することはできません。

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

`grafana_servers` 、Grafana サービスがデプロイされるマシンを指定します。また、マシン上のサービス設定も指定できます`grafana_servers`配列です。各配列要素には以下のフィールドが含まれます。

-   `host` : デプロイ先のマシンを指定します。このフィールド値はIPアドレスで、必須です。
-   `ssh_port` : 操作のためにターゲットマシンに接続するためのSSHポートを指定します。このフィールドが指定されていない場合は、セクション`global`の`ssh_port`使用されます。
-   `port` : Grafanaがサービスを提供するポートを指定します。デフォルト値は「3000」です。
-   `deploy_dir` : デプロイメントディレクトリを指定します。このフィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、デプロイメントディレクトリは`global`セクションの`deploy_dir`設定に従って生成されます。
-   `os` : `host`のフィールドで指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`番目のセクションで設定された`os`値です。
-   `arch` : `host`のフィールドで指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`番目のセクションで設定された`arch`値になります。
-   `username` : Grafana ログイン画面のユーザー名を指定します。
-   `password` : Grafana の対応するパスワードを指定します。
-   `dashboard_dir` : `dashboard(*.json)`のファイルすべてが保存されているローカルディレクトリを指定します。指定されたディレクトリ内のファイルは、クラスター構成の初期化フェーズ中にGrafanaダッシュボードとしてターゲットマシンに送信されます。
-   `resource_control` : このサービスにおけるリソース制御。このフィールドが指定された場合、このフィールドの設定はセクション`global`の`resource_control`の設定とマージされ（2つのフィールドが重複している場合は、このフィールドの設定が有効になります）、systemdの設定ファイルが生成され、セクション`host`で指定されたマシンに配布されます。このフィールドの設定ルールは、セクション`global`の`resource_control`の設定ルールと同じです。

> **注記：**
>
> `dashboard_dir`フィールドが`grafana_servers`設定されている場合、クラスターの名前を変更する`tiup cluster rename`コマンドを実行した後、次の操作を実行する必要があります。
>
> 1.  ローカルの`dashboards`ディレクトリで、 `datasource`フィールドの値を新しいクラスター名に更新します ( `datasource`クラスター名に基づいて名前が付けられます)。
> 2.  `tiup cluster reload -R grafana`コマンドを実行します。

`grafana_servers`では、デプロイメントが完了した後は、次のフィールドを変更できません。

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

`alertmanager_servers` 、Alertmanagerサービスがデプロイされるマシンを指定します。また、各マシンのサービス構成を指定することもできます`alertmanager_servers`は配列です。各配列要素には以下のフィールドが含まれます。

-   `host` : デプロイ先のマシンを指定します。このフィールド値はIPアドレスで、必須です。
-   `ssh_port` : 操作のためにターゲットマシンに接続するためのSSHポートを指定します。このフィールドが指定されていない場合は、セクション`global`の`ssh_port`使用されます。
-   `web_port` : AlertmanagerがWebサービスを提供するポートを指定します。デフォルト値は「9093」です。
-   `cluster_port` : Alertmanager間の通信ポートを指定します。デフォルト値は「9094」です。
-   `deploy_dir` : デプロイメントディレクトリを指定します。このフィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、デプロイメントディレクトリは`global`セクションの`deploy_dir`設定に従って生成されます。
-   `data_dir` : データディレクトリを指定します。このフィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、データディレクトリはセクション`global`の`data_dir`設定に従って生成されます。
-   `log_dir` : ログディレクトリを指定します。このフィールドが指定されていない場合、または相対ディレクトリとして指定されている場合、ログディレクトリはセクション`global`の`log_dir`設定に従って生成されます。
-   `numa_node` : インスタンスにNUMAポリシーを割り当てます。このフィールドを指定する前に、対象マシンに[ヌマクトル](https://linux.die.net/man/8/numactl)インストールされていることを確認する必要があります。このフィールドを指定した場合、cpubindおよびmembindポリシーは[ヌマクトル](https://linux.die.net/man/8/numactl)使用して割り当てられます。このフィールドは文字列型です。フィールド値はNUMAノードのID（例：&quot;0,1&quot;）です。
-   `config_file` : ローカルファイルを指定します。指定されたファイルは、クラスター構成の初期化フェーズ中に、Alertmanager の構成としてターゲットマシンに送信されます。
-   `os` : `host`のフィールドで指定されたマシンのオペレーティングシステム。このフィールドが指定されていない場合、デフォルト値は`global`番目のセクションで設定された`os`値です。
-   `arch` : `host`のフィールドで指定されたマシンのアーキテクチャ。このフィールドが指定されていない場合、デフォルト値は`global`番目のセクションで設定された`arch`値になります。
-   `resource_control` : このサービスにおけるリソース制御。このフィールドが指定された場合、このフィールドの設定はセクション`global`の`resource_control`の設定とマージされ（2つのフィールドが重複している場合は、このフィールドの設定が有効になります）、systemdの設定ファイルが生成され、セクション`host`で指定されたマシンに配布されます。このフィールドの設定ルールは、セクション`global`の`resource_control`の設定ルールと同じです。

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
