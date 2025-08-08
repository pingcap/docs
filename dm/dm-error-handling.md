---
title: Handle Errors in TiDB Data Migration
summary: DM を使用する際のエラー システムと一般的なエラーの処理方法について学習します。
---

# TiDBデータ移行におけるエラーの処理 {#handle-errors-in-tidb-data-migration}

このドキュメントでは、エラー システムと、DM を使用するときに発生する一般的なエラーの処理方法について説明します。

## エラーシステム {#error-system}

エラー システムでは、通常、特定のエラーの情報は次のようになります。

-   `code` : エラーコード。

    DMでは、同じエラータイプに対して同じエラーコードが使用されます。DMのバージョンが変更されても、エラーコードは変更されません。

    DM 反復処理中に一部のエラーが削除される可能性がありますが、エラー コードは削除されません。DM は、新しいエラーに対して既存のエラー コードではなく新しいエラー コードを使用します。

-   `class` : エラータイプ。

    エラーが発生したコンポーネント(エラー ソース) をマークするために使用されます。

    次の表には、すべてのエラー タイプ、エラー ソース、およびエラー サンプルが表示されます。

    | エラーの種類            | エラーソース                              | エラーサンプル                                                                                                                                                                                                                                                                                          |
    | :---------------- | :---------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `database`        | データベース操作                            | `[code=10003:class=database:scope=downstream:level=medium] database driver: invalid connection`                                                                                                                                                                                                  |
    | `functional`      | DMの基礎関数                             | `[code=11005:class=functional:scope=internal:level=high] not allowed operation: alter multiple tables in one statement`                                                                                                                                                                          |
    | `config`          | 設定が正しくありません                         | `[code=20005:class=config:scope=internal:level=medium] empty source-id not valid`                                                                                                                                                                                                                |
    | `binlog-op`       | Binlog操作                            | `[code=22001:class=binlog-op:scope=internal:level=high] empty UUIDs not valid`                                                                                                                                                                                                                   |
    | `checkpoint`      | チェックポイント操作                          | `[code=24002:class=checkpoint:scope=internal:level=high] save point bin.1234 is older than current pos bin.1371`                                                                                                                                                                                 |
    | `task-check`      | タスクチェックを実行しています                     | `[code=26003:class=task-check:scope=internal:level=medium] new table router error`                                                                                                                                                                                                               |
    | `relay-event-lib` | リレーモジュールの基本関数を実行する                  | `[code=28001:class=relay-event-lib:scope=internal:level=high] parse server-uuid.index`                                                                                                                                                                                                           |
    | `relay-unit`      | リレー処理装置                             | `[code=30015:class=relay-unit:scope=upstream:level=high] TCPReader get event: ERROR 1236 (HY000): Could not open log file`                                                                                                                                                                       |
    | `dump-unit`       | ダンプ処理装置                             | `[code=32001:class=dump-unit:scope=internal:level=high] mydumper runs with error: CRITICAL **: 15:12:17.559: Error connecting to database: Access denied for user 'root'@'172.17.0.1' (using password: NO)`                                                                                      |
    | `load-unit`       | 負荷処理装置                              | `[code=34002:class=load-unit:scope=internal:level=high] corresponding ending of sql: ')' not found`                                                                                                                                                                                              |
    | `sync-unit`       | 同期処理ユニット                            | `[code=36027:class=sync-unit:scope=internal:level=high] Column count doesn't match value count: 9 (columns) vs 10 (values)`                                                                                                                                                                      |
    | `dm-master`       | DMマスターサービス                          | `[code=38008:class=dm-master:scope=internal:level=high] grpc request error: rpc error: code = Unavailable desc = all SubConns are in TransientFailure, latest connection error: connection error: desc = "transport: Error while dialing dial tcp 172.17.0.2:8262: connect: connection refused"` |
    | `dm-worker`       | DMワーカーサービス                          | `[code=40066:class=dm-worker:scope=internal:level=high] ExecuteDDL timeout, try use query-status to query whether the DDL is still blocking`                                                                                                                                                     |
    | `dm-tracer`       | DMトレーサーサービス                         | `[code=42004:class=dm-tracer:scope=internal:level=medium] trace event test.1 not found`                                                                                                                                                                                                          |
    | `schema-tracker`  | スキーマトラッカー（増分データレプリケーション中）           | `[code=44006:class=schema-tracker:scope=internal:level=high],"cannot track DDL: ALTER TABLE test DROP COLUMN col1"`                                                                                                                                                                              |
    | `scheduler`       | 操作のスケジュール設定（データ移行タスク）               | `[code=46001:class=scheduler:scope=internal:level=high],"the scheduler has not started"`                                                                                                                                                                                                         |
    | `dmctl`           | dmctl 内または他のコンポーネントとのやり取り中にエラーが発生する | `[code=48001:class=dmctl:scope=internal:level=high],"can not create grpc connection"`                                                                                                                                                                                                            |

