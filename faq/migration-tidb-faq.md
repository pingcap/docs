---
title: Migration FAQs
summary: データ移行に関する FAQ について説明します。
---

# 移行に関するよくある質問 {#migration-faqs}

このドキュメントでは、TiDB データ移行に関するよくある質問 (FAQ) をまとめています。

移行関連ツールに関するよくある質問については、以下のリストの対応するリンクをクリックしてください。

-   [バックアップと復元に関するよくある質問](/faq/backup-and-restore-faq.md)
-   [TiDB Lightningに関するよくある質問](/tidb-lightning/tidb-lightning-faq.md)
-   [TiDB データ移行 (DM) に関するよくある質問](/dm/dm-faq.md)
-   [TiCDC よくある質問](/ticdc/ticdc-faq.md)

## 完全なデータのエクスポートとインポート {#full-data-export-and-import}

### MySQL で実行されているアプリケーションを TiDB に移行するにはどうすればよいでしょうか? {#how-to-migrate-an-application-running-on-mysql-to-tidb}

TiDB はほとんどの MySQL 構文をサポートしているため、ほとんどの場合、コードを 1 行も変更せずにアプリケーションを TiDB に移行できます。

### データのインポートとエクスポートが遅く、他のエラーがないにもかかわらず、各コンポーネントのログに多くの再試行とEOFエラーが表示されます。 {#data-import-and-export-is-slow-and-many-retries-and-eof-errors-appear-in-the-log-of-each-component-without-other-errors}

他の論理エラーが発生していない場合、再試行とEOFエラーはネットワークの問題が原因である可能性があります。まずはツールを使用してネットワーク接続を確認することをお勧めします。次の例では、トラブルシューティングに[iperf](https://iperf.fr/)使用しています。

-   再試行と EOF エラーが発生したサーバー側ノードで次のコマンドを実行します。

    ```shell
    iperf3 -s
    ```

-   再試行と EOF エラーが発生したクライアント側ノードで次のコマンドを実行します。

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

出力結果にネットワーク帯域幅が低く、帯域幅の変動が大きいことが示されている場合、各コンポーネントのログに再試行回数やEOFエラーが多数記録される可能性があります。この場合、ネットワーク品質の改善についてネットワークサービスプロバイダーにご相談ください。

各メトリックの出力が良好な場合は、各コンポーネントを更新してみてください。更新後も問題が解決しない場合は、PingCAPまたはコミュニティに[サポートを受ける](/support.md)ください。

### 誤ってMySQLユーザーテーブルをTiDBにインポートしてしまった場合、またはパスワードを忘れてログインできない場合は、どのように対処すればよいですか? {#if-i-accidentally-import-the-mysql-user-table-into-tidb-or-forget-the-password-and-cannot-log-in-how-to-deal-with-it}

TiDBサービスを再起動し、設定ファイルにパラメータ`-skip-grant-table=true`追加します。パスワードなしでクラスターにログインし、ユーザーを再作成するか、テーブル`mysql.user`を再作成してください。具体的なテーブルスキーマについては、公式ドキュメントを参照してください。

### TiDB のデータをエクスポートするにはどうすればいいですか? {#how-to-export-the-data-in-tidb}

TiDB のデータをエクスポートするには、次の方法を使用できます。

-   Dumplingを使用してデータをエクスポートします。詳細については、 [Dumplingのドキュメント](/dumpling-overview.md)参照してください。
-   mysqldump と`WHERE`句を使用してデータをエクスポートします。
-   MySQL クライアントを使用して、 `select`の結果をファイルにエクスポートします。

### Db2 または Oracle から TiDB に移行するにはどうすればよいでしょうか? {#how-to-migrate-from-db2-or-oracle-to-tidb}

Db2 または Oracle から TiDB にすべてのデータを移行するか、段階的に移行する場合は、次のソリューションを参照してください。

-   OGG、Gateway、CDC (Change Data Capture) などの Oracle の公式移行ツールを使用します。
-   データをインポートおよびエクスポートするためのプログラムを開発します。
-   スプールをテキスト ファイルとしてエクスポートし、Load infile を使用してデータをインポートします。
-   サードパーティのデータ移行ツールを使用します。

現在はOGGの使用が推奨されています。

### エラー: java.sql.BatchUpdateException: Sqoop を使用して TiDB にデータを<code>batches</code>で書き込むときに<code>java.sql.BatchUpdateException:statement count 5001 exceeds the transaction limitation</code> {#error-code-java-sql-batchupdateexception-statement-count-5001-exceeds-the-transaction-limitation-code-while-using-sqoop-to-write-data-into-tidb-in-code-batches-code}

Sqoopでは、 `--batch`各バッチで100個の`statement`文をコミットすることを意味しますが、デフォルトでは各`statement`に100個のSQL文が含まれます。つまり、100 * 100 = 10000個のSQL文となり、単一のTiDBトランザクションで許可される最大SQL文数である5000を超えてしまいます。

2つの解決策:

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

-   単一の TiDB トランザクション内のステートメントの制限数を増やすこともできますが、これにより消費されるメモリが増加します。

### Dumpling がテーブルをエクスポートするときに<code>The local disk space is insufficient</code>エラーを返したり、アップストリーム データベースのメモリ不足を引き起こしたりする原因になるのはなぜですか? {#why-does-dumpling-return-code-the-local-disk-space-is-insufficient-code-error-or-cause-the-upstream-database-to-run-out-of-memory-when-exporting-a-table}

この問題には次の原因が考えられます。

-   データベースの主キーが均等に分散されていません (たとえば、 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)有効にした場合)。
-   アップストリーム データベースは TiDB であり、エクスポートされたテーブルはパーティションテーブルです。

