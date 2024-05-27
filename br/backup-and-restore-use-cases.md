---
title: TiDB Backup and Restore Use Cases
summary: TiDB は、タイムリーなデータ復旧やビジネス監査などの特定のユースケース向けに、スナップショットおよびログ バックアップ ソリューションを提供します。ポイントインタイム リカバリ (PITR) を使用するには、TiDB クラスター >= v6.2.0 をデプロイし、 BR をTiDB クラスターと同じバージョンに更新します。Amazon S3 でバックアップstorageを構成し、データ損失と復旧の要件を満たすバックアップ ポリシーを設定します。ログとスナップショットのバックアップを実行し、PITR を使用して特定の時点にデータを復元します。古くなったデータを定期的にクリーンアップします。詳細な手順については、TiDB のドキュメントを参照してください。
---

# TiDB バックアップと復元のユースケース {#tidb-backup-and-restore-use-cases}

[TiDB スナップショットのバックアップと復元ガイド](/br/br-snapshot-guide.md)および[TiDB ログ バックアップと PITR ガイド](/br/br-pitr-guide.md)では、TiDB が提供するバックアップおよび復元ソリューション、つまりスナップショット (完全) バックアップと復元、ログ バックアップ、およびポイントインタイム リカバリ (PITR) について説明します。このドキュメントは、特定のユース ケースで TiDB のバックアップおよび復元ソリューションをすぐに開始するのに役立ちます。

AWS に TiDB本番クラスターをデプロイし、ビジネスチームが次の要件を要求しているとします。

-   データの変更をタイムリーにバックアップします。データベースに障害が発生した場合、最小限のデータ損失でアプリケーションを迅速に回復できます (許容できるデータ損失は数分のみ)。
-   毎月、特定の時間に業務監査を実行します。監査リクエストを受け取ったら、要求に応じて過去 1 か月の特定の時点のデータを照会するためのデータベースを提供する必要があります。

PITR を使用すると、前述の要件を満たすことができます。

## TiDBクラスタとBRをデプロイ {#deploy-the-tidb-cluster-and-br}

PITR を使用するには、TiDB クラスター &gt;= v6.2.0 をデプロイし、 BR をTiDB クラスターと同じバージョンに更新する必要があります。このドキュメントでは、例として v8.1.0 を使用します。

次の表は、TiDB クラスターで PITR を使用するために推奨されるハードウェア リソースを示しています。

| 成分   | CPU   | メモリ    | ディスク         | AWSインスタンス | インスタンス数 |
| ---- | ----- | ------ | ------------ | --------- | ------- |
| ティビ  | 8コア以上 | 16GB以上 | スカンジナビア航空    | c5.2特大    | 2       |
| PD   | 8コア以上 | 16GB以上 | ソリッドステートドライブ | c5.2特大    | 3       |
| ティクヴ | 8コア以上 | 32GB以上 | ソリッドステートドライブ | m5.2xラージ  | 3       |
| BR   | 8コア以上 | 16GB以上 | スカンジナビア航空    | c5.2特大    | 1       |
| モニター | 8コア以上 | 16GB以上 | スカンジナビア航空    | c5.2特大    | 1       |

> **注記：**
>
> -   BR がバックアップおよび復元タスクを実行する場合、PD および TiKV にアクセスする必要があります。BRがすべての PD および TiKV ノードに接続できることを確認してください。
> -   BRサーバーと PD サーバーは同じタイムゾーンを使用する必要があります。

TiUPを使用して TiDB クラスターをデプロイまたはアップグレードします。

-   新しい TiDB クラスターをデプロイするには、 [TiDBクラスタをデプロイ](/production-deployment-using-tiup.md)を参照してください。
-   TiDB クラスターが v6.2.0 より前の場合は、 [TiDB クラスターのアップグレード](/upgrade-tidb-using-tiup.md)を参照してアップグレードしてください。

TiUPを使用してBR をインストールまたはアップグレードします。

-   インストール：

    ```shell
    tiup install br:v8.1.0
    ```

-   アップグレード:

    ```shell
    tiup update br:v8.1.0
    ```

## バックアップstorageを構成する (Amazon S3) {#configure-backup-storage-amazon-s3}

バックアップ タスクを開始する前に、次の点を含めてバックアップstorageを準備します。

1.  バックアップデータを保存する S3 バケットとディレクトリを準備します。
2.  S3 バケットにアクセスするための権限を設定します。
3.  各バックアップデータを保存するサブディレクトリを計画します。

詳細な手順は次のとおりです。

