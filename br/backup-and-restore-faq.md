---
title: Backup & Restore FAQs
summary: Learn about Frequently Asked Questions (FAQs) and the solutions of BR.
---

# バックアップと復元に関するよくある質問 {#backup-x26-restore-faqs}

このドキュメントには、バックアップと復元 (BR) に関するよくある質問 (FAQ) と解決策が記載されています。

## TiDB v5.4.0 以降のバージョンで、ワークロードの高いクラスタでバックアップ タスクを実行すると、バックアップ タスクの速度が遅くなるのはなぜですか? {#in-tidb-v5-4-0-and-later-versions-when-backup-tasks-are-performed-on-the-cluster-under-high-workload-why-does-the-speed-of-backup-tasks-become-slow}

TiDB v5.4.0 から、BR はバックアップ タスクの自動調整機能を導入します。 v5.4.0 以降のバージョンのクラスターの場合、この機能はデフォルトで有効になっています。クラスターのワークロードが重い場合、この機能はバックアップ タスクで使用されるリソースを制限して、オンライン クラスターへの影響を軽減します。詳細については、 [BR オートチューン](/br/br-auto-tune.md)を参照してください。

TiKV は[動的構成](/tikv-control.md#modify-the-tikv-configuration-dynamically)自動調整機能をサポートしています。クラスターを再起動せずに、次の方法で機能を有効または無効にすることができます。

-   自動調整を無効にする: TiKV 構成項目[`backup.enable-auto-tune`](/tikv-configuration-file.md#enable-auto-tune-new-in-v540)から`false`を設定します。
-   自動調整を有効にする: `backup.enable-auto-tune` ～ `true`を設定します。 v5.3.x から v5.4.0 以降のバージョンにアップグレードされたクラスターの場合、自動調整機能はデフォルトで無効になっています。手動で有効にする必要があります。

`tikv-ctl`を使用して自動調整を有効または無効にするには、 [自動調整を使用する](/br/br-auto-tune.md#use-auto-tune)を参照してください。

さらに、自動調整により、バックアップ タスクで使用されるデフォルトのスレッド数が減少します。詳細については、 `backup.num-threads` ](/tikv-configuration-file.md#num-threads-1) を参照してください。そのため、Grafana ダッシュボードでは、バックアップ タスクで使用される速度、CPU 使用率、および I/O リソース使用率が、v5.4.0 より前のバージョンよりも低くなります。 v5.4.0 より前では、デフォルト値の`backup.num-threads`は`CPU * 0.75`でした。つまり、バックアップ タスクで使用されるスレッドの数は、論理 CPU コアの 75% を占めていました。その最大値は`32`でした。 v5.4.0 以降、この構成項目のデフォルト値は`CPU * 0.5`で、最大値は`8`です。

オフライン クラスターでバックアップ タスクを実行する場合、バックアップを高速化するために、 `tikv-ctl`を使用して`backup.num-threads`の値をより大きな数値に変更できます。

## データの復元中にエラー メッセージ<code>could not read local://...:download sst failed</code>が返された場合はどうすればよいですか? {#what-should-i-do-if-the-error-message-code-could-not-read-local-download-sst-failed-code-is-returned-during-data-restoration}

データを復元する場合、各ノードは**すべての**バックアップ ファイル (SST ファイル) にアクセスできる必要があります。デフォルトでは、 `local`のストレージが使用されている場合、バックアップ ファイルが異なるノードに分散しているため、データを復元できません。したがって、各 TiKV ノードのバックアップ ファイルを他の TiKV ノードにコピーする必要があります。

バックアップ中は、NFS ディスクをバックアップ ディスクとしてマウントすることをお勧めします。詳細については、 [1 つのテーブルをネットワーク ディスクにバックアップする](/br/backup-and-restore-use-cases.md#back-up-a-single-table-to-a-network-disk-recommended-for-production-environments)を参照してください。

## バックアップ操作はクラスターにどの程度の影響を与えますか? {#how-much-impact-does-a-backup-operation-have-on-the-cluster}

TiDB v5.4.0 以降のバージョンの場合、BR はバックアップ タスクで使用されるデフォルトの CPU 使用率を削減するだけでなく、負荷の高いクラスター内のバックアップ タスクで使用されるリソースを制限する[BR オートチューン](/br/br-auto-tune.md)つの機能も導入します。したがって、負荷の高い v5.4.0 クラスターでバックアップ タスクのデフォルト構成を使用すると、タスクがクラスターのパフォーマンスに与える影響は、v5.4.0 より前のクラスターよりも大幅に小さくなります。

以下は、単一ノードでの内部テストです。テスト結果は、**全速バックアップ**シナリオで v5.4.0 と v5.3.0 のデフォルト構成を使用する場合、BR を使用したバックアップがクラスター パフォーマンスに与える影響がまったく異なることを示しています。詳細なテスト結果は次のとおりです。

-   BR が v5.3.0 のデフォルト構成を使用する場合、書き込み専用ワークロードの QPS は 75% 減少します。
-   BR が v5.4.0 のデフォルト構成を使用する場合、同じワークロードの QPS は 25% 減少します。ただし、この構成を使用すると、BR を使用したバックアップ タスクの期間がそれに応じて長くなります。所要時間は v5.3.0 構成の 1.7 倍です。

次のいずれかのソリューションを使用して、クラスターのパフォーマンスに対するバックアップ タスクの影響を手動で制御できます。これらの方法は、クラスターに対するバックアップ タスクの影響を軽減しますが、バックアップ タスクの速度も低下させることに注意してください。

-   `--ratelimit`パラメータを使用して、バックアップ タスクの速度を制限します。このパラメータは、**バックアップ ファイルを外部ストレージに保存**する速度を制限することに注意してください。バックアップ ファイルの合計サイズを計算するときは、バックアップ ログの`backup data size(after compressed)`をベンチマークとして使用します。
-   TiKV 構成項目[`backup.num-threads`](/tikv-configuration-file.md#num-threads-1)を調整して、バックアップ タスクで使用されるスレッドの数を制限します。 BR がバックアップ タスクに`8`以下のスレッドを使用し、クラスターの合計 CPU 使用率が 60% を超えない場合、読み取りおよび書き込みワークロードに関係なく、バックアップ タスクはクラスターにほとんど影響を与えません。

## BR はシステム テーブルをバックアップしますか?データの復元中に競合が発生しますか? {#does-br-back-up-system-tables-during-data-restoration-do-they-raise-conflicts}

v5.1.0 より前では、BR はバックアップ中にシステム スキーマ`mysql.*`からデータを除外します。 v5.1.0 以降、BR はデフォルトで、システム スキーマを含むすべてのデータを**バックアップ**します`mysql.*` 。

`mysql.*`のシステム テーブルを復元する技術的な実装はまだ完了していないため、システム スキーマ`mysql`のテーブルはデフォルトで**は復元されません**。つまり、競合は発生しません。詳細については、 [`mysql`スキーマで作成されたテーブルを復元します (実験的)](/br/br-usage-restore.md#restore-tables-created-in-the-mysql-schema)を参照してください。

## root を使用して BR を実行しようとしても失敗した場合でも、 <code>Permission denied</code>または<code>No such file or directory</code>エラーを処理するにはどうすればよいですか? {#what-should-i-do-to-handle-the-code-permission-denied-code-or-code-no-such-file-or-directory-code-error-even-if-i-have-tried-to-run-br-using-root-in-vain}

TiKV がバックアップ ディレクトリにアクセスできるかどうかを確認する必要があります。データをバックアップするには、TiKV に書き込み権限があるかどうかを確認します。データを復元するには、読み取り権限があるかどうかを確認してください。

バックアップ操作中、ストレージ メディアがローカル ディスクまたはネットワーク ファイル システム (NFS) の場合、BR を起動するユーザーと TiKV を起動するユーザーが一致していることを確認します (BR と TiKV が異なるマシン上にある場合、ユーザーは&#39; UID は一貫している必要があります)。そうしないと、 `Permission denied`の問題が発生する可能性があります。

バックアップ ファイル (SST ファイル) は TiKV によって保存されるため、root アクセスで BR を実行すると、ディスクのアクセス許可が原因で失敗する場合があります。

> **ノート：**
>
> データの復元中に同じ問題が発生する可能性があります。 SST ファイルが初めて読み取られるときに、読み取り許可が検証されます。 DDL の実行時間は、権限のチェックと BR の実行の間に長い間隔がある可能性があることを示唆しています。長時間待機すると、エラー メッセージ`Permission denied`が表示される場合があります。
>
> したがって、次の手順に従って、データを復元する前に権限を確認することをお勧めします。

1.  プロセス クエリの Linux ネイティブ コマンドを実行します。

    {{< copyable "" >}}

    ```bash
    ps aux | grep tikv-server
    ```

    上記のコマンドの出力:

    ```shell
    tidb_ouo  9235 10.9  3.8 2019248 622776 ?      Ssl  08:28   1:12 bin/tikv-server --addr 0.0.0.0:20162 --advertise-addr 172.16.6.118:20162 --status-addr 0.0.0.0:20188 --advertise-status-addr 172.16.6.118:20188 --pd 172.16.6.118:2379 --data-dir /home/user1/tidb-data/tikv-20162 --config conf/tikv.toml --log-file /home/user1/tidb-deploy/tikv-20162/log/tikv.log
    tidb_ouo  9236  9.8  3.8 2048940 631136 ?      Ssl  08:28   1:05 bin/tikv-server --addr 0.0.0.0:20161 --advertise-addr 172.16.6.118:20161 --status-addr 0.0.0.0:20189 --advertise-status-addr 172.16.6.118:20189 --pd 172.16.6.118:2379 --data-dir /home/user1/tidb-data/tikv-20161 --config conf/tikv.toml --log-file /home/user1/tidb-deploy/tikv-20161/log/tikv.log
    ```

    または、次のコマンドを実行できます。

    {{< copyable "" >}}

    ```bash
    ps aux | grep tikv-server | awk '{print $1}'
    ```

    上記のコマンドの出力:

    ```shell
    tidb_ouo
    tidb_ouo
    ```

2.  TiUP コマンドを使用して、クラスターの起動情報を照会します。

    {{< copyable "" >}}

    ```bash
    tiup cluster list
    ```

    上記のコマンドの出力:

    ```shell
    [root@Copy-of-VM-EE-CentOS76-v1 br]# tiup cluster list
    Starting component `cluster`: /root/.tiup/components/cluster/v1.5.2/tiup-cluster list
    Name          User      Version  Path                                               PrivateKey
    ----          ----      -------  ----                                               ----------
    tidb_cluster  tidb_ouo  v5.0.2   /root/.tiup/storage/cluster/clusters/tidb_cluster  /root/.tiup/storage/cluster/clusters/tidb_cluster/ssh/id_rsa
    ```

3.  バックアップディレクトリの権限を確認してください。たとえば、 `backup`はバックアップ データ ストレージ用です。

    {{< copyable "" >}}

    ```bash
    ls -al backup
    ```

    上記のコマンドの出力:

    ```shell
    [root@Copy-of-VM-EE-CentOS76-v1 user1]# ls -al backup
    total 0
    drwxr-xr-x  2 root root   6 Jun 28 17:48 .
    drwxr-xr-x 11 root root 310 Jul  4 10:35 ..
    ```

    上記の出力から、 `tikv-server`インスタンスがユーザー`tidb_ouo`によって開始されていることがわかります。しかし、ユーザー`tidb_ouo`には`backup`に対する書き込み権限がありません。したがって、バックアップは失敗します。

## <code>Io(Os...)</code>エラーを処理するにはどうすればよいですか? {#what-should-i-do-to-handle-the-code-io-os-code-error}

これらの問題のほとんどは、TiKV がディスクにデータを書き込むときに発生するシステム コール エラーです (例: `Io(Os {code: 13, kind: PermissionDenied...})`または`Io(Os {code: 2, kind: NotFound...})` )。

このような問題を解決するには、まずバックアップ ディレクトリのマウント方法とファイル システムを確認し、別のフォルダまたは別のハードディスクにデータをバックアップしてみてください。

たとえば、 `samba`によって構築されたネットワーク ディスクにデータをバックアップするときに、 `Code: 22(invalid argument)`エラーが発生する場合があります。

## <code>rpc error: code = Unavailable desc =...</code> BR でエラーが発生しましたか? {#what-should-i-do-to-handle-the-code-rpc-error-code-unavailable-desc-code-error-occurred-in-br}

このエラーは、リストア (BR を使用) するクラスターの容量が不足している場合に発生する可能性があります。このクラスターの監視メトリクスまたは TiKV ログを確認することで、原因をさらに確認できます。

この問題を処理するには、クラスター リソースをスケールアウトし、復元中の同時実行数を減らして、 `RATE_LIMIT`オプションを有効にします。

## <code>local</code>ストレージを使用する場合、バックアップ ファイルはどこに保存されますか? {#where-are-the-backed-up-files-stored-when-i-use-code-local-code-storage}

`local`のストレージを使用すると、BR が実行されているノードに`backupmeta`が生成され、各リージョンのリーダー ノードにバックアップ ファイルが生成されます。

## バックアップデータのサイズはどうですか？バックアップのレプリカはありますか? {#how-about-the-size-of-the-backup-data-are-there-replicas-of-the-backup}

データのバックアップ中に、各リージョンのリーダー ノードでバックアップ ファイルが生成されます。バックアップのサイズはデータ サイズと同じで、冗長レプリカはありません。したがって、データの合計サイズは、ほぼ TiKV データの合計数をレプリカの数で割ったものになります。

ただし、ローカル ストレージからデータを復元する場合は、各 TiKV がすべてのバックアップ ファイルにアクセスできる必要があるため、レプリカの数は TiKV ノードの数と同じになります。

## BR が TiCDC/ Drainerの上流クラスターにデータを復元する場合、どうすればよいですか? {#what-should-i-do-when-br-restores-data-to-the-upstream-cluster-of-ticdc-drainer}

-   **BR を使用して復元されたデータは、ダウンストリームに複製できません**。これは、BR は SST ファイルを直接インポートしますが、現在、ダウンストリーム クラスターはこれらのファイルをアップストリームから取得できないためです。

-   v4.0.3 より前では、BR 復元中に生成された DDL ジョブにより、TiCDC/ Drainerで予期しない DDL が実行される場合がありました。したがって、TiCDC/ Drainer の上流クラスターで復元を実行する必要がある場合は、BR を使用して復元されたすべてのテーブルをDrainer / Drainerブロック リストに追加します。

[`filter.rules`](https://github.com/pingcap/tiflow/blob/7c3c2336f98153326912f3cf6ea2fbb7bcc4a20c/cmd/changefeed.toml#L16)を使用して TiCDC のブロック リストを構成し、 [`syncer.ignore-table`](/tidb-binlog/tidb-binlog-configuration-file.md#ignore-table)を使用してDrainerのブロック リストを構成できます。

## BR は、テーブルの<code>SHARD_ROW_ID_BITS</code>および<code>PRE_SPLIT_REGIONS</code>情報をバックアップしますか?復元されたテーブルには複数のリージョンがありますか? {#does-br-back-up-the-code-shard-row-id-bits-code-and-code-pre-split-regions-code-information-of-a-table-does-the-restored-table-have-multiple-regions}

はい。 BR は、テーブルの[`SHARD_ROW_ID_BITS`および<code>PRE_SPLIT_REGIONS</code>](/sql-statements/sql-statement-split-region.md#pre_split_regions)の情報をバックアップします。復元されたテーブルのデータも複数のリージョンに分割されます。

## <code>the entry too large, the max entry size is 6291456, the size of data is 7690800</code>というエラー メッセージで復元が失敗した場合はどうすればよいですか? {#what-should-i-do-if-the-restore-fails-with-the-error-message-code-the-entry-too-large-the-max-entry-size-is-6291456-the-size-of-data-is-7690800-code}

`--ddl-batch-size` ～ `128`以下の値を設定することで、一度に作成するテーブルの数を減らすことができます。

BR を使用して [ `--ddl-batch-size` ](/br/br-batch-create-table.md#how to use) の値が`1`より大きいバックアップ データを復元する場合、TiDB はテーブル作成の DDL ジョブを DDL ジョブ キューに書き込みます。これは TiKV によって維持されます。現時点では、TiDB が一度に送信するすべてのテーブル スキーマの合計サイズは 6 MB を超えてはなりません。これは、ジョブ メッセージの最大値がデフォルトで`6 MB`であるためです (この値を変更することは**お勧め**しません。詳細については、 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50)および を参照してください)。 [`raft-entry-max-size`](/tikv-configuration-file.md#raft-entry-max-size) ）。したがって、 `--ddl-batch-size`を過度に大きな値に設定すると、TiDB によって一度にバッチで送信されるテーブルのスキーマ サイズが指定された値を超えるため、BR は`entry too large, the max entry size is 6291456, the size of data is 7690800`エラーを報告します。

## BR を使用してバックアップ データを復元した後、SQL クエリで the <code>region is unavailable</code>エラーが報告されるのはなぜですか? {#why-is-the-code-region-is-unavailable-code-error-reported-for-a-sql-query-after-i-use-br-to-restore-the-backup-data}

BR を使用してバックアップされたクラスターに TiFlash がある場合、 `TableInfo`は BR がバックアップ データを復元するときに TiFlash 情報を格納します。復元するクラスターに TiFlash がない場合、 `region is unavailable`エラーが報告されます。

## BR は、一部の履歴バックアップのインプレース完全復元をサポートしていますか? {#does-br-support-in-place-full-restoration-of-some-historical-backup}

いいえ。BR は、一部の履歴バックアップのインプレース完全復元をサポートしていません。

## BR を Kubernetes の増分バックアップに使用するにはどうすればよいですか? {#how-can-i-use-br-for-incremental-backup-on-kubernetes}

最後の BR バックアップの`commitTs`フィールドを取得するには、kubectl を使用して`kubectl -n ${namespace} get bk ${name}`コマンドを実行します。このフィールドの内容を`--lastbackupts`として使用できます。

## BR backupTS を Unix 時間に変換するにはどうすればよいですか? {#how-can-i-convert-br-backupts-to-unix-time}

BR `backupTS`のデフォルトは、バックアップ開始前に PD から取得した最新のタイムスタンプです。 `pd-ctl tso timestamp`を使用してタイムスタンプを解析して正確な値を取得するか、 `backupTS >> 18`を使用して推定値をすばやく取得できます。

## BR がバックアップ データを復元した後、テーブルとインデックスの TiDB の統計を更新するためにテーブルで<code>ANALYZE</code>ステートメントを実行する必要がありますか? {#after-br-restores-the-backup-data-do-i-need-to-execute-the-code-analyze-code-statement-on-the-table-to-update-the-statistics-of-tidb-on-the-tables-and-indexes}

BR は統計をバックアップしません (v4.0.9 を除く)。したがって、バックアップデータを復元した後、手動で実行するか`ANALYZE TABLE` 、または TiDB が自動的に実行されるのを待つ必要があります`ANALYZE` 。

v4.0.9 では、BR はデフォルトで統計をバックアップしますが、これは大量のメモリを消費します。バックアップ プロセスが正常に行われるようにするため、v4.0.10 以降、統計のバックアップはデフォルトで無効になっています。

テーブルで`ANALYZE`を実行しない場合、TiDB は不正確な統計のために最適化された実行計画を選択できません。クエリのパフォーマンスが重要な問題でない場合は、 `ANALYZE`を無視できます。

## 複数の BR プロセスを同時に使用して、1 つのクラスターのデータを復元できますか? {#can-i-use-multiple-br-processes-at-the-same-time-to-restore-the-data-of-a-single-cluster}

次の理由により、複数の BR プロセスを同時に使用して 1 つのクラスターのデータを復元する**ことは強くお勧め**しません。

-   BR がデータを復元すると、PD の一部のグローバル構成が変更されます。そのため、複数の BR プロセスを同時にデータ復元に使用すると、これらの構成が誤って上書きされ、クラスター状態が異常になる可能性があります。
-   BR はデータを復元するために多くのクラスター リソースを消費するため、実際には、BR プロセスを並行して実行しても、復元速度は限られた範囲でしか改善されません。
-   データ復元のために複数の BR プロセスを並行して実行するテストは行われていないため、成功することは保証されていません。

## バックアップ ログで<code>key locked Error</code>が報告された場合はどうすればよいですか? {#what-should-i-do-if-the-backup-log-reports-code-key-locked-error-code}

ログのエラー メッセージ: `log - ["backup occur kv error"][error="{\"KvError\":{\"locked\":`

バックアップ プロセス中にキーがロックされている場合、BR はロックの解決を試みます。このエラーがたまにしか発生しない場合は、バックアップの正確性に影響はありません。

## バックアップ操作が失敗した場合はどうすればよいですか? {#what-should-i-do-if-a-backup-operation-fails}

ログのエラー メッセージ: `log - Error: msg:"Io(Custom { kind: AlreadyExists, error: \"[5_5359_42_123_default.sst] is already exists in /dir/backup_local/\" })"`

バックアップ操作が失敗し、前述のメッセージが表示された場合は、次のいずれかの操作を実行してから、バックアップを再度開始します。

-   バックアップのディレクトリを変更します。たとえば、 `/dir/backup_local/`を`/dir/backup-2020-01-01/`に変更します。
-   すべての TiKV ノードと BR ノードのバックアップ ディレクトリを削除します。

## BR バックアップまたは復元後に、監視ノードに表示されるディスク使用量が一貫していない場合はどうすればよいですか? {#what-should-i-do-if-the-disk-usage-shown-on-the-monitoring-node-is-inconsistent-after-br-backup-or-restoration}

この不一致は、バックアップで使用されるデータ圧縮率が、復元で使用されるデフォルトの圧縮率と異なることが原因で発生します。チェックサムが成功した場合、この問題は無視できます。

## 配置ルールをクラスターに復元するとエラーが発生するのはなぜですか? {#why-does-an-error-occur-when-i-restore-placement-rules-to-a-cluster}

v6.0.0 より前では、BR は[配置ルール](/placement-rules-in-sql.md)をサポートしていません。 v6.0.0 以降、BR は配置ルールをサポートし、コマンドライン オプション`--with-tidb-placement-mode=strict/ignore`を導入して、配置ルールのバックアップおよび復元モードを制御します。デフォルト値`strict`では、BR は配置ルールをインポートして検証しますが、値が`ignore`の場合はすべての配置ルールを無視します。

## BR が<code>new_collations_enabled_on_first_bootstrap</code>不一致を報告するのはなぜですか? {#why-does-br-report-code-new-collations-enabled-on-first-bootstrap-code-mismatch}

TiDB v6.0.0 以降、デフォルト値の[`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)が`false`から`true`に変更されました。 BR は上流クラスタの`new_collations_enabled_on_first_bootstrap`構成をバックアップし、この構成の値が上流クラスタと下流クラスタの間で一致しているかどうかを確認します。値が一致する場合、BR は上流のクラスターにバックアップされたデータを下流のクラスターに安全に復元します。値が一致しない場合、BR はデータの復元を実行せず、エラーを報告します。

v6.0.0 の以前のバージョンの TiDB クラスター内のデータをバックアップしており、このデータを v6.0.0 以降のバージョンの TiDB クラスターに復元するとします。この状況では、 `new_collations_enabled_on_first_bootstrap`の値がアップストリーム クラスターとダウンストリーム クラスター間で一貫しているかどうかを手動で確認する必要があります。

-   値が一貫している場合は、復元コマンドに`--check-requirements=false`を追加して、この構成チェックをスキップできます。
-   値に矛盾があり、強制的に復元を実行すると、BR はデータ検証エラーを報告します。