-   `scope` : エラー範囲。

    エラーが発生したときに、 DM オブジェクトのスコープとソースをマークするために使用されます。 `scope`は、 `not-set` 、 `upstream` 、 `downstream` 、 `internal` 4 つのタイプが含まれます。

    エラーのロジックが上流データベースと下流データベース間のリクエストに直接関係する場合、スコープは`upstream`または`downstream`に設定されます。それ以外の場合、現在は`internal`に設定されています。

-   `level` : エラーレベル。

    エラーの重大度レベル ( `low` 、 `medium` 、 `high` 。

    -   レベル`low`エラーは通常、ユーザー操作や誤った入力に関連します。移行タスクには影響しません。
    -   レベル`medium`エラーは通常、ユーザー設定に関連しています。これは新しく開始された一部のサービスに影響しますが、既存のDM移行ステータスには影響しません。
    -   移行タスクが中断される可能性を回避するために、レベル`high`エラーを解決する必要があるため、通常は注意が必要です。

-   `message` : エラーの説明。

    エラーの詳細な説明。エラー呼び出しチェーン上のエラーメッセージの各追加レイヤーをラップして保存するために、モード[エラー。ラップ](https://godoc.org/github.com/pkg/errors#hdr-Adding_context_to_an_error)採用されています。レイヤーにラップされたメッセージ記述はDM内のエラーを示し、最レイヤーにラップされたメッセージ記述はエラーの原因を示します。

-   `workaround` : エラー処理方法（オプション）

    このエラーの処理方法。確認済みのエラー（設定エラーなど）については、DMは`workaround`で対応する手動処理方法を示しています。

-   エラースタック情報（オプション）

    DMがエラースタック情報を出力するかどうかは、エラーの重大度と必要性によって異なります。エラースタックには、エラー発生時のスタック呼び出し情報がすべて記録されます。基本情報とエラーメッセージだけではエラーの原因を特定できない場合は、エラースタックを使用することで、エラー発生時のコード実行パスを追跡できます。

エラー コードの完全なリストについては、 [エラーコードリスト](https://github.com/pingcap/tiflow/blob/release-8.5/dm/_utils/terror_gen/errors_release.txt)を参照してください。

## トラブルシューティング {#troubleshooting}

DM の実行中にエラーが発生した場合は、次の手順に従ってこのエラーをトラブルシューティングしてください。

1.  `query-status`コマンドを実行して、タスクの実行ステータスとエラー出力を確認します。

2.  エラーに関連するログファイルを確認してください。ログファイルはDMマスターノードとDMワーカーノードにあります。エラーに関する重要な情報を取得するには、 [エラーシステム](#error-system)を参照してください。その後、 [よくあるエラーの処理](#handle-common-errors)セクションを参照して解決策を見つけてください。

3.  このドキュメントにエラーが記載されておらず、ログを確認したりメトリックを監視したりしても問題を解決できない場合は、PingCAP またはコミュニティに[サポートを受ける](/support.md) 。

4.  エラーが解決したら、dmctl を使用してタスクを再起動します。

    ```bash
    resume-task ${task name}
    ```

ただし、場合によってはデータ移行タスクをリセットする必要があります。詳細は[データ移行タスクをリセットする](/dm/dm-faq.md#how-to-reset-the-data-migration-task)を参照してください。

## よくあるエラーの処理 {#handle-common-errors}

| エラーコード       | エラーの説明                                                                                                                                       | 取り扱い方法                                                                                                                                                                                                                                                            |
| :----------- | :------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `code=10001` | 異常なデータベース操作です。                                                                                                                               | エラー メッセージとエラー スタックをさらに分析します。                                                                                                                                                                                                                                      |
| `code=10002` | 基盤データベースからのエラー`bad connection`です。これは通常、DMと下流のTiDBインスタンス間の接続に異常があり（ネットワーク障害またはTiDBの再起動が原因と考えられます）、現在要求されているデータがTiDBに送信されていないことを示します。          | DMはこのようなエラーに対して自動リカバリを提供します。長時間リカバリが成功しない場合は、ネットワークまたはTiDBのステータスを確認してください。                                                                                                                                                                                        |
| `code=10003` | 基盤データベースからのエラー`invalid connection`です。これは通常、DMと下流のTiDBインスタンス間の接続に異常があり（ネットワーク障害またはTiDBの再起動が原因と考えられます）、現在要求されているデータの一部がTiDBに送信されていることを示します。    | DMはこのようなエラーに対して自動回復機能を提供します。長時間回復できない場合は、エラーメッセージをさらに確認し、実際の状況に基づいて情報を分析してください。                                                                                                                                                                                   |
| `code=10005` | `QUERY`種類の SQL ステートメントを実行するときに発生します。                                                                                                         |                                                                                                                                                                                                                                                                   |
| `code=10006` | `EXECUTE`タイプのSQL文（ `INSERT` `UPDATE`または`DELETE`タイプのDDL文およびDML文を含む）の実行時に発生します。詳細なエラー情報については、通常、データベース操作で返されるエラーコードとエラー情報を含むエラーメッセージを確認してください。 |                                                                                                                                                                                                                                                                   |
|              |                                                                                                                                              |                                                                                                                                                                                                                                                                   |
| `code=11006` | DM の組み込みパーサーが互換性のない DDL ステートメントを解析するときに発生します。                                                                                                | 解決策については[データ移行 - 互換性のない DDL ステートメント](/dm/dm-faq.md#how-to-handle-incompatible-ddl-statements)を参照してください。                                                                                                                                                           |
| `code=20010` | タスク構成で指定されたデータベース パスワードを復号化するときに発生します。                                                                                                       | 構成タスクで指定されたダウンストリーム データベース パスワードが[dmctlを使用して正しく暗号化されました](/dm/dm-manage-source.md#encrypt-the-database-password)あるかどうかを確認します。                                                                                                                                      |
| `code=26002` | タスクチェックでデータベース接続を確立できませんでした。詳細なエラー情報については、エラーメッセージを確認してください。エラーメッセージには通常、データベース操作で返されたエラーコードとエラー情報が含まれています。                                  | DM マスターが配置されているマシンにアップストリームにアクセスする権限があるかどうかを確認します。                                                                                                                                                                                                                |
| `code=32001` | 異常ダンプ処理装置                                                                                                                                    | エラーメッセージに`mydumper: argument list too long.`が含まれている場合は、ブロック/許可リストに従って、 `task.yaml`ファイルの Mydumper 引数`extra-args`に`--regex`正規表現を手動で追加して、エクスポートするテーブルを設定します。例えば、 `hello`という名前のテーブルをすべてエクスポートするには`--regex '.*\\.hello$'`を追加し、すべてのテーブルをエクスポートするには`--regex '.*'`を追加します。 |
| `code=38008` | DM コンポーネント間の gRPC 通信でエラーが発生します。                                                                                                              | チェック`class` ：どのコンポーネントの相互作用でエラーが発生しているかを確認します。通信エラーの種類を特定します。gRPC接続の確立時にエラーが発生する場合は、通信サーバーが正常に動作しているかどうかを確認します。                                                                                                                                                   |

### <code>invalid connection</code>エラーが返され、移行タスクが中断された場合、どうすればよいですか? {#what-can-i-do-when-a-migration-task-is-interrupted-with-the-code-invalid-connection-code-error-returned}

#### 理由 {#reason}

エラー`invalid connection`は、DM と下流の TiDB データベース間の接続に異常 (ネットワーク障害、TiDB の再起動、TiKV のビジー状態など) が発生し、現在の要求のデータの一部が TiDB に送信されたことを示します。

#### ソリューション {#solutions}

DMは移行タスクにおいてデータを下流へ並行して移行する機能を備えているため、タスクが中断されると様々なエラーが発生する可能性があります。これらのエラーは`query-status`使用して確認できます。

-   増分レプリケーション プロセス中に`invalid connection`エラーのみが発生した場合、DM はタスクを自動的に再試行します。
-   バージョンの問題により DM が自動的に再試行されない場合、または再試行に失敗した場合は、 `stop-task`使用してタスクを停止し、 `start-task`使用してタスクを再起動します。

### 移行タスクが<code>driver: bad connection</code>エラーが返されました {#a-migration-task-is-interrupted-with-the-code-driver-bad-connection-code-error-returned}

#### 理由 {#reason}

エラー`driver: bad connection`は、DM と上流の TiDB データベース間の接続に異常 (ネットワーク障害や TiDB の再起動など) が発生し、その時点では現在のリクエストのデータがまだ TiDB に送信されていないことを示します。

#### 解決 {#solution}

現在のバージョンのDMは、エラー発生時に自動的に再試行します。自動再試行をサポートしていない以前のバージョンをご利用の場合は、コマンド`stop-task`を実行してタスクを停止し、その後コマンド`start-task`実行してタスクを再開してください。

### リレーユニットは<code>event from * in * diff from passed-in event *</code>スローするか、または、 binlogエラーの取得または解析に失敗して移行タスクが中断され、binlog <code>get binlog error ERROR 1236 (HY000)</code>や<code>binlog checksum mismatch, data may be corrupted</code> 。 {#the-relay-unit-throws-error-code-event-from-in-diff-from-passed-in-event-code-or-a-migration-task-is-interrupted-with-failing-to-get-or-parse-binlog-errors-like-code-get-binlog-error-error-1236-hy000-code-and-code-binlog-checksum-mismatch-data-may-be-corrupted-code-returned}

#### 理由 {#reason}

リレー ログ プルまたは増分レプリケーションの DM プロセス中に、アップストリームbinlogファイルのサイズが**4 GB**を超えると、この 2 つのエラーが発生する可能性があります。

**原因：**リレーログを書き込む際、DMはbinlogの位置とbinlogファイルのサイズに基づいてイベント検証を行い、複製されたbinlogの位置をチェックポイントとして保存する必要があります。しかし、公式のMySQLではbinlogの位置を`uint32`保存しています。そのため、4GBを超えるbinlogファイルのbinlogの位置がオーバーフローし、上記のエラーが発生します。

#### ソリューション {#solutions}

リレー ユニットの場合は、次のソリューションを使用して手動で移行を回復します。

1.  エラーが発生したときに、対応するbinlogファイルのサイズが 4GB を超えたことをアップストリームで特定します。

2.  DM ワーカーを停止します。

3.  アップストリーム内の対応するbinlogファイルをリレー ログ ファイルとしてリレー ログ ディレクトリにコピーします。

4.  リレーログディレクトリ内の対応する`relay.meta`のファイルを更新し、次のbinlogファイルから取得します。DMワーカーに`enable_gtid` ～ `true`指定した場合は、 `relay.meta`ファイルを更新するときに、次のbinlogファイルに対応するGTIDを変更する必要があります。それ以外の場合は、GTIDを変更する必要はありません。

    例: エラーが発生した場合、 `binlog-name = "mysql-bin.004451"`と`binlog-pos = 2453`をそれぞれ`binlog-name = "mysql-bin.004452"`と`binlog-pos = 4`に更新し、 `binlog-gtid`を`f0e914ef-54cf-11e7-813d-6c92bf2fa791:1-138218058`に更新します。

5.  DM ワーカーを再起動します。

binlogレプリケーション処理ユニットの場合は、次のソリューションを使用して手動で移行を回復します。

1.  エラーが発生したときに、対応するbinlogファイルのサイズが 4GB を超えたことをアップストリームで特定します。

2.  `stop-task`使用して移行タスクを停止します。

3.  グローバル チェックポイントとダウンストリーム`dm_meta`データベースの各テーブル チェックポイントの`binlog_name` 、エラーのあるbinlogファイルの名前に更新します。5 `binlog_pos` 、移行が完了した有効な位置の値 (例: 4) に更新します。

    例：エラーが発生したタスクの名前が`dm_test` 、対応するタスク`source-id`が`replica-1` 、対応するbinlogファイルが`mysql-bin|000001.004451`場合、次のコマンドを実行します。

    ```sql
    UPDATE dm_test_syncer_checkpoint SET binlog_name='mysql-bin|000001.004451', binlog_pos = 4 WHERE id='replica-1';
    ```

4.  再入可能性を確保するには、移行タスク構成の`syncers`セクションで`safe-mode: true`指定します。

5.  `start-task`使用して移行タスクを開始します。

6.  `query-status`使用して移行タスクのステータスをビュー。元のエラーの原因となったリレーログファイルの移行が完了したら、 `safe-mode`元の値に戻して移行タスクを再開できます。

### タスクをクエリするかログを確認すると、 <code>Access denied for user &#39;root&#39;@&#39;172.31.43.27&#39; (using password: YES)</code>表示されます。 {#code-access-denied-for-user-root-172-31-43-27-using-password-yes-code-shows-when-you-query-the-task-or-check-the-log}

すべてのDM設定ファイルにおけるデータベース関連のパスワードについては、 `dmctl`で暗号化したパスワードを使用することをお勧めします。データベースパスワードが空の場合は、暗号化する必要はありません。プレーンテキストパスワードの暗号化方法については、 [dmctlを使用してデータベースパスワードを暗号化する](/dm/dm-manage-source.md#encrypt-the-database-password)参照してください。

さらに、上流データベースと下流データベースのユーザーには、対応する読み取り権限と書き込み権限が必要です。データ移行タスクを開始する際には、データ移行も[対応する権限を自動的に事前チェックします](/dm/dm-precheck.md)必要です。

### <code>load</code>処理ユニットから<code>packet for query is too large. Try adjusting the &#39;max_allowed_packet&#39; variable</code> {#the-code-load-code-processing-unit-reports-the-error-code-packet-for-query-is-too-large-try-adjusting-the-max-allowed-packet-variable-code}

#### 理由 {#reasons}

-   MySQLクライアントとMySQL/TiDBサーバーの両方に`max_allowed_packet`クォータ制限があります。3 `max_allowed_packet`いずれかが制限を超えると、クライアントはエラーメッセージを受け取ります。現在、最新バージョンのDMとTiDBサーバーでは、デフォルト値は`max_allowed_packet`ではなく`64M`です。

-   DM の完全データ インポート処理ユニットは、DM のダンプ処理ユニットによってエクスポートされた SQL ファイルの分割をサポートしていません。

#### ソリューション {#solutions}

-   ダンプ処理ユニットには`extra-args`オプションのうち`statement-size`設定することをお勧めします。

    デフォルトの`--statement-size`設定によると、ダンプ処理ユニットによって生成されるデフォルトのサイズ`Insert Statement`は約`1M`です。このデフォルト設定では、ロード処理ユニットはほとんどの場合、エラー`packet for query is too large. Try adjusting the 'max_allowed_packet' variable`報告しません。

    データダンプ中に、以下のログが`WARN`出力されることがあります。この`WARN`はダンプ処理には影響しません。これは、幅の広いテーブルがダンプされたことを示しているだけです。

        Row bigger than statement_size for xxx

-   ワイドテーブルの単一行が`64M`超える場合は、次の設定を変更し、設定が有効になっていることを確認する必要があります。

    -   TiDBサーバーで`set @@global.max_allowed_packet=134217728` （ `134217728` =128MB）を実行します。

    -   まず、DMタスク設定ファイルのセクション`target-database`に`max-allowed-packet: 134217728` （128MB）を追加します。次に、コマンド`stop-task`を実行し、コマンド`start-task`実行します。
