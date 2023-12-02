---
title: Migration FAQs
summary: Learn about the FAQs related to data migration.
---

# 移行に関するよくある質問 {#migration-faqs}

このドキュメントには、TiDB データ移行に関連するよくある質問 (FAQ) がまとめられています。

移行関連ツールに関するよくある質問については、以下のリスト内の対応するリンクをクリックしてください。

-   [バックアップと復元に関するよくある質問](/faq/backup-and-restore-faq.md)
-   [TiDBBinlogFAQ](/tidb-binlog/tidb-binlog-faq.md)
-   [TiDB Lightningよくある質問](/tidb-lightning/tidb-lightning-faq.md)
-   [TiDB データ移行 (DM) に関するよくある質問](/dm/dm-faq.md)
-   [TiCDC よくある質問](/ticdc/ticdc-faq.md)

## 完全なデータのエクスポートとインポート {#full-data-export-and-import}

### MySQL 上で実行されているアプリケーションを TiDB に移行するにはどうすればよいですか? {#how-to-migrate-an-application-running-on-mysql-to-tidb}

TiDB はほとんどの MySQL 構文をサポートしているため、ほとんどの場合、コードを 1 行も変更することなくアプリケーションを TiDB に移行できます。

### データのインポートとエクスポートが遅く、他のエラーはなく、多くの再試行と EOF エラーが各コンポーネントのログに記録されます。 {#data-import-and-export-is-slow-and-many-retries-and-eof-errors-appear-in-the-log-of-each-component-without-other-errors}

他に論理エラーが発生していない場合は、ネットワークの問題が原因で再試行および EOF エラーが発生している可能性があります。最初にツールを使用してネットワーク接続を確認することをお勧めします。次の例では、トラブルシューティングに[iperf](https://iperf.fr/)が使用されます。

-   リトライおよび EOF エラーが発生したサーバー側ノードで次のコマンドを実行します。

    ```shell
    iperf3 -s
    ```

-   再試行および EOF エラーが発生したクライアント側ノードで次のコマンドを実行します。

    ```shell
    iperf3 -c <server-IP>
    ```

次の例は、ネットワーク接続が良好なクライアント ノードの出力です。

```shell
$ iperf3 -c 192.168.196.58
Connecting to host 192.168.196.58, port 5201
[  5] local 192.168.196.150 port 55397 connected to 192.168.196.58 port 5201
[ ID] Interval           Transfer     Bitrate
[  5]   0.00-1.00   sec  18.0 MBytes   150 Mbits/sec
[  5]   1.00-2.00   sec  20.8 MBytes   175 Mbits/sec
[  5]   2.00-3.00   sec  18.2 MBytes   153 Mbits/sec
[  5]   3.00-4.00   sec  22.5 MBytes   188 Mbits/sec
[  5]   4.00-5.00   sec  22.4 MBytes   188 Mbits/sec
[  5]   5.00-6.00   sec  22.8 MBytes   191 Mbits/sec
[  5]   6.00-7.00   sec  20.8 MBytes   174 Mbits/sec
[  5]   7.00-8.00   sec  20.1 MBytes   168 Mbits/sec
[  5]   8.00-9.00   sec  20.8 MBytes   175 Mbits/sec
[  5]   9.00-10.00  sec  21.8 MBytes   183 Mbits/sec
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate
[  5]   0.00-10.00  sec   208 MBytes   175 Mbits/sec                  sender
[  5]   0.00-10.00  sec   208 MBytes   174 Mbits/sec                  receiver

iperf Done.
```

出力にネットワーク帯域幅が低く、帯域幅が大きく変動していることが示されている場合、多数の再試行と EOF エラーが各コンポーネントログに表示される可能性があります。この場合、ネットワークの品質を改善するには、ネットワーク サービス プロバイダーに相談する必要があります。

各メトリックの出力が良好であると思われる場合は、各コンポーネントを更新してみてください。更新後も問題が解決しない場合は、PingCAP またはコミュニティから[支持を得ます](/support.md) 。

### 誤って MySQL ユーザー テーブルを TiDB にインポートしたり、パスワードを忘れてログインできなくなった場合は、どう対処すればよいですか? {#if-i-accidentally-import-the-mysql-user-table-into-tidb-or-forget-the-password-and-cannot-log-in-how-to-deal-with-it}

TiDB サービスを再起動し、構成ファイルに`-skip-grant-table=true`パラメータを追加します。パスワードを使用せずにクラスターにログインし、ユーザーを再作成するか、 `mysql.user`を再作成します。特定のテーブル スキーマについては、公式ドキュメントを検索してください。

### TiDB のデータをエクスポートするにはどうすればよいですか? {#how-to-export-the-data-in-tidb}

次の方法を使用して、TiDB 内のデータをエクスポートできます。

-   mysqldump と`WHERE`句を使用してデータをエクスポートします。
-   MySQL クライアントを使用して、 `select`の結果をファイルにエクスポートします。

### DB2 または Oracle から TiDB に移行するにはどうすればよいですか? {#how-to-migrate-from-db2-or-oracle-to-tidb}

すべてのデータを移行するか、DB2 または Oracle から TiDB に段階的に移行するには、次の解決策を参照してください。

-   OGG、Gateway、CDC (Change Data Capture) などの Oracle の公式移行ツールを使用します。
-   データをインポートおよびエクスポートするためのプログラムを開発します。
-   スプールをテキスト ファイルとしてエクスポートし、Load infile を使用してデータをインポートします。
-   サードパーティのデータ移行ツールを使用します。

現時点では、OGG を使用することをお勧めします。

### エラー: Sqoop を使用してデータを TiDB に<code>batches</code>で書き込むときに、 <code>java.sql.BatchUpdateExecption:statement count 5001 exceeds the transaction limitation</code> {#error-code-java-sql-batchupdateexecption-statement-count-5001-exceeds-the-transaction-limitation-code-while-using-sqoop-to-write-data-into-tidb-in-code-batches-code}

Sqoop では、 `--batch`各バッチで 100 の`statement`をコミットすることを意味しますが、デフォルトでは、各`statement`に 100 の SQL ステートメントが含まれます。したがって、SQL ステートメントは 100 * 100 = 10000 となり、単一の TiDB トランザクションで許可されるステートメントの最大数である 5000 を超えます。

2 つの解決策:

-   次のように`-Dsqoop.export.records.per.statement=10`オプションを追加します。

    ```bash
    sqoop export \
        -Dsqoop.export.records.per.statement=10 \
        --connect jdbc:mysql://mysql.example.com/sqoop \
        --username sqoop ${user} \
        --password ${passwd} \
        --table ${tab_name} \
        --export-dir ${dir} \
        --batch
    ```

-   単一の TiDB トランザクション内の限られた数のステートメントを増やすこともできますが、これによりより多くのメモリが消費されます。

### Dumpling が<code>The local disk space is insufficient</code>エラーを返したり、テーブルのエクスポート時にアップストリーム データベースのメモリ不足を引き起こしたりするのはなぜですか? {#why-does-dumpling-return-code-the-local-disk-space-is-insufficient-code-error-or-cause-the-upstream-database-to-run-out-of-memory-when-exporting-a-table}

この問題には次の原因が考えられます。

-   データベースの主キーは均等に分散されていません (たとえば、 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)を有効にした場合)。
-   アップストリーム データベースは TiDB で、エクスポートされたテーブルはパーティションテーブルです。

