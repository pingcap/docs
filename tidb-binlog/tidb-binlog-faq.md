---
title: TiDB Binlog FAQ
summary: Learn about the frequently asked questions (FAQs) and answers about TiDB Binlog.
---

# TiDB Binlog FAQ {#tidb-binlog-faq}

このドキュメントは、TiDB Binlogに関するよくある質問（FAQ）を集めたものです。

## TiDB Binlogを有効にすると、TiDBのパフォーマンスにどのような影響がありますか？ {#what-is-the-impact-of-enabling-tidb-binlog-on-the-performance-of-tidb}

-   クエリへの影響はありません。

-   `INSERT` 、および`DELETE`のトランザクションにはわずかなパフォーマンスの影響があり`UPDATE` 。レイテンシーでは、トランザクションがコミットされる前に、TiKVプリライトステージでp-binlogが同時に書き込まれます。一般に、binlogの書き込みはTiKVの事前書き込みよりも高速であるため、レイテンシーは増加しません。ポンプの監視パネルでbinlogの書き込みの応答時間を確認できます。

## TiDB Binlogのレプリケーションレイテンシはどのくらいですか？ {#how-high-is-the-replication-latency-of-tidb-binlog}

TiDB Binlogレプリケーションの遅延は秒単位で測定されます。これは、通常、オフピーク時に約3秒です。

## DrainerがダウンストリームのMySQLまたはTiDBクラスタにデータを複製するために必要な特権は何ですか？ {#what-privileges-does-drainer-need-to-replicate-data-to-the-downstream-mysql-or-tidb-cluster}

ダウンストリームのMySQLまたはTiDBクラスタにデータを複製するには、Drainerに次の権限が必要です。

-   入れる
-   アップデート
-   消去
-   作成
-   落とす
-   変更
-   実行する
-   索引
-   選択する

## ポンプディスクがほぼいっぱいになった場合はどうすればよいですか？ {#what-can-i-do-if-the-pump-disk-is-almost-full}

1.  PumpのGCが正常に機能するかどうかを確認します。

    -   Pumpの監視パネルの**gc_tso**時間が設定ファイルの時間と同じであるかどうかを確認します。

2.  GCが正常に機能する場合は、次の手順を実行して、単一のポンプに必要なスペースの量を減らします。

    -   Pumpの**GC**パラメータを変更して、データを保持する日数を減らします。

    -   ポンプインスタンスを追加します。

## ドレイナーの複製が中断された場合はどうすればよいですか？ {#what-can-i-do-if-drainer-replication-is-interrupted}

次のコマンドを実行して、Pumpのステータスが正常であるかどうか、および`offline`状態にないすべてのPumpインスタンスが実行されているかどうかを確認します。

{{< copyable "" >}}

```bash
binlogctl -cmd pumps
```

次に、Drainerモニターまたはログが対応するエラーを出力するかどうかを確認します。もしそうなら、それに応じてそれらを解決します。

## DrainerがダウンストリームのMySQLまたはTiDBクラスタにデータを複製するのが遅い場合はどうすればよいですか？ {#what-can-i-do-if-drainer-is-slow-to-replicate-data-to-the-downstream-mysql-or-tidb-cluster}

次の監視項目を確認してください。

-   **Drainer Event**モニタリングメトリックについては、Drainerが`DELETE`秒あたり`INSERT` 、および`UPDATE`トランザクションをダウンストリームに複製する速度を確認してください。

-   **SQLクエリ時間**の監視メトリックについては、DrainerがダウンストリームでSQLステートメントを実行するのにかかる時間を確認してください。

複製が遅い場合の考えられる原因と解決策：

-   レプリケートされたデータベースに主キーまたは一意のインデックスのないテーブルが含まれている場合は、テーブルに主キーを追加します。

-   Drainerとダウンストリームの間のレイテンシーが高い場合は、Drainerの`worker-count`パラメーターの値を増やします。データセンター間のレプリケーションでは、Drainerをダウンストリームにデプロイすることをお勧めします。

