---
title: TiDB Dashboard Diagnostic Report
summary: TiDB ダッシュボード診断レポートでは、基本、診断、負荷、概要、監視、構成情報などの診断レポートの内容を紹介します。また、比較レポートの詳細、DIFF_RATIO の説明、最大差異項目テーブルも含まれます。
---

# TiDBダッシュボード診断レポート {#tidb-dashboard-diagnostic-report}

このドキュメントでは、診断レポートの内容と表示のヒントを紹介します。クラスター診断ページにアクセスしてレポートを生成するには、 [TiDB ダッシュボードクラスタ診​​断ページ](/dashboard/dashboard-diagnostics-access.md)参照してください。

## レポートをビュー {#view-report}

診断レポートは次の部分で構成されます。

-   基本情報: 診断レポートの時間範囲、クラスターのハードウェア情報、クラスター トポロジのバージョン情報が含まれます。
-   診断情報: 自動診断の結果を表示します。
-   負荷情報:サーバー、TiDB、PD、または TiKV の CPU、メモリ、その他の負荷情報が含まれます。
-   概要情報: 各 TiDB、PD、または TiKV モジュールの消費時間とエラー情報が含まれます。
-   TiDB/PD/TiKV 監視情報: 各コンポーネントの監視情報が含まれます。
-   コンフィグレーション情報: 各コンポーネントの構成情報が含まれます。

診断レポートの例は次のとおりです。

![Sample report](/media/dashboard/dashboard-diagnostics-example-table.png)

上の画像では、上部の青いボックスにある**「Total Time Consume」**がレポート名です。下の赤いボックスの情報は、このレポートの内容とレポート内の各フィールドの意味を説明しています。

このレポートでは、いくつかの小さなボタンについて次のように説明しています。

-   **i**アイコン: マウスを**i**アイコンに移動すると、行の説明が表示されます。
-   **expand** : **expand を**クリックすると、この監視メトリックの詳細が表示されます。たとえば、上の画像の`tidb_get_token`の詳細情報には、各 TiDB インスタンスのレイテンシーの監視情報が含まれています。
-   **折りたたみ**:**展開**とは逆に、詳細な監視情報を折りたたむために使用するボタンです。

すべての監視メトリックは、基本的に TiDB Grafana 監視ダッシュボードのメトリックに対応しています。モジュールに異常が見つかった場合は、TiDB Grafana で詳細な監視情報を表示できます。

また、このレポートの`TOTAL_TIME`と`TOTAL_COUNT`メトリックは Prometheus から読み取られたデータを監視しているため、統計に計算の不正確さが存在する可能性があります。

このレポートの各部分は以下のように紹介されています。

### 基本情報 {#basic-information}

#### 診断時間範囲 {#diagnostics-time-range}

診断レポートを生成する時間範囲には、開始時刻と終了時刻が含まれます。

![Report time range](/media/dashboard/dashboard-diagnostics-report-time-range.png)

#### クラスタハードウェア情報 {#cluster-hardware-info}

クラスタハードウェア情報には、クラスター内の各サーバーの CPU、メモリ、ディスクなどの情報が含まれます。

![Cluster hardware report](/media/dashboard/dashboard-diagnostics-cluster-hardware.png)

上記の表のフィールドの説明は次のとおりです。

-   `HOST` :サーバーの IP アドレス。
-   `INSTANCE` :サーバーにデプロイされているインスタンスの数。たとえば、 `pd * 1` 、このサーバーに 1 つの PD インスタンスがデプロイされていることを意味し、 `tidb * 2 pd * 1` 、このサーバーに 2 つの TiDB インスタンスと 1 つの PD インスタンスがデプロイされていることを意味します。
-   `CPU_CORES` :サーバーの CPU コア (物理コアまたは論理コア) の数を示します。
-   `MEMORY` :サーバーのメモリサイズを示します。単位は GB です。
-   `DISK` :サーバーのディスクサイズを示します。単位は GB です。
-   `UPTIME` :サーバーの稼働時間。単位は日です。

#### クラスタトポロジ情報 {#cluster-topology-info}

`Cluster Info`テーブルには、クラスター トポロジ情報が表示されます。このテーブルの情報は、TiDB [情報スキーマ.クラスタ情報](/information-schema/information-schema-cluster-info.md)システム テーブルから取得されます。

