---
title: TiDB Backup and Restore Use Cases
summary: Learn the use cases of backing up and restoring data using br command-line tool.
---

# TiDB のバックアップと復元の使用例 {#tidb-backup-and-restore-use-cases}

[TiDB スナップショットのバックアップおよび復元ガイド](/br/br-snapshot-guide.md)および[TiDB ログのバックアップと PITR ガイド](/br/br-pitr-guide.md) 、TiDB が提供するバックアップおよび復元ソリューション、つまりスナップショット (フル) バックアップおよび復元、ログ バックアップ、およびポイントインタイム リカバリ (PITR) を紹介します。このドキュメントは、特定の使用例で TiDB のバックアップおよび復元ソリューションをすぐに使い始めるのに役立ちます。

TiDB本番クラスターを AWS にデプロイしており、ビジネス チームが次の要件を要求していると仮定します。

-   データの変更をタイムリーにバックアップします。データベースに障害が発生した場合、データ損失を最小限に抑えてアプリケーションを迅速に回復できます (データ損失は数分間のみ許容されます)。
-   毎月、特定の時期に業務監査を実行します。監査リクエストを受信した場合、リクエストに応じて過去 1 か月の特定の時点のデータをクエリするためのデータベースを提供する必要があります。

PITR を使用すると、前述の要件を満たすことができます。

## TiDB クラスターとBRをデプロイ {#deploy-the-tidb-cluster-and-br}

PITR を使用するには、TiDB クラスター &gt;= v6.2.0 をデプロイし、 BR をTiDB クラスターと同じバージョンに更新する必要があります。このドキュメントでは例として v7.1.2 を使用します。

次の表は、TiDB クラスターで PITR を使用する場合に推奨されるハードウェア リソースを示しています。

| 成分   | CPU   | メモリ    | ディスク | AWSインスタンス  | インスタンスの数 |
| ---- | ----- | ------ | ---- | ---------- | -------- |
| TiDB | 8コア以上 | 16GB以上 | SAS  | c5.2xlarge | 2        |
| PD   | 8コア以上 | 16GB以上 | SSD  | c5.2xlarge | 3        |
| TiKV | 8コア以上 | 32GB以上 | SSD  | m5.2x大     | 3        |
| BR   | 8コア以上 | 16GB以上 | SAS  | c5.2xlarge | 1        |
| モニター | 8コア以上 | 16GB以上 | SAS  | c5.2xlarge | 1        |

> **注記：**
>
> -   BR がバックアップおよび復元タスクを実行するときは、PD および TiKV にアクセスする必要があります。 BR がすべての PD および TiKV ノードに接続できることを確認してください。
> -   BRと PD サーバーは同じタイムゾーンを使用する必要があります。

TiUPを使用して TiDB クラスターをデプロイまたはアップグレードします。

-   新しい TiDB クラスターをデプロイするには、 [TiDB クラスターをデプロイ](/production-deployment-using-tiup.md)を参照してください。
-   TiDB クラスターが v6.2.0 より前の場合は、 [TiDB クラスターをアップグレードする](/upgrade-tidb-using-tiup.md)を参照してアップグレードします。

TiUPを使用してBR をインストールまたはアップグレードします。

-   インストール：

    ```shell
    tiup install br:v7.1.2
    ```

-   アップグレード:

    ```shell
    tiup update br:v7.1.2
    ```

## バックアップstorageの構成 (Amazon S3) {#configure-backup-storage-amazon-s3}

バックアップ タスクを開始する前に、次の点を含めてバックアップstorageを準備します。

1.  バックアップデータを格納するS3バケットとディレクトリを準備します。
2.  S3 バケットにアクセスするための権限を構成します。
3.  各バックアップ データを保存するサブディレクトリを計画します。

詳細な手順は次のとおりです。

1.  S3にバックアップデータを保存するディレクトリを作成します。この例のディレクトリは`s3://tidb-pitr-bucket/backup-data`です。

    1.  バケットを作成します。バックアップ データを保存するために既存の S3 を選択できます。存在しない場合は、 [AWS ドキュメント: バケットの作成](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)を参照してS3バケットを作成してください。この例では、バケット名は`tidb-pitr-bucket`です。
    2.  バックアップ データ用のディレクトリを作成します。バケット ( `tidb-pitr-bucket` ) に、 `backup-data`という名前のディレクトリを作成します。詳細な手順については、 [AWS ドキュメント: フォルダーを使用した Amazon S3 コンソール内のオブジェクトの整理](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html)を参照してください。

