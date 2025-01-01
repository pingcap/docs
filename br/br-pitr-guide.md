---
title: TiDB Log Backup and PITR Guide
summary: TiDB ログ バックアップおよび PITR ガイドでは、br コマンドライン ツールを使用してデータをバックアップおよび復元する方法について説明します。ログ バックアップの開始、定期的な完全バックアップの実行、古いデータのクリーンアップの手順が含まれています。また、このガイドでは、PITR の実行と PITR のパフォーマンス機能に関する情報も提供しています。
---

# TiDB ログ バックアップと PITR ガイド {#tidb-log-backup-and-pitr-guide}

フルバックアップ（スナップショットバックアップ）には、特定の時点での完全なクラスターデータが含まれますが、TiDB ログバックアップは、アプリケーションによって書き込まれたデータを指定されたstorageにタイムリーにバックアップできます。必要に応じて復元ポイントを選択する場合、つまりポイントインタイムリカバリ（PITR）を実行する場合は、 [ログバックアップを開始する](#start-log-backup)と[定期的に完全バックアップを実行する](#run-full-backup-regularly)選択できます。

br コマンドライン ツール (以下、 `br`と呼びます) を使用してデータをバックアップまたは復元する前に、まず[インストール`br`](/br/br-use-overview.md#deploy-and-use-br)を行う必要があります。

## TiDBクラスタをバックアップする {#back-up-tidb-cluster}

### ログバックアップを開始 {#start-log-backup}

> **注記：**
>
> -   次の例では、Amazon S3IAMキーとシークレットキーを使用して権限を承認することを前提としています。IAM ロールを使用して権限を承認する場合は、 `--send-credentials-to-tikv`から`false`に設定する必要があります。
> -   他のstorageシステムまたは認証方法を使用して権限を認証する場合は、 [バックアップストレージ](/br/backup-and-restore-storages.md)に従ってパラメータ設定を調整します。

ログ バックアップを開始するには、 `tiup br log start`実行します。クラスターは 1 回につき 1 つのログ バックアップ タスクのみを実行できます。

```shell
tiup br log start --task-name=pitr --pd "${PD_IP}:2379" \
--storage 's3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}'
```

ログ バックアップ タスクが開始されると、手動で停止するまで TiDB クラスターのバックグラウンドで実行されます。このプロセス中、TiDB 変更ログは指定されたstorageに小さなバッチで定期的にバックアップされます。ログ バックアップ タスクのステータスを照会するには、次のコマンドを実行します。

```shell
tiup br log status --task-name=pitr --pd "${PD_IP}:2379"
```

期待される出力:

    ● Total 1 Tasks.
    > #1 <
        name: pitr
        status: ● NORMAL
        start: 2022-05-13 11:09:40.7 +0800
          end: 2035-01-01 00:00:00 +0800
        storage: s3://backup-101/log-backup
        speed(est.): 0.00 ops/s
    checkpoint[global]: 2022-05-13 11:31:47.2 +0800; gap=4m53s

### 定期的に完全バックアップを実行する {#run-full-backup-regularly}

スナップショット バックアップは、完全バックアップの方法として使用できます`tiup br backup full`実行すると、固定スケジュール (たとえば、2 日ごと) に従ってクラスター スナップショットをバックアップstorageにバックアップできます。

```shell
tiup br backup full --pd "${PD_IP}:2379" \
--storage 's3://backup-101/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}'
```

## PITRを実行する {#run-pitr}

バックアップ保持期間内の任意の時点にクラスターを復元するには、 `tiup br restore point`使用します。このコマンドを実行するときは、**復元する時点**、**その時点より前の最新のスナップショット バックアップ データ**、および**ログ バックアップ データ**を指定する必要があります。BRは復元に必要なデータを自動的に判別して読み取り、これらのデータを指定されたクラスターに順番に復元します。

```shell
tiup br restore point --pd "${PD_IP}:2379" \
--storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}' \
--full-backup-storage='s3://backup-101/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}' \
--restored-ts '2022-05-15 18:00:00+0800'
```

データの復元中は、ターミナルの進行状況バーで進行状況を確認できます。復元は、完全復元とログ復元 (メタファイルの復元と KV ファイルの復元) の 2 つのフェーズに分かれています。各フェーズが完了すると、復元時間やデータ サイズなどの情報`br`出力されます。

```shell
Full Restore <--------------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
*** ["Full Restore success summary"] ****** [total-take=xxx.xxxs] [restore-data-size(after-compressed)=xxx.xxx] [Size=xxxx] [BackupTS={TS}] [total-kv=xxx] [total-kv-size=xxx] [average-speed=xxx]
Restore Meta Files <--------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
Restore KV Files <----------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
*** ["restore log success summary"] [total-take=xxx.xx] [restore-from={TS}] [restore-to={TS}] [total-kv-count=xxx] [total-size=xxx]
```

## 古いデータをクリーンアップする {#clean-up-outdated-data}

[TiDB バックアップと復元の使用概要](/br/br-use-overview.md)で説明したとおり:

PITR を実行するには、復元ポイントより前のフルバックアップと、フルバックアップポイントから復元ポイントまでのログバックアップを復元する必要があります。そのため、バックアップ保持期間を超えるログバックアップについては、 `tiup br log truncate`使用して指定時点より前のバックアップを削除できます。**フルスナップショットより前のログバックアップのみ削除することをお勧めします**。

次の手順では、バックアップ保持期間を超えたバックアップ データをクリーンアップする方法について説明します。

1.  バックアップ保持期間外の**最後の完全バックアップを**取得します。

2.  `validate`コマンドを使用して、バックアップに対応する時点を取得します。2022/09/01 より前のバックアップ データを消去する必要があると仮定すると、この時点より前の最後の完全バックアップを探して、消去されないことを確認する必要があります。

    ```shell
    FULL_BACKUP_TS=`tiup br validate decode --field="end-version" --storage "s3://backup-101/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}"| tail -n1`
    ```

3.  スナップショットバックアップ`FULL_BACKUP_TS`より前のログバックアップデータを削除します。

    ```shell
    tiup br log truncate --until=${FULL_BACKUP_TS} --storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}'
    ```

4.  スナップショットバックアップ`FULL_BACKUP_TS`より前のスナップショットデータを削除します。

    ```shell
    aws s3 rm --recursive s3://backup-101/snapshot-${date}
    ```

## PITRのパフォーマンス機能 {#performance-capabilities-of-pitr}

-   各 TiKV ノードでは、PITR はスナップショット データ (完全復元) を 2 TiB/h の速度で復元し、ログ データ (メタ ファイルと KV ファイルを含む) を 30 GiB/h の速度で復元できます。
-   BRは古くなったログバックアップデータ（ `tiup br log truncate` ）を600GB/hの速度で削除します。

> **注記：**
>
> 上記の仕様は、次の 2 つのテスト シナリオのテスト結果に基づいています。実際のデータは異なる場合があります。
>
> -   スナップショット データの復元速度 = クラスター内のすべての TiKV ノードに復元されたスナップショット データの合計サイズ / (所要時間 * TiKV ノードの数)
> -   ログデータの復元速度 = クラスター内のすべての TiKV ノードに復元されたログデータの合計サイズ / (期間 * TiKV ノードの数)
>
> 外部storageには、単一のレプリカの KV データのみが含まれます。したがって、外部storageのデータ サイズは、クラスターで復元された実際のデータ サイズを表すものではありません。BRは、クラスターに構成されたレプリカの数に応じてすべてのレプリカを復元します。レプリカの数が多いほど、実際に復元できるデータが多くなります。テストのすべてのクラスターのデフォルトのレプリカ数は 3 です。全体的な復元パフォーマンスを向上させるには、TiKV 構成ファイルの[`import.num-threads`](/tikv-configuration-file.md#import)項目とBRコマンドの[`concurrency`](/br/use-br-command-line-tool.md#common-options)オプションを変更します。

テストシナリオ 1 ( [TiDB Cloud](https://tidbcloud.com) ) は次のとおりです。

-   TiKVノード数（8コア、16GBメモリ）: 21
-   TiKV構成項目`import.num-threads` :8
-   BRコマンドオプション`concurrency` :128
-   地域数: 183,000
-   クラスターで作成された新しいログデータ: 10 GB/時間
-   書き込み (INSERT/UPDATE/DELETE) QPS: 10,000

テスト シナリオ 2 (TiDB Self-Managed 上) は次のとおりです。

-   TiKVノード数（8コア、64GBメモリ）: 6
-   TiKV構成項目`import.num-threads` :8
-   BRコマンドオプション`concurrency` :128
-   地域数: 50,000
-   クラスターで作成された新しいログデータ: 10 GB/時間
-   書き込み (INSERT/UPDATE/DELETE) QPS: 10,000

## 監視と警告 {#monitoring-and-alert}

ログ バックアップ タスクが分散された後、各 TiKV ノードは継続的にデータを外部storageに書き込みます。このプロセスの監視データは**、TiKV 詳細 &gt; バックアップ ログ**ダッシュボードで表示できます。

メトリックが正常範囲から外れた場合に通知を受け取るには、 [ログバックアップアラート](/br/br-monitoring-and-alert.md#log-backup-alerts)参照してアラート ルールを構成します。

## 参照 {#see-also}

-   [TiDB バックアップと復元のユースケース](/br/backup-and-restore-use-cases.md)
-   [br コマンドラインマニュアル](/br/use-br-command-line-tool.md)
-   [ログバックアップとPITRアーキテクチャ](/br/br-log-architecture.md)
-   [バックアップと復元の監視とアラート](/br/br-monitoring-and-alert.md)
