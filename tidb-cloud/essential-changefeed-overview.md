---
title: Changefeed (Beta)
summary: TiDB Cloud changefeed を使用すると、TiDB Cloudから他のデータサービスにデータをストリーミングできます。
---

# 変更フィード（ベータ版） {#changefeed-beta}

TiDB Cloudのchangefeed機能を使用すると、 TiDB Cloudから他のデータサービスへデータをストリーミングできます。現在、 TiDB CloudはApache KafkaとMySQLへのデータストリーミングをサポートしています。

> **注記：**
>
> -   現在、 TiDB Cloud、 TiDB Cloud Essentialインスタンスごとに最大10個のチェンジフィードしか許可されていません。
> -   [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter)インスタンスでは、変更フィード機能は利用できません。

## 制限 {#restrictions}

-   Changefeeds は、 `RENAME TABLE`のように、単一の`RENAME TABLE t1 TO t3, t2 TO t4` } ステートメントで複数のテーブルの名前を変更する DDL ステートメントをサポートしていません。このステートメントを実行すると、Changefeed のデータレプリケーションが永続的に中断されます。
-   変更フィードのスループットは約20 MiB/秒です。増分データ量がこの制限を超える場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

## 対応地域 {#supported-regions}

変更フィード機能は、以下の地域でご利用いただけます。

| クラウドプロバイダー | 対応地域                                                                                                                                  |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| AWS        | <li>`ap-east-1`</li><li>`ap-northeast-1`</li><li>`ap-southeast-1`</li><li>`eu-central-1`</li><li>`us-east-1`</li><li>`us-west-2`</li> |
| アリババクラウド   | <li>`ap-southeast-1`</li><li>`ap-southeast-5`</li><li>`cn-hongkong`</li>                                                              |

今後、対応地域は拡大していく予定です。特定の地域での緊急サポートについては、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)までお問い合わせください。

## Changefeedページをビュー {#view-the-changefeed-page}

変更フィード機能にアクセスするには、以下の手順に従ってください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

    > **ヒント：**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2.  対象のTiDB Cloud Essentialインスタンスの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**「データ」** &gt; **「変更フィード」**をクリックします。変更フィードページが表示されます。

**変更フィード**ページでは、変更フィードの作成、既存の変更フィードの一覧表示、および既存の変更フィードの操作（変更フィードの一時停止、再開、編集、削除など）を行うことができます。

## 変更フィードを作成する {#create-a-changefeed}

変更フィードを作成するには、チュートリアルを参照してください。

-   [Apache Kafkaへのシンク](/tidb-cloud/essential-changefeed-sink-to-kafka.md)
-   [MySQLにシンクする](/tidb-cloud/essential-changefeed-sink-to-mysql.md)

## 変更フィードをビュー {#view-a-changefeed}

変更フィードは、 TiDB CloudコンソールまたはTiDB Cloud CLIを使用して表示できます。

<SimpleTab>
<div label="Console">