-   下流の負荷が高くない場合は、Drainerの`worker-count`パラメータの値を大きくしてください。

## Pumpインスタンスがクラッシュした場合はどうすればよいですか？ {#what-can-i-do-if-a-pump-instance-crashes}

Pumpインスタンスがクラッシュした場合、Drainerはこのインスタンスのデータを取得できないため、データをダウンストリームに複製できません。このPumpインスタンスが通常の状態に回復できる場合、Drainerはレプリケーションを再開します。そうでない場合は、次の手順を実行します。

1.  [binlogctlを使用して、このPumpインスタンスの状態を`offline`に変更します](/tidb-binlog/maintain-tidb-binlog-cluster.md)を使用して、このPumpインスタンスのデータを破棄します。

2.  Drainerはこのポンプインスタンスのデータを取得できないため、ダウンストリームとアップストリームのデータに一貫性がありません。この状況では、完全バックアップと増分バックアップを再度実行してください。手順は次のとおりです。

    1.  ドレイナーを停止します。

    2.  アップストリームで完全バックアップを実行します。

    3.  `tidb_binlog.checkpoint`のテーブルを含むダウンストリームのデータをクリアします。

    4.  フルバックアップをダウンストリームに復元します。

    5.  Drainerをデプロイし、最初のレプリケーションの開始点として`initialCommitTs` （完全バックアップのスナップショットタイムスタンプとして`initialCommitTs`を設定）を使用します。

## チェックポイントとは何ですか？ {#what-is-checkpoint}

チェックポイントは、Drainerがダウンストリームに複製する`commit-ts`を記録します。 Drainerが再起動すると、チェックポイントを読み取り、対応する`commit-ts`から開始してデータをダウンストリームに複製します。 `["write save point"] [ts=411222863322546177]` Drainerログは、対応するタイムスタンプとともにチェックポイントを保存することを意味します。

チェックポイントは、さまざまなタイプのダウンストリームプラットフォームに対してさまざまな方法で保存されます。

-   MySQL / TiDBの場合、 `tidb_binlog.checkpoint`のテーブルに保存されます。

-   Kafka / fileの場合、対応する構成ディレクトリのファイルに保存されます。

kafka / fileのデータには`commit-ts`が含まれているため、チェックポイントが失われた場合、ダウンストリームで最新のデータを使用することにより、ダウンストリームデータの最新の`commit-ts`をチェックできます。

ドレイナーは、開始時にチェックポイントを読み取ります。 Drainerがチェックポイントを読み取れない場合は、構成された`initialCommitTs`を初期レプリケーションの開始点として使用します。

## Drainerに障害が発生し、ダウンストリームのデータが残っている場合に、Drainerを新しいマシンに再デプロイするにはどうすればよいですか？ {#how-to-redeploy-drainer-on-the-new-machine-when-drainer-fails-and-the-data-in-the-downstream-remains}

ダウンストリームのデータが影響を受けない場合は、対応するチェックポイントからデータを複製できる限り、新しいマシンにDrainerを再デプロイできます。

-   チェックポイントが失われていない場合は、次の手順を実行します。

    1.  新しいDrainerをデプロイして開始します（Drainerはチェックポイントを読み取り、レプリケーションを再開できます）。

    2.  [binlogctlを使用して、古いDrainerの状態を`offline`に変更します](/tidb-binlog/maintain-tidb-binlog-cluster.md)を使用します。

-   チェックポイントが失われた場合は、次の手順を実行します。

    1.  新しいドレイナーを配置するには、古いドレイナーの`commit-ts`つを新しいドレイナーの`initialCommitTs`として取得します。

    2.  [binlogctlを使用して、古いDrainerの状態を`offline`に変更します](/tidb-binlog/maintain-tidb-binlog-cluster.md)を使用します。