![Cluster info](/media/dashboard/dashboard-diagnostics-cluster-info.png)

上記の表のフィールドの説明は次のとおりです。

-   `TYPE` : ノードタイプ。
-   `INSTANCE` : インスタンス アドレス ( `IP:PORT`形式の文字列)。
-   `STATUS_ADDRESS` : HTTP API サービス アドレス。
-   `VERSION` : 対応するノードのセマンティック バージョン番号。
-   `GIT_HASH` : ノード バージョンをコンパイルするときの Git コミット ハッシュ。2 つのノードが完全に一貫したバージョンであるかどうかを識別するために使用されます。
-   `START_TIME` : 対応するノードの開始時刻。
-   `UPTIME` : 対応するノードの稼働時間。

### 診断情報 {#diagnostic-information}

TiDB には自動診断結果が組み込まれています。各フィールドの説明については、 [情報スキーマ検査結果](/information-schema/information-schema-inspection-result.md)システム テーブルを参照してください。

### ロード情報 {#load-info}

#### ノード負荷情報 {#node-load-info}

`Node Load Info`表には、時間範囲内のサーバーの次のメトリックの平均値 (AVG)、最大値 (MAX)、最小値 (MIN) を含む、サーバーノードの負荷情報が表示されます。

-   CPU使用率（最大値は`100%` ）
-   メモリ使用量
-   ディスクI/O使用量
-   ディスク書き込みレイテンシー
-   ディスク読み取りレイテンシー
-   ディスク読み取りバイト数/秒
-   ディスク書き込みバイト数/秒
-   ノードネットワークが1分間に受信したバイト数
-   ノードネットワークから1分間に送信されたバイト数
-   ノードが使用しているTCP接続の数
-   ノードの全TCP接続数

![Server Load Info report](/media/dashboard/dashboard-diagnostics-node-load-info.png)

#### インスタンスのCPU使用率 {#instance-cpu-usage}

`Instance CPU Usage`表は、各 TiDB/PD/TiKV プロセスの CPU 使用率の平均値 (AVG)、最大値 (MAX)、最小値 (MIN) を示しています。プロセスの最大 CPU 使用率は`100% * the number of CPU logical cores`です。

![Instance CPU Usage report](/media/dashboard/dashboard-diagnostics-process-cpu-usage.png)

#### インスタンスのメモリ使用量 {#instance-memory-usage}

表`Instance Memory Usage`は、各 TiDB/PD/TiKV プロセスが占有するメモリバイトの平均値 (AVG)、最大値 (MAX)、最小値 (MIN) を示しています。

![Instance memory usage report](/media/dashboard/dashboard-diagnostics-process-memory-usage.png)

#### TiKV スレッド CPU 使用率 {#tikv-thread-cpu-usage}

`TiKV Thread CPU Usage`表は、TiKV 内の各モジュール スレッドの CPU 使用率の平均値 (AVG)、最大値 (MAX)、最小値 (MIN) を示しています。プロセスの最大 CPU 使用率は`100% * the thread count of the corresponding configuration`です。

![TiKV Thread CPU Usage report](/media/dashboard/dashboard-diagnostics-thread-cpu-usage.png)

上記の表では、

-   `CONFIG_KEY` : 対応するモジュールの関連スレッド構成。
-   `CURRENT_CONFIG_VALUE` : レポートが生成された時点の構成の現在の値。

> **注記：**
>
> `CURRENT_CONFIG_VALUE`はレポート生成時の値であり、このレポートの時間範囲内の値ではありません。現在、履歴時間の一部設定値は取得できません。

#### <code>TiDB/PD Goroutines Count</code> {#code-tidb-pd-goroutines-count-code}

表`TiDB/PD Goroutines Count`は、TiDB または PD の goroutine の数の平均値 (AVG)、最大値 (MAX)、最小値 (MIN) を示しています。goroutine の数が 2,000 を超えると、プロセスの同時実行性が高くなりすぎて、全体的なリクエストのレイテンシーに影響を及ぼします。

![TiDB/PD goroutines count report](/media/dashboard/dashboard-diagnostics-goroutines-count.png)

### 概要情報 {#overview-information}

#### 各コンポーネントの消費時間 {#time-consumed-by-each-component}

