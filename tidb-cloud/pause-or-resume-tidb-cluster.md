---
title: Pause or Resume a TiDB Cluster
summary: Learn how to pause or resume a TiDB cluster.
---

# TiDB クラスターを一時停止または再開する {#pause-or-resume-a-tidb-cluster}

TiDB Cloudでは、常に稼働していないクラスタを簡単に一時停止および再開できます。

一時停止は、クラスタに保存されているデータには影響しませんが、監視情報の収集とコンピューティング リソースの消費を停止するだけです。一時停止後、いつでもクラスタを再開できます。

バックアップと復元と比較すると、クラスタの一時停止と再開にかかる時間は短く、クラスタの状態情報 (クラスタのバージョン、クラスタ構成、TiDB ユーザー アカウントなど) を保持できます。

> **ノート：**
>
> [開発者層クラスタ](/tidb-cloud/select-cluster-tier.md#developer-tier)を一時停止することはできません。開発者層については[自動ハイバネーションとレジューム](/tidb-cloud/select-cluster-tier.md#automatic-hibernation-and-resuming)を参照してください。

## 制限事項 {#limitations}

-   クラスタが**Normal**状態の場合にのみ、クラスタを一時停止できます。クラスタが<strong>スケーリング</strong>などの他の状態にある場合は、クラスタを一時停止する前に、現在の操作が完了するまで待つ必要があります。
-   データ インポート タスクの実行中は、クラスタを一時停止できません。インポート タスクが完了するのを待つか、インポート タスクをキャンセルすることができます。
-   バックアップ ジョブの実行中は、クラスタを一時停止できません。現在のバックアップ ジョブが完了するまで待つか、または[実行中のバックアップ ジョブを削除する](/tidb-cloud/backup-and-restore.md#delete-a-running-backup-job) .

<!--- - You cannot pause your cluster if it has any [Changefeeds](/tidb-cloud/changefeed-overview.md). You need to delete the existing Changefeeds ([Delete Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md#delete-a-sink) or [Delete Sink to MySQL](/tidb-cloud/changefeed-sink-to-mysql.md#delete-a-sink)) before pausing the cluster. --->

## TiDBクラスタを一時停止する {#pause-a-tidb-cluster}

クラスタが一時停止されている場合は、次の点に注意してください。

-   TiDB Cloudは、クラスタの監視情報の収集を停止します。

-   クラスターからデータを読み取ったり、クラスタにデータを書き込んだりすることはできません。

-   データのインポートまたはバックアップはできません。

-   以下の費用のみ発生します。

    -   ノード ストレージ コスト
    -   データ バックアップのコスト

-   TiDB Cloudは、クラスタの[自動バックアップ](/tidb-cloud/backup-and-restore.md#automatic-backup)を停止します。

クラスタを一時停止するには、次の手順を実行します。

1.  TiDB Cloudコンソールで、プロジェクトの [**クラスター**] ページに移動します。

2.  一時停止するクラスタクラスタの右上隅にある [ **...** ] をクリックします。

    > **ヒント：**
    >
    > または、[**クラスター**] ページで一時停止するクラスタの名前をクリックし、右上隅にある [ <strong>...</strong> ] をクリックすることもできます。

3.  ドロップダウン メニューで [**一時停止**] をクリックします。

    [**クラスタの一時停止**] ダイアログが表示されます。

4.  ダイアログで、[**一時停止**] をクリックして選択を確認します。

TiDB Cloud API を使用してクラスタを一時停止することもできます。現在、 TiDB Cloud API はまだベータ版であり、リクエストがあった場合にのみ利用できます。詳細については、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta)を参照してください。

## TiDBクラスタを再開する {#resume-a-tidb-cluster}

一時停止したクラスタが再開されたら、次の点に注意してください。

-   TiDB Cloudはクラスタの監視情報の収集を再開し、クラスターからデータを読み取ったり、クラスタにデータを書き込んだりできるようになります。
-   TiDB Cloudは、コンピューティングとストレージの両方のコストの請求を再開します。
-   TiDB Cloudが[自動バックアップ](/tidb-cloud/backup-and-restore.md#automatic-backup)のクラスタを再開します。

一時停止したクラスタを再開するには、次の手順を実行します。

1.  TiDB Cloudコンソールで、プロジェクトの [**クラスター**] ページに移動します。

2.  再開するクラスタの [ **Resume** ] をクリックします。

    [**クラスタの再開**] ダイアログが表示されます。

3.  ダイアログで、[**再開**] をクリックして選択を確認します。

クラスターのサイズによっては、クラスタの再開に数分かかる場合がありクラスタ。クラスタが再開されると、クラスタの状態は**Resuming**から<strong>Normal</strong>に変わります。

TiDB Cloud API を使用してクラスタを再開することもできます。現在、 TiDB Cloud API はまだベータ版であり、リクエストがあった場合にのみ利用できます。詳細については、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta)を参照してください。
