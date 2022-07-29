---
title: Customize Configurations of Monitoring Servers
summary: Learn how to customize the configurations of monitoring servers managed by TiUP
---

# 監視サーバーの構成をカスタマイズする {#customize-configurations-of-monitoring-servers}

TiUPを使用してTiDBクラスタをデプロイすると、TiUPはPrometheus、Grafana、Alertmanagerなどの監視サーバーもデプロイします。それまでの間、このクラスタをスケールアウトすると、TiUPは新しいノードも監視スコープに追加します。

上記の監視サーバーの構成をカスタマイズするには、以下の手順に従って、TiDBクラスタのtopology.yamlに関連する構成アイテムを追加します。

> **ノート：**
>
> -   監視サーバーの構成ファイルを直接変更しないでください。これらの変更は、展開、スケールアウト、スケールイン、リロードなどの後のTiUP操作によって上書きされるためです。
>
> -   監視サーバーがTiUPによって展開および管理されていない場合は、このドキュメントを参照する代わりに、監視サーバーの構成ファイルを直接変更できます。
>
> -   この機能は、TiUPv1.9.0以降でサポートされています。したがって、この機能を使用する前に、TiUPのバージョンを確認してください。

## Prometheus構成をカスタマイズする {#customize-prometheus-configurations}

現在、TiUPはPrometheusルールのカスタマイズと構成ファイルのスクレイプをサポートしています。

### Prometheusルール構成をカスタマイズする {#customize-prometheus-rule-configuration}

1.  ルール構成ファイルをカスタマイズして、TiUPが配置されているマシンのディレクトリの下に配置します。

2.  topology.yamlファイルで、カスタマイズされたルール構成ファイルのディレクトリに`rule_dir`を設定します。

    以下は、topology.yamlファイルのmonitoring_serversの構成例です。

    ```
    # # Server configs are used to specify the configuration of Prometheus Server.
    monitoring_servers:
      # # The ip address of the Monitoring Server.
    - host: 127.0.0.1
      rule_dir: /home/tidb/prometheus_rule   # prometheus rule dir on TiUP machine
    ```

上記の構成が完了した後、TiDBクラスタを展開、スケールアウト、スケールイン、またはリロードすると、TiUPはカスタマイズされたルール構成を`rule_dir` （たとえば、 `/home/tidb/prometheus_rule` ）からロードし、それらをPrometheusサーバーに送信してデフォルトのルール構成を置き換えます。 。

### Prometheusスクレイピング構成をカスタマイズする {#customize-prometheus-scrape-configuration}

1.  TiDBクラスタのtopology.yamlファイルを開きます。

2.  `monitoring_servers`構成で、 `additional_scrape_conf`フィールドを追加します。

    以下は、topology.yamlファイルのmonitoring_serversの構成例です。

    ```
    monitoring_servers:
    - host: xxxxxxx
    ssh_port: 22
    port: 9090
    deploy_dir: /tidb-deploy/prometheus-9090
    data_dir: /tidb-data/prometheus-9090
    log_dir: /tidb-deploy/prometheus-9090/log
    external_alertmanagers: []
    arch: amd64
    os: linux
    additional_scrape_conf:
      metric_relabel_configs:
        - source_labels: [__name__]
            separator: ;
            regex: tikv_thread_nonvoluntary_context_switches|tikv_thread_voluntary_context_switches|tikv_threads_io_bytes_total
            action: drop
        - source_labels: [__name__,name]
            separator: ;
            regex: tikv_thread_cpu_seconds_total;(tokio|rocksdb).+
            action: drop
    ```

上記の構成が完了した後、TiDBクラスタをデプロイ、スケールアウト、スケールイン、またはリロードすると、TiUPはPrometheus構成ファイルの対応するパラメーターに`additional_scrape_conf`フィールドを追加します。

## Grafana構成をカスタマイズする {#customize-grafana-configurations}

現在、TiUPはGrafanaダッシュボードおよびその他の構成のカスタマイズをサポートしています。

### Grafanaダッシュボードをカスタマイズする {#customize-grafana-dashboard}

1.  Grafanaダッシュボードの構成ファイルをカスタマイズし、TiUPが配置されているマシンのディレクトリの下に配置します。

2.  topology.yamlファイルで、カスタマイズされたダッシュボード構成ファイルのディレクトリに`dashboard_dir`を設定します。

    以下は、topology.yamlファイルのgrafana_serversの設定例です。

    ```
    # # Server configs are used to specify the configuration of Grafana Servers.
    grafana_servers:
      # # The ip address of the Grafana Server.
     - host: 127.0.0.1
     dashboard_dir: /home/tidb/dashboards   # grafana dashboard dir on TiUP machine
    ```

上記の構成が完了した後、TiDBクラスタをデプロイ、スケールアウト、スケールイン、またはリロードすると、TiUPはカスタマイズされたダッシュボード構成を`dashboard_dir` （たとえば、 `/home/tidb/dashboards` ）からロードし、構成をGrafanaサーバーに送信してデフォルトのダッシュボードを置き換えます構成。

### 他のGrafana構成をカスタマイズする {#customize-other-grafana-configurations}

1.  TiDBクラスタのtopology.yamlファイルを開きます。

2.  `grafana_servers`つの構成に他の構成アイテムを追加します。

    以下は、topology.yamlファイルの`[log.file] level`フィールドと`smtp`フィールドの構成例です。

    ```
    # # Server configs are used to specify the configuration of Grafana Servers.
    grafana_servers:
    # # The ip address of the Grafana Server.
    - host: 127.0.0.1
        config:
        log.file.level: warning
        smtp.enabled: true
        smtp.host: {IP}:{port}
        smtp.user: example@pingcap.com
        smtp.password: {password}
        smtp.skip_verify: true
    ```

上記の構成が完了した後、TiDBクラスタをデプロイ、スケールアウト、スケールイン、またはリロードすると、TiUPは`config`フィールドをGrafana構成ファイル`grafana.ini`に追加します。

## Alertmanager構成をカスタマイズする {#customize-alertmanager-configurations}

現在、TiUPはAlertmanagerのリスニングアドレスのカスタマイズをサポートしています。

TiUPによってデプロイされたAlertmanagerは、デフォルトで`alertmanager_servers.host`をリッスンします。プロキシを使用している場合、Alertmanagerにアクセスすることはできません。この問題に対処するには、クラスタ構成ファイルtopology.yamlに`listen_host`を追加して、リスニングアドレスを指定できます。推奨値は0.0.0.0です。

次の例では、 `listen_host`フィールドを0.0.0.0に設定します。

```
alertmanager_servers:
  # # The ip address of the Alertmanager Server.
  - host: 172.16.7.147
    listen_host: 0.0.0.0
    # # SSH port of the server.
    ssh_port: 22
```

上記の構成が完了した後、TiDBクラスタをデプロイ、スケールアウト、スケールイン、またはリロードすると、TiUPはAlertmanagerスタートアップパラメーターの`listen_host`フィールドを`--web.listen-address`に追加します。