`Time Consumed by Each Component`表には、クラスター内の TiDB、PD、TiKV モジュールの監視された消費時間と時間比率が表示されます。デフォルトの時間単位は秒です。この表を使用すると、どのモジュールがより多くの時間を消費しているかをすばやく見つけることができます。

![Time Consume report](/media/dashboard/dashboard-diagnostics-total-time-consume.png)

上記の表の列のフィールドは次のように説明されます。

-   `METRIC_NAME` : 監視メトリックの名前。
-   `Label` : 監視メトリックのラベル情報。メトリックの各ラベルの詳細な監視情報を表示するには、 **[展開]**をクリックします。
-   `TIME_RATIO` : この監視メトリックによって消費された合計時間と、監視行の合計時間の比率。2 は`TIME_RATIO` `1` 。たとえば、 `kv_request`によって消費された合計時間は、 `tidb_query`の`1.65` (つまり、 `38325.58` / `23223.86` ) 倍です。KV 要求は同時に実行されるため、すべての KV 要求の合計時間は、クエリの合計 ( `tidb_query` ) 実行時間を超える可能性があります。
-   `TOTAL_TIME` : この監視メトリックによって消費された合計時間。
-   `TOTAL_COUNT` : この監視メトリックが実行された合計回数。
-   `P999` : この監視メトリックの最大 P999 時間。
-   `P99` : この監視メトリックの最大 P99 時間。
-   `P90` : この監視メトリックの最大 P90 時間。
-   `P80` : この監視メトリックの最大 P80 時間。

次の画像は、上記の監視メトリックにおける関連モジュールの時間消費の関係を示しています。

![Time-consumption relationship of each module](/media/dashboard/dashboard-diagnostics-time-relation.png)

上記の画像では、黄色のボックスは TiDB 関連の監視メトリックです。青色のボックスは TiKV 関連の監視メトリックであり、灰色のボックスは特定の監視メトリックに一時的に対応していません。

上の画像では、時間消費量`tidb_query`には次の 4 つの部分が含まれます。

-   `get_token`
-   `parse`
-   `compile`
-   `execute`

`execute`回には次の部分が含まれます。

-   `wait_start_tso`
-   現在監視されていないTiDBレイヤーでの実行時間
-   KV リクエスト時間
-   `KV_backoff`時間、これはKVリクエストが失敗した後のバックオフの時間です

上記の部分のうち、KV 要求時間には次の部分が含まれます。

-   ネットワークがリクエストを送受信するのにかかる時間。現在、この項目の監視メトリックはありません。KV リクエスト時間から`tikv_grpc_message`を減算すると、この項目を大まかに見積もることができます。
-   消費時間`tikv_grpc_message` 。

上記の部品のうち、 `tikv_grpc_message`回の消費量に含まれる部品は以下のとおりです。

-   コプロセッサー要求時間の消費。これは、COP タイプの要求の処理を指します。この時間消費には、次の部分が含まれます。
    -   `tikv_cop_wait` : リクエスト キューによって消費された時間。
    -   `Coprocessor handle` :コプロセッサー要求の処理に費やされた時間。

-   `tikv_scheduler_command`時間消費、これには次の部分が含まれます:
    -   `tikv_scheduler_processing_read` : 読み取り要求の処理に費やされた時間。
    -   スナップショットを`tikv_storage_async_request`で取得するのにかかった時間 (スナップショットはこの監視メトリックのラベルです)。
    -   書き込み要求の処理にかかる時間。この時間消費には次の部分が含まれます。
        -   `tikv_scheduler_latch_wait` : ラッチを待機するのにかかる時間。
        -   `tikv_storage_async_request`の書き込みの消費時間 (書き込みはこの監視メトリックのラベルです)。

上記のメトリックのうち、 `tikv_storage_async_request`の書き込み時間の消費は、次の部分を含むRaft KV の書き込み時間の消費を指します。

-   `tikv_raft_propose_wait`
-   `tikv_raft_process` 、主に`tikv_raft_append_log`含む
-   `tikv_raft_commit_log`
-   `tikv_raft_apply_wait`
-   `tikv_raft_apply_log`

`TOTAL_TIME` 、P999 時間、および P99 時間を使用して、上記の時間消費の関係に従ってどのモジュールがより長い時間を消費しているかを判断し、関連する監視メトリックを確認できます。

