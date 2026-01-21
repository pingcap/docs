---
title: Backup & Restore FAQs
summary: よくある質問 (FAQ) とバックアップおよび復元のソリューションについて説明します。
---

# バックアップと復元に関するよくある質問 {#backup-x26-restore-faqs}

このドキュメントには、TiDB バックアップ &amp; 復元 (BR) に関するよくある質問 (FAQ) と解決策が記載されています。

## 誤ってデータを削除または更新した後、データをすばやく回復するにはどうすればよいですか? {#what-should-i-do-to-quickly-recover-data-after-mistakenly-deleting-or-updating-data}

TiDB v6.4.0では、フラッシュバック機能が導入されました。この機能を使用すると、GC時間内に特定の時点までデータを迅速に復旧できます。そのため、誤操作が発生した場合でも、この機能を使用してデータを復旧できます。詳細は[フラッシュバッククラスタ](/sql-statements/sql-statement-flashback-cluster.md)と[フラッシュバックデータベース](/sql-statements/sql-statement-flashback-database.md)参照してください。

## TiDB v5.4.0 以降のバージョンでは、ワークロードが高いクラスターでバックアップ タスクを実行すると、バックアップ タスクの速度が遅くなるのはなぜですか? {#in-tidb-v5-4-0-and-later-versions-when-backup-tasks-are-performed-on-the-cluster-under-a-heavy-workload-why-does-the-speed-of-backup-tasks-become-slow}

TiDB v5.4.0以降、 BRはバックアップタスクの自動チューニング機能を導入しました。v5.4.0以降のバージョンのクラスターでは、この機能はデフォルトで有効になっています。クラスターのワークロードが高い場合、この機能はバックアップタスクで使用されるリソースを制限し、オンラインクラスターへの影響を軽減します。詳細については、 [バックアップオートチューン](/br/br-auto-tune.md)を参照してください。