上記の場合、 Dumpling はエクスポート用に大きすぎるデータ チャンクを分割し、大きすぎる結果を含むクエリを送信します。この問題に対処するには、最新バージョンのDumplingを入手してください。

### TiDBにはOracleのフラッシュバッククエリのような機能はありますか？ DDLをサポートしていますか? {#does-tidb-have-a-function-like-the-flashback-query-in-oracle-does-it-support-ddl}

はい、そうです。また、DDL もサポートしています。詳細は[TiDB が履歴バージョンからデータを読み取る方法](/read-historical-data.md)を参照してください。

## オンラインでデータを移行する {#migrate-the-data-online}

### TiDB から HBase や Elasticsearch などの他のデータベースにデータをレプリケートする現在のソリューションはありますか? {#is-there-a-current-solution-to-replicating-data-from-tidb-to-other-databases-like-hbase-and-elasticsearch}

いいえ。現在、データ レプリケーションはアプリケーション自体に依存しています。

## トラフィックを移行する {#migrate-the-traffic}

### トラフィックを迅速に移行するにはどうすればよいですか? {#how-to-migrate-the-traffic-quickly}

[TiDB データ移行](/dm/dm-overview.md)ツールを使用して MySQL から TiDB にアプリケーション データを移行することをお勧めします。必要に応じてネットワーク構成を編集することで、読み取りおよび書き込みトラフィックをバッチで移行できます。ネットワーク構成を直接編集することでシームレスな移行を実現するには、安定したネットワーク LB (HAproxy、LVS、F5、DNS など) を上位レイヤーにデプロイ。

### TiDB の書き込みおよび読み取りの合計容量に制限はありますか? {#is-there-a-limit-for-the-total-write-and-read-capacity-in-tidb}

合計読み取り容量に制限はありません。 TiDB サーバーを追加すると、読み取り容量を増やすことができます。通常、書き込み容量にも制限はありません。 TiKV ノードを追加すると、書き込み容量を増やすことができます。

### <code>transaction too large</code>エラーメッセージが表示される {#the-error-message-code-transaction-too-large-code-is-displayed}

