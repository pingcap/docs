---
title: Daily Check
summary: TiDB クラスターのパフォーマンス指標について学習します。
---

# 毎日のチェック {#daily-check}

分散データベースであるTiDBは、スタンドアロンデータベースと比較して、メカニズムや監視項目の面で複雑です。このドキュメントでは、TiDBの運用と保守をより快適に行うために、いくつかの主要なパフォーマンス指標（KPI）を紹介します。

## TiDBダッシュボードの主要指標 {#key-indicators-of-tidb-dashboard}

TiDB v4.0以降、新しい運用・保守管理ツール[TiDBダッシュボード](/dashboard/dashboard-intro.md)が提供されます。このツールはPDコンポーネントに統合されています。TiDBダッシュボードには、デフォルトのアドレス`http://${pd-ip}:${pd_port}/dashboard`からアクセスできます。

TiDBダッシュボードは、TiDBデータベースの運用と保守を簡素化します。TiDBクラスタ全体の稼働状況を1つのインターフェースから確認できます。以下は、いくつかのパフォーマンス指標の説明です。

### インスタンスパネル {#instance-panel}

![Instance panel](/media/instance-status-panel.png)

-   **ステータス**: このインジケータは、ステータスが正常かどうかを確認するために使用されます。オンラインノードの場合は無視できます。
-   **稼働時間**：重要な指標です。2 `Up Time`変化している場合は、コンポーネントが再起動された理由を特定する必要があります。
-   **バージョン**、**デプロイメント ディレクトリ**、 **Git ハッシュ**: バージョン/デプロイメント ディレクトリの不一致や誤りを回避するには、これらのインジケーターをチェックする必要があります。

### ホストパネル {#host-panel}

![Host panel](/media/host-panel.png)

CPU、メモリ、ディスクの使用状況を確認できます。いずれかのリソースの使用率が80%を超える場合は、それに応じて容量をスケールアウトすることをお勧めします。

### SQL分析パネル {#sql-analysis-panel}

![SQL analysis panel](/media/sql-analysis-panel.png)

クラスター内で実行された遅いSQL文を特定し、そのSQL文を最適化することができます。

### リージョンパネル {#region-panel}

![Region panel](/media/region-panel.png)

-   `down-peer-region-count` : Raftリーダーによって報告された、応答しないピアがあるリージョンの数。
-   `empty-region-count` : 1MiB未満の空のリージョンの数。これらのリージョンは、 `TRUNCATE TABLE` / `DROP TABLE`ステートメントの実行によって生成されます。この数が多い場合は、 `Region Merge`有効にしてテーブル間でリージョンをマージすることを検討してください。
-   `extra-peer-region-count` : 追加のレプリカを持つリージョンの数。これらのリージョンはスケジューリングプロセス中に生成されます。
-   `learner-peer-region-count` : 学習者ピアが存在するリージョンの数。学習者ピアのソースは、 TiFlash内の学習者ピアや、設定された配置ルールに含まれる学習者ピアなど、多岐にわたります。
-   `miss-peer-region-count` : レプリカが不足しているリージョンの数。この値は常に`0`より大きいとは限りません。
-   `offline-peer-region-count` : ピアオフラインプロセス中のリージョンの数。
-   `oversized-region-count` : サイズが`region-max-size`または`region-max-keys`より大きい領域の数。
-   `pending-peer-region-count` : 古いRaftログを持つリージョンの数。スケジューリングプロセスで保留中のピアがいくつか生成されるのは正常です。ただし、この値が一定期間（30分以上）にわたって大きい場合は正常ではありません。
-   `undersized-region-count` : サイズが`max-merge-region-size`または`max-merge-region-keys`より小さい領域の数。

通常、これらの値が`0`でないことは正常です。ただし、かなり長い間`0`でないことは正常ではありません。

### KVリクエスト期間 {#kv-request-duration}

![TiKV request duration](/media/kv-duration-panel.png)

TiKVにおけるKVリクエストの継続時間は99です。継続時間が長いノードが見つかった場合は、ホットスポットやパフォーマンスの低いノードがないか確認してください。

### PD TSO 待機時間 {#pd-tso-wait-duration}

![TiDB TSO Wait Duration](/media/pd-duration-panel.png)

TiDBがPDからTSOを取得するのにかかる時間。待機時間が長くなる理由は次のとおりです。

-   TiDBからPDへのネットワークレイテンシーが大きい。pingコマンドを手動で実行して、ネットワークレイテンシーをテストできます。
-   TiDBサーバーの負荷が高くなります。
-   PDサーバーの負荷が高くなります。

### 概要パネル {#overview-panel}

![Overview panel](/media/overview-panel.png)

負荷、使用可能なメモリ、ネットワークトラフィック、I/Oユーティリティを確認できます。ボトルネックが見つかった場合は、キャパシティをスケールアウトするか、クラスタートポロジ、SQL、クラスターパラメータを最適化することをお勧めします。

### 例外 {#exceptions}

![Exceptions](/media/failed-query-panel.png)

各TiDBインスタンスでSQL文の実行によって発生したエラーを確認できます。これには、構文エラーや主キーの競合などが含まれます。

### GCステータス {#gc-status}

![GC status](/media/garbage-collation-panel.png)

GC（ガベージコレクション）の状態が正常かどうかは、最後にGCが発生した時刻を確認することで確認できます。GCが異常な場合、履歴データが過剰に蓄積され、アクセス効率が低下する可能性があります。
