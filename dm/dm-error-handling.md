---
title: Handle Errors in TiDB Data Migration
summary: Learn about the error system and how to handle common errors when you use DM.
---

# TiDB データ移行におけるエラーの処理 {#handle-errors-in-tidb-data-migration}

このドキュメントでは、DM 使用時のエラー システムと一般的なエラーの処理方法を紹介します。

## エラーシステム {#error-system}

エラー システムでは、通常、特定のエラーの情報は次のとおりです。

-   `code` : エラーコード。

    DM は、同じエラー タイプに対して同じエラー コードを使用します。 DMのバージョンが変わってもエラーコードは変わりません。

    一部のエラーは DM の反復中に削除される可能性がありますが、エラー コードは削除されません。 DM は、新しいエラーに対して既存のエラー コードではなく新しいエラー コードを使用します。

-   `class` : エラーの種類。

    これは、エラーが発生したコンポーネント(エラーソース) をマークするために使用されます。

    次の表に、すべてのエラー タイプ、エラー ソース、およびエラー サンプルを示します。

    | エラーの種類            | エラーの原因                                               | エラーサンプル                                                                                                                                                                                                                                                                                          |
    | :---------------- | :--------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `database`        | データベース操作                                             | `[code=10003:class=database:scope=downstream:level=medium] database driver: invalid connection`                                                                                                                                                                                                  |
    | `functional`      | DMの基本的な関数                                            | `[code=11005:class=functional:scope=internal:level=high] not allowed operation: alter multiple tables in one statement`                                                                                                                                                                          |
    | `config`          | 間違った構成                                               | `[code=20005:class=config:scope=internal:level=medium] empty source-id not valid`                                                                                                                                                                                                                |
    | `binlog-op`       | Binlog操作                                             | `[code=22001:class=binlog-op:scope=internal:level=high] empty UUIDs not valid`                                                                                                                                                                                                                   |
    | `checkpoint`      | チェックポイント操作                                           | `[code=24002:class=checkpoint:scope=internal:level=high] save point bin.1234 is older than current pos bin.1371`                                                                                                                                                                                 |
    | `task-check`      | タスクチェックを実行する                                         | `[code=26003:class=task-check:scope=internal:level=medium] new table router error`                                                                                                                                                                                                               |
    | `relay-event-lib` | リレーモジュールの基本関数の実行                                     | `[code=28001:class=relay-event-lib:scope=internal:level=high] parse server-uuid.index`                                                                                                                                                                                                           |
    | `relay-unit`      | 中継処理装置                                               | `[code=30015:class=relay-unit:scope=upstream:level=high] TCPReader get event: ERROR 1236 (HY000): Could not open log file`                                                                                                                                                                       |
    | `dump-unit`       | ダンプ処理ユニット                                            | `[code=32001:class=dump-unit:scope=internal:level=high] mydumper runs with error: CRITICAL **: 15:12:17.559: Error connecting to database: Access denied for user 'root'@'172.17.0.1' (using password: NO)`                                                                                      |
    | `load-unit`       | ロード処理ユニット                                            | `[code=34002:class=load-unit:scope=internal:level=high] corresponding ending of sql: ')' not found`                                                                                                                                                                                              |
    | `sync-unit`       | 同期処理ユニット                                             | `[code=36027:class=sync-unit:scope=internal:level=high] Column count doesn't match value count: 9 (columns) vs 10 (values)`                                                                                                                                                                      |
    | `dm-master`       | DMマスターサービス                                           | `[code=38008:class=dm-master:scope=internal:level=high] grpc request error: rpc error: code = Unavailable desc = all SubConns are in TransientFailure, latest connection error: connection error: desc = "transport: Error while dialing dial tcp 172.17.0.2:8262: connect: connection refused"` |
    | `dm-worker`       | DMワーカーサービス                                           | `[code=40066:class=dm-worker:scope=internal:level=high] ExecuteDDL timeout, try use query-status to query whether the DDL is still blocking`                                                                                                                                                     |
    | `dm-tracer`       | DMトレーササービス                                           | `[code=42004:class=dm-tracer:scope=internal:level=medium] trace event test.1 not found`                                                                                                                                                                                                          |
    | `schema-tracker`  | スキーマトラッカー (増分データ複製中)                                 | `[code=44006:class=schema-tracker:scope=internal:level=high],"cannot track DDL: ALTER TABLE test DROP COLUMN col1"`                                                                                                                                                                              |
    | `scheduler`       | (データ移行タスクの) 操作のスケジュール設定                              | `[code=46001:class=scheduler:scope=internal:level=high],"the scheduler has not started"`                                                                                                                                                                                                         |
    | `dmctl`           | dmctl 内でエラーが発生するか、dmctl が他のコンポーネントと対話するときにエラーが発生します。 | `[code=48001:class=dmctl:scope=internal:level=high],"can not create grpc connection"`                                                                                                                                                                                                            |

