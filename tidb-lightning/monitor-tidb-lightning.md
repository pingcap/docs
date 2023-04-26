---
title: TiDB Lightning Monitoring
summary: Learn about the monitor configuration and monitoring metrics of TiDB Lightning.
---

# TiDB Lightningモニタリング {#tidb-lightning-monitoring}

`tidb-lightning` [プロメテウス](https://prometheus.io/)を介したメトリクス コレクションをサポートします。このドキュメントでは、 TiDB Lightningの監視構成と監視メトリクスを紹介します。

## モニター構成 {#monitor-configuration}

TiDB Lightningを手動でインストールする場合は、以下の手順に従ってください。

`tidb-lightning`のメトリックは、Prometheus が検出される限り、Prometheus によって直接収集できます。 `tidb-lightning.toml`でメトリクス ポートを設定できます。

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

サーバーを検出するように Prometheus を構成する必要があります。たとえば、サーバーアドレスを`scrape_configs`セクションに直接追加できます。

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

## Grafana ダッシュボード {#grafana-dashboard}

[グラファナ](https://grafana.com/)は、Prometheus メトリクスをダッシュボードとして視覚化するための Web インターフェイスです。

### 行 1: 速度 {#row-1-speed}

![Panels in first row](/media/lightning-grafana-row-1.png)

| パネル       | シリーズ                 | 説明                                                         |
| :-------- | :------------------- | :--------------------------------------------------------- |
| インポート速度   | TiDB Lightningから書き込む | 各テーブルの複雑さに依存する、 TiDB Lightningから TiKV Importer への KV の送信速度 |
| インポート速度   | tikvにアップロード          | TiKV Importer からすべての TiKV レプリカへの合計アップロード速度                 |
| Chunk処理時間 |                      | 1 つのデータ ファイルを完全にエンコードするのに必要な平均時間                           |

場合によっては、インポート速度がゼロになり、他のパーツが追いつくことがあります。これは正常です。

### 行 2: 進行状況 {#row-2-progress}

![Panels in second row](/media/lightning-grafana-row-2.png)

| パネル         | 説明                         |
| :---------- | :------------------------- |
| インポートの進行状況  | これまでにエンコードされたデータ ファイルの割合   |
| チェックサムの進行状況 | 正常にインポートされたことが確認されたテーブルの割合 |
| 失敗          | 失敗したテーブルの数とその障害点 (通常は空)    |

### 行 3: リソース {#row-3-resource}

![Panels in third row](/media/lightning-grafana-row-3.png)

| パネル                   | 説明                              |
| :-------------------- | :------------------------------ |
| メモリ使用量                | 各サービスが占有するメモリ量                  |
| TiDB Lightningゴルーチンの数 | TiDB Lightningで使用される実行中のゴルーチンの数 |
| CPU％                  | 各サービスで使用される論理 CPU コアの数          |

### 行 4: クォータ {#row-4-quota}

![Panels in fourth row](/media/lightning-grafana-row-4.png)

| パネル     | シリーズ        | 説明                                                                                                                                                 |
| :------ | :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------- |
| アイドル労働者 | いお          | 未使用の数`io-concurrency` 、通常は設定値 (デフォルト 5) に近く、0 に近い場合はディスクが遅すぎることを意味します                                                                              |
| アイドル労働者 | クローズドエンジン   | 閉じられているがまだクリーンアップされていないエンジンの数。通常はインデックス + テーブル同時実行数 (デフォルト 8) に近く、0 に近い場合はTiDB Lightning がTiKV Importer よりも高速であることを意味し、 TiDB Lightningが停止する原因となります |
| アイドル労働者 | テーブル        | 未使用数`table-concurrency` 、通常は処理終了まで 0                                                                                                               |
| アイドル労働者 | 索引          | 未使用数`index-concurrency` 、通常は処理終了まで 0                                                                                                               |
| アイドル労働者 | 領域          | 未使用数`region-concurrency` 、通常は処理終了まで 0                                                                                                              |
| 外部リソース  | KVエンコーダー    | アクティブな KV エンコーダーをカウントします。通常、プロセスの終了までは`region-concurrency`と同じです。                                                                                   |
| 外部リソース  | インポーター エンジン | 開いているエンジン ファイルをカウントします。1 `max-open-engines`設定を超えてはいけません                                                                                            |

### 行 5: 読み取り速度 {#row-5-read-speed}

![Panels in fifth row](/media/lightning-grafana-row-5.png)

| パネル                 | シリーズ     | 説明                                      |
| :------------------ | :------- | :-------------------------------------- |
| Chunkパーサー読み取りブロック期間 | ブロックを読む  | 解析の準備のために 1 ブロックのバイトを読み取るのにかかった時間       |
| Chunkパーサー読み取りブロック期間 | 労働者を適用する | アイドル状態の io-concurrency を待機するために経過した時間   |
| SQL プロセスの所要時間       | 行エンコード   | 1 行の解析とエンコードにかかった時間                     |
| SQL プロセスの所要時間       | ブロック配信   | KV ペアのブロックを TiKV Importer に送信するのにかかった時間 |

いずれかの期間が長すぎる場合は、 TiDB Lightningが使用するディスクが遅すぎるか、I/O でビジーであることを示しています。

### 行 6: ストレージ {#row-6-storage}

![Panels in sixth row](/media/lightning-grafana-row-6.png)

| パネル      | シリーズ             | 説明                                         |
| :------- | :--------------- | :----------------------------------------- |
| SQL 処理速度 | データ配信率           | データ KV ペアの TiKV インポーターへの配信速度               |
| SQL 処理速度 | インデックス配信率        | インデックス KV ペアの TiKV インポーターへの配信速度            |
| SQL 処理速度 | 合計配信率            | 上記の 2 つのレートの合計                             |
| 合計バイト数   | パーサー読み取りサイズ      | TiDB Lightningが読み取っているバイト数                 |
| 合計バイト数   | データ配信サイズ         | TiKV Importer に既に配信されたデータ KV ペアのバイト数       |
| 合計バイト数   | インデックス配信サイズ      | TiKV Importer に既に配信されたインデックス KV ペアのバイト数    |
| 合計バイト数   | storage_size / 3 | TiKV クラスターが占める合計サイズを 3 で割った値 (レプリカのデフォルト数) |

### 行 7: インポート速度 {#row-7-import-speed}

![Panels in seventh row](/media/lightning-grafana-row-7.png)

| パネル        | シリーズ      | 説明                                     |
| :--------- | :-------- | :------------------------------------- |
| 納期         | 範囲配達      | 一連の KV ペアを TiKV クラスターにアップロードするのにかかった時間 |
| 納期         | SST 配信    | SST ファイルを TiKV クラスターにアップロードするのにかかった時間  |
| SST プロセス期間 | スプリット SST | KV ペアのストリームを SST ファイルに分割するのにかかった時間     |
| SST プロセス期間 | SSTアップロード | SST ファイルのアップロードにかかった時間                 |
| SST プロセス期間 | SST 摂取    | アップロードされた SST ファイルの取り込みにかかった時間         |
| SST プロセス期間 | SSTサイズ    | SSTファイルのファイルサイズ                        |

## 指標のモニタリング {#monitoring-metrics}

このセクションでは、デフォルトの Grafana ダッシュボードでカバーされていない他のメトリックを監視する必要がある場合に、 `tikv-importer`と`tidb-lightning`の監視メトリックについて説明します。

### <code>tikv-importer</code> {#code-tikv-importer-code}

`tikv-importer`によって提供されるメトリックは、名前空間`tikv_import_*`の下にリストされます。

-   **`tikv_import_rpc_duration`** (ヒストグラム)

    RPC アクションの期間のバケット化されたヒストグラム。ラベル:

    -   **request** : 実行される RPC の種類
        -   `switch_mode` : TiKV ノードをインポート/通常モードに切り替えました
        -   `open_engine` : エンジン ファイルを開きました
        -   `write_engine` : データを受信し、エンジンに書き込む
        -   `close_engine` : エンジン ファイルを閉じました
        -   `import_engine` : エンジン ファイルを TiKV クラスターにインポートしました
        -   `cleanup_engine` : エンジン ファイルを削除しました
        -   `compact_cluster` : TiKV クラスターを明示的に圧縮しました
        -   `upload` : SST ファイルをアップロードしました
        -   `ingest` : SST ファイルを取り込みました
        -   `compact` : TiKV ノードを明示的に圧縮
    -   **result** : RPC の実行結果
        -   `ok`
        -   `error`

-   **`tikv_import_write_chunk_bytes`** (ヒストグラム)

    TiDB Lightningから受信した KV ペアのブロックの圧縮されていないサイズのバケット化されたヒストグラム。

-   **`tikv_import_write_chunk_duration`** (ヒストグラム)

    TiDB Lightningから KV ペアのブロックを受信するのに必要な時間のバケット化されたヒストグラム。

-   **`tikv_import_upload_chunk_bytes`** (ヒストグラム)

    TiKV にアップロードされた SST ファイルのチャンクの圧縮サイズのバケット化されたヒストグラム。

-   **`tikv_import_upload_chunk_duration`** (ヒストグラム)

    SST ファイルのチャンクを TiKV にアップロードするのに必要な時間のバケット化されたヒストグラム。

-   **`tikv_import_range_delivery_duration`** (ヒストグラム)

    KV ペアの範囲を`dispatch-job`に配信するのに必要な時間のバケット化されたヒストグラム。

-   **`tikv_import_split_sst_duration`** (ヒストグラム)

    エンジン ファイルの範囲を 1 つの SST ファイルに分割するのに必要な時間のバケット化されたヒストグラム。

-   **`tikv_import_sst_delivery_duration`** (ヒストグラム)

    SST ファイルを`dispatch-job`から`ImportSSTJob`に配信するのに必要な時間のバケット化されたヒストグラム。

-   **`tikv_import_sst_recv_duration`** (ヒストグラム)

    `dispatch-job` in a `ImportSSTJob`から SST ファイルを受信するのに必要な時間のバケット化されたヒストグラム。

-   **`tikv_import_sst_upload_duration`** (ヒストグラム)

    `ImportSSTJob`から TiKV ノードに SST ファイルをアップロードするのに必要な時間のバケット化されたヒストグラム。

-   **`tikv_import_sst_chunk_bytes`** (ヒストグラム)

    TiKV ノードにアップロードされた SST ファイルの圧縮サイズのバケット化されたヒストグラム。

-   **`tikv_import_sst_ingest_duration`** (ヒストグラム)

    SST ファイルを TiKV に取り込むのに必要な時間のバケット化されたヒストグラム。

-   **`tikv_import_each_phase`** (ゲージ)

    実行フェーズを示します。可能な値は、フェーズ内で実行中を意味する 1 と、フェーズ外で実行中を意味する 0 です。ラベル:

    -   **フェーズ**: `prepare` / `import`

-   **`tikv_import_wait_store_available_count`** (カウンター)

    SST ファイルのアップロード時に、TiKV ノードに十分なスペースがないことが判明した回数をカウントします。ラベル:

    -   **store_id** : TiKV ストア ID。

### <code>tidb-lightning</code> {#code-tidb-lightning-code}

`tidb-lightning`によって提供されるメトリックは、名前空間`lightning_*`の下にリストされます。

-   **`lightning_importer_engine`** (カウンター)

    開いているエンジン ファイルと閉じているエンジン ファイルをカウントします。ラベル:

    -   **タイプ**:
        -   `open`
        -   `closed`

-   **`lightning_idle_workers`** (ゲージ)

    アイドル ワーカーをカウントします。ラベル:

    -   **名前**:
        -   `table` : `table-concurrency`の余り、通常はプロセスの最後まで 0
        -   `index` : `index-concurrency`の余り、通常はプロセスの最後まで 0
        -   `region` : `region-concurrency`の余り、通常はプロセスの最後まで 0
        -   `io` : `io-concurrency`の余り。通常は構成された値 (デフォルトの 5) に近く、0 に近い場合はディスクが遅すぎることを意味します。
        -   `closed-engine` : クローズされたがまだクリーンアップされていないエンジンの数。通常は index + table-concurrency (デフォルト 8) に近い値です。 0 に近い値は、 TiDB Lightning がTiKV Importer よりも高速であることを意味し、 TiDB Lightningが停止する可能性があります

-   **`lightning_kv_encoder`** (カウンター)

    開いている KV エンコーダと閉じている KV エンコーダをカウントします。 KV エンコーダーは、SQL `INSERT`ステートメントを KV ペアに変換するメモリ内の TiDB インスタンスです。正味の値は、健全な状況で制限する必要があります。ラベル:

    -   **タイプ**:
        -   `open`
        -   `closed`

<!---->

-   **`lightning_tables`** (カウンター)

    処理されたテーブルとそのステータスをカウントします。ラベル:

    -   **state** : どのフェーズを完了する必要があるかを示す、テーブルのステータス
        -   `pending` : 未処理
        -   `written` : すべてのデータをエンコードして送信
        -   `closed` : 対応するすべてのエンジン ファイルが閉じられている
        -   `imported` : すべてのエンジン ファイルがターゲット クラスターにインポートされました
        -   `altered_auto_inc` : AUTO_INCREMENT ID が変更されました
        -   `checksum` : チェックサムを実行
        -   `analyzed` : 統計分析が実行されました
        -   `completed` : テーブルは完全にインポートされ、検証されました
    -   **result** : 現在のフェーズの結果
        -   `success` : フェーズは正常に完了しました
        -   `failure` : フェーズは失敗しました (完了しませんでした)

-   **`lightning_engines`** (カウンター)

    処理されたエンジン ファイルの数とそのステータスをカウントします。ラベル:

    -   **state** : エンジンのステータス。どのフェーズを完了する必要があるかを示します
        -   `pending` : 未処理
        -   `written` : すべてのデータをエンコードして送信
        -   `closed` : エンジン ファイルが閉じられている
        -   `imported` : エンジン ファイルはターゲット クラスタにインポートされました
        -   `completed` : エンジンは完全にインポートされました
    -   **result** : 現在のフェーズの結果
        -   `success` : フェーズは正常に完了しました
        -   `failure` : フェーズは失敗しました (完了しませんでした)

<!---->

-   **`lightning_chunks`** (カウンター)

    処理されたチャンクの数とそのステータスをカウントします。ラベル:

    -   **state** : チャンクのステータス。チャンクがどのフェーズにあるかを示します
        -   `estimated` : (状態ではありません) この値は、現在のタスクのチャンクの総数を示します
        -   `pending` : ロードされていますが、まだ処理されていません
        -   `running` : データはエンコードされて送信されています
        -   `finished` : チャンク全体が処理されました
        -   `failed` : 処理中にエラーが発生しました

-   **`lightning_import_seconds`** (ヒストグラム)

    テーブルのインポートに必要な時間のバケット化されたヒストグラム。

-   **`lightning_row_read_bytes`** (ヒストグラム)

    単一の SQL 行のサイズのバケット化されたヒストグラム。

-   **`lightning_row_encode_seconds`** (ヒストグラム)

    1 つの SQL 行を KV ペアにエンコードするのに必要な時間のバケット化されたヒストグラム。

-   **`lightning_row_kv_deliver_seconds`** (ヒストグラム)

    1 つの SQL 行に対応する一連の KV ペアを配信するのに必要な時間のバケット化されたヒストグラム。

-   **`lightning_block_deliver_seconds`** (ヒストグラム)

    KV ペアのブロックを Importer に配信するのに必要な時間のバケット化されたヒストグラム。

-   **`lightning_block_deliver_bytes`** (ヒストグラム)

    Importer に配信される KV ペアのブロックの圧縮されていないサイズのバケット化されたヒストグラム。

-   **`lightning_chunk_parser_read_block_seconds`** (ヒストグラム)

    データ ファイル パーサーがブロックを読み取るのに必要な時間のバケット化されたヒストグラム。

-   **`lightning_checksum_seconds`** (ヒストグラム)

    テーブルのチェックサムの計算に必要な時間のバケット化されたヒストグラム。

-   **`lightning_apply_worker_seconds`** (ヒストグラム)

    アイドル状態のワーカーを取得するのに必要な時間のバケット化されたヒストグラム ( `lightning_idle_workers`ゲージも参照)。ラベル:

    -   **名前**:
        -   `table`
        -   `index`
        -   `region`
        -   `io`
        -   `closed-engine`
