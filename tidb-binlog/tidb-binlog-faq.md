---
title: TiDB Binlog FAQs
summary: Learn about the frequently asked questions (FAQs) and answers about TiDB Binlog.
---

# TiDBBinlogよくある質問 {#tidb-binlog-faqs}

このドキュメントには、 TiDB Binlogに関するよくある質問 (FAQ) がまとめられています。

## TiDB Binlogを有効にすると、TiDB のパフォーマンスにどのような影響がありますか? {#what-is-the-impact-of-enabling-tidb-binlog-on-the-performance-of-tidb}

-   クエリには影響ありません。

-   `INSERT` 、 `DELETE` 、および`UPDATE`のトランザクションでは、パフォーマンスにわずかな影響があります。 レイテンシーでは、トランザクションがコミットされる前に、TiKV 事前書き込みステージで p-binlog が同時に書き込まれます。一般に、 binlog の書き込みは TiKV prewrite よりも高速であるため、レイテンシーは増加しません。binlog書き込みの応答時間は、Pump のモニタリング パネルで確認できます。

## TiDB Binlogのレプリケーションレイテンシーはどれくらいですか? {#how-high-is-the-replication-latency-of-tidb-binlog}

TiDB Binlogレプリケーションのレイテンシーは秒単位で測定され、オフピーク時間では通常約 3 秒です。

## データをダウンストリームの MySQL または TiDB クラスターにレプリケートするには、 Drainer にはどのような権限が必要ですか? {#what-privileges-does-drainer-need-to-replicate-data-to-the-downstream-mysql-or-tidb-cluster}

データをダウンストリームの MySQL または TiDB クラスターにレプリケートするには、 Drainerには次の権限が必要です。

-   入れる
-   アップデート
-   消去
-   作成する
-   落とす
-   オルタ
-   実行する
-   索引
-   選択する
-   ビューの作成

## Pumpディスクがほぼ満杯の場合はどうすればよいですか? {#what-can-i-do-if-the-pump-disk-is-almost-full}

1.  Pump の GC が正常に動作するかどうかを確認します。

    -   Pump の監視パネルの**gc_tso 時間が設定ファイルの gc_tso**時間と同じであるかどうかを確認します。

2.  GC が正常に機能する場合は、次の手順を実行して、1 つのPumpに必要なスペースの量を削減します。

    -   Pumpの**GC**パラメータを変更して、データを保持する日数を減らします。

    -   ポンプ インスタンスを追加します。

## Drainer のレプリケーションが中断された場合はどうすればよいですか? {#what-can-i-do-if-drainer-replication-is-interrupted}

以下のコマンドを実行して、 Pumpの状態が正常であるか、および状態`offline`以外のPumpインスタンスがすべて起動しているかを確認します。

```bash
binlogctl -cmd pumps
```

次に、 Drainerモニターまたはログが対応するエラーを出力するかどうかを確認します。その場合は、それに応じて解決してください。

## Drainer がダウンストリームの MySQL または TiDB クラスターにデータをレプリケートするのが遅い場合はどうすればよいですか? {#what-can-i-do-if-drainer-is-slow-to-replicate-data-to-the-downstream-mysql-or-tidb-cluster}

以下の監視項目を確認してください。

-   **Drainerイベント**監視メトリクスについては、1 秒あたり`INSERT` `UPDATE`および`DELETE`のトランザクションをダウンストリームにレプリケートするDrainerの速度を確認します。

-   **SQL クエリ時間**監視メトリクスについては、 Drainer がダウンストリームで SQL ステートメントを実行するのにかかる時間を確認します。

レプリケーションが遅い場合の考えられる原因と解決策:

-   レプリケートされたデータベースに主キーまたは一意のインデックスのないテーブルが含まれている場合は、テーブルに主キーを追加します。

