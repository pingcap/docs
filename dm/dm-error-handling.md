---
title: Handle Errors
summary: Learn about the error system and how to handle common errors when you use DM.
---

# エラーの処理 {#handle-errors}

このドキュメントでは、エラーシステムと、DMを使用する場合の一般的なエラーの処理方法を紹介します。

## エラーシステム {#error-system}

エラーシステムでは、通常、特定のエラーの情報は次のとおりです。

-   `code` ：エラーコード。

    DMは、同じエラータイプに対して同じエラーコードを使用します。 DMのバージョンが変わってもエラーコードは変わりません。

    一部のエラーはDMの反復中に削除される可能性がありますが、エラーコードは削除されません。 DMは、新しいエラーに対して既存のエラーコードではなく、新しいエラーコードを使用します。

-   `class` ：エラータイプ。

    エラーが発生したコンポーネント（エラーソース）をマークするために使用されます。

    次の表に、すべてのエラータイプ、エラーソース、およびエラーサンプルを示します。

    | エラータイプ            | エラーソース                                  | エラーサンプル                                                                                                                                                                                                                                                                                          |
    | :---------------- | :-------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `database`        | データベース操作                                | `[code=10003:class=database:scope=downstream:level=medium] database driver: invalid connection`                                                                                                                                                                                                  |
    | `functional`      | DMの基本的な機能                               | `[code=11005:class=functional:scope=internal:level=high] not allowed operation: alter multiple tables in one statement`                                                                                                                                                                          |
    | `config`          | 設定が正しくありません                             | `[code=20005:class=config:scope=internal:level=medium] empty source-id not valid`                                                                                                                                                                                                                |
    | `binlog-op`       | ビンログ操作                                  | `[code=22001:class=binlog-op:scope=internal:level=high] empty UUIDs not valid`                                                                                                                                                                                                                   |
    | `checkpoint`      | チェックポイント操作                              | `[code=24002:class=checkpoint:scope=internal:level=high] save point bin.1234 is older than current pos bin.1371`                                                                                                                                                                                 |
    | `task-check`      | タスクチェックの実行                              | `[code=26003:class=task-check:scope=internal:level=medium] new table router error`                                                                                                                                                                                                               |
    | `relay-event-lib` | リレーモジュールの基本機能を実行する                      | `[code=28001:class=relay-event-lib:scope=internal:level=high] parse server-uuid.index`                                                                                                                                                                                                           |
    | `relay-unit`      | リレー処理装置                                 | `[code=30015:class=relay-unit:scope=upstream:level=high] TCPReader get event: ERROR 1236 (HY000): Could not open log file`                                                                                                                                                                       |
    | `dump-unit`       | ダンプ処理装置                                 | `[code=32001:class=dump-unit:scope=internal:level=high] mydumper runs with error: CRITICAL **: 15:12:17.559: Error connecting to database: Access denied for user 'root'@'172.17.0.1' (using password: NO)`                                                                                      |
    | `load-unit`       | 負荷処理装置                                  | `[code=34002:class=load-unit:scope=internal:level=high] corresponding ending of sql: ')' not found`                                                                                                                                                                                              |
    | `sync-unit`       | 同期処理装置                                  | `[code=36027:class=sync-unit:scope=internal:level=high] Column count doesn't match value count: 9 (columns) vs 10 (values)`                                                                                                                                                                      |
    | `dm-master`       | DMマスターサービス                              | `[code=38008:class=dm-master:scope=internal:level=high] grpc request error: rpc error: code = Unavailable desc = all SubConns are in TransientFailure, latest connection error: connection error: desc = "transport: Error while dialing dial tcp 172.17.0.2:8262: connect: connection refused"` |
    | `dm-worker`       | DMワーカーサービス                              | `[code=40066:class=dm-worker:scope=internal:level=high] ExecuteDDL timeout, try use query-status to query whether the DDL is still blocking`                                                                                                                                                     |
    | `dm-tracer`       | DMトレーサーサービス                             | `[code=42004:class=dm-tracer:scope=internal:level=medium] trace event test.1 not found`                                                                                                                                                                                                          |
    | `schema-tracker`  | スキーマトラッカー（増分データレプリケーション中）               | `[code=44006:class=schema-tracker:scope=internal:level=high],"cannot track DDL: ALTER TABLE test DROP COLUMN col1"`                                                                                                                                                                              |
    | `scheduler`       | （データ移行タスクの）スケジューリング操作                   | `[code=46001:class=scheduler:scope=internal:level=high],"the scheduler has not started"`                                                                                                                                                                                                         |
    | `dmctl`           | dmctl内で、または他のコンポーネントと相互作用するときにエラーが発生します | `[code=48001:class=dmctl:scope=internal:level=high],"can not create grpc connection"`                                                                                                                                                                                                            |

