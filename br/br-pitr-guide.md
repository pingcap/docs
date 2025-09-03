---
title: TiDB Log Backup and PITR Guide
summary: TiDB ログバックアップおよび PITR ガイドでは、br コマンドラインツールを使用してデータをバックアップおよびリストアする方法について説明します。ログバックアップの開始、定期的な完全バックアップの実行、古いデータのクリーンアップの手順も含まれています。また、PITR の実行方法と PITR のパフォーマンス機能に関する情報も提供します。
---

# TiDB ログバックアップと PITR ガイド {#tidb-log-backup-and-pitr-guide}

フルバックアップ（スナップショットバックアップ）には、ある時点のクラスタデータ全体が含まれますが、TiDBログバックアップは、アプリケーションによって書き込まれたデータを指定されたstorageにタイムリーにバックアップできます。必要に応じて復元ポイントを選択、つまりポイントインタイムリカバリ（PITR）を実行したい場合は、 [ログバックアップを開始する](#start-log-backup)と[定期的に完全バックアップを実行する](#run-full-backup-regularly)選択できます。

br コマンドライン ツール (以下、 `br`と呼びます) を使用してデータをバックアップまたは復元する前に、まず[インストール`br`](/br/br-use-overview.md#deploy-and-use-br)行う必要があります。

## TiDBクラスタのバックアップ {#back-up-tidb-cluster}

### ログバックアップを開始する {#start-log-backup}

> **注記：**
>
> -   以下の例では、Amazon S3 アクセスキーとシークレットキーを使用して権限を承認することを前提としています。IAMIAMを使用して権限を承認する場合は、 `--send-credentials-to-tikv`を`false`に設定する必要があります。
> -   他のstorageシステムまたは認証方法を使用して権限を認証する場合は、 [バックアップストレージ](/br/backup-and-restore-storages.md)に従ってパラメータ設定を調整します。

ログ バックアップを開始するには、 `tiup br log start`実行します。クラスターでは、一度に 1 つのログ バックアップ タスクしか実行できません。

```shell
tiup br log start --task-name=pitr --pd "${PD_IP}:2379" \
--storage 's3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}'
```

### ログバックアップのステータスを照会する {#query-the-status-of-the-log-backup}

ログバックアップタスクは開始後、手動で停止するまでTiDBクラスタのバックグラウンドで実行されます。このプロセス中、TiDBの変更ログは指定されたstorageに小さなバッチで定期的にバックアップされます。ログバックアップタスクのステータスを確認するには、次のコマンドを実行します。

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

フィールドの説明は次のとおりです。

-   `name` : ログ バックアップ タスクの名前。
-   `status` : ログ バックアップ タスクのステータス`NORMAL` 、 `PAUSED` 、 `ERROR`を含む)。
-   `start` : ログ バックアップ タスクの開始タイムスタンプ。
-   `end` ：ログバックアップタスクの終了タイムスタンプ。現在、このフィールドは無効です。
-   `storage` : ログ バックアップ用の外部storageの URI。
-   `speed(est.)` : ログバックアップの現在のデータ転送速度。この値は、過去数秒間に取得されたトラフィックサンプルに基づいて推定されます。より正確なトラフィック統計情報については、Grafana の**<a href="/grafana-tikv-dashboard.md#tikv-details-dashboard">TiKV-Details</a>**ダッシュボードの`Log Backup`行目を確認してください。
-   `checkpoint[global]` : ログバックアップの現在の進行状況。PITR を使用すると、このタイムスタンプより前の時点に復元できます。

ログバックアップタスクが一時停止されている場合、 `log status`コマンドは一時停止の詳細を表示するための追加フィールドを出力します。これらのフィールドは以下のとおりです。

-   `pause-time` : 一時停止操作が実行される時刻。
-   `pause-operator` : 一時停止操作を実行するマシンのホスト名。
-   `pause-operator-pid` : 一時停止操作を実行するプロセスの PID。
-   `pause-payload` : タスクが一時停止されているときに付加される追加情報。

一時停止の原因が TiKV のエラーである場合は、TiKV から追加のエラー レポートも表示される場合があります。

-   `error[store=*]` : TiKV のエラー コード。
-   `error-happen-at[store=*]` : TiKV でエラーが発生した時刻。
-   `error-message[store=*]` : TiKV のエラー メッセージ。

### 定期的に完全バックアップを実行する {#run-full-backup-regularly}

スナップショットバックアップは、フルバックアップの方法として使用できます。1 `tiup br backup full`実行すると、固定スケジュール（たとえば2日ごと）に従ってクラスタースナップショットをバックアップstorageにバックアップできます。

```shell
tiup br backup full --pd "${PD_IP}:2379" \
--storage 's3://backup-101/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}'
```

## PITRを実行する {#run-pitr}

バックアップ保持期間内の任意の時点にクラスターを復元するには、 `tiup br restore point`使用します。このコマンドを実行する際は、**復元する時点**、**その時点より前の最新のスナップショットバックアップデータ**、および**ログバックアップデータを**指定する必要があります。BRは復元に必要なデータを自動的に判別して読み取り、これらのデータを指定されたクラスターに順番に復元します。

```shell
tiup br restore point --pd "${PD_IP}:2379" \
--storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}' \
--full-backup-storage='s3://backup-101/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}' \
--restored-ts '2022-05-15 18:00:00+0800'
```

データ復元中は、ターミナルのプログレスバーで進行状況を確認できます。復元は、完全復元とログ復元（メタファイルの復元とKVファイルの復元）の2つのフェーズに分かれています。各フェーズが完了すると、復元時間やデータサイズなどの情報`br`出力されます。

```shell
Full Restore <--------------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
*** ["Full Restore success summary"] ****** [total-take=xxx.xxxs] [restore-data-size(after-compressed)=xxx.xxx] [Size=xxxx] [BackupTS={TS}] [total-kv=xxx] [total-kv-size=xxx] [average-speed=xxx]
Restore Meta Files <--------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
Restore KV Files <----------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
*** ["restore log success summary"] [total-take=xxx.xx] [restore-from={TS}] [restore-to={TS}] [total-kv-count=xxx] [total-size=xxx]
```

## 古いデータをクリーンアップする {#clean-up-outdated-data}

[TiDB バックアップとリストアの使用概要](/br/br-use-overview.md)で説明したとおり:

PITRを実行するには、復元ポイントより前のフルバックアップと、フルバックアップポイントから復元ポイントまでのログバックアップを復元する必要があります。そのため、バックアップ保持期間を超えるログバックアップについては、 `tiup br log truncate`使用して指定時点より前のバックアップを削除できます。**フルスナップショットより前のログバックアップのみを削除することをお勧めします**。

次の手順では、バックアップ保持期間を超えたバックアップ データをクリーンアップする方法について説明します。

1.  バックアップ保持期間外の**最後の完全バックアップ**を取得します。

2.  `validate`コマンドを使用して、バックアップに対応する時点を取得します。2022/09/01 より前のバックアップデータをクリーンアップする必要がある場合、この時点より前の最後の完全バックアップを探し、それがクリーンアップされないことを確認する必要があります。

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
> 上記の仕様は、以下の2つのテストシナリオのテスト結果に基づいています。実際のデータは異なる場合があります。
>
> -   スナップショットデータの復元速度 = クラスター内のすべての TiKV ノードに復元されたスナップショットデータの合計サイズ / (所要時間 * TiKV ノードの数)
> -   ログデータの復元速度 = クラスター内のすべての TiKV ノードに復元されたログデータの合計サイズ / (期間 * TiKV ノードの数)
>
> 外部storageには、単一のレプリカの KV データのみが含まれます。そのため、外部storageのデータ サイズは、クラスターで復元された実際のデータ サイズを表すものではありません。BRは、クラスターに設定されているレプリカの数に応じて、すべてのレプリカを復元します。レプリカの数が多いほど、実際に復元できるデータも多くなります。テストのすべてのクラスターのデフォルトのレプリカ数は 3 です。全体的な復元パフォーマンスを向上させるには、TiKV 設定ファイルの[`import.num-threads`](/tikv-configuration-file.md#import)項目とBRコマンドの[`pitr-concurrency`](/br/br-pitr-manual.md#restore-to-a-specified-point-in-time-pitr)オプションを変更できます。アップストリーム クラスターに**多くのリージョン**があり、**フラッシュ間隔が短い**場合、PITR によって多数の小さなファイルが生成されます。これにより、復元中のバッチ処理とディスパッチのオーバーヘッドが増加します。バッチごとに処理されるファイル数を増やすには、次のパラメーターの値を**適度に**増やすことができます。
>
> -   `pitr-batch-size` :**バッチあたりの累積バイト数**(デフォルト**16 MiB** )。
> -   `pitr-batch-count` :**バッチあたりのファイル数**(デフォルトは**8** )。
>
> 次のバッチを開始するかどうかを決定するときに、これら 2 つのしきい値は独立して評価されます。最初にいずれかのしきい値に達すると、現在のバッチが閉じられ、次のバッチが開始されますが、もう一方のしきい値はそのバッチでは無視されます。

テストシナリオ 1 ( [TiDB Cloud](https://tidbcloud.com)上) は次のとおりです。

-   TiKVノード数（8コア、16GBメモリ）: 21
-   TiKV構成項目`import.num-threads` ：8
-   BRコマンドオプション`pitr-concurrency` :128
-   地域数: 183,000
-   クラスターに作成された新しいログデータ: 10 GB/時
-   書き込み（挿入/更新/削除）QPS: 10,000

テスト シナリオ 2 (TiDB Self-Managed 上) は次のとおりです。

-   TiKVノード数（8コア、64GBメモリ）: 6
-   TiKV構成項目`import.num-threads` ：8
-   BRコマンドオプション`pitr-concurrency` :128
-   リージョン数: 50,000
-   クラスターに作成された新しいログデータ: 10 GB/時
-   書き込み（挿入/更新/削除）QPS: 10,000

## 監視と警告 {#monitoring-and-alert}

ログバックアップタスクが分散されると、各TiKVノードは継続的にデータを外部storageに書き込みます。このプロセスの監視データは**、「TiKV詳細」&gt;「バックアップログ」**ダッシュボードで確認できます。

メトリックが通常の範囲から外れた場合の通知を受信するには、 [ログバックアップアラート](/br/br-monitoring-and-alert.md#log-backup-alerts)参照してアラート ルールを構成してください。

## 参照 {#see-also}

-   [TiDB バックアップとリストアのユースケース](/br/backup-and-restore-use-cases.md)
-   [br コマンドラインマニュアル](/br/use-br-command-line-tool.md)
-   [ログバックアップとPITRアーキテクチャ](/br/br-log-architecture.md)
-   [バックアップと復元の監視とアラート](/br/br-monitoring-and-alert.md)
