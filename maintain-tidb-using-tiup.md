---
title: TiUP Common Operations
summary: TiUPを使用して TiDB クラスターを操作および保守するための一般的な操作を学習します。
---

# TiUP共通操作 {#tiup-common-operations}

このドキュメントでは、 TiUPを使用して TiDB クラスターを操作および保守する場合の一般的な操作について説明します。

## クラスターリストをビュー {#view-the-cluster-list}

TiUPクラスタコンポーネントを使用して、複数の TiDB クラスタを管理できます。TiDB クラスタがデプロイされると、そのクラスタはTiUPクラスタリストに表示されます。

リストを表示するには、次のコマンドを実行します。

```bash
tiup cluster list
```

## クラスターを起動する {#start-the-cluster}

TiDB クラスター内のコンポーネントは次の順序で起動されます。

**PD &gt; TiKV &gt; TiDB &gt; TiFlash &gt; TiCDC &gt; Prometheus &gt; Grafana &gt; Alertmanager**

クラスターを起動するには、次のコマンドを実行します。

```bash
tiup cluster start ${cluster-name}
```

> **注記：**
>
> `${cluster-name}`クラスター名に置き換えてください。クラスター名を忘れた場合は、 `tiup cluster list`実行して確認してください。

コマンドに`-R`または`-N`パラメータを追加することで、一部のコンポーネントのみを起動できます。例：

-   このコマンドは PDコンポーネントのみを起動します。

    ```bash
    tiup cluster start ${cluster-name} -R pd
    ```

-   このコマンドは、ホスト`1.2.3.4`と`1.2.3.5` PD コンポーネントのみを起動します。

    ```bash
    tiup cluster start ${cluster-name} -N 1.2.3.4:2379,1.2.3.5:2379
    ```

> **注記：**
>
> `-R`または`-N`パラメータを使用して指定されたコンポーネントを起動する場合は、起動順序が正しいことを確認してください。例えば、PDコンポーネントをTiKVコンポーネントより先に起動してください。そうしないと、起動に失敗する可能性があります。

## クラスターのステータスをビュー {#view-the-cluster-status}

クラスターを起動したら、各コンポーネントのステータスを確認し、正常に動作していることを確認してくださいTiUPには`display`コマンドが用意されているため、コンポーネントのステータスを確認するためにすべてのマシンにログインする必要はありません。

```bash
tiup cluster display ${cluster-name}
```

## 設定を変更する {#modify-the-configuration}

クラスタの稼働中にコンポーネントのパラメータを変更する必要がある場合は、コマンド`edit-config`を実行してください。詳細な手順は次のとおりです。

1.  クラスターの構成ファイルを編集モードで開きます。

    ```bash
    tiup cluster edit-config ${cluster-name}
    ```

