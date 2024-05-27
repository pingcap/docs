---
title: TiDB Binlog FAQs
summary: TiDB Binlogに関するよくある質問 (FAQ) と回答について説明します。
---

# TiDBBinlogよくある質問 {#tidb-binlog-faqs}

このドキュメントでは、 TiDB Binlogに関するよくある質問 (FAQ) をまとめています。

## TiDB Binlogを有効にすると、TiDB のパフォーマンスにどのような影響がありますか? {#what-is-the-impact-of-enabling-tidb-binlog-on-the-performance-of-tidb}

-   クエリには影響はありません。

-   `INSERT` `DELETE`トランザクションではパフォーマンスに若干の影響があります。レイテンシーでは、トランザクションがコミットされる前に、TiKV 事前書き込みステージで p-binlog が同時に`UPDATE`れます。通常、 binlogの書き込みは TiKV 事前書き込みよりも高速であるため、レイテンシーは増加しません。Pump の監視パネルで、 binlog書き込みの応答時間を確認できます。

## TiDB Binlogのレプリケーションレイテンシーはどれくらいですか? {#how-high-is-the-replication-latency-of-tidb-binlog}

TiDB Binlogレプリケーションのレイテンシーは秒単位で測定され、通常、オフピーク時には約 3 秒です。

## ダウンストリームの MySQL または TiDB クラスターにデータを複製するには、 Drainer にどのような権限が必要ですか? {#what-privileges-does-drainer-need-to-replicate-data-to-the-downstream-mysql-or-tidb-cluster}

ダウンストリームの MySQL または TiDB クラスターにデータを複製するには、 Drainerに次の権限が必要です。

-   入れる
-   アップデート
-   消去
-   作成する
-   落とす
-   アルター
-   実行する
-   索引
-   選択する
-   ビューの作成

## Pumpディスクがほぼいっぱいになった場合はどうすればいいですか? {#what-can-i-do-if-the-pump-disk-is-almost-full}

1.  ポンプの GC が正常に動作するかどうかを確認します。

    -   Pump の監視パネルの**gc_tso**時間が構成ファイルの時間と同じかどうかを確認します。

2.  GC が正常に動作する場合は、次の手順を実行して、単一のPumpに必要なスペースの量を減らします。

    -   Pumpの**GC**パラメータを変更して、データを保持する日数を減らします。

    -   ポンプインスタンスを追加します。

## Drainerレプリケーションが中断された場合、どうすればよいですか? {#what-can-i-do-if-drainer-replication-is-interrupted}

次のコマンドを実行して、 Pumpの状態が正常かどうか、および`offline`状態ではないすべてのPumpインスタンスが実行中かどうかを確認します。

```bash
binlogctl -cmd pumps
```

次に、 Drainerモニターまたはログが対応するエラーを出力するかどうかを確認します。出力する場合は、それに応じて解決します。

## Drainer がダウンストリームの MySQL または TiDB クラスターにデータを複製するのに時間がかかる場合はどうすればよいでしょうか? {#what-can-i-do-if-drainer-is-slow-to-replicate-data-to-the-downstream-mysql-or-tidb-cluster}

以下の監視項目を確認してください。

-   **Drainerイベント**監視メトリックについては、 Drainer が1 秒あたり`INSERT` `DELETE` `UPDATE`トランザクションをダウンストリームに複製する速度を確認します。

-   **SQL クエリ時間**監視メトリックについては、 Drainer がダウンストリームで SQL ステートメントを実行するのにかかる時間を確認します。

レプリケーションが遅い場合の考えられる原因と解決策:

-   複製されたデータベースに主キーまたは一意のインデックスのないテーブルが含まれている場合は、テーブルに主キーを追加します。

-   Drainerとダウンストリーム間のレイテンシーが高い場合は、 Drainerの`worker-count`パラメータの値を増やします。データセンター間のレプリケーションの場合は、ダウンストリームにDrainer を展開することをお勧めします。

-   下流の負荷が高くない場合は、 Drainerの`worker-count`パラメータの値を大きくします。

## Pumpインスタンスがクラッシュした場合はどうすればよいですか? {#what-can-i-do-if-a-pump-instance-crashes}

Pumpインスタンスがクラッシュした場合、 Drainer はこのインスタンスのデータを取得できないため、ダウンストリームにデータを複製できません。このPumpインスタンスが通常の状態に回復できる場合、 Drainer はレプリケーションを再開します。そうでない場合は、次の手順を実行します。

1.  このPumpインスタンスのデータを破棄するには[binlogctl を実行して、このPumpインスタンスの状態を`offline`に変更します。](/tidb-binlog/maintain-tidb-binlog-cluster.md)使用します。

