---
title: Backup & Restore FAQs
summary: Learn about Frequently Asked Questions (FAQs) and the solutions of backup and restore.
aliases: ['/tidb/stable/pitr-troubleshoot/','/tidb/stable/pitr-known-issues/']
---

# バックアップと復元に関するよくある質問 {#backup-x26-restore-faqs}

このドキュメントでは、よく寄せられる質問 (FAQ) と、TiDB のバックアップと復元 (BR) の解決策を示します。

## 誤ってデータを削除または更新した後、データを迅速に復元するにはどうすればよいですか? {#what-should-i-do-to-quickly-recover-data-after-mistakenly-deleting-or-updating-data}

TiDB v6.4.0 では、フラッシュバック機能が導入されています。この機能を使用して、GC 時間内のデータを指定された時点まで迅速に回復できます。したがって、誤操作が発生した場合は、この機能を使用してデータを回復できます。詳細については、 [フラッシュバッククラスタ](/sql-statements/sql-statement-flashback-to-timestamp.md)および[フラッシュバック データベース](/sql-statements/sql-statement-flashback-database.md)を参照してください。

## TiDB v5.4.0 以降のバージョンで、負荷の高いクラスターでバックアップ タスクを実行すると、バックアップ タスクの速度が遅くなるのはなぜですか? {#in-tidb-v5-4-0-and-later-versions-when-backup-tasks-are-performed-on-the-cluster-under-a-heavy-workload-why-does-the-speed-of-backup-tasks-become-slow}

TiDB v5.4.0 から、 BR はバックアップ タスクの自動調整機能を導入します。 v5.4.0 以降のバージョンのクラスターの場合、この機能はデフォルトで有効になっています。クラスターのワークロードが重い場合、この機能はバックアップ タスクで使用されるリソースを制限して、オンライン クラスターへの影響を軽減します。詳細については、 [バックアップの自動調整](/br/br-auto-tune.md)を参照してください。

