---
title: TiDB Dashboard Diagnostic Report
summary: Learn the TiDB Dashboard diagnostic report.
---

# TiDB ダッシュボード診断レポート {#tidb-dashboard-diagnostic-report}

このドキュメントでは、診断レポートの内容と表示のヒントを紹介します。クラスター診断ページにアクセスしてレポートを生成するには、 [TiDB ダッシュボードクラスタ診断ページ](/dashboard/dashboard-diagnostics-access.md)を参照してください。

## レポートをビュー {#view-report}

診断レポートは、次の部分で構成されています。

-   基本情報: 診断レポートの時間範囲、クラスターのハードウェア情報、クラスター トポロジのバージョン情報が含まれます。
-   診断情報: 自動診断の結果を表示します。
-   負荷情報:サーバー、TiDB、PD、または TiKV の CPU、メモリ、およびその他の負荷情報が含まれます。
-   概要情報: 各 TiDB、PD、または TiKV モジュールの消費時間とエラー情報が含まれます。
-   TiDB/PD/TiKV監視情報：各コンポーネントの監視情報を含みます。
-   コンフィグレーション情報: 各コンポーネントの構成情報が含まれます。

診断レポートの例は次のとおりです。

![Sample report](/media/dashboard/dashboard-diagnostics-example-table.png)

上の画像では、上部の青いボックスにある**Total Time Consume**がレポート名です。以下の赤いボックス内の情報は、このレポートの内容とレポートの各フィールドの意味を説明しています。

このレポートでは、いくつかの小さなボタンについて次のように説明しています。

-   **i**アイコン: <strong>i</strong>アイコンにマウスを移動すると、その行の説明文が表示されます。
-   **expand** : <strong>[展開]</strong>をクリックして、このモニタリング メトリックの詳細を表示します。たとえば、上の画像の`tidb_get_token`の詳細情報には、各 TiDB インスタンスのレイテンシーの監視情報が含まれています。
-   **collapse** : <strong>expand</strong>とは対照的に、ボタンは詳細な監視情報を折りたたむために使用されます。

すべてのモニタリング メトリックは、基本的に TiDB Grafana モニタリング ダッシュボードのメトリックに対応しています。モジュールが異常であることが判明した後、TiDB Grafana で詳細な監視情報を表示できます。

さらに、このレポートの`TOTAL_TIME`と`TOTAL_COUNT`メトリックは、Prometheus から読み込まれたデータを監視しているため、計算の不正確さが統計に存在する可能性があります。

以下、本報告書の各部を紹介する。

### 基本情報 {#basic-information}

#### 診断時間範囲 {#diagnostics-time-range}

診断レポートを生成する時間範囲には、開始時刻と終了時刻が含まれます。

![Report time range](/media/dashboard/dashboard-diagnostics-report-time-range.png)

#### クラスタウェア情報 {#cluster-hardware-info}

クラスタハードウェア情報には、クラスター内の各サーバーの CPU、メモリ、ディスクなどの情報が含まれます。

![Cluster hardware report](/media/dashboard/dashboard-diagnostics-cluster-hardware.png)

上記の表のフィールドは、次のように説明されています。

-   `HOST` :サーバーの IP アドレス。
-   `INSTANCE` :サーバーにデプロイされたインスタンスの数。たとえば、 `pd * 1` 、このサーバーに1 つの PD インスタンスが展開されていることを意味します。 `tidb * 2 pd * 1`このサーバーに2 つの TiDB インスタンスと 1 つの PD インスタンスがデプロイされていることを意味します。
-   `CPU_CORES` :サーバーの CPU コア (物理コアまたは論理コア) の数を示します。
-   `MEMORY` :サーバーのメモリサイズを示します。単位はGBです。
-   `DISK` :サーバーのディスク サイズを示します。単位はGBです。
-   `UPTIME` :サーバーの稼働時間。単位は日です。

#### クラスタトポロジ情報 {#cluster-topology-info}

`Cluster Info`表は、クラスターのトポロジー情報を示しています。このテーブルの情報は、TiDB [information_schema.cluster_info](/information-schema/information-schema-cluster-info.md)システム テーブルからのものです。

![Cluster info](/media/dashboard/dashboard-diagnostics-cluster-info.png)

上記の表のフィールドは、次のように説明されています。

