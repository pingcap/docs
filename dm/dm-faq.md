---
title: TiDB Data Migration FAQs
summary: Learn about frequently asked questions (FAQs) about TiDB Data Migration (DM).
---

# TiDB データ移行に関するよくある質問 {#tidb-data-migration-faqs}

このドキュメントには、TiDB データ移行 (DM) に関するよくある質問 (FAQ) がまとめられています。

## DM は Alibaba RDS または他のクラウド データベースからのデータの移行をサポートしていますか? {#does-dm-support-migrating-data-from-alibaba-rds-or-other-cloud-databases}

現在、DM は MySQL または MariaDB binlogの標準バージョンのデコードのみをサポートしています。 Alibaba Cloud RDS やその他のクラウド データベースに対してはテストされていません。binlogが標準形式であることが確認された場合、そのバイナリログはサポートされています。

Alibaba Cloud RDS の主キーのない上流テーブルの場合、そのbinlogに非表示の主キー列が依然として含まれており、元のテーブル構造と矛盾していることが既知の問題です。

互換性のない既知の問題をいくつか次に示します。

-   **Alibaba Cloud RDS**では、主キーのない上流テーブルの場合、そのbinlogには依然として非表示の主キー列が含まれており、元のテーブル構造と矛盾しています。
-   **HUAWEI Cloud RDS**では、 binlogファイルの直接読み取りはサポートされていません。詳細については、 [HUAWEI Cloud RDS はBinlogバックアップ ファイルを直接読み取ることができますか?](https://support.huaweicloud.com/en-us/rds_faq/rds_faq_0210.html)参照してください。

## タスク設定のブロックと許可リストの正規表現は<code>non-capturing (?!)</code>をサポートしていますか? {#does-the-regular-expression-of-the-block-and-allow-list-in-the-task-configuration-support-code-non-capturing-code}

現在、DM はこれをサポートしておらず、 Golang標準ライブラリの正規表現のみをサポートしています。 Golangでサポートされている正規表現については、 [re2 構文](https://github.com/google/re2/wiki/Syntax)参照してください。

## 上流で実行されるステートメントに複数の DDL 操作が含まれている場合、DM はそのような移行をサポートしますか? {#if-a-statement-executed-upstream-contains-multiple-ddl-operations-does-dm-support-such-migration}

DM は、複数の DDL 変更操作を含む 1 つのステートメントを、1 つの DDL 操作のみを含む複数のステートメントに分割しようとしますが、すべてのケースをカバーできるわけではありません。上流で実行されるステートメントには DDL 操作を 1 つだけ含めるか、テスト環境で検証することをお勧めします。サポートされていない場合は、DM リポジトリに[問題](https://github.com/pingcap/dm/issues)を提出できます。

## 互換性のない DDL ステートメントを処理するにはどうすればよいですか? {#how-to-handle-incompatible-ddl-statements}

TiDB でサポートされていない DDL ステートメントが発生した場合は、dmctl を使用して手動で処理する必要があります (DDL ステートメントをスキップするか、DDL ステートメントを指定された DDL ステートメントに置き換えます)。詳細は[失敗した DDL ステートメントを処理する](/dm/handle-failed-ddl-statements.md)を参照してください。

> **注記：**
>
> 現在、TiDB は、MySQL がサポートするすべての DDL ステートメントと互換性があるわけではありません。 [MySQL の互換性](/mysql-compatibility.md#ddl-operations)を参照してください。

## DM はビュー関連の DDL ステートメントと DML ステートメントを TiDB にレプリケートしますか? {#does-dm-replicate-view-related-ddl-statements-and-dml-statements-to-tidb}

現在、DM はビュー関連の DDL ステートメントをダウンストリーム TiDB クラスターに複製しません。また、ビュー関連の DML ステートメントをダウンストリーム TiDB クラスターに複製しません。

## データ移行タスクをリセットするにはどうすればよいですか? {#how-to-reset-the-data-migration-task}

データ移行中に例外が発生し、データ移行タスクを再開できない場合は、タスクをリセットしてデータを再移行する必要があります。

1.  `stop-task`コマンドを実行して、異常なデータ移行タスクを停止します。

2.  ダウンストリームに移行されたデータをパージします。

3.  次のいずれかの方法を使用して、データ移行タスクを再開します。

    -   タスク構成ファイルに新しいタスク名を指定します。次に`start-task {task-config-file}`を実行します。
    -   `start-task --remove-meta {task-config-file}`を実行します。

## <code>online-ddl: true</code>が設定された後、gh-ost テーブルに関連する DDL 操作によって返されたエラーを処理する方法は? {#how-to-handle-the-error-returned-by-the-ddl-operation-related-to-the-gh-ost-table-after-code-online-ddl-true-code-is-set}

    [unit=Sync] ["error information"="{\"msg\":\"[code=36046:class=sync-unit:scope=internal:level=high] online ddls on ghost table `xxx`.`_xxxx_gho`\\ngithub.com/pingcap/dm/pkg/terror.(*Error).Generate ......

上記のエラーは、次の理由によって発生する可能性があります。

最後の`rename ghost_table to origin table`ステップで、DM はメモリ内の DDL 情報を読み取り、それを元のテーブルの DDL に復元します。

ただし、メモリ内の DDL 情報は、次の 2 つの方法のいずれかで取得されます。

-   DM [`alter ghost_table`操作中に gh-ost テーブルを処理します](/dm/feature-online-ddl.md#online-schema-change-gh-ost)および`ghost_table`の DDL 情報を記録します。
-   タスクを開始するために DM-worker が再起動されると、DM は DDL を`dm_meta.{task_name}_onlineddl`から読み取ります。

したがって、増分レプリケーションのプロセスで、指定された Pos が`alter ghost_table` DDL をスキップしても、その Pos がまだ gh-ost の online-ddl プロセスにある場合、ghost_table はメモリまたは`dm_meta.{task_name}_onlineddl`に正しく書き込まれません。このような場合、上記のエラーが返されます。

次の手順でこのエラーを回避できます。

1.  タスクの`online-ddl-scheme`または`online-ddl`構成を削除します。

2.  `block-allow-list.ignore-tables`で`_{table_name}_gho` 、 `_{table_name}_ghc` 、および`_{table_name}_del`を構成します。

3.  ダウンストリーム TiDB でアップストリーム DDL を手動で実行します。

4.  Pos が gh-ost プロセス後の位置に複製された後、 `online-ddl-scheme`または`online-ddl`設定を再度有効にし、 `block-allow-list.ignore-tables`コメントアウトします。

## 既存のデータ移行タスクにテーブルを追加するにはどうすればよいですか? {#how-to-add-tables-to-the-existing-data-migration-tasks}

実行中のデータ移行タスクにテーブルを追加する必要がある場合は、タスクの段階に応じて次の方法で対処できます。

> **注記：**
>
> 既存のデータ移行タスクにテーブルを追加するのは複雑なため、この操作は必要な場合にのみ実行することをお勧めします。

### <code>Dump</code>ステージでは {#in-the-code-dump-code-stage}

MySQL はエクスポート用のスナップショットを指定できないため、エクスポート中にデータ移行タスクを更新し、チェックポイントを介してエクスポートを再開するために再起動することはサポートされていません。したがって、第`Dump`段階で移行が必要なテーブルを動的に追加することはできません。

移行のためにテーブルを追加する必要がある場合は、新しい構成ファイルを使用してタスクを直接再起動することをお勧めします。

### <code>Load</code>ステージで {#in-the-code-load-code-stage}

エクスポート中、複数のデータ移行タスクは通常、異なるbinlogの位置を持ちます。 `Load`段階でタスクをマージすると、binlogの位置について合意に達できない可能性があります。したがって、第`Load`段階のデータ移行タスクにテーブルを追加することはお勧めできません。

### <code>Sync</code>ステージでは {#in-the-code-sync-code-stage}

データ移行タスクが`Sync`段階にある場合、構成ファイルにテーブルを追加してタスクを再開すると、DM は新しく追加されたテーブルに対して完全なエクスポートとインポートを再実行しません。代わりに、DM は前のチェックポイントから増分レプリケーションを続行します。

したがって、新しく追加されたテーブルの完全なデータがダウンストリームにインポートされていない場合は、別のデータ移行タスクを使用して、完全なデータをダウンストリームにエクスポートおよびインポートする必要があります。

既存の移行タスクに対応するグローバル チェックポイント ( `is_global=1` ) の位置情報を`checkpoint-T` (たとえば`(mysql-bin.000100, 1234)`として記録します。移行タスクに追加するテーブルの完全エクスポート`metedata` (または`Sync`段階の別のデータ移行タスクのチェックポイント) の位置情報を`checkpoint-S` 、たとえば`(mysql-bin.000099, 5678)`として記録します。次の手順でテーブルを移行タスクに追加できます。

1.  既存の移行タスクを停止するには、 `stop-task`を使用します。追加するテーブルが実行中の別の移行タスクに属している場合は、そのタスクも停止します。

2.  MySQL クライアントを使用してダウンストリーム TiDB データベースに接続し、既存の移行タスクに対応するチェックポイント テーブル内の情報を`checkpoint-T`から`checkpoint-S`の間の小さい値に手動で更新します。この例では、 `(mysql- bin.000099, 5678)`です。

    -   更新するチェックポイントテーブルはスキーマ`{dm_meta}`の`{task-name}_syncer_checkpoint`です。

    -   更新されるチェックポイント行は`id=(source-id)`と`is_global=1`に一致します。

    -   更新されるチェックポイント列は`binlog_name`と`binlog_pos`です。

3.  再入可能実行を保証するには、タスクの`syncers`に`safe-mode: true`を設定します。

4.  `start-task`を使用してタスクを開始します。

5.  `query-status`を通じてタスクのステータスを観察します。 `syncerBinlog`が`checkpoint-T`と`checkpoint-S`の大きい値を超えると、 `safe-mode`元の値に戻してタスクを再起動します。この例では、 `(mysql-bin.000100, 1234)`です。

## <code>packet for query is too large. Try adjusting the &#39;max_allowed_packet&#39; variable</code>完全インポート中に発生する<code>packet for query is too large. Try adjusting the &#39;max_allowed_packet&#39; variable</code> 。 {#how-to-handle-the-error-code-packet-for-query-is-too-large-try-adjusting-the-max-allowed-packet-variable-code-that-occurs-during-the-full-import}

以下のパラメータをデフォルトの 67108864 (64M) より大きい値に設定します。

-   TiDBサーバーのグローバル変数: `max_allowed_packet` .
-   タスク構成ファイルの構成項目: `target-database.max-allowed-packet` .詳細は[DM 拡張タスクコンフィグレーションファイル](/dm/task-configuration-file-full.md)を参照してください。

## DM 1.0 クラスターの既存の DM 移行タスクが DM 2.0 以降のクラスターで実行されているときに発生するエラー<code>Error 1054: Unknown column &#39;binlog_gtid&#39; in &#39;field list&#39;</code>を処理する方法は? {#how-to-handle-the-error-code-error-1054-unknown-column-binlog-gtid-in-field-list-code-that-occurs-when-existing-dm-migration-tasks-of-an-dm-1-0-cluster-are-running-on-a-dm-2-0-or-newer-cluster}

DM v2.0 以降、DM 1.0 クラスターのタスク構成ファイルを使用して`start-task`コマンドを直接実行して増分データ レプリケーションを続行すると、エラー`Error 1054: Unknown column 'binlog_gtid' in 'field list'`が発生します。

このエラーは[DM 1.0 クラスターの DM 移行タスクを DM 2.0 クラスターに手動でインポート](/dm/manually-upgrade-dm-1.0-to-2.0.md)で処理できます。

## TiUP がDM の一部のバージョン (v2.0.0-hotfix など) の展開に失敗するのはなぜですか? {#why-does-tiup-fail-to-deploy-some-versions-of-dm-for-example-v2-0-0-hotfix}

`tiup list dm-master`コマンドを使用すると、 TiUPが展開をサポートする DM バージョンを表示できます。 TiUP は、このコマンドで表示されない DM バージョンを管理しません。

## DM がデータをレプリケートしているときに発生するエラー<code>parse mydumper metadata error: EOF</code>を処理する方法は? {#how-to-handle-the-error-code-parse-mydumper-metadata-error-eof-code-that-occurs-when-dm-is-replicating-data}

このエラーをさらに分析するには、エラー メッセージとログ ファイルを確認する必要があります。原因としては、権限がないためにダンプ ユニットが正しいメタデータ ファイルを生成しないことが考えられます。

## シャード化されたスキーマとテーブルをレプリケートするときに DM が致命的なエラーを報告しないのに、ダウンストリーム データが失われるのはなぜですか? {#why-does-dm-report-no-fatal-error-when-replicating-sharded-schemas-and-tables-but-downstream-data-is-lost}

設定項目`block-allow-list`と`table-route`を確認します。

-   `block-allow-list`で上流のデータベースとテーブルの名前を構成する必要があります。 `do-tables`の前に「~」を追加すると、正規表現を使用して名前を照合できます。
-   `table-route`正規表現の代わりにワイルドカード文字を使用してテーブル名を照合します。たとえば、 `table_parttern_[0-63]` `table_parttern_0`から`table_pattern_6`までの 7 つのテーブルにのみ一致します。

## DM がアップストリームからレプリケートされていないときに、 <code>replicate lag</code>モニター メトリックにデータが表示されないのはなぜですか? {#why-does-the-code-replicate-lag-code-monitor-metric-show-no-data-when-dm-is-not-replicating-from-upstream}

DM 1.0 では、モニター データを生成するには`enable-heartbeat`を有効にする必要があります。 DM 2.0 以降のバージョンでは、この機能がサポートされていないため、モニター メトリック`replicate lag`にはデータがないことが予想されます。

## DM がタスクを開始するときに<code>fail to initial unit Sync of subtask</code> 、エラー メッセージ内の<code>RawCause</code>に<code>context deadline exceeded</code>示すエラーを処理する方法はありますか? {#how-to-handle-the-error-code-fail-to-initial-unit-sync-of-subtask-code-when-dm-is-starting-a-task-with-the-code-rawcause-code-in-the-error-message-showing-code-context-deadline-exceeded-code}

これは DM 2.0.0 バージョンの既知の問題であり、DM 2.0.1 バージョンで修正される予定です。これは、レプリケーション タスクで処理するテーブルが多数ある場合にトリガーされる可能性があります。 TiUP を使用して DM を展開する場合は、DM を夜間バージョンにアップグレードしてこの問題を解決できます。または、GitHub で[DMのリリースページ](https://github.com/pingcap/tiflow/releases)から 2.0.0-hotfix バージョンをダウンロードし、実行可能ファイルを手動で置き換えることもできます。

## DM がデータを複製するときにエラー<code>duplicate entry</code>を処理するにはどうすればよいですか? {#how-to-handle-the-error-code-duplicate-entry-code-when-dm-is-replicating-data}

まず次のことを確認してください。

-   `disable-detect`はレプリケーション タスクで構成されていません (v2.0.7 以前のバージョン)。
-   データは手動または他のレプリケーション プログラムによって挿入されません。
-   このテーブルに関連付けられた DML フィルターは構成されていません。

トラブルシューティングを容易にするために、まずダウンストリーム TiDB インスタンスの一般的なログ ファイルを収集し、次に[TiDB コミュニティのスラック チャンネル](https://tidbcommunity.slack.com/archives/CH7TTLL7P)でテクニカル サポートを依頼できます。次の例は、一般的なログ ファイルを収集する方法を示しています。

```bash
# Enable general log collection
curl -X POST -d "tidb_general_log=1" http://{TiDBIP}:10080/settings
# Disable general log collection
curl -X POST -d "tidb_general_log=0" http://{TiDBIP}:10080/settings
```

`duplicate entry`エラーが発生した場合は、競合データを含むレコードがないかログ ファイルを確認する必要があります。

## 一部の監視パネルに<code>No data point</code>表示されないのはなぜですか? {#why-do-some-monitoring-panels-show-code-no-data-point-code}

一部のパネルにデータがないのは正常です。たとえば、エラーが報告されない場合、DDL ロックがない場合、またはリレー ログ機能が有効になっていない場合、対応するパネルには`No data point`が表示されます。各パネルの詳細な説明については、 [DM監視メトリクス](/dm/monitor-a-dm-cluster.md)を参照してください。

## DM v1.0 では、タスクにエラーがあるときにコマンド<code>sql-skip</code>一部のステートメントをスキップできないのはなぜですか? {#in-dm-v1-0-why-does-the-command-code-sql-skip-code-fail-to-skip-some-statements-when-the-task-is-in-error}

まず、 `sql-skip`を実行した後もbinlogの位置が進んでいるかどうかを確認する必要があります。そうであれば、 `sql-skip`有効になったことを意味します。このエラーが発生し続ける理由は、アップストリームがサポートされていない複数の DDL ステートメントを送信しているためです。 `sql-skip -s <sql-pattern>`を使用して、これらのステートメントに一致するパターンを設定できます。

場合によっては、エラー メッセージに`parse statement`情報が含まれることがあります。次に例を示します。

    if the DDL is not needed, you can use a filter rule with \"*\" schema-pattern to ignore it.\n\t : parse statement: line 1 column 11 near \"EVENT `event_del_big_table` \r\nDISABLE\" %!!(MISSING)(EXTRA string=ALTER EVENT `event_del_big_table` \r\nDISABLE

このタイプのエラーの理由は、TiDB パーサーがアップストリームによって送信された DDL ステートメント ( `ALTER EVENT`など) を解析できないため、 `sql-skip`期待どおりに機能しないことです。構成ファイルに[binlogイベントフィルター](/dm/dm-binlog-event-filter.md)追加してこれらのステートメントをフィルターし、 `schema-pattern: "*"`を設定できます。 DM v2.0.1 以降、DM は`EVENT`に関連するステートメントを事前にフィルターします。

DM v6.0 以降、 `sql-skip`と`handle-error`は`binlog`に置き換えられます。この問題を回避するには、代わりに`binlog`コマンドを使用します。

## DM の複製中に<code>REPLACE</code>ステートメントがダウンストリームに出現し続けるのはなぜですか? {#why-do-code-replace-code-statements-keep-appearing-in-the-downstream-when-dm-is-replicating}

タスクに対して[セーフモード](/dm/dm-glossary.md#safe-mode)が自動的に有効になっているかどうかを確認する必要があります。エラー後にタスクが自動的に再開される場合、または高可用性スケジュールが設定されている場合は、タスクの開始または再開後 1 分以内であるため、セーフ モードが有効になります。

DM-worker ログ ファイルを確認して、 `change count`を含む行を検索できます。行内の`new count`ゼロでない場合、セーフ モードが有効になります。有効になっている理由を調べるには、それがいつ発生するか、以前にエラーが報告されているかどうかを確認してください。

## DM v2.0 では、タスク中に DM が再起動されると完全インポート タスクが失敗するのはなぜですか? {#in-dm-v2-0-why-does-the-full-import-task-fail-if-dm-restarts-during-the-task}

DM v2.0.1 以前のバージョンでは、完全なインポートが完了する前に DM が再起動されると、アップストリーム データ ソースと DM ワーカー ノード間のバインディングが変更される可能性があります。たとえば、ダンプ ユニットの中間データは DM ワーカー ノード A 上にあるものの、ロード ユニットは DM ワーカー ノード B によって実行されているため、操作が失敗する可能性があります。

この問題に対する解決策は次の 2 つです。

-   データ ボリュームが小さい (1 TB 未満) 場合、またはタスクがシャード テーブルをマージする場合は、次の手順を実行します。

    1.  ダウンストリーム データベース内のインポートされたデータをクリーンアップします。
    2.  エクスポートされたデータのディレクトリ内のすべてのファイルを削除します。
    3.  dmctl を使用してタスクを削除し、コマンド`start-task --remove-meta`を実行して新しいタスクを作成します。

    新しいタスクの開始後は、冗長な DM ワーカー ノードがないことを確認し、完全インポート中に DM クラスターの再起動やアップグレードを避けることをお勧めします。

-   データ ボリュームが大きい (1 TB を超える) 場合は、次の手順を実行します。

    1.  ダウンストリーム データベース内のインポートされたデータをクリーンアップします。
    2.  データを処理する DM ワーカー ノードに TiDB-Lightningをデプロイ。
    3.  TiDB-Lightning のローカル バックエンド モードを使用して、DM ダンプ ユニットがエクスポートするデータをインポートします。
    4.  完全なインポートが完了したら、次の方法でタスク構成ファイルを編集し、タスクを再起動します。
        -   `task-mode`を`incremental`に変更します。
        -   値`mysql-instance.meta.pos` 、ダンプ ユニットが出力するメタデータ ファイルに記録される位置に設定します。

## DM がエラー<code>ERROR 1236 (HY000): The slave is connecting using CHANGE MASTER TO MASTER_AUTO_POSITION = 1, but the master has purged binary logs containing GTIDs that the slave requires.</code>増分タスク中に再起動した場合は? {#why-does-dm-report-the-error-code-error-1236-hy000-the-slave-is-connecting-using-change-master-to-master-auto-position-1-but-the-master-has-purged-binary-logs-containing-gtids-that-the-slave-requires-code-if-it-restarts-during-an-incremental-task}

このエラーは、ダンプ ユニットによって出力されたメタデータ ファイルに記録された上流のbinlogの位置が、完全な移行中にパージされたことを示します。

この問題が発生した場合は、タスクを一時停止し、ダウンストリーム データベース内の移行されたデータをすべて削除し、オプション`--remove-meta`を使用して新しいタスクを開始する必要があります。

次の方法で構成することで、この問題を事前に回避できます。

1.  完全な移行タスクが完了する前に、必要なbinlogファイルが誤ってパージされるのを避けるために、アップストリームの MySQL データベースの値`expire_logs_days`を増やします。データ量が大きい場合は、ダンプリングと TiDB-Lightning を同時に使用して作業を高速化することをお勧めします。
2.  このタスクのリレー ログ機能を有効にすると、binlogログの位置がパージされても DM がリレー ログからデータを読み取ることができます。

## クラスターがTiUP v1.3.0 または v1.3.1 を使用してデプロイされている場合、DM クラスターの Grafana ダッシュボード<code>failed to fetch dashboard</code>表示されるのはなぜですか? {#why-does-the-grafana-dashboard-of-a-dm-cluster-display-code-failed-to-fetch-dashboard-code-if-the-cluster-is-deployed-using-tiup-v1-3-0-or-v1-3-1}

これはTiUPの既知のバグであり、 TiUP v1.3.2 で修正されています。この問題に対する解決策は次の 2 つです。

-   解決策 1:
    1.  コマンド`tiup update --self && tiup update dm`を使用して、 TiUP を新しいバージョンにアップグレードします。
    2.  クラスター内の Grafana ノードをスケールインからスケールアウトし、Grafana サービスを再起動します。
-   解決策 2:
    1.  `deploy/grafana-$port/bin/public`フォルダをバックアップします。
    2.  [TiUP DMオフライン パッケージ](https://download.pingcap.org/tidb-dm-v2.0.1-linux-amd64.tar.gz)をダウンロードして解凍します。
    3.  オフライン パッケージの`grafana-v4.0.3-**.tar.gz`を開梱します。
    4.  `grafana-v4.0.3-**.tar.gz`のフォルダー`deploy/grafana-$port/bin/public` `public`フォルダーに置き換えます。
    5.  `tiup dm restart $cluster_name -R grafana`を実行して Grafana サービスを再起動します。

## DM v2.0 では、タスクで<code>enable-relay</code>と<code>enable-gtid</code>が同時に有効になっている場合、 <code>query-status</code>コマンドのクエリ結果で Syncer チェックポイント GTID が連続していないことが示されるのはなぜですか? {#in-dm-v2-0-why-does-the-query-result-of-the-command-code-query-status-code-show-that-the-syncer-checkpoint-gtids-are-inconsecutive-if-the-task-has-code-enable-relay-code-and-code-enable-gtid-code-enabled-at-the-same-time}

これは DM の既知のバグであり、DM v2.0.2 で修正されています。このバグは、次の 2 つの条件が同時に完全に満たされた場合に発生します。

1.  パラメータ`enable-relay`と`enable-gtid`は、ソース構成ファイルで`true`に設定されます。
2.  アップストリーム データベースは**MySQL セカンダリ データベース**です。コマンド`show binlog events in '<newest-binlog>' limit 2`を実行してデータベースの`previous_gtids`をクエリすると、次の例のように結果が不連続になります。

<!---->

    mysql> show binlog events in 'mysql-bin.000005' limit 2;
    +------------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+
    | Log_name         | Pos  | Event_type     | Server_id | End_log_pos | Info                                                               |
    +------------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+
    | mysql-bin.000005 |    4 | Format_desc    |    123452 |         123 | Server ver: 5.7.32-35-log, Binlog ver: 4                           |
    | mysql-bin.000005 |  123 | Previous_gtids |    123452 |         194 | d3618e68-6052-11eb-a68b-0242ac110002:6-7                           |
    +------------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+

このバグは、dmctl で`query-status <task>`実行してタスク情報をクエリし、 `subTaskStatus.sync.syncerBinlogGtid`は連続していないが`subTaskStatus.sync.masterBinlogGtid`は連続していることが判明した場合に発生します。次の例を参照してください。

    query-status test
    {
        ...
        "sources": [
            {
                ...
                "sourceStatus": {
                    "source": "mysql1",
                    ...
                    "relayStatus": {
                        "masterBinlog": "(mysql-bin.000006, 744)",
                        "masterBinlogGtid": "f8004e25-6067-11eb-9fa3-0242ac110003:1-50",
                        ...
                    }
                },
                "subTaskStatus": [
                    {
                        ...
                        "sync": {
                            ...
                            "masterBinlog": "(mysql-bin.000006, 744)",
                            "masterBinlogGtid": "f8004e25-6067-11eb-9fa3-0242ac110003:1-50",
                            "syncerBinlog": "(mysql-bin|000001.000006, 738)",
                            "syncerBinlogGtid": "f8004e25-6067-11eb-9fa3-0242ac110003:1-20:40-49",
                            ...
                            "synced": false,
                            "binlogType": "local"
                        }
                    }
                ]
            },
            {
                ...
                "sourceStatus": {
                    "source": "mysql2",
                    ...
                    "relayStatus": {
                        "masterBinlog": "(mysql-bin.000007, 1979)",
                        "masterBinlogGtid": "ddb8974e-6064-11eb-8357-0242ac110002:1-25",
                        ...
                    }
                },
                "subTaskStatus": [
                    {
                        ...
                        "sync": {
                            "masterBinlog": "(mysql-bin.000007, 1979)",
                            "masterBinlogGtid": "ddb8974e-6064-11eb-8357-0242ac110002:1-25",
                            "syncerBinlog": "(mysql-bin|000001.000008, 1979)",
                            "syncerBinlogGtid": "ddb8974e-6064-11eb-8357-0242ac110002:1-25",
                            ...
                            "synced": true,
                            "binlogType": "local"
                        }
                    }
                ]
            }
        ]
    }

この例では、データソース`mysql1`の`syncerBinlogGtid`不連続です。この場合、次のいずれかの方法でデータ損失に対処できます。

-   現在の時刻から完全エクスポート タスクのメタデータに記録されている位置までのアップストリーム バイナリ ログがパージされていない場合は、次の手順を実行できます。
    1.  現在のタスクを停止し、連続しない GTID を持つすべてのデータ ソースを削除します。
    2.  すべてのソース設定ファイルで`enable-relay` ～ `false`を設定します。
    3.  GTID が連続していないデータ ソース (上の例の`mysql1`など) の場合は、タスクを増分タスクに変更し、関連する`mysql-instances.meta`を各完全エクスポート タスクのメタデータ情報 ( `binlog-name` 、 `binlog-pos` 、および`binlog-gtid`の情報を含む) で構成します。
    4.  インクリメンタルタスクの`task.yaml`に`syncers.safe-mode` ～ `true`を設定し、タスクを再起動します。
    5.  増分タスクがすべての欠落データをダウンストリームにレプリケートした後、タスクを停止し、 `task.yaml`の`safe-mode`を`false`に変更します。
    6.  タスクを再度再開します。
-   アップストリームの binlog がパージされても、ローカル リレー ログが残っている場合は、次の手順を実行できます。
    1.  現在のタスクを停止します。
    2.  GTID が連続していないデータ ソース (上の例の`mysql1`など) の場合は、タスクを増分タスクに変更し、関連する`mysql-instances.meta`を各完全エクスポート タスクのメタデータ情報 ( `binlog-name` 、 `binlog-pos` 、および`binlog-gtid`の情報を含む) で構成します。
    3.  インクリメンタル タスクの`task.yaml`で、前の値`binlog-gtid`を前の値`previous_gtids`に変更します。上の例では、 `1-y`を`6-y`に変更します。
    4.  `task.yaml`のうち`syncers.safe-mode` ～ `true`設定してタスクを再起動してください。
    5.  増分タスクがすべての欠落データをダウンストリームにレプリケートした後、タスクを停止し、 `task.yaml`の`safe-mode`を`false`に変更します。
    6.  タスクを再度再開します。
    7.  データ ソースを再起動し、ソース構成ファイルで`enable-relay`または`enable-gtid`を`false`に設定します。
-   上記の条件がいずれも満たされない場合、またはタスクのデータ量が少ない場合は、次の手順を実行できます。
    1.  ダウンストリーム データベース内のインポートされたデータをクリーンアップします。
    2.  データ ソースを再起動し、ソース構成ファイルで`enable-relay`または`enable-gtid`を`false`に設定します。
    3.  新しいタスクを作成し、コマンド`start-task task.yaml --remove-meta`を実行してデータを最初から再度移行します。

上記の 1 番目と 2 番目の解決策で正常にレプリケートできるデータ ソース (上記の例の`mysql2`など) の場合、増分タスクを設定するときに、関連する`mysql-instances.meta` `subTaskStatus.sync`の`syncerBinlog`と`syncerBinlogGtid`情報で構成します。

## DM v2.0 では、ハートビート<code>heartbeat</code>が以前使用されていたものと異なります: サーバー ID が等しくない」というエラーをどのように処理すればよいですか? {#in-dm-v2-0-how-do-i-handle-the-error-heartbeat-config-is-different-from-previous-used-serverid-not-equal-when-switching-the-connection-between-dm-workers-and-mysql-instances-in-a-virtual-ip-environment-with-the-code-heartbeat-code-feature-enabled}

`heartbeat`機能は、DM v2.0 以降のバージョンではデフォルトで無効になっています。タスク構成ファイルでこの機能を有効にすると、高可用性機能が妨げられます。この問題を解決するには、タスク構成ファイルで`enable-heartbeat`から`false`を設定して`heartbeat`機能を無効にし、タスク構成ファイルを再ロードします。 DM は、以降のリリースで`heartbeat`機能を強制的に無効にします。

## DM マスターが再起動後にクラスターに参加できず、DM が「埋め込み etcd の開始に失敗しました。RawCause: member xxx はすでにブートストラップされています」というエラーを報告するのはなぜですか? {#why-does-a-dm-master-fail-to-join-the-cluster-after-it-restarts-and-dm-reports-the-error-fail-to-start-embed-etcd-rawcause-member-xxx-has-already-been-bootstrapped}

DM マスターが起動すると、DM は現在のディレクトリに etcd 情報を記録します。 DM マスターの再起動後にディレクトリが変更されると、DM は etcd 情報にアクセスできないため、再起動は失敗します。

この問題を解決するには、 TiUP を使用して DM クラスターを保守することをお勧めします。バイナリ ファイルを使用してデプロイする必要がある場合は、DM マスターの設定ファイルで絶対パスを使用して`data-dir`を設定するか、コマンドを実行する現在のディレクトリに注意する必要があります。

## dmctl を使用してコマンドを実行すると DM-master に接続できないのはなぜですか? {#why-dm-master-cannot-be-connected-when-i-use-dmctl-to-execute-commands}

dmctl 実行コマンドを使用すると、(コマンドでパラメータ値`--master-addr`指定した場合でも) DM マスターへの接続が失敗し、 `RawCause: context deadline exceeded, Workaround: please check your network connection.`のようなエラー メッセージが表示される場合があります。しかし、 `telnet <master-addr>`のようなコマンドを使用してネットワーク接続をチェックした後、例外は見つかりませんでした。

この場合、環境変数`https_proxy` ( **https**であることに注意してください) を確認できます。この変数が構成されている場合、 dmctl は`https_proxy`で指定されたホストとポートに自動的に接続します。ホストに対応する`proxy`サービスがない場合、接続は失敗します。

この問題を解決するには、 `https_proxy`が必須かどうかを確認してください。そうでない場合は、設定を解除してください。それ以外の場合は、元の dmctl コマンドの前に環境変数設定`https_proxy="" ./dmctl --master-addr "x.x.x.x:8261"`を追加します。

> **注記：**
>
> `proxy`に関連する環境変数には、 `http_proxy` 、 `https_proxy` 、および`no_proxy`があります。上記の手順を実行しても接続エラーが解決しない場合は、 `http_proxy`と`no_proxy`の構成パラメータが正しいかどうかを確認してください。

## DM バージョン 2.0.2 から 2.0.6 で start-relay コマンドを実行するときに返されたエラーを処理するにはどうすればよいですか? {#how-to-handle-the-returned-error-when-executing-start-relay-command-for-dm-versions-from-2-0-2-to-2-0-6}

    flush local meta, Rawcause: open relay-dir/xxx.000001/relay.metayyyy: no such file or directory

上記のエラーは、次の場合に発生する可能性があります。

-   DM は v2.0.1 以前から v2.0.2 ～ v2.0.6 にアップグレードされ、リレー ログはアップグレード前に開始され、アップグレード後に再起動されます。
-   stop-relay コマンドを実行してリレーログを一時停止し、再開します。

次のオプションによってこのエラーを回避できます。

-   再起動リレーログ:

        » stop-relay -s sourceID workerName
        » start-relay -s sourceID workerName

-   DM を v2.0.7 以降のバージョンにアップグレードします。

## ロード ユニットが<code>Unknown character set</code>エラーを報告するのはなぜですか? {#why-does-the-load-unit-report-the-code-unknown-character-set-code-error}

TiDB は、すべての MySQL 文字セットをサポートしているわけではありません。したがって、完全インポート中にテーブル スキーマを作成するときにサポートされていない文字セットが使用されると、DM はこのエラーを報告します。このエラーを回避するには、特定のデータに応じて[TiDB がサポートする文字セット](/character-set-and-collation.md)使用してダウンストリームにテーブル スキーマを事前に作成します。
