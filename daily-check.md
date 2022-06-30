---
title: Daily Check
summary: Learn about performance indicators of the TiDB cluster.
---

# デイリーチェック {#daily-check}

分散データベースであるTiDBは、メカニズムや監視項目の点でスタンドアロンデータベースよりも複雑です。より便利な方法でTiDBを操作および保守できるように、このドキュメントではいくつかの主要業績評価指標を紹介します。

## TiDBダッシュボードの主要な指標 {#key-indicators-of-tidb-dashboard}

v4.0以降、TiDBは新しい運用および保守管理ツール[TiDBダッシュボード](/dashboard/dashboard-intro.md)を提供します。このツールはPDコンポーネントに統合されています。デフォルトのアドレス`http://${pd-ip}:${pd_port}/dashboard`でTiDBダッシュボードにアクセスできます。

TiDBダッシュボードは、TiDBデータベースの操作と保守を簡素化します。 1つのインターフェイスを介してTiDBクラスタ全体の実行ステータスを表示できます。以下は、いくつかのパフォーマンス指標の説明です。

### インスタンスパネル {#instance-panel}

![Instance panel](/media/instance-status-panel.png)

-   **ステータス**：このインジケータは、ステータスが正常かどうかを確認するために使用されます。オンラインノードの場合、これは無視できます。
-   **稼働時間**：重要な指標。 `Up Time`が変更されていることがわかった場合は、コンポーネントが再起動された理由を特定する必要があります。
-   **バージョン**、<strong>デプロイメントディレクトリ</strong>、 <strong>Gitハッシュ</strong>：これらのインジケーターは、一貫性のない、または誤ったバージョン/デプロイメントディレクトリを回避するためにチェックする必要があります。

### ホストパネル {#host-panel}

![Host panel](/media/host-panel.png)

CPU、メモリ、およびディスクの使用状況を表示できます。リソースの使用率が80％を超える場合は、それに応じて容量をスケールアウトすることをお勧めします。

### SQL分析パネル {#sql-analysis-panel}

![SQL analysis panel](/media/sql-analysis-panel.png)

クラスタで実行された遅いSQLステートメントを見つけることができます。次に、特定のSQLステートメントを最適化できます。

### 地域パネル {#region-panel}

![Region panel](/media/region-panel.png)

-   `miss-peer-region-count` ：十分なレプリカがないリージョンの数。この値は常に`0`より大きいとは限りません。
-   `extra-peer-region-count` ：追加のレプリカを持つリージョンの数。これらのリージョンは、スケジューリングプロセス中に生成されます。
-   `empty-region-count` ： `TRUNCATE TABLE` `DROP TABLE`の実行によって生成された空のリージョンの数。この数が多い場合は、 `Region Merge`を有効にしてテーブル間でリージョンをマージすることを検討できます。
-   `pending-peer-region-count` ：古いRaftログがあるリージョンの数。スケジューリングプロセスでいくつかの保留中のピアが生成されるのは正常です。ただし、この値が一定期間（30分を超える）大きい場合は正常ではありません。
-   `down-peer-region-count` ：Raftリーダーによって報告された応答しないピアを持つリージョンの数。
-   `offline-peer-region-count` ：オフラインプロセス中のリージョンの数。

通常、これらの値は`0`ではありません。しかし、かなり長い間`0`でないのは普通ではありません。

### KVリクエスト期間 {#kv-request-duration}

![TiKV request duration](/media/kv-duration-panel.png)

TiKVでのKV要求期間99。持続時間が長いノードを見つけた場合は、ホットスポットがあるかどうか、またはパフォーマンスの低いノードがあるかどうかを確認してください。

### PDTSO待機時間 {#pd-tso-wait-duration}

![TiDB TSO Wait Duration](/media/pd-duration-panel.png)

TiDBがPDからTSOを取得するのにかかる時間。待機時間が長い理由は次のとおりです。

-   TiDBからPDへの高いネットワーク遅延。 pingコマンドを手動で実行して、ネットワーク遅延をテストできます。
-   TiDBサーバーの負荷が高い。
-   PDサーバーの負荷が高い。

### 概要パネル {#overview-panel}

![Overview panel](/media/overview-panel.png)

負荷、使用可能なメモリ、ネットワークトラフィック、およびI/Oユーティリティを表示できます。ボトルネックが見つかった場合は、容量をスケールアウトするか、クラスタトポロジ、SQL、クラスタパラメーターなどを最適化することをお勧めします。

### 例外 {#exceptions}

![Exceptions](/media/failed-query-panel.png)

各TiDBインスタンスでSQLステートメントの実行によってトリガーされたエラーを表示できます。これらには、構文エラー、主キーの競合などが含まれます。

### GCステータス {#gc-status}

![GC status](/media/garbage-collation-panel.png)

最後のGCが発生した時刻を表示することで、GC（ガベージコレクション）ステータスが正常かどうかを確認できます。 GCが異常な場合、履歴データが過剰になり、アクセス効率が低下する可能性があります。