TiKVは[動的構成](/tikv-control.md#modify-the-tikv-configuration-dynamically)チューニング機能をサポートしています。この機能は、クラスターを再起動せずに以下の方法で有効化または無効化できます。

-   自動調整を無効にする: TiKV 構成項目[`backup.enable-auto-tune`](/tikv-configuration-file.md#enable-auto-tune-new-in-v540)を`false`に設定します。
-   自動チューニングを有効にする： `backup.enable-auto-tune`を`true`に設定します。v5.3.x から v5.4.0 以降のバージョンにアップグレードしたクラスターでは、自動チューニング機能はデフォルトで無効になっています。手動で有効にする必要があります。

`tikv-ctl`使用して自動調整を有効または無効にするには、 [オートチューンを使用する](/br/br-auto-tune.md#use-auto-tune)を参照してください。

さらに、自動チューニングにより、バックアップ タスクで使用されるデフォルトのスレッド数が削減されます。詳細については、 `backup.num-threads` ](/tikv-configuration-file.md#num-threads-1) を参照してください。そのため、Grafana ダッシュボードでは、バックアップ タスクで使用される速度、CPU 使用率、および I/O リソース使用率が、v5.4.0 より前のバージョンよりも低くなります。v5.4.0 より前では、デフォルト値`backup.num-threads`は`CPU * 0.75`でした。つまり、バックアップ タスクで使用されるスレッド数は、論理 CPU コアの 75% を占めていました。その最大値は`32`でした。v5.4.0 以降、この構成項目のデフォルト値は`CPU * 0.5` 、最大値は`8`です。

オフライン クラスターでバックアップ タスクを実行する場合、バックアップを高速化するために、 `backup.num-threads`の値を`tikv-ctl`使用してより大きな数値に変更できます。

## PITRの問題 {#pitr-issues}

### <a href="/br/br-pitr-guide.md">PITR</a>と<a href="/sql-statements/sql-statement-flashback-cluster.md">クラスターフラッシュバック</a>の違いは何ですか? {#what-is-the-difference-between-a-href-br-br-pitr-guide-md-pitr-a-and-a-href-sql-statements-sql-statement-flashback-cluster-md-cluster-flashback-a}

ユースケースの観点から見ると、PITRは通常、クラスターが完全にサービス停止状態になった場合、またはデータが破損して他のソリューションでは復旧できない場合に、クラスターのデータを特定の時点に復元するために使用されます。PITRを使用するには、データ復旧用の新しいクラスターが必要です。クラスターのフラッシュバック機能は、ユーザーの誤操作やその他の要因によって発生するデータエラーのシナリオ向けに特別に設計されており、データエラーが発生する前の最新のタイムスタンプにクラスターのデータをインプレースで復元できます。

ほとんどの場合、人為的なミスによるデータエラーの場合、PITRよりもフラッシュバックの方が優れたリカバリソリューションとなります。これは、RPO（目標復旧時点）がはるかに短く（ほぼゼロ）、RTO（目標復旧時間）も短いためです。しかし、フラッシュバックを実行できないためにクラスタが完全に利用できなくなった場合、PITRがクラスタをリカバリする唯一のソリューションとなります。そのため、PITRは、RPO（最大5分）とRTOがフラッシュバックよりも長くなりますが、データベースのディザスタリカバリ戦略を策定する際には、常に必須のソリューションとなります。

### 上流データベースがTiDB Lightningを使用して物理インポートモードでデータをインポートすると、ログバックアップ機能が利用できなくなります。なぜですか？ {#when-the-upstream-database-imports-data-using-tidb-lightning-in-the-physical-import-mode-the-log-backup-feature-becomes-unavailable-why}

現在、ログバックアップ機能はTiDB Lightningに完全には対応していません。そのため、 TiDB Lightningの物理モードでインポートされたデータはログデータにバックアップできません。

ログバックアップタスクを作成する上流クラスターでは、 TiDB Lightning物理モードを使用してデータをインポートすることは避けてください。代わりに、 TiDB Lightning論理モードを使用できます。物理モードを使用する必要がある場合は、インポート完了後にスナップショットバックアップを実行し、PITR をスナップショットバックアップ後の時点に復元できるようにしてください。

### クラスターはネットワークパーティション障害から回復しましたが、ログバックアップタスクの進行状況のチェックポイントがまだ再開されません。なぜでしょうか？ {#the-cluster-has-recovered-from-the-network-partition-failure-but-the-checkpoint-of-the-log-backup-task-progress-still-does-not-resume-why}

問題: [＃13126](https://github.com/tikv/tikv/issues/13126)

クラスター内でネットワークパーティション障害が発生すると、バックアップタスクはログのバックアップを続行できなくなります。一定の再試行時間後、タスクは状態`ERROR`に設定されます。この時点で、バックアップタスクは停止しています。

この問題を解決するには、 `br log resume`コマンドを手動で実行して、ログ バックアップ タスクを再開する必要があります。

## <code>br restore point</code>コマンドを使用してダウンストリームクラスターを復元した後、 TiFlashからデータにアクセスできなくなりました。どうすればよいでしょうか？ {#after-restoring-a-downstream-cluster-using-the-code-br-restore-point-code-command-data-cannot-be-accessed-from-tiflash-what-should-i-do}

現在、PITRはリストアフェーズ中にTiFlashへの直接データ書き込みをサポートしていません。代わりに、brコマンドラインツールが`ALTER TABLE table_name SET TIFLASH REPLICA ***` DDLを実行してデータを複製します。そのため、PITRによるデータリストアが完了した直後にTiFlashレプリカは利用できません。TiKVノードからデータが複製されるまで、一定時間待つ必要があります。レプリケーションの進行状況を確認するには、 `INFORMATION_SCHEMA.tiflash_replica`番目の表の`progress`情報を確認してください。

### ログ バックアップ タスクの<code>status</code>が<code>ERROR</code>になった場合はどうすればよいでしょうか? {#what-should-i-do-if-the-code-status-code-of-a-log-backup-task-becomes-code-error-code}

ログバックアップタスクの実行中に、タスクが失敗し、再試行しても回復できない場合、タスクステータスは`ERROR`になります。以下に例を示します。

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

この問題を解決するには、エラーメッセージで原因を確認し、指示に従ってください。問題が解決したら、次のコマンドを実行してタスクを再開してください。

```shell
br log resume --task-name=task1 --pd x.x.x.x:2379
```

バックアップタスクが再開された後、 `br log status`でステータスを確認できます。タスクステータスが`NORMAL`になると、バックアップタスクが続行されます。

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
> この機能は、複数のバージョンのデータをバックアップします。長時間のバックアップタスクが失敗し、ステータスが`ERROR`になると、このタスクのチェックポイントデータは`safe point`に設定され、 `safe point`のデータは24時間以内にガベージコレクションされません。そのため、エラーからの再開後、バックアップタスクは最後のチェックポイントから続行されます。タスクが24時間以上失敗し、最後のチェックポイントデータがガベージコレクションされている場合、タスクを再開するとエラーが報告されます。この場合、まず`br log stop`コマンドを実行してタスクを停止し、新しいバックアップタスクを開始する必要があります。

### <code>br log resume</code>コマンドを使用して中断されたタスクを再開するときに、エラー メッセージ<code>ErrBackupGCSafepointExceeded</code>返された場合、どうすればよいですか? {#what-should-i-do-if-the-error-message-code-errbackupgcsafepointexceeded-code-is-returned-when-using-the-code-br-log-resume-code-command-to-resume-a-suspended-task}

```shell
Error: failed to check gc safePoint, checkpoint ts 433177834291200000: GC safepoint 433193092308795392 exceed TS 433177834291200000: [BR:Backup:ErrBackupGCSafepointExceeded]backup GC safepoint exceeded
```

ログバックアップタスクを一時停止すると、MVCCデータがガベージコレクションされるのを防ぐため、一時停止中のタスクプログラムは現在のチェックポイントをサービスセーフポイントとして自動的に設定します。これにより、24時間以内に生成されたMVCCデータが保持されます。バックアップチェックポイントのMVCCデータが24時間以上経過している場合、そのチェックポイントのデータはガベージコレクションされ、バックアップタスクを再開できなくなります。

この問題を解決するには、 `br log stop`使用して現在のタスクを削除し、 `br log start`を使用してログバックアップタスクを作成します。同時に、後続の PITR のためにフルバックアップを実行できます。

### PITR テーブル フィルターの使用時にエラー メッセージ<code>[ddl:8204]invalid ddl job type: none</code>が返された場合はどうすればよいですか? {#what-should-i-do-if-the-error-message-code-ddl-8204-invalid-ddl-job-type-none-code-is-returned-when-using-the-pitr-table-filter}

```shell
failed to refresh meta for database with schemaID=124, dbName=pitr_test: [ddl:8204]invalid ddl job type: none
```

このエラーは、DDLオーナーとして動作しているTiDBノードが、Refresh Meta DDLを認識できない古いバージョンを実行しているために発生します。この問題を解決するには、PITR [テーブルフィルター](/table-filter.md)機能を使用する前に、クラスターをv8.5.5以降にアップグレードしてください。

## 機能の互換性の問題 {#feature-compatibility-issues}

### br コマンドライン ツールを使用して復元されたデータが TiCDC のアップストリーム クラスターに複製できないのはなぜですか? {#why-does-data-restored-using-br-command-line-tool-cannot-be-replicated-to-the-upstream-cluster-of-ticdc}

-   **BRを使用して復元されたデータは、ダウンストリームに複製できません**。これは、 BR がSST ファイルを直接インポートしますが、ダウンストリーム クラスタがアップストリームからこれらのファイルを取得できないためです。

-   v4.0.3より前のバージョンでは、復元中に生成されたDDLジョブによって、TiCDCで予期しないDDL実行が発生する可能性があります。そのため、TiCDCの上流クラスターで復元を実行する必要がある場合は、brコマンドラインツールを使用して復元したすべてのテーブルをTiCDCのブロックリストに追加してください。

[`filter.rules`](https://github.com/pingcap/tiflow/blob/7c3c2336f98153326912f3cf6ea2fbb7bcc4a20c/cmd/changefeed.toml#L16)使用して、TiCDC のブロック リストを構成できます。

### 復元中に<code>new_collation_enabled</code>不一致が報告されるのはなぜですか? {#why-is-code-new-collation-enabled-code-mismatch-reported-during-restore}

TiDB v6.0.0以降、デフォルト値の[`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)は`false`から`true`に変更されました。BRは上流クラスタの`mysql.tidb`テーブルにある`new_collation_enabled`設定をバックアップし、この設定の値が上流クラスタと下流クラスタ間で一致しているかどうかを確認します。値が一致している場合、 BRは上流クラスタにバックアップされたデータを下流クラスタに安全に復元します。値が一致していない場合、 BRはデータの復元を実行せず、エラーを報告します。

以前のバージョンのTiDBクラスタでデータをバックアップし、そのデータをv6.0.0以降のバージョンのTiDBクラスタにリストアするとします。この場合、上流クラスタと下流クラスタの間で値`new_collations_enabled_on_first_bootstrap`が一致しているかどうかを手動で確認する必要があります。

-   値が一貫している場合は、復元コマンドに`--check-requirements=false`を追加して、この構成チェックをスキップできます。
-   値が矛盾している場合に強制的に復元を実行すると、 BR はデータ検証エラーを報告します。

### 配置ルールをクラスターに復元するとエラーが発生するのはなぜですか? {#why-does-an-error-occur-when-i-restore-placement-rules-to-a-cluster}

v6.0.0より前では、 BRは[配置ルール](/placement-rules-in-sql.md)サポートしていません。v6.0.0以降、 BRは配置ルールをサポートし、配置ルールのバックアップと復元モードを制御するコマンドラインオプション`--with-tidb-placement-mode=strict/ignore`を導入しました。デフォルト値`strict`の場合、 BRは配置ルールをインポートして検証しますが、値が`ignore`の場合はすべての配置ルールを無視します。

## データ復元の問題 {#data-restore-issues}

### <code>Io(Os...)</code>エラーを処理するにはどうすればよいですか? {#what-should-i-do-to-handle-the-code-io-os-code-error}

これらの問題のほとんどは、TiKV がディスクにデータを書き込むときに発生するシステム コール エラーです (例: `Io(Os {code: 13, kind: PermissionDenied...})`または`Io(Os {code: 2, kind: NotFound...})` )。

このような問題に対処するには、まずバックアップディレクトリのマウント方法とファイルシステムを確認し、別のフォルダまたは別のハードディスクにデータをバックアップしてみます。

たとえば、 `samba`で構築されたネットワーク ディスクにデータをバックアップするときに、 `Code: 22(invalid argument)`エラーが発生する可能性があります。

### 復元中に<code>rpc error: code = Unavailable desc =...</code> error occurred in restore?」を処理するにはどうすればよいですか? {#what-should-i-do-to-handle-the-code-rpc-error-code-unavailable-desc-code-error-occurred-in-restore}

このエラーは、復元するクラスターの容量が不足している場合に発生する可能性があります。このクラスターの監視メトリックまたはTiKVログを確認することで、原因をさらに確認できます。

この問題に対処するには、クラスター リソースをスケール アウトし、復元の値`tikv-max-restore-concurrency`を減らして、オプション`ratelimit`を有効にしてみてください。

### <code>the entry too large, the max entry size is 6291456, the size of data is 7690800</code> 」というエラー メッセージが表示されて復元が失敗した場合は、どうすればよいでしょうか。 {#what-should-i-do-if-the-restore-fails-with-the-error-message-code-the-entry-too-large-the-max-entry-size-is-6291456-the-size-of-data-is-7690800-code}

`--ddl-batch-size` ～ `128`またはそれより小さい値を設定することで、バッチで作成されるテーブルの数を減らすことができます。

BRを使用して[`--ddl-batch-size`](/br/br-batch-create-table.md#use-batch-create-table)の値が`1`より大きいバックアップ データを復元する場合、TiDB はテーブル作成の DDL ジョブを TiKV が管理する DDL ジョブ キューに書き込みます。このとき、ジョブ メッセージの最大値がデフォルトで`6 MB`であるため (この値を変更することは**推奨されません**。詳細については、 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500)と[`raft-entry-max-size`](/tikv-configuration-file.md#raft-entry-max-size)を参照してください)、TiDB が一度に送信するすべてのテーブル スキーマの合計サイズは 6 MB を超えてはなりません。したがって、 `--ddl-batch-size`過度に大きな値に設定すると、TiDB が一度にバッチで送信するテーブルのスキーマ サイズが指定値を超え、 BR が`entry too large, the max entry size is 6291456, the size of data is 7690800`エラーを報告します。

### <code>local</code>storageを使用する場合、バックアップされたファイルはどこに保存されますか? {#where-are-the-backed-up-files-stored-when-i-use-code-local-code-storage}

> **注記：**
>
> BRまたは TiKV ノードにネットワークファイルシステム (NFS) がマウントされていない場合、または Amazon S3、GCS、または Azure Blob Storage プロトコルをサポートする外部storageを使用している場合、 BRによってバックアップされたデータは各 TiKV ノードで生成されます。**ただし、バックアップデータが各ノードのローカルファイルシステムに分散されるため、この方法はBRの導入方法として推奨されません**。バックアップデータの収集は、データの冗長性や運用・保守上の問題を引き起こす可能性があります。また、バックアップデータの収集前にデータを直接復元すると、エラー`SST file not found`が発生します。

ローカルstorageを使用する場合、 BRが稼働しているノードに`backupmeta`生成され、各リージョンのLeaderノードにバックアップファイルが生成されます。

### データの復元中に<code>could not read local://...:download sst failed</code>というエラー メッセージが返された場合、どうすればよいですか? {#what-should-i-do-if-the-error-message-code-could-not-read-local-download-sst-failed-code-is-returned-during-data-restore}

データを復元する場合、各ノードは**すべての**バックアップファイル（SSTファイル）にアクセスできる必要があります。デフォルトでは、storageを`local`使用している場合、バックアップファイルが複数のノードに分散しているため、データを復元できません。そのため、各TiKVノードのバックアップファイルを他のTiKVノードにコピーする必要があります。**バックアップデータは、Amazon S3、Google Cloud Storage（GCS）、Azure Blob Storage、またはNFSに保存することをお勧めします**。

### ルートを使用して<code>br</code>を実行しようとしたがうまくいかなかった場合、「 <code>Permission denied</code> 」または<code>No such file or directory</code> 」というエラーを処理するにはどうすればよいでしょうか? {#what-should-i-do-to-handle-the-code-permission-denied-code-or-code-no-such-file-or-directory-code-error-even-if-i-have-tried-to-run-code-br-code-using-root-in-vain}

TiKVがバックアップディレクトリにアクセスできるかどうかを確認する必要があります。データをバックアップするには、TiKVに書き込み権限があるかどうかを確認してください。データを復元するには、TiKVに読み取り権限があるかどうかを確認してください。

バックアップ操作中、storageメディアがローカルディスクまたはネットワークファイルシステム（NFS）の場合、 `br`起動するユーザーとTiKVを起動するユーザーが一致していることを確認してください（ `br`とTiKVが異なるマシン上にある場合は、ユーザーのUIDが一致している必要があります）。一致していない場合、 `Permission denied`問題が発生する可能性があります。

バックアップ ファイル (SST ファイル) は TiKV によって保存されるため、ディスク権限が原因で`br` `root`ユーザーとして実行すると失敗する可能性があります。

> **注記：**
>
> データの復元中にも同じ問題が発生する可能性があります。SSTファイルの初回読み取り時に、読み取り権限が検証されます。DDLの実行時間から判断すると、権限の確認と`br`実行の間に長い間隔が生じる可能性があります。長時間待機した後、エラーメッセージ`Permission denied`表示される場合があります。

したがって、データを復元する前に、次の手順に従って権限を確認することをお勧めします。

1.  プロセス クエリ用の Linux コマンドを実行します。

    ```bash
    ps aux | grep tikv-server
    ```

    出力は次のようになります。

    ```shell
    tidb_ouo  9235 10.9  3.8 2019248 622776 ?      Ssl  08:28   1:12 bin/tikv-server --addr 0.0.0.0:20162 --advertise-addr 172.16.6.118:20162 --status-addr 0.0.0.0:20188 --advertise-status-addr 172.16.6.118:20188 --pd 172.16.6.118:2379 --data-dir /home/user1/tidb-data/tikv-20162 --config conf/tikv.toml --log-file /home/user1/tidb-deploy/tikv-20162/log/tikv.log
    tidb_ouo  9236  9.8  3.8 2048940 631136 ?      Ssl  08:28   1:05 bin/tikv-server --addr 0.0.0.0:20161 --advertise-addr 172.16.6.118:20161 --status-addr 0.0.0.0:20189 --advertise-status-addr 172.16.6.118:20189 --pd 172.16.6.118:2379 --data-dir /home/user1/tidb-data/tikv-20161 --config conf/tikv.toml --log-file /home/user1/tidb-deploy/tikv-20161/log/tikv.log
    ```

    または、次のコマンドを実行することもできます。

    ```bash
    ps aux | grep tikv-server | awk '{print $1}'
    ```

    出力は次のようになります。

    ```shell
    tidb_ouo
    tidb_ouo
    ```

2.  `tiup`コマンドを使用して、クラスターの起動情報を照会します。

    ```bash
    tiup cluster list
    ```

    出力は次のようになります。

    ```shell
    [root@Copy-of-VM-EE-CentOS76-v1 br]# tiup cluster list
    Starting component `cluster`: /root/.tiup/components/cluster/v1.5.2/tiup-cluster list
    Name          User      Version  Path                                               PrivateKey
    ----          ----      -------  ----                                               ----------
    tidb_cluster  tidb_ouo  v5.0.2   /root/.tiup/storage/cluster/clusters/tidb_cluster  /root/.tiup/storage/cluster/clusters/tidb_cluster/ssh/id_rsa
    ```

3.  バックアップディレクトリの権限を確認してください。例えば、 `backup`はバックアップデータのstorage先です。

    ```bash
    ls -al backup
    ```

    出力は次のようになります。

    ```shell
    [root@Copy-of-VM-EE-CentOS76-v1 user1]# ls -al backup
    total 0
    drwxr-xr-x  2 root root   6 Jun 28 17:48 .
    drwxr-xr-x 11 root root 310 Jul  4 10:35 ..
    ```

    手順2の出力から、インスタンス`tikv-server`がユーザー`tidb_ouo`によって起動されたことがわかります。しかし、ユーザー`tidb_ouo`はインスタンス`backup`への書き込み権限がありません。そのため、バックアップは失敗します。

### <code>mysql</code>スキーマ内のテーブルが復元されないのはなぜですか? {#why-are-tables-in-the-code-mysql-code-schema-not-restored}

BR v5.1.0以降では、フルバックアップを実行すると、 BRは**`mysql`スキーマ内のテーブル**をバックアップします。BR BRより前のデフォルト設定では、 BRはユーザーデータのみを復元し、 **`mysql`スキーマ**内のテーブルは復元しません。

ユーザーが`mysql`スキーマに作成したテーブル（システムテーブルではない）を復元するには、 [テーブルフィルター](/table-filter.md#syntax)を使用して明示的にテーブルを含めます。次の例は、 BR が通常の復元を実行する際に`mysql.usertable`テーブルを復元する方法を示しています。

```shell
br restore full -f '*.*' -f '!mysql.*' -f 'mysql.usertable' -s $external_storage_url --with-sys-table
```

上記のコマンドでは、

-   `-f '*.*'`はデフォルトのルールを上書きするために使用されます
-   `-f '!mysql.*'`特に指定がない限り、 `mysql`テーブルを復元しないようにBRに指示します。
-   `-f 'mysql.usertable'` `mysql.usertable`復元する必要があることを示します。

`mysql.usertable`を復元する必要がある場合は、次のコマンドを実行します。

```shell
br restore full -f 'mysql.usertable' -s $external_storage_url --with-sys-table
```

[テーブルフィルター](/table-filter.md#syntax)設定しても、 **BR は次のシステム テーブルを復元しないこと**に注意してください。

-   統計表（ `mysql.stat_*` ）。ただし、統計は復元可能です。3 [統計のバックアップ](/br/br-snapshot-manual.md#back-up-statistics)参照してください。
-   システム変数テーブル（ `mysql.tidb` `mysql.global_variables`
-   [その他のシステムテーブル](https://github.com/pingcap/tidb/blob/release-8.5/br/pkg/restore/snap_client/systable_restore.go#L31)

### 復元中に<code>cannot find rewrite rule</code>というエラーに対処するにはどうすればよいですか? {#how-to-deal-with-the-error-of-code-cannot-find-rewrite-rule-code-during-restoration}

復元クラスタ内に、バックアップデータ内の他のテーブルと同じ名前を持ちながら構造が不整合なテーブルがないか確認してください。多くの場合、この問題は復元クラスタ内のテーブルでインデックスが欠落していることが原因です。推奨される方法は、まず復元クラスタ内のそのようなテーブルを削除してから、復元を再試行することです。

## バックアップと復元について知っておきたいこと {#other-things-you-may-want-to-know-about-backup-and-restore}

### バックアップデータのサイズはどれくらいですか？バックアップのレプリカはありますか？ {#what-is-the-size-of-the-backup-data-are-there-replicas-of-the-backup}

データバックアップ中、各リージョンのLeaderノードにバックアップファイルが生成されます。バックアップのサイズはデータサイズと等しく、冗長レプリカは作成されません。したがって、合計データサイズは、TiKVデータの総数をレプリカ数で割った値とほぼ等しくなります。

ただし、ローカルstorageからデータを復元する場合、各 TiKV がすべてのバックアップ ファイルにアクセスできる必要があるため、レプリカの数は TiKV ノードの数と同じになります。

### BRを使用してバックアップまたは復元した後、監視ノードに表示されるディスク使用量が一致しないのはなぜですか? {#why-is-the-disk-usage-shown-on-the-monitoring-node-inconsistent-after-backup-or-restore-using-br}

この不整合は、バックアップで使用されるデータ圧縮率が、復元で使用されるデフォルトの圧縮率と異なるために発生します。チェックサムが成功した場合は、この問題は無視できます。

### BR がバックアップ データを復元した後、テーブルとインデックスの TiDB の統計を更新するために、テーブルに対して<code>ANALYZE</code>ステートメントを実行する必要がありますか? {#after-br-restores-the-backup-data-do-i-need-to-execute-the-code-analyze-code-statement-on-the-table-to-update-the-statistics-of-tidb-on-the-tables-and-indexes}

BRは統計情報をバックアップしません（v4.0.9を除く）。そのため、バックアップデータを復元した後は、 `ANALYZE TABLE`手動で実行するか、TiDBが`ANALYZE`自動的に実行するのを待つ必要があります。

v4.0.9では、 BRはデフォルトで統計情報をバックアップしますが、メモリ消費量が多すぎます。バックアッププロセスが確実に実行されるよう、v4.0.10以降では統計情報のバックアップはデフォルトで無効化されています。

テーブルに対して`ANALYZE`実行しないと、TiDBは統計情報が不正確であるため最適な実行プランを選択できません。クエリパフォーマンスが重要でない場合は、 `ANALYZE`無視できます。

### 複数の復元タスクを同時に開始して、単一のクラスターのデータを復元できますか? {#can-i-start-multiple-restore-tasks-at-the-same-time-to-restore-the-data-of-a-single-cluster}

次の理由により、単一のクラスターのデータを復元するために複数の復元タスクを同時に開始することは**強く推奨されません**。

-   BR がデータを復元すると、PD のグローバル設定の一部が変更されます。そのため、複数の復元タスクを同時に実行すると、これらの設定が誤って上書きされ、クラスタの状態が異常になる可能性があります。
-   BR はデータの復元に大量のクラスター リソースを消費するため、実際には復元タスクを並列で実行しても復元速度は限られた範囲でしか向上しません。
-   データの復元のために複数の復元タスクを並行して実行するテストは行われていないため、成功することは保証されません。

### BR はテーブルの<code>SHARD_ROW_ID_BITS</code>と<code>PRE_SPLIT_REGIONS</code>情報をバックアップしますか? 復元されたテーブルには複数のリージョンがありますか? {#does-br-back-up-the-code-shard-row-id-bits-code-and-code-pre-split-regions-code-information-of-a-table-does-the-restored-table-have-multiple-regions}

はい。BRはテーブルの[`SHARD_ROW_ID_BITS`と`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions)情報をバックアップします。復元されたテーブルのデータも複数のリージョンに分割されます。

## 回復プロセスが中断された場合、すでに回復されたデータを削除して、回復を再度開始する必要がありますか? {#if-the-recovery-process-is-interrupted-is-it-necessary-to-delete-the-already-recovered-data-and-start-the-recovery-again}

いいえ、必要ありません。BR BR以降では、ブレークポイントからのデータの再開をサポートしています。予期せぬ状況でリカバリが中断された場合は、リカバリタスクを再開するだけで、中断したところから再開されます。

## リカバリが完了したら、特定のテーブルを削除して再度リカバリできますか? {#after-the-recovery-is-complete-can-i-delete-a-specific-table-and-then-recover-it-again}

はい、特定のテーブルを削除した後でも、そのテーブルを再度リカバリできます。ただし、リカバリできるのは`DROP TABLE`または`TRUNCATE TABLE`ステートメントで削除されたテーブルのみであり、 `DELETE FROM`ステートメントではリカバリできないことに注意してください。これは、 `DELETE FROM`ではMVCCバージョンを更新して削除対象データをマークするだけで、実際のデータ削除はGC後に行われるためです。

### 統計情報を復元するときにBR が大量のメモリを消費するのはなぜですか? {#why-does-br-take-a-lot-of-memory-when-restoring-statistics-information}

v7.6.0より前のバージョンでは、 BRによってバックアップされた統計データはテーブル情報と共に保存され、リカバリ時にメモリにロードされます。そのため、バックアップ統計データが非常に大きい場合、 BRは大量のメモリを占有する必要があります。

バージョン7.6.0以降、バックアップ統計は特定のファイルに個別に保存されます。BRはテーブルの復元を開始するまで、どのテーブルの統計データもロードしないBR、メモリを節約できます。