2.  BRおよび TiKV が S3 ディレクトリにアクセスするための権限を設定します。 S3 バケットにアクセスする最も安全な方法であるIAMメソッドを使用して権限を付与することをお勧めします。詳細な手順については、 [AWS ドキュメント: ユーザー ポリシーによるバケットへのアクセスの制御](https://docs.aws.amazon.com/AmazonS3/latest/userguide/walkthrough1.html)を参照してください。必要な権限は次のとおりです。

    -   バックアップ クラスター内の TiKV とBRには、 `s3://tidb-pitr-bucket/backup-data`ディレクトリの`s3:ListBucket` 、 `s3:PutObject` 、および`s3:AbortMultipartUpload`アクセス許可が必要です。
    -   復元クラスター内の TiKV とBRには、 `s3://tidb-pitr-bucket/backup-data`ディレクトリの`s3:ListBucket` 、 `s3:GetObject` 、および`s3:PutObject`アクセス許可が必要です。

3.  スナップショット (フル) バックアップやログ バックアップなどのバックアップ データを保存するディレクトリ構造を計画します。

    -   すべてのスナップショット バックアップ データは`s3://tidb-pitr-bucket/backup-data/snapshot-${date}`ディレクトリに保存されます。 `${date}`はスナップショット バックアップの開始時刻です。たとえば、2022/05/12 00:01:30 から始まるスナップショット バックアップは`s3://tidb-pitr-bucket/backup-data/snapshot-20220512000130`に保存されます。
    -   ログのバックアップデータは`s3://tidb-pitr-bucket/backup-data/log-backup/`ディレクトリに保存されます。

## バックアップポリシーを決定する {#determine-the-backup-policy}

データ損失の最小化、迅速なリカバリ、および 1 か月以内のビジネス監査の要件を満たすために、次のようにバックアップ ポリシーを設定できます。

-   ログ バックアップを実行して、データベース内のデータ変更を継続的にバックアップします。
-   スナップショット バックアップを 2 日ごとの午前 00:00 に実行します。
-   スナップショット バックアップ データとログ バックアップ データは 30 日以内に保持し、30 日より古いバックアップ データはクリーンアップします。

## ログバックアップを実行する {#run-log-backup}

ログ バックアップ タスクが開始されると、ログ バックアップ プロセスが TiKV クラスター内で実行され、データベース内のデータ変更が S3storageに継続的に送信されます。ログ バックアップ タスクを開始するには、次のコマンドを実行します。

```shell
tiup br log start --task-name=pitr --pd="${PD_IP}:2379" \
--storage='s3://tidb-pitr-bucket/backup-data/log-backup'
```

ログ バックアップ タスクの実行中に、バックアップ ステータスをクエリできます。

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

crontab などの自動ツールを使用して、スナップショット バックアップ タスクを定期的に実行できます。たとえば、スナップショット バックアップを 2 日ごとの 00:00 に実行します。

次に、スナップショット バックアップの 2 つの例を示します。

-   2022/05/14 00:00:00 にスナップショット バックアップを実行します。

    ```shell
    tiup br backup full --pd="${PD_IP}:2379" \
    --storage='s3://tidb-pitr-bucket/backup-data/snapshot-20220514000000' \
    --backupts='2022/05/14 00:00:00'
    ```

-   2022/05/16 00:00:00 にスナップショット バックアップを実行します。

    ```shell
    tiup br backup full --pd="${PD_IP}:2379" \
    --storage='s3://tidb-pitr-bucket/backup-data/snapshot-20220516000000' \
    --backupts='2022/05/16 00:00:00'
    ```

## PITRを実行する {#run-pitr}

2022/05/15 18:00:00 にデータをクエリする必要があると仮定します。 PITR を使用して、2022/05/14 に作成されたスナップショット バックアップと、スナップショットと 2022/05/15 18:00:00 の間のログ バックアップ データを復元することで、クラスターをその時点に復元できます。

コマンドは次のとおりです。

```shell
tiup br restore point --pd="${PD_IP}:2379" \
--storage='s3://tidb-pitr-bucket/backup-data/log-backup' \
--full-backup-storage='s3://tidb-pitr-bucket/backup-data/snapshot-20220514000000' \
--restored-ts '2022-05-15 18:00:00+0800'

Full Restore <--------------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
[2022/05/29 18:15:39.132 +08:00] [INFO] [collector.go:69] ["Full Restore success summary"] [total-ranges=12] [ranges-succeed=xxx] [ranges-failed=0] [split-region=xxx.xxxµs] [restore-ranges=xxx] [total-take=xxx.xxxs] [restore-data-size(after-compressed)=xxx.xxx] [Size=xxxx] [BackupTS={TS}] [total-kv=xxx] [total-kv-size=xxx] [average-speed=xxx]
Restore Meta Files <--------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
Restore KV Files <----------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
[2022/05/29 18:15:39.325 +08:00] [INFO] [collector.go:69] ["restore log success summary"] [total-take=xxx.xx] [restore-from={TS}] [restore-to={TS}] [total-kv-count=xxx] [total-size=xxx]
```

## 古いデータをクリーンアップする {#clean-up-outdated-data}

crontab などの自動ツールを使用して、古いデータを 2 日ごとにクリーンアップできます。

たとえば、次のコマンドを実行して古いデータをクリーンアップできます。

-   2022/05/14 00:00:00より前のスナップショットデータを削除します

    ```shell
    rm s3://tidb-pitr-bucket/backup-data/snapshot-20220514000000
    ```

-   2022/05/14 00:00:00より前のログバックアップデータを削除します

    ```shell
    tiup br log truncate --until='2022-05-14 00:00:00 +0800' --storage='s3://tidb-pitr-bucket/backup-data/log-backup'
    ```

## こちらも参照 {#see-also}

-   [バックアップストレージ](/br/backup-and-restore-storages.md)
-   [スナップショットバックアップおよびリストアコマンドマニュアル](/br/br-snapshot-manual.md)
-   [ログバックアップとPITRコマンドマニュアル](/br/br-pitr-manual.md)
