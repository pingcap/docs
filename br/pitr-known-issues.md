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

## 自作の Minio システムをログ バックアップのストレージとして使用する場合、 <code>br restore point</code>または<code>br log truncate</code>を実行すると、 <code>RequestCanceled</code>エラーが返されます。 {#when-you-use-the-self-built-minio-system-as-the-storage-for-log-backups-running-code-br-restore-point-code-or-code-br-log-truncate-code-returns-a-code-requestcanceled-code-error}

問題: [#36515](https://github.com/pingcap/tidb/issues/36515)

```shell
[error="RequestCanceled: request context canceled\ncaused by: context canceled"]
```

このエラーは、現在のログ バックアップが多数の小さなファイルを生成するために発生します。自作の Minio ストレージ システムは、これらすべてのファイルを保存できません。

この問題を解決するには、Minio システムを大規模な分散クラスターにアップグレードするか、ログ バックアップ用のストレージとして Amazon S3 ストレージ システムを使用する必要があります。

## クラスターの負荷が高すぎる、リージョンが多すぎる、ストレージがパフォーマンスのボトルネックに達している (たとえば、自作の Minio システムをログ バックアップ用のストレージとして使用している) 場合、バックアップ進行状況チェックポイントの遅延が 10 分を超える可能性があります {#if-the-cluster-load-is-too-high-there-are-too-many-regions-and-the-storage-has-reached-a-performance-bottleneck-for-example-a-self-built-minio-system-is-used-as-storage-for-log-backups-the-backup-progress-checkpoint-delay-may-exceed-10-minutes}

問題: [#13030](https://github.com/tikv/tikv/issues/13030)

現在のログ バックアップでは多数の小さなファイルが生成されるため、自作の Minio システムは書き込み要件をサポートできず、バックアップの進行が遅くなります。

この問題を解決するには、Minio システムを大規模な分散クラスターにアップグレードするか、ログ バックアップ用のストレージとして Amazon S3 ストレージ システムを使用する必要があります。

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