1.  バックアップ データを保存するためのディレクトリを S3 に作成します。この例のディレクトリは`s3://tidb-pitr-bucket/backup-data`です。

    1.  バケットを作成します。バックアップデータを保存する既存の S3 を選択できます。存在しない場合は、 [AWS ドキュメント: バケットの作成](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)を参照して S3 バケットを作成します。この例では、バケット名は`tidb-pitr-bucket`です。
    2.  バックアップデータ用のディレクトリを作成します。バケット（ `tidb-pitr-bucket` ）に`backup-data`という名前のディレクトリを作成します。詳細な手順については、 [AWS ドキュメント: フォルダーを使用して Amazon S3 コンソールでオブジェクトを整理する](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html)を参照してください。

2.  BRと TiKV が S3 ディレクトリにアクセスするための権限を設定します。S3 バケットにアクセスする最も安全な方法であるIAMメソッドを使用して権限を付与することをお勧めします。詳細な手順については、 [AWS ドキュメント: ユーザーポリシーによるバケットへのアクセスの制御](https://docs.aws.amazon.com/AmazonS3/latest/userguide/walkthrough1.html)を参照してください。必要な権限は次のとおりです。

    -   バックアップ クラスター内の TiKV とBRに`s3://tidb-pitr-bucket/backup-data` `s3:GetObject` `s3:DeleteObject` `s3:ListBucket` 、および`s3:AbortMultipartUpload`権限`s3:PutObject`必要です。
    -   復元クラスター内の TiKV とBRには、 `s3://tidb-pitr-bucket/backup-data`ディレクトリの`s3:ListBucket` 、 `s3:GetObject` 、 `s3:DeleteObject` 、および`s3:PutObject`権限が必要です。

3.  スナップショット (完全) バックアップやログ バックアップなどのバックアップ データを保存するディレクトリ構造を計画します。

    -   すべてのスナップショットバックアップデータは`s3://tidb-pitr-bucket/backup-data/snapshot-${date}`ディレクトリに保存されます。 `${date}`スナップショットバックアップの開始時刻です。たとえば、2022/05/12 00:01:30 に開始するスナップショットバックアップは`s3://tidb-pitr-bucket/backup-data/snapshot-20220512000130`に保存されます。
    -   ログバックアップデータは`s3://tidb-pitr-bucket/backup-data/log-backup/`ディレクトリに保存されます。

## バックアップポリシーを決定する {#determine-the-backup-policy}

最小限のデータ損失、迅速な回復、および 1 か月以内のビジネス監査の要件を満たすには、次のようにバックアップ ポリシーを設定できます。

-   ログ バックアップを実行して、データベース内のデータの変更を継続的にバックアップします。
-   2 日ごとに午前 00:00 にスナップショット バックアップを実行します。
-   スナップショット バックアップ データとログ バックアップ データを 30 日以内に保持し、30 日以上経過したバックアップ データをクリーンアップします。

## ログバックアップを実行する {#run-log-backup}

ログ バックアップ タスクが開始されると、TiKV クラスターでログ バックアップ プロセスが実行され、データベースのデータ変更が S3storageに継続的に送信されます。ログ バックアップ タスクを開始するには、次のコマンドを実行します。

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

crontab などの自動ツールを使用して、スナップショット バックアップ タスクを定期的に実行できます。たとえば、2 日ごとに 00:00 にスナップショット バックアップを実行します。

以下に 2 つのスナップショット バックアップの例を示します。

-   2022/05/14 00:00:00にスナップショットバックアップを実行します

    ```shell
    tiup br backup full --pd="${PD_IP}:2379" \
    --storage='s3://tidb-pitr-bucket/backup-data/snapshot-20220514000000' \
    --backupts='2022/05/14 00:00:00'
    ```

-   2022/05/16 00:00:00にスナップショットバックアップを実行します

    ```shell
    tiup br backup full --pd="${PD_IP}:2379" \
    --storage='s3://tidb-pitr-bucket/backup-data/snapshot-20220516000000' \
    --backupts='2022/05/16 00:00:00'
    ```

## PITRを実行する {#run-pitr}

2022/05/15 18:00:00 のデータをクエリする必要があるとします。PITR を使用して、2022/05/14 に作成されたスナップショット バックアップと、スナップショットから 2022/05/15 18:00:00 までのログ バックアップ データを復元することで、クラスターをその時点に復元できます。

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

crontab などの自動ツールを使用して、2 日ごとに古いデータをクリーンアップできます。

たとえば、次のコマンドを実行して、古いデータをクリーンアップできます。

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
-   [スナップショットのバックアップと復元のコマンドマニュアル](/br/br-snapshot-manual.md)
-   [ログバックアップとPITRコマンドマニュアル](/br/br-pitr-manual.md)
