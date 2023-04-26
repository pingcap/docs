---
title: TiDB Binlog FAQs
summary: Learn about the frequently asked questions (FAQs) and answers about TiDB Binlog.
---

# TiDBBinlogよくある質問 {#tidb-binlog-faqs}

このドキュメントでは、TiDB Binlogに関するよくある質問 (FAQ) をまとめています。

## TiDB Binlogを有効にすると、TiDB のパフォーマンスにどのような影響がありますか? {#what-is-the-impact-of-enabling-tidb-binlog-on-the-performance-of-tidb}

-   クエリへの影響はありません。

-   `INSERT` 、 `DELETE` 、および`UPDATE`トランザクションのパフォーマンスにわずかな影響があります。 レイテンシーでは、トランザクションがコミットされる前に、TiKV prewrite ステージで p-binlog が同時に書き込まれます。一般に、 binlog の書き込みは TiKV prewrite よりも高速であるため、レイテンシーは増加しません。ポンプの監視パネルでbinlogの書き込みの応答時間を確認できます。

## TiDB Binlogのレプリケーションレイテンシーはどれくらいですか? {#how-high-is-the-replication-latency-of-tidb-binlog}

TiDB Binlogレプリケーションのレイテンシーは秒単位で測定されます。通常、オフピーク時には約 3 秒です。

## Drainer が下流の MySQL または TiDB クラスターにデータをレプリケートするために必要な権限は何ですか? {#what-privileges-does-drainer-need-to-replicate-data-to-the-downstream-mysql-or-tidb-cluster}

ダウンストリームの MySQL または TiDB クラスターにデータをレプリケートするには、 Drainerに次の権限が必要です。

-   入れる
-   アップデート
-   消去
-   作成
-   落とす
-   アルター
-   実行する
-   索引
-   選択する
-   ビューを作成

## Pumpディスクがほぼいっぱいになった場合、どうすればよいですか? {#what-can-i-do-if-the-pump-disk-is-almost-full}

1.  Pump の GC が正常に機能するかどうかを確認します。

    -   ポンプの監視パネルの**gc_tso**時刻が設定ファイルの時刻と一致しているか確認してください。

2.  GC がうまく機能する場合は、次の手順を実行して、単一のPumpに必要なスペースの量を減らします。

    -   Pumpの**GC**パラメータを変更して、データを保持する日数を減らします。

    -   ポンプ インスタンスを追加します。

## Drainer の複製が中断された場合、どうすればよいですか? {#what-can-i-do-if-drainer-replication-is-interrupted}

以下のコマンドを実行して、 Pumpの状態が正常かどうか、および`offline`状態以外のすべてのPumpインスタンスが稼働しているかどうかを確認します。

{{< copyable "" >}}

```bash
binlogctl -cmd pumps
```

次に、 Drainerモニターまたはログが対応するエラーを出力するかどうかを確認します。その場合は、それに応じて解決してください。

## Drainer が下流の MySQL または TiDB クラスターにデータをレプリケートするのが遅い場合はどうすればよいですか? {#what-can-i-do-if-drainer-is-slow-to-replicate-data-to-the-downstream-mysql-or-tidb-cluster}

以下の監視項目を確認してください。

-   **Drainerイベント**モニタリング メトリクスについては、 Drainer が1 秒あたり`INSERT` `UPDATE`および`DELETE`トランザクションをダウンストリームに複製する速度を確認します。

-   **SQL Query Time**モニタリング メトリックについては、 Drainer がダウンストリームで SQL ステートメントを実行するのにかかる時間を確認します。

レプリケーションが遅い場合に考えられる原因と解決策:

-   レプリケートされたデータベースに主キーまたは一意のインデックスのないテーブルが含まれている場合は、テーブルに主キーを追加します。

-   Drainerとダウンストリーム間のレイテンシーが高い場合は、 Drainerの`worker-count`パラメーターの値を増やします。データセンター間のレプリケーションの場合、 Drainer をダウンストリームにデプロイすることをお勧めします。

-   下流の負荷が高くない場合は、 Drainerの`worker-count`パラメータの値を増やします。

## Pumpインスタンスがクラッシュした場合はどうすればよいですか? {#what-can-i-do-if-a-pump-instance-crashes}

Pumpインスタンスがクラッシュした場合、 Drainer はこのインスタンスのデータを取得できないため、データをダウンストリームに複製できません。このPumpインスタンスが通常の状態に回復できる場合、 Drainer はレプリケーションを再開します。そうでない場合は、次の手順を実行します。

1.  このPumpインスタンスのデータを破棄するには、 [このPumpインスタンスの状態を`offline`に変更する binlogctl](/tidb-binlog/maintain-tidb-binlog-cluster.md)を使用します。