-   `TYPE` : ノード タイプ。
-   `INSTANCE` : `IP:PORT`形式の文字列であるインスタンス アドレス。
-   `STATUS_ADDRESS` : HTTP API サービスのアドレス。
-   `VERSION` : 対応するノードのセマンティック バージョン番号。
-   `GIT_HASH` : ノード バージョンをコンパイルするときの Git コミット ハッシュ。これは、2 つのノードが完全に一貫したバージョンであるかどうかを識別するために使用されます。
-   `START_TIME` : 対応するノードの開始時刻。
-   `UPTIME` : 対応するノードの稼働時間。

### 診断情報 {#diagnostic-information}

TiDB には、自動診断結果が組み込まれています。各フィールドの説明については、 [information_schema.検査結果](/information-schema/information-schema-inspection-result.md)システム テーブルを参照してください。

### ロード情報 {#load-info}

#### ノード負荷情報 {#node-load-info}

`Node Load Info`テーブルは、時間範囲内のサーバーの次のメトリックの平均値 (AVG)、最大値 (MAX)、最小値 (MIN) を含む、サーバーノードの負荷情報を示します。

-   CPU 使用率 (最大値は`100%`です)
-   メモリ使用量
-   ディスク I/O 使用量
-   ディスク書き込みレイテンシー
-   ディスク読み取りレイテンシー
-   1 秒あたりのディスク読み取りバイト数
-   1 秒あたりのディスク書き込みバイト数
-   ノード ネットワークが 1 分あたりに受信したバイト数
-   ノード ネットワークから送信された 1 分あたりのバイト数
-   ノードによって使用されている TCP 接続の数
-   ノードのすべての TCP 接続の数

![Server Load Info report](/media/dashboard/dashboard-diagnostics-node-load-info.png)

#### インスタンスの CPU 使用率 {#instance-cpu-usage}

`Instance CPU Usage`の表は、TiDB/PD/TiKVの各プロセスのCPU使用率の平均値(AVG)、最大値(MAX)、最小値(MIN)を示しています。プロセスの最大 CPU 使用率は`100% * the number of CPU logical cores`です。

![Instance CPU Usage report](/media/dashboard/dashboard-diagnostics-process-cpu-usage.png)

#### インスタンスのメモリ使用量 {#instance-memory-usage}

`Instance Memory Usage`表は、各TiDB/PD/TiKVプロセスが占有するメモリバイトの平均値(AVG)、最大値(MAX)、最小値(MIN)を示しています。

![Instance memory usage report](/media/dashboard/dashboard-diagnostics-process-memory-usage.png)

#### TiKV スレッドの CPU 使用率 {#tikv-thread-cpu-usage}

`TiKV Thread CPU Usage`表は、TiKVにおける各モジュールスレッドのCPU使用率の平均値(AVG)、最大値(MAX)、最小値(MIN)を示しています。プロセスの最大 CPU 使用率は`100% * the thread count of the corresponding configuration`です。

![TiKV Thread CPU Usage report](/media/dashboard/dashboard-diagnostics-thread-cpu-usage.png)

上の表では、

-   `CONFIG_KEY` : 対応するモジュールの関連するスレッド構成。
-   `CURRENT_CONFIG_VALUE` : レポート生成時の構成の現在の値。

> **ノート：**
>
> `CURRENT_CONFIG_VALUE`は、このレポートの時間範囲内の値ではなく、レポートが生成されたときの値です。現在、履歴時刻の一部の構成値を取得できません。

#### <code>TiDB/PD Goroutines Count</code> {#code-tidb-pd-goroutines-count-code}

`TiDB/PD Goroutines Count`の表は、TiDBまたはPDゴルーチンの数の平均値(AVG)、最大値(MAX)、および最小値(MIN)を示しています。ゴルーチンの数が 2,000 を超えると、プロセスの同時実行性が高すぎて、全体的なリクエストレイテンシーに影響します。

![TiDB/PD goroutines count report](/media/dashboard/dashboard-diagnostics-goroutines-count.png)

### 概要情報 {#overview-information}

#### 各コンポーネントの消費時間 {#time-consumed-by-each-component}

表`Time Consumed by Each Component`は、監視された消費時間と、クラスター内の TiDB、PD、TiKV モジュールの時間比率を示しています。デフォルトの時間単位は秒です。この表を使用して、より多くの時間を消費するモジュールをすばやく見つけることができます。

