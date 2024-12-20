---
title: Customize Configurations of Monitoring Servers
summary: TiUPによって管理される監視サーバーの構成をカスタマイズする方法を学びます
---

# 監視サーバーの構成をカスタマイズする {#customize-configurations-of-monitoring-servers}

TiUP を使用して TiDB クラスターをデプロイすると、 TiUP はPrometheus、Grafana、Alertmanager などの監視サーバーもデプロイします。その間に、このクラスターをスケールアウトすると、 TiUP は新しいノードを監視範囲に追加します。

上記の監視サーバーの構成をカスタマイズするには、以下の手順に従って、TiDB クラスターの topology.yaml に関連する構成項目を追加します。

> **注記：**
>
> -   監視サーバーの構成ファイルを直接変更しないでください。これらの変更は、デプロイメント、スケールアウト、スケールイン、再ロードなどの後のTiUP操作によって上書きされるためです。
>
> -   監視サーバーがTiUPによって展開および管理されていない場合は、このドキュメントを参照する代わりに、監視サーバーの構成ファイルを直接変更できます。
>
> -   この機能はTiUP v1.9.0 以降でサポートされています。したがって、この機能を使用する前にTiUP のバージョンを確認してください。

## Prometheusの設定をカスタマイズする {#customize-prometheus-configurations}

現在、 TiUP はPrometheus ルールとスクレイプ構成ファイルのカスタマイズをサポートしています。

### Prometheusルール設定をカスタマイズする {#customize-prometheus-rule-configuration}

1.  ルール構成ファイルをカスタマイズし、 TiUP が配置されているマシンのディレクトリの下に配置します。

2.  topology.yaml ファイルで、カスタマイズされたルール構成ファイルのディレクトリに`rule_dir`設定します。

    以下は、topology.yaml ファイル内の monitoring_servers の構成例です。

        # # Server configs are used to specify the configuration of Prometheus Server.
        monitoring_servers:
          # # The ip address of the Monitoring Server.
        - host: 127.0.0.1
          rule_dir: /home/tidb/prometheus_rule   # prometheus rule dir on TiUP machine

上記の構成が完了したら、TiDB クラスターをデプロイ、スケールアウト、スケールイン、またはリロードすると、 TiUPは`rule_dir` (たとえば`/home/tidb/prometheus_rule` ) からカスタマイズされたルール構成をロードし、それを Prometheus サーバーに送信してデフォルトのルール構成を置き換えます。

### Prometheus スクレイプ設定をカスタマイズする {#customize-prometheus-scrape-configuration}

1.  TiDB クラスターの topology.yaml ファイルを開きます。

2.  `monitoring_servers`構成で、 `additional_scrape_conf`フィールドを追加します。

    以下は、topology.yaml ファイル内の monitoring_servers の構成例です。

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

上記の構成が完了したら、TiDB クラスターをデプロイ、スケールアウト、スケールイン、またはリロードすると、 TiUP は`additional_scrape_conf`フィールドの内容を Prometheus 構成ファイルの対応するパラメーターに追加します。

## Grafana 設定をカスタマイズする {#customize-grafana-configurations}

現在、 TiUP はGrafana ダッシュボードやその他の構成のカスタマイズをサポートしています。

### Grafanaダッシュボードをカスタマイズする {#customize-grafana-dashboard}

1.  Grafana ダッシュボードの構成ファイルをカスタマイズし、 TiUP が配置されているマシンのディレクトリの下に配置します。

2.  topology.yaml ファイルで、カスタマイズされたダッシュボード構成ファイルのディレクトリに`dashboard_dir`設定します。

    以下は、topology.yaml ファイル内の grafana_servers の設定例です。

        # # Server configs are used to specify the configuration of Grafana Servers.
        grafana_servers:
          # # The ip address of the Grafana Server.
         - host: 127.0.0.1
         dashboard_dir: /home/tidb/dashboards   # grafana dashboard dir on TiUP machine

上記の構成が完了したら、TiDB クラスターをデプロイ、スケールアウト、スケールイン、またはリロードすると、 TiUPは`dashboard_dir` (たとえば`/home/tidb/dashboards` ) からカスタマイズされたダッシュボード構成をロードし、その構成を Grafana サーバーに送信してデフォルトのダッシュボード構成を置き換えます。

### その他のGrafana設定をカスタマイズする {#customize-other-grafana-configurations}

1.  TiDB クラスターの topology.yaml ファイルを開きます。

2.  `grafana_servers`構成に他の構成項目を追加します。

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

上記の構成が完了したら、TiDB クラスターをデプロイ、スケールアウト、スケールイン、またはリロードすると、 TiUP は`config`フィールドの内容を Grafana 構成ファイル`grafana.ini`に追加します。

## Alertmanager 設定をカスタマイズする {#customize-alertmanager-configurations}

現在、 TiUP はAlertmanager のリスニング アドレスのカスタマイズをサポートしています。

TiUPによってデプロイされた Alertmanager は、デフォルトで`alertmanager_servers.host`をリッスンします。プロキシを使用すると、Alertmanager にアクセスできません。この問題に対処するには、クラスター構成ファイル topology.yaml に`listen_host`追加して、リッスン アドレスを指定します。推奨値は 0.0.0.0 です。

次の例では、 `listen_host`フィールドを 0.0.0.0 に設定します。

    alertmanager_servers:
      # # The ip address of the Alertmanager Server.
      - host: 172.16.7.147
        listen_host: 0.0.0.0
        # # SSH port of the server.
        ssh_port: 22

上記の構成が完了したら、TiDB クラスターをデプロイ、スケールアウト、スケールイン、またはリロードすると、 TiUP はAlertmanager 起動パラメータの`listen_host`フィールドの内容を`--web.listen-address`に追加します。