> **注記：**
>
> Raft KV の書き込みは 1 つのバッチで処理される可能性があるため、各モジュールで消費された時間を`TOTAL_TIME`使用して測定することは、 Raft KV の書き込みに関連するメトリック (具体的には`tikv_raft_process` 、 `tikv_raft_append_log` 、 `tikv_raft_commit_log` 、 `tikv_raft_apply_wait` 、および`tikv_raft_apply_log` ) の監視には適用できません。この状況では、各モジュールの消費時間を P999 と P99 の時間と比較する方が合理的です。
>
> その理由は、非同期書き込みリクエストが 10 件ある場合、 Raft KV は内部的に 10 件のリクエストをバッチ実行にパックし、実行時間は 1 秒だからです。そのため、各リクエストの実行時間は 1 秒で、10 件のリクエストの合計時間は 10 秒ですが、 Raft KV 処理の合計時間は 1 秒です。1 `TOTAL_TIME`使用して消費時間を計測すると、残りの 9 秒がどこに費やされているかがわからない場合があります。また、リクエストの総数 ( `TOTAL_COUNT` ) から、 Raft KV の監視メトリックとこれまでの他の監視メトリックの違いを確認できます。

#### 各コンポーネントでエラーが発生しました {#errors-occurred-in-each-component}

`Errors Occurred in Each Component`表には、 binlogの書き込み失敗、 `tikv server is busy` 、 `TiKV channel full` 、 `tikv write stall`など、TiDB と TiKV のエラーの合計数が表示されています。各エラーの具体的な意味については、行のコメントを参照してください。

![Errors Occurred in Each Component report](/media/dashboard/dashboard-diagnostics-error.png)

#### 特定の TiDB/PD/TiKV 監視情報 {#specific-tidb-pd-tikv-monitoring-information}

この部分には、TiDB、PD、または TiKV のより具体的な監視情報が含まれます。

#### TiDB関連の監視情報 {#tidb-related-monitoring-information}

##### TiDB コンポーネントの消費時間 {#time-consumed-by-tidb-component}

この表は、各 TiDB モジュールで消費された時間と各時間消費の比率を示しています。これは概要の表`time consume`と似ていますが、この表のラベル情報はより詳細です。

##### TiDB サーバー接続 {#tidb-server-connections}

この表は、各 TiDB インスタンスのクライアント接続の数を示しています。

##### TiDBトランザクション {#tidb-transaction}

この表は、トランザクション関連の監視メトリックを示しています。

![Transaction report](/media/dashboard/dashboard-diagnostics-tidb-txn.png)

-   `TOTAL_VALUE` : レポート時間範囲内のすべての値の合計 (SUM)。
-   `TOTAL_COUNT` : この監視メトリックの発生回数の合計。
-   `P999` : この監視メトリックの最大 P999 値。
-   `P99` : この監視メトリックの最大 P99 値。
-   `P90` : この監視メトリックの最大 P90 値。
-   `P80` : この監視メトリックの最大 P80 値。

例：

上記の表では、レポート時間範囲内で、 `tidb_txn_kv_write_size` ：KV 書き込みのトランザクションは合計約 181,296 件あり、KV 書き込みの合計サイズは 266.772 MB です。そのうち、KV 書き込みの単一トランザクションの最大 P999、P99、P90、P80 値は、それぞれ 116.913 KB、1.996 KB、1.905 KB、1.805 KB です。

##### DDL 所有者 {#ddl-owner}

![TiDB DDL Owner Report](/media/dashboard/dashboard-diagnostics-tidb-ddl.png)

上記の表は、 `2020-05-21 14:40:00`から、クラスターの`DDL OWNER`が`10.0.1.13:10080`ノードにあることを示しています。所有者が変更されると、上記の表に複数のデータ行が存在し、 `Min_Time`列は対応する既知の所有者の最小時間を示します。

> **注記：**
>
> 所有者情報が空の場合、この期間に所有者が存在しないことを意味するわけではありません。この状況では、DDL 所有者は`ddl_worker`の監視情報に基づいて決定されるため、 `ddl_worker`この期間に DDL ジョブを実行しておらず、所有者情報が空になっている可能性があります。

TiDB のその他の監視テーブルは次のとおりです。