![Time Consume report](/media/dashboard/dashboard-diagnostics-total-time-consume.png)

上記の表の列のフィールドは、次のように説明されています。

-   `METRIC_NAME` : モニタリング メトリックの名前。
-   `Label` : モニタリング メトリックのラベル情報。**展開を**クリックして、メトリックの各ラベルの詳細な監視情報を表示します。
-   `TIME_RATIO` : 監視行の合計時間に対する、この監視メトリックによって消費された合計時間の比率`TIME_RATIO`は`1`です。たとえば、 `kv_request`による合計消費時間は、 `tidb_query`の`1.65` (つまり、 `38325.58` / `23223.86` ) 倍です。 KV 要求は同時に実行されるため、すべての KV 要求の合計時間がクエリの合計実行時間 ( `tidb_query` ) を超える場合があります。
-   `TOTAL_TIME` : このモニタリング メトリックによって消費された合計時間。
-   `TOTAL_COUNT` : このモニタリング メトリックが実行された合計回数。
-   `P999` : このモニタリング メトリックの最大 P999 時間。
-   `P99` : このモニタリング メトリックの最大 P99 時間。
-   `P90` : このモニタリング メトリックの最大 P90 時間。
-   `P80` : このモニタリング メトリックの最大 P80 時間。

次の図は、上記の監視メトリクスにおける関連モジュールの消費時間の関係を示しています。

![Time-consumption relationship of each module](/media/dashboard/dashboard-diagnostics-time-relation.png)

上の画像では、黄色のボックスは TiDB 関連の監視メトリックです。青色のボックスは TiKV 関連の監視メトリックであり、グレーのボックスは一時的に特定の監視メトリックに対応していません。

上の画像では、 `tidb_query`の消費時間には次の 4 つの部分が含まれます。

-   `get_token`
-   `parse`
-   `compile`
-   `execute`

`execute`回には次の部分が含まれます。

-   `wait_start_tso`
-   現在監視されていない TiDBレイヤーでの実行時間
-   KV 要求時間
-   KV 要求が失敗した後のバックオフの時間である`KV_backoff`時間

上記の部分のうち、KV 要求時間には次の部分が含まれます。

-   リクエストのネットワーク送受信にかかった時間。現在、このアイテムの監視指標はありません。 KV 要求時間から`tikv_grpc_message`の時間を差し引いて、この項目を大まかに見積もることができます。
-   消費時間`tikv_grpc_message` 。

上記パーツのうち、 `tikv_grpc_message`回の消費には以下のパーツが含まれます。

-   COP タイプの要求の処理を参照する、コプロセッサーの要求時間の消費。この時間消費には、次の部分が含まれます。
    -   `tikv_cop_wait` : リクエスト キューで消費された時間。
    -   `Coprocessor handle` :コプロセッサー要求の処理にかかった時間。

-   `tikv_scheduler_command`時間の消費。これには次の部分が含まれます。
    -   `tikv_scheduler_processing_read` : 読み取り要求の処理にかかった時間。
    -   `tikv_storage_async_request`でスナップショットを取得するのにかかった時間 (スナップショットは、このモニタリング メトリックのラベルです)。
    -   書き込み要求の処理にかかった時間。この時間消費には、次の部分が含まれます。
        -   `tikv_scheduler_latch_wait` : ラッチの待機にかかった時間。
        -   `tikv_storage_async_request`の書き込みの消費時間 (書き込みは、このモニタリング メトリックのラベルです)。

上記のメトリクスのうち、 `tikv_storage_async_request`書き込みの消費時間は、次の部分を含むRaft KV の書き込みにかかる時間の消費を指します。

-   `tikv_raft_propose_wait`
-   `tikv_raft_process` 、主に`tikv_raft_append_log`を含む
-   `tikv_raft_commit_log`
-   `tikv_raft_apply_wait`
-   `tikv_raft_apply_log`

`TOTAL_TIME` 、P999 時間、および P99 時間を使用して、上記の時間消費の関係に従ってどのモジュールがより長い時間を消費しているかを判断し、関連する監視メトリックを確認できます。

