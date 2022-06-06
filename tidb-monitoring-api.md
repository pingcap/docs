---
title: TiDB Monitoring API
summary: Learn the API of TiDB monitoring services.
---

# TiDBモニタリングAPI {#tidb-monitoring-api}

次のタイプのインターフェースを使用して、TiDBクラスタのステータスをモニターできます。

-   [ステータスインターフェイス](#use-the-status-interface) ：このインターフェースはHTTPインターフェースを使用してコンポーネント情報を取得します。このインターフェイスを使用すると、現在のTiDBサーバーの[実行ステータス](#running-status)つとテーブルの[ストレージ情報](#storage-information)を取得できます。
-   [メトリックインターフェイス](#use-the-metrics-interface) ：このインターフェースはPrometheusを使用してコンポーネントのさまざまな操作の詳細情報を記録し、Grafanaを使用してこれらのメトリックを表示します。

## ステータスインターフェイスを使用する {#use-the-status-interface}

ステータスインターフェイスは、TiDBクラスタの特定のコンポーネントの基本情報を監視します。キープアライブメッセージの監視インターフェイスとしても機能します。さらに、配置ドライバー（PD）のステータスインターフェイスは、TiKVクラスタ全体の詳細を取得できます。

### TiDBサーバー {#tidb-server}

-   TiDB APIアドレス： `http://${host}:${port}`
-   デフォルトのポート： `10080`

### 実行ステータス {#running-status}

次の例では、 `http://${host}:${port}/status`を使用して、TiDBサーバーの現在のステータスを取得し、サーバーが稼働しているかどうかを判別します。結果は**JSON**形式で返されます。

```bash
curl http://127.0.0.1:10080/status
{
    connections: 0,  # The current number of clients connected to the TiDB server.
    version: "5.7.25-TiDB-v3.0.0-beta-250-g778c3f4a5",  # The TiDB version number.
    git_hash: "778c3f4a5a716880bcd1d71b257c8165685f0d70"  # The Git Hash of the current TiDB code.
}
```

#### ストレージ情報 {#storage-information}

次の例では、 `http://${host}:${port}/schema_storage/${db}/${table}`を使用して特定のデータテーブルのストレージ情報を取得します。結果は**JSON**形式で返されます。

{{< copyable "" >}}

```bash
curl http://127.0.0.1:10080/schema_storage/mysql/stats_histograms
```

```
{
    "table_schema": "mysql", 
    "table_name": "stats_histograms", 
    "table_rows": 0, 
    "avg_row_length": 0, 
    "data_length": 0, 
    "max_data_length": 0, 
    "index_length": 0, 
    "data_free": 0
}
```

```bash
curl http://127.0.0.1:10080/schema_storage/test
```

```
[
    {
        "table_schema": "test", 
        "table_name": "test", 
        "table_rows": 0, 
        "avg_row_length": 0, 
        "data_length": 0, 
        "max_data_length": 0, 
        "index_length": 0, 
        "data_free": 0
    }
]
```

### PDサーバー {#pd-server}

-   PD APIアドレス： `http://${host}:${port}/pd/api/v1/${api_name}`
-   デフォルトのポート： `2379`
-   API名の詳細： [PDAPIドキュメント](https://download.pingcap.com/pd-api-v1.html)を参照

PDインターフェイスは、すべてのTiKVサーバーのステータスと負荷分散に関する情報を提供します。シングルノードTiKVクラスタについては、次の例を参照してください。

```bash
curl http://127.0.0.1:2379/pd/api/v1/stores
{
  "count": 1,  # The number of TiKV nodes.
  "stores": [  # The list of TiKV nodes.
    # The details about the single TiKV node.
    {
      "store": {
        "id": 1,
        "address": "127.0.0.1:20160",
        "version": "3.0.0-beta",
        "state_name": "Up"
      },
      "status": {
        "capacity": "20 GiB",  # The total capacity.
        "available": "16 GiB",  # The available capacity.
        "leader_count": 17,
        "leader_weight": 1,
        "leader_score": 17,
        "leader_size": 17,
        "region_count": 17,
        "region_weight": 1,
        "region_score": 17,
        "region_size": 17,
        "start_ts": "2019-03-21T14:09:32+08:00",  # The starting timestamp.
        "last_heartbeat_ts": "2019-03-21T14:14:22.961171958+08:00",  # The timestamp of the last heartbeat.
        "uptime": "4m50.961171958s"
      }
    }
  ]
```

## メトリックインターフェイスを使用する {#use-the-metrics-interface}

メトリックインターフェイスは、TiDBクラスタ全体のステータスとパフォーマンスを監視します。

-   他の展開方法を使用する場合は、このインターフェイスを使用する前に[PrometheusとGrafanaをデプロイする](/deploy-monitoring-services.md) 。

PrometheusとGrafanaが正常にデプロイされた後、 [Grafanaを構成する](/deploy-monitoring-services.md#configure-grafana) 。