-   統計情報: TiDB 統計情報の関連する監視メトリックを表示します。
-   上位 10 件の遅いクエリ: レポートの時間範囲内の上位 10 件の遅いクエリ情報を表示します。
-   ダイジェストによる上位 10 件の低速クエリ グループ: レポート時間範囲内の SQL フィンガープリントに従って集計された上位 10 件の低速クエリ情報を表示します。
-   異なるプランを持つ低速クエリ: レポート時間範囲内で実行プランが変更される SQL ステートメント。

#### PD関連モニタリング情報 {#pd-related-monitoring-information}

PD モジュールの監視情報に関連するテーブルは次のとおりです。

-   `Time Consumed by PD Component` : PD 内の関連モジュールの監視メトリックによって消費された時間。
-   `Blance Leader/Region` : `tikv_note_1`からスケジュールアウトされたリーダーの数や、スケジュールインされたリーダーの数など、レポート時間範囲内にクラスターで`balance-region`と`balance leader`の監視情報が発生しました。
-   `Cluster Status` : TiKV ノードの合計数、クラスターの合計storage容量、リージョンの数、オフラインの TiKV ノードの数などのクラスターのステータス情報。
-   `Store Status` :リージョンスコア、リーダー スコア、リージョン/リーダーの数など、各 TiKV ノードのステータス情報を記録します。
-   `Etcd Status` : PD 内の etcd 関連情報。

#### TiKV関連の監視情報 {#tikv-related-monitoring-information}

TiKV モジュールの監視情報に関連する表は次のとおりです。

-   `Time Consumed by TiKV Component` : TiKV 内の関連モジュールによって消費された時間。
-   `Time Consumed by RocksDB` : TiKV で RocksDB によって消費された時間。
-   `TiKV Error` : TiKV 内の各モジュールに関連するエラー情報。
-   `TiKV Engine Size` : TiKV 内の各ノード上の列ファミリーの保存データのサイズ。
-   `Coprocessor Info` : TiKV のコプロセッサーモジュールに関連する監視情報。
-   `Raft Info` : TiKV 内のRaftモジュールの監視情報。
-   `Snapshot Info` : TiKV 内のスナップショット関連の監視情報。
-   `GC Info` : TiKV 内のガベージ コレクション (GC) 関連の監視情報。
-   `Cache Hit` : TiKV 内の RocksDB の各キャッシュのヒット率情報。

### コンフィグレーション情報 {#configuration-information}

構成情報では、一部のモジュールの構成値がレポート時間範囲内で表示されます。ただし、これらのモジュールの他の構成の一部については履歴値を取得できないため、これらの構成の表示値は現在の値（レポート生成時）となります。

レポート時間範囲内では、次の表に、レポート時間範囲の開始時間に値が設定される項目が含まれます。

-   `Scheduler Initial Config` : レポートの開始時刻における PD スケジュール関連構成の初期値。
-   `TiDB GC Initial Config` : レポート開始時の TiDB GC 関連設定の初期値
-   `TiKV RocksDB Initial Config` : レポート開始時の TiKV RocksDB 関連設定の初期値
-   `TiKV RaftStore Initial Config` : レポート開始時の TiKV RaftStore 関連設定の初期値

レポート時間範囲内で、一部の構成が変更された場合、次のテーブルには変更された一部の構成のレコードが含まれます。

-   `Scheduler Config Change History`
-   `TiDB GC Config Change History`
-   `TiKV RocksDB Config Change History`
-   `TiKV RaftStore Config Change History`

例：

![Scheduler Config Change History report](/media/dashboard/dashboard-diagnostics-config-change.png)

上記の表は、レポート時間範囲内で`leader-schedule-limit`構成パラメータが変更されたことを示しています。

-   `2020-05-22T20:00:00+08:00` : レポートの開始時刻では、構成値`leader-schedule-limit`は`4`です。これは、構成が変更されたことを意味するのではなく、レポート時間範囲の開始時刻では、構成値が`4`であることを意味します。
-   `2020-05-22T20:07:00+08:00` : `leader-schedule-limit`構成値は`8`であり、この構成の値が`2020-05-22T20:07:00+08:00`付近で変更されたことを示します。

次の表は、レポートが生成された時点での TiDB、PD、および TiKV の現在の構成を示しています。

-   `TiDB's Current Config`
-   `PD's Current Config`
-   `TiKV's Current Config`

## 比較レポート {#comparison-report}