> **ノート：**
>
> Raft KV 書き込みは 1 つのバッチで処理される可能性があるため、 `TOTAL_TIME`を使用して各モジュールが消費する時間を測定することは、 Raft KV 書き込みに関連するメトリック、特に`tikv_raft_process` 、 `tikv_raft_append_log` 、 `tikv_raft_commit_log` 、 `tikv_raft_apply_wait` 、および`tikv_raft_apply_log`の監視には適用されません。この状況では、各モジュールの消費時間を P999 と P99 の時間と比較する方が合理的です。
>
> その理由は、10 個の非同期書き込みリクエストがある場合、 Raft KV は内部的に 10 個のリクエストをバッチ実行にパックし、実行時間は 1 秒であるためです。したがって、各リクエストの実行時間は 1 秒で、10 リクエストの合計時間は 10 秒ですが、 Raft KV 処理の合計時間は 1 秒です。 `TOTAL_TIME`を使用して消費された時間を測定すると、残りの 9 秒がどこに費やされているかがわからない場合があります。また、 Raft KV のモニタリング メトリックと他の以前のモニタリング メトリックの違いは、リクエストの総数から確認できます ( `TOTAL_COUNT` )。

#### 各コンポーネントで発生したエラー {#errors-occurred-in-each-component}

`Errors Occurred in Each Component`の表は、TiDB と TiKV でのbinlogの書き込み失敗などの合計エラー数、 `tikv server is busy` 、 `TiKV channel full` 、 `tikv write stall`を示しています。各エラーの具体的な意味については、行のコメントを参照してください。

![Errors Occurred in Each Component report](/media/dashboard/dashboard-diagnostics-error.png)

#### 特定の TiDB/PD/TiKV 監視情報 {#specific-tidb-pd-tikv-monitoring-information}

この部分には、TiDB、PD、または TiKV のより具体的な監視情報が含まれます。

#### TiDB関連の監視情報 {#tidb-related-monitoring-information}

##### TiDB コンポーネントの消費時間 {#time-consumed-by-tidb-component}

このテーブルは、TiDB モジュールごとに消費された時間と、各時間の消費の比率を示しています。これは、概要の`time consume`のテーブルと似ていますが、このテーブルのラベル情報はより詳細です。

##### TiDB サーバー接続 {#tidb-server-connections}

この表は、各 TiDB インスタンスのクライアント接続数を示しています。

##### TiDBトランザクション {#tidb-transaction}

この表は、トランザクション関連の監視メトリックを示しています。

![Transaction report](/media/dashboard/dashboard-diagnostics-tidb-txn.png)

-   `TOTAL_VALUE` : レポート時間範囲中のすべての値の合計 (SUM)。
-   `TOTAL_COUNT` : このモニタリング メトリックの発生総数。
-   `P999` : このモニタリング メトリックの最大 P999 値。
-   `P99` : このモニタリング メトリックの最大 P99 値。
-   `P90` : このモニタリング メトリックの最大 P90 値。
-   `P80` : このモニタリング メトリックの最大 P80 値。

例：

上記の表では、レポートの時間範囲内で、 `tidb_txn_kv_write_size` : 合計約 181,296 の KV 書き込みトランザクション、および合計 KV 書き込みサイズは 266.772 MB であり、そのうちの最大 P999、P99、P90、P80 の単一トランザクションの値KV 書き込みは 116.913 KB、1.996 KB、1.905 KB、1.805 KB です。

##### DDL 所有者 {#ddl-owner}

![TiDB DDL Owner Report](/media/dashboard/dashboard-diagnostics-tidb-ddl.png)

上の表は、 `2020-05-21 14:40:00`から、クラスターの`DDL OWNER` `10.0.1.13:10080`ノードにあることを示しています。所有者が変更された場合、上記の表には複数行のデータが存在します`Min_Time`列は、対応する既知の所有者の最小時間を示します。

> **ノート：**
>
> 所有者情報が空の場合、この期間に所有者が存在しないという意味ではありません。この状況では、DDL 所有者は`ddl_worker`のモニター情報に基づいて決定されるため、この期間に`ddl_worker`が DDL ジョブを実行していない可能性があり、所有者情報が空になっている可能性があります。

TiDB のその他の監視テーブルは次のとおりです。