-   Drainerとダウンストリーム間のレイテンシーが高い場合は、 Drainerの`worker-count`パラメータの値を増やします。データセンター間のレプリケーションの場合は、 Drainer をダウンストリームにデプロイすることをお勧めします。

-   下流の負荷が高くない場合は、 Drainerの`worker-count`パラメータの値を大きくします。

## Pumpインスタンスがクラッシュした場合はどうすればよいですか? {#what-can-i-do-if-a-pump-instance-crashes}

Pumpインスタンスがクラッシュすると、 Drainerはこのインスタンスのデータを取得できないため、データをダウンストリームにレプリケートできません。このPumpインスタンスが通常の状態に回復できる場合、 Drainer はレプリケーションを再開します。そうでない場合は、次の手順を実行します。

1.  このPumpインスタンスのデータを破棄するには、 [binlogctl を使用して、このPumpインスタンスの状態を`offline`に変更します。](/tidb-binlog/maintain-tidb-binlog-cluster.md)を使用します。

2.  Drainer はこのポンプ インスタンスのデータを取得できないため、下流と上流のデータに一貫性がありません。この状況では、完全バックアップと増分バックアップを再度実行します。手順は次のとおりです。

    1.  Drainerを停止します。

    2.  アップストリームで完全バックアップを実行します。

    3.  `tidb_binlog.checkpoint`テーブルを含む下流のデータをクリアします。

    4.  完全バックアップをダウンストリームに復元します。

    5.  Drainerをデプロイ、初期レプリケーションの開始点として`initialCommitTs` (完全バックアップのスナップショット タイムスタンプとして`initialCommitTs`を設定) を使用します。

## チェックポイントとは何ですか? {#what-is-checkpoint}

チェックポイントは、 Drainerがダウンストリームにレプリケートする`commit-ts`を記録します。 Drainer が再起動すると、チェックポイントを読み取り、対応する`commit-ts`から開始してダウンストリームにデータを複製します。 `["write save point"] [ts=411222863322546177]` Drainerログは、チェックポイントを対応するタイムスタンプとともに保存することを意味します。

チェックポイントは、ダウンストリーム プラットフォームの種類ごとにさまざまな方法で保存されます。

-   MySQL/TiDBの場合は`tidb_binlog.checkpoint`テーブルに保存されます。

-   Kafka/file の場合、対応する構成ディレクトリのファイルに保存されます。

kafka/file のデータには`commit-ts`含まれているため、チェックポイントが失われた場合、 downstream にある最新のデータを消費することで、下流のデータの最新`commit-ts`を確認できます。

Drainer は開始時にチェックポイントを読み取ります。 Drainer がチェックポイントを読み取ることができない場合、初期レプリケーションの開始点として構成された`initialCommitTs`が使用されます。

## Drainerに障害が発生し、ダウンストリームのデータが残っている場合に、新しいマシンにDrainer を再デプロイするにはどうすればよいですか? {#how-to-redeploy-drainer-on-the-new-machine-when-drainer-fails-and-the-data-in-the-downstream-remains}

ダウンストリームのデータが影響を受けない場合は、対応するチェックポイントからデータを複製できる限り、新しいマシンにDrainerを再デプロイできます。

-   チェックポイントが失われていない場合は、次の手順を実行します。

    1.  新しいDrainerをデプロイて開始します ( Drainer はチェックポイントを読み取り、レプリケーションを再開できます)。

    2.  [binlogctl は、古いDrainerの状態を`offline`に変更します。](/tidb-binlog/maintain-tidb-binlog-cluster.md)を使用します 。

-   チェックポイントが失われた場合は、次の手順を実行します。

    1.  新しいDrainerをデプロイするには、古いDrainerの`commit-ts`を新しいDrainerの`initialCommitTs`として取得します。

    2.  [binlogctl は、古いDrainerの状態を`offline`に変更します。](/tidb-binlog/maintain-tidb-binlog-cluster.md)を使用します 。

