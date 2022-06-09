---
title: TiDB Lightning Monitoring
summary: Learn about the monitor configuration and monitoring metrics of TiDB Lightning.
---

# TiDB Lightning Monitoring {#tidb-lightning-monitoring}

`tidb-lightning`は、 [プロメテウス](https://prometheus.io/)を介したメトリック収集をサポートします。このドキュメントでは、TiDBLightningのモニター構成とモニターメトリックを紹介します。

## モニター構成 {#monitor-configuration}

TiDB Lightningを手動でインストールする場合は、以下の手順に従ってください。

`tidb-lightning`のメトリックは、発見されている限り、Prometheusによって直接収集できます。メトリックポートは`tidb-lightning.toml`で設定できます。

```toml
[lightning]
# HTTP port for debugging and Prometheus metrics pulling (0 to disable)
pprof-port = 8289

...
```

そして`tikv-importer.toml`で：

```toml
# Listening address of the status server.
status-server-address = '0.0.0.0:8286'
```

サーバーを検出できるようにPrometheusを構成する必要があります。たとえば、サーバーアドレスを`scrape_configs`セクションに直接追加できます。

```yaml
...
scrape_configs:
  - job_name: 'tidb-lightning'
    static_configs:
      - targets: ['192.168.20.10:8289']
  - job_name: 'tikv-importer'
    static_configs:
      - targets: ['192.168.20.9:8286']
```

## Grafanaダッシュボード {#grafana-dashboard}

[Grafana](https://grafana.com/)は、Prometheusメトリックをダッシュボードとして視覚化するためのWebインターフェイスです。

[TiUPを使用してTiDBクラスタをデプロイする](/production-deployment-using-tiup.md)を実行し、トポロジ構成にGrafanaとPrometheusを追加すると、 [Grafana+Prometheusモニタリングプラットフォーム](/tidb-monitoring-framework.md)のセットが同時にデプロイされます。この状況では、最初に[ダッシュボードのJSONファイル](https://raw.githubusercontent.com/pingcap/tidb-ansible/master/scripts/lightning.json)をインポートする必要があります。

### 行1：速度 {#row-1-speed}

![Panels in first row](/media/lightning-grafana-row-1.png)

| パネル      | シリーズ                 | 説明                                                        |
| :------- | :------------------- | :-------------------------------------------------------- |
| インポート速度  | TiDBLightningからの書き込み | TiDBLightningからTiKVImporterへのKVの送信速度。これは、各テーブルの複雑さに依存します。 |
| インポート速度  | tikvにアップロード          | TiKVインポーターからすべてのTiKVレプリカへの合計アップロード速度                      |
| チャンク処理期間 |                      | 1つのデータファイルを完全にエンコードするのに必要な平均時間                            |

インポート速度がゼロに低下し、他のパーツが追いつくことがあります。これは正常です。

### 行2：進捗状況 {#row-2-progress}

![Panels in second row](/media/lightning-grafana-row-2.png)

| パネル         | 説明                               |
| :---------- | :------------------------------- |
| インポートの進行状況  | これまでにエンコードされたデータファイルの割合          |
| チェックサムの進行状況 | テーブルのパーセンテージが正常にインポートされたことを確認します |
| 失敗          | 障害が発生したテーブルの数とその障害点（通常は空）        |

### 行3：リソース {#row-3-resource}

![Panels in third row](/media/lightning-grafana-row-3.png)

| パネル                       | 説明                             |
| :------------------------ | :----------------------------- |
| メモリ使用量                    | 各サービスが占有するメモリの量                |
| TiDBLightningGoroutinesの数 | TiDBLightningで使用される実行中のゴルーチンの数 |
| CPU％                      | 各サービスで使用される論理CPUコアの数           |

### 行4：割り当て {#row-4-quota}

![Panels in fourth row](/media/lightning-grafana-row-4.png)

| パネル     | シリーズ       | 説明                                                                                                                                     |
| :------ | :--------- | :------------------------------------------------------------------------------------------------------------------------------------- |
| アイドル労働者 | io         | 未使用の数`io-concurrency` 、通常は構成された値（デフォルトは5）に近く、0に近い場合は、ディスクが遅すぎることを意味します                                                                 |
| アイドル労働者 | クローズドエンジン  | 閉じているがまだクリーンアップされていない、通常はインデックス+テーブル同時実行（デフォルトは8）に近く、0に近いエンジンの数は、TiDBLightningがTiKVImporterよりも高速であることを意味します。これにより、TiDBLightningが停止します。 |
| アイドル労働者 | テーブル       | 未使用の数`table-concurrency` 、通常はプロセスが終了するまで0                                                                                              |
| アイドル労働者 | 索引         | 未使用の数`index-concurrency` 、通常はプロセスが終了するまで0                                                                                              |
| アイドル労働者 | 領域         | 未使用の数`region-concurrency` 、通常はプロセスが終了するまで0                                                                                             |
| 外部リソース  | KVエンコーダー   | アクティブなKVエンコーダーをカウントします。通常、プロセスが終了するまで`region-concurrency`と同じです。                                                                        |
| 外部リソース  | インポーターエンジン | 開いているエンジンファイルをカウントします`max-open-engines`の設定を超えてはなりません                                                                                   |

### 行5：読み取り速度 {#row-5-read-speed}

![Panels in fifth row](/media/lightning-grafana-row-5.png)

| パネル                 | シリーズ      | 説明                                  |
| :------------------ | :-------- | :---------------------------------- |
| チャンクパーサーの読み取りブロック期間 | ブロックの読み取り | 解析の準備のために1ブロックのバイトを読み取るのにかかる時間      |
| チャンクパーサーの読み取りブロック期間 | 労働者を適用する  | アイドル状態のio-concurrencyを待機するために経過した時間 |
| SQLプロセス期間           | 行エンコード    | 単一行の解析とエンコードにかかる時間                  |
| SQLプロセス期間           | ブロック配信    | KVペアのブロックをTiKVインポーターに送信するのにかかる時間    |

期間のいずれかが長すぎる場合は、TiDBLightningによって使用されているディスクが遅すぎるかI/Oでビジーであることを示しています。

### 行6：ストレージ {#row-6-storage}

![Panels in sixth row](/media/lightning-grafana-row-6.png)

| パネル        | シリーズ             | 説明                                    |
| :--------- | :--------------- | :------------------------------------ |
| SQLプロセスレート | データ配信率           | TiKVインポーターへのデータKVペアの配信速度              |
| SQLプロセスレート | インデックス配信率        | TiKVインポーターへのインデックスKVペアの配信速度           |
| SQLプロセスレート | 総配信率             | 上記の2つのレートの合計                          |
| 合計バイト数     | パーサー読み取りサイズ      | TiDBLightningによって読み取られているバイト数         |
| 合計バイト数     | データ配信サイズ         | TiKVインポーターにすでに配信されているデータKVペアのバイト数     |
| 合計バイト数     | インデックス配信サイズ      | TiKVインポーターにすでに配信されているインデックスKVペアのバイト数  |
| 合計バイト数     | storage_size / 3 | TiKVクラスタが占める合計サイズを3で割った値（デフォルトのレプリカ数） |

### 行7：インポート速度 {#row-7-import-speed}

![Panels in seventh row](/media/lightning-grafana-row-7.png)

| パネル       | シリーズ      | 説明                               |
| :-------- | :-------- | :------------------------------- |
| 納期        | 範囲配信      | 一連のKVペアをTiKVクラスタにアップロードするのにかかる時間 |
| 納期        | SST配信     | SSTファイルをTiKVクラスタにアップロードするのにかかる時間 |
| SSTプロセス期間 | スプリットSST  | KVペアのストリームをSSTファイルに分割するのにかかる時間   |
| SSTプロセス期間 | SSTアップロード | SSTファイルのアップロードにかかる時間             |
| SSTプロセス期間 | SST摂取     | アップロードされたSSTファイルの取り込みにかかった時間     |
| SSTプロセス期間 | SSTサイズ    | SSTファイルのファイルサイズ                  |

## モニタリング指標 {#monitoring-metrics}

このセクションでは、デフォルトのGrafanaダッシュボードでカバーされていない他のメトリックを監視する必要がある場合に、 `tikv-importer`と`tidb-lightning`の監視メトリックについて説明します。

### <code>tikv-importer</code> {#code-tikv-importer-code}

`tikv-importer`によって提供されるメトリックは、名前空間`tikv_import_*`の下にリストされます。

-   **`tikv_import_rpc_duration`** （ヒストグラム）

    RPCアクションの期間中のバケット化されたヒストグラム。ラベル：

    -   **リクエスト**：どのようなRPCが実行されるか
        -   `switch_mode` —TiKVノードをインポート/通常モードに切り替えました
        -   `open_engine` —エンジンファイルを開きました
        -   `write_engine` —データを受信し、エンジンに書き込まれます
        -   `close_engine` —エンジンファイルを閉じました
        -   `import_engine` —エンジンファイルをTiKVクラスタにインポートしました
        -   `cleanup_engine` —エンジンファイルを削除しました
        -   `compact_cluster` —TiKVクラスタを明示的に圧縮しました
        -   `upload` —SSTファイルをアップロードしました
        -   `ingest` —SSTファイルを取り込んだ
        -   `compact` —TiKVノードを明示的に圧縮しました
    -   **結果**：RPCの実行結果
        -   `ok`
        -   `error`

-   **`tikv_import_write_chunk_bytes`** （ヒストグラム）

    TiDBLightningから受信したKVペアのブロックの非圧縮サイズのバケット化されたヒストグラム。

-   **`tikv_import_write_chunk_duration`** （ヒストグラム）

    TiDBLightningからKVペアのブロックを受信するために必要な時間のバケット化されたヒストグラム。

-   **`tikv_import_upload_chunk_bytes`** （ヒストグラム）

    TiKVにアップロードされたSSTファイルのチャンクの圧縮サイズのバケット化されたヒストグラム。

-   **`tikv_import_upload_chunk_duration`** （ヒストグラム）

    SSTファイルのチャンクをTiKVにアップロードするために必要な時間のバケット化されたヒストグラム。

-   **`tikv_import_range_delivery_duration`** （ヒストグラム）

    一連のKVペアを`dispatch-job`に配信するために必要な時間のバケット化されたヒストグラム。

-   **`tikv_import_split_sst_duration`** （ヒストグラム）

    エンジンファイルから単一のSSTファイルに範囲を分割するために必要な時間のバケット化されたヒストグラム。

-   **`tikv_import_sst_delivery_duration`** （ヒストグラム）

    SSTファイルを`dispatch-job`から`ImportSSTJob`に配信するために必要な時間のバケット化されたヒストグラム。

-   **`tikv_import_sst_recv_duration`** （ヒストグラム）

    `ImportSSTJob`の`dispatch-job`からSSTファイルを受信するために必要な時間のバケット化されたヒストグラム。

-   **`tikv_import_sst_upload_duration`** （ヒストグラム）

    SSTファイルを`ImportSSTJob`からTiKVノードにアップロードするために必要な時間のバケット化されたヒストグラム。

-   **`tikv_import_sst_chunk_bytes`** （ヒストグラム）

    TiKVノードにアップロードされたSSTファイルの圧縮サイズのバケット化されたヒストグラム。

-   **`tikv_import_sst_ingest_duration`** （ヒストグラム）

    SSTファイルをTiKVに取り込むのに必要な時間のバケット化されたヒストグラム。

-   **`tikv_import_each_phase`** （ゲージ）

    実行フェーズを示します。可能な値は、フェーズ内で実行されていることを意味する1と、フェーズ外で実行されていることを意味する0です。ラベル：

    -   **フェーズ**`import` `prepare`

-   **`tikv_import_wait_store_available_count`** （カウンター）

    SSTファイルをアップロードするときにTiKVノードに十分なスペースがないことが検出された回数をカウントします。ラベル：

    -   **store_id** ：TiKVストアID。

### <code>tidb-lightning</code> {#code-tidb-lightning-code}

`tidb-lightning`によって提供されるメトリックは、名前空間`lightning_*`の下にリストされます。

-   **`lightning_importer_engine`** （カウンター）

    開いているエンジンファイルと閉じているエンジンファイルをカウントします。ラベル：

    -   **タイプ**：
        -   `open`
        -   `closed`

-   **`lightning_idle_workers`** （ゲージ）

    アイドル状態のワーカーをカウントします。ラベル：

    -   **名前**：
        -   `table` — `table-concurrency`の余り、通常はプロセスが終了するまで0
        -   `index` — `index-concurrency`の余り、通常はプロセスが終了するまで0
        -   `region` — `region-concurrency`の余り、通常はプロセスが終了するまで0
        -   `io` — `io-concurrency`の残り、通常は構成された値（デフォルトは5）に近く、0に近い場合は、ディスクが遅すぎることを意味します
        -   `closed-engine` —閉じられているがまだクリーンアップされていないエンジンの数。通常はインデックス+テーブル同時実行に近い（デフォルトは8）。 0に近い値は、TiDBLightningがTiKVImporterよりも高速であることを意味します。これにより、TiDBLightningが停止する可能性があります。

-   **`lightning_kv_encoder`** （カウンター）

    開いているKVエンコーダーと閉じているKVエンコーダーをカウントします。 KVエンコーダーは、 `INSERT`ステートメントをKVペアに変換するメモリ内TiDBインスタンスです。正味の価値は、健全な状況で制限される必要があります。ラベル：

    -   **タイプ**：
        -   `open`
        -   `closed`

<!---->

-   **`lightning_tables`** （カウンター）

    処理されたテーブルとそのステータスをカウントします。ラベル：

    -   **state** ：テーブルのステータス。どのフェーズを完了する必要があるかを示します
        -   `pending` —まだ処理されていません
        -   `written` —エンコードおよび送信されたすべてのデータ
        -   `closed` —対応するすべてのエンジンファイルが閉じられました
        -   `imported` —すべてのエンジンファイルがターゲットクラスタにインポートされました
        -   `altered_auto_inc` —AUTO_INCREMENTIDが変更されました
        -   `checksum` —チェックサムが実行されました
        -   `analyzed` —実行された統計分析
        -   `completed` —テーブルは完全にインポートおよび検証されています
    -   **結果**：現在のフェーズの結果
        -   `success` —フェーズは正常に完了しました
        -   `failure` —フェーズが失敗しました（完了しませんでした）

-   **`lightning_engines`** （カウンター）

    処理されたエンジンファイルの数とそのステータスをカウントします。ラベル：

    -   **状態**：エンジンのステータス。どのフェーズを完了する必要があるかを示します
        -   `pending` —まだ処理されていません
        -   `written` —エンコードおよび送信されたすべてのデータ
        -   `closed` —エンジンファイルが閉じられました
        -   `imported` —エンジンファイルがターゲットクラスタにインポートされました
        -   `completed` —エンジンは完全にインポートされました
    -   **結果**：現在のフェーズの結果
        -   `success` —フェーズは正常に完了しました
        -   `failure` —フェーズが失敗しました（完了しませんでした）

<!---->

-   **`lightning_chunks`** （カウンター）

    処理されたチャンクの数とそのステータスをカウントします。ラベル：

    -   **状態**：チャンクのステータス。チャンクがどのフェーズにあるかを示します
        -   `estimated` —（状態ではありません）この値は、現在のタスクのチャンクの総数を示します
        -   `pending` —ロードされましたが、まだ処理されていません
        -   `running` —データはエンコードされて送信されています
        -   `finished` —チャンク全体が処理されました
        -   `failed` —処理中にエラーが発生しました

-   **`lightning_import_seconds`** （ヒストグラム）

    テーブルのインポートに必要な時間のバケット化されたヒストグラム。

-   **`lightning_row_read_bytes`** （ヒストグラム）

    単一のSQL行のサイズのバケット化されたヒストグラム。

-   **`lightning_row_encode_seconds`** （ヒストグラム）

    単一のSQL行をKVペアにエンコードするために必要な時間のバケット化されたヒストグラム。

-   **`lightning_row_kv_deliver_seconds`** （ヒストグラム）

    1つのSQL行に対応するKVペアのセットを配信するために必要な時間のバケット化されたヒストグラム。

-   **`lightning_block_deliver_seconds`** （ヒストグラム）

    KVペアのブロックをインポーターに配信するために必要な時間のバケット化されたヒストグラム。

-   **`lightning_block_deliver_bytes`** （ヒストグラム）

    インポーターに配信されたKVペアのブロックの非圧縮サイズのバケット化されたヒストグラム。

-   **`lightning_chunk_parser_read_block_seconds`** （ヒストグラム）

    データファイルパーサーがブロックを読み取るために必要な時間のバケット化されたヒストグラム。

-   **`lightning_checksum_seconds`** （ヒストグラム）

    テーブルのチェックサムを計算するために必要な時間のバケット化されたヒストグラム。

-   **`lightning_apply_worker_seconds`** （ヒストグラム）

    アイドル状態のワーカーを取得するために必要な時間のバケット化されたヒストグラム（ `lightning_idle_workers`ゲージも参照）。ラベル：

    -   **名前**：
        -   `table`
        -   `index`
        -   `region`
        -   `io`
        -   `closed-engine`