## フルバックアップとbinlogバックアップファイルを使用してクラスタのデータを復元するにはどうすればよいですか？ {#how-to-restore-the-data-of-a-cluster-using-a-full-backup-and-a-binlog-backup-file}

1.  クラスタをクリーンアップし、完全バックアップを復元します。

2.  バックアップファイルの最新データを復元するには、Reparoを使用して`start-tso` ={完全バックアップのスナップショットタイムスタンプ+1}および`end-ts` =0に設定します（または、特定の時点を指定できます）。

## プライマリ-セカンダリレプリケーションで<code>ignore-error</code>を有効にすると、重大なエラーが発生する場合にDrainerを再デプロイするにはどうすればよいですか？ {#how-to-redeploy-drainer-when-enabling-code-ignore-error-code-in-primary-secondary-replication-triggers-a-critical-error}

`ignore-error`を有効にした後でTiDBがbinlogの書き込みに失敗したときに重大なエラーがトリガーされた場合、TiDBはbinlogの書き込みを停止し、binlogデータの損失が発生します。レプリケーションを再開するには、次の手順を実行します。

1.  Drainerインスタンスを停止します。

2.  クリティカルエラーをトリガーした`tidb-server`つのインスタンスを再起動し、binlogの書き込みを再開します（クリティカルエラーがトリガーされた後、TiDBはPumpにbinlogを書き込みません）。

3.  アップストリームで完全バックアップを実行します。

4.  `tidb_binlog.checkpoint`のテーブルを含むダウンストリームのデータをクリアします。

5.  フルバックアップをダウンストリームに復元します。

6.  Drainerをデプロイし、最初のレプリケーションの開始点として`initialCommitTs` （完全バックアップのスナップショットタイムスタンプとして`initialCommitTs`を設定）を使用します。

## ポンプまたはドレイナーノードを一時停止または閉じることができるのはいつですか？ {#when-can-i-pause-or-close-a-pump-or-drainer-node}

ポンプまたはドレイナーの状態の説明と、プロセスを開始および終了する方法については、 [TiDBBinlogクラスターの操作](/tidb-binlog/maintain-tidb-binlog-cluster.md)を参照してください。

サービスを一時的に停止する必要がある場合は、ポンプノードまたはドレイナーノードを一時停止します。例えば：

-   バージョンアップグレード

    プロセスが停止した後、新しいバイナリを使用してサービスを再開します。

-   サーバのメンテナンス

    サーバーがダウンタイムのメンテナンスを必要とする場合は、プロセスを終了し、メンテナンスの終了後にサービスを再開します。

サービスが不要になったら、ポンプノードまたはドレイナーノードを閉じます。例えば：

-   ポンプスケールイン

    あまり多くのポンプサービスを必要としない場合は、それらのいくつかを閉じます。

-   レプリケーションタスクのキャンセル

    データをダウンストリームデータベースに複製する必要がなくなった場合は、対応するDrainerノードを閉じます。

-   サービスの移行

    サービスを別のサーバーに移行する必要がある場合は、サービスを閉じて、新しいサーバーに再デプロイします。

## ポンプまたはドレイナープロセスを一時停止するにはどうすればよいですか？ {#how-can-i-pause-a-pump-or-drainer-process}

-   プロセスを直接強制終了します。

    > **ノート：**
    >
    > `kill -9`コマンドは使用しないでください。そうしないと、PumpまたはDrainerノードは信号を処理できません。

-   PumpまたはDrainerノードがフォアグラウンドで実行されている場合は、 <kbd>Ctrl</kbd> + <kbd>C</kbd>を押して一時停止します。

-   binlogctlで`pause-pump`または`pause-drainer`コマンドを使用します。

## binlogctlで<code>update-pump</code>または<code>update-drainer</code> drainerコマンドを使用して、PumpまたはDrainerサービスを一時停止できますか？ {#can-i-use-the-code-update-pump-code-or-code-update-drainer-code-command-in-binlogctl-to-pause-the-pump-or-drainer-service}