2.  パラメータを設定します。

    -   構成がコンポーネントに対してグローバルに有効な場合は、 `server_configs`を編集します。

            server_configs:
              tidb:
                log.slow-threshold: 300

    -   特定のノードで設定を有効にする場合は、ノードの`config`で設定を編集します。

            tidb_servers:
            - host: 10.0.1.11
              port: 4000
              config:
                  log.slow-threshold: 300

    パラメータの形式については[TiUPパラメータテンプレート](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml)参照してください。

    **構成項目の階層を表すには、 . を使用します`.`**

    コンポーネントの構成パラメータの詳細については、 [TiDB `config.toml.example`](https://github.com/pingcap/tidb/blob/release-8.5/pkg/config/config.toml.example) 、 [TiKV `config.toml.example`](https://github.com/tikv/tikv/blob/release-8.5/etc/config-template.toml) 、および[PD `config.toml.example`](https://github.com/tikv/pd/blob/release-8.5/conf/config.toml)を参照してください。

3.  `reload`コマンドを実行して、構成をローリング更新し、対応するコンポーネントを再起動します。

    ```bash
    tiup cluster reload ${cluster-name} [-N <nodes>] [-R <roles>]
    ```

### 例 {#example}

tidb-server でトランザクション サイズ制限パラメータ ( [パフォーマンス](https://github.com/pingcap/tidb/blob/release-8.5/pkg/config/config.toml.example)モジュールの`txn-total-size-limit` ) を`1G`に設定する場合は、次のように設定を編集します。

    server_configs:
      tidb:
        performance.txn-total-size-limit: 1073741824

次に、 `tiup cluster reload ${cluster-name} -R tidb`コマンドを実行して、TiDBコンポーネントをローリング再起動します。

## 修正プログラムパッケージに置き換える {#replace-with-a-hotfix-package}

通常のアップグレードについては、 [TiUPを使用して TiDB をアップグレードする](/upgrade-tidb-using-tiup.md)参照してください。ただし、デバッグなどの一部のシナリオでは、現在実行中のコンポーネントを一時パッケージに置き換える必要がある場合があります。これを行うには、 `patch`コマンドを使用します。

```bash
tiup cluster patch --help
```

    Replace the remote package with a specified package and restart the service

    Usage:
      cluster patch <cluster-name> <package-path> [flags]

    Flags:
      -h, --help                   help for patch
      -N, --node strings           Specify the nodes
          --overwrite              Use this package in the future scale-out operations
      -R, --role strings           Specify the role
          --transfer-timeout int   Timeout in seconds when transferring PD and TiKV store leaders (default 600)

    Global Flags:

          --native-ssh        Use the system's native SSH client
          --wait-timeout int  Timeout of waiting the operation
          --ssh-timeout int   Timeout in seconds to connect host via SSH, ignored for operations that don't need an SSH connection. (default 5)
      -y, --yes               Skip all confirmations and assumes 'yes'

TiDB ホットフィックス パッケージが`/tmp/tidb-hotfix.tar.gz`にあり、クラスター内のすべての TiDB パッケージを置き換える場合は、次のコマンドを実行します。

```bash
tiup cluster patch test-cluster /tmp/tidb-hotfix.tar.gz -R tidb
```

クラスター内の 1 つの TiDB パッケージのみを置き換えることもできます。

```bash
tiup cluster patch test-cluster /tmp/tidb-hotfix.tar.gz -N 172.16.4.5:4000
```

## クラスターの名前を変更する {#rename-the-cluster}

クラスターをデプロイして起動した後、 `tiup cluster rename`コマンドを使用してクラスターの名前を変更できます。

```bash
tiup cluster rename ${cluster-name} ${new-name}
```

> **注記：**
>
> -   クラスターの名前を変更する操作により、監視システム (Prometheus および Grafana) が再起動されます。
> -   クラスターの名前を変更した後、古いクラスター名を持つパネルがGrafanaに残る場合があります。これらのパネルは手動で削除する必要があります。

## クラスターを停止する {#stop-the-cluster}

TiDB クラスター内のコンポーネントは次の順序で停止されます (監視コンポーネントも停止されます)。

**アラートマネージャー &gt; Grafana &gt; Prometheus &gt; TiCDC &gt; TiFlash &gt; TiDB &gt; TiKV &gt; PD**

クラスターを停止するには、次のコマンドを実行します。

```bash
tiup cluster stop ${cluster-name}
```

`start`コマンドと同様に、 `stop`コマンドでも`-R`または`-N`パラメータを追加することで、一部のコンポーネントを停止できます。例:

-   このコマンドは TiDBコンポーネントのみを停止します。

    ```bash
    tiup cluster stop ${cluster-name} -R tidb
    ```

-   このコマンドは、ホスト`1.2.3.4`と`1.2.3.5`の TiDB コンポーネントのみを停止します。

    ```bash
    tiup cluster stop ${cluster-name} -N 1.2.3.4:4000,1.2.3.5:4000
    ```

## クラスターデータをクリーンアップする {#clean-up-cluster-data}

クラスタデータのクリーンアップ操作では、すべてのサービスが停止し、データディレクトリまたはログディレクトリがクリーンアップされます。この操作は元に戻すことができませんので、**慎重に**進めてください。

-   クラスター内のすべてのサービスのデータをクリーンアップしますが、ログは保持します。

    ```bash
    tiup cluster clean ${cluster-name} --data
    ```

-   クラスター内のすべてのサービスのログをクリーンアップしますが、データは保持します。

    ```bash
    tiup cluster clean ${cluster-name} --log
    ```

-   クラスター内のすべてのサービスのデータとログをクリーンアップします。

    ```bash
    tiup cluster clean ${cluster-name} --all
    ```

-   Prometheus 以外のすべてのサービスのログとデータをクリーンアップします。

    ```bash
    tiup cluster clean ${cluster-name} --all --ignore-role prometheus
    ```

-   `172.16.13.11:9000`インスタンスを除くすべてのサービスのログとデータをクリーンアップします。

    ```bash
    tiup cluster clean ${cluster-name} --all --ignore-node 172.16.13.11:9000
    ```

-   `172.16.13.12`ノードを除くすべてのサービスのログとデータをクリーンアップします。

    ```bash
    tiup cluster clean ${cluster-name} --all --ignore-node 172.16.13.12
    ```

## クラスターを破壊する {#destroy-the-cluster}

削除操作はサービスを停止し、データディレクトリとデプロイメントディレクトリをクリアします。この操作は元に戻すことができないため、**慎重に**進めてください。

```bash
tiup cluster destroy ${cluster-name}
```

## PrometheusからVictoriaMetricsへの切り替え {#switch-from-prometheus-to-victoriametrics}

大規模クラスターでは、Prometheus は多数のインスタンスを処理する際にパフォーマンスのボトルネックが発生する可能性があります。TiUP v1.16.3 以降では、監視コンポーネントを Prometheus から VictoriaMetrics (VM) に切り替えることで、スケーラビリティ、パフォーマンス、リソース消費量を削減できます。

### 新しいデプロイメント用に VictoriaMetrics を設定する {#set-up-victoriametrics-for-a-new-deployment}

デフォルトでは、 TiUP はメトリクス監視コンポーネントとして Prometheus を使用します。新しいデプロイメントで Prometheus の代わりに VictoriaMetrics を使用するには、トポロジファイルを次のように設定します。

```yaml
# Monitoring server configuration
monitoring_servers:
  # IP address of the monitoring server
  - host: ip_address
    ...
    prom_remote_write_to_vm: true
    enable_prom_agent_mode: true

# Grafana server configuration
grafana_servers:
  # IP address of the Grafana server
  - host: ip_address
    ...
    use_vm_as_datasource: true
```

### 既存のデプロイメントを VictoriaMetrics に移行する {#migrate-an-existing-deployment-to-victoriametrics}

実行中のインスタンスに影響を与えることなく移行を実行できます。既存のメトリクスはPrometheusに残り、 TiUPは新しいメトリクスをVictoriaMetricsに書き込みます。

#### VictoriaMetrics リモート書き込みを有効にする {#enable-victoriametrics-remote-write}

1.  クラスター構成を編集します。

    ```bash
    tiup cluster edit-config ${cluster-name}
    ```

2.  `monitoring_servers`の下で`prom_remote_write_to_vm`を`true`に設定します:

    ```yaml
    monitoring_servers:
      - host: ip_address
        ...
        prom_remote_write_to_vm: true
    ```

3.  変更を適用するには、構成を再ロードします。

    ```bash
    tiup cluster reload ${cluster-name} -R prometheus
    ```

#### デフォルトのデータソースをVictoriaMetricsに切り替える {#switch-the-default-data-source-to-victoriametrics}

1.  クラスター構成を編集します。

    ```bash
    tiup cluster edit-config ${cluster-name}
    ```

2.  `grafana_servers`の下で`use_vm_as_datasource`を`true`に設定します:

    ```yaml
    grafana_servers:
      - host: ip_address
        ...
        use_vm_as_datasource: true
    ```

3.  変更を適用するには、構成を再ロードします。

    ```bash
    tiup cluster reload ${cluster-name} -R grafana
    ```

#### 切り替え前に生成された履歴メトリックをビュー（オプション） {#view-historical-metrics-generated-before-the-switch-optional}

切り替え前に生成された履歴メトリックを表示する必要がある場合は、次のように Grafana のデータ ソースを切り替えます。

1.  クラスター構成を編集します。

    ```bash
    tiup cluster edit-config ${cluster-name}
    ```

2.  `grafana_servers`の下で、 `use_vm_as_datasource`コメントアウトします。

    ```yaml
    grafana_servers:
      - host: ip_address
        ...
        # use_vm_as_datasource: true
    ```

3.  変更を適用するには、構成をリロードします。

    ```bash
    tiup cluster reload ${cluster-name} -R grafana
    ```

4.  VictoriaMetrics に戻るには、 [デフォルトのデータソースをVictoriaMetricsに切り替える](#switch-the-default-data-source-to-victoriametrics)の手順を繰り返します。

### 古い指標とサービスをクリーンアップする {#clean-up-old-metrics-and-services}

古いメトリックの有効期限が切れていることを確認した後、以下の手順で冗長なサービスとファイルを削除できます。これは実行中のクラスターには影響しません。

#### Prometheusをエージェントモードに設定する {#set-prometheus-to-agent-mode}

1.  クラスター構成を編集します。

    ```bash
    tiup cluster edit-config ${cluster-name}
    ```

2.  `monitoring_servers`の下で、 `enable_prom_agent_mode`を`true`に設定し、 `prom_remote_write_to_vm`と`use_vm_as_datasource`正しく設定されていることを確認します。

    ```yaml
    monitoring_servers:
      - host: ip_address
        ...
        prom_remote_write_to_vm: true
        enable_prom_agent_mode: true
    grafana_servers:
      - host: ip_address
        ...
        use_vm_as_datasource: true
    ```

3.  変更を適用するには、構成をリロードします。

    ```bash
    tiup cluster reload ${cluster-name} -R prometheus
    ```

#### 期限切れのデータディレクトリを削除する {#remove-expired-data-directories}

1.  設定ファイルで、監視サーバーの`data_dir`パスを見つけます。

    ```yaml
    monitoring_servers:
      - host: ip_address
        ...
        data_dir: "/tidb-data/prometheus-8249"
    ```

2.  データディレクトリを削除します。

    ```bash
    rm -rf /tidb-data/prometheus-8249
    ```
