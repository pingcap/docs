---
title: Pause or Resume a TiDB Cluster
summary: Learn how to pause or resume a TiDB cluster.
---

# TiDBクラスタの一時停止または再開 {#pause-or-resume-a-tidb-cluster}

TiDB Cloudでは、常に動作していないクラスターを簡単に一時停止および再開できます。

一時停止はクラスターに保存されているデータには影響しませんが、監視情報の収集とコンピューティング リソースの消費が停止するだけです。一時停止後、いつでもクラスターを再開できます。

バックアップや復元と比較すると、クラスターの一時停止と再開にかかる時間は短くなり、クラスターの状態情報 (クラスターのバージョン、クラスター構成、TiDB ユーザー アカウントなど) が保持されます。

> **ノート：**
>
> [<a href="/tidb-cloud/select-cluster-tier.md#serverless-tier-beta">Serverless Tierクラスター</a>](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)を一時停止することはできません。

## 制限事項 {#limitations}

-   クラスターが**AVAILABLE**状態にある場合にのみ、クラスターを一時停止できます。クラスターが**MODIFYING**などの他の状態にある場合は、クラスターを一時停止する前に、現在の操作が完了するまで待つ必要があります。
-   データ インポート タスクの実行中はクラスターを一時停止できません。インポート タスクが完了するまで待つか、インポート タスクをキャンセルすることができます。
-   バックアップ ジョブの実行中はクラスターを一時停止できません。現在のバックアップ ジョブが完了するまで待つか、 [<a href="/tidb-cloud/backup-and-restore.md#delete-a-running-backup-job">実行中のバックアップ ジョブを削除する</a>](/tidb-cloud/backup-and-restore.md#delete-a-running-backup-job)を待つことができます。
-   クラスターに[<a href="/tidb-cloud/changefeed-overview.md">変更フィード</a>](/tidb-cloud/changefeed-overview.md)がある場合、クラスターを一時停止することはできません。クラスターを一時停止する前に[<a href="/tidb-cloud/changefeed-overview.md#delete-a-changefeed">既存の変更フィードを削除します</a>](/tidb-cloud/changefeed-overview.md#delete-a-changefeed)を行う必要があります。

## TiDB クラスターを一時停止する {#pause-a-tidb-cluster}

クラスターが一時停止されている場合は、次の点に注意してください。

-   TiDB Cloud はクラスターの監視情報の収集を停止します。

-   クラスターからデータを読み取ったり、クラスターにデータを書き込んだりすることはできません。

-   データのインポートやバックアップはできません。

-   以下の費用のみご負担いただきます。

    -   ノードのストレージコスト
    -   データバックアップコスト

-   TiDB Cloud はクラスターの[<a href="/tidb-cloud/backup-and-restore.md#automatic-backup">自動バックアップ</a>](/tidb-cloud/backup-and-restore.md#automatic-backup)を停止します。

クラスターを一時停止するには、次の手順を実行します。

1.  TiDB Cloudコンソールで、プロジェクトの[<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動します。

2.  一時停止するクラスターの行で**[...]**をクリックします。

    > **ヒント：**
    >
    > あるいは、 **「クラスター」**ページで一時停止するクラスターの名前をクリックし、右上隅にある**「...」**をクリックすることもできます。

3.  ドロップダウン メニューで**[一時停止]**をクリックします。

    **[クラスターを一時停止]**ダイアログが表示されます。

4.  ダイアログで、 **「一時停止」**をクリックして選択を確認します。

TiDB Cloud API を使用してクラスターを一時停止することもできます。現在、 TiDB Cloud API はまだベータ版です。詳細については、 [<a href="https://docs.pingcap.com/tidbcloud/api/v1beta">TiDB CloudAPI ドキュメント</a>](https://docs.pingcap.com/tidbcloud/api/v1beta)を参照してください。

## TiDB クラスターを再開する {#resume-a-tidb-cluster}

一時停止したクラスターが再開された後は、次の点に注意してください。

-   TiDB Cloudはクラスターの監視情報の収集を再開し、クラスターからのデータの読み取りまたはクラスターへのデータの書き込みが可能になります。
-   TiDB Cloud は、コンピューティングとstorageの両方のコストの請求を再開します。
-   TiDB Cloud はクラスターの[<a href="/tidb-cloud/backup-and-restore.md#automatic-backup">自動バックアップ</a>](/tidb-cloud/backup-and-restore.md#automatic-backup)を再開します。

一時停止したクラスターを再開するには、次の手順を実行します。

1.  TiDB Cloudコンソールで、プロジェクトの[<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動します。

2.  再開するクラスターについては、 **「再開」を**クリックします。

    **[クラスターを再開]**ダイアログが表示されます。

3.  ダイアログで、 **「再開」**をクリックして選択を確認します。クラスターのステータスが**RESUMING**になります。

クラスターのサイズによっては、クラスターの再開に数分かかる場合があります。クラスターが再開されると、クラスターの状態は**RESUMING**から**AVAILABLE**に変わります。

TiDB Cloud API を使用してクラスターを再開することもできます。現在、 TiDB Cloud API はまだベータ版です。詳細については、 [<a href="https://docs.pingcap.com/tidbcloud/api/v1beta">TiDB CloudAPI ドキュメント</a>](https://docs.pingcap.com/tidbcloud/api/v1beta)を参照してください。
