---
title: TiDB Lightning Monitoring
summary: TiDB Lightningのモニター構成と監視メトリックについて学習します。
---

# TiDB Lightning監視 {#tidb-lightning-monitoring}

`tidb-lightning`は[Prometheus](https://prometheus.io/)を介してメトリクス収集をサポートします。このドキュメントでは、 TiDB Lightningの監視設定と監視メトリクスについて説明します。

## モニター構成 {#monitor-configuration}

TiDB Lightning を手動でインストールする場合は、以下の手順に従ってください。

`tidb-lightning`のメトリクスは、Prometheus が検出済みであれば直接収集できます。`tidb-lightning.toml`のメトリクスポートは次のように設定できます。

```toml
[lightning]
# HTTP port for debugging and Prometheus metrics pulling (0 to disable)
pprof-port = 8289

...
```

Prometheusがサーバーを検出するように設定する必要があります。例えば、 `scrape_configs`セクションにサーバーのアドレスを直接追加することができます。

```yaml
...
scrape_configs:
  - job_name: 'tidb-lightning'
    static_configs:
      - targets: ['192.168.20.10:8289']
```

## Grafanaダッシュボード {#grafana-dashboard}

[Grafana](https://grafana.com/)は、Prometheus メトリックをダッシュボードとして視覚化するための Web インターフェースです。

### 1行目: Speed {#row-1-speed}

![Panels in first row](/media/lightning-grafana-row-1.png)

| パネル | シリーズ | 説明 |
| :--- | :--- | :--- |
| Import speed | write from TiDB Lightning | TiDB Lightningから TiKV Importer への KV の送信速度。これは各テーブルの複雑さによって異なります。 |
| Import speed | upload to tikv | TiKVインポーターからすべてのTiKVレプリカへの合計アップロード速度 |
| Chunk process duration | | 単一のデータファイルを完全にエンコードするのにかかる平均時間 |

場合によっては、インポート速度がゼロになり、他のパーツが追いつくまで時間がかかることがあります。これは正常な動作です。

### 2行目: Progress {#row-2-progress}

![Panels in second row](/media/lightning-grafana-row-2.png)

| パネル | 説明 |
| :--- | :--- |
| Import progress | これまでにエンコードされたデータファイルの割合 |
| Checksum progress | 正常にインポートされたことが検証されたテーブルの割合 |
| Failures | 障害が発生したテーブルの数と障害発生ポイント（通常は空） |

### 3行目: Resource {#row-3-resource}

![Panels in third row](/media/lightning-grafana-row-3.png)

| パネル | 説明 |
| :--- | :--- |
| Memory usage | 各サービスが占有するメモリ量 |
| Number of TiDB Lightning Goroutines | TiDB Lightningで使用される実行中の goroutine の数 |
| CPU% | 各サービスで使用される論理CPUコアの数 |

### 4行目: Quota {#row-4-quota}

![Panels in fourth row](/media/lightning-grafana-row-4.png)

| パネル | シリーズ | 説明 |
| :--- | :--- | :--- |
| Idle workers | io | 未使用の数は`io-concurrency` 、通常は設定された値（デフォルトは5）に近いですが、0に近い場合はディスクが遅すぎることを意味します。 |
| Idle workers | closed-engine | 閉じられているがまだクリーンアップされていないエンジンの数。通常はインデックス + テーブル同時実行性（デフォルトは 8）に近い。0 に近い場合は、 TiDB Lightning がTiKV Importer よりも高速であることを意味し、 TiDB Lightning が停止する原因になります。 |
| Idle workers | table | 未使用の数は`table-concurrency` 、通常はプロセス終了まで 0 |
| Idle workers | index | 未使用の数は`index-concurrency` 、通常はプロセス終了まで 0 |
| Idle workers | region | 未使用の数は`region-concurrency` 、通常はプロセス終了まで 0 |
| External resources | KV Encoder | アクティブなKVエンコーダをカウントします。通常はプロセス終了まで`region-concurrency`と同じです。 |
| External resources | Importer Engines | 開かれたエンジンファイルの数をカウントします`max-open-engines`設定を超えないようにしてください。 |

### 5行目: Read speed {#row-5-read-speed}

![Panels in fifth row](/media/lightning-grafana-row-5.png)

| パネル | シリーズ | 説明 |
| :--- | :--- | :--- |
| Chunk parser read block duration | read block | 解析の準備のために1ブロックのバイトを読み取るのにかかる時間 |
| Chunk parser read block duration | apply worker | アイドル状態のIO同時実行を待つのにかかった時間 |
| SQL process duration | row encode | 1行の解析とエンコードにかかる時間 |
| SQL process duration | block deliver | KV ペアのブロックを TiKV インポーターに送信するのにかかる時間 |

いずれかの期間が長すぎる場合は、 TiDB Lightningが使用するディスクが遅すぎるか、I/O でビジー状態であることを示します。

### 6行目: Storage {#row-6-storage}

![Panels in sixth row](/media/lightning-grafana-row-6.png)

| パネル | シリーズ | 説明 |
| :--- | :--- | :--- |
| SQL process rate | data deliver rate | TiKVインポーターへのデータKVペアの配信速度 |
| SQL process rate | index deliver rate | TiKVインポーターへのインデックスKVペアの配信速度 |
| SQL process rate | total deliver rate | 上記の2つのレートの合計 |
| Total bytes | parser read size | TiDB Lightningによって読み取られるバイト数 |
| Total bytes | data deliver size | TiKVインポーターにすでに配信されているデータKVペアのバイト数 |
| Total bytes | index deliver size | TiKVインポーターにすでに配信されているインデックスKVペアのバイト数 |
| Total bytes | storage_size / 3 | TiKV クラスターが占める合計サイズを 3 で割った値 (レプリカのデフォルト数) |

### 7行目: Import speed {#row-7-import-speed}

![Panels in seventh row](/media/lightning-grafana-row-7.png)

| パネル | シリーズ | 説明 |
| :--- | :--- | :--- |
| Delivery duration | Range delivery | TiKV クラスターに KV ペアの範囲をアップロードするのにかかる時間 |
| Delivery duration | SST delivery | SST ファイルを TiKV クラスターにアップロードするのにかかる時間 |
| SST process duration | Split SST | KVペアのストリームをSSTファイルに分割するのにかかる時間 |
| SST process duration | SST upload | SST ファイルのアップロードにかかる時間 |
| SST process duration | SST ingest | アップロードされた SST ファイルの取り込みにかかる時間 |
| SST process duration | SST size | SSTファイルのファイルサイズ |

## 監視メトリクス {#monitoring-metrics}

このセクションでは、 `tidb-lightning`の監視メトリックについて説明します。

`tidb-lightning`によって提供されるメトリックは、名前空間`lightning_*`下にリストされます。

- **`lightning_importer_engine`** (カウンター)

    開いているエンジンファイルと閉じているエンジンファイルの数をカウントします。ラベル:

    - **type**:
        - `open`
        - `closed`

- **`lightning_idle_workers`** （ゲージ）

    アイドル状態のワーカーをカウントします。ラベル:

    - **name**:
        - `table` : `table-concurrency`の余り。通常はプロセス終了まで 0 です。
        - `index` : `index-concurrency`の余り。通常はプロセス終了まで 0 です。
        - `region` : `region-concurrency`の余り。通常はプロセス終了まで 0 です。
        - `io` : `io-concurrency`の余り。通常は設定された値（デフォルトは 5）に近い。0 に近い場合はディスクが遅すぎることを意味する。
        - `closed-engine` : 終了したがまだクリーンアップされていないエンジンの数。通常はインデックス + テーブル同時実行数（デフォルトは8）に近い値です。0に近い値は、TiDB LightningがTiKV Importerよりも高速であることを意味し、 TiDB Lightningが停止する可能性があります。

- **`lightning_kv_encoder`** (カウンター)

    オープンおよびクローズされたKVエンコーダーをカウントします。KVエンコーダーは、SQL `INSERT`文をKVペアに変換するインメモリTiDBインスタンスです。健全な状況では、正味値は制限される必要があります。ラベル：

    - **type**:
        - `open`
        - `closed`

<!---->

- **`lightning_tables`** （カウンター）

    処理されたテーブルとそのステータスをカウントします。ラベル:

    - **state**: テーブルの状態。どのフェーズを完了する必要があるかを示します。
        - `pending` : まだ処理されていません
        - `written` : すべてのデータがエンコードされて送信されました
        - `closed` : 対応するすべてのエンジンファイルが閉じられています
        - `imported` : すべてのエンジンファイルがターゲットクラスターにインポートされました
        - `altered_auto_inc` : AUTO_INCREMENT IDが変更されました
        - `checksum` : チェックサムを実行
        - `analyzed` : 統計分析を実行しました
        - `completed` : テーブルは完全にインポートされ、検証されました
    - **result**: 現在のフェーズの結果
        - `success` : フェーズは正常に完了しました
        - `failure` : フェーズが失敗しました (完了しませんでした)

- **`lightning_engines`** （カウンター）

    処理されたエンジンファイルの数とそのステータスをカウントします。ラベル:

    - **state**: エンジンの状態。どのフェーズを完了する必要があるかを示します。
        - `pending` : まだ処理されていません
        - `written` : すべてのデータがエンコードされて送信されました
        - `closed` : エンジンファイルが閉じられました
        - `imported` : エンジンファイルがターゲットクラスターにインポートされました
        - `completed` : エンジンが完全にインポートされました
    - **result**: 現在のフェーズの結果
        - `success` : フェーズは正常に完了しました
        - `failure` : フェーズが失敗しました (完了しませんでした)

<!---->

- **`lightning_chunks`** （カウンター）

    処理されたチャンクの数とそのステータスをカウントします。ラベル:

    - **state**: チャンクのステータス。チャンクがどのフェーズにあるかを示します。
        - `estimated` : (状態ではない) この値は現在のタスク内のチャンクの合計数を示します
        - `pending` : 読み込まれているがまだ処理されていない
        - `running` : データがエンコードされ送信されています
        - `finished` : チャンク全体が処理されました
        - `failed` : 処理中にエラーが発生しました

- **`lightning_import_seconds`** （ヒストグラム）

    テーブルをインポートするために必要な時間のバケット化されたヒストグラム。

- **`lightning_row_read_bytes`** （ヒストグラム）

    単一の SQL 行のサイズのバケット化されたヒストグラム。

- **`lightning_row_encode_seconds`** (ヒストグラム)

    単一の SQL 行を KV ペアにエンコードするために必要な時間のバケット化されたヒストグラム。

- **`lightning_row_kv_deliver_seconds`** (ヒストグラム)

    1 つの SQL 行に対応する KV ペアのセットを配信するために必要な時間のバケット化されたヒストグラム。

- **`lightning_block_deliver_seconds`** （ヒストグラム）

    KV ペアのブロックをインポーターに配信するために必要な時間のバケット化されたヒストグラム。

- **`lightning_block_deliver_bytes`** （ヒストグラム）

    インポーターに配信された KV ペアのブロックの非圧縮サイズのバケット化されたヒストグラム。

- **`lightning_chunk_parser_read_block_seconds`** (ヒストグラム)

    データファイル パーサーがブロックを読み取るために必要な時間のバケット化されたヒストグラム。

- **`lightning_checksum_seconds`** （ヒストグラム）

    テーブルのチェックサムを計算するために必要な時間のバケット化されたヒストグラム。

- **`lightning_apply_worker_seconds`** (ヒストグラム)

    アイドル状態のワーカーを獲得するのに必要な時間のバケット化されたヒストグラム（ `lightning_idle_workers`ゲージも参照）。ラベル:

    - **name**:
        - `table`
        - `index`
        - `region`
        - `io`
        - `closed-engine`