いいえ`update-pump`または`update-drainer`コマンドは、対応する操作を実行するようにポンプまたはドレイナーに通知することなく、PDに保存されている状態情報を直接変更します。 2つのコマンドを誤用すると、データレプリケーションが中断され、データが失われる可能性があります。

## binlogctlで<code>update-pump</code>または<code>update-drainer</code> drainerコマンドを使用して、PumpまたはDrainerサービスを閉じることはできますか？ {#can-i-use-the-code-update-pump-code-or-code-update-drainer-code-command-in-binlogctl-to-close-the-pump-or-drainer-service}

いいえ`update-pump`または`update-drainer`コマンドは、対応する操作を実行するようにポンプまたはドレイナーに通知することなく、PDに保存されている状態情報を直接変更します。 2つのコマンドを誤用すると、データレプリケーションが中断され、データの不整合が発生する可能性があります。例えば：

-   Pumpノードが正常に実行されているか`paused`状態にある場合、 `update-pump`コマンドを使用してPump状態を`offline`に設定すると、Drainerノードは7Pumpからの`offline`データのプルを停止します。この状況では、最新のbinlogをDrainerノードに複製できず、アップストリームとダウンストリームの間でデータの不整合が発生します。
-   Drainerノードが正常に実行されているときに、 `update-drainer`コマンドを使用してDrainer状態を`offline`に設定すると、新しく開始されたPumpノードは`online`状態のDrainerノードにのみ通知します。この状況では、 `offline` DrainerはPumpノードからbinlogデータを時間内にプルできず、アップストリームとダウンストリームの間でデータの不整合が発生します。

## binlogctlの<code>update-pump</code>コマンドを使用して、ポンプの状態を<code>paused</code>に設定できるのはいつですか。 {#when-can-i-use-the-code-update-pump-code-command-in-binlogctl-to-set-the-pump-state-to-code-paused-code}

いくつかの異常な状況では、ポンプはその状態を正しく維持できません。次に、 `update-pump`コマンドを使用して状態を変更します。

たとえば、Pumpプロセスが異常終了した場合（パニックが発生したときにプロセスを直接終了した場合、または誤って`kill -9`コマンドを使用してプロセスを強制終了した場合）、PDに保存されたPump状態情報は`online`のままです。この状況で、現時点でサービスを回復するためにPumpを再起動する必要がない場合は、 `update-pump`コマンドを使用してPumpの状態を`paused`に更新します。そうすれば、TiDBがbinlogを書き込み、Drainerがbinlogをプルするときに中断を回避できます。

## binlogctlの<code>update-drainer</code> drainerコマンドを使用して、Drainerの状態を<code>paused</code>に設定できるのはいつですか。 {#when-can-i-use-the-code-update-drainer-code-command-in-binlogctl-to-set-the-drainer-state-to-code-paused-code}

一部の異常な状況では、Drainerノードがその状態を正しく維持できず、レプリケーションタスクに影響を及ぼしています。次に、 `update-drainer`コマンドを使用して状態を変更します。

たとえば、Drainerプロセスが異常終了した場合（パニックが発生したときにプロセスを直接終了した場合、または誤って`kill -9`コマンドを使用してプロセスを強制終了した場合）、PDに保存されたDrainer状態情報は`online`のままです。ポンプノードが開始されると、終了したドレイナーノードへの通知に失敗し（ `notify drainer ...`エラー）、ポンプノードに障害が発生します。この状況では、 `update-drainer`コマンドを使用してDrainerの状態を`paused`に更新し、Pumpノードを再起動します。

## ポンプまたはドレイナーノードを閉じるにはどうすればよいですか？ {#how-can-i-close-a-pump-or-drainer-node}

現在、binlogctlの`offline-pump`または`offline-drainer`コマンドのみを使用して、PumpまたはDrainerノードを閉じることができます。

