---
title: TiDB Data Migration FAQs
summary: Learn about frequently asked questions (FAQs) about TiDB Data Migration (DM).
---

# TiDB データ移行に関するよくある質問 {#tidb-data-migration-faqs}

このドキュメントでは、TiDB データ移行 (DM) に関するよくある質問 (FAQ) をまとめています。

## DM は、Alibaba RDS または他のクラウド データベースからのデータの移行をサポートしていますか? {#does-dm-support-migrating-data-from-alibaba-rds-or-other-cloud-databases}

現在、DM は MySQL または MariaDB binlogの標準バージョンのデコードのみをサポートしています。 Alibaba Cloud RDS またはその他のクラウド データベースではテストされていません。binlogが標準形式であることが確認された場合、サポートされています。

Alibaba Cloud RDS でプライマリ キーを持たないアップストリーム テーブルの場合、binlogには非表示のプライマリ キー列が含まれており、元のテーブル構造と矛盾するという既知の問題があります。

互換性のない既知の問題は次のとおりです。

-   **Alibaba Cloud RDS**では、主キーのないアップストリーム テーブルのbinlogには、元のテーブル構造と矛盾する非表示の主キー列が含まれています。
-   **HUAWEI Cloud RDS**では、 binlogファイルの直接読み取りはサポートされていません。詳細については、 [HUAWEI Cloud RDS はBinlogバックアップ ファイルを直接読み取ることができますか?](https://support.huaweicloud.com/en-us/rds_faq/rds_faq_0210.html)参照してください。

## タスク構成のブロック リストと許可リストの正規表現は<code>non-capturing (?!)</code>をサポートしていますか? {#does-the-regular-expression-of-the-block-and-allow-list-in-the-task-configuration-support-code-non-capturing-code}

現在、DM はそれをサポートしておらず、 Golang標準ライブラリの正規表現のみをサポートしています。 [re2-syntax](https://github.com/google/re2/wiki/Syntax)経由でGolangがサポートする正規表現を参照してください。

## アップストリームで実行されるステートメントに複数の DDL 操作が含まれる場合、DM はそのような移行をサポートしますか? {#if-a-statement-executed-upstream-contains-multiple-ddl-operations-does-dm-support-such-migration}

DM は、複数の DDL 変更操作を含む 1 つのステートメントを、1 つの DDL 操作のみを含む複数のステートメントに分割しようとしますが、すべてのケースをカバーできるわけではありません。アップストリームで実行されるステートメントに DDL 操作を 1 つだけ含めるか、テスト環境で検証することをお勧めします。サポートされていない場合は、DM リポジトリに[問題](https://github.com/pingcap/dm/issues)を提出できます。

## 互換性のない DDL ステートメントを処理する方法は? {#how-to-handle-incompatible-ddl-statements}

TiDB でサポートされていない DDL ステートメントに遭遇した場合は、dmctl を使用して手動で処理する必要があります (DDL ステートメントをスキップするか、DDL ステートメントを指定された DDL ステートメントに置き換えます)。詳細については、 [失敗した DDL ステートメントを処理する](/dm/handle-failed-ddl-statements.md)を参照してください。

> **ノート：**
>
> 現在、TiDB は、MySQL がサポートするすべての DDL ステートメントと互換性があるわけではありません。 [MySQL の互換性](/mysql-compatibility.md#ddl)を参照してください。

## DM はビュー関連の DDL ステートメントと DML ステートメントを TiDB に複製しますか? {#does-dm-replicate-view-related-ddl-statements-and-dml-statements-to-tidb}

現在、DM はビュー関連の DDL ステートメントを下流の TiDB クラスターに複製することも、ビュー関連の DML ステートメントを下流の TiDB クラスターに複製することもありません。

## データ移行タスクをリセットする方法は? {#how-to-reset-the-data-migration-task}

データ移行中に例外が発生し、データ移行タスクを再開できない場合は、タスクをリセットしてデータを再移行する必要があります。

1.  `stop-task`コマンドを実行して、異常なデータ移行タスクを停止します。

2.  ダウンストリームに移行されたデータをパージします。

3.  次のいずれかの方法を使用して、データ移行タスクを再開します。

    -   タスク構成ファイルで新しいタスク名を指定します。次に`start-task {task-config-file}`を実行します。
    -   `start-task --remove-meta {task-config-file}`を実行します。

## <code>online-ddl-scheme: &quot;gh-ost&quot;</code>設定された後、gh-ost テーブルに関連する DDL 操作によって返されるエラーを処理する方法は? {#how-to-handle-the-error-returned-by-the-ddl-operation-related-to-the-gh-ost-table-after-code-online-ddl-scheme-gh-ost-code-is-set}

```
[unit=Sync] ["error information"="{\"msg\":\"[code=36046:class=sync-unit:scope=internal:level=high] online ddls on ghost table `xxx`.`_xxxx_gho`\\ngithub.com/pingcap/dm/pkg/terror.(*Error).Generate ......
```

上記のエラーは、次の理由で発生する可能性があります。

最後の`rename ghost_table to origin table`ステップで、DM はメモリ内の DDL 情報を読み取り、元のテーブルの DDL に復元します。

ただし、メモリ内の DDL 情報は、次の 2 つの方法のいずれかで取得されます。

-   DM [`alter ghost_table`操作中に gh-ost テーブルを処理します](/dm/feature-online-ddl.md#online-schema-change-gh-ost)および`ghost_table`の DDL 情報を記録します。
-   DM-worker を再起動してタスクを開始すると、DM は DDL を`dm_meta.{task_name}_onlineddl`から読み取ります。

したがって、増分レプリケーションのプロセスで、指定された Pos が`alter ghost_table` DDL をスキップしたが、Pos がまだ gh-ost の online-ddl プロセスにある場合、ghost_table はメモリまたは`dm_meta.{task_name}_onlineddl`に正しく書き込まれません。このような場合、上記のエラーが返されます。

このエラーは、次の手順で回避できます。

1.  タスクの`online-ddl-scheme`構成を削除します。

2.  `block-allow-list.ignore-tables`で`_{table_name}_gho` 、および`_{table_name}_del`を設定`_{table_name}_ghc`ます。

3.  ダウンストリーム TiDB でアップストリーム DDL を手動で実行します。

4.  Pos が gh-ost プロセス後の位置に複製されたら、 `online-ddl-scheme`を再度有効にして`block-allow-list.ignore-tables`コメントアウトします。

## 既存のデータ移行タスクにテーブルを追加する方法は? {#how-to-add-tables-to-the-existing-data-migration-tasks}

実行中のデータ移行タスクにテーブルを追加する必要がある場合は、タスクの段階に応じて次の方法で対処できます。

> **ノート：**
>
> 既存のデータ移行タスクへのテーブルの追加は複雑であるため、この操作は必要な場合にのみ実行することをお勧めします。

### <code>Dump</code>段階で {#in-the-code-dump-code-stage}

MySQL はエクスポート用のスナップショットを指定できないため、エクスポート中にデータ移行タスクを更新し、チェックポイントを介してエクスポートを再開するために再起動することはサポートされていません。したがって、 `Dump`段階で移行する必要があるテーブルを動的に追加することはできません。

移行のためにテーブルを追加する必要がある場合は、新しい構成ファイルを使用して直接タスクを再開することをお勧めします。

### <code>Load</code>段階で {#in-the-code-load-code-stage}

エクスポート中、複数のデータ移行タスクは通常、binlogの位置が異なります。 `Load`段階でタスクをマージすると、binlogの位置について合意に達することができない場合があります。したがって、第`Load`段階でテーブルをデータ移行タスクに追加することはお勧めしません。

### <code>Sync</code>段階で {#in-the-code-sync-code-stage}

データ移行タスクが`Sync`段階の場合、構成ファイルにテーブルを追加してタスクを再開すると、DM は新しく追加されたテーブルに対して完全なエクスポートとインポートを再実行しません。代わりに、DM は前のチェックポイントから増分レプリケーションを続行します。

したがって、新しく追加されたテーブルの完全なデータがダウンストリームにインポートされていない場合は、別のデータ移行タスクを使用して、完全なデータをエクスポートしてダウンストリームにインポートする必要があります。

既存の移行タスクに対応するグローバル チェックポイント ( `is_global=1` ) の位置情報を`checkpoint-T` `(mysql-bin.000100, 1234)`など) に記録します。 `(mysql-bin.000099, 5678)`のように`checkpoint-S`として移行タスクに追加するテーブルのフル エクスポート`metedata` (または`Sync`段階の別のデータ移行タスクのチェックポイント) の位置情報を記録します。次の手順でテーブルを移行タスクに追加できます。

1.  `stop-task`を使用して、既存の移行タスクを停止します。追加するテーブルが実行中の別の移行タスクに属している場合は、そのタスクも停止します。

2.  MySQL クライアントを使用してダウンストリームの TiDB データベースに接続し、既存の移行タスクに対応するチェックポイント テーブルの情報を`checkpoint-T` ～ `checkpoint-S`の小さい値に手動で更新します。この例では、 `(mysql- bin.000099, 5678)`です。

    -   更新するチェックポイント テーブルは、スキーマ`{dm_meta}`の`{task-name}_syncer_checkpoint`です。

    -   更新されるチェックポイント行は`id=(source-id)`と`is_global=1`に一致します。

    -   更新するチェックポイント列は`binlog_name`と`binlog_pos`です。

3.  タスクの`syncers`に`safe-mode: true`を設定して、再入可能実行を保証します。

4.  `start-task`を使用してタスクを開始します。

5.  `query-status`からタスクのステータスを観察します。 `syncerBinlog`が`checkpoint-T`と`checkpoint-S`の大きい方の値を超えたら、 `safe-mode`元の値に戻してタスクを再開します。この例では、 `(mysql-bin.000100, 1234)`です。

## <code>packet for query is too large. Try adjusting the &#39;max_allowed_packet&#39; variable</code>フル インポート中に発生する<code>packet for query is too large. Try adjusting the &#39;max_allowed_packet&#39; variable</code> 。 {#how-to-handle-the-error-code-packet-for-query-is-too-large-try-adjusting-the-max-allowed-packet-variable-code-that-occurs-during-the-full-import}

以下のパラメーターをデフォルトの 67108864 (64M) より大きい値に設定します。

-   TiDBサーバーのグローバル変数: `max_allowed_packet` 。
-   タスク構成ファイル内の構成項目: `target-database.max-allowed-packet` .詳細は[DM 拡張タスクコンフィグレーションファイル](/dm/task-configuration-file-full.md)を参照してください。

## DM 1.0 クラスターの既存の DM 移行タスクが DM 2.0 以降のクラスターで実行されているときに発生するエラー<code>Error 1054: Unknown column &#39;binlog_gtid&#39; in &#39;field list&#39;</code>処理方法を教えてください。 {#how-to-handle-the-error-code-error-1054-unknown-column-binlog-gtid-in-field-list-code-that-occurs-when-existing-dm-migration-tasks-of-an-dm-1-0-cluster-are-running-on-a-dm-2-0-or-newer-cluster}

DM v2.0 以降、DM 1.0 クラスターのタスク構成ファイルで`start-task`コマンドを直接実行して増分データ レプリケーションを続行すると、エラー`Error 1054: Unknown column 'binlog_gtid' in 'field list'`が発生します。

このエラーは[DM 1.0 クラスターの DM 移行タスクを DM 2.0 クラスターに手動でインポートする](/dm/manually-upgrade-dm-1.0-to-2.0.md)で処理できます。

## TiUP がDM の一部のバージョン (v2.0.0-hotfix など) の展開に失敗するのはなぜですか? {#why-does-tiup-fail-to-deploy-some-versions-of-dm-for-example-v2-0-0-hotfix}

`tiup list dm-master`コマンドを使用して、 TiUPがデプロイをサポートしている DM のバージョンを表示できます。 TiUP は、このコマンドで表示されない DM バージョンを管理しません。

## エラー<code>parse mydumper metadata error: EOF</code> ? {#how-to-handle-the-error-code-parse-mydumper-metadata-error-eof-code-that-occurs-when-dm-is-replicating-data}

このエラーをさらに分析するには、エラー メッセージとログ ファイルを確認する必要があります。原因として、権限がないためにダンプ ユニットが正しいメタデータ ファイルを生成しないことが考えられます。

## シャードされたスキーマとテーブルをレプリケートするときに DM が致命的なエラーを報告しないのに、ダウンストリーム データが失われるのはなぜですか? {#why-does-dm-report-no-fatal-error-when-replicating-sharded-schemas-and-tables-but-downstream-data-is-lost}

構成項目`block-allow-list`と`table-route`を確認します。

-   アップストリームのデータベースとテーブルの名前を`block-allow-list`の下に構成する必要があります。 `do-tables`の前に「~」を追加すると、正規表現を使用して名前を一致させることができます。
-   `table-route`正規表現の代わりにワイルドカード文字を使用してテーブル名を照合します。たとえば、 `table_parttern_[0-63]` `table_parttern_0`から`table_pattern_6`までの 7 つのテーブルにのみ一致します。

## DM がアップストリームからレプリケートしていない場合、 <code>replicate lag</code>モニター メトリックにデータが表示されないのはなぜですか? {#why-does-the-code-replicate-lag-code-monitor-metric-show-no-data-when-dm-is-not-replicating-from-upstream}

DM 1.0 では、モニター データを生成するには`enable-heartbeat`を有効にする必要があります。 DM 2.0 以降のバージョンでは、この機能がサポートされていないため、モニター メトリック`replicate lag`にデータがないと予想されます。

## DM がタスクを開始しているときに<code>fail to initial unit Sync of subtask</code> 、エラー メッセージの<code>RawCause</code>が<code>context deadline exceeded</code>示すエラーを処理する方法は? {#how-to-handle-the-error-code-fail-to-initial-unit-sync-of-subtask-code-when-dm-is-starting-a-task-with-the-code-rawcause-code-in-the-error-message-showing-code-context-deadline-exceeded-code}

これは DM 2.0.0 バージョンの既知の問題であり、DM 2.0.1 バージョンで修正される予定です。レプリケーション タスクで処理するテーブルが多数ある場合にトリガーされる可能性があります。 TiUP を使用して DM をデプロイする場合は、DM をナイトリー バージョンにアップグレードして、この問題を解決できます。または、GitHub の[DMのリリースページ](https://github.com/pingcap/tiflow/releases)から 2.0.0-hotfix バージョンをダウンロードして、実行可能ファイルを手動で置き換えることができます。

## DM がデータをレプリケートしているときにエラー<code>duplicate entry</code>を処理する方法は? {#how-to-handle-the-error-code-duplicate-entry-code-when-dm-is-replicating-data}

まず、次のことを確認して確認する必要があります。

-   `disable-detect`はレプリケーション タスクで構成されていません (v2.0.7 以前のバージョン)。
-   データは、手動または他の複製プログラムによって挿入されません。
-   このテーブルに関連付けられた DML フィルタは構成されていません。

トラブルシューティングを容易にするために、まず下流の TiDB インスタンスの一般的なログ ファイルを収集してから、 [TiDB コミュニティ slack チャンネル](https://tidbcommunity.slack.com/archives/CH7TTLL7P)でテクニカル サポートを依頼できます。次の例は、一般的なログ ファイルを収集する方法を示しています。

```bash
# Enable general log collection
curl -X POST -d "tidb_general_log=1" http://{TiDBIP}:10080/settings
# Disable general log collection
curl -X POST -d "tidb_general_log=0" http://{TiDBIP}:10080/settings
```

`duplicate entry`のエラーが発生した場合は、競合データを含むレコードのログ ファイルを確認する必要があります。

## 一部の監視パネルに<code>No data point</code>が表示されるのはなぜですか? {#why-do-some-monitoring-panels-show-code-no-data-point-code}

一部のパネルにデータがないのは正常です。たとえば、エラーが報告されていない場合、DDL ロックがない場合、またはリレー ログ機能が有効になっていない場合、対応するパネルには`No data point`が表示されます。各パネルの詳細な説明については、 [DM モニタリング指標](/dm/monitor-a-dm-cluster.md)を参照してください。

## DM v1.0 で、タスクにエラーがある場合、コマンド<code>sql-skip</code>一部のステートメントをスキップできないのはなぜですか? {#in-dm-v1-0-why-does-the-command-code-sql-skip-code-fail-to-skip-some-statements-when-the-task-is-in-error}

`sql-skip`を実行した後、binlogの位置がまだ進んでいるかどうかを最初に確認する必要があります。もしそうなら、それは`sql-skip`発効したことを意味します。このエラーが発生し続ける理由は、アップストリームが複数のサポートされていない DDL ステートメントを送信するためです。 `sql-skip -s <sql-pattern>`を使用して、これらのステートメントに一致するパターンを設定できます。

場合によっては、エラー メッセージに次のような`parse statement`情報が含まれることがあります。

```
if the DDL is not needed, you can use a filter rule with \"*\" schema-pattern to ignore it.\n\t : parse statement: line 1 column 11 near \"EVENT `event_del_big_table` \r\nDISABLE\" %!!(MISSING)(EXTRA string=ALTER EVENT `event_del_big_table` \r\nDISABLE
```

このタイプのエラーの理由は、TiDB パーサーがアップストリームから送信された DDL ステートメント ( `ALTER EVENT`など) を解析できないため、 `sql-skip`期待どおりに機能しないためです。構成ファイルに[binlogイベント フィルタ](/dm/dm-binlog-event-filter.md)を追加して、これらのステートメントをフィルタリングし、 `schema-pattern: "*"`を設定できます。 DM v2.0.1 以降、DM は`EVENT`に関連するステートメントを事前にフィルター処理します。

DM v6.0 以降、 `binlog` `sql-skip`と`handle-error`を置き換えます。この問題を回避するには、代わりに`binlog`コマンドを使用できます。

## DM がレプリケートしているときに、 <code>REPLACE</code>ステートメントがダウンストリームに表示され続けるのはなぜですか? {#why-do-code-replace-code-statements-keep-appearing-in-the-downstream-when-dm-is-replicating}

タスクに対して[セーフモード](/dm/dm-glossary.md#safe-mode)が自動的に有効になっているかどうかを確認する必要があります。エラー後にタスクが自動的に再開される場合、または高可用性スケジュールが設定されている場合は、タスクの開始または再開後 1 分以内であるため、セーフ モードが有効になります。

DM-worker ログ ファイルを確認して、 `change count`を含む行を検索できます。行の`new count`ゼロでない場合、セーフ モードが有効になっています。有効になっている理由を確認するには、いつ発生するか、以前にエラーが報告されていないかどうかを確認してください。

## DM v2.0 で、タスク中に DM が再起動すると、完全インポート タスクが失敗するのはなぜですか? {#in-dm-v2-0-why-does-the-full-import-task-fail-if-dm-restarts-during-the-task}

DM v2.0.1 以前のバージョンでは、フル インポートが完了する前に DM が再起動すると、アップストリーム データ ソースと DM-worker ノード間のバインディングが変更される可能性があります。たとえば、ダンプ ユニットの中間データは DM-worker ノード A にありますが、ロード ユニットは DM-worker ノード B によって実行され、操作が失敗する可能性があります。

この問題の解決策は次の 2 つです。

-   データ ボリュームが小さい (1 TB 未満) か、タスクがシャード テーブルをマージする場合は、次の手順を実行します。

    1.  ダウンストリーム データベースでインポートされたデータをクリーンアップします。
    2.  エクスポートされたデータのディレクトリ内のすべてのファイルを削除します。
    3.  dmctl を使用してタスクを削除し、コマンド`start-task --remove-meta`を実行して新しいタスクを作成します。

    新しいタスクが開始されたら、冗長な DM ワーカー ノードがないことを確認し、フル インポート中に DM クラスターを再起動またはアップグレードしないようにすることをお勧めします。

-   データ ボリュームが大きい (1 TB を超える) 場合は、次の手順を実行します。

    1.  ダウンストリーム データベースでインポートされたデータをクリーンアップします。
    2.  データを処理する DM ワーカー ノードに TiDB-Lightningをデプロイ。
    3.  DM ダンプ ユニットがエクスポートするデータをインポートするには、TiDB-Lightning のローカル バックエンド モードを使用します。
    4.  フル インポートが完了したら、次の方法でタスク構成ファイルを編集し、タスクを再起動します。
        -   `task-mode`を`incremental`に変更します。
        -   ダンプ ユニットが出力するメタデータ ファイルに記録されている位置に値`mysql-instance.meta.pos`を設定します。

## DM <code>ERROR 1236 (HY000): The slave is connecting using CHANGE MASTER TO MASTER_AUTO_POSITION = 1, but the master has purged binary logs containing GTIDs that the slave requires.</code>増分タスク中に再起動する場合は? {#why-does-dm-report-the-error-code-error-1236-hy000-the-slave-is-connecting-using-change-master-to-master-auto-position-1-but-the-master-has-purged-binary-logs-containing-gtids-that-the-slave-requires-code-if-it-restarts-during-an-incremental-task}

このエラーは、ダンプ ユニットによって出力されたメタデータ ファイルに記録された上流のbinlogの位置が、完全な移行中に削除されたことを示します。

この問題が発生した場合は、タスクを一時停止し、ダウンストリーム データベース内のすべての移行済みデータを削除して、オプション`--remove-meta`で新しいタスクを開始する必要があります。

次の方法で構成することにより、この問題を事前に回避できます。

1.  アップストリームの MySQL データベースの値を`expire_logs_days`増やして、完全な移行タスクが完了する前に必要なbinlogファイルを誤って削除しないようにします。データ量が多い場合は、dumpling と TiDB-Lightning を同時に使用してタスクを高速化することをお勧めします。
2.  このタスクのリレー ログ機能を有効にして、 binlog の位置が削除されても DM がリレー ログからデータを読み取れるようにします。

## クラスターがTiUP v1.3.0 または v1.3.1 を使用してデプロイされている場合、DM クラスター表示の Grafana ダッシュボード<code>failed to fetch dashboard</code>なぜですか? {#why-does-the-grafana-dashboard-of-a-dm-cluster-display-code-failed-to-fetch-dashboard-code-if-the-cluster-is-deployed-using-tiup-v1-3-0-or-v1-3-1}

これはTiUPの既知のバグで、 TiUP v1.3.2 で修正されています。この問題の解決策は次の 2 つです。

-   解決策 1:
    1.  コマンド`tiup update --self && tiup update dm`を使用して、 TiUP を新しいバージョンにアップグレードします。
    2.  クラスター内の Grafana ノードをスケールインからスケール アウトし、Grafana サービスを再起動します。
-   解決策 2:
    1.  `deploy/grafana-$port/bin/public`フォルダをバックアップします。
    2.  [TiUP DMオフライン パッケージ](https://download.pingcap.org/tidb-dm-v2.0.1-linux-amd64.tar.gz)をダウンロードして解凍します。
    3.  オフライン パッケージの`grafana-v4.0.3-**.tar.gz`を解凍します。
    4.  フォルダ`deploy/grafana-$port/bin/public` `grafana-v4.0.3-**.tar.gz`の`public`フォルダに置き換えます。
    5.  `tiup dm restart $cluster_name -R grafana`を実行して Grafana サービスを再起動します。

## DM v2.0 で、コマンド<code>query-status</code>のクエリ結果が、タスクで<code>enable-relay</code>と<code>enable-gtid</code>が同時に有効になっている場合、Syncer チェックポイント GTID が不連続であることを示すのはなぜですか? {#in-dm-v2-0-why-does-the-query-result-of-the-command-code-query-status-code-show-that-the-syncer-checkpoint-gtids-are-inconsecutive-if-the-task-has-code-enable-relay-code-and-code-enable-gtid-code-enabled-at-the-same-time}

これは DM の既知のバグで、DM v2.0.2 で修正されています。このバグは、次の 2 つの条件が同時に完全に満たされた場合に発生します。

1.  パラメータ`enable-relay`と`enable-gtid`は、ソース構成ファイルで`true`に設定されています。
2.  アップストリーム データベースは**MySQL セカンダリ データベース**です。コマンド`show binlog events in '<newest-binlog>' limit 2`を実行してデータベースの`previous_gtids`を照会すると、次の例のように結果が不連続になります。

```
mysql> show binlog events in 'mysql-bin.000005' limit 2;
+------------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+
| Log_name         | Pos  | Event_type     | Server_id | End_log_pos | Info                                                               |
+------------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+
| mysql-bin.000005 |    4 | Format_desc    |    123452 |         123 | Server ver: 5.7.32-35-log, Binlog ver: 4                           |
| mysql-bin.000005 |  123 | Previous_gtids |    123452 |         194 | d3618e68-6052-11eb-a68b-0242ac110002:6-7                           |
+------------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+
```

このバグは、dmctl で`query-status <task>`実行してタスク情報を照会し、 `subTaskStatus.sync.syncerBinlogGtid`は不連続であるが`subTaskStatus.sync.masterBinlogGtid`は連続していることが判明した場合に発生します。次の例を参照してください。

```
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
```

この例では、データ ソース`mysql1`の`syncerBinlogGtid`連続していません。この場合、次のいずれかを実行してデータ損失を処理できます。

-   現時点からフル エクスポート タスクのメタデータに記録された位置までのアップストリーム バイナリログがパージされていない場合は、次の手順を実行できます。
    1.  現在のタスクを停止し、連続していない GTID を持つすべてのデータ ソースを削除します。
    2.  すべてのソース構成ファイルで`enable-relay` ～ `false`を設定します。
    3.  連続していない GTID (上記の例の`mysql1`など) を持つデータ ソースの場合、タスクを増分タスクに変更し、関連する`mysql-instances.meta`を、 `binlog-name` 、 `binlog-pos` 、および`binlog-gtid`の情報を含む各フル エクスポート タスクのメタデータ情報で構成します。
    4.  増分タスクの`task.yaml`で`syncers.safe-mode` ～ `true`を設定し、タスクを再起動します。
    5.  増分タスクが不足しているすべてのデータをダウンストリームに複製したら、タスクを停止し、 `task.yaml`の`safe-mode`を`false`に変更します。
    6.  タスクを再始動してください。
-   アップストリーム バイナリログが削除されたが、ローカル リレー ログが残っている場合は、次の手順を実行できます。
    1.  現在のタスクを停止します。
    2.  連続していない GTID (上記の例の`mysql1`など) を持つデータ ソースの場合、タスクを増分タスクに変更し、関連する`mysql-instances.meta`を、 `binlog-name` 、 `binlog-pos` 、および`binlog-gtid`の情報を含む各フル エクスポート タスクのメタデータ情報で構成します。
    3.  増分タスクの`task.yaml`で、前の値`binlog-gtid`を前の値`previous_gtids`に変更します。上記の例では、 `1-y`を`6-y`に変更します。
    4.  `task.yaml`に`syncers.safe-mode` ～ `true`を設定し、タスクを再起動します。
    5.  増分タスクが不足しているすべてのデータをダウンストリームに複製したら、タスクを停止し、 `task.yaml`の`safe-mode`を`false`に変更します。
    6.  タスクを再始動してください。
    7.  データ ソースを再起動し、ソース構成ファイルで`enable-relay`または`enable-gtid` ～ `false`を設定します。
-   上記の条件のいずれも満たされていない場合、またはタスクのデータ量が少ない場合は、次の手順を実行できます。
    1.  ダウンストリーム データベースでインポートされたデータをクリーンアップします。
    2.  データ ソースを再起動し、ソース構成ファイルで`enable-relay`または`enable-gtid` ～ `false`を設定します。
    3.  新しいタスクを作成し、コマンド`start-task task.yaml --remove-meta`を実行して、最初からデータを移行します。

上記の 1 番目と 2 番目のソリューションで正常に複製できるデータ ソース (上記の例の`mysql2`など) については、増分タスクを設定するときに、関連する`mysql-instances.meta` `subTaskStatus.sync`の`syncerBinlog`と`syncerBinlogGtid`情報で構成します。

## DM v2.0 で、ハートビート<code>heartbeat</code>が以前に使用されたものと異なります: サーバー ID が等しくありません」というエラーを処理するにはどうすればよいですか? {#in-dm-v2-0-how-do-i-handle-the-error-heartbeat-config-is-different-from-previous-used-serverid-not-equal-when-switching-the-connection-between-dm-workers-and-mysql-instances-in-a-virtual-ip-environment-with-the-code-heartbeat-code-feature-enabled}

`heartbeat`機能は、DM v2.0 以降のバージョンではデフォルトで無効になっています。タスク構成ファイルでこの機能を有効にすると、高可用性機能が妨げられます。この問題を解決するには、タスク構成ファイルで`enable-heartbeat`から`false`を設定して`heartbeat`機能を無効にしてから、タスク構成ファイルをリロードします。 DM は、以降のリリースで`heartbeat`機能を強制的に無効にします。

## DM マスターが再起動後にクラスターに参加できず、DM が「埋め込み etcd の開始に失敗しました。RawCause: メンバー xxx は既にブートストラップされています」というエラーを報告するのはなぜですか? {#why-does-a-dm-master-fail-to-join-the-cluster-after-it-restarts-and-dm-reports-the-error-fail-to-start-embed-etcd-rawcause-member-xxx-has-already-been-bootstrapped}

DM-master が起動すると、DM は現在のディレクトリに etcd 情報を記録します。 DM マスターの再始動後にディレクトリーが変更された場合、DM は etcd 情報にアクセスできないため、再始動は失敗します。

この問題を解決するには、 TiUPを使用して DM クラスターを維持することをお勧めします。バイナリ ファイルを使用して展開する必要がある場合は、DM マスターの構成ファイルで絶対パスを使用して`data-dir`を構成するか、コマンドを実行する現在のディレクトリに注意する必要があります。

## dmctl を使用してコマンドを実行すると、DM マスターに接続できないのはなぜですか? {#why-dm-master-cannot-be-connected-when-i-use-dmctl-to-execute-commands}

dmctl execute コマンドを使用すると、(コマンドでパラメーター値`--master-addr`指定した場合でも) DM マスターへの接続が失敗し、エラー メッセージが`RawCause: context deadline exceeded, Workaround: please check your network connection.`のようになる場合があります。ただし、 `telnet <master-addr>`などのコマンドを使用してネットワーク接続を確認した後、例外は見つかりません。

この場合、環境変数`https_proxy`を確認できます (これは**https**であることに注意してください)。この変数が構成されている場合、dmctl は`https_proxy`で指定されたホストとポートに自動的に接続します。ホストに対応する`proxy`転送サービスがない場合、接続は失敗します。

この問題を解決するには、 `https_proxy`が必須かどうかを確認してください。そうでない場合は、設定をキャンセルしてください。それ以外の場合は、元の dmctl コマンドの前に環境変数設定`https_proxy="" ./dmctl --master-addr "x.x.x.x:8261"`を追加します。

> **ノート：**
>
> `proxy`に関連する環境変数には、 `http_proxy` 、 `https_proxy` 、および`no_proxy`が含まれます。上記の手順を実行しても接続エラーが続く場合は、構成パラメーター`http_proxy`と`no_proxy`が正しいかどうかを確認してください。

## DM バージョン 2.0.2 から 2.0.6 で start-relay コマンドを実行したときに返されたエラーを処理するにはどうすればよいですか? {#how-to-handle-the-returned-error-when-executing-start-relay-command-for-dm-versions-from-2-0-2-to-2-0-6}

```
flush local meta, Rawcause: open relay-dir/xxx.000001/relay.metayyyy: no such file or directory
```

上記のエラーは、次の場合に発生する可能性があります。

-   DM は v2.0.1 以前から v2.0.2 ～ v2.0.6 にアップグレードされ、リレー ログはアップグレード前に開始され、アップグレード後に再開されます。
-   stop-relay コマンドを実行して、リレー ログを一時停止してから再開します。

このエラーは、次のオプションで回避できます。

-   リレー ログを再開します。

    ```
    » stop-relay -s sourceID workerName
    » start-relay -s sourceID workerName
    ```

-   DM を v2.0.7 以降のバージョンにアップグレードします。

## ロード ユニットが<code>Unknown character set</code>エラーを報告するのはなぜですか? {#why-does-the-load-unit-report-the-code-unknown-character-set-code-error}

TiDB はすべての MySQL 文字セットをサポートしているわけではありません。したがって、フル インポート中にテーブル スキーマを作成するときに、サポートされていない文字セットが使用されている場合、DM はこのエラーを報告します。このエラーを回避するには、特定のデータに従って[TiDB がサポートする文字セット](/character-set-and-collation.md)を使用して、事前にダウンストリームでテーブル スキーマを作成できます。