-   `scope` ：エラースコープ。

    エラーが発生したときにDMオブジェクトのスコープとソースをマークするために使用されます。 `scope`には、 `not-set` 、および`downstream`の`upstream`つのタイプが含まれ`internal` 。

    エラーのロジックにアップストリームデータベースとダウンストリームデータベース間のリクエストが直接含まれる場合、スコープは`upstream`または`downstream`に設定されます。それ以外の場合は、現在`internal`に設定されています。

-   `level` ：エラーレベル。

    `low` 、および`medium`を含むエラーの重大度`high` 。

    -   `low`レベルのエラーは通常、ユーザーの操作と誤った入力に関連しています。移行タスクには影響しません。
    -   `medium`レベルのエラーは通常、ユーザー構成に関連しています。新しく開始されたサービスに影響します。ただし、既存のDM移行ステータスには影響しません。
    -   `high`レベルのエラーは、移行タスクの中断を回避するために解決する必要があるため、通常は注意が必要です。

-   `message` ：エラーの説明。

    エラーの詳細な説明。エラーメッセージのすべての追加レイヤーをエラーコールチェーンにラップして保存するために、 [エラー。ラップ](https://godoc.org/github.com/pkg/errors#hdr-Adding_context_to_an_error)モードが採用されています。最外層でラップされたメッセージの説明はDMのエラーを示し、最内層でラップされたメッセージの説明はエラーの原因を示します。

-   `workaround` ：エラー処理方法（オプション）

    このエラーの処理方法。一部の確認済みエラー（構成エラーなど）については、DMは対応する手動処理方法を`workaround`で示しています。

-   エラースタック情報（オプション）

    DMがエラースタック情報を出力するかどうかは、エラーの重大度と必要性によって異なります。エラースタックは、エラーが発生したときに完全なスタック呼び出し情報を記録します。基本情報やエラーメッセージからエラーの原因がわからない場合は、エラースタックを使用してエラー発生時のコードの実行パスをたどることができます。

エラーコードの完全なリストについては、 [エラーコードリスト](https://github.com/pingcap/dm/blob/master/_utils/terror_gen/errors_release.txt)を参照してください。

## トラブルシューティング {#troubleshooting}

DMの実行中にエラーが発生した場合は、次の手順を実行してこのエラーのトラブルシューティングを行ってください。

1.  `query-status`コマンドを実行して、タスクの実行状態とエラー出力を確認してください。

2.  エラーに関連するログファイルを確認してください。ログファイルはDM-masterノードとDM-workerノードにあります。エラーに関する重要な情報を取得するには、 [エラーシステム](#error-system)を参照してください。次に、 [一般的なエラーの処理](#handle-common-errors)のセクションをチェックして解決策を見つけます。

3.  エラーがこのドキュメントでカバーされておらず、ログを確認したりメトリックを監視したりしても問題を解決できない場合は、R＆Dに連絡できます。

4.  エラーが解決したら、dmctlを使用してタスクを再開します。

    {{< copyable "" >}}

    ```bash
    resume-task ${task name}
    ```

ただし、場合によっては、データ移行タスクをリセットする必要があります。詳しくは[データ移行タスクをリセットする](/dm/dm-faq.md#how-to-reset-the-data-migration-task)をご覧ください。

## 一般的なエラーを処理する {#handle-common-errors}

| エラーコード       | エラーの説明                                                                                                                                                           | 処理する方法                                                                                                                                                                                                                                                                       |
| :----------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `code=10001` | 異常なデータベース操作。                                                                                                                                                     | エラーメッセージとエラースタックをさらに分析します。                                                                                                                                                                                                                                                   |
| `code=10002` | 基盤となるデータベースからの`bad connection`のエラー。これは通常、DMとダウンストリームTiDBインスタンス間の接続が異常であり（ネットワーク障害、TiDBの再起動などが原因である可能性があります）、現在要求されているデータがTiDBに送信されないことを示します。                     | DMは、このようなエラーの自動回復を提供します。リカバリが長期間成功しない場合は、ネットワークまたはTiDBのステータスを確認してください。                                                                                                                                                                                                       |
| `code=10003` | 基盤となるデータベースからの`invalid connection`のエラー。これは通常、DMとダウンストリームTiDBインスタンス間の接続が異常であり（ネットワーク障害、TiDBの再起動などが原因である可能性があります）、現在要求されているデータの一部がTiDBに送信されていることを示します。             | DMは、このようなエラーの自動回復を提供します。長期間リカバリが成功しない場合は、エラーメッセージをさらに確認し、実際の状況に基づいて情報を分析します。                                                                                                                                                                                                 |
| `code=10005` | `QUERY`型SQLステートメントを実行するときに発生します。                                                                                                                                 |                                                                                                                                                                                                                                                                              |
| `code=10006` | `INSERT` 、または`UPDATE`タイプのDDLステートメントおよびDMLステートメントを含む`EXECUTE`タイプのSQLステートメントを実行するときに発生し`DELETE` 。より詳細なエラー情報については、通常、データベース操作で返されるエラーコードとエラー情報を含むエラーメッセージを確認してください。 |                                                                                                                                                                                                                                                                              |
|              |                                                                                                                                                                  |                                                                                                                                                                                                                                                                              |
| `code=11006` | DMの組み込みパーサーが互換性のないDDLステートメントを解析するときに発生します。                                                                                                                       | 解決策については[データ移行-互換性のないDDLステートメント](/dm/dm-faq.md#how-to-handle-incompatible-ddl-statements)を参照してください。                                                                                                                                                                          |
| `code=20010` | タスク構成で提供されるデータベースパスワードを復号化するときに発生します。                                                                                                                            | 構成タスクで提供されたダウンストリームデータベースのパスワードが[dmctlを使用して正しく暗号化されている](/dm/dm-manage-source.md#encrypt-the-database-password)であるかどうかを確認します。                                                                                                                                                 |
| `code=26002` | タスクチェックはデータベース接続の確立に失敗します。より詳細なエラー情報については、通常、データベース操作で返されるエラーコードとエラー情報を含むエラーメッセージを確認してください。                                                                      | DM-masterが配置されているマシンにアップストリームへのアクセス許可があるかどうかを確認します。                                                                                                                                                                                                                          |
| `code=32001` | 異常なダンプ処理装置                                                                                                                                                       | エラーメッセージに`mydumper: argument list too long.`が含まれている場合は、block-allowリストに従って、 `task.yaml`ファイルのMydumper引数`extra-args`に`--regex`の正規表現を手動で追加して、エクスポートするテーブルを構成します。たとえば、 `hello`という名前のすべてのテーブルをエクスポートするには、 `--regex '.*\\.hello$'`を追加します。すべてのテーブルをエクスポートするには、 `--regex '.*'`を追加します。 |
| `code=38008` | DMコンポーネント間のgRPC通信でエラーが発生します。                                                                                                                                     | `class`を確認してください。どのコンポーネントの相互作用でエラーが発生するかを調べます。通信エラーの種類を判別してください。 gRPC接続の確立時にエラーが発生した場合は、通信サーバーが正常に動作しているか確認してください。                                                                                                                                                          |

### <code>invalid connection</code>エラーが返されて移行タスクが中断された場合はどうすればよいですか？ {#what-can-i-do-when-a-migration-task-is-interrupted-with-the-code-invalid-connection-code-error-returned}

#### 理由 {#reason}

`invalid connection`エラーは、DMとダウンストリームTiDBデータベース間の接続に異常（ネットワーク障害、TiDB再起動、TiKVビジーなど）が発生し、現在の要求のデータの一部がTiDBに送信されたことを示します。

#### ソリューション {#solutions}

DMには、移行タスクでデータをダウンストリームに同時に移行する機能があるため、タスクが中断されると、いくつかのエラーが発生する可能性があります。これらのエラーは、 `query-status`を使用して確認できます。

-   インクリメンタルレプリケーションプロセス中に`invalid connection`のエラーのみが発生した場合、DMはタスクを自動的に再試行します。
-   バージョンの問題が原因でDMが自動的に再試行しない、または再試行に失敗した場合は、 `stop-task`を使用してタスクを停止し、 `start-task`を使用してタスクを再開します。

### 移行タスクが<code>driver: bad connection</code>エラーが返されました {#a-migration-task-is-interrupted-with-the-code-driver-bad-connection-code-error-returned}

#### 理由 {#reason}

`driver: bad connection`エラーは、DMとアップストリームTiDBデータベース間の接続に異常（ネットワーク障害、TiDB再起動など）が発生し、現在の要求のデータがその時点でTiDBに送信されていないことを示します。

#### 解決 {#solution}

DMの現在のバージョンは、エラー時に自動的に再試行します。自動再試行をサポートしていない以前のバージョンを使用している場合は、 `stop-task`コマンドを実行してタスクを停止できます。次に、 `start-task`を実行してタスクを再開します。

### リレーユニットがエラー<code>event from * in * diff from passed-in event *</code>スローするか、移行タスクが中断され、 <code>get binlog error ERROR 1236 (HY000)</code>や<code>binlog checksum mismatch, data may be corrupted</code> {#the-relay-unit-throws-error-code-event-from-in-diff-from-passed-in-event-code-or-a-migration-task-is-interrupted-with-failing-to-get-or-parse-binlog-errors-like-code-get-binlog-error-error-1236-hy000-code-and-code-binlog-checksum-mismatch-data-may-be-corrupted-code-returned}

#### 理由 {#reason}

リレーログプルまたはインクリメンタルレプリケーションのDMプロセス中に、アップストリームbinlogファイルのサイズが**4 GB**を超えると、この2つのエラーが発生する可能性があります。

**原因：**リレーログを書き込む場合、DMはbinlogの位置とbinlogファイルのサイズに基づいてイベント検証を実行し、複製されたbinlogの位置をチェックポイントとして保存する必要があります。ただし、公式のMySQLは`uint32`を使用してbinlogの位置を格納します。これは、4 GBを超えるbinlogファイルのbinlog位置がオーバーフローし、上記のエラーが発生することを意味します。

#### ソリューション {#solutions}

リレーユニットの場合、次のソリューションを使用して手動で移行を回復します。

1.  エラーが発生したときに、対応するbinlogファイルのサイズが4GBを超えたことをアップストリームで識別します。

2.  DMワーカーを停止します。

3.  アップストリームの対応するbinlogファイルをリレーログファイルとしてリレーログディレクトリにコピーします。

4.  リレーログディレクトリで、対応する`relay.meta`のファイルを更新して、次のbinlogファイルからプルします。 DM-workerに`enable_gtid`を指定した場合は、 `true`ファイルを更新するときに、次の`relay.meta`ファイルに対応するGTIDを変更する必要があります。それ以外の場合は、GTIDを変更する必要はありません。

    例：エラーが発生した場合、 `binlog-name = "mysql-bin.004451"`と`binlog-pos = 2453` 。それらをそれぞれ`binlog-name = "mysql-bin.004452"`と`binlog-pos = 4`に更新し、 `binlog-gtid`を`f0e914ef-54cf-11e7-813d-6c92bf2fa791:1-138218058`に更新します。

5.  DMワーカーを再起動します。

binlogレプリケーション処理装置の場合、次のソリューションを使用して手動でマイグレーションをリカバリーします。

1.  エラーが発生したときに、対応するbinlogファイルのサイズが4GBを超えたことをアップストリームで識別します。

2.  `stop-task`を使用して移行タスクを停止します。

3.  グローバルチェックポイントおよびダウンストリーム`dm_meta`データベースの各テーブルチェックポイントの`binlog_name`を、エラーのあるbinlogファイルの名前に更新します。 `binlog_pos`を、移行が完了した有効な位置の値（たとえば、4）に更新します。

    例：エラーのあるタスクの名前は`dm_test` 、対応するs `source-id`は`replica-1` 、対応するbinlogファイルは`mysql-bin|000001.004451`です。次のコマンドを実行します。

    {{< copyable "" >}}

    ```sql
    UPDATE dm_test_syncer_checkpoint SET binlog_name='mysql-bin|000001.004451', binlog_pos = 4 WHERE id='replica-1';
    ```

4.  再入可能を確保するために、移行タスク構成の`syncers`セクションで`safe-mode: true`を指定します。

5.  `start-task`を使用して移行タスクを開始します。

6.  `query-status`を使用して移行タスクのステータスを表示します。 `safe-mode`を元の値に復元し、元のエラートリガーリレーログファイルの移行が完了したら、移行タスクを再開できます。

### <code>Access denied for user &#39;root&#39;@&#39;172.31.43.27&#39; (using password: YES)</code>た。タスクを照会するか、ログを確認すると表示されます {#code-access-denied-for-user-root-172-31-43-27-using-password-yes-code-shows-when-you-query-the-task-or-check-the-log}

すべてのDM構成ファイルのデータベース関連のパスワードには、 `dmctl`で暗号化されたパスワードを使用することをお勧めします。データベースパスワードが空の場合、暗号化する必要はありません。プレーンテキストのパスワードを暗号化する方法については、 [dmctlを使用してデータベースパスワードを暗号化します](/dm/dm-manage-source.md#encrypt-the-database-password)を参照してください。

さらに、アップストリームおよびダウンストリームデータベースのユーザーは、対応する読み取りおよび書き込み権限を持っている必要があります。データ移行タスクの開始時にも[対応する特権を自動的に事前チェックします](/dm/dm-precheck.md)データ移行。

### <code>load</code>処理装置は、 <code>packet for query is too large. Try adjusting the &#39;max_allowed_packet&#39; variable</code> {#the-code-load-code-processing-unit-reports-the-error-code-packet-for-query-is-too-large-try-adjusting-the-max-allowed-packet-variable-code}

#### 理由 {#reasons}

-   MySQLクライアントとMySQL/TiDBサーバーの両方に`max_allowed_packet`のクォータ制限があります。 `max_allowed_packet`が制限を超えると、クライアントはエラーメッセージを受け取ります。現在、最新バージョンのDMおよびTiDBサーバーの場合、デフォルト値の`max_allowed_packet`は`64M`です。

-   DMの完全なデータインポート処理装置は、DMのダンプ処理装置によってエクスポートされたSQLファイルの分割をサポートしていません。

#### ソリューション {#solutions}

-   ダンプ処理装置には、 `extra-args`の`statement-size`オプションを設定することをお勧めします。

    デフォルトの`--statement-size`設定によると、ダンプ処理装置によって生成されるデフォルトのサイズ`Insert Statement`は約`1M`です。このデフォルト設定では、ほとんどの場合、負荷処理装置はエラー`packet for query is too large. Try adjusting the 'max_allowed_packet' variable`を報告しません。

    データダンプ中に次の`WARN`のログを受け取る場合があります。この`WARN`のログは、ダンププロセスには影響しません。これは、幅の広いテーブルがダンプされることを意味するだけです。

    ```
    Row bigger than statement_size for xxx
    ```

-   ワイドテーブルの1行が`64M`を超える場合は、次の構成を変更して、構成が有効になっていることを確認する必要があります。

    -   TiDBサーバーで`set @@global.max_allowed_packet=134217728` （ `134217728` = 128 MB）を実行します。

    -   まず、DMタスク構成ファイルの`target-database`セクションに`max-allowed-packet: 134217728` （128 MB）を追加します。次に、 `stop-task`コマンドを実行し、 `start-task`コマンドを実行します。