## 完全バックアップとbinlogバックアップ ファイルを使用してクラスターのデータを復元するにはどうすればよいですか? {#how-to-restore-the-data-of-a-cluster-using-a-full-backup-and-a-binlog-backup-file}

1.  クラスターをクリーンアップし、完全バックアップを復元します。

2.  バックアップ ファイルの最新データを復元するには、 Reparoを使用して`start-tso` = {完全バックアップのスナップショット タイムスタンプ + 1} および`end-ts` = 0 を設定します (または、時点を指定することもできます)。

## プライマリ - セカンダリ レプリケーションで<code>ignore-error</code>有効にすると重大なエラーが発生する場合、 Drainerを再デプロイするにはどうすればよいですか? {#how-to-redeploy-drainer-when-enabling-code-ignore-error-code-in-primary-secondary-replication-triggers-a-critical-error}

`ignore-error`を有効にした後に TiDB がbinlogの書き込みに失敗し、重大なエラーがトリガーされた場合、TiDB はbinlogの書き込みを停止し、binlogデータの損失が発生します。レプリケーションを再開するには、次の手順を実行します。

1.  Drainerインスタンスを停止します。

2.  重大なエラーをトリガーする`tidb-server`インスタンスを再起動し、binlogの書き込みを再開します (重大なエラーがトリガーされた後、TiDB はbinlogをPumpに書き込みません)。

3.  アップストリームで完全バックアップを実行します。

4.  `tidb_binlog.checkpoint`テーブルを含む下流のデータをクリアします。

5.  完全バックアップをダウンストリームに復元します。

6.  Drainerをデプロイ、初期レプリケーションの開始点として`initialCommitTs` (完全バックアップのスナップショット タイムスタンプとして`initialCommitTs`を設定) を使用します。

## PumpまたはDrainerノードを一時停止または閉じることができるのはいつですか? {#when-can-i-pause-or-close-a-pump-or-drainer-node}

PumpまたはDrainerの状態の説明と、プロセスの開始および終了方法については、 [TiDBBinlogクラスタの操作](/tidb-binlog/maintain-tidb-binlog-cluster.md)を参照してください。

サービスを一時的に停止する必要がある場合は、 PumpノードまたはDrainerノードを一時停止します。例えば：

-   バージョンアップ

    プロセスが停止した後、新しいバイナリを使用してサービスを再起動します。

-   サーバのメンテナンス

    サーバーのダウンタイムメンテナンスが必要な場合は、プロセスを終了し、メンテナンス終了後にサービスを再起動します。

サービスが必要なくなったら、PumpまたはDrainerノードを閉じます。例えば：

-   Pumpのスケールイン

    あまり多くのPumpサービスが必要ない場合は、いくつかを閉じてください。

-   レプリケーションタスクのキャンセル

    データをダウンストリーム データベースにレプリケートする必要がなくなった場合は、対応するDrainerノードを閉じます。

-   サービスの移行

    サービスを別のサーバーに移行する必要がある場合は、サービスを閉じて、新しいサーバーに再デプロイします。

## PumpまたはDrainerのプロセスを一時停止するにはどうすればよいですか? {#how-can-i-pause-a-pump-or-drainer-process}

-   プロセスを直接強制終了します。

    > **注記：**
    >
    > `kill -9`コマンドは使用しないでください。そうしないと、 PumpノードまたはDrainerノードは信号を処理できません。

-   PumpまたはDrainerノードがフォアグラウンドで実行されている場合は、 <kbd>Ctrl</kbd> + <kbd>C</kbd>を押して一時停止します。

-   binlogctl の`pause-pump`または`pause-drainer`コマンドを使用します。

## binlogctl で<code>update-pump</code>または<code>update-drainer</code>コマンドを使用して、 PumpサービスまたはDrainerサービスを一時停止できますか? {#can-i-use-the-code-update-pump-code-or-code-update-drainer-code-command-in-binlogctl-to-pause-the-pump-or-drainer-service}

