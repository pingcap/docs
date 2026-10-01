---
title: データをストリーミングする
summary: Changefeed や Data Pipeline を含む、TiDB Cloud からダウンストリームシステムへデータ変更をストリーミングするためのオプションについて説明します。
---

# データをストリーミングする

TiDB Cloud は、TiDB Cloud インスタンスからダウンストリームシステムへデータ変更を継続的にストリーミングできます。データをストリーミングするために、次のオプションを提供しています。

- **Changefeed**: Apache Kafka、MySQL、TiDB Cloud、クラウドストレージなどのダウンストリームシステムに増分の行変更をストリーミングします。
- **Data Pipeline**: 選択したデータの完全なスナップショットをエクスポートし、その後、行変更を TiDB Cloud Lake に継続的にレプリケートします。

## Changefeed {#changefeed}

changefeed は、TiDB Cloud からダウンストリームシステムへ増分データ変更をストリーミングします。増分変更のみを継続的にレプリケートする必要があり、かつダウンストリームシステムが増分イベントを処理できる場合に使用します。

TiDB Cloud コンソールの **Changefeed** ページで changefeed を作成および管理できます。詳細は、[変更フィード](/tidb-cloud/changefeed-overview.md) を参照してください。

## Data Pipeline (PREVIEW) {#data-pipeline-preview}

Data Pipeline は、TiDB Cloud インスタンスから TiDB Cloud Lake に完全なデータと増分変更をレプリケートします。Amazon S3 や Alibaba Cloud OSS などの外部 stage を使用してソースと宛先の間でデータをバッファリングするため、信頼性が向上し、コストとレイテンシーを制御できます。詳細は、[Data Pipeline](/tidb-cloud/data-pipeline.md) を参照してください。

> **Note:**
>
> TiDB Cloud コンソールの Data Pipeline 機能は現在プライベートプレビュー中で、リクエストに応じて利用できます。この機能をリクエストするには、[TiDB Cloud コンソール](https://tidbcloud.com) の右下にある **?** をクリックし、**Support Tickets** をクリックして [ヘルプセンター](https://tidb.support.pingcap.com/servicedesk/customer/portals) に移動します。チケットを作成し、**Description** フィールドに "Apply for `Data Pipeline to TiDB Cloud Lake`" と入力して、**Submit** をクリックします。
