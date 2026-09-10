---
title: TiDB Cloud Built-in Metrics
summary: TiDB Cloudに組み込まれているメトリクスを表示する方法と、これらのメトリクスの意味を理解する方法を学びましょう。
---

# TiDB Cloud の組み込みメトリクス {#tidb-cloud-built-in-metrics}

TiDB Cloudは、TiDBリソースの標準メトリック一式を収集し、メトリックページに表示します。これらのメトリックを確認することで、パフォーマンスの問題を容易に特定し、現在のデータベースデプロイが要件を満たしているかどうかを判断できます。

## メトリクスページを確認する {#view-the-metrics-page}

**Metrics**ページでメトリクスを表示するには、以下の手順に従ってください。

1. [**My TiDB**](https://tidbcloud.com/tidbs)ページで、対象リソースの名前をクリックすると、その概要ページに移動します。

    > **Tip:**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2. 左側のナビゲーションペインで、 **Monitoring** &gt; **Metrics**をクリックします。

## メトリクス保持ポリシー {#metrics-retention-policy}

TiDB Cloudでは、メトリクスデータは7日間保持されます。

<CustomContent plan="dedicated">

## TiDB Cloud Dedicatedクラスターのメトリクス {#metrics-for-tidb-cloud-dedicated-clusters}

以下のセクションでは、TiDB Cloud Dedicatedクラスターの**Metrics**ページに表示されるメトリクスについて説明します。

### 概要 {#overview}

| メトリック名              | ラベル                               | 説明                                                                                                                                                                                                                                                                                                                                                   |
| :------------------ | :-------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Database Time by SQL types    | database time, {SQL type}                 | データベース時間：1秒あたりのデータベース処理時間の合計。<br/> {SQL type}: SQL文が 1秒あたりに消費するデータベース時間。これは、 `SELECT` 、 `INSERT` 、 `UPDATE`などの SQL タイプごとに収集されます。                                                                                                                                                                                                             |
| Query Per Second          | {SQL type}                            | すべての TiDB ノードで 1秒あたりに実行される SQL文の数。これは、 `SELECT` 、 `INSERT` 、 `UPDATE`などの SQL タイプごとに収集されます。                                                                                                                                                                                                                                                   |
| Query Duration             | avg-{SQL type}、99-{SQL type}           | クライアントから TiDB にリクエストが送信されてから、TiDB がリクエストを実行して結果をクライアントに返すまでの時間。一般的に、クライアントのリクエストは SQL文の形式で送信されますが、この時間には`COM_PING` 、 `COM_SLEEP` 、 `COM_STMT_FETCH` 、 `COM_SEND_LONG_DATA`などのコマンドの実行時間が含まれる場合があります。TiDB はマルチクエリをサポートしており、クライアントは`select 1; select 1; select 1;`のように複数の SQL文を一度に送信できます。この場合、このクエリの合計実行時間には、すべての SQL文の実行時間が含まれます。 |
| Failed Queries             | All、{Error type} @ {instance}           | 各TiDBノードにおける1分あたりのSQL文実行エラー数に基づいた、エラーの種類（構文エラーや主キーの競合など）に関する統計情報です。エラーが発生したモジュールとエラーコードが含まれています。                                                                                                                                                                                                                                                     |
| Command Per Second         | Query、StmtExecute、およびStmtPrepare        | コマンドの種類に基づいて、すべての TiDB ノードが 1秒あたりに処理するコマンドの数。                                                                                                                                                                                                                                                                                                       |
| Queries Using Plan Cache OPS | hit、miss                            | hit: すべてのTiDBノードにおいて、1秒あたりにプランキャッシュを使用するクエリの数。<br/> miss: すべての TiDB ノードにおいて、1秒あたりにプランキャッシュに見つからないクエリの数。                                                                                                                                                                                                                                            |
| Transaction Per Second          | {types}-{transaction model}               | 1秒あたりに実行されるトランザクション数。                                                                                                                                                                                                                                                                                                                                |
| Transaction Duration          | avg-{transaction model}、99-{transaction model} | トランザクションの平均期間、または99パーセンタイル値。                                                                                                                                                                                                                                                                                                                               |
| Connection Count                 | All、active connection                      | All: すべてのTiDBノードへの接続数。<br/>アクティブな接続数：すべてのTiDBノードへのアクティブな接続数。                                                                                                                                                                                                                                                                                         |
| Disconnection Count                | {instance}-{result}                     | 各TiDBノードから切断されたクライアントの数。                                                                                                                                                                                                                                                                                                                             |

### 高度な {#advanced}

| メトリック名                        | ラベル                | 説明                                                                                                                                 |
| :---------------------------- | :----------------- | :--------------------------------------------------------------------------------------------------------------------------------- |
| Average Idle Connection Duration                    | avg-in-txn、avg-not-in-txn        | 接続アイドル時間とは、接続がアイドル状態であった時間を示します。<br/> avg-in-txn: 接続がトランザクション内にある場合の平均接続アイドル時間。<br/> avg-not-in-txn: 接続がトランザクション内にない場合の平均接続アイドル時間。 |
| Get Token Duration                | avg、99              | SQL文のトークンを取得するのに要する平均時間、または99パーセンタイル値。                                                                                             |
| Parse Duration                          | avg、99              | SQL文の解析に要する平均時間、または99パーセンタイル値。                                                                                                     |
| Compile Duration                       | avg、99              | 解析されたSQL抽象構文木（AST）を実行計画にコンパイルする際に要する平均時間、または99パーセンタイル値。                                                                            |
| Execute Duration                          | avg、99              | SQL文の実行計画の実行に要する平均時間、または99パーセンタイル値。                                                                                         |
| Average TiDB KV Request Duration           | {Request Type}         | `Get` 、 `Prewrite`などのリクエストタイプに基づいて、すべて`Commit`でKVリクエストを実行するのに要する平均時間。                                                              |
| Average TiKV gRPC Duration              | {Request Type}         | `kv_get` 、 `kv_prewrite` `kv_commit`でgRPCリクエストを実行するのに要した平均時間。                                                                      |
| Average / P99 PD TSO Wait/RPC Duration | wait-avg/99、rpc-avg/99 | 待機時間：すべてのTiDBノードにおいてPDがTSOを返すまでの待機時間の平均値、または99パーセンタイル値。<br/> RPC: PDにTSOリクエストを送信してから、すべてのTiDBノードでTSOを受信するまでの平均時間、または99パーセンタイル値。    |
| Average / P99 Storage Async Write Duration       | avg、99              | 非同期書き込みで消費される平均時間、または99パーセンタイル値。平均ストレージ非同期書き込み時間 = 平均ストレージ時間 + 平均適用時間。                                                           |
| Average / P99 Store Duration             | avg、99              | 非同期書き込み時のストレージループで消費される平均時間、または99パーセンタイル値。                                                                                         |
| Average / P99 Apply Duration                 | avg、99              | 非同期書き込み中にループを適用する際に要する平均時間、または99パーセンタイル値。                                                                                          |
| Average / P99 Append Log Duration            | avg、99              | Raftがログを追加する際に要する平均時間、または99パーセンタイル値。                                                                                               |
| Average / P99 Commit Log Duration             | avg、99              | Raftがログをコミットするのに要する平均時間、または99パーセンタイル値。                                                                                             |
| Average / P99 Apply Log Duration               | avg、99              | Raftがログを適用するために要する平均時間、または99パーセンタイル値。                                                                                              |
| Affected Rows                       | {SQL type}             | SQLタイプ別の1秒あたりの処理行数。                                                                                                                |
| Leader Count                       | {instance}               | TiKVノードによってホストされているRaftリーダーリージョンの数。                                                                                                |
| Region Count                        | {instance}               | TiKVノードによって管理されるデータ領域の総数。                                                                                                          |

### サーバ {#server}

| メトリック名            | ラベル             | 説明                                                                                         |
| :---------------- | :-------------- | :----------------------------------------------------------------------------------------- |
| TiDB Uptime         | node             | 各TiDBノードの前回再起動以降の実行時間。                                                                     |
| TiDB CPU Usage       | node、limit          | 各TiDBノードのCPU使用率統計情報または上限値。                                                                 |
| TiDB Memory Usage       | node、limit          | 各TiDBノードのメモリ使用量統計または上限値。                                                                   |
| TiKV Uptime         | node             | 各TiKVノードの前回再起動以降の実行時間。                                                                     |
| TiKV CPU Usage       | node、limit          | 各TiKVノードのCPU使用率統計または上限値。                                                                   |
| TiKV Memory Usage       | node、limit          | 各TiKVノードのメモリ使用量統計または上限値。                                                                   |
| TiKV IO Bps       | node-write、node-read | 各TiKVノードにおける、1秒あたりの読み取りおよび書き込みの総入出力バイト数。                                                   |
| TiKV Storage Usage    | node、limit          | 各TiKVノードのストレージ使用量統計または上限値。ストレージ使用量には、ストレージエンジン内の論理データサイズ、WALファイル、および一時ファイルが含まれます。    |
| TiFlash Uptime      | node             | 各TiFlashノードの前回再起動以降の実行時間。                                                                  |
| TiFlash CPU Usage    | node、limit          | 各TiFlashノードのCPU使用率統計または上限値。                                                                |
| TiFlash Memory Usage   | node、limit          | 各TiFlashノードのメモリ使用量統計または上限値。                                                                |
| TiFlash IO MBps   | node-write、node-read | 各TiFlashノードにおける読み書きの合計バイト数。                                                                |
| TiFlash Storage Usage | node、limit          | 各TiFlashノードのストレージ使用量統計または上限値。ストレージ使用量には、ストレージエンジン内の論理データサイズ、WALファイル、および一時ファイルが含まれます。 |
| TiProxy CPU Usage    | node             | 各TiProxyノードのCPU使用率統計情報。上限は100%です。                                                          |
| TiProxy Connections         | node             | 各TiProxyノード上の接続数。                                                                          |
| TiProxy Throughput    | node             | 各TiProxyノードで1秒あたりに転送されるバイト数。                                                               |
| TiProxy Sessions Migration Reasons | reason              | 1分ごとに発生するセッション移行の数と、その理由。                                                                  |

</CustomContent>

<CustomContent plan="starter,essential">

## TiDB Cloud StarterおよびTiDB Cloud Essentialインスタンスのメトリクス {#metrics-for-tidb-cloud-starter-and-tidb-cloud-essential-instances}

**Metrics**ページには、TiDB Cloud StarterとTiDB Cloud Essentialインスタンスのメトリクスを表示する2つのタブがあります。

- **Instance Overview**：インスタンスレベルの主要なメトリクスを表示します。
- **Database Status**：データベースレベルの主要なメトリックを表示します。

### インスタンスの概要 {#instance-overview}

以下の表は**Instance Overview**タブに表示されるインスタンスレベルの主要メトリクスを示しています。

| メトリック名       | ラベル                      | 説明                                                                                                                                                                 |
| :----------- | :----------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Request Units | RU per second                     | リクエストユニット（RU）は、 TiDB Cloud Starterインスタンスにおけるクエリまたはトランザクションのリソース消費量を追跡するために使用される測定単位です。ユーザークエリに加えて、バックグラウンドアクティビティもRUを消費するため、QPSが0の場合でも、1秒あたりのRU使用量はゼロにならない場合があります。 |
| Capacity vs Usage (RU/s) | Provisioned capacity (RCU)、Consumed RU/s | TiDB Cloud Essentialインスタンスにおける、1秒あたりのリクエストキャパシティユニット（RCU）と消費リクエストユニット（RU）。                                                                                             |
| Used Storage Size | Row-based storage、Row-based standard storage、Columnar storage  | 行ベースストレージ、行ベースStandardストレージ、列指向ストレージのサイズ。TiDB Cloud は、各ストレージタイプのサイズが50 MiB以上の場合にのみこのメトリックを表示します。**Row-based standard storage**は**Row-based storage**と同じ意味です。|
| Query Per Second   | All、{SQL type}             | 1秒あたりに実行される SQL文の数。これは、 `SELECT` 、 `INSERT` 、 `UPDATE`などの SQL タイプごとに収集されます。                                                                                |
| Query Duration      | Avg、P99、P99-{SQL type}     | クライアントからTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスにリクエストが送信されてから、インスタンスがリクエストを実行して結果をクライアントに返すまでの時間。                                                          |
| Failed Query   | All                       | 1秒あたりのSQL文実行エラー数。                                                                                                                                                  |
| Transaction Per Second   | All                       | 1秒あたりに実行されるトランザクション数。                                                                                                                                              |
| Transaction Duration   | Avg、P99                   | トランザクションの実行時間。                                                                                                                                                     |
| Lock-wait        | P95、P99                  | トランザクションが悲観的ロックの取得を待機する時間。値が高いほど、同じ行またはキーに対する競合が発生していることを示します。                                                                                                     |
| Total Connection   | All                       | TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスへの接続数。                                                                                                              |
| Idle Connection Duration     | P99、P99(in-txn)、P99(not-in-txn)    | トランザクションが開いている間、接続がアイドル状態になっている時間。この時間が長い場合は、通常、アプリケーションロジックの処理速度が遅いか、トランザクションの実行時間が長いことを示しています。                                                                   |

### データベースの状態 {#database-status}

以下の表は**Database Status**タブにあるデータベースレベルの主要なメトリックを示しています。

| メトリック名              | ラベル           | 説明                                                                                     |
| :------------------ | :------------ | :------------------------------------------------------------------------------------- |
| QPS Per DB              | All、{Database name} | 各データベースで1秒あたりに実行されるSQL文の数。これは、 `SELECT` 、 `INSERT` 、 `UPDATE`などのSQLタイプごとに収集されます。 |
| Average Query Duration Per DB | All、{Database name} | クライアントからデータベースへのリクエストを受信してから、データベースがリクエストを実行し、結果をクライアントに返すまでの時間。                     |
| Failed Query Per DB      | All、{Database name} | 各データベースにおける、1秒あたりのSQL文実行エラー数に基づいたエラータイプの統計情報。                                    |

</CustomContent>

## FAQ {#faq}

**1. なぜこのページの一部のペインが空になっているのですか？**

ペインにメトリクスが表示されない場合、考えられる理由は以下のとおりです。

- 対応するTiDB Cloudリソースのワークロードは、このメトリックをトリガーしません。たとえば、失敗したクエリがない場合、失敗したクエリのメトリックは常に空になります。
- お使いのTiDB CloudリソースのTiDBバージョンが低いです。これらのメトリクスを表示するには、最新バージョンのTiDBにアップグレードする必要があります。

これらの理由がすべて除外される場合は、トラブルシューティングのために[PingCAPサポートチーム](/tidb-cloud/tidb-cloud-support.md)に連絡できます。

**2. まれなケースで、メトリクスが不連続になるのはなぜでしょうか？**

まれなケースでは、メトリクスシステムが高負荷状態になった場合など、メトリクスが失われる可能性があります。

この問題が発生した場合は、 [PingCAPサポート](/tidb-cloud/tidb-cloud-support.md)に連絡してトラブルシューティングを依頼してください。
