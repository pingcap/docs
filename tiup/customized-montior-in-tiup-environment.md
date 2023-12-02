---
title: Customize Configurations of Monitoring Servers
summary: Learn how to customize the configurations of monitoring servers managed by TiUP
---

# 監視サーバーの構成をカスタマイズする {#customize-configurations-of-monitoring-servers}

TiUPを使用して TiDB クラスターをデプロイすると、 TiUP はPrometheus、Grafana、Alertmanager などのモニタリング サーバーもデプロイします。その間、このクラスターをスケールアウトすると、 TiUP は新しいノードも監視スコープに追加します。

上記のモニタリング サーバーの構成をカスタマイズするには、以下の手順に従って、関連する構成項目を TiDB クラスターの topology.yaml に追加します。

> **注記：**
>
> -   監視サーバーの構成ファイルを直接変更しないでください。これらの変更は、デプロイメント、スケールアウト、スケールイン、リロードなどの後のTiUP操作によって上書きされるためです。
>
> -   モニタリング サーバーがTiUPによって展開および管理されていない場合は、このドキュメントを参照する代わりに、モニタリング サーバーの構成ファイルを直接変更できます。
>
> -   この機能はTiUP v1.9.0 以降でサポートされています。したがって、この機能を使用する前にTiUP のバージョンを確認してください。

## Prometheus 構成をカスタマイズする {#customize-prometheus-configurations}

現在、 TiUP はPrometheus ルールとスクレイプ構成ファイルのカスタマイズをサポートしています。

### Prometheus ルール構成をカスタマイズする {#customize-prometheus-rule-configuration}

1.  ルール設定ファイルをカスタマイズし、 TiUPが存在するマシンのディレクトリの下に配置します。

2.  topology.yaml ファイルで、カスタマイズされたルール構成ファイルのディレクトリに`rule_dir`を設定します。

    以下は、topology.yaml ファイル内のmonitoring_servers の構成例です。

        # # Server configs are used to specify the configuration of Prometheus Server.
        monitoring_servers:
          # # The ip address of the Monitoring Server.
        - host: 127.0.0.1
          rule_dir: /home/tidb/prometheus_rule   # prometheus rule dir on TiUP machine

前述の構成が完了した後、TiDB クラスターをデプロイ、スケールアウト、スケールイン、またはリロードすると、 TiUP はカスタマイズされたルール構成を`rule_dir` (たとえば、 `/home/tidb/prometheus_rule` ) からロードし、それらを Prometheus Server に送信して、デフォルトのルール構成を置き換えます。 。

### Prometheus のスクレイピング構成をカスタマイズする {#customize-prometheus-scrape-configuration}

1.  TiDB クラスターの topology.yaml ファイルを開きます。

2.  `monitoring_servers`の構成に`additional_scrape_conf`フィールドを追加します。

    以下は、topology.yaml ファイル内のmonitoring_servers の構成例です。

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

前述の構成が完了した後、TiDB クラスターをデプロイ、スケールアウト、スケールイン、またはリロードすると、 TiUP はPrometheus 構成ファイルの対応するパラメーターに`additional_scrape_conf`フィールドを追加します。

## Grafana 構成をカスタマイズする {#customize-grafana-configurations}

現在、 TiUP はGrafana ダッシュボードとその他の構成のカスタマイズをサポートしています。

### Grafana ダッシュボードをカスタマイズする {#customize-grafana-dashboard}

1.  Grafana ダッシュボードの構成ファイルをカスタマイズし、 TiUP が配置されているマシンのディレクトリの下に配置します。

2.  topology.yaml ファイルで、カスタマイズされたダッシュボード構成ファイルのディレクトリに`dashboard_dir`を設定します。

    以下は、topology.yaml ファイル内の grafana_servers の構成例です。

        # # Server configs are used to specify the configuration of Grafana Servers.
        grafana_servers:
          # # The ip address of the Grafana Server.
         - host: 127.0.0.1
         dashboard_dir: /home/tidb/dashboards   # grafana dashboard dir on TiUP machine

前述の構成が完了した後、TiDB クラスターをデプロイ、スケールアウト、スケールイン、またはリロードすると、 TiUP はカスタマイズされたダッシュボード構成を`dashboard_dir` (たとえば、 `/home/tidb/dashboards` ) からロードし、その構成を Grafana サーバーに送信してデフォルトのダッシュボードを置き換えます。構成。

### 他の Grafana 構成をカスタマイズする {#customize-other-grafana-configurations}

1.  TiDB クラスターの topology.yaml ファイルを開きます。

2.  `grafana_servers`の構成に他の構成項目を追加します。

    以下は、topology.yaml ファイルの`[log.file] level`フィールドと`smtp`フィールドの構成例です。

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

前述の構成が完了した後、TiDB クラスターをデプロイ、スケールアウト、スケールイン、またはリロードすると、 TiUP は`config`フィールドを Grafana 構成ファイル`grafana.ini`に追加します。

## Alertmanager 構成をカスタマイズする {#customize-alertmanager-configurations}

現在、 TiUP はAlertmanager のリスニング アドレスのカスタマイズをサポートしています。

TiUPによって展開された Alertmanager は、デフォルトで`alertmanager_servers.host`をリッスンします。プロキシを使用している場合は、Alertmanager にアクセスできません。この問題に対処するには、クラスター構成ファイル topology.yaml に`listen_host`追加して、リスニング アドレスを指定します。推奨値は 0.0.0.0 です。

次の例では、 `listen_host`フィールドを 0.0.0.0 に設定します。

    alertmanager_servers:
      # # The ip address of the Alertmanager Server.
      - host: 172.16.7.147
        listen_host: 0.0.0.0
        # # SSH port of the server.
        ssh_port: 22

前述の構成が完了した後、TiDB クラスターをデプロイ、スケールアウト、スケールイン、またはリロードすると、 TiUP はAlertmanager 起動パラメーターの`listen_host`フィールドを`--web.listen-address`に追加します。
