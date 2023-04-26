---
title: Handle Errors in TiDB Data Migration
summary: Learn about the error system and how to handle common errors when you use DM.
---

# TiDB データ移行でエラーを処理する {#handle-errors-in-tidb-data-migration}

このドキュメントでは、エラー システムと、DM を使用する際の一般的なエラーの処理方法を紹介します。

## エラーシステム {#error-system}

エラーシステムでは、通常、特定のエラーの情報は次のとおりです。

-   `code` : エラー コード。

    DM は、同じエラー タイプに対して同じエラー コードを使用します。 DMのバージョンが変わってもエラーコードは変わりません。

    DM 反復中に一部のエラーが除去される可能性がありますが、エラー コードは除去されません。 DM は、新しいエラーに対して既存のエラー コードではなく、新しいエラー コードを使用します。

-   `class` : エラーの種類。

    エラーが発生したコンポーネント(エラー ソース) をマークするために使用されます。

    次の表に、すべてのエラー タイプ、エラー ソース、およびエラー サンプルを示します。

    | エラーの種類            | エラーの原因                                | エラーサンプル                                                                                                                                                                                                                                                                                          |
    | :---------------- | :------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `database`        | データベース操作                              | `[code=10003:class=database:scope=downstream:level=medium] database driver: invalid connection`                                                                                                                                                                                                  |
    | `functional`      | DMの基本関数                               | `[code=11005:class=functional:scope=internal:level=high] not allowed operation: alter multiple tables in one statement`                                                                                                                                                                          |
    | `config`          | 不適切な構成                                | `[code=20005:class=config:scope=internal:level=medium] empty source-id not valid`                                                                                                                                                                                                                |
    | `binlog-op`       | Binlog操作                              | `[code=22001:class=binlog-op:scope=internal:level=high] empty UUIDs not valid`                                                                                                                                                                                                                   |
    | `checkpoint`      | チェックポイント操作                            | `[code=24002:class=checkpoint:scope=internal:level=high] save point bin.1234 is older than current pos bin.1371`                                                                                                                                                                                 |
    | `task-check`      | タスクチェックの実行                            | `[code=26003:class=task-check:scope=internal:level=medium] new table router error`                                                                                                                                                                                                               |
    | `relay-event-lib` | リレーモジュールの基本関数の実行                      | `[code=28001:class=relay-event-lib:scope=internal:level=high] parse server-uuid.index`                                                                                                                                                                                                           |
    | `relay-unit`      | 中継処理ユニット                              | `[code=30015:class=relay-unit:scope=upstream:level=high] TCPReader get event: ERROR 1236 (HY000): Could not open log file`                                                                                                                                                                       |
    | `dump-unit`       | ダンプ処理装置                               | `[code=32001:class=dump-unit:scope=internal:level=high] mydumper runs with error: CRITICAL **: 15:12:17.559: Error connecting to database: Access denied for user 'root'@'172.17.0.1' (using password: NO)`                                                                                      |
    | `load-unit`       | 負荷処理ユニット                              | `[code=34002:class=load-unit:scope=internal:level=high] corresponding ending of sql: ')' not found`                                                                                                                                                                                              |
    | `sync-unit`       | 同期処理ユニット                              | `[code=36027:class=sync-unit:scope=internal:level=high] Column count doesn't match value count: 9 (columns) vs 10 (values)`                                                                                                                                                                      |
    | `dm-master`       | DMマスターサービス                            | `[code=38008:class=dm-master:scope=internal:level=high] grpc request error: rpc error: code = Unavailable desc = all SubConns are in TransientFailure, latest connection error: connection error: desc = "transport: Error while dialing dial tcp 172.17.0.2:8262: connect: connection refused"` |
    | `dm-worker`       | DMワーカーサービス                            | `[code=40066:class=dm-worker:scope=internal:level=high] ExecuteDDL timeout, try use query-status to query whether the DDL is still blocking`                                                                                                                                                     |
    | `dm-tracer`       | DMトレーサーサービス                           | `[code=42004:class=dm-tracer:scope=internal:level=medium] trace event test.1 not found`                                                                                                                                                                                                          |
    | `schema-tracker`  | schema-tracker (増分データ複製時)             | `[code=44006:class=schema-tracker:scope=internal:level=high],"cannot track DDL: ALTER TABLE test DROP COLUMN col1"`                                                                                                                                                                              |
    | `scheduler`       | (データ移行タスクの) 操作のスケジューリング               | `[code=46001:class=scheduler:scope=internal:level=high],"the scheduler has not started"`                                                                                                                                                                                                         |
    | `dmctl`           | dmctl 内で、または他のコンポーネントと対話するときにエラーが発生する | `[code=48001:class=dmctl:scope=internal:level=high],"can not create grpc connection"`                                                                                                                                                                                                            |

