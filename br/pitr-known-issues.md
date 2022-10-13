---
title: Known Issues in Log Backup
summary: Learn known issues in log backup.
---

# ログ バックアップの既知の問題 {#known-issues-in-log-backup}

このドキュメントでは、ログ バックアップ機能を使用する場合の既知の問題と対応する回避策を示します。

## PITR 中または<code>br log truncate</code>コマンドの実行後に BR で OOM 問題が発生する {#br-encounters-the-oom-problem-during-a-pitr-or-after-you-run-the-code-br-log-truncate-code-command}

問題: [#36648](https://github.com/pingcap/tidb/issues/36648)

次の考えられる原因を検討してください。

-   回復するログ データが多すぎるため、PITR で OOM が発生します。代表的な原因として、次の 2 つが挙げられます。

    -   リカバリするログ範囲が大きすぎます。

        2 日以内、最長で 1 週間のログを回復することをお勧めします。つまり、PITR バックアップ プロセス中に少なくとも 2 日に 1 回、フル バックアップ操作を実行します。

    -   ログ バックアップ プロセス中に大量の書き込みが長時間発生します。

        クラスターを初期化するためにフル データ インポートを実行すると、通常、長時間にわたる大量の書き込みが発生します。最初のインポート後にスナップショット バックアップを実行し、そのバックアップを使用してクラスターを復元することをお勧めします。

-   削除するログの範囲が大きすぎるため、ログを削除すると OOM が発生します。

    この問題を解決するには、最初に削除するログの範囲を縮小し、対象のログを一度に削除するのではなく、数回に分けて削除します。

-   BR プロセスが配置されているノードのメモリ割り当てが低すぎます。

    ノードのメモリ構成を少なくとも 16 GB にスケールアップして、PITR にリカバリ用の十分なメモリ リソースがあることを確認することをお勧めします。

## アップストリーム データベースは物理インポート モードでTiDB Lightningを使用してデータをインポートするため、ログ バックアップ機能を使用できません。 {#the-upstream-database-imports-data-using-tidb-lightning-in-the-physical-import-mode-which-makes-it-impossible-to-use-the-log-backup-feature}

現在、ログ バックアップ機能はTiDB Lightningに完全には適合していません。そのため、 TiDB Lightningの物理モードでインポートされたデータは、ログにバックアップできません。

ログ バックアップ タスクを作成するアップストリーム クラスターでは、 TiDB Lightning物理モードを使用してデータをインポートすることは避けてください。代わりに、 TiDB Lightning論理モードを使用できます。物理モードを使用する必要がある場合は、インポートの完了後にスナップショット バックアップを実行して、PITR をスナップショット バックアップ後の時点に復元できるようにします。

## クラスターはネットワーク パーティションの障害から回復しましたが、ログ バックアップ タスクの進行状況のチェックポイントはまだ再開されません。 {#the-cluster-has-recovered-from-the-network-partition-failure-but-the-checkpoint-of-the-log-backup-task-progress-still-does-not-resume}

問題: [#13126](https://github.com/tikv/tikv/issues/13126)

クラスタでネットワーク パーティションに障害が発生した後、バックアップ タスクはログのバックアップを続行できません。一定の再試行時間の後、タスクは`ERROR`状態に設定されます。この時点で、バックアップ タスクは停止しています。

この問題を解決するには、 `br log resume`コマンドを手動で実行して、ログ バックアップ タスクを再開する必要があります。

## ログ バックアップで使用される実際のストレージ スペースは、クラスタ モニタリング メトリックに表示される増分データのボリュームの 2 ～ 3 倍です。 {#the-actual-storage-space-used-by-log-backup-is-2-3-times-the-volume-of-the-incremental-data-displayed-in-the-cluster-monitoring-metrics}

問題: [#13306](https://github.com/tikv/tikv/issues/13306)

この問題は、ログ バックアップ データがカスタマイズされたエンコード形式を使用するために発生します。フォーマットが異なればデータ圧縮率も異なり、その差は 2 ～ 3 倍です。

ログ バックアップは、RocksDB が SST ファイルを生成する方法ではデータを保存しません。これは、ログ バックアップ中に生成されるデータの範囲が大きく、内容が小さい可能性があるためです。このような場合、SST ファイルを取り込んでデータを復元しても、復元のパフォーマンスは向上しません。

## PITR を<code>execute over region id</code>エラーが返される {#the-error-code-execute-over-region-id-code-is-returned-when-you-perform-pitr}

問題: [#37207](https://github.com/pingcap/tidb/issues/37207)

この問題は通常、完全なデータ インポート中にログ バックアップを有効にし、その後 PITR を実行して、データ インポート中のある時点でデータを復元する場合に発生します。

具体的には、長時間 (24 時間など) に多数のホットスポット書き込みがあり、各 TiKV ノードの OPS が 50k/s を超える場合 (メトリクスはGrafana: **TiKV-Details** -&gt; <strong>Backup Log</strong> -&gt; <strong>Handle Event Rate</strong> )。

現在のバージョンでは、データのインポート後にスナップショット バックアップを実行し、このスナップショット バックアップに基づいて PITR を実行することをお勧めします。

## 大規模なトランザクションのコミット時間は、ログ バックアップのチェックポイント ラグに影響します {#the-commit-time-of-a-large-transaction-affects-the-checkpoint-lag-of-log-backup}

問題: [#13304](https://github.com/tikv/tikv/issues/13304)

大規模なトランザクションがある場合、ログ チェックポイント ラグは、トランザクションがコミットされる前に更新されません。したがって、トランザクションのコミット時間に近い時間、チェックポイントの遅延が増加します。

## インデックス追加機能の高速化は PITR と互換性がありません {#the-acceleration-of-adding-indexes-feature-is-not-compatible-with-pitr}

問題: [#38045](https://github.com/pingcap/tidb/issues/38045)

現在、 [インデックス追加の高速化](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)の機能は PITR と互換性がありません。インデックス アクセラレーションを使用する場合は、バックグラウンドで実行されている PITR ログ バックアップ タスクがないことを確認する必要があります。そうしないと、次のような予期しない動作が発生する可能性があります。

-   最初にログ バックアップ タスクを開始してから、インデックスを追加する場合。インデックス アクセラレーションが有効になっていても、インデックスの追加プロセスは高速化されません。しかし、インデックスはゆっくりと追加されます。
-   最初にインデックス アクセラレーション タスクを開始してから、ログ バックアップ タスクを開始した場合。ログ バックアップ タスクがエラーを返します。しかし、インデックスの加速は影響を受けません。
-   ログ バックアップ タスクとインデックス アクセラレーション タスクを同時に開始すると、2 つのタスクが互いを認識しない場合があります。これにより、PITR が新しく追加されたインデックスのバックアップに失敗する可能性があります。

## GCS または Azure Blob Storage で初めて<code>PITR Truncate</code>コマンドを実行するとエラーが発生する {#an-error-occurs-when-you-run-the-code-pitr-truncate-code-command-on-gcs-or-azure-blob-storage-for-the-first-time}

問題: [#38229](https://github.com/pingcap/tidb/issues/38229)

GCS または Azure Blob Storage で初めて`PITR Truncate`を実行すると、ファイル`v1_stream_trancate_safepoint.txt`が存在しないことが通知されます。この問題に対処するには、次の手順を実行します。

PITR のバックアップ ルート ディレクトリに、ファイル`v1_stream_trancate_safepoint.txt`を作成し、その中に`0`を書き込みます。このファイルには他の文字を含めてはならず、 `PITR Truncate`を初めて実行するときにのみ作成する必要があることに注意してください。

<!-- TODO: Add the following content upon v6.4.0 release  -->

<!-- Alternatively, use BR of v6.4.0 or later. -->