TiKV は[動的構成](/tikv-control.md#modify-the-tikv-configuration-dynamically)自動調整機能をサポートしています。クラスターを再起動せずに、次の方法で機能を有効または無効にすることができます。

-   自動調整を無効にする: TiKV 構成項目[`backup.enable-auto-tune`](/tikv-configuration-file.md#enable-auto-tune-new-in-v540)から`false`を設定します。
-   自動調整を有効にする: `backup.enable-auto-tune` ～ `true`を設定します。 v5.3.x から v5.4.0 以降のバージョンにアップグレードされたクラスターの場合、自動調整機能はデフォルトで無効になっています。手動で有効にする必要があります。

`tikv-ctl`を使用して自動調整を有効または無効にするには、 [自動調整を使用する](/br/br-auto-tune.md#use-auto-tune)を参照してください。

さらに、自動調整により、バックアップ タスクで使用されるデフォルトのスレッド数が減少します。詳細については、 `backup.num-threads` ](/tikv-configuration-file.md#num-threads-1) を参照してください。そのため、Grafana ダッシュボードでは、バックアップ タスクで使用される速度、CPU 使用率、および I/O リソース使用率が、v5.4.0 より前のバージョンよりも低くなります。 v5.4.0 より前では、デフォルト値の`backup.num-threads` `CPU * 0.75`でした。つまり、バックアップ タスクで使用されるスレッドの数は、論理 CPU コアの 75% を占めていました。その最大値は`32`でした。 v5.4.0 以降、この構成項目のデフォルト値は`CPU * 0.5`で、最大値は`8`です。

オフライン クラスターでバックアップ タスクを実行する場合、バックアップを高速化するために、 `tikv-ctl`を使用して`backup.num-threads`の値をより大きな数値に変更できます。

## PITR の問題 {#pitr-issues}

### <a href="/br/br-pitr-guide.md">PITR</a>と<a href="/sql-statements/sql-statement-flashback-to-timestamp.md">クラスター フラッシュバック</a>の違いは何ですか? {#what-is-the-difference-between-a-href-br-br-pitr-guide-md-pitr-a-and-a-href-sql-statements-sql-statement-flashback-to-timestamp-md-cluster-flashback-a}

ユースケースの観点から、PITR は通常、クラスターが完全にサービスを停止している場合、またはデータが破損しており、他のソリューションを使用して回復できない場合に、クラスターのデータを指定された時点に復元するために使用されます。 PITR を使用するには、データ リカバリ用の新しいクラスターが必要です。クラスターのフラッシュバック機能は、ユーザーの誤操作やその他の要因によって引き起こされるデータ エラーのシナリオ向けに特別に設計されており、データ エラーが発生する前の最新のタイムスタンプにクラスターのデータをインプレースで復元できます。

ほとんどの場合、フラッシュバックは RPO (ゼロに近い) と RTO がはるかに短いため、人的ミスによるデータ エラーの場合、PITR よりも優れた復旧ソリューションです。ただし、現時点ではフラッシュバックを実行できないため、クラスターが完全に使用できない場合、PITR はクラスターを回復する唯一のソリューションです。したがって、PITR は、RPO (最大 5 分) と RTO がフラッシュバックよりも長くなりますが、データベースの災害復旧戦略を策定する際には常に必須のソリューションです。

### アップストリーム データベースが物理インポート モードでTiDB Lightningを使用してデータをインポートすると、ログ バックアップ機能が使用できなくなります。なぜ？ {#when-the-upstream-database-imports-data-using-tidb-lightning-in-the-physical-import-mode-the-log-backup-feature-becomes-unavailable-why}

現在、ログ バックアップ機能はTiDB Lightningに完全には適合していません。そのため、 TiDB Lightningの物理モードでインポートされたデータは、ログ データにバックアップできません。

ログ バックアップ タスクを作成するアップストリーム クラスターでは、 TiDB Lightning物理モードを使用してデータをインポートすることは避けてください。代わりに、 TiDB Lightning論理モードを使用できます。物理モードを使用する必要がある場合は、インポートの完了後にスナップショット バックアップを実行して、PITR をスナップショット バックアップ後の時点に復元できるようにします。

### インデックス追加機能の高速化が PITR と互換性がないのはなぜですか? {#why-is-the-acceleration-of-adding-indexes-feature-incompatible-with-pitr}

問題: [#38045](https://github.com/pingcap/tidb/issues/38045)

現在、 [インデックス追加の高速化](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)機能は PITR と互換性がありません。インデックス アクセラレーションを使用する場合は、バックグラウンドで実行されている PITR ログ バックアップ タスクがないことを確認する必要があります。そうしないと、次のような予期しない動作が発生する可能性があります。

-   最初にログ バックアップ タスクを開始してから、インデックスを追加する場合。インデックス アクセラレーションが有効になっていても、インデックスの追加プロセスは高速化されません。しかし、インデックスはゆっくりと追加されます。
-   最初にインデックス アクセラレーション タスクを開始してから、ログ バックアップ タスクを開始した場合。ログ バックアップ タスクがエラーを返します。しかし、インデックスの加速は影響を受けません。
-   ログ バックアップ タスクとインデックス アクセラレーション タスクを同時に開始すると、2 つのタスクが互いを認識しない場合があります。これにより、PITR が新しく追加されたインデックスのバックアップに失敗する可能性があります。

### クラスターはネットワーク パーティションの障害から回復しましたが、ログ バックアップ タスクの進行状況のチェックポイントはまだ再開されません。なぜ？ {#the-cluster-has-recovered-from-the-network-partition-failure-but-the-checkpoint-of-the-log-backup-task-progress-still-does-not-resume-why}

問題: [#13126](https://github.com/tikv/tikv/issues/13126)

クラスタでネットワーク パーティションに障害が発生した後、バックアップ タスクはログのバックアップを続行できません。一定の再試行時間の後、タスクは`ERROR`状態に設定されます。この時点で、バックアップ タスクは停止しています。

この問題を解決するには、 `br log resume`コマンドを手動で実行して、ログ バックアップ タスクを再開する必要があります。

### PITR を実行したときに、 <code>execute over region id</code>エラーが返された場合はどうすればよいですか? {#what-should-i-do-if-the-error-code-execute-over-region-id-code-is-returned-when-i-perform-pitr}

問題: [#37207](https://github.com/pingcap/tidb/issues/37207)

この問題は通常、完全なデータ インポート中にログ バックアップを有効にし、その後 PITR を実行して、データ インポート中のある時点でデータを復元する場合に発生します。

具体的には、長時間 (24 時間など) に多数のホットスポット書き込みがあり、各 TiKV ノードの OPS が 50k/s を超える場合 (メトリクスはGrafana: **TiKV-Details** -&gt; <strong>Backup Log</strong> -&gt; <strong>Handle Event Rate</strong> )。

データのインポート後にスナップショット バックアップを実行し、このスナップショット バックアップに基づいて PITR を実行することをお勧めします。

## <code>br restore point</code>コマンドを使用してダウンストリーム クラスターを復元した後、 TiFlashからデータにアクセスできません。私は何をすべきか？ {#after-restoring-a-downstream-cluster-using-the-code-br-restore-point-code-command-data-cannot-be-accessed-from-tiflash-what-should-i-do}

現在、PITR は、復元段階でのTiFlashへのデータの直接書き込みをサポートしていません。代わりに、br コマンドライン ツールが`ALTER TABLE table_name SET TIFLASH REPLICA ***` DDL を実行してデータをレプリケートします。したがって、PITR がデータの復元を完了した直後は、 TiFlashレプリカは使用できません。代わりに、TiKV ノードからデータがレプリケートされるまで、一定期間待機する必要があります。レプリケーションの進行状況を確認するには、 `INFORMATION_SCHEMA.tiflash_replica`テーブルの`progress`情報を確認します。

### ログ バックアップ タスクの<code>status</code> <code>ERROR</code>になった場合はどうすればよいですか? {#what-should-i-do-if-the-code-status-code-of-a-log-backup-task-becomes-code-error-code}

ログ バックアップ タスク中に失敗し、再試行後に回復できない場合、タスク ステータスは`ERROR`になります。次に例を示します。

```shell
br log status --pd x.x.x.x:2379

● Total 1 Tasks.
> #1 <
                    name: task1
                  status: ○ ERROR
                   start: 2022-07-25 13:49:02.868 +0000
                     end: 2090-11-18 14:07:45.624 +0000
                 storage: s3://tmp/br-log-backup0ef49055-5198-4be3-beab-d382a2189efb/Log
             speed(est.): 0.00 ops/s
      checkpoint[global]: 2022-07-25 14:46:50.118 +0000; gap=11h31m29s
          error[store=1]: KV:LogBackup:RaftReq
error-happen-at[store=1]: 2022-07-25 14:54:44.467 +0000; gap=11h23m35s
  error-message[store=1]: retry time exceeds: and error failed to get initial snapshot: failed to get the snapshot (region_id = 94812): Error during requesting raftstore: message: "read index not ready, reason can not read index due to merge, region 94812" read_index_not_ready { reason: "can not read index due to merge" region_id: 94812 }: failed to get initial snapshot: failed to get the snapshot (region_id = 94812): Error during requesting raftstore: message: "read index not ready, reason can not read index due to merge, region 94812" read_index_not_ready { reason: "can not read index due to merge" region_id: 94812 }: failed to get initial snapshot: failed to get the snapshot (region_id = 94812): Error during requesting raftstore: message: "read index not ready, reason can not read index due to merge, region 94812" read_index_not_ready { reason: "can not read index due to merge" region_id: 94812 }
```

この問題を解決するには、エラー メッセージで原因を確認し、指示に従ってください。問題が解決したら、次のコマンドを実行してタスクを再開します。

```shell
br log resume --task-name=task1 --pd x.x.x.x:2379
```

バックアップ タスクが再開されたら、 `br log status`を使用してステータスを確認できます。タスクのステータスが`NORMAL`になると、バックアップ タスクは続行されます。

```shell
● Total 1 Tasks.
> #1 <
              name: task1
            status: ● NORMAL
             start: 2022-07-25 13:49:02.868 +0000
               end: 2090-11-18 14:07:45.624 +0000
           storage: s3://tmp/br-log-backup0ef49055-5198-4be3-beab-d382a2189efb/Log
       speed(est.): 15509.75 ops/s
checkpoint[global]: 2022-07-25 14:46:50.118 +0000; gap=6m28s
```

> **ノート：**
>
> この機能は、複数のバージョンのデータをバックアップします。長時間のバックアップ タスクが失敗し、ステータスが`ERROR`になると、このタスクのチェックポイント データは`safe point`に設定され、 `safe point`のデータは 24 時間以内にガベージ コレクションされません。したがって、エラーが再開された後、バックアップ タスクは最後のチェックポイントから続行されます。タスクが 24 時間以上失敗し、最後のチェックポイント データがガベージ コレクションされている場合、タスクを再開するとエラーが報告されます。この場合、最初にタスクを停止してから新しいバックアップ タスクを開始する`br log stop`コマンドしか実行できません。

### <code>br log resume</code>コマンドを使用して中断されたタスクを再開するときに、エラー メッセージ<code>ErrBackupGCSafepointExceeded</code>が返された場合はどうすればよいですか? {#what-should-i-do-if-the-error-message-code-errbackupgcsafepointexceeded-code-is-returned-when-using-the-code-br-log-resume-code-command-to-resume-a-suspended-task}

```shell
Error: failed to check gc safePoint, checkpoint ts 433177834291200000: GC safepoint 433193092308795392 exceed TS 433177834291200000: [BR:Backup:ErrBackupGCSafepointExceeded]backup GC safepoint exceeded
```

ログ バックアップ タスクを一時停止した後、MVCC データがガベージ コレクションされるのを防ぐために、一時停止中のタスク プログラムは、現在のチェックポイントをサービス セーフポイントとして自動的に設定します。これにより、24 時間以内に生成された MVCC データを確実に残すことができます。バックアップ チェックポイントの MVCC データが 24 時間以上生成されている場合、チェックポイントのデータはガベージ コレクションされ、バックアップ タスクは再開できません。

この問題に対処するには、 `br log stop`使用して現在のタスクを削除し、 `br log start`使用してログ バックアップ タスクを作成します。同時に、後続の PITR のフル バックアップを実行できます。

## 機能の互換性の問題 {#feature-compatibility-issues}

### br コマンドライン ツールを使用して復元されたデータを TiCDC またはDrainerのアップストリーム クラスターに複製できないのはなぜですか? {#why-does-data-restored-using-br-command-line-tool-cannot-be-replicated-to-the-upstream-cluster-of-ticdc-or-drainer}

-   **BRを使用して復元されたデータは、ダウンストリームに複製できません**。これは、 BR はSST ファイルを直接インポートしますが、現在、ダウンストリーム クラスターはこれらのファイルをアップストリームから取得できないためです。

-   v4.0.3 より前では、復元中に生成された DDL ジョブにより、TiCDC/ Drainerで予期しない DDL が実行される場合がありました。したがって、TiCDC/ Drainerのアップストリーム クラスターで復元を実行する必要がある場合は、br コマンドライン ツールを使用して復元されたすべてのテーブルを TiCDC/ Drainerブロック リストに追加します。

[`filter.rules`](https://github.com/pingcap/tiflow/blob/7c3c2336f98153326912f3cf6ea2fbb7bcc4a20c/cmd/changefeed.toml#L16)を使用して TiCDC のブロック リストを構成し、 [`syncer.ignore-table`](/tidb-binlog/tidb-binlog-configuration-file.md#ignore-table)を使用してDrainerのブロック リストを構成できます。

### 復元中に<code>new_collations_enabled_on_first_bootstrap</code>の不一致が報告されるのはなぜですか? {#why-is-code-new-collations-enabled-on-first-bootstrap-code-mismatch-reported-during-restore}

TiDB v6.0.0 以降、デフォルト値の[`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)が`false`から`true`に変更されました。 BR は上流クラスタの`new_collations_enabled_on_first_bootstrap`構成をバックアップし、この構成の値が上流クラスタと下流クラスタの間で一致しているかどうかを確認します。値が一致する場合、 BR は上流のクラスターにバックアップされたデータを下流のクラスターに安全に復元します。値が一致しない場合、 BR はデータの復元を実行せず、エラーを報告します。

v6.0.0 の以前のバージョンの TiDB クラスター内のデータをバックアップしており、このデータを v6.0.0 以降のバージョンの TiDB クラスターに復元するとします。この状況では、 `new_collations_enabled_on_first_bootstrap`の値がアップストリーム クラスターとダウンストリーム クラスター間で一貫しているかどうかを手動で確認する必要があります。

-   値が一貫している場合は、restore コマンドに`--check-requirements=false`を追加して、この構成チェックをスキップできます。
-   値に一貫性がなく、復元を強制的に実行すると、 BR はデータ検証エラーを報告します。

### 配置ルールをクラスターに復元するとエラーが発生するのはなぜですか? {#why-does-an-error-occur-when-i-restore-placement-rules-to-a-cluster}

v6.0.0 より前では、 BR は[配置ルール](/placement-rules-in-sql.md)をサポートしていません。 v6.0.0 以降、 BR は配置ルールをサポートし、コマンドライン オプション`--with-tidb-placement-mode=strict/ignore`を導入して、配置ルールのバックアップおよび復元モードを制御します。デフォルト値`strict`では、 BR は配置ルールをインポートして検証しますが、値が`ignore`の場合はすべての配置ルールを無視します。

## データ復元の問題 {#data-restore-issues}

### <code>Io(Os...)</code>エラーを処理するにはどうすればよいですか? {#what-should-i-do-to-handle-the-code-io-os-code-error}

これらの問題のほとんどは、TiKV がディスクにデータを書き込むときに発生するシステム コール エラーです (例: `Io(Os {code: 13, kind: PermissionDenied...})`または`Io(Os {code: 2, kind: NotFound...})` )。

このような問題を解決するには、まずバックアップ ディレクトリのマウント方法とファイル システムを確認し、別のフォルダまたは別のハードディスクにデータをバックアップしてみてください。

たとえば、 `samba`によって構築されたネットワーク ディスクにデータをバックアップするときに、 `Code: 22(invalid argument)`エラーが発生する場合があります。

### <code>rpc error: code = Unavailable desc =...</code>復元中にエラーが発生しましたか? {#what-should-i-do-to-handle-the-code-rpc-error-code-unavailable-desc-code-error-occurred-in-restore}

このエラーは、復元するクラスターの容量が不足している場合に発生する可能性があります。このクラスターの監視メトリクスまたは TiKV ログを確認することで、原因をさらに確認できます。

この問題を処理するには、クラスター リソースをスケール アウトし、復元中の同時実行数を減らして、 `RATE_LIMIT`オプションを有効にします。

### <code>the entry too large, the max entry size is 6291456, the size of data is 7690800</code>エラー メッセージで復元が失敗した場合はどうすればよいですか? {#what-should-i-do-if-the-restore-fails-with-the-error-message-code-the-entry-too-large-the-max-entry-size-is-6291456-the-size-of-data-is-7690800-code}

`--ddl-batch-size` ～ `128`以下の値を設定することで、一度に作成するテーブルの数を減らすことができます。

BRを使用して [ `--ddl-batch-size` ](/br/br-batch-create-table.md#how to use) の値が`1`より大きいバックアップ データを復元する場合、TiDB はテーブル作成の DDL ジョブを DDL ジョブ キューに書き込みます。これは TiKV によって維持されます。現時点では、TiDB が一度に送信するすべてのテーブル スキーマの合計サイズは 6 MB を超えてはなりません。これは、ジョブ メッセージの最大値がデフォルトで`6 MB`であるためです (この値を変更することは**お勧めしません**。詳細については、 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50)および を参照してください)。 [`raft-entry-max-size`](/tikv-configuration-file.md#raft-entry-max-size) ）。したがって、 `--ddl-batch-size`過度に大きな値に設定すると、TiDB によって一度にバッチで送信されるテーブルのスキーマ サイズが指定された値を超えるため、 BR は`entry too large, the max entry size is 6291456, the size of data is 7690800`エラーを報告します。

### <code>local</code>storageを使用する場合、バックアップ ファイルはどこに保存されますか? {#where-are-the-backed-up-files-stored-when-i-use-code-local-code-storage}

> **ノート：**
>
> ネットワーク ファイル システム (NFS) がBRまたは TiKV ノードにマウントされていない場合、または Amazon S3、GCS、または Azure Blob Storage プロトコルをサポートする外部storageを使用している場合、 BRによってバックアップされたデータは各 TiKV ノードで生成されます。バックアップ データは各ノードのローカル ファイル システムに分散しているため、**これはBRを展開するための推奨される方法ではないことに注意してください**。バックアップデータを採取すると、データの冗長性や運用・保守上の問題が発生する可能性があります。一方、バックアップ データを収集する前にデータを直接復元すると、エラー`SST file not found`が発生します。

ローカルstorageを使用する場合、 BRが実行されているノードに`backupmeta`が生成され、各リージョンのLeaderノードにバックアップ ファイルが生成されます。

### データの復元中にエラー メッセージ<code>could not read local://...:download sst failed</code>返された場合はどうすればよいですか? {#what-should-i-do-if-the-error-message-code-could-not-read-local-download-sst-failed-code-is-returned-during-data-restore}

データを復元する場合、各ノードは**すべての**バックアップ ファイル (SST ファイル) にアクセスできる必要があります。デフォルトでは、 `local`storageが使用されている場合、バックアップ ファイルが異なるノードに分散しているため、データを復元できません。したがって、各 TiKV ノードのバックアップ ファイルを他の TiKV ノードにコピーする必要があります。<strong>バックアップ データを Amazon S3、Google Cloud Storage (GCS)、Azure Blob Storage、または NFS に保存することをお勧めします</strong>。

### root を使用して<code>br</code>を実行しようとしても失敗した場合でも、 <code>Permission denied</code>または<code>No such file or directory</code>エラーを処理するにはどうすればよいですか? {#what-should-i-do-to-handle-the-code-permission-denied-code-or-code-no-such-file-or-directory-code-error-even-if-i-have-tried-to-run-code-br-code-using-root-in-vain}

TiKV がバックアップ ディレクトリにアクセスできるかどうかを確認する必要があります。データをバックアップするには、TiKV に書き込み権限があるかどうかを確認します。データを復元するには、読み取り権限があるかどうかを確認してください。

バックアップ操作中、storageメディアがローカル ディスクまたはネットワーク ファイル システム (NFS) の場合、 `br`を起動するユーザーと TiKV を起動するユーザーが一致していることを確認します ( `br`と TiKV が別のマシンにある場合、ユーザーは&#39; UID は一貫している必要があります)。そうしないと、 `Permission denied`問題が発生する可能性があります。

バックアップ ファイル (SST ファイル) は TiKV によって保存されるため、 `root`人のユーザーとして`br`を実行すると、ディスクのアクセス許可が原因で失敗する可能性があります。

> **ノート：**
>
> データの復元中に同じ問題が発生する可能性があります。 SST ファイルが初めて読み取られるときに、読み取り許可が検証されます。 DDL の実行時間は、アクセス許可のチェックと実行の間に長い間隔がある可能性があることを示唆しています`br` 。長時間待機すると、エラー メッセージ`Permission denied`表示される場合があります。

したがって、次の手順に従って、データを復元する前に権限を確認することをお勧めします。

1.  プロセス クエリの Linux コマンドを実行します。

    {{< copyable "" >}}

    ```bash
    ps aux | grep tikv-server
    ```

    出力は次のとおりです。

    ```shell
    tidb_ouo  9235 10.9  3.8 2019248 622776 ?      Ssl  08:28   1:12 bin/tikv-server --addr 0.0.0.0:20162 --advertise-addr 172.16.6.118:20162 --status-addr 0.0.0.0:20188 --advertise-status-addr 172.16.6.118:20188 --pd 172.16.6.118:2379 --data-dir /home/user1/tidb-data/tikv-20162 --config conf/tikv.toml --log-file /home/user1/tidb-deploy/tikv-20162/log/tikv.log
    tidb_ouo  9236  9.8  3.8 2048940 631136 ?      Ssl  08:28   1:05 bin/tikv-server --addr 0.0.0.0:20161 --advertise-addr 172.16.6.118:20161 --status-addr 0.0.0.0:20189 --advertise-status-addr 172.16.6.118:20189 --pd 172.16.6.118:2379 --data-dir /home/user1/tidb-data/tikv-20161 --config conf/tikv.toml --log-file /home/user1/tidb-deploy/tikv-20161/log/tikv.log
    ```

    または、次のコマンドを実行できます。

    {{< copyable "" >}}

    ```bash
    ps aux | grep tikv-server | awk '{print $1}'
    ```

    出力は次のとおりです。

    ```shell
    tidb_ouo
    tidb_ouo
    ```

2.  `tiup`コマンドを使用して、クラスターの起動情報を照会します。

    {{< copyable "" >}}

    ```bash
    tiup cluster list
    ```

    出力は次のとおりです。

    ```shell
    [root@Copy-of-VM-EE-CentOS76-v1 br]# tiup cluster list
    Starting component `cluster`: /root/.tiup/components/cluster/v1.5.2/tiup-cluster list
    Name          User      Version  Path                                               PrivateKey
    ----          ----      -------  ----                                               ----------
    tidb_cluster  tidb_ouo  v5.0.2   /root/.tiup/storage/cluster/clusters/tidb_cluster  /root/.tiup/storage/cluster/clusters/tidb_cluster/ssh/id_rsa
    ```

3.  バックアップディレクトリの権限を確認してください。たとえば、 `backup`はバックアップ データstorage用です。

    {{< copyable "" >}}

    ```bash
    ls -al backup
    ```

    出力は次のとおりです。

    ```shell
    [root@Copy-of-VM-EE-CentOS76-v1 user1]# ls -al backup
    total 0
    drwxr-xr-x  2 root root   6 Jun 28 17:48 .
    drwxr-xr-x 11 root root 310 Jul  4 10:35 ..
    ```

    ステップ 2 の出力から、 `tikv-server`インスタンスがユーザー`tidb_ouo`によって開始されていることがわかります。しかし、ユーザー`tidb_ouo`は`backup`に対する書き込み権限がありません。したがって、バックアップは失敗します。

### <code>mysql</code>スキーマのテーブルが復元されないのはなぜですか? {#why-are-tables-in-the-code-mysql-code-schema-not-restored}

BR v5.1.0 以降、フル バックアップを実行すると、 BR は**`mysql`スキーマのテーブル**をバックアップします。 BR v6.2.0 より前のデフォルト設定では、 BR はユーザー データのみを復元し、 <strong><code>mysql</code>スキーマ</strong>内のテーブルは復元しません。

`mysql`スキーマ (システム テーブルではない) でユーザーが作成したテーブルを復元するには、 [テーブル フィルター](/table-filter.md#syntax)使用して明示的にテーブルを含めることができます。次の例は、 BR が通常の復元を実行するときに`mysql.usertable`テーブルを復元する方法を示しています。

{{< copyable "" >}}

```shell
br restore full -f '*.*' -f '!mysql.*' -f 'mysql.usertable' -s $external_storage_url --with-sys-table
```

前のコマンドでは、

-   `-f '*.*'`は、デフォルトのルールをオーバーライドするために使用されます
-   `-f '!mysql.*'`特に明記されていない限り、 `mysql`でテーブルを復元しないようにBRに指示します。
-   `-f 'mysql.usertable'` `mysql.usertable`を復元する必要があることを示します。

`mysql.usertable`のみを復元する必要がある場合は、次のコマンドを実行します。

{{< copyable "" >}}

```shell
br restore full -f 'mysql.usertable' -s $external_storage_url --with-sys-table
```

[テーブル フィルター](/table-filter.md#syntax)を構成しても、 **BR は次のシステム テーブルを復元しないこと**に注意してください。

-   統計表 ( `mysql.stat_*` )
-   システム変数テーブル ( `mysql.tidb` 、 `mysql.global_variables` )
-   [その他のシステム テーブル](https://github.com/pingcap/tidb/blob/master/br/pkg/restore/systable_restore.go#L31)

## バックアップと復元について知っておくべきその他の事項 {#other-things-you-may-want-to-know-about-backup-and-restore}

### バックアップデータのサイズは？バックアップのレプリカはありますか? {#what-is-the-size-of-the-backup-data-are-there-replicas-of-the-backup}

データのバックアップ中に、各リージョンのLeaderノードでバックアップ ファイルが生成されます。バックアップのサイズはデータ サイズと同じで、冗長レプリカはありません。したがって、データの合計サイズは、ほぼ TiKV データの合計数をレプリカの数で割ったものになります。

ただし、ローカルstorageからデータを復元する場合は、各 TiKV がすべてのバックアップ ファイルにアクセスできる必要があるため、レプリカの数は TiKV ノードの数と同じになります。

### BRを使用したバックアップまたは復元後に、監視ノードに表示されるディスク使用量が一貫していないのはなぜですか? {#why-is-the-disk-usage-shown-on-the-monitoring-node-inconsistent-after-backup-or-restore-using-br}

この不一致は、バックアップで使用されるデータ圧縮率が復元で使用されるデフォルトの率と異なるという事実によって発生します。チェックサムが成功した場合、この問題は無視できます。

### BR がバックアップ データを復元した後、テーブルとインデックスの TiDB の統計を更新するためにテーブルで<code>ANALYZE</code>ステートメントを実行する必要がありますか? {#after-br-restores-the-backup-data-do-i-need-to-execute-the-code-analyze-code-statement-on-the-table-to-update-the-statistics-of-tidb-on-the-tables-and-indexes}

BR は統計をバックアップしません (v4.0.9 を除く)。したがって、バックアップデータを復元した後、手動で実行するか`ANALYZE TABLE` 、または TiDB が自動的に実行されるのを待つ必要があります`ANALYZE` 。

v4.0.9 では、 BR はデフォルトで統計をバックアップしますが、これは大量のメモリを消費します。バックアップ プロセスが正常に行われるようにするため、v4.0.10 以降、統計のバックアップはデフォルトで無効になっています。

テーブルに対して`ANALYZE`を実行しないと、TiDB は不正確な統計のために最適な実行計画を選択できません。クエリのパフォーマンスが重要な問題でない場合は、 `ANALYZE`を無視できます。

### 複数の復元タスクを同時に開始して、1 つのクラスターのデータを復元することはできますか? {#can-i-start-multiple-restore-tasks-at-the-same-time-to-restore-the-data-of-a-single-cluster}

次の理由から、複数の復元タスクを同時に開始して単一クラスターのデータを復元すること**は強くお勧めしません**。

-   BR がデータを復元すると、PD の一部のグローバル構成が変更されます。そのため、データの復元のために複数の復元タスクを同時に開始すると、これらの構成が誤って上書きされ、クラスターの状態が異常になる可能性があります。
-   BR はデータを復元するために多くのクラスター リソースを消費するため、実際には、復元タスクを並行して実行しても復元速度は限られた範囲でしか改善されません。
-   データ復元のために複数の復元タスクを並行して実行するテストは行われていないため、成功する保証はありません。

### BR は、テーブルの<code>SHARD_ROW_ID_BITS</code>および<code>PRE_SPLIT_REGIONS</code>情報をバックアップしますか?復元されたテーブルには複数のリージョンがありますか? {#does-br-back-up-the-code-shard-row-id-bits-code-and-code-pre-split-regions-code-information-of-a-table-does-the-restored-table-have-multiple-regions}

はい。 BR は、テーブルの[`SHARD_ROW_ID_BITS`および<code>PRE_SPLIT_REGIONS</code>](/sql-statements/sql-statement-split-region.md#pre_split_regions)情報をバックアップします。復元されたテーブルのデータも複数のリージョンに分割されます。