2.  Drainer はこのポンプ インスタンスのデータを取得できないため、下流と上流のデータは矛盾しています。この状況では、フル バックアップと増分バックアップを再度実行します。手順は次のとおりです。

    1.  Drainerを停止します。

    2.  アップストリームでフル バックアップを実行します。

    3.  `tidb_binlog.checkpoint`テーブルを含む下流のデータをクリアします。

    4.  フル バックアップをダウンストリームに復元します。

    5.  Drainerをデプロイ、最初のレプリケーションの開始点として`initialCommitTs` (フル バックアップのスナップショット タイムスタンプとして`initialCommitTs`を設定) を使用します。

## チェックポイントとは？ {#what-is-checkpoint}

Checkpoint は、 Drainerがダウンストリームにレプリケートする`commit-ts`を記録します。 Drainer が再起動すると、チェックポイントが読み取られ、対応する`commit-ts`から始まるダウンストリームにデータがレプリケートされます。 `["write save point"] [ts=411222863322546177]` Drainerログは、対応するタイムスタンプでチェックポイントを保存することを意味します。

チェックポイントは、ダウンストリーム プラットフォームの種類ごとに異なる方法で保存されます。

-   MySQL/TiDB の場合は`tidb_binlog.checkpoint`テーブルに保存されます。

-   Kafka/file の場合、対応する構成ディレクトリのファイルに保存されます。

kafka/file のデータには`commit-ts`含まれているため、チェックポイントが失われた場合は、ダウンストリームの最新データを消費することで、ダウンストリーム データの最新の`commit-ts`を確認できます。

Drainer は、開始時にチェックポイントを読み取ります。 Drainer がチェックポイントを読み取ることができない場合、構成された`initialCommitTs`最初のレプリケーションの開始点として使用します。

## Drainer が失敗し、ダウンストリームのデータが残っている場合、新しいマシンにDrainerを再デプロイする方法は? {#how-to-redeploy-drainer-on-the-new-machine-when-drainer-fails-and-the-data-in-the-downstream-remains}

ダウンストリームのデータが影響を受けない場合は、対応するチェックポイントからデータをレプリケートできる限り、新しいマシンにDrainerを再デプロイできます。

-   チェックポイントが失われていない場合は、次の手順を実行します。

    1.  新しいDrainerをデプロイ開始します ( Drainer はチェックポイントを読み取り、レプリケーションを再開できます)。

    2.  [古いDrainerの状態を`offline`に変更する binlogctl](/tidb-binlog/maintain-tidb-binlog-cluster.md)を使用します。

-   チェックポイントが失われた場合は、次の手順を実行します。

    1.  新しいDrainerをデプロイするには、古いDrainerの`commit-ts`を新しいDrainerの`initialCommitTs`として取得します。

    2.  [古いDrainerの状態を`offline`に変更する binlogctl](/tidb-binlog/maintain-tidb-binlog-cluster.md)を使用します。

## フル バックアップとbinlogバックアップ ファイルを使用してクラスターのデータを復元する方法を教えてください。 {#how-to-restore-the-data-of-a-cluster-using-a-full-backup-and-a-binlog-backup-file}

1.  クラスターをクリーンアップし、完全バックアップを復元します。

2.  バックアップ ファイルの最新データを復元するには、 Reparoを使用して`start-tso` = {フル バックアップのスナップショット タイムスタンプ + 1} および`end-ts` = 0 を設定します (または、特定の時点を指定できます)。

## Primary-Secondary レプリケーションで<code>ignore-error</code>有効にすると重大なエラーが発生する場合、 Drainerを再デプロイする方法を教えてください。 {#how-to-redeploy-drainer-when-enabling-code-ignore-error-code-in-primary-secondary-replication-triggers-a-critical-error}

`ignore-error`を有効にした後、TiDB がbinlog の書き込みに失敗したときに重大なエラーがトリガーされた場合、TiDB はbinlog の書き込みを停止し、 binlogデータの損失が発生します。レプリケーションを再開するには、次の手順を実行します。

1.  Drainerインスタンスを停止します。

2.  重大なエラーをトリガーした`tidb-server`インスタンスを再起動し、 binlog の書き込みを再開します (重大なエラーがトリガーされた後、TiDB はbinlog をPumpに書き込みません)。

3.  アップストリームでフル バックアップを実行します。

4.  `tidb_binlog.checkpoint`テーブルを含む下流のデータをクリアします。

5.  フル バックアップをダウンストリームに復元します。

