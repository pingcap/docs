---
title: Migration FAQs
summary: Learn about the FAQs related to data migration.
---

# 移行に関するFAQ {#migration-faqs}

このドキュメントは、TiDBデータ移行に関連するよくある質問（FAQ）をまとめたものです。

移行関連ツールに関するよくある質問については、以下のリストにある対応するリンクをクリックしてください。

-   [バックアップと復元に関するFAQ](/br/backup-and-restore-faq.md)
-   [TiDB Binlog FAQ](/tidb-binlog/tidb-binlog-faq.md)
-   [TiDB Lightning](/tidb-lightning/tidb-lightning-faq.md)
-   [TiDBデータ移行（DM）に関するFAQ](/dm/dm-faq.md)
-   [TiCDCのFAQ](/ticdc/ticdc-faq.md)

## 完全なデータのエクスポートとインポート {#full-data-export-and-import}

### MySQLで実行されているアプリケーションをTiDBに移行するにはどうすればよいですか？ {#how-to-migrate-an-application-running-on-mysql-to-tidb}

TiDBはほとんどのMySQL構文をサポートしているため、通常、ほとんどの場合、コードを1行も変更せずにアプリケーションをTiDBに移行できます。

### データのインポートとエクスポートは遅く、多くの再試行とEOFエラーが他のエラーなしで各コンポーネントのログに表示されます {#data-import-and-export-is-slow-and-many-retries-and-eof-errors-appear-in-the-log-of-each-component-without-other-errors}

