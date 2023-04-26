---
title: Pause or Resume a TiDB Cluster
summary: Learn how to pause or resume a TiDB cluster.
---

# TiDBクラスタを一時停止または再開する {#pause-or-resume-a-tidb-cluster}

TiDB Cloudでは、常に稼働していないクラスターを簡単に一時停止および再開できます。

一時停止は、クラスターに保存されているデータには影響しませんが、監視情報の収集とコンピューティング リソースの消費を停止するだけです。一時停止後、いつでもクラスターを再開できます。

バックアップと復元と比較して、クラスターの一時停止と再開にかかる時間は短く、クラスターの状態情報 (クラスターのバージョン、クラスター構成、TiDB ユーザー アカウントなど) を保持します。

> **ノート：**
>
> [Serverless Tierクラスター](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)を一時停止することはできません。

## 制限事項 {#limitations}

-   クラスターが**AVAILABLE**状態の場合にのみ一時停止できます。クラスターが<strong>MODIFYING</strong>などの他の状態にある場合は、クラスターを一時停止する前に、現在の操作が完了するまで待機する必要があります。
-   データ インポート タスクの実行中は、クラスターを一時停止できません。インポート タスクが完了するのを待つか、インポート タスクをキャンセルすることができます。
-   バックアップ ジョブの実行中は、クラスターを一時停止できません。現在のバックアップ ジョブが完了するまで待つか、または[実行中のバックアップ ジョブを削除する](/tidb-cloud/backup-and-restore.md#delete-a-running-backup-job) .
-   クラスターに[チェンジフィード](/tidb-cloud/changefeed-overview.md)がある場合、クラスターを一時停止することはできません。クラスターを一時停止する前に[既存の変更フィードを削除します](/tidb-cloud/changefeed-overview.md#delete-a-changefeed)が必要です。

## TiDB クラスターを一時停止する {#pause-a-tidb-cluster}

クラスターが一時停止されている場合は、次の点に注意してください。

-   TiDB Cloud がクラスターの監視情報の収集を停止します。

-   クラスターからデータを読み取ったり、クラスターにデータを書き込んだりすることはできません。

-   データのインポートまたはバックアップはできません。

-   以下の費用のみ発生します。

    -   ノード ストレージ コスト
    -   データ バックアップのコスト

-   TiDB Cloud はクラスターの[自動バックアップ](/tidb-cloud/backup-and-restore.md#automatic-backup)を停止します。

クラスターを一時停止するには、次の手順を実行します。

1.  TiDB Cloudコンソールで、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

2.  一時停止するクラスターの行で、 **[...]**をクリックします。

    > **ヒント：**
    >
    > または、 **[クラスター]**ページで一時停止するクラスターの名前をクリックし、右上隅にある<strong>[...]</strong>をクリックすることもできます。

3.  ドロップダウン メニューで**[一時停止]**をクリックします。

    **[クラスターの一時停止]**ダイアログが表示されます。

4.  ダイアログで、 **[一時停止]**をクリックして選択を確認します。

TiDB Cloud API を使用してクラスターを一時停止することもできます。現在、 TiDB Cloud API はまだベータ版です。詳細については、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta)を参照してください。

## TiDB クラスターを再開する {#resume-a-tidb-cluster}

一時停止したクラスターが再開されたら、次の点に注意してください。

-   TiDB Cloud がクラスターの監視情報の収集を再開し、クラスターからデータを読み書きできるようになります。
-   TiDB Cloud は、コンピューティングとstorageの両方のコストの請求を再開します。
-   TiDB Cloud がクラスターの[自動バックアップ](/tidb-cloud/backup-and-restore.md#automatic-backup)を再開します。

一時停止したクラスターを再開するには、次の手順を実行します。

1.  TiDB Cloudコンソールで、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

2.  再開するクラスターの**[Resume]**をクリックします。

    **[クラスターの再開]**ダイアログが表示されます。

3.  ダイアログで、 **[再開]**をクリックして選択を確認します。クラスターのステータスは<strong>RESUMING</strong>になります。

クラスターのサイズによっては、クラスターの再開に数分かかる場合があります。クラスターが再開されると、クラスターの状態は**RESUMING**から<strong>AVAILABLE</strong>に変わります。

TiDB Cloud API を使用してクラスターを再開することもできます。現在、 TiDB Cloud API はまだベータ版です。詳細については、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta)を参照してください。
