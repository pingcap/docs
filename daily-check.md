---
title: Daily Check
summary: TiDBクラスタのパフォーマンス指標について学びましょう。
---

# 日々のチェック {#daily-check}

分散データベースであるTiDBは、その仕組みや監視項目において、スタンドアロンデータベースよりも複雑です。TiDBの運用と保守をより容易にするために、本ドキュメントではいくつかの主要なパフォーマンス指標を紹介します。

## TiDBダッシュボードの主要指標 {#key-indicators-of-tidb-dashboard}

バージョン4.0以降、TiDBは新しい運用保守管理ツール[TiDBダッシュボード](/dashboard/dashboard-intro.md)を提供します。このツールはPDコンポーネントに統合されています。TiDBダッシュボードにはデフォルトのアドレス`http://${pd-ip}:${pd_port}/dashboard`からアクセスできます。

TiDBダッシュボードは、TiDBデータベースの運用と保守を簡素化します。単一のインターフェースから、TiDBクラスタ全体の稼働状況を確認できます。以下に、いくつかのパフォーマンス指標について説明します。

### インスタンスパネル {#instance-panel}

![Instance panel](/media/instance-status-panel.png)

-   **ステータス**：このインジケーターは、ステータスが正常かどうかを確認するために使用されます。オンラインノードの場合は、このインジケーターは無視できます。
-   **稼働時間**：重要な指標です。2の`Up Time`が変更されている場合は、コンポーネントが再起動された理由を特定する必要があります。
-   **バージョン**、**デプロイメントディレクトリ**、 **Gitハッシュ**：これらの指標を確認することで、バージョンやデプロイメントディレクトリの不整合や誤りを回避できます。

### ホストパネル {#host-panel}

![Host panel](/media/host-panel.png)

CPU、メモリ、ディスクの使用状況を確認できます。いずれかのリソースの使用率が80%を超えた場合は、それに応じて容量を拡張することをお勧めします。

### SQL分析パネル {#sql-analysis-panel}

![SQL analysis panel](/media/sql-analysis-panel.png)

クラスタ内で実行されている処理の遅いSQL文を特定できます。その後、その特定のSQL文を最適化できます。

### リージョンパネル {#region-panel}

![Region panel](/media/region-panel.png)

-   `down-peer-region-count` ： Raftリーダーによって報告された、応答しないピアを持つリージョンの数。
-   `empty-region-count` ：サイズが1MiB未満の空のリージョンの数。これらのリージョンは、 `TRUNCATE TABLE` / `DROP TABLE`ステートメントを実行することによって生成されます。この数が多い場合は、 `Region Merge`有効にして複数のテーブル間でリージョンをマージすることを検討してください。
-   `extra-peer-region-count` ：追加のレプリカを持つリージョンの数。これらのリージョンはスケジューリング処理中に生成されます。
-   `learner-peer-region-count` ：学習者ピアが存在するリージョンの数。学習者ピアのソースは様々で、例えば、 TiFlashの学習者ピアや、設定済みの配置ルールに含まれる学習者ピアなどがあります。
-   `miss-peer-region-count` ：レプリカが不足しているリージョンの数。この値は必ずしも`0`より大きいとは限りません。
-   `offline-peer-region-count` ：ピアオフライン処理中のリージョン数。
-   `oversized-region-count` : サイズが`region-max-size`または`region-max-keys`より大きい領域の数。
-   `pending-peer-region-count` ： Raftログが古いリージョンの数。スケジューリング処理中に保留中のピアがいくつか生成されるのは正常です。ただし、この値が一定期間（30分以上）大きい場合は正常ではありません。
-   `undersized-region-count` : サイズが`max-merge-region-size`または`max-merge-region-keys`より小さい領域の数。

一般的に、これらの指標が小さく、かつゼロ以外の値を示すのは正常なことです。

### KVリクエスト期間 {#kv-request-duration}

![TiKV request duration](/media/kv-duration-panel.png)

TiKVにおけるKVリクエストの所要時間は99です。所要時間が長いノードが見つかった場合は、ホットスポットが存在するか、パフォーマンスの低いノードが存在するかを確認してください。

### PD TSO 待ち時間 {#pd-tso-wait-duration}

![TiDB TSO Wait Duration](/media/pd-duration-panel.png)

TiDBがPDからTSOを取得するのにかかる時間。待ち時間が長くなる理由は以下のとおりです。

-   TiDBからPDへのネットワークレイテンシーが大きい。pingコマンドを手動で実行して、ネットワークレイテンシーをテストできます。
-   TiDBサーバーへの負荷が高い。
-   PDサーバーへの負荷が高い。

### 概要パネル {#overview-panel}

![Overview panel](/media/overview-panel.png)

負荷、利用可能なメモリ、ネットワークトラフィック、およびI/Oユーティリティを確認できます。ボトルネックが見つかった場合は、容量を拡張するか、クラスタトポロジ、SQL、およびクラスタパラメータを最適化することをお勧めします。

### 例外 {#exceptions}

![Exceptions](/media/failed-query-panel.png)

各TiDBインスタンス上でSQL文の実行によって発生したエラーを確認できます。これには構文エラーや主キーの競合などが含まれます。

### GCステータス {#gc-status}

![GC status](/media/garbage-collation-panel.png)

GC（ガベージコレクション）の状態が正常かどうかは、最後にGCが実行された時刻を確認することで判断できます。GCが異常な場合、履歴データが過剰に蓄積され、アクセス効率が低下する可能性があります。