2 つの時間範囲の比較レポートを生成できます。レポートの内容は、2 つの時間範囲の差を示す比較列が追加されていることを除いて、単一の時間範囲のレポートと同じです。次のセクションでは、比較レポートのいくつかの固有のテーブルと、比較レポートの表示方法について説明します。

まず、基本情報の`Compare Report Time Range`のレポートには、比較のための 2 つの時間範囲が表示されます。

![Compare Report Time Range report](/media/dashboard/dashboard-diagnostics-compare-time.png)

上記の表では、 `t1`正常な時間範囲、つまり基準時間範囲です。3 `t2`異常な時間範囲です。

遅いクエリに関連するテーブルは次のように表示されます。

-   `Slow Queries In Time Range t2` : `t2`にのみ表示され、 `t1`には表示されない低速クエリを表示します。
-   `Top 10 slow query in time range t1` : `t1`期間中に最も遅いクエリのトップ 10。
-   `Top 10 slow query in time range t2` : `t2`期間中に最も遅いクエリのトップ 10。

### DIFF_RATIOの紹介 {#diff-ratio-introduction}

このセクションでは、 `Instance CPU Usage`表を例に`DIFF_RATIO`紹介します。

![Compare Instance CPU Usage report](/media/dashboard/dashboard-diagnostics-compare-instance-cpu-usage.png)

-   `t1.AVG` `t1.MAX` `t1.Min` `t1`におけるCPU使用率の平均値、最大値、最小値です。
-   `t2.AVG` `t2.Min` `t2.MAX` `t2`期間中のCPU使用率の平均値、最大値、最小値です。
-   `AVG_DIFF_RATIO`は`t1`と`t2`間の平均値の`DIFF_RATIO`です。
-   `MAX_DIFF_RATIO`は`t1`と`t2`間の最大値の`DIFF_RATIO`です。
-   `MIN_DIFF_RATIO`は`t1`と`t2`間の最小値の`DIFF_RATIO`です。

`DIFF_RATIO` : 2 つの時間範囲の差の値を示します。次の値があります。

-   監視メトリックの値が`t2`範囲内のみにあり、 `t1`範囲内に値がない場合は、 `DIFF_RATIO`の値は`1`なります。
-   監視メトリックの値が`t1`範囲内のみにあり、 `t2`時間範囲内に値がない場合は、 `DIFF_RATIO`の値は`-1`なります。
-   `t2`の値が`t1`より大きい場合、 `DIFF_RATIO` = `(t2.value / t1.value)-1`
-   `t2`の値が`t1`の値より小さい場合、 `DIFF_RATIO` = `1-(t1.value / t2.value)`

たとえば、上の表では、 `t2`の`tidb`ノードの平均 CPU 使用率は`t1`の 2.02 倍、つまり`2.02` = `1240/410-1`になります。

### 最大相違項目テーブル {#maximum-different-item-table}

`Maximum Different Item`表は、2 つの時間範囲の監視メトリックを比較し、監視メトリックの差に応じて並べ替えます。この表を使用すると、2 つの時間範囲でどの監視メトリックの差が最も大きいかをすぐに見つけることができます。次の例を参照してください。

![Maximum Different Item table](/media/dashboard/dashboard-diagnostics-maximum-different-item.png)

-   `Table` : この監視メトリックが比較レポート内のどのテーブルから取得されるかを示します。たとえば、 `TiKV, coprocessor_info` TiKVコンポーネントの`coprocessor_info`テーブルを示します。
-   `METRIC_NAME` : 監視メトリック名。メトリックのさまざまなラベルの比較を表示するには、 `expand`をクリックします。
-   `LABEL` : 監視メトリックに対応するラベル。たとえば、監視メトリック`TiKV Coprocessor scan`には、 `instance` 、 `req` 、 `tag` 、 `sql_type` 2 つのラベルがあり、これらは TiKV アドレス、リクエスト タイプ、操作タイプ、および操作カラムファミリーです。
-   `MAX_DIFF` : `t1.VALUE`と`t2.VALUE`の`DIFF_RATIO`計算結果である差の値。

上記の表から、 `t2`時間範囲では`t1`時間範囲よりもコプロセッサー要求がはるかに多く、 `t2`の TiDB の SQL 解析時間が大幅に長くなっていることがわかります。