-   統計情報: TiDB 統計情報の関連する監視メトリックを表示します。
-   トップ 10 スロー クエリ: レポートの時間範囲内のトップ 10 スロー クエリ情報を表示します。
-   上位 10 件のスロー クエリ グループ ダイジェスト: レポートの時間範囲内の上位 10 件のスロー クエリ情報を表示します。これは、SQL フィンガープリントに従って集計されます。
-   差分プランを使用したスロー クエリ: レポートの時間範囲内で実行プランが変更される SQL ステートメント。

#### PD関連の監視情報 {#pd-related-monitoring-information}

PD モジュールの監視情報に関連するテーブルは次のとおりです。

-   `Time Consumed by PD Component` : PD 内の関連モジュールのモニタリング メトリックに費やされた時間。
-   `Blance Leader/Region` : `balance-region`と`balance leader`の監視情報が、レポートの時間範囲内にクラスタで発生しました。たとえば、 `tikv_note_1`から予定されているリーダーの数または予定されているリーダーの数です。
-   `Cluster Status` : TiKV ノードの合計数、クラスターの合計storage容量、リージョンの数、オフラインの TiKV ノードの数を含む、クラスターのステータス情報。
-   `Store Status` :リージョンスコア、リーダー スコア、リージョン/リーダーの数など、各 TiKV ノードのステータス情報を記録します。
-   `Etcd Status` : PD の etcd 関連情報。

#### TiKV関連の監視情報 {#tikv-related-monitoring-information}

TiKV モジュールの監視情報に関連するテーブルは次のとおりです。

-   `Time Consumed by TiKV Component` : TiKV の関連モジュールが消費した時間。
-   `Time Consumed by RocksDB` : TiKV で RocksDB が消費した時間。
-   `TiKV Error` : TiKV の各モジュールに関するエラー情報。
-   `TiKV Engine Size` : TiKV の各ノードに格納されている列ファミリーのデータのサイズ。
-   `Coprocessor Info` : TiKV のコプロセッサーモジュールに関する情報を監視します。
-   `Raft Info` : TiKV のRaftモジュールの監視情報。
-   `Snapshot Info` : TiKV のスナップショット関連の監視情報。
-   `GC Info` : TiKV のガベージ コレクション (GC) 関連の監視情報。
-   `Cache Hit` : TiKVにおけるRocksDBの各キャッシュのヒット率情報。

### コンフィグレーション情報 {#configuration-information}

構成情報では、一部のモジュールの構成値がレポートの時間範囲内に表示されます。ただし、これらのモジュールの他の一部の構成の履歴値は取得できないため、これらの構成の表示値は現在 (レポートが生成された時点) の値です。

レポートの時間範囲内で、次の表には、レポートの時間範囲の開始時に値が構成されている項目が含まれています。

-   `Scheduler Initial Config` : レポート開始時の PD スケジュール関連設定の初期値。
-   `TiDB GC Initial Config` : レポート開始時の TiDB GC 関連設定の初期値
-   `TiKV RocksDB Initial Config` : レポート開始時のTiKV RocksDB関連設定の初期値
-   `TiKV RaftStore Initial Config` : レポート開始時の TiKV RaftStore 関連設定の初期値

レポートの時間範囲内で、一部の構成が変更された場合、次の表には変更された一部の構成の記録が含まれます。

-   `Scheduler Config Change History`
-   `TiDB GC Config Change History`
-   `TiKV RocksDB Config Change History`
-   `TiKV RaftStore Config Change History`

例：

![Scheduler Config Change History report](/media/dashboard/dashboard-diagnostics-config-change.png)

上の表は、レポートの時間範囲内で`leader-schedule-limit`構成パラメーターが変更されたことを示しています。

-   `2020-05-22T20:00:00+08:00` : レポートの開始時に、構成値`leader-schedule-limit`は`4`です。これは構成が変更されたことを意味するのではなく、レポートの時間範囲の開始時にその構成値が`4`であることを意味します。
-   `2020-05-22T20:07:00+08:00` : `leader-schedule-limit`構成値は`8`です。これは、この構成の値が`2020-05-22T20:07:00+08:00`付近で変更されたことを示します。

次の表は、レポートが生成された時点での TiDB、PD、および TiKV の現在の構成を示しています。

-   `TiDB's Current Config`
-   `PD's Current Config`
-   `TiKV's Current Config`

## 比較レポート {#comparison-report}

