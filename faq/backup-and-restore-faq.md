---
title: Backup & Restore FAQs
summary: よくある質問 (FAQ) とバックアップおよび復元のソリューションについて学習します。
---

# バックアップと復元に関するよくある質問 {#backup-x26-restore-faqs}

このドキュメントでは、TiDB バックアップと復元 (BR) に関するよくある質問 (FAQ) と解決策を示します。

## 誤ってデータを削除または更新した後、データを素早く回復するにはどうすればよいですか? {#what-should-i-do-to-quickly-recover-data-after-mistakenly-deleting-or-updating-data}

TiDB v6.4.0 ではフラッシュバック機能が導入されました。この機能を使用すると、GC 時間内のデータを指定した時点に迅速に回復できます。そのため、誤操作が発生した場合は、この機能を使用してデータを回復できます。詳細については、 [フラッシュバッククラスタ](/sql-statements/sql-statement-flashback-cluster.md)および[フラッシュバックデータベース](/sql-statements/sql-statement-flashback-database.md)参照してください。

## TiDB v5.4.0 以降のバージョンでは、ワークロードが高いクラスターでバックアップ タスクを実行すると、バックアップ タスクの速度が遅くなるのはなぜですか? {#in-tidb-v5-4-0-and-later-versions-when-backup-tasks-are-performed-on-the-cluster-under-a-heavy-workload-why-does-the-speed-of-backup-tasks-become-slow}

TiDB v5.4.0 以降、 BRバックアップ タスクの自動調整機能が導入されています。v5.4.0 以降のバージョンのクラスターでは、この機能はデフォルトで有効になっています。クラスターのワークロードが重い場合、この機能によりバックアップ タスクで使用されるリソースが制限され、オンライン クラスターへの影響が軽減されます。詳細については、 [バックアップオートチューン](/br/br-auto-tune.md)を参照してください。

