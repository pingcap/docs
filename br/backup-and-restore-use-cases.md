---
title: TiDB Backup and Restore Use Cases
summary: Learn the use cases of backing up and restoring data using br command-line tool.
aliases: ['/tidb/stable/backup-and-restore-use-cases-for-maintain/']
---

# TiDB のバックアップと復元の使用例 {#tidb-backup-and-restore-use-cases}

[TiDB スナップショットのバックアップと復元ガイド](/br/br-snapshot-guide.md)と[TiDB ログのバックアップと PITR ガイド](/br/br-pitr-guide.md) 、TiDB が提供するバックアップと復元のソリューション、つまり、スナップショット (完全) バックアップと復元、ログ バックアップ、およびポイント イン タイム リカバリ (PITR) を紹介します。このドキュメントは、特定のユース ケースで TiDB のバックアップおよび復元ソリューションをすばやく開始するのに役立ちます。

AWS に TiDB本番クラスターをデプロイし、ビジネス チームが次の要件を要求したとします。

-   データの変更をタイムリーにバックアップします。データベースに障害が発生した場合、最小限のデータ損失でアプリケーションを迅速に復旧できます (数分間のデータ損失のみが許容されます)。
-   毎月特定の時間にビジネス監査を実行します。監査要求を受け取ったら、要求に応じて過去 1 か月の特定の時点でデータをクエリするためのデータベースを提供する必要があります。

PITR を使用すると、前述の要件を満たすことができます。

## TiDB クラスターとBRをデプロイ {#deploy-the-tidb-cluster-and-br}

PITR を使用するには、TiDB クラスター &gt;= v6.2.0 をデプロイし、 BR をTiDB クラスターと同じバージョンに更新する必要があります。このドキュメントでは、例として v6.5.2 を使用しています。

次の表は、TiDB クラスターで PITR を使用するために推奨されるハードウェア リソースを示しています。

| 成分   | CPU  | メモリー   | ディスク | AWS インスタンス | インスタンス数 |
| ---- | ---- | ------ | ---- | ---------- | ------- |
| TiDB | 8コア+ | 16GB以上 | SAS  | c5.2xlarge | 2       |
| PD   | 8コア+ | 16GB以上 | SSD  | c5.2xlarge | 3       |
| TiKV | 8コア+ | 32GB以上 | SSD  | m5.2x大     | 3       |
| BR   | 8コア+ | 16GB以上 | SAS  | c5.2xlarge | 1       |
| モニター | 8コア+ | 16GB以上 | SAS  | c5.2xlarge | 1       |

> **ノート：**
>
> -   BR がバックアップおよび復元タスクを実行するとき、PD および TiKV にアクセスする必要があります。 BR がすべての PD および TiKV ノードに接続できることを確認します。
> -   BRと PD サーバーは同じタイム ゾーンを使用する必要があります。

TiUPを使用して TiDB クラスターをデプロイまたはアップグレードします。

-   新しい TiDB クラスターをデプロイするには、 [TiDB クラスターをデプロイ](/production-deployment-using-tiup.md)を参照してください。
-   TiDB クラスターが v6.2.0 より前の場合は、 [TiDB クラスターをアップグレードする](/upgrade-tidb-using-tiup.md)を参照してアップグレードします。

TiUPを使用してBR をインストールまたはアップグレードします。

-   インストール：

    ```shell
    tiup install br:v6.5.2
    ```

-   アップグレード:

    ```shell
    tiup update br:v6.5.2
    ```

## バックアップstorageの構成 (Amazon S3) {#configure-backup-storage-amazon-s3}

バックアップ タスクを開始する前に、次の側面を含むバックアップstorageを準備します。

1.  バックアップデータを格納する S3 バケットとディレクトリを準備します。
2.  S3 バケットにアクセスする権限を設定します。
3.  各バックアップ データを格納するサブディレクトリを計画します。

詳細な手順は次のとおりです。

1.  バックアップデータを保存するディレクトリを S3 に作成します。この例のディレクトリは`s3://tidb-pitr-bucket/backup-data`です。

    1.  バケットを作成します。バックアップ データを保存する既存の S3 を選択できます。無い場合は[AWS ドキュメント: バケットの作成](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)を参照してS3バケットを作成してください。この例では、バケット名は`tidb-pitr-bucket`です。
    2.  バックアップ データ用のディレクトリを作成します。バケット ( `tidb-pitr-bucket` ) で、 `backup-data`という名前のディレクトリを作成します。詳細な手順については、 [AWS ドキュメント: フォルダを使用して Amazon S3 コンソールでオブジェクトを整理する](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html)を参照してください。