いいえ`update-pump`または`update-drainer`コマンドは、 PumpまたはDrainerに対応する操作を実行するように通知せずに、PD に保存されている状態情報を直接変更します。 2 つのコマンドを誤って使用すると、データ レプリケーションが中断され、データ損失が発生する可能性もあります。

## binlogctl で<code>update-pump</code>または<code>update-drainer</code>コマンドを使用して、 PumpサービスまたはDrainerサービスを閉じることはできますか? {#can-i-use-the-code-update-pump-code-or-code-update-drainer-code-command-in-binlogctl-to-close-the-pump-or-drainer-service}

いいえ`update-pump`または`update-drainer`コマンドは、 PumpまたはDrainerに対応する操作を実行するように通知せずに、PD に保存されている状態情報を直接変更します。 2 つのコマンドを誤って使用すると、データ レプリケーションが中断され、データの不整合が発生する可能性もあります。例えば：

-   Pumpノードが正常に実行されているとき、または`paused`状態にあるときに、 `update-pump`コマンドを使用してPump状態を`offline`に設定すると、 Drainerノードは`offline` Pumpからのbinlogデータのプルを停止します。この状況では、最新のbinlogをDrainerノードに複製できず、アップストリームとダウンストリームの間でデータの不整合が発生します。
-   Drainerノードが正常に実行されている場合、 `update-drainer`コマンドを使用してDrainer状態を`offline`に設定すると、新しく開始されたPumpノードは`online`状態のDrainerノードのみに通知します。この状況では、 `offline` Drainer がPumpノードからbinlogデータを時間内に取得できず、アップストリームとダウンストリームの間でデータの不整合が発生します。

## binlogctl の<code>update-pump</code>コマンドを使用してPump状態を<code>paused</code>に設定できるのはいつですか? {#when-can-i-use-the-code-update-pump-code-command-in-binlogctl-to-set-the-pump-state-to-code-paused-code}

異常な状況では、Pumpがその状態を正しく維持できなくなることがあります。次に、 `update-pump`コマンドを使用して状態を変更します。

たとえば、 Pumpプロセスが異常終了した場合 (panic発生時にプロセスを直接終了したり、誤って`kill -9`コマンドを使用してプロセスを強制終了したりしたことが原因)、PD に保存されるPump状態情報は`online`のままです。この状況で、現時点でサービスを回復するためにPumpを再起動する必要がない場合は、 `update-pump`コマンドを使用してPump の状態を`paused`に更新します。これにより、TiDB がバイナリログを書き込み、 Drainer がバイナリログをプルするときの中断を回避できます。

## binlogctl の<code>update-drainer</code>コマンドを使用して、 Drainer状態を<code>paused</code>に設定できるのはいつですか? {#when-can-i-use-the-code-update-drainer-code-command-in-binlogctl-to-set-the-drainer-state-to-code-paused-code}

一部の異常な状況では、Drainerノードがその状態を正しく維持できず、レプリケーション タスクに影響を及ぼします。次に、 `update-drainer`コマンドを使用して状態を変更します。

たとえば、 Drainerプロセスが異常終了した場合 (panic発生時にプロセスを直接終了したり、誤って`kill -9`コマンドを使用してプロセスを強制終了したりしたことが原因)、PD に保存されるDrainer の状態情報は`online`のままです。 Pumpノードが開始されると、終了したDrainerノードへの通知が失敗し ( `notify drainer ...`エラー)、 Pumpノードの障害が発生します。この状況では、 `update-drainer`コマンドを使用してDrainer状態を`paused`に更新し、 Pumpノードを再起動します。

## PumpまたはDrainerノードを閉じるにはどうすればよいですか? {#how-can-i-close-a-pump-or-drainer-node}

現在、PumpまたはDrainerノードを閉じるには、binlogctl で`offline-pump`または`offline-drainer`コマンドのみを使用できます。