2.  Drainer はこのポンプ インスタンスのデータを取得できないため、ダウンストリームとアップストリームのデータが不整合になります。この状況では、完全バックアップと増分バックアップを再度実行してください。手順は次のとおりです。

    1.  Drainerを停止します。

    2.  アップストリームで完全バックアップを実行します。

    3.  `tidb_binlog.checkpoint`テーブルを含む下流のデータをクリアします。

    4.  フルバックアップをダウンストリームに復元します。

    5.  Drainerをデプロイ、初期レプリケーションの開始点として`initialCommitTs` (完全バックアップのスナップショット タイムスタンプとして`initialCommitTs`を設定) を使用します。

## チェックポイントとは何ですか? {#what-is-checkpoint}

チェックポイントは、 Drainer がダウンストリームに複製する`commit-ts`記録します。Drainerが再起動すると、チェックポイントが読み取られ、対応する`commit-ts`からダウンストリームにデータが複製されます。5 `["write save point"] [ts=411222863322546177]`ログは、対応するタイムスタンプとともにチェックポイントを保存することを意味します。

チェックポイントは、ダウンストリーム プラットフォームの種類に応じて異なる方法で保存されます。

-   MySQL/TiDBの場合は`tidb_binlog.checkpoint`テーブルに保存されます。

-   Kafka/file の場合は、対応する設定ディレクトリのファイルに保存されます。

kafka/file のデータには`commit-ts`含まれているため、チェックポイントが失われた場合は、ダウンストリームの最新データを消費することで、ダウンストリームのデータの最新の`commit-ts`を確認できます。

Drainer は起動時にチェックポイントを読み取ります。Drainerがチェックポイントを読み取れない場合は、設定された`initialCommitTs`初期レプリケーションの開始ポイントとして使用します。

## Drainer に障害が発生し、ダウンストリームのデータが残っている場合に、新しいマシンにDrainer を再展開するにはどうすればよいですか? {#how-to-redeploy-drainer-on-the-new-machine-when-drainer-fails-and-the-data-in-the-downstream-remains}

ダウンストリームのデータが影響を受けない場合は、対応するチェックポイントからデータを複製できる限り、新しいマシンにDrainer を再デプロイできます。

-   チェックポイントが失われていない場合は、次の手順を実行します。

    1.  新しいDrainer をデプロイて起動します ( Drainer はチェックポイントを読み取り、レプリケーションを再開できます)。

    2.  [binlogctl を実行して、古いDrainerの状態を`offline`に変更します。](/tidb-binlog/maintain-tidb-binlog-cluster.md)使用します 。

-   チェックポイントが失われた場合は、次の手順を実行します。

    1.  新しいDrainerを展開するには、古いDrainerの`commit-ts`新しいDrainerの`initialCommitTs`として取得します。

    2.  [binlogctl を実行して、古いDrainerの状態を`offline`に変更します。](/tidb-binlog/maintain-tidb-binlog-cluster.md)使用します 。

## 完全バックアップとbinlogバックアップ ファイルを使用してクラスターのデータを復元するにはどうすればよいですか? {#how-to-restore-the-data-of-a-cluster-using-a-full-backup-and-a-binlog-backup-file}

1.  クラスターをクリーンアップし、完全バックアップを復元します。

2.  バックアップ ファイルの最新データを復元するには、 Reparoを使用して、 `start-tso` = {完全バックアップのスナップショット タイムスタンプ + 1}、 `end-ts` = 0 (または時点を指定することもできます) を設定します。

## プライマリ - セカンダリ レプリケーションで<code>ignore-error</code>有効にすると重大なエラーが発生する場合、 Drainer を再デプロイするにはどうすればよいですか? {#how-to-redeploy-drainer-when-enabling-code-ignore-error-code-in-primary-secondary-replication-triggers-a-critical-error}

`ignore-error`を有効にした後に TiDB がbinlogの書き込みに失敗して重大なエラーがトリガーされると、TiDB はbinlogの書き込みを停止し、 binlogデータの損失が発生します。レプリケーションを再開するには、次の手順を実行します。

1.  Drainerインスタンスを停止します。

2.  重大なエラーをトリガーした`tidb-server`インスタンスを再起動し、binlogの書き込みを再開します (重大なエラーがトリガーされた後、TiDB はPumpにbinlogを書き込みません)。

3.  アップストリームで完全バックアップを実行します。

4.  `tidb_binlog.checkpoint`テーブルを含む下流のデータをクリアします。

5.  フルバックアップをダウンストリームに復元します。