2.  S3 ディレクトリにアクセスするためのBRと TiKV のアクセス許可を構成します。 S3 バケットにアクセスする最も安全な方法であるIAMメソッドを使用してアクセス許可を付与することをお勧めします。詳細な手順については、 [AWS ドキュメント: ユーザー ポリシーによるバケットへのアクセスの制御](https://docs.aws.amazon.com/AmazonS3/latest/userguide/walkthrough1.html)を参照してください。必要な権限は次のとおりです。

    -   バックアップ クラスター内の TiKV およびBRには、 `s3://tidb-pitr-bucket/backup-data`ディレクトリの`s3:ListBucket` 、 `s3:PutObject` 、および`s3:AbortMultipartUpload`アクセス許可が必要です。
    -   復元クラスター内の TiKV とBRには、 `s3://tidb-pitr-bucket/backup-data`ディレクトリの`s3:ListBucket`と`s3:GetObject`アクセス許可が必要です。

3.  スナップショット (完全) バックアップとログ バックアップを含む、バックアップ データを格納するディレクトリ構造を計画します。

    -   すべてのスナップショット バックアップ データは、 `s3://tidb-pitr-bucket/backup-data/snapshot-${date}`ディレクトリに格納されます。 `${date}`は、スナップショット バックアップの開始時刻です。たとえば、2022/05/12 00:01:30 から始まるスナップショット バックアップは`s3://tidb-pitr-bucket/backup-data/snapshot-20220512000130`に格納されます。
    -   ログバックアップデータは`s3://tidb-pitr-bucket/backup-data/log-backup/`ディレクトリに格納されます。

## バックアップ ポリシーを決定する {#determine-the-backup-policy}

最小限のデータ損失、迅速な復旧、および 1 か月以内のビジネス監査の要件を満たすために、次のようにバックアップ ポリシーを設定できます。

-   ログ バックアップを実行して、データベースのデータ変更を継続的にバックアップします。
-   スナップショット バックアップを 2 日ごとに 00:00 AM に実行します。
-   スナップショット バックアップ データとログ バックアップ データを 30 日以内に保持し、30 日より古いバックアップ データをクリーンアップします。

## ログのバックアップを実行する {#run-log-backup}

ログ バックアップ タスクが開始されると、TiKV クラスターでログ バックアップ プロセスが実行され、データベース内のデータ変更が S3storageに継続的に送信されます。ログ バックアップ タスクを開始するには、次のコマンドを実行します。

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

## スナップショット バックアップの実行 {#run-snapshot-backup}

crontab などの自動ツールを使用して、定期的にスナップショット バックアップ タスクを実行できます。たとえば、2 日おきに 00:00 にスナップショット バックアップを実行します。

次に、2 つのスナップショット バックアップの例を示します。

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

## PITR を実行する {#run-pitr}

2022/05/15 18:00:00 にデータをクエリする必要があるとします。 PITR を使用して、2022/05/14 に作成されたスナップショット バックアップと、スナップショットと 2022/05/15 18:00:00 の間のログ バックアップ データを復元することで、クラスターをその時点に復元できます。

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

## 古いデータのクリーンアップ {#clean-up-outdated-data}

crontab などの自動ツールを使用して、2 日ごとに古いデータをクリーンアップできます。

たとえば、次のコマンドを実行して古いデータをクリーンアップできます。

-   2022/05/14 00:00:00より前のスナップショットデータを削除

    ```shell
    rm s3://tidb-pitr-bucket/backup-data/snapshot-20220514000000
    ```

-   2022/05/14 00:00:00より前のログバックアップデータを削除

    ```shell
    tiup br log truncate --until='2022-05-14 00:00:00 +0800' --storage='s3://tidb-pitr-bucket/backup-data/log-backup'
    ```

## こちらもご覧ください {#see-also}

-   [バックアップ ストレージ](/br/backup-and-restore-storages.md)
-   [スナップショットのバックアップと復元コマンド マニュアル](/br/br-snapshot-manual.md)
-   [ログのバックアップと PITR コマンド マニュアル](/br/br-pitr-manual.md)
