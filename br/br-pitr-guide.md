---
title: TiDB Log Backup and PITR Guide
summary: Learns about how to perform log backup and PITR in TiDB.
aliases: ['/tidb/stable/pitr-usage/']
---

# TiDB ログのバックアップと PITR ガイド {#tidb-log-backup-and-pitr-guide}

完全バックアップ (スナップショット バックアップ) には、特定の時点での完全なクラスター データが含まれますが、TiDB ログ バックアップでは、アプリケーションによって書き込まれたデータを指定されたstorageにタイムリーにバックアップできます。必要に応じて復元ポイントを選択する場合、つまりポイント イン タイム リカバリ (PITR) を実行する場合は、 [ログのバックアップを開始](#start-log-backup)と[完全バックアップを定期的に実行する](#run-full-backup-regularly)を実行できます。

br コマンドライン ツール (以下`br`と呼びます) を使用してデータをバックアップまたは復元する前に、まず[インストール`br`](/br/br-use-overview.md#deploy-and-use-br)実行する必要があります。

## TiDB クラスターのバックアップ {#back-up-tidb-cluster}

### ログのバックアップを開始 {#start-log-backup}

> **ノート：**
>
> -   次の例では、Amazon S3 アクセス キーとシークレット キーを使用してアクセス許可を承認することを前提としています。 IAMロールを使用してパーミッションを承認する場合は、 `--send-credentials-to-tikv`から`false`を設定する必要があります。
> -   他のstorageシステムまたは認証方法を使用してパーミッションを認証する場合は、 [バックアップ ストレージ](/br/backup-and-restore-storages.md)に従ってパラメーター設定を調整します。

ログ バックアップを開始するには、 `br log start`を実行します。クラスターは、毎回 1 つのログ バックアップ タスクしか実行できません。

```shell
tiup br log start --task-name=pitr --pd "${PD_IP}:2379" \
--storage 's3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}"'
```

ログ バックアップ タスクが開始されると、手動で停止するまで TiDB クラスターのバックグラウンドで実行されます。このプロセス中、TiDB の変更ログは指定されたstorageに小さなバッチで定期的にバックアップされます。ログ バックアップ タスクの状態を照会するには、次のコマンドを実行します。

```shell
tiup br log status --task-name=pitr --pd "${PD_IP}:2379"
```

期待される出力:

```
● Total 1 Tasks.
> #1 <
    name: pitr
    status: ● NORMAL
    start: 2022-05-13 11:09:40.7 +0800
      end: 2035-01-01 00:00:00 +0800
    storage: s3://backup-101/log-backup
    speed(est.): 0.00 ops/s
checkpoint[global]: 2022-05-13 11:31:47.2 +0800; gap=4m53s
```

### 完全バックアップを定期的に実行する {#run-full-backup-regularly}

スナップショット バックアップは、フル バックアップの方法として使用できます。 `br backup full`実行すると、固定スケジュール (たとえば、2 日ごと) に従ってクラスター スナップショットをバックアップstorageにバックアップできます。

```shell
tiup br backup full --pd "${PD_IP}:2379" \
--storage 's3://backup-101/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}"'
```

## PITR を実行する {#run-pitr}

バックアップ保持期間内の任意の時点にクラスターを復元するには、 `br restore point`を使用できます。このコマンドを実行するときは、**復元する時点**、<strong>その時点より前の最新のスナップショット バックアップ データ</strong>、および<strong>ログ バックアップ データ</strong>を指定する必要があります。 BR は、復元に必要なデータを自動的に判別して読み取り、指定されたクラスターにこれらのデータを順番に復元します。

```shell
br restore point --pd "${PD_IP}:2379" \
--storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}"' \
--full-backup-storage='s3://backup-101/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}"' \
--restored-ts '2022-05-15 18:00:00+0800'
```

データの復元中は、ターミナルの進行状況バーで進行状況を確認できます。復元は、完全復元とログ復元 (メタ ファイルの復元と KV ファイルの復元) の 2 つのフェーズに分かれています。各フェーズが完了すると、 `br`復元時間やデータ サイズなどの情報を出力します。

```shell
Full Restore <--------------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
*** ["Full Restore success summary"] ****** [total-take=xxx.xxxs] [restore-data-size(after-compressed)=xxx.xxx] [Size=xxxx] [BackupTS={TS}] [total-kv=xxx] [total-kv-size=xxx] [average-speed=xxx]
Restore Meta Files <--------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
Restore KV Files <----------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
*** ["restore log success summary"] [total-take=xxx.xx] [restore-from={TS}] [restore-to={TS}] [total-kv-count=xxx] [total-size=xxx]
```

## 古いデータのクリーンアップ {#clean-up-outdated-data}

[TiDB バックアップと復元の使用概要](/br/br-use-overview.md)で説明したように：

PITR を実行するには、復元ポイントの前に完全バックアップを復元し、完全バックアップ ポイントと復元ポイントの間にログ バックアップを復元する必要があります。したがって、バックアップ保持期間を超えるログ バックアップの場合は、 `br log truncate`を使用して、指定した時点より前のバックアップを削除できます。**完全なスナップショットの前に、ログ バックアップのみを削除することをお勧めします**。

次の手順では、バックアップ保持期間を超えたバックアップ データをクリーンアップする方法について説明します。

1.  バックアップ保持期間外の**最後の完全バックアップ**を取得します。

2.  `validate`コマンドを使用して、バックアップに対応する時点を取得します。 2022/09/01 より前のバックアップ データをクリーンアップする必要があると仮定すると、この時点より前の最後の完全バックアップを探して、クリーンアップされないようにする必要があります。

    ```shell
    FULL_BACKUP_TS=`tiup br validate decode --field="end-version" --storage "s3://backup-101/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}"| tail -n1`
    ```

3.  スナップショット バックアップ`FULL_BACKUP_TS`より前のログ バックアップ データを削除します。

    ```shell
    tiup br log truncate --until=${FULL_BACKUP_TS} --storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}"'
    ```

4.  スナップショット バックアップより前のスナップショット データを削除します`FULL_BACKUP_TS` :

    ```shell
    rm -rf s3://backup-101/snapshot-${date}
    ```

## PITRのパフォーマンスと影響 {#performance-and-impact-of-pitr}

### 機能 {#capabilities}

-   各 TiKV ノードで、PITR は 280 GB/h の速度でスナップショット データを復元し、30 GB/h のログ データを復元できます。
-   BR は、 600 GB/h の速度で古いログ バックアップ データを削除します。

> **ノート：**
>
> 上記の仕様は、次の 2 つのテスト シナリオのテスト結果に基づいています。実際のデータは異なる場合があります。
>
> -   スナップショット データの復元速度 = スナップショット データのサイズ / (期間 * TiKV ノードの数)
> -   ログデータの復元速度 = 復元されたログデータのサイズ / (期間 * TiKV ノードの数)

テスト シナリオ 1 ( [TiDB Cloud](https://tidbcloud.com)で):

-   TiKV ノード数 (8 コア、16 GBメモリ): 21
-   リージョン数: 183,000
-   クラスターで作成された新しいログ データ: 10 GB/h
-   書き込み (INSERT/UPDATE/DELETE) QPS: 10,000

テスト シナリオ 2 (オンプレミス):

-   TiKV ノード数 (8 コア、64 GBメモリ): 6
-   リージョン数: 50,000
-   クラスターで作成された新しいログ データ: 10 GB/h
-   書き込み (INSERT/UPDATE/DELETE) QPS: 10,000

## こちらもご覧ください {#see-also}

-   [TiDB のバックアップと復元の使用例](/br/backup-and-restore-use-cases.md)
-   [br コマンドラインマニュアル](/br/use-br-command-line-tool.md)
-   [ログ バックアップと PITRアーキテクチャ](/br/br-log-architecture.md)
