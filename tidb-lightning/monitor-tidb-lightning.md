---
title: TiDB Lightning Monitoring
summary: Learn about the monitor configuration and monitoring metrics of TiDB Lightning.
---

# TiDB Lightning監視 {#tidb-lightning-monitoring}

`tidb-lightning` [プロメテウス](https://prometheus.io/)によるメトリクス収集をサポートします。このドキュメントでは、 TiDB Lightningのモニター構成とモニタリングメトリクスを紹介します。

## モニターの設定 {#monitor-configuration}

TiDB Lightningを手動でインストールする場合は、以下の手順に従ってください。

`tidb-lightning`のメトリクスは、それが検出されている限り、Prometheus によって直接収集できます。 `tidb-lightning.toml`でメトリクス ポートを設定できます。

```toml
[lightning]
# HTTP port for debugging and Prometheus metrics pulling (0 to disable)
pprof-port = 8289

...
```

Prometheus がサーバーを検出できるように構成する必要があります。たとえば、サーバーアドレスを`scrape_configs`セクションに直接追加できます。

```yaml
...
scrape_configs:
  - job_name: 'tidb-lightning'
    static_configs:
      - targets: ['192.168.20.10:8289']
```

## グラファナダッシュボード {#grafana-dashboard}

[グラファナ](https://grafana.com/)は、Prometheus メトリクスをダッシュ​​ボードとして視覚化するための Web インターフェイスです。

### 行 1: 速度 {#row-1-speed}

![Panels in first row](/media/lightning-grafana-row-1.png)

| パネル       | シリーズ                  | 説明                                                              |
| :-------- | :-------------------- | :-------------------------------------------------------------- |
| インポート速度   | TiDB Lightningからの書き込み | TiDB Lightningから TiKV Importer への KV の送信速度 (各テーブルの複雑さによって異なります) |
| インポート速度   | tikvにアップロードする         | TiKV インポーターからすべての TiKV レプリカへの合計アップロード速度                         |
| Chunk処理時間 |                       | 1 つのデータ ファイルを完全にエンコードするのに必要な平均時間                                |

場合によっては、インポート速度がゼロに低下し、他の部分が追いつくことがあります。これは正常です。

### 行 2: 進捗状況 {#row-2-progress}

![Panels in second row](/media/lightning-grafana-row-2.png)

| パネル         | 説明                         |
| :---------- | :------------------------- |
| インポートの進行状況  | これまでにエンコードされたデータ ファイルの割合   |
| チェックサムの進行状況 | 正常にインポートされたことが確認されたテーブルの割合 |
| 失敗          | 失敗したテーブルの数とその障害点 (通常は空)    |

### 行 3: リソース {#row-3-resource}

![Panels in third row](/media/lightning-grafana-row-3.png)

| パネル                   | 説明                                 |
| :-------------------- | :--------------------------------- |
| メモリ使用量                | 各サービスが占有するメモリ量                     |
| TiDB Lightningゴルーチンの数 | TiDB Lightningによって使用される実行中のゴルーチンの数 |
| CPU％                  | 各サービスが使用する論理 CPU コアの数              |

### 行 4: クォータ {#row-4-quota}

![Panels in fourth row](/media/lightning-grafana-row-4.png)

| パネル    | シリーズ       | 説明                                                                                                                                              |
| :----- | :--------- | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| 怠惰な労働者 | イオ         | 未使用の数`io-concurrency` 、通常は設定値 (デフォルト 5) に近く、0 に近い場合はディスクが遅すぎることを意味します                                                                           |
| 怠惰な労働者 | クローズドエンジン  | 閉じられているがまだクリーンアップされていないエンジンの数。通常はインデックス + テーブル同時実行数 (デフォルトは 8) に近く、0 に近い場合は、 TiDB Lightningが TiKV Importer より高速であることを意味し、 TiDB Lightningが停止します。 |
| 怠惰な労働者 | テーブル       | 未使用の数`table-concurrency` 、通常はプロセスが終了するまで 0                                                                                                      |
| 怠惰な労働者 | 索引         | 未使用の数`index-concurrency` 、通常はプロセスが終了するまで 0                                                                                                      |
| 怠惰な労働者 | 地域         | 未使用の数`region-concurrency` 、通常はプロセスが終了するまで 0                                                                                                     |
| 外部リソース | KVエンコーダ    | アクティブな KV エンコーダをカウントします。通常はプロセスが終了するまで`region-concurrency`と同じです。                                                                                |
| 外部リソース | インポーターエンジン | 開かれたエンジン ファイルをカウントします。設定`max-open-engines`を超えることはありません                                                                                          |

### 行 5: 読み取り速度 {#row-5-read-speed}

![Panels in fifth row](/media/lightning-grafana-row-5.png)

| パネル                  | シリーズ      | 説明                                  |
| :------------------- | :-------- | :---------------------------------- |
| Chunkパーサーの読み取りブロック期間 | ブロックの読み取り | 解析の準備のためにバイトの 1 ブロックを読み取るのにかかる時間    |
| Chunkパーサーの読み取りブロック期間 | ワーカーを適用する | アイドル状態の IO 同時実行を待機するために経過した時間       |
| SQLの処理時間             | 行エンコード    | 単一行の解析とエンコードにかかる時間                  |
| SQLの処理時間             | ブロック配信    | KV ペアのブロックを TiKV インポーターに送信するのにかかる時間 |

いずれかの時間が長すぎる場合は、 TiDB Lightningによって使用されるディスクが遅すぎるか、I/O でビジーであることを示します。

### 行 6: ストレージ {#row-6-storage}

![Panels in sixth row](/media/lightning-grafana-row-6.png)

| パネル     | シリーズ         | 説明                                          |
| :------ | :----------- | :------------------------------------------ |
| SQL処理速度 | データ配信速度      | データ KV ペアの TiKV インポーターへの配信速度                |
| SQL処理速度 | インデックス配信率    | TiKV インポーターへのインデックス KV ペアの配信速度              |
| SQL処理速度 | 合計配信率        | 上記 2 つのレートの合計                               |
| 合計バイト数  | パーサーの読み取りサイズ | TiDB Lightningによって読み取られているバイト数              |
| 合計バイト数  | データ配信サイズ     | TiKV インポーターにすでに配信されたデータ KV ペアのバイト数          |
| 合計バイト数  | インデックス配信サイズ  | TiKV インポーターにすでに配信されたインデックス KV ペアのバイト数       |
| 合計バイト数  | ストレージサイズ / 3 | TiKV クラスターが占める合計サイズを 3 (デフォルトのレプリカ数) で割ったもの |

### 行 7: インポート速度 {#row-7-import-speed}

![Panels in seventh row](/media/lightning-grafana-row-7.png)

| パネル           | シリーズ      | 説明                                    |
| :------------ | :-------- | :------------------------------------ |
| 配達期間          | 範囲配達      | 一連の KV ペアを TiKV クラスターにアップロードするのにかかる時間 |
| 配達期間          | SSTの配送    | SST ファイルを TiKV クラスターにアップロードするのにかかる時間  |
| SST プロセスの所要時間 | スプリットSST  | KV ペアのストリームを SST ファイルに分割するのにかかる時間     |
| SST プロセスの所要時間 | SSTアップロード | SST ファイルのアップロードにかかる時間                 |
| SST プロセスの所要時間 | SST の取り込み | アップロードされた SST ファイルの取り込みにかかる時間         |
| SST プロセスの所要時間 | SSTサイズ    | SSTファイルのファイルサイズ                       |

## モニタリング指標 {#monitoring-metrics}

このセクションでは、 `tidb-lightning`の監視メトリクスについて説明します。

`tidb-lightning`によって提供されるメトリックは、名前空間`lightning_*`の下にリストされます。

-   **`lightning_importer_engine`** (カウンター)

    開いているエンジン ファイルと閉じているエンジン ファイルをカウントします。ラベル:

    -   **タイプ**：
        -   `open`
        -   `closed`

-   **`lightning_idle_workers`** (ゲージ)

    アイドル状態のワーカーをカウントします。ラベル:

    -   **名前**：
        -   `table` : `table-concurrency`の余り、通常はプロセスが終了するまで 0
        -   `index` : `index-concurrency`の余り、通常はプロセスが終了するまで 0
        -   `region` : `region-concurrency`の余り、通常はプロセスが終了するまで 0
        -   `io` : `io-concurrency`の残り。通常は設定値 (デフォルト 5) に近く、0 に近い場合はディスクが遅すぎることを意味します。
        -   `closed-engine` : 閉じられているがまだクリーンアップされていないエンジンの数。通常はインデックス + テーブル同時実行数に近い値 (デフォルトは 8)。 0 に近い値は、 TiDB Lightning がTiKV Importer よりも高速であることを意味し、 TiDB Lightningが停止する可能性があります。

-   **`lightning_kv_encoder`** (カウンター)

    開いた KV エンコーダーと閉じた KV エンコーダーをカウントします。 KV エンコーダーは、SQL `INSERT`ステートメントを KV ペアに変換するメモリ内の TiDB インスタンスです。健全な状況では、正味値を制限する必要があります。ラベル:

    -   **タイプ**：
        -   `open`
        -   `closed`

<!---->

-   **`lightning_tables`** (カウンター)

    処理されたテーブルとそのステータスをカウントします。ラベル:

    -   **state** : どのフェーズを完了する必要があるかを示すテーブルのステータス
        -   `pending` : まだ処理されていません
        -   `written` : すべてのデータがエンコードされて送信される
        -   `closed` : 対応するすべてのエンジン ファイルが閉じられています
        -   `imported` : すべてのエンジン ファイルがターゲット クラスターにインポートされています
        -   `altered_auto_inc` : AUTO_INCREMENT ID が変更されました
        -   `checksum` : チェックサムを実行
        -   `analyzed` : 統計分析を実行
        -   `completed` : テーブルは完全にインポートされ、検証されています。
    -   **result** : 現在のフェーズの結果
        -   `success` : フェーズは正常に完了しました
        -   `failure` : フェーズは失敗しました (完了しませんでした)

-   **`lightning_engines`** (カウンター)

    処理されたエンジン ファイルの数とそのステータスをカウントします。ラベル:

    -   **state** : エンジンのステータス。どのフェーズを完了する必要があるかを示します。
        -   `pending` : まだ処理されていません
        -   `written` : すべてのデータがエンコードされて送信される
        -   `closed` : エンジン ファイルが閉じられました
        -   `imported` : エンジン ファイルはターゲット クラスターにインポートされています
        -   `completed` : エンジンは完全にインポートされています
    -   **result** : 現在のフェーズの結果
        -   `success` : フェーズは正常に完了しました
        -   `failure` : フェーズは失敗しました (完了しませんでした)

<!---->

-   **`lightning_chunks`** (カウンター)

    処理されたチャンクの数とそのステータスをカウントします。ラベル:

    -   **state** : チャンクのステータス。チャンクがどのフェーズにあるかを示します。
        -   `estimated` : (状態ではない) この値は現在のタスクのチャンクの総数を示します。
        -   `pending` : ロードされていますが、まだ処理されていません
        -   `running` : データはエンコードされて送信されています
        -   `finished` : チャンク全体が処理されました
        -   `failed` : 処理中にエラーが発生しました

-   **`lightning_import_seconds`** (ヒストグラム)

    テーブルのインポートに必要な時間のバケット化されたヒストグラム。

-   **`lightning_row_read_bytes`** (ヒストグラム)

    単一 SQL 行のサイズのバケット化されたヒストグラム。

-   **`lightning_row_encode_seconds`** (ヒストグラム)

    単一の SQL 行を KV ペアにエンコードするのに必要な時間のバケット化されたヒストグラム。

-   **`lightning_row_kv_deliver_seconds`** (ヒストグラム)

    1 つの SQL 行に対応する KV ペアのセットを配信するのに必要な時間を表すバケット化されたヒストグラム。

-   **`lightning_block_deliver_seconds`** (ヒストグラム)

    KV ペアのブロックをインポーターに配信するのに必要な時間のバケット化されたヒストグラム。

-   **`lightning_block_deliver_bytes`** (ヒストグラム)

    インポーターに配信された KV ペアのブロックの非圧縮サイズのバケット化されたヒストグラム。

-   **`lightning_chunk_parser_read_block_seconds`**秒 (ヒストグラム)

    データ ファイル パーサーがブロックを読み取るのに必要な時間のバケット化されたヒストグラム。

-   **`lightning_checksum_seconds`** (ヒストグラム)

    テーブルのチェックサムの計算に必要な時間のバケット化されたヒストグラム。

-   **`lightning_apply_worker_seconds`** (ヒストグラム)

    アイドル状態のワーカーを取得するのに必要な時間のバケット化されたヒストグラム ( `lightning_idle_workers`ゲージも参照)。ラベル:

    -   **名前**：
        -   `table`
        -   `index`
        -   `region`
        -   `io`
        -   `closed-engine`
