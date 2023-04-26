---
title: Handle Performance Issues of TiDB Data Migration
summary: Learn about common performance issues that might exist in DM and how to deal with them.
---

# TiDB データ移行のパフォーマンスの問題を処理する {#handle-performance-issues-of-tidb-data-migration}

このドキュメントでは、DM に存在する可能性のある一般的なパフォーマンスの問題とその対処方法について説明します。

問題を診断する前に、 [DM ベンチマーク レポート](https://github.com/pingcap/docs-dm/blob/release-5.3/en/dm-benchmark-v5.3.0.md)を参照できます。

パフォーマンスの問題を診断して処理するときは、次のことを確認してください。

-   DM 監視コンポーネントが正しく構成され、インストールされている。
-   [メトリックの監視](/dm/monitor-a-dm-cluster.md#task) Grafana 監視ダッシュボードで確認できます。
-   診断したコンポーネントはうまく機能します。そうしないと、モニタリング メトリックの例外が発生し、パフォーマンスの問題の診断が妨げられる可能性があります。

データ移行で大きなレイテンシーが発生した場合、ボトルネックが DMコンポーネント内にあるか、TiDB クラスター内にあるかをすばやく把握するには、まず`DML queue remain length` in [ダウンストリームへの SQL ステートメントの書き込み](#write-sql-statements-to-downstream)を確認します。

## リレーログユニット {#relay-log-unit}

リレー ログ ユニットでパフォーマンスの問題を診断するには、 `binlog file gap between master and relay`監視メトリックを確認します。このメトリックの詳細については、 [リレーログの監視メトリクス](/dm/monitor-a-dm-cluster.md#relay-log)を参照してください。このメトリックが長時間 1 より大きい場合は、通常、パフォーマンスの問題があることを示しています。このメトリックが 0 の場合、通常はパフォーマンスの問題がないことを示します。

`binlog file gap between master and relay`の値が 0 であるが、パフォーマンスの問題があると思われる場合は、 `binlog pos`確認できます。このメトリクスの`master` `relay`よりはるかに大きい場合、パフォーマンスの問題が存在する可能性があります。この場合、この問題を適切に診断して処理してください。

### binlogデータの読み取り {#read-binlog-data}

`read binlog event duration` 、リレー ログがアップストリーム データベース (MySQL/MariaDB) からbinlogを読み取る期間を表します。理想的には、このメトリクスは DM-worker と MySQL/MariaDB インスタンス間のネットワークレイテンシーに近い値です。

-   1 つのデータ センターでのデータ移行の場合、 binlogデータの読み取りはパフォーマンスのボトルネックにはなりません。 `read binlog event duration`の値が大きすぎる場合は、DM-worker と MySQL/MariaDB 間のネットワーク接続を確認してください。

-   地理的に分散した環境でのデータ移行の場合、DM-worker と MySQL/MariaDB を 1 つのデータ センターに展開し、TiDB クラスターをターゲット データ センターに展開してみてください。

アップストリーム データベースからbinlogデータを読み取るプロセスには、次のサブプロセスが含まれます。

-   アップストリームの MySQL/MariaDB はbinlogデータをローカルで読み取り、ネットワーク経由で送信します。 MySQL/MariaDB のロードで例外が発生しない場合、通常、このサブプロセスはボトルネックにはなりません。
-   binlogデータは、MySQL/MariaDB が配置されているマシンから DM-worker が配置されているマシンにネットワーク経由で転送されます。このサブプロセスがボトルネックになるかどうかは、主に DM-worker と上流の MySQL/MariaDB 間のネットワーク接続に依存します。
-   DM-worker は、ネットワーク データ ストリームからbinlogデータを読み取り、それをbinlogイベントとして構築します。 DM-worker 負荷で例外が発生しない場合、通常、このサブプロセスはボトルネックにはなりません。

> **ノート：**
>
> `read binlog event duration`の値が大きい場合、別の理由として、上流の MySQL/MariaDB の負荷が低いことが考えられます。これは、一定期間binlogイベントを DM に送信する必要がなく、リレー ログ ユニットが待機状態のままであることを意味します。したがって、この値には追加の待機時間が含まれます。

### binlogデータのデコードと検証 {#binlog-data-decoding-and-verification}

binlogイベントを DMメモリに読み取った後、DM のリレー処理ユニットはデータをデコードして検証します。これは通常、パフォーマンスのボトルネックにはなりません。したがって、デフォルトでは、監視ダッシュボードに関連するパフォーマンス メトリックはありません。このメトリクスを表示する必要がある場合は、Grafana で監視項目を手動で追加できます。この監視項目は、Prometheus のメトリックである`dm_relay_read_transform_duration`に対応します。

### リレーログファイルの書き込み {#write-relay-log-files}

binlogイベントをリレー ログ ファイルに書き込む場合、関連するパフォーマンス メトリックは`write relay log duration`です。 `binlog event size`が大きすぎない場合、この値はマイクロ秒にする必要があります。 `write relay log duration`が大きすぎる場合は、ディスクの書き込みパフォーマンスを確認してください。書き込みパフォーマンスの低下を回避するには、DM ワーカーにローカル SSD を使用します。

## 負荷ユニット {#load-unit}

ロード ユニットの主な操作は、SQL ファイル データをローカルから読み取り、ダウンストリームに書き込むことです。関連するパフォーマンス メトリックは`transaction execution latency`です。この値が大きすぎる場合は、ダウンストリーム データベースの監視を確認して、ダウンストリームのパフォーマンスを確認します。 DM とダウンストリーム データベースの間に大きなネットワークレイテンシーがあるかどうかを確認することもできます。

## Binlogレプリケーション ユニット {#binlog-replication-unit}

Binlogレプリケーション ユニットのパフォーマンスの問題を診断するには、 `binlog file gap between master and syncer`監視メトリックを確認します。このメトリックの詳細については、 [Binlogレプリケーションの監視メトリクス](/dm/monitor-a-dm-cluster.md#binlog-replication)を参照してください。

-   このメトリックが長時間 1 より大きい場合は、通常、パフォーマンスの問題があることを示しています。
-   このメトリックが 0 の場合、通常はパフォーマンスの問題がないことを示します。

`binlog file gap between master and syncer`が 1 より大きい場合は、 `binlog file gap between relay and syncer`確認して、レイテンシーが主にどのユニットに存在するかを調べます。この値が通常 0 である場合、レイテンシーはリレー ログ ユニットに存在する可能性があります。その後、 [リレーログユニット](#relay-log-unit)を参照してこの問題を解決できます。それ以外の場合は、 Binlogレプリケーション ユニットのチェックを続けます。

### binlogデータの読み取り {#read-binlog-data}

Binlogレプリケーション ユニットは、binlogイベントを上流の MySQL/MariaDB から読み取るか、構成に従ってリレー ログ ファイルから読み取るかを決定します。関連するパフォーマンス メトリックは`read binlog event duration`で、通常は数マイクロ秒から数十マイクロ秒の範囲です。

-   DM のBinlogレプリケーション処理ユニットが上流の MySQL/MariaDB からbinlogイベントを読み取る場合、問題を特定して解決するには、「リレー ログ ユニット」セクションの[binlogデータを読む](#read-binlog-data)を参照してください。

-   DM のBinlogレプリケーション処理ユニットがリレー ログ ファイルからbinlogイベントを読み取る場合、 `binlog event size`が大きすぎない場合、 `read binlog event duration`の値はマイクロ秒になるはずです。 `read binlog event duration`が大きすぎる場合は、ディスクの読み取りパフォーマンスを確認してください。書き込みパフォーマンスの低下を回避するには、DM ワーカーにローカル SSD を使用します。

### binlogイベント変換 {#binlog-event-conversion}

Binlogレプリケーション ユニットは、DML を構築し、DDL を解析し、 binlogイベント データから[テーブルルーター](/dm/dm-table-routing.md)変換を実行します。関連するメトリックは`transform binlog event duration`です。

期間は、主にアップストリームの書き込み操作の影響を受けます。 `INSERT INTO`ステートメントを例にとると、単一の`VALUES`変換するのにかかる時間は、大量の`VALUES`を変換するのとは大きく異なります。消費される時間は、数十マイクロ秒から数百マイクロ秒の範囲です。ただし、通常、これはシステムのボトルネックではありません。

### SQL ステートメントをダウンストリームに書き込む {#write-sql-statements-to-downstream}

Binlogレプリケーション ユニットが変換された SQL ステートメントをダウンストリームに書き込むとき、関連するパフォーマンス メトリックは`DML queue remain length`と`transaction execution latency`です。

binlogイベントから SQL ステートメントを作成した後、DM は`worker-count`キューを使用して、これらのステートメントを同時にダウンストリームに書き込みます。ただし、監視エントリが多すぎるのを避けるために、DM は同時キューの ID に対してモジュロ`8`操作を実行します。これは、すべての同時キューが`q_0`から`q_7`までの 1 つの項目に対応することを意味します。

`DML queue remain length` 、コンカレント処理キューで、消費されておらず、ダウンストリームへの書き込みが開始されていない DML ステートメントの数を示します。理想的には、各`q_*`に対応する曲線はほぼ同じです。そうでない場合は、同時負荷が非常に不均衡であることを示しています。

負荷が分散されていない場合は、移行する必要があるテーブルに主キーまたは一意のキーがあるかどうかを確認します。これらのキーが存在しない場合は、主キーまたは一意のキーを追加します。負荷が分散されていないときにこれらのキーが存在する場合は、DM を v1.0.5 以降のバージョンにアップグレードしてください。

-   データ移行リンク全体に目立ったレイテンシーがない場合、対応する曲線`DML queue remain length`はほぼ常に 0 であり、最大値はタスク構成ファイルの値`batch`を超えません。

-   データ移行リンクで顕著なレイテンシーが見つかり、各`q_*`に対応する`DML queue remain length`の曲線がほぼ同じで、ほぼ常に 0 である場合、DM がアップストリームからのデータの読み取り、変換、または同時書き込みに失敗したことを意味します。時間 (ボトルネックはリレー ログ ユニットにある可能性があります)。トラブルシューティングについては、このドキュメントの前のセクションを参照してください。

`DML queue remain length`の対応する曲線が 0 でない場合 (通常、最大値は 1024 以下)、下流に SQL ステートメントを書き込むときにボトルネックがあることを示します。 `transaction execution latency`使用して、ダウンストリームへの 1 つのトランザクションの実行にかかった時間を表示できます。

`transaction execution latency`は通常、数十ミリ秒です。この値が大きすぎる場合は、ダウンストリーム データベースの監視に基づいてダウンストリームのパフォーマンスを確認します。 DM とダウンストリーム データベースの間に大きなネットワークレイテンシーがあるかどうかを確認することもできます。

`BEGIN` 、 `INSERT` 、 `UPDATE` 、 `DELETE` 、または`COMMIT`などの単一のステートメントをダウンストリームに書き込むのにかかった時間を表示するには、 `statement execution latency`も確認できます。
