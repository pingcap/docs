---
title: Changefeed (Beta)
summary: TiDB Cloudチェンジフィードは、 TiDB Cloudから他のデータ サービスにデータをストリーミングするのに役立ちます。
---

# チェンジフィード（ベータ版） {#changefeed-beta}

TiDB Cloud changefeed は、TiDB Cloudから他のデータサービスへのデータストリーミングに役立ちます。現在、 TiDB Cloud はApache Kafka と MySQL へのデータストリーミングをサポートしています。

> **注記：**
>
> -   現在、 TiDB Cloud、 TiDB Cloud Essential クラスターごとに最大 10 個の変更フィードのみが許可されます。
> -   [TiDB Cloudスターター](/tidb-cloud/select-cluster-tier.md#starter)クラスターでは、changefeed 機能は使用できません。

## 制限 {#restrictions}

-   Changefeed は、1 つの`RENAME TABLE`ステートメント（例: `RENAME TABLE t1 TO t3, t2 TO t4` ）で複数のテーブルの名前を変更する DDL ステートメントをサポートしていません。このステートメントを実行すると、Changefeed データのレプリケーションが永続的に中断されます。
-   チェンジフィードのスループットは約20 MiB/秒です。増分データ量がこの制限を超える場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

## サポートされている地域 {#supported-regions}

changefeed 機能は次のリージョンで利用できます。

| クラウドプロバイダー | サポートされている地域                                                                                                                           |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| AWS        | <li>`ap-east-1`</li><li>`ap-northeast-1`</li><li>`ap-southeast-1`</li><li>`eu-central-1`</li><li>`us-east-1`</li><li>`us-west-2`</li> |
| アリババクラウド   | <li>`ap-southeast-1`</li><li>`ap-southeast-5`</li><li>`cn-hongkong`</li>                                                              |

今後、他の地域でもサポートされる予定です。特定の地域での緊急サポートについては、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

## Changefeedページをビュー {#view-the-changefeed-page}

changefeed 機能にアクセスするには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲットクラスターの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「データ」** &gt; **「Changefeed」**をクリックします。Changefeedページが表示されます。

**「Changefeed」**ページでは、変更フィードを作成したり、既存の変更フィードの一覧を表示したり、既存の変更フィードを操作したり (変更フィードの一時停止、再開、編集、削除など) できます。

## チェンジフィードを作成する {#create-a-changefeed}

チェンジフィードを作成するには、チュートリアルを参照してください。

-   [Apache Kafka にシンクする](/tidb-cloud/essential-changefeed-sink-to-kafka.md)
-   [MySQLに沈む](/tidb-cloud/essential-changefeed-sink-to-mysql.md)

## チェンジフィードをビュー {#view-a-changefeed}

TiDB CloudコンソールまたはTiDB Cloud CLI を使用して変更フィードを表示できます。

<SimpleTab>
<div label="Console">

1.  ターゲット TiDB クラスターの[**チェンジフィード**](#view-the-changefeed-page)ページに移動します。
2.  表示する対応する変更フィードを見つけて、 **[アクション]**列の**[...]** &gt; **[ビュー]**をクリックします。
3.  構成、ステータス、メトリックなど、変更フィードの詳細を確認できます。

</div>

<div label="CLI">

次のコマンドを実行します。

```bash
ticloud serverless changefeed get --cluster-id <cluster-id> --changefeed-id <changefeed-id>
```

</div>
</SimpleTab>

## チェンジフィードを一時停止または再開する {#pause-or-resume-a-changefeed}

TiDB CloudコンソールまたはTiDB Cloud CLI を使用して、変更フィードを一時停止または再開できます。

<SimpleTab>
<div label="Console">

1.  ターゲット TiDB クラスターの[**チェンジフィード**](#view-the-changefeed-page)ページに移動します。
2.  一時停止または再開する対応する変更フィードを見つけて、 **[アクション]**列の**[...]** &gt; **[一時停止/再開]**をクリックします。

</div>

<div label="CLI">

変更フィードを一時停止するには、次のコマンドを実行します。

```bash
ticloud serverless changefeed pause --cluster-id <cluster-id> --changefeed-id <changefeed-id>
```

チェンジフィードを再開するには:

    ticloud serverless changefeed resume -c <cluster-id> --changefeed-id <changefeed-id>

</div>
</SimpleTab>

## 変更フィードを編集する {#edit-a-changefeed}

> **注記：**
>
> TiDB Cloud現在、一時停止状態の変更フィードのみ編集できます。

TiDB CloudコンソールまたはTiDB Cloud CLI を使用して、変更フィードを編集できます。

<SimpleTab>
<div label="Console">

1.  ターゲット TiDB クラスターの[**チェンジフィード**](#view-the-changefeed-page)ページに移動します。

2.  一時停止する変更フィードを見つけて、 **[アクション]**列の**[...]** &gt; **[一時停止]**をクリックします。

3.  changefeed のステータスが`Paused`に変更されたら、 **[...]** &gt; **[編集]**をクリックして、対応する changefeed を編集します。

    TiDB Cloud はデフォルトで changefeed 設定を設定します。以下の設定を変更できます。

    -   Apache Kafka シンク: **Destination** 、 **Connection** 、 **Start Position**を除くすべての構成
    -   MySQLシンク:**宛先**、**接続**、**開始位置**を除くすべての構成

4.  設定を編集した後、 **[...]** &gt; **[再開]**をクリックして、対応する変更フィードを再開します。

</div>

<div label="CLI">

Apache Kafka シンクを使用して変更フィードを編集します。

```bash
ticloud serverless changefeed edit --cluster-id <cluster-id> --changefeed-id <changefeed-id> --name <new-displayName> --kafka <full-specified-kafka> --filter <full-specified-filter>
```

MySQL シンクを使用して変更フィードを編集します。

```bash
ticloud serverless changefeed edit --cluster-id <cluster-id> --changefeed-id <changefeed-id> --name <new-displayName> --mysql <full-specified-mysql> --filter <full-specified-filter>
```

</div>
</SimpleTab>

## チェンジフィードを複製する {#duplicate-a-changefeed}

1.  ターゲット TiDB クラスターの[**チェンジフィード**](#view-the-changefeed-page)ページに移動します。
2.  複製したい変更フィードを見つけます。 **「アクション」**列で、 **「...」** &gt; **「複製」を**クリックします。
3.  TiDB Cloud は、新しい変更フィード設定に元の設定を自動的に入力します。必要に応じて設定を確認し、変更できます。
4.  設定を確認したら、 **[送信]**をクリックして新しい変更フィードを作成し、開始します。

## 変更フィードを削除する {#delete-a-changefeed}

TiDB CloudコンソールまたはTiDB Cloud CLI を使用して、変更フィードを削除できます。

<SimpleTab>
<div label="Console">

1.  ターゲット TiDB クラスターの[**チェンジフィード**](#view-the-changefeed-page)ページに移動します。
2.  削除する変更フィードを見つけて、 **[アクション]**列の**[...]** &gt; **[削除]**をクリックします。

</div>

<div label="CLI">

次のコマンドを実行します。

```bash
ticloud serverless changefeed delete --cluster-id <cluster-id> --changefeed-id <changefeed-id>
```

</div>
</SimpleTab>

## チェンジフィード課金 {#changefeed-billing}

ベータ フェーズでは、Changefeeds は無料です。

## チェンジフィードの状態 {#changefeed-states}

実行プロセス中に、変更フィードがエラーで失敗したり、手動で一時停止または再開されたりすることがあります。これらの動作により、変更フィードの状態が変化する可能性があります。

各状態は次のように説明されます。

-   `CREATING` : 変更フィードを作成中です。
-   `CREATE_FAILED` : 変更フィードの作成に失敗しました。変更フィードを削除して、新しい変更フィードを作成する必要があります。
-   `RUNNING` : チェンジフィードは正常に実行され、チェックポイント ts は正常に進行します。
-   `PAUSED` : チェンジフィードは一時停止されます。
-   `WARNING` : チェンジフィードは警告を返します。回復可能なエラーのため、チェンジフィードは続行できません。この状態のチェンジフィードは、状態が`RUNNING`に遷移するまで再開を試行し続けます。この状態のチェンジフィードは[GC操作](https://docs.pingcap.com/tidb/stable/garbage-collection-overview)ブロックします。
-   `RUNNING_FAILED` : 変更フィードが失敗しました。何らかのエラーが発生したため、変更フィードを再開できず、自動復旧もできません。増分データのガベージコレクション(GC) 前に問題が解決された場合は、失敗した変更フィードを手動で再開できます。増分データのデフォルトの Time-To-Live (TTL) 期間は 24 時間です。つまり、変更フィードが中断されてから 24 時間以内には、GC メカニズムによってデータが削除されることはありません。
