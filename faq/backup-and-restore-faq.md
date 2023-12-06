---
title: Backup & Restore FAQs
summary: Learn about Frequently Asked Questions (FAQs) and the solutions of backup and restore.
---

# バックアップと復元に関するよくある質問 {#backup-x26-restore-faqs}

このドキュメントには、TiDB バックアップ &amp; リストア (BR) に関するよくある質問 (FAQ) と解決策がリストされています。

## 誤ってデータを削除または更新した後、すぐにデータを復元するにはどうすればよいですか? {#what-should-i-do-to-quickly-recover-data-after-mistakenly-deleting-or-updating-data}

TiDB v6.4.0 にはフラッシュバック機能が導入されています。この機能を使用すると、GC 時間内で指定した時点までデータを迅速にリカバリできます。したがって、誤操作が発生した場合、この機能を使用してデータを回復できます。詳細は[フラッシュバッククラスタ](/sql-statements/sql-statement-flashback-to-timestamp.md)および[フラッシュバックデータベース](/sql-statements/sql-statement-flashback-database.md)を参照してください。

## TiDB v5.4.0 以降のバージョンでは、負荷の高いクラスターでバックアップ タスクが実行されると、バックアップ タスクの速度が遅くなるのはなぜですか? {#in-tidb-v5-4-0-and-later-versions-when-backup-tasks-are-performed-on-the-cluster-under-a-heavy-workload-why-does-the-speed-of-backup-tasks-become-slow}

TiDB v5.4.0 以降、 BR にはバックアップ タスクの自動調整機能が導入されています。 v5.4.0 以降のバージョンのクラスターの場合、この機能はデフォルトで有効になっています。クラスターのワークロードが重い場合、この機能はバックアップ タスクで使用されるリソースを制限し、オンライン クラスターへの影響を軽減します。詳細については、 [バックアップの自動調整](/br/br-auto-tune.md)を参照してください。