## binlogctlで<code>update-pump</code>コマンドを使用して、ポンプの状態を<code>offline</code>に設定できるのはいつですか。 {#when-can-i-use-the-code-update-pump-code-command-in-binlogctl-to-set-the-pump-state-to-code-offline-code}

次の状況では、 `update-pump`コマンドを使用してポンプ状態を`offline`に設定できます。

-   Pumpプロセスが異常終了し、サービスを回復できない場合、レプリケーションタスクは中断されます。レプリケーションを回復し、binlogデータの損失を受け入れる場合は、 `update-pump`コマンドを使用してPump状態を`offline`に設定します。次に、DrainerノードはPumpノードからのbinlogのプルを停止し、データの複製を続行します。
-   いくつかの古いポンプノードは、履歴タスクから残されています。それらのプロセスは終了し、それらのサービスはもはや必要ありません。次に、 `update-pump`コマンドを使用して状態を`offline`に設定します。

その他の状況では、 `offline-pump`コマンドを使用して、通常のプロセスであるポンプサービスを閉じます。

> **警告：**
>
> > binlogデータの損失とアップストリームとダウンストリーム間のデータの不整合を許容できる場合、またはポンプノードに保存されているbinlogデータが不要になった場合を除いて、 `update-pump`コマンドを使用しないでください。

## 終了して<code>paused</code>に設定されているPumpノードを閉じたい場合、binlogctlの<code>update-pump</code>コマンドを使用してPump状態を<code>offline</code>に設定できますか？ {#can-i-use-the-code-update-pump-code-command-in-binlogctl-to-set-the-pump-state-to-code-offline-code-if-i-want-to-close-a-pump-node-that-is-exited-and-set-to-code-paused-code}

Pumpプロセスが終了し、ノードが`paused`状態の場合、ノード内のすべてのbinlogデータがそのダウンストリームのDrainerノードで消費されるわけではありません。したがって、そうすると、アップストリームとダウンストリームの間でデータの不整合が発生する可能性があります。この状況では、Pumpを再起動し、 `offline-pump`コマンドを使用してPumpノードを閉じます。

## binlogctlの<code>update-drainer</code> drainerコマンドを使用して、Drainerの状態を<code>offline</code>に設定できるのはいつですか。 {#when-can-i-use-the-code-update-drainer-code-command-in-binlogctl-to-set-the-drainer-state-to-code-offline-code}

いくつかの古いDrainerノードは、履歴タスクから残されています。それらのプロセスは終了し、それらのサービスはもはや必要ありません。次に、 `update-drainer`コマンドを使用して状態を`offline`に設定します。

## <code>change pump</code>の<code>change drainer</code>やドレイナーの変更などのSQL操作を使用して、ポンプまたはドレイナーサービスを一時停止または閉じることはできますか？ {#can-i-use-sql-operations-such-as-code-change-pump-code-and-code-change-drainer-code-to-pause-or-close-the-pump-or-drainer-service}