## binlogctl の<code>update-pump</code>コマンドを使用してPump状態を<code>offline</code>に設定できるのはいつですか? {#when-can-i-use-the-code-update-pump-code-command-in-binlogctl-to-set-the-pump-state-to-code-offline-code}

次の状況では、 `update-pump`コマンドを使用してPump状態を`offline`に設定できます。

-   Pumpプロセスが異常終了し、サービスを回復できない場合、レプリケーション タスクは中断されます。レプリケーションを回復し、binlogデータの一部の損失を許容する場合は、 `update-pump`コマンドを使用してPump状態を`offline`に設定します。その後、 DrainerノードはPumpノードからのbinlogの取得を停止し、データのレプリケーションを続行します。
-   一部の古いPumpノードは、履歴タスクから残っています。彼らのプロセスは終了しており、サービスはもう必要ありません。次に、 `update-pump`コマンドを使用して状態を`offline`に設定します。

その他の状況では、 `offline-pump`コマンドを使用してPumpサービスを閉じます。これは通常のプロセスです。

> **警告：**
>
> > binlogデータの損失やアップストリームとダウンストリーム間のデータの不一致を許容できる場合、またはPumpノードに保存されているbinlogデータが不要になった場合を除き、 `update-pump`コマンドを使用しないでください。

## 終了して一時停止に設定されているPumpノードを閉じたい場合、binlogctl で<code>update-pump</code>コマンドを使用してPump状態を<code>offline</code> <code>paused</code>設定できますか? {#can-i-use-the-code-update-pump-code-command-in-binlogctl-to-set-the-pump-state-to-code-offline-code-if-i-want-to-close-a-pump-node-that-is-exited-and-set-to-code-paused-code}

Pumpプロセスが終了し、ノードが`paused`状態にある場合、ノード内のすべてのbinlogデータが下流のDrainerノードで消費されるわけではありません。したがって、これを行うと、上流と下流の間でデータの不整合が生じる危険性があります。この状況では、 Pump を再起動し、 `offline-pump`コマンドを使用してPumpノードを閉じます。

## binlogctl の<code>update-drainer</code>コマンドを使用してDrainer状態を<code>offline</code>に設定できるのはいつですか? {#when-can-i-use-the-code-update-drainer-code-command-in-binlogctl-to-set-the-drainer-state-to-code-offline-code}

一部の古いDrainerノードは、履歴タスクから残されています。彼らのプロセスは終了しており、サービスはもう必要ありません。次に、 `update-drainer`コマンドを使用して状態を`offline`に設定します。

## <code>change pump</code>や<code>change drainer</code>などの SQL 操作を使用して、PumpまたはDrainerサービスを一時停止または終了できますか? {#can-i-use-sql-operations-such-as-code-change-pump-code-and-code-change-drainer-code-to-pause-or-close-the-pump-or-drainer-service}