-   `scope` : エラー範囲。

    エラーが発生したときに、DM オブジェクトのスコープとソースをマークするために使用されます。 `scope` `not-set` 、 `upstream` 、 `downstream` 、および`internal`の 4 つのタイプが含まれます。

    エラーのロジックがアップストリーム データベースとダウンストリーム データベースの間の要求に直接関係している場合、スコープは`upstream`または`downstream`に設定されます。それ以外の場合、現在は`internal`に設定されています。

-   `level` : エラーレベル。

    `low` 、 `medium` 、および`high`を含む、エラーの重大度レベル。

    -   `low`レベルのエラーは、通常、ユーザーの操作と誤った入力に関連しています。移行タスクには影響しません。
    -   通常、 `medium`レベルのエラーはユーザー構成に関連しています。新しく開始された一部のサービスに影響します。ただし、既存の DM 移行ステータスには影響しません。
    -   `high`レベルのエラーは、移行タスクが中断される可能性を回避するために解決する必要があるため、通常は注意が必要です。

-   `message` : エラーの説明。

    エラーの詳細な説明。エラー コール チェーンのエラー メッセージのすべての追加レイヤーをラップして格納するには、 [エラー。ラップ](https://godoc.org/github.com/pkg/errors#hdr-Adding_context_to_an_error)モードが採用されます。レイヤーでラップされたメッセージの説明は DM のエラーを示し、最レイヤーでラップされたメッセージの説明はエラーのソースを示します。

-   `workaround` : エラー処理方法 (オプション)

    このエラーの処理方法。一部の確認済みエラー (構成エラーなど) については、DM は対応する手動処理方法を`workaround`に示します。

-   エラースタック情報 (オプション)

    DM がエラースタック情報を出力するかどうかは、エラーの重大度と必要性によって異なります。エラー スタックは、エラーが発生したときの完全なスタック呼び出し情報を記録します。基本情報とエラーメッセージからエラー原因が特定できない場合は、エラースタックを使用してエラー発生時のコードの実行経路をたどることができます。

エラー コードの完全なリストについては、 [エラーコード一覧](https://github.com/pingcap/dm/blob/master/_utils/terror_gen/errors_release.txt)を参照してください。

## トラブルシューティング {#troubleshooting}

DM の実行中にエラーが発生した場合は、次の手順に従ってこのエラーをトラブルシューティングします。

1.  `query-status`コマンドを実行して、タスクの実行状況とエラー出力を確認します。

2.  エラーに関連するログ ファイルを確認します。ログ ファイルは、DM-master ノードと DM-worker ノードにあります。エラーに関する重要な情報を取得するには、 [エラーシステム](#error-system)を参照してください。次に、 [一般的なエラーを処理する](#handle-common-errors)セクションを確認して解決策を見つけます。

3.  エラーがこのドキュメントでカバーされておらず、ログを確認したりメトリックを監視したりしても問題を解決できない場合は、PingCAP またはコミュニティから[支持を得ます](/support.md) .

4.  エラーが解決したら、dmctl を使用してタスクを再開します。

    {{< copyable "" >}}

    ```bash
    resume-task ${task name}
    ```

ただし、場合によっては、データ移行タスクをリセットする必要があります。詳細については、 [データ移行タスクのリセット](/dm/dm-faq.md#how-to-reset-the-data-migration-task)を参照してください。

## 一般的なエラーを処理する {#handle-common-errors}

| エラーコード       | エラーの説明                                                                                                                                                                         | 処理する方法                                                                                                                                                                                                                                                                        |
| :----------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `code=10001` | データベースの異常動作。                                                                                                                                                                   | エラー メッセージとエラー スタックをさらに分析します。                                                                                                                                                                                                                                                  |
| `code=10002` | 基になるデータベースからの`bad connection`エラー。これは通常、DM とダウンストリームの TiDB インスタンス間の接続が異常であり (ネットワーク障害または TiDB の再起動が原因である可能性があります)、現在要求されているデータが TiDB に送信されていないことを示しています。                        | DM は、このようなエラーの自動回復を提供します。リカバリが長時間成功しない場合は、ネットワークまたは TiDB のステータスを確認してください。                                                                                                                                                                                                     |
| `code=10003` | 基になるデータベースからの`invalid connection`エラー。これは通常、DM とダウンストリームの TiDB インスタンス間の接続が異常であり (ネットワーク障害または TiDB の再起動が原因である可能性があります)、現在要求されているデータの一部が TiDB に送信されていることを示しています。                  | DM は、このようなエラーの自動回復を提供します。リカバリが長時間成功しない場合は、エラー メッセージをさらに確認し、実際の状況に基づいて情報を分析します。                                                                                                                                                                                                |
| `code=10005` | `QUERY`型SQL文実行時に発生します。                                                                                                                                                         |                                                                                                                                                                                                                                                                               |
| `code=10006` | `EXECUTE`タイプの SQL ステートメント (DDL ステートメントおよび`INSERT` 、 `UPDATE`または`DELETE`タイプの DML ステートメントを含む) を実行するときに発生します。詳細なエラー情報については、通常、データベース操作に対して返されるエラー コードとエラー情報を含むエラー メッセージを確認してください。 |                                                                                                                                                                                                                                                                               |
|              |                                                                                                                                                                                |                                                                                                                                                                                                                                                                               |
| `code=11006` | DM の組み込みパーサーが互換性のない DDL ステートメントを解析するときに発生します。                                                                                                                                  | 解決策は[データ移行 - 互換性のない DDL ステートメント](/dm/dm-faq.md#how-to-handle-incompatible-ddl-statements)を参照してください。                                                                                                                                                                           |
| `code=20010` | タスク構成で指定されたデータベース パスワードを復号化するときに発生します。                                                                                                                                         | 構成タスクで指定されたダウンストリーム データベースのパスワードが[dmctl を使用して正しく暗号化されている](/dm/dm-manage-source.md#encrypt-the-database-password)かどうかを確認します。                                                                                                                                                   |
| `code=26002` | タスク チェックは、データベース接続の確立に失敗します。詳細なエラー情報については、通常、データベース操作に対して返されるエラー コードとエラー情報を含むエラー メッセージを確認してください。                                                                               | DM-master が配置されているマシンにアップストリームへのアクセス権限があるかどうかを確認します。                                                                                                                                                                                                                          |
| `code=32001` | 異常ダンプ処理部                                                                                                                                                                       | エラー メッセージに`mydumper: argument list too long.`が含まれている場合は、ブロック許可リストに従って、 `task.yaml`ファイルの Mydumper 引数`extra-args`に`--regex`正規表現を手動で追加して、テーブルがエクスポートされるように構成します。たとえば、 `hello`という名前のすべてのテーブルをエクスポートするには、 `--regex '.*\\.hello$'`を追加します。すべてのテーブルをエクスポートするには、 `--regex '.*'`を追加します。 |
| `code=38008` | DM コンポーネント間の gRPC 通信でエラーが発生します。                                                                                                                                                | `class`を確認してください。どのコンポーネントの相互作用でエラーが発生するかを調べます。通信エラーのタイプを判別してください。 gRPC接続時にエラーが発生する場合は、通信サーバーが正常に動作しているか確認してください。                                                                                                                                                             |

### <code>invalid connection</code>エラーが返されて移行タスクが中断された場合、どうすればよいですか? {#what-can-i-do-when-a-migration-task-is-interrupted-with-the-code-invalid-connection-code-error-returned}

#### 理由 {#reason}

`invalid connection`エラーは、DM と下流の TiDB データベース間の接続に異常 (ネットワーク障害、TiDB 再起動、TiKV ビジーなど) が発生し、現在の要求のデータの一部が TiDB に送信されたことを示します。

#### ソリューション {#solutions}

DM には、移行タスクでデータを下流に同時に移行する機能があるため、タスクが中断されると、いくつかのエラーが発生する可能性があります。これらのエラーは、 `query-status`を使用して確認できます。

-   増分レプリケーション プロセス中にエラーが`invalid connection`だけ発生した場合、DM はタスクを自動的に再試行します。
-   バージョンの問題が原因で DM が自動的に再試行しない場合、または失敗した場合は、 `stop-task`を使用してタスクを停止し、 `start-task`を使用してタスクを再開します。

### 移行タスクが<code>driver: bad connection</code>エラーが返されました {#a-migration-task-is-interrupted-with-the-code-driver-bad-connection-code-error-returned}

#### 理由 {#reason}

`driver: bad connection`エラーは、DM と上流の TiDB データベースとの間の接続に異常 (ネットワーク障害や TiDB の再起動など) が発生し、その時点で現在の要求のデータがまだ TiDB に送信されていないことを示します。

#### 解決 {#solution}

DM の現在のバージョンでは、エラーが発生すると自動的に再試行されます。自動再試行をサポートしていない以前のバージョンを使用している場合は、 `stop-task`コマンドを実行してタスクを停止できます。その後、 `start-task`を実行してタスクを再開します。

### リレー ユニットが<code>event from * in * diff from passed-in event *</code>スローするか、 <code>get binlog error ERROR 1236 (HY000)</code>や<code>binlog checksum mismatch, data may be corrupted</code>などのbinlogエラーの取得または解析に失敗して移行タスクが中断されます。 {#the-relay-unit-throws-error-code-event-from-in-diff-from-passed-in-event-code-or-a-migration-task-is-interrupted-with-failing-to-get-or-parse-binlog-errors-like-code-get-binlog-error-error-1236-hy000-code-and-code-binlog-checksum-mismatch-data-may-be-corrupted-code-returned}

#### 理由 {#reason}

リレー ログのプルまたは増分レプリケーションの DM プロセス中に、上流のbinlogファイルのサイズが**4 GB**を超えると、この 2 つのエラーが発生する可能性があります。

**原因:**リレー ログを書き込むとき、DM はbinlog の位置とbinlogファイルのサイズに基づいてイベント検証を実行し、レプリケートされたbinlog の位置をチェックポイントとして保存する必要があります。ただし、公式の MySQL は`uint32`を使用してbinlogの位置を保存します。これは、 binlogファイルのbinlog位置が 4 GB を超えてオーバーフローし、上記のエラーが発生することを意味します。

#### ソリューション {#solutions}

リレー ユニットの場合は、次の解決策を使用して移行を手動で回復します。

1.  エラーが発生した時点で、対応するbinlogファイルのサイズが 4GB を超えていることをアップストリームで特定します。

2.  DM ワーカーを停止します。

3.  アップストリームの対応するbinlogファイルをリレー ログ ファイルとしてリレー ログ ディレクトリにコピーします。

4.  リレー ログ ディレクトリで、対応する`relay.meta`ファイルを更新して、次のbinlogファイルからプルします。 DM-worker に`enable_gtid` ～ `true`指定した場合は、 `relay.meta`ファイルの更新時に次のbinlogファイルに対応する GTID を変更する必要があります。それ以外の場合、GTID を変更する必要はありません。

    例: エラーが発生した場合、 `binlog-name = "mysql-bin.004451"`と`binlog-pos = 2453` .それらをそれぞれ`binlog-name = "mysql-bin.004452"`と`binlog-pos = 4`に更新し、 `binlog-gtid`を`f0e914ef-54cf-11e7-813d-6c92bf2fa791:1-138218058`に更新します。

5.  DM-worker を再起動します。

binlogレプリケーション処理ユニットの場合、次のソリューションを使用して移行を手動で回復します。

1.  エラーが発生した時点で、対応するbinlogファイルのサイズが 4GB を超えていることをアップストリームで特定します。

2.  `stop-task`を使用して移行タスクを停止します。

3.  グローバル チェックポイントおよびダウンストリーム`dm_meta`データベースの各テーブル チェックポイントの`binlog_name`を、エラーが発生したbinlogファイルの名前に更新します。 `binlog_pos`移行が完了した有効な位置の値 (4 など) に更新します。

    例: エラーのあるタスクの名前は`dm_test` 、対応する s `source-id`は`replica-1` 、対応するbinlogファイルは`mysql-bin|000001.004451`です。次のコマンドを実行します。

    {{< copyable "" >}}

    ```sql
    UPDATE dm_test_syncer_checkpoint SET binlog_name='mysql-bin|000001.004451', binlog_pos = 4 WHERE id='replica-1';
    ```

4.  移行タスク構成の`syncers`セクションで`safe-mode: true`を指定して、再入可能にします。

5.  `start-task`を使用して移行タスクを開始します。

6.  `query-status`を使用して、移行タスクのステータスをビュー。元のエラー トリガー リレー ログ ファイルの移行が完了したら、 `safe-mode`元の値に復元し、移行タスクを再開できます。

### <code>Access denied for user &#39;root&#39;@&#39;172.31.43.27&#39; (using password: YES)</code>タスクを照会するか、ログを確認すると表示されます {#code-access-denied-for-user-root-172-31-43-27-using-password-yes-code-shows-when-you-query-the-task-or-check-the-log}

すべての DM 構成ファイルのデータベース関連のパスワードについては、 `dmctl`で暗号化されたパスワードを使用することをお勧めします。データベースのパスワードが空の場合、暗号化する必要はありません。平文パスワードを暗号化する方法については、 [dmctl を使用してデータベース パスワードを暗号化する](/dm/dm-manage-source.md#encrypt-the-database-password)を参照してください。

さらに、アップストリーム データベースとダウンストリーム データベースのユーザーには、対応する読み取り権限と書き込み権限が必要です。データ移行タスクの開始中にデータ移行も[対応する権限を自動的に事前チェックします](/dm/dm-precheck.md)なります。

### <code>load</code>処理ユニットは<code>packet for query is too large. Try adjusting the &#39;max_allowed_packet&#39; variable</code> {#the-code-load-code-processing-unit-reports-the-error-code-packet-for-query-is-too-large-try-adjusting-the-max-allowed-packet-variable-code}

#### 理由 {#reasons}

-   MySQL クライアントと MySQL/TiDBサーバーの両方に`max_allowed_packet`のクォータ制限があります。いずれかの`max_allowed_packet`制限を超えると、クライアントはエラー メッセージを受け取ります。現在、DM および TiDBサーバーの最新バージョンでは、デフォルト値の`max_allowed_packet`は`64M`です。

-   DM のフル データ インポート処理ユニットは、DM の Dump 処理ユニットによってエクスポートされた SQL ファイルの分割をサポートしていません。

#### ソリューション {#solutions}

-   ダンプ処理ユニットには`extra-args`の`statement-size`オプションを設定することをお勧めします。

    デフォルトの`--statement-size`設定によれば、Dump 処理ユニットによって生成されるデフォルトのサイズ`Insert Statement`は約`1M`です。このデフォルト設定では、ほとんどの場合、ロード処理ユニットはエラー`packet for query is too large. Try adjusting the 'max_allowed_packet' variable`を報告しません。

    データ ダンプ中に次の`WARN`ログを受け取る場合があります。この`WARN`ログは、ダンプ プロセスには影響しません。これは、幅の広いテーブルがダンプされることを意味するだけです。

    ```
    Row bigger than statement_size for xxx
    ```

-   ワイド テーブルの 1 行が`64M`を超える場合は、次の構成を変更し、構成が有効になるようにする必要があります。

    -   TiDBサーバーで`set @@global.max_allowed_packet=134217728` ( `134217728` = 128 MB) を実行します。

    -   まず、DM タスク構成ファイルの`target-database`セクションに`max-allowed-packet: 134217728` (128 MB) を追加します。次に、 `stop-task`コマンドを実行し、 `start-task`コマンドを実行します。
