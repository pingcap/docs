---
title: TiDB Data Migration FAQ
summary: Learn about frequently asked questions (FAQs) about TiDB Data Migration (DM).
---

# TiDBデータ移行FAQ {#tidb-data-migration-faq}

このドキュメントは、TiDBデータ移行（DM）に関するよくある質問（FAQ）を集めたものです。

## DMは、Alibaba RDSまたは他のクラウドデータベースからのデータの移行をサポートしていますか？ {#does-dm-support-migrating-data-from-alibaba-rds-or-other-cloud-databases}

現在、DMはMySQLまたはMariaDBbinlogの標準バージョンのデコードのみをサポートしています。これは、AlibabaCloudRDSまたはその他のクラウドデータベースではテストされていません。 binlogが標準形式であることが確認された場合は、サポートされています。

既知の問題として、Alibaba Cloud RDSに主キーがないアップストリームテーブルの場合、そのbinlogに非表示の主キー列が含まれているため、元のテーブル構造と矛盾しています。

互換性のない既知の問題は次のとおりです。

-   **Alibaba Cloud RDS**では、主キーのないアップストリームテーブルの場合、そのbinlogに非表示の主キー列が含まれているため、元のテーブル構造と矛盾しています。
-   **HUAWEI Cloud RDS**では、binlogファイルの直接読み取りはサポートされていません。詳細については、 [HUAWEI Cloud RDSはBinlogバックアップファイルを直接読み取ることができますか？](https://support.huaweicloud.com/en-us/rds_faq/rds_faq_0210.html)を参照してください。

## タスク構成のブロックと許可リストの正規表現は、 <code>non-capturing (?!)</code>サポートしていますか？ {#does-the-regular-expression-of-the-block-and-allow-list-in-the-task-configuration-support-code-non-capturing-code}

現在、DMはそれをサポートしておらず、Golang標準ライブラリの正規表現のみをサポートしています。 [re2-構文](https://github.com/google/re2/wiki/Syntax)を介してGolangでサポートされている正規表現を参照してください。

## アップストリームで実行されるステートメントに複数のDDL操作が含まれている場合、DMはそのような移行をサポートしますか？ {#if-a-statement-executed-upstream-contains-multiple-ddl-operations-does-dm-support-such-migration}

DMは、複数のDDL変更操作を含む単一のステートメントを1つのDDL操作のみを含む複数のステートメントに分割しようとしますが、すべての場合をカバーするわけではありません。アップストリームで実行されるステートメントにDDL操作を1つだけ含めるか、テスト環境で検証することをお勧めします。サポートされていない場合は、DMリポジトリに[問題](https://github.com/pingcap/dm/issues)をファイルできます。

## 互換性のないDDLステートメントを処理する方法は？ {#how-to-handle-incompatible-ddl-statements}

TiDBでサポートされていないDDLステートメントに遭遇した場合は、dmctlを使用して手動で処理する必要があります（DDLステートメントをスキップするか、DDLステートメントを指定されたDDLステートメントに置き換えます）。詳細については、 [失敗したDDLステートメントを処理する](/dm/handle-failed-ddl-statements.md)を参照してください。

> **ノート：**
>
> 現在、TiDBはMySQLがサポートするすべてのDDLステートメントと互換性があるわけではありません。 [MySQLの互換性](/mysql-compatibility.md#ddl)を参照してください。

## データ移行タスクをリセットするにはどうすればよいですか？ {#how-to-reset-the-data-migration-task}

データ移行中に例外が発生し、データ移行タスクを再開できない場合は、タスクをリセットしてデータを再移行する必要があります。

1.  `stop-task`コマンドを実行して、異常なデータ移行タスクを停止します。

2.  ダウンストリームに移行されたデータをパージします。

3.  次のいずれかの方法を使用して、データ移行タスクを再開します。

    -   タスク構成ファイルで新しいタスク名を指定します。次に、 `start-task {task-config-file}`を実行します。
    -   `start-task --remove-meta {task-config-file}`を実行します。

## <code>online-ddl-scheme: &quot;gh-ost&quot;</code>が設定された後、gh-ostテーブルに関連するDDL操作によって返されるエラーを処理する方法は？ {#how-to-handle-the-error-returned-by-the-ddl-operation-related-to-the-gh-ost-table-after-code-online-ddl-scheme-gh-ost-code-is-set}

```
[unit=Sync] ["error information"="{\"msg\":\"[code=36046:class=sync-unit:scope=internal:level=high] online ddls on ghost table `xxx`.`_xxxx_gho`\\ngithub.com/pingcap/dm/pkg/terror.(*Error).Generate ......
```

上記のエラーは、次の理由で発生する可能性があります。

最後の`rename ghost_table to origin table`ステップで、DMはメモリ内のDDL情報を読み取り、それを元のテーブルのDDLに復元します。

ただし、メモリ内のDDL情報は、次の2つの方法のいずれかで取得されます。

-   [`alter ghost_table`操作中にgh-ostテーブルを処理します](/dm/feature-online-ddl.md#online-schema-change-gh-ost)および`ghost_table`のDDL情報を記録します。
-   DM-workerを再起動してタスクを開始すると、DMは`dm_meta.{task_name}_onlineddl`からDDLを読み取ります。

したがって、インクリメンタルレプリケーションのプロセスで、指定されたPosが`alter ghost_table` DDLをスキップしたが、Posがまだgh-ostのonline-ddlプロセスにある場合、ghost_tableはメモリまたは`dm_meta.{task_name}_onlineddl`に正しく書き込まれません。このような場合、上記のエラーが返されます。

次の手順でこのエラーを回避できます。

1.  タスクの`online-ddl-scheme`の構成を削除します。

2.  `_{table_name}_del` `_{table_name}_gho` `_{table_name}_ghc`し`block-allow-list.ignore-tables` 。

3.  ダウンストリームTiDBでアップストリームDDLを手動で実行します。

4.  Posがgh-ostプロセス後の位置に複製されたら、 `online-ddl-scheme`を再度有効にして、 `block-allow-list.ignore-tables`をコメントアウトします。

## 既存のデータ移行タスクにテーブルを追加するにはどうすればよいですか？ {#how-to-add-tables-to-the-existing-data-migration-tasks}

実行中のデータ移行タスクにテーブルを追加する必要がある場合は、タスクの段階に応じて次の方法で対処できます。

> **ノート：**
>
> 既存のデータ移行タスクへのテーブルの追加は複雑であるため、この操作は必要な場合にのみ実行することをお勧めします。

### <code>Dump</code>段階で {#in-the-code-dump-code-stage}

MySQLはエクスポート用のスナップショットを指定できないため、エクスポート中にデータ移行タスクを更新してから再起動してチェックポイントからエクスポートを再開することはサポートされていません。したがって、 `Dump`段階で移行する必要のあるテーブルを動的に追加することはできません。

移行のためにテーブルを本当に追加する必要がある場合は、新しい構成ファイルを使用してタスクを直接再開することをお勧めします。

### <code>Load</code>段階で {#in-the-code-load-code-stage}

エクスポート中、複数のデータ移行タスクは通常、異なるbinlog位置を持ちます。 `Load`段階でタスクをマージすると、binlogの位置について合意に達することができない場合があります。したがって、 `Load`段階のデータ移行タスクにテーブルを追加することはお勧めしません。

### <code>Sync</code>段階 {#in-the-code-sync-code-stage}

データ移行タスクが`Sync`段階の場合、構成ファイルにテーブルを追加してタスクを再開すると、DMは新しく追加されたテーブルの完全なエクスポートとインポートを再実行しません。代わりに、DMは前のチェックポイントから増分レプリケーションを続行します。

したがって、新しく追加されたテーブルの完全なデータがダウンストリームにインポートされていない場合は、別のデータ移行タスクを使用して、完全なデータをダウンストリームにエクスポートおよびインポートする必要があります。

既存の移行タスクに対応するグローバルチェックポイント（ `is_global=1` ）の位置情報を`(mysql-bin.000100, 1234)`などの`checkpoint-T`として記録します。移行タスクに追加するテーブルの完全エクスポート`metedata` （または`Sync`ステージの別のデータ移行タスクのチェックポイント）の位置情報を`checkpoint-S` （ `(mysql-bin.000099, 5678)`など）として記録します。次の手順で、テーブルを移行タスクに追加できます。

1.  `stop-task`を使用して、既存の移行タスクを停止します。追加するテーブルが実行中の別の移行タスクに属している場合は、そのタスクも停止します。

2.  MySQLクライアントを使用してダウンストリームTiDBデータベースに接続し、既存の移行タスクに対応するチェックポイントテーブルの情報を`checkpoint-T`の小さい値に手動で更新し`checkpoint-S` 。この例では、 `(mysql- bin.000099, 5678)`です。

    -   更新されるチェックポイントテーブルは、 `{dm_meta}`スキーマの`{task-name}_syncer_checkpoint`つです。

    -   更新されるチェックポイント行は`id=(source-id)`と`is_global=1`に一致します。

    -   更新されるチェックポイント列は`binlog_name`と`binlog_pos`です。

3.  再入可能な実行を確実にするために、タスクの`syncers`に`safe-mode: true`を設定します。

4.  `start-task`を使用してタスクを開始します。

5.  `query-status`を介してタスクのステータスを観察します。 `syncerBinlog`が`checkpoint-T`と`checkpoint-S`の大きい方の値を超えたら、 `safe-mode`を元の値に戻し、タスクを再開します。この例では、 `(mysql-bin.000100, 1234)`です。

## <code>packet for query is too large. Try adjusting the &#39;max_allowed_packet&#39; variable</code>完全なインポート中に発生<code>packet for query is too large. Try adjusting the &#39;max_allowed_packet&#39; variable</code> 。 {#how-to-handle-the-error-code-packet-for-query-is-too-large-try-adjusting-the-max-allowed-packet-variable-code-that-occurs-during-the-full-import}

以下のパラメーターをデフォルトの67108864（64M）より大きい値に設定します。

-   TiDBサーバーのグローバル変数： `max_allowed_packet` 。
-   タスク構成ファイルの構成項目： `target-database.max-allowed-packet` 。詳しくは[DM Advanced Task Configuration / コンフィグレーション File](/dm/task-configuration-file-full.md)をご覧ください。

## エラー1054の処理方法：DM1.0クラスタの既存のDM移行タスクがDM2.0以降のクラスタで実行されているときに発生する<code>Error 1054: Unknown column &#39;binlog_gtid&#39; in &#39;field list&#39;</code> ？ {#how-to-handle-the-error-code-error-1054-unknown-column-binlog-gtid-in-field-list-code-that-occurs-when-existing-dm-migration-tasks-of-an-dm-1-0-cluster-are-running-on-a-dm-2-0-or-newer-cluster}

DM v2.0以降、DM 1.0クラスタのタスク構成ファイルで`start-task`コマンドを直接実行して増分データ複製を続行すると、エラー`Error 1054: Unknown column 'binlog_gtid' in 'field list'`が発生します。

このエラーは[DM1.0クラスタのDM移行タスクをDM2.0クラスタに手動でインポートする](/dm/manually-upgrade-dm-1.0-to-2.0.md)で処理できます。

## TiUPがDMの一部のバージョン（v2.0.0-hotfixなど）の展開に失敗するのはなぜですか？ {#why-does-tiup-fail-to-deploy-some-versions-of-dm-for-example-v2-0-0-hotfix}

`tiup list dm-master`コマンドを使用して、TiUPが展開をサポートするDMバージョンを表示できます。 TiUPは、このコマンドで表示されないDMバージョンを管理しません。

## エラー<code>parse mydumper metadata error: EOF</code> ？ {#how-to-handle-the-error-code-parse-mydumper-metadata-error-eof-code-that-occurs-when-dm-is-replicating-data}

このエラーをさらに分析するには、エラーメッセージとログファイルを確認する必要があります。原因は、権限がないためにダンプユニットが正しいメタデータファイルを生成しないことである可能性があります。

## シャーディングされたスキーマとテーブルを複製するときにDMが致命的なエラーを報告しないのに、ダウンストリームデータが失われるのはなぜですか？ {#why-does-dm-report-no-fatal-error-when-replicating-sharded-schemas-and-tables-but-downstream-data-is-lost}

構成項目`block-allow-list`と`table-route`を確認してください。

-   アップストリームデータベースとテーブルの名前を`block-allow-list`で構成する必要があります。 `do-tables`の前に「〜」を追加して、正規表現を使用して名前を照合できます。
-   `table-route`は、正規表現の代わりにワイルドカード文字を使用してテーブル名を照合します。たとえば、 `table_parttern_[0-63]`は`table_parttern_0`から`table_pattern_6`までの7つのテーブルにのみ一致します。

## DMがアップストリームからレプリケートしていないのに、 <code>replicate lag</code>モニターメトリックにデータが表示されないのはなぜですか？ {#why-does-the-code-replicate-lag-code-monitor-metric-show-no-data-when-dm-is-not-replicating-from-upstream}

DM 1.0では、モニターデータを生成するために`enable-heartbeat`を有効にする必要があります。 DM 2.0以降のバージョンでは、この機能がサポートされていないため、モニターメトリック`replicate lag`にデータがないことが予想されます。

## DMがタスクを開始しているとき<code>fail to initial unit Sync of subtask</code>たエラーを処理する方法。エラーメッセージの<code>RawCause</code>は、 <code>context deadline exceeded</code>たことを示していますか？ {#how-to-handle-the-error-code-fail-to-initial-unit-sync-of-subtask-code-when-dm-is-starting-a-task-with-the-code-rawcause-code-in-the-error-message-showing-code-context-deadline-exceeded-code}

これはDM2.0.0バージョンの既知の問題であり、DM2.0.1バージョンで修正される予定です。レプリケーションタスクに処理するテーブルが多数ある場合にトリガーされる可能性があります。 TiUPを使用してDMをデプロイする場合は、DMをナイトリーバージョンにアップグレードしてこの問題を修正できます。または、GitHubの[DMのリリースページ](https://github.com/pingcap/tiflow/releases)から2.0.0-hotfixバージョンをダウンロードして、実行可能ファイルを手動で置き換えることができます。

## DMがデータを複製しているときにエラー<code>duplicate entry</code>を処理するにはどうすればよいですか？ {#how-to-handle-the-error-code-duplicate-entry-code-when-dm-is-replicating-data}

まず、次のことを確認して確認する必要があります。

-   `disable-detect`はレプリケーションタスクで構成されていません（v2.0.7以前のバージョン）。
-   データは手動または他のレプリケーションプログラムによって挿入されません。
-   このテーブルに関連付けられたDMLフィルターは構成されていません。

トラブルシューティングを容易にするために、最初にダウンストリームTiDBインスタンスの一般的なログファイルを収集してから、 [TiDBコミュニティのスラックチャネル](https://tidbcommunity.slack.com/archives/CH7TTLL7P)でテクニカルサポートを依頼できます。次の例は、一般的なログファイルを収集する方法を示しています。

```bash
# Enable general log collection
curl -X POST -d "tidb_general_log=1" http://{TiDBIP}:10080/settings
# Disable general log collection
curl -X POST -d "tidb_general_log=0" http://{TiDBIP}:10080/settings
```

`duplicate entry`エラーが発生した場合は、ログファイルで競合データを含むレコードを確認する必要があります。

## 一部の監視パネルに<code>No data point</code>のはなぜですか？ {#why-do-some-monitoring-panels-show-code-no-data-point-code}

一部のパネルにはデータがないのが普通です。たとえば、エラーが報告されていない場合、DDLロックがない場合、またはリレーログ機能が有効になっていない場合、対応するパネルには`No data point`が表示されます。各パネルの詳細については、 [DMモニタリングメトリクス](/dm/monitor-a-dm-cluster.md)を参照してください。

## DM v1.0では、タスクにエラーがあるときにコマンド<code>sql-skip</code>が一部のステートメントをスキップできないのはなぜですか？ {#in-dm-v1-0-why-does-the-command-code-sql-skip-code-fail-to-skip-some-statements-when-the-task-is-in-error}

`sql-skip`を実行した後、最初にbinlogの位置がまだ進んでいるかどうかを確認する必要があります。もしそうなら、それは`sql-skip`が有効になったことを意味します。このエラーが引き続き発生する理由は、アップストリームがサポートされていない複数のDDLステートメントを送信するためです。 `sql-skip -s <sql-pattern>`を使用して、これらのステートメントに一致するパターンを設定できます。

エラーメッセージに`parse statement`の情報が含まれている場合があります。次に例を示します。

```
if the DDL is not needed, you can use a filter rule with \"*\" schema-pattern to ignore it.\n\t : parse statement: line 1 column 11 near \"EVENT `event_del_big_table` \r\nDISABLE\" %!!(MISSING)(EXTRA string=ALTER EVENT `event_del_big_table` \r\nDISABLE
```

このタイプのエラーの理由は、TiDBパーサーが`ALTER EVENT`などのアップストリームによって送信されたDDLステートメントを解析できないため、 `sql-skip`が期待どおりに有効にならないためです。構成ファイルに[binlogイベントフィルター](/dm/dm-key-features.md#binlog-event-filter)を追加して、これらのステートメントをフィルター処理し、 `schema-pattern: "*"`を設定できます。 DM v2.0.1以降、DMは`EVENT`に関連するステートメントを事前にフィルタリングします。

DM v6.0以降、 `sql-skip`と`handle-error`は`binlog`に置き換わります。この問題を回避するには、代わりに`binlog`コマンドを使用できます。

## DMが複製しているときに、 <code>REPLACE</code>ステートメントがダウンストリームに表示され続けるのはなぜですか？ {#why-do-code-replace-code-statements-keep-appearing-in-the-downstream-when-dm-is-replicating}

[セーフモード](/dm/dm-glossary.md#safe-mode)がタスクに対して自動的に有効になっているかどうかを確認する必要があります。エラー後にタスクが自動的に再開される場合、または高可用性スケジューリングがある場合、タスクが開始または再開されてから1分以内であるため、セーフモードが有効になります。

DM-workerログファイルを確認して、 `change count`を含む行を検索できます。行の`new count`がゼロでない場合、セーフモードが有効になります。有効になっている理由を確認するには、いつ発生するか、以前にエラーが報告されていないかどうかを確認してください。

## DM v2.0では、タスク中にDMが再起動すると、完全なインポートタスクが失敗するのはなぜですか？ {#in-dm-v2-0-why-does-the-full-import-task-fail-if-dm-restarts-during-the-task}

DM v2.0.1以前のバージョンでは、完全なインポートが完了する前にDMが再起動すると、アップストリームデータソースとDMワーカーノード間のバインディングが変更される可能性があります。たとえば、ダンプユニットの中間データがDMワーカーノードAにあるが、ロードユニットがDMワーカーノードBによって実行されているため、操作が失敗する可能性があります。

この問題に対する2つの解決策は次のとおりです。

-   データ量が少ない（1 TB未満）場合、またはタスクがシャードテーブルをマージする場合は、次の手順を実行します。

    1.  ダウンストリームデータベースにインポートされたデータをクリーンアップします。
    2.  エクスポートされたデータのディレクトリ内のすべてのファイルを削除します。
    3.  dmctlを使用してタスクを削除し、コマンド`start-task --remove-meta`を実行して新しいタスクを作成します。

    新しいタスクの開始後、冗長なDMワーカーノードがないことを確認し、完全なインポート中にDMクラスタを再起動またはアップグレードしないようにすることをお勧めします。

-   データ量が多い（1 TBを超える）場合は、次の手順を実行します。

    1.  ダウンストリームデータベースにインポートされたデータをクリーンアップします。
    2.  データを処理するDMワーカーノードにTiDB-Lightningをデプロイします。
    3.  TiDB-Lightningのローカルバックエンドモードを使用して、DMダンプユニットがエクスポートするデータをインポートします。
    4.  完全なインポートが完了したら、次の方法でタスク構成ファイルを編集し、タスクを再開します。
        -   `task-mode`を`incremental`に変更します。
        -   ダンプユニットが出力するメタデータファイルに記録されている位置に値`mysql-instance.meta.pos`を設定します。

## DMがエラー<code>ERROR 1236 (HY000): The slave is connecting using CHANGE MASTER TO MASTER_AUTO_POSITION = 1, but the master has purged binary logs containing GTIDs that the slave requires.</code>インクリメンタルタスク中に再起動した場合はどうなりますか？ {#why-does-dm-report-the-error-code-error-1236-hy000-the-slave-is-connecting-using-change-master-to-master-auto-position-1-but-the-master-has-purged-binary-logs-containing-gtids-that-the-slave-requires-code-if-it-restarts-during-an-incremental-task}

このエラーは、ダンプユニットによって出力されたメタデータファイルに記録されたアップストリームbinlog位置が、完全な移行中にパージされたことを示します。

この問題が発生した場合は、タスクを一時停止し、ダウンストリームデータベース内の移行されたすべてのデータを削除して、 `--remove-meta`オプションで新しいタスクを開始する必要があります。

次の方法で構成することにより、この問題を事前に回避できます。

1.  完全な移行タスクが完了する前に必要なbinlogファイルを誤ってパージしないように、アップストリームMySQLデータベースの値を`expire_logs_days`に増やします。データ量が多い場合は、餃子とTiDB-Lightningを同時に使用してタスクを高速化することをお勧めします。
2.  このタスクのリレーログ機能を有効にして、binlogの位置が削除された場合でも、DMがリレーログからデータを読み取れるようにします。

## クラスタがTiUPv1.3.0またはv1.3.1を使用してデプロイされている場合、DMクラスタディスプレイのGrafanaダッシュボードがダッシュボードの<code>failed to fetch dashboard</code>たのはなぜですか？ {#why-does-the-grafana-dashboard-of-a-dm-cluster-display-code-failed-to-fetch-dashboard-code-if-the-cluster-is-deployed-using-tiup-v1-3-0-or-v1-3-1}

これはTiUPの既知のバグであり、TiUPv1.3.2で修正されています。この問題に対する2つの解決策は次のとおりです。

-   解決策1：
    1.  コマンド`tiup update --self && tiup update dm`を使用して、TiUPを新しいバージョンにアップグレードします。
    2.  クラスタのGrafanaノードをスケールインしてからスケールアウトし、Grafanaサービスを再起動します。
-   解決策2：
    1.  `deploy/grafana-$port/bin/public`のフォルダをバックアップします。
    2.  [TiUP DMオフラインパッケージ](https://download.pingcap.org/tidb-dm-v2.0.1-linux-amd64.tar.gz)をダウンロードして解凍します。
    3.  オフラインパッケージで`grafana-v4.0.3-**.tar.gz`を解凍します。
    4.  フォルダ`deploy/grafana-$port/bin/public`を`grafana-v4.0.3-**.tar.gz`の`public`フォルダに置き換えます。
    5.  `tiup dm restart $cluster_name -R grafana`を実行して、Grafanaサービスを再起動します。

## DM v2.0で、コマンド<code>query-status</code>のクエリ結果に、タスクで<code>enable-relay</code>と<code>enable-gtid</code>が同時に有効になっている場合に、SyncerチェックポイントGTIDが連続していないことが示されるのはなぜですか？ {#in-dm-v2-0-why-does-the-query-result-of-the-command-code-query-status-code-show-that-the-syncer-checkpoint-gtids-are-inconsecutive-if-the-task-has-code-enable-relay-code-and-code-enable-gtid-code-enabled-at-the-same-time}

これはDMの既知のバグであり、DMv2.0.2で修正されています。このバグは、次の2つの条件が同時に完全に満たされたときにトリガーされます。

1.  ソース構成ファイルでは、パラメーター`enable-relay`と`enable-gtid`が`true`に設定されています。
2.  アップストリームデータベースは**MySQLセカンダリデータベース**です。コマンド`show binlog events in '<newest-binlog>' limit 2`を実行してデータベースの`previous_gtids`を照会すると、次の例のように、結果は連続しません。

```
mysql> show binlog events in 'mysql-bin.000005' limit 2;
+------------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+
| Log_name         | Pos  | Event_type     | Server_id | End_log_pos | Info                                                               |
+------------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+
| mysql-bin.000005 |    4 | Format_desc    |    123452 |         123 | Server ver: 5.7.32-35-log, Binlog ver: 4                           |
| mysql-bin.000005 |  123 | Previous_gtids |    123452 |         194 | d3618e68-6052-11eb-a68b-0242ac110002:6-7                           |
+------------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+
```

このバグは、dmctlで`query-status <task>`を実行してタスク情報を照会し、 `subTaskStatus.sync.syncerBinlogGtid`が連続していないが、 `subTaskStatus.sync.masterBinlogGtid`が連続していることがわかった場合に発生します。次の例を参照してください。

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

この例では、データソース`mysql1`の`syncerBinlogGtid`は連続していません。この場合、次のいずれかを実行してデータ損失を処理できます。

-   現在の時刻から完全なエクスポートタスクのメタデータに記録されている位置までのアップストリームbinlogがパージされていない場合は、次の手順を実行できます。
    1.  現在のタスクを停止し、GTIDが連続していないすべてのデータソースを削除します。
    2.  すべてのソース構成ファイルで`enable-relay`から`false`に設定します。
    3.  GTIDが連続していないデータソース（上記の例の`mysql1`など）の場合、タスクをインクリメンタルタスクに変更し、 `binlog-name` 、および`binlog-pos`の情報を含む各完全エクスポートタスクのメタデータ情報を使用して関連する`mysql-instances.meta`を構成し`binlog-gtid` 。
    4.  インクリメンタルタスクの`task.yaml`分の`syncers.safe-mode`を`true`に設定し、タスクを再開します。
    5.  インクリメンタルタスクが欠落しているすべてのデータをダウンストリームに複製した後、タスクを停止し、 `task.yaml`の`safe-mode`を`false`に変更します。
    6.  タスクを再開します。
-   アップストリームbinlogがパージされたが、ローカルリレーログが残っている場合は、次の手順を実行できます。
    1.  現在のタスクを停止します。
    2.  GTIDが連続していないデータソース（上記の例の`mysql1`など）の場合、タスクをインクリメンタルタスクに変更し、 `binlog-name` 、および`binlog-pos`の情報を含む各完全エクスポートタスクのメタデータ情報を使用して関連する`mysql-instances.meta`を構成し`binlog-gtid` 。
    3.  インクリメンタルタスクの`task.yaml`で、前の値`binlog-gtid`を前の値`previous_gtids`に変更します。上記の例では、 `1-y`を`6-y`に変更します。
    4.  `task.yaml`に`syncers.safe-mode`から`true`を設定し、タスクを再開します。
    5.  インクリメンタルタスクが欠落しているすべてのデータをダウンストリームに複製した後、タスクを停止し、 `task.yaml`の`safe-mode`を`false`に変更します。
    6.  タスクを再開します。
    7.  データソースを再起動し、ソース構成ファイルで`enable-relay`または`enable-gtid`を`false`に設定します。
-   上記の条件のいずれも満たされない場合、またはタスクのデータ量が少ない場合は、次の手順を実行できます。
    1.  ダウンストリームデータベースにインポートされたデータをクリーンアップします。
    2.  データソースを再起動し、ソース構成ファイルで`enable-relay`または`enable-gtid`を`false`に設定します。
    3.  新しいタスクを作成し、コマンド`start-task task.yaml --remove-meta`を実行して、データを最初から再度移行します。

上記の第1および第2のソリューションで正常に複製できるデータソース（上記の例の`mysql2`など）の場合、増分タスクを設定するときに、関連する`mysql-instances.meta`を`subTaskStatus.sync`からの`syncerBinlog`および`syncerBinlogGtid`の情報で構成します。

## DM v2.0で、 <code>heartbeat</code>機能が有効になっている仮想IP環境でDMワーカーとMySQLインスタンス間の接続を切り替えるときに、「ハートビート構成が以前に使用されたものと異なります：サーバーIDが等しくありません」というエラーを処理するにはどうすればよいですか？ {#in-dm-v2-0-how-do-i-handle-the-error-heartbeat-config-is-different-from-previous-used-serverid-not-equal-when-switching-the-connection-between-dm-workers-and-mysql-instances-in-a-virtual-ip-environment-with-the-code-heartbeat-code-feature-enabled}

DM v2.0以降のバージョンでは、 `heartbeat`機能はデフォルトで無効になっています。タスク構成ファイルでこの機能を有効にすると、高可用性機能が妨げられます。この問題を解決するには、タスク構成ファイルで`enable-heartbeat`を`false`に設定して、 `heartbeat`機能を無効にしてから、タスク構成ファイルを再ロードします。 DMは、以降のリリースで`heartbeat`機能を強制的に無効にします。

## DMマスターが再起動した後、クラスタへの参加に失敗し、DMが「埋め込みetcdの開始に失敗しました。RawCause：メンバーxxxはすでにブートストラップされています」というエラーを報告するのはなぜですか？ {#why-does-a-dm-master-fail-to-join-the-cluster-after-it-restarts-and-dm-reports-the-error-fail-to-start-embed-etcd-rawcause-member-xxx-has-already-been-bootstrapped}

DMマスターが起動すると、DMはetcd情報を現在のディレクトリに記録します。 DMマスターの再起動後にディレクトリが変更された場合、DMはetcd情報にアクセスできないため、再起動は失敗します。

この問題を解決するには、TiUPを使用してDMクラスターを維持することをお勧めします。バイナリファイルを使用して展開する必要がある場合は、DMマスターの構成ファイルで絶対パスを使用して`data-dir`を構成するか、コマンドを実行する現在のディレクトリに注意する必要があります。

## dmctlを使用してコマンドを実行するとDMマスターに接続できないのはなぜですか？ {#why-dm-master-cannot-be-connected-when-i-use-dmctl-to-execute-commands}

dmctl executeコマンドを使用すると、DMマスターへの接続が失敗する場合があり（コマンドでパラメーター値`--master-addr`を指定した場合でも）、エラーメッセージは`RawCause: context deadline exceeded, Workaround: please check your network connection.`のようになります。ただし、 `telnet <master-addr>`などのコマンドを使用してネットワーク接続を確認した後、例外は見つかりません。

この場合、環境変数`https_proxy`を確認できます（ **https**であることに注意してください）。この変数が構成されている場合、dmctlは`https_proxy`で指定されたホストとポートを自動的に接続します。ホストに対応する転送サービスがない場合、接続は失敗し`proxy` 。

この問題を解決するには、 `https_proxy`が必須かどうかを確認してください。そうでない場合は、設定をキャンセルしてください。それ以外の場合は、元のdmctlコマンドの前に環境変数設定`https_proxy="" ./dmctl --master-addr "x.x.x.x:8261"`を追加します。

> **ノート：**
>
> `proxy`に関連する環境変数には、 `http_proxy` 、および`https_proxy`が含まれ`no_proxy` 。上記の手順を実行しても接続エラーが続く場合は、 `http_proxy`と`no_proxy`の構成パラメーターが正しいかどうかを確認してください。

## 2.0.2から2.0.6までのDMバージョンでstart-relayコマンドを実行するときに返されたエラーを処理するにはどうすればよいですか？ {#how-to-handle-the-returned-error-when-executing-start-relay-command-for-dm-versions-from-2-0-2-to-2-0-6}

```
flush local meta, Rawcause: open relay-dir/xxx.000001/relay.metayyyy: no such file or directory
```

上記のエラーは、次の場合に発生する可能性があります。

-   DMはv2.0.1以前からv2.0.2-v2.0.6にアップグレードされており、リレーログはアップグレード前に開始され、アップグレード後に再起動されます。
-   stop-relayコマンドを実行してリレーログを一時停止してから再起動します。

次のオプションにより、このエラーを回避できます。

-   リレーログを再起動します。

    ```
    » stop-relay -s sourceID workerName
    » start-relay -s sourceID workerName
    ```

-   DMをv2.0.7以降のバージョンにアップグレードします。