TiKV は自動調整[動的構成](/tikv-control.md#modify-the-tikv-configuration-dynamically)をサポートしています。クラスターを再起動せずに、次の方法でこの機能を有効または無効にすることができます。

-   自動調整を無効にする: TiKV 構成項目[`backup.enable-auto-tune`](/tikv-configuration-file.md#enable-auto-tune-new-in-v540)を`false`に設定します。
-   自動調整を有効にする: `backup.enable-auto-tune`から`true`に設定します。v5.3.x から v5.4.0 以降のバージョンにアップグレードされたクラスターの場合、自動調整機能はデフォルトで無効になっています。手動で有効にする必要があります。

`tikv-ctl`使用して自動調整を有効または無効にするには、 [オートチューンを使用する](/br/br-auto-tune.md#use-auto-tune)を参照してください。

また、自動チューニングにより、バックアップ タスクで使用されるデフォルトのスレッド数が削減されます。詳細については、 `backup.num-threads` ](/tikv-configuration-file.md#num-threads-1) を参照してください。そのため、Grafana ダッシュボードでは、バックアップ タスクで使用される速度、CPU 使用率、および I/O リソース使用率は、v5.4.0 より前のバージョンよりも低くなります。v5.4.0 より前では、デフォルト値`backup.num-threads`は`CPU * 0.75`でした。つまり、バックアップ タスクで使用されるスレッド数は、論理 CPU コアの 75% を占めていました。最大値は`32`でした。v5.4.0 以降、この構成項目のデフォルト値は`CPU * 0.5`で、最大値は`8`です。

オフライン クラスターでバックアップ タスクを実行する場合、バックアップを高速化するために、 `backup.num-threads`の値を`tikv-ctl`使用してより大きな数値に変更できます。

## PITRの問題 {#pitr-issues}

### <a href="/br/br-pitr-guide.md">PITR</a>と<a href="/sql-statements/sql-statement-flashback-cluster.md">クラスターフラッシュバック</a>の違いは何ですか? {#what-is-the-difference-between-a-href-br-br-pitr-guide-md-pitr-a-and-a-href-sql-statements-sql-statement-flashback-cluster-md-cluster-flashback-a}

ユースケースの観点から見ると、PITR は通常、クラスターが完全に使用不能になった場合、またはデータが破損していて他のソリューションを使用しても回復できない場合に、クラスターのデータを指定された時点に復元するために使用されます。PITR を使用するには、データ回復用の新しいクラスターが必要です。クラスター フラッシュバック機能は、ユーザーの誤操作やその他の要因によって発生するデータ エラー シナリオ向けに特別に設計されており、データ エラーが発生する前の最新のタイムスタンプにクラスターのデータをインプレースで復元できます。

ほとんどの場合、人為的なミスによって生じたデータ エラーの場合、フラッシュバックは PITR よりも優れたリカバリ ソリューションです。これは、RPO (ゼロに近い) と RTO がはるかに短いためです。ただし、フラッシュバックを実行できないためにクラスターが完全に使用できない場合は、PITR がクラスターをリカバリする唯一のソリューションです。したがって、PITR は、フラッシュバックよりも RPO (最大 5 分) と RTO が長いにもかかわらず、データベースの災害復旧戦略を開発するときには常に必須のソリューションです。

### 上流データベースが物理インポート モードでTiDB Lightning を使用してデータをインポートすると、ログ バックアップ機能が使用できなくなります。なぜでしょうか? {#when-the-upstream-database-imports-data-using-tidb-lightning-in-the-physical-import-mode-the-log-backup-feature-becomes-unavailable-why}

現在、ログバックアップ機能はTiDB Lightningに完全には適応されていません。そのため、 TiDB Lightningの物理モードでインポートされたデータはログデータにバックアップできません。

ログ バックアップ タスクを作成するアップストリーム クラスターでは、 TiDB Lightning物理モードを使用してデータをインポートしないでください。代わりに、 TiDB Lightning論理モードを使用できます。物理モードを使用する必要がある場合は、インポートが完了した後にスナップショット バックアップを実行し、PITR をスナップショット バックアップ後の時点に復元できるようにします。

### クラスターはネットワーク パーティション障害から回復しましたが、ログ バックアップ タスクの進行状況のチェックポイントはまだ再開されません。なぜでしょうか。 {#the-cluster-has-recovered-from-the-network-partition-failure-but-the-checkpoint-of-the-log-backup-task-progress-still-does-not-resume-why}

問題: [＃13126](https://github.com/tikv/tikv/issues/13126)

クラスターでネットワーク パーティション障害が発生すると、バックアップ タスクはログのバックアップを続行できなくなります。一定の再試行時間が経過すると、タスクは`ERROR`状態に設定されます。この時点で、バックアップ タスクは停止しています。

この問題を解決するには、 `br log resume`コマンドを手動で実行して、ログ バックアップ タスクを再開する必要があります。

## <code>br restore point</code>コマンドを使用してダウンストリーム クラスターを復元した後、 TiFlashからデータにアクセスできません。どうすればよいでしょうか。 {#after-restoring-a-downstream-cluster-using-the-code-br-restore-point-code-command-data-cannot-be-accessed-from-tiflash-what-should-i-do}

現在、PITR は復元フェーズ中にTiFlashにデータを直接書き込むことをサポートしていません。代わりに、br コマンドライン ツールが`ALTER TABLE table_name SET TIFLASH REPLICA ***` DDL を実行してデータを複製します。そのため、PITR がデータの復元を完了した直後にTiFlashレプリカは利用できません。代わりに、TiKV ノードからデータが複製されるまで、一定時間待つ必要があります。レプリケーションの進行状況を確認するには、 `INFORMATION_SCHEMA.tiflash_replica`表の`progress`情報を確認します。

### ログ バックアップ タスクの<code>status</code>が<code>ERROR</code>になった場合はどうすればよいでしょうか? {#what-should-i-do-if-the-code-status-code-of-a-log-backup-task-becomes-code-error-code}

ログ バックアップ タスクの実行中に、タスクが失敗し、再試行しても回復できない場合、タスク ステータスは`ERROR`になります。次に例を示します。

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

この問題を解決するには、エラー メッセージで原因を確認し、指示に従って実行します。問題が解決したら、次のコマンドを実行してタスクを再開します。

```shell
br log resume --task-name=task1 --pd x.x.x.x:2379
```

バックアップタスクが再開された後、 `br log status`使用してステータスを確認できます。タスクステータスが`NORMAL`になると、バックアップタスクが続行されます。

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
> この機能は、複数のバージョンのデータをバックアップします。長時間のバックアップ タスクが失敗してステータスが`ERROR`になると、このタスクのチェックポイント データは`safe point`に設定され、 `safe point`のデータは 24 時間以内にガベージ コレクションされません。そのため、エラーの再開後、バックアップ タスクは最後のチェックポイントから続行されます。タスクが 24 時間以上失敗し、最後のチェックポイント データがガベージ コレクションされている場合は、タスクを再開するとエラーが報告されます。この場合、最初に`br log stop`コマンドを実行してタスクを停止してから、新しいバックアップ タスクを開始するしかありません。

### <code>br log resume</code>コマンドを使用して中断されたタスクを再開するときに、エラー メッセージ<code>ErrBackupGCSafepointExceeded</code>が返された場合はどうすればよいですか? {#what-should-i-do-if-the-error-message-code-errbackupgcsafepointexceeded-code-is-returned-when-using-the-code-br-log-resume-code-command-to-resume-a-suspended-task}

```shell
Error: failed to check gc safePoint, checkpoint ts 433177834291200000: GC safepoint 433193092308795392 exceed TS 433177834291200000: [BR:Backup:ErrBackupGCSafepointExceeded]backup GC safepoint exceeded
```

ログ バックアップ タスクを一時停止すると、MVCC データがガベージ コレクションされるのを防ぐために、一時停止タスク プログラムは現在のチェックポイントをサービス セーフポイントとして自動的に設定します。これにより、24 時間以内に生成された MVCC データが保持されます。バックアップ チェックポイントの MVCC データの生成が 24 時間を超えると、チェックポイントのデータがガベージ コレクションされ、バックアップ タスクを再開できなくなります。

この問題を解決するには、 `br log stop`使用して現在のタスクを削除し、 `br log start`使用してログ バックアップ タスクを作成します。同時に、後続の PITR の完全バックアップを実行できます。

## 機能の互換性の問題 {#feature-compatibility-issues}

### br コマンドライン ツールを使用して復元されたデータが、 TiCDC またはDrainerのアップストリーム クラスターに複製できないのはなぜですか? {#why-does-data-restored-using-br-command-line-tool-cannot-be-replicated-to-the-upstream-cluster-of-ticdc-or-drainer}

-   **BR を使用して復元されたデータは、ダウンストリームに複製できません**。これは、 BRが SST ファイルを直接インポートしますが、ダウンストリーム クラスターは現在、アップストリームからこれらのファイルを取得できないためです。

-   v4.0.3 より前では、復元中に生成された DDL ジョブによって、 TiCDC/ Drainerで予期しない DDL 実行が発生する可能性があります。したがって、 TiCDC/ Drainerのアップストリーム クラスターで復元を実行する必要がある場合は、 br コマンドライン ツールを使用して復元されたすべてのテーブルを TiCDC/ Drainerブロック リストに追加します。

[`filter.rules`](https://github.com/pingcap/tiflow/blob/7c3c2336f98153326912f3cf6ea2fbb7bcc4a20c/cmd/changefeed.toml#L16)使用して TiCDC のブロック リストを構成し、 [`syncer.ignore-table`](/tidb-binlog/tidb-binlog-configuration-file.md#ignore-table)使用してDrainerのブロック リストを構成できます。

### 復元中に<code>new_collation_enabled</code>不一致が報告されるのはなぜですか? {#why-is-code-new-collation-enabled-code-mismatch-reported-during-restore}

TiDB v6.0.0 以降、デフォルト値[`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)は`false`から`true`に変更されました。BRは、上流クラスターの`mysql.tidb`テーブルの`new_collation_enabled`構成をバックアップし、この構成の値が上流クラスターと下流クラスター間で一貫しているかどうかを確認します。値が一致している場合、 BR は上流クラスターでバックアップされたデータを下流クラスターに安全に復元します。値が一致していない場合、 BR はデータの復元を実行せず、エラーを報告します。

以前のバージョンの v6.0.0 の TiDB クラスターでデータをバックアップし、このデータを v6.0.0 以降のバージョンの TiDB クラスターに復元するとします。この状況では、上流クラスターと下流クラスターの間で`new_collations_enabled_on_first_bootstrap`の値が一貫しているかどうかを手動で確認する必要があります。

-   値が一貫している場合は、復元コマンドに`--check-requirements=false`を追加して、この構成チェックをスキップできます。
-   値が矛盾しているときに強制的に復元を実行すると、 BR はデータ検証エラーを報告します。

### 配置ルールをクラスターに復元するとエラーが発生するのはなぜですか? {#why-does-an-error-occur-when-i-restore-placement-rules-to-a-cluster}

v6.0.0 より前では、 BR は[配置ルール](/placement-rules-in-sql.md)サポートしていません。v6.0.0 以降では、 BR は配置ルールをサポートし、配置ルールのバックアップおよび復元モードを制御するためのコマンドライン オプション`--with-tidb-placement-mode=strict/ignore`を導入しています。デフォルト値`strict`では、 BR は配置ルールをインポートして検証しますが、値が`ignore`の場合はすべての配置ルールを無視します。

## データ復元の問題 {#data-restore-issues}

### <code>Io(Os...)</code>エラーを処理するにはどうすればよいですか? {#what-should-i-do-to-handle-the-code-io-os-code-error}

これらの問題のほとんどは、TiKV がディスクにデータを書き込むときに発生するシステム コール エラーです (例: `Io(Os {code: 13, kind: PermissionDenied...})`または`Io(Os {code: 2, kind: NotFound...})` 。

このような問題に対処するには、まずバックアップディレクトリのマウント方法とファイルシステムを確認し、別のフォルダまたは別のハードディスクにデータをバックアップしてみてください。

たとえば、 `samba`で構築されたネットワーク ディスクにデータをバックアップするときに、 `Code: 22(invalid argument)`エラーが発生する可能性があります。

### 復元中に発生した<code>rpc error: code = Unavailable desc =...</code>処理するにはどうすればよいですか? {#what-should-i-do-to-handle-the-code-rpc-error-code-unavailable-desc-code-error-occurred-in-restore}

このエラーは、復元するクラスターの容量が不足している場合に発生する可能性があります。このクラスターの監視メトリックまたは TiKV ログを確認することで、原因をさらに確認できます。

この問題に対処するには、クラスター リソースをスケール アウトし、復元中の同時実行性を減らして、 `RATE_LIMIT`オプションを有効にしてみてください。

### <code>the entry too large, the max entry size is 6291456, the size of data is 7690800</code>エラー メッセージが表示されて復元が失敗した場合は、どうすればよいですか? {#what-should-i-do-if-the-restore-fails-with-the-error-message-code-the-entry-too-large-the-max-entry-size-is-6291456-the-size-of-data-is-7690800-code}

`--ddl-batch-size` ～ `128`またはそれより小さい値を設定することで、バッチで作成されるテーブルの数を減らすことができます。

[`--ddl-batch-size`](/br/br-batch-create-table.md#use-batch-create-table) `1`より大きい値でBR を使用してバックアップ データを復元する場合、TiDB はテーブル作成の DDL ジョブを TiKV によって管理されている DDL ジョブ キューに書き込みます。このとき、ジョブ メッセージの最大値がデフォルトで`6 MB`であるため (この値を変更することは**推奨されません**。詳細については、 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500)および[`raft-entry-max-size`](/tikv-configuration-file.md#raft-entry-max-size)を参照してください)、TiDB が一度に送信するすべてのテーブル スキーマの合計サイズは 6 MB を超えてはなりません。したがって、 `--ddl-batch-size`過度に大きな値に設定すると、TiDB が一度にバッチで送信するテーブルのスキーマ サイズが指定値を超え、 BR が`entry too large, the max entry size is 6291456, the size of data is 7690800`エラーを報告します。

### <code>local</code>storageを使用する場合、バックアップされたファイルはどこに保存されますか? {#where-are-the-backed-up-files-stored-when-i-use-code-local-code-storage}

> **注記：**
>
> BRまたは TiKV ノードにネットワーク ファイル システム (NFS) がマウントされていない場合、または Amazon S3、GCS、または Azure Blob Storage プロトコルをサポートする外部storageを使用する場合、 BRによってバックアップされたデータは各 TiKV ノードで生成されます。バックアップ データは各ノードのローカル ファイル システムに分散されるため、**これはBRを展開する推奨方法ではないことに注意してください**。バックアップ データを収集すると、データの冗長性や運用および保守の問題が発生する可能性があります。一方、バックアップ データを収集する前にデータを直接復元すると、 `SST file not found`エラーが発生します。

ローカルstorageを使用する場合、 BR が稼働しているノードに`backupmeta`が生成され、各リージョンのLeaderノードにバックアップファイルが生成されます。

### データの復元中に<code>could not read local://...:download sst failed</code>エラー メッセージが返された場合、どうすればよいですか? {#what-should-i-do-if-the-error-message-code-could-not-read-local-download-sst-failed-code-is-returned-during-data-restore}

データを復元する場合、各ノードは**すべての**バックアップ ファイル (SST ファイル) にアクセスできる必要があります。デフォルトでは、 `local`storageが使用されている場合、バックアップ ファイルが異なるノードに分散しているため、データを復元できません。そのため、各 TiKV ノードのバックアップ ファイルを他の TiKV ノードにコピーする必要があります。**バックアップ データは、Amazon S3、Google Cloud Storage (GCS)、Azure Blob Storage、または NFS に保存することをお勧めします**。

### ルートを使用して<code>br</code>実行しようとしたが、失敗した場合でも、「 <code>Permission denied</code> 」または<code>No such file or directory</code> 」というエラーを処理するにはどうすればよいでしょうか? {#what-should-i-do-to-handle-the-code-permission-denied-code-or-code-no-such-file-or-directory-code-error-even-if-i-have-tried-to-run-code-br-code-using-root-in-vain}

TiKV がバックアップ ディレクトリにアクセスできるかどうかを確認する必要があります。データをバックアップするには、TiKV に書き込み権限があるかどうかを確認します。データを復元するには、読み取り権限があるかどうかを確認します。

バックアップ操作中、storageメディアがローカル ディスクまたはネットワーク ファイル システム (NFS) である場合は、 `br`起動するユーザーと TiKV を起動するユーザーが一致していることを確認してください ( `br`と TiKV が異なるマシン上にある場合は、ユーザーの UID が一致している必要があります)。一致していないと、 `Permission denied`問題が発生する可能性があります。

バックアップ ファイル (SST ファイル) は TiKV によって保存されるため、ディスク権限が原因で`br` `root`ユーザーとして実行すると失敗する可能性があります。

> **注記：**
>
> データの復元中に同じ問題が発生する可能性があります。SST ファイルが初めて読み取られるときに、読み取り権限が検証されます。DDL の実行時間から、権限の確認と`br`実行の間に長い間隔がある可能性があります。長時間待機した後、エラー メッセージ`Permission denied`が表示される場合があります。

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

3.  バックアップ ディレクトリの権限を確認します。たとえば、 `backup`バックアップ データのstorage用です。

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

    ステップ 2 の出力から、インスタンス`tikv-server`がユーザー`tidb_ouo`によって開始されたことがわかります。ただし、ユーザー`tidb_ouo`には`backup`に対する書き込み権限がありません。そのため、バックアップは失敗します。

### <code>mysql</code>スキーマ内のテーブルが復元されないのはなぜですか? {#why-are-tables-in-the-code-mysql-code-schema-not-restored}

BR v5.1.0 以降では、完全バックアップを実行すると、 BRは**`mysql`スキーマ内のテーブル**をバックアップします。BR v6.2.0 より前のデフォルト構成では、 BRはユーザー データのみを復元し、 **`mysql`スキーマ**内のテーブルは復元しません。

`mysql`スキーマ (システム テーブルではない) でユーザーが作成したテーブルを復元するには、 [テーブルフィルター](/table-filter.md#syntax)使用してテーブルを明示的に含めることができます。次の例は、 BR が通常の復元を実行するときに`mysql.usertable`テーブルを復元する方法を示しています。

```shell
br restore full -f '*.*' -f '!mysql.*' -f 'mysql.usertable' -s $external_storage_url --with-sys-table
```

前述のコマンドでは、

-   `-f '*.*'`デフォルトのルールを上書きするために使用されます
-   `-f '!mysql.*'`特に指定がない限り、 BRに`mysql`のテーブルを復元しないように指示します。
-   `-f 'mysql.usertable'` `mysql.usertable`復元する必要があることを示します。

`mysql.usertable`のみを復元する必要がある場合は、次のコマンドを実行します。

```shell
br restore full -f 'mysql.usertable' -s $external_storage_url --with-sys-table
```

[テーブルフィルター](/table-filter.md#syntax)設定した場合でも、 **BR は次のシステム テーブルを復元しないこと**に注意してください。

-   統計表（ `mysql.stat_*` ）。ただし、統計は復元可能です[統計のバックアップ](/br/br-snapshot-manual.md#back-up-statistics)参照してください。
-   `mysql.global_variables` `mysql.tidb`
-   [その他のシステムテーブル](https://github.com/pingcap/tidb/blob/release-8.1/br/pkg/restore/systable_restore.go#L31)

### 復元中に<code>cannot find rewrite rule</code>というエラーに対処するにはどうすればよいですか? {#how-to-deal-with-the-error-of-code-cannot-find-rewrite-rule-code-during-restoration}

復元クラスター内に、バックアップ データ内の他のテーブルと同じ名前を持ちながら、構造が一貫していないテーブルがあるかどうかを確認します。ほとんどの場合、この問題は復元クラスターのテーブルにインデックスがないために発生します。推奨される方法は、まず復元クラスター内のそのようなテーブルを削除してから、復元を再試行することです。

## バックアップと復元について知っておきたいその他のこと {#other-things-you-may-want-to-know-about-backup-and-restore}

### バックアップ データのサイズはどれくらいですか? バックアップのレプリカはありますか? {#what-is-the-size-of-the-backup-data-are-there-replicas-of-the-backup}

データのバックアップ中、各リージョンのLeaderノードにバックアップファイルが生成されます。バックアップのサイズはデータサイズと同じで、冗長レプリカはありません。したがって、合計データサイズは、TiKV データの合計数をレプリカ数で割った値とほぼ同じになります。

ただし、ローカルstorageからデータを復元する場合、各 TiKV はすべてのバックアップ ファイルにアクセスできる必要があるため、レプリカの数は TiKV ノードの数と同じになります。

### BR を使用してバックアップまたは復元した後、監視ノードに表示されるディスク使用量が一致しないのはなぜですか? {#why-is-the-disk-usage-shown-on-the-monitoring-node-inconsistent-after-backup-or-restore-using-br}

この不一致は、バックアップで使用されるデータ圧縮率が復元で使用されるデフォルトの率と異なるために発生します。チェックサムが成功した場合は、この問題を無視できます。

### BR がバックアップ データを復元した後、テーブルとインデックスの TiDB の統計を更新するために、テーブルに対して<code>ANALYZE</code>ステートメントを実行する必要がありますか? {#after-br-restores-the-backup-data-do-i-need-to-execute-the-code-analyze-code-statement-on-the-table-to-update-the-statistics-of-tidb-on-the-tables-and-indexes}

BR は統計情報をバックアップしません（v4.0.9 を除く）。そのため、バックアップデータを復元した後、 `ANALYZE TABLE`手動で実行するか、TiDB が`ANALYZE`自動的に実行するのを待つ必要があります。

v4.0.9 では、 BR はデフォルトで統計をバックアップしますが、メモリを大量に消費します。バックアップ プロセスが適切に行われるように、v4.0.10 以降では、統計のバックアップはデフォルトで無効になっています。

テーブルに対して`ANALYZE`実行しないと、統計が不正確になるため、TiDB は最適な実行プランを選択できません。クエリのパフォーマンスが重要でない場合は、 `ANALYZE`無視できます。

### 複数の復元タスクを同時に開始して、単一のクラスターのデータを復元できますか? {#can-i-start-multiple-restore-tasks-at-the-same-time-to-restore-the-data-of-a-single-cluster}

次の理由により、単一のクラスターのデータを復元するために複数の復元タスクを同時に開始することは**強く推奨されません**。

-   BR がデータを復元すると、PD の一部のグローバル構成が変更されます。そのため、データ復元のために複数の復元タスクを同時に開始すると、これらの構成が誤って上書きされ、クラスターの状態が異常になる可能性があります。
-   BR はデータを復元するために大量のクラスター リソースを消費するため、実際には復元タスクを並列で実行しても復元速度は限られた範囲でしか向上しません。
-   データの復元のために複数の復元タスクを並行して実行するテストは行われていないため、成功することは保証されません。

### BR はテーブルの<code>SHARD_ROW_ID_BITS</code>および<code>PRE_SPLIT_REGIONS</code>情報をバックアップしますか? 復元されたテーブルには複数のリージョンがありますか? {#does-br-back-up-the-code-shard-row-id-bits-code-and-code-pre-split-regions-code-information-of-a-table-does-the-restored-table-have-multiple-regions}

はい。BRはテーブルの[`SHARD_ROW_ID_BITS`と`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions)情報をバックアップします。復元されたテーブルのデータも複数のリージョンに分割されます。

## 回復プロセスが中断された場合、すでに回復されたデータを削除して、回復を再度開始する必要がありますか? {#if-the-recovery-process-is-interrupted-is-it-necessary-to-delete-the-already-recovered-data-and-start-the-recovery-again}

いいえ、必要ありません。バージョン 7.1.0 以降、 BR はブレークポイントからのデータの再開をサポートしています。予期しない状況によりリカバリが中断された場合は、リカバリ タスクを再開するだけで、中断したところから再開されます。

## リカバリが完了したら、特定のテーブルを削除して再度リカバリできますか? {#after-the-recovery-is-complete-can-i-delete-a-specific-table-and-then-recover-it-again}

はい、特定のテーブルを削除した後、再度回復することができます。ただし、回復できるのは`DROP TABLE`または`TRUNCATE TABLE`ステートメントを使用して削除されたテーブルのみであり、 `DELETE FROM`ステートメントを使用して削除されたテーブルは回復できないことに注意してください。これは、 `DELETE FROM` MVCC バージョンを更新して削除対象のデータをマークするだけで、実際のデータ削除は GC 後に行われるためです。

### 統計情報を復元するときにBR が大量のメモリを消費するのはなぜですか? {#why-does-br-take-a-lot-of-memory-when-restoring-statistics-information}

v7.6.0 より前では、 BRによってバックアップされた統計データはテーブル情報と一緒に保存され、リカバリ時にメモリにロードされます。そのため、バックアップ統計データが非常に大きい場合、 BR は大量のメモリを占有する必要があります。

v7.6.0 以降では、バックアップ統計は特定のファイルに個別に保存されます。BRはテーブルの復元を開始するまでどのテーブルの統計データもロードしないため、メモリが節約されます。