6.  Drainerをデプロイ、初期レプリケーションの開始点として`initialCommitTs` (完全バックアップのスナップショット タイムスタンプとして`initialCommitTs`を設定) を使用します。

## PumpまたはDrainerノードを一時停止または閉じることができるのはいつですか? {#when-can-i-pause-or-close-a-pump-or-drainer-node}

PumpまたはDrainerの状態の説明と、プロセスを開始および終了する方法については、 [TiDBBinlogクラスタ操作](/tidb-binlog/maintain-tidb-binlog-cluster.md)を参照してください。

サービスを一時的に停止する必要がある場合は、PumpまたはDrainerノードを一時停止します。例:

-   バージョンアップグレード

    プロセスが停止した後、新しいバイナリを使用してサービスを再起動します。

-   サーバのメンテナンス

    サーバーのダウンタイムメンテナンスが必要な場合は、プロセスを終了し、メンテナンスの完了後にサービスを再起動します。

サービスが不要になったら、PumpまたはDrainerノードを閉じます。例:

-   Pumpスケールイン

    あまり多くのPumpサービスが必要ない場合は、いくつかを閉じます。

-   レプリケーションタスクのキャンセル

    下流のデータベースにデータを複製する必要がなくなった場合は、対応するDrainerノードを閉じます。

-   サービス移行

    サービスを別のサーバーに移行する必要がある場合は、サービスを閉じて新しいサーバーに再デプロイします。

## PumpまたはDrainerのプロセスを一時停止するにはどうすればよいですか? {#how-can-i-pause-a-pump-or-drainer-process}

-   プロセスを直接終了します。

    > **注記：**
    >
    > `kill -9`コマンドは使用しないでください。そうしないと、PumpまたはDrainerノードが信号を処理できません。

-   PumpまたはDrainerノードがフォアグラウンドで実行されている場合は、 <kbd>Ctrl</kbd> + <kbd>C</kbd>を押して一時停止します。

-   binlogctl で`pause-pump`または`pause-drainer`コマンドを使用します。

## binlogctl の<code>update-pump</code>または<code>update-drainer</code>コマンドを使用して、 PumpまたはDrainerサービスを一時停止できますか? {#can-i-use-the-code-update-pump-code-or-code-update-drainer-code-command-in-binlogctl-to-pause-the-pump-or-drainer-service}

いいえ。コマンド`update-pump`または`update-drainer`は、 PumpまたはDrainer に対応する操作を実行するように通知せずに、PD に保存されている状態情報を直接変更します。2 つのコマンドを誤って使用すると、データのレプリケーションが中断され、データが失われる可能性もあります。

## binlogctl の<code>update-pump</code>または<code>update-drainer</code>コマンドを使用して、 PumpまたはDrainerサービスを閉じることはできますか? {#can-i-use-the-code-update-pump-code-or-code-update-drainer-code-command-in-binlogctl-to-close-the-pump-or-drainer-service}

いいえ。コマンド`update-pump`または`update-drainer`は、 PumpまたはDrainerに対応する操作を実行するように通知せずに、PD に保存されている状態情報を直接変更します。2 つのコマンドを誤って使用すると、データのレプリケーションが中断され、データの不整合が発生する可能性もあります。例:

-   Pumpノードが正常に実行されているか、または`paused`状態にあるときに、 `update-pump`コマンドを使用してPump状態を`offline`に設定すると、 Drainerノードは`offline` Pumpからのbinlogデータの取得を停止します。この状況では、最新のbinlog をDrainerノードに複製できず、上流と下流の間でデータの不整合が発生します。
-   Drainerノードが正常に動作しているときに、 `update-drainer`コマンドを使用してDrainer状態を`offline`に設定すると、新しく起動したPumpノードは`online`状態のDrainerノードにのみ通知します。この状況では、 `offline` Drainer はPumpノードからbinlogデータを時間内に取得できず、上流と下流の間でデータの不整合が発生します。

## いつ binlogctl の<code>update-pump</code>コマンドを使用して、Pumpの状態を<code>paused</code>に設定できますか? {#when-can-i-use-the-code-update-pump-code-command-in-binlogctl-to-set-the-pump-state-to-code-paused-code}

異常な状況によっては、Pumpが状態を正しく維持できないことがあります。その場合は、 `update-pump`コマンドを使用して状態を変更します。

たとえば、 Pumpプロセスが異常終了した場合 (panic発生時にプロセスを直接終了した場合や、誤って`kill -9`コマンドを使用してプロセスを強制終了した場合)、PD に保存されているPumpの状態情報は`online`ままです。この状況で、現時点でPumpを再起動してサービスを回復する必要がない場合は、 `update-pump`コマンドを使用してPump の状態を`paused`に更新します。そうすれば、TiDB が binlog を書き込み、 Drainer がbinlog をプルするときに中断を回避できます。