-   `scope` : エラー範囲。

    これは、エラーが発生したときに DM オブジェクトのスコープとソースをマークするために使用されます。 `scope` `not-set` 、 `upstream` 、 `downstream` 、および`internal`の 4 つのタイプが含まれます。

    エラーのロジックがアップストリーム データベースとダウンストリーム データベース間のリクエストに直接関係する場合、スコープは`upstream`または`downstream`に設定されます。それ以外の場合は、現在`internal`に設定されています。

-   `level` : エラーレベル。

    エラーの重大度レベル ( `low` 、 `medium` 、および`high`を含む)。

    -   `low`レベルのエラーは通常、ユーザーの操作や誤った入力に関連しています。移行タスクには影響しません。
    -   `medium`レベルのエラーは通常、ユーザー設定に関連しています。新しく開始された一部のサービスに影響します。ただし、既存の DM 移行ステータスには影響しません。
    -   レベル`high`エラーは、移行タスクの中断を避けるために解決する必要があるため、通常は注意が必要です。

-   `message` : エラーの説明。

    エラーの詳細な説明。エラー呼び出しチェーン上のエラー メッセージのすべての追加レイヤーをラップして保存するには、 [エラー.ラップ](https://godoc.org/github.com/pkg/errors#hdr-Adding_context_to_an_error)モードが採用されます。レイヤーでラップされたメッセージ記述は DM のエラーを示し、最レイヤーでラップされたメッセージ記述はエラーの原因を示します。

-   `workaround` : エラー処理メソッド (オプション)

    このエラーの処理方法。一部の確認されたエラー (構成エラーなど) については、DM は対応する手動処理方法を`workaround`に示します。

-   エラースタック情報(オプション)

    DM がエラースタック情報を出力するかどうかは、エラーの重大度と必要性に応じて異なります。エラー スタックには、エラーが発生したときの完全なスタック呼び出し情報が記録されます。基本情報やエラーメッセージからはエラーの原因が特定できない場合は、エラースタックを使用してエラー発生時のコードの実行パスを追跡できます。

エラー コードの完全なリストについては、 [エラーコードリスト](https://github.com/pingcap/dm/blob/master/_utils/terror_gen/errors_release.txt)を参照してください。

## トラブルシューティング {#troubleshooting}

DM の実行中にエラーが発生した場合は、次の手順を実行してこのエラーのトラブルシューティングを行ってください。

1.  `query-status`コマンドを実行してタスクの実行状況とエラー出力を確認します。

2.  エラーに関連するログ ファイルを確認してください。ログ ファイルは DM マスター ノードと DM ワーカー ノード上にあります。エラーに関する重要な情報を取得するには、 [エラーシステム](#error-system)を参照してください。次に、 [一般的なエラーの処理](#handle-common-errors)セクションを確認して解決策を見つけます。

3.  このドキュメントでエラーが説明されておらず、ログを確認したりメトリックを監視したりしても問題を解決できない場合は、 [支持を得ます](/support.md) PingCAP またはコミュニティから問い合わせてください。

4.  エラーが解決したら、dmctl を使用してタスクを再起動します。

    ```bash
    resume-task ${task name}
    ```

ただし、場合によっては、データ移行タスクをリセットする必要があります。詳細は[データ移行タスクをリセットする](/dm/dm-faq.md#how-to-reset-the-data-migration-task)を参照してください。

## 一般的なエラーを処理する {#handle-common-errors}

| エラーコード       | エラーの説明                                                                                                                                                                         | 処理する方法                                                                                                                                                                                                                                                                   |
| :----------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `code=10001` | データベースの異常な動作。                                                                                                                                                                  | エラー メッセージとエラー スタックをさらに分析します。                                                                                                                                                                                                                                             |
| `code=10002` | 基礎となるデータベースからの`bad connection`エラー。これは通常、DM とダウンストリーム TiDB インスタンス間の接続が異常で (ネットワーク障害または TiDB の再起動が原因である可能性があります)、現在要求されているデータが TiDB に送信されていないことを示します。                            | DM は、このようなエラーに対して自動回復機能を提供します。リカバリが長時間にわたって成功しない場合は、ネットワークまたは TiDB のステータスを確認してください。                                                                                                                                                                                      |
| `code=10003` | 基礎となるデータベースからの`invalid connection`エラー。これは通常、DM とダウンストリーム TiDB インスタンスの間の接続が異常であり (ネットワーク障害または TiDB の再起動が原因である可能性があります)、現在要求されているデータの一部が TiDB に送信されていることを示します。                   | DM は、このようなエラーに対して自動回復機能を提供します。長期間にわたって回復が成功しない場合は、エラー メッセージをさらに確認し、実際の状況に基づいて情報を分析してください。                                                                                                                                                                                |
| `code=10005` | `QUERY`種類の SQL ステートメントを実行するときに発生します。                                                                                                                                           |                                                                                                                                                                                                                                                                          |
| `code=10006` | `INSERT` `UPDATE`または`DELETE`タイプの DDL ステートメントおよび DML ステートメントを含む、 `EXECUTE`タイプの SQL ステートメントを実行するときに発生します。詳細なエラー情報については、エラー メッセージを確認してください。通常、データベース操作で返されたエラー コードとエラー情報が含まれています。 |                                                                                                                                                                                                                                                                          |
|              |                                                                                                                                                                                |                                                                                                                                                                                                                                                                          |
| `code=11006` | DM の組み込みパーサーが互換性のない DDL ステートメントを解析するときに発生します。                                                                                                                                  | 解決策については[データ移行 - 互換性のない DDL ステートメント](/dm/dm-faq.md#how-to-handle-incompatible-ddl-statements)を参照してください。                                                                                                                                                                  |
| `code=20010` | タスク構成で指定されたデータベースのパスワードを復号化するときに発生します。                                                                                                                                         | 構成タスクで指定されたダウンストリーム データベースのパスワードが[dmctl を使用して正しく暗号化されている](/dm/dm-manage-source.md#encrypt-the-database-password)であるかどうかを確認します。                                                                                                                                           |
| `code=26002` | タスクチェックでデータベース接続の確立に失敗しました。詳細なエラー情報については、エラー メッセージを確認してください。通常、データベース操作で返されたエラー コードとエラー情報が含まれています。                                                                             | DM-master が配置されているマシンにアップストリームへのアクセス許可があるかどうかを確認します。                                                                                                                                                                                                                     |
| `code=32001` | ダンプ処理装置異常                                                                                                                                                                      | エラー メッセージに`mydumper: argument list too long.`が含まれている場合は、ブロック許可リストに従って`task.yaml`ファイルの Mydumper 引数`extra-args`に`--regex`正規表現を手動で追加して、エクスポートされるテーブルを構成します。たとえば、 `hello`という名前のすべてのテーブルをエクスポートするには、 `--regex '.*\\.hello$'`を追加します。すべてのテーブルをエクスポートするには、 `--regex '.*'`を追加します。 |
| `code=38008` | DM コンポーネント間の gRPC 通信でエラーが発生します。                                                                                                                                                | チェック`class` 。どのコンポーネントの相互作用でエラーが発生したかを調べます。通信エラーの種類を特定します。 gRPC接続確立時にエラーが発生する場合は、通信サーバーが正常に動作しているか確認してください。                                                                                                                                                              |

### <code>invalid connection</code>エラーが返されて移行タスクが中断された場合はどうすればよいですか? {#what-can-i-do-when-a-migration-task-is-interrupted-with-the-code-invalid-connection-code-error-returned}

#### 理由 {#reason}

`invalid connection`エラーは、DM とダウンストリーム TiDB データベース間の接続で異常が発生し (ネットワーク障害、TiDB の再起動、TiKV ビジーなど)、現在のリクエストのデータの一部が TiDB に送信されたことを示します。

#### ソリューション {#solutions}

DM には、移行タスクでデータを下流に同時に移行する機能があるため、タスクが中断されるといくつかのエラーが発生する可能性があります。これらのエラーは、 `query-status`を使用して確認できます。

-   増分レプリケーション プロセス中にエラーが`invalid connection`だけ発生した場合、DM はタスクを自動的に再試行します。
-   バージョンの問題により DM が自動的に再試行しない、または失敗する場合は、 `stop-task`を使用してタスクを停止し、 `start-task`使用してタスクを再開します。

### 移行タスクが<code>driver: bad connection</code>エラーが返されました {#a-migration-task-is-interrupted-with-the-code-driver-bad-connection-code-error-returned}

#### 理由 {#reason}

`driver: bad connection`エラーは、DM と上流の TiDB データベースの間の接続で異常が発生し (ネットワーク障害や TiDB の再起動など)、その時点で現在のリクエストのデータがまだ TiDB に送信されていないことを示します。

#### 解決 {#solution}

現在のバージョンの DM は、エラーが発生した場合に自動的に再試行します。自動リトライをサポートしていない以前のバージョンを使用している場合は、 `stop-task`コマンドを実行してタスクを停止できます。次に`start-task`を実行してタスクを再開します。

### リレー ユニットが<code>event from * in * diff from passed-in event *</code>エラー イベントをスローするか、 <code>get binlog error ERROR 1236 (HY000)</code>やバイナリ チェックサムの不一致などのbinlogエラーの取得または解析に失敗して移行タスクが中断され<code>binlog checksum mismatch, data may be corrupted</code> {#the-relay-unit-throws-error-code-event-from-in-diff-from-passed-in-event-code-or-a-migration-task-is-interrupted-with-failing-to-get-or-parse-binlog-errors-like-code-get-binlog-error-error-1236-hy000-code-and-code-binlog-checksum-mismatch-data-may-be-corrupted-code-returned}

#### 理由 {#reason}

リレー ログのプルまたは増分レプリケーションの DM プロセス中に、アップストリームのbinlogファイルのサイズが**4 GB**を超えると、この 2 つのエラーが発生する可能性があります。

**原因:**リレー ログを書き込むとき、DM はbinlogの位置とbinlogログ ファイルのサイズに基づいてイベント検証を実行し、レプリケートされたbinlogの位置をチェックポイントとして保存する必要があります。ただし、公式の MySQL では、binlogの位置を保存するために`uint32`を使用します。これは、4 GB を超えるbinlogファイルのbinlog位置がオーバーフローし、上記のエラーが発生することを意味します。

#### ソリューション {#solutions}

中継ユニットの場合は、次の解決策を使用して移行を手動で回復します。

1.  エラーが発生したときに、対応するbinlogファイルのサイズが 4GB を超えていたことをアップストリームで特定します。

2.  DM ワーカーを停止します。

3.  アップストリームの対応するbinlogファイルをリレー ログ ファイルとしてリレー ログ ディレクトリにコピーします。

4.  リレー ログ ディレクトリで、次のbinlogファイルから取得するように対応する`relay.meta`ファイルを更新します。 DM-worker に`enable_gtid` ～ `true`指定した場合、 `relay.meta`ファイルを更新するときに、次のbinlogファイルに対応する GTID を変更する必要があります。それ以外の場合は、GTID を変更する必要はありません。

    例: エラーが発生した場合、 `binlog-name = "mysql-bin.004451"`と`binlog-pos = 2453` 。それぞれ`binlog-name = "mysql-bin.004452"`と`binlog-pos = 4`に更新し、 `binlog-gtid` `f0e914ef-54cf-11e7-813d-6c92bf2fa791:1-138218058`に更新します。

5.  DM ワーカーを再起動します。

binlogレプリケーション処理ユニットの場合は、次の解決策を使用して移行を手動で回復します。

1.  エラーが発生したときに、対応するbinlogファイルのサイズが 4GB を超えていたことをアップストリームで特定します。

2.  `stop-task`を使用して移行タスクを停止します。

3.  グローバル チェックポイントの 1 と、ダウンストリーム`dm_meta`データベースの各テーブル チェックポイントの`binlog_name`を、エラーが発生したbinlogファイルの名前に更新します。 `binlog_pos`を、移行が完了した有効な位置の値、たとえば 4 に更新します。

    例: エラーが発生したタスクの名前は`dm_test` 、対応する s `source-id`は`replica-1` 、対応するbinlogファイルは`mysql-bin|000001.004451`です。次のコマンドを実行します。

    ```sql
    UPDATE dm_test_syncer_checkpoint SET binlog_name='mysql-bin|000001.004451', binlog_pos = 4 WHERE id='replica-1';
    ```

4.  再入可能を確保するには、移行タスク構成の`syncers`セクションで`safe-mode: true`を指定します。

5.  `start-task`を使用して移行タスクを開始します。

6.  `query-status`を使用して移行タスクのステータスをビュー。元のエラーの原因となったリレー ログ ファイルの移行が完了したら、 `safe-mode`元の値に復元し、移行タスクを再開できます。

### タスクをクエリするかログを確認すると<code>Access denied for user &#39;root&#39;@&#39;172.31.43.27&#39; (using password: YES)</code>と表示される {#code-access-denied-for-user-root-172-31-43-27-using-password-yes-code-shows-when-you-query-the-task-or-check-the-log}

すべての DM 構成ファイル内のデータベース関連のパスワードには、 `dmctl`で暗号化されたパスワードを使用することをお勧めします。データベースのパスワードが空の場合、暗号化する必要はありません。平文パスワードを暗号化する方法については、 [dmctlを使用してデータベースのパスワードを暗号化する](/dm/dm-manage-source.md#encrypt-the-database-password)を参照してください。

さらに、アップストリームおよびダウンストリーム データベースのユーザーは、対応する読み取りおよび書き込み権限を持っている必要があります。データ移行タスクの開始時にデータ移行も[対応する権限を自動的に事前チェックします](/dm/dm-precheck.md)なります。

### <code>load</code>処理ユニットは<code>packet for query is too large. Try adjusting the &#39;max_allowed_packet&#39; variable</code> {#the-code-load-code-processing-unit-reports-the-error-code-packet-for-query-is-too-large-try-adjusting-the-max-allowed-packet-variable-code}

#### 理由 {#reasons}

-   MySQL クライアントと MySQL/TiDBサーバーの両方のクォータ制限は`max_allowed_packet`です。 `max_allowed_packet`つのいずれかが制限を超えると、クライアントはエラー メッセージを受け取ります。現在、最新バージョンの DM および TiDBサーバーのデフォルト値は`max_allowed_packet` `64M` 。

-   DM の完全データ インポート処理ユニットは、DM のダンプ処理ユニットによってエクスポートされた SQL ファイルの分割をサポートしていません。

#### ソリューション {#solutions}

-   ダンプ処理ユニットには`extra-args`の`statement-size`オプションを設定することをお勧めします。

    デフォルトの`--statement-size`設定によると、ダンプ処理ユニットによって生成されるデフォルトのサイズ`Insert Statement`は約`1M`です。このデフォルト設定では、ほとんどの場合、ロード処理ユニットはエラー`packet for query is too large. Try adjusting the 'max_allowed_packet' variable`を報告しません。

    データ ダンプ中に`WARN`のログを受け取る場合があります。この`WARN`ログはダンプ プロセスには影響しません。これは、幅の広いテーブルがダンプされることを意味するだけです。

        Row bigger than statement_size for xxx

-   幅の広いテーブルの 1 行が`64M`を超える場合は、次の構成を変更し、構成が有効になることを確認する必要があります。

    -   TiDBサーバーで`set @@global.max_allowed_packet=134217728` ( `134217728` = 128 MB) を実行します。

    -   まず、DM タスク構成ファイルの`target-database`セクションに`max-allowed-packet: 134217728` (128 MB) を追加します。次に、 `stop-task`コマンドを実行し、 `start-task`コマンドを実行します。
