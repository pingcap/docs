---
title: TiDB Data Migration FAQs
summary: TiDB データ移行 (DM) に関するよくある質問 (FAQ) について説明します。
---

# TiDBデータ移行に関するよくある質問 {#tidb-data-migration-faqs}

このドキュメントでは、TiDB データ移行 (DM) に関するよくある質問 (FAQ) をまとめています。

## DM は Alibaba RDS またはその他のクラウド データベースからのデータ移行をサポートしていますか? {#does-dm-support-migrating-data-from-alibaba-rds-or-other-cloud-databases}

現在、DMはMySQLまたはMariaDBの標準バージョンのbinlogのデコードのみをサポートしています。Alibaba Cloud RDSやその他のクラウドデータベースではテストされていません。binlogが標準形式であることが確認できれば、サポートされます。

Alibaba Cloud RDS の主キーのないアップストリーム テーブルの場合、そのbinlogに非表示の主キー列が含まれたままになり、元のテーブル構造と一致しないという既知の問題があります。

互換性に関する既知の問題は次のとおりです。

-   **Alibaba Cloud RDS**では、主キーのないアップストリーム テーブルの場合、そのbinlogには非表示の主キー列がまだ含まれており、元のテーブル構造と一致していません。
-   **HUAWEI Cloud RDS**では、 binlogファイルの直接読み取りはサポートされていません。詳細については、 [HUAWEI Cloud RDS はBinlogバックアップファイルを直接読み取ることができますか?](https://support.huaweicloud.com/en-us/rds_faq/rds_faq_0210.html)参照してください。

## タスク構成のブロックおよび許可リストの正規表現は<code>non-capturing (?!)</code> ? {#does-the-regular-expression-of-the-block-and-allow-list-in-the-task-configuration-support-code-non-capturing-code}

現在、DMはこれをサポートしておらず、 Golang標準ライブラリの正規表現のみをサポートしています。Golangでサポートされている正規表現については、 [re2構文](https://github.com/google/re2/wiki/Syntax)参照してください。

## アップストリームで実行されたステートメントに複数の DDL 操作が含まれている場合、DM はそのような移行をサポートしますか? {#if-a-statement-executed-upstream-contains-multiple-ddl-operations-does-dm-support-such-migration}

DMは、複数のDDL変更操作を含む単一の文を、1つのDDL操作のみを含む複数の文に分割しようとしますが、すべてのケースに対応できるとは限りません。上流で実行される文には1つのDDL操作のみを含めるか、テスト環境で検証することをお勧めします。サポートされていない場合は、リポジトリ[問題](https://github.com/pingcap/tiflow/issues) ～ `pingcap/tiflow`にアップグレードしてください。

## 互換性のない DDL ステートメントをどのように処理しますか? {#how-to-handle-incompatible-ddl-statements}

TiDBでサポートされていないDDL文に遭遇した場合は、dmctlを使用して手動で処理する必要があります（DDL文をスキップするか、指定されたDDL文に置き換えます）。詳細は[失敗したDDL文を処理する](/dm/handle-failed-ddl-statements.md)参照してください。

> **注記：**
>
> 現在、TiDBはMySQLがサポートするすべてのDDL文と互換性がありません[MySQLの互換性](/mysql-compatibility.md#ddl-operations)参照してください。

## DM はビュー関連の DDL ステートメントと DML ステートメントを TiDB に複製しますか? {#does-dm-replicate-view-related-ddl-statements-and-dml-statements-to-tidb}

現在、DM はビュー関連の DDL ステートメントをダウンストリーム TiDB クラスターに複製しません。また、ビュー関連の DML ステートメントをダウンストリーム TiDB クラスターに複製しません。

## データ移行タスクをリセットするにはどうすればいいですか? {#how-to-reset-the-data-migration-task}

データ移行中に例外が発生し、データ移行タスクを再開できない場合は、タスクをリセットしてデータを再移行する必要があります。

1.  異常なデータ移行タスクを停止するには、コマンド`stop-task`を実行します。

2.  ダウンストリームに移行されたデータを消去します。

3.  データ移行タスクを再開するには、次のいずれかの方法を使用します。

    -   タスク設定ファイルで新しいタスク名を指定します。次に、 `start-task {task-config-file}`実行します。
    -   `start-task --remove-meta {task-config-file}`実行します。

## <code>online-ddl: true</code>を設定した後、gh-ost テーブルに関連する DDL 操作によって返されたエラーをどのように処理しますか? {#how-to-handle-the-error-returned-by-the-ddl-operation-related-to-the-gh-ost-table-after-code-online-ddl-true-code-is-set}

    [unit=Sync] ["error information"="{\"msg\":\"[code=36046:class=sync-unit:scope=internal:level=high] online ddls on ghost table `xxx`.`_xxxx_gho`\\ngithub.com/pingcap/tiflow/pkg/terror.(*Error).Generate ......

上記のエラーは、次の理由により発生する可能性があります。

最後の`rename ghost_table to origin table`ステップでは、DM はメモリ内の DDL 情報を読み取り、元のテーブルの DDL に復元します。

ただし、メモリ内の DDL 情報は、次の 2 つの方法のいずれかで取得されます。

-   DM [`alter ghost_table`操作中に gh-ost テーブルを処理する](/dm/feature-online-ddl.md#online-schema-change-gh-ost)および`ghost_table`の DDL 情報を記録しま す。
-   DM ワーカーが再起動されてタスクが開始されると、DM は`dm_meta.{task_name}_onlineddl`から DDL を読み取ります。

そのため、増分レプリケーションのプロセスにおいて、指定されたPosが`alter ghost_table` DDLをスキップしたにもかかわらず、そのPosがgh-ostのオンラインDDLプロセス中である場合、ghost_tableはメモリまたは`dm_meta.{task_name}_onlineddl`に正しく書き込まれません。このような場合、上記のエラーが返されます。

このエラーは次の手順で回避できます。

1.  タスクの`online-ddl-scheme`または`online-ddl`構成を削除します。

2.  `block-allow-list.ignore-tables`で`_{table_name}_gho` `_{table_name}_ghc`設定`_{table_name}_del`ます。

3.  ダウンストリーム TiDB でアップストリーム DDL を手動で実行します。

4.  gh-ost プロセス後の位置に Pos が複製されたら、 `online-ddl-scheme`または`online-ddl`構成を再度有効にして、 `block-allow-list.ignore-tables`コメント アウトします。

## 既存のデータ移行タスクにテーブルを追加するにはどうすればよいですか? {#how-to-add-tables-to-the-existing-data-migration-tasks}

実行中のデータ移行タスクにテーブルを追加する必要がある場合は、タスクの段階に応じて次の方法で対処できます。

> **注記：**
>
> 既存のデータ移行タスクにテーブルを追加するのは複雑なため、必要な場合にのみこの操作を実行することをお勧めします。

### <code>Dump</code>段階 {#in-the-code-dump-code-stage}

MySQLはエクスポート時にスナップショットを指定できないため、エクスポート中にデータ移行タスクを更新し、その後再起動してチェックポイントからエクスポートを再開することができません。そのため、第`Dump`ステージで移行が必要なテーブルを動的に追加することはできません。

移行のためにテーブルを追加する必要がある場合は、新しい構成ファイルを使用してタスクを直接再起動することをお勧めします。

### <code>Load</code>ステージ {#in-the-code-load-code-stage}

エクスポート中、複数のデータ移行タスクは通常、異なるbinlogの位置を持ちます。第`Load`ステージでタスクをマージすると、binlogの位置について合意が得られない可能性があります。そのため、第`Load`ステージでデータ移行タスクにテーブルを追加することは推奨されません。

### <code>Sync</code>段階では {#in-the-code-sync-code-stage}

データ移行タスクが第`Sync`ステージにあるときに、設定ファイルにテーブルを追加してタスクを再開すると、DMは新しく追加されたテーブルに対してフルエクスポートとインポートを再実行しません。代わりに、DMは前回のチェックポイントから増分レプリケーションを継続します。

したがって、新しく追加されたテーブルの完全なデータがダウンストリームにインポートされていない場合は、別のデータ移行タスクを使用して、完全なデータをエクスポートしてダウンストリームにインポートする必要があります。

既存の移行タスクに対応するグローバルチェックポイント（ `is_global=1` ）の位置情報を`checkpoint-T` （例： `(mysql-bin.000100, 1234)` ）として記録します。移行タスクに追加するテーブルのフルエクスポート`metedata` （または`Sync`ステージにある別のデータ移行タスクのチェックポイント）の位置情報を`checkpoint-S` （例： `(mysql-bin.000099, 5678)` ）として記録します。以下の手順でテーブルを移行タスクに追加できます。

1.  既存の移行タスクを停止するには、 `stop-task`使用します。追加するテーブルが実行中の別の移行タスクに属している場合は、そのタスクも停止してください。

2.  MySQLクライアントを使用して下流のTiDBデータベースに接続し、既存の移行タスクに対応するチェックポイントテーブルの情報を、 `checkpoint-T`と`checkpoint-S`間の小さい方の値に手動で更新します。この例では`(mysql- bin.000099, 5678)`です。

    -   更新するチェックポイント テーブルは、スキーマ`{dm_meta}`の`{task-name}_syncer_checkpoint`です。

    -   更新するチェックポイント行は`id=(source-id)`と`is_global=1`一致します。

    -   更新するチェックポイント列は`binlog_name`と`binlog_pos`です。

3.  再入実行を確実にするために、タスクの`syncers`に`safe-mode: true`設定します。

4.  `start-task`を使用してタスクを開始します。

5.  `query-status`までタスクの状態を観察します。3 `syncerBinlog` `checkpoint-T`と`checkpoint-S`うち大きい方の値を超えた場合、 `safe-mode`元の値に戻し、タスクを再開します。この例では`(mysql-bin.000100, 1234)`です。

## クエリ<code>packet for query is too large. Try adjusting the &#39;max_allowed_packet&#39; variable</code>いかがでしょうか？ {#how-to-handle-the-error-code-packet-for-query-is-too-large-try-adjusting-the-max-allowed-packet-variable-code-that-occurs-during-the-full-import}

以下のパラメータをデフォルトの 67108864 (64M) より大きい値に設定します。

-   TiDBサーバーのグローバル変数: `max_allowed_packet` 。
-   タスク設定ファイルの設定項目： `target-database.max-allowed-packet` 。詳細は[DM 高度なタスクコンフィグレーションファイル](/dm/task-configuration-file-full.md)を参照してください。

## DM 1.0 クラスターの既存の DM 移行タスクが DM 2.0 以降のクラスターで実行されているときに発生するエラー「 <code>Error 1054: Unknown column &#39;binlog_gtid&#39; in &#39;field list&#39;</code>を処理する方法を教えてください。 {#how-to-handle-the-error-code-error-1054-unknown-column-binlog-gtid-in-field-list-code-that-occurs-when-existing-dm-migration-tasks-of-an-dm-1-0-cluster-are-running-on-a-dm-2-0-or-newer-cluster}

DM v2.0 以降、増分データレプリケーションを続行するために DM 1.0 クラスターのタスク構成ファイルで`start-task`コマンドを直接実行すると、エラー`Error 1054: Unknown column 'binlog_gtid' in 'field list'`が発生します。

このエラーは[DM 1.0 クラスタの DM 移行タスクを DM 2.0 クラスタに手動でインポートする](/dm/manually-upgrade-dm-1.0-to-2.0.md)で処理できます。

## TiUP がDM の一部のバージョン (たとえば、v2.0.0-hotfix) の展開に失敗するのはなぜですか? {#why-does-tiup-fail-to-deploy-some-versions-of-dm-for-example-v2-0-0-hotfix}

`tiup list dm-master`コマンドを使用すると、 TiUP がデプロイをサポートしている DM バージョンを表示できます。このコマンドで表示されない DM バージョンはTiUPでは管理されません。

## DM がデータを複製しているときに発生するエラー<code>parse mydumper metadata error: EOF</code>を処理するにはどうすればよいですか? {#how-to-handle-the-error-code-parse-mydumper-metadata-error-eof-code-that-occurs-when-dm-is-replicating-data}

このエラーをさらに分析するには、エラーメッセージとログファイルを確認してください。原因としては、権限不足のためにダンプユニットが正しいメタデータファイルを生成していないことが考えられます。

## シャード化されたスキーマとテーブルを複製するときに DM が致命的なエラーを報告しないのに、ダウンストリーム データが失われるのはなぜですか? {#why-does-dm-report-no-fatal-error-when-replicating-sharded-schemas-and-tables-but-downstream-data-is-lost}

構成項目`block-allow-list`と`table-route`確認します。

-   `block-allow-list`下にある上流のデータベースとテーブルの名前を設定する必要があります。3 `do-tables`前に「~」を追加すると、正規表現を使用して名前を一致させることができます。
-   `table-route` 、テーブル名の一致に正規表現ではなくワイルドカード文字を使用します。例えば、 `table_parttern_[0-63]` `table_parttern_0`から`table_pattern_6`までの 7 つのテーブルのみに一致します。

## DM がアップストリームからレプリケートしていないのに、 <code>replicate lag</code>モニター メトリックにデータが表示されないのはなぜですか? {#why-does-the-code-replicate-lag-code-monitor-metric-show-no-data-when-dm-is-not-replicating-from-upstream}

DM 1.0では、監視データを生成するために`enable-heartbeat`有効にする必要があります。DM 2.0以降のバージョンでは、この機能はサポートされていないため、監視メトリック`replicate lag`にはデータが存在しないことが想定されます。

## DM がタスクを開始しているときに、 <code>context deadline exceeded</code>を示すエラー メッセージの<code>RawCause</code>で<code>fail to initial unit Sync of subtask</code>エラーを処理する方法を教えてください。 {#how-to-handle-the-error-code-fail-to-initial-unit-sync-of-subtask-code-when-dm-is-starting-a-task-with-the-code-rawcause-code-in-the-error-message-showing-code-context-deadline-exceeded-code}

これはDM 2.0.0バージョンの既知の問題であり、DM 2.0.1バージョンで修正される予定です。レプリケーションタスクで処理するテーブル数が多い場合に発生する可能性があります。TiUPを使用してDMをデプロイしている場合は、DMをナイトリーバージョンにアップグレードすることでこの問題を修正できます。または、GitHubの[DMのリリースページ](https://github.com/pingcap/tiflow/releases)から2.0.0-hotfixバージョンをダウンロードし、実行ファイルを手動で置き換えることもできます。

## DM がデータを複製しているときに<code>duplicate entry</code>エラーを処理するにはどうすればよいでしょうか? {#how-to-handle-the-error-code-duplicate-entry-code-when-dm-is-replicating-data}

まず、以下の点を確認していただく必要があります。

-   レプリケーション タスクで`disable-detect`が構成されていません (v2.0.7 以前のバージョン)。
-   データは手動でも他のレプリケーション プログラムによっても挿入されません。
-   このテーブルに関連付けられた DML フィルターは構成されていません。

トラブルシューティングを容易にするために、まず下流のTiDBインスタンスの一般的なログファイルを収集し、その後[TiDBコミュニティSlackチャンネル](https://tidbcommunity.slack.com/archives/CH7TTLL7P)でテクニカルサポートに問い合わせることができます。次の例は、一般的なログファイルを収集する方法を示しています。

```bash
# Enable general log collection
curl -X POST -d "tidb_general_log=1" http://{TiDBIP}:10080/settings
# Disable general log collection
curl -X POST -d "tidb_general_log=0" http://{TiDBIP}:10080/settings
```

`duplicate entry`エラーが発生した場合は、競合データを含むレコードのログ ファイルを確認する必要があります。

## 一部の監視パネルに<code>No data point</code>と表示されるのはなぜですか? {#why-do-some-monitoring-panels-show-code-no-data-point-code}

一部のパネルにデータが表示されないのは正常です。例えば、エラーが報告されていない場合、DDLロックがない場合、またはリレーログ機能が有効になっていない場合、対応するパネルには`No data point`表示されます。各パネルの詳細については、 [DM モニタリング メトリック](/dm/monitor-a-dm-cluster.md)参照してください。

## DM v1.0 では、タスクにエラーがある場合にコマンド<code>sql-skip</code>一部のステートメントをスキップできないのはなぜですか? {#in-dm-v1-0-why-does-the-command-code-sql-skip-code-fail-to-skip-some-statements-when-the-task-is-in-error}

まず、 `sql-skip`実行した後もbinlogの位置が進んでいるかどうかを確認する必要があります。進んでいる場合は、 `sql-skip`有効になっていることを意味します。このエラーが繰り返し発生する理由は、アップストリームがサポートされていない複数の DDL 文を送信しているためです。5 `sql-skip -s <sql-pattern>`使用して、これらの文に一致するパターンを設定できます。

場合によっては、エラー メッセージに`parse statement`情報が含まれます。次に例を示します。

    if the DDL is not needed, you can use a filter rule with \"*\" schema-pattern to ignore it.\n\t : parse statement: line 1 column 11 near \"EVENT `event_del_big_table` \r\nDISABLE\" %!!(MISSING)(EXTRA string=ALTER EVENT `event_del_big_table` \r\nDISABLE

このタイプのエラーの原因は、TiDBパーサーがアップストリームから送信されたDDL文（例えば`ALTER EVENT` ）を解析できないため、 `sql-skip`期待どおりに機能しないことです。設定ファイルに[binlogイベントフィルター](/dm/dm-binlog-event-filter.md)追加してこれらの文をフィルタリングし、 `schema-pattern: "*"`設定することができます。DM v2.0.1以降、DMは`EVENT`に関連する文を事前にフィルタリングします。

DM v6.0以降、 `sql-skip`と`handle-error` `binlog`に置き換えられました。この問題を回避するには、代わりに`binlog`コマンドを使用してください。

## DM がレプリケートされているときに、ダウンストリームに<code>REPLACE</code>ステートメントが表示され続けるのはなぜですか? {#why-do-code-replace-code-statements-keep-appearing-in-the-downstream-when-dm-is-replicating}

タスクに対して[セーフモード](/dm/dm-glossary.md#safe-mode)自動的に有効になっているかどうかを確認する必要があります。エラー発生後にタスクが自動的に再開される場合、または高可用性スケジュールが設定されている場合は、タスクの開始または再開から1分以内であるため、セーフモードが有効になっています。

DM-worker のログファイルを確認し、 `change count`を含む行を探してください。その行の`new count` 0 でない場合、セーフモードが有効になっています。セーフモードが有効になっている理由を確認するには、セーフモードがいつ発生するか、またそれ以前にエラーが報告されているかどうかを確認してください。

## DM v2.0 では、タスク中に DM が再起動すると、完全インポート タスクが失敗するのはなぜですか? {#in-dm-v2-0-why-does-the-full-import-task-fail-if-dm-restarts-during-the-task}

DM v2.0.1 以前のバージョンでは、完全インポートが完了する前に DM が再起動すると、上流データソースと DM ワーカーノード間のバインディングが変更される可能性があります。例えば、ダンプユニットの中間データが DM ワーカーノード A にあるにもかかわらず、ロードユニットが DM ワーカーノード B で実行されている場合、操作が失敗する可能性があります。

この問題に対する解決策は次の 2 つです。

-   データ量が少ない (1 TB 未満) 場合、またはタスクがシャード化されたテーブルをマージする場合は、次の手順を実行します。

    1.  ダウンストリーム データベースにインポートされたデータをクリーンアップします。
    2.  エクスポートされたデータのディレクトリ内のすべてのファイルを削除します。
    3.  dmctl を使用してタスクを削除し、コマンド`start-task --remove-meta`を実行して新しいタスクを作成します。

    新しいタスクが開始したら、冗長な DM ワーカー ノードが存在しないことを確認し、完全インポート中に DM クラスターの再起動やアップグレードを行わないようにすることをお勧めします。

-   データ量が大きい場合（1 TB を超える場合）は、次の手順を実行します。

    1.  ダウンストリーム データベースにインポートされたデータをクリーンアップします。
    2.  データを処理する DM ワーカーノードに TiDB-Lightningをデプロイ。
    3.  DM ダンプ ユニットがエクスポートするデータをインポートするには、TiDB-Lightning のローカル バックエンド モードを使用します。
    4.  完全なインポートが完了したら、次の方法でタスク構成ファイルを編集し、タスクを再起動します。
        -   `task-mode`を`incremental`に変更します。
        -   ダンプユニットが出力するメタデータファイルに記録されている位置に値`mysql-instance.meta.pos`を設定します。

## 増分タスク中に再起動すると、DM がエラー<code>ERROR 1236 (HY000): The slave is connecting using CHANGE MASTER TO MASTER_AUTO_POSITION = 1, but the master has purged binary logs containing GTIDs that the slave requires.</code>報告するのはなぜですか? {#why-does-dm-report-the-error-code-error-1236-hy000-the-slave-is-connecting-using-change-master-to-master-auto-position-1-but-the-master-has-purged-binary-logs-containing-gtids-that-the-slave-requires-code-if-it-restarts-during-an-incremental-task}

このエラーは、ダンプ ユニットによって出力されたメタデータ ファイルに記録されたアップストリームbinlogの位置が、完全な移行中に消去されたことを示します。

この問題が発生した場合は、タスクを一時停止し、ダウンストリーム データベースに移行されたすべてのデータを削除して、 `--remove-meta`オプションで新しいタスクを開始する必要があります。

次の方法で設定することで、この問題を事前に回避できます。

1.  移行タスクが完了する前に必要なbinlogファイルが誤って削除されるのを防ぐため、上流のMySQLデータベースの値を`expire_logs_days`増やしてください。データ量が多い場合は、タスクを高速化するために、dumplingとTiDB-Lightningを同時に使用することをお勧めします。
2.  このタスクのリレー ログ機能を有効にすると、binlogの位置が消去されていても DM がリレー ログからデータを読み取ることができます。

## クラスターがTiUP v1.3.0 または v1.3.1 を使用してデプロイされている場合、DM クラスターの Grafana ダッシュボードに<code>failed to fetch dashboard</code>表示されるのはなぜですか? {#why-does-the-grafana-dashboard-of-a-dm-cluster-display-code-failed-to-fetch-dashboard-code-if-the-cluster-is-deployed-using-tiup-v1-3-0-or-v1-3-1}

これはTiUPの既知のバグで、 TiUP v1.3.2で修正されています。この問題の解決策は以下の2つです。

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

これはDMの既知のバグで、DM v2.0.2で修正されています。このバグは、以下の2つの条件が同時に満たされた場合に発生します。

1.  ソース構成ファイルでは、パラメータ`enable-relay`と`enable-gtid` `true`に設定されています。
2.  アップストリームデータベースは**MySQLのセカンダリデータベース**です。コマンド`show binlog events in '<newest-binlog>' limit 2`を実行してデータベースの`previous_gtids`クエリすると、次の例のように結果が不連続になります。

<!---->

    mysql> show binlog events in 'mysql-bin.000005' limit 2;
    +------------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+
    | Log_name         | Pos  | Event_type     | Server_id | End_log_pos | Info                                                               |
    +------------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+
    | mysql-bin.000005 |    4 | Format_desc    |    123452 |         123 | Server ver: 5.7.32-35-log, Binlog ver: 4                           |
    | mysql-bin.000005 |  123 | Previous_gtids |    123452 |         194 | d3618e68-6052-11eb-a68b-0242ac110002:6-7                           |
    +------------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+

このバグは、dmctlで`query-status <task>`実行してタスク情報を照会した際に、 `subTaskStatus.sync.syncerBinlogGtid`連続していないのに`subTaskStatus.sync.masterBinlogGtid`が連続していることがわかった場合に発生します。次の例をご覧ください。

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

この例では、データソース`mysql1`の`syncerBinlogGtid`不連続です。この場合、データ損失に対処するには、次のいずれかの方法を実行できます。

-   現在の時刻から完全エクスポート タスクのメタデータに記録された位置までのアップストリーム バイナリ ログが消去されていない場合は、次の手順を実行できます。
    1.  現在のタスクを停止し、連続しない GTID を持つすべてのデータ ソースを削除します。
    2.  すべてのソース構成ファイルで`enable-relay` ～ `false`設定します。
    3.  連続しない GTID を持つデータ ソース (上記の例の`mysql1`など) の場合は、タスクを増分タスクに変更し、 `binlog-name` 、 `binlog-pos` 、および`binlog-gtid`情報を含む各完全エクスポート タスクのメタデータ情報を使用して関連する`mysql-instances.meta`構成します。
    4.  増分タスクの`task.yaml`に`syncers.safe-mode`を`true`に設定し、タスクを再開します。
    5.  増分タスクがすべての欠落データをダウンストリームに複製した後、タスクを停止し、 `task.yaml`の`safe-mode`を`false`変更します。
    6.  タスクを再度開始します。
-   アップストリームのバイナリログが消去されたが、ローカルリレーログが残っている場合は、次の手順を実行できます。
    1.  現在のタスクを停止します。
    2.  連続しない GTID を持つデータ ソース (上記の例の`mysql1`など) の場合は、タスクを増分タスクに変更し、 `binlog-name` 、 `binlog-pos` 、および`binlog-gtid`情報を含む各完全エクスポート タスクのメタデータ情報を使用して関連する`mysql-instances.meta`構成します。
    3.  増分タスクの`task.yaml`で、前の値`binlog-gtid`を前の値`previous_gtids`に変更します。上記の例では、 `1-y`を`6-y`に変更します。
    4.  `task.yaml`の`syncers.safe-mode`を`true`に設定してタスクを再開します。
    5.  増分タスクがすべての欠落データをダウンストリームに複製した後、タスクを停止し、 `task.yaml`の`safe-mode`を`false`変更します。
    6.  タスクを再度開始します。
    7.  データ ソースを再起動し、ソース構成ファイルで`enable-relay`または`enable-gtid`を`false`に設定します。
-   上記の条件がいずれも満たされていない場合、またはタスクのデータ量が少ない場合は、次の手順を実行できます。
    1.  ダウンストリーム データベースにインポートされたデータをクリーンアップします。
    2.  データ ソースを再起動し、ソース構成ファイルで`enable-relay`または`enable-gtid`を`false`に設定します。
    3.  新しいタスクを作成し、コマンド`start-task task.yaml --remove-meta`を実行して、データを最初から再度移行します。

上記の 1 番目と 2 番目のソリューションで正常にレプリケートできるデータ ソース (上記の例の`mysql2`など) の場合は、増分タスクを設定するときに、 `subTaskStatus.sync`の`syncerBinlog`と`syncerBinlogGtid`情報を使用して関連する`mysql-instances.meta`構成します。

## DM v2.0 では、 <code>heartbeat</code>機能が有効になっている仮想 IP 環境で DM ワーカーと MySQL インスタンス間の接続を切り替えるときに、「ハートビート構成が以前に使用したものと異なります: serverID が等しくありません」というエラーをどのように処理すればよいですか? {#in-dm-v2-0-how-do-i-handle-the-error-heartbeat-config-is-different-from-previous-used-serverid-not-equal-when-switching-the-connection-between-dm-workers-and-mysql-instances-in-a-virtual-ip-environment-with-the-code-heartbeat-code-feature-enabled}

DM v2.0以降のバージョンでは、 `heartbeat`機能はデフォルトで無効になっています。タスク設定ファイルでこの機能を有効にすると、高可用性機能に干渉します。この問題を解決するには、タスク設定ファイルで`enable-heartbeat`を`false`に設定して`heartbeat`機能を無効にし、その後タスク設定ファイルをリロードしてください。DMは、以降のリリースで`heartbeat`機能を強制的に無効にします。

## DM マスターが再起動後にクラスターに参加できず、DM が「埋め込み etcd の開始に失敗しました。RawCause: メンバー xxx はすでにブートストラップされています」というエラーを報告するのはなぜですか? {#why-does-a-dm-master-fail-to-join-the-cluster-after-it-restarts-and-dm-reports-the-error-fail-to-start-embed-etcd-rawcause-member-xxx-has-already-been-bootstrapped}

DMマスターが起動すると、DMはetcd情報を現在のディレクトリに記録します。DMマスターの再起動後にディレクトリが変更されると、DMはetcd情報にアクセスできず、再起動に失敗します。

この問題を解決するには、 TiUPを使用して DM クラスターをメンテナンスすることをお勧めします。バイナリファイルを使用してデプロイする必要がある場合は、DM マスターの設定ファイルに絶対パスで`data-dir`設定するか、コマンドを実行する現在のディレクトリに注意してください。

## dmctl を使用してコマンドを実行すると、DM マスターに接続できないのはなぜですか? {#why-dm-master-cannot-be-connected-when-i-use-dmctl-to-execute-commands}

dmctl execute コマンドを使用すると、DMマスターへの接続に失敗し（コマンドでパラメータ値`--master-addr`指定している場合でも）、エラーメッセージ`RawCause: context deadline exceeded, Workaround: please check your network connection.`表示される場合があります。ただし、コマンド`telnet <master-addr>`などを使用してネットワーク接続を確認すると、例外は見つかりません。

この場合、環境変数`https_proxy` （ **https** ）を確認してください。この変数が設定されている場合、dmctl は`https_proxy`で指定されたホストとポートに自動的に接続します。ホストに対応する`proxy`転送サービスがない場合、接続は失敗します。

この問題を解決するには、 `https_proxy`が必須かどうかを確認してください。必須でない場合は設定を解除してください。必須でない場合は、元のdmctlコマンドの前に環境変数設定`https_proxy="" ./dmctl --master-addr "x.x.x.x:8261"`追加してください。

> **注記：**
>
> `proxy`に関連する環境変数には`http_proxy` 、 `https_proxy` 、 `no_proxy`があります。上記の手順を実行しても接続エラーが解決しない場合は、 `http_proxy`と`no_proxy`の設定パラメータが正しいかどうかを確認してください。

## DM バージョン 2.0.2 から 2.0.6 で start-relay コマンドを実行したときに返されるエラーを処理するにはどうすればよいですか? {#how-to-handle-the-returned-error-when-executing-start-relay-command-for-dm-versions-from-2-0-2-to-2-0-6}

    flush local meta, Rawcause: open relay-dir/xxx.000001/relay.metayyyy: no such file or directory

上記のエラーは次のような場合に発生する可能性があります。

-   DM は v2.0.1 以前から v2.0.2 - v2.0.6 にアップグレードされており、アップグレード前にリレー ログが開始され、アップグレード後に再起動されます。
-   stop-relay コマンドを実行してリレー ログを一時停止してから再開します。

次のオプションによりこのエラーを回避できます。

-   リレーログを再起動:

        » stop-relay -s sourceID workerName
        » start-relay -s sourceID workerName

-   DM を v2.0.7 以降のバージョンにアップグレードします。

## ロード ユニットが<code>Unknown character set</code>エラーを報告するのはなぜですか? {#why-does-the-load-unit-report-the-code-unknown-character-set-code-error}

TiDBはMySQLのすべての文字セットをサポートしていません。そのため、フルインポート中にテーブルスキーマを作成する際にサポートされていない文字セットが使用されると、DMはこのエラーを報告します。このエラーを回避するには、特定のデータに応じて、 [TiDBでサポートされている文字セット](/character-set-and-collation.md)使用して下流で事前にテーブルスキーマを作成してください。