1.  ターゲットのTiDB Cloud Essentialインスタンスの[**変更フィード**](#view-the-changefeed-page)ページに移動します。
2.  表示したい該当する変更フィードを見つけて、 **[アクション]**列の**[...]** &gt; **[ビュー]**をクリックします。
3.  変更フィードの詳細（設定、ステータス、メトリクスなど）を確認できます。

</div>

<div label="CLI">

以下のコマンドを実行してください。

```bash
ticloud serverless changefeed get --cluster-id <cluster-id> --changefeed-id <changefeed-id>
```

</div>
</SimpleTab>

## 変更フィードを一時停止または再開する {#pause-or-resume-a-changefeed}

TiDB CloudコンソールまたはTiDB Cloud CLIを使用して、変更フィードを一時停止または再開できます。

<SimpleTab>
<div label="Console">

1.  ターゲットのTiDB Cloud Essentialインスタンスの[**変更フィード**](#view-the-changefeed-page)ページに移動します。
2.  一時停止または再開したい該当する変更フィードを見つけて、 **[アクション]**列の**[...]** &gt; **[一時停止/再開]**をクリックします。

</div>

<div label="CLI">

変更フィードを一時停止するには、次のコマンドを実行します。

```bash
ticloud serverless changefeed pause --cluster-id <cluster-id> --changefeed-id <changefeed-id>
```

変更フィードを再開するには：

    ticloud serverless changefeed resume -c <cluster-id> --changefeed-id <changefeed-id>

</div>
</SimpleTab>

## 変更フィードを編集する {#edit-a-changefeed}

> **注記：**
>
> TiDB Cloud現在、一時停止状態の変更フィードの編集のみが許可されています。

変更フィードは、 TiDB CloudコンソールまたはTiDB Cloud CLIを使用して編集できます。

<SimpleTab>
<div label="Console">

1.  ターゲットのTiDB Cloud Essentialインスタンスの[**変更フィード**](#view-the-changefeed-page)ページに移動します。

2.  一時停止したい変更フィードを見つけて、 **[アクション]**列の**[...]** &gt; **[一時停止]**をクリックします。

3.  変更フィードのステータスが`Paused`に変更されたら、 **[...]** &gt; **[編集]**をクリックして、対応する変更フィードを編集します。

    TiDB Cloudはデフォルトで変更フィードの設定を自動的に行います。以下の設定を変更できます。

    -   Apache Kafkaシンク：**宛先**、**接続**、**開始位置**を除くすべての設定
    -   MySQLシンク：**宛先**、**接続**、**開始位置**を除くすべての設定

4.  設定を編集した後、 **[...]** &gt; **[再開]**をクリックして、対応する変更フィードを再開します。

</div>

<div label="CLI">

Apache Kafkaシンクを使用して変更フィードを編集する：

```bash
ticloud serverless changefeed edit --cluster-id <cluster-id> --changefeed-id <changefeed-id> --name <new-displayName> --kafka <full-specified-kafka> --filter <full-specified-filter>
```

MySQLシンクを使用して変更フィードを編集する：

```bash
ticloud serverless changefeed edit --cluster-id <cluster-id> --changefeed-id <changefeed-id> --name <new-displayName> --mysql <full-specified-mysql> --filter <full-specified-filter>
```

</div>
</SimpleTab>

## 変更フィードを複製する {#duplicate-a-changefeed}

1.  ターゲットのTiDB Cloud Essentialインスタンスの[**変更フィード**](#view-the-changefeed-page)ページに移動します。
2.  複製したい変更フィードを探します。**アクション**列で、 **...** &gt;**複製を**クリックします。
3.  TiDB Cloudは、新しい変更フィード設定に元の設定を自動的に反映します。必要に応じて設定を確認および変更できます。
4.  設定を確認後、 **「送信」**をクリックして新しい変更フィードを作成して開始します。

## 変更フィードを削除する {#delete-a-changefeed}

TiDB CloudコンソールまたはTiDB Cloud CLIを使用して、変更フィードを削除できます。

<SimpleTab>
<div label="Console">

1.  ターゲットのTiDB Cloud Essentialインスタンスの[**変更フィード**](#view-the-changefeed-page)ページに移動します。
2.  削除したい変更フィードを見つけて、 **[アクション]**列の**[...]** &gt; **[削除]**をクリックします。

</div>

<div label="CLI">

以下のコマンドを実行してください。

```bash
ticloud serverless changefeed delete --cluster-id <cluster-id> --changefeed-id <changefeed-id>
```

</div>
</SimpleTab>

## Changefeedの請求 {#changefeed-billing}

変更フィードはベータ版期間中は無料です。

## Changefeedの状態 {#changefeed-states}

実行プロセス中に、変更フィードはエラーで失敗したり、手動で一時停止または再開されたりする場合があります。これらの動作により、変更フィードの状態が変化する可能性があります。

各州は以下のように説明されます。

-   `CREATING` : 変更フィードが作成されています。
-   `CREATE_FAILED` : 変更フィードの作成に失敗しました。変更フィードを削除して、新しいものを作成する必要があります。
-   `RUNNING` : changefeed は正常に実行され、checkpoint-ts も正常に進行します。
-   `PAUSED` : 変更フィードが一時停止されています。
-   `WARNING` : 変更フィードが警告を返します。回復可能なエラーのため、変更フィードは続行できません。この状態の変更フィードは、状態が`RUNNING`に遷移するまで再開を試み続けます。この状態の変更フィードは[GCオペレーション](https://docs.pingcap.com/tidb/stable/garbage-collection-overview)ブロックします 。
-   `RUNNING_FAILED` : 変更フィードが失敗しました。何らかのエラーにより、変更フィードを再開できず、自動的に復旧することもできません。増分データのガベージコレクション(GC) の前に問題が解決された場合は、失敗した変更フィードを手動で再開できます。増分データのデフォルトの有効期限 (TTL) は 24 時間です。つまり、変更フィードが中断されてから 24 時間以内に GC メカニズムによってデータが削除されることはありません。
