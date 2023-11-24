---
title: Deploy Monitoring Services for the TiDB Cluster
summary: Learn how to deploy monitoring services for the TiDB cluster.
---

# TiDBクラスタのモニタリング サービスのデプロイ {#deploy-monitoring-services-for-the-tidb-cluster}

このドキュメントは、TiDB モニタリングおよびアラート サービスを手動で導入したいユーザーを対象としています。

TiUPを使用して TiDB クラスターをデプロイする場合、モニタリングおよびアラート サービスは自動的にデプロイされ、手動でデプロイする必要はありません。

## Prometheus と Grafanaをデプロイ {#deploy-prometheus-and-grafana}

TiDB クラスターのトポロジーが次のとおりであると仮定します。

| 名前   | ホストIP           | サービス                              |
| :--- | :-------------- | :-------------------------------- |
| ノード1 | 192.168.199.113 | PD1、TiDB、node_export、プロメテウス、グラファナ |
| ノード2 | 192.168.199.114 | PD2、ノードエクスポート                     |
| ノード3 | 192.168.199.115 | PD3、ノードエクスポート                     |
| ノード4 | 192.168.199.116 | TiKV1、node_export                 |
| ノード5 | 192.168.199.117 | TiKV2、node_export                 |
| ノード6 | 192.168.199.118 | TiKV3、node_export                 |

### ステップ 1: バイナリ パッケージをダウンロードする {#step-1-download-the-binary-package}

```bash
# Downloads the package.
wget https://download.pingcap.org/prometheus-2.27.1.linux-amd64.tar.gz
wget https://download.pingcap.org/node_exporter-v1.3.1-linux-amd64.tar.gz
wget https://download.pingcap.org/grafana-7.5.11.linux-amd64.tar.gz
```

```bash
# Extracts the package.
tar -xzf prometheus-2.27.1.linux-amd64.tar.gz
tar -xzf node_exporter-v1.3.1-linux-amd64.tar.gz
tar -xzf grafana-7.5.11.linux-amd64.tar.gz
```

### ステップ2: Node1、Node2、Node3、およびNode4で<code>node_exporter</code>起動します。 {#step-2-start-code-node-exporter-code-on-node1-node2-node3-and-node4}

```bash
cd node_exporter-v1.3.1-linux-amd64

# Starts the node_exporter service.
$ ./node_exporter --web.listen-address=":9100" \
    --log.level="info" &
```

### ステップ 3: Node1 で Prometheus を起動する {#step-3-start-prometheus-on-node1}

Prometheus 構成ファイルを編集します。

```bash
cd prometheus-2.27.1.linux-amd64 &&
vi prometheus.yml
```

```ini
...

global:
  scrape_interval:     15s  # By default, scrape targets every 15 seconds.
  evaluation_interval: 15s  # By default, scrape targets every 15 seconds.
  # scrape_timeout is set to the global default value (10s).
  external_labels:
    cluster: 'test-cluster'
    monitor: "prometheus"

scrape_configs:
  - job_name: 'overwritten-nodes'
    honor_labels: true  # Do not overwrite job & instance labels.
    static_configs:
    - targets:
      - '192.168.199.113:9100'
      - '192.168.199.114:9100'
      - '192.168.199.115:9100'
      - '192.168.199.116:9100'
      - '192.168.199.117:9100'
      - '192.168.199.118:9100'

  - job_name: 'tidb'
    honor_labels: true  # Do not overwrite job & instance labels.
    static_configs:
    - targets:
      - '192.168.199.113:10080'

  - job_name: 'pd'
    honor_labels: true  # Do not overwrite job & instance labels.
    static_configs:
    - targets:
      - '192.168.199.113:2379'
      - '192.168.199.114:2379'
      - '192.168.199.115:2379'

  - job_name: 'tikv'
    honor_labels: true  # Do not overwrite job & instance labels.
    static_configs:
    - targets:
      - '192.168.199.116:20180'
      - '192.168.199.117:20180'
      - '192.168.199.118:20180'

...

```

Prometheus サービスを開始します。

```bash
$ ./prometheus \
    --config.file="./prometheus.yml" \
    --web.listen-address=":9090" \
    --web.external-url="http://192.168.199.113:9090/" \
    --web.enable-admin-api \
    --log.level="info" \
    --storage.tsdb.path="./data.metrics" \
    --storage.tsdb.retention="15d" &
```

### ステップ 4: Node1 で Grafana を開始する {#step-4-start-grafana-on-node1}

Grafana 構成ファイルを編集します。

