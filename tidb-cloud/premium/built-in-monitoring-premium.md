---
title: "TiDB Cloud Premium Built-in Metrics"
summary: TiDB Cloud Premiumに組み込まれているメトリクスを表示する方法と、これらのメトリクスの意味を理解する方法を学びましょう。
---

# TiDB Cloud Premium の組み込みメトリクス {#tidb-cloud-premium-built-in-metrics}

TiDB Cloudは、 TiDB Cloud Premiumインスタンスの標準メトリック一式を収集し、メトリックページに表示します。これらのメトリックを確認することで、パフォーマンスの問題を容易に特定し、現在のデータベース環境が要件を満たしているかどうかを判断できます。

## メトリクスページを確認する {#view-the-metrics-page}

**Metrics**ページでメトリクスを表示するには、以下の手順に従ってください。

1. [**My TiDB**](https://tidbcloud.com/tidbs)ページで、対象のTiDB Cloud Premiumインスタンスの名前をクリックすると、その概要ページに移動します。

    > **Tip:**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2. 左側のナビゲーションペインで、 **Monitoring** &gt; **Metrics**をクリックします。

## メトリクス保持ポリシー {#metrics-retention-policy}

TiDB Cloud Premiumインスタンスの場合、メトリクスデータは7日間保持されます。

## TiDB Cloud Premiumインスタンスのメトリクス {#metrics-for-tidb-cloud-premium-instances}

以下のセクションでは、TiDB Cloud Premiumインスタンスの**Metrics**ページに表示されるメトリクスについて説明します。

### 概要 {#overview}

| メトリック名              | ラベル                                                                                                                             | 説明                                                                                                                                                                                                                                                                                |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Request Units per Second    | Total RU per second、AVG RU/s                                                                                                               | リクエストユニット (RU) は、クエリまたはトランザクションのリソース消費を追跡するために使用される測定単位です。 `Total RU per second` 1秒あたりのリアルタイム RU 消費量を表示します。 `AVG RU/s`は選択した時間範囲における 1秒あたりの平均 RU 消費量を表示し、リソース消費量をよりよく理解するのに役立ちます。実行するクエリに加えて、バックグラウンド アクティビティも RU を消費する可能性があります。そのため、QPS が 0 の場合でも、1秒あたりの RU 消費量は 0 を超える場合があります。 |
| Used Storage Size        | {type}                                                                                                                           | 行ストアのサイズと列ストアのサイズ。                                                                                                                                                                                                                                                                |
| Query Per Second          | All、{SQL type}                                                                                                                    | 1秒あたりに実行される SQL文の数。これは、 `SELECT` 、 `INSERT` 、 `UPDATE`などの SQL タイプごとに収集されます。                                                                                                                                                                                               |
| Query Duration             | avg、avg-{SQL type}、99、99-{SQL type}                                                                                                 | クライアントからTiDBへのリクエストを受信して​​から、TiDBがリクエストを実行し、結果をクライアントに返すまでの時間。                                                                                                                                                                                                                    |
| Database Time by SQL Types  | All、{SQL type}                                                                                                                    | すべて：1秒あたりのデータベース処理時間の合計。<br/> {SQL type}: SQL文が 1秒あたりに消費するデータベース時間。これは、 `SELECT` 、 `INSERT` 、 `UPDATE`などの SQL タイプごとに収集されます。                                                                                                                                               |
| Failed Queries             | All                                                                                                                              | 1分あたりのSQL文実行エラー数に基づいた、エラーの種類（構文エラーや主キーの競合など）の統計情報。                                                                                                                                                                                                                                |
| Command Per Second         | {type}                                                                                                                           | コマンドの種類に基づいた、1秒あたりに処理されるコマンドの数。                                                                                                                                                                                                                                                   |
| Queries Using Plan Cache OPS | hit、miss                                                                                                                          | hit: プランキャッシュを使用するクエリが1秒あたりに実行される回数。<br/> miss: 1秒あたりにプランキャッシュに見つからないクエリの数。                                                                                                                                                                                                       |
| Transaction Per Second          | {types}-{transaction model}                                                                                                             | 1秒あたりに実行されるトランザクション数。                                                                                                                                                                                                                                                             |
| Transaction Duration          | avg-{transaction model}、99-{transaction model}                                                                                               | トランザクションの平均期間、または99パーセンタイル値。                                                                                                                                                                                                                                                            |
| Connection Count                 | All、active connection                                                                                                                    | すべて：接続数。<br/>アクティブな接続数：アクティブな接続の数。                                                                                                                                                                                                                                                |
| Disconnection Count                | {result}                                                                                                                            | 接続が切断されたクライアントの数。                                                                                                                                                                                                                                                                 |
| Table Count by TTL Schedule Delay | `{name}`                                                                                                                        | スケジュール遅延ごとにグループ化された TTL が有効なテーブルの数を表示します。 `name`ラベルは遅延バケットです。バケットの値として、 `01 hour` 、 `02 hour` 、 `06 hour` 、 `12 hour` 、 `24 hour` 、 `72 hour` 、 `one week` 、および`others` 。                                                                                                         |
| TTL Insert/Delete Rows by Day      | `insert current day` 、 `delete current day` 、 `insert last day` 、 `delete last day` 、 `insert 2 days ago` 、 `delete 2 days ago` | TTL管理テーブルに挿入された行数と、TTLジョブによって削除された行数を、各暦日ごとに表示します。挿入数が削除数を継続的に上回る状態が続く場合は、TTL処理がデータ取り込みに追いついていないことを示しており、ストレージの増加につながる可能性があります。複数日にわたって値を比較することで、通常のワークロードの変動と長期的なバックログの傾向を区別できます。                                                                                              |

### データベース {#database}

| メトリック名           | ラベル                             | 説明                                                                                     |
| :--------------- | :------------------------------ | :------------------------------------------------------------------------------------- |
| QPS Per DB           | All、{database}                    | 各データベースで1秒あたりに実行されるSQL文の数。これは、 `SELECT` 、 `INSERT` 、 `UPDATE`などのSQLタイプごとに収集されます。 |
| Query Duration Per DB | avg、avg-{database}、99、99-{database} | クライアントからデータベースへのリクエストを受信して​​から、データベースがリクエストを実行し、結果をクライアントに返すまでの時間。                     |
| Failed Query Per DB   | All、{database}                    | 各データベースにおける、1秒あたりのSQL文実行エラー数に基づいたエラータイプの統計情報。                                    |

### 高度な {#advanced}

| メトリック名                        | ラベル                | 説明                                                                                                                                 |
| :---------------------------- | :----------------- | :--------------------------------------------------------------------------------------------------------------------------------- |
| Average Idle Connection Duration                    | avg-in-txn、avg-not-in-txn        | 接続アイドル時間とは、接続がアイドル状態であった時間を示します。<br/> avg-in-txn: 接続がトランザクション内にある場合の平均接続アイドル時間。<br/> avg-not-in-txn: 接続がトランザクション内にない場合の平均接続アイドル時間。 |
| Get Token Duration                | avg、99              | SQL文のトークンを取得するのに要する平均時間、または99パーセンタイル値。                                                                                             |
| Parse Duration                          | avg、99              | SQL文の解析に要する平均時間、または99パーセンタイル値。                                                                                                     |
| Compile Duration                       | avg、99              | 解析されたSQL抽象構文木（AST）を実行計画にコンパイルする際に要する平均時間、または99パーセンタイル値。                                                                            |
| Execute Duration                          | avg、99              | SQL文の実行計画の実行に要する平均時間、または99パーセンタイル値。                                                                                         |
| Average TiDB KV Request Duration           | {Request Type}         | `Get` 、 `Prewrite`などのリクエストタイプに基づいて、KV `Commit` 。                                                                                   |
| Average / P99 PD TSO Wait/RPC Duration | wait-avg/99、rpc-avg/99 | 待機時間：PDがTSOに戻るまでの待ち時間の平均または99パーセンタイル値。<br/> RPC: PDにTSOリクエストを送信してからTSOを受信するまでの平均時間、または99パーセンタイル値。                                  |

## FAQ {#faq}

**1. なぜこのページの一部のペインが空になっているのですか？**

ペインにメトリクスが表示されない場合、考えられる理由は以下のとおりです。

- 対応するTiDB Cloud Premiumインスタンスのワークロードは、このメトリックをトリガーしません。たとえば、失敗したクエリがない場合、失敗したクエリのメトリックは常に空になります。
- TiDB Cloud PremiumインスタンスのTiDBバージョンが低いです。これらのメトリクスを表示するには、最新バージョンのTiDBにアップグレードする必要があります。

これらの理由がすべて除外される場合は、トラブルシューティングのために[PingCAPサポートチーム](/tidb-cloud/tidb-cloud-support.md)に連絡できます。

**2. まれなケースで、メトリクスが不連続になるのはなぜでしょうか？**

まれなケースでは、メトリクスシステムが高負荷状態になった場合など、メトリクスが失われる可能性があります。

この問題が発生した場合は、 [PingCAPサポート](/tidb-cloud/tidb-cloud-support.md)に連絡してトラブルシューティングを依頼してください。