## binlogctl の<code>update-drainer</code>コマンドを使用して、 Drainer の状態を<code>paused</code>に設定できるのはいつですか? {#when-can-i-use-the-code-update-drainer-code-command-in-binlogctl-to-set-the-drainer-state-to-code-paused-code}

異常な状況では、 Drainerノードが状態を正しく維持できず、レプリケーション タスクに影響を及ぼします。その場合は、 `update-drainer`コマンドを使用して状態を変更します。

たとえば、 Drainerプロセスが異常終了した場合 (panicが発生したときにプロセスを直接終了するか、誤って`kill -9`コマンドを使用してプロセスを強制終了した場合)、PD に保存されているDrainerPump情報は`online`ままです。Pump ノードを起動すると、終了したDrainerノードに通知できず ( `notify drainer ...`エラー)、 Pumpノードが失敗します。この状況では、 `update-drainer`コマンドを使用してDrainer状態を`paused`に更新し、 Pumpノードを再起動します。

## PumpまたはDrainerノードを閉じるにはどうすればよいですか? {#how-can-i-close-a-pump-or-drainer-node}

現在、 PumpまたはDrainerノードを閉じるには、binlogctl の`offline-pump`または`offline-drainer`コマンドのみを使用できます。

## いつ binlogctl の<code>update-pump</code>コマンドを使用して、Pumpの状態を<code>offline</code>に設定できますか? {#when-can-i-use-the-code-update-pump-code-command-in-binlogctl-to-set-the-pump-state-to-code-offline-code}

次の状況では、 `update-pump`コマンドを使用してPumpの状態を`offline`に設定できます。

-   Pumpプロセスが異常終了し、サービスを回復できない場合、レプリケーション タスクは中断されます。レプリケーションを回復し、binlogデータの損失を受け入れる場合は、 `update-pump`コマンドを使用してPump状態を`offline`に設定します。すると、 DrainerノードはPumpノードからのbinlogの取得を停止し、データのレプリケーションを続行します。
-   過去のタスクから古いPumpノードがいくつか残っています。それらのプロセスは終了しており、サービスは不要になっています。次に、 `update-pump`コマンドを使用して、それらの状態を`offline`に設定します。

その他の状況では、 `offline-pump`コマンドを使用して、通常のプロセスであるPumpサービスを閉じます。

> **警告：**
>
> > binlogデータの損失やアップストリームとダウンストリーム間のデータの不整合を許容できる場合、またはPumpノードに保存されているbinlogデータが不要になった場合を除き、 `update-pump`コマンドを使用しないでください。

## 終了して一時<code>paused</code>に設定されているPumpノードを閉じる場合、binlogctl の<code>update-pump</code>コマンドを使用してPump の状態を<code>offline</code>設定できますか? {#can-i-use-the-code-update-pump-code-command-in-binlogctl-to-set-the-pump-state-to-code-offline-code-if-i-want-to-close-a-pump-node-that-is-exited-and-set-to-code-paused-code}

Pumpプロセスが終了し、ノードが`paused`状態にある場合、ノード内のすべてのbinlogデータが下流のDrainerノードで消費されるわけではありません。そのため、これを行うと上流と下流の間でデータの不整合が生じる可能性があります。この状況では、 Pump を再起動し、 `offline-pump`コマンドを使用してPumpノードを閉じます。

## binlogctl の<code>update-drainer</code>コマンドを使用して、 Drainer の状態を<code>offline</code>に設定できるのはいつですか? {#when-can-i-use-the-code-update-drainer-code-command-in-binlogctl-to-set-the-drainer-state-to-code-offline-code}

過去のタスクから古いDrainerノードがいくつか残っています。それらのプロセスは終了しており、サービスは不要になっています。次に、 `update-drainer`コマンドを使用して、それらの状態を`offline`に設定します。

## PumpまたはDrainerサービスを一時停止または閉じるには、 <code>change pump</code>や<code>change drainer</code>などの SQL 操作を使用できますか? {#can-i-use-sql-operations-such-as-code-change-pump-code-and-code-change-drainer-code-to-pause-or-close-the-pump-or-drainer-service}