```ini
cd grafana-7.5.11 &&
vi conf/grafana.ini

...

[paths]
data = ./data
logs = ./data/log
plugins = ./data/plugins
[server]
http_port = 3000
domain = 192.168.199.113
[database]
[session]
[analytics]
check_for_updates = true
[security]
admin_user = admin
admin_password = admin
[snapshots]
[users]
[auth.anonymous]
[auth.basic]
[auth.ldap]
[smtp]
[emails]
[log]
mode = file
[log.console]
[log.file]
level = info
format = text
[log.syslog]
[event_publisher]
[dashboards.json]
enabled = false
path = ./data/dashboards
[metrics]
[grafana_net]
url = https://grafana.net

...

```

Grafana サービスを開始します。

```bash
./bin/grafana-server \
    --config="./conf/grafana.ini" &
```

## グラファナの構成 {#configure-grafana}

このセクションでは、Grafana の構成方法について説明します。

### ステップ 1: Prometheus データ ソースを追加する {#step-1-add-a-prometheus-data-source}

1.  Grafana Web インターフェイスにログインします。

    -   デフォルトのアドレス: [http://ローカルホスト:3000](http://localhost:3000)

    -   デフォルトのアカウント: 管理者

    -   デフォルトのパスワード: 管理者

    > **注記：**
    >
    > **[パスワードの変更]**ステップでは、 **[スキップ]**を選択できます。

2.  Grafana サイドバー メニューで、 **[コンフィグレーション]**内の**[データ ソース]**をクリックします。

3.  **[データ ソースの追加]**をクリックします。

4.  データソース情報を指定します。

    -   データ ソースの**名前**を指定します。
    -   **[タイプ]**で、 **[Prometheus]**を選択します。
    -   **URL**には、Prometheus アドレスを指定します。
    -   必要に応じて他のフィールドを指定します。

5.  **[追加]**をクリックして新しいデータ ソースを保存します。

### ステップ 2: Grafana ダッシュボードをインポートする {#step-2-import-a-grafana-dashboard}

PDサーバー、TiKVサーバー、および TiDBサーバーの Grafana ダッシュボードをインポートするには、それぞれ次の手順を実行します。

1.  Grafana ロゴをクリックしてサイドバー メニューを開きます。

2.  サイドバー メニューで、 **[ダッシュボード**] -&gt; **[インポート]**をクリックして、 **[ダッシュボードのインポート]**ウィンドウを開きます。

3.  **「.json ファイルのアップロード」**をクリックして JSON ファイルをアップロードします (TiDB Grafana 構成ファイルを[pingcap/tidb](https://github.com/pingcap/tidb/tree/release-7.1/metrics/grafana) 、 [ティクブ/ティクブ](https://github.com/tikv/tikv/tree/master/metrics/grafana) 、および[tikv/pd](https://github.com/tikv/pd/tree/master/metrics/grafana)からダウンロードします)。

    > **注記：**
    >
    > TiKV、PD、および TiDB ダッシュボードの場合、対応する JSON ファイルは`tikv_summary.json` 、 `tikv_details.json` 、 `tikv_trouble_shooting.json` 、 `pd.json` 、 `tidb.json` 、および`tidb_summary.json`です。

4.  **「ロード」**をクリックします。

5.  Prometheus データ ソースを選択します。

6.  **「インポート」**をクリックします。 Prometheus ダッシュボードがインポートされます。

## コンポーネントのメトリクスをビュー {#view-component-metrics}

上部のメニューで**[新しいダッシュボード]**をクリックし、表示するダッシュボードを選択します。

![view dashboard](/media/view-dashboard.png)

クラスター コンポーネントの次のメトリックを取得できます。

-   **TiDBサーバー:**

    -   レイテンシーとスループットを監視するためのクエリ処理時間
    -   DDLプロセス監視
    -   TiKV クライアント関連の監視
    -   PDクライアント関連の監視

-   **PDサーバー：**

    -   コマンドが実行された合計回数
    -   特定のコマンドが失敗した合計回数
    -   コマンドが成功するまでの時間
    -   コマンドが失敗するまでの期間
    -   コマンドが終了して結果を返すまでの時間

-   **TiKVサーバー:**

    -   ガベージ コレクション (GC) の監視
    -   TiKV コマンドが実行された合計回数
    -   スケジューラがコマンドを実行する期間
    -   Raft提案コマンドの合計回数
    -   Raftがコマンドを実行する時間
    -   Raftコマンドが失敗した合計回数
    -   Raft が準備完了状態を処理した合計回数
