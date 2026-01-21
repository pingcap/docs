---
title: TiDB Backup and Restore Use Cases
summary: TiDBは、タイムリーなデータリカバリやビジネス監査など、特定のユースケース向けにスナップショットおよびログバックアップソリューションを提供します。ポイントインタイムリカバリ（PITR）を使用するには、TiDBクラスター（v6.2.0以上）をデプロイし、 BRをTiDBクラスターと同じバージョンに更新してください。Amazon S3にバックアップstorageを設定し、データ損失とリカバリの要件を満たすバックアップポリシーを設定してください。ログバックアップとスナップショットバックアップを実行し、PITRを使用して特定の時点にデータを復元します。古くなったデータは定期的にクリーンアップしてください。詳細な手順については、TiDBのドキュメントをご覧ください。
---

# TiDB バックアップと復元のユースケース {#tidb-backup-and-restore-use-cases}

[TiDB スナップショットのバックアップと復元ガイド](/br/br-snapshot-guide.md)と[TiDB ログバックアップと PITR ガイド](/br/br-pitr-guide.md) 、TiDBが提供するバックアップとリストアのソリューション、すなわちスナップショット（フル）バックアップとリストア、ログバックアップ、そしてポイントインタイムリカバリ（PITR）について紹介します。このドキュメントは、特定のユースケースにおいてTiDBのバックアップとリストアのソリューションを迅速に導入するのに役立ちます。

AWS に TiDB本番クラスターをデプロイし、ビジネスチームが次の要件を要求しているとします。

-   データの変更はタイムリーにバックアップしてください。データベースに災害が発生した場合でも、最小限のデータ損失（許容できるのは数分間のデータ損失のみ）でアプリケーションを迅速に復旧できます。
-   毎月、特定の時間に業務監査を実施します。監査依頼を受けた場合、要求に応じて過去1ヶ月間の特定の時点のデータにクエリを実行するためのデータベースを提供する必要があります。

PITR を使用すると、前述の要件を満たすことができます。

## TiDBクラスタとBRをデプロイ {#deploy-the-tidb-cluster-and-br}

PITRを使用するには、TiDBクラスタ（v6.2.0以上）をデプロイし、 BRをTiDBクラスタと同じバージョンにアップデートする必要があります。このドキュメントでは、例としてv8.5.5を使用しています。

次の表は、TiDB クラスターで PITR を使用するために推奨されるハードウェア リソースを示しています。

| 成分   | CPU   | メモリ     | ディスク | AWSインスタンス | インスタンス数 |
| ---- | ----- | ------- | ---- | --------- | ------- |
| ティドブ | 8コア以上 | 16 GB以上 | SAS  | c5.2特大    | 2       |
| PD   | 8コア以上 | 16 GB以上 | SSD  | c5.2特大    | 3       |
| ティクブ | 8コア以上 | 32 GB以上 | SSD  | m5.2特大    | 3       |
| BR   | 8コア以上 | 16 GB以上 | SAS  | c5.2特大    | 1       |
| モニター | 8コア以上 | 16 GB以上 | SAS  | c5.2特大    | 1       |

> **注記：**
>
> -   BR がバックアップおよび復元タスクを実行する際、PD および TiKV にアクセスする必要があります。BRがすべての PD および TiKV ノードに接続できることを確認してください。
> -   BRと PD サーバーは同じタイムゾーンを使用する必要があります。

TiUPを使用して TiDB クラスターをデプロイまたはアップグレードします。

-   新しい TiDB クラスターをデプロイするには、 [TiDBクラスタをデプロイ](/production-deployment-using-tiup.md)を参照してください。
-   TiDB クラスターが v6.2.0 より前の場合は、 [TiDBクラスタのアップグレード](/upgrade-tidb-using-tiup.md)を参照してアップグレードしてください。

TiUPを使用してBRをインストールまたはアップグレードします。

-   インストール：

    ```shell
    tiup install br:v8.5.5
    ```