いいえ。これらのSQL操作の詳細については、 [SQLステートメントを使用してPumpまたはDrainerを管理する](/tidb-binlog/maintain-tidb-binlog-cluster.md#use-sql-statements-to-manage-pump-or-drainer)を参照してください。

これらのSQL操作は、PDに保存されている状態情報を直接変更し、binlogctlの`update-pump`および`update-drainer`コマンドと機能的に同等です。 PumpまたはDrainerサービスを一時停止または閉じるには、binlogctlツールを使用します。

## アップストリームデータベースでサポートされている一部のDDLステートメントがダウンストリームデータベースで実行されたときにエラーを引き起こす場合はどうすればよいですか？ {#what-can-i-do-when-some-ddl-statements-supported-by-the-upstream-database-cause-error-when-executed-in-the-downstream-database}

問題を解決するには、次の手順に従います。

1.  `drainer.log`を確認してください。 Drainerプロセスが終了する前に、最後に失敗したDDL操作を`exec failed`で検索します。

2.  DDLバージョンをダウンストリームと互換性のあるバージョンに変更します。ダウンストリームデータベースでこの手順を手動で実行します。

3.  `drainer.log`を確認してください。失敗したDDL操作を検索し、この操作の`commit-ts`を見つけます。例えば：

    ```
    [2020/05/21 09:51:58.019 +08:00] [INFO] [syncer.go:398] ["add ddl item to syncer, you can add this commit ts to `ignore-txn-commit-ts` to skip this ddl if needed"] [sql="ALTER TABLE `test` ADD INDEX (`index1`)"] ["commit ts"=416815754209656834].
    ```

4.  `drainer.toml`の構成ファイルを変更します。 `ignore-txn-commit-ts`項目に`commit-ts`を追加し、Drainerノードを再起動します。

## TiDBはbinlogへの書き込みに失敗してスタックし、 <code>listener stopped, waiting for manual stop</code>ていることがログに表示されます {#tidb-fails-to-write-to-binlog-and-gets-stuck-and-code-listener-stopped-waiting-for-manual-stop-code-appears-in-the-log}

TiDB v3.0.12以前のバージョンでは、binlogの書き込みに失敗すると、TiDBは致命的なエラーを報告します。 TiDBは自動的に終了せず、サービスを停止するだけで、スタックしているように見えます。ログに`listener stopped, waiting for manual stop`のエラーが表示されます。

binlog書き込みの失敗の具体的な原因を特定する必要があります。 binlogがダウンストリームにゆっくりと書き込まれるために障害が発生した場合は、Pumpをスケールアウトするか、binlogを書き込むためのタイムアウト時間を増やすことを検討できます。

v3.0.13以降、エラー報告ロジックが最適化されています。 binlogの書き込みに失敗すると、トランザクションの実行が失敗し、TiDB Binlogはエラーを返しますが、TiDBがスタックすることはありません。

## TiDBは重複したbinlogをPumpに書き込みます {#tidb-writes-duplicate-binlogs-to-pump}

この問題は、ダウンストリームおよびレプリケーションロジックには影響しません。

binlogの書き込みが失敗するかタイムアウトになると、TiDBは、書き込みが成功するまで、次に使用可能なPumpノードへのbinlogの書き込みを再試行します。したがって、Pumpノードへのbinlogの書き込みが遅く、TiDBタイムアウト（デフォルトは15秒）が発生した場合、TiDBは書き込みが失敗したと判断し、次のPumpノードへの書き込みを試みます。 binlogがタイムアウトの原因となるPumpノードに実際に正常に書き込まれる場合、同じbinlogが複数のPumpノードに書き込まれます。 Drainerがbinlogを処理するとき、同じTSOでbinlogを自動的に重複排除するため、この重複書き込みはダウンストリームおよびレプリケーションロジックに影響を与えません。

## Reparoは、完全および増分復元プロセス中に中断されます。ログの最後のTSOを使用してレプリケーションを再開できますか？ {#reparo-is-interrupted-during-the-full-and-incremental-restore-process-can-i-use-the-last-tso-in-the-log-to-resume-replication}

はい。 Reparoは、起動時にセーフモードを自動的に有効にしません。次の手順を手動で実行する必要があります。

1.  Reparoが中断された後、最後のTSOを`checkpoint-tso`としてログに記録します。
2.  Reparo構成ファイルを変更し、構成項目`start-tso`を`checkpoint-tso + 1`に設定し、 `stop-tso`を`checkpoint-tso + 80,000,000,000`に設定し（ `checkpoint-tso`の約5分後）、 `safe-mode`を`true`に設定します。 Reparoを起動すると、Reparoはデータを`stop-tso`に複製してから、自動的に停止します。
3.  Reparoが自動的に停止した後、 `start-tso`から`checkpoint tso + 80,000,000,001`に設定し、 `stop-tso`から`0`に設定し、 `safe-mode`から`false`に設定します。 Reparoを起動して、レプリケーションを再開します。
