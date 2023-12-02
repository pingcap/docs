---
title: Daily Check
summary: Learn about performance indicators of the TiDB cluster.
---

# 毎日のチェック {#daily-check}

TiDB は分散型データベースであるため、スタンドアロン型データベースに比べて仕組みや監視項目が複雑になります。 TiDB をより便利な方法で運用および保守できるように、このドキュメントではいくつかの重要なパフォーマンス指標を紹介します。

## TiDB ダッシュボードの主要な指標 {#key-indicators-of-tidb-dashboard}

TiDB は v4.0 から、新しい運用および保守管理ツール[TiDB ダッシュボード](/dashboard/dashboard-intro.md)を提供します。このツールは PDコンポーネントに統合されています。 TiDB ダッシュボードにはデフォルトのアドレス`http://${pd-ip}:${pd_port}/dashboard`でアクセスできます。

TiDB ダッシュボードは、TiDB データベースの運用とメンテナンスを簡素化します。 1 つのインターフェイスを通じて TiDB クラスター全体の実行ステータスを表示できます。以下に、いくつかのパフォーマンス指標について説明します。

### インスタンスパネル {#instance-panel}

![Instance panel](/media/instance-status-panel.png)

-   **ステータス**: ステータスが正常かどうかを確認するために使用されます。オンライン ノードの場合、これは無視できます。
-   **稼働時間**: 重要な指標。 `Up Time`が変更されたことがわかった場合は、コンポーネントが再起動された理由を特定する必要があります。
-   **バージョン**、**デプロイメント ディレクトリ**、 **Git ハッシュ**: これらのインジケーターは、バージョン/デプロイメント ディレクトリの不一致や不正確を避けるためにチェックする必要があります。

### ホストパネル {#host-panel}

![Host panel](/media/host-panel.png)

CPU、メモリ、ディスクの使用状況を表示できます。リソースの使用率が 80% を超えた場合は、それに応じて容量をスケールアウトすることをお勧めします。

### SQL分析パネル {#sql-analysis-panel}

![SQL analysis panel](/media/sql-analysis-panel.png)

クラスター内で実行された遅い SQL ステートメントを見つけることができます。その後、特定の SQL ステートメントを最適化できます。

### リージョンパネル {#region-panel}

![Region panel](/media/region-panel.png)

-   `miss-peer-region-count` : 十分なレプリカがないリージョンの数。この値は常に`0`より大きいとは限りません。
-   `extra-peer-region-count` : 追加のレプリカを持つリージョンの数。これらの領域は、スケジューリング プロセス中に生成されます。
-   `empty-region-count` : `TRUNCATE TABLE` / `DROP TABLE`ステートメントの実行によって生成される空のリージョンの数。この数が大きい場合は、 `Region Merge`有効にしてテーブル全体のリージョンをマージすることを検討できます。
-   `pending-peer-region-count` : 古いRaftログを持つリージョンの数。スケジューリング プロセスでいくつかの保留ピアが生成されるのは正常です。ただし、この値が一定期間 (30 分を超えて) 大きくなる場合は異常ではありません。
-   `down-peer-region-count` : Raftリーダーによって報告された、応答しないピアのあるリージョンの数。
-   `offline-peer-region-count` : オフラインプロセス中のリージョンの数。

一般に、これらの値が`0`でないのは正常です。しかし、かなり長い間`0`でないのは普通ではありません。

### KV リクエスト期間 {#kv-request-duration}

![TiKV request duration](/media/kv-duration-panel.png)

TiKV の KV リクエスト期間は 99。継続時間が長いノードが見つかった場合は、ホット スポットが存在していないか、パフォーマンスが低下しているノードが存在していないかを確認してください。

### PD TSO 待機時間 {#pd-tso-wait-duration}

![TiDB TSO Wait Duration](/media/pd-duration-panel.png)

TiDB が PD から TSO を取得するのにかかる時間。待機時間が長くなる理由は次のとおりです。

-   TiDB から PD までのネットワークレイテンシーが長い。 ping コマンドを手動で実行して、ネットワークレイテンシーをテストできます。
-   TiDBサーバーの高負荷。
-   PDサーバーの負荷が高い。

### 概要パネル {#overview-panel}

![Overview panel](/media/overview-panel.png)

負荷、使用可能なメモリ、ネットワーク トラフィック、および I/O ユーティリティを表示できます。ボトルネックが見つかった場合は、容量をスケールアウトするか、クラスター トポロジ、SQL、およびクラスター パラメーターを最適化することをお勧めします。

### 例外 {#exceptions}

![Exceptions](/media/failed-query-panel.png)

各 TiDB インスタンスでの SQL ステートメントの実行によってトリガーされたエラーを表示できます。これには、構文エラーや主キーの競合が含まれます。

### GCステータス {#gc-status}

![GC status](/media/garbage-collation-panel.png)

前回の GC が発生した時刻を確認することで、GC (ガベージ コレクション) の状態が正常かどうかを確認できます。 GCが異常な場合、履歴データが過剰になり、アクセス効率が低下する可能性があります。