-   アップグレード:

    ```shell
    tiup update br:v8.5.5
    ```

## バックアップstorage（Amazon S3）を構成する {#configure-backup-storage-amazon-s3}

バックアップ タスクを開始する前に、次の点を含めてバックアップstorageを準備します。

1.  バックアップデータを保存する S3 バケットとディレクトリを準備します。
2.  S3 バケットにアクセスするための権限を設定します。
3.  各バックアップ データを保存するサブディレクトリを計画します。

詳細な手順は次のとおりです。

1.  バックアップデータを保存するためのディレクトリをS3に作成します。この例ではディレクトリは`s3://tidb-pitr-bucket/backup-data`です。

    1.  バケットを作成します。バックアップデータの保存先として既存のS3を選択できます。S3が存在しない場合は、 [AWSドキュメント: バケットの作成](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)を参照してS3バケットを作成してください。この例では、バケット名は`tidb-pitr-bucket`です。
    2.  バックアップデータ用のディレクトリを作成します。バケット（ `tidb-pitr-bucket` ）内に`backup-data`という名前のディレクトリを作成します。詳細な手順は[AWS ドキュメント: Amazon S3 コンソールでフォルダを使用してオブジェクトを整理する](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html)を参照してください。

2.  BRとTiKVがS3ディレクトリにアクセスするための権限を設定します。S3バケットにアクセスする最も安全な方法であるIAMメソッドを使用して権限を付与することをお勧めします。詳細な手順については、 [AWS ドキュメント: ユーザーポリシーによるバケットへのアクセスの制御](https://docs.aws.amazon.com/AmazonS3/latest/userguide/walkthrough1.html)を参照してください。必要な権限は次のとおりです。

    -   バックアップ クラスター内の TiKV とBRには`s3:GetObject` `s3://tidb-pitr-bucket/backup-data`ディレクトリ`s3:DeleteObject` `s3:ListBucket` 、および`s3:PutObject` `s3:AbortMultipartUpload`権限が必要です。
    -   復元クラスター内の TiKV とBRには、 `s3://tidb-pitr-bucket/backup-data`ディレクトリの`s3:ListBucket`と`s3:GetObject`権限が必要です。

3.  スナップショット (完全) バックアップやログ バックアップなどのバックアップ データを保存するディレクトリ構造を計画します。

    -   すべてのスナップショットバックアップデータは`s3://tidb-pitr-bucket/backup-data/snapshot-${date}`ディレクトリに保存されます。 `${date}`スナップショットバックアップの開始時刻です。例えば、2022/05/12 00:01:30 に開始されたスナップショットバックアップは`s3://tidb-pitr-bucket/backup-data/snapshot-20220512000130`に保存されます。
    -   ログバックアップデータは`s3://tidb-pitr-bucket/backup-data/log-backup/`ディレクトリに保存されます。

## バックアップポリシーを決定する {#determine-the-backup-policy}

最小限のデータ損失、迅速な回復、および 1 か月以内のビジネス監査の要件を満たすには、次のようにバックアップ ポリシーを設定できます。

-   ログ バックアップを実行して、データベース内のデータの変更を継続的にバックアップします。
-   2 日ごとに午前 0 時にスナップショット バックアップを実行します。
-   スナップショット バックアップ データとログ バックアップ データを 30 日以内に保持し、30 日以上経過したバックアップ データをクリーンアップします。

## ログバックアップを実行する {#run-log-backup}

ログバックアップタスクが開始されると、TiKVクラスター内でログバックアッププロセスが実行され、データベース内のデータ変更がS3storageに継続的に送信されます。ログバックアップタスクを開始するには、次のコマンドを実行します。

```shell
tiup br log start --task-name=pitr --pd="${PD_IP}:2379" \
--storage='s3://tidb-pitr-bucket/backup-data/log-backup'
```

ログ バックアップ タスクの実行中に、バックアップ ステータスを照会できます。

```shell
tiup br log status --task-name=pitr --pd="${PD_IP}:2379"

● Total 1 Tasks.
> #1 <
    name: pitr
    status: ● NORMAL
    start: 2022-05-13 11:09:40.7 +0800
      end: 2035-01-01 00:00:00 +0800
    storage: s3://tidb-pitr-bucket/backup-data/log-backup
    speed(est.): 0.00 ops/s
checkpoint[global]: 2022-05-13 11:31:47.2 +0800; gap=4m53s
```

## スナップショットバックアップを実行する {#run-snapshot-backup}

crontabなどの自動ツールを使えば、スナップショットバックアップタスクを定期的に実行できます。例えば、2日ごとに00:00にスナップショットバックアップを実行するなどです。

以下に 2 つのスナップショット バックアップの例を示します。

-   2022/05/14 00:00:00にスナップショットバックアップを実行します

    ```shell
    tiup br backup full --pd="${PD_IP}:2379" \
    --storage='s3://tidb-pitr-bucket/backup-data/snapshot-20220514000000' \
    --backupts='2022/05/14 00:00:00 +08:00'
    ```

-   2022/05/16 00:00:00にスナップショットバックアップを実行します

    ```shell
    tiup br backup full --pd="${PD_IP}:2379" \
    --storage='s3://tidb-pitr-bucket/backup-data/snapshot-20220516000000' \
    --backupts='2022/05/16 00:00:00 +08:00'
    ```

## PITRを実行する {#run-pitr}

2022/05/15 18:00:00 のデータに対してクエリを実行する必要がある場合、PITR を使用することで、2022/05/14 に取得したスナップショットバックアップと、そのスナップショットから 2022/05/15 18:00:00 までのログバックアップデータを復元することで、クラスターをその時点に復元できます。

コマンドは次のとおりです。

```shell
tiup br restore point --pd="${PD_IP}:2379" \
--storage='s3://tidb-pitr-bucket/backup-data/log-backup' \
--full-backup-storage='s3://tidb-pitr-bucket/backup-data/snapshot-20220514000000' \
--restored-ts '2022-05-15 18:00:00+0800'

Split&Scatter Region <--------------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
Download&Ingest SST <--------------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
Restore Pipeline <--------------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
[2022/05/29 18:15:39.132 +08:00] [INFO] [collector.go:69] ["Full Restore success summary"] [total-ranges=12] [ranges-succeed=xxx] [ranges-failed=0] [split-region=xxx.xxxµs] [restore-ranges=xxx] [total-take=xxx.xxxs] [restore-data-size(after-compressed)=xxx.xxx] [Size=xxxx] [BackupTS={TS}] [total-kv=xxx] [total-kv-size=xxx] [average-speed=xxx]
Restore Meta Files <--------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
Restore KV Files <----------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
[2022/05/29 18:15:39.325 +08:00] [INFO] [collector.go:69] ["restore log success summary"] [total-take=xxx.xx] [restore-from={TS}] [restore-to={TS}] [total-kv-count=xxx] [total-size=xxx]
```

## 古いデータをクリーンアップする {#clean-up-outdated-data}

crontab などの自動ツールを使用して、2 日ごとに古いデータをクリーンアップできます。

たとえば、次のコマンドを実行して古いデータをクリーンアップできます。

-   2022/05/14 00:00:00より前のスナップショットデータを削除します

    ```shell
    rm s3://tidb-pitr-bucket/backup-data/snapshot-20220514000000
    ```

-   2022/05/14 00:00:00より前のログバックアップデータを削除します

    ```shell
    tiup br log truncate --until='2022-05-14 00:00:00 +0800' --storage='s3://tidb-pitr-bucket/backup-data/log-backup'
    ```

## 参照 {#see-also}

-   [バックアップストレージ](/br/backup-and-restore-storages.md)
-   [スナップショットのバックアップと復元コマンドマニュアル](/br/br-snapshot-manual.md)
-   [ログバックアップとPITRコマンドマニュアル](/br/br-pitr-manual.md)