いいえ。これらの SQL 操作の詳細については、 [SQL ステートメントを使用してPumpまたはDrainerを管理する](/tidb-binlog/maintain-tidb-binlog-cluster.md#use-sql-statements-to-manage-pump-or-drainer)を参照してください。

これらの SQL 操作は、PD に保存された状態情報を直接変更し、binlogctl の`update-pump`および`update-drainer`コマンドと機能的に同等です。 PumpサービスまたはDrainerサービスを一時停止または閉じるには、binlogctl ツールを使用します。

## アップストリーム データベースでサポートされている一部の DDL ステートメントをダウンストリーム データベースで実行するとエラーが発生する場合は、どうすればよいですか? {#what-can-i-do-when-some-ddl-statements-supported-by-the-upstream-database-cause-error-when-executed-in-the-downstream-database}

問題を解決するには、次の手順に従います。

1.  チェック`drainer.log` 。 Drainerプロセスが終了する前に、 `exec failed`に失敗した DDL 操作を検索します。

2.  DDL バージョンをダウンストリームと互換性のあるものに変更します。この手順はダウンストリーム データベースで手動で実行します。

3.  チェック`drainer.log` 。失敗した DDL 操作を検索し、この操作の`commit-ts`を見つけます。例えば：

        [2020/05/21 09:51:58.019 +08:00] [INFO] [syncer.go:398] ["add ddl item to syncer, you can add this commit ts to `ignore-txn-commit-ts` to skip this ddl if needed"] [sql="ALTER TABLE `test` ADD INDEX (`index1`)"] ["commit ts"=416815754209656834].

4.  `drainer.toml`設定ファイルを変更します。 `ignore-txn-commit-ts`項目に`commit-ts`追加し、 Drainerノードを再起動します。

## TiDB がbinlogへの書き込みに失敗してスタックし、 <code>listener stopped, waiting for manual stop</code>ログに表示される {#tidb-fails-to-write-to-binlog-and-gets-stuck-and-code-listener-stopped-waiting-for-manual-stop-code-appears-in-the-log}

TiDB v3.0.12 以前のバージョンでは、binlogの書き込みエラーにより TiDB が致命的なエラーを報告します。 TiDB は自動的に終了せず、サービスを停止するだけなので、スタックしているように見えます。ログに`listener stopped, waiting for manual stop`エラーが表示されます。

binlog書き込み失敗の具体的な原因を特定する必要があります。 binlog のダウンストリームへの書き込みが遅いために障害が発生した場合は、 Pump をスケールアウトするか、 binlog の書き込みのタイムアウト時間を増やすことを検討できます。

v3.0.13 以降、エラー報告ロジックが最適化されています。 binlog書き込みの失敗によりトランザクションの実行が失敗し、TiDB Binlog はエラーを返しますが、TiDB はスタックしません。

## TiDB は重複したバイナリログをPumpに書き込みます {#tidb-writes-duplicate-binlogs-to-pump}

この問題は、ダウンストリームおよびレプリケーション ロジックには影響しません。

binlogの書き込みが失敗するかタイムアウトになると、TiDB は書き込みが成功するまで、次に利用可能なPumpノードへのbinlogの書き込みを再試行します。したがって、Pumpノードへのbinlogの書き込みが遅く、TiDB タイムアウト (デフォルトは 15 秒) が発生する場合、TiDB は書き込みが失敗したと判断し、次のPumpノードへの書き込みを試行します。実際にタイムアウトの原因となったPumpノードにbinlogが正常に書き込まれた場合、同じbinlogが複数のPumpノードに書き込まれます。 Drainer がbinlogを処理するとき、同じ TSO を持つ binlog の重複が自動的に除外されるため、この重複書き込みはダウンストリームおよびレプリケーション ロジックに影響を与えません。

## Reparo は、完全復元プロセスおよび増分復元プロセス中に中断されます。ログ内の最後の TSO を使用してレプリケーションを再開できますか? {#reparo-is-interrupted-during-the-full-and-incremental-restore-process-can-i-use-the-last-tso-in-the-log-to-resume-replication}

はい。 Reparo は、起動時にセーフ モードを自動的に有効にしません。次の手順を手動で実行する必要があります。

1.  Reparoが中断された後、ログ内の最後の TSO を`checkpoint-tso`として記録します。
2.  Reparo設定ファイルを変更し、設定項目`start-tso`を`checkpoint-tso + 1`に設定し、 `stop-tso` `checkpoint-tso + 80,000,000,000`に設定します ( `checkpoint-tso`の約 5 分後)、 `safe-mode`を`true`に設定します。 Reparo を開始すると、 Reparo はデータを`stop-tso`に複製し、その後自動的に停止します。
3.  Reparoが自動停止した後、 `start-tso` ～ `checkpoint tso + 80,000,000,001` `stop-tso` `0` ～ `safe-mode` `false`設定します。 Reparoを起動してレプリケーションを再開します。