上記のケースでは、 Dumpling はエクスポート時に過度に大きなデータチャンクを分割し、過度に大きな結果を含むクエリを送信します。この問題に対処するには、 Dumplingの最新バージョンを入手してください。

### TiDB には Oracle のフラッシュバック クエリのような機能がありますか? DDL をサポートしていますか? {#does-tidb-have-a-function-like-the-flashback-query-in-oracle-does-it-support-ddl}

はい、サポートしています。DDLもサポートしています。詳細は[TiDBが履歴バージョンからデータを読み取る方法](/read-historical-data.md)ご覧ください。

## データをオンラインで移行する {#migrate-the-data-online}

### TiDB から HBase や Elasticsearch などの他のデータベースにデータを複製するための現在のソリューションはありますか? {#is-there-a-current-solution-to-replicating-data-from-tidb-to-other-databases-like-hbase-and-elasticsearch}

いいえ。現在、データのレプリケーションはアプリケーション自体に依存しています。

## トラフィックを移行する {#migrate-the-traffic}

### トラフィックを素早く移行するにはどうすればよいでしょうか? {#how-to-migrate-the-traffic-quickly}

アプリケーションデータをMySQLからTiDBに移行する際は、 [TiDBデータ移行](/dm/dm-overview.md)ツールを使用することをお勧めします。必要に応じてネットワーク構成を編集することで、読み取りトラフィックと書き込みトラフィックを一括移行できます。上位レイヤーに安定したネットワークLB（HAproxy、LVS、F5、DNSなど）をデプロイことで、ネットワーク構成を直接編集し、シームレスな移行を実現できます。

### TiDB の書き込み容量と読み取り容量の合計に制限はありますか? {#is-there-a-limit-for-the-total-write-and-read-capacity-in-tidb}

読み取り容量の合計に制限はありません。TiDBサーバーを追加することで、読み取り容量を増やすことができます。書き込み容量にも、一般的に制限はありません。TiKVノードを追加することで、書き込み容量を増やすことができます。

### <code>transaction too large</code>エラーメッセージが表示されます {#the-error-message-code-transaction-too-large-code-is-displayed}

基盤となるstorageエンジンの制限により、TiDB の各キーと値のエントリ（1行）は 6MB 以下にする必要があります。1 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500)設定値は最大 120MB まで調整できます。

分散トランザクションは2相コミットを必要とし、最レイヤーでRaftレプリケーションを実行します。トランザクションが非常に大きい場合、コミットプロセスは非常に遅くなり、書き込み競合が発生する可能性が高くなります。さらに、失敗したトランザクションのロールバックは、不要なパフォーマンスの低下につながります。これらの問題を回避するため、デフォルトでは、トランザクション内のキーと値のエントリの合計サイズを100MB以下に制限しています。より大きなトランザクションが必要な場合は、TiDB設定ファイルの値`txn-total-size-limit`変更してください。この設定項目の最大値は10GBです。実際の制限は、マシンの物理メモリにも影響されます。