6.  Drainerをデプロイ、最初のレプリケーションの開始点として`initialCommitTs` (フル バックアップのスナップショット タイムスタンプとして`initialCommitTs`を設定) を使用します。

## PumpまたはDrainerノードを一時停止または閉じることができるのはいつですか? {#when-can-i-pause-or-close-a-pump-or-drainer-node}

PumpまたはDrainer状態の説明と、プロセスの開始方法と終了方法については、 [TiDB Binlogクラスタの操作](/tidb-binlog/maintain-tidb-binlog-cluster.md)を参照してください。

サービスを一時的に停止する必要がある場合は、 PumpまたはDrainerノードを一時停止します。例えば：

-   バージョンアップ

    プロセスが停止した後、新しいバイナリを使用してサービスを再起動します。

-   サーバのメンテナンス

    サーバーのダウンタイム メンテナンスが必要な場合は、プロセスを終了し、メンテナンスの終了後にサービスを再起動します。

サービスが不要になったら、 PumpまたはDrainerノードを閉じます。例えば：

-   Pumpのスケールイン

    あまり多くのPumpサービスが必要ない場合は、それらのいくつかを閉じます。

-   レプリケーション タスクのキャンセル

    ダウンストリーム データベースにデータをレプリケートする必要がなくなった場合は、対応するDrainerノードを閉じます。

-   サービスの移行

    サービスを別のサーバーに移行する必要がある場合は、サービスを閉じて、新しいサーバーに再デプロイします。

## PumpまたはDrainerプロセスを一時停止するにはどうすればよいですか? {#how-can-i-pause-a-pump-or-drainer-process}

-   プロセスを直接強制終了します。

    > **ノート：**
    >
    > `kill -9`コマンドは使用しないでください。そうしないと、 PumpまたはDrainerノードは信号を処理できません。

-   PumpまたはDrainerノードがフォアグラウンドで実行されている場合は、 <kbd>Ctrl</kbd> + <kbd>C</kbd>を押して一時停止します。

-   binlogctl で`pause-pump`または`pause-drainer`コマンドを使用します。

## binlogctl で<code>update-pump</code>または<code>update-drainer</code>コマンドを使用して、 PumpまたはDrainerサービスを一時停止できますか? {#can-i-use-the-code-update-pump-code-or-code-update-drainer-code-command-in-binlogctl-to-pause-the-pump-or-drainer-service}

いいえ`update-pump`または`update-drainer`コマンドは、対応する操作を実行するようにPumpまたはDrainerに通知することなく、PD に保存された状態情報を直接変更します。 2 つのコマンドを誤って使用すると、データの複製が中断され、データが失われる可能性さえあります。

## binlogctl で<code>update-pump</code>または<code>update-drainer</code>コマンドを使用して、 PumpまたはDrainerサービスを閉じることはできますか? {#can-i-use-the-code-update-pump-code-or-code-update-drainer-code-command-in-binlogctl-to-close-the-pump-or-drainer-service}

いいえ`update-pump`または`update-drainer`コマンドは、対応する操作を実行するようにPumpまたはDrainerに通知することなく、PD に保存された状態情報を直接変更します。 2 つのコマンドを誤って使用すると、データの複製が中断され、データの不整合が生じる可能性さえあります。例えば：

-   Pumpノードが正常に実行されているか、状態が`paused`のときに、 `update-pump`コマンドを使用してPump状態を`offline`に設定すると、 Drainerノードは`offline` Pumpからのbinlogデータのプルを停止します。この状況では、最新のbinlog をDrainerノードにレプリケートできず、上流と下流の間でデータの不整合が発生します。
-   Drainerノードが正常に実行されている場合、 `update-drainer`コマンドを使用してDrainer の状態を`offline`に設定すると、新しく起動されたPumpノードは`online`状態のDrainerノードにのみ通知します。この状況では、 `offline` Drainer がPumpノードからbinlogデータを時間内に引き出すことができず、アップストリームとダウンストリームの間でデータの不整合が発生します。

## binlogctl で<code>update-pump</code>コマンドを使用して、Pumpの状態を<code>paused</code>に設定できるのはいつですか? {#when-can-i-use-the-code-update-pump-code-command-in-binlogctl-to-set-the-pump-state-to-code-paused-code}

いくつかの異常な状況では、 Pump はその状態を正しく維持できません。次に、 `update-pump`コマンドを使用して状態を変更します。

たとえば、 Pumpプロセスが異常終了した場合 (panicが発生したときにプロセスを直接終了したり、誤って`kill -9`コマンドを使用してプロセスを強制終了したことが原因)、PD に保存されているPump状態情報は`online`のままです。この状況で、現時点でサービスを回復するためにPumpを再起動する必要がない場合は、 `update-pump`コマンドを使用してPumpの状態を`paused`に更新します。これにより、TiDB がバイナリログを書き込み、 Drainer がバイナリログをプルする際の中断を回避できます。