TiKV は自動調整[動的構成](/tikv-control.md#modify-the-tikv-configuration-dynamically)をサポートしています。クラスターを再起動せずに、次の方法でこの機能を有効または無効にできます。

-   自動調整を無効にする: TiKV 構成項目[`backup.enable-auto-tune`](/tikv-configuration-file.md#enable-auto-tune-new-in-v540)から`false`を設定します。
-   自動調整を有効にする: `backup.enable-auto-tune` ～ `true`を設定します。 v5.3.x から v5.4.0 以降のバージョンにアップグレードされたクラスターの場合、自動調整機能はデフォルトで無効になっています。手動で有効にする必要があります。

`tikv-ctl`を使用して自動調整を有効または無効にするには、 [自動調整を使用する](/br/br-auto-tune.md#use-auto-tune)を参照してください。

さらに、自動調整により、バックアップ タスクで使用されるデフォルトのスレッド数が減少します。詳細については、 `backup.num-threads` ](/tikv-configuration-file.md#num-threads-1)」を参照してください。したがって、Grafana ダッシュボードでは、バックアップ タスクによって使用される速度、CPU 使用率、および I/O リソース使用率が v5.4.0 より前のバージョンよりも低くなります。 v5.4.0 より前では、デフォルト値`backup.num-threads`は`CPU * 0.75`でした。つまり、バックアップ タスクによって使用されるスレッドの数が論理 CPU コアの 75% を占めます。その最大値は`32`でした。 v5.4.0 以降、この構成項目のデフォルト値は`CPU * 0.5` 、最大値は`8`です。

オフライン クラスターでバックアップ タスクを実行する場合、バックアップを高速化するために、 `tikv-ctl`を使用して`backup.num-threads`の値をより大きな数値に変更できます。

## PITRの問題 {#pitr-issues}

### <a href="/br/br-pitr-guide.md">PITR</a>と<a href="/sql-statements/sql-statement-flashback-to-timestamp.md">クラスターフラッシュバック</a>の違いは何ですか? {#what-is-the-difference-between-a-href-br-br-pitr-guide-md-pitr-a-and-a-href-sql-statements-sql-statement-flashback-to-timestamp-md-cluster-flashback-a}

ユースケースの観点から見ると、PITR は通常、クラスターが完全にサービス停止になった場合、またはデータが破損して他のソリューションを使用して回復できない場合に、クラスターのデータを指定された時点に復元するために使用されます。 PITR を使用するには、データ回復用の新しいクラスターが必要です。クラスターのフラッシュバック機能は、ユーザーの誤操作やその他の要因によって引き起こされるデータ エラーのシナリオ向けに特別に設計されており、データ エラーが発生する前の最新のタイムスタンプにクラスターのデータをインプレースで復元できます。

ほとんどの場合、フラッシュバックは、RPO (ゼロに近い) と RTO がはるかに短いため、人的ミスによって引き起こされたデータ エラーに対しては、PITR よりも優れた回復ソリューションです。ただし、クラスターが完全に使用できない場合、現時点ではフラッシュバックを実行できないため、この場合クラスターを回復する唯一のソリューションは PITR です。したがって、PITR は、フラッシュバックよりも RPO (最大 5 分) と RTO が長いにもかかわらず、データベースのディザスタ リカバリ戦略を策定する際には常に必須のソリューションです。

### アップストリーム データベースが物理インポート モードでTiDB Lightningを使用してデータをインポートすると、ログ バックアップ機能が使用できなくなります。なぜ？ {#when-the-upstream-database-imports-data-using-tidb-lightning-in-the-physical-import-mode-the-log-backup-feature-becomes-unavailable-why}

現在、ログ バックアップ機能はTiDB Lightningに完全には適合していません。そのため、 TiDB Lightningの物理モードでインポートしたデータはログデータにバックアップできません。

ログ バックアップ タスクを作成するアップストリーム クラスターでは、データのインポートにTiDB Lightning物理モードを使用しないでください。代わりに、 TiDB Lightning論理モードを使用できます。物理モードを使用する必要がある場合は、インポートの完了後にスナップショット バックアップを実行して、PITR をスナップショット バックアップ後の時点に復元できるようにします。

### インデックス追加の高速化機能が PITR と互換性がないのはなぜですか? {#why-is-the-acceleration-of-adding-indexes-feature-incompatible-with-pitr}

問題: [#38045](https://github.com/pingcap/tidb/issues/38045)

現在、 [インデックス加速度](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)機能で作成されたインデックス データは PITR でバックアップできません。

したがって、PITR リカバリの完了後、 BR はインデックス アクセラレーションによって作成されたインデックス データを削除し、再作成します。インデックス アクセラレーションによって多数のインデックスが作成された場合、またはログ バックアップ中にインデックス データが大きい場合は、インデックスの作成後にフル バックアップを実行することをお勧めします。

### クラスターはネットワーク パーティションの障害から回復しましたが、ログ バックアップ タスクの進行状況のチェックポイントはまだ再開されません。なぜ？ {#the-cluster-has-recovered-from-the-network-partition-failure-but-the-checkpoint-of-the-log-backup-task-progress-still-does-not-resume-why}

問題: [#13126](https://github.com/tikv/tikv/issues/13126)

クラスター内でネットワーク パーティションに障害が発生すると、バックアップ タスクはログのバックアップを続行できなくなります。一定の再試行時間が経過すると、タスクは`ERROR`状態に設定されます。この時点で、バックアップ タスクは停止しました。

この問題を解決するには、 `br log resume`コマンドを手動で実行してログ バックアップ タスクを再開する必要があります。

### PITR を実行すると、 <code>execute over region id</code>エラーが返された場合はどうすればよいですか? {#what-should-i-do-if-the-error-code-execute-over-region-id-code-is-returned-when-i-perform-pitr}

問題: [#37207](https://github.com/pingcap/tidb/issues/37207)

この問題は通常、完全データ インポート中にログ バックアップを有効にし、その後 PITR を実行してデータ インポート中の特定の時点でデータを復元した場合に発生します。

具体的には、長時間 (24 時間など) に大量のホットスポット書き込みがあり、各 TiKV ノードの OPS が 50k/s を超えている場合に、この問題が発生する可能性があります (メトリクスは次のとおりです)。 Grafana: **TiKV-詳細**-&gt;**バックアップ ログ**-&gt;**ハンドル イベント レート**)。

データのインポート後にスナップショット バックアップを実行し、このスナップショット バックアップに基づいて PITR を実行することをお勧めします。

## <code>br restore point</code>コマンドを使用してダウンストリーム クラスターを復元した後、 TiFlashからデータにアクセスできなくなります。どうすればいいですか？ {#after-restoring-a-downstream-cluster-using-the-code-br-restore-point-code-command-data-cannot-be-accessed-from-tiflash-what-should-i-do}

現在、PITR は復元フェーズ中にTiFlashにデータを直接書き込むことをサポートしていません。代わりに、br コマンドライン ツールは`ALTER TABLE table_name SET TIFLASH REPLICA ***` DDL を実行してデータを複製します。したがって、 TiFlashレプリカは、PITR がデータの復元を完了した直後には使用できません。代わりに、TiKV ノードからデータがレプリケートされるまで一定期間待機する必要があります。レプリケーションの進行状況を確認するには、 `INFORMATION_SCHEMA.tiflash_replica`表の`progress`情報を確認します。

### ログ バックアップ タスクの<code>status</code> <code>ERROR</code>になった場合はどうすればよいですか? {#what-should-i-do-if-the-code-status-code-of-a-log-backup-task-becomes-code-error-code}

ログ バックアップ タスク中に失敗し、再試行しても回復できない場合、タスク ステータスは`ERROR`になります。以下は例です。

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

この問題を解決するには、エラー メッセージで原因を確認し、指示に従って実行してください。問題が解決されたら、次のコマンドを実行してタスクを再開します。

```shell
br log resume --task-name=task1 --pd x.x.x.x:2379
```

バックアップ タスクが再開された後、 `br log status`使用してステータスを確認できます。タスクのステータスが`NORMAL`になっても、バックアップ タスクは続行されます。

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

> **注記：**
>
> この機能は、複数のバージョンのデータをバックアップします。長時間バックアップ タスクが失敗し、ステータスが`ERROR`になると、このタスクのチェックポイント データは`safe point`に設定され、 `safe point`のデータは 24 時間以内にガベージ コレクションされません。したがって、バックアップ タスクは、エラーが再開された後、最後のチェックポイントから続行されます。タスクが 24 時間以上失敗し、最後のチェックポイント データがガベージ コレクションされている場合、タスクを再開するとエラーが報告されます。この場合、 `br log stop`コマンドを実行して最初にタスクを停止し、次に新しいバックアップ タスクを開始することしかできません。

### <code>br log resume</code>コマンドを使用して一時停止されたタスクを再開するときに、エラー メッセージ<code>ErrBackupGCSafepointExceeded</code>が返された場合はどうすればよいですか? {#what-should-i-do-if-the-error-message-code-errbackupgcsafepointexceeded-code-is-returned-when-using-the-code-br-log-resume-code-command-to-resume-a-suspended-task}

```shell
Error: failed to check gc safePoint, checkpoint ts 433177834291200000: GC safepoint 433193092308795392 exceed TS 433177834291200000: [BR:Backup:ErrBackupGCSafepointExceeded]backup GC safepoint exceeded
```

ログ バックアップ タスクを一時停止した後、MVCC データがガベージ コレクションされるのを防ぐために、一時停止中のタスク プログラムは現在のチェックポイントをサービス セーフポイントとして自動的に設定します。これにより、24 時間以内に生成された MVCC データが確実に保持されます。バックアップ チェックポイントの MVCC データが生成されてから 24 時間以上経過している場合、チェックポイントのデータはガベージ コレクションされ、バックアップ タスクは再開できません。

この問題に対処するには、 `br log stop`使用して現在のタスクを削除し、 `br log start`使用してログ バックアップ タスクを作成します。同時に、後続の PITR 用に完全バックアップを実行できます。

## 機能の互換性の問題 {#feature-compatibility-issues}

### br コマンドライン ツールを使用して復元されたデータが TiCDC またはDrainerの上流クラスターに複製できないのはなぜですか? {#why-does-data-restored-using-br-command-line-tool-cannot-be-replicated-to-the-upstream-cluster-of-ticdc-or-drainer}

-   **BRを使用して復元されたデータは、ダウンストリームに複製できません**。これは、 BR がSST ファイルを直接インポートしますが、現在ダウンストリーム クラスターがアップストリームからこれらのファイルを取得できないためです。

-   v4.0.3 より前では、リストア中に生成された DDL ジョブにより、 TiCDC/ Drainerで予期しない DDL 実行が発生する可能性がありました。したがって、 TiCDC/ Drainerの上流クラスターでリストアを実行する必要がある場合は、 br コマンドライン ツールを使用してリストアされたすべてのテーブルを TiCDC/ Drainerブロック リストに追加します。

[`filter.rules`](https://github.com/pingcap/tiflow/blob/7c3c2336f98153326912f3cf6ea2fbb7bcc4a20c/cmd/changefeed.toml#L16)を使用して TiCDC のブロック リストを構成し、 [`syncer.ignore-table`](/tidb-binlog/tidb-binlog-configuration-file.md#ignore-table)を使用してDrainerのブロック リストを構成できます。

### 復元中に<code>new_collation_enabled</code>不一致が報告されるのはなぜですか? {#why-is-code-new-collation-enabled-code-mismatch-reported-during-restore}

TiDB v6.0.0 以降、デフォルト値[`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)が`false`から`true`に変更されました。 BR は、上流クラスタの`mysql.tidb`テーブル内の`new_collation_enabled`設定をバックアップし、この設定の値が上流クラスタと下流クラスタ間で一貫しているかどうかを確認します。値が一貫している場合、 BR は上流クラスターにバックアップされたデータを下流クラスターに安全に復元します。値が矛盾している場合、 BR はデータの復元を実行せず、エラーを報告します。

以前のバージョンの v6.0.0 の TiDB クラスターにデータをバックアップしており、このデータを v6.0.0 以降のバージョンの TiDB クラスターに復元するとします。この状況では、値`new_collations_enabled_on_first_bootstrap`がアップストリーム クラスターとダウンストリーム クラスター間で一致しているかどうかを手動で確認する必要があります。

-   値が一貫している場合は、restore コマンドに`--check-requirements=false`を追加して、この構成チェックをスキップできます。
-   値に一貫性がない場合、リストアを強制的に実行すると、 BR はデータ検証エラーを報告します。

### 配置ルールをクラスターに復元するとエラーが発生するのはなぜですか? {#why-does-an-error-occur-when-i-restore-placement-rules-to-a-cluster}

v6.0.0 より前では、 BR は[配置ルール](/placement-rules-in-sql.md)をサポートしていません。 v6.0.0 以降、 BR は配置ルールをサポートし、配置ルールのバックアップおよび復元モードを制御するコマンド ライン オプション`--with-tidb-placement-mode=strict/ignore`を導入します。デフォルト値`strict`では、 BR は配置ルールをインポートして検証しますが、値が`ignore`の場合はすべての配置ルールを無視します。

## データ復元の問題 {#data-restore-issues}

### <code>Io(Os...)</code>エラーを処理するにはどうすればよいですか? {#what-should-i-do-to-handle-the-code-io-os-code-error}

これらの問題のほとんどは、TiKV がディスクにデータを書き込むときに発生するシステム コール エラーです (たとえば、 `Io(Os {code: 13, kind: PermissionDenied...})`または`Io(Os {code: 2, kind: NotFound...})` )。

このような問題に対処するには、まずバックアップ ディレクトリのマウント方法とファイル システムを確認し、別のフォルダまたは別のハードディスクにデータをバックアップしてみてください。

たとえば、 `samba`によって構築されたネットワーク ディスクにデータをバックアップするときに、 `Code: 22(invalid argument)`エラーが発生する可能性があります。

### <code>rpc error: code = Unavailable desc =...</code>復元中にエラーが発生しました。 {#what-should-i-do-to-handle-the-code-rpc-error-code-unavailable-desc-code-error-occurred-in-restore}

このエラーは、復元するクラスターの容量が不十分な場合に発生する可能性があります。このクラスターの監視メトリクスまたは TiKV ログを確認することで、原因をさらに確認できます。

この問題に対処するには、クラスター リソースをスケールアウトし、復元中の同時実行性を減らし、 `RATE_LIMIT`オプションを有効にしてみてください。

### リストアが失敗し<code>the entry too large, the max entry size is 6291456, the size of data is 7690800</code> 」というエラー メッセージが表示された場合はどうすればよいですか? {#what-should-i-do-if-the-restore-fails-with-the-error-message-code-the-entry-too-large-the-max-entry-size-is-6291456-the-size-of-data-is-7690800-code}

`--ddl-batch-size` ～ `128` 、またはそれより小さい値を設定すると、バッチで作成されるテーブルの数を減らすことができます。

BRを使用して`1`より大きい[`--ddl-batch-size`](/br/br-batch-create-table.md#use-batch-create-table)の値を持つバックアップ データを復元すると、TiDB はテーブル作成の DDL ジョブを TiKV によって維持される DDL ジョブ キューに書き込みます。現時点では、ジョブ メッセージの最大値はデフォルトで`6 MB`であるため、TiDB によって一度に送信されるすべてのテーブル スキーマの合計サイズは 6 MB を超えてはなりません (この値を変更することは**お勧めできません**。詳細については、 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50)と を参照してください)。 [`raft-entry-max-size`](/tikv-configuration-file.md#raft-entry-max-size) ）。したがって、 `--ddl-batch-size`過度に大きな値に設定すると、TiDB によって一度にバッチで送信されるテーブルのスキーマ サイズが指定値を超え、 BRで`entry too large, the max entry size is 6291456, the size of data is 7690800`エラーが報告されます。

### <code>local</code>storageを使用する場合、バックアップ ファイルはどこに保存されますか? {#where-are-the-backed-up-files-stored-when-i-use-code-local-code-storage}

> **注記：**
>
> BRまたは TiKV ノードにネットワーク ファイル システム (NFS) がマウントされていない場合、または Amazon S3、GCS、または Azure Blob Storage プロトコルをサポートする外部storageを使用している場合、 BRによってバックアップされたデータは各 TiKV ノードで生成されます。バックアップ データは各ノードのローカル ファイル システムに分散しているため、**これはBRを展開する推奨方法ではないことに注意してください**。バックアップデータを採取すると、データの冗長化や運用保守上の問題が発生する可能性があります。一方、バックアップ データを収集する前にデータを直接復元すると、 `SST file not found`エラーが発生します。

ローカルstorageを使用すると、 BRが実行されているノードに`backupmeta`が生成され、各リージョンのLeaderノードにバックアップ ファイルが生成されます。

### データの復元中に<code>could not read local://...:download sst failed</code>エラー メッセージが返された場合はどうすればよいですか? {#what-should-i-do-if-the-error-message-code-could-not-read-local-download-sst-failed-code-is-returned-during-data-restore}

データを復元する場合、各ノードは**すべての**バックアップ ファイル (SST ファイル) にアクセスできる必要があります。デフォルトでは、 `local`storageが使用されている場合、バックアップ ファイルが異なるノードに分散しているため、データを復元できません。したがって、各 TiKV ノードのバックアップ ファイルを他の TiKV ノードにコピーする必要があります。**バックアップ データは、Amazon S3、Google Cloud Storage (GCS)、Azure Blob Storage、または NFS に保存することをお勧めします**。

### root を使用して<code>br</code>を実行しようとしても無駄であった場合でも、 <code>Permission denied</code> 」または<code>No such file or directory</code>エラーを処理するにはどうすればよいですか? {#what-should-i-do-to-handle-the-code-permission-denied-code-or-code-no-such-file-or-directory-code-error-even-if-i-have-tried-to-run-code-br-code-using-root-in-vain}

TiKV がバックアップ ディレクトリにアクセスできるかどうかを確認する必要があります。データをバックアップするには、TiKV に書き込み権限があるかどうかを確認してください。データを復元する場合は、読み取り権限があるかどうかを確認してください。

バックアップ操作中に、storageメディアがローカル ディスクまたはネットワーク ファイル システム (NFS) である場合、 `br`を起動するユーザーと TiKV を起動するユーザーが一致していることを確認してください ( `br`と TiKV が別のマシン上にある場合、ユーザーは&#39; UID は一貫している必要があります)。そうしないと、 `Permission denied`問題が発生する可能性があります。

バックアップ ファイル (SST ファイル) は TiKV によって保存されるため、 `root`ユーザーとして`br`を実行すると、ディスク権限が原因で失敗する可能性があります。

> **注記：**
>
> データの復元中に同じ問題が発生する可能性があります。 SST ファイルを初めて読み取るときに、読み取り権限が検証されます。 DDL の実行時間は、アクセス許可の確認と`br`の実行の間に長い間隔がある可能性があることを示唆しています。長時間待機すると、エラー メッセージ`Permission denied`表示される場合があります。

したがって、データを復元する前に、次の手順に従って権限を確認することをお勧めします。

1.  プロセス クエリの Linux コマンドを実行します。

    ```bash
    ps aux | grep tikv-server
    ```

    出力は次のとおりです。

    ```shell
    tidb_ouo  9235 10.9  3.8 2019248 622776 ?      Ssl  08:28   1:12 bin/tikv-server --addr 0.0.0.0:20162 --advertise-addr 172.16.6.118:20162 --status-addr 0.0.0.0:20188 --advertise-status-addr 172.16.6.118:20188 --pd 172.16.6.118:2379 --data-dir /home/user1/tidb-data/tikv-20162 --config conf/tikv.toml --log-file /home/user1/tidb-deploy/tikv-20162/log/tikv.log
    tidb_ouo  9236  9.8  3.8 2048940 631136 ?      Ssl  08:28   1:05 bin/tikv-server --addr 0.0.0.0:20161 --advertise-addr 172.16.6.118:20161 --status-addr 0.0.0.0:20189 --advertise-status-addr 172.16.6.118:20189 --pd 172.16.6.118:2379 --data-dir /home/user1/tidb-data/tikv-20161 --config conf/tikv.toml --log-file /home/user1/tidb-deploy/tikv-20161/log/tikv.log
    ```

    または、次のコマンドを実行することもできます。

    ```bash
    ps aux | grep tikv-server | awk '{print $1}'
    ```

    出力は次のとおりです。

    ```shell
    tidb_ouo
    tidb_ouo
    ```

2.  `tiup`コマンドを使用して、クラスターの起動情報を照会します。

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

3.  バックアップディレクトリの権限を確認してください。たとえば、 `backup`はバックアップ データstorageの場合です。

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

    ステップ 2 の出力から、 `tikv-server`インスタンスがユーザー`tidb_ouo`によって開始されたことがわかります。しかし、ユーザー`tidb_ouo`は`backup`に対する書き込み権限がありません。したがって、バックアップは失敗します。

### <code>mysql</code>スキーマ内のテーブルが復元されないのはなぜですか? {#why-are-tables-in-the-code-mysql-code-schema-not-restored}

BR v5.1.0 以降、完全バックアップを実行すると、 BR は**`mysql`スキーマ内のテーブル**をバックアップします。 BR v6.2.0 より前のデフォルト設定では、 BR はユーザー データのみを復元し、 **`mysql`スキーマ**内のテーブルは復元しません。

ユーザーが`mysql`スキーマ (システム テーブルではない) で作成したテーブルを復元するには、 [テーブルフィルター](/table-filter.md#syntax)使用してテーブルを明示的に含めます。次の例は、 BR が通常の復元を実行するときに`mysql.usertable`テーブルを復元する方法を示しています。

```shell
br restore full -f '*.*' -f '!mysql.*' -f 'mysql.usertable' -s $external_storage_url --with-sys-table
```

前述のコマンドでは、

-   `-f '*.*'`はデフォルトのルールを上書きするために使用されます
-   `-f '!mysql.*'`特に指定がない限り、 BR に`mysql`テーブルを復元しないよう指示します。
-   `-f 'mysql.usertable'` `mysql.usertable`を復元する必要があることを示します。

`mysql.usertable`のみを復元する必要がある場合は、次のコマンドを実行します。

```shell
br restore full -f 'mysql.usertable' -s $external_storage_url --with-sys-table
```

[テーブルフィルター](/table-filter.md#syntax)を設定した場合でも、 **BR は次のシステム テーブルを復元しないこと**に注意してください。

-   統計テーブル ( `mysql.stat_*` )
-   システム変数テーブル ( `mysql.tidb` 、 `mysql.global_variables` )
-   [その他のシステムテーブル](https://github.com/pingcap/tidb/blob/master/br/pkg/restore/systable_restore.go#L31)

## バックアップと復元についてその他知っておきたいこと {#other-things-you-may-want-to-know-about-backup-and-restore}

### バックアップデータのサイズはどれくらいですか?バックアップのレプリカはありますか? {#what-is-the-size-of-the-backup-data-are-there-replicas-of-the-backup}

データのバックアップ中に、各リージョンのLeaderノード上にバックアップ ファイルが生成されます。バックアップのサイズはデータ サイズと等しく、冗長レプリカはありません。したがって、合計データ サイズは、TiKV データの合計数をレプリカの数で割ったものとほぼなります。

ただし、ローカルstorageからデータを復元する場合は、各 TiKV がすべてのバックアップ ファイルにアクセスできる必要があるため、レプリカの数は TiKV ノードの数と同じになります。

### BRを使用したバックアップまたは復元後、監視ノードに表示されるディスク使用量が一貫していないのはなぜですか? {#why-is-the-disk-usage-shown-on-the-monitoring-node-inconsistent-after-backup-or-restore-using-br}

この不一致は、バックアップで使用されるデータ圧縮率がリストアで使用されるデフォルトの圧縮率と異なることが原因で発生します。チェックサムが成功した場合は、この問題を無視してかまいません。

### BR がバックアップ データを復元した後、テーブルに対して<code>ANALYZE</code>ステートメントを実行して、テーブルとインデックス上の TiDB の統計を更新する必要がありますか? {#after-br-restores-the-backup-data-do-i-need-to-execute-the-code-analyze-code-statement-on-the-table-to-update-the-statistics-of-tidb-on-the-tables-and-indexes}

BR は統計をバックアップしません (v4.0.9 を除く)。したがって、バックアップ データを復元した後、手動で`ANALYZE TABLE`を実行するか、TiDB が自動的に実行する`ANALYZE`を待つ必要があります。

v4.0.9 では、 BR はデフォルトで統計をバックアップするため、メモリを大量に消費します。バックアップ プロセスが確実に正常に完了するように、v4.0.10 以降、統計のバックアップはデフォルトで無効になっています。

テーブルで`ANALYZE`実行しない場合、統計が不正確であるため、TiDB は最適な実行プランを選択できません。クエリのパフォーマンスが重要な問題ではない場合は、 `ANALYZE`無視してかまいません。

### 単一クラスターのデータを復元するために、複数の復元タスクを同時に開始できますか? {#can-i-start-multiple-restore-tasks-at-the-same-time-to-restore-the-data-of-a-single-cluster}

以下の理由により、単一クラスターのデータを復元するために複数の復元タスクを同時に開始すること**は強く推奨されません**。

-   BR がデータを復元すると、PD の一部のグローバル構成が変更されます。したがって、データの復元のために複数の復元タスクを同時に開始すると、これらの構成が誤って上書きされ、クラスターの状態が異常になる可能性があります。
-   BR はデータを復元するために大量のクラスター リソースを消費するため、実際には、復元タスクを並行して実行しても復元速度は限られた範囲でしか向上しません。
-   データの復元のために複数の復元タスクを並行して実行するテストは行われていないため、成功するかどうかは保証されません。

### BR はテーブルの<code>SHARD_ROW_ID_BITS</code>および<code>PRE_SPLIT_REGIONS</code>情報をバックアップしますか?復元されたテーブルには複数のリージョンがありますか? {#does-br-back-up-the-code-shard-row-id-bits-code-and-code-pre-split-regions-code-information-of-a-table-does-the-restored-table-have-multiple-regions}

はい。 BRはテーブルの[`SHARD_ROW_ID_BITS`および`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions)情報をバックアップします。復元されたテーブルのデータも複数のリージョンに分割されます。
