---
title: Daily Check
summary: TiDB クラスターのパフォーマンス指標について学習します。
---

# 毎日のチェック {#daily-check}

分散データベースである TiDB は、メカニズムや監視項目の点でスタンドアロン データベースよりも複雑です。このドキュメントでは、TiDB をより便利に運用および保守できるように、いくつかの主要なパフォーマンス指標を紹介します。

## TiDBダッシュボードの主要指標 {#key-indicators-of-tidb-dashboard}

TiDB v4.0 から、新しい運用および保守管理ツール[TiDBダッシュボード](/dashboard/dashboard-intro.md)が提供されます。このツールは PDコンポーネントに統合されています。デフォルトのアドレス`http://${pd-ip}:${pd_port}/dashboard`で TiDB ダッシュボードにアクセスできます。

TiDB ダッシュボードは、TiDB データベースの操作と保守を簡素化します。1 つのインターフェイスから、TiDB クラスター全体の実行ステータスを表示できます。次に、いくつかのパフォーマンス インジケーターについて説明します。

### インスタンスパネル {#instance-panel}

![Instance panel](/media/instance-status-panel.png)

-   **ステータス**: このインジケータは、ステータスが正常かどうかを確認するために使用されます。オンライン ノードの場合、これは無視できます。
-   **アップタイム**: 重要な指標。2 `Up Time`変更されていることがわかった場合は、コンポーネントが再起動された理由を特定する必要があります。
-   **バージョン**、**デプロイメント ディレクトリ**、 **Git ハッシュ**: バージョン/デプロイメント ディレクトリの不一致や誤りを回避するには、これらのインジケーターをチェックする必要があります。

### ホストパネル {#host-panel}

![Host panel](/media/host-panel.png)

CPU、メモリ、ディスクの使用状況を表示できます。いずれかのリソースの使用率が 80% を超える場合は、それに応じて容量をスケールアウトすることをお勧めします。

### SQL分析パネル {#sql-analysis-panel}

![SQL analysis panel](/media/sql-analysis-panel.png)

クラスター内で実行された遅い SQL ステートメントを特定できます。その後、特定の SQL ステートメントを最適化できます。

### リージョンパネル {#region-panel}

![Region panel](/media/region-panel.png)

-   `down-peer-region-count` : Raftリーダーによって報告された応答しないピアを持つリージョンの数。
-   `empty-region-count` : サイズが 1 MiB 未満の空の領域の数。これらの領域は、 `TRUNCATE TABLE` / `DROP TABLE`ステートメントを実行することによって生成されます。この数が大きい場合は、 `Region Merge`有効にしてテーブル間で領域をマージすることを検討できます。
-   `extra-peer-region-count` : 追加のレプリカを持つリージョンの数。これらのリージョンは、スケジュール プロセス中に生成されます。
-   `learner-peer-region-count` : 学習者ピアがあるリージョンの数。学習者ピアのソースはさまざまです。たとえば、 TiFlash内の学習者ピアや、構成された配置ルールに含まれる学習者ピアなどです。
-   `miss-peer-region-count` : レプリカが十分でないリージョンの数。この値は常に`0`より大きいとは限りません。
-   `offline-peer-region-count` : ピアオフラインプロセス中のリージョンの数。
-   `oversized-region-count` : サイズが`region-max-size`または`region-max-keys`より大きい領域の数。
-   `pending-peer-region-count` : 古いRaftログを持つリージョンの数。スケジューリング プロセスで保留中のピアがいくつか生成されるのは正常です。ただし、この値が一定期間 (30 分以上) にわたって大きい場合は正常ではありません。
-   `undersized-region-count` : サイズが`max-merge-region-size`または`max-merge-region-keys`より小さい領域の数。

一般的に、これらの値が`0`でないことは正常です。ただし、かなり長い間`0`でないことは正常ではありません。

### KV リクエスト期間 {#kv-request-duration}

![TiKV request duration](/media/kv-duration-panel.png)

TiKV の KV 要求期間 99。期間が長いノードが見つかった場合は、ホット スポットがあるかどうか、またはパフォーマンスが低いノードがあるかどうかを確認します。

### PD TSO 待機時間 {#pd-tso-wait-duration}

![TiDB TSO Wait Duration](/media/pd-duration-panel.png)

TiDB が PD から TSO を取得するのにかかる時間。待機時間が長くなる理由は次のとおりです。

-   TiDB から PD へのネットワークレイテンシーが長い。ping コマンドを手動で実行して、ネットワークレイテンシーをテストできます。
-   TiDBサーバーの負荷が高くなります。
-   PDサーバーの負荷が高くなります。

### 概要パネル {#overview-panel}

![Overview panel](/media/overview-panel.png)

負荷、使用可能なメモリ、ネットワーク トラフィック、および I/O ユーティリティを表示できます。ボトルネックが見つかった場合は、容量をスケール アウトするか、クラスター トポロジ、SQL、およびクラスター パラメータを最適化することをお勧めします。

### 例外 {#exceptions}

![Exceptions](/media/failed-query-panel.png)

各 TiDB インスタンスでの SQL ステートメントの実行によって発生したエラーを表示できます。これには、構文エラーや主キーの競合が含まれます。

### GC ステータス {#gc-status}

![GC status](/media/garbage-collation-panel.png)

最後の GC が発生した時刻を表示することで、GC (ガベージ コレクション) の状態が正常かどうかを確認できます。GC が異常な場合、履歴データが過剰になり、アクセス効率が低下する可能性があります。