## binlogctl で<code>update-drainer</code>コマンドを使用してDrainer の状態を<code>paused</code>に設定できるのはいつですか? {#when-can-i-use-the-code-update-drainer-code-command-in-binlogctl-to-set-the-drainer-state-to-code-paused-code}

一部の異常な状況では、 Drainerノードがその状態を正しく維持できず、レプリケーション タスクに影響を与えます。次に、 `update-drainer`コマンドを使用して状態を変更します。

たとえば、 Drainerプロセスが異常終了した場合 (panicが発生したときにプロセスを直接終了したり、誤って`kill -9`コマンドを使用してプロセスを強制終了したことが原因)、PD に保存されているDrainer状態情報は`online`のままです。Pumpノードを起動すると、終了したDrainerノードへの通知に失敗し ( `notify drainer ...`エラー)、Pumpノードの障害が発生します。この状況では、 `update-drainer`コマンドを使用してDrainer の状態を`paused`に更新し、 Pumpノードを再起動します。

## PumpまたはDrainerノードを閉じるにはどうすればよいですか? {#how-can-i-close-a-pump-or-drainer-node}

現在、binlogctl で`offline-pump`または`offline-drainer`コマンドのみを使用して、 PumpまたはDrainerノードを閉じることができます。

## binlogctl で<code>update-pump</code>コマンドを使用して、 Pump の状態を<code>offline</code>に設定できるのはいつですか? {#when-can-i-use-the-code-update-pump-code-command-in-binlogctl-to-set-the-pump-state-to-code-offline-code}

次の状況では、 `update-pump`コマンドを使用してPump状態を`offline`に設定できます。

-   Pumpプロセスが異常終了し、サービスを回復できない場合、レプリケーション タスクは中断されます。レプリケーションを回復し、binlogデータの一部の損失を受け入れる場合は、 `update-pump`コマンドを使用してPump状態を`offline`に設定します。次に、 DrainerノードはPumpノードからのbinlogのプルを停止し、データの複製を続行します。
-   一部の古いPumpノードは、過去のタスクから取り残されています。それらのプロセスは終了し、サービスは不要になりました。次に、 `update-pump`コマンドを使用して状態を`offline`に設定します。

その他の状況では、通常のプロセスである`offline-pump`コマンドを使用してPumpサービスを閉じます。

> **警告：**
>
> > binlogデータの損失とアップストリームとダウンストリーム間のデータの不一致を許容できる場合、またはPumpノードに保存されているbinlogデータが不要になった場合を除き、 `update-pump`コマンドは使用しないでください。

## 終了して一時停止に設定されているPumpノードを閉じる場合、binlogctl で<code>update-pump</code>コマンドを使用してPumpの状態を<code>offline</code> <code>paused</code>できますか? {#can-i-use-the-code-update-pump-code-command-in-binlogctl-to-set-the-pump-state-to-code-offline-code-if-i-want-to-close-a-pump-node-that-is-exited-and-set-to-code-paused-code}

Pumpプロセスが終了し、ノードが`paused`状態の場合、ノード内のすべてのbinlogデータがその下流のDrainerノードで消費されるわけではありません。したがって、これを行うと、上流と下流の間でデータの不整合が発生する可能性があります。この場合、Pumpを再起動し、 `offline-pump`コマンドを使用してPumpノードを閉じます。

## binlogctl で<code>update-drainer</code>コマンドを使用してDrainer の状態を<code>offline</code>に設定できるのはいつですか? {#when-can-i-use-the-code-update-drainer-code-command-in-binlogctl-to-set-the-drainer-state-to-code-offline-code}

古いDrainerノードの一部は、過去のタスクから取り残されています。それらのプロセスは終了し、サービスは不要になりました。次に、 `update-drainer`コマンドを使用して状態を`offline`に設定します。

## <code>change pump</code>や<code>change drainer</code>などの SQL 操作を使用して、PumpまたはDrainerサービスを一時停止または終了できますか? {#can-i-use-sql-operations-such-as-code-change-pump-code-and-code-change-drainer-code-to-pause-or-close-the-pump-or-drainer-service}