2 つの時間範囲の比較レポートを生成できます。レポートの内容は、単一の時間範囲のレポートと同じですが、2 つの時間範囲の違いを示す比較列が追加されています。次のセクションでは、比較レポートのいくつかの固有のテーブルと、比較レポートを表示する方法について説明します。

まず、基本情報の`Compare Report Time Range`レポートには、比較のために 2 つの時間範囲が表示されます。

![Compare Report Time Range report](/media/dashboard/dashboard-diagnostics-compare-time.png)

上記の表で、 `t1`は通常の時間範囲、または参照時間範囲です。 `t2`は異常な時間範囲です。

スロー クエリに関連するテーブルを以下に示します。

-   `Slow Queries In Time Range t2` : `t2`でのみ表示され、 `t1`では表示されない低速クエリを示します。
-   `Top 10 slow query in time range t1` : `t1`の間の上位 10 件の遅いクエリ。
-   `Top 10 slow query in time range t2` : `t2`の間の上位 10 件の遅いクエリ。

### DIFF_RATIO の紹介 {#diff-ratio-introduction}

このセクションでは、例として`Instance CPU Usage`テーブルを使用して`DIFF_RATIO`を紹介します。

![Compare Instance CPU Usage report](/media/dashboard/dashboard-diagnostics-compare-instance-cpu-usage.png)

-   `t1.AVG` 、 `t1.MAX` 、 `t1.Min`は`t1`の CPU 使用率の平均値、最大値、および最小値です。
-   `t2.AVG` `t2.Min` `t2.MAX` `t2`中の CPU 使用率の平均値、最大値、最小値です。
-   `AVG_DIFF_RATIO` `t1`と`t2`の間の平均値の`DIFF_RATIO`です。
-   `MAX_DIFF_RATIO` `t1`と`t2`の間の最大値の`DIFF_RATIO`です。
-   `MIN_DIFF_RATIO` `t1`と`t2`の間の最小値の`DIFF_RATIO`です。

`DIFF_RATIO` : 2 つの時間範囲の差の値を示します。次の値があります。

-   モニタリング メトリックの値が`t2`範囲内にのみあり、 `t1`範囲内に値がない場合、 `DIFF_RATIO`の値は`1`です。
-   モニタリング メトリックの値が`t1`内にのみあり、 `t2`時間範囲内に値がない場合、 `DIFF_RATIO`の値は`-1`です。
-   `t2`の値が`t1`の値より大きい場合、 `DIFF_RATIO` = `(t2.value / t1.value)-1`
-   `t2`の値が`t1`の値より小さい場合、 `DIFF_RATIO` = `1-(t1.value / t2.value)`

たとえば、上記の表では、 `t2`の`tidb`ノードの平均 CPU 使用率は`t1`のそれより 2.02 倍高く、 `2.02` = `1240/410-1`です。

### 最大異項目テーブル {#maximum-different-item-table}

`Maximum Different Item`表は、2 つの時間範囲のモニタリング メトリックを比較し、モニタリング メトリックの違いに従って並べ替えます。この表を使用すると、2 つの時間範囲でどのモニタリング メトリックに最大の違いがあるかをすばやく見つけることができます。次の例を参照してください。

![Maximum Different Item table](/media/dashboard/dashboard-diagnostics-maximum-different-item.png)

-   `Table` : このモニタリング メトリックが比較レポートのどのテーブルから取得されたかを示します。たとえば、 `TiKV, coprocessor_info` TiKVコンポーネントの`coprocessor_info`テーブルを示します。
-   `METRIC_NAME` : モニタリング メトリック名。 `expand`をクリックして、指標のさまざまなラベルの比較を表示します。
-   `LABEL` : モニタリング メトリックに対応するラベル。たとえば、モニタリング メトリック`TiKV Coprocessor scan`には`instance` 、 `req` 、 `tag` 、 `sql_type`という 2 つのラベルがあり、TiKV アドレス、リクエスト タイプ、操作タイプ、および操作カラムファミリーです。
-   `MAX_DIFF` : `t1.VALUE`と`t2.VALUE`の`DIFF_RATIO`の計算である差分値。

上の表から、時間範囲`t2`は時間範囲`t1`よりもはるかに多くのコプロセッサーリクエストを持っており、時間範囲`t2`の TiDB の SQL 解析時間ははるかに長いことがわかります。