基礎となるstorageエンジンの制限により、TiDB 内の各キーと値のエントリ (1 行) は 6MB 以下である必要があります。 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50)設定値は最大 120MB まで調整できます。

分散トランザクションには 2 フェーズ コミットが必要で、最下層でRaftレプリケーションが実行されます。トランザクションが非常に大きい場合、コミット プロセスが非常に遅くなり、書き込み競合が発生する可能性が高くなります。さらに、失敗したトランザクションのロールバックは、不必要なパフォーマンスの低下につながります。これらの問題を回避するために、デフォルトでは、トランザクション内のキーと値のエントリの合計サイズが 100MB 以下に制限されています。より大きなトランザクションが必要な場合は、TiDB 構成ファイルの値`txn-total-size-limit`を変更します。本設定項目の最大値は10Gまでです。実際の制限は、マシンの物理メモリにも影響されます。

Google Cloud Spanner には[同様の制限](https://cloud.google.com/spanner/docs/limits)あります。

### データをバッチでインポートするにはどうすればよいですか? {#how-to-import-data-in-batches}

データをインポートするときは、バッチに分けて挿入し、各バッチの行数を 10,000 以内に保ちます。

### TiDB はデータを削除した後すぐにスペースを解放しますか? {#does-tidb-release-space-immediately-after-deleting-data}

`DELETE` 、 `TRUNCATE` 、および`DROP`操作はいずれも、データを直ちに解放しません。 `TRUNCATE`と`DROP`の操作では、TiDB GC (ガベージ コレクション) 時間 (デフォルトでは 10 分) が経過すると、データが削除され、スペースが解放されます。 `DELETE`操作では、データは削除されますが、TiDB GC に従ってスペースは解放されません。後続のデータが RocksDB に書き込まれて実行されるとき`COMPACT` 、スペースは再利用されます。

### データをロードするときにターゲットテーブルに対して DDL 操作を実行できますか? {#can-i-execute-ddl-operations-on-the-target-table-when-loading-data}

いいえ。データをロードするときにターゲット テーブルに対して DDL 操作を実行することはできません。実行しないと、データのロードに失敗します。

### TiDB は<code>replace into</code>構文をサポートしていますか? {#does-tidb-support-the-code-replace-into-code-syntax}

はい。

### データを削除するとクエリの速度が遅くなるのはなぜですか? {#why-does-the-query-speed-getting-slow-after-deleting-data}

大量のデータを削除すると、無駄なキーが大量に残り、クエリの効率に影響します。現在、リージョン結合機能が開発中であり、この問題が解決されることが期待されています。詳細は[TiDB ベスト プラクティスのデータの削除セクション](https://en.pingcap.com/blog/tidb-best-practice/#write)を参照してください。

### データを削除する最も効率的な方法は何ですか? {#what-is-the-most-efficient-way-of-deleting-data}

大量のデータを削除する場合は、 `Delete from t where xx limit 5000;`を使用することをお勧めします。トランザクションサイズの制限を超えないように、ループを介して削除し、ループを終了する条件として`Affected Rows == 0`を使用します。ビジネス フィルタリング ロジックを満たすことを前提として、強力なフィルタ インデックス列を追加するか、主キーを直接使用して範囲を選択する ( `id >= 5000*n+m and id < 5000*(n+1)+m`など) ことをお勧めします。

一度に削除する必要があるデータの量が非常に多い場合、各削除が逆方向に実行されるため、このループ方法はますます遅くなります。以前のデータを削除した後、多数の削除済みフラグが短期間残り (その後、すべてがガベージ コレクションによって処理されます)、次の Delete ステートメントに影響を与えます。可能であれば、Where 条件を調整することをお勧めします。 [TiDB ベスト プラクティスの詳細](https://en.pingcap.com/blog/tidb-best-practice/#write)を参照してください。

### TiDB でのデータの読み込み速度を向上させるにはどうすればよいですか? {#how-to-improve-the-data-loading-speed-in-tidb}

-   [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)ツールは分散データ インポート用に開発されました。データ インポート プロセスは、パフォーマンス上の理由から完全なトランザクション プロセスを実行しないことに注意してください。したがって、インポート プロセス中にインポートされるデータのACID制約は保証できません。インポートされたデータのACID制約は、インポート プロセス全体が終了した後にのみ保証されます。したがって、該当するシナリオには主に、新しいデータ (新しいテーブルや新しいインデックスなど) のインポート、または完全バックアップと復元 (元のテーブルを切り詰めてからデータをインポート) が含まれます。
-   TiDB へのデータのロードは、ディスクとクラスター全体のステータスに関連しています。データをロードするときは、ホストのディスク使用率、TiClient エラー、バックオフ、スレッド CPU などのメトリクスに注意してください。これらのメトリクスを使用してボトルネックを分析できます。