いいえ。これらの SQL 操作の詳細については、 [SQL文を使用してPumpまたはDrainerを管理する](/tidb-binlog/maintain-tidb-binlog-cluster.md#use-sql-statements-to-manage-pump-or-drainer)を参照してください。

これらの SQL 操作は、PD に保存されている状態情報を直接変更し、機能的には binlogctl の`update-pump`および`update-drainer`コマンドと同等です。Pump またはDrainerサービスを一時停止または閉じるには、binlogctl ツールを使用します。

## アップストリーム データベースでサポートされている一部の DDL ステートメントをダウンストリーム データベースで実行するとエラーが発生する場合は、どうすればよいですか? {#what-can-i-do-when-some-ddl-statements-supported-by-the-upstream-database-cause-error-when-executed-in-the-downstream-database}

この問題を解決するには、次の手順に従ってください。

1.  チェック`drainer.log` 。DrainerDrainerが終了する前に最後に失敗した DDL 操作を`exec failed`で検索します。

2.  DDL バージョンをダウンストリームと互換性のあるバージョンに変更します。この手順はダウンストリーム データベースで手動で実行します。

3.  チェック`drainer.log`失敗した DDL 操作を検索し、この操作の`commit-ts`を見つけます。例:

        [2020/05/21 09:51:58.019 +08:00] [INFO] [syncer.go:398] ["add ddl item to syncer, you can add this commit ts to `ignore-txn-commit-ts` to skip this ddl if needed"] [sql="ALTER TABLE `test` ADD INDEX (`index1`)"] ["commit ts"=416815754209656834].

4.  `drainer.toml`構成ファイルを変更`ignore-txn-commit-ts`ます。5 項目に`commit-ts`を追加し、 Drainerノードを再起動します。

## TiDB がbinlogへの書き込みに失敗して停止し、 <code>listener stopped, waiting for manual stop</code>がログに表示されます。 {#tidb-fails-to-write-to-binlog-and-gets-stuck-and-code-listener-stopped-waiting-for-manual-stop-code-appears-in-the-log}

TiDB v3.0.12 およびそれ以前のバージョンでは、 binlog書き込みの失敗により、TiDB は致命的なエラーを報告します。TiDB は自動的に終了せず、サービスを停止するだけなので、スタックしているように見えます。ログに`listener stopped, waiting for manual stop`エラーが表示されます。

binlog書き込み失敗の具体的な原因を特定する必要があります。binlog がダウンストリームにゆっくりと書き込まれるためにbinlogが発生する場合は、 Pumpをスケールアウトするか、 binlog書き込みのタイムアウト時間を長くすることを検討できます。

v3.0.13 以降、エラー報告ロジックが最適化されています。binlogの書き込みに失敗するとトランザクションの実行が失敗し、TiDBBinlogはエラーを返しますが、TiDB はスタックしません。

## TiDBは重複したバイナリログをPumpに書き込む {#tidb-writes-duplicate-binlogs-to-pump}

この問題は、ダウンストリームおよびレプリケーション ロジックには影響しません。

binlogの書き込みが失敗するかタイムアウトになると、TiDB は書き込みが成功するまで、次の利用可能なPumpノードへのバイナリbinlogの書き込みを再試行します。したがって、 Pumpノードへのbinlogログの書き込みが遅く、TiDB がタイムアウト (デフォルトは 15 秒) になった場合、TiDB は書き込みが失敗したと判断し、次のPumpノードへの書き込みを試みます。タイムアウトの原因となったPumpノードへのbinlogが実際に成功した場合、同じbinlogが複数のPumpノードに書き込まれます。Drainerはbinlogを処理するときに、同じ TSO を持つバイナリログの重複を自動的に排除するため、この重複した書き込みはダウンストリームおよびレプリケーション ロジックに影響しません。

## Reparo は、完全復元および増分復元プロセス中に中断されます。ログ内の最後の TSO を使用してレプリケーションを再開できますか? {#reparo-is-interrupted-during-the-full-and-incremental-restore-process-can-i-use-the-last-tso-in-the-log-to-resume-replication}

はい。Reparoは起動時に自動的にセーフモードを有効にしません。次の手順を手動で実行する必要があります。

1.  Reparoが中断された後、最後の TSO をログに`checkpoint-tso`として記録します。
2.  Reparo構成ファイルを変更し、構成項目`start-tso`を`checkpoint-tso + 1`に、 `stop-tso`を`checkpoint-tso + 80,000,000,000` ( `checkpoint-tso`の約 5 分後) に、 `safe-mode`を`true`に設定します。Reparoを起動すると、 Reparo はデータを`stop-tso`に複製し、その後自動的に停止します。
3.  Reparoが自動的に停止したら、 `start-tso`を`checkpoint tso + 80,000,000,001` 、 `stop-tso`を`0` 、 `safe-mode`を`false`に設定し、 Reparo を起動してレプリケーションを再開します。
