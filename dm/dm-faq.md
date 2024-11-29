---
title: TiDB Data Migration FAQs
summary: TiDB データ移行 (DM) に関するよくある質問 (FAQ) について説明します。
---

# TiDB データ移行に関する FAQ {#tidb-data-migration-faqs}

このドキュメントでは、TiDB データ移行 (DM) に関するよくある質問 (FAQ) をまとめています。

## DM は Alibaba RDS またはその他のクラウド データベースからのデータ移行をサポートしていますか? {#does-dm-support-migrating-data-from-alibaba-rds-or-other-cloud-databases}

現在、DM は MySQL または MariaDB binlogの標準バージョンのデコードのみをサポートしています。Alibaba Cloud RDS やその他のクラウド データベースではテストされていません。binlogが標準形式であることが確認されている場合は、サポートされます。

Alibaba Cloud RDS の主キーのないアップストリーム テーブルの場合、そのbinlog に非表示の主キー列が含まれたままになり、元のテーブル構造と一致しないという既知の問題があります。

互換性に関する既知の問題は次のとおりです。

-   **Alibaba Cloud RDS**では、主キーのないアップストリーム テーブルの場合、そのbinlogには非表示の主キー列がまだ含まれており、元のテーブル構造と一致していません。
-   **HUAWEI Cloud RDS**では、 binlogファイルを直接読み取ることはできません。詳細については、 [HUAWEI Cloud RDS はBinlogバックアップファイルを直接読み取ることができますか?](https://support.huaweicloud.com/en-us/rds_faq/rds_faq_0210.html)参照してください。

## タスク構成のブロックおよび許可リストの正規表現は<code>non-capturing (?!)</code> ? {#does-the-regular-expression-of-the-block-and-allow-list-in-the-task-configuration-support-code-non-capturing-code}

現在、DM はこれをサポートしておらず、 Golang標準ライブラリの正規表現のみをサポートしています。Golang でサポートされている正規表現については、 [re2構文](https://github.com/google/re2/wiki/Syntax)参照してください。

## アップストリームで実行されたステートメントに複数の DDL 操作が含まれている場合、DM はそのような移行をサポートしますか? {#if-a-statement-executed-upstream-contains-multiple-ddl-operations-does-dm-support-such-migration}

DM は、複数の DDL 変更操作を含む単一のステートメントを、1 つの DDL 操作のみを含む複数のステートメントに分割しようとしますが、すべてのケースをカバーできるとは限りません。アップストリームで実行されるステートメントには 1 つの DDL 操作のみを含めるか、テスト環境で検証することをお勧めします。サポートされていない場合は、 [問題](https://github.com/pingcap/tiflow/issues) `pingcap/tiflow`のリポジトリを提出できます。

## 互換性のない DDL ステートメントをどのように処理しますか? {#how-to-handle-incompatible-ddl-statements}

TiDB でサポートされていない DDL 文に遭遇した場合は、dmctl を使用して手動で処理する必要があります (DDL 文をスキップするか、DDL 文を指定された DDL 文に置き換えます)。詳細については、 [失敗したDDLステートメントを処理する](/dm/handle-failed-ddl-statements.md)参照してください。

> **注記：**
>
> 現在、TiDB は MySQL がサポートするすべての DDL ステートメントと互換性がありません。1 [MySQL 互換性](/mysql-compatibility.md#ddl-operations)参照してください。

## DM はビュー関連の DDL ステートメントと DML ステートメントを TiDB に複製しますか? {#does-dm-replicate-view-related-ddl-statements-and-dml-statements-to-tidb}

現在、DM はビュー関連の DDL ステートメントをダウンストリーム TiDB クラスターに複製しません。また、ビュー関連の DML ステートメントをダウンストリーム TiDB クラスターに複製しません。

## データ移行タスクをリセットするにはどうすればいいですか? {#how-to-reset-the-data-migration-task}

データ移行中に例外が発生し、データ移行タスクを再開できない場合は、タスクをリセットしてデータを再移行する必要があります。

1.  異常なデータ移行タスクを停止するには、 `stop-task`コマンドを実行します。

2.  ダウンストリームに移行されたデータを消去します。

3.  次のいずれかの方法でデータ移行タスクを再開します。

    -   タスク設定ファイルで新しいタスク名を指定します。次に、 `start-task {task-config-file}`実行します。
    -   `start-task --remove-meta {task-config-file}`実行します。

## <code>online-ddl: true</code>を設定した後、gh-ost テーブルに関連する DDL 操作によって返されたエラーをどのように処理しますか? {#how-to-handle-the-error-returned-by-the-ddl-operation-related-to-the-gh-ost-table-after-code-online-ddl-true-code-is-set}

    [unit=Sync] ["error information"="{\"msg\":\"[code=36046:class=sync-unit:scope=internal:level=high] online ddls on ghost table `xxx`.`_xxxx_gho`\\ngithub.com/pingcap/tiflow/pkg/terror.(*Error).Generate ......

上記のエラーは、次の理由により発生する可能性があります。

最後の`rename ghost_table to origin table`ステップでは、DM はメモリ内の DDL 情報を読み取り、元のテーブルの DDL に復元します。

ただし、メモリ内の DDL 情報は、次の 2 つの方法のいずれかで取得されます。

-   DM [`alter ghost_table`操作中に gh-ost テーブルを処理する](/dm/feature-online-ddl.md#online-schema-change-gh-ost)および`ghost_table`の DDL 情報を記録しま す。
-   DM ワーカーが再起動されてタスクが開始されると、DM は`dm_meta.{task_name}_onlineddl`から DDL を読み取ります。

そのため、増分レプリケーションのプロセスで、指定された Pos が`alter ghost_table` DDL をスキップしたが、その Pos がまだ gh-ost の online-ddl プロセス中である場合、ghost_table はメモリまたは`dm_meta.{task_name}_onlineddl`に正しく書き込まれません。このような場合、上記のエラーが返されます。

このエラーは次の手順で回避できます。

1.  タスクの`online-ddl-scheme`または`online-ddl`構成を削除します。

2.  `_{table_name}_del` `block-allow-list.ignore-tables` `_{table_name}_gho` `_{table_name}_ghc` 。

3.  ダウンストリーム TiDB でアップストリーム DDL を手動で実行します。

4.  gh-ost プロセス後に Pos が位置に複製されたら、 `online-ddl-scheme`または`online-ddl`構成を再度有効にして、 `block-allow-list.ignore-tables`コメント アウトします。

## 既存のデータ移行タスクにテーブルを追加するにはどうすればよいですか? {#how-to-add-tables-to-the-existing-data-migration-tasks}

実行中のデータ移行タスクにテーブルを追加する必要がある場合は、タスクの段階に応じて次の方法で対処できます。

> **注記：**
>
> 既存のデータ移行タスクにテーブルを追加するのは複雑なため、必要な場合にのみこの操作を実行することをお勧めします。

### <code>Dump</code>段階 {#in-the-code-dump-code-stage}

MySQL はエクスポートのスナップショットを指定できないため、エクスポート中にデータ移行タスクを更新し、その後再起動してチェックポイントを介してエクスポートを再開することはサポートされていません。したがって、第`Dump`段階で移行する必要があるテーブルを動的に追加することはできません。

移行のためにテーブルを追加する必要がある場合は、新しい構成ファイルを使用してタスクを直接再起動することをお勧めします。

### <code>Load</code>ステージ {#in-the-code-load-code-stage}

エクスポート中、複数のデータ移行タスクは通常、異なるbinlog位置を持ちます。第`Load`段階でタスクをマージすると、binlog位置について合意に達することができない可能性があります。したがって、第`Load`段階でデータ移行タスクにテーブルを追加することはお勧めしません。

### <code>Sync</code>段階 {#in-the-code-sync-code-stage}

データ移行タスクが第`Sync`段階にあるときに、構成ファイルにテーブルを追加してタスクを再開すると、DM は新しく追加されたテーブルに対して完全なエクスポートとインポートを再実行しません。代わりに、DM は前のチェックポイントから増分レプリケーションを続行します。

したがって、新しく追加されたテーブルの完全なデータがダウンストリームにインポートされていない場合は、別のデータ移行タスクを使用して、完全なデータをダウンストリームにエクスポートおよびインポートする必要があります。

既存の移行タスクに対応するグローバルチェックポイント（ `is_global=1` ）の位置情報を`checkpoint-T` （例： `(mysql-bin.000100, 1234)` ）として記録します。移行タスクに追加するテーブルのフルエクスポート`metedata` （または`Sync`ステージの別のデータ移行タスクのチェックポイント）の位置情報を`checkpoint-S` （例： `(mysql-bin.000099, 5678)`として記録します。次の手順でテーブルを移行タスクに追加できます。

1.  既存の移行タスクを停止するには、 `stop-task`使用します。追加するテーブルが実行中の別の移行タスクに属している場合は、そのタスクも停止します。

2.  MySQL クライアントを使用してダウンストリーム TiDB データベースに接続し、既存の移行タスクに対応するチェックポイント テーブル内の情報を`checkpoint-T`と`checkpoint-S`間の小さい方の値に手動で更新します。この例では`(mysql- bin.000099, 5678)`です。

    -   更新するチェックポイント テーブルは、スキーマ`{dm_meta}`の`{task-name}_syncer_checkpoint`です。

    -   更新するチェックポイント行は`id=(source-id)`と`is_global=1`と一致します。

    -   更新するチェックポイント列は`binlog_name`と`binlog_pos`です。

3.  再入実行を確実にするために、タスクの`syncers`を`safe-mode: true`設定します。

4.  `start-task`使用してタスクを開始します。

5.  `query-status`を通してタスクの状態を観察します。 `syncerBinlog` `checkpoint-T`と`checkpoint-S`の大きい方の値を超えたら、 `safe-mode`元の値に戻し、タスクを再開します。この例では`(mysql-bin.000100, 1234)`です。

## <code>packet for query is too large. Try adjusting the &#39;max_allowed_packet&#39; variable</code> ? {#how-to-handle-the-error-code-packet-for-query-is-too-large-try-adjusting-the-max-allowed-packet-variable-code-that-occurs-during-the-full-import}

以下のパラメータをデフォルトの 67108864 (64M) より大きい値に設定します。

-   TiDBサーバーのグローバル変数: `max_allowed_packet` 。
-   タスク設定ファイル内の設定項目： `target-database.max-allowed-packet` . 詳細については[DM 高度なタスクコンフィグレーションファイル](/dm/task-configuration-file-full.md)を参照してください。

## DM 1.0 クラスターの既存の DM 移行タスクが DM 2.0 以降のクラスターで実行されているときに発生するエラー<code>Error 1054: Unknown column &#39;binlog_gtid&#39; in &#39;field list&#39;</code>を処理する方法を教えてください。 {#how-to-handle-the-error-code-error-1054-unknown-column-binlog-gtid-in-field-list-code-that-occurs-when-existing-dm-migration-tasks-of-an-dm-1-0-cluster-are-running-on-a-dm-2-0-or-newer-cluster}

DM v2.0 以降、増分データレプリケーションを続行するために DM 1.0 クラスターのタスク構成ファイルで`start-task`コマンドを直接実行すると、エラー`Error 1054: Unknown column 'binlog_gtid' in 'field list'`が発生します。

このエラーは[DM 1.0 クラスターの DM 移行タスクを DM 2.0 クラスターに手動でインポートする](/dm/manually-upgrade-dm-1.0-to-2.0.md)で処理できます。

## TiUP がDM の一部のバージョン (たとえば、v2.0.0-hotfix) の展開に失敗するのはなぜですか? {#why-does-tiup-fail-to-deploy-some-versions-of-dm-for-example-v2-0-0-hotfix}

`tiup list dm-master`コマンドを使用すると、 TiUP が展開をサポートする DM バージョンを表示できます。TiUPは、このコマンドで表示されない DM バージョンを管理しません。

## DM がデータを複製しているときに発生するエラー<code>parse mydumper metadata error: EOF</code>をどのように処理すればよいですか? {#how-to-handle-the-error-code-parse-mydumper-metadata-error-eof-code-that-occurs-when-dm-is-replicating-data}

このエラーをさらに分析するには、エラー メッセージとログ ファイルを確認する必要があります。原因としては、権限不足のためダンプ ユニットが正しいメタデータ ファイルを生成していないことが考えられます。

## シャード化されたスキーマとテーブルを複製するときに DM が致命的なエラーを報告しないのに、ダウンストリーム データが失われるのはなぜですか? {#why-does-dm-report-no-fatal-error-when-replicating-sharded-schemas-and-tables-but-downstream-data-is-lost}

構成項目`block-allow-list`と`table-route`確認します。

-   `block-allow-list`下にあるアップストリーム データベースとテーブルの名前を設定する必要があります。 `do-tables`前に「~」を追加すると、正規表現を使用して名前を一致させることができます。
-   `table-route` 、テーブル名を一致させるために正規表現ではなくワイルドカード文字を使用します。たとえば、 `table_parttern_[0-63]` `table_parttern_0` `table_pattern_6`までの 7 つのテーブルにのみ一致します。

## DM がアップストリームからレプリケートしていないのに、 <code>replicate lag</code>モニター メトリックにデータが表示されないのはなぜですか? {#why-does-the-code-replicate-lag-code-monitor-metric-show-no-data-when-dm-is-not-replicating-from-upstream}

DM 1.0 では、モニター データを生成するには`enable-heartbeat`有効にする必要があります。DM 2.0 以降のバージョンでは、この機能はサポートされていないため、モニター メトリック`replicate lag`にデータがないと考えられます。

## DM がタスクを開始しているときに、 <code>context deadline exceeded</code>を示すエラー メッセージの<code>RawCause</code>で<code>fail to initial unit Sync of subtask</code>エラーをどのように処理しますか? {#how-to-handle-the-error-code-fail-to-initial-unit-sync-of-subtask-code-when-dm-is-starting-a-task-with-the-code-rawcause-code-in-the-error-message-showing-code-context-deadline-exceeded-code}

これは DM 2.0.0 バージョンの既知の問題であり、DM 2.0.1 バージョンで修正される予定です。レプリケーション タスクで処理するテーブルが多数ある場合に発生する可能性があります。TiUPを使用して DM を展開する場合は、DM をナイトリー バージョンにアップグレードしてこの問題を修正できます。または、GitHub の[DMのリリースページ](https://github.com/pingcap/tiflow/releases)から 2.0.0-hotfix バージョンをダウンロードして、実行可能ファイルを手動で置き換えることもできます。

## DM がデータを複製しているときに<code>duplicate entry</code>エラーを処理する方法を教えてください。 {#how-to-handle-the-error-code-duplicate-entry-code-when-dm-is-replicating-data}

まず、以下の点を確認して確認する必要があります。

-   レプリケーション タスクで`disable-detect`が構成されていません (v2.0.7 以前のバージョン)。
-   データは手動でも他のレプリケーション プログラムによっても挿入されません。
-   このテーブルに関連付けられた DML フィルターは構成されていません。

トラブルシューティングを容易にするために、まずダウンストリーム TiDB インスタンスの一般的なログ ファイルを収集し、次に[TiDB コミュニティ Slack チャンネル](https://tidbcommunity.slack.com/archives/CH7TTLL7P)でテクニカル サポートを依頼します。次の例は、一般的なログ ファイルを収集する方法を示しています。

```bash
# Enable general log collection
curl -X POST -d "tidb_general_log=1" http://{TiDBIP}:10080/settings
# Disable general log collection
curl -X POST -d "tidb_general_log=0" http://{TiDBIP}:10080/settings
```

`duplicate entry`エラーが発生した場合は、競合データを含むレコードのログ ファイルを確認する必要があります。

## 一部の監視パネルに<code>No data point</code> 。なぜですか? {#why-do-some-monitoring-panels-show-code-no-data-point-code}

一部のパネルにデータがないのは正常です。たとえば、エラーが報告されていない場合、DDL ロックがない場合、またはリレー ログ機能が有効になっていない場合、対応するパネルには`No data point`が表示されます。各パネルの詳細な説明については、 [DM モニタリング メトリック](/dm/monitor-a-dm-cluster.md)参照してください。

## DM v1.0 では、タスクにエラーがある場合にコマンド<code>sql-skip</code>一部のステートメントをスキップできないのはなぜですか? {#in-dm-v1-0-why-does-the-command-code-sql-skip-code-fail-to-skip-some-statements-when-the-task-is-in-error}

まず、 `sql-skip`実行した後、binlogの位置がまだ進んでいるかどうかを確認する必要があります。進んでいる場合は、 `sql-skip`有効になっていることを意味します。このエラーが引き続き発生する理由は、アップストリームが複数のサポートされていない DDL ステートメントを送信するためです。 `sql-skip -s <sql-pattern>`使用して、これらのステートメントに一致するパターンを設定できます。

場合によっては、エラー メッセージに`parse statement`情報が含まれることがあります。次に例を示します。

    if the DDL is not needed, you can use a filter rule with \"*\" schema-pattern to ignore it.\n\t : parse statement: line 1 column 11 near \"EVENT `event_del_big_table` \r\nDISABLE\" %!!(MISSING)(EXTRA string=ALTER EVENT `event_del_big_table` \r\nDISABLE

このタイプのエラーの原因は、TiDB パーサーがアップストリームから送信された`ALTER EVENT`などの DDL ステートメントを解析できないため、 `sql-skip`期待どおりに機能しないことです。構成ファイルに[binlogイベント フィルター](/dm/dm-binlog-event-filter.md)を追加してこれらのステートメントをフィルタリングし、 `schema-pattern: "*"`設定できます。DM v2.0.1 以降、DM は`EVENT`に関連するステートメントを事前にフィルタリングします。

DM v6.0 以降、 `sql-skip`と`handle-error` `binlog`に置き換えられました。この問題を回避するには、代わりに`binlog`コマンドを使用できます。

## DM がレプリケートされているときに、ダウンストリームに<code>REPLACE</code>ステートメントが表示され続けるのはなぜですか? {#why-do-code-replace-code-statements-keep-appearing-in-the-downstream-when-dm-is-replicating}

タスクに対して[セーフモード](/dm/dm-glossary.md#safe-mode)自動的に有効になっているかどうかを確認する必要があります。エラー後にタスクが自動的に再開される場合、または高可用性スケジュールがある場合は、タスクが開始または再開されてから 1 分以内であるため、セーフ モードが有効になっています。

DM-worker ログ ファイルをチェックして、 `change count`含む行を検索できます。行の`new count`が 0 でない場合、セーフ モードが有効になっています。セーフ モードが有効になっている理由を確認するには、セーフ モードがいつ発生するか、以前にエラーが報告されているかどうかを確認します。

## DM v2.0 では、タスク中に DM が再起動すると、完全インポート タスクが失敗するのはなぜですか? {#in-dm-v2-0-why-does-the-full-import-task-fail-if-dm-restarts-during-the-task}

DM v2.0.1 以前のバージョンでは、完全なインポートが完了する前に DM が再起動すると、上流のデータ ソースと DM ワーカー ノード間のバインディングが変更される場合があります。たとえば、ダンプ ユニットの中間データが DM ワーカー ノード A にあるが、ロード ユニットが DM ワーカー ノード B によって実行されている場合、操作が失敗する可能性があります。

この問題に対する解決策は次の 2 つです。

-   データ量が少ない (1 TB 未満) 場合、またはタスクがシャード化されたテーブルをマージする場合は、次の手順を実行します。

    1.  ダウンストリーム データベースにインポートされたデータをクリーンアップします。
    2.  エクスポートされたデータのディレクトリ内のすべてのファイルを削除します。
    3.  dmctl を使用してタスクを削除し、コマンド`start-task --remove-meta`を実行して新しいタスクを作成します。

    新しいタスクが開始したら、冗長な DM ワーカー ノードが存在しないことを確認し、完全インポート中に DM クラスターを再起動またはアップグレードしないようにすることをお勧めします。

-   データ量が大きい場合（1 TB を超える場合）は、次の手順を実行します。

    1.  ダウンストリーム データベースにインポートされたデータをクリーンアップします。
    2.  データを処理する DM ワーカーノードに TiDB-Lightning をデプロイ。
    3.  TiDB-Lightning のローカルバックエンド モードを使用して、DM ダンプ ユニットがエクスポートするデータをインポートします。
    4.  完全なインポートが完了したら、次の方法でタスク構成ファイルを編集し、タスクを再起動します。
        -   `task-mode` `incremental`に変更します。
        -   ダンプユニットが出力するメタデータファイルに記録されている位置に値`mysql-instance.meta.pos`を設定します。

## 増分タスク中に再起動すると、DM がエラー<code>ERROR 1236 (HY000): The slave is connecting using CHANGE MASTER TO MASTER_AUTO_POSITION = 1, but the master has purged binary logs containing GTIDs that the slave requires.</code>のはなぜですか? {#why-does-dm-report-the-error-code-error-1236-hy000-the-slave-is-connecting-using-change-master-to-master-auto-position-1-but-the-master-has-purged-binary-logs-containing-gtids-that-the-slave-requires-code-if-it-restarts-during-an-incremental-task}

このエラーは、ダンプ ユニットによって出力されたメタデータ ファイルに記録されたアップストリームbinlogの位置が、完全な移行中に消去されたことを示します。

この問題が発生した場合は、タスクを一時停止し、ダウンストリーム データベースに移行されたすべてのデータを削除し、 `--remove-meta`オプションを使用して新しいタスクを開始する必要があります。

次の方法で設定することで、この問題を事前に回避できます。

1.  完全な移行タスクが完了する前に、必要なbinlogファイルが誤って消去されるのを防ぐため、アップストリーム MySQL データベースの値を`expire_logs_days`増やします。データ量が多い場合は、タスクを高速化するために dumpling と TiDB-Lightning を同時に使用することをお勧めします。
2.  このタスクのリレー ログ機能を有効にすると、binlogの位置が消去されても DM がリレー ログからデータを読み取ることができます。

## クラスターがTiUP v1.3.0 または v1.3.1 を使用してデプロイされている場合、DM クラスターの Grafana ダッシュボードに<code>failed to fetch dashboard</code>表示されるのはなぜですか? {#why-does-the-grafana-dashboard-of-a-dm-cluster-display-code-failed-to-fetch-dashboard-code-if-the-cluster-is-deployed-using-tiup-v1-3-0-or-v1-3-1}

これはTiUPの既知のバグであり、 TiUP v1.3.2 で修正されています。この問題の解決策は次の 2 つです。

-   解決策 1:
    1.  コマンド`tiup update --self && tiup update dm`を使用して、 TiUP を新しいバージョンにアップグレードします。
    2.  クラスター内の Grafana ノードをスケールインからスケールアウトして、Grafana サービスを再起動します。
-   解決策2:
    1.  `deploy/grafana-$port/bin/public`フォルダをバックアップします。
    2.  [TiUP DMオフラインパッケージ](https://download.pingcap.org/tidb-dm-v2.0.1-linux-amd64.tar.gz)ダウンロードして解凍します。
    3.  オフライン パッケージの`grafana-v4.0.3-**.tar.gz`解凍します。
    4.  フォルダー`deploy/grafana-$port/bin/public` `grafana-v4.0.3-**.tar.gz`のフォルダー`public`に置き換えます。
    5.  `tiup dm restart $cluster_name -R grafana`実行して Grafana サービスを再起動します。

## DM v2.0 では、タスクで<code>enable-relay</code>と<code>enable-gtid</code>同時に有効になっている場合、コマンド<code>query-status</code>のクエリ結果に、Syncer チェックポイント GTID が連続していないと表示されるのはなぜですか? {#in-dm-v2-0-why-does-the-query-result-of-the-command-code-query-status-code-show-that-the-syncer-checkpoint-gtids-are-inconsecutive-if-the-task-has-code-enable-relay-code-and-code-enable-gtid-code-enabled-at-the-same-time}

これは DM の既知のバグであり、DM v2.0.2 で修正されています。このバグは、次の 2 つの条件が同時に完全に満たされたときに発生します。

1.  ソース構成ファイルでは、パラメータ`enable-relay`と`enable-gtid` `true`に設定されています。
2.  アップストリーム データベースは**MySQL セカンダリ データベース**です。コマンド`show binlog events in '<newest-binlog>' limit 2`を実行してデータベースの`previous_gtids`クエリすると、次の例のように結果が連続しなくなります。

<!---->

    mysql> show binlog events in 'mysql-bin.000005' limit 2;
    +------------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+
    | Log_name         | Pos  | Event_type     | Server_id | End_log_pos | Info                                                               |
    +------------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+
    | mysql-bin.000005 |    4 | Format_desc    |    123452 |         123 | Server ver: 5.7.32-35-log, Binlog ver: 4                           |
    | mysql-bin.000005 |  123 | Previous_gtids |    123452 |         194 | d3618e68-6052-11eb-a68b-0242ac110002:6-7                           |
    +------------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+

このバグは、dmctl で`query-status <task>`実行してタスク情報を照会し、 `subTaskStatus.sync.syncerBinlogGtid`は連続していないが`subTaskStatus.sync.masterBinlogGtid`連続していることがわかった場合に発生します。次の例を参照してください。

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

この例では、データ ソース`mysql1`の`syncerBinlogGtid`連続していません。この場合、データ損失を処理するには、次のいずれかを実行します。

-   現在の時刻から完全エクスポート タスクのメタデータに記録された位置までのアップストリーム バイナリログが消去されていない場合は、次の手順を実行できます。
    1.  現在のタスクを停止し、連続していない GTID を持つすべてのデータ ソースを削除します。
    2.  すべてのソース構成ファイルで`enable-relay` ～ `false`設定します。
    3.  連続していない GTID を持つデータ ソース (上記の例の`mysql1`など) の場合は、タスクを増分タスクに変更し、 `binlog-name` 、 `binlog-pos` 、および`binlog-gtid`情報を含む各完全エクスポート タスクのメタデータ情報を使用して関連する`mysql-instances.meta`を構成します。
    4.  増分タスクの`task.yaml`に`syncers.safe-mode` `true`設定し、タスクを再起動します。
    5.  増分タスクがすべての欠落データをダウンストリームに複製した後、タスクを停止し、 `task.yaml`の`safe-mode`を`false`に変更します。
    6.  タスクをもう一度再開します。
-   アップストリームのバイナリログが消去されたが、ローカルリレーログが残っている場合は、次の手順を実行できます。
    1.  現在のタスクを停止します。
    2.  連続していない GTID を持つデータ ソース (上記の例の`mysql1`など) の場合は、タスクを増分タスクに変更し、 `binlog-name` 、 `binlog-pos` 、および`binlog-gtid`情報を含む各完全エクスポート タスクのメタデータ情報を使用して関連する`mysql-instances.meta`を構成します。
    3.  増分タスクの`task.yaml`で、前の値`binlog-gtid`を前の値`previous_gtids`に変更します。上記の例では、 `1-y` `6-y`に変更します。
    4.  `task.yaml`の`syncers.safe-mode`から`true`設定し、タスクを再開します。
    5.  増分タスクがすべての欠落データをダウンストリームに複製した後、タスクを停止し、 `task.yaml`の`safe-mode`を`false`に変更します。
    6.  タスクをもう一度再開します。
    7.  データ ソースを再起動し、ソース構成ファイルで`enable-relay`または`enable-gtid`を`false`に設定します。
-   上記の条件がいずれも満たされていない場合、またはタスクのデータ量が少ない場合は、次の手順を実行できます。
    1.  ダウンストリーム データベースにインポートされたデータをクリーンアップします。
    2.  データ ソースを再起動し、ソース構成ファイルで`enable-relay`または`enable-gtid`を`false`に設定します。
    3.  新しいタスクを作成し、コマンド`start-task task.yaml --remove-meta`を実行して、データを最初から再度移行します。

上記の 1 番目と 2 番目のソリューションで正常にレプリケートできるデータ ソース (上記の例の`mysql2`など) の場合は、増分タスクを設定するときに、 `subTaskStatus.sync`の`syncerBinlog`と`syncerBinlogGtid`情報を使用して関連する`mysql-instances.meta`構成します。

## DM v2.0 では、 <code>heartbeat</code>機能が有効になっている仮想 IP 環境で DM ワーカーと MySQL インスタンス間の接続を切り替えるときに、「ハートビート設定が以前に使用されたものと異なります: serverID が等しくありません」というエラーをどのように処理すればよいですか? {#in-dm-v2-0-how-do-i-handle-the-error-heartbeat-config-is-different-from-previous-used-serverid-not-equal-when-switching-the-connection-between-dm-workers-and-mysql-instances-in-a-virtual-ip-environment-with-the-code-heartbeat-code-feature-enabled}

DM v2.0 以降のバージョンでは、 `heartbeat`機能はデフォルトで無効になっています。タスク構成ファイルでこの機能を有効にすると、高可用性機能に干渉します。この問題を解決するには、タスク構成ファイルで`enable-heartbeat`を`false`に設定して`heartbeat`機能を無効にし、タスク構成ファイルを再ロードします。DM は、以降のリリースで`heartbeat`機能を強制的に無効にします。

## DM マスターが再起動後にクラスターに参加できず、DM が「埋め込み etcd の開始に失敗しました。RawCause: メンバー xxx はすでにブートストラップされています」というエラーを報告するのはなぜですか? {#why-does-a-dm-master-fail-to-join-the-cluster-after-it-restarts-and-dm-reports-the-error-fail-to-start-embed-etcd-rawcause-member-xxx-has-already-been-bootstrapped}

DM マスターが起動すると、DM は現在のディレクトリに etcd 情報を記録します。DM マスターの再起動後にディレクトリが変更されると、DM は etcd 情報にアクセスできず、再起動が失敗します。

この問題を解決するには、 TiUP を使用して DM クラスターを保守することをお勧めします。バイナリ ファイルを使用してデプロイする必要がある場合は、DM マスターの構成ファイルで絶対パスを使用して`data-dir`構成するか、コマンドを実行する現在のディレクトリに注意する必要があります。

## dmctl を使用してコマンドを実行すると、DM マスターに接続できないのはなぜですか? {#why-dm-master-cannot-be-connected-when-i-use-dmctl-to-execute-commands}

dmctl 実行コマンドを使用すると、DM マスターへの接続が失敗し (コマンドでパラメータ値`--master-addr`を指定した場合でも)、エラー メッセージが`RawCause: context deadline exceeded, Workaround: please check your network connection.`ようになる場合があります。ただし、 `telnet <master-addr>`などのコマンドを使用してネットワーク接続をチェックした後、例外は見つかりません。

この場合、環境変数`https_proxy`確認できます ( **https**であることに注意してください)。この変数が設定されている場合、dmctl は`https_proxy`で指定されたホストとポートに自動的に接続します。ホストに対応する`proxy`転送サービスがない場合、接続は失敗します。

この問題を解決するには、 `https_proxy`必須かどうかを確認します。必須でない場合は、設定をキャンセルします。必須でない場合は、元の dmctl コマンドの前に環境変数設定`https_proxy="" ./dmctl --master-addr "x.x.x.x:8261"`を追加します。

> **注記：**
>
> `proxy`に関連する環境変数には`http_proxy` 、 `https_proxy` 、 `no_proxy`があります。上記の手順を実行しても接続エラーが解決しない場合は、 `http_proxy`と`no_proxy`の設定パラメータが正しいかどうかを確認してください。

## DM バージョン 2.0.2 から 2.0.6 で start-relay コマンドを実行したときに返されるエラーをどのように処理しますか? {#how-to-handle-the-returned-error-when-executing-start-relay-command-for-dm-versions-from-2-0-2-to-2-0-6}

    flush local meta, Rawcause: open relay-dir/xxx.000001/relay.metayyyy: no such file or directory

上記のエラーは、次の場合に発生する可能性があります。

-   DM は v2.0.1 以前から v2.0.2 - v2.0.6 にアップグレードされており、アップグレード前にリレー ログが開始され、アップグレード後に再起動されます。
-   stop-relay コマンドを実行してリレー ログを一時停止し、再起動します。

次のオプションによりこのエラーを回避できます。

-   リレーログを再起動します:

        » stop-relay -s sourceID workerName
        » start-relay -s sourceID workerName

-   DM を v2.0.7 以降のバージョンにアップグレードします。

## ロード ユニットが<code>Unknown character set</code>エラーを報告するのはなぜですか? {#why-does-the-load-unit-report-the-code-unknown-character-set-code-error}

TiDB はすべての MySQL 文字セットをサポートしていません。そのため、フルインポート中にテーブル スキーマを作成するときにサポートされていない文字セットが使用されると、DM はこのエラーを報告します。このエラーを回避するには、特定のデータに応じて[TiDB でサポートされている文字セット](/character-set-and-collation.md)使用してダウンストリームで事前にテーブル スキーマを作成します。
