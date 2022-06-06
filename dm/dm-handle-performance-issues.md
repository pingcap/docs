---
title: Handle Performance Issues
summary: Learn about common performance issues that might exist in DM and how to deal with them.
---

# パフォーマンスの問題を処理する {#handle-performance-issues}

このドキュメントでは、DMに存在する可能性のある一般的なパフォーマンスの問題と、それらの対処方法を紹介します。

問題を診断する前に、 [DMベンチマークレポート](https://github.com/pingcap/docs-dm/blob/release-5.3/en/dm-benchmark-v5.3.0.md)を参照できます。

パフォーマンスの問題を診断および処理するときは、次のことを確認してください。

-   DM監視コンポーネントが正しく構成およびインストールされている。
-   Grafanaモニタリングダッシュボードで[モニタリング指標](/dm/monitor-a-dm-cluster.md#task)を表示できます。
-   診断するコンポーネントはうまく機能します。そうしないと、監視メトリックの例外がパフォーマンスの問題の診断に干渉する可能性があります。

データ移行の待ち時間が長い場合、ボトルネックがDMコンポーネント内にあるのか、TiDBクラスタ内にあるのかをすばやく把握するために、最初に[ダウンストリームへのSQLステートメントの記述](#write-sql-statements-to-downstream)の`DML queue remain length`を確認できます。

## リレーログユニット {#relay-log-unit}

リレーログユニットのパフォーマンスの問題を診断するために、 `binlog file gap between master and relay`の監視メトリックを確認できます。このメトリックの詳細については、 [リレーログの監視メトリック](/dm/monitor-a-dm-cluster.md#relay-log)を参照してください。このメトリックが長期間1より大きい場合は、通常、パフォーマンスの問題があることを示しています。このメトリックが0の場合、通常、パフォーマンスの問題がないことを示します。

`binlog file gap between master and relay`の値が0であるが、パフォーマンスの問題があると思われる場合は、 `binlog pos`を確認できます。このメトリックの`master`が`relay`よりもはるかに大きい場合、パフォーマンスの問題が存在する可能性があります。この場合、それに応じてこの問題を診断して処理します。

### binlogデータを読み取る {#read-binlog-data}

`read binlog event duration`は、リレーログがアップストリームデータベース（MySQL / MariaDB）からbinlogを読み取る期間を示します。理想的には、このメトリックは、DM-workerとMySQL/MariaDBインスタンス間のネットワーク遅延に近いものです。

-   1つのデータセンターでのデータ移行の場合、binlogデータの読み取りはパフォーマンスのボトルネックにはなりません。 `read binlog event duration`の値が大きすぎる場合は、DM-workerとMySQL/MariaDBの間のネットワーク接続を確認してください。

-   地理分散環境でのデータ移行の場合は、ターゲットデータセンターにTiDBクラスタをデプロイしながら、DM-workerとMySQL/MariaDBを1つのデータセンターにデプロイしてみてください。

アップストリームデータベースからbinlogデータを読み取るプロセスには、次のサブプロセスが含まれます。

-   アップストリームのMySQL/MariaDBは、binlogデータをローカルで読み取り、ネットワーク経由で送信します。 MySQL / MariaDBのロードで例外が発生しない場合、このサブプロセスは通常、ボトルネックにはなりません。
-   binlogデータは、MySQL / MariaDBが配置されているマシンから、DM-workerが配置されているマシンにネットワーク経由で転送されます。このサブプロセスがボトルネックになるかどうかは、主にDM-workerとアップストリームのMySQL/MariaDB間のネットワーク接続に依存します。
-   DM-workerは、ネットワークデータストリームからbinlogデータを読み取り、それをbinlogイベントとして構築します。 DMワーカーのロードで例外が発生しない場合、このサブプロセスは通常、ボトルネックにはなりません。

> **ノート：**
>
> 値`read binlog event duration`が大きい場合、別の考えられる理由は、アップストリームのMySQL/MariaDBの負荷が低いことです。これは、binlogイベントを一定期間DMに送信する必要がなく、リレーログユニットが待機状態のままであるため、この値には追加の待機時間が含まれることを意味します。

### binlogデータのデコードと検証 {#binlog-data-decoding-and-verification}

binlogイベントをDMメモリに読み込んだ後、DMのリレー処理ユニットはデータをデコードして検証します。これは通常、パフォーマンスのボトルネックにはなりません。したがって、デフォルトでは、監視ダッシュボードに関連するパフォーマンスメトリックはありません。このメトリックを表示する必要がある場合は、Grafanaに監視項目を手動で追加できます。この監視項目は、Prometheusのメトリックである`dm_relay_read_transform_duration`に対応します。

### リレーログファイルの書き込み {#write-relay-log-files}

binlogイベントをリレーログファイルに書き込む場合、関連するパフォーマンスメトリックは`write relay log duration`です。 `binlog event size`が大きすぎない場合、この値はマイクロ秒である必要があります。 `write relay log duration`が大きすぎる場合は、ディスクの書き込みパフォーマンスを確認してください。書き込みパフォーマンスの低下を回避するには、DMワーカーにローカルSSDを使用します。

## ロードユニット {#load-unit}

ロードユニットの主な操作は、ローカルからSQLファイルデータを読み取り、それをダウンストリームに書き込むことです。関連するパフォーマンスメトリックは`transaction execution latency`です。この値が大きすぎる場合は、ダウンストリームデータベースの監視を確認して、ダウンストリームのパフォーマンスを確認してください。 DMとダウンストリームデータベースの間に大きなネットワーク遅延があるかどうかを確認することもできます。

## Binlogレプリケーションユニット {#binlog-replication-unit}

Binlogレプリケーションユニットのパフォーマンスの問題を診断するために、 `binlog file gap between master and syncer`の監視メトリックを確認できます。このメトリックの詳細については、 [Binlogレプリケーションの監視メトリック](/dm/monitor-a-dm-cluster.md#binlog-replication)を参照してください。

-   このメトリックが長期間1より大きい場合は、通常、パフォーマンスの問題があることを示しています。
-   このメトリックが0の場合、通常、パフォーマンスの問題がないことを示します。

`binlog file gap between master and syncer`が長期間1より大きい場合は、 `binlog file gap between relay and syncer`をチェックして、遅延が主に存在するユニットを特定します。この値が通常0の場合、遅延はリレーログユニットに存在する可能性があります。次に、 [リレーログユニット](#relay-log-unit)を参照してこの問題を解決できます。それ以外の場合は、Binlogレプリケーションユニットのチェックを続行します。

### binlogデータを読み取る {#read-binlog-data}

Binlogレプリケーションユニットは、構成に応じて、binlogイベントをアップストリームのMySQL / MariaDBから読み取るか、リレーログファイルから読み取るかを決定します。関連するパフォーマンスメトリックは`read binlog event duration`で、通常は数マイクロ秒から数十マイクロ秒の範囲です。

-   DMのBinlogレプリケーション処理ユニットがアップストリームのMySQL/MariaDBからbinlogイベントを読み取る場合、問題を特定して解決するには、「リレーログユニット」セクションの[binlogデータを読み取る](#read-binlog-data)を参照してください。

-   DMのBinlogレプリケーション処理ユニットがリレーログファイルからbinlogイベントを読み取る場合、 `binlog event size`が大きすぎない場合、 `read binlog event duration`の値はマイクロ秒である必要があります。 `read binlog event duration`が大きすぎる場合は、ディスクの読み取りパフォーマンスを確認してください。書き込みパフォーマンスの低下を回避するには、DMワーカーにローカルSSDを使用します。

### binlogイベント変換 {#binlog-event-conversion}

Binlogレプリケーションユニットは、DMLを構築し、DDLを解析し、binlogイベントデータから[テーブルルーター](/dm/dm-key-features.md#table-routing)の変換を実行します。関連するメトリックは`transform binlog event duration`です。

期間は、主にアップストリームの書き込み操作の影響を受けます。 `INSERT INTO`ステートメントを例にとると、単一の`VALUES`を変換するのにかかる時間は、多くの`VALUES`を変換するのにかかる時間とは大きく異なります。消費される時間は、数十マイクロ秒から数百マイクロ秒の範囲である可能性があります。ただし、通常、これはシステムのボトルネックではありません。

### ダウンストリームにSQLステートメントを書き込む {#write-sql-statements-to-downstream}

Binlogレプリケーションユニットが変換されたSQLステートメントをダウンストリームに書き込む場合、関連するパフォーマンスメトリックは`DML queue remain length`と`transaction execution latency`です。

binlogイベントからSQLステートメントを作成した後、DMは`worker-count`のキューを使用して、これらのステートメントをダウンストリームに同時に書き込みます。ただし、監視エントリが多すぎるのを避けるために、DMは同時キューのIDに対してモジュロ`8`演算を実行します。これは、すべての同時キューが`q_0`から`q_7`までの1つのアイテムに対応することを意味します。

`DML queue remain length`は、並行処理キューで、消費されておらず、ダウンストリームへの書き込みが開始されていないDMLステートメントの数を示します。理想的には、各`q_*`に対応する曲線はほぼ同じです。そうでない場合は、同時負荷が極端に不均衡であることを示しています。

負荷が分散されていない場合は、テーブルを移行する必要があるかどうかを確認してください。主キーまたは一意のキーがあります。これらのキーが存在しない場合は、主キーまたは一意のキーを追加します。負荷が分散されていないときにこれらのキーが存在する場合は、DMをv1.0.5以降のバージョンにアップグレードしてください。

-   データ移行リンク全体に目立った遅延がない場合、対応する`DML queue remain length`の曲線はほとんどの場合0であり、最大値はタスク構成ファイルの値`batch`を超えません。

-   データ移行リンクに顕著な遅延があり、各`q_*`に対応する`DML queue remain length`の曲線がほぼ同じで、ほとんどの場合0である場合、DMは、のアップストリームからのデータの読み取り、変換、または同時書き込みに失敗することを意味します。時間（ボトルネックはリレーログユニットにある可能性があります）。トラブルシューティングについては、このドキュメントの前のセクションを参照してください。

対応する`DML queue remain length`の曲線が0でない場合（通常、最大値は1024以下）、SQLステートメントをダウンストリームに書き込むときにボトルネックがあることを示します。 `transaction execution latency`を使用して、ダウンストリームへの単一のトランザクションを実行するために消費された時間を表示できます。

`transaction execution latency`は通常、数十ミリ秒です。この値が大きすぎる場合は、ダウンストリームデータベースの監視に基づいてダウンストリームのパフォーマンスを確認してください。 DMとダウンストリームデータベースの間に大きなネットワーク遅延があるかどうかを確認することもできます。

`BEGIN` 、または`UPDATE`などの単一の`COMMIT`をダウンストリームに書き込むのにかかる時間を表示するために、 `INSERT`をチェックすることも`statement execution latency` `DELETE` 。