Google Cloud Spanner には[同様の制限](https://cloud.google.com/spanner/docs/limits)あります。

### データを一括でインポートするにはどうすればいいですか? {#how-to-import-data-in-batches}

データをインポートするときは、バッチで挿入し、バッチごとに行数を 10,000 以内に抑えます。

### TiDB はデータを削除した後すぐにスペースを解放しますか? {#does-tidb-release-space-immediately-after-deleting-data}

`DELETE` `TRUNCATE`操作`DROP`いずれもデータを即時に解放しません。7と`TRUNCATE` `DROP`操作では、TiDB GC（ガベージコレクション）時間（デフォルトでは10分）後にデータが削除され、領域が解放されます。11 `DELETE`操作では、データは削除されますが、TiDB GCに従って領域は解放されません。後続のデータがRocksDBに書き込まれ、 `COMPACT`実行されると、領域は再利用されます。

### データをロードするときに、ターゲット テーブルで DDL 操作を実行できますか? {#can-i-execute-ddl-operations-on-the-target-table-when-loading-data}

いいえ。データをロードするときに、ターゲット テーブルで DDL 操作を実行することはできません。そうしないと、データのロードに失敗します。

### TiDB は<code>replace into</code>構文をサポートしていますか? {#does-tidb-support-the-code-replace-into-code-syntax}

はい。

### データを削除した後、クエリ速度が遅くなるのはなぜですか? {#why-does-the-query-speed-getting-slow-after-deleting-data}

大量のデータを削除すると、多くの無駄なキーが残り、クエリの効率に影響します。この問題は[リージョン結合機能](/best-practices/massive-regions-best-practices.md#method-3-enable-region-merge)解決できます。詳細については、 [TiDBベストプラクティスのデータセクションの削除](https://www.pingcap.com/blog/tidb-best-practice/#write)をご覧ください。

### データを削除する最も効率的な方法は何ですか? {#what-is-the-most-efficient-way-of-deleting-data}

大量のデータを削除する場合は、 `Delete from t where xx limit 5000;`使用をお勧めします。これはループを通して削除を行い、 `Affected Rows == 0`ループ終了条件として使用することで、トランザクションサイズの制限を超えないようにします。ビジネスフィルタリングロジックを満たすことを前提として、強力なフィルターインデックス列を追加するか、 `id >= 5000*n+m and id < 5000*(n+1)+m`のように主キーを直接使用して範囲を選択することをお勧めします。

一度に削除する必要があるデータの量が非常に多い場合、このループメソッドは削除処理が後方に移動するにつれて速度が低下します。前のデータを削除した後、多くの削除フラグが短期間残り（その後、すべてガベージコレクションによって処理されます）、後続のDelete文に影響を与えます。可能であれば、Where条件を絞り込むことをお勧めします。1 [詳細はTiDBベストプラクティスをご覧ください](https://www.pingcap.com/blog/tidb-best-practice/#write)参照してください。

### TiDB のデータ読み込み速度を向上させるにはどうすればよいでしょうか? {#how-to-improve-the-data-loading-speed-in-tidb}

-   [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)ツールは分散データインポート用に開発されています。パフォーマンス上の理由から、データインポートプロセスは完全なトランザクション処理を実行しないことに注意してください。そのため、インポートプロセス中にインポートされるデータのACID制約は保証されません。インポートされたデータのACID制約は、インポートプロセス全体が終了した後にのみ保証されます。したがって、適用可能なシナリオは主に、新規データ（新規テーブルや新規インデックスなど）のインポート、またはフルバックアップとリストア（元のテーブルを切り捨ててからデータをインポートする）です。
-   TiDBへのデータロードは、ディスクとクラスタ全体の状態に関連しています。データをロードする際は、ホストのディスク使用率、TiClientエラー、バックオフ、スレッドCPUなどのメトリクスに注目してください。これらのメトリクスを用いてボトルネックを分析できます。