他の論理エラーが発生しない場合は、ネットワークの問題が原因で再試行とEOFエラーが発生している可能性があります。最初にツールを使用してネットワーク接続を確認することをお勧めします。次の例では、トラブルシューティングに[iperf](https://iperf.fr/)が使用されています。

-   再試行とEOFエラーが発生するサーバー側ノードで次のコマンドを実行します。

    {{< copyable "" >}}

    ```shell
    iperf3 -s
    ```

-   再試行とEOFエラーが発生するクライアント側ノードで次のコマンドを実行します。

    {{< copyable "" >}}

    ```shell
    iperf3 -c <server-IP>
    ```

次の例は、ネットワーク接続が良好なクライアントノードの出力です。

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

出力に低いネットワーク帯域幅と高い帯域幅変動が示されている場合、各コンポーネントログに多数の再試行とEOFエラーが表示される可能性があります。この場合、ネットワーク品質を向上させるためにネットワークサービスプロバイダーに相談する必要があります。

各メトリックの出力が良好に見える場合は、各コンポーネントを更新してみてください。更新後も問題が解決しない場合は、 [お問い合わせ](https://tidbcommunity.slack.com/archives/CH7TTLL7P)を実行できます。

### 誤ってMySQLユーザーテーブルをTiDBにインポートした場合、またはパスワードを忘れてログインできない場合、どのように対処しますか？ {#if-i-accidentally-import-the-mysql-user-table-into-tidb-or-forget-the-password-and-cannot-log-in-how-to-deal-with-it}

TiDBサービスを再起動し、構成ファイルに`-skip-grant-table=true`つのパラメーターを追加します。パスワードなしでクラスタにログインしてユーザーを再作成するか、 `mysql.user`のテーブルを再作成します。特定のテーブルスキーマについては、公式ドキュメントを検索してください。

### TiDBでデータをエクスポートする方法は？ {#how-to-export-the-data-in-tidb}

次の方法を使用して、TiDBにデータをエクスポートできます。

-   中国語の[MySQLはmysqldumpを使用してテーブルデータの一部をエクスポートします](https://blog.csdn.net/xin_yu_xin/article/details/7574662)を参照し、mysqldumpと`WHERE`句を使用してデータをエクスポートします。
-   MySQLクライアントを使用して、 `select`の結果をファイルにエクスポートします。

### DB2またはOracleからTiDBに移行するにはどうすればよいですか？ {#how-to-migrate-from-db2-or-oracle-to-tidb}

すべてのデータをマイグレーションするか、DB2またはOracleからTiDBに段階的にマイグレーションするには、以下のソリューションを参照してください。

-   OGG、Gateway、CDC（Change Data Capture）などのOracleの公式移行ツールを使用します。
-   データをインポートおよびエクスポートするためのプログラムを開発します。
-   スプールをテキストファイルとしてエクスポートし、Loadinfileを使用してデータをインポートします。
-   サードパーティのデータ移行ツールを使用します。

現在、OGGの使用をお勧めします。

### エラー： <code>java.sql.BatchUpdateExecption:statement count 5001 exceeds the transaction limitation</code> Sqoopを使用してデータを<code>batches</code>でTiDBに書き込むときに、トランザクション制限を超えています {#error-code-java-sql-batchupdateexecption-statement-count-5001-exceeds-the-transaction-limitation-code-while-using-sqoop-to-write-data-into-tidb-in-code-batches-code}

Sqoopでは、 `--batch`は各バッチで100個の`statement`をコミットすることを意味しますが、デフォルトでは、各`statement`に100個のSQLステートメントが含まれています。したがって、100 * 100 = 10000 SQLステートメント。これは5000を超えます。これは、単一のTiDBトランザクションで許可されるステートメントの最大数です。

2つの解決策：

-   次のように`-Dsqoop.export.records.per.statement=10`のオプションを追加します。

    {{< copyable "" >}}

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

-   1つのTiDBトランザクションで制限された数のステートメントを増やすこともできますが、これはより多くのメモリを消費します。

### Dumpling <code>The local disk space is insufficient</code>はなぜですか、またはテーブルをエクスポートするときにアップストリームデータベースのメモリが不足する原因になりますか？ {#why-does-dumpling-return-code-the-local-disk-space-is-insufficient-code-error-or-cause-the-upstream-database-to-run-out-of-memory-when-exporting-a-table}

この問題には、次の原因が考えられます。

-   データベースの主キーが均等に分散されていません（たとえば、 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)を有効にした場合）。
-   アップストリームデータベースはTiDBであり、エクスポートされたテーブルはパーティションテーブルです。

上記の場合、 Dumplingは、エクスポート用に非常に大きなデータチャンクを分割し、非常に大きな結果を持つクエリを送信します。この問題に対処するには、 [お問い合わせ](https://tidbcommunity.slack.com/archives/CH7TTLL7P)ナイトリーバージョンのDumplingを入手します。

### TiDBにはOracleのフラッシュバッククエリのような機能がありますか？ DDLをサポートしていますか？ {#does-tidb-have-a-function-like-the-flashback-query-in-oracle-does-it-support-ddl}

はい、そうです。また、DDLもサポートしています。詳細については、 [TiDBが履歴バージョンからデータを読み取る方法](/read-historical-data.md)を参照してください。

## オンラインでデータを移行する {#migrate-the-data-online}

### TiDBからHBaseやElasticsearchなどの他のデータベースにデータを複製するための現在のソリューションはありますか？ {#is-there-a-current-solution-to-replicating-data-from-tidb-to-other-databases-like-hbase-and-elasticsearch}

いいえ。現在、データ複製はアプリケーション自体に依存しています。

## トラフィックを移行する {#migrate-the-traffic}

### トラフィックをすばやく移行するにはどうすればよいですか？ {#how-to-migrate-the-traffic-quickly}

[TiDBデータ移行](/dm/dm-overview.md)のツールを使用してMySQLからTiDBにアプリケーションデータを移行することをお勧めします。必要に応じてネットワーク構成を編集することにより、読み取りトラフィックと書き込みトラフィックをバッチで移行できます。ネットワーク構成を直接編集してシームレスな移行を実装するために、安定したネットワークLB（HAproxy、LVS、F5、DNSなど）を上位層にデプロイします。

### TiDBの書き込みと読み取りの合計容量に制限はありますか？ {#is-there-a-limit-for-the-total-write-and-read-capacity-in-tidb}

総読み取り容量に制限はありません。 TiDBサーバーを追加することで、読み取り容量を増やすことができます。通常、書き込み容量にも制限はありません。 TiKVノードを追加することで、書き込み容量を増やすことができます。

### <code>transaction too large</code>というエラーメッセージが表示されます {#the-error-message-code-transaction-too-large-code-is-displayed}

基盤となるストレージエンジンの制限により、TiDBの各Key-Valueエントリ（1行）は6MB以下にする必要があります。 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50)の構成値を最大120MBまで調整できます。

分散トランザクションには2フェーズコミットが必要であり、最下層がRaftレプリケーションを実行します。トランザクションが非常に大きい場合、コミットプロセスは非常に遅くなり、書き込みの競合が発生する可能性が高くなります。さらに、失敗したトランザクションのロールバックは、不必要なパフォーマンスの低下につながります。これらの問題を回避するために、デフォルトでは、トランザクション内のKey-Valueエントリの合計サイズを100MB以下に制限しています。より大きなトランザクションが必要な場合は、TiDB構成ファイルの値`txn-total-size-limit`を変更します。この構成アイテムの最大値は最大10Gです。実際の制限は、マシンの物理メモリによっても影響を受けます。

GoogleCloudSpannerには[同様の制限](https://cloud.google.com/spanner/docs/limits)あります。

### データをバッチでインポートする方法は？ {#how-to-import-data-in-batches}

データをインポートするときは、バッチで挿入し、各バッチの行数を10,000以内に保ちます。

### TiDBはデータを削除した直後にスペースを解放しますか？ {#does-tidb-release-space-immediately-after-deleting-data}

`DELETE` 、および`TRUNCATE`の操作のいずれも、データをすぐに解放しませ`DROP` 。 `TRUNCATE`および`DROP`の操作では、TiDB GC（ガベージコレクション）時間（デフォルトでは10分）の後、データが削除され、スペースが解放されます。 `DELETE`操作の場合、データは削除されますが、TiDBGCに従ってスペースは解放されません。後続のデータがRocksDBに書き込まれ、 `COMPACT`を実行すると、スペースが再利用されます。

### データのロード時にターゲットテーブルでDDL操作を実行できますか？ {#can-i-execute-ddl-operations-on-the-target-table-when-loading-data}

いいえ。データをロードするときに、ターゲットテーブルでDDL操作を実行することはできません。実行しないと、データのロードに失敗します。

### TiDBは構文への<code>replace into</code>サポートしていますか？ {#does-tidb-support-the-code-replace-into-code-syntax}

はい。

### データを削除した後、クエリの速度が遅くなるのはなぜですか？ {#why-does-the-query-speed-getting-slow-after-deleting-data}

大量のデータを削除すると、多くの役に立たないキーが残り、クエリの効率に影響します。現在、リージョンマージ機能が開発中であり、この問題の解決が期待されています。詳細については、 [TiDBベストプラクティスのデータセクションの削除](https://en.pingcap.com/blog/tidb-best-practice/#write)を参照してください。

### データを削除する最も効率的な方法は何ですか？ {#what-is-the-most-efficient-way-of-deleting-data}

大量のデータを削除する場合は、 `Delete from t where xx limit 5000;`を使用することをお勧めします。ループを介して削除し、トランザクションサイズの制限を超えないように、ループを終了する条件として`Affected Rows == 0`を使用します。ビジネスフィルタリングロジックを満たすことを前提として、強力なフィルタインデックス列を追加するか、主キーを直接使用して`id >= 5000*n+m and id < 5000*(n+1)+m`などの範囲を選択することをお勧めします。

一度に削除する必要のあるデータの量が非常に多い場合、各削除は逆方向にトラバースするため、このループメソッドはますます遅くなります。以前のデータを削除した後、削除されたフラグの多くは短期間残り（その後、すべてがガベージコレクションによって処理されます）、次のDeleteステートメントに影響を与えます。可能であれば、Where条件を調整することをお勧めします。 [TiDBのベストプラクティスの詳細](https://en.pingcap.com/blog/tidb-best-practice/#write)を参照してください。

### TiDBでのデータ読み込み速度を向上させる方法は？ {#how-to-improve-the-data-loading-speed-in-tidb}

-   [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)ツールは、分散データのインポート用に開発されています。データインポートプロセスは、パフォーマンス上の理由から完全なトランザクションプロセスを実行しないことに注意してください。したがって、インポートプロセス中にインポートされるデータのACID制約は保証できません。インポートされたデータのACID制約は、インポートプロセス全体が終了した後にのみ保証されます。したがって、適用可能なシナリオには、主に新しいデータ（新しいテーブルや新しいインデックスなど）のインポート、または完全バックアップと復元（元のテーブルを切り捨ててからデータをインポートする）が含まれます。
-   TiDBでのデータの読み込みは、ディスクとクラスタ全体のステータスに関連しています。データをロードするときは、ホストのディスク使用率、TiClientエラー、バックオフ、スレッドCPUなどのメトリックに注意してください。これらのメトリックを使用してボトルネックを分析できます。