いいえ。これらの SQL 操作の詳細については、 [SQL ステートメントを使用してPumpまたはDrainerを管理する](/tidb-binlog/maintain-tidb-binlog-cluster.md#use-sql-statements-to-manage-pump-or-drainer)を参照してください。

これらの SQL 操作は、PD に保存された状態情報を直接変更し、binlogctl の`update-pump`および`update-drainer`コマンドと機能的に同等です。 PumpまたはDrainerサービスを一時停止または終了するには、binlogctl ツールを使用します。

## アップストリーム データベースでサポートされている一部の DDL ステートメントをダウンストリーム データベースで実行すると、エラーが発生する場合はどうすればよいですか? {#what-can-i-do-when-some-ddl-statements-supported-by-the-upstream-database-cause-error-when-executed-in-the-downstream-database}

この問題を解決するには、次の手順に従います。

1.  `drainer.log`を確認してください。 Drainerプロセスが終了する前に、最後に失敗した DDL 操作を`exec failed`で検索します。

2.  DDL バージョンをダウンストリームと互換性のあるバージョンに変更します。この手順は、ダウンストリーム データベースで手動で実行します。

3.  `drainer.log`を確認してください。失敗した DDL 操作を検索し、この操作の`commit-ts`を見つけます。例えば：

    ```
    [2020/05/21 09:51:58.019 +08:00] [INFO] [syncer.go:398] ["add ddl item to syncer, you can add this commit ts to `ignore-txn-commit-ts` to skip this ddl if needed"] [sql="ALTER TABLE `test` ADD INDEX (`index1`)"] ["commit ts"=416815754209656834].
    ```

4.  `drainer.toml`構成ファイルを変更します。 `commit-ts` in the `ignore-txn-commit-ts`項目を追加し、 Drainerノードを再起動します。

## TiDB がbinlogへの書き込みに失敗してスタックし、 <code>listener stopped, waiting for manual stop</code>ログに表示される {#tidb-fails-to-write-to-binlog-and-gets-stuck-and-code-listener-stopped-waiting-for-manual-stop-code-appears-in-the-log}

TiDB v3.0.12 以前のバージョンでは、 binlog の書き込みに失敗すると、TiDB は致命的なエラーを報告します。 TiDB は自動的に終了せず、サービスを停止するだけで、スタックしているように見えます。ログに`listener stopped, waiting for manual stop`エラーが表示されます。

binlogの書き込み失敗の具体的な原因を特定する必要があります。 binlog がダウンストリームにゆっくりと書き込まれるために障害が発生した場合は、 Pump をスケールアウトするか、 binlog を書き込むためのタイムアウト時間を長くすることを検討できます。

v3.0.13 以降、エラー報告ロジックが最適化されました。 binlog の書き込みエラーにより、トランザクションの実行が失敗し、TiDB Binlog はエラーを返しますが、TiDB がスタックすることはありません。

## TiDB は重複したバイナリログをPumpに書き込みます {#tidb-writes-duplicate-binlogs-to-pump}

この問題は、ダウンストリームおよびレプリケーション ロジックには影響しません。

binlogの書き込みが失敗するかタイムアウトになると、TiDB は、書き込みが成功するまで、次に使用可能なPumpノードにbinlogの書き込みを再試行します。したがって、 Pumpノードへのbinlogの書き込みが遅く、TiDB タイムアウト (デフォルトは 15 秒) が発生する場合、TiDB は書き込みが失敗したと判断し、次のPumpノードへの書き込みを試みます。 binlogが実際にタイムアウトの原因となったPumpノードに正常に書き込まれた場合、同じbinlog が複数のPumpノードに書き込まれます。 Drainer がbinlogを処理するとき、同じ TSO の binlog を自動的に重複排除するため、この重複した書き込みはダウンストリームおよびレプリケーション ロジックに影響しません。

## 完全および増分復元プロセス中にReparoが中断されます。ログ内の最後の TSO を使用して複製を再開できますか? {#reparo-is-interrupted-during-the-full-and-incremental-restore-process-can-i-use-the-last-tso-in-the-log-to-resume-replication}

はい。 Reparo は、起動時にセーフモードを自動的に有効にしません。次の手順を手動で実行する必要があります。

1.  Reparoが中断された後、ログに最後の TSO を`checkpoint-tso`として記録します。
2.  Reparo の設定ファイルを修正し、設定項目`start-tso`を`checkpoint-tso + 1`に、 `stop-tso`を`checkpoint-tso + 80,000,000,000`に設定し ( `checkpoint-tso`の約 5 分後)、 `safe-mode`を`true`に設定します。 Reparo を起動すると、 Reparo はデータを`stop-tso`にレプリケートしてから自動的に停止します。
3.  Reparoが自動停止したら、 `start-tso` ～ `checkpoint tso + 80,000,000,001` `stop-tso` `0` ～ `safe-mode` `false`設定します。 Reparo を起動してレプリケーションを再開します。
